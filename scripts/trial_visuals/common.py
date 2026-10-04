"""Shared helpers for the trial-mock diagram sets (one module per subject registers ITEMS)."""
from pathlib import Path

from kit import *  # noqa: F401,F403
from kit import BODY, COLORS, GOLD, GOLD_DARK, INK, LINE, MUTED, NAVY, RED, circle, embed, line, path, pill, t

FIG = Path(__file__).resolve().parent / "fig"


class Registry:
    def __init__(self, subject, folder):
        self.subject = subject
        self.folder = folder
        self.items = []

    def add(self, qid, slug, title, template, h=600, w=1200):
        def deco(fn):
            self.items.append(dict(id=qid, subject=self.subject, url=f"{self.folder}/{slug}.webp", title=title,
                                   template=template, draw=fn, w=w, h=h))
            return fn
        return deco


def graph(name, x, y, w, h):
    """Embed a manual figure; returns (svg, P) where P maps figure pixels to canvas coordinates."""
    s, sc, ox, oy = embed(FIG / name, x, y, w, h)
    return s, (lambda px, py: (ox + px * sc, oy + py * sc))


def trace(pts, color="red", w=5, arrow_end=True):
    """Reading path over a chart: white halo under a coloured line, arrow at the end (color is a kit COLORS key)."""
    d = "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    s = path(d, "none", "#ffffff", w + 6)
    s += path(d, "none", COLORS[color], w, color if arrow_end else None)
    return s


def dot(p, color=RED, r=9):
    return circle(p[0], p[1], r, "#ffffff", color, 4)


def tag(x, y, text, size=22, fill=GOLD, color=INK):
    return pill(x, y, text, fill, color, size, stroke=GOLD_DARK)


def steps(y, items, x0=40, x1=1160, size=19):
    """Numbered steps laid out left to right in equal columns."""
    n = len(items)
    w = (x1 - x0) / n
    s = ""
    for i, txt in enumerate(items):
        cx = x0 + i * w
        s += circle(cx + 20, y, 17, NAVY, NAVY, 0)
        s += t(cx + 20, y + 7, str(i + 1), 19, 800, "#ffffff")
        s += t(cx + 46, y + 7 - (txt.count("\n")) * size * 0.62, txt, size, 600, BODY, "start", lh=1.25)
    return s


def interp(x, y, w, left, right, frac, top=("", "", ""), bottom=("", "", ""), color=GOLD_DARK):
    """Interpolation bar: left/right end values, gold marker at frac with the interpolated result."""
    s = line(x, y, x + w, y, INK, 4)
    for xx in (x, x + w):
        s += line(xx, y - 14, xx, y + 14, INK, 4)
    mx = x + frac * w
    s += circle(mx, y, 12, GOLD, GOLD_DARK, 3)
    s += t(x, y - 28, top[0], 20, 700, MUTED)
    s += t(x + w, y - 28, top[2], 20, 700, MUTED)
    s += t(mx, y - 28, top[1], 20, 800, GOLD_DARK)
    s += t(x, y + 46, bottom[0] or left, 24, 800, INK)
    s += t(x + w, y + 46, bottom[2] or right, 24, 800, INK)
    s += pill(mx, y + 46, bottom[1], GOLD, INK, 24, stroke=GOLD_DARK)
    return s


def band(x, y, widths, labels, h=40, fill=NAVY, size=19):
    """Header band with spanning cells: widths and labels are parallel lists."""
    s = ""
    for w, lab in zip(widths, labels):
        s += f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h}" fill="{fill}" stroke="{LINE}" stroke-width="1.5"/>\n'
        if lab:
            s += t(x + w / 2, y + h / 2 + size * 0.36, lab, size, 800, "#ffffff")
        x += w
    return s
