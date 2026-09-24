"""Piston-engine explanation diagrams (ATG)."""
import math
import sys
from pathlib import Path
import os
REPO = Path(__file__).resolve().parents[2]
WORK = Path(os.environ.get("ATG_WORK", "/tmp/atg-work"))

import importlib.util

HERE = Path(__file__).parent
_spec = importlib.util.spec_from_file_location("g", HERE / "gen_airframes.py")
g = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(g)
header, footer, t, line, poly, polyline = g.header, g.footer, g.t, g.line, g.poly, g.polyline
INK, BODY, MUTED, GOLD, GOLD_DARK, NAVY, RED, BLUE = g.INK, g.BODY, g.MUTED, g.GOLD, g.GOLD_DARK, g.NAVY, g.RED, g.BLUE
GREEN = "#15803d"
FUEL = "#f59e0b"
OUT = REPO / "public/explanation-images/aircraft-technical-and-general"


def panel(x=40, y=142, w=710, h=444, hl=False):
    fill, stroke, sw = ("#fff8e1", GOLD, 4) if hl else ("#f8fafc", "#cbd5e1", 2)
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>\n'


def fpipe(pts, col=FUEL, w=6):
    return polyline(pts, INK, w + 5) + polyline(pts, col, w)


# =====================================================================
# float-type carburettor: rich, lean, strainer, accelerator pump
# =====================================================================

CARB = {
    "rich": ("MIXTURE CONTROL: RICH",
             [("MORE FUEL", ["The mixture valve opens: more", "fuel reaches the discharge", "nozzle and inlet manifold."]),
              ("FUEL-TO-AIR RATIO UP", ["A rich mixture has a higher", "fuel-to-air ratio."]),
              ("WHEN", ["Full rich for take-off, climb", "and descent, as the POH says."])],
             "Moving the mixture to rich increases the fuel entering the diffuser and inlet manifold."),
    "lean": ("MIXTURE CONTROL: LEAN",
             [("LESS FUEL", ["The mixture valve closes down:", "less fuel reaches the", "discharge nozzle."]),
              ("RATIO CHANGES", ["Fuel-to-air ratio falls; the", "air-to-fuel ratio rises."]),
              ("WHEN", ["Cruise, especially at altitude,", "as the POH says."])],
             "Leaning reduces the fuel entering the diffuser: the fuel-to-air ratio falls."),
    "strainer": ("CARBURETTOR FUEL STRAINER",
                 [("UPSTREAM OF THE NEEDLE VALVE", ["Fuel is strained before it", "reaches the float chamber."]),
                  ("PROTECTS", ["Stops dirt holding the needle", "valve open or blocking jets."]),
                  ("CHECK", ["Drain and inspect for water", "and sediment as required."])],
                 "The fuel strainer is fitted upstream of the carburettor needle valve."),
    "accel": ("ACCELERATOR PUMP",
              [("THROTTLE OPENED QUICKLY", ["Air speeds up faster than the", "heavier fuel: the mixture", "goes weak for a moment."]),
               ("EXTRA SQUIRT OF FUEL", ["The pump discharges fuel", "straight into the venturi."]),
               ("RESULT", ["No hesitation or cut when", "power is applied quickly."])],
              "When the throttle is opened quickly the accelerator pump discharges extra fuel into the venturi."),
}


def carb(answer):
    title, facts, foot = CARB[answer]
    s = header(title)
    s += panel()
    # venturi duct (updraft)
    s += f'<path d="M 440,580 L 440,440 Q 440,400 462,390 Q 440,380 440,340 L 440,170" fill="none" stroke="{INK}" stroke-width="5"/>\n'
    s += f'<path d="M 540,580 L 540,440 Q 540,400 518,390 Q 540,380 540,340 L 540,170" fill="none" stroke="{INK}" stroke-width="5"/>\n'
    for x in (470, 510):
        s += line(x, 575, x, 520, BLUE, 3.5, "aBlue")
    s += t(490, 600 - 6, "AIR IN", 12, 800, BLUE)
    s += line(490, 210, 490, 176, BLUE, 3.5, "aBlue")
    s += t(560, 188, "TO INLET MANIFOLD", 12, 800, MUTED, "start")
    if answer != "accel":
        s += t(560, 396, "VENTURI", 12, 800, MUTED, "start")
    # throttle butterfly
    s += line(452, 262, 528, 238, INK, 6)
    s += f'<circle cx="490" cy="250" r="5" fill="{INK}"/>\n'
    s += t(560, 256, "THROTTLE VALVE", 12, 800, MUTED, "start")
    # float chamber
    s += f'<rect x="150" y="300" width="190" height="190" rx="8" fill="#ffffff" stroke="{INK}" stroke-width="4"/>\n'
    s += f'<rect x="154" y="386" width="182" height="100" fill="{FUEL}" fill-opacity="0.8"/>\n'
    s += f'<rect x="206" y="364" width="80" height="34" rx="12" fill="#e2e8f0" stroke="{INK}" stroke-width="2.5"/>\n'
    s += t(246, 386, "FLOAT", 11, 800, INK)
    s += line(246, 364, 246, 312, "#475569", 4)
    s += f'<path d="M 238,312 L 254,312 L 246,296 Z" fill="#475569"/>\n'
    s += t(214, 476, "FLOAT CHAMBER", 12, 800, INK)
    # fuel inlet with strainer, needle valve
    st = answer == "strainer"
    s += fpipe([(60, 280), (246, 280), (246, 296)])
    s += f'<rect x="92" y="264" width="44" height="32" rx="4" fill="#fef3c7" stroke="{GOLD if st else INK}" stroke-width="{5 if st else 2.5}"/>\n'
    for k in range(5):
        s += line(96 + k * 9, 266, 96 + k * 9, 294, "#92400e", 1.5)
    s += t(114, 254, "STRAINER", 12, 800, GOLD_DARK if st else INK)
    s += t(262, 272, "NEEDLE VALVE", 12, 800, GOLD_DARK if st else MUTED, "start")
    s += t(64, 314, "FUEL IN", 12, 800, MUTED, "start")
    s += line(64, 272, 88, 272, "#92400e", 2.5, "aDark")
    # main jet to discharge nozzle
    s += fpipe([(336, 470), (400, 470), (400, 392), (480, 392)])
    s += f'<circle cx="480" cy="392" r="6" fill="{FUEL}" stroke="{INK}" stroke-width="2"/>\n'
    for k in range(6):
        s += f'<circle cx="{474 + (k % 3) * 6}" cy="{380 - k * 7}" r="2.5" fill="#d97706"/>\n'
    if answer != "accel":
        s += t(560, 434, "DISCHARGE NOZZLE", 12, 800, GOLD_DARK if answer in ("rich", "lean") else MUTED, "start")
        s += t(560, 450, "(DIFFUSER)", 12, 800, GOLD_DARK if answer in ("rich", "lean") else MUTED, "start")
        s += line(556, 438, 488, 398, GOLD_DARK if answer in ("rich", "lean") else MUTED, 2, "aDark")
    # mixture control needle entering the main jet from below
    mix = answer in ("rich", "lean")
    tip_y = 492 if answer == "rich" else 474
    s += f'<path d="M 364,{tip_y + 60} L 376,{tip_y + 60} L 370,{tip_y} Z" fill="{GOLD if mix else "#94a3b8"}" stroke="{INK}" stroke-width="2"/>\n'
    s += line(370, tip_y + 60, 370, 548, "#475569", 3)
    s += t(370, 566, "MIXTURE CONTROL", 12, 800, GOLD_DARK if mix else MUTED)
    if mix:
        note = "NEEDLE WITHDRAWN: MORE FUEL" if answer == "rich" else "NEEDLE IN: LESS FUEL"
        s += t(60, 176, note, 16, 800, GOLD_DARK, "start")
        s += t(370, 582, "RICH" if answer == "rich" else "LEAN", 12, 800, GOLD_DARK)
    # accelerator pump linked to the throttle (only drawn where it is the subject)
    if answer == "accel":
        ac = answer == "accel"
        s += f'<rect x="600" y="460" width="56" height="80" rx="6" fill="#ffffff" stroke="{GOLD if ac else INK}" stroke-width="{5 if ac else 2.5}"/>\n'
        s += f'<rect x="604" y="496" width="48" height="40" fill="{FUEL}" fill-opacity="0.8"/>\n'
        s += line(628, 496, 628, 440, "#475569", 5)
        s += polyline([(628, 440), (628, 300), (528, 242)], "#475569", 2.5, dash="6 5")
        s += fpipe([(604, 520), (570, 520), (570, 360), (540, 360)])
        s += t(628, 564, "ACCELERATOR", 12, 800, GOLD_DARK if ac else MUTED)
        s += t(628, 580, "PUMP", 12, 800, GOLD_DARK if ac else MUTED)
        if ac:
            for k in range(5):
                s += f'<circle cx="{526 - k * 8}" cy="{358 - k * 3}" r="3" fill="#d97706"/>\n'
            s += t(60, 176, "THROTTLE OPENED FAST: PUMP SQUIRTS FUEL", 15, 800, GOLD_DARK, "start")
            s += line(628, 450, 628, 470, RED, 3, "aRedS")
    s += g.fact_column(facts)
    s += footer(foot)
    return s


