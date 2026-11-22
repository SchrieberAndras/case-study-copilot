#!/usr/bin/env python3
"""Render a pptx to PNGs (one per slide) via LibreOffice, optionally a contact sheet.

    python render.py deck.pptx outdir [--dpi 80] [--sheet]
"""
import argparse, glob, os, subprocess, shutil, tempfile
ap = argparse.ArgumentParser()
ap.add_argument("pptx"); ap.add_argument("outdir"); ap.add_argument("--dpi", type=int, default=80); ap.add_argument("--sheet", action="store_true")
a = ap.parse_args()
os.makedirs(a.outdir, exist_ok=True)
tmp = tempfile.mkdtemp()
subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", tmp, a.pptx], check=True, capture_output=True, timeout=240)
pdf = os.path.join(tmp, os.path.splitext(os.path.basename(a.pptx))[0] + ".pdf")
for f in glob.glob(os.path.join(a.outdir, "slide-*.png")):
    os.remove(f)
subprocess.run(["pdftoppm", "-r", str(a.dpi), "-png", pdf, os.path.join(a.outdir, "slide")], check=True)
os.makedirs(os.path.join(a.outdir, "_extra"), exist_ok=True)
shutil.copy(pdf, os.path.join(a.outdir, "_extra", "deck.pdf"))
pngs = sorted(glob.glob(os.path.join(a.outdir, "slide-*.png")))
print(f"{len(pngs)} slides -> {a.outdir}")
if a.sheet and pngs:
    from PIL import Image
    ims = [Image.open(p) for p in pngs]; w, h = ims[0].size; cols = 3; tw, th = w // 2, h // 2
    rows = (len(ims) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tw + (cols + 1) * 10, rows * th + (rows + 1) * 10), "#888")
    for i, im in enumerate(ims):
        sheet.paste(im.resize((tw, th)), (10 + (i % cols) * (tw + 10), 10 + (i // cols) * (th + 10)))
    sheet.save(os.path.join(a.outdir, "_extra", "sheet.png")); print("sheet.png written")
