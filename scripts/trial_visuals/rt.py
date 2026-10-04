"""Radio Telephony trial-mock diagrams.

R holds the diagrams in use (rendered by build.py and applied to the questions table). HOLD keeps the other
drafts that were reviewed but not chosen; build.py does not render them.
"""
import math

from common import Registry, band
from kit import (BLUE, BLUE_SOFT, BODY, GOLD, GOLD_DARK, GOLD_SOFT, GREEN, GREEN_SOFT, GROUND, INK, LINE, MUTED, NAVY,
                 PANEL, RED, RED_SOFT, SKY, arrow, card, circle, cloud, dim, line, path, pill, plane_side, plane_top, poly,
                 rect, t, template)

R = Registry("radio-telephony", "/explanation-images/radio-telephony/refined-batch-1")
HOLD = Registry("radio-telephony", "/explanation-images/radio-telephony/refined-batch-1")


def span(x0, x1, y, h, text, fill, color=INK, stroke=None, size=21):
    s = rect(x0, y, x1 - x0, h, fill, stroke or fill, 2, 8)
    return s + t((x0 + x1) / 2, y + h / 2 + size * 0.36, text, size, 800, color)


def axis(x0, x1, y, ticks=(), size=19):
    s = line(x0, y, x1, y, INK, 4)
    for x, lab in ticks:
        s += line(x, y - 10, x, y + 10, INK, 3)
        s += t(x, y + 36, lab, size, 700, MUTED)
    return s


def strip(x, y, w, h, fill="#475569", keys=False):
    """Runway seen from above (left to right) with centreline dashes; keys adds threshold bars at the left end."""
    s = rect(x, y, w, h, fill, INK, 2, 2)
    if keys:
        for j in range(4):
            s += rect(x + 16, y + 10 + j * (h - 20) / 4, 44, (h - 20) / 4 - 8, "#ffffff", "#ffffff", 0, 0)
    k = x + (90 if keys else 60)
    while k + 30 < x + w - 40:
        s += f'<rect x="{k:.1f}" y="{y + h / 2 - 2:.1f}" width="30" height="4" fill="#ffffff"/>\n'
        k += 60
    return s


def clock(cx, cy, r, hh, mm, label, color=NAVY):
    s = circle(cx, cy, r, "#ffffff", color, 6)
    for k in range(12):
        a = math.radians(k * 30)
        s += line(cx + (r - 18) * math.sin(a), cy - (r - 18) * math.cos(a), cx + (r - 6) * math.sin(a),
                  cy - (r - 6) * math.cos(a), INK, 4 if k % 3 == 0 else 2)
    ah = math.radians((hh % 12) * 30 + mm * 0.5)
    am = math.radians(mm * 6)
    s += line(cx, cy, cx + r * 0.5 * math.sin(ah), cy - r * 0.5 * math.cos(ah), INK, 9)
    s += line(cx, cy, cx + r * 0.78 * math.sin(am), cy - r * 0.78 * math.cos(am), INK, 5)
    s += circle(cx, cy, 8, INK, INK, 0)
    s += t(cx, cy + r + 50, f"{hh:02d}:{mm:02d}", 36, 800, color)
    s += t(cx, cy - r - 24, label, 24, 800, color)
    return s


# ------------------------------------------------------------------ flight planning

@R.add(484, "rt-trial-flight-plan-30min", "Filing a Flight Plan — 30 Minutes",
       template("FILE AT LEAST 30 MINUTES BEFORE DEPARTURE",
                "60 MINUTES FOR AN INTERNATIONAL FLIGHT",
                [("WHY", "The ATSU needs time to process the plan and pass it to other units"),
                 ("EARLIEST", "A flight plan may be filed up to 5 days in advance")]), h=400)
