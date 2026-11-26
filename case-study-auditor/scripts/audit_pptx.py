#!/usr/bin/env python3
"""Mechanical checks for a COBE case deck.

Usage: python audit_pptx.py deck.pptx [--minutes N | --main-slides N] [--case-title "Title"]
                             [--part] [--extra notes.docx qa.docx gameplan.md] [--json out.json]

--case-title  the case's own title: its line on the Sources slide needs no URL
--part        one member's part file (case-study-ppt part mode): no title slide; skips the
              Sources, "We recommend" and slide-count checks (the merged deck gets those)

Per slide: title (title placeholder, else a shape named "title", else the largest text
starting in the top inch, so decks built from plain text boxes work too), main vs appendix,
body word count (information only: a guide for a clean look, never a rule or a blocker),
smallest font, shrink-to-fit, speaker notes, hyperlinks, number formats.
Deck level: SUBMISSION BLOCKERS (placeholders like "[link to add]", TBD, empty
table cells, sources without a link, missing "We recommend").
Judgement (logic, ideas, design quality) stays with the reviewer.
"""
import argparse
import json
import re
import sys
from pptx import Presentation

EMU_IN = 914400
MAIN_MIN_PT, APPX_MIN_PT, SOURCE_MIN_PT = 16, 14, 10
MAIN_MAX_WORDS = 40
ANSWER_MAX_WORDS = 60   # executive summary / recommendation slide: they carry the "We recommend" sentence
TITLE_ZONE_IN = 1.6     # title must start within this distance from the top
TITLE_TOP_IN = 1.0      # preferred zone: a title starts above this line; big KPI numbers in the content area
                        # (y 1.30+) must not beat a real title that sits above it
FOOTER_ZONE_IN = 0.55   # text starting this close to the bottom (y >= 6.95 in on a 7.5 in slide) = source line,
                        # tracker, slide number; matches case-study-ppt section 5 (content area ends at y 6.95)

NUM_PATTERNS = [
    # (?<![\d,.]) so a year followed by a count ("In 2024 150 stores") is not read as "2 024 150"
    (re.compile(r"(?<![\d,.])\d{1,3} \d{3}\b"), "space inside number (use comma: 29,400)"),
    (re.compile(r"[$€]\d[\d.,]*[KMB]?\s?-\s?[$€]?\d"), "hyphen in money range (use en dash $3–5M)"),
    (re.compile(r"\d, \d"), "space after comma inside number"),
    (re.compile(r"\b\d+(\.\d+)?\s?(USD|EUR|HUF|Ft)\b"), "currency after number (use symbol first, e.g. $7.7M)"),
    (re.compile(r"[$€]\s\d"), "space between currency symbol and number"),
    (re.compile(r"\d\s(K|M|B)\b"), "space before scale letter (use $1.2B)"),
    (re.compile(r"\b\d+(\.\d+)?\s?(bn|mn|mio|million|billion)\b", re.I), "scale word spelled out (use K/M/B)"),
    (re.compile(r"\d\s?-\s?\d+\s?(min|%|years?)"), "hyphen in range (use en dash 10–15)"),
]
# Brackets count as placeholders only with "to do" words; citations like "[Source: AGF 2024]" or "[1]" are fine.
PLACEHOLDER = re.compile(
    r"\[[^\]]*\b(add|insert|tbd|todo|tbc|placeholder|missing|fill in|to come|xx+)\b[^\]]*\]"
    r"|\bTBD\b|\bTODO\b|\bTBC\b|\bXXX?\b|lorem ipsum|\?\?\?|<[^>]*\b(insert|add)\b[^>]*>",
    re.I)
SOURCE_LINE = re.compile(r"^\s*sources?\s*:", re.I)
URL_TEXT = re.compile(r"(https?://\S+|www\.\S+)", re.I)
URL = re.compile(r"https?://|www\.|doi\.org", re.I)
# Optional appendix prefix ("A9 – ", "A-AN3: ") before a slide's real title.
APPX_PREFIX = r"(?:A(?:-[A-Z]{1,4})?\d+\s*[–—:.-]?\s*)?"
# Appendix starts at the first title numbered A1 / A-AN1 / A-AS12 (capital A only), or starting
# "Appendix", or "Backup" followed by a separator ("Backup: ..." / "Backup - ..."). A main-slide
# action title such as "Backup plans cut downtime by 30%" must NOT start the appendix.
APPENDIX_TITLE = re.compile(
    r"^\s*((?-i:A\d+\b|A-[A-Z]{1,4}\d+\b)|Appendix\b|Backup\s*(?:[–—:.-]|$))", re.I)
