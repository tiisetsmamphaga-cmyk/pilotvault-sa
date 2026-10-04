"""Flight Planning trial-mock diagrams (25). Table values are copied from the SACAA-01 PPL Flight Planning Manual."""
import math

from common import Registry, band, dot, graph, interp, steps, tag, trace
from kit import (BLUE, BLUE_SOFT, BODY, GOLD, GOLD_DARK, GOLD_SOFT, GREEN, GREEN_SOFT, GROUND, INK, LINE, MUTED, NAVY,
                 PANEL, RED, RED_SOFT, arrow, card, circle, dim, line, path, pill, plane_side, plane_top, poly, rect,
                 t, table, template)

R = Registry("flight-planning", "/explanation-images/flight-planning/trial-v1")


# ------------------------------------------------------------------ manual graphs

@R.add(2305, "fp-fig-1-7-climb-rate", "Figure 1-7 — Reading the Rate of Climb",
       template("ENTER AT THE TEMPERATURE, UP TO THE ALTITUDE, ACROSS, THEN DOWN",
                "OAT +10°C AT PRESSURE ALTITUDE 4000 FT GIVES ABOUT 540 FT/MIN",
                [("STEP 1", "Enter the OAT scale at +10°C and go up to the 4000 ft pressure-altitude line"),
                 ("STEP 2", "Go straight across to the rate-of-climb line"),
                 ("STEP 3", "Drop down to the RATE OF CLIMB scale: about 540 ft/min")]), h=920)
def _():
    s, P = graph("fig-1-7.png", 0, 0, 1200, 830)
    pts = [P(354, 930), P(354, 640), P(1161, 640), P(1161, 930)]
    s += trace(pts)
    s += dot(P(354, 640)) + dot(P(1161, 640))
    x, y = P(1161, 930)
    s += tag(x + 95, y - 60, "≈ 540 fpm")
    x, y = P(354, 640)
    s += tag(x + 110, y - 34, "4000 ft line", 19, "#ffffff")
    s += steps(880, ["Enter at +10°C", "Up to the 4000 ft line", "Across to the climb line", "Down: ≈ 540 ft/min"])
    return s


@R.add(2312, "fp-fig-1-8-climb-distance", "Figure 1-8 — Distance to Climb Is a Difference",
       template("THE CHART IS CUMULATIVE FROM SEA LEVEL: READ TWICE AND SUBTRACT",
                "TOP-OF-CLIMB READING MINUS THE DEPARTURE READING",
                [("DEPARTURE", "PA = 1380 + (1013 − 1009) × 30 = 1500 ft at +12°C → about 4 NM"),
                 ("CRUISE", "PA 7500 ft, ISA+12 = 0 + 12 = +12°C → about 24 NM"),
                 ("CLIMB DISTANCE", "24 − 4 ≈ 20 NM")],
                "Climb distance = cruise reading − departure reading"), h=920)
def _():
    s, P = graph("fig-1-8.png", 0, 0, 1200, 830)
    s += trace([P(364, 930), P(364, 825), P(726, 825), P(726, 930)], "blue")
    s += trace([P(364, 930), P(364, 376), P(984, 376), P(984, 930)])
    s += dot(P(364, 825), BLUE) + dot(P(726, 825), BLUE) + dot(P(364, 376)) + dot(P(984, 376))
    x, y = P(726, 880)
    s += tag(x - 80, y, "≈ 4 NM", 21, BLUE_SOFT)
    x, y = P(984, 880)
    s += tag(x + 82, y, "≈ 24 NM", 21)
    x, y = P(364, 825)
    s += tag(x + 60, y - 28, "1500 ft", 18, "#ffffff")
    x, y = P(364, 376)
    s += tag(x + 60, y - 28, "7500 ft", 18, "#ffffff")
    s += steps(880, ["Departure: +12°C, 1500 ft", "Cruise: +12°C, 7500 ft", "Read DISTANCE twice", "24 − 4 ≈ 20 NM"])
    return s


def _fuel_x(y):  # Figure 1-15 fuel line runs from (552, 940) to (620, 158) in figure pixels
    return 552 + 68 * (940 - y) / 782


@R.add(2239, "fp-fig-1-15-descent-fuel", "Figure 1-15 — Fuel to Descend Is a Difference",
       template("READ THE CRUISE CONDITION AND THE DESTINATION CONDITION, THEN SUBTRACT",
                "THE DESCENT CHART IS CUMULATIVE FROM SEA LEVEL",
                [("CRUISE", "9000 ft at +16°C → about 4 USG"),
                 ("DESTINATION", "4000 ft at ISA (15 − 8 = +7°C) → about 2 USG"),
                 ("FUEL TO DESCEND", "4 − 2 = 2 USG")],
                "Descent fuel = cruise reading − destination reading"), h=930)
def _():
    s, P = graph("fig-1-15.png", 0, 0, 1200, 830)
    xc, xd = _fuel_x(370), _fuel_x(677)
    s += trace([P(334.5, 940), P(334.5, 677), P(xd, 677), P(xd, 940)], "blue")
    s += trace([P(394, 940), P(394, 370), P(xc, 370), P(xc, 940)])
    s += dot(P(334.5, 677), BLUE) + dot(P(xd, 677), BLUE) + dot(P(394, 370)) + dot(P(xc, 370))
    x, y = P(xc, 370)
    s += tag(x + 105, y, "≈ 4 USG", 21)
    x, y = P(xd, 677)
    s += tag(x + 105, y, "≈ 2 USG", 21, BLUE_SOFT)
    s += steps(890, ["Cruise: +16°C, 9000 ft", "Destination: +7°C, 4000 ft", "Read FUEL twice", "4 − 2 = 2 USG"])
    return s


