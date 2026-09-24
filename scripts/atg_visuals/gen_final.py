"""Pressure instruments, compass, fuel, gyro and legal explanation diagrams (ATG)."""
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
OUT = REPO / "public/explanation-images/aircraft-technical-and-general"


def panel(x=40, y=142, w=710, h=444, hl=False):
    fill, stroke, sw = ("#fff8e1", GOLD, 4) if hl else ("#f8fafc", "#cbd5e1", 2)
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>\n'


def box(x, y, w, h, hl=False, fill="#ffffff"):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{"#fde68a" if hl else fill}" stroke="{GOLD if hl else "#cbd5e1"}" stroke-width="{4 if hl else 2}"/>\n'


def lines(x, y, rows, size=15, weight=400, fill=BODY, anchor="start", gap=22):
    s = ""
    for i, r in enumerate(rows):
        s += t(x, y + i * gap, r, size, weight, fill, anchor)
    return s


# =====================================================================
# airspeed chain (q2657 CAS, q2634/q2659 TAS)
# =====================================================================

def airspeed_chain(answer):
    title = "CALIBRATED (RECTIFIED) AIRSPEED" if answer == "cas" else "TRUE AIRSPEED"
    s = header(title)
    s += panel(hl=True)
    steps = [("IAS", "Indicated airspeed", "as read on the ASI"),
             ("CAS / RAS", "Calibrated (rectified)", ""),
             ("EAS", "Equivalent airspeed", "(compressibility, high speed)"),
             ("TAS", "True airspeed", "speed through the air")]
    corr = ["+ instrument & position error", "(+ compressibility)", "+ density (altitude and temperature)"]
    y = 190
    for i, (ab, nm, sub) in enumerate(steps):
        hl = (answer == "cas" and ab.startswith("CAS")) or (answer == "tas" and ab == "TAS")
        s += box(90, y, 240, 70, hl)
        s += t(110, y + 32, ab, 22, 800, INK, "start")
        s += t(110, y + 54, nm, 14, 400, BODY, "start")
        if sub:
            s += t(350, y + 42, sub, 13, 400, MUTED, "start")
        if i < 3:
            hl2 = (answer == "cas" and i == 0) or (answer == "tas" and i == 2)
            s += line(210, y + 72, 210, y + 102, GOLD_DARK if hl2 else "#94a3b8", 4, "aDark")
            s += t(232, y + 94, corr[i], 14, 800, GOLD_DARK if hl2 else MUTED, "start")
        y += 102
    facts = {
        "cas": [("IAS", ["What the airspeed indicator", "shows."]),
                ("CORRECT FOR", ["Instrument error and position", "(pressure) error."]),
                ("RESULT", ["Calibrated (rectified)", "airspeed: CAS / RAS."])],
        "tas": [("START FROM CAS/RAS", ["Instrument and position error", "already corrected."]),
                ("CORRECT FOR DENSITY", ["Altitude (pressure) and", "temperature: less dense air", "means TAS > CAS."]),
                ("RULE OF THUMB", ["TAS is about 2% more than", "CAS per 1,000 ft."])],
    }[answer]
    s += g.fact_column(facts)
    foot = ("Calibrated (rectified) airspeed is IAS corrected for instrument and position error."
            if answer == "cas" else "True airspeed is CAS/RAS corrected for density: temperature and altitude.")
    s += footer(foot)
    return s


# =====================================================================
# alternate static inside cockpit (q2588, q2660, q2661)
# =====================================================================

def alt_static():
    s = header("ALTERNATE STATIC SOURCE")
    s += panel(hl=True)
    # fuselage outline
    s += f'<path d="M 70,300 Q 90,230 200,220 L 600,230 Q 700,240 720,300 Q 700,380 600,390 L 200,400 Q 90,390 70,300 Z" fill="#e2e8f0" stroke="{INK}" stroke-width="3"/>\n'
    s += t(400, 212, "FUSELAGE (SIDE VIEW)", 12, 800, MUTED)
    s += f'<circle cx="560" cy="386" r="8" fill="{RED}" stroke="{INK}" stroke-width="2"/>\n'
    s += f'<path d="M 552,378 l 16,16 M 568,378 l -16,16" stroke="#ffffff" stroke-width="3"/>\n'
    s += t(600, 420, "STATIC VENT BLOCKED", 12, 800, RED)
    s += f'<rect x="260" y="270" width="220" height="80" rx="10" fill="#ffffff" stroke="{INK}" stroke-width="2.5"/>\n'
    s += t(370, 296, "COCKPIT", 13, 800, INK)
    s += t(370, 316, "slightly lower pressure", 12, 400, BODY)
    s += t(370, 334, "(suction from the airflow)", 12, 400, BODY)
    s += f'<rect x="300" y="352" width="44" height="22" rx="4" fill="{GOLD}" stroke="{INK}" stroke-width="2"/>\n'
    s += t(322, 424, "ALTERNATE STATIC", 12, 800, GOLD_DARK)
    s += t(322, 438, "(INSIDE THE COCKPIT)", 11, 800, GOLD_DARK)
    rows = [("ASI", "OVER-READS"), ("ALTIMETER", "OVER-READS"), ("VSI", "brief climb indication")]
    s += t(90, 460, "WITH THE ALTERNATE SOURCE SELECTED:", 14, 800, INK, "start")
    for i, (ins, eff) in enumerate(rows):
        s += box(90 + i * 215, 476, 200, 80, i == 0)
        s += t(190 + i * 215, 506, ins, 16, 800, INK)
        s += t(190 + i * 215, 532, eff, 14, 800, RED if i < 2 else BODY)
    s += g.fact_column([
        ("WHERE", ["In many light aircraft the", "alternate static draws air", "from within the cockpit."]),
        ("WHY THE ERROR", ["Cockpit pressure is usually", "slightly below true static", "pressure."]),
        ("EFFECT", ["Lower static pressure: the", "ASI and altimeter over-read."]),
    ])
    s += footer("The alternate static source draws air from the cockpit; the ASI then over-reads.")
    return s


# =====================================================================
# two static vents (q2598, q2656)
# =====================================================================

