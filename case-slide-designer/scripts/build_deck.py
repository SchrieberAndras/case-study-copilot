#!/usr/bin/env python3
"""Build a deck from a JSON spec.

    python build_deck.py spec.json out.pptx [--primary 1E3A5F] [--logo logo.png] [--fonts premium|safe]
                         [--style "PRIMARY #E51636, PRIMARY_DARK #AD1129, OUTLINE #EB2A48, MID #F17F90, NEUTRAL #E4D5D7"]

--style takes the game plan's Style line as written: every ROLE #HEX pair in it is used exactly
(PRIMARY also sets the accent), so the deck matches the team palette instead of re-deriving it.

Spec: {"primary": "...", "logo": "...", "fonts": "...", "tracker": ["Analysis", ...],
       "slides": [{"layout": "kpis", "title": "...", ...}, ...]}
Command-line flags override the spec. Prints layout warnings (text overflow, long titles).
"""
import argparse, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core import Deck
from layouts import LAYOUTS


ROLE_HEX = re.compile(r"\b(PRIMARY_DARK|PRIMARY|OUTLINE|MID|NEUTRAL)\b\s*#?([0-9A-Fa-f]{6})\b")


def parse_style(line):
    return {k: v.upper() for k, v in ROLE_HEX.findall(line or "")}


def build(spec, out, primary=None, logo=None, fonts=None, style=None):
    roles = parse_style(style or spec.get("style"))
    if primary and roles.get("PRIMARY") and primary.lstrip("#").upper() != roles["PRIMARY"]:
        print(f"WARN --primary {primary} differs from the Style line's PRIMARY #{roles['PRIMARY']}; using the Style line")
    primary = roles.get("PRIMARY") or primary
    fonts = fonts or spec.get("fonts", "premium")
    if isinstance(fonts, str) and "," in fonts:
        h, bd = [x.strip() for x in fonts.split(",", 1)]
        fonts = {"head": h, "body": bd}
    d = Deck(primary=primary or spec.get("primary", "1E3A5F"), font_profile=fonts,
             logo=logo or spec.get("logo"))
    d.pal.update({k: v for k, v in roles.items() if k != "PRIMARY"})
    if roles:   # COBE deck: only the five roles (case-study-ppt section 4); house tints map onto them
        d.pal.update(TINT=d.pal["NEUTRAL"], SOFT=d.pal["MID"])
    for sl in spec["slides"]:
        sl = dict(sl)
        if spec.get("tracker") and sl.get("phase") is not None:
            sl["_tracker"] = spec["tracker"]
        lay = LAYOUTS.get(sl["layout"])
        if not lay:
            raise SystemExit(f"unknown layout '{sl['layout']}'. Options: {', '.join(LAYOUTS)}")
        lay(d, sl)
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    d.save(out)
    return d


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("spec"); ap.add_argument("out")
    ap.add_argument("--primary"); ap.add_argument("--logo"); ap.add_argument("--fonts", help="premium | safe | 'Head Font,Body Font'")
    ap.add_argument("--style", help="the game plan's Style line (ROLE #HEX pairs)")
    a = ap.parse_args()
    d = build(json.load(open(a.spec)), a.out, a.primary, a.logo, a.fonts, a.style)
    print(f"saved {a.out} ({d.n} slides)")
    for w in d.warnings:
        print("WARN", w)
