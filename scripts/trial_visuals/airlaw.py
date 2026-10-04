"""Air Law trial-mock diagrams.

R holds the diagrams in use (rendered by build.py and applied to the questions table). HOLD keeps drafts that were
reviewed but not chosen; build.py does not render them.
"""
from common import Registry, band, tag
from kit import (BLUE, BLUE_SOFT, BODY, GOLD, GOLD_DARK, GOLD_SOFT, GREEN, GREEN_SOFT, GROUND, INK, LINE, MUTED, NAVY,
                 PANEL, RED, RED_SOFT, SKY, arrow, card, circle, cloud, dim, line, path, pill, plane_side, plane_top, poly,
                 rect, t, template)

R = Registry("air-law", "/explanation-images/air-law/refined-batch-1")
HOLD = Registry("air-law", "/explanation-images/air-law/refined-batch-1")


def axis(x0, x1, y, ticks=(), size=19):
    """Plain horizontal time axis with labelled ticks [(x, label)]."""
    s = line(x0, y, x1, y, INK, 4)
    for x, lab in ticks:
        s += line(x, y - 10, x, y + 10, INK, 3)
        s += t(x, y + 36, lab, size, 700, MUTED)
    return s


def span(x0, x1, y, h, text, fill, color=INK, stroke=None, size=21):
    s = rect(x0, y, x1 - x0, h, fill, stroke or fill, 2, 8)
    s += t((x0 + x1) / 2, y + h / 2 + size * 0.36, text, size, 800, color)
    return s


def marker(x, y0, y1, label, color=INK, size=20, above=True):
    s = line(x, y0, x, y1, color, 4)
    s += t(x, (y0 - 14) if above else (y1 + size + 10), label, size, 800, color)
    return s


def sun(x, y, r=26, fill=GOLD):
    s = ""
    for k in range(8):
        import math
        a = k * math.pi / 4
        s += line(x + (r + 6) * math.cos(a), y + (r + 6) * math.sin(a), x + (r + 18) * math.cos(a),
                  y + (r + 18) * math.sin(a), GOLD_DARK, 4)
    return s + circle(x, y, r, fill, GOLD_DARK, 3)


def aerodrome(x, y, label, color=NAVY):
    s = circle(x, y, 24, "#ffffff", color, 4)
    s += line(x - 14, y + 10, x + 14, y - 10, color, 6)
    s += t(x, y + 56, label, 20, 800, color)
    return s


def doc(x, y, w, h, title, sub, ok=True):
    s = rect(x, y, w, h, "#ffffff", LINE, 2, 8)
    s += path(f"M {x + w - 34},{y} L {x + w},{y + 34}", "none", LINE, 2)
    for k in range(4):
        s += line(x + 28, y + 120 + k * 22, x + w - 40 - (k % 2) * 50, y + 120 + k * 22, "#e2e8f0", 6)
    s += t(x + w / 2, y + 50, title, 22, 800, INK)
    s += t(x + w / 2, y + 82, sub, 18, 600, MUTED)
    s += circle(x + w - 26, y + h - 26, 22, GREEN if ok else RED, GREEN if ok else RED, 0)
    s += t(x + w - 26, y + h - 17, "✓" if ok else "✗", 26, 800, "#ffffff")
    return s


# ------------------------------------------------------------------ accidents & incidents

@R.add(764, "al-trial-accident-notify-24h", "Accident Notification — Time Limit",
       template("NOTIFY AS SOON AS POSSIBLE — AND NEVER LATER THAN 24 HOURS",
                "A GENERAL DUTY WITH A HARD BACKSTOP",
                [("AS SOON AS POSSIBLE", "Injured people, SAR and evidence are all time-critical"),
                 ("LATEST", "24 hours after the accident"),
                 ("WHO", "The PIC (or the operator if the PIC cannot)")]), h=420)
