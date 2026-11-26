#!/usr/bin/env python3
"""Mechanical QA for a built deck. Run before delivering; fix everything it reports.

    python check_deck.py deck.pptx [--fonts premium|safe|"Head,Body"] [--primary HEX] [--accent none|HEX] [--no-slop]

Checks: shapes outside the slide, text below the size floor (text boxes, groups and table cells), estimated text
overflow, fonts outside the house pair, empty placeholders, speaker notes, pictures without alt text.
Then runs the slide slop detector (slop_check.py, P0-P3): P0 findings count as issues; clear P1 too before
delivering; judge P2-P3 on the rendered slide. Pass --primary (and --accent) from the Style line.
The word count per slide is printed as a note only: a guide for a clean look, never a problem to clear.
Same limits as case-study-ppt sections 3 and 4a and the auditor's audit_pptx.py (whose title, appendix and
Sources detection is reused when case-study-auditor is installed next to this skill):
  main slides 16pt body, 40 words (60 on a slide carrying "We recommend": executive summary and closing slide);
  appendix slides 14pt, no word limit; title slide no word limit; Sources slide, source line and slide number 10pt;
  tracker, chart and axis labels, legends and footnotes 14pt; title and footer band not counted as body words.
"""
import argparse, os, sys, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pptx import Presentation
from pptx.util import Emu
from core import Deck, role_floor

try:  # reuse the auditor's detection so both scripts judge a slide the same way
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "case-study-auditor", "scripts"))
    from audit_pptx import find_title, has_appendix_footer, APPENDIX_TITLE, SOURCES_TITLE, FOOTER_ZONE_IN
except Exception:  # auditor not installed: verbatim copy of its detection (audit_pptx.py)
    FOOTER_ZONE_IN = 0.55
    EMU_IN = 914400
    TITLE_ZONE_IN = 1.6
    TITLE_TOP_IN = 1.0
    APPX_PREFIX = r"(?:A(?:-[A-Z]{1,4})?\d+\s*[–—:.-]?\s*)?"
    SOURCES_TITLE = re.compile(
        r"^\s*" + APPX_PREFIX
        + r"(sources?(\s+used)?|references?|bibliography|works\s+cited)"
        + r"(\s*(&|and)\s*(sources?|references?|citations?))?\s*$", re.I)
    APPENDIX_TITLE = re.compile(
        r"^\s*((?-i:A\d+\b|A-[A-Z]{1,4}\d+\b)|Appendix\b|Backup\s*(?:[–—:.-]|$))", re.I)
    def max_font(tf):
        sizes = [r.font.size.pt for p in tf.paragraphs for r in p.runs if r.font.size is not None]
        psz = [p.font.size.pt for p in tf.paragraphs if p.font.size is not None]
        return max(sizes + psz) if (sizes or psz) else None


    def find_title(slide):
        """Same rule as audit_pptx.py: placeholder, a shape named "title", the largest text starting in the
        top inch, else the largest text in the wider top zone."""
        if slide.shapes.title is not None and slide.shapes.title.text_frame.text.strip():
            return slide.shapes.title
        for sh in slide.shapes:
            if (sh.has_text_frame and sh.text_frame.text.strip()
                    and (sh.name or "").lower() in ("title", "slide-title", "action-title")):
                return sh
        for zone in (TITLE_TOP_IN, TITLE_ZONE_IN):
            best, best_key = None, None
            for sh in slide.shapes:
                if not sh.has_text_frame or not sh.text_frame.text.strip():
                    continue
                if sh.top is None or sh.top / EMU_IN > zone:
                    continue
                mf = max_font(sh.text_frame) or 0
                if mf < 20:  # labels like "COBE Individual Case" are not titles
                    continue
                key = (mf, -sh.top)
                if best_key is None or key > best_key:
                    best, best_key = sh, key
            if best is not None:
                return best
        return None


    APPENDIX_FOOTER = re.compile(r"^\s*(appendi(x|ces)?|backup)\s*$", re.I)   # also catches the "Appendi" typo


    def _walk(shapes):
        for sh in shapes:
            if sh.shape_type == 6:
                yield from _walk(sh.shapes)
            else:
                yield sh


    def has_appendix_footer(slide, slide_h_emu):
        """An "Appendix" / "Backup" label in the bottom band of the slide OR its layout marks a backup slide."""
        for shapes in (slide.shapes, slide.slide_layout.shapes):
            for sh in _walk(shapes):
                if (sh.has_text_frame and sh.top is not None and sh.top > 0.85 * slide_h_emu
                        and APPENDIX_FOOTER.match(sh.text_frame.text)):
                    return True
        return False


    def sources_title_box(slide):
        """A top-zone text box whose whole text is a Sources title, whatever its font size (often inherited)."""
        for sh in _walk(slide.shapes):
            if (sh.has_text_frame and sh.top is not None and sh.top / EMU_IN <= TITLE_ZONE_IN
                    and SOURCES_TITLE.match(sh.text_frame.text.strip().replace("\n", " "))):
                return sh
        return None



BODY_MIN_PT, MAX_WORDS, APPX_MIN, SOURCE_MIN, ANSWER_MAX_WORDS = 16, 40, 14, 10, 60

ap = argparse.ArgumentParser()
ap.add_argument("pptx")
ap.add_argument("--fonts", default="premium", help="premium | safe | 'Head Font,Body Font'")
ap.add_argument("--primary", default=None, help="Style line PRIMARY hex, for the slop check's colour rule")
ap.add_argument("--accent", default=None, help="Style line ACCENT: 'none' or a hex")
ap.add_argument("--no-slop", action="store_true", help="skip the slop check")
a = ap.parse_args()
prs = Presentation(a.pptx)
W, H = prs.slide_width, prs.slide_height
fp = a.fonts
if "," in fp:
    h, b = [x.strip() for x in fp.split(",", 1)]; fp = {"head": h, "body": b}
