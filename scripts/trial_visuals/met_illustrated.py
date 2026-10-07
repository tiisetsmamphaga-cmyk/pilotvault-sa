"""Meteorology explanation illustrations in the textbook look of the existing refined-batch-2 images:
shaded sky and terrain, metallic instruments, plain labels on the picture rather than boxes.
"""
import math

from aircraft import aircraft, aircraft_defs
from common import Registry
from kit import INK, MUTED, circle, line, path, t, template

R = Registry("meteorology", "/explanation-images/meteorology/refined-batch-2")

RED = "#d63a24"
BLUE = "#2f8be6"
ICE = "#8cc8ff"


def defs(*items):
    return "<defs>" + "".join(items) + "</defs>\n"


def lg(gid, stops, x1=0, y1=0, x2=0, y2=1):
    s = "".join(f'<stop offset="{o}" stop-color="{c}"{f" stop-opacity={chr(34)}{a}{chr(34)}" if a is not None else ""}/>'
                for o, c, a in [(st + (None,))[:3] for st in stops])
    return f'<linearGradient id="{gid}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">{s}</linearGradient>'


def rg(gid, stops, cx=0.5, cy=0.5, r=0.5):
    s = "".join(f'<stop offset="{o}" stop-color="{c}"{f" stop-opacity={chr(34)}{a}{chr(34)}" if a is not None else ""}/>'
                for o, c, a in [(st + (None,))[:3] for st in stops])
    return f'<radialGradient id="{gid}" cx="{cx}" cy="{cy}" r="{r}">{s}</radialGradient>'


SHADOW = ('<filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">'
          '<feDropShadow dx="0" dy="5" stdDeviation="7" flood-color="#0b1726" flood-opacity="0.28"/></filter>')


def arrowhead_marker(mid, color):
    return (f'<marker id="{mid}" markerUnits="userSpaceOnUse" markerWidth="26" markerHeight="26" refX="20" refY="13" '
            f'orient="auto"><path d="M0,2 L24,13 L0,24 L6,13 z" fill="{color}"/></marker>')


def flow(pts, color, mid, w=6, opacity=1.0):
    """Smooth streamline through pts with an arrowhead at the end."""
    d = f"M {pts[0][0]:.1f},{pts[0][1]:.1f} "
    for (x0, y0), (x1, y1) in zip(pts[:-1], pts[1:]):
        d += f"Q {x0:.1f},{y0:.1f} {(x0 + x1) / 2:.1f},{(y0 + y1) / 2:.1f} "
    d += f"L {pts[-1][0]:.1f},{pts[-1][1]:.1f}"
    return (f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{w}" stroke-linecap="round" '
            f'stroke-opacity="{opacity}" marker-end="url(#{mid})"/>\n')


def label(x, y, s, size=24, weight=400, fill=INK, anchor="middle", halo=True):
    """Text with a soft white halo so it stays readable over shaded backgrounds."""
    out = ""
    for i, ln in enumerate(s.split("\n")):
        yy = y + i * size * 1.22
        if halo:
            out += (f'<text x="{x}" y="{yy}" text-anchor="{anchor}" font-family="Arial,Helvetica,sans-serif" '
                    f'font-size="{size}" font-weight="{weight}" fill="none" stroke="{halo if isinstance(halo, str) else "#ffffff"}" '
                    f'stroke-width="6" stroke-linejoin="round" stroke-opacity="0.85">{ln}</text>')
        out += (f'<text x="{x}" y="{yy}" text-anchor="{anchor}" font-family="Arial,Helvetica,sans-serif" '
                f'font-size="{size}" font-weight="{weight}" fill="{fill}">{ln}</text>\n')
    return out


# ------------------------------------------------------------------ anabatic / katabatic

def ridge_y(x):
    """Valley floor on the left rising smoothly to a ridge on the right."""
    return 452 - 320 / (1 + math.exp(-(x - 360) / 80))


def terrain_path(ox):
    return f"M {ox},560 " + " ".join(f"L {ox + x},{ridge_y(x):.1f}" for x in range(0, 601, 5)) + f" L {ox + 600},560 Z"


def crescent(x, y, r, fill="#f1f5f9"):
    return (f'<path d="M {x},{y - r} A {r},{r} 0 1 0 {x},{y + r} A {r * 0.75:.1f},{r} 0 1 1 {x},{y - r} Z" '
            f'fill="{fill}"/>')