# =====================================================================
# mixture richens with altitude (q2747)
# =====================================================================

def altitude_rich():
    s = header("WHY THE MIXTURE RICHENS WITH ALTITUDE")
    import random
    random.seed(7)
    for i, (head, n_air, verdict, col) in enumerate((("SEA LEVEL: DENSE AIR", 26, "CORRECT MIXTURE", GREEN),
                                                     ("HIGH ALTITUDE: THIN AIR", 13, "TOO RICH", RED))):
        px = 48 + i * 362
        s += panel(px, 142, 346, 444, hl=i == 1)
        s += t(px + 20, 176, head, 17, 800, INK, "start")
        s += f'<rect x="{px + 50}" y="200" width="246" height="240" rx="12" fill="#ffffff" stroke="{INK}" stroke-width="3"/>\n'
        pts = []
        while len(pts) < n_air:
            x, y = px + 70 + random.random() * 206, 220 + random.random() * 200
            if all((x - a) ** 2 + (y - b) ** 2 > 900 for a, b in pts) and not (px + 150 < x < px + 200 and 290 < y < 350):
                pts.append((x, y))
        for x, y in pts:
            s += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="9" fill="#93c5fd" stroke="#1d4ed8" stroke-width="1.5"/>\n'
        s += f'<path d="M {px + 173},{292} Q {px + 196},{322} {px + 173},{344} Q {px + 150},{322} {px + 173},{292} Z" fill="{FUEL}" stroke="{INK}" stroke-width="2"/>\n'
        s += t(px + 173, 466, f"{n_air} parts air : same fuel", 15, 700, BODY)
        s += t(px + 173, 500, verdict, 20, 800, col)
    s += g.fact_column([
        ("LESS DENSE AIR", ["Each intake stroke draws in", "less mass of air."]),
        ("ABOUT THE SAME FUEL", ["The carburettor still meters", "roughly the same fuel."]),
        ("LEAN WITH ALTITUDE", ["Lean the mixture to restore", "the correct ratio."]),
    ])
    s += footer("As altitude increases air density falls while the fuel stays about the same: the mixture richens.")
    return s


_lspec = importlib.util.spec_from_file_location("lub", HERE / "gen_lubrication.py")
lub = importlib.util.module_from_spec(_lspec)
_lspec.loader.exec_module(lub)


def ans_badge(x, y):
    return f'<rect x="{x}" y="{y}" width="92" height="28" rx="14" fill="{GOLD}"/>\n' + t(x + 46, y + 19, "ANSWER", 14, 800, NAVY)


def cylinder(cx, top, piston_y, spark=False, hot=False, flame=None):
    """Cylinder cross-section. flame: None | (x, y, r) of a flame front centred in the chamber."""
    s = f'<path d="M {cx - 80},{top + 230} L {cx - 80},{top + 40} Q {cx - 80},{top} {cx - 40},{top} L {cx + 40},{top} Q {cx + 80},{top} {cx + 80},{top + 40} L {cx + 80},{top + 230}" fill="#ffffff" stroke="{INK}" stroke-width="6"/>\n'
    for k in range(5):
        s += line(cx - 80, top + 60 + k * 32, cx - 104, top + 60 + k * 32, "#94a3b8", 5, cap="butt")
        s += line(cx + 80, top + 60 + k * 32, cx + 104, top + 60 + k * 32, "#94a3b8", 5, cap="butt")
    s += f'<rect x="{cx - 8}" y="{top - 34}" width="16" height="38" fill="#94a3b8" stroke="{INK}" stroke-width="2"/>\n'
    if spark:
        for a in range(0, 360, 45):
            r = math.radians(a)
            s += line(cx + 8 * math.cos(r), top + 10 + 8 * math.sin(r), cx + 20 * math.cos(r), top + 10 + 20 * math.sin(r), "#facc15", 3)
    if flame:
        fx, fy, fr = flame
        s += f'<circle cx="{fx}" cy="{fy}" r="{fr}" fill="#fb923c" fill-opacity="0.55" stroke="#ea580c" stroke-width="3" stroke-dasharray="6 4"/>\n'
    if hot:
        hx, hy = cx - 50, top + 20
        s += f'<circle cx="{hx}" cy="{hy}" r="18" fill="#ef4444" fill-opacity="0.35"/>\n'
        s += f'<circle cx="{hx}" cy="{hy}" r="9" fill="#dc2626" stroke="#7f1d1d" stroke-width="2"/>\n'
    s += f'<rect x="{cx - 74}" y="{piston_y}" width="148" height="56" rx="6" fill="#94a3b8" stroke="{INK}" stroke-width="3"/>\n'
    for k in (10, 20):
        s += line(cx - 74, piston_y + k, cx + 74, piston_y + k, "#475569", 2.5)
    s += line(cx, piston_y + 40, cx + 24, top + 262, "#475569", 12)
    s += f'<circle cx="{cx}" cy="{top + 262}" r="34" fill="none" stroke="#64748b" stroke-width="4" stroke-dasharray="6 5"/>\n'
    return s


# =====================================================================
# pre-ignition (q2519, q2546, q2562) and run-on (q2749)
# =====================================================================

PRE = {
    "pre": ("PRE-IGNITION",
            ("NORMAL: SPARK IGNITES THE MIXTURE", "PRE-IGNITION: A HOT SPOT FIRES IT EARLY"),
            [("CAUSE: HOT SPOTS", ["Glowing carbon, an overheated", "plug or valve edge ignites", "the charge before the spark."]),
             ("LEAN MIXTURE", ["Runs hotter, so pre-ignition", "can start in just one", "cylinder."]),
             ("CURE", ["Increase cooling (cowl flaps,", "airspeed), enrich the", "mixture, reduce power."])],
            "Pre-ignition: hot spots fire the mixture early. Cool the engine and enrich the mixture."),
    "runon": ("RUN-ON AFTER SHUTDOWN",
              ("IGNITION OFF: NO SPARK", "GLOWING CARBON STILL FIRES THE MIXTURE"),
              [("MAGNETOS GROUNDED", ["Switching off stops the", "sparks, and the magnetos", "are correctly grounded."]),
               ("HOT SPOT IGNITION", ["Glowing carbon in a hot", "combustion chamber keeps", "igniting the mixture."]),
               ("PREVENTION", ["Shut down with the idle", "cut-off after a cool-down", "period."])],
              "Run-on with the magnetos grounded is caused by glowing carbon deposits in a combustion chamber."),
}


