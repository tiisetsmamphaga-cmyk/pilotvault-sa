"""Electrical-system explanation diagrams (ATG)."""
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
WIRE = "#334155"
OUT = REPO / "public/explanation-images/aircraft-technical-and-general"


def panel(x=40, y=142, w=710, h=444, hl=False):
    fill, stroke, sw = ("#fff8e1", GOLD, 4) if hl else ("#f8fafc", "#cbd5e1", 2)
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>\n'


def ans_badge(x, y):
    return f'<rect x="{x}" y="{y}" width="92" height="28" rx="14" fill="{GOLD}"/>\n' + t(x + 46, y + 19, "ANSWER", 14, 800, NAVY)


def wire(pts, col=WIRE, w=3, dash=None):
    return polyline(pts, col, w, dash=dash)


def earth(x, y, col=WIRE):
    s = line(x, y, x, y + 10, col, 3)
    for k, hw in enumerate((14, 9, 4)):
        s += line(x - hw, y + 10 + k * 6, x + hw, y + 10 + k * 6, col, 3)
    return s


def glow(x, y, w, h, on):
    if not on:
        return ""
    return f'<rect x="{x - 8}" y="{y - 8}" width="{w + 16}" height="{h + 16}" rx="12" fill="none" stroke="{GOLD}" stroke-width="5"/>\n'


def note(text2, x=60, y=172):
    s = ""
    for i, ln in enumerate(text2):
        s += t(x, y + i * 18, ln, 14, 800, GOLD_DARK, "start")
    return s


# =====================================================================
# magneto
# =====================================================================

MAG = {
    "magnet": ("MAGNETO: ROTATING MAGNET",
               [("ROTATING MAGNET", ["As the magnet turns, the flux", "through the soft-iron core", "keeps reversing."]),
                ("INDUCED CURRENT", ["The changing flux induces", "current in the primary coil."]),
                ("SELF-CONTAINED", ["No battery is needed: the", "magneto makes its own", "electricity."])],
               ("THE CURRENT IS CREATED BY", "THE ROTATING MAGNET"),
               "A magneto generates its electrical current from its rotating magnet."),
    "induction": ("HOW A MAGNETO MAKES HIGH VOLTAGE",
                  [("PRIMARY CURRENT", ["Current builds in the few", "turns of the primary coil."]),
                   ("POINTS OPEN", ["The primary circuit is broken:", "the magnetic flux collapses", "very rapidly."]),
                   ("SECONDARY WINDING", ["Thousands of turns: the fast", "flux change induces a very", "high voltage."])],
                  ("POINTS OPEN: FLUX COLLAPSES,", "HIGH VOLTAGE IN THE SECONDARY"),
                  "Opening the primary circuit rapidly changes the flux, inducing high voltage in the secondary."),
    "distributor": ("MAGNETO DISTRIBUTOR",
                    [("ROTOR ARM", ["Turns with the magneto and", "points to one plug lead", "at a time."]),
                     ("FIRING ORDER", ["Each plug gets its spark at", "the right point in its", "cylinder's cycle."]),
                     ("HIGH TENSION LEADS", ["Carry the high voltage from", "the distributor to the plugs."])],
                    ("ROUTES HIGH VOLTAGE TO EACH", "PLUG IN FIRING ORDER"),
                    "The distributor routes high voltage to each spark plug in the correct firing order."),
    "condenser": ("MAGNETO CONDENSER (CAPACITOR)",
                  [("ACROSS THE POINTS", ["Connected in parallel with", "the contact-breaker points."]),
                   ("ABSORBS THE SURGE", ["Stops current arcing across", "the points as they open."]),
                   ("RESULT", ["Faster flux collapse, a", "stronger spark and less", "burnt points."])],
                  ("PREVENTS ARCING ACROSS", "THE CONTACT-BREAKER POINTS"),
                  "The condenser prevents arcing across the contact-breaker points."),
    "impulse": ("IMPULSE COUPLING",
                [("SLOW CRANKING", ["At starting RPM the magnet", "turns too slowly for a", "good spark."]),
                 ("SPRING SNAPS", ["A spring winds up, then flicks", "the magnet round quickly:", "a strong spark."]),
                 ("RETARDED SPARK", ["Fires late (near TDC) so the", "engine cannot kick back."])],
                ("STRONG, RETARDED SPARK", "AT STARTING RPM"),
                "The impulse coupling produces a strong, retarded spark at the low RPM of engine start."),
    "pwire": ("BROKEN MAGNETO EARTH WIRE",
              [("SWITCH OFF = EARTHED", ["Ignition OFF earths the", "primary circuit through the", "P-lead: no sparks."]),
               ("P-LEAD BROKEN", ["The magneto can no longer", "be earthed: it stays live."]),
               ("DANGER", ["Engine keeps running with", "the switch OFF; treat every", "propeller as live."])],
              ("P-LEAD BROKEN: THE MAGNETO", "CANNOT BE SWITCHED OFF"),
              "If the magneto earth wire is broken, the engine cannot be stopped by switching off the ignition."),
}


