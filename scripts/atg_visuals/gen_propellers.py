"""Propeller explanation diagrams (ATG)."""
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
UP, LO = g.naca(0.03, 0.4, 0.12, 60)


def section(le, chord_len, beta_deg, fill="#b8c0ca"):
    """Blade section, LE at `le`, TE down-right at beta below the plane of rotation;
    the section moves left (rotation) and its cambered face points forward (up the page)."""
    a = math.radians(beta_deg)
    dx, dy = math.cos(a), math.sin(a)        # LE -> TE, page coords (down-right)
    nx, ny = math.sin(a), -math.cos(a)       # toward the forward (cambered) face
    pts = [(le[0] + dx * x * chord_len + nx * y * chord_len, le[1] + dy * x * chord_len + ny * y * chord_len)
           for x, y in CAMBERED()]
    return poly(pts, fill, INK, 3)


def CAMBERED():
    return UP + list(reversed(LO))


def ray(v, ang_deg, r):
    a = math.radians(ang_deg)
    return v[0] + r * math.cos(a), v[1] - r * math.sin(a)


def arc(v, a0, a1, r, col, w=4):
    p0, p1 = ray(v, a0, r), ray(v, a1, r)
    sweep = 0 if a1 > a0 else 1
    large = 1 if abs(a1 - a0) > 180 else 0
    return f'<path d="M {p0[0]:.1f} {p0[1]:.1f} A {r} {r} 0 {large} {sweep} {p1[0]:.1f} {p1[1]:.1f}" fill="none" stroke="{col}" stroke-width="{w}"/>\n'


def def_boxes(items, answer, y0=146, h=138):
    s = ""
    for i, (key, title, lines_) in enumerate(items):
        fy = y0 + i * (h + 12)
        ans = key == answer
        fill, stroke, sw = ("#fff8e1", GOLD, 4) if ans else ("#f8fafc", "#cbd5e1", 2)
        s += f'<rect x="770" y="{fy}" width="378" height="{h}" rx="12" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>\n'
        s += t(790, fy + 34, title, 18, 800, GOLD_DARK if ans else INK, "start")
        if ans:
            s += f'<rect x="1048" y="{fy + 14}" width="88" height="26" rx="13" fill="{GOLD}"/>\n'
            s += t(1092, fy + 32, "ANSWER", 13, 800, NAVY)
        for j, ln in enumerate(lines_):
            s += t(790, fy + 66 + j * 24, ln, 16, 400, BODY, "start")
    return s


# =====================================================================
# blade angle (q2419) / helix angle (q2513)
# =====================================================================

def blade_angles(answer):
    title = "PROPELLER BLADE ANGLE" if answer == "blade" else "PROPELLER HELIX ANGLE"
    s = header(title)
    s += f'<rect x="40" y="142" width="710" height="444" rx="12" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2"/>\n'
    beta, phi = 32, 16
    le = (400, 350)
    s += line(70, le[1], 730, le[1], "#64748b", 3, dash="12 8")
    s += t(726, le[1] - 10, "PLANE OF ROTATION", 14, 800, MUTED, "end")
    s += section(le, 260, beta)
    ce = ray(le, 180 - beta, 190)
    s += line(ce[0], ce[1], *ray(le, -beta, 260), INK, 2, dash="6 5")
    s += t(ce[0] - 6, ce[1] - 8, "CHORD LINE", 13, 800, INK, "end")
    ra = ray(le, 180 - phi, 280)
    s += line(ra[0], ra[1], le[0] - 6, le[1] - 2, BLUE, 4, "aBlue")
    s += t(ra[0], ra[1] - 12, "RELATIVE AIRFLOW", 13, 800, BLUE, "start")
    cb = GOLD_DARK if answer == "blade" else "#94a3b8"
    ch = GOLD_DARK if answer == "helix" else "#94a3b8"
    s += arc(le, 180, 180 - beta, 150, cb, 6 if answer == "blade" else 3)
    s += arc(le, 180, 180 - phi, 105, ch, 6 if answer == "helix" else 3)
    s += arc(le, 180 - phi, 180 - beta, 62, GREEN, 4)
    labels = [("BLADE ANGLE", cb, ray(le, 180 - beta * 0.8, 150)),
              ("HELIX ANGLE", ch, ray(le, 180 - phi / 2, 105)),
              ("ANGLE OF ATTACK", GREEN, ray(le, 180 - (beta + phi) / 2, 62))]
    for i, (txt, col, tgt) in enumerate(labels):
        y = le[1] + 60 + i * 36
        s += t(90, y, txt, 15, 800, col, "start")
        s += line(92 + len(txt) * 10, y - 6, tgt[0], tgt[1] + 2, col, 2, "aDark")
    s += line(720, 216, 620, 216, INK, 4, "aDark")
    s += t(670, 242, "ROTATION", 13, 800, INK)
    s += line(560, 250, 560, 170, INK, 4, "aDark")
    s += t(572, 190, "FORWARD", 13, 800, INK, "start")
    s += t(395, 566, "Angle of attack = blade angle \u2212 helix angle", 16, 700, BODY)
    s += def_boxes([
        ("blade", "BLADE ANGLE", ["Between the chord line and", "the plane of rotation.", "Fixed by the blade setting."]),
        ("helix", "HELIX ANGLE", ["Between the relative airflow", "and the plane of rotation.", "Grows with forward speed."]),
        ("aoa", "ANGLE OF ATTACK", ["Between the chord line and", "the relative airflow."]),
    ], answer)
    foot = ("Blade angle is the angle between the chord line and the plane of rotation."
            if answer == "blade" else "Helix angle is the angle between the relative airflow and the plane of rotation.")
    s += footer(foot)
    return s