def pre_ignition(answer):
    title, (h1, h2), facts, foot = PRE[answer]
    s = header(title)
    for i, head in enumerate((h1, h2)):
        px = 40 + i * 362
        s += panel(px, 142, 348, 444, hl=i == 1)
        s += t(px + 174, 176, head, 13, 800, INK)
        cx = px + 174
        if i == 0:
            if answer == "pre":
                s += cylinder(cx, 240, 300, spark=True, flame=(cx, 262, 30))
                s += t(cx, 564, "Spark at the correct time", 15, 800, GREEN)
            else:
                s += cylinder(cx, 240, 300)
                s += t(cx, 564, "Ignition switched OFF", 15, 800, INK)
        else:
            s += cylinder(cx, 240, 340, hot=True, flame=(cx - 44, 262, 40))
            s += t(cx + 26, 214, "HOT SPOT", 13, 800, RED, "start")
            s += line(cx + 24, 216, cx - 40, 254, RED, 2, "aRedS")
            s += t(cx, 564, "Uncontrolled ignition" if answer == "pre" else "Engine keeps running", 15, 800, RED)
    s += g.fact_column(facts)
    s += footer(foot)
    return s


# =====================================================================
# exhaust smoke (q2526 blue, q2547 black)
# =====================================================================

def smoke(answer):
    title = "BLUE EXHAUST SMOKE" if answer == "blue" else "BLACK EXHAUST SMOKE"
    s = header(title)
    cols = [("blue", "BLUE SMOKE", "#60a5fa", "Engine is burning oil", "Worn rings or valve guides"),
            ("black", "BLACK SMOKE", "#1f2937", "Mixture too rich", "Unburnt fuel (soot)"),
            ("none", "NO VISIBLE SMOKE", None, "Normal running", "Correct mixture")]
    for i, (key, head, col, l1, l2) in enumerate(cols):
        px = 48 + i * 372
        ans = key == answer
        s += panel(px, 142, 356, 444, hl=ans)
        s += t(px + 20, 178, head, 20, 800, INK, "start")
        if ans:
            s += ans_badge(px + 248, 158)
        # cowling and exhaust stub
        s += f'<path d="M {px + 30},{250} L {px + 170},{250} Q {px + 210},{250} {px + 210},{300} L {px + 210},{340} L {px + 30},{340} Z" fill="#dfe5ec" stroke="{INK}" stroke-width="3"/>\n'
        s += f'<rect x="{px + 150}" y="{340}" width="24" height="44" fill="#64748b" stroke="{INK}" stroke-width="2.5"/>\n'
        if col:
            for k, (dx, dy, r) in enumerate(((10, 30, 22), (40, 62, 30), (82, 96, 38), (130, 126, 44))):
                s += f'<circle cx="{px + 162 + dx}" cy="{384 + dy}" r="{r}" fill="{col}" fill-opacity="{0.8 - k * 0.14:.2f}"/>\n'
        s += t(px + 178, 540, l1, 18, 800, GOLD_DARK if ans else INK)
        s += t(px + 178, 566, l2, 15, 400, BODY)
    foot = ("Blue smoke from the exhaust of a running engine indicates it is burning oil."
            if answer == "blue" else "Black smoke from the exhaust after start indicates the mixture is too rich.")
    s += footer(foot)
    return s


# =====================================================================
# ignition timing (q2556 20-25 deg BTDC, q2554 fixed with RPM)
# =====================================================================

def timing(answer):
    title = "IGNITION TIMING" if answer == "btdc" else "IGNITION TIMING IS FIXED"
    s = header(title)
    s += panel(40, 142, 710, 444, hl=True)
    cx, cy, R = 250, 370, 150
    s += f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="#ffffff" stroke="#cbd5e1" stroke-width="3"/>\n'
    s += line(cx, cy - R - 16, cx, cy + R + 16, "#94a3b8", 2, dash="6 5")
    s += t(cx, cy - R - 24, "TDC", 15, 800, INK)
    s += t(cx, cy + R + 36, "BDC", 15, 800, INK)
    # compression stroke: BDC -> TDC up the left side (crank turning clockwise)

    def pt(deg_btdc, r):
        a = math.radians(90 + deg_btdc)
        return cx + r * math.cos(a), cy - r * math.sin(a)

    c0, c1 = pt(178, R - 6), pt(27, R - 6)
    s += f'<path d="M {c0[0]:.1f} {c0[1]:.1f} A {R - 6} {R - 6} 0 0 1 {c1[0]:.1f} {c1[1]:.1f}" fill="none" stroke="#94a3b8" stroke-width="7"/>\n'

    a20, a25 = pt(20, R), pt(25, R)
    s += f'<path d="M {cx},{cy} L {a25[0]:.1f},{a25[1]:.1f} A {R} {R} 0 0 1 {a20[0]:.1f},{a20[1]:.1f} Z" fill="{GOLD}" fill-opacity="0.85" stroke="{GOLD_DARK}" stroke-width="2"/>\n'
    p = pt(22.5, R + 30)
    s += t(p[0] - 10, p[1], "SPARK", 16, 800, GOLD_DARK, "end")
    s += t(p[0] - 10, p[1] + 20, "20–25° BTDC", 16, 800, GOLD_DARK, "end")
    arr0, arr1 = pt(-30, R + 14), pt(-60, R + 14)
    s += f'<path d="M {arr0[0]:.1f} {arr0[1]:.1f} A {R + 14} {R + 14} 0 0 1 {arr1[0]:.1f} {arr1[1]:.1f}" fill="none" stroke="{INK}" stroke-width="4" marker-end="url(#aDark)"/>\n'
    s += t(cx + 40, cy - R - 30, "ROTATION", 13, 800, INK, "start")
    q = pt(95, R * 0.6)
    s += t(q[0], q[1], "COMPRESSION", 13, 800, MUTED)
    s += t(q[0], q[1] + 16, "STROKE", 13, 800, MUTED)
    # right side: why early / fixed timing table
    if answer == "btdc":
        s += t(440, 250, "WHY BEFORE TDC?", 17, 800, INK, "start")
        for i, ln in enumerate(["The mixture takes time to", "burn. Firing early lets peak", "pressure arrive just after", "TDC, pushing the piston", "down on the power stroke."]):
            s += t(440, 282 + i * 24, ln, 15, 400, BODY, "start")
    else:
        s += t(440, 236, "RPM", 15, 800, INK, "start")
        s += t(560, 236, "SPARK", 15, 800, INK, "start")
        for i, rpm in enumerate(("1000", "1800", "2500")):
            y = 276 + i * 44
            s += f'<rect x="430" y="{y - 26}" width="290" height="36" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="2"/>\n'
            s += t(440, y, rpm, 16, 800, INK, "start")
            s += t(560, y, "25° BTDC", 16, 800, GOLD_DARK, "start")
        s += t(440, 432, "Magneto timing does not", 15, 400, BODY, "start")
        s += t(440, 454, "change as RPM changes.", 15, 400, BODY, "start")
    s += g.fact_column([
        ("SPARK BEFORE TDC", ["Ignition occurs about 20–25°", "before TDC on the", "compression stroke."]),
        ("FIXED TIMING", ["Aircraft magnetos fire at a", "set crank angle whatever", "the RPM."]),
        ("EXCEPTION: STARTING", ["An impulse coupling retards", "the spark to TDC for", "starting."]),
    ])
    foot = ("Ignition is timed to occur about 20 to 25 degrees before TDC on the compression stroke."
            if answer == "btdc" else "If engine RPM is increased, the ignition timing remains the same.")
    s += footer(foot)
    return s