# The Sources slide is the one whose title IS "Sources", "Sources used", "References", "Bibliography"
# (optionally numbered), not any slide that mentions sources ("Revenue sources shift to digital").
SOURCES_TITLE = re.compile(
    r"^\s*" + APPX_PREFIX
    + r"(sources?(\s+used)?|references?|bibliography|works\s+cited)"
    + r"(\s*(&|and)\s*(sources?|references?|citations?))?\s*$", re.I)
# The case itself is cited without a URL. Recognised ONLY by a case number (Ivey 9B24M001,
# HBS 9-321-045, Darden UV1234), or by a case publisher together with the word "case", or by
# --case-title. The bare word "case", company names (Kellogg, Darden) and "WDI" are NOT enough:
# "The business case for X", "Kellogg Company annual report" and "World Bank WDI" need a link.
CASE_NUMBER = re.compile(r"\b9B\d{2}[A-Z]\d{3}\b|\b9-\d{3}-\d{3}\b|\bUV\d{4}\b|\(Case\s+[A-Z]{1,4}\d{3,6}\)")  # last: "(Case MH0084)"
CASE_PUBLISHER = re.compile(
    r"\bIvey\b|Harvard Business (School|Publishing)|\bHBS\b|\bHBP\b|Case Centre|\bINSEAD\b"
    r"|Darden (Graduate|Business Publishing)|UVA Darden|\bKellogg School\b|\bWDI Publishing\b|McGraw[- ]Hill", re.I)
CASE_WORD = re.compile(r"\bcase\b", re.I)
# Sentence = from "We recommend" to the first . ! ? that is not a decimal point ("$7.7M", "1.5x"),
# or to the end of the text. The old [^.!?]* pattern stopped at "$7" and hid later differences.
WE_RECOMMEND = re.compile(r"we recommend\b[^\n]*?(?:[.!?](?!\d)|$)", re.I)


def text_frames(shape):
    """Yield (shape, text_frame, is_table) for a shape, recursing into groups and tables."""
    if shape.shape_type == 6:  # group
        for s in shape.shapes:
            yield from text_frames(s)
        return
    if shape.has_text_frame:
        yield shape, shape.text_frame, False
    if getattr(shape, "has_table", False) and shape.has_table:
        for row in shape.table.rows:
            for c in row.cells:
                yield shape, c.text_frame, True


def max_font(tf):
    sizes = [r.font.size.pt for p in tf.paragraphs for r in p.runs if r.font.size is not None]
    psz = [p.font.size.pt for p in tf.paragraphs if p.font.size is not None]
    return max(sizes + psz) if (sizes or psz) else None


def find_title(slide):
    """Title placeholder if present; else a shape named "title"; else the largest-font text box that
    starts above TITLE_TOP_IN; only if none exists, the largest-font text box in the wider top zone."""
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


def empty_table_cells(slide):
    """Empty body cells in tables that hold content. A table whose body is mostly empty (75%+) is a
    layout grid or background with text boxes on top, not a table with missing content: skip it."""
    out = []
    for sh in slide.shapes:
        if getattr(sh, "has_table", False) and sh.has_table:
            t = sh.table
            body = [(ri, ci, c) for ri, row in enumerate(t.rows) if ri > 0 for ci, c in enumerate(row.cells)]
            empty = [(ri, ci) for ri, ci, c in body if not c.text_frame.text.strip()]
            if body and len(empty) / len(body) >= 0.75:
                continue
            out += [f"row {ri + 1}, col {ci + 1}" for ri, ci in empty]
    return out


def is_case_line(line, case_title=None):
    if CASE_NUMBER.search(line):
        return True
    if CASE_PUBLISHER.search(line) and CASE_WORD.search(line):
        return True
    return bool(case_title) and case_title.lower() in line.lower()


def norm_sentence(s):
    return re.sub(r"\s+", " ", s.replace("’", "'").replace("–", "-").replace("—", "-")).strip(" .").lower()


