"""Aircraft Technical and General trial pictures, phone-first (docs/EXPLANATION_ILLUSTRATION_STANDARD.md).

Built on the Aircraft General Knowledge manual's own figures, upscaled to HD by atg_figures.py: each picture keeps
the textbook figure and adds at most two phone-size labels and a caption, replacing the manual's small print.
"""
from pathlib import Path

import math

from PIL import Image

from common import Registry
from kit import embed, template
from nav_phone import NAV_DEFS, NORTH_H, north_panel
from scene import (BLUE, COMMON_DEFS, GOLD, INK, NAVY_BLUE, RED, TXT_L, TXT_M, W, circle, defs, flow, head, label,
                   lg, path, stack, stack_height)

R = Registry("aircraft-technical-and-general", "/explanation-images/aircraft-technical-and-general/refined-batch-1")

FIG = Path(__file__).resolve().parent / "fig" / "atg"


OIL = "#e0a526"
FLUID = "#d63a24"
METAL = "#9aa4b2"
DARK = "#334155"
ATG_DEFS = (head("hd_navy", NAVY_BLUE, 30), head("hd_red", RED, 30), head("ring_blue", BLUE, 70), head("ring_red", RED, 70),
            lg("oil", [(0, "#f6c95a"), (1, "#d99a1c")]), lg("steel", [(0, "#e5e9ef"), (1, "#8d97a6")]))


def picture(panels):
    body, _ = stack(panels)
    return defs(*COMMON_DEFS, *NAV_DEFS, *ATG_DEFS) + body


def polar(cx, cy, r, deg):
    """Point at `deg` clockwise from straight up."""
    return cx + r * math.sin(math.radians(deg)), cy - r * math.cos(math.radians(deg))


def arc(cx, cy, r, a0, a1, n=60):
    pts = [polar(cx, cy, r, a0 + (a1 - a0) * i / n) for i in range(n + 1)]
    return "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in pts)


def figure_panel(name, caption, color, labels=(), crop=None, covers=(), strokes=()):
    """One HD manual figure filling the panel width. All positions are in figure pixels: labels
    (x, y, text, colour, anchor); covers = rectangles of print too small for a phone, filled with the paper colour
    beside them; strokes = leader lines of that print, painted over in the paper colour."""
    im = Image.open(FIG / f"{name}.png").convert("RGB")
    x0, y0, x1, y1 = crop or (0, 0, im.width, im.height)
    k = W / (x1 - x0)

    def paper(x, y):
        r, g, b = im.getpixel((max(min(x, im.width - 1), 0), max(min(y, im.height - 1), 0)))
        return f"#{r:02x}{g:02x}{b:02x}"

    def draw(pw, ph):
        s, *_ = embed(FIG / f"{name}.png", -x0 * k, -y0 * k, im.width * k, im.height * k)
        for a, b, c, d in covers:
            s += (f'<rect x="{(a - x0) * k:.1f}" y="{(b - y0) * k:.1f}" width="{(c - a) * k:.1f}" '
                  f'height="{(d - b) * k:.1f}" fill="{paper(a - 6, b)}"/>')
        for pts, width in strokes:
            d = "M " + " L ".join(f"{(x - x0) * k:.1f},{(y - y0) * k:.1f}" for x, y in pts)
            s += f'<path d="{d}" fill="none" stroke="{paper(pts[0][0] - 12, pts[0][1])}" stroke-width="{width * k:.1f}"/>'
        for x, y, text, col, anchor in labels:
            s += label((x - x0) * k, (y - y0) * k, text, TXT_M, col, anchor)
        return s
    return dict(h=round((y1 - y0) * k), sky="sky_day", draw=draw, caption=caption, color=color)


def one(panel):
    return dict(h=stack_height([panel["h"]]), w=W), panel


def add(qid, slug, title, card, panel):
    size, p = one(panel)
    R.add(qid, slug, title, card, **size)(lambda: picture([p]))


# ------------------------------------------------------------------ airframe

add(2428, "semi-cantilever-struts-v1", "Semi-cantilever Monoplane",
    template("SEMI-CANTILEVER: STRUTS FROM THE LOWER FUSELAGE BRACE THE WING"),
    figure_panel("braced-monoplane", "SEMI-CANTILEVER: STRUTS BRACE THE WING", RED,
                 [(1010, 860, "Bracing struts", RED, "start")], crop=(0, 120, 1964, 1000)))

# ------------------------------------------------------------------ engine