d = Deck(font_profile=fp)
allowed = {d.fonts["head"], d.fonts["body"], "Arial", None}
FOOTER = {"source", "page-number", "legend", "footnote", "tracker", "axis-label", "chart-label"}
problems = 0


def say(n, msg):
    global problems
    problems += 1
    print(f"slide {n}: {msg}")


def inner_text(shape):
    """(text, sizes) for text that sits inside groups and table cells, which the top-level loop cannot see."""
    if shape.shape_type == 6:  # group
        for s in shape.shapes:
            if s.shape_type == 6:
                yield from inner_text(s)
            elif s.has_text_frame and s.text_frame.text.strip():
                yield s.text_frame.text, [r.font.size.pt for p in s.text_frame.paragraphs for r in p.runs if r.font.size]
    elif getattr(shape, "has_table", False) and shape.has_table:
        for row in shape.table.rows:
            for c in row.cells:
                if c.text_frame.text.strip():
                    yield c.text_frame.text, [r.font.size.pt for p in c.text_frame.paragraphs for r in p.runs if r.font.size]


appendix = False
for n, s in enumerate(prs.slides, 1):
    words = 0
    tsh = find_title(s)
    title = tsh.text_frame.text.strip().replace("\n", " ") if tsh is not None else ""
    is_sources = bool(SOURCES_TITLE.match(title))
    if APPENDIX_TITLE.match(title) or is_sources or (n > 1 and has_appendix_footer(s, H)):
        appendix = True
    body_floor = SOURCE_MIN if is_sources else (APPX_MIN if appendix else BODY_MIN_PT)
    slide_text = " ".join(sh.text_frame.text for sh in s.shapes if sh.has_text_frame).lower()
    for sh in s.shapes:
        nm = sh.name
        if sh.left is not None and (sh.left < -Emu(20000) or sh.top < -Emu(20000) or sh.left + sh.width > W + Emu(20000) or sh.top + sh.height > H + Emu(20000)) and sh.rotation == 0:
            say(n, f"'{nm}' extends past the slide edge")
        if nm.startswith("icon:") and not sh._element.nvPicPr.cNvPr.get("descr"):
            say(n, f"icon '{nm}' has no alt text")
        if sh.has_text_frame and sh.text_frame.text.strip():
            txt = sh.text_frame.text
            in_footer_band = (sh.top is not None and sh.top > H - Emu(int(FOOTER_ZONE_IN * 914400))) or bool(re.match(r"^\s*sources?\s*:", txt, re.I))
            is_title = (tsh is not None and sh.shape_id == tsh.shape_id) or nm.startswith("title")
            named_footer = any(nm.startswith(f) for f in FOOTER)
            if not (named_footer or in_footer_band or is_title):
                words += len(txt.split())
            sizes = [r.font.size.pt for p in sh.text_frame.paragraphs for r in p.runs if r.font.size]
            if named_footer:
                floor = min(role_floor(nm), body_floor)
            elif in_footer_band:
                floor = SOURCE_MIN
            else:
                floor = body_floor
            if sizes and min(sizes) < floor:
                say(n, f"text at {min(sizes):g}pt (< {floor:g}): '{txt[:40]}'")
            for p in sh.text_frame.paragraphs:
                for r in p.runs:
                    if r.font.name not in allowed:
                        say(n, f"font '{r.font.name}' outside house fonts: '{r.text[:30]}'"); break
            # overflow estimate (only for text we sized ourselves)
            if sizes and sh.rotation == 0:
                size = max(sizes)
                w = sh.width / 914400 - (sh.text_frame.margin_left + sh.text_frame.margin_right) / 914400
                h = sh.height / 914400 - (sh.text_frame.margin_top + sh.text_frame.margin_bottom) / 914400
                head = any(r.font.name == d.fonts["head"] for p in sh.text_frame.paragraphs for r in p.runs)
                bold = any(r.font.bold for p in sh.text_frame.paragraphs for r in p.runs)
                lines = sum(len(d.wrap(p.text, size, w, bold, head)) for p in sh.text_frame.paragraphs)
                if lines * size * 1.15 / 72 > h * 1.12 + 0.03:
                    say(n, f"'{nm}' likely overflows its box ({lines} lines at {size:g}pt in {h:.2f}in): '{txt[:40]}'")
        small_inner = []                     # groups and table cells: count the words, check the size floor
        for txt, sizes in inner_text(sh):
            words += len(txt.split())
            if sizes and min(sizes) < body_floor:
                small_inner.append((min(sizes), txt))
        if small_inner:
            sz, txt = min(small_inner)
            say(n, f"'{nm}' (table or group): {len(small_inner)} text(s) below {body_floor:g}pt, smallest {sz:g}pt: '{txt[:40]}'")
        if sh.is_placeholder and sh.has_text_frame and not sh.text_frame.text.strip():
            say(n, f"empty placeholder '{nm}'")
    limit = None if (appendix or n == 1) else (ANSWER_MAX_WORDS if "we recommend" in slide_text else MAX_WORDS)
    if limit is not None and words > limit:
        print(f"slide {n}: note - {words} words (guide {limit}); judge the rendered slide, this is not a rule")
    if s.has_notes_slide and s.notes_slide.notes_text_frame.text.strip():
        print(f"slide {n}: note - has speaker notes")
if not a.no_slop:
    from slop_check import scan as slop_scan, report as slop_report
    findings = slop_scan(prs, a.accent, a.primary)
    print(slop_report(findings))
    for f in findings:
        if f["p"] == 0:
            problems += 1
print("OK: nothing to fix" if not problems else f"\n{problems} issue(s)")
sys.exit(1 if problems else 0)