def _():
    x0, x1 = 120, 1080
    s = span(x0, 520, 140, 70, "AS SOON AS POSSIBLE", GREEN, "#ffffff")
    s += span(520, x1, 140, 70, "still within the limit — but late", GOLD_SOFT, GOLD_DARK, GOLD)
    s += axis(x0, x1, 260, [(x0 + i * (x1 - x0) / 4, f"{i * 6} h") for i in range(5)])
    s += marker(x0, 100, 260, "ACCIDENT", RED)
    s += line(x1, 100, x1, 262, RED, 6)
    s += pill(x1, 80, "24 h LIMIT", RED, "#ffffff", 22)
    s += t(600, 370, "Notification must reach the authority within 24 hours at the very latest.", 21, 700, BODY)
    return s


@R.add(1402, "al-trial-accident-notify-order", "Accident Notification — Order of Priority",
       template("DIRECTOR → ATSU → NEAREST POLICE STATION",
                "THE AUTHORITY THAT DIRECTS THE INVESTIGATION IS TOLD FIRST",
                [("1 DIRECTOR", "Director of Civil Aviation (SACAA): starts the investigation"),
                 ("2 ATSU", "Air traffic services: manages the airspace and alerts SAR"),
                 ("3 POLICE", "Nearest police station: secures and guards the site")]), h=380)
def _():
    items = [("1", "DIRECTOR", "Civil Aviation\nAuthority", NAVY), ("2", "ATSU", "air traffic\nservices unit", BLUE),
             ("3", "POLICE", "nearest police\nstation", GREEN)]
    s = ""
    for i, (n, head, sub, col) in enumerate(items):
        x = 40 + i * 400
        s += rect(x, 70, 320, 240, "#ffffff", col, 4, 14)
        s += circle(x + 160, 70, 34, col, col, 0)
        s += t(x + 160, 83, n, 34, 800, "#ffffff")
        s += t(x + 160, 170, head, 34, 800, col)
        s += t(x + 160, 220, sub, 22, 600, BODY)
        if i < 2:
            s += arrow(x + 330, 190, x + 392, 190, "ink", 5)
    return s


@HOLD.add(773, "al-trial-accident-guard-wreck", "Guarding the Wreckage",
       template("THE PIC GUARDS THE WRECKAGE UNTIL THE POLICE ARRIVE",
                "IF THE PIC CAN'T, THE NEXT CREW MEMBER IN LINE TAKES OVER",
                [("WHY", "The PIC is on scene and can stop evidence being disturbed"),
                 ("EXCEPTIONS", "Moving wreckage only to rescue people or prevent further danger"),
                 ("HANDOVER", "Police take over the guard when they arrive")]), h=480)
def _():
    s = rect(40, 60, 480, 360, "#fff7ed", RED, 3, 12, "16 10")
    s += t(280, 100, "DO NOT DISTURB", 22, 800, RED)
    s += path("M 120,330 L 460,330", "none", GROUND, 30)
    s += plane_side(270, 280, 2.2, "#64748b", pitch=-12)
    s += path("M 330,250 l 30,-40 l 10,30 l 30,-25", "none", RED, 4)
    steps = [("1  Pilot-in-command", "guards the wreck and keeps people away", GOLD_SOFT, True),
             ("2  Next crew member in line", "if the PIC is injured or unable", PANEL, False),
             ("3  Police", "take over the guard on arrival", PANEL, False)]
    for i, (h_, b, f, hl) in enumerate(steps):
        s += card(580, 60 + i * 125, 580, 105, h_, b, NAVY, f, hl=hl)
        if i < 2:
            s += arrow(870, 167 + i * 125, 870, 183 + i * 125, "ink", 4)
    return s


# ------------------------------------------------------------------ licensing & logbooks

@R.add(893, "al-trial-ppl-exam-validity", "PPL Theory — Two Separate Clocks",
       template("SKILLS TEST WITHIN 36 MONTHS OF THE FINAL THEORY PASS",
                "AND ALL THEORY EXAMS WITHIN 18 MONTHS OF THE FIRST CREDIT",
                [("CLOCK 1", "18 months to pass the whole exam series"),
                 ("CLOCK 2", "36 months from the final pass to the skills test")]), h=420)
