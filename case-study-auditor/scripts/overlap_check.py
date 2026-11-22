#!/usr/bin/env python3
"""Flag text in a deck (or notes) copied too closely from the case or other sources.

Usage: python overlap_check.py deck.pptx source1.pdf [source2.pdf|.txt ...] [--n 7]

Finds every run of N+ consecutive words (default 7) that appears both in the
deck and in a source. Long matches mean the text was lifted, not paraphrased.
Accepts .pptx, .docx, .pdf, .txt, .md for both sides.
"""
import argparse
import re
import subprocess
import sys


def shape_texts(shapes):
    """Text of every shape, recursing into groups and tables."""
    for sh in shapes:
        if sh.shape_type == 6:  # group
            yield from shape_texts(sh.shapes)
            continue
        if sh.has_text_frame:
            yield sh.text_frame.text
        if getattr(sh, "has_table", False) and sh.has_table:
            for row in sh.table.rows:
                for c in row.cells:
                    yield c.text_frame.text


def read_text(path):
    p = path.lower()
    if p.endswith(".pptx"):
        from pptx import Presentation
        prs = Presentation(path)
        out = []
        for i, s in enumerate(prs.slides, 1):
            parts = list(shape_texts(s.shapes))
            if s.has_notes_slide and s.notes_slide.notes_text_frame is not None:
                parts.append(s.notes_slide.notes_text_frame.text)
            out.append((f"slide {i}", " ".join(parts)))
        return out
    if p.endswith(".docx"):
        import docx
        d = docx.Document(path)
        parts = [par.text for par in d.paragraphs]
        for t in d.tables:  # Q&A and notes files often use tables
            parts += [c.text for row in t.rows for c in row.cells]
        return [("doc", " ".join(parts))]
    if p.endswith(".pdf"):
        txt = subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True).stdout
        return [("pdf", txt)]
    with open(path, encoding="utf-8", errors="ignore") as f:
        return [("text", f.read())]


def words(t):
    # \w keeps accented letters (é, ő, ü) inside words; the old a-z class split them into fragments
    return re.findall(r"[\w$%€.,'-]+", t.lower().replace("’", "'"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("deck")
    ap.add_argument("sources", nargs="+")
    ap.add_argument("--n", type=int, default=7)
    a = ap.parse_args()

    src_grams = set()
    for s in a.sources:
        for _, t in read_text(s):
            w = [x.strip(".,") for x in words(t)]
            src_grams.update(tuple(w[i:i + a.n]) for i in range(len(w) - a.n + 1))

    total = 0
    for label, t in read_text(a.deck):
        w = [x.strip(".,") for x in words(t)]
        hits = [i for i in range(len(w) - a.n + 1) if tuple(w[i:i + a.n]) in src_grams]
        if not hits:
            continue
        # merge overlapping windows into spans
        spans, start, end = [], hits[0], hits[0] + a.n
        for i in hits[1:]:
            if i <= end:
                end = i + a.n
            else:
                spans.append((start, end)); start, end = i, i + a.n
        spans.append((start, end))
        for s, e in spans:
            total += 1
            print(f"[{label}] {e - s} words copied: \"{' '.join(w[s:e])}\"")
    if total == 0:
        print(f"No passages of {a.n}+ identical consecutive words found.")
    else:
        print(f"\n{total} copied passage(s). Paraphrase them or quote and cite.")


if __name__ == "__main__":
    sys.exit(main())
