"""Meteorology replacement diagrams for explanation images that were missing, off-topic or misleading.

Rendered by build.py into the approved refined-batch-2 folder so the practice page shows the KEY FACT card.
"""
import math

from common import Registry, tag
from kit import (BLUE, BLUE_SOFT, BODY, GOLD, GOLD_DARK, GOLD_SOFT, GREEN, GROUND, INK, LINE, MUTED, NAVY, PANEL, RED,
                 RED_SOFT, SKY, arrow, card, circle, cloud, line, path, pill, poly, rect, t, template)

R = Registry("meteorology", "/explanation-images/meteorology/refined-batch-2")


def sun(x, y, r=30):
    s = ""
    for k in range(8):
        a = k * math.pi / 4
        s += line(x + (r + 8) * math.cos(a), y + (r + 8) * math.sin(a), x + (r + 22) * math.cos(a),
                  y + (r + 22) * math.sin(a), GOLD_DARK, 4)
    return s + circle(x, y, r, GOLD, GOLD_DARK, 3)


def moon(x, y, r=28):
    return (circle(x, y, r, "#e2e8f0", MUTED, 3) +
            circle(x + 14, y - 8, r - 2, "#1e293b", "#1e293b", 0))


def thermometer(x, y, h, frac, label, color=BLUE):
    """Bulb thermometer, (x, y) = top of the tube; frac = fill height 0..1."""
    s = rect(x - 12, y, 24, h, "#ffffff", INK, 3, 12)
    s += rect(x - 6, y + h - h * frac, 12, h * frac, color, color, 0, 4)
    s += circle(x, y + h + 18, 24, color, INK, 3)
    s += t(x, y + h + 84, label, 26, 800, color)
    return s


# ------------------------------------------------------------------ #1536 aneroid barometer

@R.add(1536, "aneroid-barometer-v2", "How an Aneroid Barometer Works",
       template("A BAROMETER MEASURES ATMOSPHERIC PRESSURE",
                "THE ANEROID TYPE USES A SEALED CAPSULE THAT FLEXES AS OUTSIDE PRESSURE CHANGES",
                [("Capsule", "Sealed and partly emptied of air, so it does not leak or fill"),
                 ("Pressure rises", "The capsule is squeezed thinner"),
                 ("Pressure falls", "The capsule expands"),
                 ("Reading", "A linkage turns the movement into a needle reading in hPa")]), h=560)
def _():
    s = rect(60, 40, 1080, 480, PANEL, LINE, 2, 14)
    # capsule (corrugated bellows), seen side-on
    cx, cy = 300, 330
    top = "M 170,300 " + " ".join(f"Q {170 + 26 * i + 13},{288 if i % 2 else 312} {170 + 26 * (i + 1)},300" for i in range(10))
    bot = "M 170,360 " + " ".join(f"Q {170 + 26 * i + 13},{372 if i % 2 else 348} {170 + 26 * (i + 1)},360" for i in range(10))
    s += rect(170, 300, 260, 60, BLUE_SOFT, BLUE_SOFT, 0, 0)
    s += path(top, "none", BLUE, 5)
    s += line(170, 300, 170, 360, BLUE, 5) + line(430, 300, 430, 360, BLUE, 5)
    s += t(cx, cy + 9, "partial vacuum", 22, 700, BLUE)
    s += rect(150, 360, 300, 22, "#94a3b8", INK, 2, 4)  # base plate
    # outside pressure squeezing
    for x in (200, 250, 300, 350):
        s += arrow(x, 210, x, 278, "red", 5)
    s += t(275, 190, "outside air pressure", 24, 800, RED)
    s += t(300, 430, "Sealed capsule", 26, 800, INK)
    # linkage from capsule top to needle
    s += line(410, 296, 410, 250, INK, 4)
    s += path("M 410,250 L 560,250 L 640,300", "none", INK, 4)
    s += circle(560, 250, 7, INK, INK, 0)
    s += t(470, 236, "linkage", 21, 700, MUTED)
    # dial
    dx, dy, r = 840, 300, 170
    s += circle(dx, dy, r, "#ffffff", NAVY, 6)
    for k, v in enumerate(range(960, 1061, 20)):
        a = math.radians(-120 + k * 48)
        s += line(dx + (r - 26) * math.sin(a), dy - (r - 26) * math.cos(a), dx + (r - 8) * math.sin(a),
                  dy - (r - 8) * math.cos(a), INK, 4)
        s += t(dx + (r - 58) * math.sin(a), dy - (r - 58) * math.cos(a) + 8, str(v), 20, 700, INK)
    a = math.radians(-120 + 2.65 * 48)
    s += line(dx, dy, dx + (r - 40) * math.sin(a), dy - (r - 40) * math.cos(a), RED, 7)
    s += circle(dx, dy, 12, INK, INK, 0)
    s += path(f"M 640,300 L {dx - 12},{dy}", "none", INK, 4)
    s += t(dx, dy + 70, "hPa", 24, 800, MUTED)
    s += t(dx, 105, "Needle reads pressure", 26, 800, INK)
    return s


