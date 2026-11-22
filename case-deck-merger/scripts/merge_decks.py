#!/usr/bin/env python3
"""Merge slides from several team members' .pptx files into one deck in the base deck's style.

Usage:
  python merge_decks.py --base base.pptx --order order.json --out merged.pptx
                        [--font Arial] [--colormap colors.json] [--keep-notes]

order.json: final slide order, one entry per slide, e.g.
  [{"deck": "anna.pptx", "slide": 1, "owner": "Anna"},
   {"deck": "base.pptx", "slide": 4, "owner": "member3"}, ...]
  ("slide" is 1-based. The base deck's own slides are only included if listed.)
colors.json: {"E5163A": "1F2A44", ...}  member hex colour -> base hex colour.

What it does: starts from the base deck's masters/layouts/theme (the style that wins), copies
each listed slide's shapes with their images, charts (+ data), tables and hyperlinks, scales
slides from a different slide size to fit, gives member slides the base background, optionally
unifies fonts and colours, and renumbers plain slide-number boxes.
Speaker notes: house rule is no notes inside the deck, so member notes are NOT copied into the
.pptx; they go to <out stem>_member_notes.md (merged slide # -> owner -> notes text). They are
copied in only with --keep-notes or when the base deck itself has notes.
Refuses to overwrite any input file (base or any deck in order.json).
Prints warnings for anything it could not carry over (SmartArt, video, OLE objects).
"""
import argparse
import collections
import copy
import io
import json
import os
import re
import sys

from pptx import Presentation
from pptx.opc.constants import RELATIONSHIP_TYPE as RT
from pptx.opc.package import Part
from pptx.opc.packuri import PackURI
from pptx.oxml.ns import qn
from pptx.parts.chart import ChartPart
from pptx.parts.embeddedpackage import EmbeddedXlsxPart

R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
SHAPE_TAGS = {qn("p:sp"), qn("p:pic"), qn("p:graphicFrame"), qn("p:grpSp"), qn("p:cxnSp"),
              "{http://schemas.openxmlformats.org/markup-compatibility/2006}AlternateContent"}
EMU_IN = 914400


def clear_slides(prs):
    lst = prs.slides._sldIdLst
    for sid in list(lst):
        prs.part.rels.pop(sid.rId)
        lst.remove(sid)


def pick_layout(dst, name):
    for l in dst.slide_layouts:
        if l.name == name:
            return l, True
    for l in dst.slide_layouts:
        if l.name.lower() in ("blank", "leer", "vide", "üres"):
            return l, False
    return min(dst.slide_layouts, key=lambda l: len(l.placeholders)), False


def unique_partname(pkg, original):
    m = re.match(r"(.*?)(\d*)(\.\w+)$", str(original))
    stem, ext = m.group(1), m.group(3)
    return pkg.next_partname(stem + "%d" + ext)


def copy_rels(src_slide, new_slide, dst, warn, label):
    """Recreate the source slide's relationships on the new slide; return old rId -> new rId."""
    pkg = dst.part.package
    rid_map = {}
    for rel in list(src_slide.part.rels.values()):
        rt = rel.reltype
        if rt in (RT.SLIDE_LAYOUT, RT.NOTES_SLIDE):
            continue
        if rel.is_external:
            rid_map[rel.rId] = new_slide.part.relate_to(rel.target_ref, rt, is_external=True)
        elif rt == RT.IMAGE:
            _, rid = new_slide.part.get_or_add_image_part(io.BytesIO(rel.target_part.blob))
            rid_map[rel.rId] = rid
        elif rt == RT.CHART:
            src_chart = rel.target_part
            cp = ChartPart.load(pkg.next_partname(ChartPart.partname_template),
                                src_chart.content_type, pkg, src_chart.blob)
            for crel in list(src_chart.rels.values()):
                if crel.reltype == RT.PACKAGE and not crel.is_external:
                    xl = EmbeddedXlsxPart.new(crel.target_part.blob, pkg)
                    new_rid = cp.relate_to(xl, RT.PACKAGE)
                    ext = cp._element.find(qn("c:externalData"))
                    if ext is not None:
                        ext.set(qn("r:id"), new_rid)
            rid_map[rel.rId] = new_slide.part.relate_to(cp, RT.CHART)
        elif rt == RT.SLIDE:
            warn(f"{label}: link to another slide dropped (re-link it after merging)")
        else:
            # ponytail: one-level generic copy; SmartArt/video/OLE keep their visuals only if
            # PowerPoint can re-render them. Check the render.
            tp = rel.target_part
            np = Part.load(unique_partname(pkg, tp.partname), tp.content_type, pkg, tp.blob)
            rid_map[rel.rId] = new_slide.part.relate_to(np, rt)
            warn(f"{label}: copied a '{rt.rsplit('/', 1)[-1]}' part as-is; check this slide in the render")
    return rid_map


