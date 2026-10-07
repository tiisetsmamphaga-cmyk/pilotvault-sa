"""Shared parts for explanation illustrations (docs/EXPLANATION_ILLUSTRATION_STANDARD.md).

Phone first: pictures are drawn on a 900-wide canvas and shown about 330 px wide on a phone, so every label
is at least MIN_TXT (about 12 px on a phone). Comparisons are stacked panels, top and bottom.

Parts: panel stacks with captions, sky and ground gradients, terrain, sun, moon, stars, trees, airflow
streamlines, labels with halos, molecule grids, clouds measured from the cloud-types chart (cumulus,
cumulonimbus, rain, lightning, fog), the aircraft from aircraft.py (side and top view), and for navigation an
aerial view of the ground, angle arcs and north arrows.
"""
import math
import random

from aircraft import aircraft, aircraft_defs, aircraft_top  # noqa: F401  (re-exported for scene modules)

W = 900                      # canvas width
PHONE_W = 328                # width the picture gets on a phone (CSS px)
TXT_L = 42                   # main label in a panel
TXT_M = 34                   # secondary label
CAPTION = 38                 # caption under a panel
MIN_TXT = 32                 # nothing smaller: 32 * 328 / 900 = 11.7 px on a phone
FLOW_W = 9                   # main streamline width

INK = "#0f172a"
RED = "#d63a24"
BLUE = "#2f8be6"
NAVY_BLUE = "#1e40af"
ICE = "#8cc8ff"
GOLD = "#e08a00"
FONT = "Arial,Helvetica,sans-serif"


# ------------------------------------------------------------------ svg helpers

def stop_list(stops):
    out = ""
    for st in stops:
        o, c = st[0], st[1]
        a = st[2] if len(st) > 2 else None
        out += f'<stop offset="{o}" stop-color="{c}"' + (f' stop-opacity="{a}"' if a is not None else "") + "/>"
    return out


def lg(gid, stops, x1=0, y1=0, x2=0, y2=1, user=None):
    """Linear gradient; user=(x1, y1, x2, y2) switches to userSpaceOnUse coordinates."""
    if user:
        x1, y1, x2, y2 = user
        return (f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="{x1:.1f}" y1="{y1:.1f}" '
                f'x2="{x2:.1f}" y2="{y2:.1f}">{stop_list(stops)}</linearGradient>')
    return f'<linearGradient id="{gid}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">{stop_list(stops)}</linearGradient>'


def rg(gid, stops, cx=0.5, cy=0.5, r=0.5):
    return f'<radialGradient id="{gid}" cx="{cx}" cy="{cy}" r="{r}">{stop_list(stops)}</radialGradient>'


def defs(*items):
    return "<defs>" + "".join(items) + "</defs>\n"


def circle(x, y, r, fill, stroke="none", sw=0, extra=""):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{extra}/>'


def path(d, fill="none", stroke="none", w=0, extra=""):
    return (f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{w}" stroke-linejoin="round" '
            f'stroke-linecap="round"{extra}/>\n')


def head(mid, color, size=44):
    return (f'<marker id="{mid}" markerUnits="userSpaceOnUse" markerWidth="{size}" markerHeight="{size}" '
            f'refX="{size * 0.77:.1f}" refY="{size / 2}" orient="auto"><path d="M0,{size * 0.08:.1f} '
            f'L{size * 0.92:.1f},{size / 2} L0,{size * 0.92:.1f} L{size * 0.23:.1f},{size / 2} z" fill="{color}"/></marker>')


COMMON_DEFS = (
    lg("sky_day", [(0, "#5fb4ea"), (1, "#e6f5fd")]),
    lg("sky_night", [(0, "#081230"), (1, "#26396b")]),
    lg("sky_hot", [(0, "#f2a85c"), (0.55, "#fbd9a6"), (1, "#fff3dd")]),
    lg("sky_grey", [(0, "#64748b"), (1, "#cbd5e1")]),
    lg("sky_fog", [(0, "#b8c6d6"), (1, "#eef2f6")]),
    rg("sunglow", [(0, "#fff3b0", 0.9), (1, "#fff3b0", 0)]),
    lg("ground_day", [(0, "#9c8a62"), (0.45, "#7f9a52"), (1, "#4f7a3a")]),
    lg("ground_night", [(0, "#4a4a55"), (0.5, "#33463a"), (1, "#1f2e26")]),
    lg("grass", [(0, "#8fb35e"), (1, "#4f7a3a")]),
    lg("sea", [(0, "#2b8fd6"), (1, "#0d4f8b")]),
    lg("aerial", [(0, "#9db57d"), (1, "#86a468")]),
    lg("sand", [(0, "#f1dfb5"), (1, "#d9bf86")]),
    lg("frost", [(0, "#e8eef5"), (1, "#c3cfdc")]),
    lg("metal", [(0, "#eef1f5"), (0.5, "#b8c0cc"), (1, "#7c8796")]),
    lg("bezel", [(0, "#f3f4f6"), (0.5, "#9ca3af"), (1, "#4b5563")], 0, 0, 1, 1),
    rg("face", [(0, "#ffffff"), (0.85, "#f7f4ea"), (1, "#e7e1cf")]),
    rg("hub", [(0, "#9ca3af"), (1, "#111827")], 0.35, 0.35, 0.7),
    rg("drop", [(0, "#ffffff"), (0.35, "#bfe0ff"), (1, "#2f8be6")], 0.35, 0.3, 0.75),
    rg("lens", [(0, "#f8fbff"), (1, "#dbe8f5")]),
    rg("lobe_shade", [(0, "#ffffff", 0), (0.62, "#ffffff", 0), (1, "#5b6b80", 0.42)], 0.38, 0.32, 0.62),
    head("head_red", RED), head("head_blue", BLUE), head("head_ice", ICE), head("head_gold", GOLD),
    head("head_white", "#ffffff"), head("head_ink", INK),
    '<filter id="soft" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="14"/></filter>',
    '<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="4"/></filter>',
    aircraft_defs(),
)