def _():
    k = 600 / 36
    x0 = 120
    xf = x0 + 18 * k
    xe = xf + 36 * k
    s = span(x0, xf, 110, 64, "all exams: 18 months", BLUE_SOFT, BLUE, BLUE)
    s += span(xf, xe, 200, 64, "skills test: within 36 months", GOLD_SOFT, GOLD_DARK, GOLD)
    s += axis(x0, xe + 40, 320, [(x0, "0"), (xf, "18"), (x0 + 36 * k, "36"), (xe, "54 months")])
    s += marker(x0, 90, 320, "", BLUE)
    s += marker(xf, 90, 320, "", GOLD_DARK)
    s += t(x0, 395, "first exam passed", 19, 800, BLUE)
    s += t(xf, 395, "final exam passed", 19, 800, GOLD_DARK)
    s += line(xe, 180, xe, 330, RED, 6)
    s += pill(xe - 10, 150, "skills test deadline", RED, "#ffffff", 19)
    return s


@R.add(898, "al-trial-ppl-dual-hours", "PPL(A) — Minimum Flight Time",
       template("AT LEAST 25 OF THE 45 HOURS MUST BE DUAL INSTRUCTION",
                "45 HOURS IS THE MINIMUM TOTAL FLIGHT TIME FOR THE PPL(A)",
                [("DUAL", "At least 25 h with a flight instructor"),
                 ("THE REST", "Includes the required solo and solo cross-country flying"),
                 ("TOTAL", "At least 45 h")]), h=380)
def _():
    k = 900 / 45
    x0 = 150
    s = span(x0, x0 + 25 * k, 120, 100, "25 h DUAL instruction", NAVY, "#ffffff", size=26)
    s += span(x0 + 25 * k, x0 + 45 * k, 120, 100, "remaining 20 h", GOLD_SOFT, GOLD_DARK, GOLD, 24)
    s += axis(x0, x0 + 45 * k, 270, [(x0, "0 h"), (x0 + 25 * k, "25 h"), (x0 + 45 * k, "45 h")])
    s += t(600, 80, "MINIMUM 45 HOURS TOTAL", 24, 800, INK)
    return s


@R.add(910, "al-trial-ppl-long-nav", "PPL(A) Long Navigation Flight",
       template("150 NM, ONE POINT ≥ 50 NM FROM BASE, TWO FULL-STOP LANDINGS AWAY",
                "THE TWO LANDINGS ARE AT DIFFERENT AERODROMES, NOT AT BASE",
                [("DISTANCE", "At least 150 NM in total"),
                 ("REACH", "At least one point 50 NM or more from base"),
                 ("LANDINGS", "Two full-stop landings at two different aerodromes away from base")]), h=520)
def _():
    B, A, C = (180, 380), (620, 110), (1000, 360)
    s = rect(30, 30, 1140, 460, SKY, SKY, 0, 14)
    s += arrow(B[0] + 40, B[1] - 25, A[0] - 40, A[1] + 25, "navy", 5)
    s += arrow(A[0] + 40, A[1] + 22, C[0] - 40, C[1] - 22, "navy", 5)
    s += arrow(C[0] - 45, C[1] + 2, B[0] + 45, B[1] - 1, "navy", 5)
    s += aerodrome(*B, "BASE")
    s += aerodrome(*A, "")
    s += aerodrome(*C, "")
    s += pill(A[0] + 170, A[1], "full-stop landing 1", GREEN, "#ffffff", 19)
    s += pill(C[0], C[1] + 60, "full-stop landing 2", GREEN, "#ffffff", 19)
    s += t(330, 200, "≥ 50 NM from base", 22, 800, RED)
    s += pill(600, 455, "TOTAL ≥ 150 NM", GOLD, INK, 24, stroke=GOLD_DARK)
    return s


@R.add(1429, "al-trial-logbook-48h", "Logbook Entries — Away From Base",
       template("AWAY FROM BASE: UPDATE THE LOGBOOK WITHIN 48 HOURS OF RETURNING",
                "ROUTINE ENTRIES OTHERWISE HAVE A 7-DAY WINDOW",
                [("AWAY FROM BASE", "Within 48 h after returning to base"),
                 ("ROUTINE", "Within 7 days")]), h=400)
