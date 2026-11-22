#!/usr/bin/env python3
"""Editable US map: every state is a native PowerPoint freeform the user can recolour.

    from us_map import draw_us_map
    centre = draw_us_map(slide, x, y, w, h, highlight={"CA": "E51636", "NY": "E51636"},
                         base="E3D3CF", border="FFFFFF")
    cx, cy = centre(["MI", "IL"])     # inch coordinates of a region's bounding-box centre (for pins/labels)

Lower 48 only (Alaska/Hawaii dropped) unless include_ak_hi=True. Data: us-atlas states-albers-10m
(pre-projected Albers USA, ISC licence, assets/US-ATLAS-LICENSE.txt). The map keeps its aspect ratio and is
centred in the (x, y, w, h) box, so check the render for leftover white space and size the box to the map.
"""
import json, os
from pptx.util import Pt, Emu
from pptx.dml.color import RGBColor

E = 914400
DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "us-states-albers.json")
FIPS = {"AL": "01", "AK": "02", "AZ": "04", "AR": "05", "CA": "06", "CO": "08", "CT": "09", "DE": "10", "DC": "11",
        "FL": "12", "GA": "13", "HI": "15", "ID": "16", "IL": "17", "IN": "18", "IA": "19", "KS": "20", "KY": "21",
        "LA": "22", "ME": "23", "MD": "24", "MA": "25", "MI": "26", "MN": "27", "MS": "28", "MO": "29", "MT": "30",
        "NE": "31", "NV": "32", "NH": "33", "NJ": "34", "NM": "35", "NY": "36", "NC": "37", "ND": "38", "OH": "39",
        "OK": "40", "OR": "41", "PA": "42", "RI": "44", "SC": "45", "SD": "46", "TN": "47", "TX": "48", "UT": "49",
        "VT": "50", "VA": "51", "WA": "53", "WV": "54", "WI": "55", "WY": "56", "PR": "72"}
CODE = {v: k for k, v in FIPS.items()}


def _states(include_ak_hi=False):
    if not os.path.exists(DATA):
        from fetch_assets import main as _fetch  # large public assets are not stored in git
        _fetch()
    topo = json.load(open(DATA))
    sx, sy = topo["transform"]["scale"]; tx, ty = topo["transform"]["translate"]
    arcs = []
    for a in topo["arcs"]:
        x = y = 0; pts = []
        for dx, dy in a:
            x += dx; y += dy; pts.append((x * sx + tx, y * sy + ty))
        arcs.append(pts)

    def ring(idx):
        pts = []
        for i in idx:
            seg = arcs[i] if i >= 0 else arcs[~i][::-1]
            pts.extend(seg if not pts else seg[1:])
        return pts

    skip = {"72", "78", "60", "66", "69"} | (set() if include_ak_hi else {"02", "15"})
    out = {}
    for g in topo["objects"]["states"]["geometries"]:
        if g["id"] in skip:
            continue
        polys = g["arcs"] if g["type"] == "MultiPolygon" else [g["arcs"]]
        out[CODE.get(g["id"], g["id"])] = [r for r in (ring(r) for p in polys for r in p) if len(r) > 2]
    return out


def draw_us_map(slide, x, y, w, h, highlight=None, base="E8E8E8", border="FFFFFF", border_pt=0.5,
                include_ak_hi=False, valign="m"):
    """highlight: {postal code: hex fill}. Returns centre(codes) -> (cx, cy) in inches."""
    highlight = {k.upper(): v for k, v in (highlight or {}).items()}
    states = _states(include_ak_hi)
    allp = [p for rs in states.values() for r in rs for p in r]
    minx, maxx = min(p[0] for p in allp), max(p[0] for p in allp)
    miny, maxy = min(p[1] for p in allp), max(p[1] for p in allp)
    k = min(w / (maxx - minx), h / (maxy - miny))
    ox = x + (w - (maxx - minx) * k) / 2
    oy = y + {"t": 0, "m": (h - (maxy - miny) * k) / 2, "b": h - (maxy - miny) * k}[valign]

    def to_in(p):
        return ox + (p[0] - minx) * k, oy + (p[1] - miny) * k

    def emu(pt):
        return Emu(int(pt[0] * E)), Emu(int(pt[1] * E))

    for code, rings in states.items():
        p0 = [to_in(p) for p in rings[0]]
        fb = slide.shapes.build_freeform(*emu(p0[0]), scale=1.0)
        fb.add_line_segments([emu(p) for p in p0[1:]], close=True)
        for r in rings[1:]:
            pr = [to_in(p) for p in r]
            fb.move_to(*emu(pr[0]))
            fb.add_line_segments([emu(p) for p in pr[1:]], close=True)
        shp = fb.convert_to_shape(); shp.name = f"state-{code}"
        shp.fill.solid(); shp.fill.fore_color.rgb = RGBColor.from_string(highlight.get(code, base))
        shp.line.color.rgb = RGBColor.from_string(border); shp.line.width = Pt(border_pt)
        shp.shadow.inherit = False

    def centre(codes):
        ps = [to_in(p) for c in codes for r in states[c.upper()] for p in r]
        xs = [p[0] for p in ps]; ys = [p[1] for p in ps]
        return (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2

    return centre
