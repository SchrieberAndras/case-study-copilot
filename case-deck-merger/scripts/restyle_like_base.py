#!/usr/bin/env python3
"""Make merged member slides look like the base deck's slides.

Usage: python restyle_like_base.py merged.pptx --ref 2 --slides 3 4 [--table-ref 6]
                                   [--highlight 1] [--primary HEX] [--neutral HEX] --out styled.pptx

--ref        a merged slide that shows the base style (a normal content slide from the base deck)
--slides     merged slides to restyle (the member slides)
--table-ref  a merged slide containing a base-styled table (optional)
--highlight  1-based series that carries the message in multi-series charts (default 1)
--primary    PRIMARY hex (use the game plan's Style line when there is one; else detected)
--neutral    NEUTRAL hex for the other series (default: derived from PRIMARY, light tint)

Per slide: title moved/sized/coloured like the reference title; the reference's decor (accent
bars, small logo near the top, other text-free shapes) copied if missing; a slide-number box
added if the reference has one; tables get the reference table's header fill, header text
colour and body font size; charts follow think-cell rules: one highlight series in PRIMARY,
all other series NEUTRAL, no gridlines, data labels on. Everything else (content, layout of the
body) is left for review and manual tidy-up.
"""
import argparse
import collections
import copy
import io
import os
import re
import sys
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.oxml.ns import qn
from pptx.util import Pt

EMU_IN = 914400


def title_shape(slide):
    if slide.shapes.title is not None and slide.shapes.title.text_frame.text.strip():
        return slide.shapes.title
    best = None
    for sh in slide.shapes:
        if sh.has_text_frame and sh.text_frame.text.strip() and sh.top is not None and sh.top / EMU_IN < 1.6:
            sizes = [r.font.size.pt for p in sh.text_frame.paragraphs for r in p.runs if r.font.size]
            m = max(sizes) if sizes else (30 if sh.is_placeholder else 0)
            if m >= 20 and (best is None or m > best[0]):
                best = (m, sh)
    return best[1] if best else None


def first_run(sh):
    for p in sh.text_frame.paragraphs:
        for r in p.runs:
            return p, r
    return None, None


def is_slide_number(sh, h):
    return (sh.has_text_frame and sh.top is not None and sh.top > h - 0.9 * EMU_IN
            and re.fullmatch(r"\d{1,3}", sh.text_frame.text.strip() or "x"))


def is_decor(sh, title):
    """Title-zone decor only: text-free accent bars/lines and small pictures (logos) near the top.
    Content shapes lower down (dividers, boxes) belong to that slide and are never copied."""
    if title is not None and sh.shape_id == title.shape_id:
        return False
    if sh.top is None or sh.top / EMU_IN >= 1.6:
        return False
    if sh.shape_type == 13:  # picture
        return sh.top is not None and sh.top / EMU_IN < 1.6 and sh.width / EMU_IN < 2.5
    if getattr(sh, "has_chart", False) and sh.has_chart:
        return False
    if getattr(sh, "has_table", False) and sh.has_table:
        return False
    if sh.has_text_frame and sh.text_frame.text.strip():
        return False
    return sh.shape_type in (1, 9)  # autoshape, line


def primary_color(prs):
    c = collections.Counter()
    for s in prs.slides:
        for e in s._element.iter(qn("a:srgbClr")):
            v = e.get("val").upper()
            r, g, b = int(v[:2], 16), int(v[2:4], 16), int(v[4:], 16)
            if max(r, g, b) - min(r, g, b) > 30:  # skip greys, white, black, cream
                c[v] += 1
    return c.most_common(1)[0][0] if c else None


def neutral_from(prim):
    """case-study-ppt NEUTRAL: very light grey tinted toward PRIMARY (L ~85-88%).
    Taken from case-study-ppt's scripts/palette.py when that skill is installed next to this one."""
    import colorsys
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "case-study-ppt", "scripts"))
        from palette import roles
        return roles(prim)[0]["NEUTRAL"]
    except Exception:
        pass
    r, g, b = (int(prim[i:i + 2], 16) / 255 for i in (0, 2, 4))
    h, _, s = colorsys.rgb_to_hls(r, g, b)
    # keep PRIMARY's hue, fix lightness at 86.5% (spec: 85-88%), cap saturation so it stays a grey tint.
    # The old 12% tint toward 0xDE gave L = 79-83% for most brand colours (too dark).
    nr, ng, nb = colorsys.hls_to_rgb(h, 0.865, min(s, 0.22))
    return f"{round(nr * 255):02X}{round(ng * 255):02X}{round(nb * 255):02X}"