def audit(path, minutes=None, main_slides=None, case_title=None, part=False):
    prs = Presentation(path)
    slide_h = prs.slide_height / EMU_IN
    slides = []
    appendix_started = False
    for idx, slide in enumerate(prs.slides, start=1):
        title_shape = find_title(slide)
        src_box = sources_title_box(slide)
        if src_box is not None and (title_shape is None or not SOURCES_TITLE.match(title_shape.text_frame.text.strip())):
            title_shape = src_box
        title = title_shape.text_frame.text.strip().replace("\n", " ") if title_shape is not None else ""
        is_sources = bool(SOURCES_TITLE.match(title))
        if APPENDIX_TITLE.match(title) or is_sources or (idx > 1 and has_appendix_footer(slide, prs.slide_height)):  # the Sources slide closes the appendix
            appendix_started = True
        section = "appendix" if appendix_started else ("title" if idx == 1 and not part else "main")

        body_words, all_text, small, links, unclickable = 0, [], [], [], []
        autofit = False
        for sh in slide.shapes:
            for shp, tf, in_table in text_frames(sh):
                body = tf._txBody.find("{http://schemas.openxmlformats.org/drawingml/2006/main}bodyPr")
                if body is not None and body.find("{http://schemas.openxmlformats.org/drawingml/2006/main}normAutofit") is not None:
                    autofit = True
                is_title = title_shape is not None and shp.shape_id == title_shape.shape_id and not in_table
                top = (shp.top or 0) / EMU_IN
                # footer = source line, tracker, slide number: the bottom band, or a line starting "Source:"
                # (case-study-ppt section 5 puts the source line at y 6.70, above the tracker)
                is_footer = (not in_table) and (top > slide_h - FOOTER_ZONE_IN or SOURCE_LINE.match(tf.text)
                                                or (shp.name or "").startswith(("source", "page-number")))
                for p in tf.paragraphs:
                    psize = p.font.size.pt if p.font.size is not None else None
                    for r in p.runs:
                        t = r.text.strip()
                        if not t:
                            continue
                        all_text.append(t)
                        if not is_title and not is_footer:
                            body_words += len(t.split())
                        sz = r.font.size.pt if r.font.size is not None else psize
                        floor = SOURCE_MIN_PT if (is_sources or is_footer) else (APPX_MIN_PT if appendix_started else MAIN_MIN_PT)
                        if (shp.name or "").startswith(("tracker", "axis-label", "chart-label", "legend", "footnote")):
                            floor = min(floor, APPX_MIN_PT)   # case-study-ppt 4a: tracker, chart and axis labels 14pt
                        if sz is not None and sz < floor and not re.fullmatch(r"\d+", t):
                            small.append((sz, t[:40]))
                        if r.hyperlink is not None and r.hyperlink.address:
                            links.append(r.hyperlink.address)
                        elif URL_TEXT.search(t):
                            unclickable.append(URL_TEXT.search(t).group(0)[:60])
        text = " ".join(all_text)
        # one text frame at a time: joining frames let a sentence without a full stop run on into the next box
        rec_sentences = [norm_sentence(m.group(0)) for sh in slide.shapes for _, tf, _ in text_frames(sh)
                         for m in WE_RECOMMEND.finditer(tf.text.replace("\v", "\n"))]

        num_issues = [f"{msg}: '{m.group(0)}'" for rx, msg in NUM_PATTERNS for m in [rx.search(text)] if m]
        placeholders = sorted({m.group(0) for m in PLACEHOLDER.finditer(text)})
        empties = empty_table_cells(slide)
        unlinked_sources = []
        if is_sources:
            for sh in slide.shapes:
                for shp, tf, in_tbl in text_frames(sh):
                    # footer band (Appendix label, tracker, slide number) and the title box are not source entries
                    if not in_tbl and (shp.top or 0) / EMU_IN > slide_h - FOOTER_ZONE_IN:
                        continue
                    if APPENDIX_FOOTER.match(tf.text) or (title_shape is not None and shp.shape_id == title_shape.shape_id):
                        continue
                    for p in tf.paragraphs:
                        line = "".join(r.text for r in p.runs).strip()
                        has_link = any(r.hyperlink is not None and r.hyperlink.address for r in p.runs)
                        is_case_itself = is_case_line(line, case_title)  # the case PDF has no URL
                        if (line and line != title and not re.fullmatch(r"\d+", line)
                                and not is_case_itself and not URL.search(line) and not has_link):
                            unlinked_sources.append(line[:80])
        notes = slide.notes_slide.notes_text_frame.text.strip() if slide.has_notes_slide else ""
        word_limit = ANSWER_MAX_WORDS if "we recommend" in text.lower() else MAIN_MAX_WORDS
        slides.append({
            "slide": idx, "section": section, "title": title, "title_chars": len(title),
            "title_found": title_shape is not None, "is_sources": is_sources,
            "body_words": body_words,
            "word_limit": word_limit,
            "over_word_limit": section == "main" and body_words > word_limit,
            "text_below_minimum": sorted(set(small))[:5],
            "shrink_autofit": autofit, "has_speaker_notes": bool(notes),
            "hyperlinks": links, "number_format_issues": num_issues,
            "placeholders": placeholders, "empty_table_cells": empties,
            "sources_without_link": unlinked_sources,
            "unclickable_urls": unclickable,
            "has_we_recommend": "we recommend" in text.lower(),
            "we_recommend_sentences": rec_sentences,
            "notes_placeholders": sorted({m.group(0) for m in PLACEHOLDER.finditer(notes)}),
        })

    # Build sequences (case-study-ppt: progressive "Providing -> In order to" slides) repeat the same title on
    # consecutive main slides; they are presented as ONE slide, so they count once for the slide-count check.
    prev_title = None
    for s in slides:
        s["build_step"] = bool(s["section"] == "main" and s["title"] and s["title"] == prev_title)
        prev_title = s["title"] if s["section"] == "main" else None
    main = [s for s in slides if s["section"] == "main" and not s["build_step"]]
    blockers = []
    for s in slides:
        if s["placeholders"]:
            blockers.append(f"slide {s['slide']}: placeholder text {s['placeholders']}")
        if s["notes_placeholders"]:
            blockers.append(f"slide {s['slide']} notes: placeholder text {s['notes_placeholders']}")
        if s["empty_table_cells"]:
            blockers.append(f"slide {s['slide']}: empty table cells {s['empty_table_cells'][:5]}")
        if s["sources_without_link"]:
            blockers.append(f"slide {s['slide']}: {len(s['sources_without_link'])} source(s) without a link: {s['sources_without_link'][:3]}")
    for s in slides:
        if s["unclickable_urls"]:
            blockers.append(f"slide {s['slide']}: {len(s['unclickable_urls'])} URL(s) typed as text, not clickable links: {s['unclickable_urls'][:2]}")
    if not part:
        if not any(s["is_sources"] for s in slides):
            blockers.append("no Sources slide found")
        if not any(s["has_we_recommend"] for s in slides):
            blockers.append("no 'We recommend ...' sentence anywhere in the deck")
    # word-for-word check: first vs last slide carrying "We recommend" (exec summary vs closing slide)
    # main slides only: an appendix title such as "A1 - why we recommend hubs" is not the closing slide
    rec = [s for s in slides if s["we_recommend_sentences"] and s["section"] != "appendix"]
    we_rec_check = None
    if not part and rec:
        first, last = rec[0], rec[-1]
        if first is last:
            we_rec_check = f"only slide {first['slide']} carries 'We recommend' (exec summary and closing slide should both)"
        elif first["we_recommend_sentences"][0] != last["we_recommend_sentences"][0]:
            we_rec_check = (f"MISMATCH slide {first['slide']} vs slide {last['slide']}: "
                            f"'{first['we_recommend_sentences'][0]}' vs '{last['we_recommend_sentences'][0]}'")
        else:
            we_rec_check = f"match (slide {first['slide']} = slide {last['slide']})"
    deck = {
        "part_mode": part,
        "we_recommend_check": we_rec_check,
        "file": path, "slide_count": len(slides), "main_slides": len(main),
        "build_step_slides": [s["slide"] for s in slides if s.get("build_step")],
        "appendix_slides": sum(1 for s in slides if s["section"] == "appendix"),
        "slides_without_detected_title": [s["slide"] for s in slides if not s["title_found"] and s["section"] != "title"],
        "slides_with_notes": [s["slide"] for s in slides if s["has_speaker_notes"]],
        "we_recommend_slides": [s["slide"] for s in slides if s["has_we_recommend"]],
        "all_links": sorted({l for s in slides for l in s["hyperlinks"]}),
        "long_titles": [s["slide"] for s in slides if s["title_chars"] > 60],
        "submission_blockers": blockers,
        "ready_to_submit_mechanically": not blockers,
    }
    if part:
        pass  # slide count is checked on the merged deck
    elif main_slides is not None:
        deck["required_main_slides"] = main_slides
        deck["main_slide_count_ok"] = len(main) == main_slides
    elif minutes:
        # same sizing as case-study-ppt section 0: 10 min -> 7-8, 15 -> 10-12, 20 -> 13-16
        lo, hi = round(minutes / 1.5), round(minutes / 1.25)
        deck["expected_main_slides"] = f"{lo}-{hi}"
        deck["main_slide_count_ok"] = lo <= len(main) <= hi
    return {"deck": deck, "slides": slides}