add(2525, "cylinder-cooling-fins-v1", "Cylinder Cooling Fins",
    template("FINS GIVE THE CYLINDER MORE AREA TO LOSE HEAT"),
    figure_panel("cylinder-fins", "FINS ADD AREA TO LOSE HEAT", RED,
                 [(690, 590, "Cooling fins", RED, "middle")]))




# ------------------------------------------------------------------ valve lead: the manual's valve timing diagram
# Redrawn from the AGK manual's timing circle: TDC at the top, crankshaft turning clockwise; inlet opens 20 deg
# before TDC and closes 71 deg after BDC; exhaust opens 62 deg before BDC and closes 29 deg after TDC.

VT_H = 760


def valve_timing_panel():
    def draw(w, h):
        cx, cy = 450, 410
        s = path(f"M {cx},{cy - 345} L {cx},{cy + 345}", "none", "#94a3b8", 4, ' stroke-dasharray="14 10"')
        s += path(arc(cx, cy, 290, -20, 245), "none", BLUE, 30, ' marker-end="url(#ring_blue)"')
        s += path(arc(cx, cy, 215, 118, 383), "none", RED, 30, ' marker-end="url(#ring_red)"')
        ivo = polar(cx, cy, 290, -20)
        s += circle(*ivo, 22, NAVY_BLUE, "#ffffff", 5)
        s += path(arc(cx, cy, 340, -20, 0), "none", GOLD, 8)
        s += circle(cx, cy, 34, "url(#steel)", DARK, 4)
        s += label(cx, 50, "TDC", TXT_L, INK, "middle")
        s += label(300, 92, "Inlet opens\nbefore TDC", TXT_M, NAVY_BLUE, "end")
        return s
    return dict(h=VT_H, sky="chart_paper", draw=draw, caption="VALVE LEAD: INLET OPENS BEFORE TDC", color=NAVY_BLUE)


@R.add(2474, "valve-lead-v1", "Valve Lead", template("VALVE LEAD: THE INLET VALVE OPENS BEFORE TDC"),
       h=stack_height([VT_H]), w=W)
def _():
    return picture([valve_timing_panel()])


# ------------------------------------------------------------------ gear-type oil pump
# Redrawn from the manual's gear pump: inlet at the top of the mesh, outlet at the bottom, oil carried round the
# outside between the teeth, and a spring-loaded ball relief valve returning excess outlet oil to the inlet.

GP_H = 720


def gear(cx, cy, n=12, r_tip=132, r_root=106, phase=0.0):
    pts = []
    for i in range(n):
        a = 360 / n * i + phase
        for da, r in ((-0.30, r_root), (-0.16, r_tip), (0.16, r_tip), (0.30, r_root)):
            pts.append(polar(cx, cy, r, a + da * 360 / n))
    d = "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z"
    return (path(d, "url(#steel)", DARK, 4) + circle(cx, cy, 40, "#cbd5e1", DARK, 4) + circle(cx, cy, 13, DARK))


def pipe(d, w=64):
    return path(d, "none", DARK, w + 10) + path(d, "none", OIL, w)


def gear_pump_panel():
    def draw(w, h):
        L, Rg, cy = (310, 400), (570, 400), 400
        s = pipe("M 440,-20 L 440,330")                                   # inlet
        s += pipe(f"M 440,470 L 440,{h + 20}")                              # outlet
        s += pipe("M 440,640 L 790,640 L 790,120 L 440,120", 46)           # relief return to the inlet
        s += path("M 760,330 L 820,330 L 820,470 L 760,470 Z", "#fde68a", DARK, 6)     # valve chamber
        s += path("M 772,342 " + " ".join(f"L {772 + (36 if i % 2 else 0)},{342 + 13 * (i + 1)}" for i in range(7)),
                  "none", DARK, 5)                                          # spring
        s += circle(790, 440, 24, "url(#steel)", DARK, 4)                   # ball on its seat
        for c in (L, Rg):
            s += circle(*c, 160, DARK) + circle(*c, 150, "url(#oil)")
        s += path(f"M {L[0]},{cy - 150} L {Rg[0]},{cy - 150} L {Rg[0]},{cy + 150} L {L[0]},{cy + 150} Z", "url(#oil)")
        s += gear(*L, phase=15) + gear(*Rg, phase=0)
        s += path(arc(*L, 190, -40, -150), "none", NAVY_BLUE, 6, ' marker-end="url(#hd_navy)"')
        s += path(arc(*Rg, 190, 40, 150), "none", NAVY_BLUE, 6, ' marker-end="url(#hd_navy)"')
        s += label(392, 70, "Inlet", TXT_L, INK, "end")
        s += label(392, h - 40, "Outlet", TXT_L, INK, "end")
        return s
    return dict(h=GP_H, sky="chart_paper", draw=draw, caption="GEAR PUMP: OIL CARRIED ROUND THE TEETH",
                color=NAVY_BLUE)