def tree(x, y, s=1.0, fill="#2f6b3a"):
    return (f'<rect x="{x - 2 * s:.1f}" y="{y - 8 * s:.1f}" width="{4 * s:.1f}" height="{10 * s:.1f}" fill="#5a4630"/>'
            f'<path d="M {x:.1f},{y - 40 * s:.1f} L {x + 13 * s:.1f},{y - 6 * s:.1f} L {x - 13 * s:.1f},{y - 6 * s:.1f} Z" '
            f'fill="{fill}"/>\n')


def slope_scene(ox, day):
    clip = f'<clipPath id="clip{ox}"><rect x="{ox}" y="0" width="600" height="560" rx="16"/></clipPath>'
    s = defs(clip)
    s += f'<g clip-path="url(#clip{ox})">'
    s += f'<rect x="{ox}" y="0" width="600" height="560" fill="url(#{"sky_day" if day else "sky_night"})"/>'
    if day:
        s += circle(ox + 105, 95, 90, "url(#sunglow)", "none", 0)
        s += circle(ox + 105, 95, 38, "#ffd23f", "#f5a300", 3)
    else:
        import random
        rnd = random.Random(3)
        for _ in range(40):
            s += circle(ox + rnd.uniform(10, 590), rnd.uniform(10, 230), rnd.uniform(1, 2.4), "#ffffff", "none", 0)
        s += crescent(ox + 105, 90, 34)
    s += path(terrain_path(ox), f"url(#{'ground_day' if day else 'ground_night'})", "#5d4a33" if day else "#1f2a2a", 2)
    # sunlit / radiating face highlight just along the slope surface
    s += path(" ".join(f"{'M' if i == 0 else 'L'} {ox + x},{ridge_y(x) + 2:.1f}" for i, x in enumerate(range(170, 600, 10))),
              "none", "#ffd46b" if day else "#7aa7d9", 7, extra=' stroke-opacity="0.55"')
    for x, sc in ((40, 1.0), (75, 0.8), (110, 1.1), (520, 0.7), (560, 0.8)):
        s += tree(ox + x, ridge_y(x) + 4, sc, "#2f6b3a" if day else "#1d3326")
    xs = list(range(200, 556, 30))
    for k, off in enumerate((18, 42, 66)):
        pts = [(ox + x, ridge_y(x) - off) for x in xs]
        if day:
            s += flow(pts, RED, "head_red", 6 - k, 1 - k * 0.2)
        else:
            s += flow(list(reversed(pts)), ICE, "head_ice", 6 - k, 1 - k * 0.2)
    if not day:
        # terrestrial radiation leaving the slope, cold air pooling in the valley
        x_top = 360 - 80 * math.log(320 / (452 - 418) - 1)
        s += (f'<path d="M {ox},418 L {ox + x_top:.1f},418 '
              + " ".join(f"L {ox + x},{ridge_y(x):.1f}" for x in range(int(x_top), -1, -5))
              + f' Z" fill="{BLUE}" fill-opacity="0.45"/>')
    s += "</g>"
    s += f'<rect x="{ox}" y="0" width="600" height="560" rx="16" fill="none" stroke="#94a3b8" stroke-width="2"/>'
    if day:
        s += label(ox + 40, 250, "Warm air rises\nup the sunlit slope", 26, 700, RED, "start")
        s += label(ox + 470, 420, "Slope heated\nby the sun", 21, 700, "#3b2f1f", halo=False)
    else:
        s += label(ox + 40, 250, "Cold, dense air\ndrains downhill", 26, 700, "#ffffff", "start", halo="#0f1d3d")
        s += label(ox + 470, 420, "Slope cools by\nradiation", 21, 700, "#e2e8f0", halo=False)
        s += label(ox + 100, 500, "Cold air pools\nin the valley", 20, 700, "#ffffff", halo="#0f1d3d")
    return s


@R.add(46, "anabatic-katabatic-v2", "Anabatic and Katabatic Winds",
       template("AN ANABATIC WIND BLOWS UP A SLOPE BY DAY",
                "A KATABATIC WIND BLOWS DOWN THE SLOPE AT NIGHT",
                [("Anabatic", "Sun heats the slope, the air in contact warms, becomes less dense and rises"),
                 ("Katabatic", "The slope cools by radiation at night; cold, dense air drains downhill"),
                 ("Memory aid", "ANA = UP (like ascend), KATA = DOWN")]), h=650, w=1240)