def label(x, y, s, size=TXT_L, fill=INK, anchor="start", halo="#ffffff", weight=700, role="label"):
    """Bold label with a soft halo; one <text> per line. role='caption' marks captions for the checker."""
    assert size >= MIN_TXT, f"label '{s}' at {size}px is below the {MIN_TXT}px minimum"
    out = ""
    for i, ln in enumerate(s.split("\n")):
        yy = y + i * size * 1.18
        common = (f'x="{x:.1f}" y="{yy:.1f}" text-anchor="{anchor}" font-family="{FONT}" font-size="{size}" '
                  f'font-weight="{weight}"')
        if halo:
            out += (f'<text {common} fill="none" stroke="{halo}" stroke-width="{size * 0.22:.1f}" '
                    f'stroke-linejoin="round" stroke-opacity="0.9" data-halo="1">{ln}</text>')
        out += f'<text {common} fill="{fill}" data-{role}="{abs(hash((s, round(x), round(y)))) % 1000000}">{ln}</text>\n'
    return out


# ------------------------------------------------------------------ panels

def stack(panels, width=W, gap=28, cap_h=70):
    """panels: [dict(h, sky, draw, caption, color)]; draw(w, h) returns SVG in panel-local coordinates.
    Panels are stacked top to bottom with a caption band under each. Returns (svg, total height)."""
    s, y = "", 0
    for i, p in enumerate(panels):
        h = p["h"]
        s += f'<g transform="translate(0,{y})" data-panel="{i}" data-box="0,{y},{width},{h}">'
        s += defs(f'<clipPath id="pclip{i}"><rect x="0" y="0" width="{width}" height="{h}" rx="18"/></clipPath>')
        s += f'<g clip-path="url(#pclip{i})"><rect x="0" y="0" width="{width}" height="{h}" fill="url(#{p["sky"]})"/>'
        s += p["draw"](width, h)
        s += f'</g><rect x="1" y="1" width="{width - 2}" height="{h - 2}" rx="18" fill="none" stroke="#94a3b8" stroke-width="2"/></g>'
        if p.get("caption"):
            s += label(width / 2, y + h + cap_h * 0.66, p["caption"], CAPTION, p.get("color", INK), "middle",
                       halo=None, role="caption")
        y += h + (cap_h if p.get("caption") else 0) + gap
    return s, y - gap


def stack_height(heights, captions=True, gap=28, cap_h=70):
    return sum(heights) + (cap_h * len(heights) if captions else 0) + gap * (len(heights) - 1)


# ------------------------------------------------------------------ scenery

def sun(x, y, r=40):
    return circle(x, y, r * 2.4, "url(#sunglow)") + circle(x, y, r, "#ffd23f", "#f5a300", 3)


def moon(x, y, r=34, fill="#f1f5f9"):
    return path(f"M {x},{y - r} A {r},{r} 0 1 0 {x},{y + r} A {r * 0.75:.1f},{r} 0 1 1 {x},{y - r} Z", fill)


def stars(rnd, box, n=40):
    x0, y0, x1, y1 = box
    return "".join(circle(rnd.uniform(x0, x1), rnd.uniform(y0, y1), rnd.uniform(1.2, 2.8), "#ffffff") for _ in range(n))


def tree(x, y, s=1.0, fill="#2f6b3a"):
    return (f'<rect x="{x - 3 * s:.1f}" y="{y - 10 * s:.1f}" width="{6 * s:.1f}" height="{13 * s:.1f}" fill="#5a4630"/>'
            + path(f"M {x:.1f},{y - 56 * s:.1f} L {x + 18 * s:.1f},{y - 8 * s:.1f} L {x - 18 * s:.1f},{y - 8 * s:.1f} Z", fill))


