"""Meteorology explanation pictures, phone-first (docs/EXPLANATION_ILLUSTRATION_STANDARD.md), built from scene.py."""
import math
import random

import json

from common import Registry
from kit import REPO, template
from scene import (BLUE, COMMON_DEFS, CAPTION, GOLD, ICE, INK, MIN_TXT, NAVY_BLUE, RED, TXT_L, TXT_M, W, aircraft,
                   capsule, circle, cumulonimbus, cumulus, defs, dial, droplet, fence, flow, flow_band, fog_bank,
                   grid_points, label, lightning, magnifier, molecule, moon, path, rain, stack, stack_height, stars,
                   sun, terrain, tree)

R = Registry("meteorology", "/explanation-images/meteorology/refined-batch-2")

# KEY FACT cards and titles as they are live (recorded when the pictures went live on 2026-10-07)
_LIVE = {row["id"]: row["after"] for row in
         json.loads((REPO / "data/content-fixes/met-visuals-2026-10-07.json").read_text())["rows"]}


def card(qid):
    return _LIVE[qid]["explanation_visual_template"]


def title(qid):
    return _LIVE[qid]["explanation_image_title"]


def picture(panels):
    body, _ = stack(panels)
    return defs(*COMMON_DEFS) + body


# ------------------------------------------------------------------ anabatic / katabatic (the reference picture)

def ridge_y(x):
    """Valley floor on the left rising smoothly to a ridge on the right."""
    return 410 - 270 / (1 + math.exp(-(x - 560) / 95))


SLOPE = [(x, ridge_y(x) + 2) for x in range(330, 830, 35)]
SLOPE_H = 470


def slope_panel(day):
    def draw(w, h):
        rnd = random.Random(3)
        s = ""
        if day:
            s += sun(600, 92, 42)
        else:
            s += stars(rnd, (380, 15, 890, 200), 45) + moon(600, 88, 36)
        s += terrain(ridge_y, w, h, "url(#ground_day)" if day else "url(#ground_night)", "#5d4a33" if day else "#1f2a2a")
        # the slope surface: warmed by the sun or cooling by radiation
        s += path("M " + " L ".join(f"{x},{ridge_y(x) + 3:.1f}" for x in range(240, w + 1, 10)), "none",
                  "#ffd46b" if day else "#7aa7d9", 9, ' stroke-opacity="0.6"')
        for x, sc in ((60, 1.0), (110, 0.8), (160, 1.1), (835, 0.75), (880, 0.85)):
            s += tree(x, ridge_y(x) + 5, sc, "#2f6b3a" if day else "#1d3326")
        if day:
            s += flow_band(SLOPE, RED, "head_red")
            s += label(36, 82, "Warm air rises\nup the slope", TXT_L, RED)
            s += label(870, 448, "Sun heats the slope", TXT_M, "#3b2f1f", "end", halo="#e9dfc4")
        else:
            pool_top = 374
            x_edge = 560 - 95 * math.log(270 / (410 - pool_top) - 1)
            s += path(f"M 0,{pool_top} L {x_edge:.1f},{pool_top} "
                      + " ".join(f"L {x},{ridge_y(x):.1f}" for x in range(int(x_edge), -1, -5)) + " Z",
                      BLUE, extra=' fill-opacity="0.45"')
            s += flow_band(SLOPE, ICE, "head_ice", reverse=True)
            s += label(36, 82, "Cold, dense air\ndrains downhill", TXT_L, "#ffffff", halo="#0f1d3d")
            s += label(30, 452, "Cold air pools in the valley", TXT_M, "#ffffff", halo="#0f1d3d")
        return s
    return dict(h=SLOPE_H, sky="sky_day" if day else "sky_night", draw=draw,
                caption="DAY — ANABATIC (upslope)" if day else "NIGHT — KATABATIC (downslope)",
                color=RED if day else BLUE)


@R.add(46, "anabatic-katabatic-v3", "Anabatic and Katabatic Winds",
       template("AN ANABATIC WIND BLOWS UP A SLOPE BY DAY",
                "A KATABATIC WIND BLOWS DOWN THE SLOPE AT NIGHT",
                [("Anabatic", "Sun heats the slope, the air in contact warms, becomes less dense and rises"),
                 ("Katabatic", "The slope cools by radiation at night; cold, dense air drains downhill"),
                 ("Memory aid", "ANA = UP (like ascend), KATA = DOWN")]),
       h=stack_height([SLOPE_H, SLOPE_H]), w=W)