def _():
    k = 840 / 7
    x0 = 200
    s = span(x0, x0 + 2 * k, 100, 70, "48 h", GOLD, INK, GOLD_DARK, 26)
    s += t(x0 + 2 * k + 20, 145, "away from base: from the RETURN to base", 21, 800, INK, "start")
    s += span(x0, x0 + 7 * k, 200, 60, "routine entries: 7 days", PANEL, MUTED, LINE)
    s += axis(x0, x0 + 7 * k, 310, [(x0 + d * k, f"day {d}") for d in range(0, 8)], 17)
    s += marker(x0, 80, 310, "", NAVY)
    s += t(x0 - 14, 136, "return\nto base", 19, 800, NAVY, "end")
    return s


@R.add(1400, "al-trial-flight-time", "Flight Time (Aeroplane)",
       template("FLIGHT TIME RUNS FROM FIRST MOVEMENT FOR TAKE-OFF TO COMING TO REST",
                "IT INCLUDES TAXI TIME — IT IS NOT JUST THE AIRBORNE TIME",
                [("STARTS", "When the aeroplane first moves under its own power for take-off"),
                 ("ENDS", "When it finally comes to rest at the end of the flight"),
                 ("NOT", "Engine start to shutdown, or lift-off to touchdown")]), h=470)
def _():
    ev = [(90, "engine\nstart"), (260, "first\nmovement"), (470, "lift-off"), (760, "touchdown"),
          (950, "comes to\nrest"), (1120, "engine\nshutdown")]
    s = axis(70, 1140, 300)
    for x, lab in ev:
        key = lab.startswith("first") or lab.startswith("comes")
        s += circle(x, 300, 11, GOLD if key else "#ffffff", GOLD_DARK if key else INK, 3)
        s += t(x, 345, lab, 19, 800 if key else 600, INK if key else MUTED)
    s += span(260, 950, 160, 70, "FLIGHT TIME", GOLD, INK, GOLD_DARK, 26)
    s += line(260, 230, 260, 290, GOLD_DARK, 3, None, "6 5") + line(950, 230, 950, 290, GOLD_DARK, 3, None, "6 5")
    s += span(470, 760, 245, 40, "airborne only", PANEL, MUTED, LINE, 18)
    s += path("M 470,120 Q 615,40 760,120", "none", BLUE, 3, dash="8 6")
    s += plane_side(615, 80, 0.7, BLUE)
    return s


# ------------------------------------------------------------------ rules of the air

@R.add(1028, "al-trial-head-on-turn-right", "Head-On Approach — Both Turn Right",
       template("HEAD-ON: BOTH AIRCRAFT ALTER HEADING TO THE RIGHT",
                "THEY PASS LEFT SIDE TO LEFT SIDE",
                [("WHY RIGHT", "One predictable response, so pilots never turn into each other"),
                 ("CONVERGING", "The aircraft with the other on its right gives way"),
                 ("OVERTAKING", "Overtake by altering heading to the right")]), h=460)
def _():
    s = rect(30, 30, 1140, 400, SKY, SKY, 0, 14)
    s += line(180, 230, 1020, 230, MUTED, 2, None, "10 8")
    s += plane_top(250, 230, 1.1, 90, NAVY)
    s += plane_top(950, 230, 1.1, -90, RED)
    s += path("M 330,230 C 450,230 520,260 560,360", "none", NAVY, 6, "navy")
    s += path("M 870,230 C 750,230 680,200 640,100", "none", RED, 6, "red")
    s += pill(470, 395, "turns RIGHT", NAVY, "#ffffff", 20)
    s += pill(730, 70, "turns RIGHT", RED, "#ffffff", 20)
    return s


@R.add(1093, "al-trial-built-up-areas", "Minimum Height Over Built-Up Areas",
       template("1000 FT ABOVE THE HIGHEST OBSTACLE WITHIN 2000 FT OF THE AIRCRAFT",
                "EXCEPT FOR TAKE-OFF, LANDING OR WITH WRITTEN APPROVAL",
                [("VERTICAL", "At least 1000 ft above the highest obstacle"),
                 ("RADIUS", "Obstacles within 2000 ft of the aircraft count"),
                 ("WHY", "Room to glide clear of the town if the engine fails")]), h=560)