def magneto(answer):
    title, facts, nt, foot = MAG[answer]
    s = header(title)
    s += panel(hl=True)
    s += note(nt)
    # drive + impulse coupling
    s += line(50, 420, 130, 420, "#64748b", 12)
    s += t(60, 452, "ENGINE", 12, 800, MUTED, "start")
    s += t(60, 468, "DRIVE", 12, 800, MUTED, "start")
    s += f'<rect x="72" y="400" width="40" height="40" rx="6" fill="#e2e8f0" stroke="{INK}" stroke-width="2.5"/>\n'
    for k in range(4):
        s += line(78 + k * 9, 406, 84 + k * 9, 434, "#475569", 2)
    s += glow(72, 400, 40, 40, answer == "impulse")
    s += t(92, 388, "IMPULSE COUPLING", 11, 800, GOLD_DARK if answer == "impulse" else MUTED)
    # rotating magnet
    mx, my = 180, 420
    s += f'<path d="M {mx - 44},{my} A 44 44 0 0 1 {mx + 44},{my} Z" fill="#ef4444" stroke="{INK}" stroke-width="2.5"/>\n'
    s += f'<path d="M {mx - 44},{my} A 44 44 0 0 0 {mx + 44},{my} Z" fill="#3b82f6" stroke="{INK}" stroke-width="2.5"/>\n'
    s += t(mx, my - 14, "N", 16, 800, "#ffffff")
    s += t(mx, my + 28, "S", 16, 800, "#ffffff")
    s += f'<path d="M {mx + 40},{my - 50} A 64 64 0 0 1 {mx + 62},{my + 10}" fill="none" stroke="{INK}" stroke-width="3" marker-end="url(#aDark)"/>\n'
    s += glow(mx - 44, my - 44, 88, 88, answer == "magnet")
    s += t(mx, my + 70, "ROTATING MAGNET", 12, 800, GOLD_DARK if answer == "magnet" else INK)
    # soft iron core and coils
    s += polyline([(mx, my - 44), (mx, 250), (430, 250)], "#94a3b8", 14)
    for k in range(5):
        x = 236 + k * 10
        s += f'<ellipse cx="{x}" cy="250" rx="5" ry="16" fill="none" stroke="#b45309" stroke-width="4"/>\n'
    for k in range(14):
        x = 300 + k * 8
        s += f'<ellipse cx="{x}" cy="250" rx="3" ry="22" fill="none" stroke="#1d4ed8" stroke-width="2"/>\n'
    coil_hl = answer == "induction"
    s += glow(222, 222, 196, 56, coil_hl)
    s += t(256, 212, "PRIMARY", 11, 800, "#b45309")
    s += t(352, 212, "SECONDARY", 11, 800, "#1d4ed8")
    # primary circuit: coil -> points -> earth, condenser across
    s += wire([(236, 272), (236, 470), (262, 470)])
    s += line(262, 470, 300, 458, INK, 4) if answer == "induction" else line(262, 470, 302, 470, INK, 4)
    s += wire([(304, 470), (330, 470), (330, 500)])
    s += earth(330, 500)
    s += f'<ellipse cx="282" cy="500" rx="14" ry="9" fill="#cbd5e1" stroke="{INK}" stroke-width="2"/>\n'
    s += polyline([(mx + 30, my + 30), (268, 500)], "#94a3b8", 2, dash="4 4")
    s += glow(254, 452, 54, 58, coil_hl)
    s += t(282, 540, "CONTACT-BREAKER", 11, 800, GOLD_DARK if coil_hl else INK)
    s += t(282, 554, "POINTS AND CAM", 11, 800, GOLD_DARK if coil_hl else INK)
    cond_hl = answer == "condenser"
    s += wire([(236, 430), (390, 430), (390, 456)])
    s += line(374, 456, 406, 456, INK, 4)
    s += line(374, 466, 406, 466, INK, 4)
    s += wire([(390, 466), (390, 500)])
    s += earth(390, 500)
    s += glow(366, 444, 48, 30, cond_hl)
    s += t(420, 466, "CONDENSER", 11, 800, GOLD_DARK if cond_hl else INK, "start")
    # P-lead and ignition switch
    p_hl = answer == "pwire"
    s += wire([(236, 330), (120, 330), (120, 300)], RED if p_hl else WIRE, 3, dash="8 5" if p_hl else None)
    if p_hl:
        s += f'<path d="M 162,318 l 12,24 M 174,318 l -12,24" stroke="{RED}" stroke-width="4"/>\n'
    s += f'<circle cx="120" cy="300" r="5" fill="{INK}"/>\n'
    s += line(120, 300, 98, 272, INK, 4)
    s += f'<circle cx="98" cy="270" r="4" fill="{INK}"/>\n'
    s += earth(98, 274)
    s += glow(80, 262, 60, 76, p_hl)
    s += t(150, 318, "P-LEAD", 11, 800, RED if p_hl else INK, "start") if not p_hl else t(180, 312, "P-LEAD BROKEN", 11, 800, RED, "start")
    s += t(60, 236, "IGNITION SWITCH", 11, 800, GOLD_DARK if p_hl else INK, "start")
    # secondary to distributor and plugs
    d_hl = answer == "distributor"
    s += wire([(412, 250), (500, 250), (500, 300)], "#1d4ed8", 3)
    dx, dy = 540, 340
    s += f'<circle cx="{dx}" cy="{dy}" r="42" fill="#e2e8f0" stroke="{INK}" stroke-width="3"/>\n'
    s += line(dx, dy, dx + 26, dy - 26, INK, 6)
    s += f'<circle cx="{dx}" cy="{dy}" r="6" fill="{INK}"/>\n'
    s += glow(dx - 42, dy - 42, 84, 84, d_hl)
    s += t(dx, dy + 66, "DISTRIBUTOR", 12, 800, GOLD_DARK if d_hl else INK)
    s += wire([(500, 300), (dx - 6, dy - 2)], "#1d4ed8", 2)
    plugs = [(690, 230), (690, 300), (690, 370), (690, 440)]
    for k, (px, py) in enumerate(plugs):
        a = math.radians(60 - k * 40)
        ex, ey = dx + 42 * math.cos(a), dy - 42 * math.sin(a)
        s += wire([(ex, ey), (620, py), (670, py)], "#1d4ed8", 2.5)
        s += f'<rect x="670" y="{py - 8}" width="30" height="16" rx="3" fill="#94a3b8" stroke="{INK}" stroke-width="2"/>\n'
        s += line(700, py, 712, py, INK, 3)
        spark = answer in ("distributor", "induction") and k == 0
        if spark:
            for aa in range(0, 360, 60):
                r = math.radians(aa)
                s += line(716 + 3 * math.cos(r), py + 3 * math.sin(r), 716 + 10 * math.cos(r), py + 10 * math.sin(r), "#eab308", 2.5)
    s += t(690, 208, "SPARK PLUGS", 11, 800, INK)
    s += g.fact_column(facts)
    s += footer(foot)
    return s


def low_tension():
    s = header("LOW-TENSION IGNITION: TRANSFORMER")
    s += panel(hl=True)
    s += f'<rect x="70" y="300" width="130" height="110" rx="12" fill="#e2e8f0" stroke="{INK}" stroke-width="3"/>\n'
    s += t(135, 350, "LOW-TENSION", 12, 800, INK)
    s += t(135, 368, "MAGNETO", 12, 800, INK)
    ys = (220, 330, 440)
    for y in ys:
        s += wire([(200, 355), (260, 355), (260, y), (410, y)], "#b45309", 3)
        s += f'<rect x="410" y="{y - 26}" width="90" height="52" rx="8" fill="#fde68a" stroke="{GOLD}" stroke-width="4"/>\n'
        s += t(455, y + 5, "TRANSFORMER", 10, 800, INK)
        s += wire([(500, y), (600, y)], "#1d4ed8", 5)
        s += f'<rect x="600" y="{y - 10}" width="40" height="20" rx="3" fill="#94a3b8" stroke="{INK}" stroke-width="2"/>\n'
        s += t(660, y + 5, "PLUG", 12, 800, INK, "start")
    s += t(330, 190, "LOW VOLTAGE", 13, 800, "#b45309")
    s += t(330, 206, "(LONG LEADS)", 12, 800, "#b45309")
    s += t(550, 190, "HIGH VOLTAGE", 13, 800, "#1d4ed8")
    s += t(550, 206, "(SHORT LEADS)", 12, 800, "#1d4ed8")
    s += t(395, 540, "Each transformer steps the low voltage up to a high voltage close to its plug.", 14, 400, BODY)
    s += g.fact_column([
        ("LOW VOLTAGE HARNESS", ["The magneto sends low", "voltage along the long", "ignition leads."]),
        ("TRANSFORMER AT THE PLUG", ["Steps it up to the high", "voltage needed for the spark."]),
        ("WHY", ["Less risk of flash-over and", "leakage at altitude."]),
    ])
    s += footer("In a low-tension system a transformer steps the low voltage up to a high voltage for the plug.")
    return s