# =====================================================================
# helical twist (q2435)
# =====================================================================

def helical_twist():
    s = header("PROPELLER HELICAL TWIST")
    s += f'<rect x="40" y="142" width="1108" height="444" rx="12" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2"/>\n'
    # blade planform
    s += f'<path d="M 120,210 C 300,188 700,186 1000,200 Q 1060,208 1000,222 C 700,238 300,236 120,226 Z" fill="#b8c0ca" stroke="{INK}" stroke-width="3"/>\n'
    s += f'<circle cx="100" cy="218" r="26" fill="#64748b" stroke="{INK}" stroke-width="3"/>\n'
    s += t(100, 270, "HUB", 13, 800, INK)
    stations = [(260, "ROOT", 40), (590, "MID-BLADE", 26), (920, "TIP", 12)]
    for x, name, beta in stations:
        s += line(x, 196, x, 240, RED, 3)
        s += t(x, 262, name, 14, 800, INK)
        cx = x - 90
        vy = 390
        s += line(cx - 60, vy, cx + 230, vy, "#64748b", 2.5, dash="10 7")
        le = (cx, vy)
        s += section(le, 150, beta)
        s += arc(le, 180, 180 - beta, 70, GOLD_DARK, 4)
        s += line(*le, *ray(le, 180 - beta, 90), INK, 2, dash="5 4")
        s += t(x, 526, f"Blade angle about {beta}°", 16, 800, GOLD_DARK)
    s += line(260, 290, 920, 290, RED, 3, "aRedS")
    s += t(590, 312, "BLADE SPEED INCREASES TOWARD THE TIP", 14, 800, RED)
    s += t(594, 560, "Blade angle is reduced toward the tip so every section works at a similar angle of attack.", 16, 400, BODY)
    s += footer("Helical twist: the blade angle decreases from root to tip to keep thrust even along the blade.")
    return s


# =====================================================================
# torque reaction (q2450) / torque bending (q2422)
# =====================================================================