def terrain(fn, w, h, fill, stroke="none", step=5):
    """Ground below the curve y = fn(x)."""
    d = f"M 0,{h} " + " ".join(f"L {x},{fn(x):.1f}" for x in range(0, w + 1, step)) + f" L {w},{h} Z"
    return path(d, fill, stroke, 2 if stroke != "none" else 0)


def flow(pts, color, mid, w=FLOW_W, opacity=1.0):
    """Smooth streamline through pts with an arrowhead at the end."""
    d = f"M {pts[0][0]:.1f},{pts[0][1]:.1f} "
    for (x0, y0), (x1, y1) in zip(pts[:-1], pts[1:]):
        d += f"Q {x0:.1f},{y0:.1f} {(x0 + x1) / 2:.1f},{(y0 + y1) / 2:.1f} "
    d += f"L {pts[-1][0]:.1f},{pts[-1][1]:.1f}"
    return (f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{w}" stroke-linecap="round" '
            f'stroke-opacity="{opacity}" marker-end="url(#{mid})" data-flow="1"/>\n')


def flow_band(base_pts, color, mid, offsets=(22, 52, 82), reverse=False):
    """Three parallel streamlines above a surface (base_pts), strongest nearest the surface."""
    s = ""
    for k, off in enumerate(offsets):
        pts = [(x, y - off) for x, y in base_pts]
        if reverse:
            pts = pts[::-1]
        s += flow(pts, color, mid, FLOW_W - 2 * k, 1 - 0.22 * k)
    return s


