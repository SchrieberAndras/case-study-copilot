#!/usr/bin/env python3
"""Slide slop detector: fixed rules (no AI judgement) for design habits that make a deck look AI-made or careless.
Idea taken from Impeccable's slop detector (web UI), rewritten for .pptx decks and the COBE house style.

    python slop_check.py deck.pptx [--accent none|HEX] [--json out.json]

Every finding has a priority:
  P0  unreadable: must be fixed before submitting
  P1  clearly wrong against the house style (gradient, 3-D, emoji, extra accent hue, low contrast)
  P2  reads as AI slop or template work (cards everywhere, effects, slop words, banner restating the title)
  P3  polish: fine alone, a problem when several stack up
Findings are leads: confirm each on the rendered slide. The house style (case-study-ppt, design-rules.md) always
wins: anything it asks for (accent bar, icon badges, kicker, phase tracker, check/cross marks) is never flagged.
check_deck.py runs these rules too and prints them after its own checks.
"""
import argparse, colorsys, json, os, re, sys
from pptx import Presentation

EMU = 914400
NS = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main",
      "c": "http://schemas.openxmlformats.org/drawingml/2006/chart",
      "p": "http://schemas.openxmlformats.org/presentationml/2006/main"}

try:  # same main/appendix/title detection as the auditor and check_deck.py
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "case-study-auditor", "scripts"))
    from audit_pptx import find_title, has_appendix_footer, APPENDIX_TITLE, SOURCES_TITLE
except Exception:  # auditor not installed: simplified fallback
    APPENDIX_TITLE = re.compile(r"^\s*((?-i:A\d+\b|A-[A-Z]{1,4}\d+\b)|Appendix\b|Backup\s*(?:[–—:.-]|$))", re.I)
    SOURCES_TITLE = re.compile(r"^\s*(?:A\d+\s*[–—:.-]?\s*)?(sources?(\s+used)?|references?|bibliography)\s*$", re.I)

    def find_title(slide):
        if slide.shapes.title is not None and slide.shapes.title.text_frame.text.strip():
            return slide.shapes.title
        best, key = None, None
        for sh in slide.shapes:
            if sh.has_text_frame and sh.text_frame.text.strip() and sh.top is not None and sh.top / EMU <= 1.6:
                sz = max([r.font.size.pt for p in sh.text_frame.paragraphs for r in p.runs if r.font.size] or [0])
                if sz >= 20 and (key is None or (sz, -sh.top) > key):
                    best, key = sh, (sz, -sh.top)
        return best

    def has_appendix_footer(slide, h):
        return any(sh.has_text_frame and sh.top is not None and sh.top > 0.85 * h
                   and re.match(r"^\s*(appendi(x|ces)?|backup)\s*$", sh.text_frame.text, re.I) for sh in slide.shapes)

# ---------- fix hints (the fixer's design moves, fix-playbook.md "Design moves") ----------
HINT = {
    "contrast": "typeset: change the text to INK or white (whichever reaches 4.5:1) or the box to a lighter/darker role",
    "gradient": "quieter: replace with a flat PRIMARY, NEUTRAL or TINT fill",
    "3d": "quieter: flat 2-D shape or chart",
    "emoji": "clarify: remove the emoji; use a Lucide line icon with a label if a visual is needed",
    "extra-hue": "quieter: recolour to the five palette roles (plus the Style line's ACCENT, if any)",
    "effects": "quieter: remove shadow / glow / soft edges / reflection",
    "cards-everywhere": "distill / layout: rebuild some slides as a chart, process, comparison or big number",
    "icon-card-row": "layout: rebuild one or two of those slides with another pattern (chart, process, comparison)",
    "same-layout": "layout: give one of the two slides a different pattern (case-study-ppt 4c)",
    "banner-restates-title": "clarify: write the implication (the so-what), not the title again",
    "too-many-bullets": "distill: max 3 bullets per box; move the rest to the appendix or notes",
    "paragraph-in-box": "distill: phrases, not paragraphs; move narration to the notes",
    "slop-word": "clarify: replace with a concrete claim or number",
    "sparkle-icon": "clarify: pick a concrete icon (store, users, trending-up, shield-check)",
    "chart-gridlines": "polish: remove gridlines; data labels carry the values",
    "pie-chart": "layout: bar chart, or a donut with max 4 slices",
    "rainbow-chart": "quieter: one highlight (PRIMARY), the rest NEUTRAL",
    "single-series-legend": "polish: delete the legend; the chart title or label names the series",
    "interpuncts": "polish: use line breaks or a short list instead of dots between words",
    "arrows-everywhere": "polish: arrows only where something leads to something",
    "pill-above-title": "quieter: drop the pill; the tracker already shows the section",
    "left-borders": "polish: drop the coloured left edges; one emphasis device per slide",
    "two-word-sentences": "clarify: write full action titles / sentences",
    "full-bleed-image": "layout: smaller, purposeful image (full-bleed only on the title slide)",
}


