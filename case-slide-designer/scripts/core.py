"""Drawing toolkit on top of python-pptx. All geometry in inches, 13.333 x 7.5 slide."""
import os, re, sys
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn
from lxml import etree
from PIL import ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import theme, icons

W, H = 13.333, 7.5
# Frame and grid = case-study-ppt section 5 (that skill's values win)
MX = 0.182                    # side margin = accent bar width; title, subtitle and source start here
CX0, CX1 = MX, 13.15          # content x range
CY0, CY1 = 1.30, 6.95         # content y range (the source line, when present, takes the bottom 0.25 in)
SOURCE_Y = 6.70               # source line (one line, 10-12pt), above the tracker and the appendix footer
FONT_DIRS = ["/usr/share/fonts/truetype/google-fonts", "/usr/share/fonts/opentype/inter",
             "/usr/share/fonts/truetype", "/usr/share/fonts"]


def rgb(h):
    return RGBColor.from_string(h.lstrip("#").upper())


def _font_path(fname):
    for d in FONT_DIRS:
        for root, _, files in os.walk(d):
            if fname in files:
                return os.path.join(root, fname)
    return None


# Size floors (case-study-ppt section 4a). Everything not named here is body text: 16pt minimum.
# Only the source line and the slide number go below 14pt (10-12pt); legends and footnotes are 14pt like chart labels.
ROLE_FLOORS = {"tracker": 14, "axis-label": 14, "chart-label": 14, "legend": 14, "footnote": 14,
               "source": 10, "page-number": 10}
BODY_MIN = 16


def role_floor(name):
    for role, pt in ROLE_FLOORS.items():
        if name and name.startswith(role):
            return pt
    return BODY_MIN


