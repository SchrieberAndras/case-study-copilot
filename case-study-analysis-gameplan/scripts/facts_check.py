#!/usr/bin/env python3
"""Case facts completeness check (case-study-analysis-gameplan section 1.0; also run by case-study-auditor).

Usage: python3 facts_check.py <case.pdf> COBE_<Case>_CaseFacts.md
Lists every number and exhibit/endnote in the PDF text that the facts file lacks, with page and context.
Needs pdftotext (poppler-utils).

How a number counts as covered:
- page by page: a PDF number on page N is covered when the facts file carries it in a line or block that
  cites that page ("p. N", "p.N", "page N", "pp. N-M") or, if the file cites no pages at all, anywhere;
- or when it is listed under a heading "## Ignored numbers" in the facts file (page numbers, years in
  references, footnote markers: one per line or comma-separated, with a short reason if you like).
Single digits are checked only when they carry a unit sign (%, $, EUR, x) because bare 1-9 are mostly noise.
Exit code 2 when the PDF has no text layer (scanned): the check cannot run, say so instead of reporting 0.
"""
import re, subprocess, sys

if len(sys.argv) != 3:
    sys.exit(__doc__)
pdf, md = sys.argv[1], sys.argv[2]
try:
    raw = subprocess.run(["pdftotext", "-layout", pdf, "-"], capture_output=True, text=True).stdout
except FileNotFoundError:
    sys.exit("pdftotext not found: install poppler-utils")
pages = raw.split("\f")
if len(re.findall(r"\w", raw)) < 200:
    print("CANNOT RUN: the PDF has almost no text layer (scanned or image-only). "
          "Render the pages (pdftoppm -r 200 -png) and read them; this check is NOT a pass.")
    sys.exit(2)
facts = open(md, encoding="utf-8").read()

# A thousands group is exactly 3 digits and is not followed by another digit, so "1,200 2022" stays two numbers.
# A space is accepted as thousands separator only between digit groups of a single number ("1 200 000").
NUM = re.compile(r"(?<![\w.,])\d{1,3}(?:,\d{3})+(?:\.\d+)?(?!\d)"          # 1,200 / 1,200.5
                 r"|(?<![\w.,])\d{1,3}(?: \d{3}){2,}(?!\d)"                 # 1 200 000 (two+ groups only)
                 r"|(?<![\w.,])\d+(?:[.,]\d+)?(?!\d)")                      # 1200 / 7.7 / 7,7


def norm(s):
    s = s.replace(" ", "")
    if re.fullmatch(r"\d{1,3}(,\d{3})+(\.\d+)?", s):
        s = s.replace(",", "")
    elif re.fullmatch(r"\d+,\d{1,2}", s):          # decimal comma
        s = s.replace(",", ".")
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return s


def unit_near(text, m):
    return bool(re.match(r"\s?(%|x\b|percent)", text[m.end():m.end() + 9]) or re.search(r"[$€£]\s?$", text[max(0, m.start() - 2):m.start()]))


# facts file: numbers per cited page, numbers anywhere, ignored list
ign = re.search(r"^##+\s*Ignored numbers\s*$(.*?)(?=^##+\s|\Z)", facts, re.M | re.S | re.I)
ignored = {norm(n) for n in NUM.findall(ign.group(1))} if ign else set()
PAGE = re.compile(r"\bpp?\.?\s?(\d+)(?:\s?[-–]\s?(\d+))?|\bpages?\s+(\d+)(?:\s?[-–]\s?(\d+))?", re.I)
by_page, anywhere = {}, {norm(n) for n in NUM.findall(facts)}
blocks = re.split(r"\n\s*\n", facts)            # a paragraph, list or table with its page reference
for blk in blocks:
    nums = {norm(n) for n in NUM.findall(blk)}
    for m in PAGE.finditer(blk):
        a = int(m.group(1) or m.group(3)); b = int(m.group(2) or m.group(4) or a)
        for pg in range(a, min(b, a + 60) + 1):
            by_page.setdefault(pg, set()).update(nums)
cites_pages = bool(by_page)

missing, weak = [], []
for p, text in enumerate(pages, 1):
    for m in NUM.finditer(text):
        n = norm(m.group())
        if n in ignored:
            continue
        if len(n.replace(".", "")) < 2 and not unit_near(text, m):
            continue
        ctx = " ".join(text[max(0, m.start() - 40):m.end() + 40].split())
        if cites_pages and n in by_page.get(p, set()):
            continue
        if n in anywhere:
            if cites_pages and len(n.replace(".", "")) <= 2:
                weak.append((p, m.group(), ctx))   # short number found only under another page: may be a different fact
            continue
        missing.append((p, m.group(), ctx))

for kind in ("Exhibit", "Appendix", "Table", "Figure"):
    ids = lambda t: set(re.findall(rf"\b{kind}\s+(\d+|[A-H])\b", t))
    gap = ids(raw) - ids(facts)
    if gap:
        print(f"MISSING {kind.upper()}S: {sorted(gap)}")
if re.search(r"\b(End ?notes?|Notes)\s*$", raw, re.M | re.I) and not re.search(r"end ?notes?", facts, re.I):
    print("ENDNOTES: the PDF has an endnotes section; the facts file has no 'Endnotes' section")


def show(rows, label):
    seen = set()
    for p, n, ctx in rows:
        if (n, p) not in seen:
            seen.add((n, p)); print(f"{label} p.{p}  {n}  ...{ctx}...")
    return len(seen)


n_missing = show(missing, "MISSING")
n_weak = show(weak, "CHECK  ")
print(f"RESULT: {n_missing} numbers from the PDF not found in the facts file; "
      f"{n_weak} short numbers found only under a different page (check they are the same fact). "
      "Add each fact with its page, or list it under '## Ignored numbers'.")
sys.exit(1 if n_missing else 0)
