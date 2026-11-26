#!/usr/bin/env python3
"""Deck-native mode: build a redesigned slide INSIDE the user's own deck, so it shares the deck's
master, layout, accent bar, logo, title styles, tracker and slide-number field.

    python deck_native.py scan deck.pptx            # colours, fonts, layouts, trackers, icon style hints

Library use (see SKILL.md "Deck-native mode" for the full recipe):

    from deck_native import HostSlide
    h = HostSlide("deck.pptx", layout_from=14)             # reuse slide 14's layout (accent bar, logo...)
    h.set_titles("US expansion: four growth regions",       # keep the user's title lines verbatim
                 "Grow where we are under-represented and commuter traffic is heavy")
    h.copy_tracker(from_slide=12, active="Recommendation")  # exact copy of the deck's own tracker
    h.copy_slide_number(from_slide=12)                      # keeps the automatic page-number field
    h.box(...); h.text(...); h.num_badge(...); h.line_icon(...); h.chevron(...)
    h.save_single("out.pptx")                               # one-slide file that shares the master

All measurements are inches. Colours are hex strings without '#'.
"""
import sys, os, re, copy, collections
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_SHAPE_TYPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
E = 914400
TRACKER_WORDS = {"analysis", "strategy", "recommendation", "feasibility", "implementation", "impact", "appendix",
                 "appendi", "executive", "financials", "risks", "situation", "solution", "next steps", "evaluate",
                 "advocate", "impacts", "insights"}
EXTRA_TRACKER_WORDS = set()   # pillar names used as tracker labels; filled by HostSlide(tracker_labels=[...])


def rgb(h):
    return RGBColor.from_string(h.lstrip("#").upper())


# ------------------------------------------------------------------ scanning the host deck
def _runs(slide):
    for sh in slide.shapes:
        if sh.has_text_frame:
            for p in sh.text_frame.paragraphs:
                for r in p.runs:
                    yield sh, r


def tracker_shapes(slide, prs):
    """Shapes in the bottom band that form the section tracker (lines + label boxes).
    Excludes the slide-number placeholder."""
    H = prs.slide_height
    out = []
    for sh in slide.shapes:
        if sh.top is None or sh.top < 0.86 * H:
            continue
        if sh.is_placeholder and sh.placeholder_format.type is not None and "SLIDE_NUMBER" in str(sh.placeholder_format.type):
            continue
        if sh.shape_type == MSO_SHAPE_TYPE.LINE or getattr(sh, "shape_type", None) == MSO_SHAPE_TYPE.LINE:
            out.append(sh)
        elif sh.has_text_frame and sh.text_frame.text.strip().lower() in (TRACKER_WORDS | EXTRA_TRACKER_WORDS):
            out.append(sh)
        elif sh._element.tag.endswith("cxnSp"):
            out.append(sh)
    return out


def _is_active_run(r):
    """A tracker label counts as active when it is bold (run or list style) or coloured (not black)."""
    f = r.font
    if f.bold:
        return True
    if f.bold is None:
        txb = r._r.getparent().getparent()
        for d in txb.iter(qn("a:defRPr")):
            if d.get("b") == "1":
                return True
    sf = r._r.find(qn("a:rPr"))
    if sf is not None:
        fill = sf.find(qn("a:solidFill"))
        if fill is not None:
            c = fill[0]
            if c.tag == qn("a:srgbClr") and c.get("val", "").upper() not in ("000000", "0A0A0A", "1A1A1A", "262626"):
                return True
            if c.tag == qn("a:schemeClr") and c.get("val") not in ("tx1", "dk1"):
                return True
    return False


def scan(path):
    prs = Presentation(path)
    cols, fonts, lays = collections.Counter(), collections.Counter(), collections.Counter()
    print(f"slide size: {prs.slide_width / E:.3f} x {prs.slide_height / E:.3f} in, {len(prs.slides)} slides\n")
    for i, s in enumerate(prs.slides, 1):
        x = s._element.xml
        cols.update(re.findall(r'srgbClr val="([0-9A-Fa-f]{6})"', x))
        fonts.update(re.findall(r'latin typeface="([^"+][^"]*)"', x))
        lays[s.slide_layout.name] += 1
        title = s.shapes.title.text_frame.text if s.shapes.title is not None and s.shapes.title.has_text_frame else ""
        if not title:   # many decks use plain text boxes as titles: take the top-most text
            tops = sorted((sh for sh in s.shapes if sh.has_text_frame and sh.text_frame.text.strip() and sh.top is not None),
                          key=lambda sh: (sh.top, sh.left))
            title = tops[0].text_frame.text.split("\n")[0] if tops else ""
        tr = tracker_shapes(s, prs)
        labs = sorted([t for t in tr if t.has_text_frame], key=lambda t: t.left)
        lab_txt = []
        for t in labs:
            act = any(_is_active_run(r) for p in t.text_frame.paragraphs for r in p.runs)
            lab_txt.append(("*" if act else "") + t.text_frame.text.strip())
        pics = sum(1 for sh in s.shapes if sh.shape_type == MSO_SHAPE_TYPE.PICTURE)
        if not lab_txt:
            lt = [sh.text_frame.text.strip() for sh in s.slide_layout.shapes if sh.has_text_frame
                  and sh.top is not None and sh.top > 0.86 * prs.slide_height and sh.text_frame.text.strip().lower() in (TRACKER_WORDS | EXTRA_TRACKER_WORDS)]
            if lt: lab_txt = ["(in layout) " + " | ".join(lt)]
        print(f"{i:3}. [{s.slide_layout.name[:18]:18}] {title[:45]:45} tracker: {' | '.join(lab_txt) or '-'}  pics:{pics}")
    print("\nlayouts:", dict(lays))
    print("colours (count):", ", ".join(f"{c.upper()}x{n}" for c, n in cols.most_common(14)))
    print("fonts (count):", ", ".join(f"{f}x{n}" for f, n in fonts.most_common(6)))
    print("\nActive tracker label is marked with *. Pick a slide whose tracker labels are correct as the copy source.")


