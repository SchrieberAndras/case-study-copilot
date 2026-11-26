#!/usr/bin/env python3
"""Helpers for editing an existing case deck in place with python-pptx while keeping its formatting.

CLI:   python pptx_edit_helpers.py map deck.pptx      -> every shape (groups expanded): id, position (in), font size, text
Import (from a fix script in the working directory):
    import sys; sys.path.insert(0, "<skill-dir>/scripts")
    from pptx_edit_helpers import *

Why these exist: python-pptx's `text_frame.text = ...` wipes run formatting (font, size,
colour, bullets). These helpers clone the existing paragraph/run XML instead, so edited
text looks exactly like the original.
"""
import copy
import re
import sys
from pptx import Presentation
from pptx.opc.constants import RELATIONSHIP_TYPE as RT
from pptx.util import Pt, Inches
from pptx.dml.color import RGBColor
from pptx.oxml.ns import qn
from pptx.text.text import _Run

EMU_IN = 914400


def iter_shapes(shapes):
    """Every shape, including shapes inside groups (depth-first)."""
    for sh in shapes:
        yield sh
        if sh.shape_type == 6:  # group
            yield from iter_shapes(sh.shapes)


def shape(slide, sid):
    """Shape on a slide by shape_id (ids come from `map`), also inside groups."""
    for sh in iter_shapes(slide.shapes):
        if sh.shape_id == sid:
            return sh
    raise KeyError(f"shape id {sid} not on slide")


def set_paras(tf, texts, size=None, bold_prefix=False):
    """Replace all paragraphs with `texts`, cloning paragraph 1's formatting (bullets, spacing, font).
    bold_prefix=True makes the part before the first ':' bold ("Budget: ...")."""
    ps = tf._txBody.findall(qn("a:p"))
    tmpl = copy.deepcopy(ps[0])
    for p in ps:
        tf._txBody.remove(p)
    for t in texts:
        p = copy.deepcopy(tmpl)
        runs = p.findall(qn("a:r"))
        if not runs:  # empty template paragraph: create a run
            r = p.makeelement(qn("a:r"), {}); r.append(r.makeelement(qn("a:t"), {}))
            end = p.find(qn("a:endParaRPr"))
            (end.addprevious(r) if end is not None else p.append(r)); runs = [r]
        for r in runs[1:]:
            p.remove(r)
        for el in p.findall(qn("a:br")) + p.findall(qn("a:fld")):
            p.remove(el)
        r = runs[0]
        if bold_prefix and ":" in t:
            head, tail = t.split(":", 1)
            r.find(qn("a:t")).text = head + ":"
            r2 = copy.deepcopy(r); r2.find(qn("a:t")).text = tail
            r.get_or_add_rPr().set("b", "1"); r2.get_or_add_rPr().set("b", "0")
            r.addnext(r2)
        else:
            r.find(qn("a:t")).text = t
        tf._txBody.append(p)
    if size:
        font_size(tf, size)


def set_text(sh, text, size=None):
    set_paras(sh.text_frame, [text], size)


def font_size(tf, size):
    for p in tf.paragraphs:
        for r in p.runs:
            r.font.size = Pt(size)


def set_cell(tbl, r, c, text, size=None):
    set_paras(tbl.cell(r, c).text_frame, [text], size)


def table_font(tbl, size):
    for row in tbl.rows:
        for c in row.cells:
            font_size(c.text_frame, size)


def add_table_column(tbl, widths_in=None):
    """Append a column cloned from the last one (keeps borders/fills). Optionally set all widths."""
    t = tbl._tbl
    grid = t.find(qn("a:tblGrid"))
    grid.append(copy.deepcopy(grid.findall(qn("a:gridCol"))[-1]))
    for tr in t.findall(qn("a:tr")):
        tr.append(copy.deepcopy(tr.findall(qn("a:tc"))[-1]))
    if widths_in:
        for col, w in zip(tbl.columns, widths_in):
            col.width = Inches(w)


def add_table_row(tbl, values=None):
    """Append a row cloned from the last row; fill with values if given. Returns the row index."""
    t = tbl._tbl
    t.append(copy.deepcopy(t.findall(qn("a:tr"))[-1]))
    i = len(tbl.rows) - 1
    for c, v in enumerate(values or []):
        set_cell(tbl, i, c, v)
    return i


def add_text(slide, x, y, w, h, text, size, bold=False, color=RGBColor(0x1E, 0x22, 0x30),
             fill=None, font=None):
    """New text box in inches. `text` may be a list of lines. Match font/colour to the deck;
    without `font=` the run inherits the theme font."""
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame; tf.word_wrap = True
    if fill is not None:
        tb.fill.solid(); tb.fill.fore_color.rgb = fill
        tf.margin_left = tf.margin_right = Inches(0.15); tf.margin_top = tf.margin_bottom = Inches(0.08)
    else:
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    for i, line in enumerate(text if isinstance(text, list) else [text]):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        r = p.add_run(); r.text = line
        r.font.size = Pt(size); r.font.bold = bold; r.font.color.rgb = color
        if font:
            r.font.name = font
    return tb