def first_xfrm(el):
    for path in ("p:spPr/a:xfrm", "p:xfrm", "p:grpSpPr/a:xfrm"):
        x = el.find(path.replace("p:", "{%s}" % "http://schemas.openxmlformats.org/presentationml/2006/main")
                    .replace("a:", "{%s}" % "http://schemas.openxmlformats.org/drawingml/2006/main"))
        if x is not None:
            return x
    return None


def scale_el(el, s, ox, oy):
    x = first_xfrm(el)
    if x is not None:
        off, ext = x.find(qn("a:off")), x.find(qn("a:ext"))
        if off is not None:
            off.set("x", str(int(int(off.get("x")) * s + ox)))
            off.set("y", str(int(int(off.get("y")) * s + oy)))
        if ext is not None:
            ext.set("cx", str(int(int(ext.get("cx")) * s)))
            ext.set("cy", str(int(int(ext.get("cy")) * s)))
    for gc in el.iter(qn("a:gridCol")):
        gc.set("w", str(int(int(gc.get("w")) * s)))
    for tr in el.iter(qn("a:tr")):
        tr.set("h", str(int(int(tr.get("h")) * s)))


def notes_text(slide):
    if not slide.has_notes_slide:
        return ""
    tf = slide.notes_slide.notes_text_frame
    if tf is not None:
        return tf.text.strip()
    return "\n".join(sh.text_frame.text for sh in slide.notes_slide.shapes if sh.has_text_frame).strip()


def copy_slide(src_prs, src_slide, dst, warn, label, bg=None, keep_notes=False):
    layout, same_layout = pick_layout(dst, src_slide.slide_layout.name)
    new = dst.slides.add_slide(layout)
    tree = new.shapes._spTree
    for el in list(tree):
        if el.tag in SHAPE_TAGS:
            tree.remove(el)
    rid_map = copy_rels(src_slide, new, dst, warn, label)

    sw, sh = src_prs.slide_width, src_prs.slide_height
    dw, dh = dst.slide_width, dst.slide_height
    s = min(dw / sw, dh / sh)
    ox, oy = (dw - sw * s) / 2, (dh - sh * s) / 2
    resize = (sw, sh) != (dw, dh)
    if resize:
        warn(f"{label}: slide size {sw/EMU_IN:.2f}x{sh/EMU_IN:.2f} in scaled by {s:.2f} and centred; font sizes not scaled, check text fit")

    by_el = {shp._element: shp for shp in src_slide.shapes}
    for el in src_slide.shapes._spTree:
        if el.tag not in SHAPE_TAGS:
            continue
        new_el = copy.deepcopy(el)
        shp = by_el.get(el)
        # placeholders without their own position inherit it from the source layout: write it down
        if shp is not None and shp.is_placeholder and first_xfrm(new_el) is None and not same_layout:
            spPr = new_el.find(qn("p:spPr"))
            if spPr is not None and shp.left is not None:
                xfrm = spPr.get_or_add_xfrm()
                xfrm.x, xfrm.y, xfrm.cx, xfrm.cy = shp.left, shp.top, shp.width, shp.height
        for e in new_el.iter():
            for k, v in list(e.attrib.items()):
                if k.startswith("{%s}" % R_NS):
                    if v in rid_map:
                        e.set(k, rid_map[v])
                    else:
                        warn(f"{label}: dangling reference {v} removed")
                        del e.attrib[k]
        if resize:
            scale_el(new_el, s, ox, oy)
        tree.insert_element_before(new_el, "p:extLst")

    # background: keep the slide's own if it is a base slide, else the base deck's common one
    src_bg = src_slide._element.cSld.find(qn("p:bg"))
    use_bg = src_bg if bg is None else bg
    if use_bg is not None:
        cSld = new._element.cSld
        old = cSld.find(qn("p:bg"))
        if old is not None:
            cSld.remove(old)
        cSld.insert(0, copy.deepcopy(use_bg))

    if keep_notes and src_slide.has_notes_slide:
        stf = src_slide.notes_slide.notes_text_frame
        txt = stf.text if stf is not None else ""
        if txt.strip():
            ntf = new.notes_slide.notes_text_frame
            if ntf is not None:
                ntf.text = txt
            else:  # base notes master has no body placeholder: carry the source notes shapes over
                ntree = new.notes_slide.shapes._spTree
                for el in src_slide.notes_slide.shapes._spTree:
                    if el.tag == qn("p:sp"):
                        ntree.insert_element_before(copy.deepcopy(el), "p:extLst")
    return new