def _():
    k = 840 / 60
    x1 = 1060
    s = span(x1 - 30 * k, x1, 100, 70, "domestic: at least 30 min", GOLD, INK, GOLD_DARK, 22)
    s += span(x1 - 60 * k, x1, 200, 60, "international: at least 60 min", PANEL, MUTED, LINE)
    s += axis(x1 - 60 * k, x1, 310, [(x1 - m * k, f"−{m} min" if m else "0") for m in range(60, -1, -10)])
    s += line(x1, 70, x1, 310, NAVY, 5)
    s += t(x1, 55, "DEPARTURE", 20, 800, NAVY)
    return s


@R.add(460, "rt-trial-local-to-utc", "South African Time to UTC",
       template("UTC = SOUTH AFRICAN LOCAL TIME − 2 HOURS",
                "SOUTH AFRICAN STANDARD TIME IS UTC+2 ALL YEAR (NO DAYLIGHT SAVING)",
                [("LOCAL → UTC", "Subtract 2 hours: 17:00 SAST = 15:00 UTC"),
                 ("UTC → LOCAL", "Add 2 hours: 06:30 UTC = 08:30 SAST")]), h=480)
def _():
    s = clock(260, 230, 140, 17, 0, "SA LOCAL TIME")
    s += clock(940, 230, 140, 15, 0, "UTC", RED)
    s += arrow(450, 230, 740, 230, "red", 6)
    s += pill(595, 180, "− 2 hours", RED, "#ffffff", 26)
    return s


@R.add(485, "rt-trial-item10-s", "Flight Plan Item 10 — Equipment Code S",
       template("S = V + O + L: VHF RADIO, VOR AND ILS",
                "THE STANDARD COM/NAV/APPROACH FIT, NO MORE AND NO LESS",
                [("V", "VHF radiotelephony"),
                 ("O", "VOR"),
                 ("L", "ILS"),
                 ("ANYTHING ELSE", "Add its own letter, e.g. D for DME, F for ADF")]), h=420)
def _():
    s = rect(40, 110, 200, 200, GOLD, GOLD_DARK, 4, 16)
    s += t(140, 240, "S", 110, 800, INK)
    s += t(270, 235, "=", 60, 800, INK)
    items = [("V", "VHF radio"), ("O", "VOR"), ("L", "ILS")]
    for i, (k, lab) in enumerate(items):
        x = 320 + i * 290
        s += rect(x, 110, 220, 200, NAVY, NAVY, 0, 16)
        s += t(x + 110, 215, k, 80, 800, "#ffffff")
        s += t(x + 110, 280, lab, 24, 700, "#cbd5e1")
        if i < 2:
            s += t(x + 255, 235, "+", 60, 800, INK)
    s += t(600, 380, "Not included in S: DME (D), ADF (F), transponder — list them separately.", 21, 700, BODY)
    return s


@R.add(567, "rt-trial-sar-phases", "The Three Emergency (SAR) Phases",
       template("UNCERTAINTY → ALERT → DISTRESS",
                "INCERFA → ALERFA → DETRESFA: THE RESPONSE GROWS AS CONCERN GROWS",
                [("INCERFA", "Uncertainty: doubt about the aircraft's safety"),
                 ("ALERFA", "Alert: apprehension about the aircraft and occupants"),
                 ("DETRESFA", "Distress: reasonable certainty of grave and imminent danger")]), h=440)
def _():
    phases = [("INCERFA", "UNCERTAINTY", "#fde68a", INK), ("ALERFA", "ALERT", "#fb923c", INK),
              ("DETRESFA", "DISTRESS", RED, "#ffffff")]
    s = ""
    for i, (code, name, f, c) in enumerate(phases):
        x = 40 + i * 390
        h = 150 + i * 60
        s += rect(x, 360 - h, 330, h, f, f, 0, 14)
        s += t(x + 165, 360 - h + 60, name, 30, 800, c)
        s += t(x + 165, 360 - h + 100, code, 24, 700, c)
        if i < 2:
            s += arrow(x + 338, 300, x + 382, 300, "ink", 6)
    s += t(600, 410, "concern increases  →", 22, 800, MUTED)
    return s