def _():
    s = defs(
        lg("sky_day", [(0, "#5fb4ea"), (1, "#e6f5fd")]),
        lg("sky_night", [(0, "#081230"), (1, "#26396b")]),
        rg("sunglow", [(0, "#fff3b0", 0.9), (1, "#fff3b0", 0)]),
        lg("ground_day", [(0, "#9c8a62"), (0.45, "#7f9a52"), (1, "#4f7a3a")]),
        lg("ground_night", [(0, "#4a4a55"), (0.5, "#33463a"), (1, "#1f2e26")]),
        arrowhead_marker("head_red", RED), arrowhead_marker("head_ice", ICE), arrowhead_marker("head_rad", "#f59e0b"),
    )
    s += slope_scene(10, True) + slope_scene(630, False)
    s += label(310, 610, "DAY — ANABATIC (upslope)", 28, 700, RED, halo=False)
    s += label(930, 610, "NIGHT — KATABATIC (downslope)", 28, 700, BLUE, halo=False)
    return s


# ------------------------------------------------------------------ shared scene pieces

PANEL_W, PANEL_H = 600, 560


def panel_open(ox, sky, w=PANEL_W, h=PANEL_H):
    return (defs(f'<clipPath id="clip{ox}"><rect x="{ox}" y="0" width="{w}" height="{h}" rx="16"/></clipPath>')
            + f'<g clip-path="url(#clip{ox})"><rect x="{ox}" y="0" width="{w}" height="{h}" fill="url(#{sky})"/>')


def panel_close(ox, w=PANEL_W, h=PANEL_H):
    return f'</g><rect x="{ox}" y="0" width="{w}" height="{h}" rx="16" fill="none" stroke="#94a3b8" stroke-width="2"/>'


def caption(x, s, color, y=PANEL_H + 50):
    return label(x, y, s, 28, 700, color, halo=False)


def sun(x, y, r=38):
    return circle(x, y, r * 2.4, "url(#sunglow)", "none", 0) + circle(x, y, r, "#ffd23f", "#f5a300", 3)


def puff_cloud(blobs, gid="puff"):
    """Cumulus built from overlapping shaded discs [(x, y, r)], back to front."""
    return "".join(circle(x, y, r, f"url(#{gid})", "none", 0) for x, y, r in blobs)


def molecules(ox, rnd, n, box, avoid=(), r=4.5, color="#ffffff", stroke="#3b82f6", opacity=0.9):
    x0, y0, x1, y1 = box
    s, k = "", 0
    while k < n:
        x, y = rnd.uniform(x0, x1), rnd.uniform(y0, y1)
        if any(a <= x <= c and b <= y <= d for a, b, c, d in avoid):
            continue
        s += f'<circle cx="{ox + x:.1f}" cy="{y:.1f}" r="{r}" fill="{color}" stroke="{stroke}" stroke-width="2" opacity="{opacity}"/>'
        k += 1
    return s


COMMON = (
    lg("sky_day", [(0, "#5fb4ea"), (1, "#e6f5fd")]),
    lg("sky_hot", [(0, "#f2a85c"), (0.55, "#fbd9a6"), (1, "#fff3dd")]),
    lg("sky_grey", [(0, "#64748b"), (1, "#cbd5e1")]),
    lg("sky_fog", [(0, "#b8c6d6"), (1, "#eef2f6")]),
    rg("sunglow", [(0, "#fff3b0", 0.9), (1, "#fff3b0", 0)]),
    rg("puff", [(0, "#ffffff"), (0.6, "#f1f5f9"), (1, "#a8b4c4")], 0.4, 0.35, 0.65),
    rg("puff_dark", [(0, "#94a3b8"), (0.6, "#64748b"), (1, "#334155")], 0.4, 0.35, 0.65),
    lg("ground_day", [(0, "#9c8a62"), (0.45, "#7f9a52"), (1, "#4f7a3a")]),
    lg("grass", [(0, "#8fb35e"), (1, "#4f7a3a")]),
    lg("hull", [(0, "#ffffff"), (1, "#d6dde6")]),
    lg("metal", [(0, "#eef1f5"), (0.5, "#b8c0cc"), (1, "#7c8796")]),
    lg("bezel", [(0, "#f3f4f6"), (0.5, "#9ca3af"), (1, "#4b5563")], 0, 0, 1, 1),
    rg("face", [(0, "#ffffff"), (0.85, "#f7f4ea"), (1, "#e7e1cf")]),
    rg("hub", [(0, "#9ca3af"), (1, "#111827")], 0.35, 0.35, 0.7),
    arrowhead_marker("head_red", RED), arrowhead_marker("head_blue", BLUE), arrowhead_marker("head_ice", ICE),
    arrowhead_marker("head_gold", "#e08a00"),
    '<filter id="soft" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="14"/></filter>',
    aircraft_defs(),
)


# ------------------------------------------------------------------ aneroid barometer