def _():
    s = rect(0, 470, 1200, 90, GROUND, GROUND, 0, 0)
    import random
    rnd = random.Random(4)
    x = 120
    while x < 1080:
        w = rnd.randint(50, 80)
        h = rnd.randint(50, 130)
        s += rect(x, 470 - h, w, h, "#94a3b8", "#64748b", 2, 2)
        x += w + rnd.randint(6, 20)
    s += rect(560, 260, 30, 210, "#475569", INK, 2, 2)
    s += circle(575, 256, 8, RED, RED, 0)
    s += t(610, 300, "highest obstacle", 20, 800, RED, "start")
    s += plane_side(575, 110, 1.0, NAVY)
    s += dim(500, 128, 500, 256, "1000 ft", "navy", 22, side="left")
    s += line(575, 140, 575, 250, MUTED, 2, None, "6 6")
    s += dim(575, 510, 1000, 510, "2000 ft", "gold", 22, side="below")
    s += dim(150, 510, 575, 510, "2000 ft", "gold", 22, side="below")
    return s


@R.add(1407, "al-trial-over-water-rafts", "Over-Water Flight — Life Rafts",
       template("BEYOND 30 MIN AT CRUISE OR 50 NM FROM LAND — WHICHEVER IS LESS — CARRY LIFE RAFTS",
                "A FORCED LANDING THAT FAR OUT MEANS DITCHING AND WAITING FOR RESCUE",
                [("TRIGGER", "30 minutes at normal cruising speed or 50 NM, whichever is less"),
                 ("EQUIPMENT", "Life rafts and survival equipment for everyone on board")]), h=460)
def _():
    s = rect(0, 30, 1200, 400, "#bfdbfe", "#bfdbfe", 0, 0)
    s += path("M 0,30 L 230,30 C 260,120 200,200 250,280 C 290,350 230,400 260,430 L 0,430 Z", "#d9c7a3", "#a8956f", 3)
    s += t(110, 240, "LAND", 24, 800, INK)
    s += line(640, 30, 640, 430, RED, 4, None, "14 10")
    s += dim(260, 110, 640, 110, "30 min or 50 NM", "red", 22)
    s += t(450, 160, "whichever is LESS", 20, 800, RED)
    s += plane_top(900, 150, 1.0, 90, NAVY)
    s += rect(820, 270, 170, 80, "#f97316", "#c2410c", 4, 36)
    s += rect(845, 290, 120, 40, "#fdba74", "#c2410c", 2, 18)
    s += t(905, 390, "life rafts + survival equipment", 21, 800, INK)
    return s


# ------------------------------------------------------------------ VFR minima

def _vfr(band_text, plane_xy, rules, surface=False):
    s = rect(0, 0, 1200, 520, SKY, SKY, 0, 0)
    s += rect(0, 470, 1200, 50, GROUND, GROUND, 0, 0)
    s += pill(600, 34, band_text, NAVY, "#ffffff", 19)
    s += cloud(820, 200, 380, 140)
    s += plane_side(*plane_xy, 1.0, RED)
    s += rules
    if surface:
        s += line(plane_xy[0] + 20, plane_xy[1] + 20, plane_xy[0] + 160, 468, GREEN, 3, "green", "8 6")
    return s


@R.add(1062, "al-trial-vfr-minima-mid", "VFR Minima — 3000 ft AMSL / 1000 ft AGL to 10 000 ft",
       template("5 KM VISIBILITY, 1.5 KM HORIZONTALLY AND 1000 FT VERTICALLY FROM CLOUD",
                "ABOVE 3000 FT AMSL OR 1000 FT ABOVE TERRAIN (HIGHER OF THE TWO), BELOW 10 000 FT AMSL",
                [("VISIBILITY", "5 km flight visibility"),
                 ("HORIZONTAL", "1.5 km from cloud"),
                 ("VERTICAL", "1000 ft from cloud")]), h=520)
