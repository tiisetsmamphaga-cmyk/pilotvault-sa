"""Drawing kit for the trial-mock explanation diagrams.

Same look as the ATG clean-v1 diagrams: white canvas, navy/gold/red/blue palette, Arial (Liberation Sans).
The practice page's card supplies the title and the KEY FACT panel, so the images carry only the diagram.
"""
import json
import math
import os
import subprocess
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image

REPO = Path(__file__).resolve().parents[2]
PUBLIC = REPO / "public"

F = "Arial,Helvetica,sans-serif"
NAVY = "#06111f"
INK = "#101827"
BODY = "#334155"
MUTED = "#64748b"
LINE = "#cbd5e1"
PANEL = "#f8fafc"
GOLD = "#f4b400"
GOLD_DARK = "#b7860b"
GOLD_SOFT = "#fef3c7"
BLUE = "#1e88e5"
BLUE_SOFT = "#dbeafe"
RED = "#dc2626"
RED_SOFT = "#fee2e2"
GREEN = "#15803d"
GREEN_SOFT = "#dcfce7"
SKY = "#e0f2fe"
GROUND = "#d9c7a3"

COLORS = {"ink": INK, "blue": BLUE, "red": RED, "green": GREEN, "gold": GOLD_DARK, "muted": MUTED, "navy": NAVY}


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def svg(body, w=1200, h=600):
    markers = "".join(
        f'<marker id="a-{k}" markerUnits="userSpaceOnUse" markerWidth="18" markerHeight="18" refX="15" refY="9" orient="auto">'
        f'<path d="M0,1 L17,9 L0,17 z" fill="{c}"/></marker>'
        for k, c in COLORS.items()
    )
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
            f"<defs>{markers}</defs><rect width=\"{w}\" height=\"{h}\" fill=\"#ffffff\"/>\n{body}</svg>\n")


def t(x, y, s, size=20, weight=700, fill=INK, anchor="middle", lh=1.25, italic=False):
    """Text; s may contain \\n for extra lines (each line drawn below the first)."""
    out = ""
    st = ' font-style="italic"' if italic else ""
    for i, line in enumerate(str(s).split("\n")):
        out += (f'<text x="{x:.1f}" y="{y + i * size * lh:.1f}" text-anchor="{anchor}" font-family="{F}" '
                f'font-size="{size}" font-weight="{weight}" fill="{fill}"{st}>{esc(line)}</text>\n')
    return out


def rect(x, y, w, h, fill=PANEL, stroke=LINE, sw=2, rx=10, dash=None, opacity=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    o = f' fill-opacity="{opacity}"' if opacity is not None else ""
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}{o}/>\n'


def circle(x, y, r, fill="#fff", stroke=INK, sw=3):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>\n'


def line(x1, y1, x2, y2, stroke=INK, w=3, arrow=None, dash=None):
    m = f' marker-end="url(#a-{arrow})"' if arrow else ""
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{w}" '
            f'stroke-linecap="round"{m}{d}/>\n')


def path(d, fill="none", stroke=INK, w=3, arrow=None, dash=None, extra=""):
    m = f' marker-end="url(#a-{arrow})"' if arrow else ""
    ds = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round"{m}{ds}{extra}/>\n'


def poly(pts, fill, stroke=INK, w=3):
    return path("M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z", fill, stroke, w)


def arrow(x1, y1, x2, y2, color="ink", w=4, dash=None):
    return line(x1, y1, x2, y2, COLORS[color], w, color, dash)


def pill(x, y, text, fill=NAVY, color="#ffffff", size=20, pad=18, h=None, w=None, stroke=None, weight=800):
    """Centred label box at (x, y) = centre."""
    lines = str(text).split("\n")
    h = h or size * 1.35 * len(lines) + 16
    w = w or max(len(l) for l in lines) * size * 0.58 + 2 * pad
    s = rect(x - w / 2, y - h / 2, w, h, fill, stroke or fill, 2, 10)
    y0 = y - (len(lines) - 1) * size * 1.35 / 2 + size * 0.36
    s += t(x, y0, text, size, weight, color, lh=1.35)
    return s


def card(x, y, w, h, head, body="", accent=NAVY, fill="#ffffff", head_size=22, body_size=20, hl=False):
    """Box with a bold heading line and optional body lines, left-aligned."""
    s = rect(x, y, w, h, GOLD_SOFT if hl else fill, GOLD if hl else LINE, 4 if hl else 2, 10)
    s += f'<rect x="{x:.1f}" y="{y:.1f}" width="8" height="{h:.1f}" rx="4" fill="{GOLD if hl else accent}"/>\n'
    s += t(x + 24, y + 34, head, head_size, 800, INK, "start")
    if body:
        s += t(x + 24, y + 34 + head_size * 1.45, body, body_size, 400, BODY, "start", lh=1.3)
    return s