def capsule(cx, cy, w, h, folds=5):
    """Corrugated aneroid capsule seen side-on."""
    step = w / folds
    d = f"M {cx - w / 2},{cy - h / 2} "
    for i in range(folds):
        x0 = cx - w / 2 + i * step
        d += f"Q {x0 + step / 2},{cy - h / 2 - h * 0.28} {x0 + step},{cy - h / 2} "
    d += f"L {cx + w / 2},{cy + h / 2} "
    for i in range(folds):
        x0 = cx + w / 2 - i * step
        d += f"Q {x0 - step / 2},{cy + h / 2 + h * 0.28} {x0 - step},{cy + h / 2} "
    s = path(d + "Z", "url(#metal)", "#4b5563", 2.5)
    for i in range(1, folds):
        x = cx - w / 2 + i * step
        s += line(x, cy - h / 2 + 4, x, cy + h / 2 - 4, "#6b7280", 1.5)
    return s


def dial(cx, cy, r, hpa):
    ang = lambda v: math.radians(-120 + (v - 960) * 2.6)
    s = circle(cx, cy, r, "url(#bezel)", "#374151", 3)
    s += circle(cx, cy, r - 16, "url(#face)", "#6b7280", 2)
    for v in range(960, 1051, 2):
        a, major = ang(v), v % 10 == 0
        r1, r2 = r - 24, r - (42 if major else 33)
        s += line(cx + r1 * math.sin(a), cy - r1 * math.cos(a), cx + r2 * math.sin(a), cy - r2 * math.cos(a),
                  "#111827", 3 if major else 1.4)
        if v % 20 == 0:
            s += t(cx + (r - 62) * math.sin(a), cy - (r - 62) * math.cos(a) + 7, str(v), 18, 700, "#111827")
    s += t(cx, cy + 46, "hPa", 18, 700, MUTED)
    a = ang(hpa)
    dx, dy = math.sin(a), -math.cos(a)
    L = r - 30
    s += (f'<path d="M {cx - dx * 22 + dy * 6:.1f},{cy - dy * 22 - dx * 6:.1f} L {cx + dx * L:.1f},{cy + dy * L:.1f} '
          f'L {cx - dx * 22 - dy * 6:.1f},{cy - dy * 22 + dx * 6:.1f} Z" fill="#0f172a"/>')
    s += (f'<path d="M {cx + dx * (L - 30) + dy * 3:.1f},{cy + dy * (L - 30) - dx * 3:.1f} L {cx + dx * L:.1f},{cy + dy * L:.1f} '
          f'L {cx + dx * (L - 30) - dy * 3:.1f},{cy + dy * (L - 30) + dx * 3:.1f} Z" fill="{RED}"/>')
    return s + circle(cx, cy, 11, "url(#hub)", "#111827", 2)


def barometer_panel(ox, high):
    import random
    rnd = random.Random(11 if high else 5)
    s = panel_open(ox, "sky_day" if high else "sky_grey")
    if high:
        s += sun(ox + 90, 80, 32)
    else:
        for x, y, rx, ry in ((60, 40, 160, 60), (300, 20, 200, 55), (540, 45, 160, 60)):
            s += f'<ellipse cx="{ox + x}" cy="{y}" rx="{rx}" ry="{ry}" fill="#334155" opacity="0.75" filter="url(#soft)"/>'
    cx, top = ox + 300, 60
    # instrument: dial above a glass-fronted case holding the capsule
    case = (cx - 100, 300, 200, 150)
    avoid = [(150, 40, 450, 470), (60, 470, 540, 530)] + ([(40, 30, 150, 130)] if high else [])
    s += molecules(ox, rnd, 90 if high else 26, (15, 15, 585, 545), avoid)
    s += f'<rect x="{case[0]}" y="{case[1]}" width="{case[2]}" height="{case[3]}" rx="18" fill="url(#bezel)" stroke="#374151" stroke-width="3"/>'
    s += f'<rect x="{case[0] + 14}" y="{case[1] + 14}" width="{case[2] - 28}" height="{case[3] - 28}" rx="10" fill="#eef4fa" stroke="#6b7280" stroke-width="2"/>'
    h = 26 if high else 52
    base = case[1] + case[3] - 30
    s += f'<rect x="{cx - 70}" y="{base}" width="140" height="10" rx="3" fill="#6b7280"/>'
    s += capsule(cx, base - h / 2, 120, h)
    s += line(cx, base - h, cx, 225, "#1f2937", 4)
    s += dial(cx, 175, 125, 1032 if high else 988)
    arrows = [((cx - 160, 335), (cx - 112, 360)), ((cx + 160, 335), (cx + 112, 360)), ((cx - 160, 420), (cx - 112, 400)),
              ((cx + 160, 420), (cx + 112, 400))]
    for (x0, y0), (x1, y1) in arrows:
        if high:
            s += line(x0, y0, x1, y1, RED, 6).replace("/>", ' marker-end="url(#head_red)"/>')
        else:
            s += line(x1, y1, x0, y0, BLUE, 6).replace("/>", ' marker-end="url(#head_blue)"/>')
    if high:
        s += label(cx, 505, "More air presses on the capsule", 24, 700, RED)
    else:
        s += label(cx, 505, "Less air: the capsule expands", 24, 700, "#1e3a8a")
        for k in range(14):  # light rain
            x = ox + 20 + k * 42
            s += line(x, 110, x - 10, 140, "#e2e8f0", 2)
    return s + panel_close(ox)