def _():
    rules = dim(330, 200, 625, 200, "1.5 km", "navy", 24)
    rules += dim(820, 290, 820, 420, "1000 ft", "navy", 24, side="right")
    rules += plane_side(820, 430, 0.8, RED)
    rules += pill(170, 420, "visibility 5 km", GOLD, INK, 22, stroke=GOLD_DARK)
    return _vfr("ABOVE 3000 FT AMSL / 1000 FT AGL, BELOW 10 000 FT AMSL", (260, 200), rules)


@R.add(1049, "al-trial-vfr-minima-low", "VFR Minima — Low Level, Uncontrolled Airspace",
       template("5 KM VISIBILITY, CLEAR OF CLOUD, SURFACE IN SIGHT",
                "CLASS F/G AT OR BELOW 3000 FT AMSL OR 1000 FT ABOVE TERRAIN, BY DAY",
                [("VISIBILITY", "5 km flight visibility (aeroplanes)"),
                 ("CLOUD", "Clear of cloud"),
                 ("SURFACE", "Ground or water in sight")]), h=520)
def _():
    rules = pill(1000, 420, "clear of cloud", "#ffffff", INK, 21, stroke=LINE)
    rules += pill(170, 120, "visibility 5 km", GOLD, INK, 22, stroke=GOLD_DARK)
    rules += t(420, 430, "surface in sight", 21, 800, GREEN, "start")
    return _vfr("CLASS F / G · AT OR BELOW 3000 FT AMSL OR 1000 FT AGL", (300, 330), rules, surface=True)


# ------------------------------------------------------------------ flight planning

@R.add(1061, "al-trial-flight-plan-30min", "Filing a Flight Plan — Lead Time",
       template("FILE AT LEAST 30 MINUTES BEFORE DEPARTURE",
                "FOR A DEPARTURE INTO CONTROLLED OR ADVISORY AIRSPACE, UNLESS THE ATSU AGREES OTHERWISE",
                [("DOMESTIC", "At least 30 min before departure"),
                 ("INTERNATIONAL", "At least 60 min before departure")]), h=400)
def _():
    k = 840 / 60
    x1 = 1060
    s = span(x1 - 30 * k, x1, 100, 70, "domestic: 30 min", GOLD, INK, GOLD_DARK, 24)
    s += span(x1 - 60 * k, x1, 200, 60, "international: 60 min", PANEL, MUTED, LINE)
    s += axis(x1 - 60 * k, x1, 310, [(x1 - m * k, f"−{m} min" if m else "0") for m in range(60, -1, -10)])
    s += marker(x1, 70, 310, "DEPARTURE", NAVY)
    s += pill(x1 - 30 * k, 60, "file by here", NAVY, "#ffffff", 19)
    return s


@R.add(1080, "al-trial-semicircular-rule", "Semi-Circular Rule",
       template("THE SEMI-CIRCULAR RULE APPLIES AT AND ABOVE 1500 FT AGL",
                "CRUISING LEVEL CHOSEN BY MAGNETIC TRACK, UNLESS ATC DIRECTS OTHERWISE",
                [("000° – 179°", "Odd thousands; VFR adds 500 ft (3500, 5500, 7500 …)"),
                 ("180° – 359°", "Even thousands; VFR adds 500 ft (4500, 6500, 8500 …)"),
                 ("BELOW 1500 FT AGL", "The rule does not apply")]), h=520)