def common_bg(prs):
    seen = collections.Counter()
    els = {}
    for s in prs.slides:
        bg = s._element.cSld.find(qn("p:bg"))
        if bg is not None:
            key = str(bg.xml)
            seen[key] += 1
            els[key] = bg
    return els[seen.most_common(1)[0][0]] if seen else None


def unify(dst, font, colormap):
    for slide in dst.slides:
        for e in slide._element.iter():
            if font and e.tag in (qn("a:latin"), qn("a:ea"), qn("a:cs")):
                tf = e.get("typeface", "")
                if tf and not tf.startswith("+"):
                    e.set("typeface", font)
            if colormap and e.tag == qn("a:srgbClr"):
                v = e.get("val", "").upper()
                if v in colormap:
                    e.set("val", colormap[v])


def renumber(dst):
    """Plain-number text boxes in the bottom strip are slide numbers: set them to the new position."""
    h = dst.slide_height
    for i, slide in enumerate(dst.slides, start=1):
        for shp in slide.shapes:
            if (shp.has_text_frame and shp.top is not None and shp.top > h - 0.9 * EMU_IN
                    and re.fullmatch(r"\d{1,3}", shp.text_frame.text.strip())):
                runs = [r for p in shp.text_frame.paragraphs for r in p.runs]
                if runs:
                    runs[0].text = str(i)
                    for r in runs[1:]:
                        r.text = ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True)
    ap.add_argument("--order", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--font")
    ap.add_argument("--colormap")
    ap.add_argument("--keep-notes", action="store_true",
                    help="copy member speaker notes into the .pptx (default: never; house rule is no notes in the deck, they go to the _member_notes.md sidecar)")
    a = ap.parse_args()

    order = json.load(open(a.order))
    inputs = {os.path.realpath(a.base)} | {os.path.realpath(item["deck"]) for item in order}
    if os.path.realpath(a.out) in inputs:
        sys.exit(f"refusing to overwrite an input file: {a.out}. Choose another --out name "
                 "(copy a base deck named COBE_<Case>.pptx to COBE_<Case>_Skeleton.pptx first).")
    colormap = {k.upper(): v.upper() for k, v in json.load(open(a.colormap)).items()} if a.colormap else {}
    warnings = []
    warn = warnings.append

    base_prs = Presentation(a.base)
    keep_notes = a.keep_notes  # house rule: no notes in the deck; they go to the sidecar file
    dst = Presentation(a.base)
    base_bg = common_bg(base_prs)
    clear_slides(dst)
    sources = {}
    origin = []
    sidecar = []
    base_real = os.path.realpath(a.base)
    for i, item in enumerate(order, start=1):
        path = item["deck"]
        if path not in sources:
            sources[path] = Presentation(path)
        src = sources[path]
        n = item["slide"]
        if not 1 <= n <= len(src.slides):
            sys.exit(f"order entry {i}: {path} has no slide {n}")
        label = f"merged slide {i} ({path} #{n})"
        is_base = os.path.realpath(path) == base_real
        copy_slide(src, src.slides[n - 1], dst, warn, label, bg=None if is_base else base_bg,
                   keep_notes=keep_notes)
        txt = notes_text(src.slides[n - 1])
        if txt:
            sidecar.append((i, item.get("owner", ""), path, n, txt))
        origin.append((i, item.get("owner", ""), path, n))

    unify(dst, a.font, colormap)
    renumber(dst)
    dst.save(a.out)

    print(f"saved {a.out}: {len(order)} slides")
    if sidecar:
        side = os.path.splitext(a.out)[0] + "_member_notes.md"
        with open(side, "w", encoding="utf-8") as f:
            f.write(f"# Member speaker notes (from the source decks, not in {os.path.basename(a.out)})\n\n")
            for i, owner, path, n, txt in sidecar:
                f.write(f"## Merged slide {i} | {owner or '-'} | {os.path.basename(path)} #{n}\n\n{txt}\n\n")
        print(f"speaker notes {'copied into the deck AND ' if keep_notes else ''}written to {side} "
              f"({len(sidecar)} slides) -> fold them into COBE_<Case>_SpeakerNotes.docx")
    print("\nOrigin (merged # | owner | source deck | source #):")
    for i, owner, path, n in origin:
        print(f"  {i:>2} | {owner or '-'} | {path} | {n}")
    if warnings:
        print("\nWarnings:")
        for w in dict.fromkeys(warnings):
            print("  - " + w)


if __name__ == "__main__":
    main()