# =====================================================================
# fuel grade (q2524 MOGAS, q2550 higher octane)
# =====================================================================

def fuel_grade(answer):
    title = "UNAPPROVED MOGAS" if answer == "mogas" else "HIGHER-OCTANE FUEL THAN RECOMMENDED"
    s = header(title)
    cols = [("mogas", "LOWER GRADE / UNAPPROVED MOGAS", ["Detonation", "Reduced power", "Lead fouling of the plugs", "Vapour lock risk"]),
            ("higher", "HIGHER OCTANE THAN RECOMMENDED", ["Higher lead content", "Lead fouling of the plugs", "Deposits on valves"])]
    for i, (key, head, items) in enumerate(cols):
        px = 48 + i * 362
        ans = key == answer
        s += panel(px, 142, 346, 444, hl=ans)
        s += t(px + 20, 176, head, 14, 800, INK, "start")
        if ans:
            s += ans_badge(px + 238, 190)
        for j, it in enumerate(items):
            y = 260 + j * 58
            s += f'<circle cx="{px + 40}" cy="{y - 6}" r="9" fill="{RED}"/>\n'
            s += t(px + 60, y, it, 18, 800, INK, "start")
    s += f'<rect x="770" y="146" width="378" height="438" rx="12" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2"/>\n'
    s += t(790, 180, "AVGAS COLOUR CODES", 18, 800, INK, "start")
    for j, (grade, col, note) in enumerate((("AVGAS 80", "#dc2626", "red"), ("AVGAS 100LL", "#2563eb", "blue"), ("AVGAS 100", "#16a34a", "green"))):
        y = 220 + j * 96
        s += f'<rect x="790" y="{y}" width="60" height="76" rx="8" fill="{col}" stroke="{INK}" stroke-width="2"/>\n'
        s += t(866, y + 34, grade, 18, 800, INK, "start")
        s += t(866, y + 58, note, 15, 400, BODY, "start")
    s += t(790, 520, "Always use the grade in", 16, 800, GOLD_DARK, "start")
    s += t(790, 544, "the flight manual.", 16, 800, GOLD_DARK, "start")
    foot = ("Unapproved MOGAS may cause detonation, reduced power and lead fouling of the spark plugs."
            if answer == "mogas" else "Using fuel of a higher octane than recommended may cause lead fouling of the spark plugs.")
    s += footer(foot)
    return s


# =====================================================================
# CHT from the hottest cylinder (q2561)
# =====================================================================

def cht():
    s = header("CYLINDER HEAD TEMPERATURE GAUGE")
    s += panel(40, 142, 710, 444)
    s += t(60, 172, "FLAT-FOUR ENGINE FROM ABOVE", 15, 800, INK, "start")
    s += f'<rect x="250" y="220" width="160" height="300" rx="16" fill="#cbd5e1" stroke="{INK}" stroke-width="3"/>\n'
    s += t(330, 374, "CRANKCASE", 13, 800, INK)
    cyls = [(1, 160, 300), (3, 160, 440), (2, 420, 300), (4, 420, 440)]
    for n, x, y in cyls:
        hot = n == 3
        s += f'<rect x="{x}" y="{y - 50}" width="80" height="100" rx="10" fill="{"#fecaca" if hot else "#e2e8f0"}" stroke="{GOLD if hot else INK}" stroke-width="{5 if hot else 2.5}"/>\n'
        for k in range(5):
            s += line(x + 8, y - 40 + k * 20, x + 72, y - 40 + k * 20, "#94a3b8", 2)
        s += t(x + 40, y + 6, f"#{n}", 18, 800, INK)
    s += line(330, 192, 330, 220, BLUE, 4, "aBlue")
    s += t(342, 206, "COOLING AIR (FRONT)", 12, 800, BLUE, "start")
    s += f'<circle cx="170" cy="400" r="8" fill="{RED}" stroke="#ffffff" stroke-width="2"/>\n'
    s += polyline([(170, 400), (150, 400), (150, 560), (560, 560)], RED, 3, dash="6 4")
    gx, gy = 640, 480
    s += f'<circle cx="{gx}" cy="{gy}" r="54" fill="#1f2937" stroke="{INK}" stroke-width="3"/>\n'
    s += line(gx, gy, gx + 32, gy - 30, "#f8fafc", 4)
    s += t(gx, gy + 32, "CHT", 14, 800, "#f8fafc")
    s += line(560, 560, 600, 520, RED, 3, "aRedS")
    s += t(60, 470, "HOTTEST", 14, 800, GOLD_DARK, "start")
    s += t(60, 488, "CYLINDER", 14, 800, GOLD_DARK, "start")
    s += t(60, 506, "(IN TESTS)", 13, 700, GOLD_DARK, "start")
    s += g.fact_column([
        ("ONE PROBE", ["The sensor is fitted to the", "cylinder that tests show", "runs hottest."]),
        ("WORST CASE", ["The gauge shows the highest", "cylinder head temperature."]),
        ("CONTROL CHT WITH", ["Cowl flaps, mixture, power", "and airspeed."]),
    ])
    s += footer("The CHT gauge usually takes its reading from the cylinder that tests show runs hottest.")
    return s


# =====================================================================
# primer (q2482, q2501)
# =====================================================================

def primer():
    s = header("ENGINE PRIMER")
    s += panel(40, 142, 710, 444)
    # carburettor and induction manifold to four inlet ports
    s += f'<rect x="330" y="460" width="100" height="80" rx="8" fill="#e2e8f0" stroke="{INK}" stroke-width="3"/>\n'
    s += t(380, 506, "CARB", 14, 800, INK)
    s += polyline([(380, 460), (380, 390)], "#94a3b8", 18)
    s += polyline([(140, 390), (620, 390)], "#94a3b8", 18)
    for x in (140, 300, 460, 620):
        s += polyline([(x, 390), (x, 280)], "#94a3b8", 18)
        s += f'<rect x="{x - 44}" y="{190}" width="88" height="90" rx="10" fill="#cbd5e1" stroke="{INK}" stroke-width="2.5"/>\n'
        s += f'<path d="M {x - 12},{280} L {x + 12},{280} L {x + 4},{268} L {x - 4},{268} Z" fill="{INK}"/>\n'
        s += t(x, 236, "CYL", 13, 800, INK)
    s += t(648, 416, "INDUCTION", 12, 800, MUTED, "start")
    s += t(648, 432, "MANIFOLD", 12, 800, MUTED, "start")
    # primer pump and lines
    s += f'<rect x="70" y="470" width="80" height="60" rx="8" fill="{GOLD}" stroke="{INK}" stroke-width="3"/>\n'
    s += line(110, 470, 110, 440, INK, 6)
    s += f'<rect x="92" y="428" width="36" height="14" rx="4" fill="{INK}"/>\n'
    s += t(110, 506, "PRIMER", 13, 800, INK)
    s += t(110, 552, "PUMP (COCKPIT)", 12, 800, INK)
    s += polyline([(150, 500), (250, 500), (250, 330)], FUEL, 4)
    s += polyline([(250, 330), (140, 330), (140, 296)], FUEL, 4)
    s += polyline([(250, 330), (620, 330), (620, 296)], FUEL, 4)
    for x in (300, 460):
        s += polyline([(x, 330), (x, 296)], FUEL, 4)
    for x in (140, 300, 460, 620):
        s += f'<circle cx="{x}" cy="{300}" r="7" fill="{FUEL}" stroke="{INK}" stroke-width="2"/>\n'
    s += t(460, 478, "FUEL SPRAYED INTO THE INTAKE", 13, 800, GOLD_DARK, "start")
    s += t(460, 496, "PORTS NEAR THE INLET VALVES", 13, 800, GOLD_DARK, "start")
    s += g.fact_column([
        ("STRAIGHT TO THE CYLINDERS", ["Fuel goes into the induction", "system close to the inlet", "valves, bypassing the carb."]),
        ("WHY PRIME", ["In a cold engine fuel", "vaporises poorly and the", "carb meters little when cranking."]),
        ("DON'T OVER-PRIME", ["Too much fuel floods the", "cylinders and is a fire risk."]),
    ])
    s += footer("The primer delivers fuel directly into the induction system close to the inlet valves.")
    return s