@R.add(1536, "aneroid-barometer-v4", "How an Aneroid Barometer Works",
       template("A BAROMETER MEASURES ATMOSPHERIC PRESSURE",
                "THE ANEROID TYPE USES A SEALED CAPSULE THAT FLEXES AS OUTSIDE PRESSURE CHANGES",
                [("Capsule", "Sealed and partly emptied of air; a spring stops it collapsing"),
                 ("Pressure rises", "The capsule is squeezed thinner and the needle reads higher"),
                 ("Pressure falls", "The capsule expands and the needle reads lower"),
                 ("Units", "Read in hectopascals (hPa)")]), h=650, w=1240)
def _():
    s = defs(*COMMON)
    s += barometer_panel(10, True) + barometer_panel(630, False)
    s += caption(310, "HIGH PRESSURE — reads higher", RED)
    s += caption(930, "LOW PRESSURE — reads lower", BLUE)
    return s


# ------------------------------------------------------------------ density altitude

def airfield_panel(ox, hot):
    import random
    rnd = random.Random(21 if hot else 4)
    s = panel_open(ox, "sky_hot" if hot else "sky_day")
    if hot:
        s += sun(ox + 500, 80, 40)
    # distant mountains and the airfield plateau
    s += path(f"M {ox},330 L {ox + 90},250 L {ox + 170},300 L {ox + 260},220 L {ox + 360},290 L {ox + 450},235 "
              f"L {ox + 600},300 L {ox + 600},560 L {ox},560 Z", "#9fb3c8" if not hot else "#c8a98a", "none", 0)
    s += f'<rect x="{ox}" y="455" width="600" height="105" fill="url(#grass)"/>'
    s += f'<rect x="{ox + 40}" y="462" width="420" height="16" rx="3" fill="#475569"/>'
    for k in range(8):
        s += f'<rect x="{ox + 60 + k * 50}" y="468" width="26" height="4" fill="#ffffff"/>'
    s += molecules(ox, rnd, 30 if hot else 95, (15, 20, 585, 440), [(20, 30, 360, 190)] + ([(420, 20, 600, 150)] if hot else []),
                   4, "#ffffff", "#ef4444" if hot else "#3b82f6", 0.85)
    if hot:
        for k in range(6):  # heat shimmer
            x = ox + 70 + k * 60
            s += path(f"M {x},452 q 8,-10 0,-20 q -8,-10 0,-20", "none", "#f97316", 3, extra=' stroke-opacity="0.7"')
    # climb path and aircraft
    if hot:
        pts = [(ox + 90, 458), (ox + 250, 440), (ox + 420, 395), (ox + 560, 345)]
        s += flow(pts, RED, "head_red", 4, 0.55)
        s += aircraft(ox + 350, 400, 190, 9)
    else:
        pts = [(ox + 90, 458), (ox + 200, 410), (ox + 330, 300), (ox + 470, 170)]
        s += flow(pts, BLUE, "head_blue", 4, 0.55)
        s += aircraft(ox + 290, 318, 190, 26)
    s += label(ox + 520, 510, "Airfield 5,000 ft", 21, 700, "#1f2937", "end", halo=False)
    if hot:
        s += label(ox + 30, 60, "Hot day 30°C", 26, 700, RED, "start")
        s += label(ox + 30, 92, "Thin air: long take-off,\nweak climb", 21, 700, "#7c2d12", "start")
    else:
        s += label(ox + 30, 60, "Standard day 5°C", 26, 700, "#1e40af", "start")
        s += label(ox + 30, 92, "Denser air: normal\nperformance", 21, 700, "#1e3a8a", "start")
    return s + panel_close(ox)