@R.add(2250, "fp-fig-1-16-glide-range", "Figure 1-16 — Glide Range From Height Above Terrain",
       template("ENTER WITH THE HEIGHT AVAILABLE, NOT THE CRUISING ALTITUDE",
                "10 500 FT − 1500 FT TERRAIN = 9000 FT OF HEIGHT → ABOUT 19 NM",
                [("HEIGHT AVAILABLE", "Cruising pressure altitude − terrain pressure altitude"),
                 ("READ", "Across from 9000 ft to the glide line, then down to the NM scale"),
                 ("CONDITIONS", "Power off, flaps 0°, 75 KIAS, 2500 lb, zero wind")]), h=880)
def _():
    s, P = graph("fig-1-16.png", 0, 0, 1200, 790)
    s += trace([P(118, 347), P(1277, 347), P(1277, 932)])
    s += dot(P(1277, 347))
    x, y = P(118, 347)
    s += tag(x + 140, y - 30, "9000 ft available", 19, "#ffffff")
    x, y = P(1277, 932)
    s += tag(x - 95, y - 50, "≈ 19 NM", 22)
    s += steps(845, ["10 500 − 1500 = 9000 ft", "Across to the glide line", "Down to the NM scale", "≈ 19 NM"])
    return s


# ------------------------------------------------------------------ tables

@R.add(2291, "fp-fig-1-19-airspeed-calibration", "Figure 1-19 — Interpolating the Calibration Table",
       template("77 KIAS LIES 7/10 OF THE WAY FROM 70 TO 80 — SO DOES THE KCAS",
                "FLAPS 40° ROW: 70 KIAS = 71 KCAS, 80 KIAS = 81 KCAS",
                [("FRACTION", "(77 − 70) ÷ (80 − 70) = 0.7"),
                 ("APPLY", "71 + 0.7 × (81 − 71) = 71 + 7 = 78 KCAS")],
                "KCAS = 71 + 0.7 × 10 = 78 KCAS"), h=600)
def _():
    s = t(600, 50, "FIGURE 1-19 · AIRSPEED CALIBRATION · FLAPS 40°", 24, 800, NAVY)
    cols = [140] + [100] * 9
    rows = [["KIAS", "40", "50", "60", "70", "80", "90", "100", "110", "120"],
            ["KCAS", "45", "54", "62", "71", "81", "91", "101", "111", "122"]]
    s += table(80, 80, cols, rows, hl={(0, 4), (0, 5), (1, 4), (1, 5)}, head_rows=0, row_h=58, size=24,
               hl_ring=[(0, 4), (0, 5), (1, 4), (1, 5)])
    s += t(150, 316, "KIAS", 24, 800, NAVY, "end")
    s += interp(200, 308, 800, "70", "80", 0.7, bottom=("70", "77", "80"))
    s += t(150, 476, "KCAS", 24, 800, NAVY, "end")
    s += interp(200, 468, 800, "71", "81", 0.7, bottom=("71", "78", "81"))
    s += line(760, 380, 760, 440, GOLD_DARK, 3, "gold", "6 6")
    s += t(1060, 400, "0.7 of\nthe gap", 20, 700, MUTED, "start")
    return s


@R.add(2290, "fp-fig-1-21-stall-speeds", "Figure 1-21 — Interpolating Between Weights",
       template("2300 LB IS HALFWAY BETWEEN THE 2400 LB AND 2200 LB ROWS",
                "FLAPS 40°, 60° BANK: 60 KIAS AT 2400 LB AND 54 KIAS AT 2200 LB",
                [("READ", "KIAS column under 60° bank, on both flaps-40° rows"),
                 ("INTERPOLATE", "(60 + 54) ÷ 2 = 57 KIAS"),
                 ("REMEMBER", "Stall speed rises with weight and with angle of bank")],
                "Stall speed = (60 + 54) ÷ 2 = 57 KIAS"), h=580)
def _():
    x0 = 100
    cols = [130, 110] + [95] * 8
    s = band(x0, 30, [240, 190, 190, 190, 190], ["", "0° BANK", "30° BANK", "45° BANK", "60° BANK"], h=40)
    rows = [["WEIGHT", "FLAP"] + ["KIAS", "KCAS"] * 4,
            ["2400", "UP", "48", "54", "52", "58", "58", "64", "68", "76"],
            ["", "10°", "45", "52", "48", "56", "54", "60", "64", "74"],
            ["", "40°", "42", "48", "46", "52", "50", "56", "60", "68"],
            ["2200", "UP", "44", "52", "48", "54", "52", "58", "60", "68"],
            ["", "10°", "42", "48", "46", "52", "50", "56", "56", "64"],
            ["", "40°", "40", "46", "44", "50", "48", "54", "54", "62"]]
    s += table(x0, 70, cols, rows, hl={(3, 1), (6, 1), (3, 8), (6, 8)}, row_h=44, size=20, hl_ring=[(3, 8), (6, 8)])
    s += interp(250, 470, 700, "60", "54", 0.5, top=("2400 lb", "2300 lb", "2200 lb"), bottom=("60", "57 KIAS", "54"))
    return s


TO_HEAD = ["PA (FT)", "GND ROLL", "TO 50 FT", "GND ROLL", "TO 50 FT", "GND ROLL", "TO 50 FT"]
TO_ROWS = [["3000", "1110", "1985", "1190", "2125", "1280", "2275"],
           ["4000", "1220", "2185", "1310", "2345", "1405", "2515"],
           ["5000", "1340", "2415", "1440", "2595", "1550", "2790"]]


def _to_table(hl, ring):
    s = t(600, 34, "FIGURE 1-22 · TAKE-OFF · 2400 LB, FLAPS UP, PAVED DRY RUNWAY, ZERO WIND", 21, 800, NAVY)
    s += band(75, 56, [150, 300, 300, 300], ["", "+10°C", "+20°C", "+30°C"], h=40)
    s += table(75, 96, [150] * 7, [TO_HEAD] + TO_ROWS, hl=hl, row_h=50, size=21, hl_ring=ring)
    return s