# =====================================================================
# alternate air, fuel injection (q2503)
# =====================================================================

def alternate_air():
    s = header("ALTERNATE AIR (FUEL INJECTION)")
    s += panel(40, 142, 710, 444)
    s += f'<rect x="60" y="190" width="670" height="360" rx="30" fill="none" stroke="#94a3b8" stroke-width="4" stroke-dasharray="12 8"/>\n'
    s += t(80, 214, "ENGINE COWLING", 13, 800, MUTED, "start")
    # intake scoop and filter
    s += line(40, 300, 110, 300, BLUE, 5, "aBlue")
    s += t(62, 282, "RAM AIR", 12, 800, BLUE)
    s += f'<rect x="110" y="270" width="70" height="60" rx="6" fill="#e5e7eb" stroke="{INK}" stroke-width="3"/>\n'
    for k in range(6):
        s += line(118 + k * 10, 274, 118 + k * 10, 326, "#64748b", 2)
    s += t(145, 356, "AIR FILTER", 13, 800, INK)
    s += f'<path d="M 128,288 L 162,312 M 162,288 L 128,312" stroke="{RED}" stroke-width="4"/>\n'
    s += t(145, 250, "BLOCKED / ICED", 12, 800, RED)
    s += polyline([(180, 300), (420, 300)], "#94a3b8", 24)
    # alternate air door
    s += f'<rect x="300" y="312" width="60" height="16" rx="3" fill="{GOLD}" stroke="{INK}" stroke-width="2.5" transform="rotate(35 300 320)"/>\n'
    for x in (270, 300, 330):
        s += line(x, 420, x + 20, 332, "#f97316", 4, "aDark")
    s += t(300, 450, "WARM AIR FROM INSIDE", 13, 800, GOLD_DARK)
    s += t(300, 468, "THE COWLING", 13, 800, GOLD_DARK)
    s += t(366, 372, "ALTERNATE AIR DOOR", 13, 800, GOLD_DARK, "start")
    # servo / engine
    s += f'<rect x="420" y="270" width="90" height="60" rx="6" fill="#e2e8f0" stroke="{INK}" stroke-width="3"/>\n'
    s += t(465, 306, "SERVO", 13, 800, INK)
    s += polyline([(510, 300), (560, 300)], "#94a3b8", 24)
    s += f'<rect x="560" y="240" width="140" height="130" rx="12" fill="#cbd5e1" stroke="{INK}" stroke-width="3"/>\n'
    s += t(630, 310, "ENGINE", 15, 800, INK)
    s += g.fact_column([
        ("PURPOSE", ["Keeps air reaching the engine", "if the intake or filter is", "blocked, e.g. by ice."]),
        ("WHERE THE AIR COMES FROM", ["From within the engine", "cowling: warmer and", "unfiltered."]),
        ("OPERATION", ["Manual control, or a door", "that opens automatically", "on suction."]),
    ])
    s += footer("Alternate air feeds air from within the engine cowling to the induction system.")
    return s


# =====================================================================
# carburettor icing symptoms (q2500)
# =====================================================================

def carb_icing():
    s = header("CARBURETTOR ICING")
    s += panel(40, 142, 350, 444)
    s += t(60, 176, "ICE IN THE VENTURI", 16, 800, INK, "start")
    x0 = 215
    s += f'<path d="M {x0 - 60},560 L {x0 - 60},420 Q {x0 - 60},380 {x0 - 36},370 Q {x0 - 60},360 {x0 - 60},320 L {x0 - 60},210" fill="none" stroke="{INK}" stroke-width="5"/>\n'
    s += f'<path d="M {x0 + 60},560 L {x0 + 60},420 Q {x0 + 60},380 {x0 + 36},370 Q {x0 + 60},360 {x0 + 60},320 L {x0 + 60},210" fill="none" stroke="{INK}" stroke-width="5"/>\n'
    for (dx, dy) in ((-38, 352), (26, 356), (-30, 386), (22, 380)):
        s += f'<path d="M {x0 + dx},{dy} l 14,-8 l 12,10 l -6,14 l -16,2 Z" fill="#bfdbfe" stroke="#1d4ed8" stroke-width="2"/>\n'
    s += line(x0 - 48, 262, x0 + 48, 242, INK, 6)
    for (dx, dy) in ((-40, 250), (30, 236)):
        s += f'<path d="M {x0 + dx},{dy} l 12,-8 l 10,8 l -4,12 l -14,2 Z" fill="#bfdbfe" stroke="#1d4ed8" stroke-width="2"/>\n'
    s += line(x0, 550, x0, 480, BLUE, 4, "aBlue")
    s += t(x0 + 70, 380, "VENTURI", 12, 800, MUTED, "start")
    s += t(x0 + 70, 256, "THROTTLE", 12, 800, MUTED, "start")
    # RPM trace
    s += panel(400, 142, 350, 444, hl=True)
    s += t(420, 176, "SYMPTOMS (FIXED-PITCH PROP)", 15, 800, INK, "start")
    ox, oy, w, h = 450, 470, 270, 220
    s += line(ox, oy, ox + w, oy, INK, 2.5, "aDark")
    s += line(ox, oy, ox, oy - h, INK, 2.5, "aDark")
    s += t(ox + w / 2, oy + 28, "TIME", 13, 800, INK)
    s += f'<text x="{ox - 18}" y="{oy - h / 2}" text-anchor="middle" font-family="{g.F}" font-size="13" font-weight="800" fill="{INK}" transform="rotate(-90 {ox - 18} {oy - h / 2})">RPM</text>\n'
    pts = []
    for k in range(0, 61):
        x = ox + k / 60 * (w - 10)
        base = 190 - (0 if k < 15 else (k - 15) * 2.6)
        rough = 0 if k < 25 else 7 * math.sin(k * 2.3)
        pts.append((x, oy - base + rough))
    s += polyline(pts, RED, 4)
    s += t(ox + w - 10, oy - 36, "RPM FALLS", 14, 800, RED, "end")
    s += t(ox + w - 10, oy - 18, "SLOWLY", 14, 800, RED, "end")
    s += t(ox + 110, oy - 196, "ROUGH RUNNING", 14, 800, RED, "start")
    s += t(575, 530, "Then: gradual loss of power.", 15, 400, BODY)
    s += t(575, 552, "With a CSU: manifold pressure falls.", 15, 400, BODY)
    s += g.fact_column([
        ("CAUSE", ["Fuel evaporation and the", "venturi pressure drop cool", "the air: moisture freezes."]),
        ("WHEN", ["Possible from about -10 to", "+30 °C in humid air, worst", "at low power."]),
        ("ACTION", ["Full carburettor heat; expect", "brief extra roughness as", "the ice melts."]),
    ])
    s += footer("An engine that starts to run rough and then slowly loses power probably has carburettor icing.")
    return s