def grid_points(rnd, box, step, jitter, avoid=()):
    """Evenly spread points on a jittered grid inside box, skipping avoid rectangles."""
    x0, y0, x1, y1 = box
    out = []
    for row, y in enumerate(range(int(y0), int(y1), step)):
        for x in range(int(x0) + (step // 2 if row % 2 else 0), int(x1), step):
            xx, yy = x + rnd.uniform(-jitter, jitter), y + rnd.uniform(-jitter, jitter)
            if not any(a <= xx <= c and b <= yy <= d for a, b, c, d in avoid):
                out.append((xx, yy))
    return out


def molecule(x, y, kind="air"):
    if kind == "air":
        return circle(x, y, 8, "#ffffff", "#1d4ed8", 3)
    return circle(x, y, 5.5, "#67e8f9", "#0891b2", 2.5)  # water vapour: smaller, lighter


# ------------------------------------------------------------------ clouds (proportions measured from
# public/explanation-images/meteorology/refined-batch-2/cloud-types-chart-v1.png)

_cloud_n = [0]


def _cloud(shapes, edge_lobes, top, base, dark=False, side_shade=0.3, base_shade=0.12, inner_lobes=()):
    """Fill the union of shapes with one continuous top-to-bottom gradient, then add soft shadows inside it:
    a crescent under each edge lobe (the cauliflower texture), a darker right side and a darker underside."""
    _cloud_n[0] += 1
    n = _cloud_n[0]
    hi, mid, lo = ("#94a3b8", "#64748b", "#334155") if dark else ("#ffffff", "#f1f5f9", "#b4bfcc")
    s = defs(lg(f"cf{n}", [(0, hi), (0.5, mid), (1, lo)], user=(0, top, 0, base)),
             f'<clipPath id="cc{n}">{"".join(shapes)}</clipPath>',
             f'<clipPath id="cb{n}"><rect x="-2000" y="{top - 200:.1f}" width="6000" height="{base - top + 200:.1f}"/></clipPath>')
    s += f'<g clip-path="url(#cb{n})"><g fill="url(#cf{n})">{"".join(shapes)}</g><g clip-path="url(#cc{n})">'
    for (x, y, r), op in [(lobe, 0.16) for lobe in edge_lobes] + [(lobe, 0.09) for lobe in inner_lobes]:
        # crescent shadow on the lower-right rim of each lobe
        s += (f'<path d="M {x - r * 0.85:.1f},{y + r * 0.45:.1f} A {r:.1f},{r:.1f} 0 0 0 {x + r * 0.9:.1f},{y - r * 0.2:.1f} '
              f'A {r * 1.15:.1f},{r * 1.15:.1f} 0 0 1 {x - r * 0.85:.1f},{y + r * 0.45:.1f} Z" fill="#64748b" '
              f'fill-opacity="{op}"/>')
    x0 = min(x - r for x, y, r in edge_lobes)
    x1 = max(x + r for x, y, r in edge_lobes)
    if side_shade:
        s += defs(lg(f"cs{n}", [(0, "#ffffff", 0), (0.55, "#ffffff", 0), (1, "#475569", side_shade)], user=(x0, 0, x1, 0)))
        s += f'<rect x="{x0:.1f}" y="{top:.1f}" width="{x1 - x0:.1f}" height="{base - top:.1f}" fill="url(#cs{n})"/>'
    if base_shade:
        y0 = base - (base - top) * base_shade
        s += defs(lg(f"cu{n}", [(0, "#334155", 0), (1, "#334155", 0.75)], user=(0, y0, 0, base)))
        s += f'<rect x="{x0:.1f}" y="{y0:.1f}" width="{x1 - x0:.1f}" height="{base - y0:.1f}" fill="url(#cu{n})"/>'
    return s + "</g></g>\n"


# lobes of a fair-weather cumulus as (x across the width 0..1, radius and top as fractions of the height),
# read off the cumulus in the cloud-types chart: low shoulders, tallest dome just left of centre
CU_LOBES = [(0.16, 0.30, 0.52), (0.33, 0.40, 0.84), (0.52, 0.46, 1.0), (0.70, 0.36, 0.76), (0.85, 0.26, 0.46)]


def cumulus(cx, base, w, seed=1, dark=False):
    """Fair-weather cumulus: flat base, height ~0.42 of the width."""
    rnd = random.Random(seed)
    h = 0.42 * w
    lobes = []
    for fx, fr, ft in CU_LOBES:
        r = fr * h * rnd.uniform(0.92, 1.08)
        lobes.append((cx - w / 2 + fx * w, base - ft * h + r, r))
    shapes = [circle(x, y, r, "inherit") for x, y, r in lobes]
    shapes.append(f'<rect x="{cx - w * 0.42:.1f}" y="{base - 0.4 * h:.1f}" width="{w * 0.84:.1f}" height="{0.4 * h:.1f}" rx="{0.2 * h:.1f}"/>')
    return _cloud(shapes, lobes, base - h, base, dark, side_shade=0.22, base_shade=0.25)


def cumulonimbus(cx, base, top, seed=3):
    """Thunderstorm cloud measured from the chart: height ~2.5x the base width, tower narrowing to ~0.6 of the
    base width at the top, flat anvil ~1.4x the base width and ~8% of the height, flat dark base."""
    rnd = random.Random(seed)
    H = base - top
    base_w = 0.42 * H
    anvil = 0.08 * H
    tower_top = top + anvil * 1.4
    profile = [(0, 1.0), (0.15, 1.12), (0.35, 1.3), (0.6, 1.22), (0.8, 1.0), (1.0, 0.76)]

    def hw(t):
        for (t0, f0), (t1, f1) in zip(profile[:-1], profile[1:]):
            if t <= t1:
                u = (t - t0) / (t1 - t0)
                u = u * u * (3 - 2 * u)
                return base_w / 2 * (f0 + (f1 - f0) * u)
        return base_w / 2 * profile[-1][1]
    lobes = []
    steps = 11
    for i in range(steps + 1):
        t = i / steps
        y = base - 0.06 * H - t * (base - 0.06 * H - tower_top) + rnd.uniform(-0.01, 0.01) * H
        for side in (-1, 1):
            r = base_w * rnd.uniform(0.1, 0.19)
            lobes.append((cx + side * (hw(t) - r * rnd.uniform(0.45, 0.8)), y, r))
    pts = [(cx - hw(i / 20), base - i / 20 * (base - tower_top)) for i in range(21)]
    pts += [(cx + hw(i / 20), base - i / 20 * (base - tower_top)) for i in range(20, -1, -1)]
    shapes = ['<path d="M ' + " L ".join(f"{x:.1f},{y:.1f}" for x, y in pts) + ' Z"/>']
    shapes += [circle(x, y, r, "inherit") for x, y, r in lobes]
    aw = 1.4 * base_w
    shapes.append(f'<path d="M {cx - aw / 2:.1f},{top + anvil * 0.6:.1f} C {cx - aw * 0.3:.1f},{top:.1f} '
                  f'{cx + aw * 0.3:.1f},{top:.1f} {cx + aw / 2:.1f},{top + anvil * 0.55:.1f} '
                  f'C {cx + aw * 0.32:.1f},{top + anvil * 1.1:.1f} {cx + hw(1) * 1.05:.1f},{top + anvil * 1.2:.1f} '
                  f'{cx + hw(1) * 0.9:.1f},{top + anvil * 2.4:.1f} L {cx - hw(1) * 0.9:.1f},{top + anvil * 2.4:.1f} '
                  f'C {cx - hw(1) * 1.05:.1f},{top + anvil * 1.2:.1f} {cx - aw * 0.32:.1f},{top + anvil * 1.1:.1f} '
                  f'{cx - aw / 2:.1f},{top + anvil * 0.6:.1f} Z"/>')
    shapes.append(f'<rect x="{cx - hw(0):.1f}" y="{base - 0.05 * H:.1f}" width="{2 * hw(0):.1f}" height="{0.05 * H:.1f}"/>')
    inner = []
    for i in range(14):  # faint cauliflower texture across the face of the tower
        t = rnd.uniform(0.05, 0.95)
        y = base - 0.06 * H - t * (base - 0.06 * H - tower_top)
        inner.append((cx + rnd.uniform(-0.6, 0.6) * hw(t), y, base_w * rnd.uniform(0.1, 0.16)))
    return _cloud(shapes, lobes, top, base, side_shade=0.4, base_shade=0.1, inner_lobes=inner)


def rain(x0, x1, top, bottom, slant=-18, rnd=None, heavy=True):
    """Rain shaft with soft edges and streaks."""
    rnd = rnd or random.Random(5)
    s = path(f"M {x0},{top} L {x1},{top} L {x1 + slant},{bottom} L {x0 + slant},{bottom} Z", "#64748b",
             extra=' fill-opacity="0.45" filter="url(#soft)"')
    gap = 13 if heavy else 22
    for k in range(int((x1 - x0) / gap)):
        x = x0 + 8 + k * gap + rnd.uniform(-3, 3)
        y = top + rnd.uniform(4, 40)
        s += (f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x + slant * 0.5:.1f}" y2="{y + (bottom - top) * 0.5:.1f}" '
              f'stroke="#475569" stroke-width="2.5" stroke-opacity="0.45" stroke-linecap="round"/>')
    return s


def lightning(pts):
    d = "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return (path(d, "none", "#fff7a8", 12, ' filter="url(#glow)" stroke-opacity="0.8"')
            + path(d, "none", "#facc15", 5))