def _():
    return picture([slope_panel(True), slope_panel(False)])


# ------------------------------------------------------------------ barometer

BARO_H = 470


def baro_panel(high):
    def draw(w, h):
        rnd = random.Random(11 if high else 5)
        s = ""
        if high:
            s += sun(470, 72, 34)
        else:
            for x, y, rx, ry in ((120, 30, 260, 70), (450, 10, 280, 60), (780, 30, 260, 70)):
                s += f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="#334155" opacity="0.8" filter="url(#soft)"/>'
            for k in range(22):
                x = 20 + k * 42
                s += f'<line x1="{x}" y1="95" x2="{x - 12}" y2="135" stroke="#e2e8f0" stroke-width="3" stroke-opacity="0.7"/>'
        avoid = [(0, 20, 450, 200), (0, 375, 450, 460), (450, 10, 900, 460)] + ([(410, 20, 530, 130)] if high else [])
        for x, y in grid_points(rnd, (16, 16, 890, 455), 50 if high else 100, 10, avoid):
            s += molecule(x, y)
        # the instrument: dial on top of a glass-fronted case holding the capsule
        cx, cap_h = 660, 30 if high else 62
        s += f'<rect x="560" y="300" width="200" height="150" rx="18" fill="url(#bezel)" stroke="#374151" stroke-width="3"/>'
        s += f'<rect x="576" y="316" width="168" height="118" rx="10" fill="#eef4fa" stroke="#6b7280" stroke-width="2"/>'
        s += f'<rect x="595" y="412" width="130" height="12" rx="3" fill="#6b7280"/>'
        s += capsule(cx, 412 - cap_h / 2, 120, cap_h)
        s += f'<line x1="{cx}" y1="{412 - cap_h}" x2="{cx}" y2="300" stroke="#1f2937" stroke-width="5"/>'
        s += dial(cx, 160, 140, 1030 if high else 975)
        for (x0, y0), (x1, y1) in (((470, 330), (540, 355)), ((470, 430), (540, 405)), ((850, 330), (780, 355)),
                                   ((850, 430), (780, 405))):
            if high:
                s += flow([(x0, y0), (x1, y1)], RED, "head_red", 8)
            else:
                s += flow([(x1, y1), (x0, y0)], BLUE, "head_blue", 8)
        if high:
            s += label(36, 82, "More air presses\non the capsule", TXT_L, RED)
            s += label(36, 430, "Needle reads higher", TXT_M, INK)
        else:
            s += label(36, 82, "Less air: the\ncapsule expands", TXT_L, NAVY_BLUE)
            s += label(36, 430, "Needle reads lower", TXT_M, INK)
        return s
    return dict(h=BARO_H, sky="sky_day" if high else "sky_grey", draw=draw,
                caption="HIGH PRESSURE — reads higher" if high else "LOW PRESSURE — reads lower",
                color=RED if high else BLUE)


@R.add(1536, "aneroid-barometer-v5", title(1536), card(1536), h=stack_height([BARO_H, BARO_H]), w=W)
def _():
    return picture([baro_panel(True), baro_panel(False)])


# ------------------------------------------------------------------ density altitude

DA_H = 470


def airfield_panel(hot):
    def draw(w, h):
        rnd = random.Random(21 if hot else 4)
        s = sun(800, 92, 42) if hot else ""
        s += path("M 0,300 L 130,210 L 250,270 L 380,180 L 520,260 L 660,195 L 900,280 L 900,470 L 0,470 Z",
                  "#c8a98a" if hot else "#9fb3c8")
        s += f'<rect x="0" y="400" width="{w}" height="{h - 400}" fill="url(#grass)"/>'
        s += f'<rect x="30" y="408" width="520" height="20" rx="3" fill="#475569"/>'
        s += "".join(f'<rect x="{60 + k * 60}" y="415" width="30" height="5" fill="#ffffff"/>' for k in range(8))
        plane_box = (420, 280, 700, 398) if hot else (380, 140, 660, 330)
        avoid = [(0, 20, 470, 170), plane_box] + ([(700, 20, 900, 175)] if hot else [])
        for x, y in grid_points(rnd, (16, 16, 890, 390), 100 if hot else 56, 12, avoid):
            s += molecule(x, y)
        if hot:
            for k in range(6):
                x = 80 + k * 70
                s += path(f"M {x},398 q 10,-14 0,-28 q -10,-14 0,-28", "none", "#f97316", 4, ' stroke-opacity="0.7"')
            s += flow([(70, 404), (300, 392), (520, 356), (700, 312), (860, 268)], RED, "head_red", 6, 0.6)
            s += aircraft(560, 338, 270, 9)
            s += label(36, 82, "Hot day, 30°C\nthin air", TXT_L, RED)
        else:
            s += flow([(70, 400), (260, 356), (430, 262), (630, 142), (790, 62)], BLUE, "head_blue", 6, 0.6)
            s += aircraft(520, 232, 270, 28)
            s += label(36, 82, "Standard day, 5°C\ndense air", TXT_L, NAVY_BLUE)
        s += label(870, 458, "Airfield 5,000 ft", TXT_M, INK, "end")
        return s
    return dict(h=DA_H, sky="sky_hot" if hot else "sky_day", draw=draw,
                caption="HOT DAY — performs as at ≈ 8,000 ft" if hot else "ISA DAY — performs as at 5,000 ft",
                color=RED if hot else NAVY_BLUE)