def move(sh, x=None, y=None, w=None, h=None):
    """Reposition/resize in inches; None keeps the current value."""
    if x is not None: sh.left = Inches(x)
    if y is not None: sh.top = Inches(y)
    if w is not None: sh.width = Inches(w)
    if h is not None: sh.height = Inches(h)


URL_RX = re.compile(r"(?:https?://|www\.)[^\s<>\"]+", re.I)


def link_urls(tf):
    """Make every URL typed as text (https://, http://, www.) a clickable hyperlink.
    The URL becomes its own run with the same formatting; text before and after it stays as is.
    Trailing punctuation ('.', ',', ')') is kept out of the link; www. links get https://.
    Returns the number of links created."""
    made = 0
    for p in tf.paragraphs:
        for r in list(p.runs):
            if r.hyperlink.address is not None:
                continue
            text = r.text
            pieces, last = [], 0
            for m in URL_RX.finditer(text):
                url = m.group(0).rstrip(".,;:)]")
                end = m.start() + len(url)
                if m.start() > last:
                    pieces.append((text[last:m.start()], None))
                pieces.append((url, url if url.lower().startswith("http") else "https://" + url))
                last = end
            if not any(addr for _, addr in pieces):
                continue
            if last < len(text):
                pieces.append((text[last:], None))
            anchor = r._r
            r.text = pieces[0][0]
            if pieces[0][1]:
                r.hyperlink.address = pieces[0][1]; made += 1
            for txt, addr in pieces[1:]:
                el = copy.deepcopy(r._r)
                rPr = el.find(qn("a:rPr"))
                if rPr is not None:
                    for h in rPr.findall(qn("a:hlinkClick")):
                        rPr.remove(h)
                anchor.addnext(el); anchor = el
                run = _Run(el, p); run.text = txt
                if addr:
                    run.hyperlink.address = addr; made += 1
    return made


def remove_notes(prs):
    """Delete every slide's speaker notes from the .pptx (house rule: notes live in the
    _SpeakerNotes.docx). Copy the text there first. Returns the slide numbers cleaned."""
    cleaned = []
    for i, s in enumerate(prs.slides, 1):
        for rId, rel in list(s.part.rels.items()):
            if rel.reltype == RT.NOTES_SLIDE:
                s.part.rels.pop(rId)
                cleaned.append(i)
    return cleaned


def disable_shrink(prs):
    """Turn shrink-to-fit off everywhere so font sizes stay as set."""
    for s in prs.slides:
        for el in s._element.iter(qn("a:normAutofit")):
            el.tag = qn("a:noAutofit")


def copy_background(prs, src_idx, dst_indices):
    """Give slides the same solid background colour as slide src_idx (0-based)."""
    rgb = prs.slides[src_idx].background.fill.fore_color.rgb
    for i in dst_indices:
        f = prs.slides[i].background.fill; f.solid(); f.fore_color.rgb = rgb


def _inch(v):
    return f"{v / EMU_IN:5.2f}" if v is not None else "    ?"


def map_deck(path):
    prs = Presentation(path)
    print(f"slide size {prs.slide_width/EMU_IN:.2f} x {prs.slide_height/EMU_IN:.2f} in")
    for i, s in enumerate(prs.slides, 1):
        notes = " (has speaker notes)" if s.has_notes_slide and s.notes_slide.notes_text_frame is not None \
            and s.notes_slide.notes_text_frame.text.strip() else ""
        print(f"=== slide {i}{notes}")
        _map_shapes(s.shapes, "")


def _map_shapes(shapes, indent):
    for sh in shapes:
        if sh.shape_type == 6:  # group: list it, then its members indented
            print(f"{indent}{sh.shape_id:>4} x{_inch(sh.left)} y{_inch(sh.top)} "
                  f"w{_inch(sh.width)} h{_inch(sh.height)}  GROUP")
            _map_shapes(sh.shapes, indent + "    ")
            continue
        if getattr(sh, "has_table", False) and sh.has_table:
            t = f"TABLE {len(sh.table.rows)}x{len(sh.table.columns)}"
        elif getattr(sh, "has_chart", False) and sh.has_chart:
            t = f"CHART {sh.chart.chart_type}"
        elif sh.has_text_frame:
            t = sh.text_frame.text[:60].replace("\n", " | ")
        else:
            t = ""
        sz = None
        if sh.has_text_frame:
            for p in sh.text_frame.paragraphs:
                for r in p.runs:
                    if r.font.size: sz = r.font.size.pt; break
                if sz: break
        print(f"{indent}{sh.shape_id:>4} x{_inch(sh.left)} y{_inch(sh.top)} "
              f"w{_inch(sh.width)} h{_inch(sh.height)} {str(sz):>5}pt {t!r}")


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "map":
        map_deck(sys.argv[2])
    else:
        print(__doc__)