def fog_bank(x, y, rx, ry, opacity=0.6):
    return f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="#ffffff" opacity="{opacity}" filter="url(#soft)"/>'


# ------------------------------------------------------------------ instruments and objects

def capsule(cx, cy, w, h, folds=5):
    """Corrugated aneroid capsule seen side-on (as in the barometer and altimeter)."""
    step = w / folds
    d = f"M {cx - w / 2:.1f},{cy - h / 2:.1f} "
    for i in range(folds):
        x0 = cx - w / 2 + i * step
        d += f"Q {x0 + step / 2:.1f},{cy - h / 2 - h * 0.28:.1f} {x0 + step:.1f},{cy - h / 2:.1f} "
    d += f"L {cx + w / 2:.1f},{cy + h / 2:.1f} "
    for i in range(folds):
        x0 = cx + w / 2 - i * step
        d += f"Q {x0 - step / 2:.1f},{cy + h / 2 + h * 0.28:.1f} {x0 - step:.1f},{cy + h / 2:.1f} "
    s = path(d + "Z", "url(#metal)", "#4b5563", 3)
    for i in range(1, folds):
        x = cx - w / 2 + i * step
        s += f'<line x1="{x:.1f}" y1="{cy - h / 2 + 5:.1f}" x2="{x:.1f}" y2="{cy + h / 2 - 5:.1f}" stroke="#6b7280" stroke-width="2"/>'
    return s


def dial(cx, cy, r, value, lo=960, hi=1040, numbers=(960, 1000, 1040), unit="hPa", sweep=240):
    """Round instrument dial with a needle at `value`; only the given numbers are printed (phone-size text)."""
    ang = lambda v: math.radians(-sweep / 2 + (v - lo) * sweep / (hi - lo))  # noqa: E731
    s = circle(cx, cy, r, "url(#bezel)", "#374151", 3) + circle(cx, cy, r - 16, "url(#face)", "#6b7280", 2)
    step = (hi - lo) / 40
    for k in range(41):
        v = lo + k * step
        a, major = ang(v), k % 5 == 0
        r1, r2 = r - 24, r - (46 if major else 36)
        s += (f'<line x1="{cx + r1 * math.sin(a):.1f}" y1="{cy - r1 * math.cos(a):.1f}" x2="{cx + r2 * math.sin(a):.1f}" '
              f'y2="{cy - r2 * math.cos(a):.1f}" stroke="#111827" stroke-width="{4 if major else 2}"/>')
    for v in numbers:
        a = ang(v)
        s += (f'<text x="{cx + (r - 78) * math.sin(a):.1f}" y="{cy - (r - 78) * math.cos(a) + 11:.1f}" text-anchor="middle" '
              f'font-family="{FONT}" font-size="{MIN_TXT}" font-weight="700" fill="#111827">{v}</text>')
    if unit:
        s += (f'<text x="{cx}" y="{cy + r * 0.8:.1f}" text-anchor="middle" font-family="{FONT}" font-size="{MIN_TXT}" '
              f'font-weight="700" fill="#64748b">{unit}</text>')
    a = ang(value)
    dx, dy = math.sin(a), -math.cos(a)
    L = r - 34
    s += (f'<path d="M {cx - dx * 26 + dy * 8:.1f},{cy - dy * 26 - dx * 8:.1f} L {cx + dx * L:.1f},{cy + dy * L:.1f} '
          f'L {cx - dx * 26 - dy * 8:.1f},{cy - dy * 26 + dx * 8:.1f} Z" fill="#0f172a"/>')
    s += (f'<path d="M {cx + dx * (L - 34) + dy * 4:.1f},{cy + dy * (L - 34) - dx * 4:.1f} L {cx + dx * L:.1f},{cy + dy * L:.1f} '
          f'L {cx + dx * (L - 34) - dy * 4:.1f},{cy + dy * (L - 34) + dx * 4:.1f} Z" fill="{RED}"/>')
    return s + circle(cx, cy, 14, "url(#hub)", "#111827", 2)