@R.add(19, "density-altitude-v3", title(19), card(19), h=stack_height([DA_H, DA_H]), w=W)
def _():
    return picture([airfield_panel(False), airfield_panel(True)])


# ------------------------------------------------------------------ ISA sea level

ISA_H = 600


def isa_draw(w, h):
    rnd = random.Random(9)
    s = sun(820, 82, 38) + cumulus(330, 290, 150, seed=2)
    # sea out to the horizon, beach across the foreground
    s += f'<rect x="0" y="370" width="{w}" height="{h - 370}" fill="url(#sea)"/>'
    s += "".join(path(f"M {40 + k * 95},{410 + (k % 3) * 34} q 18,-9 36,0", "none", "#bfdbfe", 4, ' stroke-opacity="0.7"')
                 for k in range(5))
    s += path("M 300,600 C 360,520 470,470 640,450 C 740,440 840,432 900,430 L 900,600 Z", "url(#sand)")
    s += path("M 300,600 C 360,520 470,470 640,450 C 740,440 840,432 900,430", "none", "#ffffff", 6, ' stroke-opacity="0.6"')
    # one cubic metre of air standing on the sand, with its mass on a tag
    x, y, a, d = 520, 330, 170, 40          # front face bottom at y + a + d = 540, on the sand
    s += f'<ellipse cx="{x + (a + d) / 2}" cy="{y + a + d + 4}" rx="{(a + d) / 2 + 10}" ry="12" fill="#8a7550" opacity="0.35"/>'
    s += (f'<path d="M {x},{y + d} L {x + d},{y} L {x + a + d},{y} L {x + a + d},{y + a} L {x + a},{y + a + d} '
          f'L {x},{y + a + d} Z" fill="#bfdbfe" fill-opacity="0.65" stroke="#1d4ed8" stroke-width="4"/>')
    s += path(f"M {x},{y + d} L {x + a},{y + d} L {x + a + d},{y} M {x + a},{y + d} L {x + a},{y + a + d}", "none",
              "#1d4ed8", 4)
    for px, py in grid_points(rnd, (x + 16, y + d + 16, x + a - 8, y + a + d - 8), 34, 5):
        s += molecule(px, py)
    tx, ty = 738, 300                       # mass tag tied to the top corner of the cube
    s += f'<line x1="{x + a + d - 6}" y1="{y + 6}" x2="{tx + 20}" y2="{ty + 8}" stroke="#475569" stroke-width="3"/>'
    s += (f'<path d="M {tx},{ty + 8} L {tx + 22},{ty - 14} L {tx + 150},{ty - 14} L {tx + 150},{ty + 46} L {tx + 22},{ty + 46} Z" '
          f'fill="#fef3c7" stroke="#b7860b" stroke-width="3"/>')
    s += circle(tx + 22, ty + 16, 5, "#ffffff", "#b7860b", 2)
    s += label(tx + 92, ty + 30, "1225 g", 36, INK, "middle", halo=None)
    s += label(36, 82, "ISA at sea level\n1013.25 hPa, +15°C", TXT_L, INK)
    s += label(x, y - 18, "1 m³ of air", TXT_M, "#1e3a8a")
    return s


@R.add(32, "isa-sea-level-v3", title(32), card(32), h=stack_height([ISA_H]), w=W)
def _():
    return picture([dict(h=ISA_H, sky="sky_day", draw=isa_draw, caption="1 m³ OF AIR AT SEA LEVEL = 1225 g",
                         color="#1e3a8a")])