def prop_torque(answer):
    title = "PROPELLER TORQUE REACTION" if answer == "reaction" else "TORQUE BENDING OF THE BLADES"
    s = header(title)
    s += f'<rect x="40" y="142" width="710" height="444" rx="12" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2"/>\n'
    s += t(60, 172, "VIEWED FROM THE COCKPIT (BEHIND)", 15, 800, INK, "start")
    cx, cy = 395, 380
    s += f'<rect x="{cx - 330}" y="{cy - 10}" width="660" height="20" rx="8" fill="#dfe5ec" stroke="{INK}" stroke-width="2.5"/>\n'
    s += f'<circle cx="{cx}" cy="{cy}" r="46" fill="#dfe5ec" stroke="{INK}" stroke-width="3"/>\n'
    # blades: straight ghost and bent (lagging against clockwise rotation)
    for sgn in (-1, 1):
        s += line(cx, cy, cx, cy + sgn * 170, "#94a3b8", 14, dash="10 8")
        bend = f"M {cx},{cy} Q {cx},{cy + sgn * 90} {cx + sgn * 34},{cy + sgn * 168}"
        col = GOLD if answer == "bending" else "#64748b"
        s += f'<path d="{bend}" fill="none" stroke="{INK}" stroke-width="18" stroke-linecap="round"/>\n'
        s += f'<path d="{bend}" fill="none" stroke="{col}" stroke-width="12" stroke-linecap="round"/>\n'
    s += f'<circle cx="{cx}" cy="{cy}" r="16" fill="#475569" stroke="{INK}" stroke-width="2.5"/>\n'
    # rotation arrow (clockwise from cockpit)
    s += f'<path d="M {cx + 120},{cy - 150} A 190 190 0 0 1 {cx + 185},{cy - 20}" fill="none" stroke="{INK}" stroke-width="4" marker-end="url(#aDark)"/>\n'
    s += t(cx + 180, cy - 150, "PROPELLER ROTATION", 13, 800, INK, "start")
    s += t(cx + 180, cy - 132, "(CLOCKWISE)", 13, 800, INK, "start")
    # reaction torque on the aircraft (anticlockwise)
    rc = RED if answer == "reaction" else "#94a3b8"
    s += f'<path d="M {cx - 92},{cy + 92} A 130 130 0 0 0 {cx + 92},{cy + 92}" fill="none" stroke="{rc}" stroke-width="{6 if answer == "reaction" else 4}" marker-end="url(#aRed)"/>\n'
    s += t(cx, cy + 190, "REACTION TORQUE ON THE AIRCRAFT", 15, 800, rc)
    s += t(cx, cy + 190 + 20, "(OPPOSITE TO ROTATION: LEFT WING DOWN)", 13, 700, rc)
    if answer == "bending":
        s += t(cx - 60, cy - 150, "BLADES BEND BACK,", 14, 800, GOLD_DARK, "end")
        s += t(cx - 60, cy - 132, "AGAINST ROTATION", 14, 800, GOLD_DARK, "end")
        s += line(cx - 58, cy - 140, cx - 38, cy - 150, GOLD_DARK, 2.5, "aDark")
    facts = {
        "reaction": [("EQUAL AND OPPOSITE", ["Turning the propeller one way", "twists the aircraft the other", "way (Newton's third law)."]),
                     ("ROLL AND YAW", ["Clockwise propeller: the", "aircraft tends to roll left."]),
                     ("GREATEST", ["At high power and low", "airspeed, e.g. take-off."])],
        "bending": [("TORQUE BENDING", ["Air resistance opposes the", "blades, bending them back", "against the rotation."]),
                    ("OTHER BLADE LOADS", ["Thrust bends the blades", "forward; centrifugal force", "pulls them outward."]),
                    ("CHECK", ["Blades must be inspected for", "damage that could lead to", "failure."])],
    }[answer]
    s += g.fact_column(facts)
    foot = ("A rotating propeller produces a reaction force opposite to its rotation: torque."
            if answer == "reaction" else "Propeller torque bends the blades in the direction opposite to rotation.")
    s += footer(foot)
    return s


# =====================================================================
# take-off swing (q2452)
# =====================================================================