@R.add(19, "density-altitude-v2", "Density Altitude",
       template("DENSITY ALTITUDE IS PRESSURE ALTITUDE CORRECTED FOR TEMPERATURE",
                "HOT AIR IS LESS DENSE, SO THE AIRCRAFT PERFORMS AS IF IT WERE HIGHER",
                [("Start with", "Pressure altitude (1013 hPa set on the altimeter)"),
                 ("Correct for", "How far the temperature is above or below ISA"),
                 ("Rule of thumb", "About 120 ft for every 1°C above ISA"),
                 ("Example", "5,000 ft at 30°C: ISA is 5°C, so +25°C ≈ +3,000 ft, giving about 8,000 ft")],
                formula="Density altitude ≈ pressure altitude + 120 × (OAT − ISA temperature)"), h=650, w=1240)
def _():
    s = defs(*COMMON)
    s += airfield_panel(10, False) + airfield_panel(630, True)
    s += caption(310, "ISA DAY — performs as at 5,000 ft", "#1e40af")
    s += caption(930, "HOT DAY — performs as at ≈ 8,000 ft", RED)
    return s


# ------------------------------------------------------------------ ISA sea level

@R.add(32, "isa-sea-level-v2", "ISA Sea-Level Values",
       template("ISA SEA-LEVEL DENSITY IS 1.225 kg/m³ (1225 g/m³)",
                "THE STANDARD ATMOSPHERE FIXES PRESSURE, TEMPERATURE AND DENSITY AT MEAN SEA LEVEL",
                [("Pressure", "1013.25 hPa"),
                 ("Temperature", "+15°C"),
                 ("Density", "1.225 kg/m³ = 1225 g/m³"),
                 ("Lapse rate", "1.98°C per 1,000 ft up to the tropopause at 36,090 ft (11 km)")]), h=630, w=1240)
def _():
    import random
    rnd = random.Random(9)
    W = 1220
    s = defs(*COMMON, lg("sea", [(0, "#2b8fd6"), (1, "#0d4f8b")]), lg("sand", [(0, "#f1dfb5"), (1, "#d9bf86")]),
             lg("cube", [(0, "#dbeafe", 0.75), (1, "#93c5fd", 0.6)], 0, 0, 1, 1))
    s += panel_open(10, "sky_day", W)
    s += sun(1080, 90, 36)
    s += puff_cloud([(700, 100, 34), (740, 85, 44), (785, 102, 32)])
    s += f'<rect x="10" y="400" width="{W}" height="160" fill="url(#sea)"/>'
    for k in range(10):
        s += path(f"M {40 + k * 70},{430 + (k % 3) * 30} q 15,-8 30,0", "none", "#bfdbfe", 3, extra=' stroke-opacity="0.7"')
    s += path("M 760,560 L 830,436 C 900,430 1100,428 1230,426 L 1230,560 Z", "url(#sand)", "none", 0)
    s += label(60, 395, "Mean sea level", 22, 700, "#ffffff", "start", halo="#0d4f8b")
    # one cubic metre of air on a kitchen scale standing on the beach
    x, y, a, d = 900, 200, 140, 34
    s += f'<rect x="{x - 20}" y="374" width="{a + 74}" height="58" rx="10" fill="url(#metal)" stroke="#4b5563" stroke-width="2"/>'
    s += f'<rect x="{x + a / 2 - 52}" y="384" width="120" height="40" rx="6" fill="#1f2937"/>'
    s += t(x + a / 2 + 8, 413, "1225 g", 26, 800, "#4ade80")
    s += f'<rect x="{x - 30}" y="360" width="{a + 94}" height="14" rx="5" fill="url(#metal)" stroke="#4b5563" stroke-width="2"/>'
    s += (f'<path d="M {x},{y + d} L {x + d},{y} L {x + a + d},{y} L {x + a + d},{y + a} L {x + a},{y + a + d} '
          f'L {x},{y + a + d} Z" fill="url(#cube)" stroke="#1d4ed8" stroke-width="3"/>')
    s += path(f"M {x},{y + d} L {x + a},{y + d} L {x + a + d},{y} M {x + a},{y + d} L {x + a},{y + a + d}", "none",
              "#1d4ed8", 3)
    for _ in range(30):
        s += circle(x + rnd.uniform(12, a - 12), y + d + rnd.uniform(12, a - 12), 4.5, "#ffffff", "#3b82f6", 2)
    s += label(x + (a + d) / 2, y - 22, "1 m³ of air", 26, 700, "#1e3a8a")
    # the other ISA values written on the sky
    s += label(60, 120, "ISA at mean sea level", 30, 700, "#0f172a", "start")
    s += label(60, 175, "Pressure   1013.25 hPa", 26, 700, "#1f2937", "start")
    s += label(60, 215, "Temperature   +15°C", 26, 700, "#1f2937", "start")
    s += label(60, 255, "Density   1225 g/m³", 26, 700, RED, "start")
    s += label(60, 300, "Cools 1.98°C per 1,000 ft as you climb", 21, 700, "#334155", "start")
    s += panel_close(10, W)
    s += caption(620, "ISA SEA LEVEL — 1 m³ of air has a mass of 1225 g (1.225 kg)", "#1e3a8a")
    return s


