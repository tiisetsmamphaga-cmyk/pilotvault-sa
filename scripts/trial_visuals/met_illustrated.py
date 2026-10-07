"""Meteorology explanation illustrations in the textbook look of the existing refined-batch-2 images:
shaded sky and terrain, metallic instruments, plain labels on the picture rather than boxes.
"""
import math

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


# ------------------------------------------------------------------ aneroid barometer

def capsule(cx, cy, w, h, folds=5, gid="metal"):
    """Corrugated aneroid capsule seen side-on."""
    d = f"M {cx - w / 2},{cy} "
    step = w / folds
    for i in range(folds):
        x0 = cx - w / 2 + i * step
        d += f"C {x0 + step * 0.25},{cy - h * 0.62} {x0 + step * 0.75},{cy - h * 0.38} {x0 + step},{cy - h / 2 - (0 if i % 2 else 0)} "
    d = f"M {cx - w / 2},{cy - h / 2} "
    for i in range(folds):
        x0 = cx - w / 2 + i * step
        d += f"Q {x0 + step / 2},{cy - h / 2 - h * 0.28} {x0 + step},{cy - h / 2} "
    d += f"L {cx + w / 2},{cy + h / 2} "
    for i in range(folds):
        x0 = cx + w / 2 - i * step
        d += f"Q {x0 - step / 2},{cy + h / 2 + h * 0.28} {x0 - step},{cy + h / 2} "
    d += "Z"
    s = path(d, f"url(#{gid})", "#4b5563", 2.5)
    for i in range(1, folds):
        x = cx - w / 2 + i * step
        s += line(x, cy - h / 2 + 4, x, cy + h / 2 - 4, "#6b7280", 1.5)
    return s


def needle(cx, cy, ang, length, color="#0f172a", tip=RED):
    a = math.radians(ang)
    dx, dy = math.sin(a), -math.cos(a)
    px, py = -dy, dx
    tipx, tipy = cx + dx * length, cy + dy * length
    tail = (cx - dx * length * 0.22, cy - dy * length * 0.22)
    s = (f'<path d="M {tail[0] + px * 7:.1f},{tail[1] + py * 7:.1f} L {tipx:.1f},{tipy:.1f} '
         f'L {tail[0] - px * 7:.1f},{tail[1] - py * 7:.1f} Z" fill="{color}"/>')
    s += (f'<path d="M {cx + dx * length * 0.72 + px * 3.5:.1f},{cy + dy * length * 0.72 + py * 3.5:.1f} L {tipx:.1f},{tipy:.1f} '
          f'L {cx + dx * length * 0.72 - px * 3.5:.1f},{cy + dy * length * 0.72 - py * 3.5:.1f} Z" fill="{tip}"/>')
    return s + circle(cx, cy, 13, "url(#hub)", "#111827", 2)


def ang_for(hpa):
    return -120 + (hpa - 950) * 2.4


@R.add(1536, "aneroid-barometer-v3", "How an Aneroid Barometer Works",
       template("A BAROMETER MEASURES ATMOSPHERIC PRESSURE",
                "THE ANEROID TYPE USES A SEALED CAPSULE THAT FLEXES AS OUTSIDE PRESSURE CHANGES",
                [("Capsule", "Sealed and partly emptied of air; a spring stops it collapsing"),
                 ("Pressure rises", "The capsule is squeezed thinner"),
                 ("Pressure falls", "The capsule expands"),
                 ("Reading", "Levers magnify the tiny movement and turn the needle, read in hPa")]), h=770, w=1240)