def takeoff_swing():
    s = header("TAKE-OFF SWING: CLOCKWISE PROPELLER")
    s += f'<rect x="40" y="142" width="710" height="444" rx="12" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2"/>\n'
    s += t(60, 172, "VIEW FROM ABOVE: TRICYCLE, PROPELLER CLOCKWISE FROM COCKPIT", 14, 800, INK, "start")
    cx, cy, sc = 395, 390, 1.25
    gtxt, pg = g.top_plane(cx, cy, sc)
    s += gtxt
    # spiral slipstream wrapping round the fuselage to the left of the fin
    pts = []
    for k in range(0, 60):
        tt = k / 59
        y = cy - 110 + tt * 270
        x = cx + 34 * math.sin(tt * 3.4 * math.pi) * (1 - 0.3 * tt)
        pts.append((x, y))
    s += polyline(pts, BLUE, 3.5)
    fin = pg(0, 128)
    s += line(fin[0] - 70, fin[1] - 26, fin[0] - 8, fin[1] - 6, BLUE, 4, "aBlue")
    s += t(fin[0] - 76, fin[1] - 34, "SLIPSTREAM HITS", 13, 800, BLUE, "end")
    s += t(fin[0] - 76, fin[1] - 18, "LEFT SIDE OF FIN", 13, 800, BLUE, "end")
    n = pg(0, -92)
    s += f'<path d="M {n[0] + 44},{n[1] - 14} Q {n[0]},{n[1] - 46} {n[0] - 48},{n[1] - 14}" fill="none" stroke="{GOLD_DARK}" stroke-width="6" marker-end="url(#aDark)"/>\n'
    s += t(n[0] - 60, n[1] - 30, "NOSE YAWS LEFT", 17, 800, GOLD_DARK, "end")
    for wx, wy, col in ((-40, 34, RED), (40, 34, INK), (0, -66, INK)):
        w = pg(wx, wy)
        s += f'<rect x="{w[0] - 6:.1f}" y="{w[1] - 12:.1f}" width="12" height="24" rx="3" fill="{col}"/>\n'
    lw = pg(-40, 34)
    s += t(230, 452, "MORE LOAD ON", 13, 800, RED)
    s += t(230, 468, "LEFT WHEEL", 13, 800, RED)
    s += line(262, 442, lw[0] - 8, lw[1] - 4, RED, 2, "aRedS")
    rw = pg(110, 0)
    s += line(rw[0], rw[1] - 20, rw[0], rw[1] - 80, RED, 5, "aRed")
    s += t(rw[0] + 12, rw[1] - 60, "MORE THRUST ON THE", 13, 800, RED, "start")
    s += t(rw[0] + 12, rw[1] - 44, "RIGHT (DOWN-GOING BLADE)", 13, 800, RED, "start")
    s += g.fact_column([
        ("SPIRAL SLIPSTREAM", ["Strikes the left side of the", "fin, pushing the tail right", "and the nose left."]),
        ("TORQUE REACTION", ["Presses the left wheel down:", "more friction on the left."]),
        ("ASYMMETRIC BLADE EFFECT", ["The down-going (right) blade", "gives more thrust at high", "power and angle of attack."]),
    ])
    s += footer("With a clockwise propeller (from the cockpit) the aeroplane tends to yaw left on take-off.")
    return s


# =====================================================================
# fine vs coarse (q2475 fine for take-off, q2497 coarse for cruise)
# =====================================================================

def fine_coarse(answer):
    title = "FINE PITCH FOR TAKE-OFF" if answer == "fine" else "COARSE PITCH FOR CRUISE"
    s = header(title)
    cols = [("fine", "FINE PITCH", 14, 8, ["Small blade angle", "High RPM, full power at", "low speed: take-off, climb"], "Like a low gear"),
            ("coarse", "COARSE PITCH", 38, 30, ["Large blade angle", "Efficient at high forward", "speed: cruise"], "Like a high gear")]
    for i, (key, head, beta, phi, lines_, gear) in enumerate(cols):
        px = 48 + i * 562
        ans = key == answer
        fill, stroke, sw = ("#fff8e1", GOLD, 4) if ans else ("#f8fafc", "#cbd5e1", 2)
        s += f'<rect x="{px}" y="142" width="542" height="444" rx="12" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>\n'
        s += t(px + 20, 178, head, 21, 800, INK, "start")
        if ans:
            s += f'<rect x="{px + 432}" y="158" width="92" height="28" rx="14" fill="{GOLD}"/>\n'
            s += t(px + 478, 177, "ANSWER", 14, 800, NAVY)
        le = (px + 200, 330)
        s += line(px + 30, le[1], px + 512, le[1], "#64748b", 2.5, dash="10 7")
        s += section(le, 230, beta)
        s += arc(le, 180, 180 - beta, 110, GOLD_DARK, 4)
        s += line(*le, *ray(le, 180 - beta, 130), INK, 2, dash="5 4")
        p = ray(le, 180 - beta / 2, 110)
        s += t(p[0], le[1] + 26, f"{beta}°", 16, 800, GOLD_DARK)
        ra = ray(le, 180 - phi, 170)
        s += line(ra[0], ra[1], le[0] - 6, le[1] - 2, BLUE, 3.5, "aBlue")
        for j, ln in enumerate(lines_):
            s += t(px + 271, 470 + j * 26, ln, 17 if j else 18, 800 if j == 0 else 400, INK if j == 0 else BODY)
        s += t(px + 271, 562, gear, 15, 800, MUTED)
    foot = ("For take-off a constant-speed propeller should be in fine pitch: a small blade angle."
            if answer == "fine" else "A coarse-pitch fixed propeller gives better cruise performance than a fine-pitch one.")
    s += footer(foot)
    return s