# ------------------------------------------------------------------ thunderstorm ingredients

TS_H = 640


def storm_draw(w, h):
    s = sun(110, 80, 34)
    s += f'<rect x="0" y="520" width="320" height="{h - 520}" fill="url(#sea)"/>'
    s += terrain(lambda x: 520 if x < 300 else 520 - max(0, x - 640) * 0.22, w, h, "url(#grass)")
    s += f'<rect x="0" y="520" width="310" height="{h - 520}" fill="url(#sea)"/>'
    s += rain(492, 606, 398, 525)
    s += cumulonimbus(560, 400, 30)
    s += lightning([(612, 404), (594, 440), (614, 440), (596, 480), (612, 480), (598, 516)])
    for k, off in enumerate((0, 30, 60)):  # 1: moist air flowing in from the sea
        s += flow([(30, 505 - off), (200, 500 - off), (360, 482 - off), (470, 432 - off * 0.5)], BLUE, "head_blue",
                  9 - 2 * k, 1 - 0.22 * k)
    for k, dx in enumerate((-30, 10, 50)):  # 2: unstable air keeps rising inside the cloud
        s += flow([(550 + dx, 385), (558 + dx, 290), (546 + dx, 200), (554 + dx, 110)], RED, "head_red",
                  9 - 2 * k, 1 - 0.22 * k)
    for x in (660, 715, 770):  # 3: lift, warm air rising off the heated ground into the cloud base
        gy = 520 - max(0, x - 640) * 0.22
        s += flow([(x, gy - 8), (x - 6, gy - 60), (x - 36, 414)], GOLD, "head_gold", 7, 0.9)
    s += label(36, 175, "2  Unstable air\nkeeps rising", TXT_L, RED)
    s += label(36, 392, "1  Moist air", TXT_L, BLUE)
    s += label(870, 600, "3  Lift: heating, hills, fronts", TXT_M, "#9a5b00", "end")
    return s


@R.add(53, "thunderstorm-ingredients-v3", title(53), card(53), h=stack_height([TS_H]), w=W)
def _():
    return picture([dict(h=TS_H, sky="sky_day", draw=storm_draw, caption="MOISTURE + INSTABILITY + LIFT", color=INK)])


# ------------------------------------------------------------------ freezing fog

FOG_H = 600


def fog_draw(w, h):
    rnd = random.Random(2)
    s = ""
    for k in range(12):
        x = 40 + k * 78 + rnd.uniform(-15, 15)
        th = rnd.uniform(80, 130)
        s += path(f"M {x:.1f},{430 - th:.1f} L {x + 30:.1f},430 L {x - 30:.1f},430 Z", "#8a9bb0", extra=' opacity="0.6"')
    s += f'<rect x="0" y="420" width="{w}" height="{h - 420}" fill="url(#frost)"/>'
    for x, y, rx, ry in ((150, 400, 260, 80), (500, 410, 300, 70), (820, 390, 260, 80), (450, 300, 280, 50)):
        s += fog_bank(x, y, rx, ry)
    s += fence(430, 610, 530, 110, posts=4, rime=True)
    s += aircraft(745, 476, 300, 0, rime=True)
    s += f'<rect x="0" y="500" width="{w}" height="{h - 500}" fill="#ffffff" opacity="0.25" filter="url(#soft)"/>'
    inner = '<rect x="0" y="0" width="900" height="600" fill="url(#lens)"/>'
    for x, y in grid_points(rnd, (70, 80, 340, 350), 62, 10):
        inner += droplet(x, y, rnd.uniform(15, 22))
    s += magnifier(200, 210, 150, inner)
    s += label(410, 82, "Air at −3°C:\ndroplets stay liquid", TXT_L, "#1e3a8a")
    s += label(870, 578, "Rime ice on contact", TXT_M, INK, "end")
    return s


@R.add(1471, "freezing-fog-v3", title(1471), card(1471), h=stack_height([FOG_H]), w=W)
def _():
    return picture([dict(h=FOG_H, sky="sky_fog", draw=fog_draw, caption="FREEZING FOG: SUPERCOOLED DROPLETS",
                         color="#1e3a8a")])


# ------------------------------------------------------------------ what changes air density

AD_H = 470