# =====================================================================
# flooded start (q2491) and throttle handling (q2499)
# =====================================================================

def lever(cx, top, col, knob, label, pos, hl=False):
    s = f'<rect x="{cx - 8}" y="{top}" width="16" height="220" rx="8" fill="#cbd5e1" stroke="{INK}" stroke-width="2"/>\n'
    y = top + 20 + (1 - pos) * 180
    s += f'<rect x="{cx - 36}" y="{y - 18}" width="72" height="36" rx="10" fill="{col}" stroke="{GOLD if hl else INK}" stroke-width="{5 if hl else 2.5}"/>\n'
    s += t(cx, y + 6, knob, 12, 800, "#ffffff")
    s += t(cx, top + 250, label, 13, 800, GOLD_DARK if hl else INK)
    return s


def flooded():
    s = header("STARTING A FLOODED ENGINE")
    s += panel(40, 142, 380, 444)
    s += t(60, 174, "LEVER POSITIONS WHILE CRANKING", 14, 800, INK, "start")
    s += lever(120, 210, "#111827", "THR", "THROTTLE: OPEN", 0.9)
    s += lever(300, 210, "#dc2626", "MIX", "MIXTURE: LEAN", 0.02, hl=True)
    s += t(300, 480, "(idle cut-off)", 13, 700, MUTED)
    s += panel(430, 142, 320, 444, hl=True)
    s += t(450, 176, "SEQUENCE", 17, 800, INK, "start")
    steps = ["Mixture full lean", "Throttle open (per POH)", "Crank: clears excess fuel", "Engine fires: richen the", "mixture slowly, close", "the throttle"]
    y = 222
    for i, (n, st) in enumerate(((1, steps[0]), (2, steps[1]), (3, steps[2]), (4, steps[3]))):
        s += g.badge(466, y - 6, n)
        s += t(492, y, st, 15, 800, INK, "start")
        y += 58
    s += t(492, y - 34, steps[4], 15, 800, INK, "start")
    s += t(492, y - 12, steps[5], 15, 800, INK, "start")
    s += g.fact_column([
        ("WHY LEAN", ["The cylinders already hold", "too much fuel; no more is", "added while cranking."]),
        ("AIR CLEARS IT", ["Cranking draws air through", "until the mixture can fire."]),
        ("THEN RICHEN", ["Slowly, to keep the", "engine running."]),
    ])
    s += footer("For a flooded engine keep the mixture full lean until it fires, then richen slowly.")
    return s


def throttle_smooth():
    s = header("SMOOTH THROTTLE HANDLING")
    for i, (head, ok) in enumerate((("SMOOTH MOVEMENT", True), ("RAPID MOVEMENT", False))):
        px = 48 + i * 362
        s += panel(px, 142, 346, 444, hl=ok)
        s += t(px + 20, 176, head, 18, 800, INK, "start")
        if ok:
            s += ans_badge(px + 238, 158)
        ox, oy, w, h = px + 50, 440, 260, 200
        s += line(ox, oy, ox + w, oy, INK, 2.5, "aDark")
        s += line(ox, oy, ox, oy - h, INK, 2.5, "aDark")
        s += t(ox + w / 2, oy + 26, "TIME", 12, 800, INK)
        s += f'<text x="{ox - 16}" y="{oy - h / 2}" text-anchor="middle" font-family="{g.F}" font-size="12" font-weight="800" fill="{INK}" transform="rotate(-90 {ox - 16} {oy - h / 2})">LOAD ON CRANKSHAFT</text>\n'
        if ok:
            pts = [(ox + k / 40 * w, oy - 30 - 120 / (1 + math.exp(-(k - 18) / 3))) for k in range(41)]
            col = GREEN
        else:
            pts = [(ox + k / 40 * w, oy - 30 - (0 if k < 12 else 120 + 60 * math.exp(-(k - 12) / 2.5) * math.cos((k - 12) * 1.4))) for k in range(41)]
            col = RED
        s += polyline(pts, col, 4)
        s += t(px + 173, 490, "Gradual power change" if ok else "Shock loads and", 16, 800, col)
        s += t(px + 173, 514, "no shock loads" if ok else "possible hesitation", 16, 800, col)
    s += g.fact_column([
        ("SMOOTHLY, OVER A FEW SECONDS", ["Open and close the throttle", "progressively."]),
        ("PROTECTS THE ENGINE", ["Avoids overstressing the", "crankshaft and propeller."]),
        ("AVOIDS HESITATION", ["Sudden opening can weaken", "the mixture momentarily."]),
    ])
    s += footer("The throttle should be opened and closed smoothly to avoid overstressing the crankshaft.")
    return s


# =====================================================================
# engine theory: counterweights, density, over-leaning, Otto cycle, wastegate, power
# =====================================================================

def counterweights():
    s = header("CRANKSHAFT COUNTERWEIGHTS")
    s += panel(40, 142, 710, 444, hl=True)
    y = 360
    s += line(70, y, 720, y, "#64748b", 22)
    for k, x in enumerate((180, 340, 500, 640)):
        up = k % 2 == 0
        pin_y = y - 90 if up else y + 90
        s += f'<rect x="{x - 40}" y="{min(y, pin_y) - 14}" width="22" height="{abs(pin_y - y) + 28}" rx="6" fill="#94a3b8" stroke="{INK}" stroke-width="2.5"/>\n'
        s += f'<rect x="{x + 18}" y="{min(y, pin_y) - 14}" width="22" height="{abs(pin_y - y) + 28}" rx="6" fill="#94a3b8" stroke="{INK}" stroke-width="2.5"/>\n'
        s += line(x - 18, pin_y, x + 18, pin_y, "#475569", 22)
        cw_y = y + 70 if up else y - 70
        s += f'<path d="M {x - 44},{cw_y - 30} L {x + 44},{cw_y - 30} L {x + 34},{cw_y + 30} L {x - 34},{cw_y + 30} Z" fill="{GOLD}" stroke="{INK}" stroke-width="2.5"/>\n'
    s += t(180, y - 124, "CRANK THROW", 13, 800, INK)
    s += t(180, y + 132, "COUNTERWEIGHT", 13, 800, GOLD_DARK)
    s += t(395, 560, "Each counterweight sits opposite a crank throw to balance it.", 15, 400, BODY)
    s += g.fact_column([
        ("BALANCE", ["Weights opposite the crank", "throws balance the rotating", "masses."]),
        ("LESS VIBRATION", ["Reduces the vibration that", "could damage the engine", "and airframe."]),
        ("SMOOTHER RUNNING", ["Lower bearing loads and", "smoother power delivery."]),
    ])
    s += footer("Counterweights are fitted to the crankshaft to prevent damage from vibration.")
    return s