@R.add(2520, "gear-oil-pump-v1", "Gear-type Oil Pump",
       template("A GEAR-TYPE PUMP SUPPLIES PRESSURE OIL; SPLASH DOES THE REST"), h=stack_height([GP_H]), w=W)
def _():
    return picture([gear_pump_panel()])


# ------------------------------------------------------------------ hydraulic brake: Pascal's law
# Redrawn from the manual's brake figure (positions scaled 0.632 from it): pedal and push rod into the master
# cylinder under its reservoir, a fluid line to the slave cylinder in the caliper gripping the disc by the wheel.

HB_H = 760


def brake_panel():
    def draw(w, h):
        s = path("M 30,250 L 170,250 L 170,730 L 30,730 Z", "#3f3f46", "#18181b", 5)          # tyre, edge on
        for x in (55, 80, 105, 130, 150):
            s += path(f"M {x},262 L {x},718", "none", "#27272a", 4)
        s += path("M 214,410 L 246,410 L 246,650 L 214,650 Z", "url(#steel)", DARK, 4)          # disc
        s += path("M 190,312 L 300,312 L 300,440 L 190,440 Z", "#cbd5e1", DARK, 5)              # caliper
        s += path("M 252,350 L 300,350 L 300,400 L 252,400 Z", FLUID)                          # slave cylinder
        s += path("M 230,350 L 252,350 L 252,400 L 230,400 Z", GOLD, DARK, 3)                  # piston and pad
        s += path("M 300,375 L 380,375", "none", FLUID, 22)                                     # fluid line
        s += path("M 360,330 L 520,330 L 520,430 L 360,430 Z", "#cbd5e1", DARK, 5)              # master cylinder
        s += path("M 368,340 L 450,340 L 450,420 L 368,420 Z", FLUID)
        s += path("M 450,340 L 478,340 L 478,420 L 450,420 Z", "url(#steel)", DARK, 3)          # piston
        s += path("M 478,380 L 690,380", "none", DARK, 12)                                      # push rod
        s += path("M 420,240 L 420,332", "none", FLUID, 16)
        s += path("M 340,90 L 600,90 L 600,245 L 340,245 Z", FLUID, DARK, 5)                     # reservoir
        s += path("M 340,90 L 600,90 L 600,130 L 340,130 Z", "#fde68a", DARK, 5)
        s += path("M 430,70 L 510,70 L 510,90 L 430,90 Z", "url(#steel)", DARK, 4)
        s += path("M 610,270 L 845,520", "none", "#1f2937", 26)                                 # pedal
        s += circle(845, 520, 16, "url(#steel)", DARK, 4)
        s += path("M 870,290 L 770,290 L 770,250 L 700,320 L 770,390 L 770,350 L 870,350 Z", RED)  # foot force
        s += label(560, 482, "Master cylinder", TXT_M, INK, "middle")
        s += label(262, 495, "Slave\ncylinder", TXT_M, INK, "start")
        return s
    return dict(h=HB_H, sky="chart_paper", draw=draw, caption="PRESSURE IS PASSED ON THROUGH THE FLUID", color=RED)


@R.add(2559, "hydraulic-brake-pascal-v1", "Hydraulic Brakes: Pascal's Law",
       template("PRESSURE ON A CONFINED FLUID IS TRANSMITTED THROUGH IT"), h=stack_height([HB_H]), w=W)
def _():
    return picture([brake_panel()])


# ------------------------------------------------------------------ engine cooling: baffles and the cowl flap
# Redrawn from the manual's cooling figure (scaled 0.42 from it): air enters the front of the cowling, is forced
# down between the cylinders by the inter-cylinder baffles, and leaves heated past the cowl flap at the firewall.

EC_H = 650
CYL = (300, 458, 612)


