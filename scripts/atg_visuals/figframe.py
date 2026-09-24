"""Wrap an extracted textbook figure in the ATG house frame (SVG, rendered later to WebP)."""
import base64
import io
from pathlib import Path
import os
REPO = Path(__file__).resolve().parents[2]
WORK = Path(os.environ.get("ATG_WORK", "/tmp/atg-work"))

from PIL import Image

import importlib.util

_spec = importlib.util.spec_from_file_location("g", Path(__file__).parent / "gen_airframes.py")
g = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(g)

BOX = (48, 146, 1152, 552)  # x0, y0, x1, y1 available for the figure


def frame(crop, title, sub, foot, notes=(), box=BOX, crop_box=None):
    """crop: path or PIL image. notes: (text, (tx, ty) frame coords, (cx, cy) crop coords, anchor)."""
    im = Image.open(crop).convert("RGB") if not isinstance(crop, Image.Image) else crop
    if crop_box:
        im = im.crop(crop_box)
    x0, y0, x1, y1 = box
    sc = min((x1 - x0) / im.width, (y1 - y0) / im.height)
    w, h = im.width * sc, im.height * sc
    ix, iy = x0 + (x1 - x0 - w) / 2, y0 + (y1 - y0 - h) / 2
    big = im.resize((int(w * 1.5), int(h * 1.5)), Image.LANCZOS) if sc * 1.5 < 1 else im
    buf = io.BytesIO()
    big.save(buf, "PNG", optimize=True)
    data = base64.b64encode(buf.getvalue()).decode()
    s = g.header(title)
    s += f'<image x="{ix:.1f}" y="{iy:.1f}" width="{w:.1f}" height="{h:.1f}" href="data:image/png;base64,{data}" preserveAspectRatio="none"/>\n'
    s += f'<rect x="{ix:.1f}" y="{iy:.1f}" width="{w:.1f}" height="{h:.1f}" fill="none" stroke="#d7e0ea" stroke-width="1.5"/>\n'
    for text, (tx, ty), (cx, cy), anchor in notes:
        px, py = (ix + cx * sc, iy + cy * sc) if cx is not None else (0, 0)
        lines = text.split("\n")
        tw = max(len(l) for l in lines) * 10.6 + 28
        th = 24 * len(lines) + 8
        bx = tx - tw / 2 if anchor == "middle" else (tx - 11 if anchor == "start" else tx - tw + 11)
        # leader from the nearest edge of the label box
        lx = min(max(px, bx), bx + tw)
        ly = min(max(py, ty - 20), ty - 20 + th)
        if cx is not None:
            s += g.line(lx, ly, px, py, g.INK, 3, "aDark")
        s += f'<rect x="{bx:.1f}" y="{ty - 20:.1f}" width="{tw:.1f}" height="{th:.1f}" rx="8" fill="#ffffff" fill-opacity="0.94" stroke="{g.GOLD}" stroke-width="3"/>\n'
        for k, l in enumerate(lines):
            s += g.t(tx, ty + k * 24, l, 17, 800, g.INK, anchor)
    s += g.t(600, 582, sub, 18, 400, g.BODY)
    s += g.footer(foot)
    return s