def table(x, y, cols, rows, hl=(), head_rows=1, row_h=46, size=19, hl_ring=(), first_col_bold=True):
    """cols: list of widths. rows: list of lists of strings. hl: set of (r, c) cells shaded gold.
    hl_ring: list of (r, c) cells drawn with a heavy gold outline (the value read off)."""
    s = ""
    total = sum(cols)
    for r, row in enumerate(rows):
        cx = x
        yy = y + r * row_h
        for c, val in enumerate(row):
            w = cols[c]
            if r < head_rows:
                fill, fc, wt = NAVY, "#ffffff", 800
            elif (r, c) in hl:
                fill, fc, wt = GOLD_SOFT, INK, 800
            else:
                fill, fc, wt = "#ffffff" if r % 2 else PANEL, INK, 800 if (c == 0 and first_col_bold) else 400
            s += f'<rect x="{cx:.1f}" y="{yy:.1f}" width="{w:.1f}" height="{row_h}" fill="{fill}" stroke="{LINE}" stroke-width="1.5"/>\n'
            if val is not None and val != "":
                s += t(cx + w / 2, yy + row_h / 2 + size * 0.36, val, size, wt, fc)
            cx += w
    for r, c in hl_ring:
        cx = x + sum(cols[:c])
        s += f'<rect x="{cx - 3:.1f}" y="{y + r * row_h - 3:.1f}" width="{cols[c] + 6:.1f}" height="{row_h + 6}" fill="none" stroke="{GOLD}" stroke-width="5" rx="4"/>\n'
    s += f'<rect x="{x:.1f}" y="{y:.1f}" width="{total:.1f}" height="{row_h * len(rows)}" fill="none" stroke="{INK}" stroke-width="2"/>\n'
    return s


def plane_top(x, y, s=1.0, rot=0, fill=NAVY):
    """Light aircraft seen from above, nose pointing up (rot in degrees clockwise)."""
    d = ("M0,-46 C5,-46 7,-38 7,-30 L7,-12 L60,-6 L60,4 L7,6 L5,30 L22,36 L22,43 L0,41 L-22,43 L-22,36 "
         "L-5,30 L-7,6 L-60,4 L-60,-6 L-7,-12 L-7,-30 C-7,-38 -5,-46 0,-46 Z")
    return f'<path d="{d}" transform="translate({x:.1f},{y:.1f}) rotate({rot}) scale({s})" fill="{fill}" stroke="#ffffff" stroke-width="2"/>\n'


def plane_side(x, y, s=1.0, fill=NAVY, flip=False, pitch=0):
    """Light high-wing aircraft seen from the side, nose to the right (left if flip)."""
    d = ("M-58,-4 L-50,-24 L-44,-24 L-36,-6 L30,-8 C44,-8 54,-4 58,2 C54,6 44,8 30,8 L-50,6 Z "
         "M-6,-12 L22,-12 L20,-8 L-8,-8 Z")
    sx = -s if flip else s
    return (f'<g transform="translate({x:.1f},{y:.1f}) rotate({-pitch if not flip else pitch}) scale({sx},{s})">'
            f'<path d="{d}" fill="{fill}" stroke="#ffffff" stroke-width="1.5"/>'
            f'<rect x="-14" y="-16" width="40" height="5" rx="2" fill="{fill}"/>'
            f'<circle cx="-30" cy="12" r="4" fill="{INK}"/><circle cx="20" cy="12" r="4" fill="{INK}"/></g>\n')


def cloud(x, y, w=200, h=80, fill="#ffffff", stroke="#94a3b8"):
    """Cumulus-style cloud centred on (x, y): overlapping lobes, outlined only on the outside."""
    lobes = [(-0.32, 0.18, 0.30), (-0.08, -0.12, 0.42), (0.2, 0.0, 0.36), (0.38, 0.22, 0.26), (0.0, 0.25, 0.32)]
    s = ""
    for fx, fy, fr in lobes:
        s += circle(x + fx * w, y + fy * h * 1.2, fr * h * 1.25, fill, stroke, 3)
    for fx, fy, fr in lobes:
        s += circle(x + fx * w, y + fy * h * 1.2, fr * h * 1.25 - 1.6, fill, fill, 0)
    s += rect(x - w * 0.42, y + h * 0.22, w * 0.8, h * 0.32, fill, fill, 0, 0)
    s += line(x - w * 0.4, y + h * 0.54, x + w * 0.4, y + h * 0.54, stroke, 3)
    return s


def dim(x1, y1, x2, y2, label, color=INK, size=19, off=0, side="above", w=2.5):
    """Dimension line with arrowheads at both ends and a centred label."""
    s = line(x1, y1, x2, y2, COLORS.get(color, color), w, color if color in COLORS else None)
    s += line(x2, y2, x1, y1, COLORS.get(color, color), w, color if color in COLORS else None)
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    if side == "above":
        s += t(mx, my - 12 + off, label, size, 800, COLORS.get(color, color))
    elif side == "below":
        s += t(mx, my + size + 8 + off, label, size, 800, COLORS.get(color, color))
    elif side == "right":
        s += t(mx + 14, my + size * 0.36, label, size, 800, COLORS.get(color, color), "start")
    else:
        s += t(mx - 14, my + size * 0.36, label, size, 800, COLORS.get(color, color), "end")
    return s