def restyle(path, ref_n, targets, table_ref, out, highlight=1, primary=None, neutral=None):
    prs = Presentation(path)
    S = list(prs.slides)
    h = prs.slide_height
    ref = S[ref_n - 1]
    rt = title_shape(ref)
    rp, rr = first_run(rt) if rt is not None else (None, None)
    decor = [sh for sh in ref.shapes if is_decor(sh, rt)]
    ref_num = next((sh for sh in ref.shapes if is_slide_number(sh, h)), None)
    tref = None
    if table_ref:
        tref = next((sh.table for sh in S[table_ref - 1].shapes if getattr(sh, "has_table", False) and sh.has_table), None)
    prim = (primary or primary_color(prs) or "").lstrip("#").upper() or None
    neut = (neutral.lstrip("#").upper() if neutral else (neutral_from(prim) if prim else None))
    log = []
    if prim is None:
        log.append("no PRIMARY found or given (--primary): charts left uncoloured")

    for n in targets:
        s = S[n - 1]
        t = title_shape(s)
        if t is not None and rt is not None:
            t.left, t.top, t.width, t.height = rt.left, rt.top, rt.width, rt.height
            for p in t.text_frame.paragraphs:
                p.alignment = rp.alignment
                for r in p.runs:
                    r.font.size = rr.font.size or Pt(24)
                    r.font.bold = rr.font.bold
                    r.font.name = rr.font.name
                    if rr.font.color and rr.font.color.type is not None and rr.font.color.rgb is not None:
                        r.font.color.rgb = rr.font.color.rgb
            t.text_frame.word_wrap = True
            log.append(f"slide {n}: title restyled")
        # decor: copy what the target lacks (same geometry already present = skip)
        if any(d.shape_type == 13 for d in decor):  # base has a logo: drop the member's own top logos
            for sh in list(s.shapes):
                if is_decor(sh, t) and sh.shape_type == 13:
                    sh._element.getparent().remove(sh._element)
                    log.append(f"slide {n}: member logo removed")
        have = {(sh.left, sh.top, sh.width, sh.height) for sh in s.shapes}
        for d in decor:
            if (d.left, d.top, d.width, d.height) in have:
                continue
            if d.shape_type == 13:
                s.shapes.add_picture(io.BytesIO(d.image.blob), d.left, d.top, d.width, d.height)
            else:
                s.shapes._spTree.insert_element_before(copy.deepcopy(d._element), "p:extLst")
            log.append(f"slide {n}: decor copied ({d.name})")
        if ref_num is not None:  # replace any member slide-number box with the base one
            for sh in list(s.shapes):
                if is_slide_number(sh, h):
                    sh._element.getparent().remove(sh._element)
            el = copy.deepcopy(ref_num._element)
            s.shapes._spTree.insert_element_before(el, "p:extLst")
            for tnode in el.iter(qn("a:t")):
                tnode.text = str(n)
            log.append(f"slide {n}: slide number added")
        for sh in s.shapes:
            if getattr(sh, "has_table", False) and sh.has_table and tref is not None:
                hdr_src = tref.cell(0, 0)
                body_src = tref.cell(1, 0) if len(tref.rows) > 1 else hdr_src
                _, hr = first_run(hdr_src)
                _, br = first_run(body_src)
                for ci, c in enumerate(sh.table.rows[0].cells):
                    if hdr_src.fill.type == 1:
                        c.fill.solid(); c.fill.fore_color.rgb = hdr_src.fill.fore_color.rgb
                    for p in c.text_frame.paragraphs:
                        for r in p.runs:
                            if hr is not None:
                                r.font.size = hr.font.size; r.font.bold = hr.font.bold
                                if hr.font.color and hr.font.color.type is not None:
                                    r.font.color.rgb = hr.font.color.rgb
                for row in list(sh.table.rows)[1:]:
                    for c in row.cells:
                        c.fill.background()
                        for p in c.text_frame.paragraphs:
                            for r in p.runs:
                                if br is not None:
                                    r.font.size = br.font.size
                                    if br.font.color and br.font.color.type is not None:
                                        r.font.color.rgb = br.font.color.rgb
                # drop the built-in table style banding so fills above win
                tblPr = sh.table._tbl.tblPr
                for attr in ("bandRow", "firstRow"):
                    tblPr.set(attr, "0")
                log.append(f"slide {n}: table restyled")
            if getattr(sh, "has_chart", False) and sh.has_chart and prim:
                ch = sh.chart
                try:
                    ch.value_axis.has_major_gridlines = False
                    ch.value_axis.visible = False
                    ch.has_legend = False if len(list(ch.plots[0].series)) == 1 else ch.has_legend
                    ch.plots[0].has_data_labels = True
                except (ValueError, IndexError):
                    pass  # pie charts etc. have no value axis
                series = [ser for plot in ch.plots for ser in plot.series]
                hi = highlight if 1 <= highlight <= len(series) else 1
                for k, ser in enumerate(series, start=1):
                    colour = prim if (k == hi or len(series) == 1) else neut
                    ser.format.fill.solid(); ser.format.fill.fore_color.rgb = RGBColor.from_string(colour)
                log.append(f"slide {n}: chart series {hi} of {len(series)} in PRIMARY {prim}"
                           + (f", others NEUTRAL {neut}" if len(series) > 1 else ""))
    prs.save(out)
    print(f"saved {out}")
    for l in log:
        print("  - " + l)
    print("Check every restyled slide in a render; body layout is not changed.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pptx")
    ap.add_argument("--ref", type=int, required=True)
    ap.add_argument("--slides", type=int, nargs="+", required=True)
    ap.add_argument("--table-ref", type=int)
    ap.add_argument("--highlight", type=int, default=1, help="1-based series to highlight in PRIMARY")
    ap.add_argument("--primary", help="PRIMARY hex, e.g. 1F2A44 (game plan Style line)")
    ap.add_argument("--neutral", help="NEUTRAL hex for non-highlight series")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    restyle(a.pptx, a.ref, a.slides, a.table_ref, a.out, a.highlight, a.primary, a.neutral)


if __name__ == "__main__":
    main()
