#!/usr/bin/env python3
"""Compare team members' decks before merging.

Usage: python inventory_decks.py member1.pptx member2.pptx member3.pptx [--json out.json]

Per deck: slide size, fonts and colours actually used (most common first), layouts, and per
slide: title, word count, numbers on the slide, speaker-notes yes/no, sources/links.
Across decks: likely duplicate slides (similar titles) and numbers that appear with
different values next to the same label (possible conflicts to resolve against the game plan).
"""
import argparse
import collections
import difflib
import json
import re
from pptx import Presentation
from pptx.oxml.ns import qn

EMU_IN = 914400
NUM = re.compile(r"[$€£]?\d[\d,.]*\s?(?:%|[KMB]\b|bn\b|million\b|t\b|kg\b)?")


def title_of(slide):
    if slide.shapes.title is not None and slide.shapes.title.text_frame.text.strip():
        return slide.shapes.title.text_frame.text.strip().replace("\n", " ")
    best = None
    for sh in slide.shapes:
        if sh.has_text_frame and sh.text_frame.text.strip() and sh.top is not None and sh.top / EMU_IN < 1.6:
            sizes = [r.font.size.pt for p in sh.text_frame.paragraphs for r in p.runs if r.font.size]
            m = max(sizes) if sizes else 0
            if m >= 20 and (best is None or m > best[0]):
                best = (m, sh.text_frame.text.strip().replace("\n", " "))
    return best[1] if best else ""


def slide_text(slide):
    out = []
    for sh in slide.shapes:
        if sh.has_text_frame:
            out.append(sh.text_frame.text)
        if getattr(sh, "has_table", False) and sh.has_table:
            out += [c.text_frame.text for r in sh.table.rows for c in r.cells]
    return " ".join(out)


def inventory(path):
    prs = Presentation(path)
    fonts, colors = collections.Counter(), collections.Counter()
    slides = []
    for i, s in enumerate(prs.slides, 1):
        for e in s._element.iter():
            if e.tag == qn("a:latin") and e.get("typeface"):
                fonts[e.get("typeface")] += 1
            if e.tag == qn("a:srgbClr"):
                colors[e.get("val").upper()] += 1
        txt = slide_text(s)
        nums = []
        for m in NUM.finditer(txt):
            v = m.group(0).strip()
            if re.fullmatch(r"\d{1,2}|(19|20)\d\d", v):  # slide numbers, list numbers, years
                continue
            before = re.findall(r"[A-Za-z][A-Za-z-]+", txt[max(0, m.start() - 40):m.start()])
            nums.append({"value": v, "label": " ".join(before[-3:]).lower()})
        links = [r.hyperlink.address for sh in s.shapes if sh.has_text_frame
                 for p in sh.text_frame.paragraphs for r in p.runs if r.hyperlink.address]
        slides.append({"slide": i, "title": title_of(s), "layout": s.slide_layout.name,
                       "words": len(txt.split()), "numbers": nums, "links": links,
                       "notes": s.has_notes_slide and bool(s.notes_slide.notes_text_frame.text.strip())})
    return {"deck": path, "size_in": [round(prs.slide_width / EMU_IN, 2), round(prs.slide_height / EMU_IN, 2)],
            "fonts": fonts.most_common(5), "colors": colors.most_common(8), "slides": slides}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("decks", nargs="+")
    ap.add_argument("--json")
    a = ap.parse_args()
    inv = [inventory(d) for d in a.decks]
    for d in inv:
        print(f"=== {d['deck']}  size {d['size_in'][0]}x{d['size_in'][1]} in  ({len(d['slides'])} slides)")
        print(f"  fonts:  {d['fonts']}")
        print(f"  colors: {d['colors']}")
        for s in d["slides"]:
            print(f"  [{s['slide']:>2}] {s['title'][:60]!r} ({s['words']} w, layout '{s['layout']}'"
                  f"{', notes' if s['notes'] else ''}{', ' + str(len(s['links'])) + ' links' if s['links'] else ''})")
    sizes = {tuple(d["size_in"]) for d in inv}
    if len(sizes) > 1:
        print(f"\n!! Different slide sizes: {sizes} -> the merge scales them to the base size")
    print("\nPossible duplicate slides across decks:")
    found = False
    for i, d1 in enumerate(inv):
        for d2 in inv[i + 1:]:
            for s1 in d1["slides"]:
                for s2 in d2["slides"]:
                    if s1["title"] and s2["title"] and difflib.SequenceMatcher(None, s1["title"].lower(), s2["title"].lower()).ratio() > 0.7:
                        found = True
                        print(f"  {d1['deck']} #{s1['slide']} ~ {d2['deck']} #{s2['slide']}: {s1['title'][:50]!r}")
    if not found:
        print("  none")
    print("\nSame label, different numbers (check against the game plan):")
    by_label = collections.defaultdict(set)
    for d in inv:
        for s in d["slides"]:
            for n in s["numbers"]:
                if n["label"]:
                    by_label[n["label"]].add((n["value"], f"{d['deck']}#{s['slide']}"))
    conflicts = {k: v for k, v in by_label.items() if len({x[0] for x in v}) > 1 and len({x[1].split('#')[0] for x in v}) > 1}
    for k, v in list(conflicts.items())[:30]:
        print(f"  '{k}': " + "; ".join(f"{val} ({where})" for val, where in sorted(v)))
    if not conflicts:
        print("  none found")
    if a.json:
        json.dump(inv, open(a.json, "w"), indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