# =====================================================================
# CSU keeps RPM constant (q2508)
# =====================================================================

def tacho(cx, cy, val, label):
    s = f'<circle cx="{cx}" cy="{cy}" r="58" fill="#1f2937" stroke="{INK}" stroke-width="3"/>\n'
    for k in range(0, 7):
        a = math.radians(225 - k * 45)
        s += line(cx + 44 * math.cos(a), cy - 44 * math.sin(a), cx + 54 * math.cos(a), cy - 54 * math.sin(a), "#e2e8f0", 2)
    a = math.radians(225 - val * 270)
    s += line(cx, cy, cx + 44 * math.cos(a), cy - 44 * math.sin(a), "#f8fafc", 4)
    s += f'<circle cx="{cx}" cy="{cy}" r="6" fill="#f8fafc"/>\n'
    s += t(cx, cy + 34, "RPM", 12, 800, "#e2e8f0")
    s += t(cx, cy + 84, label, 14, 800, INK)
    return s


def csu_constant():
    s = header("CONSTANT-SPEED UNIT: RPM STAYS THE SAME")
    s += f'<rect x="40" y="142" width="710" height="444" rx="12" fill="#fff8e1" stroke="{GOLD}" stroke-width="4"/>\n'
    steps = [("1", "PILOT ADDS POWER", "Throttle opened slowly"),
             ("2", "RPM STARTS TO RISE", "Governor senses the change"),
             ("3", "BLADES COARSEN", "Blade angle increases"),
             ("4", "RPM BACK TO SELECTED", "Extra power becomes thrust")]
    for i, (n, head, sub) in enumerate(steps):
        y = 180 + i * 72
        s += g.badge(80, y + 4, n)
        s += t(108, y + 10, head, 17, 800, INK, "start")
        s += t(108, y + 32, sub, 15, 400, BODY, "start")
    s += tacho(560, 250, 0.55, "BEFORE: 2400 RPM")
    s += tacho(560, 440, 0.55, "AFTER: 2400 RPM")
    s += line(560, 330, 560, 368, GOLD_DARK, 4, "aDark")
    s += t(572, 356, "MORE POWER", 13, 800, GOLD_DARK, "start")
    s += g.fact_column([
        ("GOVERNOR", ["Senses RPM and changes the", "blade angle to hold the", "selected RPM."]),
        ("MORE POWER", ["Blade angle coarsens: the", "blades take bigger bites.", "RPM unchanged."]),
        ("LESS POWER", ["Blade angle fines off to", "stop the RPM falling."]),
    ])
    s += footer("With a CSU, increasing power coarsens the blades and the selected RPM remains the same.")
    return s


# =====================================================================
# fixed pitch in a dive (q2514)
# =====================================================================

def fixed_dive():
    s = header("FIXED-PITCH PROPELLER IN A DIVE")
    cols = [("LEVEL FLIGHT", 12, "Normal angle of attack", 0.5, "RPM NORMAL"),
            ("SHALLOW DIVE: SPEED UP", 22, "Smaller angle of attack", 0.72, "RPM INCREASES")]
    beta = 30
    for i, (head, phi, sub, rpm, rl) in enumerate(cols):
        px = 48 + i * 562
        ans = i == 1
        fill, stroke, sw = ("#fff8e1", GOLD, 4) if ans else ("#f8fafc", "#cbd5e1", 2)
        s += f'<rect x="{px}" y="142" width="542" height="444" rx="12" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>\n'
        s += t(px + 20, 178, head, 20, 800, INK, "start")
        le = (px + 180, 320)
        s += line(px + 30, le[1], px + 360, le[1], "#64748b", 2.5, dash="10 7")
        s += section(le, 200, beta)
        ra = ray(le, 180 - phi, 170)
        s += line(ra[0], ra[1], le[0] - 6, le[1] - 2, BLUE, 3.5, "aBlue")
        s += arc(le, 180 - phi, 180 - beta, 80, GREEN, 5)
        p = ray(le, 180 - (phi + beta) / 2, 96)
        s += t(p[0] - 4, p[1] - 4, "AoA", 14, 800, GREEN, "end")
        s += t(px + 180, 430, sub, 17, 800, INK)
        s += tacho(px + 440, 270, rpm, rl)
    s += t(330, 530, "Faster airflow meets the blade at a smaller", 15, 400, BODY)
    s += t(330, 552, "angle: less drag, so the propeller speeds up.", 15, 400, BODY)
    s += footer("With a fixed-pitch propeller, a dive at constant power makes the RPM increase.")
    return s


