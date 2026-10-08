"""Human Performance explanation pictures, phone-first (docs/EXPLANATION_ILLUSTRATION_STANDARD.md).

Human Performance mostly shows the textbook figures (they stay); these are the approach illusions the textbook
describes in words only. Built from scene.py parts and the flight-path helpers in fp_phone.py; the pilot's-eye
runway views are true perspective (3° approach, 1.5 km out).
"""
import math
import random

from common import Registry
from fp_phone import FP_DEFS, curve, plane_on, track
from kit import template
from scene import (COMMON_DEFS, INK, NAVY_BLUE, RED, TXT_L, TXT_M, W, defs, label, path, stack, stack_height, stars,
                   terrain)

R = Registry("human-performance", "/explanation-images/human-performance/refined-batch-11")

SLATE = "#465569"


def picture(panels):
    body, _ = stack(panels)
    return defs(*COMMON_DEFS, *FP_DEFS) + body


# ------------------------------------------------------------------ runway slope (side view)

SL_H = 440
NORMAL = 20          # the familiar approach angle, drawn steep so the difference shows on a phone
SLOPE = 8            # runway slope, exaggerated the same way


def slope_panel(up):
    def draw(w, h):
        thr = (520, 360)
        k = math.tan(math.radians(SLOPE)) * (1 if up else -1)
        far = (w + 10, thr[1] - k * (w + 10 - thr[0]))
        ground = lambda x: thr[1] if x < thr[0] else thr[1] - k * (x - thr[0])  # noqa: E731
        s = terrain(ground, w, h, "url(#ground_day)")
        s += path(f"M {thr[0]},{thr[1]} L {far[0]:.0f},{far[1]:.0f}", "none", SLATE, 12)
        # the pilot copies the familiar picture: the same angle to the runway surface
        flown = NORMAL - SLOPE if up else NORMAL + SLOPE
        start = 40
        normal = [(start, thr[1] - (thr[0] - start) * math.tan(math.radians(NORMAL))), thr]
        fly = curve([(start, thr[1] - (thr[0] - start) * math.tan(math.radians(flown))), (thr[0] - 6, thr[1] - 3)])
        s += track(normal, INK, w=4, dash="14 10")
        s += track(fly, RED, "nh_red")
        s += plane_on(fly, 0.3, 120, pitch=-3)
        s += label(30, 60 if up else 360, "Normal approach", TXT_M, INK)
        return s
    return dict(h=SL_H, sky="sky_day", draw=draw, color=RED,
                caption="UPSLOPE: FEELS HIGH, FLOWN LOW" if up else "DOWNSLOPE: FEELS LOW, FLOWN HIGH")


@R.add(2108, "runway-slope-illusion-v1", "Runway Slope Illusion",
       template("AN UPSLOPING RUNWAY MAKES YOU FEEL TOO HIGH", "SO THE APPROACH IS FLOWN LOW"),
       h=stack_height([SL_H, SL_H]), w=W)
def _():
    return picture([slope_panel(True), slope_panel(False)])


# ------------------------------------------------------------------ runway width (pilot's eye view)

WD_H = 440
HORIZON = 130
F = 5000                   # focal length in canvas units
DIST, LENGTH = 1500.0, 1500.0
EYE = DIST * math.tan(math.radians(3))


def project(x, z):
    """Ground point x metres right of the centreline, z metres ahead -> canvas point."""
    return 450 + F * x / z, HORIZON + F * EYE / z


