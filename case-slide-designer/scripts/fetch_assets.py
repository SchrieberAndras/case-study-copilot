#!/usr/bin/env python3
"""Download the three large public data assets this skill needs (kept out of git for size).

    python scripts/fetch_assets.py

Builds, from the public npm registry:
  assets/icons.json          Lucide icons (lucide-static 0.468.0, ISC licence) as {name: svg}
  assets/icon-tags.json      Lucide search tags
  assets/us-states-albers.json  us-atlas 3.0.1 states-albers-10m (ISC licence)
"""
import io, json, os, re, tarfile, urllib.request

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
LUCIDE = "https://registry.npmjs.org/lucide-static/-/lucide-static-0.468.0.tgz"
ATLAS = "https://registry.npmjs.org/us-atlas/-/us-atlas-3.0.1.tgz"


def _tar(url):
    with urllib.request.urlopen(url) as r:
        return tarfile.open(fileobj=io.BytesIO(r.read()), mode="r:gz")


def _norm(svg):
    svg = re.sub(r"<!--.*?-->", "", svg, flags=re.S)
    svg = re.sub(r"\s+", " ", svg).strip()
    return re.sub(r'class="[^"]*"\s*', "", svg)


def main():
    os.makedirs(ASSETS, exist_ok=True)
    t = _tar(LUCIDE)
    icons, tags = {}, None
    for m in t.getmembers():
        if m.name.startswith("package/icons/") and m.name.endswith(".svg"):
            icons[os.path.basename(m.name)[:-4]] = _norm(t.extractfile(m).read().decode())
        elif m.name == "package/tags.json":
            tags = json.load(t.extractfile(m))
    icons = dict(sorted(icons.items()))
    with open(os.path.join(ASSETS, "icons.json"), "w") as f:
        json.dump(icons, f, separators=(",", ":"))
    with open(os.path.join(ASSETS, "icon-tags.json"), "w") as f:
        json.dump({k: tags[k] for k in icons if k in tags}, f, indent=2)
    a = _tar(ATLAS)
    with open(os.path.join(ASSETS, "us-states-albers.json"), "wb") as f:
        f.write(a.extractfile("package/states-albers-10m.json").read())
    print(f"icons: {len(icons)}  tags: {len(tags)}  map: ok  ->  {os.path.abspath(ASSETS)}")


if __name__ == "__main__":
    main()