def diode(x, y, col=INK):
    s = f'<path d="M {x - 10},{y - 10} L {x - 10},{y + 10} L {x + 8},{y} Z" fill="{col}"/>\n'
    s += line(x + 9, y - 11, x + 9, y + 11, col, 3)
    return s


def battery_sym(x, y, label="BATTERY", hl=False):
    s = ""
    for k in range(3):
        s += line(x - 18 + k * 14, y - 18, x - 18 + k * 14, y + 18, INK, 4)
        s += line(x - 11 + k * 14, y - 9, x - 11 + k * 14, y + 9, INK, 4)
    s += glow(x - 26, y - 26, 58, 52, hl)
    s += t(x + 4, y + 44, label, 12, 800, GOLD_DARK if hl else INK)
    return s


def bus(x0, x1, y, label="BUS BAR"):
    s = line(x0, y, x1, y, INK, 8)
    s += t(x1 + 6, y + 5, label, 12, 800, INK, "start")
    return s


# =====================================================================
# alternator (q2573/2597/2610 rectifier, 2600 reverse current, 2585 stator, 2580/2589 low RPM, 2614 purpose)
# =====================================================================

ALT = {
    "rectifier": ("ALTERNATOR RECTIFIER",
                  [("AC IS GENERATED", ["The alternator's stator", "produces alternating current."]),
                   ("DIODES RECTIFY IT", ["A bridge of diodes (the", "rectifier) converts the", "AC output to DC."]),
                   ("DC TO THE BUS", ["The aircraft system and", "battery need direct current."])],
                  ("DIODES (RECTIFIER) CONVERT", "THE AC OUTPUT TO DC"),
                  "The alternator's AC output is converted to DC by rectifier diodes."),
    "reverse": ("ALTERNATOR: NO REVERSE CURRENT",
                [("DIODES ARE ONE-WAY", ["Current can flow out of the", "alternator but not back in."]),
                 ("NO CUT-OUT NEEDED", ["Unlike a DC generator, no", "reverse-current relay is", "required."]),
                 ("BATTERY PROTECTED", ["The battery cannot discharge", "through a stopped alternator."])],
                ("RECTIFIER DIODES BLOCK", "CURRENT FROM THE BATTERY"),
                "Reverse current from the battery to the alternator is prevented by the rectifier diodes."),
    "stator": ("ALTERNATOR STATOR AND ROTOR",
               [("STATOR", ["The output windings in the", "casing: they remain", "stationary."]),
                ("ROTOR", ["The field winding spins,", "fed through slip rings.", "Needs battery power."]),
                ("NO COMMUTATOR", ["Output is taken from fixed", "windings, so no heavy", "brushes carry the load."])],
               ("THE STATOR REMAINS", "STATIONARY"),
               "In an alternator the stator remains stationary; the rotor (field) turns."),
    "purpose": ("PURPOSE OF THE ALTERNATOR",
                [("SUPPLIES THE SYSTEM", ["Powers the electrical loads", "while the engine runs."]),
                 ("CHARGES THE BATTERY", ["Keeps the battery topped up", "for starting and emergencies."]),
                 ("IF IT FAILS", ["The battery alone supplies", "the loads, for a limited", "time."])],
                ("SUPPLIES THE SYSTEM AND", "RECHARGES THE BATTERY"),
                "The alternator supplies the aircraft electrical system and recharges the battery."),
}


def alternator(answer):
    title, facts, nt, foot = ALT[answer]
    s = header(title)
    s += panel(hl=True)
    s += note(nt)
    # alternator body
    cx, cy = 180, 360
    stat_hl = answer == "stator"
    s += f'<circle cx="{cx}" cy="{cy}" r="92" fill="#e2e8f0" stroke="{GOLD if stat_hl else INK}" stroke-width="{6 if stat_hl else 3}"/>\n'
    for k in range(12):
        a = math.radians(k * 30)
        s += f'<rect x="{cx + 70 * math.cos(a) - 8:.1f}" y="{cy + 70 * math.sin(a) - 8:.1f}" width="16" height="16" fill="#b45309" transform="rotate({k * 30} {cx + 70 * math.cos(a):.1f} {cy + 70 * math.sin(a):.1f})"/>\n'
    s += f'<circle cx="{cx}" cy="{cy}" r="44" fill="#94a3b8" stroke="{INK}" stroke-width="3"/>\n'
    s += f'<path d="M {cx - 44},{cy} A 44 44 0 0 1 {cx + 44},{cy} Z" fill="#ef4444" fill-opacity="0.7"/>\n'
    s += f'<path d="M {cx + 50},{cy - 30} A 58 58 0 0 1 {cx + 50},{cy + 30}" fill="none" stroke="{INK}" stroke-width="3" marker-end="url(#aDark)"/>\n'
    s += t(cx, cy + 5, "ROTOR", 12, 800, "#ffffff")
    s += t(cx, cy + 118, "STATOR (FIXED)" if stat_hl else "ALTERNATOR", 13, 800, GOLD_DARK if stat_hl else INK)
    if stat_hl:
        s += t(cx, cy - 104, "STATOR WINDINGS", 12, 800, "#b45309")
    # AC output
    s += f'<path d="M 280,{cy} q 12,-24 24,0 t 24,0 t 24,0" fill="none" stroke="#b45309" stroke-width="3"/>\n'
    s += t(316, cy - 26, "AC", 13, 800, "#b45309")
    # rectifier
    rec_hl = answer in ("rectifier", "reverse")
    s += f'<rect x="370" y="{cy - 50}" width="100" height="100" rx="8" fill="#ffffff" stroke="{GOLD if rec_hl else INK}" stroke-width="{5 if rec_hl else 2.5}"/>\n'
    for dy in (-24, 0, 24):
        s += diode(420, cy + dy, GOLD_DARK if rec_hl else INK)
    s += t(420, cy + 74, "RECTIFIER DIODES", 12, 800, GOLD_DARK if rec_hl else INK)
    s += wire([(470, cy), (560, cy), (560, 250)])
    s += t(515, cy - 10, "DC", 13, 800, GREEN)
    s += bus(500, 640, 250)
    # loads and battery
    s += wire([(600, 250), (600, 200)])
    s += f'<circle cx="600" cy="186" r="14" fill="#fde68a" stroke="{INK}" stroke-width="2"/>\n'
    s += t(624, 192, "LOADS", 12, 800, INK, "start")
    s += wire([(520, 250), (520, 440), (560, 440)])
    s += battery_sym(600, 440, "BATTERY", hl=answer == "purpose")
    if answer == "purpose":
        s += line(540, 300, 540, 410, GREEN, 4, "aDark")
        s += t(548, 380, "CHARGE", 12, 800, GREEN, "start")
        s += line(600, 236, 600, 212, GREEN, 4, "aDark")
    if answer == "reverse":
        s += line(500, cy + 30, 450, cy + 30, RED, 4, "aRedS")
        s += f'<path d="M 440,{cy + 20} l 14,20 M 454,{cy + 20} l -14,20" stroke="{RED}" stroke-width="4"/>\n'
        s += t(500, cy + 56, "REVERSE CURRENT BLOCKED", 12, 800, RED)
    s += g.fact_column(facts)
    s += footer(foot)
    return s