# ------------------------------------------------------------------ thunderstorm ingredients

@R.add(53, "thunderstorm-ingredients-v2", "What a Thunderstorm Needs",
       template("A THUNDERSTORM NEEDS MOIST AIR, INSTABILITY AND A LIFTING ACTION",
                "TAKE AWAY ANY ONE OF THE THREE AND NO CUMULONIMBUS FORMS",
                [("Moisture", "Enough water vapour to build deep cloud and release latent heat"),
                 ("Instability", "Rising air stays warmer than its surroundings, so it keeps rising"),
                 ("Lifting action", "Surface heating, a front, high ground or convergence starts the air rising")]),
       h=630, w=1240)
def _():
    W = 1220
    s = defs(*COMMON, lg("sea", [(0, "#2b8fd6"), (1, "#0d4f8b")]),
             lg("anvil", [(0, "#ffffff"), (1, "#cbd5e1")]), lg("cbbase", [(0, "#64748b"), (1, "#1e293b")]),
             lg("rain", [(0, "#64748b", 0.55), (1, "#64748b", 0.15)]))
    s += panel_open(10, "sky_day", W)
    s += sun(120, 90, 34)
    # ground: sea on the left, land rising to a hill on the right
    s += f'<rect x="10" y="480" width="330" height="80" fill="url(#sea)"/>'
    s += path("M 330,480 C 500,470 700,476 860,470 C 960,466 1040,420 1120,400 C 1170,392 1210,400 1230,410 "
              "L 1230,560 L 330,560 Z", "url(#grass)", "none", 0)
    # cumulonimbus: anvil, tower of shaded puffs, dark flat base
    cx = 700
    s += path(f"M {cx - 290},88 C {cx - 160},62 {cx + 200},58 {cx + 340},82 C {cx + 250},98 {cx + 120},110 {cx + 80},150 "
              f"L {cx - 90},150 C {cx - 130},112 {cx - 220},100 {cx - 290},88 Z", "url(#anvil)", "#94a3b8", 2)
    tower = [(cx - 40, 160, 55), (cx + 40, 165, 55), (cx - 80, 220, 62), (cx, 205, 70), (cx + 85, 225, 60),
             (cx - 120, 290, 66), (cx - 40, 275, 75), (cx + 50, 280, 75), (cx + 130, 295, 62),
             (cx - 150, 355, 62), (cx - 70, 345, 72), (cx + 20, 345, 76), (cx + 110, 350, 70), (cx + 175, 365, 52)]
    s += puff_cloud(tower)
    s += path(f"M {cx - 200},380 C {cx - 120},405 {cx + 120},405 {cx + 225},380 L {cx + 210},412 L {cx - 190},412 Z",
              "url(#cbbase)", "none", 0)
    s += f'<rect x="{cx - 170}" y="410" width="250" height="{470 - 410}" fill="url(#rain)"/>'
    for k in range(16):
        x = cx - 160 + k * 15
        s += line(x, 416, x - 12, 466, "#475569", 2)
    s += path(f"M {cx + 120},412 L {cx + 100},440 L {cx + 118},440 L {cx + 95},476", "none", "#facc15", 5)
    # 2: instability, rising air inside the cloud
    for k, off in enumerate((-20, 20, 60)):
        pts = [(cx + off, 400), (cx + off + 10, 320), (cx + off - 5, 240), (cx + off + 5, 165)]
        s += flow(pts, RED, "head_red", 7 - 2 * k, 1 - k * 0.2)
    # 1: moist air flowing in from the sea
    for k, off in enumerate((0, 22, 44)):
        pts = [(40, 455 - off), (200, 450 - off), (380, 440 - off), (500, 425 - off), (560, 405 - off)]
        s += flow(pts, BLUE, "head_blue", 6 - k, 1 - k * 0.25)
    # 3: lift, warm thermals rising off the heated ground towards the cloud base
    for x in (840, 885, 930):
        y0 = 474
        s += path(f"M {x},{y0} q 14,-22 0,-44 q -14,-22 0,-44", "none", "#e08a00", 4, extra=' marker-end="url(#head_gold)"')
    s += label(40, 360, "1  Moist air flows in", 26, 700, BLUE, "start")
    s += label(cx + 170, 250, "2  Unstable air\nkeeps rising", 26, 700, RED, "start")
    s += label(1210, 440, "3  Something lifts it:\nheating, hills, fronts", 24, 700, "#9a5b00", "end")
    s += panel_close(10, W)
    s += caption(620, "MOIST AIR + INSTABILITY + LIFT = THUNDERSTORM", "#0f172a")
    return s


