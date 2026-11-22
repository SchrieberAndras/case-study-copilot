#!/usr/bin/env python3
"""Compute the five case-study-ppt palette roles from the case brand's PRIMARY colour.

Usage: python palette.py E51636

Formulas (case-study-ppt section 4), all in HSL unless noted, rounded to hex:
  PRIMARY_DARK  lightness minus 12 points, same hue and saturation (= PRIMARY if its lightness is below 25%)
  OUTLINE       lightness plus 5 points
  MID           RGB mix of 55% PRIMARY and 45% white
  NEUTRAL       PRIMARY's hue, lightness 86.5%, saturation = min(PRIMARY's, 22%)
  NEUTRAL_DARK  same as NEUTRAL at lightness 78% (tracker base line)
Also prints the contrast of white text on PRIMARY (needs 4.5:1; if lower, use near-black text on PRIMARY boxes).
The NEUTRAL formula is the same one case-deck-merger's restyle_like_base.py uses.
"""
import colorsys
import sys


def parse(h):
    h = h.lstrip("#").upper()
    if len(h) != 6:
        sys.exit("PRIMARY must be a 6-digit hex code, e.g. E51636")
    return [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]


def to_hex(rgb):
    return "".join(f"{max(0, min(255, round(c * 255))):02X}" for c in rgb)


def lum(rgb):
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (f(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def roles(primary_hex):
    rgb = parse(primary_hex)
    h, l, s = colorsys.rgb_to_hls(*rgb)
    at = lambda light, sat=s: to_hex(colorsys.hls_to_rgb(h, max(0.0, min(1.0, light)), sat))
    mid = to_hex([0.55 * c + 0.45 for c in rgb])
    contrast = 1.05 / (lum(rgb) + 0.05)
    # a PRIMARY that is already dark (lightness < 25%) cannot be darkened without turning near-black,
    # which would look the same as the body text, so PRIMARY_DARK = PRIMARY in that case
    dark = at(l - 0.12) if l >= 0.25 else primary_hex.lstrip("#").upper()
    return {
        "PRIMARY": primary_hex.lstrip("#").upper(),
        "PRIMARY_DARK": dark,
        "OUTLINE": at(l + 0.05),
        "MID": mid,
        "NEUTRAL": at(0.865, min(s, 0.22)),
        "NEUTRAL_DARK": at(0.78, min(s, 0.22)),
    }, contrast


if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1].startswith("-"):
        print(__doc__)
        sys.exit(1)
    out, contrast = roles(sys.argv[1])
    for k, v in out.items():
        print(f"{k:<13} #{v}")
    verdict = "ok: white text on PRIMARY" if contrast >= 4.5 else "too low: use near-black text on PRIMARY boxes"
    print(f"white-on-PRIMARY contrast {contrast:.2f}:1 ({verdict})")
