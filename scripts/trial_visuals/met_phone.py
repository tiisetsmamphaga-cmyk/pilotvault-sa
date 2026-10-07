"""Meteorology explanation pictures, phone-first (docs/EXPLANATION_ILLUSTRATION_STANDARD.md), built from scene.py."""
import math
import random

from common import Registry
from kit import template
from scene import (BLUE, COMMON_DEFS, ICE, RED, TXT_L, TXT_M, W, defs, flow_band, label, moon, path, stack,
                   stack_height, stars, sun, terrain, tree)

R = Registry("meteorology", "/explanation-images/meteorology/refined-batch-2")


def picture(panels):
    body, _ = stack(panels)
    return defs(*COMMON_DEFS) + body


# ------------------------------------------------------------------ anabatic / katabatic (the reference picture)

def ridge_y(x):
    """Valley floor on the left rising smoothly to a ridge on the right."""
    return 410 - 270 / (1 + math.exp(-(x - 560) / 95))


SLOPE = [(x, ridge_y(x) + 2) for x in range(330, 830, 35)]
SLOPE_H = 470


def slope_panel(day):
    def draw(w, h):
        rnd = random.Random(3)
        s = ""
        if day:
            s += sun(600, 92, 42)
        else:
            s += stars(rnd, (380, 15, 890, 200), 45) + moon(600, 88, 36)
        s += terrain(ridge_y, w, h, "url(#ground_day)" if day else "url(#ground_night)", "#5d4a33" if day else "#1f2a2a")
        # the slope surface: warmed by the sun or cooling by radiation
        s += path("M " + " L ".join(f"{x},{ridge_y(x) + 3:.1f}" for x in range(240, w + 1, 10)), "none",
                  "#ffd46b" if day else "#7aa7d9", 9, ' stroke-opacity="0.6"')
        for x, sc in ((60, 1.0), (110, 0.8), (160, 1.1), (835, 0.75), (880, 0.85)):
            s += tree(x, ridge_y(x) + 5, sc, "#2f6b3a" if day else "#1d3326")
        if day:
            s += flow_band(SLOPE, RED, "head_red")
            s += label(36, 82, "Warm air rises\nup the slope", TXT_L, RED)
            s += label(870, 448, "Sun heats the slope", TXT_M, "#3b2f1f", "end", halo="#e9dfc4")
        else:
            pool_top = 374
            x_edge = 560 - 95 * math.log(270 / (410 - pool_top) - 1)
            s += path(f"M 0,{pool_top} L {x_edge:.1f},{pool_top} "
                      + " ".join(f"L {x},{ridge_y(x):.1f}" for x in range(int(x_edge), -1, -5)) + " Z",
                      BLUE, extra=' fill-opacity="0.45"')
            s += flow_band(SLOPE, ICE, "head_ice", reverse=True)
            s += label(36, 82, "Cold, dense air\ndrains downhill", TXT_L, "#ffffff", halo="#0f1d3d")
            s += label(30, 452, "Cold air pools in the valley", TXT_M, "#ffffff", halo="#0f1d3d")
        return s
    return dict(h=SLOPE_H, sky="sky_day" if day else "sky_night", draw=draw,
                caption="DAY — ANABATIC (upslope)" if day else "NIGHT — KATABATIC (downslope)",
                color=RED if day else BLUE)


@R.add(46, "anabatic-katabatic-v3", "Anabatic and Katabatic Winds",
       template("AN ANABATIC WIND BLOWS UP A SLOPE BY DAY",
                "A KATABATIC WIND BLOWS DOWN THE SLOPE AT NIGHT",
                [("Anabatic", "Sun heats the slope, the air in contact warms, becomes less dense and rises"),
                 ("Katabatic", "The slope cools by radiation at night; cold, dense air drains downhill"),
                 ("Memory aid", "ANA = UP (like ascend), KATA = DOWN")]),
       h=stack_height([SLOPE_H, SLOPE_H]), w=W)
def _():
    return picture([slope_panel(True), slope_panel(False)])