# ------------------------------------------------------------------ the host slide
class HostSlide:
    def __init__(self, path, layout_from=None, layout_name=None, font="Avenir Next LT Pro", tracker_labels=None):
        """tracker_labels: pass the deck's labels when its tracker uses pillar names, so they are found and copied."""
        EXTRA_TRACKER_WORDS.update(l.strip().lower() for l in (tracker_labels or []))
        self.prs = Presentation(path)
        self.W, self.H = self.prs.slide_width / E, self.prs.slide_height / E
        if layout_from:
            layout = self.prs.slides[layout_from - 1].slide_layout
        else:
            layout = next(l for l in self.prs.slide_layouts if l.name == layout_name)
        self.s = self.prs.slides.add_slide(layout)
        self.font = font

    # ---- frame
    def set_titles(self, title, subtitle=None):
        """Fill the layout's title and subtitle placeholders; drop empty or off-slide placeholders."""
        sub_done = False
        for ph in list(self.s.placeholders):
            idx = ph.placeholder_format.idx
            if idx == 0:
                ph.text_frame.text = title
            elif subtitle and not sub_done and ph.left is not None and ph.left / E < self.W and ph.top / E < 1.4:
                ph.text_frame.text = subtitle; sub_done = True
            else:
                ph._element.getparent().remove(ph._element)
        if subtitle and not sub_done:
            print("warning: layout has no subtitle placeholder; add the subtitle as a text box styled like other slides")

    def copy_shape(self, from_slide, name):
        src = self.prs.slides[from_slide - 1]
        for sh in src.shapes:
            if sh.name == name:
                el = copy.deepcopy(sh._element)
                self.s.shapes._spTree.append(el)
                return el
        raise KeyError(f"no shape named {name!r} on slide {from_slide}")

    def copy_slide_number(self, from_slide):
        src = self.prs.slides[from_slide - 1]
        for sh in src.shapes:
            if sh.is_placeholder and "SLIDE_NUMBER" in str(sh.placeholder_format.type):
                self.s.shapes._spTree.append(copy.deepcopy(sh._element))
                return
        print("warning: no slide-number placeholder on slide", from_slide)

    def copy_tracker(self, from_slide, active=None, labels=None):
        """Deep-copy the tracker of `from_slide`. `labels` (left->right) rewrites label texts (fix typos);
        `active` (label text or index) moves the highlight segment and swaps the active/inactive text styles."""
        src = self.prs.slides[from_slide - 1]
        els = [copy.deepcopy(sh._element) for sh in tracker_shapes(src, self.prs)]
        for el in els:
            self.s.shapes._spTree.append(el)
        new = [sh for sh in self.s.shapes if any(sh._element is el for el in els)]
        labs = sorted([sh for sh in new if sh.has_text_frame], key=lambda t: t.left)
        lines = [sh for sh in new if not sh.has_text_frame]
        if labels:
            for t, txt in zip(labs, labels):
                runs = [r for p in t.text_frame.paragraphs for r in p.runs]
                if runs:
                    runs[0].text = txt
                    for r in runs[1:]: r.text = ""
        if active is None or not labs:
            return labs
        tgt = active if isinstance(active, int) else next(
            i for i, t in enumerate(labs) if t.text_frame.text.strip().lower() == str(active).lower())
        cur = next((i for i, t in enumerate(labs) if any(_is_active_run(r) for p in t.text_frame.paragraphs for r in p.runs)), None)
        if cur is not None and cur != tgt:
            def rpr(t):
                r = [r for p in t.text_frame.paragraphs for r in p.runs][0]
                return r._r.find(qn("a:rPr"))
            a, b = rpr(labs[cur]), rpr(labs[tgt])
            a_copy, b_copy = copy.deepcopy(a), copy.deepcopy(b)
            for t, newpr in ((labs[cur], b_copy), (labs[tgt], a_copy)):
                for p in t.text_frame.paragraphs:
                    for r in p.runs:
                        old = r._r.find(qn("a:rPr"))
                        if old is not None: r._r.remove(old)
                        r._r.insert(0, copy.deepcopy(newpr))
                # also neutralise list-style defaults that force bold (some decks set b=1 in lstStyle)
                for d in t.text_frame._txBody.iter(qn("a:defRPr")):
                    if t is labs[cur]: d.set("b", "0")
        if len(lines) >= 2:
            lines.sort(key=lambda l: l.width)
            hi = lines[0]                     # the short, thick highlight segment
            hi.left = labs[tgt].left; hi.width = labs[tgt].width
        return labs

    # ---- drawing primitives in the host deck's style
    def box(self, x, y, w, h, fill=None, line=None, lw=1.0, kind=MSO_SHAPE.RECTANGLE, radius=None, dash=False, name=None):
        sh = self.s.shapes.add_shape(kind, Inches(x), Inches(y), Inches(w), Inches(h))
        if name: sh.name = name
        if fill: sh.fill.solid(); sh.fill.fore_color.rgb = rgb(fill)
        else: sh.fill.background()
        if line:
            sh.line.color.rgb = rgb(line); sh.line.width = Pt(lw)
            if dash: sh.line.dash_style = 7   # dash
        else: sh.line.fill.background()
        if radius is not None and kind == MSO_SHAPE.ROUNDED_RECTANGLE:
            sh.adjustments[0] = radius
        sh.shadow.inherit = False
        return sh

    def text(self, x, y, w, h, paras, size=16, color="000000", bold=False, italic=False, align="l", valign="t",
             spacing=1.0, name=None, font=None):
        """Text box; `**bold**` markup; a list makes several paragraphs. Body text never goes below 16pt
        (case-study-ppt 4a); name a box tracker/axis-label/chart-label (14pt) or source/footnote (10pt) to go lower."""
        from core import role_floor
        size = max(size, role_floor(name))
        tb = self.s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        if name: tb.name = name
        tf = tb.text_frame; tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        tf.vertical_anchor = {"t": MSO_ANCHOR.TOP, "m": MSO_ANCHOR.MIDDLE, "b": MSO_ANCHOR.BOTTOM}[valign]
        paras = paras if isinstance(paras, list) else [paras]
        for i, ptxt in enumerate(paras):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.alignment = {"l": PP_ALIGN.LEFT, "c": PP_ALIGN.CENTER, "r": PP_ALIGN.RIGHT}[align]
            p.line_spacing = spacing
            for part in re.split(r"(\*\*.+?\*\*)", ptxt):
                if not part: continue
                b = part.startswith("**")
                r = p.add_run(); r.text = part[2:-2] if b else part
                f = r.font; f.name = font or self.font; f.size = Pt(size); f.bold = bold or b; f.italic = italic
                f.color.rgb = rgb(color)
        return tb

    def num_badge(self, cx, cy, d, n, color, size=16, filled=False):
        """Numbered circle. Outline style (white fill, coloured ring + number) or filled."""
        o = self.box(cx - d / 2, cy - d / 2, d, d, fill=color if filled else "FFFFFF", line=color, lw=2.0, kind=MSO_SHAPE.OVAL)
        tf = o.text_frame; tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
        r = p.add_run(); r.text = str(n); r.font.name = self.font; r.font.size = Pt(size); r.font.bold = True
        r.font.color.rgb = rgb("FFFFFF" if filled else color)
        return o

    def line_icon(self, name, cx, cy, d, color, ring=True, ring_color=None, ring_fill="FFFFFF", stroke=1.5):
        """Bundled line icon, optionally inside an outline circle (the common case-deck look)."""
        import icons
        if ring:
            self.box(cx - d / 2, cy - d / 2, d, d, fill=ring_fill, line=ring_color or color, lw=1.75, kind=MSO_SHAPE.OVAL)
        isz = d * (0.56 if ring else 1.0)
        png = icons.render(name, color, stroke=stroke)
        return self.s.shapes.add_picture(png, Inches(cx - isz / 2), Inches(cy - isz / 2), Inches(isz), Inches(isz))

    def chevron(self, x, y, color, w=0.26, h=0.34):
        return self.box(x, y, w, h, fill=color, kind=MSO_SHAPE.CHEVRON)

    def connector(self, x1, y1, x2, y2, color, lw=1.0, dash=True):
        ln = self.s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
        ln.line.color.rgb = rgb(color); ln.line.width = Pt(lw)
        if dash: ln.line.dash_style = 4
        return ln

    # ---- output
    def save_single(self, out):
        """Keep only the new slide (unreferenced parts are dropped on save)."""
        lst = self.prs.slides._sldIdLst
        for sid in list(lst)[:-1]:
            self.prs.part.drop_rel(sid.get(qn("r:id")))
            lst.remove(sid)
        self.prs.save(out)
        return out


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "scan":
        # optional: --labels "Pillar A,Pillar B" for decks whose tracker uses pillar names
        if "--labels" in sys.argv:
            EXTRA_TRACKER_WORDS.update(x.strip().lower() for x in sys.argv[sys.argv.index("--labels") + 1].split(","))
        scan(sys.argv[2])
    else:
        print(__doc__)