# ------------------------------------------------------------------ #19 density altitude

@R.add(19, "density-altitude-v1", "Density Altitude",
       template("DENSITY ALTITUDE IS PRESSURE ALTITUDE CORRECTED FOR TEMPERATURE",
                "HOT AIR IS LESS DENSE, SO THE AIRCRAFT PERFORMS AS IF IT WERE HIGHER",
                [("Start with", "Pressure altitude (1013 hPa set on the altimeter)"),
                 ("Correct for", "How far the temperature is above or below ISA"),
                 ("Rule of thumb", "About 120 ft for every 1°C above ISA"),
                 ("Example", "5,000 ft at 30°C: ISA is 5°C, so +25°C ≈ +3,000 ft, giving about 8,000 ft")],
                formula="Density altitude ≈ pressure altitude + 120 × (OAT − ISA temperature)"), h=560)
def _():
    s = ""
    # altitude scale
    x0, base, k = 120, 470, 0.045  # px per ft
    s += line(x0, base, x0, base - 9000 * k, INK, 4)
    for ft in range(0, 9001, 1000):
        y = base - ft * k
        s += line(x0 - 10, y, x0, y, INK, 3)
        s += t(x0 - 18, y + 7, f"{ft:,}", 19, 700, MUTED, "end")
    s += t(x0, 40, "ft", 20, 800, MUTED)
    # aerodrome on ground at 5000 ft
    yp, yd = base - 5000 * k, base - 8000 * k
    s += rect(160, yp, 300, base - yp, GROUND, "#b8a27a", 2, 0)
    s += t(310, yp + 50, "Aerodrome", 24, 800, INK)
    s += t(310, yp + 80, "pressure altitude 5,000 ft", 20, 600, BODY)
    s += line(160, yp, 1100, yp, NAVY, 3, dash="10 8")
    s += pill(980, yp, "Pressure altitude 5,000 ft", NAVY, "#ffffff", 20)
    s += line(160, yd, 1100, yd, RED, 3, dash="10 8")
    s += pill(980, yd, "Density altitude ≈ 8,000 ft", RED, "#ffffff", 20)
    s += arrow(620, yp - 6, 620, yd + 8, "red", 5)
    s += t(640, (yp + yd) / 2 + 8, "+3,000 ft", 24, 800, RED, "start")
    # temperature panel
    s += card(520, 310, 560, 120, "OAT 30°C, ISA at 5,000 ft is 5°C",
              "ISA + 25°C  →  25 × 120 ft ≈ 3,000 ft\nThe aircraft performs as if at 8,000 ft", RED)
    return s


# ------------------------------------------------------------------ #32 ISA sea level

@R.add(32, "isa-sea-level-v1", "ISA Sea-Level Values",
       template("ISA SEA-LEVEL DENSITY IS 1.225 kg/m³ (1225 g/m³)",
                "THE STANDARD ATMOSPHERE FIXES PRESSURE, TEMPERATURE AND DENSITY AT MEAN SEA LEVEL",
                [("Pressure", "1013.25 hPa"),
                 ("Temperature", "+15°C"),
                 ("Density", "1.225 kg/m³ = 1225 g/m³"),
                 ("Lapse rate", "1.98°C per 1,000 ft up to the tropopause at 36,090 ft (11 km)")]), h=440)
def _():
    s = rect(40, 330, 1120, 70, BLUE_SOFT, BLUE, 2, 0)
    s += t(600, 375, "Mean sea level (ISA)", 24, 800, BLUE)
    vals = [("Pressure", "1013.25 hPa", False), ("Temperature", "+15°C", False),
            ("Density", "1225 g/m³", True), ("Lapse rate", "1.98°C / 1,000 ft", False)]
    w, gap = 250, 30
    x = 40 + (1120 - 4 * w - 3 * gap) / 2
    for lab, val, hl in vals:
        s += rect(x, 70, w, 200, GOLD_SOFT if hl else "#ffffff", GOLD if hl else LINE, 4 if hl else 2, 12)
        s += t(x + w / 2, 125, lab, 24, 700, MUTED)
        s += t(x + w / 2, 195, val, 34 if len(val) < 12 else 28, 800, INK)
        if hl:
            s += t(x + w / 2, 245, "= 1.225 kg/m³", 22, 700, GOLD_DARK)
        s += line(x + w / 2, 270, x + w / 2, 330, LINE, 3)
        x += w + gap
    return s


# ------------------------------------------------------------------ #46 anabatic / katabatic

