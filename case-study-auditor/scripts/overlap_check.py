#!/usr/bin/env python3
"""Flag text in a deck (or notes) copied too closely from the case or other sources.

Usage: python overlap_check.py deck.pptx source1.pdf [source2.pdf|.txt ...]

Finds every run of 7+ consecutive words that appears both in the
deck and in a source. Long matches mean the text was lifted, not paraphrased.
Accepts .pptx, .docx, .pdf, .txt, .md for both sides.
"""
import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from audit_pptx import text_frames, read_lines

N = 7  # case-study-ppt 3a: never copy 7+ consecutive words


def read_text(path):
    if not path.lower().endswith(".pptx"):
        return [("doc", " ".join(read_lines(path)))]
    from pptx import Presentation
    out = []
    for i, s in enumerate(Presentation(path).slides, 1):
        parts = [tf.text for sh in s.shapes for _, tf, _ in text_frames(sh)]
        if s.has_notes_slide and s.notes_slide.notes_text_frame is not None:
            parts.append(s.notes_slide.notes_text_frame.text)
        out.append((f"slide {i}", " ".join(parts)))
    return out


def words(t):
    # \w keeps accented letters (é, ő, ü) inside words; the old a-z class split them into fragments
    return re.findall(r"[\w$%€.,'-]+", t.lower().replace("’", "'"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("deck")
    ap.add_argument("sources", nargs="+")
    a = ap.parse_args()

    src_grams = set()
    for s in a.sources:
        for _, t in read_text(s):
            w = [x.strip(".,") for x in words(t)]
            src_grams.update(tuple(w[i:i + N]) for i in range(len(w) - N + 1))

    total = 0
    for label, t in read_text(a.deck):
        w = [x.strip(".,") for x in words(t)]
        hits = [i for i in range(len(w) - N + 1) if tuple(w[i:i + N]) in src_grams]
        if not hits:
            continue
        # merge overlapping windows into spans
        spans, start, end = [], hits[0], hits[0] + N
        for i in hits[1:]:
            if i <= end:
                end = i + N
            else:
                spans.append((start, end)); start, end = i, i + N
        spans.append((start, end))
        for s, e in spans:
            total += 1
            print(f"[{label}] {e - s} words copied: \"{' '.join(w[s:e])}\"")
    if total == 0:
        print(f"No passages of {N}+ identical consecutive words found.")
    else:
        print(f"\n{total} copied passage(s). Paraphrase them or quote and cite.")


if __name__ == "__main__":
    sys.exit(main())