def _():
    s = defs(
        lg("bezel", [(0, "#f3f4f6"), (0.5, "#9ca3af"), (1, "#4b5563")], 0, 0, 1, 1),
        rg("face", [(0, "#ffffff"), (0.85, "#f7f4ea"), (1, "#e7e1cf")]),
        lg("metal", [(0, "#eef1f5"), (0.5, "#b8c0cc"), (1, "#7c8796")]),
        rg("hub", [(0, "#9ca3af"), (1, "#111827")], 0.35, 0.35, 0.7),
        lg("glass", [(0, "#ffffff", 0.55), (0.4, "#ffffff", 0)], 0, 0, 1, 1),
        SHADOW, arrowhead_marker("head_red", RED), arrowhead_marker("head_blue", BLUE),
    )
    cx, cy, R0 = 360, 330, 270
    s += circle(cx, cy, R0, "url(#bezel)", "#374151", 3).replace("/>", ' filter="url(#shadow)"/>')
    s += circle(cx, cy, R0 - 26, "url(#face)", "#6b7280", 2)
    # scale
    for hpa in range(950, 1051, 2):
        a = math.radians(ang_for(hpa))
        major = hpa % 10 == 0
        r1, r2 = R0 - 40, R0 - (68 if major else 54)
        s += line(cx + r1 * math.sin(a), cy - r1 * math.cos(a), cx + r2 * math.sin(a), cy - r2 * math.cos(a),
                  "#111827", 3 if major else 1.5)
        if major:
            rt = R0 - 94
            s += t(cx + rt * math.sin(a), cy - rt * math.cos(a) + 8, str(hpa), 21, 700, "#111827")
    s += t(cx, cy - 60, "hPa", 26, 700, MUTED)
    # cut-away window showing the mechanism
    s += (f'<rect x="{cx - 110}" y="{cy + 46}" width="220" height="166" rx="18" fill="#f1f5f9" stroke="#94a3b8" '
          f'stroke-width="2" stroke-dasharray="7 6"/>')
    s += f'<rect x="{cx - 95}" y="{cy + 178}" width="190" height="16" rx="4" fill="#6b7280"/>'
    s += capsule(cx, cy + 150, 170, 44)
    # spring holding the capsule open
    zz = " ".join(f"L {cx + (12 if i % 2 else -12)},{cy + 126 - i * 8}" for i in range(1, 8))
    s += path(f"M {cx},{cy + 128} {zz} L {cx},{cy + 62}", "none", "#374151", 3)
    s += f'<rect x="{cx - 40}" y="{cy + 54}" width="80" height="10" rx="3" fill="#4b5563"/>'
    # linkage to needle hub
    s += path(f"M {cx + 60},{cy + 128} L {cx + 60},{cy + 84} L {cx + 20},{cy + 30} L {cx},{cy}", "none", "#1f2937", 3.5)
    s += circle(cx + 60, cy + 84, 5, "#1f2937", "none", 0) + circle(cx + 20, cy + 30, 5, "#1f2937", "none", 0)
    s += needle(cx, cy, ang_for(1015), R0 - 52)
    s += f'<circle cx="{cx}" cy="{cy}" r="{R0 - 26}" fill="url(#glass)"/>'
    # labels with leaders
    def lead(px, py, ly, head, sub=None):
        o = line(px, py, 760, ly, "#475569", 2) + circle(px, py, 5, "#475569", "none", 0)
        o += label(772, ly + 8, head, 25, 700, INK, "start", halo=False)
        if sub:
            o += label(772, ly + 38, sub, 21, 400, MUTED, "start", halo=False)
        return o
    a = math.radians(ang_for(1015))
    s += lead(cx + 150 * math.sin(a), cy - 150 * math.cos(a), cy - 190, "Needle reads pressure", "here 1015 hPa")
    s += lead(cx + 60, cy + 84, cy - 10, "Levers magnify the movement")
    s += lead(cx + 12, cy + 114, cy + 118, "Spring stops it collapsing")
    s += lead(cx + 85, cy + 150, cy + 178, "Sealed capsule", "partly emptied of air")
    # what happens when pressure changes
    y0 = 630
    s += capsule(830, y0 + 20, 110, 24)
    for x in (800, 860):
        s += line(x, y0 - 40, x, y0 - 2, RED, 4).replace("/>", ' marker-end="url(#head_red)"/>')
    s += label(830, y0 + 82, "Pressure rises:\ncapsule squeezed", 20, 700, RED, halo=False)
    s += capsule(1080, y0 + 20, 110, 44)
    for x in (1050, 1110):
        s += line(x, y0 - 6, x, y0 - 44, BLUE, 4).replace("/>", ' marker-end="url(#head_blue)"/>')
    s += label(1080, y0 + 82, "Pressure falls:\ncapsule expands", 20, 700, BLUE, halo=False)
    return s