def alt_vs_gen():
    s = header("ALTERNATOR VS GENERATOR AT LOW RPM")
    s += panel(hl=True)
    ox, oy, w, h = 110, 520, 560, 300
    s += line(ox, oy, ox + w, oy, INK, 2.5, "aDark")
    s += line(ox, oy, ox, oy - h, INK, 2.5, "aDark")
    s += t(ox + w, oy + 28, "ENGINE RPM", 13, 800, INK, "end")
    s += f'<text x="{ox - 22}" y="{oy - h / 2}" text-anchor="middle" font-family="{g.F}" font-size="13" font-weight="800" fill="{INK}" transform="rotate(-90 {ox - 22} {oy - h / 2})">ELECTRICAL OUTPUT</text>\n'
    idle = ox + 0.22 * w
    s += line(idle, oy, idle, oy - h, "#94a3b8", 2, dash="6 5")
    s += t(idle, oy + 28, "IDLE / TAXI", 12, 800, MUTED)
    alt = [(ox + k / 50 * w, oy - h * 0.85 * (1 - math.exp(-k / 8))) for k in range(51)]
    gen = [(ox + k / 50 * w, oy - (0 if k < 14 else h * 0.8 * (1 - math.exp(-(k - 14) / 10)))) for k in range(51)]
    s += polyline(alt, GREEN, 5)
    s += polyline(gen, RED, 5)
    s += t(ox + 0.5 * w, oy - h * 0.92, "ALTERNATOR", 15, 800, GREEN)
    s += t(ox + 0.62 * w, oy - h * 0.38, "DC GENERATOR", 15, 800, RED)
    s += t(idle + 10, oy - h * 0.45, "Alternator already", 13, 700, GREEN, "start")
    s += t(idle + 10, oy - h * 0.45 + 16, "charging at idle", 13, 700, GREEN, "start")
    s += g.fact_column([
        ("ALTERNATOR", ["Produces useful power even", "at low RPM, e.g. taxiing."]),
        ("DC GENERATOR", ["Output is low until the", "engine RPM is higher."]),
        ("ALSO", ["Lighter for its output and", "no heavy commutator."]),
    ])
    s += footer("An alternator gives more output at low RPM than a generator and still charges at idle.")
    return s


# =====================================================================
# DC generator (q2578 commutator, 2572/2594 regulator, 2568 cut-out, 2599 self-excited)
# =====================================================================

GEN = {
    "commutator": ("DC GENERATOR COMMUTATOR",
                   [("AC IN THE ARMATURE", ["The rotating armature coils", "generate alternating current."]),
                    ("COMMUTATOR", ["Split copper segments reverse", "the connection every half", "turn."]),
                    ("DC OUT", ["The brushes pick off current", "that always flows one way."])],
                   ("THE COMMUTATOR CONVERTS", "THE AC OUTPUT TO DC"),
                   "In a DC generator the AC produced in the armature is converted to DC by the commutator."),
    "regulator": ("VOLTAGE REGULATOR",
                  [("CONTROLS FIELD CURRENT", ["Varies the current in the", "generator's field winding."]),
                   ("STEADY VOLTAGE", ["Keeps output voltage constant", "as RPM and load change."]),
                   ("PROTECTS", ["Stops over-voltage damaging", "the battery and equipment."])],
                  ("THE VOLTAGE REGULATOR", "CONTROLS THE OUTPUT VOLTAGE"),
                  "The voltage regulator controls the voltage output from a DC generator."),
    "cutout": ("REVERSE-CURRENT CUT-OUT",
               [("GENERATOR SLOW OR STOPPED", ["Its voltage falls below the", "battery voltage."]),
                ("CUT-OUT OPENS", ["The relay disconnects the", "generator from the bus."]),
                ("RESULT", ["The battery cannot discharge", "back through the generator."])],
               ("PREVENTS CURRENT FLOWING FROM", "THE BATTERY TO THE GENERATOR"),
               "A reverse-current cut-out stops current flowing from the battery to the generator."),
    "selfexc": ("DC GENERATOR: SELF-EXCITED",
                [("RESIDUAL MAGNETISM", ["The field poles keep a little", "magnetism when stopped."]),
                 ("BUILDS UP ITSELF", ["As it turns, its own output", "feeds the field and output", "rises."]),
                 ("NO BATTERY NEEDED", ["It can come on line without", "battery power (unlike an", "alternator)."])],
                ("SELF-EXCITED: NO BATTERY", "NEEDED TO COME ON LINE"),
                "A DC generator is self-excited and does not need battery power to come on line."),
}