def slope_panel(x0, day):
    s = rect(x0, 40, 540, 420, SKY if day else "#1e293b", LINE, 2, 14)
    s += poly([(x0, 460), (x0 + 120, 460), (x0 + 430, 170), (x0 + 540, 150), (x0 + 540, 460)], GROUND, "#b8a27a", 2)
    if day:
        s += sun(x0 + 90, 110)
        s += path(f"M {x0 + 150},430 L {x0 + 400},205", "none", RED, 7, "red")
        s += t(x0 + 40, 230, "warm air rises\nup the slope", 23, 800, RED, "start", lh=1.2)
        s += t(x0 + 270, 520, "DAY: anabatic wind (upslope)", 26, 800, RED)
    else:
        s += moon(x0 + 90, 110)
        s += path(f"M {x0 + 400},205 L {x0 + 150},430", "none", BLUE, 7, "blue")
        s += t(x0 + 40, 230, "cold air drains\ndown the slope", 23, 800, "#93c5fd", "start", lh=1.2)
        s += t(x0 + 270, 520, "NIGHT: katabatic wind (downslope)", 26, 800, BLUE)
    s += t(x0 + 440, 260, "slope heated" if day else "slope cooled", 21, 700, INK)
    return s


@R.add(46, "anabatic-katabatic-v1", "Anabatic and Katabatic Winds",
       template("AN ANABATIC WIND BLOWS UP A SLOPE BY DAY",
                "A KATABATIC WIND BLOWS DOWN THE SLOPE AT NIGHT",
                [("Anabatic", "Sun heats the slope, the air in contact warms, becomes less dense and rises"),
                 ("Katabatic", "The slope cools by radiation at night; cold, dense air drains downhill"),
                 ("Memory aid", "ANA = UP (like ascend), KATA = DOWN")]), h=560)
def _():
    return slope_panel(40, True) + slope_panel(620, False)


# ------------------------------------------------------------------ #53 thunderstorm ingredients

@R.add(53, "thunderstorm-ingredients-v1", "What a Thunderstorm Needs",
       template("A THUNDERSTORM NEEDS MOIST AIR, INSTABILITY AND A LIFTING ACTION",
                "TAKE AWAY ANY ONE OF THE THREE AND NO CUMULONIMBUS FORMS",
                [("Moisture", "Enough water vapour to build deep cloud and release latent heat"),
                 ("Instability", "Rising air stays warmer than its surroundings, so it keeps rising"),
                 ("Lifting action", "Surface heating, a front, high ground or convergence starts the air rising")]),
       h=560)
def _():
    s = rect(40, 470, 1120, 50, GROUND, "#b8a27a", 2, 0)
    # cumulonimbus with anvil
    s += path("M 480,440 L 720,440 C 770,440 780,395 745,378 C 790,358 772,305 728,306 C 760,276 742,228 700,226 "
              "L 760,172 L 820,148 L 380,148 L 440,172 L 500,226 C 458,228 440,276 472,306 C 428,305 410,358 455,378 "
              "C 420,395 430,440 480,440 Z", "#e2e8f0", "#94a3b8", 3)
    s += t(600, 120, "Cumulonimbus", 26, 800, INK)
    s += arrow(600, 460, 600, 200, "red", 7)
    # three ingredients
    s += card(60, 180, 330, 120, "1  Moist air", "plenty of water vapour", BLUE)
    s += card(810, 180, 330, 120, "2  Instability", "rising air keeps rising", RED)
    s += card(60, 330, 330, 120, "3  Lifting action", "heating, front, hills,\nconvergence", GOLD_DARK)
    s += path("M 390,240 L 470,290", "none", BLUE, 4, "blue")
    s += path("M 810,240 L 745,280", "none", RED, 4, "red")
    s += path("M 390,410 L 555,450", "none", GOLD_DARK, 4, "gold")
    return s


# ------------------------------------------------------------------ #1471 freezing fog

@R.add(1471, "freezing-fog-v1", "Freezing Fog",
       template("FREEZING FOG IS MADE OF SUPERCOOLED WATER DROPLETS",
                "THE DROPLETS STAY LIQUID BELOW 0°C AND FREEZE ON CONTACT WITH A SURFACE",
                [("Temperature", "Below 0°C"),
                 ("Droplets", "Liquid (supercooled), not ice crystals"),
                 ("On contact", "They freeze onto aircraft, trees and fences as rime ice"),
                 ("Hazard", "Poor visibility plus icing on the ground and during take-off")]), h=520)
def _():
    s = rect(40, 40, 1120, 440, "#eef2f7", LINE, 2, 14)
    s += rect(40, 400, 1120, 80, "#f8fafc", LINE, 2, 0)
    import random
    rnd = random.Random(7)
    for _ in range(140):
        x, y = rnd.uniform(240, 1140), rnd.uniform(70, 390)
        if (330 < x < 790 and y < 150) or 770 < x < 880:
            continue
        s += circle(x, y, 5, BLUE_SOFT, BLUE, 2)
    s += thermometer(140, 90, 210, 0.25, "−3°C", BLUE)
    # post with rime
    s += rect(820, 230, 26, 170, "#64748b", INK, 2, 3)
    for k in range(7):
        s += poly([(820, 240 + k * 22), (796, 248 + k * 22), (820, 256 + k * 22)], "#ffffff", BLUE, 2)
    s += pill(560, 110, "liquid droplets below 0°C = supercooled", NAVY, "#ffffff", 22)
    s += pill(880, 440, "freeze on contact → rime ice", BLUE, "#ffffff", 22)
    return s
