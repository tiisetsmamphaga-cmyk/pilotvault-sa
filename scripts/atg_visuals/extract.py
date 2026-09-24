"""Detect and crop figures from pages of the ATG textbook PDF.

Usage: python3 extract.py <page> [<page> ...]
Writes crops to figs/p<page>-<n>.png and a contact sheet figs/sheet-<pages>.png
"""
import re
import subprocess
import sys
from html import unescape
from pathlib import Path
import os
REPO = Path(__file__).resolve().parents[2]
WORK = Path(os.environ.get("ATG_WORK", "/tmp/atg-work"))

import cv2
import numpy as np
from PIL import Image, ImageDraw

PDF = str(REPO / "091e41264c1bdb10.pdf")
HERE = Path(__file__).parent
OUT = WORK / "figs"
OUT.mkdir(exist_ok=True)
DPI = 200


def render(page):
    base = WORK / "pages" / f"hi-{page}"
    base.parent.mkdir(parents=True, exist_ok=True)
    png = Path(f"{base}.png")
    if not png.exists():
        subprocess.run(["pdftoppm", "-f", str(page), "-l", str(page), "-r", str(DPI), "-png", "-singlefile", PDF, str(base)], check=True)
    return Image.open(png).convert("RGB")


def words(page):
    xml = subprocess.run(["pdftotext", "-f", str(page), "-l", str(page), "-bbox", PDF, "-"], capture_output=True, text=True).stdout
    ws = []
    for m in re.finditer(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">([^<]*)</word>', xml):
        x0, y0, x1, y1 = (float(v) * DPI / 72 for v in m.groups()[:4])
        ws.append((x0, y0, x1, y1, unescape(m.group(5))))
    return ws


def lines_of(ws, tol=6):
    rows = []
    for w in sorted(ws, key=lambda w: (w[1], w[0])):
        for r in rows:
            if abs(r[0][1] - w[1]) < tol:
                r.append(w)
                break
        else:
            rows.append([w])
    return rows


def detect(page):
    im = render(page)
    g = np.asarray(im.convert("L"))
    ink = (g < 225).astype(np.uint8)
    ws = words(page)
    text_mask = np.zeros_like(ink)
    for x0, y0, x1, y1, _ in ws:
        text_mask[int(y0) - 3:int(y1) + 3, int(x0) - 3:int(x1) + 3] = 1
    fig_ink = ink * (1 - text_mask)
    dil = cv2.dilate(fig_ink, np.ones((21, 21), np.uint8))
    n, lab, stats, _ = cv2.connectedComponentsWithStats(dil)
    boxes = []
    for i in range(1, n):
        x, y, w, h, a = stats[i]
        real = int(fig_ink[y:y + h, x:x + w].sum())
        if w > 160 and h > 110 and real > 2500:
            boxes.append([x, y, x + w, y + h])
    # merge overlapping boxes
    merged = True
    while merged:
        merged = False
        for i in range(len(boxes)):
            for j in range(i + 1, len(boxes)):
                a, b = boxes[i], boxes[j]
                if a[0] < b[2] + 10 and b[0] < a[2] + 10 and a[1] < b[3] + 10 and b[1] < a[3] + 10:
                    boxes[i] = [min(a[0], b[0]), min(a[1], b[1]), max(a[2], b[2]), max(a[3], b[3])]
                    boxes.pop(j)
                    merged = True
                    break
            if merged:
                break
    # pull in figure labels (text lines touching the box), never "Fig..." captions
    results = []
    for bx in boxes:
        x0, y0, x1, y1 = bx
        for row in lines_of(ws):
            txt = " ".join(w[4] for w in row)
            if re.match(r"\s*Fig", txt):
                continue
            for w in row:
                cx, cy = (w[0] + w[2]) / 2, (w[1] + w[3]) / 2
                if x0 - 25 < cx < x1 + 25 and y0 - 25 < cy < y1 + 25 and (w[2] - w[0]) < (x1 - x0):
                    x0, y0, x1, y1 = min(x0, w[0]), min(y0, w[1]), max(x1, w[2]), max(y1, w[3])
        pad = 8
        results.append((max(0, int(x0) - pad), max(0, int(y0) - pad), min(im.width, int(x1) + pad), min(im.height, int(y1) + pad)))
    return im, results


def main(pages):
    crops = []
    for p in pages:
        im, boxes = detect(p)
        for k, b in enumerate(sorted(boxes, key=lambda b: (b[1], b[0])), 1):
            c = im.crop(b)
            path = OUT / f"p{p}-{k}.png"
            c.save(path)
            crops.append((path, c))
            print(f"{path.name} box={b} size={c.size}")
    if not crops:
        return
    thumbs = []
    for path, c in crops:
        t = c.copy()
        t.thumbnail((420, 300))
        thumbs.append((path.stem, t))
    cols = 4
    rows = (len(thumbs) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * 430, rows * 330), "white")
    d = ImageDraw.Draw(sheet)
    for i, (name, t) in enumerate(thumbs):
        x, y = (i % cols) * 430, (i // cols) * 330
        sheet.paste(t, (x + 5, y + 24))
        d.rectangle([x + 4, y + 23, x + 6 + t.width, y + 25 + t.height], outline="red")
        d.text((x + 6, y + 4), name, fill="red")
    name = "sheet-" + "-".join(map(str, pages[:3])) + ("-etc" if len(pages) > 3 else "") + ".png"
    sheet.save(OUT / name)
    print("sheet", OUT / name)


def stitch(page_a, page_b, name):
    """Join a figure split across a page break: last figure on page_a + first on page_b."""
    im_a, boxes_a = detect(page_a)
    im_b, boxes_b = detect(page_b)
    ba = max(boxes_a, key=lambda b: b[3])
    bb = min(boxes_b, key=lambda b: b[1])
    a, b = im_a.crop(ba), im_b.crop(bb)
    x0 = min(ba[0], bb[0])
    st = Image.new("RGB", (max(ba[2], bb[2]) - x0, a.height + b.height), "white")
    st.paste(a, (ba[0] - x0, 0))
    st.paste(b, (bb[0] - x0, a.height))
    gray = np.asarray(st.convert("L")).astype(float)
    band = range(max(0, a.height - 60), min(st.height, a.height + 60))
    blank = [y for y in band if gray[y, 40:-40].mean() > 244]
    if blank:
        y0, y1 = blank[0], blank[-1] + 1
        top, bot = st.crop((0, 0, st.width, y0)), st.crop((0, y1, st.width, st.height))
        st = Image.new("RGB", (st.width, top.height + bot.height), "white")
        st.paste(top, (0, 0))
        st.paste(bot, (0, top.height))
    st.save(OUT / f"{name}.png")
    print("stitched", name, st.size)


if __name__ == "__main__":
    if sys.argv[1:2] == ["stitch"]:
        stitch(int(sys.argv[2]), int(sys.argv[3]), sys.argv[4])
    else:
        main([int(a) for a in sys.argv[1:]])
