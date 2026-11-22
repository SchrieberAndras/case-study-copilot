#!/usr/bin/env python3
"""Dump a rough/semi-built .pptx to JSON so it can be re-planned slide by slide.

    python extract_deck.py input.pptx outdir

Writes outdir/outline.json (per slide: title, text blocks in reading order, tables, chart data,
pictures, notes) and outdir/media/* (embedded images, e.g. logos). Read-only: the input is never changed.
"""
import json, os, sys
from pptx import Presentation
from pptx.util import Emu
from pptx.enum.shapes import MSO_SHAPE_TYPE as T


def walk(shapes):
    for sh in shapes:
        if sh.shape_type == T.GROUP:
            yield from walk(sh.shapes)
        else:
            yield sh


def main(path, out):
    prs = Presentation(path)
    os.makedirs(os.path.join(out, "media"), exist_ok=True)
    W, H = prs.slide_width, prs.slide_height
    slides = []
    for i, s in enumerate(prs.slides, 1):
        rec = {"n": i, "layout": s.slide_layout.name, "title": None, "blocks": [], "tables": [], "charts": [], "pictures": [], "notes": ""}
        items = []
        for sh in walk(s.shapes):
            top, left = (sh.top or 0), (sh.left or 0)
            if sh.has_text_frame and sh.text_frame.text.strip():
                sizes = [r.font.size.pt for p in sh.text_frame.paragraphs for r in p.runs if r.font.size]
                paras = [{"text": p.text.strip(), "level": p.level} for p in sh.text_frame.paragraphs if p.text.strip()]
                is_title = sh.is_placeholder and sh.placeholder_format.type is not None and "TITLE" in str(sh.placeholder_format.type)
                items.append((top, left, {"paras": paras, "max_pt": max(sizes) if sizes else None, "is_title": bool(is_title),
                                          "pos": [round(left / W, 2), round(top / H, 2)]}))
            if getattr(sh, "has_table", False) and sh.has_table:
                rec["tables"].append([[c.text.strip() for c in r.cells] for r in sh.table.rows])
            if getattr(sh, "has_chart", False) and sh.has_chart:
                ch = sh.chart
                try:
                    cats = [str(c) for c in ch.plots[0].categories]
                    series = [{"name": se.name, "values": list(se.values)} for se in ch.plots[0].series]
                except Exception:
                    cats, series = [], []
                rec["charts"].append({"type": str(ch.chart_type), "categories": cats, "series": series})
            if sh.shape_type == T.PICTURE:
                try:
                    ext = sh.image.ext
                    fn = f"s{i}_{len(rec['pictures']) + 1}.{ext}"
                    with open(os.path.join(out, "media", fn), "wb") as f:
                        f.write(sh.image.blob)
                except Exception:
                    fn = "(not embedded)"
                rec["pictures"].append({"file": f"media/{fn}", "w_in": round(sh.width / 914400, 2), "h_in": round(sh.height / 914400, 2),
                                        "pos": [round(left / W, 2), round(top / H, 2)], "name": sh.name})
        items.sort(key=lambda t: (t[0] // 300000, t[1]))      # reading order: rows, then left to right
        for _, _, b in items:
            rec["blocks"].append(b)
        cand = [b for b in rec["blocks"] if b["is_title"]] or sorted([b for b in rec["blocks"] if b["max_pt"]], key=lambda b: -b["max_pt"])[:1]
        if cand:
            rec["title"] = " ".join(p["text"] for p in cand[0]["paras"])
        if s.has_notes_slide:
            rec["notes"] = s.notes_slide.notes_text_frame.text.strip()
        slides.append(rec)
    with open(os.path.join(out, "outline.json"), "w") as f:
        json.dump({"source": os.path.basename(path), "slides": slides}, f, indent=1, ensure_ascii=False)
    print(f"{len(slides)} slides -> {out}/outline.json")
    for r in slides:
        words = sum(len(p['text'].split()) for b in r['blocks'] for p in b['paras'])
        print(f"  {r['n']:>2}. {str(r['title'])[:70]!s:<70} | {words} words, {len(r['tables'])} tables, {len(r['charts'])} charts, {len(r['pictures'])} pics")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