def droplet(x, y, r):
    """Liquid water droplet: blue with a highlight."""
    return circle(x, y, r, "url(#drop)", "#1d6fd6", 2)


def magnifier(cx, cy, r, inner):
    """Magnifying glass; `inner` is drawn clipped to the lens."""
    _cloud_n[0] += 1
    n = _cloud_n[0]
    s = f'<line x1="{cx + r * 0.7:.1f}" y1="{cy + r * 0.7:.1f}" x2="{cx + r * 1.12:.1f}" y2="{cy + r * 1.12:.1f}" stroke="#334155" stroke-width="22" stroke-linecap="round"/>'
    s += defs(f'<clipPath id="mg{n}"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath>')
    s += circle(cx, cy, r, "url(#lens)") + f'<g clip-path="url(#mg{n})">{inner}</g>'
    return s + circle(cx, cy, r, "none", "#334155", 12)


def rime_teeth(x, y0, y1, side=-1, size=11):
    """White rime ice growing out of a surface into the wind (side=-1: to the left)."""
    s, y = "", y0
    while y < y1:
        s += (f'<path d="M {x:.1f},{y:.1f} l {side * size:.1f},{size * 0.45:.1f} l {-side * size:.1f},{size * 0.45:.1f} z" '
              f'fill="#ffffff" stroke="#60a5fa" stroke-width="1.5"/>')
        y += size * 0.9
    return s


def fence(x0, x1, ground, height=110, posts=5, rime=False):
    s = ""
    for k in range(posts):
        x = x0 + k * (x1 - x0) / (posts - 1)
        s += f'<rect x="{x - 8:.1f}" y="{ground - height:.1f}" width="16" height="{height}" rx="3" fill="#5b4a38"/>'
        if rime:
            s += rime_teeth(x - 8, ground - height + 6, ground - 10)
    for f in (0.25, 0.65):
        y = ground - height * (1 - f)
        s += f'<line x1="{x0:.1f}" y1="{y:.1f}" x2="{x1:.1f}" y2="{y:.1f}" stroke="#5b4a38" stroke-width="6"/>'
    return s


# ------------------------------------------------------------------ navigation: the ground from above

FIELD_COLOURS = ("#a9bf86", "#93ad72", "#b8c48f", "#c9c79a", "#8fa66e", "#a3b07a")


