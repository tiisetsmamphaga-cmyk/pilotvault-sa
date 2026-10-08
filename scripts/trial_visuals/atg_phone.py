"""Aircraft Technical and General trial pictures, phone-first (docs/EXPLANATION_ILLUSTRATION_STANDARD.md).

Built on the Aircraft General Knowledge manual's own figures, upscaled to HD by atg_figures.py: each picture keeps
the textbook figure and adds at most two phone-size labels and a caption, replacing the manual's small print.
"""
from pathlib import Path

from PIL import Image

from common import Registry
from kit import embed, template
from scene import COMMON_DEFS, INK, NAVY_BLUE, RED, TXT_M, W, defs, label, stack, stack_height

R = Registry("aircraft-technical-and-general", "/explanation-images/aircraft-technical-and-general/refined-batch-1")

FIG = Path(__file__).resolve().parent / "fig" / "atg"


def picture(panels):
    body, _ = stack(panels)
    return defs(*COMMON_DEFS) + body


def fig_h(name, crop=None):
    w, h = Image.open(FIG / f"{name}.png").size
    if crop:
        w, h = crop[2] - crop[0], crop[3] - crop[1]
    return round(h * W / w)


def figure_panel(name, caption, color, labels=(), crop=None):
    """One HD manual figure filling the panel width; labels (x, y, text, colour, anchor) in figure pixels."""
    w, h = Image.open(FIG / f"{name}.png").size
    x0, y0 = 0, 0
    if crop:
        x0, y0, w, h = crop[0], crop[1], crop[2] - crop[0], crop[3] - crop[1]
    k = W / w
    ph = round(h * k)

    def draw(pw, hh):
        full_w, full_h = Image.open(FIG / f"{name}.png").size
        s, *_ = embed(FIG / f"{name}.png", -x0 * k, -y0 * k, full_w * k, full_h * k)
        for x, y, text, col, anchor in labels:
            s += label((x - x0) * k, (y - y0) * k, text, TXT_M, col, anchor)
        return s
    return dict(h=ph, sky="sky_day", draw=draw, caption=caption, color=color)