def density_power():
    s = header("CONDITIONS FOR MAXIMUM ENGINE POWER")
    cols = [("COLD", "Colder air is denser"), ("DRY", "Water vapour displaces air"), ("HIGH PRESSURE", "More air in each cylinder")]
    for i, (head, sub) in enumerate(cols):
        px = 48 + i * 240
        s += panel(px, 142, 226, 300, hl=True)
        s += t(px + 113, 180, head, 20, 800, INK)
        n = 22
        import random
        random.seed(i)
        for k in range(n):
            x, y2 = px + 30 + random.random() * 166, 210 + random.random() * 150
            s += f'<circle cx="{x:.1f}" cy="{y2:.1f}" r="8" fill="#93c5fd" stroke="#1d4ed8" stroke-width="1.5"/>\n'
        s += t(px + 113, 400, sub, 14, 800, GOLD_DARK)
    s += panel(48, 456, 706, 130)
    s += t(70, 494, "DENSE AIR = MORE AIR MASS PER INTAKE STROKE = MORE POWER", 16, 800, INK, "start")
    s += t(70, 526, "Hot, humid, low-pressure air (high density altitude) reduces power.", 15, 400, BODY, "start")
    s += t(70, 552, "Humid air is less dense than dry air at the same temperature and pressure.", 15, 400, BODY, "start")
    s += f'<rect x="770" y="146" width="378" height="438" rx="12" fill="#fff8e1" stroke="{GOLD}" stroke-width="4"/>\n'
    s += t(959, 220, "BEST POWER:", 20, 800, INK)
    s += t(959, 266, "COLD", 30, 800, GOLD_DARK)
    s += t(959, 310, "DRY", 30, 800, GOLD_DARK)
    s += t(959, 354, "HIGH PRESSURE", 30, 800, GOLD_DARK)
    s += t(959, 420, "Worst: hot, humid,", 17, 400, BODY)
    s += t(959, 444, "low pressure", 17, 400, BODY)
    s += footer("A normally aspirated engine produces most power in cold, dry air at high pressure.")
    return s


def over_lean():
    s = header("LEANING TOO FAR")
    s += panel(40, 142, 710, 444)
    ox, oy, w, h = 110, 500, 580, 300
    s += line(ox, oy, ox + w, oy, INK, 2.5, "aDark")
    s += line(ox, oy, ox, oy - h, INK, 2.5, "aDark")
    s += t(ox, oy + 28, "FULL RICH", 13, 800, INK, "start")
    s += t(ox + w, oy + 28, "LEAN", 13, 800, INK, "end")
    s += t(ox + w / 2, oy + 28, "MIXTURE →", 13, 800, INK)
    pk = 0.62
    egt = [(ox + x / 50 * w, oy - 40 - 220 * math.exp(-((x / 50 - pk) / 0.22) ** 2)) for x in range(51)]
    pw = [(ox + x / 50 * w, oy - 60 - 190 * math.exp(-((x / 50 - 0.45) / 0.33) ** 2)) for x in range(51)]
    s += polyline(egt, RED, 4)
    s += polyline(pw, BLUE, 4)
    s += t(ox + pk * w, oy - 270, "PEAK EGT", 13, 800, RED)
    s += t(ox + 0.45 * w - 60, oy - 262, "BEST POWER", 13, 800, BLUE, "end")
    s += line(ox + 0.45 * w - 56, oy - 258, ox + 0.45 * w - 4, oy - 252, BLUE, 2, "aDark")
    x0 = ox + 0.8 * w
    s += f'<rect x="{x0:.1f}" y="{oy - h}" width="{ox + w - x0:.1f}" height="{h}" fill="{RED}" fill-opacity="0.12"/>\n'
    s += t(x0 + 6, oy - h + 22, "TOO LEAN", 14, 800, RED, "start")
    s += t(ox + 40, oy - h + 22, "EGT", 13, 800, RED, "start")
    s += t(ox + 40, oy - h + 42, "POWER", 13, 800, BLUE, "start")
    s += g.fact_column([
        ("ROUGH RUNNING", ["The mixture becomes too weak", "to burn evenly in every", "cylinder."]),
        ("POWER FALLS", ["Less fuel is burnt, so", "power drops away."]),
        ("TEMPERATURES FALL", ["Beyond peak EGT, EGT and", "CHT generally decrease."]),
    ])
    s += footer("Leaning well past best economy makes the engine run rough and lose power; temperatures fall.")
    return s


def otto():
    s = header("IDEAL OTTO CYCLE")
    s += panel(40, 142, 710, 444, hl=True)
    ox, oy = 170, 520
    s += line(ox, oy, 700, oy, INK, 2.5, "aDark")
    s += line(ox, oy, ox, 170, INK, 2.5, "aDark")
    s += t(730, oy + 26, "VOLUME", 13, 800, INK, "end")
    s += f'<text x="{ox - 22}" y="345" text-anchor="middle" font-family="{g.F}" font-size="13" font-weight="800" fill="{INK}" transform="rotate(-90 {ox - 22} 345)">PRESSURE</text>\n'
    r, gam = 6.0, 1.4
    P1 = 1.0
    P2 = P1 * r ** gam
    P3 = 2.4 * P2
    P4 = P3 / r ** gam
    X = lambda V: 220 + (V - 1) * 84
    Y = lambda P: oy - P * (330 / 32)
    comp = [(X(V), Y(P1 * (r / V) ** gam)) for V in [r - k * (r - 1) / 40 for k in range(41)]]
    expn = [(X(V), Y(P3 * (1 / V) ** gam)) for V in [1 + k * (r - 1) / 40 for k in range(41)]]
    s += poly(comp + expn, GOLD, "none", 0, ' fill-opacity="0.35"')
    s += polyline(comp, BLUE, 4)
    s += polyline(expn, RED, 4)
    s += line(X(1), Y(P2), X(1), Y(P3), "#7c3aed", 5)
    s += line(X(r), Y(P4), X(r), Y(P1), "#7c3aed", 5)
    for txt, (x, y), anc in (("1", (X(r) + 10, Y(P1) + 4), "start"), ("2", (X(1) - 10, Y(P2) + 6), "end"),
                             ("3", (X(1) - 10, Y(P3) + 6), "end"), ("4", (X(r) + 10, Y(P4) - 6), "start")):
        s += t(x, y, txt, 16, 800, INK, anc)
    s += t(X(1), oy + 24, "TDC", 12, 800, MUTED)
    s += t(X(r), oy + 24, "BDC", 12, 800, MUTED)
    s += t(X(1) + 14, Y(P3) - 4, "2→3 CONSTANT VOLUME (HEAT ADDED)", 13, 800, "#7c3aed", "start")
    lab = [("3→4 ADIABATIC EXPANSION", RED, 280, (X(1.6), Y(P3 * (1 / 1.6) ** gam))),
           ("USEFUL WORK (ENCLOSED AREA)", GOLD_DARK, 330, (X(1.8), (Y(P3 / 1.8 ** gam) + Y(P1 * (r / 1.8) ** gam)) / 2)),
           ("1→2 ADIABATIC COMPRESSION", BLUE, 380, (X(2.2), Y(P1 * (r / 2.2) ** gam)))]
    for txt, col, y, tgt in lab:
        s += t(440, y, txt, 13, 800, col, "start")
        s += line(436, y - 5, tgt[0] + 4, tgt[1], col, 2, "aDark")
    s += t(X(r) - 8, 432, "4→1 CONSTANT VOLUME", 13, 800, "#7c3aed", "end")
    s += t(X(r) - 8, 448, "(HEAT REJECTED)", 12, 800, "#7c3aed", "end")
    s += line(X(r) - 4, 454, X(r) - 2, (Y(P4) + Y(P1)) / 2, "#7c3aed", 2, "aDark")
    s += g.fact_column([
        ("TWO ADIABATIC", ["Compression (1→2) and", "expansion (3→4): no heat", "exchanged."]),
        ("TWO CONSTANT-VOLUME", ["Heat added at TDC (2→3) and", "rejected at BDC (4→1)."]),
        ("ENCLOSED AREA", ["The area inside the loop is", "the useful work per cycle."]),
    ])
    s += footer("The Otto-cycle work area is enclosed by two adiabatic and two constant-volume processes.")
    return s