def _():
    s = rect(40, 40, 560, 440, SKY, SKY, 0, 12)
    s += rect(40, 420, 560, 60, GROUND, GROUND, 0, 0)
    s += line(40, 250, 600, 250, RED, 4, None, "14 10")
    s += t(60, 238, "1500 ft AGL", 22, 800, RED, "start")
    s += t(320, 160, "semi-circular rule applies", 22, 800, NAVY)
    s += plane_side(320, 110, 0.8, NAVY)
    s += t(320, 330, "below: rule not required", 21, 700, MUTED)
    cx, cy, r = 900, 260, 190
    s += path(f"M {cx},{cy - r} A {r} {r} 0 0 1 {cx},{cy + r} Z", BLUE_SOFT, BLUE, 3)
    s += path(f"M {cx},{cy + r} A {r} {r} 0 0 1 {cx},{cy - r} Z", GOLD_SOFT, GOLD_DARK, 3)
    s += t(cx, cy - r - 14, "000°", 20, 800, INK)
    s += t(cx, cy + r + 30, "180°", 20, 800, INK)
    s += t(cx + 95, cy - 20, "ODD", 30, 800, BLUE)
    s += t(cx + 95, cy + 14, "+ 500 ft", 20, 800, BLUE)
    s += t(cx + 95, cy + 44, "3500, 5500", 18, 700, BODY)
    s += t(cx - 95, cy - 20, "EVEN", 30, 800, GOLD_DARK)
    s += t(cx - 95, cy + 14, "+ 500 ft", 20, 800, GOLD_DARK)
    s += t(cx - 95, cy + 44, "4500, 6500", 18, 700, BODY)
    s += t(cx, 30, "VFR, magnetic track", 20, 800, NAVY)
    return s


# ------------------------------------------------------------------ medical, definitions, documents

@R.add(1086, "al-trial-scuba-24h", "Scuba Diving and Flying",
       template("NO FLIGHT CREW DUTIES WITHIN 24 HOURS OF SCUBA DIVING",
                "DISSOLVED NITROGEN CAN FORM BUBBLES AT LOWER CABIN PRESSURE",
                [("RISK", "Decompression sickness ('the bends') at altitude"),
                 ("RULE", "Wait at least 24 hours after diving before acting as crew")]), h=420)
def _():
    s = rect(60, 80, 220, 260, "#bfdbfe", "#60a5fa", 3, 14)
    s += t(170, 130, "DIVE", 26, 800, NAVY)
    for (x, y, r) in [(130, 220, 14), (170, 260, 10), (210, 200, 18), (160, 300, 8), (220, 280, 12)]:
        s += circle(x, y, r, "#ffffff", "#2563eb", 3)
    s += span(300, 900, 170, 80, "NO FLIGHT CREW DUTIES · 24 h", RED_SOFT, RED, RED, 24)
    s += arrow(910, 210, 960, 210, "green", 5)
    s += rect(970, 140, 180, 140, GREEN_SOFT, GREEN, 3, 14)
    s += t(1060, 220, "may fly", 24, 800, GREEN)
    s += axis(300, 900, 330, [(300, "0 h"), (600, "12 h"), (900, "24 h")])
    return s


@R.add(1019, "al-trial-night-definition", "Definition of Night",
       template("NIGHT = 15 MIN AFTER SUNSET TO 15 MIN BEFORE SUNRISE",
                "THE MIRROR IMAGE OF THE DEFINITION OF DAY",
                [("STARTS", "Sunset + 15 minutes"),
                 ("ENDS", "Sunrise − 15 minutes"),
                 ("WHY IT MATTERS", "Flying in this window needs a night rating")]), h=440)
def _():
    s = rect(60, 140, 300, 110, SKY, LINE, 2, 0)
    s += rect(360, 140, 50, 110, "#fdba74", "#fdba74", 0, 0)
    s += rect(410, 140, 380, 110, NAVY, NAVY, 0, 0)
    s += rect(790, 140, 50, 110, "#fdba74", "#fdba74", 0, 0)
    s += rect(840, 140, 300, 110, SKY, LINE, 2, 0)
    s += t(210, 205, "DAY", 26, 800, INK)
    s += t(600, 205, "NIGHT", 30, 800, "#ffffff")
    s += t(990, 205, "DAY", 26, 800, INK)
    for cx in (220, 300, 520, 680):
        s += circle(cx + 30 if cx > 400 else -100, 165, 3, "#ffffff", "#ffffff", 0)
    s += sun(360, 100, 22)
    s += sun(840, 100, 22)
    s += t(360, 52, "sunset", 20, 800, GOLD_DARK)
    s += t(840, 52, "sunrise", 20, 800, GOLD_DARK)
    s += line(410, 130, 410, 300, RED, 4)
    s += line(790, 130, 790, 300, RED, 4)
    s += pill(410, 330, "sunset + 15 min", RED, "#ffffff", 20)
    s += pill(790, 330, "sunrise − 15 min", RED, "#ffffff", 20)
    s += t(385, 400, "15 min", 18, 700, MUTED)
    s += t(815, 400, "15 min", 18, 700, MUTED)
    return s