@R.add(2247, "fp-fig-1-22-takeoff-distance", "Figure 1-22 — Distance to Clear 50 ft",
       template("+15°C IS HALFWAY BETWEEN THE +10°C AND +20°C COLUMNS",
                "PA 4000 FT, TOTAL TO CLEAR 50 FT: 2185 FT AT +10°C AND 2345 FT AT +20°C",
                [("ROW", "Pressure altitude 4000 ft"),
                 ("COLUMN", "TOTAL TO CLEAR 50 FT (not ground roll)"),
                 ("CORRECTIONS", "No wind or grass correction is given, so none applies")],
                "(2185 + 2345) ÷ 2 = 2265 ft"), h=560)
def _():
    s = _to_table({(2, 2), (2, 4)}, [(2, 2), (2, 4)])
    s += interp(250, 420, 700, "2185", "2345", 0.5, top=("+10°C", "+15°C", "+20°C"), bottom=("2185", "2265 ft", "2345"))
    return s


@R.add(2320, "fp-fig-1-22-ground-roll-tailwind", "Figure 1-22 — Ground Roll With a Tailwind",
       template("INTERPOLATE FIRST, THEN APPLY THE WIND NOTE",
                "TAILWIND: +10% FOR EACH 2 KT, SO 4 KT ADDS 20%",
                [("ROW", "PA 3500 ft is halfway between 3000 ft and 4000 ft"),
                 ("GROUND ROLL AT +20°C", "(1190 + 1310) ÷ 2 = 1250 ft"),
                 ("TAILWIND 4 KT", "1250 × 1.20 = 1500 ft")],
                "1250 × 1.20 = 1500 ft"), h=600)
def _():
    s = _to_table({(1, 3), (2, 3)}, [(1, 3), (2, 3)])
    s += interp(120, 440, 520, "1190", "1310", 0.5, top=("PA 3000", "PA 3500", "PA 4000"), bottom=("1190", "1250 ft", "1310"))
    s += arrow(700, 440, 790, 440, "red", 5)
    s += card(810, 380, 350, 150, "4 kt tailwind: +20%", "1250 × 1.20\n= 1500 ft ground roll", RED, hl=True,
              head_size=22, body_size=22)
    return s


CR_HEAD = ["PA (FT)", "RPM", "% BHP", "KTAS", "GPH", "ENDUR. (h)", "RANGE (nm)"]
CR_COLS = [140, 130, 130, 130, 130, 180, 180]


def _cruise(rows, hl, ring):
    s = t(600, 34, "FIGURE 1-23 · CRUISE PERFORMANCE · 2300 LB, MIXTURE LEANED, ZERO WIND", 21, 800, NAVY)
    s += table(90, 56, CR_COLS, [CR_HEAD] + rows, hl=hl, row_h=44, size=20, hl_ring=ring)
    return s


@R.add(2252, "fp-fig-1-23-endurance", "Figure 1-23 — Endurance Between Two Altitudes",
       template("PA 9000 FT IS HALFWAY BETWEEN THE 8000 FT AND 10 000 FT BLOCKS",
                "2400 RPM ENDURANCE: 6.8 H AT 8000 FT AND 7.6 H AT 10 000 FT",
                [("READ", "The 2400 RPM line in each altitude block, ENDURANCE column"),
                 ("INTERPOLATE", "(6.8 + 7.6) ÷ 2 = 7.2 hours"),
                 ("NOTE", "Based on 48 USG usable fuel, no reserve")],
                "(6.8 + 7.6) ÷ 2 = 7.2 h"), h=560)
def _():
    rows = [["8000", "2600", "69", "119", "7.5", "6.1", "800"],
            ["", "2500", "66", "115", "7.2", "6.3", "810"],
            ["", "2400", "60", "108", "6.8", "6.8", "820"],
            ["10 000", "2600", "62", "113", "6.9", "6.6", "830"],
            ["", "2500", "56", "105", "6.5", "7.1", "825"],
            ["", "2400", "50", "95", "6.1", "7.6", "805"]]
    s = _cruise(rows, {(3, 1), (6, 1), (3, 5), (6, 5)}, [(3, 5), (6, 5)])
    s += interp(250, 440, 700, "6.8", "7.6", 0.5, top=("PA 8000", "PA 9000", "PA 10 000"), bottom=("6.8 h", "7.2 h", "7.6 h"))
    return s


@R.add(2337, "fp-fig-1-23-ktas", "Figure 1-23 — True Airspeed Between Two Altitudes",
       template("PA 7000 FT IS HALFWAY BETWEEN THE 6000 FT AND 8000 FT BLOCKS",
                "2600 RPM: 123 KTAS AT 6000 FT AND 119 KTAS AT 8000 FT",
                [("READ", "The 2600 RPM line in each altitude block, KTAS column"),
                 ("INTERPOLATE", "(123 + 119) ÷ 2 = 121 KTAS")],
                "(123 + 119) ÷ 2 = 121 KTAS"), h=560)
def _():
    rows = [["6000", "2600", "77", "123", "8.3", "5.5", "745"],
            ["", "2500", "70", "117", "7.6", "6.0", "780"],
            ["", "2400", "63", "111", "7.0", "6.5", "790"],
            ["8000", "2600", "69", "119", "7.5", "6.1", "800"],
            ["", "2500", "66", "115", "7.2", "6.3", "810"],
            ["", "2400", "60", "108", "6.8", "6.8", "820"]]
    s = _cruise(rows, {(1, 1), (4, 1), (1, 3), (4, 3)}, [(1, 3), (4, 3)])
    s += interp(250, 440, 700, "123", "119", 0.5, top=("PA 6000", "PA 7000", "PA 8000"), bottom=("123", "121 KTAS", "119"))
    return s