@R.add(570, "rt-trial-ground-signal-v", "Ground-to-Air Signal — V",
       template("V = REQUIRE ASSISTANCE",
                "LAY OUT LARGE, HIGH-CONTRAST STRIPS SO A SEARCH AIRCRAFT CAN READ THEM",
                [("V", "Require assistance"),
                 ("X", "Require medical assistance"),
                 ("N / Y", "No (negative) / Yes (affirmative)")]), h=480)
def _():
    s = rect(40, 40, 620, 400, "#c7b38c", "#a8956f", 3, 14)
    s += path("M 190,110 L 350,370 L 510,110", "none", "#f97316", 46, extra=' stroke-linecap="square" stroke-linejoin="miter"')
    legend = [("V", "require assistance", True), ("X", "require medical assistance", False),
              ("N", "no / negative", False), ("Y", "yes / affirmative", False)]
    for i, (k, lab, hl) in enumerate(legend):
        y = 60 + i * 95
        s += rect(700, y, 460, 80, GOLD_SOFT if hl else PANEL, GOLD if hl else LINE, 4 if hl else 2, 10)
        s += t(750, y + 56, k, 44, 800, "#f97316" if hl else INK)
        s += t(800, y + 50, lab, 24, 800 if hl else 600, INK, "start")
    return s


# ------------------------------------------------------------------ navigation & flight rules

@R.add(410, "rt-trial-qdr", "Q-Codes — QDR and QDM",
       template("QDR = MAGNETIC BEARING FROM THE STATION",
                "QDM IS THE MAGNETIC BEARING TO THE STATION (QDR ± 180°)",
                [("QDR", "Magnetic bearing FROM the station"),
                 ("QDM", "Magnetic heading/bearing TO the station (zero wind)"),
                 ("QTE / QUJ", "True bearing from / to the station")]), h=520)
def _():
    cx, cy = 260, 400
    s = rect(30, 30, 700, 460, SKY, SKY, 0, 14)
    s += arrow(cx, cy, cx, 90, "navy", 4)
    s += t(cx, 76, "MAGNETIC N", 20, 800, NAVY)
    ang = math.radians(60)
    sx, sy = math.sin(ang), math.cos(ang)
    px, py = cx + 420 * sx, cy - 420 * sy
    s += line(cx, cy, px, py, MUTED, 2, None, "8 6")
    s += arrow(cx + 30 * sx, cy - 30 * sy, cx + 230 * sx, cy - 230 * sy, "blue", 6)
    s += arrow(px - 45 * sx, py + 45 * sy, cx + 290 * sx, cy - 290 * sy, "red", 6)
    s += path(f"M {cx},{cy - 110} A 110 110 0 0 1 {cx + 110 * sx:.1f},{cy - 110 * sy:.1f}", "none", BLUE, 4)
    s += t(cx + 52, cy - 124, "060°", 22, 800, BLUE)
    s += circle(cx, cy, 20, "#ffffff", NAVY, 5) + circle(cx, cy, 6, NAVY, NAVY, 0)
    s += t(cx, cy + 52, "STATION", 20, 800, NAVY)
    s += plane_top(px, py, 0.8, 240, INK)
    s += pill(cx + 150 * sx + 120, cy - 150 * sy + 46, "QDR 060° — FROM", BLUE, "#ffffff", 21)
    s += pill(cx + 330 * sx - 150, cy - 330 * sy - 40, "QDM 240° — TO", RED, "#ffffff", 21)
    rows = [("QDR", "magnetic bearing FROM the station", BLUE_SOFT, True),
            ("QDM", "magnetic bearing TO the station", RED_SOFT, False),
            ("QTE", "true bearing FROM the station", PANEL, False),
            ("QUJ", "true bearing TO the station", PANEL, False)]
    for i, (k, b, f, hl) in enumerate(rows):
        s += card(770, 30 + i * 116, 400, 100, k, b, NAVY, f, 26, 19, hl)
    return s


