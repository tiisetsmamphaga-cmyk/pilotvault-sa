"""Radio Telephony explanation pictures, phone-first (docs/EXPLANATION_ILLUSTRATION_STANDARD.md).

Ground movement (backtrack, line up and wait) and the ground-air emergency signals as aerial scenes in the
Navigation style, built from scene.py parts: the measured top-view aircraft, runway_close / taxiway, and the
handbook's signal strips (white, 2.5 m by 0.6 m). No PilotVault picture or manual figure showed these ideas as
a scene (the handbook gives the signals as letters only), so they are drawn from the shared parts.
"""
import math

from common import Registry
from fp_phone import FP_DEFS, at, curve, track
from kit import template
from scene import (COMMON_DEFS, NAVY_BLUE, RED, TXT_L, TXT_M, W, aircraft_top, defs, ground_above, label,
                   runway_close, signal_strip, stack, stack_height, taxiway)

R = Registry("radio-telephony", "/explanation-images/radio-telephony/refined-batch-2")

GREEN = "#15803d"
GRASS = "#dfe8cf"


def picture(panels):
    body, _ = stack(panels)
    return defs(*COMMON_DEFS, *FP_DEFS) + body


def plane_top_on(dense, f, span=120):
    """Top-view aircraft on its taxi path a fraction f along, nose along the path."""
    (x, y), ang = at(dense, f)
    return aircraft_top(x, y, span, heading=(90 - ang) % 360)


# ------------------------------------------------------------------ the airfield: runway in use to the right

RWY_Y, RWY_X, RWY_W = 250, 40, 200
GM_H = 560


def airfield(w, h, seed, taxi_x):
    """Grass, the runway (threshold on the left, in use towards the right) and a taxiway from the bottom edge
    joining it at taxi_x, with its holding point."""
    s = ground_above(w, h, seed=seed, river=False, road=False)
    edge = RWY_Y + RWY_W / 2
    s += taxiway([(taxi_x, h + 20), (taxi_x, RWY_Y)], 76, hold=(taxi_x, edge + 95, -90))
    return s + runway_close(RWY_X, RWY_Y, w + 40, RWY_W)


def in_use_arrow(x0, x1, y):
    """The runway direction in use: a green arrow above the runway with its label."""
    s = track([(x0, y), (x1, y)], GREEN, "nh_green")
    return s + label(x0, y - 22, "Runway in use", TXT_M, GREEN, halo=GRASS)


# ------------------------------------------------------------------ backtrack

def backtrack_panel():
    def draw(w, h):
        s = airfield(w, h, 41, 640)
        s += in_use_arrow(470, 860, 95)
        y_out, y_back = RWY_Y + 45, RWY_Y - 25
        path = curve([(640, h - 40), (640, 400), (600, y_out), (480, y_out), (200, y_out), (115, y_out - 10),
                      (95, (y_out + y_back) / 2), (130, y_back), (250, y_back)], 24)
        s += track(path, RED, "nh_red")
        s += plane_top_on(path, 0.45)
        s += label(330, y_out + 105, "Backtrack", TXT_L, RED, "middle", halo=GRASS)
        return s
    return dict(h=GM_H, sky="aerial", draw=draw, caption="BACKTRACK: TAXI BACK DOWN THE RUNWAY",
                color=RED)


@R.add(506, "backtrack-v1", "Backtrack",
       template("BACKTRACK: TAXI ALONG THE RUNWAY IN USE, AGAINST THE LANDING AND TAKE-OFF DIRECTION",
                "USUALLY TO TURN ROUND AT THE END AND LINE UP"),
       h=stack_height([GM_H]), w=W)
def _():
    return picture([backtrack_panel()])


# ------------------------------------------------------------------ line up and wait

def line_up_panel():
    def draw(w, h):
        s = airfield(w, h, 43, 330)
        s += in_use_arrow(470, 860, 95)
        path = curve([(330, h - 40), (330, 420), (338, RWY_Y + 70), (390, RWY_Y + 8), (470, RWY_Y)], 24)
        s += track(path, NAVY_BLUE, "nh_navy")
        s += aircraft_top(550, RWY_Y, 120, heading=90)
        s += label(500, RWY_Y + 160, "Wait: no take-off\nuntil cleared", TXT_M, RED, "start", halo=GRASS)
        return s
    return dict(h=GM_H, sky="aerial", draw=draw, caption="LINE UP AND WAIT ON THE RUNWAY", color=NAVY_BLUE)


@R.add(518, "line-up-and-wait-v1", "Line Up and Wait",
       template("LINE UP AND WAIT: TAXI ONTO THE RUNWAY, LINE UP, AND HOLD THERE",
                "DO NOT START THE TAKE-OFF ROLL UNTIL CLEARED FOR TAKE-OFF"),
       h=stack_height([GM_H]), w=W)
def _():
    return picture([line_up_panel()])


# ------------------------------------------------------------------ ground-air emergency signals

SIG_H = 470
STRIP = 92          # one strip; letters are laid with two strips per arm


def letter(kind, cx, cy, size):
    """V or X laid out with signal strips, two per arm, `size` = height of the letter."""
    s = ""
    half = 30 if kind == "V" else 38          # arm angle from the vertical
    if kind == "V":
        arms = [((cx - size * math.tan(math.radians(half)), cy - size / 2), (cx, cy + size / 2)),
                ((cx + size * math.tan(math.radians(half)), cy - size / 2), (cx, cy + size / 2))]
    else:
        dx = size / 2 * math.tan(math.radians(half))
        arms = [((cx - dx, cy - size / 2), (cx + dx, cy + size / 2)), ((cx + dx, cy - size / 2), (cx - dx, cy + size / 2))]
    for (x0, y0), (x1, y1) in arms:
        ang = math.degrees(math.atan2(y1 - y0, x1 - x0))
        n = max(2, round(math.dist((x0, y0), (x1, y1)) / STRIP))
        for k in range(n):
            t = (k + 0.5) / n
            s += signal_strip(x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, math.dist((x0, y0), (x1, y1)) / n - 4, ang)
    return s


def signal_panel(kind):
    def draw(w, h):
        s = ground_above(w, h, seed=51 if kind == "V" else 53, river=False, road=True)
        s += aircraft_top(220, 250, 230, heading=200, prop=False)
        s += letter(kind, 620, 235, 210)
        return s
    medical = kind == "X"
    return dict(h=SIG_H, sky="aerial", draw=draw,
                caption="X: REQUIRE MEDICAL ASSISTANCE" if medical else "V: REQUIRE ASSISTANCE",
                color=RED if medical else NAVY_BLUE)


@R.add(570, "ground-signals-v-x-v1", "Ground Signals: V and X",
       template("V = REQUIRE ASSISTANCE", "X = REQUIRE MEDICAL ASSISTANCE"),
       h=stack_height([SIG_H, SIG_H]), w=W)
def _():
    return picture([signal_panel("V"), signal_panel("X")])