def ground_above(w, h, seed=1, river=True, road=True):
    """Quiet aerial view: a patchwork of fields, a river and a road. Use with sky='aerial'."""
    rnd = random.Random(seed)
    s = ""
    cell = 150
    for gx in range(-1, w // cell + 2):
        for gy in range(-1, h // cell + 2):
            x, y = gx * cell + rnd.uniform(-20, 20), gy * cell + rnd.uniform(-20, 20)
            fw, fh = rnd.uniform(110, 170), rnd.uniform(90, 160)
            s += (f'<rect x="{x:.0f}" y="{y:.0f}" width="{fw:.0f}" height="{fh:.0f}" rx="6" '
                  f'fill="{rnd.choice(FIELD_COLOURS)}" transform="rotate({rnd.uniform(-8, 8):.1f} {x + fw / 2:.0f} {y + fh / 2:.0f})" '
                  f'fill-opacity="0.75" stroke="#7f9762" stroke-width="2" stroke-opacity="0.5"/>')
    if river:
        y0 = h * rnd.uniform(0.25, 0.75)
        pts = [(x, y0 + 60 * math.sin(x / 140 + seed)) for x in range(-20, w + 40, 30)]
        d = "M " + " L ".join(f"{x:.0f},{y:.0f}" for x, y in pts)
        s += path(d, "none", "#5f86a8", 22, ' stroke-opacity="0.55"') + path(d, "none", "#8fb6d6", 12, ' stroke-opacity="0.8"')
    if road:
        x0 = w * rnd.uniform(0.2, 0.8)
        d = f"M {x0:.0f},-10 C {x0 + 80:.0f},{h * 0.35:.0f} {x0 - 120:.0f},{h * 0.65:.0f} {x0 + 40:.0f},{h + 10}"
        s += path(d, "none", "#d6d0bf", 12, ' stroke-opacity="0.85"') + path(d, "none", "#9a937f", 2, ' stroke-dasharray="14 12"')
    return s


def runway_above(x, y, length=200, heading=0):
    """Airfield seen from above, centred on (x, y), runway pointing along `heading` (0 = up, clockwise).
    Measured from radio-telephony/refined-batch-1/rt-trial-runway-contaminated.webp: slate surface, length
    about 6.9 x width, white centreline dashes about 4.8% of the length with 4% gaps. Threshold bars added."""
    wd = length / 6.9
    L2, W2 = length / 2, wd / 2
    s = f'<g transform="translate({x:.1f},{y:.1f}) rotate({heading})">'
    # taxiway and apron on the right-hand side
    s += f'<rect x="{W2 - 2:.1f}" y="{-wd * 0.25:.1f}" width="{wd * 0.9:.1f}" height="{wd * 0.5:.1f}" fill="#7b8696"/>'
    s += f'<rect x="{W2 + wd * 0.75:.1f}" y="{-wd * 0.9:.1f}" width="{wd * 0.8:.1f}" height="{wd * 1.8:.1f}" rx="3" fill="#8a94a3"/>'
    s += f'<rect x="{-W2:.1f}" y="{-L2:.1f}" width="{wd:.1f}" height="{length:.1f}" rx="2" fill="#465569" stroke="#2f3a49" stroke-width="2"/>'
    dash, gap = length * 0.048, length * 0.04
    yy = -L2 + wd * 0.9
    while yy + dash < L2 - wd * 0.9:
        s += f'<rect x="{-wd * 0.04:.1f}" y="{yy:.1f}" width="{wd * 0.08:.1f}" height="{dash:.1f}" fill="#ffffff"/>'
        yy += dash + gap
    for end in (-1, 1):
        for k in range(4):
            bx = -W2 + wd * (0.12 + k * 0.22)
            by = end * (L2 - wd * 0.15) - (wd * 0.45 if end > 0 else 0)
            s += f'<rect x="{bx:.1f}" y="{by:.1f}" width="{wd * 0.1:.1f}" height="{wd * 0.45:.1f}" fill="#ffffff"/>'
    return s + "</g>"


def beacon_side(x, ground, h=120, color="#334155"):
    """Radio beacon mast seen from the side, standing on `ground` at x, `h` high. Measured from the airfield
    beacon in radio-telephony/refined-batch-1/rt-qnh-qfe-explanation-v1.webp (71 px tall: dish 61 px wide on top,
    29 px at its base and 30% of the height deep; legs splay to 20 px)."""
    k = h / 71
    top, bowl = ground - h, ground - h + 21 * k
    s = path(f"M {x - 30.5 * k:.1f},{top:.1f} L {x + 30.5 * k:.1f},{top:.1f} L {x + 14.5 * k:.1f},{bowl:.1f} "
             f"L {x - 14.5 * k:.1f},{bowl:.1f} Z", "#e2e8f0", color, 4)
    s += path(f"M {x - 10 * k:.1f},{ground} L {x:.1f},{bowl:.1f} L {x + 10 * k:.1f},{ground}", "none", color, 5)
    return s


def vor_rose(x, y, r=110, numbers=True):
    """VOR station on a chart: compass ring with ticks every 30 degrees and the station in the middle.
    From the SA 1:1 000 000 chart symbol in public/question-images/navigation/v1/chart-symbol-vor-reporting-point.svg."""
    s = f'<circle cx="{x}" cy="{y}" r="{r}" fill="#ffffff" fill-opacity="0.55" stroke="#111827" stroke-width="3"/>'
    for k in range(12):
        x0, y0 = compass_xy(x, y, r, k * 30)
        x1, y1 = compass_xy(x, y, r * 0.84, k * 30)
        s += f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" stroke="#111827" stroke-width="3"/>'
    hexagon = " ".join(f"{compass_xy(x, y, r * 0.16, 30 + 60 * k)[0]:.1f},{compass_xy(x, y, r * 0.16, 30 + 60 * k)[1]:.1f}"
                       for k in range(6))
    s += f'<polygon points="{hexagon}" fill="#ffffff" stroke="#111827" stroke-width="3"/>'
    s += f'<circle cx="{x}" cy="{y}" r="{r * 0.04:.1f}" fill="#111827"/>'
    if numbers:
        for deg, txt in ((0, "0"), (90, "9"), (180, "18"), (270, "27")):
            tx, ty = compass_xy(x, y, r * 0.62, deg)
            s += label(tx, ty + MIN_TXT * 0.36, txt, MIN_TXT, INK, "middle", halo="#ffffff")
    return s


def ndb_symbol(x, y, r=40):
    """NDB on a chart: a centre dot inside rings of dots."""
    s = f'<circle cx="{x}" cy="{y}" r="{r * 0.18:.1f}" fill="#7c2d12"/>'
    for ring, n in ((0.5, 10), (0.8, 16), (1.0, 20)):
        for k in range(n):
            dx, dy = compass_xy(x, y, r * ring, k * 360 / n)
            s += f'<circle cx="{dx:.1f}" cy="{dy:.1f}" r="{r * 0.05:.1f}" fill="#7c2d12"/>'
    return s


def heading_dial(cx, cy, r, heading, aircraft_mark=True):
    """Compass card in a square bezel, reading `heading` at the top index. Measured from the heading indicator in
    human-performance/refined-batch-8/hp-analogue-heading-v1.webp: ticks to 0.94R, long every 10 deg (0.11R),
    short every 5 deg (0.06R), numbers every 30 deg at 0.71R turning with the card, orange index marks every 45
    deg and an orange aircraft outline."""
    s = f'<rect x="{cx - r * 1.12:.0f}" y="{cy - r * 1.12:.0f}" width="{r * 2.24:.0f}" height="{r * 2.24:.0f}" rx="{r * 0.28:.0f}" fill="#2f3337" stroke="#1b1e21" stroke-width="3"/>'
    s += f'<circle cx="{cx}" cy="{cy}" r="{r:.0f}" fill="#202326" stroke="#4b5056" stroke-width="5"/>'
    s += f'<g transform="rotate({-heading} {cx} {cy})">'
    for k in range(72):
        long = k % 2 == 0
        x0, y0 = compass_xy(cx, cy, r * 0.94, k * 5)
        x1, y1 = compass_xy(cx, cy, r * (0.83 if long else 0.88), k * 5)
        s += f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" stroke="#f4f4f4" stroke-width="{4 if long else 3}"/>'
    names = {0: "N", 90: "E", 180: "S", 270: "W"}
    for k in range(12):
        deg = k * 30
        tx, ty = compass_xy(cx, cy, r * 0.66, deg)
        txt = names.get(deg, str(deg // 10))
        s += (f'<g transform="rotate({deg} {tx:.1f} {ty:.1f})">'
              + label(tx, ty + MIN_TXT * 0.36, txt, MIN_TXT, "#f4f4f4", "middle", halo=None) + '</g>')
    s += "</g>"
    for k in range(8):
        x0, y0 = compass_xy(cx, cy, r * 1.0, k * 45)
        s += f'<g transform="rotate({k * 45} {x0:.1f} {y0:.1f})"><path d="M {x0:.1f},{y0 + 2:.1f} l -9,-16 l 18,0 z" fill="#f28a1e"/></g>'
    if aircraft_mark:
        k = r / 470
        s += (f'<path transform="translate({cx},{cy}) scale({k:.3f})" d="M 0,-260 C 12,-260 14,-240 14,-200 L 14,-60 '
              f'L 140,10 L 140,40 L 14,10 L 14,150 L 50,190 L 50,210 L 0,195 L -50,210 L -50,190 L -14,150 L -14,10 '
              f'L -140,40 L -140,10 L -14,-60 L -14,-200 C -14,-240 -12,-260 0,-260 Z" fill="none" stroke="#f28a1e" stroke-width="{3 / k:.1f}"/>')
    return s


def compass_xy(cx, cy, r, deg):
    """Point at compass bearing `deg` (0 = up, clockwise) and distance r from (cx, cy)."""
    a = math.radians(deg)
    return cx + r * math.sin(a), cy - r * math.cos(a)


def north_line(cx, cy, length, deg, color, mid, w=9, dash=""):
    """Straight arrow from (cx, cy) towards compass bearing `deg`, with a halo so it reads on any ground."""
    x, y = compass_xy(cx, cy, length, deg)
    d = f"M {cx:.1f},{cy:.1f} L {x:.1f},{y:.1f}"
    extra = f' stroke-dasharray="{dash}"' if dash else ""
    return path(d, "none", "#ffffff", w + 6, ' stroke-opacity="0.85"' + extra) + path(d, "none", color, w, f' marker-end="url(#{mid})"' + extra)


def angle_arc(cx, cy, r, a0, a1, color, w=7, clockwise=False):
    """Arc between compass bearings a0 and a1 (degrees, 0 = up, clockwise). By default the shorter way round;
    clockwise=True always sweeps clockwise from a0 to a1, the long way if needed (e.g. a bearing past 180)."""
    x0, y0 = compass_xy(cx, cy, r, a0)
    x1, y1 = compass_xy(cx, cy, r, a1)
    if clockwise:
        large, sweep = (1 if (a1 - a0) % 360 > 180 else 0), 1
    else:
        large, sweep = 0, (1 if (a1 - a0) % 360 < 180 else 0)
    return path(f"M {x0:.1f},{y0:.1f} A {r},{r} 0 {large} {sweep} {x1:.1f},{y1:.1f}", "none", color, w)


def svg_doc(body, w, h):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
            f'<rect width="{w}" height="{h}" fill="#ffffff"/>{defs(*COMMON_DEFS)}{body}</svg>')