@R.add(2389, "fp-fig-1-24-landing-distance", "Figure 1-24 — Landing Distance in Two Steps",
       template("CONVERT TO PRESSURE ALTITUDE, THEN INTERPOLATE ALTITUDE AND TEMPERATURE",
                "PA = 2650 + (1013 − 1018) × 30 = 2500 FT",
                [("PA 2500 FT", "Halfway row: 1367.5 ft at +20°C and 1402.5 ft at +30°C"),
                 ("+24°C", "0.4 of the way from +20°C to +30°C"),
                 ("RESULT", "1367.5 + 0.4 × 35 = 1381.5 ≈ 1382 ft")],
                "1367.5 + 0.4 × 35 ≈ 1382 ft"), h=600)
def _():
    s = pill(600, 40, "PA = 2650 + (1013 − 1018) × 30 = 2500 ft", NAVY, "#ffffff", 22)
    x0 = 155
    s += band(x0, 90, [170, 360, 360], ["", "+20°C", "+30°C"], h=40)
    rows = [["PA (FT)", "GND ROLL", "TO 50 FT", "GND ROLL", "TO 50 FT"],
            ["2000", "575", "1350", "595", "1385"],
            ["2500 *", "585", "1367.5", "605", "1402.5"],
            ["3000", "595", "1385", "615", "1420"]]
    s += table(x0, 130, [170, 180, 180, 180, 180], rows, hl={(2, 0), (2, 2), (2, 4)}, row_h=50, size=21,
               hl_ring=[(2, 2), (2, 4)])
    s += t(x0, 360, "* halfway between the 2000 ft and 3000 ft rows", 18, 400, MUTED, "start", italic=True)
    s += interp(250, 460, 700, "1367.5", "1402.5", 0.4, top=("+20°C", "+24°C", "+30°C"),
                bottom=("1367.5", "≈ 1382 ft", "1402.5"))
    return s


# ------------------------------------------------------------------ concept diagrams

@R.add(2374, "fp-density-altitude-ladder", "Density Altitude — Worked Example",
       template("DENSITY ALTITUDE ≈ 4560 FT",
                "THE AEROPLANE PERFORMS AS IF IT WERE 1350 FT HIGHER THAN THE AERODROME",
                [("PRESSURE ALTITUDE", "3210 + (1013 − 1020) × 30 = 3000 ft"),
                 ("ISA DEVIATION", "ISA at 3000 ft = 15 − 6 = +9°C, so 22 − 9 = +13°C"),
                 ("DENSITY ALTITUDE", "3000 + 120 × 13 = 4560 ft")],
                "DA = PA + 120 × (OAT − ISA temp)"), h=600)
def _():
    def yv(ft):
        return 530 - (ft - 2500) * 0.18
    s = line(160, yv(2500), 160, yv(5000), INK, 4)
    for ft in range(2500, 5001, 500):
        s += line(150, yv(ft), 170, yv(ft), INK, 3)
        s += t(138, yv(ft) + 7, f"{ft}", 19, 600, MUTED, "end")
    for ft, lab, col in [(3210, "Aerodrome elevation 3210 ft", MUTED), (3000, "Pressure altitude 3000 ft", NAVY),
                         (4560, "Density altitude 4560 ft", RED)]:
        s += line(160, yv(ft), 460, yv(ft), col, 3, None, "8 6" if ft == 3210 else None)
        s += circle(160, yv(ft), 9, col, col, 0)
        s += t(186, yv(ft) - 10 + (34 if ft == 3000 else 0), lab, 21, 800, col, "start")
    s += arrow(500, yv(3000), 500, yv(4560) + 6, "red", 5)
    s += t(512, (yv(3000) + yv(4560)) / 2 + 8, "+1560 ft", 22, 800, RED, "start")
    s += card(640, 60, 520, 130, "1  Pressure altitude", "3210 + (1013 − 1020) × 30\n= 3210 − 210 = 3000 ft", NAVY)
    s += card(640, 210, 520, 130, "2  ISA deviation", "ISA at 3000 ft = 15 − 2 × 3 = +9°C\nOAT 22°C → ISA +13°C", NAVY)
    s += card(640, 360, 520, 130, "3  Density altitude", "3000 + 120 × 13\n= 3000 + 1560 = 4560 ft", RED, hl=True)
    return s


@R.add(2240, "fp-density-altitude-climb", "High Density Altitude Reduces Climb Performance",
       template("HIGHER DENSITY ALTITUDE = THINNER AIR = POORER CLIMB",
                "HOT, HIGH AND LOW-PRESSURE DAYS ALL RAISE DENSITY ALTITUDE",
                [("ENGINE", "Less air mass per stroke, so less power"),
                 ("PROPELLER", "Less thrust from the thinner air"),
                 ("WING", "Higher TAS needed for the same lift; longer take-off and landing runs")]), h=640)
def _():
    s = rect(0, 520, 1200, 120, GROUND, GROUND, 0, 0)
    s += rect(60, 505, 380, 18, "#475569", INK, 2, 2)
    s += path("M 240,512 L 1060,140", "none", BLUE, 6, "blue")
    s += path("M 240,512 L 1060,400", "none", RED, 6, "red")
    s += plane_side(1000, 167, 1.0, BLUE, pitch=24)
    s += plane_side(1000, 408, 1.0, RED, pitch=8)
    s += t(60, 80, "LOW density altitude — cold, low elevation, high pressure", 22, 800, BLUE, "start")
    s += t(60, 112, "dense air: full power, thrust and lift → steep climb", 20, 600, BODY, "start")
    s += t(60, 572, "HIGH density altitude — hot, high elevation, low pressure", 22, 800, RED, "start")
    s += t(60, 606, "thin air: less power, less thrust, less lift → shallow climb", 20, 700, INK, "start")
    return s


