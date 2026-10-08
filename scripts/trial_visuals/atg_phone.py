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
from scene import (BLUE, COMMON_DEFS, GOLD, INK, NAVY_BLUE, RED, TXT_L, TXT_M, W, aircraft, aircraft_front, cg_mark, circle, cumulus,
                   defs, flow, head, label, lg, path, stack, stack_height)

R = Registry("aircraft-technical-and-general", "/explanation-images/aircraft-technical-and-general/refined-batch-1")
HOLD = Registry("aircraft-technical-and-general", "/explanation-images/aircraft-technical-and-general/refined-batch-1")

FIG = Path(__file__).resolve().parent / "fig" / "atg"


def dim_head(mid, color, size=30):
    """Arrowhead for a dimension line: points outwards at both ends (marker-start and marker-end)."""
    return (f'<marker id="{mid}" markerUnits="userSpaceOnUse" markerWidth="{size}" markerHeight="{size}" '
            f'refX="{size * 0.8:.1f}" refY="{size / 2}" orient="auto-start-reverse"><path d="M0,{size * 0.12:.1f} '
            f'L{size * 0.9:.1f},{size / 2} L0,{size * 0.88:.1f} Z" fill="{color}"/></marker>')


OIL = "#e0a526"
FLUID = "#d63a24"
METAL = "#9aa4b2"
DARK = "#334155"
ATG_DEFS = (dim_head("dim_navy", NAVY_BLUE), dim_head("dim_red", RED), head("hd_navy", NAVY_BLUE, 30), head("hd_red", RED, 30), head("ring_blue", BLUE, 70), head("ring_red", RED, 70),
            lg("oil", [(0, "#f6c95a"), (1, "#d99a1c")]), lg("steel", [(0, "#e5e9ef"), (1, "#8d97a6")]))


def picture(panels):
    body, _ = stack(panels)
    return defs(*COMMON_DEFS, *NAV_DEFS, *ATG_DEFS, *LUB_DEFS) + body


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
    hub = r_root * 0.38
    return (path(d, "url(#steel)", DARK, 4) + circle(cx, cy, hub, "#cbd5e1", DARK, 4) + circle(cx, cy, hub / 3, DARK))


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