def two_vents():
    s = header("TWO INTERCONNECTED STATIC VENTS")
    s += panel(hl=True)
    s += t(60, 172, "SIDESLIP, VIEWED FROM ABOVE", 14, 800, INK, "start")
    cx, cy = 395, 360
    s += f'<g transform="rotate(-15 {cx} {cy})">\n'
    s += f'<path d="M {cx},{cy - 170} C {cx + 40},{cy - 160} {cx + 40},{cy - 60} {cx + 34},{cy + 10} L {cx + 12},{cy + 160} L {cx - 12},{cy + 160} L {cx - 34},{cy + 10} C {cx - 40},{cy - 60} {cx - 40},{cy - 160} {cx},{cy - 170} Z" fill="#e2e8f0" stroke="{INK}" stroke-width="3"/>\n'
    s += f'<circle cx="{cx - 36}" cy="{cy - 40}" r="8" fill="{GOLD}" stroke="{INK}" stroke-width="2"/>\n'
    s += f'<circle cx="{cx + 36}" cy="{cy - 40}" r="8" fill="{GOLD}" stroke="{INK}" stroke-width="2"/>\n'
    s += polyline([(cx - 36, cy - 40), (cx, cy - 20), (cx + 36, cy - 40)], "#b45309", 3)
    s += line(cx, cy - 20, cx, cy + 20, "#b45309", 3)
    s += "</g>\n"
    for y in (190, 250, 310):
        s += line(80, y, 230, y + 40, BLUE, 4, "aBlue")
    s += t(150, 386, "RELATIVE AIRFLOW", 13, 800, BLUE)
    s += t(330, 440, "HIGHER PRESSURE", 13, 800, RED, "end")
    s += t(560, 330, "LOWER PRESSURE", 13, 800, BLUE, "start")
    s += t(395, 540, "Joined vents average the two pressures: position error is reduced.", 15, 800, GOLD_DARK)
    s += g.fact_column([
        ("ONE VENT ONLY", ["In a sideslip it is on the", "windward or sheltered side:", "pressure is wrong."]),
        ("ONE EACH SIDE", ["Interconnected vents on both", "sides of the fuselage."]),
        ("AVERAGED", ["The errors largely cancel:", "position error is reduced."]),
    ])
    s += footer("Two interconnected static vents, one each side of the fuselage, reduce position error.")
    return s


# =====================================================================
# manoeuvre-induced error (q2636)
# =====================================================================

def manoeuvre_error():
    s = header("MANOEUVRE-INDUCED ERROR")
    s += panel(hl=True)
    for i, (head, pitch, ok) in enumerate((("STEADY FLIGHT", 0, True), ("RAPID ATTITUDE CHANGE", 14, False))):
        px = 60 + i * 340
        s += box(px, 170, 320, 300)
        s += t(px + 160, 200, head, 16, 800, INK)
        cx, cy = px + 160, 320
        s += f'<g transform="rotate({-pitch} {cx} {cy})"><path d="M {cx - 120},{cy} Q {cx - 100},{cy - 24} {cx - 40},{cy - 26} L {cx + 100},{cy - 14} L {cx + 120},{cy} L {cx + 100},{cy + 12} L {cx - 40},{cy + 22} Q {cx - 100},{cy + 20} {cx - 120},{cy} Z" fill="#e2e8f0" stroke="{INK}" stroke-width="3"/>\n'
        s += f'<circle cx="{cx}" cy="{cy + 20}" r="6" fill="{GOLD}" stroke="{INK}" stroke-width="2"/></g>\n'
        if ok:
            s += t(cx, 430, "Steady static pressure", 15, 800, GREEN)
        else:
            for k in range(4):
                s += f'<path d="M {cx - 20 + k * 12},{cy + 50} q 4,-8 8,0 q 4,8 8,0" fill="none" stroke="{RED}" stroke-width="2.5"/>\n'
            s += t(cx, 420, "Pressure fluctuates at", 15, 800, RED)
            s += t(cx, 440, "the static vent", 15, 800, RED)
    s += t(395, 520, "Result: brief false readings on the pressure instruments.", 15, 800, GOLD_DARK)
    s += t(395, 546, "Most VSIs damp this with a small counterbalance weight.", 14, 400, BODY)
    s += g.fact_column([
        ("CAUSE", ["Airflow round the static vent", "changes during rapid attitude", "and altitude changes."]),
        ("EFFECT", ["The static pressure fluctuates:", "a false indication, e.g. a", "false climb or descent."]),
        ("TEMPORARY", ["Settles once the manoeuvre", "is complete."]),
    ])
    s += footer("Manoeuvre-induced error: static-pressure fluctuations during rapid changes cause false readings.")
    return s


# =====================================================================
# ISA (q2702 density, q2707 temperature and lapse rate)
# =====================================================================