def runway(x, y, w, h=60, left="18", right="36", fill="#475569"):
    """Runway seen from above, drawn left to right; designators shown upright just outside each end."""
    s = rect(x, y, w, h, fill, INK, 2, 2)
    k = x + 70
    while k + 30 < x + w - 70:
        s += f'<rect x="{k:.1f}" y="{y + h / 2 - 2:.1f}" width="30" height="4" fill="#ffffff"/>\n'
        k += 60
    for xx in (x + 18, x + w - 30):
        for j in range(4):
            s += f'<rect x="{xx:.1f}" y="{y + 8 + j * (h - 16) / 4:.1f}" width="12" height="{(h - 16) / 4 - 4:.1f}" fill="#ffffff"/>\n'
    if left:
        s += t(x + 6, y + h + 30, left, 22, 800, INK, "start")
    if right:
        s += t(x + w - 6, y + h + 30, right, 22, 800, INK, "end")
    return s


def embed(png_path, x, y, w, h, crop=None):
    """Embed a raster (e.g. a manual figure) scaled into the box (x, y, w, h); returns (svg, scale, ox, oy, crop)."""
    import base64, io
    im = Image.open(png_path).convert("RGB")
    if crop:
        im = im.crop(crop)
    sc = min(w / im.width, h / im.height)
    iw, ih = im.width * sc, im.height * sc
    ox, oy = x + (w - iw) / 2, y + (h - ih) / 2
    buf = io.BytesIO()
    im.save(buf, "PNG", optimize=True)
    data = base64.b64encode(buf.getvalue()).decode()
    s = f'<image x="{ox:.1f}" y="{oy:.1f}" width="{iw:.1f}" height="{ih:.1f}" href="data:image/png;base64,{data}" preserveAspectRatio="none"/>\n'
    s += rect(ox, oy, iw, ih, "none", LINE, 1.5, 0)
    return s, sc, ox, oy


# ------------------------------------------------------------------ rendering

RENDER_JS = r"""
let chromium
try { ({ chromium } = require("playwright")) } catch { ({ chromium } = require("/opt/node22/lib/node_modules/playwright")) }
const fs = require("fs"), path = require("path")
;(async () => {
  const [dir, ...files] = process.argv.slice(2)
  const browser = await chromium.launch()
  const page = await browser.newPage({ viewport: { width: 1400, height: 1200 }, deviceScaleFactor: 1.5 })
  for (const f of files) {
    const svg = fs.readFileSync(path.join(dir, f), "utf8")
    await page.setContent(`<html><body style="margin:0;background:#fff">${svg}</body></html>`)
    await page.locator("svg").screenshot({ path: path.join(dir, f.replace(/\.svg$/, ".png")) })
  }
  await browser.close()
})()
"""


def trim(img, pad=28):
    a = np.asarray(img.convert("RGB")).astype(int)
    ink = np.abs(a - 255).sum(axis=2) > 24
    ys, xs = np.where(ink)
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    return img.crop((max(0, x0 - pad), max(0, y0 - pad), min(img.width, x1 + pad), min(img.height, y1 + pad)))


def render(items, keep_svg_dir=None):
    """items: list of (svg_text, public_url). Writes <public>/<url> as WebP (and the SVG source next to it)."""
    work = Path(tempfile.mkdtemp(prefix="trialvis-"))
    (work / "render.js").write_text(RENDER_JS)
    names = []
    for i, (s, url) in enumerate(items):
        name = f"{i:03d}.svg"
        (work / name).write_text(s)
        names.append(name)
    env = dict(os.environ, NODE_PATH="/opt/node22/lib/node_modules")
    subprocess.run(["node", str(work / "render.js"), str(work), *names], check=True, env=env, cwd=REPO)
    for name, (s, url) in zip(names, items):
        out = PUBLIC / url.lstrip("/")
        out.parent.mkdir(parents=True, exist_ok=True)
        trim(Image.open(work / name.replace(".svg", ".png"))).save(out, quality=90, method=6)
        if keep_svg_dir:
            Path(keep_svg_dir).mkdir(parents=True, exist_ok=True)
            (Path(keep_svg_dir) / (out.stem + ".svg")).write_text(s)
    return work


def template(headline, subline=None, blocks=(), formula=None, kicker="KEY FACT"):
    d = {"kicker": kicker, "headline": headline}
    if subline:
        d["subline"] = subline
    if blocks:
        d["blocks"] = [{"label": a, "value": b} for a, b in blocks]
    if formula:
        d["formula"] = formula
    return json.dumps(d, ensure_ascii=False)