def cooling_panel(focus):
    def draw(w, h):
        s = path("M 28,12 L 28,560", "none", "#64748b", 12)                                    # firewall
        s += path("M 28,14 L 660,14 Q 760,18 800,40", "none", "#64748b", 12)                   # upper cowling
        s += path("M 800,300 L 230,540", "none", "#64748b", 12)                                # lower cowling
        s += path("M 230,540 L 130,620", "none", RED if focus == "flap" else DARK, 16)          # cowl flap, open
        s += circle(230, 540, 11, "url(#steel)", DARK, 4)
        s += path("M 110,196 L 720,196 L 720,216 L 110,216 Z", "#64748b")                      # crankcase
        for x in CYL:
            s += circle(x, 205, 66, "url(#steel)", DARK, 4)
            for r in (50, 36, 22):
                s += circle(x, 205, r, "none", "#64748b", 3)
            s += path(arc(x, 205, 80, 105, 255), "none", NAVY_BLUE if focus == "baffle" else "#111827", 8)
        for y, x_end in ((70, 379), (120, 535)):
            s += flow([(880, y), (700, y - 10), (520, y), (x_end, y + 40), (x_end, 255)], BLUE, "head_blue", 8)
        for x0, mid, end in ((379, (149, 440), (66, 600)), (535, (305, 450), (112, 612))):
            s += flow([(x0, 300), (x0 - 90, 370), mid, end], RED, "head_red", 8)
        if focus == "flap":
            s += label(250, 625, "Cowl flap", TXT_M, RED, "start")
        else:
            s += label(600, 395, "Baffles", TXT_M, NAVY_BLUE, "start")
        s += label(890, 175, "Cooling air", TXT_M, BLUE, "end")
        return s
    caption = ("THE COWL FLAP CONTROLS THE COOLING AIR" if focus == "flap" else "BAFFLES DIRECT AIR OVER THE CYLINDERS")
    return dict(h=EC_H, sky="chart_paper", draw=draw, caption=caption, color=RED if focus == "flap" else NAVY_BLUE)


@R.add(2553, "cowl-flap-v1", "Cowl Flap",
       template("COWL FLAPS CONTROL THE COOLING AIRFLOW OVER THE CYLINDERS"), h=stack_height([EC_H]), w=W)
def _():
    return picture([cooling_panel("flap")])


@R.add(2564, "engine-baffles-v1", "Engine Baffles",
       template("BAFFLES DIRECT THE COOLING AIR OVER THE CYLINDERS"), h=stack_height([EC_H]), w=W)
def _():
    return picture([cooling_panel("baffle")])


# ------------------------------------------------------------------ oil pressure gauge
# Redrawn from the manual's gauge: 0-100 scale, yellow 25-60, green 60-81, yellow 81-100, red limits at 25 and 100.

OG_H = 580


def oil_angle(v):
    return -55 + 110 * v / 100


def oil_gauge_panel():
    def draw(w, h):
        cx, cy, r = 330, 450, 250
        s = path("M 40,40 L 620,40 L 620,540 L 40,540 Z", "#1f2937", "#9ca3af", 10)
        for a, b, col in ((25, 60, "#facc15"), (60, 81, "#22c55e"), (81, 100, "#facc15")):
            s += path(arc(cx, cy, r, oil_angle(a), oil_angle(b)), "none", col, 44)
        for v in (25, 100):
            s += path("M {:.1f},{:.1f} L {:.1f},{:.1f}".format(*polar(cx, cy, r - 26, oil_angle(v)),
                                                             *polar(cx, cy, r + 26, oil_angle(v))), "none", RED, 9)
        for v in (0, 25, 60, 100):
            x, y = polar(cx, cy, r + 55, oil_angle(v))
            s += label(x, y + 14, str(v), TXT_M, "#ffffff", "middle", halo=None)
        x, y = polar(cx, cy, r - 20, oil_angle(0))
        s += path(f"M {cx},{cy} L {x:.1f},{y:.1f}", "none", "#ffffff", 12)
        s += circle(cx, cy, 20, "#e5e7eb", "#111827", 4)
        s += label(cx, 515, "OIL PRESS", TXT_M, "#ffffff", "middle", halo=None)
        s += label(650, 260, "Still at\nzero", TXT_L, RED, "start")
        return s
    return dict(h=OG_H, sky="chart_paper", draw=draw, caption="NO OIL PRESSURE: SHUT DOWN AT ONCE", color=RED)


@R.add(2773, "oil-pressure-not-rising-v1", "No Oil Pressure After Start",
       template("NO OIL PRESSURE IN TIME: SHUT THE ENGINE DOWN"), h=stack_height([OG_H]), w=W)
def _():
    return picture([oil_gauge_panel()])


# ------------------------------------------------------------------ compass deviation: the Navigation scene

@R.add(2701, "compass-deviation-v1", "Compass Deviation",
       template("DEVIATION: THE AIRCRAFT'S OWN MAGNETIC FIELDS PULL THE COMPASS"), h=stack_height([NORTH_H]), w=W)
def _():
    return picture([north_panel("dev")])