@R.add(2264, "fp-windshear-headwind-increase", "Wind Shear on Final — Sudden Headwind Increase",
       template("A SUDDEN HEADWIND INCREASE MAKES THE AIRCRAFT OVERSHOOT",
                "IAS AND LIFT JUMP, SO THE AIRCRAFT BALLOONS ABOVE THE GLIDE PATH",
                [("HEADWIND ↑ (OR TAILWIND ↓)", "IAS ↑ → lift ↑ → above the path → overshoot"),
                 ("HEADWIND ↓ (OR TAILWIND ↑)", "IAS ↓ → lift ↓ → below the path → undershoot"),
                 ("RECOVERY", "Smooth, positive corrections — don't chase the airspeed")]), h=580)
def _():
    s = rect(0, 480, 1200, 100, GROUND, GROUND, 0, 0)
    s += rect(760, 466, 400, 16, "#475569", INK, 2, 2)
    s += line(60, 150, 880, 474, GREEN, 4, None, "14 10")
    s += t(200, 160, "Intended glide path", 21, 800, GREEN, "start")
    s += path("M 380,277 C 520,250 640,270 760,330 C 850,375 930,430 1040,470", "none", RED, 6, "red")
    s += plane_side(380, 277, 0.95, NAVY, pitch=-20)
    s += circle(840, 474, 10, GREEN, GREEN, 0)
    s += t(840, 520, "aim point", 19, 700, GREEN)
    s += t(1040, 520, "lands long", 19, 800, RED)
    for i, (y, ln) in enumerate([(70, 90), (110, 150), (150, 210)]):
        s += arrow(1150, y, 1150 - ln, y, "blue", 4 + i * 2)
    s += t(1150, 200, "sudden headwind increase", 20, 800, BLUE, "end")
    s += pill(600, 120, "IAS ↑  →  lift ↑  →  balloons above the path", RED_SOFT, RED, 21, stroke=RED)
    return s


def _vortex(x, y, r=22):
    s = circle(x, y, r, "none", RED, 3)
    s += circle(x, y, r * 0.5, "none", RED, 2)
    s += path(f"M {x + r},{y} l -6,-10 M {x + r},{y} l 8,-8", "none", RED, 3)
    return s


@R.add(2363, "fp-wake-landing-behind-heavy", "Landing Behind a Heavy Aircraft",
       template("TOUCH DOWN BEYOND THE HEAVY AIRCRAFT'S TOUCHDOWN POINT",
                "WAKE VORTICES STOP ONCE THE HEAVY AIRCRAFT'S WEIGHT IS ON THE RUNWAY",
                [("APPROACH", "Stay at or above the heavy aircraft's flight path"),
                 ("TOUCHDOWN", "Land beyond the point where it touched down"),
                 ("VORTICES", "Sink below the path and drift with the wind")]), h=560)
def _():
    s = rect(0, 440, 1200, 130, GROUND, GROUND, 0, 0)
    s += rect(240, 426, 920, 16, "#475569", INK, 2, 2)
    s += line(40, 140, 560, 432, MUTED, 4, None, "12 9")
    for x in (180, 300, 420):
        _vy = 140 + (x - 40) * 292 / 520 + 46
        s += _vortex(x, _vy, 20)
    s += t(40, 545, "Wake vortices sink below the heavy aircraft's path", 20, 800, RED, "start")
    s += line(560, 396, 560, 436, INK, 5)
    s += pill(560, 478, "heavy touchdown", NAVY, "#ffffff", 18)
    s += path("M 40,60 L 560,330 L 830,432", "none", GREEN, 6, "green")
    s += plane_side(250, 169, 0.9, GREEN, pitch=-27)
    s += pill(860, 478, "light aircraft touches down beyond", GREEN, "#ffffff", 18)
    s += line(700, 70, 760, 70, MUTED, 4, None, "12 9")
    s += t(775, 77, "heavy aircraft's approach path", 20, 700, BODY, "start")
    s += line(700, 112, 760, 112, GREEN, 6)
    s += t(775, 119, "light aircraft: at or above it, land beyond", 20, 700, BODY, "start")
    return s


@R.add(2332, "fp-fuel-required-stack", "Total Fuel Required — Build It Up",
       template("TOTAL FUEL = TAXI/TAKE-OFF/CLIMB + CRUISE + RESERVE",
                "3 + 8.37 + 8 = 19.4 USG",
                [("TIME", "107 NM ÷ 92 kt = 1.163 h (69.8 min)"),
                 ("CRUISE FUEL", "1.163 h × 7.2 USG/h = 8.37 USG"),
                 ("ADD", "3 USG taxi/take-off/climb + 8 USG reserve")],
                "3 + 8.37 + 8 = 19.4 USG"), h=580)
def _():
    s = card(40, 60, 520, 150, "1  Flight time", "107 NM ÷ 92 kt = 1.163 h\n= 69.8 min", NAVY)
    s += card(40, 230, 520, 150, "2  Cruise fuel", "1.163 h × 7.2 USG/h\n= 8.37 USG", NAVY)
    s += card(40, 400, 520, 130, "3  Add the fixed amounts", "taxi/take-off/climb 3 + reserve 8", NAVY)
    base, k = 530, 21
    segs = [(3, BLUE, "Taxi, take-off & climb  3 USG"), (8.37, NAVY, "Cruise  8.37 USG"), (8, GOLD, "Reserve  8 USG")]
    y = base
    for v, col, lab in segs:
        h = v * k
        s += rect(640, y - h, 150, h, col, "#ffffff", 3, 0)
        s += t(812, y - h / 2 + 8, lab, 21, 800, INK, "start")
        y -= h
    s += line(630, y, 800, y, INK, 3)
    s += tag(715, y - 34, "TOTAL 19.4 USG", 22)
    return s