def wastegate():
    s = header("TURBOCHARGER WASTEGATE STUCK CLOSED")
    s += panel(40, 142, 710, 444, hl=True)
    s += f'<rect x="80" y="250" width="160" height="150" rx="14" fill="#cbd5e1" stroke="{INK}" stroke-width="3"/>\n'
    s += t(160, 332, "ENGINE", 16, 800, INK)
    s += polyline([(240, 360), (420, 360)], "#f97316", 16)
    s += f'<circle cx="460" cy="360" r="40" fill="#fed7aa" stroke="{INK}" stroke-width="3"/>\n'
    s += t(460, 366, "TURBINE", 12, 800, INK)
    s += polyline([(460, 400), (460, 520)], "#f97316", 16)
    s += t(476, 520, "EXHAUST OUT", 12, 800, MUTED, "start")
    s += polyline([(340, 360), (340, 470), (452, 470)], "#fdba74", 12)
    s += f'<rect x="318" y="410" width="44" height="30" rx="4" fill="{RED}" stroke="{INK}" stroke-width="2.5"/>\n'
    s += f'<path d="M 324,416 L 356,434 M 356,416 L 324,434" stroke="#ffffff" stroke-width="4"/>\n'
    s += t(300, 430, "WASTEGATE", 13, 800, RED, "end")
    s += t(300, 448, "STUCK CLOSED", 13, 800, RED, "end")
    s += line(500, 360, 560, 360, "#475569", 8)
    s += f'<circle cx="600" cy="360" r="46" fill="#bfdbfe" stroke="{INK}" stroke-width="3"/>\n'
    s += t(600, 365, "COMPRESSOR", 10, 800, INK)
    s += polyline([(600, 320), (600, 210), (160, 210), (160, 250)], "#60a5fa", 16)
    s += t(380, 198, "BOOSTED AIR TO THE INTAKE", 13, 800, "#1d4ed8")
    s += line(720, 360, 646, 360, BLUE, 4, "aBlue")
    s += t(700, 340, "AIR", 12, 800, BLUE)
    s += t(395, 566, "All exhaust drives the turbine: boost cannot be limited.", 15, 800, RED)
    s += g.fact_column([
        ("NORMAL", ["The wastegate bypasses", "exhaust round the turbine", "to limit boost."]),
        ("STUCK CLOSED", ["All exhaust passes through", "the turbine: boost keeps", "rising."]),
        ("IN A DESCENT", ["Denser air at full throttle", "can overboost: manifold", "pressure exceeds maximum."]),
    ])
    s += footer("With the wastegate stuck closed, manifold pressure may exceed the maximum permitted value.")
    return s


def power_torque():
    s = header("ENGINE POWER = TORQUE x ANGULAR SPEED")
    s += panel(40, 142, 710, 444, hl=True)
    cx, cy = 260, 370
    s += f'<circle cx="{cx}" cy="{cy}" r="130" fill="#e2e8f0" stroke="{INK}" stroke-width="3"/>\n'
    s += f'<circle cx="{cx}" cy="{cy}" r="16" fill="#475569"/>\n'
    s += line(cx, cy, cx + 130, cy, "#475569", 3, dash="6 5")
    s += line(cx + 130, cy + 50, cx + 130, cy - 60, RED, 6, "aRed")
    s += t(cx + 140, cy - 64, "FORCE", 14, 800, RED, "start")
    s += t(cx + 60, cy + 22, "RADIUS", 13, 800, INK)
    a0, a1 = math.radians(200), math.radians(320)
    s += f'<path d="M {cx + 160 * math.cos(a0):.1f} {cy - 160 * math.sin(a0):.1f} A 160 160 0 0 0 {cx + 160 * math.cos(a1):.1f} {cy - 160 * math.sin(a1):.1f}" fill="none" stroke="{GOLD_DARK}" stroke-width="5" marker-end="url(#aDark)"/>\n'
    s += t(cx - 170, cy + 196, "ANGULAR SPEED (ω)", 14, 800, GOLD_DARK, "start")
    s += t(560, 250, "TORQUE", 18, 800, INK)
    s += t(560, 276, "= force × radius", 15, 400, BODY)
    s += t(560, 350, "POWER", 22, 800, GOLD_DARK)
    s += t(560, 388, "P = T × ω", 26, 800, GOLD_DARK)
    s += t(560, 450, "Same torque at higher", 15, 400, BODY)
    s += t(560, 472, "RPM gives more power.", 15, 400, BODY)
    s += g.fact_column([
        ("TORQUE", ["The turning moment the", "crankshaft produces."]),
        ("ANGULAR SPEED", ["How fast it turns, in", "radians per second (from RPM)."]),
        ("POWER", ["Torque multiplied by", "angular speed."]),
    ])
    s += footer("The mechanical power of a rotating engine is torque multiplied by angular speed.")
    return s


BATCHES = {
    "piston-batch-2": {
        "q2470-mixture-rich": lambda: carb("rich"),
        "q2472-mixture-lean": lambda: carb("lean"),
        "q2744-carburettor-fuel-strainer": lambda: carb("strainer"),
        "q2511-accelerator-pump": lambda: carb("accel"),
        "q2747-mixture-richens-with-altitude": altitude_rich,
    },
    "piston-batch-3": {
        "q2519-pre-ignition": lambda: pre_ignition("pre"),
        "q2749-run-on-glowing-carbon": lambda: pre_ignition("runon"),
        "q2526-blue-exhaust-smoke": lambda: smoke("blue"),
        "q2547-black-exhaust-smoke": lambda: smoke("black"),
        "q2772-spark-plug-oil-fouling": lambda: lub.spark_plugs("oil"),
    },
    "piston-batch-4": {
        "q2556-ignition-timing-btdc": lambda: timing("btdc"),
        "q2554-ignition-timing-fixed": lambda: timing("fixed"),
        "q2524-unapproved-mogas": lambda: fuel_grade("mogas"),
        "q2550-higher-octane-fuel": lambda: fuel_grade("higher"),
        "q2561-cht-hottest-cylinder": cht,
    },
    "piston-batch-5": {
        "q2482-engine-primer": primer,
        "q2503-alternate-air": alternate_air,
        "q2500-carburettor-icing-symptoms": carb_icing,
        "q2491-flooded-engine-start": flooded,
        "q2499-smooth-throttle-handling": throttle_smooth,
    },
    "piston-batch-6": {
        "q2548-crankshaft-counterweights": counterweights,
        "q2726-maximum-power-conditions": density_power,
        "q2729-over-leaning": over_lean,
        "q2730-otto-cycle": otto,
        "q2741-wastegate-stuck-closed": wastegate,
        "q2742-power-torque-angular-speed": power_torque,
    },
}

if __name__ == "__main__":
    for batch in sys.argv[1:] or BATCHES:
        pub = OUT / batch
        pub.mkdir(parents=True, exist_ok=True)
        for name, fn in BATCHES[batch].items():
            (pub / f"{name}.svg").write_text(fn(), encoding="utf-8")
            print("wrote", batch, name)