# =====================================================================
# power change sequence (q2484, q2737)
# =====================================================================

def lever(cx, top, col, knob, label, pos):
    s = f'<rect x="{cx - 8}" y="{top}" width="16" height="240" rx="8" fill="#cbd5e1" stroke="{INK}" stroke-width="2"/>\n'
    y = top + 20 + (1 - pos) * 200
    s += f'<rect x="{cx - 34}" y="{y - 18}" width="68" height="36" rx="10" fill="{col}" stroke="{INK}" stroke-width="2.5"/>\n'
    s += t(cx, y + 6, knob, 12, 800, "#ffffff")
    s += t(cx, top + 272, label, 14, 800, INK)
    return s


def power_sequence():
    s = header("CHANGING POWER WITH A CONSTANT-SPEED PROPELLER")
    s += f'<rect x="40" y="142" width="420" height="444" rx="12" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2"/>\n'
    s += t(60, 174, "POWER LEVERS", 16, 800, INK, "start")
    s += lever(130, 200, "#111827", "THR", "THROTTLE (MP)", 0.8)
    s += lever(250, 200, "#1d4ed8", "RPM", "PROPELLER", 0.8)
    s += lever(370, 200, "#dc2626", "MIX", "MIXTURE", 1.0)
    for bx, head, steps, ans in ((480, "INCREASING POWER", ["Mixture: rich", "RPM: increase", "Throttle (MP): increase"], True),
                                 (820, "DECREASING POWER", ["Throttle (MP): reduce", "RPM: reduce", "Mixture: as required"], False)):
        fill, stroke, sw = ("#fff8e1", GOLD, 4) if ans else ("#f8fafc", "#cbd5e1", 2)
        s += f'<rect x="{bx}" y="142" width="330" height="444" rx="12" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>\n'
        s += t(bx + 20, 176, head, 19, 800, INK, "start")
        for i, st in enumerate(steps):
            y = 250 + i * 90
            s += g.badge(bx + 40, y - 6, i + 1)
            s += t(bx + 68, y, st, 18, 800, INK, "start")
            if i < 2:
                s += line(bx + 40, y + 14, bx + 40, y + 62, "#94a3b8", 3, "aDark")
        memo = "RICH → REVS → THROTTLE" if ans else "THROTTLE → REVS → MIXTURE"
        s += t(bx + 165, 560, memo, 15, 800, GOLD_DARK if ans else MUTED)
    s += footer("To increase power: richen the mixture, increase RPM, then increase manifold pressure.")
    return s


BATCHES = {
    "propellers-batch-1": {
        "q2419-propeller-blade-angle": lambda: blade_angles("blade"),
        "q2513-propeller-helix-angle": lambda: blade_angles("helix"),
        "q2435-propeller-helical-twist": helical_twist,
        "q2450-propeller-torque-reaction": lambda: prop_torque("reaction"),
        "q2422-propeller-torque-bending": lambda: prop_torque("bending"),
    },
    "propellers-batch-2": {
        "q2452-take-off-swing-clockwise-propeller": takeoff_swing,
        "q2475-fine-pitch-take-off": lambda: fine_coarse("fine"),
        "q2497-coarse-pitch-cruise": lambda: fine_coarse("coarse"),
        "q2508-csu-constant-rpm": csu_constant,
        "q2514-fixed-pitch-dive-rpm": fixed_dive,
    },
    "propellers-batch-3": {
        "q2484-power-increase-sequence": power_sequence,
    },
}

if __name__ == "__main__":
    for batch in sys.argv[1:] or BATCHES:
        pub = OUT / batch
        pub.mkdir(parents=True, exist_ok=True)
        for name, fn in BATCHES[batch].items():
            (pub / f"{name}.svg").write_text(fn(), encoding="utf-8")
            print("wrote", batch, name)