@R.add(2265, "fp-fuel-volume-to-mass", "Fuel Volume to Mass",
       template("CONVERT TO LITRES FIRST, THEN MULTIPLY BY THE SPECIFIC GRAVITY",
                "42 USG × 3.785 = 159 L; 159 L × 0.72 = 114 KG",
                [("USG → LITRES", "× 3.785"),
                 ("LITRES → KG", "× SG (kg per litre)"),
                 ("CHECK", "Fuel is lighter than water, so kg < litres")],
                "kg = USG × 3.785 × SG"), h=460)
def _():
    boxes = [(40, "42 USG", "volume"), (460, "159 L", "volume"), (880, "114 kg", "mass")]
    for i, (x, big, small) in enumerate(boxes):
        hl = i == 2
        s_ = rect(x, 120, 280, 150, GOLD_SOFT if hl else PANEL, GOLD if hl else LINE, 4 if hl else 2, 14)
        s_ += t(x + 140, 205, big, 44, 800, INK)
        s_ += t(x + 140, 248, small, 20, 600, MUTED)
        boxes[i] = s_
    s = "".join(boxes)
    s += arrow(330, 195, 450, 195, "navy", 5)
    s += t(390, 170, "× 3.785", 24, 800, NAVY)
    s += arrow(750, 195, 870, 195, "navy", 5)
    s += t(810, 170, "× 0.72", 24, 800, NAVY)
    s += t(810, 236, "(SG)", 19, 700, MUTED)
    s += t(600, 360, "1 litre of water = 1 kg.  1 litre of fuel at SG 0.72 = 0.72 kg.", 22, 700, BODY)
    s += t(600, 400, "42 × 3.785 = 158.97 L  →  158.97 × 0.72 = 114.5 kg ≈ 114 kg", 22, 800, INK)
    return s


@R.add(2244, "fp-max-ramp-weight", "Maximum Ramp Weight",
       template("MAXIMUM RAMP WEIGHT = MTOW + TAXI FUEL",
                "THE TAXI FUEL IS BURNED BEFORE THE TAKE-OFF ROLL STARTS",
                [("ON THE RAMP", "May exceed MTOW by the taxi fuel"),
                 ("AT BRAKE RELEASE", "Must be at or below MTOW")]), h=600)
def _():
    s = line(120, 190, 1080, 190, RED, 3, None, "12 8")
    s += t(1080, 176, "MTOW limit", 20, 800, RED, "end")
    for x, cap in ((260, True), (740, False)):
        s += rect(x, 190, 200, 320, NAVY, NAVY, 0, 4)
        s += t(x + 100, 360, "aircraft +\nload +\ntake-off fuel", 20, 700, "#ffffff")
        if cap:
            s += rect(x, 150, 200, 40, GOLD, GOLD_DARK, 2, 4)
            s += t(x + 100, 177, "taxi fuel", 19, 800, INK)
    s += line(220, 512, 1000, 512, INK, 3)
    s += t(360, 552, "PARKED: max ramp weight", 22, 800, INK)
    s += t(840, 552, "BRAKE RELEASE: ≤ MTOW", 22, 800, INK)
    s += arrow(490, 300, 710, 300, "gold", 5)
    s += t(600, 280, "taxi burns", 20, 800, GOLD_DARK)
    s += t(600, 334, "the taxi fuel", 20, 800, GOLD_DARK)
    return s


@R.add(2355, "fp-moment-weight-arm", "Moment = Weight × Arm",
       template("MOMENT = WEIGHT × ARM",
                "THE TURNING EFFECT OF A WEIGHT ABOUT THE DATUM",
                [("ARM", "Distance from the datum to the item's CG (inches)"),
                 ("MOMENT", "Weight × arm (lb·in)"),
                 ("CG", "Total moment ÷ total weight")],
                "CG = Σ moments ÷ Σ weights"), h=520)
def _():
    s = line(140, 70, 140, 420, NAVY, 5)
    s += t(140, 55, "DATUM", 22, 800, NAVY)
    s += rect(140, 300, 900, 22, "#94a3b8", INK, 2, 3)
    s += rect(640, 200, 160, 100, GOLD_SOFT, GOLD_DARK, 3, 8)
    s += t(720, 258, "200 lb", 28, 800, INK)
    s += arrow(720, 330, 720, 400, "red", 5)
    s += t(735, 392, "weight", 20, 700, RED, "start")
    s += dim(140, 160, 720, 160, "arm = 80 in", "navy", 22)
    s += line(720, 150, 720, 196, MUTED, 2, None, "5 5")
    s += pill(600, 470, "MOMENT = 200 lb × 80 in = 16 000 lb·in", NAVY, "#ffffff", 24)
    return s


@R.add(2263, "fp-cg-late-passenger", "New CG After Adding Load",
       template("NEW CG = TOTAL MOMENT ÷ TOTAL WEIGHT",
                "220 420 LB·IN ÷ 2405 LB = 91.65 IN",
                [("MOMENTS", "Weight × arm for each item, then add"),
                 ("TOTAL WEIGHT", "2200 + 175 + 30 = 2405 lb (within MAUW 2500 lb)"),
                 ("CG MOVES AFT", "Both new items sit well behind the old CG")],
                "CG = 220 420 ÷ 2405 = 91.65 in"), h=520)
def _():
    rows = [["ITEM", "WEIGHT (lb)", "ARM (in)", "MOMENT (lb·in)"],
            ["Loaded aircraft", "2200", "89.0", "195 800"],
            ["Late passenger (rear seat)", "175", "116.6", "20 405"],
            ["Baggage", "30", "140.5", "4 215"],
            ["TOTAL", "2405", "", "220 420"]]
    s = table(85, 40, [360, 220, 200, 250], rows, hl={(4, 0), (4, 1), (4, 3)}, row_h=56, size=22,
              hl_ring=[(4, 1), (4, 3)])
    s += pill(600, 400, "CG = 220 420 ÷ 2405 = 91.65 in", NAVY, "#ffffff", 28)
    s += t(600, 470, "2405 lb ≤ MAUW 2500 lb  ✓", 22, 800, GREEN)
    return s