def read_lines(path):
    """Lines of text from .docx / .pdf / .md / .txt (notes, Q&A, game plan files; overlap_check.py reuses it)."""
    p = path.lower()
    if p.endswith(".docx"):
        import docx
        d = docx.Document(path)
        lines = [par.text for par in d.paragraphs]
        for t in d.tables:
            for row in t.rows:
                lines += [c.text for c in row.cells]
        return lines
    if p.endswith(".pdf"):
        import subprocess
        return subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True).stdout.splitlines()
    with open(path, encoding="utf-8", errors="ignore") as f:
        return f.read().splitlines()


def scan_extra(paths):
    """Placeholder scan of companion files (speaker notes, Q&A, game plan)."""
    blockers = []
    for path in paths:
        hits = [(i + 1, m.group(0)) for i, line in enumerate(read_lines(path)) for m in PLACEHOLDER.finditer(line)]
        if hits:
            blockers.append(f"{path}: placeholder text {[h for _, h in hits[:5]]} (lines {[i for i, _ in hits[:5]]})")
    return blockers


def audit_pdf(path, main_slides=None, case_title=None, part=False):
    """PDF deck: text-level checks only (placeholders, sources without links, 'We recommend').
    Fonts, word limits and layout must be checked visually."""
    import subprocess
    from pypdf import PdfReader
    reader = PdfReader(path)
    slides, blockers = [], []
    for i, page in enumerate(reader.pages, start=1):
        txt = subprocess.run(["pdftotext", "-layout", "-f", str(i), "-l", str(i), path, "-"],
                             capture_output=True, text=True).stdout
        lines = [l.strip() for l in txt.splitlines() if l.strip()]
        title = lines[0] if lines else ""
        annots = page.get("/Annots") or []
        link_count = 0
        for a in annots:
            try:
                if a.get_object().get("/Subtype") == "/Link":
                    link_count += 1
            except Exception:
                pass
        ph = sorted({m.group(0) for m in PLACEHOLDER.finditer(txt)})
        is_sources = bool(SOURCES_TITLE.match(title))
        unlinked = []
        if is_sources:
            # join wrapped lines into entries: a new entry starts with a bullet or "1." / "[1]"
            entries, cur = [], ""
            for l in lines[1:]:
                if re.fullmatch(r"\d+", l):
                    continue
                if re.match(r"^(•|-|–|\*|\d+[.)]|\[\d+\])\s*", l) or not cur:
                    if cur:
                        entries.append(cur)
                    cur = l
                else:
                    cur += " " + l
            if cur:
                entries.append(cur)
            for e in entries:
                if is_case_line(e, case_title):
                    continue
                if not URL.search(e):
                    unlinked.append(e[:80])
        if ph:
            blockers.append(f"page {i}: placeholder text {ph}")
        if unlinked:
            blockers.append(f"page {i}: source line(s) without a URL (check, may be wrapped lines): {unlinked[:3]}")
        if is_sources and URL.search(txt) and link_count == 0:
            blockers.append(f"page {i}: URLs present but none clickable in the PDF")
        slides.append({"slide": i, "title": title[:80], "words": len(txt.split()), "is_sources": is_sources,
                       "has_we_recommend": "we recommend" in txt.lower(), "links": link_count})
    if not part:
        if not any(s["is_sources"] for s in slides):
            blockers.append("no Sources page found (check visually)")
        if not any(s["has_we_recommend"] for s in slides):
            blockers.append("no 'We recommend ...' sentence anywhere in the deck")
    deck = {"file": path, "slide_count": len(slides), "pdf_mode": True,
            "submission_blockers": blockers, "ready_to_submit_mechanically": not blockers}
    return {"deck": deck, "slides": slides}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pptx", help=".pptx deck, or a .pdf export of a deck (text checks only)")
    ap.add_argument("--minutes", type=float)
    ap.add_argument("--main-slides", type=int, help="fixed main-slide count from the brief")
    ap.add_argument("--case-title", help="the case's title; its Sources line needs no URL")
    ap.add_argument("--part", action="store_true", help="one member's part file: skip Sources, We recommend, slide-count checks")
    ap.add_argument("--extra", nargs="*", default=[], help="notes / Q&A / game plan files to scan for placeholders")
    ap.add_argument("--json")
    a = ap.parse_args()
    if a.pptx.lower().endswith(".pdf"):
        res = audit_pdf(a.pptx, a.main_slides, a.case_title, a.part)
        res["deck"]["submission_blockers"] += scan_extra(a.extra)
        res["deck"]["ready_to_submit_mechanically"] = not res["deck"]["submission_blockers"]
        if a.json:
            with open(a.json, "w") as f:
                json.dump(res, f, indent=2, ensure_ascii=False)
        d = res["deck"]
        print("PDF mode: text checks only - check fonts, word counts and layout on the rendered pages.")
        if d["submission_blockers"]:
            print("=" * 60 + "\nNOT READY TO SUBMIT - blockers found:")
            print("\n".join(f"  - {b}" for b in d["submission_blockers"]))
            print("=" * 60)
        else:
            print("No mechanical submission blockers found.")
        for s in res["slides"]:
            print(f"[p{s['slide']:>2}] {s['title'][:65]!r} ({s['words']} w, {s['links']} links)")
        return
    res = audit(a.pptx, a.minutes, a.main_slides, a.case_title, a.part)
    res["deck"]["submission_blockers"] += scan_extra(a.extra)
    res["deck"]["ready_to_submit_mechanically"] = not res["deck"]["submission_blockers"]
    if a.json:
        with open(a.json, "w") as f:
            json.dump(res, f, indent=2, ensure_ascii=False)
    d = res["deck"]
    out = []
    if d["submission_blockers"]:
        out.append("=" * 60)
        out.append("NOT READY TO SUBMIT - blockers found:")
        out += [f"  - {b}" for b in d["submission_blockers"]]
        out.append("=" * 60)
    else:
        out.append("No mechanical submission blockers found.")
    out.append(f"Deck: {d['slide_count']} slides | main: {d['main_slides']} | appendix: {d['appendix_slides']}")
    if d.get("build_step_slides"):
        out.append(f"Build steps counted with the slide before them (same title): {d['build_step_slides']}")
    if "main_slide_count_ok" in d:
        target = d.get("required_main_slides", d.get("expected_main_slides"))
        out.append(f"Main-slide target {target} -> {'OK' if d['main_slide_count_ok'] else 'MISMATCH'}")
    if d["part_mode"]:
        out.append("Part mode: Sources, 'We recommend' and slide-count checks skipped (run them on the merged deck)")
    out.append(f"'We recommend' on slides: {d['we_recommend_slides'] or 'NONE'}")
    if d["we_recommend_check"]:
        out.append(f"'We recommend' word-for-word check: {d['we_recommend_check']}")
    if d["slides_without_detected_title"]:
        out.append(f"No title detected on slides: {d['slides_without_detected_title']} (check visually)")
    if d["slides_with_notes"]:
        out.append(f"Speaker notes inside the .pptx on slides: {d['slides_with_notes']} (house rule: none; "
                   "move them to the notes .docx, then remove with the fixer's remove_notes helper)")
    if d["long_titles"]:
        out.append(f"Titles likely over one line: {d['long_titles']}")
    out.append(f"Links found: {len(d['all_links'])}")
    out.append("")
    for s in res["slides"]:
        flags = []
        if s["over_word_limit"]:
            flags.append(f"note: {s['body_words']} words (guide {s['word_limit']}; judge the look, not a rule)")
        if s["text_below_minimum"]:
            flags.append("small text: " + "; ".join(f"{sz}pt '{t}'" for sz, t in s["text_below_minimum"]))
        if s["shrink_autofit"]:
            flags.append("shrink-to-fit on")
        if s["number_format_issues"]:
            flags.append("numbers: " + "; ".join(s["number_format_issues"]))
        out.append(f"[{s['slide']:>2} {s['section']:<8}] {s['title'][:65]!r} ({s['body_words']} w): {' | '.join(flags) or 'ok'}")
    try:
        print("\n".join(out))
    except BrokenPipeError:
        pass


if __name__ == "__main__":
    sys.exit(main())