def generator(answer):
    title, facts, nt, foot = GEN[answer]
    s = header(title)
    s += panel(hl=True)
    s += note(nt)
    cx, cy = 180, 370
    s += f'<rect x="{cx - 110}" y="{cy - 90}" width="36" height="180" rx="6" fill="#ef4444" stroke="{INK}" stroke-width="2.5"/>\n'
    s += f'<rect x="{cx + 74}" y="{cy - 90}" width="36" height="180" rx="6" fill="#3b82f6" stroke="{INK}" stroke-width="2.5"/>\n'
    s += t(cx - 92, cy + 6, "N", 18, 800, "#ffffff")
    s += t(cx + 92, cy + 6, "S", 18, 800, "#ffffff")
    fhl = answer in ("regulator", "selfexc")
    for k in range(6):
        s += f'<ellipse cx="{cx - 92}" cy="{cy - 70 + k * 28}" rx="24" ry="5" fill="none" stroke="{GOLD_DARK if fhl else "#b45309"}" stroke-width="3"/>\n'
    s += t(cx - 92, cy - 104, "FIELD WINDING", 11, 800, GOLD_DARK if fhl else "#b45309")
    s += f'<rect x="{cx - 40}" y="{cy - 50}" width="80" height="100" rx="10" fill="none" stroke="#b45309" stroke-width="4"/>\n'
    s += t(cx, cy + 5, "ARMATURE", 11, 800, INK)
    s += f'<path d="M {cx - 20},{cy - 64} A 30 30 0 0 1 {cx + 24},{cy - 60}" fill="none" stroke="{INK}" stroke-width="3" marker-end="url(#aDark)"/>\n'
    # commutator
    com = answer == "commutator"
    kx, ky = cx, cy + 128
    s += f'<path d="M {kx - 26},{ky} A 26 26 0 0 1 {kx + 26},{ky} L {kx + 22},{ky} A 22 22 0 0 0 {kx - 22},{ky} Z" fill="#d97706" stroke="{INK}" stroke-width="2"/>\n'
    s += f'<path d="M {kx - 26},{ky + 4} A 26 26 0 0 0 {kx + 26},{ky + 4} L {kx + 22},{ky + 4} A 22 22 0 0 1 {kx - 22},{ky + 4} Z" fill="#d97706" stroke="{INK}" stroke-width="2"/>\n'
    s += line(cx, cy + 50, kx, ky - 26, "#b45309", 3)
    s += f'<rect x="{kx - 48}" y="{ky - 6}" width="18" height="16" fill="#1f2937"/>\n'
    s += f'<rect x="{kx + 30}" y="{ky - 6}" width="18" height="16" fill="#1f2937"/>\n'
    s += glow(kx - 54, ky - 32, 108, 62, com)
    s += t(kx, ky + 50, "COMMUTATOR + BRUSHES", 11, 800, GOLD_DARK if com else INK)
    # output to regulator / cut-out to bus
    s += wire([(kx + 48, ky + 2), (340, ky + 2), (340, 300)])
    reg = answer == "regulator"
    s += f'<rect x="300" y="240" width="90" height="60" rx="8" fill="#ffffff" stroke="{GOLD if reg else INK}" stroke-width="{5 if reg else 2.5}"/>\n'
    s += t(345, 266, "VOLTAGE", 11, 800, INK)
    s += t(345, 282, "REGULATOR", 11, 800, INK)
    s += wire([(300, 270), (cx - 92, 270), (cx - 92, cy - 90)], GOLD_DARK if reg else "#b45309", 2.5, dash="6 4")
    s += t(236, 262, "FIELD CONTROL", 10, 800, GOLD_DARK if reg else MUTED)
    cut = answer == "cutout"
    s += wire([(390, 270), (440, 270)])
    s += f'<rect x="440" y="240" width="80" height="60" rx="8" fill="#ffffff" stroke="{GOLD if cut else INK}" stroke-width="{5 if cut else 2.5}"/>\n'
    s += line(456, 282, 500, 262 if cut else 282, INK, 4)
    s += t(480, 316, "CUT-OUT", 11, 800, GOLD_DARK if cut else INK)
    s += wire([(520, 270), (580, 270), (580, 220)])
    s += bus(540, 660, 220)
    s += wire([(620, 220), (620, 400)])
    s += battery_sym(620, 430)
    if cut:
        s += line(560, 336, 470, 336, RED, 4, "aRedS")
        s += f'<path d="M 450,326 l 14,20 M 464,326 l -14,20" stroke="{RED}" stroke-width="4"/>\n'
        s += t(505, 364, "BATTERY CURRENT BLOCKED", 11, 800, RED)
    if answer == "selfexc":
        s += t(cx, cy - 128, "RESIDUAL MAGNETISM", 12, 800, GOLD_DARK)
    s += g.fact_column(facts)
    s += footer(foot)
    return s


# =====================================================================
# battery (Ah ratings, electrolyte, cells)
# =====================================================================