def _walk(shapes):
    for sh in shapes:
        if sh.shape_type == 6:
            yield from _walk(sh.shapes)
        else:
            yield sh


def _srgb(el):
    """First srgbClr value directly in a solidFill element."""
    if el is None:
        return None
    c = el.find("a:srgbClr", NS)
    return c.get("val").upper() if c is not None else None


def _sppr(sh):
    return sh._element.find(".//p:spPr", NS) if sh._element.tag.endswith("}sp") or sh._element.tag.endswith("}cxnSp") \
        else sh._element.find("p:spPr", NS)


def fill_hex(sh):
    sp = _sppr(sh)
    return _srgb(sp.find("a:solidFill", NS)) if sp is not None else None


def line_hex(sh):
    sp = _sppr(sh)
    if sp is None:
        return None
    ln = sp.find("a:ln", NS)
    return _srgb(ln.find("a:solidFill", NS)) if ln is not None else None


def _grad(sh):
    sp = _sppr(sh)
    return sp is not None and sp.find("a:gradFill", NS) is not None


def prst(sh):
    sp = _sppr(sh)
    g = sp.find("a:prstGeom", NS) if sp is not None else None
    return g.get("prst") if g is not None else None


def run_colors(tf):
    out = []
    for p in tf.paragraphs:
        for r in p.runs:
            rpr = r._r.find("a:rPr", NS)
            hx = _srgb(rpr.find("a:solidFill", NS)) if rpr is not None else None
            out.append((hx, r.font.size.pt if r.font.size else None, bool(r.font.bold), r.text))
    return out


