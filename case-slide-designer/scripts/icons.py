"""Line-icon helper (Lucide, ISC licence). Recolours SVGs and rasterises to PNG.

    from icons import find, render
    find("growth money")      -> ['trending-up', 'banknote', ...]
    render("rocket", "1E3A5F") -> path to a 512px PNG (cached)
"""
import json, os, re, hashlib, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "..", "assets")
CACHE = os.path.join(tempfile.gettempdir(), "slide-designer-icons")
_tags = None
_svgs = None


def _ensure_assets():
    if not os.path.exists(os.path.join(ASSETS, "icons.json")):
        from fetch_assets import main as _fetch  # large public assets are not stored in git
        _fetch()


def _load_svgs():
    global _svgs
    if _svgs is None:
        _ensure_assets()
        with open(os.path.join(ASSETS, "icons.json")) as f:
            _svgs = json.load(f)
    return _svgs


def _load_tags():
    global _tags
    if _tags is None:
        _ensure_assets()
        with open(os.path.join(ASSETS, "icon-tags.json")) as f:
            _tags = json.load(f)
    return _tags


def exists(name):
    return name in _load_svgs()


def find(query, limit=8):
    """Rank icons by how well their name/tags match the query words."""
    words = [w for w in re.split(r"[\s,/]+", query.lower()) if w]
    scored = []
    for name, tags in _load_tags().items():
        hay = [name.replace("-", " ")] + [t.lower() for t in tags]
        score = 0
        for w in words:
            if name == w: score += 10
            elif w in name.split("-"): score += 6
            elif w in name: score += 3
            score += sum(2 for t in hay[1:] if t == w) + sum(1 for t in hay[1:] if w in t and t != w)
        if score and exists(name):
            scored.append((score, len(name), name))
    scored.sort(key=lambda x: (-x[0], x[1]))
    return [n for _, _, n in scored[:limit]]


def resolve(name_or_query):
    """Accept an exact icon name or a free-text query; always return a valid icon name."""
    if exists(name_or_query):
        return name_or_query
    hits = find(name_or_query, 1)
    return hits[0] if hits else "circle"


def render(name, color="1E3A5F", px=512, stroke=1.75, opacity=1.0):
    import cairosvg
    name = resolve(name)
    key = hashlib.md5(f"{name}{color}{px}{stroke}{opacity}".encode()).hexdigest()[:10]
    os.makedirs(CACHE, exist_ok=True)
    out = os.path.join(CACHE, f"{name}-{key}.png")
    if not os.path.exists(out):
        svg = _load_svgs()[name]
        svg = svg.replace("currentColor", "#" + color.lstrip("#")).replace('stroke-width="2"', f'stroke-width="{stroke}"')
        if opacity < 1:
            svg = svg.replace("<svg", f'<svg opacity="{opacity}"', 1)
        cairosvg.svg2png(bytestring=svg.encode(), write_to=out, output_width=px, output_height=px)
    return out


if __name__ == "__main__":
    import sys
    print(find(" ".join(sys.argv[1:]), 12))