def isa(answer):
    s = header("INTERNATIONAL STANDARD ATMOSPHERE")
    s += panel(hl=True)
    s += t(60, 176, "ISA MEAN SEA-LEVEL VALUES", 16, 800, INK, "start")
    vals = [("temp", "TEMPERATURE", "15 °C"), ("press", "PRESSURE", "1013.25 hPa"),
            ("density", "DENSITY", "1.225 kg/m³"), ("lapse", "LAPSE RATE", "1.98 °C / 1,000 ft")]
    for i, (key, nm, v) in enumerate(vals):
        x, y = 60 + (i % 2) * 340, 196 + (i // 2) * 110
        hl = (answer == "density" and key == "density") or (answer == "temp" and key in ("temp", "lapse"))
        s += box(x, y, 320, 96, hl)
        s += t(x + 20, y + 34, nm, 14, 800, MUTED, "start")
        s += t(x + 20, y + 72, v, 26, 800, INK, "start")
    s += t(60, 452, "TEMPERATURE PROFILE", 14, 800, INK, "start")
    ox, oy = 90, 560
    s += line(ox, oy, 700, oy, "#94a3b8", 2)
    s += line(ox, oy, ox, 462, "#94a3b8", 2, "aDark")
    s += t(ox + 6, 474, "HEIGHT", 11, 800, MUTED, "start")
    s += t(700, oy + 18, "WARMER →", 11, 800, MUTED, "end")
    s += polyline([(620, oy), (300, 478), (300, 462)], RED, 4)
    s += t(630, oy - 8, "+15 °C at MSL", 13, 800, RED, "start")
    s += t(310, 478, "−56.5 °C at 36,090 ft (tropopause), then constant", 13, 800, RED, "start")
    s += g.fact_column([
        ("SEA-LEVEL DENSITY", ["1.225 kg/m³ (ISA), used to", "calibrate the ASI."]),
        ("TEMPERATURE", ["15 °C at sea level, falling", "1.98 °C per 1,000 ft."]),
        ("TROPOPAUSE", ["36,090 ft: temperature", "then constant at −56.5 °C."]),
    ])
    foot = ("In the ISA, sea-level air density is 1.225 kg/m³."
            if answer == "density" else "ISA: 15 °C at sea level, lapse rate 1.98 °C per 1,000 ft up to 36,090 ft.")
    s += footer(foot)
    return s


# =====================================================================
# ASI: dynamic pressure (q2733) and calibration (q2771)
# =====================================================================

def asi(answer):
    title = "DYNAMIC PRESSURE" if answer == "q" else "ASI CALIBRATION"
    s = header(title)
    s += panel(hl=True)
    # pitot / static into ASI capsule
    s += f'<rect x="90" y="250" width="120" height="16" rx="4" fill="#94a3b8" stroke="{INK}" stroke-width="2"/>\n'
    s += line(40, 258, 88, 258, BLUE, 4, "aBlue")
    s += t(150, 240, "PITOT (TOTAL)", 12, 800, INK)
    s += polyline([(210, 258), (330, 258), (330, 330)], "#1d4ed8", 4)
    s += polyline([(150, 420), (440, 420), (440, 380)], "#64748b", 4)
    s += f'<circle cx="150" cy="420" r="7" fill="#64748b"/>\n'
    s += t(150, 448, "STATIC", 12, 800, INK)
    s += f'<rect x="300" y="330" width="170" height="110" rx="12" fill="#ffffff" stroke="{INK}" stroke-width="3"/>\n'
    s += f'<ellipse cx="385" cy="366" rx="54" ry="22" fill="#fde68a" stroke="{INK}" stroke-width="2.5"/>\n'
    s += t(385, 370, "CAPSULE", 11, 800, INK)
    s += t(385, 414, "ASI CASE (STATIC)", 11, 800, MUTED)
    s += t(620, 250, "DYNAMIC PRESSURE", 16, 800, GOLD_DARK if answer == "q" else INK)
    s += t(620, 290, "q = ½ ρ V²", 28, 800, GOLD_DARK if answer == "q" else INK)
    s += t(620, 322, "= pitot − static", 15, 400, BODY)
    s += t(620, 400, "CALIBRATED FOR", 15, 800, GOLD_DARK if answer == "cal" else INK)
    s += t(620, 424, "ISA sea-level density", 15, 800, GOLD_DARK if answer == "cal" else INK)
    s += t(620, 448, "ρ = 1.225 kg/m³", 15, 400, BODY)
    s += t(395, 540, "ρ = air density, V = true airspeed", 14, 400, BODY)
    s += g.fact_column([
        ("DEPENDS ON", ["Air density and the square", "of the airflow speed."]),
        ("THE ASI MEASURES q", ["Pitot minus static pressure", "moves the capsule."]),
        ("CALIBRATION", ["Scaled assuming ISA sea-level", "density, so IAS = TAS only", "in those conditions."]),
    ])
    foot = ("Dynamic pressure depends on air density and the square of airflow speed (q = ½ρV²)."
            if answer == "q" else "A simple ASI is calibrated for standard (ISA) sea-level air density.")
    s += footer(foot)
    return s


# =====================================================================
# take-off: VR (q2758)
# =====================================================================

def vr():
    s = header("VR: ROTATION SPEED")
    s += panel(hl=True)
    s += f'<rect x="60" y="430" width="670" height="40" fill="#475569"/>\n'
    for x in range(80, 720, 60):
        s += line(x, 450, x + 30, 450, "#ffffff", 3)
    s += line(700, 370, 600, 370, INK, 4, "aDark")
    s += t(650, 360, "DIRECTION OF TAKE-OFF", 12, 800, MUTED)
    stages = [(640, 409, 0, "START OF ROLL", 500), (430, 409, 7, "VR: ROTATE", 500),
              (270, 392, 9, "VLOF: LIFT-OFF", 500), (120, 318, 11, "CLIMB (VX / VY)", 272)]
    for x, y, pitch, lab, ly in stages:
        gsvg, _ = g.plane(x, y, 0.55, pitch)
        s += gsvg
        hl = lab.startswith("VR")
        s += t(x, ly, lab, 14, 800, GOLD_DARK if hl else INK)
        if hl:
            s += f'<rect x="{x - 70}" y="{ly - 22}" width="140" height="32" rx="8" fill="none" stroke="{GOLD}" stroke-width="3"/>\n'
    s += t(395, 196, "The pilot begins to raise the nose wheel at VR.", 16, 800, INK)
    s += g.fact_column([
        ("VR", ["Rotation speed: start raising", "the nose wheel."]),
        ("VLOF", ["Lift-off speed: the main", "wheels leave the runway."]),
        ("VX / VY", ["Best angle / best rate of", "climb speeds after take-off."]),
    ])
    s += footer("VR is the speed at which the pilot begins to raise the nose wheel during take-off.")
    return s


# =====================================================================
# compass: TVMDC (q2683 variation, q2704 deviation), deviation card (q2674)
# =====================================================================

def tvmdc(answer):
    title = "MAGNETIC VARIATION" if answer == "var" else "COMPASS DEVIATION"
    s = header(title)
    s += panel(hl=True)
    items = [("TRUE", "Geographic north"), ("MAGNETIC", "Magnetic north"), ("COMPASS", "What the compass shows")]
    for i, (nm, sub) in enumerate(items):
        x = 80 + i * 230
        s += box(x, 250, 190, 90)
        s += t(x + 95, 290, nm, 20, 800, INK)
        s += t(x + 95, 316, sub, 13, 400, BODY)
    for i, (nm, why, key) in enumerate((("VARIATION", "Earth's magnetic field", "var"), ("DEVIATION", "Aircraft's own magnetism", "dev"))):
        x = 270 + i * 230
        hl = key == answer
        s += line(x, 295, x + 40, 295, GOLD_DARK if hl else "#94a3b8", 5, "aDark")
        s += f'<rect x="{x - 66}" y="370" width="172" height="80" rx="10" fill="{"#fde68a" if hl else "#ffffff"}" stroke="{GOLD if hl else "#cbd5e1"}" stroke-width="{4 if hl else 2}"/>\n'
        s += t(x + 20, 402, nm, 18, 800, GOLD_DARK if hl else INK)
        s += t(x + 20, 426, why, 12, 400, BODY)
    s += t(395, 510, "True → Magnetic: apply VARIATION.   Magnetic → Compass: apply DEVIATION.", 14, 800, INK)
    s += t(395, 540, "Memory aid: T V M D C", 15, 400, BODY)
    s += g.fact_column([
        ("VARIATION", ["Angle between true and", "magnetic north; changes", "with location."]),
        ("DEVIATION", ["Angle between magnetic and", "compass north; caused by", "the aircraft's magnetism."]),
        ("DEVIATION CARD", ["Shows the correction for", "each heading."]),
    ])
    foot = ("The difference between true and magnetic bearings is caused by variation."
            if answer == "var" else "The difference between magnetic and compass bearings is caused by deviation.")
    s += footer(foot)
    return s


def deviation_card():
    s = header("DEVIATION VARIES WITH HEADING")
    s += panel(hl=True)
    s += f'<rect x="100" y="190" width="590" height="250" rx="10" fill="#ffffff" stroke="{INK}" stroke-width="3"/>\n'
    s += t(395, 220, "COMPASS DEVIATION CARD", 16, 800, INK)
    heads = ["N", "030", "060", "E", "120", "150", "S", "210", "240", "W", "300", "330"]
    steer = ["358", "029", "061", "092", "123", "152", "181", "212", "241", "268", "297", "328"]
    for i in range(12):
        x = 120 + (i % 6) * 95
        y = 250 + (i // 6) * 90
        s += f'<rect x="{x}" y="{y}" width="85" height="76" rx="6" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>\n'
        s += t(x + 42, y + 24, f"FOR {heads[i]}", 12, 800, MUTED)
        s += t(x + 42, y + 56, f"STEER {steer[i]}", 13, 800, INK)
    s += t(395, 490, "The correction is different on each heading.", 16, 800, GOLD_DARK)
    s += t(395, 520, "Checked by a compass swing and placed next to the compass.", 14, 400, BODY)
    s += g.fact_column([
        ("CAUSE", ["The aircraft's own magnetic", "fields (steel parts, wiring,", "radios)."]),
        ("VARIES WITH HEADING", ["As the aircraft turns, these", "fields act on the compass", "differently."]),
        ("RECORDED ON A CARD", ["Measured in a compass swing", "and displayed in the cockpit."]),
    ])
    s += footer("Compass deviation in a particular aircraft varies with each heading.")
    return s


# =====================================================================
# acceleration errors (q2681 SH, q2728 NH decel on 270)
# =====================================================================

def accel_error(answer):
    if answer == "sh":
        title = "ACCELERATION ERROR: SOUTHERN HEMISPHERE"
        rows = [("ACCELERATE", "apparent turn towards SOUTH", RED), ("DECELERATE", "apparent turn towards NORTH", BLUE)]
        rule = "SH: ACCELERATE SOUTH, DECELERATE NORTH"
        foot = "Southern Hemisphere, E/W headings: accelerating shows a turn south, decelerating a turn north."
    else:
        title = "DECELERATION ERROR: NORTHERN HEMISPHERE"
        rows = [("ACCELERATE", "apparent turn towards NORTH", RED), ("DECELERATE", "apparent turn towards SOUTH", BLUE)]
        rule = "NH: ANDS (ACCELERATE NORTH, DECELERATE SOUTH)"
        foot = "Northern Hemisphere, decelerating on 270°: apparent turn south, compass reads about 240°."
    s = header(title)
    s += panel(hl=True)
    s += t(395, 178, "ON EAST OR WEST HEADINGS", 15, 800, INK)
    for i, (a, txt, col) in enumerate(rows):
        s += box(80, 200 + i * 80, 630, 66, i == (1 if answer == "nh" else 0) or answer == "sh")
        s += t(100, 240 + i * 80, a, 18, 800, INK, "start")
        s += t(300, 240 + i * 80, txt, 17, 800, col, "start")
    s += t(395, 390, rule, 17, 800, GOLD_DARK)
    if answer == "nh":
        cx, cy = 395, 490
        s += f'<circle cx="{cx}" cy="{cy}" r="70" fill="#ffffff" stroke="{INK}" stroke-width="3"/>\n'
        for hdg, lab in ((0, "N"), (90, "E"), (180, "S"), (270, "W")):
            a = math.radians(hdg - 90)
            s += t(cx + 54 * math.cos(a), cy + 54 * math.sin(a) + 6, lab, 16, 800, INK)
        for hdg, col, w in ((270, "#94a3b8", 4), (240, RED, 5)):
            a = math.radians(hdg - 90)
            s += line(cx, cy, cx + 44 * math.cos(a), cy + 44 * math.sin(a), col, w, "aRedS" if col == RED else None)
        s += t(cx + 90, cy - 10, "Actual heading 270°", 14, 800, MUTED, "start")
        s += t(cx + 90, cy + 14, "Compass shows ~240°", 14, 800, RED, "start")
    else:
        s += t(395, 440, "Opposite to the Northern Hemisphere (ANDS).", 15, 400, BODY)
        s += t(395, 470, "Caused by magnetic dip acting on the pendulous", 15, 400, BODY)
        s += t(395, 494, "magnet system when speed changes.", 15, 400, BODY)
    s += g.fact_column([
        ("CAUSE", ["Magnetic dip: the magnets are", "offset from the pivot, so", "inertia swings them."]),
        ("EAST/WEST HEADINGS", ["Error is greatest on E and W,", "zero on N and S."]),
        ("TEMPORARY", ["Reads correctly again once", "the speed is steady."]),
    ])
    s += footer(foot)
    return s


def turning_error():
    s = header("COMPASS TURNING ERROR")
    s += panel(hl=True)
    s += t(60, 176, "CAUSED BY MAGNETIC DIP + ACCELERATION IN THE TURN", 15, 800, INK, "start")
    s += box(60, 196, 320, 150, True)
    s += t(220, 232, "NORTHERN HEMISPHERE", 15, 800, INK)
    s += t(220, 270, "UNOS", 32, 800, GOLD_DARK)
    s += t(220, 300, "Undershoot North", 14, 400, BODY)
    s += t(220, 322, "Overshoot South", 14, 400, BODY)
    s += box(400, 196, 320, 150)
    s += t(560, 232, "SOUTHERN HEMISPHERE", 15, 800, INK)
    s += t(560, 270, "ONUS", 32, 800, INK)
    s += t(560, 300, "Overshoot North", 14, 400, BODY)
    s += t(560, 322, "Undershoot South", 14, 400, BODY)
    s += t(60, 386, "EXAMPLE (NH): TURN FROM 030° TO 180° BY THE SHORTEST WAY", 14, 800, INK, "start")
    s += t(60, 416, "Right turn onto south: the compass lags, so roll out", 15, 400, BODY, "start")
    s += t(60, 440, "after it passes south, at about 210° indicated.", 15, 400, BODY, "start")
    cx, cy = 600, 480
    s += f'<circle cx="{cx}" cy="{cy}" r="72" fill="#ffffff" stroke="{INK}" stroke-width="3"/>\n'
    for hdg, lab in ((0, "N"), (90, "E"), (180, "S"), (270, "W")):
        a = math.radians(hdg - 90)
        s += t(cx + 56 * math.cos(a), cy + 56 * math.sin(a) + 6, lab, 15, 800, INK)
    a0, a1 = math.radians(30 - 90), math.radians(210 - 90)
    s += f'<path d="M {cx + 86 * math.cos(a0):.1f} {cy + 86 * math.sin(a0):.1f} A 86 86 0 0 1 {cx + 86 * math.cos(a1):.1f} {cy + 86 * math.sin(a1):.1f}" fill="none" stroke="{GOLD_DARK}" stroke-width="4" marker-end="url(#aDark)"/>\n'
    s += t(cx - 110, cy + 90, "ROLL OUT AT ~210°", 14, 800, GOLD_DARK, "end")
    s += g.fact_column([
        ("TWO CAUSES", ["Magnetic dip and the", "acceleration forces in the", "turn."]),
        ("TURNS THROUGH N AND S", ["Error is greatest on", "northerly and southerly", "headings."]),
        ("ALLOW FOR IT", ["Roll out early or late, or", "use the heading indicator."]),
    ])
    s += footer("Compass turning error is caused mainly by magnetic dip and acceleration forces in the turn.")
    return s


# =====================================================================
# fuel systems
# =====================================================================

def fuel_outlet():
    s = header("FUEL TANK OUTLET AND SUMP")
    s += panel(hl=True)
    s += f'<path d="M 120,210 L 640,210 L 640,420 L 420,420 L 400,470 L 360,470 L 340,420 L 120,420 Z" fill="#ffffff" stroke="{INK}" stroke-width="4"/>\n'
    s += f'<path d="M 124,290 L 636,290 L 636,416 L 124,416 Z" fill="#60a5fa" fill-opacity="0.55"/>\n'
    s += f'<path d="M 344,424 L 416,424 L 398,466 L 362,466 Z" fill="#7dd3fc"/>\n'
    for k in range(6):
        s += f'<circle cx="{362 + (k % 3) * 18}" cy="{440 + (k // 3) * 14}" r="4" fill="#78350f"/>\n'
    s += t(120, 500, "WATER AND SEDIMENT", 13, 800, "#78350f", "start")
    s += t(120, 518, "SETTLE IN THE SUMP", 13, 800, "#78350f", "start")
    s += line(270, 496, 352, 454, "#78350f", 2, "aDark")
    s += polyline([(560, 470), (560, 380)], INK, 10)
    s += polyline([(560, 470), (560, 380)], "#f59e0b", 6)
    s += line(560, 470, 560, 540, "#f59e0b", 6)
    s += t(576, 540, "TO THE ENGINE", 13, 800, INK, "start")
    s += t(652, 364, "OUTLET", 13, 800, GOLD_DARK, "start")
    s += t(652, 380, "ABOVE THE", 13, 800, GOLD_DARK, "start")
    s += t(652, 396, "SUMP", 13, 800, GOLD_DARK, "start")
    s += line(648, 378, 566, 382, GOLD_DARK, 2, "aDark")
    s += line(380, 470, 380, 520, INK, 5)
    s += f'<rect x="366" y="520" width="28" height="18" rx="3" fill="#94a3b8" stroke="{INK}" stroke-width="2"/>\n'
    s += t(360, 560, "DRAIN VALVE", 13, 800, INK, "end")
    s += g.fact_column([
        ("OUTLET RAISED", ["Fuel is drawn from above", "the lowest point of the", "tank."]),
        ("SUMP COLLECTS", ["Heavier water and dirt settle", "at the bottom, below the", "outlet."]),
        ("DRAIN BEFORE FLIGHT", ["Take a sample from the", "drain to check for water."]),
    ])
    s += footer("The fuel outlet is above the sump so water and impurities settle below it and can be drained.")
    return s


def bonding():
    s = header("BONDING WHEN REFUELLING")
    s += panel(hl=True)
    s += f'<rect x="80" y="300" width="200" height="110" rx="14" fill="#dc2626" stroke="{INK}" stroke-width="3"/>\n'
    s += t(180, 360, "FUEL TRUCK", 15, 800, "#ffffff")
    s += f'<path d="M 420,300 L 700,290 L 710,310 L 420,320 Z" fill="#e2e8f0" stroke="{INK}" stroke-width="3"/>\n'
    s += f'<rect x="520" y="316" width="120" height="50" rx="12" fill="#e2e8f0" stroke="{INK}" stroke-width="3"/>\n'
    s += t(612, 392, "AIRCRAFT", 14, 800, INK, "start")
    s += polyline([(280, 340), (360, 300), (470, 290)], "#111827", 6)
    s += f'<rect x="466" y="284" width="30" height="14" rx="3" fill="#475569"/>\n'
    s += t(380, 280, "NOZZLE", 12, 800, INK)
    s += line(40, 470, 750, 470, "#78350f", 4)
    s += t(60, 492, "GROUND", 12, 800, "#78350f", "start")
    for x0, y0, lab in ((160, 410, "TRUCK → GROUND"), (600, 366, "AIRCRAFT → GROUND")):
        s += polyline([(x0, y0), (x0, 470)], GREEN, 4, dash="8 5")
        s += t(x0 + 8, 450, lab, 12, 800, GREEN, "start")
    s += polyline([(250, 300), (250, 240), (540, 240), (540, 316)], GREEN, 4, dash="8 5")
    s += t(395, 232, "TRUCK → AIRCRAFT", 12, 800, GREEN)
    s += polyline([(482, 284), (482, 262), (520, 262)], GREEN, 3, dash="6 4")
    s += t(526, 266, "NOZZLE BONDED", 12, 800, GREEN, "start")
    s += t(395, 540, "All parts at the same electrical potential: no static spark.", 15, 800, GOLD_DARK)
    s += g.fact_column([
        ("STATIC ELECTRICITY", ["Fuel flowing through hoses", "and the airframe builds up", "static charge."]),
        ("BOND EVERYTHING", ["Earth leads join the ground,", "truck, nozzle and aircraft."]),
        ("NO SPARK", ["Equal potential means no", "spark to ignite fuel vapour."]),
    ])
    s += footer("Earth leads between ground, fuel truck, nozzle and aircraft remove the risk of a static spark.")
    return s


def avgas_colour():
    s = header("AVGAS 100LL IS BLUE")
    s += panel(hl=True)
    fuels = [("AVGAS 80", "#dc2626", "RED", False), ("AVGAS 100LL", "#2563eb", "BLUE", True), ("AVGAS 100", "#16a34a", "GREEN", False), ("JET A-1", "#fef3c7", "STRAW / CLEAR", False)]
    for i, (nm, col, cname, ans) in enumerate(fuels):
        x = 70 + i * 170
        s += f'<path d="M {x + 30},200 L {x + 110},200 L {x + 110},220 L {x + 128},240 L {x + 128},400 Q {x + 128},416 {x + 112},416 L {x + 28},416 Q {x + 12},416 {x + 12},400 L {x + 12},240 L {x + 30},220 Z" fill="#ffffff" stroke="{GOLD if ans else INK}" stroke-width="{5 if ans else 3}"/>\n'
        s += f'<rect x="{x + 18}" y="270" width="104" height="140" rx="8" fill="{col}"/>\n'
        s += t(x + 70, 446, nm, 15, 800, INK)
        s += t(x + 70, 470, cname, 14, 800, GOLD_DARK if ans else BODY)
    s += t(395, 530, "Always check the colour and grade before and after refuelling.", 15, 400, BODY)
    s += g.fact_column([
        ("100LL = BLUE", ["The most common piston-", "engine fuel is dyed blue."]),
        ("WHY DYED", ["Colour lets a pilot identify", "the grade in a fuel sample."]),
        ("JET FUEL", ["Clear or straw-coloured: never", "use in a piston engine."]),
    ])
    s += footer("100LL AVGAS can be identified by its blue colour.")
    return s


def full_tanks():
    s = header("FILL THE TANKS AFTER FLIGHT")
    for i, (head, level, ok) in enumerate((("HALF-FULL TANK OVERNIGHT", 0.45, False), ("FULL TANK OVERNIGHT", 0.95, True))):
        px = 48 + i * 362
        s += panel(px, 142, 346, 444, hl=ok)
        s += t(px + 20, 176, head, 16, 800, INK, "start")
        x0, y0, w, h = px + 50, 220, 246, 220
        s += f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" rx="10" fill="#ffffff" stroke="{INK}" stroke-width="4"/>\n'
        fy = y0 + h * (1 - level)
        s += f'<rect x="{x0 + 4}" y="{fy:.1f}" width="{w - 8}" height="{y0 + h - 4 - fy:.1f}" fill="#60a5fa" fill-opacity="0.55"/>\n'
        if not ok:
            for k in range(10):
                s += f'<circle cx="{x0 + 20 + k * 22}" cy="{y0 + 14}" r="4" fill="#0ea5e9"/>\n'
                s += f'<circle cx="{x0 + 10}" cy="{y0 + 30 + k * 9}" r="3" fill="#0ea5e9"/>\n'
            s += t(px + 173, 480, "Large air space: moist air", 15, 800, RED)
            s += t(px + 173, 502, "condenses on cold walls", 15, 800, RED)
        else:
            s += t(px + 173, 480, "Little air space:", 15, 800, GREEN)
            s += t(px + 173, 502, "minimal condensation", 15, 800, GREEN)
    s += g.fact_column([
        ("CONDENSATION", ["Moist air in an empty space", "condenses on cold tank walls", "overnight."]),
        ("WATER IN THE FUEL", ["The water sinks to the sump", "and can stop the engine."]),
        ("FULL TANKS", ["Leave little air space, so", "little water can form."]),
    ])
    s += footer("Refuelling to full after flight minimises condensation forming in the tanks overnight.")
    return s


def wet_wing():
    s = header("WET WING")
    s += panel(hl=True)
    s += f'<path d="M 80,260 L 700,230 L 700,330 L 80,360 Z" fill="#e2e8f0" stroke="{INK}" stroke-width="3"/>\n'
    s += f'<path d="M 200,256 L 520,241 L 520,339 L 200,353 Z" fill="#60a5fa" fill-opacity="0.6" stroke="{GOLD}" stroke-width="4"/>\n'
    for x in (200, 520):
        s += line(x, 256 if x == 200 else 241, x, 353 if x == 200 else 339, INK, 5)
    s += t(360, 305, "FUEL IN THE SEALED WING BOX", 14, 800, INK)
    s += t(200, 390, "SEALED SPAR / RIB", 12, 800, INK)
    s += t(520, 380, "SEALED SPAR / RIB", 12, 800, INK)
    s += t(395, 440, "The wing structure itself is the tank: no separate tank or bag.", 15, 800, GOLD_DARK)
    s += t(395, 470, "Sealant on the skins, spars and ribs keeps the fuel in.", 15, 400, BODY)
    s += g.fact_column([
        ("INTEGRAL TANK", ["The sealed wing structure", "forms the fuel tank."]),
        ("NOT REMOVABLE", ["Unlike a rigid or bladder", "tank fitted inside the wing."]),
        ("ADVANTAGES", ["Maximum fuel volume for", "the least weight."]),
    ])
    s += footer("A wet wing: the sealed wing structure itself forms an integral fuel tank.")
    return s


# =====================================================================
# gyroscopes
# =====================================================================

def gyro_rotor(cx, cy, r=70, col="#94a3b8"):
    s = f'<ellipse cx="{cx}" cy="{cy}" rx="{r}" ry="{r * 0.36:.1f}" fill="{col}" stroke="{INK}" stroke-width="3"/>\n'
    s += line(cx, cy - r * 0.9, cx, cy + r * 0.9, INK, 4)
    s += f'<path d="M {cx + r * 0.55},{cy - r * 0.46} A {r * 0.7} {r * 0.2} 0 0 1 {cx - r * 0.55},{cy - r * 0.46}" fill="none" stroke="{RED}" stroke-width="3" marker-end="url(#aRedS)"/>\n'
    return s


def gyro_props():
    s = header("GYROSCOPIC RIGIDITY AND PRECESSION")
    for i, (head, ans) in enumerate((("RIGIDITY", True), ("PRECESSION", False))):
        px = 48 + i * 362
        s += panel(px, 142, 346, 444, hl=ans)
        s += t(px + 20, 176, head, 20, 800, INK, "start")
        cx, cy = px + 173, 320
        s += gyro_rotor(cx, cy)
        if ans:
            s += line(cx, cy - 64, cx, cy - 120, GOLD_DARK, 5, "aDark")
            s += t(cx, 480, "A spinning gyro resists", 15, 800, INK)
            s += t(cx, 502, "any change to the", 15, 800, INK)
            s += t(cx, 524, "direction of its spin axis", 15, 800, INK)
        else:
            s += line(cx + 90, cy - 20, cx + 90, cy + 30, RED, 4, "aRedS")
            s += t(cx + 96, cy - 30, "FORCE", 12, 800, RED, "start")
            s += f'<path d="M {cx - 40},{cy - 96} A 60 30 0 0 1 {cx + 40},{cy - 96}" fill="none" stroke="{GOLD_DARK}" stroke-width="4" marker-end="url(#aDark)"/>\n'
            s += t(cx, 480, "A force on the rim acts", 15, 800, INK)
            s += t(cx, 502, "90° later in the direction", 15, 800, INK)
            s += t(cx, 524, "of rotation", 15, 800, INK)
    s += g.fact_column([
        ("TWO PROPERTIES", ["Every spinning gyroscope has", "rigidity and precession."]),
        ("RIGIDITY", ["Reluctance to turn away from", "its spin axis: used for", "attitude and heading."]),
        ("PRECESSION", ["Used in the turn indicator;", "also the cause of wander."]),
    ])
    s += footer("Rigidity: a spinning gyro's reluctance to move from its spin axis. It also has precession.")
    return s


def gyro_rigidity():
    s = header("WHAT INCREASES GYRO RIGIDITY")
    s += panel(hl=True)
    for i, (head, r, col) in enumerate((("LIGHT, SLOW ROTOR", 50, "#cbd5e1"), ("HEAVY, FAST ROTOR", 80, "#64748b"))):
        cx = 220 + i * 350
        s += t(cx, 186, head, 16, 800, INK)
        s += gyro_rotor(cx, 320, r, col)
        s += t(cx, 450, "LOW RIGIDITY" if i == 0 else "HIGH RIGIDITY", 18, 800, RED if i == 0 else GREEN)
    s += t(395, 510, "Rigidity ∝ moment of inertia × angular speed", 18, 800, GOLD_DARK)
    s += t(395, 540, "(mass, and how far it is from the axis)  ×  (RPM)", 14, 400, BODY)
    s += g.fact_column([
        ("MORE MASS", ["A heavier rotor, with mass", "near the rim, increases the", "moment of inertia."]),
        ("MORE SPEED", ["A faster spinning rotor", "increases rigidity."]),
        ("RESULT", ["Increase mass and speed:", "rigidity increases."]),
    ])
    s += footer("Gyro rigidity is proportional to the rotor's moment of inertia and angular speed.")
    return s


def real_wander():
    s = header("REAL WANDER OF A GYRO")
    s += panel(hl=True)
    for i, (head, subs, ans) in enumerate((("REAL WANDER", ["The spin axis physically", "moves in space."], True),
                                           ("APPARENT WANDER", ["The axis stays fixed; the", "Earth rotates beneath it."], False))):
        x = 60 + i * 340
        s += box(x, 176, 320, 190, ans)
        s += t(x + 160, 212, head, 18, 800, INK)
        s += lines(x + 160, 250, subs, 15, 400, BODY, "middle")
        if ans:
            s += lines(x + 20, 312, ["Caused by: bearing and gimbal", "wear, friction, imbalance,", "air turbulence"], 13, 800, RED, "start", 18)
    s += t(395, 420, "WEAR IN THE BEARINGS AND GIMBALS AND AIR TURBULENCE", 14, 800, GOLD_DARK)
    s += t(395, 444, "PRODUCE REAL WANDER", 14, 800, GOLD_DARK)
    s += t(395, 500, "Reset the heading indicator to the compass about every 15 minutes.", 15, 400, BODY)
    s += g.fact_column([
        ("REAL WANDER", ["Imperfections in the gyro", "itself move the spin axis."]),
        ("CAUSES", ["Bearing and gimbal wear,", "friction, imbalance and", "air turbulence."]),
        ("APPARENT WANDER", ["Due to the Earth's rotation,", "not a fault in the gyro."]),
    ])
    s += footer("Bearing and gimbal wear and air turbulence cause real wander of the gyro.")
    return s


def load_factor():
    s = header("LOAD FACTOR IN A LEVEL TURN")
    s += panel(hl=True)
    ox, oy, w, h = 110, 520, 560, 320
    s += line(ox, oy, ox + w, oy, INK, 2.5, "aDark")
    s += line(ox, oy, ox, oy - h, INK, 2.5, "aDark")
    s += t(ox + w, oy + 28, "ANGLE OF BANK", 13, 800, INK, "end")
    s += f'<text x="{ox - 26}" y="{oy - h / 2}" text-anchor="middle" font-family="{g.F}" font-size="13" font-weight="800" fill="{INK}" transform="rotate(-90 {ox - 26} {oy - h / 2})">LOAD FACTOR (g)</text>\n'
    X = lambda b: ox + b / 80 * w
    Y = lambda n: oy - (n - 1) / 4.8 * h
    pts = [(X(b), Y(1 / math.cos(math.radians(b)))) for b in range(0, 79)]
    s += polyline(pts, RED, 4)
    for b in (30, 45, 60):
        n = 1 / math.cos(math.radians(b))
        s += f'<circle cx="{X(b):.1f}" cy="{Y(n):.1f}" r="6" fill="{GOLD}" stroke="{INK}" stroke-width="2"/>\n'
        s += t(X(b) - 10, Y(n) - 12, f"{b}°: {n:.2f} g", 14, 800, INK, "end")
        s += t(X(b), oy + 20, f"{b}°", 12, 800, MUTED)
    s += t(ox + 20, oy - h + 10, "n = 1 / cos(bank)", 18, 800, GOLD_DARK, "start")
    s += g.fact_column([
        ("DEPENDS ON BANK", ["In a level, coordinated turn", "the load factor depends only", "on the bank angle."]),
        ("RISES STEEPLY", ["60° of bank doubles the", "load: 2 g."]),
        ("STALL SPEED", ["Rises with the square root", "of the load factor."]),
    ])
    s += footer("In a level coordinated turn the extra load on the wings is a function of the angle of bank.")
    return s


# =====================================================================
# ATG legal (South Africa)
# =====================================================================

def mpi_crs(answer):
    title = "MANDATORY PERIODIC INSPECTION" if answer == "mpi" else "CERTIFICATE OF RELEASE TO SERVICE"
    s = header(title)
    s += panel(hl=True)
    s += t(395, 184, "MPI → CERTIFICATE OF RELEASE TO SERVICE (CRS)", 16, 800, INK)
    for i, (head, big, sub) in enumerate((("CALENDAR", "12 MONTHS", "one year"), ("FLYING", "100 HOURS", "of flight time"))):
        x = 90 + i * 330
        s += box(x, 210, 280, 150, True)
        s += t(x + 140, 244, head, 15, 800, MUTED)
        s += t(x + 140, 296, big, 34, 800, GOLD_DARK)
        s += t(x + 140, 330, sub, 15, 400, BODY)
    s += t(395, 300, "OR", 20, 800, INK)
    s += t(395, 410, "WHICHEVER COMES FIRST", 24, 800, RED)
    s += t(395, 470, "The CRS issued on completion of the MPI is valid until the", 15, 400, BODY)
    s += t(395, 494, "next MPI is due: 12 months or 100 hours, whichever is first.", 15, 400, BODY)
    s += g.fact_column([
        ("MPI", ["Mandatory periodic inspection:", "at least yearly or every", "100 flying hours."]),
        ("CRS", ["Issued on completion of the", "MPI."]),
        ("WHICHEVER FIRST", ["A busy aircraft reaches 100 h", "before 12 months are up."]),
    ])
    foot = ("An MPI is required once a year or every 100 hours of flight time, whichever comes first."
            if answer == "mpi" else "A CRS issued after an MPI is valid for 12 months or 100 flight hours, whichever comes first.")
    s += footer(foot)
    return s


def logbook_48():
    s = header("MAINTENANCE LOGBOOK ENTRIES: 48 HOURS")
    s += panel(hl=True)
    for i, (head, rows) in enumerate((("AT BASE", ["Maintenance completed", "↓", "Entered in the logbook(s)", "within 48 HOURS of completion"]),
                                     ("AWAY FROM BASE", ["Maintenance done away", "↓", "Aircraft returns to base", "↓", "Transferred to the logbook(s)", "within 48 HOURS of return"]))):
        x = 70 + i * 340
        s += box(x, 176, 310, 380, True)
        s += t(x + 155, 212, head, 18, 800, INK)
        y = 262
        for r in rows:
            big = "48 HOURS" in r
            s += t(x + 155, y, r, 17 if big else 15, 800 if big else 400, GOLD_DARK if big else BODY)
            y += 44 if r == "↓" else 34
    s += g.fact_column([
        ("AT BASE", ["Log the work within 48 hours", "of completing it."]),
        ("AWAY FROM BASE", ["Transfer the details within", "48 hours after returning to", "base."]),
        ("WHY", ["The logbooks must show the", "aircraft's true maintenance", "status."]),
    ])
    s += footer("Maintenance must be entered in the logbooks within 48 hours (or 48 hours after return to base).")
    return s


def afm_supplements():
    s = header("FLIGHT MANUAL SUPPLEMENTS")
    s += panel(hl=True)
    secs = ["1 GENERAL", "2 LIMITATIONS", "3 EMERGENCY PROCEDURES", "4 NORMAL PROCEDURES", "5 PERFORMANCE", "6 WEIGHT & BALANCE", "7 SYSTEMS", "8 HANDLING & SERVICING", "9 SUPPLEMENTS"]
    for i, sec in enumerate(secs):
        y = 172 + i * 44
        hl = i == 8
        s += f'<rect x="90" y="{y}" width="330" height="36" rx="6" fill="{"#fde68a" if hl else "#ffffff"}" stroke="{GOLD if hl else "#cbd5e1"}" stroke-width="{4 if hl else 1.5}"/>\n'
        s += t(106, y + 24, sec, 15, 800 if hl else 700, INK, "start")
    s += lines(450, 520, ["Optional equipment, e.g.", "extra avionics, autopilot,", "floats or skis"], 15, 800, GOLD_DARK, "start", 22)
    s += line(440, 540, 424, 540, GOLD_DARK, 3)
    s += g.fact_column([
        ("SUPPLEMENTS", ["Cover optional equipment not", "installed in the standard", "aircraft."]),
        ("WHAT THEY GIVE", ["Limitations, procedures and", "performance for that", "equipment."]),
        ("CHECK", ["Read the supplements for the", "equipment fitted to your", "aircraft."]),
    ])
    s += footer("The Supplements section covers optional equipment not installed in a standard aircraft.")
    return s


def documents():
    s = header("DOCUMENTS TO CARRY: DOMESTIC FLIGHT")
    s += panel(hl=True)
    docs = [("CERTIFICATE OF REGISTRATION", True), ("CERTIFICATE OF AIRWORTHINESS", True), ("CERTIFICATE OF RELEASE TO SERVICE", True),
            ("VISUAL SIGNALS AND PROCEDURES FOR", True), ("USE BY INTERCEPTING AIRCRAFT", None)]
    y = 186
    for txt, hl in docs:
        if hl is None:
            s += t(126, y - 14, txt, 16, 800, INK, "start")
            continue
        s += f'<rect x="80" y="{y}" width="30" height="30" rx="6" fill="{GOLD}" stroke="{INK}" stroke-width="2"/>\n'
        s += f'<path d="M {86},{y + 16} l 7,7 l 12,-15" fill="none" stroke="{INK}" stroke-width="3"/>\n'
        s += t(126, y + 22, txt, 16, 800, INK, "start")
        y += 60
    s += t(80, 500, "Plus the other documents required by current Part 91", 14, 400, BODY, "start")
    s += t(80, 522, "(check the latest regulations).", 14, 400, BODY, "start")
    s += g.fact_column([
        ("LEGAL STATUS", ["Registration and airworthiness", "prove the aircraft may fly."]),
        ("MAINTENANCE STATUS", ["The CRS shows maintenance", "is current."]),
        ("INTERCEPTION", ["Signals so the crew can", "follow an interceptor's", "instructions."]),
    ])
    s += footer("Carry the registration, airworthiness and release-to-service certificates plus interception signals.")
    return s


def part43():
    s = header("PILOT MAINTENANCE UNDER PART 43")
    s += panel(hl=True)
    s += t(395, 184, "A PILOT MAY DO THE MAINTENANCE IN SA-CATS 43 ONLY IF:", 15, 800, INK)
    conds = [("HOLDS AN APPROPRIATE", "TYPE RATING"), ("IS THE OWNER", "OR OPERATOR"), ("AIRCRAFT IS USED FOR", "NON-COMMERCIAL OPERATIONS")]
    for i, (a, b) in enumerate(conds):
        x = 70 + i * 225
        s += box(x, 210, 210, 150, True)
        s += g.badge(x + 105, 244, i + 1)
        s += t(x + 105, 296, a, 14, 800, INK)
        s += t(x + 105, 318, b, 14, 800, GOLD_DARK)
    s += t(395, 410, "ALL THREE MUST APPLY", 22, 800, RED)
    s += t(395, 460, "Only the tasks listed in SA-CATS 43 may be done,", 15, 400, BODY)
    s += t(395, 484, "and the work must be recorded in the logbook.", 15, 400, BODY)
    s += g.fact_column([
        ("TYPE RATING", ["Rated on the aircraft type."]),
        ("OWNER / OPERATOR", ["The pilot owns or operates", "the aircraft."]),
        ("NON-COMMERCIAL", ["Not used for commercial", "operations."]),
    ])
    s += footer("A pilot may do SA-CATS 43 maintenance with a type rating, as owner/operator, non-commercially.")
    return s


BATCHES = {
    "pressure-batch-1": {
        "q2657-calibrated-airspeed": lambda: airspeed_chain("cas"),
        "q2634-true-airspeed": lambda: airspeed_chain("tas"),
        "q2661-alternate-static-source": alt_static,
        "q2656-two-static-vents": two_vents,
        "q2636-manoeuvre-induced-error": manoeuvre_error,
    },
    "pressure-batch-2": {
        "q2702-isa-sea-level-density": lambda: isa("density"),
        "q2707-isa-temperature-lapse-rate": lambda: isa("temp"),
        "q2733-dynamic-pressure": lambda: asi("q"),
        "q2771-asi-calibration": lambda: asi("cal"),
        "q2758-vr-rotation-speed": vr,
    },
    "compass-batch-1": {
        "q2683-variation": lambda: tvmdc("var"),
        "q2704-deviation": lambda: tvmdc("dev"),
        "q2674-deviation-card": deviation_card,
        "q2681-acceleration-error-southern": lambda: accel_error("sh"),
        "q2728-deceleration-error-northern": lambda: accel_error("nh"),
        "q2753-compass-turning-error": turning_error,
    },
    "fuel-batch-2": {
        "q2488-fuel-outlet-above-sump": fuel_outlet,
        "q2494-refuelling-bonding": bonding,
        "q2504-avgas-100ll-blue": avgas_colour,
        "q2510-full-tanks-condensation": full_tanks,
        "q2517-wet-wing": wet_wing,
    },
    "gyro-batch-1": {
        "q2622-gyro-rigidity-precession": gyro_props,
        "q2663-gyro-rigidity-factors": gyro_rigidity,
        "q2714-gyro-real-wander": real_wander,
        "q2673-load-factor-level-turn": load_factor,
    },
    "legal-batch-1": {
        "q2666-mpi": lambda: mpi_crs("mpi"),
        "q2697-certificate-of-release-to-service": lambda: mpi_crs("crs"),
        "q2694-logbook-48-hours": logbook_48,
        "q2692-afm-supplements": afm_supplements,
        "q2712-documents-to-carry": documents,
        "q2769-part-43-pilot-maintenance": part43,
    },
}

if __name__ == "__main__":
    for batch in sys.argv[1:] or BATCHES:
        pub = OUT / batch
        pub.mkdir(parents=True, exist_ok=True)
        for name, fn in BATCHES[batch].items():
            (pub / f"{name}.svg").write_text(fn(), encoding="utf-8")
            print("wrote", batch, name)