@R.add(2267, "fp-lda-displaced-threshold", "Landing Distance Available",
       template("LDA STARTS AT THE DISPLACED THRESHOLD AND ENDS AT THE RUNWAY END",
                "1150 − 25 = 1125 M — THE STOPWAY IS NEVER PART OF THE LDA",
                [("DISPLACED THRESHOLD", "Usable for take-off, not for landing"),
                 ("STOPWAY", "Counts towards ASDA only (decelerating after a rejected take-off)"),
                 ("LDA", "Runway length − displaced portion")],
                "LDA = 1150 − 25 = 1125 m"), h=520)
def _():
    y, h = 200, 100
    s = rect(80, y, 900, h, "#475569", INK, 2, 2)
    for k in range(300, 940, 70):
        s += f'<rect x="{k}" y="{y + h / 2 - 3}" width="36" height="6" fill="#ffffff"/>\n'
    for xx in (100, 150):
        s += path(f"M {xx},{y + h / 2} l 34,0 m -12,-12 l 12,12 l -12,12", "none", "#ffffff", 4)
    s += rect(196, y + 6, 10, h - 12, "#ffffff", "#ffffff", 0, 0)
    for j in range(4):
        s += rect(222, y + 12 + j * 20, 40, 12, "#ffffff", "#ffffff", 0, 0)
    s += rect(980, y, 130, h, "#e2e8f0", INK, 2, 2)
    for k in range(992, 1100, 34):
        s += path(f"M {k + 18},{y + 18} l -18,{h / 2 - 18} l 18,{h / 2 - 18}", "none", GOLD, 6)
    s += plane_top(40, y + h / 2, 0.55, 90)
    s += dim(80, 150, 980, 150, "Runway 1150 m", "navy", 22)
    s += dim(80, 350, 200, 350, "25 m", "red", 20, side="below")
    s += t(140, 420, "displaced\nthreshold", 18, 700, RED)
    s += dim(200, 350, 980, 350, "LDA 1125 m", "gold", 26, side="below")
    s += dim(980, 350, 1110, 350, "30 m", "muted", 20, side="below")
    s += t(1045, 420, "stopway\n(not LDA)", 18, 700, MUTED)
    return s


@R.add(2255, "fp-runway-slope", "Runway Slope",
       template("SLOPE % = HEIGHT DIFFERENCE ÷ RUNWAY LENGTH × 100",
                "RUNWAY 18 RUNS FROM 5180 FT DOWN TO 5125 FT: 1.45% DOWN",
                [("DIFFERENCE", "5180 − 5125 = 55 ft"),
                 ("SLOPE", "55 ÷ 3800 × 100 = 1.45%"),
                 ("DIRECTION", "Runway 18 starts at the high end, so it slopes down")],
                "55 ÷ 3800 × 100 = 1.45% down"), h=560)
def _():
    s = poly([(120, 200), (1060, 380), (1060, 470), (120, 470)], GROUND, GROUND, 0)
    s += line(120, 200, 1060, 380, INK, 8)
    s += line(120, 200, 1110, 200, MUTED, 2, None, "8 6")
    s += dim(1090, 200, 1090, 380, "55 ft", "red", 22, side="right")
    s += t(120, 130, "Threshold RWY 18 · 5180 ft", 22, 800, INK, "start")
    s += t(1050, 296, "Threshold RWY 36\n5125 ft", 22, 800, INK, "end")
    s += arrow(260, 255, 600, 320, "blue", 5)
    s += t(260, 350, "Using RWY 18: downhill", 21, 800, BLUE, "start")
    s += pill(600, 430, "55 ÷ 3800 × 100 = 1.45% DOWN", NAVY, "#ffffff", 24)
    s += dim(120, 515, 1060, 515, "Length 3800 ft", "navy", 22, side="below")
    return s


def _asi_pt(cx, cy, r, v):
    a = math.radians(-150 + (v - 30) / 170 * 300)
    return cx + r * math.sin(a), cy - r * math.cos(a)


def _asi_arc(cx, cy, r, v1, v2, color, w):
    x1, y1 = _asi_pt(cx, cy, r, v1)
    x2, y2 = _asi_pt(cx, cy, r, v2)
    large = 1 if (v2 - v1) / 170 * 300 > 180 else 0
    return path(f"M {x1:.1f},{y1:.1f} A {r} {r} 0 {large} 1 {x2:.1f},{y2:.1f}", "none", color, w, extra=' stroke-linecap="butt"')


@R.add(2254, "fp-asi-vfe-white-arc", "VFE — Top of the White Arc",
       template("VFE = MAXIMUM SPEED WITH FLAPS EXTENDED",
                "IT IS THE UPPER END OF THE WHITE ARC ON THE AIRSPEED INDICATOR",
                [("WHITE ARC", "Flap operating range: VS0 (bottom) to VFE (top)"),
                 ("GREEN ARC", "Normal operating range: VS1 to VNO"),
                 ("YELLOW ARC / RED LINE", "Caution range VNO to VNE; never exceed VNE")]), h=620)