@R.add(428, "rt-trial-svfr-ceiling", "Special VFR — Minimum Ceiling",
       template("SPECIAL VFR (AEROPLANE): CEILING AT LEAST 600 FT AGL",
                "ATC SEPARATES SVFR TRAFFIC, SO THE CEILING CAN BE LOWER THAN FOR NORMAL VFR",
                [("SVFR", "Ceiling ≥ 600 ft; stay clear of cloud with the surface in sight"),
                 ("NORMAL VFR IN A CTR", "Ceiling ≥ 1500 ft"),
                 ("CLEARANCE", "SVFR is only flown with an ATC clearance inside a control zone")]), h=520)
def _():
    s = rect(0, 0, 1200, 520, SKY, SKY, 0, 0)
    s += rect(0, 460, 1200, 60, GROUND, GROUND, 0, 0)
    y15, y6 = 100, 460 - 360 * 600 / 1500
    s += line(120, y15, 1180, y15, MUTED, 3, None, "12 8")
    s += t(1170, y15 - 12, "normal VFR ceiling in a CTR: 1500 ft", 20, 800, MUTED, "end")
    for x in range(80, 1200, 230):
        s += cloud(x + 100, y6 - 40, 260, 70)
    s += line(0, y6, 1200, y6, RED, 4)
    s += pill(160, y6 + 34, "cloud base 600 ft AGL", RED, "#ffffff", 20)
    s += plane_side(620, y6 + 90, 1.0, NAVY)
    s += dim(1080, y6, 1080, 460, "600 ft", "red", 24, side="left")
    return s


@R.add(414, "rt-trial-ifr-vfr-imc-vmc", "Flight Rules vs Weather Conditions",
       template("IFR CAN BE FLOWN IN VMC OR IMC — VFR ONLY IN VMC",
                "VFR/IFR ARE THE RULES YOU FLY BY; VMC/IMC ARE THE WEATHER CONDITIONS",
                [("VFR", "Needs VMC: the pilot sees and avoids"),
                 ("IFR", "Legal in VMC and in IMC (instrument navigation, ATC separation)")]), h=460)
def _():
    x0, y0, cw, ch = 300, 110, 380, 140
    s = rect(x0, y0 - 60, cw, 56, NAVY, NAVY, 0, 8) + t(x0 + cw / 2, y0 - 22, "VMC (good weather)", 22, 800, "#ffffff")
    s += rect(x0 + cw + 10, y0 - 60, cw, 56, NAVY, NAVY, 0, 8) + t(x0 + cw * 1.5 + 10, y0 - 22, "IMC (in cloud / poor vis)", 22, 800, "#ffffff")
    for r, rule in enumerate(["VFR", "IFR"]):
        y = y0 + r * (ch + 10)
        s += rect(60, y, 230, ch, NAVY, NAVY, 0, 8) + t(175, y + ch / 2 + 14, rule, 40, 800, "#ffffff")
        for c in range(2):
            ok = not (r == 0 and c == 1)
            x = x0 + c * (cw + 10)
            s += rect(x, y, cw, ch, GREEN_SOFT if ok else RED_SOFT, GREEN if ok else RED, 3, 8)
            s += t(x + cw / 2, y + ch / 2 + 22, "✓ allowed" if ok else "✗ not allowed", 34, 800, GREEN if ok else RED)
    return s


@R.add(2814, "rt-trial-runway-contaminated", "Contaminated Runway",
       template("CONTAMINATED: MORE THAN 25% OF THE RUNWAY COVERED",
                "BY STANDING WATER DEEPER THAN 3 MM, SLUSH, SNOW OR ICE",
                [("AREA", "More than 25% of the required runway length and width"),
                 ("WHAT COUNTS", "Standing water deeper than 3 mm, or slush, snow or ice"),
                 ("WHY IT MATTERS", "Braking and aquaplaning change enough to need separate performance data")]), h=480)