def runway_view(width, outline=False):
    a, b = project(-width / 2, DIST), project(width / 2, DIST)
    c, d = project(width / 2, DIST + LENGTH), project(-width / 2, DIST + LENGTH)
    pts = " L ".join(f"{x:.1f},{y:.1f}" for x, y in (a, b, c, d))
    if outline:
        return path(f"M {pts} Z", "none", "#ffffff", 5, ' stroke-dasharray="14 9"')
    s = path(f"M {pts} Z", SLATE, "#2f3a49", 2)
    for k in range(12):   # centreline dashes, 30 m long every 100 m
        z0, z1 = DIST + 60 + k * 120, DIST + 90 + k * 120
        if z1 > DIST + LENGTH - 40:
            break
        p0, p1 = project(-0.45, z0), project(0.45, z0)
        p2, p3 = project(0.45, z1), project(-0.45, z1)
        s += path(f"M {p0[0]:.1f},{p0[1]:.1f} L {p1[0]:.1f},{p1[1]:.1f} L {p2[0]:.1f},{p2[1]:.1f} L {p3[0]:.1f},{p3[1]:.1f} Z",
                  "#ffffff")
    for k in range(8):    # threshold bars
        x0 = -width / 2 + width * (0.06 + k * 0.115)
        q = [project(x0, DIST + 6), project(x0 + width * 0.07, DIST + 6), project(x0 + width * 0.07, DIST + 36),
             project(x0, DIST + 36)]
        s += path("M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in q) + " Z", "#ffffff")
    return s


def width_panel(narrow):
    def draw(w, h):
        s = f'<rect x="0" y="{HORIZON}" width="{w}" height="{h - HORIZON}" fill="url(#aerial)"/>'
        s += path(f"M 0,{HORIZON} L {w},{HORIZON}", "none", "#6b8f5a", 3)
        s += runway_view(23 if narrow else 92)
        s += runway_view(46, outline=True)
        s += label(450, 70, "Dashed: the familiar 46 m width", TXT_M, INK, "middle")
        return s
    return dict(h=WD_H, sky="sky_day", draw=draw, color=RED,
                caption="NARROW: FEELS HIGH, FLOWN LOW" if narrow else "WIDE: FEELS LOW, FLOWN HIGH")


@R.add(2158, "runway-width-illusion-v1", "Runway Width Illusion",
       template("A NARROW RUNWAY MAKES YOU FEEL TOO HIGH", "SO THE APPROACH IS FLOWN LOW"),
       h=stack_height([WD_H, WD_H]), w=W)
def _():
    return picture([width_panel(True), width_panel(False)])


# ------------------------------------------------------------------ black hole approach (night, side view)

BH_H = 480


def black_hole_panel():
    def draw(w, h):
        g = 380
        s = stars(random.Random(7), (0, 0, w, 220), 50)
        s += terrain(lambda x: g, w, h, "url(#ground_night)")
        thr = (600, g)
        s += path(f"M {thr[0]},{g} L {w},{g}", "none", "#1f2937", 10)
        for x in range(thr[0], w, 34):   # runway edge lights: the only lights in view
            s += f'<circle cx="{x}" cy="{g - 4}" r="5" fill="#fde68a"/><circle cx="{x}" cy="{g - 4}" r="11" fill="#fde68a" fill-opacity="0.25"/>'
        normal = [(40, g - (thr[0] - 40) * math.tan(math.radians(14))), thr]
        fly = curve([(40, normal[0][1]), (250, normal[0][1] + 75), (430, g - 3)])
        s += track(normal, "#cbd5e1", w=4, dash="14 10")
        s += track(fly, RED, "nh_red")
        s += plane_on(fly, 0.18, 120, pitch=-3)
        s += label(30, 70, "Normal approach", TXT_M, "#e2e8f0", halo="#0b1020")
        s += label(430, g + 70, "Lands short", TXT_L, "#fca5a5", "middle", halo="#0b1020")
        return s
    return dict(h=BH_H, sky="sky_night", draw=draw, color=RED, caption="BLACK HOLE: FEELS HIGH, FLOWN LOW")


@R.add(2795, "black-hole-approach-v1", "Black Hole Approach",
       template("ONLY THE RUNWAY LIGHTS: YOU FEEL TOO HIGH", "SO THE APPROACH IS FLOWN LOW AND SHORT"),
       h=stack_height([BH_H]), w=W)
def _():
    return picture([black_hole_panel()])