class Deck:
    def __init__(self, primary=theme.DEFAULT_PRIMARY, font_profile="premium", logo=None, template=None):
        self.prs = Presentation(template) if template else Presentation()   # template: optional .pptx/.potx master
        self.prs.slide_width, self.prs.slide_height = Inches(W), Inches(H)
        self.pal = theme.make_palette(primary)
        if isinstance(font_profile, dict):      # {"head": "...", "body": "..."}: custom names, measured with Poppins/Inter
            self.fonts = dict(theme.FONTS["premium"], **font_profile)
        else:
            self.fonts = theme.FONTS[font_profile]
        self.logo = logo
        self.warnings = []
        self._fcache = {}
        self.n = 0

    # ---------- slides ----------
    def new_slide(self, bg=None):
        layout = self.prs.slide_layouts[6]
        s = self.prs.slides.add_slide(layout)
        for ph in list(s.placeholders):
            ph._element.getparent().remove(ph._element)
        self.n += 1
        s._deck_n = self.n
        if bg:
            f = s.background.fill
            f.solid(); f.fore_color.rgb = rgb(self.pal.get(bg, bg))
        return s

    def warn(self, msg):
        self.warnings.append(f"slide {self.n}: {msg}")

    # ---------- text measurement ----------
    def _pil(self, bold, head, size):
        key = (bold, head, size)
        if key not in self._fcache:
            f = self.fonts
            fn = f["head_file"] if head else (f["body_bold_file"] if bold else f["body_file"])
            p = _font_path(fn) or _font_path("DejaVuSans.ttf")
            self._fcache[key] = ImageFont.truetype(p, int(size * 10))   # 10px per pt for precision
        return self._fcache[key]

    def text_width(self, text, size, bold=False, head=False):
        return self._pil(bold, head, size).getlength(text) / 10 / 72   # inches

    def wrap(self, text, size, width, bold=False, head=False):
        lines = []
        for para in text.split("\n"):
            words, cur = para.split(" "), ""
            for w in words:
                t = (cur + " " + w).strip()
                if self.text_width(t, size, bold, head) <= width or not cur:
                    cur = t
                else:
                    lines.append(cur); cur = w
            lines.append(cur)
        return lines

    def fit(self, text, w, h, max_pt, min_pt, bold=False, head=False, spacing=1.18, step=1):
        """Largest size in [min_pt, max_pt] whose wrapped height fits; second value = fits?"""
        plain = re.sub(r"\*\*", "", text)
        size = max_pt
        while size >= min_pt:
            ls = self.wrap(plain, size, w, bold, head)
            widest = max(self.text_width(l, size, bold, head) for l in ls)
            if len(ls) * size * spacing / 72 <= h and widest <= w + 0.01:
                return size, True
            size -= step
        return min_pt, False

    # ---------- primitives ----------
    def shape(self, s, kind, x, y, w, h, fill=None, line=None, lw=1.0, dash=False, radius=None, name=None):
        shp = s.shapes.add_shape(kind, Inches(x), Inches(y), Inches(w), Inches(h))
        self._nostyle(shp)
        if fill:
            shp.fill.solid(); shp.fill.fore_color.rgb = rgb(self.pal.get(fill, fill))
        else:
            shp.fill.background()
        if line:
            shp.line.color.rgb = rgb(self.pal.get(line, line)); shp.line.width = Pt(lw)
            if dash:
                from pptx.enum.dml import MSO_LINE
                shp.line.dash_style = MSO_LINE.DASH
        else:
            shp.line.fill.background()
        if radius is not None and kind == MSO_SHAPE.ROUNDED_RECTANGLE:
            shp.adjustments[0] = min(0.5, radius / min(w, h))
        if name:
            shp.name = name
        return shp

    @staticmethod
    def _nostyle(shp):
        st = shp._element.find(qn("p:style"))
        if st is not None:
            shp._element.remove(st)

    def rect(self, s, x, y, w, h, fill=None, line=None, lw=1.0, dash=False, radius=None, name=None):
        kind = MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE
        return self.shape(s, kind, x, y, w, h, fill, line, lw, dash, radius, name)

    def oval(self, s, x, y, w, h, fill=None, line=None, lw=1.0, name=None):
        return self.shape(s, MSO_SHAPE.OVAL, x, y, w, h, fill, line, lw, name=name)

    def line(self, s, x1, y1, x2, y2, color="LINE", lw=1.0, dash=False, arrow=False):
        c = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
        self._nostyle(c)
        c.line.color.rgb = rgb(self.pal.get(color, color)); c.line.width = Pt(lw)
        ln = c.line._get_or_add_ln()
        if dash:
            from pptx.enum.dml import MSO_LINE
            c.line.dash_style = MSO_LINE.DASH
        if arrow:
            tail = etree.SubElement(ln, qn("a:tailEnd")); tail.set("type", "triangle"); tail.set("w", "med"); tail.set("len", "med")
        return c

    def picture(self, s, path, x, y, w=None, h=None, name=None):
        pic = s.shapes.add_picture(path, Inches(x), Inches(y), Inches(w) if w else None, Inches(h) if h else None)
        if name:
            pic.name = name
        return pic

    def icon(self, s, name, x, y, size, color="PRIMARY", opacity=1.0, stroke=1.75):
        nm = icons.resolve(name)
        path = icons.render(nm, self.pal.get(color, color), stroke=stroke, opacity=opacity)
        pic = self.picture(s, path, x, y, size, size, name=f"icon:{nm}")
        pic._element.nvPicPr.cNvPr.set("descr", nm.replace("-", " "))
        return pic

    def icon_badge(self, s, name, cx, cy, d, fill="PRIMARY", icon_color=None, ratio=0.52):
        """Round badge with a centred icon; cx, cy = centre."""
        icon_color = icon_color or (self.pal["ON_PRIMARY"] if fill == "PRIMARY" else "PRIMARY")
        self.oval(s, cx - d / 2, cy - d / 2, d, d, fill=fill)
        isz = d * ratio
        self.icon(s, name, cx - isz / 2, cy - isz / 2, isz, color=icon_color)

    # ---------- text ----------
    def text(self, s, x, y, w, h, text, size=16, color="INK", bold=False, italic=False, align="l", valign="t",
             head=False, min_size=None, spacing=1.0, bullets=False, bullet_color="PRIMARY", margin=0.0,
             name=None, space_after=0, upper=False, autofit=True):
        """Text box with **bold** markup. If min_size is set, shrinks (measured, never autofit) to fit.
        Lists of strings become paragraphs (bullets=True adds bullet characters)."""
        floor = role_floor(name)
        size = max(size, floor)
        if min_size is not None:
            min_size = max(min_size, floor)
        paras = text if isinstance(text, list) else [text]
        if upper:
            paras = [p.upper() for p in paras]
        my = min(margin, 0.05)
        iw, ih = w - 2 * margin, h - 2 * my
        eff = size
        if min_size is not None and autofit:
            joined = "\n".join(paras)
            bw = iw - (0.22 * size / 16 if bullets else 0)
            eff, ok = self.fit(joined, bw, ih - len(paras) * space_after / 72, size, min_size, bold, head, 1.2 * spacing)
            if not ok:
                self.warn(f"text overflows even at {min_size}pt: '{paras[0][:40]}...'")
        tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        if name:
            tb.name = name
        tf = tb.text_frame
        tf.word_wrap = True
        tf.auto_size = None
        tf.margin_left = tf.margin_right = Inches(margin)
        tf.margin_top = tf.margin_bottom = Inches(my)
        tf.vertical_anchor = {"t": MSO_ANCHOR.TOP, "m": MSO_ANCHOR.MIDDLE, "b": MSO_ANCHOR.BOTTOM}[valign]
        bp = tf._txBody.find(qn("a:bodyPr"))
        for ch in list(bp):
            bp.remove(ch)
        etree.SubElement(bp, qn("a:noAutofit"))
        for i, ptxt in enumerate(paras):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.alignment = {"l": PP_ALIGN.LEFT, "c": PP_ALIGN.CENTER, "r": PP_ALIGN.RIGHT}[align]
            p.line_spacing = spacing
            if space_after and i < len(paras) - 1:
                p.space_after = Pt(space_after)
            if bullets:
                self._bullet(p, eff, bullet_color)
            for j, part in enumerate(re.split(r"(\*\*.+?\*\*)", ptxt)):
                if not part:
                    continue
                b = part.startswith("**") and part.endswith("**")
                r = p.add_run(); r.text = part[2:-2] if b else part
                f = r.font
                f.name = self.fonts["head"] if head else self.fonts["body"]
                f.size = Pt(eff); f.bold = bool(bold or b); f.italic = italic
                f.color.rgb = rgb(self.pal.get(color, color))
        return tb

    def _bullet(self, p, size, color):
        pPr = p._p.get_or_add_pPr()
        ind = int(Inches(0.22 * max(size, 12) / 16))
        pPr.set("marL", str(ind)); pPr.set("indent", str(-ind))
        for tag in ("a:buClr", "a:buFont", "a:buChar"):
            for e in pPr.findall(qn(tag)):
                pPr.remove(e)
        bc = etree.SubElement(pPr, qn("a:buClr")); sc = etree.SubElement(bc, qn("a:srgbClr")); sc.set("val", self.pal.get(color, color))
        bf = etree.SubElement(pPr, qn("a:buFont")); bf.set("typeface", "Arial")
        ch = etree.SubElement(pPr, qn("a:buChar")); ch.set("char", "•")

    def box_text(self, s, shp, text, size=16, color="INK", bold=False, align="c", valign="m", margin=0.12, **kw):
        """Text laid over an existing shape (separate textbox so fitting is measured)."""
        x, y = shp.left / 914400, shp.top / 914400
        w, h = shp.width / 914400, shp.height / 914400
        return self.text(s, x, y, w, h, text, size=size, color=color, bold=bold, align=align, valign=valign, margin=margin, **kw)

    # ---------- composite pieces ----------
    def harvey(self, s, cx, cy, d, level, color="PRIMARY"):
        """level 0..4 quarters. Outline circle + pie wedge."""
        x, y = cx - d / 2, cy - d / 2
        self.oval(s, x, y, d, d, fill="WHITE", line=color, lw=1.5)
        if level >= 4:
            self.oval(s, x, y, d, d, fill=color, line=color, lw=1.5)
        elif level > 0:
            pie = self.shape(s, MSO_SHAPE.PIE, x, y, d, d, fill=color, line=None)
            end = {1: 0, 2: 90, 3: 180}[level]
            pie.adjustments[0] = 270 * 0.6
            pie.adjustments[1] = end * 0.6

    def frame(self, s, title, kicker=None, source=None, tracker=None, active=None, dark=False, logo=True, subtitle=None):
        """Content-slide frame = case-study-ppt section 5: PRIMARY accent bar flush left (x 0, y 0.214, w 0.182,
        h 0.981), action title 24pt on one line (about 60 characters) at x 0.182, y 0.214, optional 20pt subtitle at
        y 0.757, logo top right (x ~11.32, h ~0.84), source line, slide number bottom right, phase tracker.
        The old `kicker` key is shown as the subtitle (the COBE style has no small kicker line)."""
        tcol = "WHITE" if dark else "INK"
        tw = 11.0 if (logo and self.logo) else CX1 - MX
        sub_txt = subtitle or kicker
        nlines = 1; size = 24
        if len(self.wrap(title, 24, tw, head=True)) > 1 or len(title) > 60:
            self.warn(f"title over one line / 60 chars ({len(title)}): shorten it rather than shrink it")
            nlines = 2
            for sz in range(24, 19, -1):
                if len(self.wrap(title, sz, tw, head=True)) <= 2:
                    size = sz; break
        ty = 0.214
        th = max(0.51, nlines * size * 1.2 / 72)
        sy = ty + th + 0.033 if nlines > 1 else 0.757
        self.rect(s, 0, ty, 0.182, max(0.981, (sy + 0.41 - ty) if sub_txt else th), fill="PRIMARY" if not dark else "WHITE", name="accent-bar")
        self.text(s, MX, ty, tw, th, title, size=size, color=tcol, head=True, valign="t", name="title", spacing=1.0, margin=0.1)
        if sub_txt:
            self.text(s, MX, sy, tw, 0.41, sub_txt, size=20, color=tcol, name="subtitle", margin=0.1)
        if logo and self.logo:
            self._place_logo(s)
        if source:
            self.text(s, MX, SOURCE_Y, 11.0, 0.25, "Source: " + source if not source.lower().startswith("source") else source,
                      size=10, color="GREY" if not dark else "MID", name="source", margin=0.1)
        self.page_number(s)
        if tracker:
            self.tracker(s, tracker, active)

    def page_number(self, s, color="GREY"):
        self.text(s, 12.56, 7.08, 0.6, 0.25, str(s._deck_n), size=10, color=color, align="r", name="page-number")

    def _place_logo(self, s):
        from PIL import Image
        iw, ih = Image.open(self.logo).size
        maxw, maxh = CX1 - 11.32, 0.84
        sc = min(maxw / iw, maxh / ih)
        w, h = iw * sc, ih * sc
        self.picture(s, self.logo, CX1 - w, 0.214 + (maxh - h) / 2, w, h, name="logo")

    def tracker(self, s, labels, active):
        """case-study-ppt section 5: 3pt NEUTRAL_DARK base line x 2.667-10.667 at y 7.108, split into equal segments
        (four labels: 2.0 in each); active segment 4.5pt PRIMARY_DARK and its label bold PRIMARY_DARK; others regular, dark."""
        n = len(labels); x0, total = 2.667, 8.0; seg = total / n
        self.line(s, x0, 7.108, x0 + total, 7.108, color="NEUTRAL_DARK", lw=3)
        for i, lab in enumerate(labels):
            on = (i == active)
            if on:
                self.line(s, x0 + i * seg, 7.108, x0 + (i + 1) * seg, 7.108, color="PRIMARY_DARK", lw=4.5)
            self.text(s, x0 + i * seg, 7.128, seg, 0.34, lab, size=14, color="PRIMARY_DARK" if on else "INK", bold=on, align="c", name="tracker")

    def takeaway(self, s, text, y=6.25, h=0.62, icon="lightbulb"):
        """Primary-filled one-line takeaway banner across the content width."""
        r = self.rect(s, CX0, y, CX1 - CX0, h, fill="PRIMARY", radius=0.08, name="takeaway")
        on = self.pal["ON_PRIMARY"]
        self.icon(s, icon, CX0 + 0.22, y + (h - 0.36) / 2, 0.36, color=on)
        self.text(s, CX0 + 0.8, y, CX1 - CX0 - 1.0, h, text, size=18, color=on, bold=True, valign="m", min_size=16, name="takeaway-text")

    def save(self, path):
        self.prs.save(path)
        return path