def _():
    x, y, w, h = 80, 140, 1040, 150
    s = strip(x, y, w, h)
    for k in range(1, 4):
        s += line(x + k * w / 4, y - 30, x + k * w / 4, y + h + 30, INK, 2, None, "6 6")
    for (px, py, rx, ry) in [(220, 190, 110, 40), (330, 250, 120, 30), (520, 200, 140, 45), (170, 250, 60, 25)]:
        s += f'<ellipse cx="{px}" cy="{py}" rx="{rx}" ry="{ry}" fill="#60a5fa" fill-opacity="0.85" stroke="#2563eb" stroke-width="2"/>\n'
    for k in range(4):
        s += t(x + (k + 0.5) * w / 4, y - 40, "25%", 20, 700, MUTED)
    s += pill(600, 360, "covered area > 25%  →  CONTAMINATED", RED, "#ffffff", 24)
    s += rect(860, 390, 260, 70, PANEL, LINE, 2, 8)
    s += rect(880, 430, 220, 14, "#475569", "#475569", 0, 0)
    s += rect(880, 418, 220, 12, "#60a5fa", "#2563eb", 1, 0)
    s += t(990, 410, "water > 3 mm deep", 18, 800, INK)
    return s


# ------------------------------------------------------------------ phraseology

@R.add(506, "rt-trial-backtrack", "Backtrack the Runway",
       template("BACKTRACK = TAXI ON THE RUNWAY AGAINST THE DIRECTION IN USE",
                "USED WHEN THERE IS NO PARALLEL TAXIWAY TO REACH THE THRESHOLD",
                [("WHERE", "On the active runway — follow the clearance exactly"),
                 ("THEN", "Turn around at the end and line up, or vacate, as cleared")]), h=460)
def _():
    s = strip(80, 170, 1040, 110, keys=True)
    s += rect(700, 280, 80, 150, "#94a3b8", INK, 2, 2)
    s += t(800, 420, "taxiway", 20, 700, MUTED, "start")
    s += arrow(900, 110, 1120, 110, "green", 6)
    s += t(1120, 90, "runway direction in use (landing / take-off)", 20, 800, GREEN, "end")
    s += path("M 740,410 L 740,225 L 230,225", "none", RED, 6, "red")
    s += path("M 210,225 C 120,225 120,195 210,195 L 300,195", "none", RED, 4, "red", "8 6")
    s += plane_top(480, 225, 0.75, -90, NAVY)
    s += pill(480, 330, "BACKTRACK: taxi against the runway direction", RED, "#ffffff", 21)
    s += t(160, 150, "turn around and line up", 19, 800, RED)
    return s


@R.add(518, "rt-trial-line-up-and-wait", "Line Up and Wait",
       template("LINE UP AND WAIT: ENTER THE RUNWAY, LINE UP, DO NOT TAKE OFF",
                "IT IS NOT A TAKE-OFF CLEARANCE",
                [("DO", "Taxi onto the runway and line up on the centreline"),
                 ("DON'T", "Start the take-off roll until cleared for take-off"),
                 ("READ BACK", "'Lining up and waiting, runway 03'")]), h=460)
def _():
    s = strip(80, 170, 1040, 110, keys=True)
    s += rect(200, 280, 80, 150, "#94a3b8", INK, 2, 2)
    s += line(196, 330, 284, 330, GOLD, 6) + line(196, 342, 284, 342, GOLD, 4, None, "10 6")
    s += t(300, 345, "holding point", 18, 700, MUTED, "start")
    s += path("M 240,410 L 240,250 Q 240,225 270,225 L 290,225", "none", BLUE, 5, "blue")
    s += plane_top(340, 225, 0.75, 90, NAVY)
    s += line(420, 176, 420, 274, RED, 6, None, "12 8")
    s += arrow(440, 225, 600, 225, "muted", 5, "10 8")
    s += pill(520, 120, "no take-off roll until cleared for take-off", RED, "#ffffff", 20)
    s += t(560, 330, "lined up on the centreline: WAIT", 21, 800, NAVY, "start")
    return s