def density_panel(dense):
    def draw(w, h):
        rnd = random.Random(31 if dense else 8)
        s = ""
        if dense:
            s += path("M 0,330 L 150,215 L 260,290 L 430,170 L 610,280 L 900,215 L 900,470 L 0,470 Z", "#8da4bd")
            s += path("M 392,203 L 430,170 L 470,201 L 448,197 L 430,209 Z", "#ffffff")
            s += path("M 125,234 L 150,215 L 178,236 L 152,232 Z", "#ffffff")
        else:
            s += sun(800, 92, 42)
            s += path("M 0,340 L 180,265 L 330,320 L 520,250 L 900,330 L 900,470 L 0,470 Z", "#c8a98a")
            for x, y, rx, ry in ((200, 200, 280, 50), (600, 250, 280, 50)):
                s += fog_bank(x, y, rx, ry, 0.45)
        s += f'<rect x="0" y="405" width="{w}" height="{h - 405}" fill="url(#grass)"/>'
        avoid = [(0, 20, 470, 175)] + ([] if dense else [(700, 20, 900, 175)])
        pts = grid_points(rnd, (18, 18, 890, 395), 50 if dense else 84, 10 if dense else 14, avoid)
        for i, (x, y) in enumerate(pts):
            s += molecule(x, y, "vapour" if (not dense and i % 3 == 2) else "air")
        if dense:
            s += label(36, 82, "More air packed into\nthe same space", TXT_L, NAVY_BLUE)
        else:
            s += label(36, 82, "Fewer, lighter\nmolecules", TXT_L, RED)
            s += molecule(50, 443) + label(70, 455, "air", MIN_TXT, "#ffffff", halo="#1f3d1f")
            s += molecule(160, 443, "vapour") + label(180, 455, "water vapour (lighter)", MIN_TXT, "#ffffff", halo="#1f3d1f")
        return s
    return dict(h=AD_H, sky="sky_day" if dense else "sky_hot", draw=draw,
                caption="DENSE AIR — high pressure, cold, dry" if dense else "THIN AIR — low pressure, hot, humid",
                color=NAVY_BLUE if dense else RED)


def _density():
    return picture([density_panel(True), density_panel(False)])


for _qid in (14, 15):
    R.add(_qid, "air-density-factors-v4", title(_qid), card(_qid), h=stack_height([AD_H, AD_H]), w=W)(_density)


# ------------------------------------------------------------------ relative humidity

RH_H = 640
# glass sizes follow the saturation vapour amounts at 10, 20 and 30°C (about 1 : 1.9 : 3.45); the water in each
# glass is the same amount, so it fills 100%, 52% and 28% of the glass
GLASSES = [(150, "10°C", 120, "100%"), (450, "20°C", 228, "52%"), (750, "30°C", 414, "28%")]


def rh_draw(w, h):
    s = f'<rect x="0" y="520" width="{w}" height="{h - 520}" fill="#d9c7a3"/>'
    s += f'<rect x="0" y="520" width="{w}" height="8" fill="#b8a27a"/>'
    water_h = 120
    for cx, temp, gh, rh in GLASSES:
        top, bw, tw = 520 - gh, 150, 170
        s += path(f"M {cx - tw / 2},{top} L {cx - bw / 2},520 L {cx + bw / 2},520 L {cx + tw / 2},{top}", "#ffffff",
                  extra=' fill-opacity="0.45"')
        wy = 520 - water_h
        ww = bw + (tw - bw) * water_h / gh
        s += path(f"M {cx - ww / 2:.1f},{wy} L {cx - bw / 2},520 L {cx + bw / 2},520 L {cx + ww / 2:.1f},{wy} Z",
                  "url(#sea)", extra=' fill-opacity="0.85"')
        s += path(f"M {cx - tw / 2},{top} L {cx - bw / 2},520 L {cx + bw / 2},520 L {cx + tw / 2},{top}", "none",
                  "#475569", 5)
        s += label(cx, top - 22, temp, TXT_L, RED if temp == "30°C" else INK, "middle")
        s += label(cx, 590, rh, TXT_L, "#1e3a8a", "middle", halo=None)
    s += label(36, 82, "Same water vapour,\nbigger capacity", TXT_M, INK)
    return s


@R.add(36, "relative-humidity-temperature-v3", title(36), card(36), h=stack_height([RH_H]), w=W)
def _():
    return picture([dict(h=RH_H, sky="sky_day", draw=rh_draw, caption="WARMER AIR → LOWER RELATIVE HUMIDITY",
                         color=RED)])


for _qid in (18, 622, 659, 1481, 1487):
    R.add(_qid, "relative-humidity-temperature-v3", title(_qid), card(_qid), h=stack_height([RH_H]), w=W)(R.items[-1]["draw"])
