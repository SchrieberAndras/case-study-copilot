"""Palette + font profiles for the house style.

One accent colour in, a full set of roles out. The five COBE roles (PRIMARY, PRIMARY_DARK, OUTLINE, MID,
NEUTRAL, plus NEUTRAL_DARK for the tracker base line) come from case-study-ppt's scripts/palette.py when that
skill is installed next to this one, else from the same formulas below, so a game plan Style line and this
skill give identical colours. TINT, SOFT, LINE, INK and GREY are house-style extras for this skill's own
layouts; case-study-ppt decks use only the five roles plus white and near-black text.
"""
import colorsys, os, sys

try:
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "case-study-ppt", "scripts"))
    from palette import roles as _ppt_roles
except Exception:
    _ppt_roles = None

DEFAULT_PRIMARY = "1E3A5F"   # deep navy; swap for the case company's brand colour


def _rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _hex(rgb):
    return "%02X%02X%02X" % tuple(max(0, min(255, round(c))) for c in rgb)


def _lum(rgb):
    def f(c):
        c /= 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (f(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = _lum(_rgb(a)), _lum(_rgb(b))
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def make_palette(primary=DEFAULT_PRIMARY):
    primary = primary.lstrip("#").upper()
    r, g, b = (c / 255 for c in _rgb(primary))
    h, l, s = colorsys.rgb_to_hls(r, g, b)

    def hls(h_, l_, s_):
        return _hex(tuple(c * 255 for c in colorsys.hls_to_rgb(h_, max(0, min(1, l_)), max(0, min(1, s_)))))

    pr = _rgb(primary)
    if _ppt_roles is not None:
        cobe = _ppt_roles(primary)[0]
    else:  # case-study-ppt section 4 formulas
        cobe = {"PRIMARY": primary,
                "PRIMARY_DARK": primary if l < 0.25 else hls(h, l - 0.12, s),
                "OUTLINE": hls(h, l + 0.05, s),
                "MID": _hex(tuple(c * 0.55 + 255 * 0.45 for c in pr)),
                "NEUTRAL": hls(h, 0.865, min(s, 0.22)),
                "NEUTRAL_DARK": hls(h, 0.78, min(s, 0.22))}
    dark = cobe["PRIMARY_DARK"]
    ink = "1B1F27"
    pal = dict(cobe)                                  # PRIMARY, PRIMARY_DARK, OUTLINE, MID (secondary series, dashed outlines), NEUTRAL, NEUTRAL_DARK
    pal.update({
        "TINT": hls(h, 0.95, min(s, 0.30)),           # light panel fill (house style)
        "SOFT": _hex(tuple(c * 0.25 + 255 * 0.75 for c in pr)),   # de-emphasised bars / series (house style)
        "LINE": hls(h, 0.82, min(s, 0.12)),           # hairlines
        "INK": ink,
        "GREY": "6B7280",
        "WHITE": "FFFFFF",
    })
    # text colour to use on top of PRIMARY: white if it reaches 4.5:1, else ink
    pal["ON_PRIMARY"] = "FFFFFF" if contrast(primary, "FFFFFF") >= 4.5 else ink
    pal["ON_DARK"] = "FFFFFF" if contrast(dark, "FFFFFF") >= 4.5 else ink
    return pal


# Two font profiles. "premium" matches the reference-deck look but needs the
# fonts installed on the machine that opens the file; "safe" renders everywhere.
FONTS = {
    "premium": {"head": "Avenir Next LT Pro", "body": "Avenir Next LT Pro",   # case-study-ppt section 4; measured with Poppins/Inter as proxies
                "head_file": "Poppins-SemiBold.ttf", "body_file": "Inter-Regular.otf",
                "body_bold_file": "Inter-SemiBold.otf"},
    "safe": {"head": "Aptos", "body": "Aptos",
             "head_file": "Poppins-SemiBold.ttf", "body_file": "Inter-Regular.otf",
             "body_bold_file": "Inter-SemiBold.otf"},   # measurement proxies only
}

if __name__ == "__main__":
    import sys, json
    p = make_palette(sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PRIMARY)
    print(json.dumps(p, indent=1))
    print("white on PRIMARY contrast: %.2f" % contrast(p["PRIMARY"], "FFFFFF"))