@HOLD.add(2520, "gear-oil-pump-v1", "Gear-type Oil Pump",
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


# ------------------------------------------------------------------ pitot-static: the ASI
# Redrawn from the textbook pitot-static figure used in Navigation: the pitot tube faces into the airflow and feeds
# the capsule; static pressure from the static vent fills the instrument case around the capsule.

PS_H = 540


def capsule(cx, top, bottom, half_w, folds=5):
    """Corrugated capsule (bellows), drawn with smooth waisted folds like the textbook's diaphragm."""
    step = (bottom - top) / folds
    right = f"M {cx - half_w:.1f},{top:.1f} L {cx + half_w:.1f},{top:.1f} "
    for i in range(folds):
        y0 = top + i * step
        right += f"Q {cx + half_w * 0.72:.1f},{y0 + step / 2:.1f} {cx + half_w:.1f},{y0 + step:.1f} "
    left = f"L {cx - half_w:.1f},{bottom:.1f} "
    for i in range(folds, 0, -1):
        y0 = top + i * step
        left += f"Q {cx - half_w * 0.72:.1f},{y0 - step / 2:.1f} {cx - half_w:.1f},{y0 - step:.1f} "
    s = path(right + left + "Z", "#f9c4bb", RED, 6)
    for i in range(1, folds):
        y = top + i * step
        s += path(f"M {cx - half_w + 4:.1f},{y:.1f} L {cx + half_w - 4:.1f},{y:.1f}", "none", RED, 3)
    return s


def pitot_panel(focus):
    def draw(w, h):
        s = path("M 30,470 L 520,470", "none", "#64748b", 10)                                   # fuselage skin
        s += path("M 150,395 L 150,470", "none", DARK, 26) + path("M 150,395 L 150,470", "none", "#bfdbfe", 14)
        s += path("M 60,90 L 420,90 L 420,395 L 60,395 Z", "#dbeafe", DARK, 8)                    # instrument case
        s += path("M 300,230 L 820,230", "none", DARK, 40) + path("M 300,230 L 830,230", "none", "#f9c4bb", 22)
        s += path("M 806,206 L 830,206 M 806,254 L 830,254", "none", DARK, 8)                    # open mouth
        s += capsule(240, 130, 340, 70)
        for y in (190, 230, 270):
            s += flow([(890, y + (0 if y == 230 else (y - 230) * 0.4)), (845, y)], BLUE, "head_blue", 8)
        s += flow([(150, 520), (150, 482)], BLUE, "head_blue", 7)
        if focus == "capsule":
            s += label(240, 70, "Capsule", TXT_M, RED, "middle")
            s += label(190, 445, "Static vent", TXT_M, NAVY_BLUE, "start")
        else:
            s += label(620, 190, "Pitot tube", TXT_M, RED, "middle")
            s += label(890, 340, "Airflow", TXT_M, BLUE, "end")
        return s
    caption = ("PITOT PRESSURE GOES INTO THE CAPSULE" if focus == "capsule" else "THE PITOT TUBE FACES INTO THE AIRFLOW")
    return dict(h=PS_H, sky="chart_paper", draw=draw, caption=caption, color=RED)


@R.add(2566, "asi-pitot-capsule-v1", "Airspeed Indicator: Pitot and Static",
       template("PITOT PRESSURE GOES INTO THE CAPSULE; STATIC FILLS THE CASE"), h=stack_height([PS_H]), w=W)
def _():
    return picture([pitot_panel("capsule")])


@R.add(2584, "pitot-tube-airflow-v1", "Pitot Tube",
       template("PITOT PRESSURE IS TAKEN FROM A TUBE FACING INTO THE AIRFLOW"), h=stack_height([PS_H]), w=W)
def _():
    return picture([pitot_panel("tube")])


# ------------------------------------------------------------------ propeller torque reaction
# Seen from ahead: the propeller turns one way (anticlockwise from the front, clockwise from the cockpit) and the
# reaction tries to roll the aircraft the other way.

PT_H = 560


def torque_panel():
    def draw(w, h):
        cx, cy, span = 450, 260, 840
        s = aircraft_front(cx, cy, span)
        pc = (cx, cy + 22 * span / 1300)
        s += path(arc(*pc, 105, 60, -200), "none", NAVY_BLUE, 8, ' marker-end="url(#hd_navy)"')
        s += path(arc(cx, cy, 420, 66, 114), "none", RED, 9, ' marker-end="url(#hd_red)"')
        s += path(arc(cx, cy, 420, -114, -66), "none", RED, 9, ' marker-end="url(#hd_red)"')
        s += label(575, 470, "Propeller turns", TXT_M, NAVY_BLUE, "start")
        s += label(450, 530, "Aircraft rolls the other way", TXT_M, RED, "middle")
        return s
    return dict(h=PT_H, sky="sky_day", draw=draw, caption="TORQUE: ACTS OPPOSITE TO THE PROPELLER", color=RED)


@R.add(2450, "propeller-torque-reaction-v1", "Propeller Torque Reaction",
       template("TORQUE REACTION ACTS OPPOSITE TO THE PROPELLER'S ROTATION"), h=stack_height([PT_H]), w=W)
def _():
    return picture([torque_panel()])


# ------------------------------------------------------------------ tailplane: longitudinal stability
# The measured side-view trainer, nose disturbed up or down: the tailplane's angle of attack changes, its force acts
# up or down and pitches the nose back. Tail and centre-of-pressure points are taken from aircraft.py's side view
# (tailplane at local 676,137; wing centre of pressure at 330,160; drawing centred on 385,130).

TS_H = 500
TS_W = 560                # aircraft length on the canvas


def ac_point(cx, cy, pitch, lx, ly, width=TS_W):
    """Canvas position of a point of the side-view aircraft (local units, nose right) flown at `pitch`."""
    k = width / 660
    px, py = -(lx - 385) * k, (ly - 130) * k
    t = math.radians(-pitch)
    return cx + px * math.cos(t) - py * math.sin(t), cy + px * math.sin(t) + py * math.cos(t)


def tail_panel(nose_up):
    pitch = 12 if nose_up else -12

    def draw(w, h):
        cx, cy = 480, 250
        s = aircraft(cx, cy, TS_W, pitch=pitch)
        tx, ty = ac_point(cx, cy, pitch, 758, 137)                  # just aft of the tailplane and fin
        dy = -150 if nose_up else 150
        s += path(f"M {tx:.1f},{ty:.1f} L {tx:.1f},{ty + dy:.1f}", "none", RED, 10, ' marker-end="url(#hd_red)"')
        # the nose is pitched back about the centre of gravity: down after nose-up, up after nose-down
        a0, a1 = (70, 102) if nose_up else (122, 82)
        s += path(arc(cx, cy, 330, a0, a1), "none", NAVY_BLUE, 9, ' marker-end="url(#hd_navy)"')
        s += label(30, ty + dy - 24 if nose_up else ty + dy + 50, "Tail force up" if nose_up else "Tail force down",
                   TXT_M, RED, "start")
        s += label(890, 60, "Nose pushed\nback down" if nose_up else "Nose pushed\nback up", TXT_M, NAVY_BLUE, "end")
        return s
    caption = "NOSE PITCHES UP: TAIL FORCE UP" if nose_up else "NOSE PITCHES DOWN: TAIL FORCE DOWN"
    return dict(h=TS_H, sky="sky_day", draw=draw, caption=caption, color=RED if nose_up else NAVY_BLUE)


@R.add(2464, "tailplane-stability-v1", "Tailplane and Longitudinal Stability",
       template("THE TAILPLANE GIVES LONGITUDINAL STABILITY WITH AN UP OR DOWN FORCE"),
       h=stack_height([TS_H, TS_H]), w=W)
def _():
    return picture([tail_panel(True), tail_panel(False)])


# ------------------------------------------------------------------ CG position and longitudinal stability
# The same side-view trainer, level: with the CG forward the tailplane works on a long arm and its restoring moment
# is strong; with the CG aft the arm is shorter, the restoring moment weaker and the aircraft less stable.

CG_H = 420


def cg_panel(aft):
    def draw(w, h):
        cx, cy = 450, 190
        s = aircraft(cx, cy, TS_W, pitch=0)
        gx, gy = ac_point(cx, cy, 0, 395 if aft else 300, 158)
        tx, _ = ac_point(cx, cy, 0, 676, 137)
        col, mid = (RED, "dim_red") if aft else (NAVY_BLUE, "dim_navy")
        s += cg_mark(gx, gy, 22)
        y = 330
        s += path(f"M {gx:.1f},{y - 26} L {gx:.1f},{y + 26} M {tx:.1f},{y - 26} L {tx:.1f},{y + 26}", "none", col, 4)
        s += path(f"M {gx - 6:.1f},{y} L {tx + 6:.1f},{y}", "none", col, 6,
                  f' marker-start="url(#{mid})" marker-end="url(#{mid})"')
        s += label((gx + tx) / 2, y - 22, "Short tail arm" if aft else "Long tail arm", TXT_M, col, "middle")
        s += label(gx, 136, "CG", TXT_L, INK, "middle")
        return s
    caption = "CG AFT: SHORT ARM, LESS STABLE" if aft else "CG FORWARD: LONG ARM, STABLE"
    return dict(h=CG_H, sky="sky_day", draw=draw, caption=caption, color=RED if aft else NAVY_BLUE)


@R.add(2432, "cg-aft-stability-v1", "CG Position and Longitudinal Stability",
       template("AFT CG: SHORTER TAIL ARM, WEAKER RESTORING MOMENT, LESS STABLE"),
       h=stack_height([CG_H, CG_H]), w=W)
def _():
    return picture([cg_panel(False), cg_panel(True)])


# ------------------------------------------------------------------ lubrication: gear pump pressure plus splash
# An engine cutaway redrawn from the AGK manual's cylinder figure (finned barrel, inclined inlet and exhaust valves,
# piston with three rings, connecting rod, crank in a bell-shaped crankcase; piston width : rod length about
# 1 : 0.88; stroke about 0.65 of the bore, as on flat-four aero engines) and its crankshaft figure (oil drillings through the webs).
# The gear pump in the sump sends pressure oil up a gallery to the main bearing and through the web to the big end;
# the big end throws splash onto the cylinder walls and the underside of the piston.

LB_H = 880
AX, MAIN, PIN, SMALL = 430, (430, 612), (516, 572), (430, 330)
LUB_DEFS = (lg("alu", [(0, "#f1f4f8"), (1, "#c5ced9")]), lg("alu_h", [(0, "#c5ced9"), (0.5, "#f4f6f9"), (1, "#b4bfcc")], 0, 0, 1, 0),
            lg("barrel", [(0, "#9aa5b4"), (0.5, "#e9edf2"), (1, "#8b96a6")], 0, 0, 1, 0),
            lg("chamber", [(0, "#fde9c8"), (1, "#f7d9a8")]))


def drop(x, y, r=9, ang=0):
    return (f'<g transform="rotate({ang:.0f} {x:.1f} {y:.1f})">' +
            path(f"M {x:.1f},{y - r * 1.7:.1f} Q {x + r:.1f},{y - r * 0.1:.1f} {x:.1f},{y + r:.1f} "
                 f"Q {x - r:.1f},{y - r * 0.1:.1f} {x:.1f},{y - r * 1.7:.1f} Z", "url(#oil)", "#a16207", 2) + "</g>")


def valve(x0, y0, ang, length=86):
    """Poppet valve seated at (x0, y0), stem leaning `ang` degrees from vertical, spring round the upper stem."""
    g = f'<g transform="rotate({ang} {x0:.1f} {y0:.1f})">'
    g += path(f"M {x0:.1f},{y0:.1f} L {x0:.1f},{y0 - length:.1f}", "none", DARK, 9)
    g += path(f"M {x0 - 16:.1f},{y0 - 40:.1f} " + " ".join(
        f"L {x0 + (16 if k % 2 else -16):.1f},{y0 - 40 - 7 * (k + 1):.1f}" for k in range(6)), "none", "#64748b", 5)
    g += path(f"M {x0 - 30:.1f},{y0:.1f} L {x0 + 30:.1f},{y0:.1f} L {x0 + 7:.1f},{y0 - 18:.1f} L {x0 - 7:.1f},{y0 - 18:.1f} Z",
              "url(#steel)", DARK, 4)
    return g + "</g>"


def lubrication_panel():
    def draw(w, h):
        bx0, bx1 = AX - 150, AX + 150                      # cylinder bore
        # crankcase (aluminium) and sump
        s = path(f"M {bx0 - 24},380 C 230,420 205,500 205,600 C 205,690 240,730 255,740 L 255,830 "
                 f"Q 255,850 275,850 L 585,850 Q 605,850 605,830 L 605,740 C 620,730 655,690 655,600 "
                 f"C 655,500 630,420 {bx1 + 24},380 Z", "url(#alu)", DARK, 7)
        s += path("M 262,758 Q 300,750 340,758 T 420,758 T 500,758 T 598,758 L 598,843 L 262,843 Z", "url(#oil)")
        # cylinder barrel with cooling fins, oil film on the walls
        for k, y in enumerate(range(150, 372, 22)):
            s += path(f"M {bx0 - 62},{y} L {bx1 + 62},{y} L {bx1 + 62},{y + 10} L {bx0 - 62},{y + 10} Z", "#b4bfcc", "#64748b", 2)
        s += path(f"M {bx0 - 24},120 L {bx1 + 24},120 L {bx1 + 24},382 L {bx0 - 24},382 Z", "url(#barrel)", DARK, 6)
        s += path(f"M {bx0},120 L {bx1},120 L {bx1},385 L {bx0},385 Z", "#eef2f6")
        s += path(f"M {bx0 + 4},250 L {bx0 + 4},380 M {bx1 - 4},250 L {bx1 - 4},380", "none", OIL, 7)
        # cylinder head with combustion chamber, ports and inclined valves
        s += path(f"M {bx0 - 40},120 L {bx0 - 40},40 Q {bx0 - 40},20 {bx0 - 20},20 L {bx1 + 20},20 Q {bx1 + 40},20 {bx1 + 40},40 "
                  f"L {bx1 + 40},120 Z", "url(#alu)", DARK, 6)
        s += path(f"M {bx0},122 Q {AX},84 {bx1},122 Z", "url(#chamber)", DARK, 3)
        for side in (-1, 1):                                                                              # ports
            d = f"M {AX + side * 66},{104} Q {AX + side * 110},{70} {AX + side * 176},{66}"
            s += path(d, "none", DARK, 34) + path(d, "none", "#94a3b8", 26)
        s += valve(AX - 66, 106, -22) + valve(AX + 66, 106, 22)
        s += path(f"M {AX - 12},30 L {AX + 12},30 L {AX + 8},82 L {AX - 8},82 Z", "#cbd5e1", DARK, 3)          # spark plug
        # piston with rings and gudgeon pin
        s += path(f"M {bx0 + 6},236 L {bx1 - 6},236 L {bx1 - 6},356 L {bx0 + 6},356 Z", "url(#steel)", DARK, 5)
        for y in (250, 264, 278):
            s += path(f"M {bx0 + 6},{y} L {bx1 - 6},{y}", "none", DARK, 4)
        # connecting rod (H-section, tapering) and big end on the crankpin
        dx, dy = PIN[0] - SMALL[0], PIN[1] - SMALL[1]
        L = math.hypot(dx, dy)
        nx, ny = -dy / L, dx / L
        rod = [(SMALL[0] + nx * 16, SMALL[1] + ny * 16), (PIN[0] + nx * 26, PIN[1] + ny * 26),
               (PIN[0] - nx * 26, PIN[1] - ny * 26), (SMALL[0] - nx * 16, SMALL[1] - ny * 16)]
        # crank web with counterweight (opposite the crankpin), main journal and drilling to the crankpin
        s += circle(*MAIN, 132, "url(#steel)", DARK, 5) + circle(*MAIN, 116, "none", "#94a3b8", 3)          # crank web
        s += path("M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in rod) + " Z", "url(#steel)", DARK, 5)
        s += path(f"M {SMALL[0]:.1f},{SMALL[1]:.1f} L {PIN[0]:.1f},{PIN[1]:.1f}", "none", "#94a3b8", 8)
        s += circle(*SMALL, 20, "#e2e8f0", DARK, 4)
        s += circle(*PIN, 44, "url(#steel)", DARK, 5) + circle(*PIN, 30, "#e2e8f0", OIL, 8)
        s += circle(*MAIN, 40, "#e2e8f0", OIL, 10) + circle(*MAIN, 16, DARK)
        s += path(f"M {MAIN[0]:.1f},{MAIN[1]:.1f} L {PIN[0]:.1f},{PIN[1]:.1f}", "none", OIL, 6, ' stroke-dasharray="10 8"')
        # gear pump in the sump: housing, two gears, pick-up below, gallery up the crankcase wall to the main bearing
        s += path("M 300,818 L 300,840 M 286,840 L 314,840", "none", DARK, 5)
        s += path("M 262,770 Q 262,752 280,752 L 364,752 Q 382,752 382,770 L 382,800 Q 382,818 364,818 L 280,818 "
                  "Q 262,818 262,800 Z", "#cbd5e1", DARK, 5)
        s += gear(298, 785, n=10, r_tip=28, r_root=21) + gear(347, 785, n=10, r_tip=28, r_root=21, phase=18)
        s += pipe(f"M 270,752 L 270,660 Q 270,{MAIN[1]} 300,{MAIN[1]} L {MAIN[0] - 42},{MAIN[1]}", 20)
        s += path("M 270,734 L 270,684", "none", NAVY_BLUE, 6, ' marker-end="url(#hd_navy)"')
        s += path(f"M 316,{MAIN[1]} L 372,{MAIN[1]}", "none", NAVY_BLUE, 6, ' marker-end="url(#hd_navy)"')
        # splash thrown from the big end
        for x, y, a in ((300, 392, -8), (306, 440, -12), (318, 492, -20), (560, 392, 8), (554, 440, 12),
                        (540, 494, 20), (372, 376, -4), (430, 386, 0), (490, 378, 6), (352, 420, -10), (512, 424, 10)):
            s += drop(x, y, 9, a)
        s += path(f"M {PIN[0] - 30},{PIN[1] - 40} Q 380,470 330,420", "none", OIL, 5, ' stroke-dasharray="10 9"')
        s += path(f"M {PIN[0] + 10},{PIN[1] - 48} Q 545,480 548,420", "none", OIL, 5, ' stroke-dasharray="10 9"')
        s += label(668, 545, "Splash", TXT_M, "#a16207", "start")
        s += label(20, 800, "Gear pump", TXT_M, NAVY_BLUE, "start")
        return s
    return dict(h=LB_H, sky="chart_paper", draw=draw, caption="GEAR PUMP PRESSURE PLUS SPLASH", color=NAVY_BLUE)


@R.add(2520, "lubrication-pump-splash-v1", "Gear Pump and Splash Lubrication",
       template("A GEAR-TYPE PUMP SUPPLIES PRESSURE OIL; SPLASH DOES THE REST"), h=stack_height([LB_H]), w=W)
def _():
    return picture([lubrication_panel()])