# ------------------------------------------------------------------ freezing fog

@R.add(1471, "freezing-fog-v2", "Freezing Fog",
       template("FREEZING FOG IS MADE OF SUPERCOOLED WATER DROPLETS",
                "THE DROPLETS STAY LIQUID BELOW 0°C AND FREEZE ON CONTACT WITH A SURFACE",
                [("Temperature", "Below 0°C"),
                 ("Droplets", "Liquid (supercooled), not ice crystals"),
                 ("On contact", "They freeze onto aircraft, trees and fences as rime ice"),
                 ("Hazard", "Poor visibility plus icing on the ground and during take-off")]), h=630, w=1240)
def _():
    import random
    rnd = random.Random(2)
    W = 1220
    s = defs(*COMMON, lg("frost", [(0, "#e8eef5"), (1, "#c3cfdc")]),
             rg("drop", [(0, "#ffffff"), (0.35, "#bfe0ff"), (1, "#2f8be6")], 0.35, 0.3, 0.75),
             rg("lens", [(0, "#f8fbff"), (1, "#dbe8f5")]))
    s += panel_open(10, "sky_fog", W)
    # far frosted trees and ground
    for k in range(14):
        x = 30 + k * 90 + rnd.uniform(-20, 20)
        h = rnd.uniform(70, 120)
        s += f'<path d="M {x},{420 - h} L {x + 28},420 L {x - 28},420 Z" fill="#8a9bb0" opacity="0.6"/>'
    s += f'<rect x="10" y="410" width="{W}" height="150" fill="url(#frost)"/>'
    for x, y, rx, ry in ((200, 380, 300, 80), (600, 390, 340, 70), (1000, 370, 320, 80), (400, 300, 260, 50),
                         (900, 290, 260, 50)):
        s += f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="#ffffff" opacity="0.6" filter="url(#soft)"/>'
    # fence with rime on the posts, parked aircraft with rime on the nose and fin
    for k in range(5):
        x = 560 + k * 62
        s += f'<rect x="{x}" y="380" width="12" height="80" rx="2" fill="#5b4a38"/>'
        s += "".join(f'<path d="M {x},{386 + j * 11} l -10,5 l 10,5 z" fill="#ffffff" stroke="#60a5fa" stroke-width="1"/>'
                     for j in range(6))
    s += line(560, 398, 820, 398, "#5b4a38", 4) + line(560, 430, 820, 430, "#5b4a38", 4)
    s += aircraft(1030, 440, 300, 0, rime=True)
    s += f'<rect x="10" y="470" width="{W}" height="90" fill="#ffffff" opacity="0.25" filter="url(#soft)"/>'
    # magnifier showing liquid droplets
    mx, my, mr = 270, 230, 140
    s += line(mx + mr * 0.7, my + mr * 0.7, mx + mr * 1.05, my + mr * 1.05, "#334155", 18)
    s += circle(mx, my, mr, "url(#lens)", "#334155", 10)
    for _ in range(26):
        a, r = rnd.uniform(0, 2 * math.pi), mr * math.sqrt(rnd.uniform(0, 0.78))
        s += circle(mx + r * math.cos(a), my + r * math.sin(a), rnd.uniform(9, 14), "url(#drop)", "#1d6fd6", 1.5)
    s += label(mx, my + mr + 52, "Tiny LIQUID droplets at −3°C", 26, 700, "#1e3a8a")
    s += label(mx, my + mr + 84, "(supercooled)", 22, 700, "#334155")
    s += label(830, 120, "Air temperature −3°C", 30, 700, "#0f172a")
    s += label(830, 175, "They freeze on contact:\nrime ice on posts and aircraft", 24, 700, "#1d4ed8")
    s += panel_close(10, W)
    s += caption(620, "FREEZING FOG — supercooled droplets that freeze on contact", "#1e3a8a")
    return s