@R.add(1034, "al-trial-documents-domestic", "Documents Carried on a Domestic Flight",
       template("RELEASE TO SERVICE, CERTIFICATE OF REGISTRATION, PILOT'S LICENCE",
                "ORIGINALS OR CERTIFIED COPIES — DOMESTIC FLIGHTS INCLUDED",
                [("RELEASE TO SERVICE", "Proves the aircraft is airworthy after maintenance"),
                 ("REGISTRATION", "Proves who the aircraft is"),
                 ("LICENCE", "Proves the pilot is qualified")]), h=420)
def _():
    s = doc(60, 50, 320, 300, "Certificate of", "release to service")
    s += doc(440, 50, 320, 300, "Certificate of", "registration")
    s += doc(820, 50, 320, 300, "Pilot's", "licence")
    s += t(600, 400, "Carry originals or certified copies on board.", 22, 700, BODY)
    return s


@R.add(1401, "al-trial-child-passenger", "Passenger Age Categories",
       template("CHILD = FROM THE 2ND BIRTHDAY UP TO 12 YEARS",
                "UNDER 2 IS AN INFANT; FROM 12 THE PASSENGER IS TREATED AS AN ADULT",
                [("INFANT", "Under 2 years"),
                 ("CHILD", "2 to 12 years"),
                 ("ADULT", "12 years and older")]), h=340)
def _():
    k = 60
    x0 = 120
    s = span(x0, x0 + 2 * k, 110, 90, "INFANT", BLUE_SOFT, BLUE, BLUE, 20)
    s += span(x0 + 2 * k, x0 + 12 * k, 110, 90, "CHILD", GOLD, INK, GOLD_DARK, 30)
    s += span(x0 + 12 * k, x0 + 16 * k, 110, 90, "ADULT", PANEL, MUTED, LINE, 24)
    s += axis(x0, x0 + 16 * k, 250, [(x0 + a * k, str(a)) for a in (0, 2, 4, 6, 8, 10, 12, 14, 16)])
    s += t(x0 + 16 * k + 20, 257, "years", 19, 700, MUTED, "start")
    return s


@R.add(1383, "al-trial-empty-mass", "What Empty Mass Includes",
       template("EMPTY MASS = AIRFRAME + FIXED EQUIPMENT + UNUSABLE FUEL + ALL OIL, COOLANT, HYDRAULIC FLUID",
                "EVERYTHING THAT STAYS IN THE AIRCRAFT; PAYLOAD AND USABLE FUEL ARE ADDED PER FLIGHT",
                [("INCLUDED", "Coolant, unusable fuel, total oil, total hydraulic fluid, fixed ballast, fixed equipment"),
                 ("NOT INCLUDED", "Usable fuel, crew, passengers, baggage")]), h=520)
def _():
    segs = [(230, NAVY, "#ffffff", "EMPTY MASS"), (70, BLUE, "#ffffff", "usable fuel"),
            (70, GOLD, INK, "crew + passengers"), (40, GOLD_SOFT, INK, "baggage")]
    y = 470
    s = ""
    for h, f, c, lab in segs:
        s += rect(70, y - h, 230, h, f, "#ffffff", 3, 0)
        s += t(185, y - h / 2 + 8, lab, 21 if lab != "EMPTY MASS" else 24, 800, c)
        y -= h
    s += t(185, y - 16, "take-off mass", 20, 800, INK)
    s += card(360, 50, 380, 420, "Included", "airframe & engine\nfixed equipment\nfixed ballast\nunusable fuel\n"
                                              "total oil\ntotal hydraulic fluid\nengine coolant", GREEN, GREEN_SOFT,
              24, 22)
    s += card(780, 50, 380, 420, "Not included", "usable fuel\ncrew\npassengers\nbaggage and cargo", RED, RED_SOFT,
              24, 22)
    return s