def lum(hx):
    def ch(v):
        v = v / 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (int(hx[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(b)


def contrast(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def hue_of(hx):
    r, g, b = (int(hx[i:i + 2], 16) / 255 for i in (0, 2, 4))
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    if s < 0.30 or l < 0.12 or l > 0.92:
        return None  # greys, near-black, near-white and soft tints carry no accent hue
    return h * 360


def box(sh):
    return (sh.left / EMU, sh.top / EMU, sh.width / EMU, sh.height / EMU)


def inside(inner, outer, pad=0.05):
    x, y, w, h = inner
    cx, cy = x + w / 2, y + h / 2
    ox, oy, ow, oh = outer
    return ox - pad <= cx <= ox + ow + pad and oy - pad <= cy <= oy + oh + pad


def slide_bg(slide):
    for el in (slide._element, slide.slide_layout._element, slide.slide_layout.slide_master._element):
        bg = el.find(".//p:bg/p:bgPr", NS)
        if bg is not None:
            if bg.find("a:gradFill", NS) is not None:
                return "GRADIENT"
            hx = _srgb(bg.find("a:solidFill", NS))
            if hx:
                return hx
    return "FFFFFF"


EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-⛿⭐⭕✀-✒✙-➿]")
SLOP_WORDS = re.compile(
    r"\b(quiet(ly)?|seamless(ly)?|elevat(e|es|ed|ing)|unlock(s|ed|ing)?|supercharg\w*|effortless(ly)?|"
    r"game[- ]chang\w+|next[- ]level|cutting[- ]edge|revolutioni[sz]\w*|revolutionary|delv(e|es|ing)|"
    r"leverag(e|es|ed|ing)|synerg(y|ies)|real (impact|results|value|difference|change))\b", re.I)
TWO_WORDS = re.compile(r"(?:^|(?<=[.!?]\s))[A-Z][a-z']+\s+[a-z']+\.(?=\s|$)")
SPARKLE = re.compile(r"icon:.*(sparkle|stars?\b|wand|magic)", re.I)


def scan(prs, accent=None, primary=None):
    """Return a list of findings: dicts with p (0-3), slide (int or 'deck'), rule, msg, fix."""
    W, H = prs.slide_width / EMU, prs.slide_height / EMU
    F = []

    def add(p, n, rule, msg):
        F.append({"p": p, "slide": n, "rule": rule, "msg": msg, "fix": HINT.get(rule, "")})

    hue_slides = {}            # hue bucket -> set of slides
    hue_hex = {}
    main_with_cards, main_slides, rounded, card_total = [], [], 0, 0
    two_word_hits = []
    icon_rows = []
    prev_sig = None
    appendix = False

    for n, s in enumerate(prs.slides, 1):
        tsh = find_title(s)
        title = tsh.text_frame.text.strip().replace("\n", " ") if tsh is not None else ""
        if APPENDIX_TITLE.match(title) or SOURCES_TITLE.match(title) or (n > 1 and has_appendix_footer(s, prs.slide_height)):
            appendix = True
        is_main = not appendix and n > 1
        if is_main:
            main_slides.append(n)
        bg = slide_bg(s)
        if bg == "GRADIENT":
            add(1, n, "gradient", "gradient slide background")
            bg = "FFFFFF"
        shapes = list(_walk(s.shapes))

        # ---- cards: filled or outlined boxes big enough to hold content
        cards = []
        for sh in shapes:
            if sh.shape_type != 1 or sh.width is None:
                continue
            x, y, w, h = box(sh)
            if w >= 1.2 and h >= 0.9 and w < W - 1.0 and (fill_hex(sh) or line_hex(sh)) and y > 1.0:
                cards.append(sh)
        card_total += len(cards)
        rounded += sum(1 for c in cards if (prst(c) or "").startswith("roundRect"))
        rows = {}
        for c in cards:
            x, y, w, h = box(c)
            rows.setdefault((round(y * 10), round(w * 10), round(h * 10)), []).append(c)
        card_rows = [r for r in rows.values() if len(r) >= 3]
        longest = max((len(r) for r in card_rows), default=0)
        if is_main and card_rows:
            main_with_cards.append(n)

        # icons sitting in the top of every card of a row
        pics = [sh for sh in shapes if sh.shape_type == 13]
        for r in card_rows:
            topped = 0
            for c in r:
                cx, cy, cw, ch_ = box(c)
                if any(inside(box(pc), (cx, cy, cw, ch_ * 0.45)) and box(pc)[2] < 1.0 for pc in pics):
                    topped += 1
            if topped == len(r) and is_main and n not in icon_rows:
                icon_rows.append(n)

        # ---- per-shape rules
        for idx, sh in enumerate(shapes):
            el = sh._element
            sp = _sppr(sh)
            nm = sh.name or ""
            if sp is not None and sp.find("a:gradFill", NS) is not None and sh.shape_type != 13:
                add(1, n, "gradient", f"gradient fill on '{nm}'")
            if el.find(".//a:scene3d", NS) is not None or el.find(".//a:sp3d", NS) is not None:
                add(1, n, "3d", f"3-D effect on '{nm}'")
            eff = sp.find("a:effectLst", NS) if sp is not None else None
            if eff is not None and len(eff):
                kinds = sorted({c.tag.split('}')[1] for c in eff})
                add(2, n, "effects", f"{', '.join(kinds)} on '{nm}'")
            if SPARKLE.search(nm):
                add(2, n, "sparkle-icon", f"decorative icon '{nm}'")
            if sh.shape_type == 13 and n > 1:
                x, y, w, h = box(sh)
                if w * h >= 0.6 * W * H:
                    add(3, n, "full-bleed-image", f"image '{nm}' covers {w * h / (W * H):.0%} of the slide")
            # colours for the hue census (charts and pictures excluded)
            for hx in (fill_hex(sh), line_hex(sh)):
                hu = hue_of(hx) if hx else None
                if hu is not None:
                    b = int(hu // 20) % 18
                    hue_slides.setdefault(b, set()).add(n)
                    hue_hex.setdefault(b, set()).add(hx)
            if getattr(sh, "has_chart", False) and sh.has_chart:
                cx = sh.chart._chartSpace
                if cx.find(".//c:majorGridlines", NS) is not None:
                    add(2, n, "chart-gridlines", f"gridlines in chart '{nm}'")
                if cx.find(".//c:view3D", NS) is not None or any(cx.find(f".//c:{t}", NS) is not None for t in
                                                              ("bar3DChart", "pie3DChart", "line3DChart", "area3DChart")):
                    add(1, n, "3d", f"3-D chart '{nm}'")
                if cx.find(".//c:pieChart", NS) is not None:
                    add(2, n, "pie-chart", f"pie chart '{nm}'")
                vc = cx.find(".//c:barChart/c:varyColors", NS)
                if vc is not None and vc.get("val") in ("1", "true"):
                    add(2, n, "rainbow-chart", f"'vary colours by point' on bar chart '{nm}'")
                if cx.find(".//c:legend", NS) is not None and len(cx.findall(".//c:ser", NS)) == 1:
                    add(3, n, "single-series-legend", f"legend on a one-series chart '{nm}'")
            if not (sh.has_text_frame and sh.text_frame.text.strip()):
                continue
            txt = sh.text_frame.text
            is_title = tsh is not None and sh.shape_id == tsh.shape_id
            if EMOJI.search(txt):
                add(1, n, "emoji", f"emoji in '{txt.strip()[:40]}'")
            for m in SLOP_WORDS.finditer(txt):
                add(2, n, "slop-word", f"'{m.group(0)}' in '{txt.strip()[:50]}'")
            # contrast: explicit text colour against the box behind it
            x, y, w, h = box(sh) if sh.width is not None else (0, 0, 0, 0)
            back = fill_hex(sh)
            if not back:  # topmost filled shape below this one in z-order that holds the text's centre
                behind = [o for o in shapes[:idx] if o.shape_type == 1 and o.width is not None
                          and (fill_hex(o) or _grad(o)) and inside((x, y, w, h), box(o))]
                back = (None if _grad(behind[-1]) else fill_hex(behind[-1])) if behind else bg
            if back is None:
                back_unknown = True
            else:
                back_unknown = False
            for hx, size, bold, rt in run_colors(sh.text_frame):
                if back_unknown or not hx or not rt.strip():
                    continue
                cr = contrast(hx, back)
                large = (size or 0) >= 24 or ((size or 0) >= 18 and bold)
                need = 3.0 if large else 4.5
                if cr < (1.5 if large else 2.0):
                    add(0, n, "contrast", f"text #{hx} on #{back} = {cr:.1f}:1 (unreadable): '{rt.strip()[:30]}'")
                    break
                if cr < need:
                    lvl = 1 if cr < need - 0.5 else 2
                    add(lvl, n, "contrast", f"text #{hx} on #{back} = {cr:.1f}:1 (needs {need:g}:1"
                        + (", borderline" if lvl == 2 else "") + f"): '{rt.strip()[:30]}'")
                    break
                hu = hue_of(hx)
                if hu is not None:
                    b = int(hu // 20) % 18
                    hue_slides.setdefault(b, set()).add(n)
                    hue_hex.setdefault(b, set()).add(hx)
            if not is_main:
                continue
            # text inside a card (or a filled / outlined text box)
            in_card = bool(fill_hex(sh) or line_hex(sh)) or any(c is not sh and inside((x, y, w, h), box(c)) for c in cards)
            paras = [p.text.strip() for p in sh.text_frame.paragraphs if p.text.strip()]
            if in_card and not is_title:
                if len(paras) > 3:
                    add(2, n, "too-many-bullets", f"{len(paras)} lines/bullets in one box: '{paras[0][:40]}'")
                long_p = [p for p in paras if len(p.split()) > 30]
                if long_p:
                    add(2, n, "paragraph-in-box", f"{len(long_p[0].split())}-word paragraph in a box: '{long_p[0][:40]}'")
            mids = len(re.findall(r"\S\s+[·•]\s+\S", txt))
            if mids >= 3:
                add(3, n, "interpuncts", f"{mids} dots between words in '{txt.strip()[:40]}'")
            # pill above the headline: a short label on a small rounded shape in the title zone
            if y < 1.3 and not is_title and len(txt.split()) <= 4:
                pill = [o for o in shapes if o.shape_type == 1 and o.width is not None and (prst(o) or "").startswith("roundRect")
                        and box(o)[3] < 0.55 and box(o)[2] < 3 and box(o)[1] < 1.3 and (o is sh or inside((x, y, w, h), box(o)))]
                if pill:
                    add(3, n, "pill-above-title", f"pill label '{txt.strip()}' in the title zone")
            # banner that restates the title
            if title and y > 5.4 and w > 8 and len(txt.split()) >= 4 and not is_title:
                cw = lambda t: {w_.lower().strip(".,:;%") for w_ in t.split() if len(w_) > 3}
                a_, b_ = cw(title), cw(txt)
                if a_ and b_ and len(a_ & b_) / len(a_ | b_) >= 0.5:
                    add(2, n, "banner-restates-title", f"banner '{txt.strip()[:50]}' repeats the title")
            if is_title or (max([r.font.size.pt for p in sh.text_frame.paragraphs for r in p.runs if r.font.size] or [0]) >= 20):
                two_word_hits += [(n, m.group(0)) for m in TWO_WORDS.finditer(txt)]

        if is_main:
            arrows = sum(1 for sh in shapes if sh.has_text_frame for p in sh.text_frame.paragraphs
                         if re.match(r"^\s*(→|->|➜|➔)", p.text) or re.search(r"(→|->|➜|➔)\s*$", p.text))
            if arrows >= 3:
                add(3, n, "arrows-everywhere", f"{arrows} lines start or end with an arrow")
            borders = 0
            for sh in shapes:
                if sh.shape_type == 1 and sh.width is not None:
                    x, y, w, h = box(sh)
                    if w <= 0.12 and h >= 0.5 and y > 1.2 and fill_hex(sh) and any(abs(box(c)[0] - (x + w)) < 0.12 or abs(box(c)[0] - x) < 0.05 for c in cards):
                        borders += 1
            if borders >= 2:
                add(3, n, "left-borders", f"{borders} cards with a coloured left edge")
            # layout signature for back-to-back repeats
            charts = sum(1 for sh in shapes if getattr(sh, "has_chart", False) and sh.has_chart)
            tables = sum(1 for sh in shapes if getattr(sh, "has_table", False) and sh.has_table)
            sig = (charts, tables, longest, len(card_rows))
            if prev_sig is not None and sig == prev_sig[1] and sum(sig) > 0:
                p = 2 if longest >= 3 else 3
                add(p, n, "same-layout", f"same layout as slide {prev_sig[0]} ({charts} chart, {tables} table, card row of {longest})")
            prev_sig = (n, sig)
        else:
            prev_sig = None

    # ---- deck-level rules
    if len(main_slides) >= 4 and len(main_with_cards) >= 0.6 * len(main_slides):
        add(2, "deck", "cards-everywhere",
            f"{len(main_with_cards)} of {len(main_slides)} main slides are rows of equal cards (slides {', '.join(map(str, main_with_cards))})")
    if len(icon_rows) >= 3:
        add(3, "deck", "icon-card-row", f"the same icon-topped card row on {len(icon_rows)} main slides "
            f"({', '.join(map(str, icon_rows))}); the house style allows it, but not as the default pattern")
    if len(two_word_hits) >= 3:
        add(3, "deck", "two-word-sentences", "two-word sentences: " + "; ".join(f"S{n} '{t}'" for n, t in two_word_hits[:5]))
    if hue_slides:
        ranked = sorted(hue_slides.items(), key=lambda kv: -len(kv[1]))
        # merge neighbouring 20-degree buckets into one hue family
        fams = []
        for b, sl in ranked:
            for f in fams:
                if any(min(abs(b - fb), 18 - abs(b - fb)) <= 1 for fb in f["b"]):
                    f["b"].add(b); f["s"] |= sl; f["hex"] |= hue_hex[b]; break
            else:
                fams.append({"b": {b}, "s": set(sl), "hex": set(hue_hex[b])})
        fams.sort(key=lambda f: -len(f["s"]))

        def near(hx):
            hu = hue_of(hx.lstrip("#").upper()) if hx else None
            if hu is None:
                return lambda f: False
            hb = int(hu // 20) % 18
            return lambda f: any(min(abs(hb - fb), 18 - abs(hb - fb)) <= 1 for fb in f["b"])
        is_p = near(primary)
        is_a = near(accent if accent and accent.lower() != "none" else None)
        allowed = 1 if (accent or "").lower() == "none" else 2
        if primary:  # known PRIMARY first, then the named ACCENT, then the rest by how often they appear
            fams.sort(key=lambda f: (0 if is_p(f) else 1 if is_a(f) else 2, -len(f["s"])))
            if accent is None:
                allowed = 2
        elif accent and accent.lower() != "none":
            fams.sort(key=lambda f: (0 if f is fams[0] else 1 if is_a(f) else 2, -len(f["s"])))
        for f in fams[allowed:]:
            sl = sorted(f["s"])
            p = 3 if len(sl) == 1 else 1
            add(p, "deck", "extra-hue", f"colour family {', '.join('#' + h for h in sorted(f['hex'])[:4])} on slides "
                f"{', '.join(map(str, sl))} is outside the palette roles" + (" (one slide: fine if it carries meaning, e.g. a risk scale)" if p == 3 else ""))
    # one line per colour pair per slide
    merged, seen = [], {}
    for f in F:
        m = re.match(r"(text #\w+ on #\w+ = [\d.]+:1 \([^)]*\)): '(.*)'$", f["msg"]) if f["rule"] == "contrast" else None
        if m:
            k = (f["slide"], f["p"], m.group(1))
            if k in seen:
                seen[k]["_t"].append(m.group(2)); continue
            f = dict(f, _t=[m.group(2)], _h=m.group(1)); seen[k] = f
        elif f["rule"] != "contrast":
            k = (f["slide"], f["p"], f["rule"], f["msg"])
            if k in seen:
                seen[k]["_n"] = seen[k].get("_n", 1) + 1; continue
            seen[k] = f
        merged.append(f)
    for f in merged:
        if f.get("_n"):
            f["msg"] += f" (x{f.pop('_n')})"
    for f in merged:
        if "_t" in f:
            t = f.pop("_t"); h = f.pop("_h")
            f["msg"] = f"{h}: " + ", ".join(f"'{x}'" for x in t[:4]) + (f" +{len(t) - 4} more" if len(t) > 4 else "")
    merged.sort(key=lambda f: (f["p"], 999 if f["slide"] == "deck" else f["slide"]))
    return merged


def report(F):
    if not F:
        return "slop check: clean"
    counts = {p: sum(1 for f in F if f["p"] == p) for p in range(4)}
    lines = [f"slop check: {len(F)} finding(s) - P0 {counts[0]}, P1 {counts[1]}, P2 {counts[2]}, P3 {counts[3]}"]
    for f in F:
        where = "deck" if f["slide"] == "deck" else f"slide {f['slide']}"
        lines.append(f"  P{f['p']} {where}: [{f['rule']}] {f['msg']}  -> {f['fix']}")
    return "\n".join(lines)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("pptx")
    ap.add_argument("--accent", default=None, help="the Style line's ACCENT: 'none' or a hex; default: one extra hue allowed")
    ap.add_argument("--primary", default=None, help="the Style line's PRIMARY hex (recommended)")
    ap.add_argument("--json", default=None)
    a = ap.parse_args()
    F = scan(Presentation(a.pptx), a.accent, a.primary)
    print(report(F))
    if a.json:
        with open(a.json, "w") as fh:
            json.dump(F, fh, indent=1)
