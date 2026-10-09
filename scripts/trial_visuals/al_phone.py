"""Air Law trial pictures, phone-first (docs/EXPLANATION_ILLUSTRATION_STANDARD.md).

VFR minima: the radio handbook's "VFR minima for aeroplanes" figure (prepared by al_figures.py) with phone-size
labels for the band each question asks about. Head-on and long navigation flight: aerial scenes in the
Navigation style, built from scene.py parts (measured top-view aircraft, airfields) and smooth tracks.
"""
from pathlib import Path

from common import Registry
from fp_phone import FP_DEFS, curve, track
from kit import embed, template
from scene import (COMMON_DEFS, INK, NAVY_BLUE, RED, TXT_L, TXT_M, W, aircraft_top, defs, ground_above, label,
                   runway_above, stack, stack_height)

R = Registry("air-law", "/explanation-images/air-law/refined-batch-2")

FIG = Path(__file__).resolve().parent / "fig" / "al"
SRC_W, SRC_H = 699, 491          # the handbook figure (cropped); label positions below are in its pixels
K = W / SRC_W
VFR_H = round(SRC_H * K)


def picture(panels):
    body, _ = stack(panels)
    return defs(*COMMON_DEFS, *FP_DEFS) + body


def vfr_panel(caption, labels):
    def draw(w, h):
        s, *_ = embed(FIG / "vfr-minima.png", 0, 0, w, h)
        for x, y, text, anchor in labels:
            s += label(x * K, y * K, text, TXT_M, INK, anchor)
        return s
    return dict(h=VFR_H, sky="sky_day", draw=draw, caption=caption, color=NAVY_BLUE)


@R.add(1403, "vfr-minima-above-fl100-v1", "VFR Minima Above FL100",
       template("ABOVE FL100: 8 KM VISIBILITY", "1.5 KM HORIZONTALLY AND 1000 FT VERTICALLY FROM CLOUD"),
       h=stack_height([VFR_H]), w=W)
def _():
    return picture([vfr_panel("ABOVE FL100: 8 KM, 1.5 KM, 1000 FT",
                              [(480, 106, "8 km visibility", "end"), (20, 28, "1.5 km · 1000 ft", "start")])])


@R.add(1062, "vfr-minima-below-fl100-v1", "VFR Minima Below FL100",
       template("BELOW FL100: 5 KM VISIBILITY", "1.5 KM HORIZONTALLY AND 1000 FT VERTICALLY FROM CLOUD"),
       h=stack_height([VFR_H]), w=W)
def _():
    return picture([vfr_panel("BELOW FL100: 5 KM, 1.5 KM, 1000 FT",
                              [(392, 284, "5 km visibility", "end"), (300, 158, "1.5 km · 1000 ft", "end")])])


@R.add(1049, "vfr-minima-low-v1", "VFR Minima at Low Level",
       template("LOW LEVEL, UNCONTROLLED: 5 KM, CLEAR OF CLOUD", "WITH THE SURFACE IN SIGHT"),
       h=stack_height([VFR_H]), w=W)
def _():
    return picture([vfr_panel("LOW LEVEL: 5 KM, CLEAR OF CLOUD",
                              [(485, 372, "5 km visibility", "end"), (405, 412, "Clear of cloud", "start")])])


# ------------------------------------------------------------------ head-on: both turn right

HO_H = 560


def head_on_panel():
    def draw(w, h):
        s = ground_above(w, h, seed=21)
        a = curve([(60, 280), (300, 280), (390, 320), (430, 430)])      # eastbound, turning right (south)
        b = curve([(840, 280), (600, 280), (510, 240), (470, 130)])     # westbound, turning right (north)
        s += track(a, NAVY_BLUE, "nh_navy") + track(b, RED, "nh_red")
        s += aircraft_top(150, 280, 120, heading=90) + aircraft_top(750, 280, 120, heading=270)
        s += label(60, 210, "Turns right", TXT_M, NAVY_BLUE, halo="#dfe8cf")
        s += label(840, 380, "Turns right", TXT_M, RED, "end", halo="#dfe8cf")
        return s
    return dict(h=HO_H, sky="aerial", draw=draw, caption="HEAD-ON: BOTH TURN RIGHT", color=INK)


@R.add(1028, "head-on-turn-right-v1", "Head-on: Both Turn Right",
       template("HEAD-ON: BOTH AIRCRAFT ALTER HEADING TO THE RIGHT", "THEY PASS LEFT SIDE TO LEFT SIDE"),
       h=stack_height([HO_H]), w=W)
def _():
    return picture([head_on_panel()])


# ------------------------------------------------------------------ PPL long navigation flight

LN_H = 620


def long_nav_panel():
    def draw(w, h):
        s = ground_above(w, h, seed=33)
        base, a, b = (160, 480), (560, 130), (770, 470)
        for p, hdg in ((base, 20), (a, 120), (b, 160)):
            s += runway_above(p[0], p[1], 150, hdg)
        for p, q in ((base, a), (a, b), (b, base)):
            s += track([p, q], NAVY_BLUE, "nh_navy", dash="")
        s += label(60, 560, "Base", TXT_L, INK, halo="#dfe8cf")
        s += label(600, 70, "50 NM+ from base", TXT_M, RED, "start", halo="#dfe8cf")
        return s
    return dict(h=LN_H, sky="aerial", draw=draw, caption="150 NM, 2 FULL-STOP LANDINGS AWAY", color=NAVY_BLUE)


@R.add(910, "ppl-long-nav-v1", "PPL Long Navigation Flight",
       template("150 NM, ONE POINT 50 NM FROM BASE, TWO FULL-STOP LANDINGS AWAY"),
       h=stack_height([LN_H]), w=W)
def _():
    return picture([long_nav_panel()])