def _():
    cx, cy = 330, 310
    s = circle(cx, cy, 265, NAVY, INK, 6)
    s += _asi_arc(cx, cy, 228, 48, 129, "#22c55e", 18)
    s += _asi_arc(cx, cy, 228, 129, 163, "#facc15", 18)
    s += _asi_arc(cx, cy, 204, 40, 85, "#ffffff", 14)
    a1, a2 = _asi_pt(cx, cy, 214, 163), _asi_pt(cx, cy, 246, 163)
    s += line(*a1, *a2, "#ef4444", 7)
    for v in range(40, 201, 10):
        p1, p2 = _asi_pt(cx, cy, 250 if v % 20 == 0 else 254, v), _asi_pt(cx, cy, 262, v)
        s += line(*p1, *p2, "#ffffff", 3)
    for v in range(40, 201, 20):
        x, y = _asi_pt(cx, cy, 168, v)
        s += t(x, y + 9, str(v), 24, 800, "#ffffff")
    s += t(cx, cy + 95, "KNOTS", 20, 800, "#94a3b8")
    p = _asi_pt(cx, cy, 204, 85)
    s += circle(*p, 12, GOLD, GOLD_DARK, 3)
    q = _asi_pt(cx, cy, 300, 85)
    s += line(p[0], p[1], q[0], q[1], GOLD_DARK, 4)
    s += pill(q[0], q[1] - 12, "VFE", GOLD, INK, 24, stroke=GOLD_DARK)
    s += circle(cx, cy, 14, "#94a3b8", "#94a3b8", 0)
    rows = [("White arc", "VS0 → VFE: flaps may be extended", PANEL, True),
            ("Green arc", "VS1 → VNO: normal operations", GREEN_SOFT, False),
            ("Yellow arc", "VNO → VNE: smooth air only", GOLD_SOFT, False),
            ("Red line", "VNE: never exceed", RED_SOFT, False)]
    for i, (h_, b, fill, hl) in enumerate(rows):
        s += card(660, 60 + i * 128, 500, 110, h_, b, NAVY, fill, 22, 19, hl)
    return s


@R.add(2342, "fp-vx-vs-vy", "VX vs VY",
       template("VX = BEST ANGLE OF CLIMB; VY = BEST RATE OF CLIMB",
                "VX GIVES THE MOST HEIGHT PER DISTANCE; VY THE MOST HEIGHT PER MINUTE",
                [("VX", "Use to clear an obstacle close to the runway"),
                 ("VY", "Use for the normal climb to cruising altitude"),
                 ("SPEEDS", "VX is lower than VY")]), h=600)
def _():
    s = rect(0, 500, 1200, 100, GROUND, GROUND, 0, 0)
    s += rect(60, 486, 300, 16, "#475569", INK, 2, 2)
    s += poly([(530, 500), (556, 500), (546, 322), (540, 322)], INK, INK, 2)
    s += circle(543, 318, 8, RED, RED, 0)
    s += t(543, 545, "obstacle", 20, 800, RED)
    s += path("M 120,494 L 700,124", "none", BLUE, 6, "blue")
    s += path("M 120,494 L 1120,138", "none", GREEN, 6, "green")
    s += circle(560, 213, 11, "#ffffff", BLUE, 4)
    s += circle(1000, 181, 11, "#ffffff", GREEN, 4)
    s += pill(470, 213, "1 min", BLUE_SOFT, BLUE, 18, stroke=BLUE)
    s += pill(1000, 226, "1 min", GREEN_SOFT, GREEN, 18, stroke=GREEN)
    s += t(330, 110, "VX — best ANGLE", 24, 800, BLUE)
    s += t(330, 140, "most height per distance: clears the obstacle", 19, 600, BODY)
    s += t(900, 330, "VY — best RATE", 24, 800, GREEN)
    s += t(900, 360, "most height per minute, but a flatter path", 19, 600, BODY)
    return s


@R.add(2300, "fp-aquaplaning", "Aquaplaning and Groundspeed",
       template("AQUAPLANING IS MORE LIKELY AT HIGH GROUNDSPEED",
                "THE TYRE CAN'T PUSH THE WATER AWAY FAST ENOUGH AND RIDES ON A FILM",
                [("RISK UP WITH", "Speed, standing water, worn tread, low tyre pressure"),
                 ("EFFECT", "Braking and steering are lost while the tyre is off the surface"),
                 ("RULE OF THUMB", "Aquaplaning speed (kt) ≈ 9 × √tyre pressure (psi)")]), h=520)
def _():
    s = ""
    for x0, title, high in [(30, "LOW GROUNDSPEED", False), (620, "HIGH GROUNDSPEED", True)]:
        s += rect(x0, 30, 550, 440, PANEL, LINE, 2, 14)
        s += t(x0 + 275, 74, title, 24, 800, RED if high else GREEN)
        gy = 380
        s += rect(x0 + 20, gy, 510, 40, "#475569", "#475569", 0, 0)
        s += rect(x0 + 20, gy - 10, 510, 10, "#60a5fa", "#60a5fa", 0, 0)
        cx = x0 + 300
        lift = 22 if high else 0
        cy = gy - 110 - lift
        if high:
            s += path(f"M {cx - 190},{gy - 10} Q {cx - 110},{gy - 14} {cx - 75},{gy - 10 - lift - 30} "
                      f"L {cx + 70},{gy - 10 - lift - 4} L {cx + 70},{gy - 10} Z", "#60a5fa", "#2563eb", 2)
        s += circle(cx, cy, 110, "#1f2937", INK, 4)
        s += circle(cx, cy, 45, "#9ca3af", "#6b7280", 3)
        s += arrow(x0 + 120, 150, x0 + 40, 150, "navy", 5)
        s += t(x0 + 80, 128, "motion", 18, 700, NAVY)
        if high:
            s += t(x0 + 275, 452, "water wedge lifts the tyre: no contact", 20, 800, RED)
        else:
            s += path(f"M {cx - 70},{gy - 20} l -60,-30 M {cx + 70},{gy - 20} l 60,-30", "none", "#2563eb", 4)
            s += t(x0 + 275, 452, "water squeezed out: tyre grips", 20, 800, GREEN)
    return s