def battery_ah(cap, amps, hours, qfoot):
    s = header("BATTERY CAPACITY: AMPERE-HOURS")
    s += panel(hl=True)
    s += f'<rect x="90" y="230" width="220" height="150" rx="12" fill="#1f2937" stroke="{INK}" stroke-width="3"/>\n'
    s += f'<rect x="120" y="212" width="30" height="18" fill="#94a3b8"/>\n<rect x="250" y="212" width="30" height="18" fill="#94a3b8"/>\n'
    s += t(200, 318, f"{cap} Ah", 34, 800, GOLD)
    s += t(420, 276, "CAPACITY", 15, 800, INK, "start")
    s += t(420, 300, "= CURRENT × TIME", 18, 800, GOLD_DARK, "start")
    s += t(420, 344, f"{cap} Ah = {amps} A × {hours} h", 22, 800, INK, "start")
    rows = [(cap, 1), (cap // 2, 2), (cap // 4, 4), (cap // 10 if cap >= 20 else cap // 5, 10 if cap >= 20 else 5)]
    s += t(90, 430, "SAME CAPACITY, DIFFERENT RATES (THEORETICAL)", 14, 800, INK, "start")
    for i, (a, h) in enumerate(rows):
        x = 90 + i * 160
        hl = a == amps and h == hours
        s += f'<rect x="{x}" y="446" width="148" height="70" rx="10" fill="{"#fde68a" if hl else "#ffffff"}" stroke="{GOLD if hl else "#cbd5e1"}" stroke-width="{4 if hl else 2}"/>\n'
        s += t(x + 74, 476, f"{a} A", 18, 800, INK)
        s += t(x + 74, 500, f"for {h} h", 15, 400, BODY)
    s += t(395, 556, "Real batteries deliver less at high discharge rates and in the cold.", 14, 400, BODY)
    s += g.fact_column([
        ("AMPERE-HOURS", ["Battery capacity is stated", "in ampere-hours (Ah)."]),
        ("AMPS × HOURS", ["Current multiplied by the time", "it can be supplied."]),
        ("THEORETICAL", ["Actual capacity falls with", "age, cold and heavy loads."]),
    ])
    s += footer(qfoot)
    return s


def battery_cells(answer):
    title = "LEAD-ACID BATTERY ELECTROLYTE" if answer == "electrolyte" else "LEAD-ACID BATTERY CELLS"
    s = header(title)
    s += panel(hl=True)
    n = 12
    for k in range(n):
        x = 80 + k * 52
        s += f'<rect x="{x}" y="250" width="44" height="130" rx="4" fill="#ffffff" stroke="{INK}" stroke-width="2.5"/>\n'
        s += f'<rect x="{x + 3}" y="290" width="38" height="87" fill="#93c5fd" fill-opacity="0.8"/>\n'
        s += line(x + 14, 264, x + 14, 370, "#475569", 5)
        s += line(x + 30, 264, x + 30, 370, "#7f1d1d", 5)
        s += t(x + 22, 400, "2 V", 12, 800, INK)
    s += t(395, 232, "12 CELLS × 2 V = 24 V", 22, 800, GOLD_DARK if answer == "cells" else INK)
    s += t(395, 440, "(a 12 V battery has 6 cells)", 14, 400, BODY)
    s += t(395, 486, "ELECTROLYTE: SULPHURIC ACID + DISTILLED (PURE) WATER", 15, 800, GOLD_DARK if answer == "electrolyte" else INK)
    s += t(395, 516, "Top up the level with distilled water only.", 15, 400, BODY)
    s += t(395, 540, "Never add acid unless spilt electrolyte is being replaced.", 14, 400, BODY)
    s += g.fact_column([
        ("2 VOLTS PER CELL", ["Each lead-acid cell gives", "about 2 V, so 24 V needs", "12 cells."]),
        ("ELECTROLYTE", ["Dilute sulphuric acid: acid", "mixed with pure water."]),
        ("TOPPING UP", ["Water is lost in charging:", "replace it with distilled", "water."]),
    ])
    foot = ("A lead-acid battery's electrolyte is sulphuric acid and pure water; top up with distilled water."
            if answer == "electrolyte" else "A 24-volt lead-acid battery has twelve 2-volt cells.")
    s += footer(foot)
    return s


# =====================================================================
# circuit protection (fuses, circuit breakers)
# =====================================================================

def protection(answer):
    title = "BLOWN FUSE" if answer == "fuse" else "TRIPPED CIRCUIT BREAKER"
    s = header(title)
    for i, (key, head) in enumerate((("fuse", "FUSE"), ("cb", "CIRCUIT BREAKER"))):
        px = 48 + i * 362
        ans = key == answer
        s += panel(px, 142, 346, 444, hl=ans)
        s += t(px + 20, 176, head, 20, 800, INK, "start")
        if ans:
            s += ans_badge(px + 238, 158)
        cx = px + 173
        if key == "fuse":
            s += f'<rect x="{cx - 80}" y="226" width="160" height="50" rx="24" fill="#e0f2fe" stroke="{INK}" stroke-width="3"/>\n'
            s += f'<rect x="{cx - 96}" y="232" width="20" height="38" rx="4" fill="#94a3b8" stroke="{INK}" stroke-width="2"/>\n'
            s += f'<rect x="{cx + 76}" y="232" width="20" height="38" rx="4" fill="#94a3b8" stroke="{INK}" stroke-width="2"/>\n'
            s += polyline([(cx - 76, 251), (cx - 14, 251)], "#475569", 3)
            s += polyline([(cx + 14, 251), (cx + 76, 251)], "#475569", 3)
            s += t(cx, 300, "5 A", 18, 800, INK)
            lines_ = [("Rated in AMPERES", True), ("Replace ONCE only", True), ("with the SAME rating", True), ("Blows again: leave it", False), ("out - there is a fault", False)]
        else:
            s += f'<rect x="{cx - 34}" y="214" width="68" height="44" rx="8" fill="#1f2937" stroke="{INK}" stroke-width="3"/>\n'
            s += f'<rect x="{cx - 16}" y="190" width="32" height="26" rx="4" fill="#e2e8f0" stroke="{INK}" stroke-width="2"/>\n'
            s += f'<rect x="{cx - 16}" y="190" width="32" height="8" fill="#ffffff"/>\n'
            s += t(cx, 242, "5", 16, 800, "#ffffff")
            s += t(cx, 290, "POPPED OUT = TRIPPED", 14, 800, RED)
            lines_ = [("Allow it to COOL first", True), ("Reset ONCE only", True), ("Trips again: leave it", False), ("out - there is a fault", False), ("Never hold it in", False)]
        for j, (ln, b) in enumerate(lines_):
            s += t(px + 30, 350 + j * 36, ln, 17, 800 if b else 400, INK if b else BODY, "start")
    s += f'<rect x="770" y="146" width="378" height="438" rx="12" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2"/>\n'
    s += t(790, 184, "WHY ONLY ONCE?", 18, 800, INK, "start")
    for j, ln in enumerate(["A fuse or breaker opens to", "protect the wiring from", "overheating.", "", "Repeated resetting of a", "genuine fault can start", "an electrical fire.", "", "Never fit a higher-rated", "fuse."]):
        if ln:
            s += t(790, 222 + j * 26, ln, 16, 400, BODY, "start")
    foot = ("A blown fuse may be replaced only once, with a fuse of the same value (rated in amperes)."
            if answer == "fuse" else "A tripped circuit breaker should be reset only once, after a cooling-off period.")
    s += footer(foot)
    return s


# =====================================================================
# meters: ammeter / voltmeter / left-zero / centre-zero
# =====================================================================

def meter_face(cx, cy, lo, hi, needle, zero_label, title, marks):
    s = f'<rect x="{cx - 120}" y="{cy - 100}" width="240" height="170" rx="14" fill="#1f2937" stroke="{INK}" stroke-width="3"/>\n'
    R = 84

    def pt(v, r):
        a = math.radians(150 - (v - lo) / (hi - lo) * 120)
        return cx + r * math.cos(a), cy + 40 - r * math.sin(a)

    a0, a1 = pt(lo, R), pt(hi, R)
    s += f'<path d="M {a0[0]:.1f} {a0[1]:.1f} A {R} {R} 0 0 1 {a1[0]:.1f} {a1[1]:.1f}" fill="none" stroke="#e2e8f0" stroke-width="3"/>\n'
    for v, lab in marks:
        p, q = pt(v, R - 8), pt(v, R + 6)
        s += line(p[0], p[1], q[0], q[1], "#e2e8f0", 2)
        r = pt(v, R - 26)
        s += t(r[0], r[1] + 5, lab, 13, 800, "#e2e8f0")
    n = pt(needle, R - 6)
    s += line(cx, cy + 40, n[0], n[1], "#f8fafc", 4)
    s += f'<circle cx="{cx}" cy="{cy + 40}" r="6" fill="#f8fafc"/>\n'
    s += t(cx, cy + 58, title, 13, 800, "#e2e8f0")
    return s


METERS = {
    "ammeter": ("AMMETER: CURRENT FLOW", "An ammeter measures electrical current flow (amperes)."),
    "voltmeter": ("VOLTMETER: SYSTEM VOLTAGE", "A voltmeter indicates the electrical system voltage."),
    "leftzero": ("LEFT-ZERO AMMETER (LOADMETER)", "A left-zero ammeter shows the alternator or generator output current only."),
    "centrezero": ("CENTRE-ZERO AMMETER", "On a centre-zero ammeter, positive (charging) indications are right of centre."),
}


def meters(answer):
    title, foot = METERS[answer]
    s = header(title)
    items = [
        ("ammeter", 190, 300, -60, 60, 20, "0", "AMPS", [(-60, "-60"), (0, "0"), (60, "+60")], "CURRENT (AMPERES)"),
        ("voltmeter", 520, 300, 0, 32, 28, "", "VOLTS", [(0, "0"), (16, "16"), (32, "32")], "SYSTEM VOLTAGE"),
    ]
    if answer in ("leftzero", "centrezero"):
        items = [
            ("leftzero", 190, 300, 0, 60, 24, "", "LOAD", [(0, "0"), (30, "30"), (60, "60")], "ALTERNATOR OUTPUT ONLY"),
            ("centrezero", 520, 300, -60, 60, 22, "", "AMPS", [(-60, "−"), (0, "0"), (60, "+")], "BATTERY CHARGE / DISCHARGE"),
        ]
    for key, cx, cy, lo, hi, nd, _, ttl, marks, sub in items:
        ans = key == answer
        s += panel(cx - 145, 142, 290, 444, hl=ans)
        if ans:
            s += ans_badge(cx + 44, 156)
        s += meter_face(cx, cy, lo, hi, nd, "", ttl, marks)
        s += t(cx, 430, sub, 14, 800, GOLD_DARK if ans else INK)
    if answer in ("leftzero", "centrezero"):
        s += t(190, 470, "Needle only moves right of", 14, 400, BODY)
        s += t(190, 490, "zero: shows the load taken", 14, 400, BODY)
        s += t(190, 510, "from the alternator.", 14, 400, BODY)
        s += t(520, 470, "RIGHT of centre (+): charging", 14, 800, GREEN)
        s += t(520, 494, "LEFT of centre (−): battery", 14, 800, RED)
        s += t(520, 512, "discharging", 14, 800, RED)
        facts = [("LEFT-ZERO", ["Reads alternator/generator", "output only (a loadmeter)."]),
                 ("CENTRE-ZERO", ["In the battery circuit: shows", "charge (+) or discharge (−)."]),
                 ("IN FLIGHT", ["Normal: small charge after", "start, settling near zero."])]
    else:
        s += t(190, 470, "Measures CURRENT", 15, 800, INK)
        s += t(190, 492, "in amperes (A)", 14, 400, BODY)
        s += t(520, 470, "Measures VOLTAGE", 15, 800, INK)
        s += t(520, 492, "in volts (V)", 14, 400, BODY)
        facts = [("AMMETER", ["Measures electrical current", "flow, in amperes."]),
                 ("VOLTMETER", ["Indicates the electrical", "system voltage."]),
                 ("TOGETHER", ["Show whether the alternator", "is charging and the system", "is healthy."])]
    s += g.fact_column(facts)
    s += footer(foot)
    return s


# =====================================================================
# components: capacitor, resistor, inverter, CSD
# =====================================================================

COMP = {
    "capacitor": ("CAPACITOR", "A capacitor stores an electrical charge.",
                  [("TWO PLATES", ["Conductors separated by an", "insulator (dielectric)."]),
                   ("STORES CHARGE", ["Charge builds on the plates", "when a voltage is applied."]),
                   ("RELEASES IT", ["Can give the charge back", "quickly, e.g. to smooth or", "suppress surges."])]),
    "resistor": ("RESISTOR", "Resistors oppose current flow, dropping (varying) the voltage in a circuit.",
                 [("OPPOSES CURRENT", ["Resistance is measured in", "ohms."]),
                  ("DROPS VOLTAGE", ["Voltage falls across it, so it", "can set or vary the voltage", "a component receives."]),
                  ("OHM'S LAW", ["V = I × R"])]),
    "inverter": ("INVERTER: DC TO AC", "An inverter converts direct current (DC) into alternating current (AC).",
                 [("DC IN", ["From the aircraft's DC bus", "(battery / alternator)."]),
                  ("AC OUT", ["For instruments or avionics", "that need alternating", "current."]),
                  ("OPPOSITE OF A RECTIFIER", ["A rectifier converts AC to DC."])]),
    "csd": ("CONSTANT-SPEED DRIVE (CSD)", "A constant-speed drive turns the AC generator at an almost constant speed.",
            [("VARIABLE ENGINE SPEED IN", ["Engine RPM changes with", "power setting."]),
             ("CONSTANT SPEED OUT", ["The generator is driven at a", "near-constant speed."]),
             ("CONSTANT FREQUENCY", ["So the AC frequency (e.g.", "400 Hz) stays constant."])]),
}


def component(answer):
    title, foot, facts = COMP[answer]
    s = header(title)
    s += panel(hl=True)
    cy = 360
    if answer == "capacitor":
        s += wire([(90, cy), (360, cy)])
        s += wire([(400, cy), (680, cy)])
        s += f'<rect x="354" y="{cy - 90}" width="12" height="180" fill="#475569"/>\n'
        s += f'<rect x="394" y="{cy - 90}" width="12" height="180" fill="#475569"/>\n'
        for k in range(6):
            s += t(344, cy - 70 + k * 30, "+", 18, 800, RED, "end")
            s += t(416, cy - 70 + k * 30 + 2, "−", 18, 800, BLUE, "start")
        s += t(380, cy - 110, "STORED CHARGE", 15, 800, GOLD_DARK)
        s += t(380, cy + 126, "DIELECTRIC (INSULATOR)", 12, 800, MUTED)
    elif answer == "resistor":
        s += wire([(90, cy), (300, cy)])
        pts = [(300, cy)] + [(320 + k * 20, cy + (-22 if k % 2 == 0 else 22)) for k in range(8)] + [(480, cy)]
        s += polyline(pts, GOLD_DARK, 5)
        s += wire([(480, cy), (680, cy)])
        s += t(160, cy - 30, "12 V", 22, 800, INK)
        s += t(600, cy - 30, "8 V", 22, 800, INK)
        s += line(300, cy + 70, 480, cy + 70, RED, 3, "aRedS")
        s += t(390, cy + 100, "4 V DROPPED ACROSS THE RESISTOR", 14, 800, RED)
        s += t(390, cy - 60, "RESISTOR", 15, 800, GOLD_DARK)
    elif answer == "inverter":
        s += line(90, cy, 250, cy, INK, 5)
        s += t(170, cy - 26, "DC", 22, 800, INK)
        s += f'<rect x="270" y="{cy - 70}" width="220" height="140" rx="12" fill="#fde68a" stroke="{GOLD}" stroke-width="4"/>\n'
        s += t(380, cy + 8, "INVERTER", 22, 800, INK)
        s += line(250, cy, 270, cy, INK, 5, "aDark")
        s += f'<path d="M 500,{cy} q 22,-50 44,0 t 44,0 t 44,0" fill="none" stroke="#b45309" stroke-width="5"/>\n'
        s += t(580, cy - 60, "AC", 22, 800, "#b45309")
    else:
        s += f'<rect x="80" y="{cy - 60}" width="140" height="120" rx="12" fill="#cbd5e1" stroke="{INK}" stroke-width="3"/>\n'
        s += t(150, cy + 6, "ENGINE", 16, 800, INK)
        s += t(150, cy + 90, "VARIABLE RPM", 13, 800, RED)
        s += line(220, cy, 280, cy, "#64748b", 10)
        s += f'<rect x="280" y="{cy - 60}" width="170" height="120" rx="12" fill="#fde68a" stroke="{GOLD}" stroke-width="4"/>\n'
        s += t(365, cy + 6, "CSD", 22, 800, INK)
        s += line(450, cy, 510, cy, "#64748b", 10)
        s += f'<circle cx="580" cy="{cy}" r="70" fill="#e2e8f0" stroke="{INK}" stroke-width="3"/>\n'
        s += t(580, cy + 6, "AC GEN", 16, 800, INK)
        s += t(580, cy + 100, "CONSTANT SPEED", 13, 800, GREEN)
        s += t(580, cy + 118, "CONSTANT FREQUENCY", 13, 800, GREEN)
    s += g.fact_column(facts)
    s += footer(foot)
    return s


# =====================================================================
# starter: solenoid (q2558), series winding (q2723); motor principle (q2738)
# =====================================================================

def starter(answer):
    title = "STARTER SOLENOID" if answer == "solenoid" else "STARTER MOTOR: SERIES WINDING"
    s = header(title)
    s += panel(hl=True)
    s += battery_sym(120, 330)
    s += wire([(120, 304), (120, 250), (420, 250)], RED, 6)
    sol = answer == "solenoid"
    s += f'<rect x="420" y="220" width="110" height="64" rx="8" fill="#ffffff" stroke="{GOLD if sol else INK}" stroke-width="{5 if sol else 2.5}"/>\n'
    s += t(475, 257, "SOLENOID", 13, 800, INK)
    s += wire([(530, 250), (600, 250), (600, 300)], RED, 6)
    ser = answer == "series"
    s += f'<circle cx="600" cy="360" r="56" fill="#e2e8f0" stroke="{GOLD if ser else INK}" stroke-width="{5 if ser else 3}"/>\n'
    s += t(600, 356, "STARTER", 13, 800, INK)
    s += t(600, 372, "MOTOR", 13, 800, INK)
    s += wire([(120, 356), (120, 520), (600, 520), (600, 416)], WIRE, 4)
    s += t(270, 240, "HEAVY CABLE: HIGH CURRENT", 12, 800, RED)
    s += wire([(475, 284), (475, 420), (300, 420)], BLUE, 2.5, dash="6 4")
    s += f'<rect x="220" y="400" width="80" height="40" rx="6" fill="#ffffff" stroke="{INK}" stroke-width="2.5"/>\n'
    s += t(260, 426, "START", 12, 800, INK)
    s += t(260, 470, "COCKPIT SWITCH", 12, 800, INK)
    s += t(400, 404, "LIGHT WIRING: SMALL CURRENT", 11, 800, BLUE)
    if ser:
        for k, ln in enumerate(("FIELD IN", "SERIES WITH", "ARMATURE")):
            s += t(666, 340 + k * 15, ln, 11, 800, GOLD_DARK, "start")
    if sol:
        s += t(475, 206, "NEAR THE STARTER", 12, 800, GOLD_DARK)
    facts = {
        "solenoid": [("HEAVY-DUTY SWITCH", ["A relay that switches the", "very large starter current."]),
                     ("NEAR THE STARTER", ["Keeps the heavy cable short;", "only a light wire runs to", "the cockpit."]),
                     ("CONTROLLED BY", ["The key/start switch, which", "energises the solenoid coil."])],
        "series": [("SERIES WINDING", ["The field winding carries the", "full armature current."]),
                   ("HIGH STARTING TORQUE", ["Greatest torque at low speed:", "ideal for turning a cold", "engine."]),
                   ("NEVER RUN UNLOADED", ["A series motor would", "overspeed with no load."])],
    }[answer]
    s += g.fact_column(facts)
    foot = ("Starter motor power is controlled by a solenoid located near the starter motor."
            if sol else "DC starter motors normally use a series-wound field for high starting torque.")
    s += footer(foot)
    return s


def motor_principle():
    s = header("FORCE ON A CURRENT-CARRYING CONDUCTOR")
    s += panel(hl=True)
    s += f'<rect x="100" y="230" width="90" height="220" rx="8" fill="#ef4444" stroke="{INK}" stroke-width="3"/>\n'
    s += f'<rect x="520" y="230" width="90" height="220" rx="8" fill="#3b82f6" stroke="{INK}" stroke-width="3"/>\n'
    s += t(145, 348, "N", 30, 800, "#ffffff")
    s += t(565, 348, "S", 30, 800, "#ffffff")
    for y in (260, 300, 340, 380, 420):
        s += line(200, y, 510, y, "#94a3b8", 2, "aDark")
    s += t(355, 222, "MAGNETIC FIELD (N TO S)", 13, 800, MUTED)
    s += f'<circle cx="355" cy="340" r="30" fill="#fde68a" stroke="{INK}" stroke-width="3"/>\n'
    s += f'<circle cx="355" cy="340" r="8" fill="{INK}"/>\n'
    s += t(355, 400, "CURRENT OUT OF THE PAGE", 12, 800, INK)
    s += line(355, 306, 355, 196, RED, 7, "aRed")
    s += t(372, 200, "FORCE", 16, 800, RED, "start")
    s += t(355, 520, "The conductor is pushed at right angles to both the field and the current.", 14, 400, BODY)
    s += t(355, 544, "(Fleming's left-hand rule)", 14, 400, BODY)
    s += g.fact_column([
        ("FORCE ON THE CONDUCTOR", ["A current across a magnetic", "field experiences a force."]),
        ("DIRECTION", ["At right angles to both the", "field and the current."]),
        ("MOTOR PRINCIPLE", ["This force is what turns an", "electric (starter) motor."]),
    ])
    s += footer("Current through a conductor at right angles to a magnetic field produces a force on it.")
    return s


BATCHES = {
    "electrics-batch-1": {
        "q2569-magneto-rotating-magnet": lambda: magneto("magnet"),
        "q2751-magneto-high-voltage": lambda: magneto("induction"),
        "q2575-magneto-distributor": lambda: magneto("distributor"),
        "q2591-magneto-condenser": lambda: magneto("condenser"),
        "q2595-magneto-impulse-coupling": lambda: magneto("impulse"),
        "q2576-magneto-broken-earth-wire": lambda: magneto("pwire"),
        "q2596-low-tension-transformer": low_tension,
    },
    "electrics-batch-2": {
        "q2610-alternator-rectifier": lambda: alternator("rectifier"),
        "q2600-alternator-reverse-current": lambda: alternator("reverse"),
        "q2585-alternator-stator": lambda: alternator("stator"),
        "q2614-alternator-purpose": lambda: alternator("purpose"),
        "q2589-alternator-vs-generator-low-rpm": alt_vs_gen,
        "q2578-generator-commutator": lambda: generator("commutator"),
        "q2594-voltage-regulator": lambda: generator("regulator"),
        "q2568-reverse-current-cut-out": lambda: generator("cutout"),
        "q2599-generator-self-excited": lambda: generator("selfexc"),
    },
    "electrics-batch-3": {
        "q2602-battery-40-ah": lambda: battery_ah(40, 4, 10, "A 40 ampere-hour battery can theoretically provide 4 amperes for 10 hours."),
        "q2613-battery-20-ah": lambda: battery_ah(20, 20, 1, "A 20 ampere-hour rating means the battery can provide 20 amps for 1 hour."),
        "q2609-battery-electrolyte": lambda: battery_cells("electrolyte"),
        "q2612-battery-24v-cells": lambda: battery_cells("cells"),
        "q2571-blown-fuse": lambda: protection("fuse"),
        "q2608-tripped-circuit-breaker": lambda: protection("cb"),
        "q2582-ammeter-voltmeter": lambda: meters("ammeter"),
        "q2611-voltmeter": lambda: meters("voltmeter"),
        "q2577-left-zero-ammeter": lambda: meters("leftzero"),
        "q2579-centre-zero-ammeter": lambda: meters("centrezero"),
    },
    "electrics-batch-4": {
        "q2590-capacitor": lambda: component("capacitor"),
        "q2604-resistor": lambda: component("resistor"),
        "q2607-inverter": lambda: component("inverter"),
        "q2725-constant-speed-drive": lambda: component("csd"),
        "q2558-starter-solenoid": lambda: starter("solenoid"),
        "q2723-starter-series-winding": lambda: starter("series"),
        "q2738-force-on-conductor": motor_principle,
    },
}

if __name__ == "__main__":
    for batch in sys.argv[1:] or BATCHES:
        pub = OUT / batch
        pub.mkdir(parents=True, exist_ok=True)
        for name, fn in BATCHES[batch].items():
            (pub / f"{name}.svg").write_text(fn(), encoding="utf-8")
            print("wrote", batch, name)
