import math
from pathlib import Path
import os
REPO = Path(__file__).resolve().parents[2]
WORK = Path(os.environ.get("ATG_WORK", "/tmp/atg-work"))

OUT = REPO / "public/explanation-images/aircraft-technical-and-general/airframes-batch-1"

W, H = 1200, 680
F = "Arial,Helvetica,sans-serif"
NAVY = "#06111f"
GOLD = "#f4b400"
GOLD_DARK = "#b7860b"
INK = "#101827"
BODY = "#334155"
MUTED = "#64748b"
BLUE = "#1e88e5"
RED = "#dc2626"
STRUCT = "#c8cdd4"
MOVE = "#8fb8de"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def header(title):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{esc(title)}">
<defs>
  <marker id="aDark" markerUnits="userSpaceOnUse" markerWidth="16" markerHeight="16" refX="13" refY="8" orient="auto"><path d="M0,1 L15,8 L0,15 z" fill="{INK}"/></marker>
  <marker id="aBlue" markerUnits="userSpaceOnUse" markerWidth="18" markerHeight="18" refX="15" refY="9" orient="auto"><path d="M0,1 L17,9 L0,17 z" fill="{BLUE}"/></marker>
  <marker id="aRed" markerUnits="userSpaceOnUse" markerWidth="20" markerHeight="20" refX="17" refY="10" orient="auto"><path d="M0,1 L19,10 L0,19 z" fill="{RED}"/></marker>
  <marker id="aRedS" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto"><path d="M0,0.5 L11,6 L0,11.5 z" fill="{RED}"/></marker>
</defs>
<rect width="{W}" height="{H}" fill="#ffffff"/>
<rect width="{W}" height="112" fill="{NAVY}"/>
<text x="600" y="34" text-anchor="middle" font-family="{F}" font-size="17" font-weight="700" letter-spacing="3.2" fill="{GOLD}">PILOTVAULT AIRCRAFT TECHNICAL &amp; GENERAL</text>
<text x="600" y="79" text-anchor="middle" font-family="{F}" font-size="34" font-weight="800" fill="#ffffff">{esc(title)}</text>
<rect x="0" y="108" width="{W}" height="4" fill="{GOLD}"/>
<rect x="28" y="130" width="1144" height="470" rx="10" fill="#ffffff" stroke="#d7e0ea" stroke-width="2"/>
'''


def footer(text):
    return f'<text x="600" y="642" text-anchor="middle" font-family="{F}" font-size="19" font-weight="700" fill="{INK}">{esc(text)}</text>\n</svg>\n'


def t(x, y, s, size=18, weight=700, fill=INK, anchor="middle", extra=""):
    return f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" font-family="{F}" font-size="{size}" font-weight="{weight}" fill="{fill}"{extra}>{esc(s)}</text>\n'


def line(x1, y1, x2, y2, stroke=INK, w=3, marker=None, dash=None, cap="round"):
    m = f' marker-end="url(#{marker})"' if marker else ""
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{w}" stroke-linecap="{cap}"{m}{d}/>\n'


def poly(points, fill, stroke=INK, w=3, extra=""):
    d = "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in points) + " Z"
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{w}" stroke-linejoin="round"{extra}/>\n'


def polyline(points, stroke, w=3, dash=None, marker=None):
    d = "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in points)
    ds = f' stroke-dasharray="{dash}"' if dash else ""
    m = f' marker-end="url(#{marker})"' if marker else ""
    return f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"{ds}{m}/>\n'


# ---------- aerofoil geometry (x along chord 0..1, y up) ----------

def naca(m, p, th, n=80):
    up, lo = [], []
    for i in range(n + 1):
        beta = math.pi * i / n
        x = (1 - math.cos(beta)) / 2
        yt = 5 * th * (0.2969 * math.sqrt(x) - 0.1260 * x - 0.3516 * x ** 2 + 0.2843 * x ** 3 - 0.1036 * x ** 4)
        if m == 0:
            yc, dyc = 0.0, 0.0
        elif x < p:
            yc = m / p ** 2 * (2 * p * x - x ** 2)
            dyc = 2 * m / p ** 2 * (p - x)
        else:
            yc = m / (1 - p) ** 2 * ((1 - 2 * p) + 2 * p * x - x ** 2)
            dyc = 2 * m / (1 - p) ** 2 * (p - x)
        a = math.atan(dyc)
        up.append((x - yt * math.sin(a), yc + yt * math.cos(a)))
        lo.append((x + yt * math.sin(a), yc - yt * math.cos(a)))
    return up, lo


def interp(pts, x):
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if x0 <= x <= x1 and x1 != x0:
            return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
    return pts[-1][1] if x >= pts[-1][0] else pts[0][1]


def seg(pts, a, b):
    """Surface points with a <= x <= b, including interpolated ends."""
    out = [(a, interp(pts, a))]
    out += [p for p in pts if a < p[0] < b]
    out.append((b, interp(pts, b)))
    return out


def rot(p, h, deg):
    """Rotate p about h. Positive deg = trailing edge DOWN (clockwise, y-up frame)."""
    th = -math.radians(deg)
    dx, dy = p[0] - h[0], p[1] - h[1]
    return (h[0] + dx * math.cos(th) - dy * math.sin(th), h[1] + dx * math.sin(th) + dy * math.cos(th))


def to_px(pts, X0, Y0, C):
    return [(X0 + x * C, Y0 - y * C) for x, y in pts]


# =====================================================================
# q2421 semi-monocoque fuselage
# =====================================================================

def q2421():
    s = header("SEMI-MONOCOQUE FUSELAGE")
    cy = 285

    def ry(x):
        return 95.0 if x <= 550 else 95.0 - (x - 550) / 500 * 65

    # stringers
    for k in [1, 0.6, 0.2, -0.2, -0.6, -1]:
        pts = [(150, cy - ry(150) * k), (550, cy - ry(550) * k), (1030, cy - ry(1030) * k)]
        wdt = 4 if abs(k) == 1 else 3
        col = INK if abs(k) == 1 else "#475569"
        s += polyline(pts, col, wdt)
    # formers / bulkheads
    for x in [260, 370, 480, 590, 700, 810, 920, 1030]:
        s += f'<ellipse cx="{x}" cy="{cy}" rx="16" ry="{ry(x):.1f}" fill="none" stroke="{INK}" stroke-width="4"/>\n'
    # firewall
    s += f'<ellipse cx="150" cy="{cy}" rx="18" ry="95" fill="#94a3b8" stroke="{INK}" stroke-width="4"/>\n'
    # wing attachment fittings
    for x in [480, 590]:
        y = cy + ry(x) * 0.6
        s += f'<rect x="{x - 13}" y="{y - 10:.1f}" width="26" height="20" rx="3" fill="#334155" stroke="{INK}" stroke-width="2"/>\n'
    # stressed skin panel over the rear section
    skin = [(700, cy - ry(700)), (1030, cy - ry(1030)), (1030, cy + ry(1030)), (700, cy + ry(700))]
    s += poly(skin, "#cfe3f5", "#1f4e79", 3, ' fill-opacity="0.88"')
    for x in [700, 810, 920, 1030]:
        for k in [1, 0.6, 0.2, -0.2, -0.6, -1]:
            s += f'<circle cx="{x}" cy="{cy - ry(x) * k:.1f}" r="3.2" fill="#1f4e79"/>\n'

    # labels above
    s += t(315, 166, "BULKHEADS / FORMERS")
    s += line(290, 174, 262, 188, marker="aDark", w=2.5)
    s += line(340, 174, 368, 188, marker="aDark", w=2.5)
    s += t(640, 166, "STRINGERS")
    s += line(640, 174, 640, 197, marker="aDark", w=2.5)
    s += t(905, 166, "STRESSED SKIN")
    s += line(905, 174, 905, 227, marker="aDark", w=2.5)
    # labels below
    s += t(150, 414, "FIREWALL")
    s += line(150, 398, 150, 384, marker="aDark", w=2.5)
    s += t(535, 414, "WING ATTACHMENT POINTS")
    s += line(505, 397, 484, 358, marker="aDark", w=2.5)
    s += line(565, 397, 586, 355, marker="aDark", w=2.5)

    s += construction_boxes("SEMI-MONOCOQUE")
    s += footer("The skin is stressed: it shares the flight and ground loads with the internal frame.")
    return s


def construction_boxes(answer, by=440, h=145):
    s = ""
    boxes = [
        (60, "TRUSS", ["Longerons and bracing", "carry the loads; the", "covering only gives shape."]),
        (430, "MONOCOQUE", ["The skin carries all the", "loads; formers only", "hold the shape."]),
        (800, "SEMI-MONOCOQUE", ["Formers and stringers", "keep the shape; the", "stressed skin shares the load."]),
    ]
    for bx, title, lines_ in boxes:
        ans = title == answer
        if ans:
            s += f'<rect x="{bx}" y="{by}" width="340" height="{h}" rx="12" fill="#fff8e1" stroke="{GOLD}" stroke-width="4"/>\n'
            s += f'<rect x="{bx + 236}" y="{by + 14}" width="90" height="28" rx="14" fill="{GOLD}"/>\n'
            s += t(bx + 281, by + 33, "ANSWER", 14, 800, NAVY)
        else:
            s += f'<rect x="{bx}" y="{by}" width="340" height="{h}" rx="12" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2"/>\n'
        s += t(bx + 20, by + 36, title, 20, 800, INK, "start")
        for i, ln in enumerate(lines_):
            s += t(bx + 20, by + 70 + i * 26, ln, 17, 400, BODY, "start")
    return s


# =====================================================================
# q2424 torsion
# =====================================================================

def q2424():
    s = header("TORSION: A TWISTING LOAD")
    cy, r, x0, x1 = 282, 75, 230, 860
    # wall
    s += f'<rect x="190" y="175" width="40" height="215" fill="#e2e8f0" stroke="{INK}" stroke-width="3"/>\n'
    for yy in range(197, 391, 18):
        s += line(192, yy, 228, yy - 18, "#94a3b8", 2)
    # body
    s += f'<rect x="{x0}" y="{cy - r}" width="{x1 - x0}" height="{2 * r}" fill="#eef1f5" stroke="none"/>\n'
    s += line(x0, cy - r, x1, cy - r, INK, 4)
    s += line(x0, cy + r, x1, cy + r, INK, 4)
    # straight reference line (before loading)
    ref_y = cy - r * math.sin(math.radians(-10))
    s += line(x0, ref_y, x1, ref_y, "#94a3b8", 3, dash="12 9")
    # helical lines after twisting
    for phi0 in [-50, -10, 30]:
        pts = []
        for i in range(0, 64):
            x = x0 + (x1 - x0) * i / 63
            phi = phi0 + 55 * (x - x0) / (x1 - x0)
            if -86 < phi < 86:
                pts.append((x, cy - r * math.sin(math.radians(phi))))
        s += polyline(pts, BLUE, 4)
    # free end
    s += f'<ellipse cx="{x1}" cy="{cy}" rx="26" ry="{r}" fill="#dfe5ec" stroke="{INK}" stroke-width="4"/>\n'
    # applied torque at free end
    def ell(cx, cyy, rx, ryy, deg):
        a = math.radians(deg)
        return cx + rx * math.cos(a), cyy + ryy * math.sin(a)
    sx, sy = ell(x1, cy, 58, 112, -112)
    ex, ey = ell(x1, cy, 58, 112, 42)
    s += f'<path d="M {sx:.1f} {sy:.1f} A 58 112 0 0 1 {ex:.1f} {ey:.1f}" fill="none" stroke="{RED}" stroke-width="6" marker-end="url(#aRed)"/>\n'
    s += t(1030, 262, "TWISTING", 20, 800, RED)
    s += t(1030, 288, "MOMENT", 20, 800, RED)
    s += t(1030, 314, "(TORQUE)", 17, 700, RED)
    # root reaction
    sx, sy = ell(248, cy, 40, 104, 112)
    ex, ey = ell(248, cy, 40, 104, -112)
    s += f'<path d="M {sx:.1f} {sy:.1f} A 40 104 0 1 0 {ex:.1f} {ey:.1f}" fill="none" stroke="{INK}" stroke-width="4" marker-end="url(#aDark)"/>\n'
    s += t(210, 162, "FIXED ROOT")
    s += t(230, 420, "ROOT RESISTS THE TWIST")
    s += t(650, 420, "TWIST PRODUCES SHEAR ACROSS THE STRUCTURE")
    # legend
    s += line(560, 150, 610, 150, "#94a3b8", 3, dash="12 9")
    s += t(622, 156, "Straight line before loading", 16, 400, BODY, "start")
    s += line(560, 178, 610, 178, BLUE, 4)
    s += t(622, 184, "Same line after twisting", 16, 400, BODY, "start")

    # load types strip
    by = 440
    items = [
        ("TENSION", "Pulling apart"),
        ("COMPRESSION", "Squeezing together"),
        ("SHEAR", "Layers sliding"),
        ("BENDING", "Sagging or flexing"),
        ("TORSION", "Twisting"),
    ]
    for i, (title, desc) in enumerate(items):
        bx = 68 + i * 216
        cx, cyy = bx + 100, by + 78
        ans = title == "TORSION"
        if ans:
            s += f'<rect x="{bx}" y="{by}" width="200" height="145" rx="12" fill="#fff8e1" stroke="{GOLD}" stroke-width="4"/>\n'
        else:
            s += f'<rect x="{bx}" y="{by}" width="200" height="145" rx="12" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2"/>\n'
        s += t(cx, by + 32, title, 18, 800, INK)
        if title == "TENSION":
            s += f'<rect x="{cx - 38}" y="{cyy - 10}" width="76" height="20" fill="{STRUCT}" stroke="{INK}" stroke-width="2.5"/>\n'
            s += line(cx - 44, cyy, cx - 86, cyy, RED, 4, "aRedS")
            s += line(cx + 44, cyy, cx + 86, cyy, RED, 4, "aRedS")
        elif title == "COMPRESSION":
            s += f'<rect x="{cx - 38}" y="{cyy - 10}" width="76" height="20" fill="{STRUCT}" stroke="{INK}" stroke-width="2.5"/>\n'
            s += line(cx - 88, cyy, cx - 46, cyy, RED, 4, "aRedS")
            s += line(cx + 88, cyy, cx + 46, cyy, RED, 4, "aRedS")
        elif title == "SHEAR":
            s += f'<rect x="{cx - 50}" y="{cyy - 21}" width="84" height="19" fill="{STRUCT}" stroke="{INK}" stroke-width="2.5"/>\n'
            s += f'<rect x="{cx - 34}" y="{cyy + 2}" width="84" height="19" fill="{STRUCT}" stroke="{INK}" stroke-width="2.5"/>\n'
            s += line(cx + 42, cyy - 12, cx + 86, cyy - 12, RED, 4, "aRedS")
            s += line(cx - 42, cyy + 12, cx - 86, cyy + 12, RED, 4, "aRedS")
        elif title == "BENDING":
            s += f'<path d="M {cx - 62} {cyy - 4} Q {cx} {cyy + 30} {cx + 62} {cyy - 4}" fill="none" stroke="{INK}" stroke-width="18" stroke-linecap="butt"/>\n'
            s += f'<path d="M {cx - 61} {cyy - 4} Q {cx} {cyy + 30} {cx + 61} {cyy - 4}" fill="none" stroke="{STRUCT}" stroke-width="12" stroke-linecap="butt"/>\n'
            s += line(cx, cyy - 38, cx, cyy - 2, RED, 4, "aRedS")
        else:
            s += f'<rect x="{cx - 46}" y="{cyy - 16}" width="92" height="32" fill="{STRUCT}" stroke="none"/>\n'
            s += line(cx - 46, cyy - 16, cx + 46, cyy - 16, INK, 2.5)
            s += line(cx - 46, cyy + 16, cx + 46, cyy + 16, INK, 2.5)
            s += f'<ellipse cx="{cx - 46}" cy="{cyy}" rx="7" ry="16" fill="{STRUCT}" stroke="{INK}" stroke-width="2.5"/>\n'
            s += f'<ellipse cx="{cx + 46}" cy="{cyy}" rx="7" ry="16" fill="{STRUCT}" stroke="{INK}" stroke-width="2.5"/>\n'
            a1 = ell(cx + 50, cyy, 16, 30, -100)
            a2 = ell(cx + 50, cyy, 16, 30, 60)
            s += f'<path d="M {a1[0]:.1f} {a1[1]:.1f} A 16 30 0 0 1 {a2[0]:.1f} {a2[1]:.1f}" fill="none" stroke="{RED}" stroke-width="4" marker-end="url(#aRedS)"/>\n'
            b1 = ell(cx - 50, cyy, 16, 30, -80)
            b2 = ell(cx - 50, cyy, 16, 30, 120)
            s += f'<path d="M {b1[0]:.1f} {b1[1]:.1f} A 16 30 0 0 0 {b2[0]:.1f} {b2[1]:.1f}" fill="none" stroke="{RED}" stroke-width="4" marker-end="url(#aRedS)"/>\n'
        s += t(cx, by + 128, desc, 16, 800 if ans else 400, INK if ans else BODY)

    s += footer("Torsion is a twisting load about a member's long axis, e.g. a wing twisted by aileron loads.")
    return s


# =====================================================================
# q2425 flap types
# =====================================================================

FLAP_FOOTERS = {
    "PLAIN FLAP": "Plain flap: the whole rear section of the wing hinges down as one piece.",
    "SPLIT FLAP": "Split flap: the upper surface stays in place and only the lower skin deflects.",
    "SLOTTED FLAP": "Slotted flap: a gap between wing and flap lets air flow over the flap's upper surface.",
    "FOWLER FLAP": "Fowler flap: moves aft and down, increasing wing area as well as camber.",
}


def flaps(answer):
    s = header(f"{answer} VS OTHER FLAP TYPES")
    up, lo = naca(0.02, 0.4, 0.12)
    C = 300

    def camber(x):
        return (interp(up, x) + interp(lo, x)) / 2

    cells = [
        (48, 142, "PLAIN FLAP", ["Rear section of the wing hinges down.", "Increases camber: more lift and more drag."]),
        (612, 142, "SPLIT FLAP", ["Only the lower surface hinges down; the upper", "surface stays fixed. High drag, modest lift gain."]),
        (48, 374, "SLOTTED FLAP", ["A slot feeds high-energy air over the flap,", "delaying separation for a larger lift gain."]),
        (612, 374, "FOWLER FLAP", ["Slides aft on tracks, then down: more wing", "area and camber for the largest lift gain."]),
    ]
    for cx, cy, title, desc in cells:
        ans = title == answer
        if ans:
            s += f'<rect x="{cx}" y="{cy}" width="540" height="220" rx="12" fill="#fff8e1" stroke="{GOLD}" stroke-width="4"/>\n'
            s += f'<rect x="{cx + 420}" y="{cy + 14}" width="100" height="28" rx="14" fill="{GOLD}"/>\n'
            s += t(cx + 470, cy + 33, "ANSWER", 14, 800, NAVY)
        else:
            s += f'<rect x="{cx}" y="{cy}" width="540" height="220" rx="12" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2"/>\n'
        s += t(cx + 20, cy + 34, title, 21, 800, INK, "start")
        for i, d in enumerate(desc):
            s += t(cx + 270, cy + 184 + i * 22, d, 16, 400, BODY)

        X0, Y0 = cx + 90, cy + 90
        P = lambda pts: to_px(pts, X0, Y0, C)
        fixed = "#b8c0ca"
        moving = GOLD if ans else MOVE

        if title == "PLAIN FLAP":
            hx = 0.72
            h = (hx, camber(hx))
            rr = (interp(up, hx) - interp(lo, hx)) / 2
            flap = seg(up, hx, 1.0) + list(reversed(seg(lo, hx, 1.0)))
            flap = [rot(p, h, 32) for p in flap]
            s += poly(P(flap), moving, INK, 3)
            hp = P([h])[0]
            s += f'<circle cx="{hp[0]:.1f}" cy="{hp[1]:.1f}" r="{rr * C:.1f}" fill="{moving}" stroke="{INK}" stroke-width="3"/>\n'
            main = seg(up, 0, hx) + list(reversed(seg(lo, 0, hx)))
            s += poly(P(main), fixed, INK, 3)
        elif title == "SPLIT FLAP":
            hx = 0.70
            main = seg(up, 0, 1.0) + [(hx, interp(lo, hx))] + list(reversed(seg(lo, 0, hx)))
            s += poly(P(main), fixed, INK, 3)
            hinge = (hx, interp(lo, hx))
            tip = rot((hx + 0.30, interp(lo, hx)), hinge, 48)
            a, b = P([hinge, tip])
            s += line(a[0], a[1], b[0], b[1], INK, 11, cap="round")
            s += line(a[0], a[1], b[0], b[1], moving, 6, cap="round")
            if ans:
                ux = 0.86
                upx = P([(ux, interp(up, ux))])[0]
                s += t(cx + 472, cy + 120, "UPPER SURFACE", 14, 800, GOLD_DARK)
                s += t(cx + 472, cy + 138, "STAYS FIXED", 14, 800, GOLD_DARK)
                s += line(cx + 404, cy + 114, upx[0] + 6, upx[1] + 3, GOLD_DARK, 2, "aDark")
        elif title in ("SLOTTED FLAP", "FOWLER FLAP"):
            shroud = 0.76 if title == "SLOTTED FLAP" else 0.80
            cove_lo = 0.66
            main_up = seg(up, 0, shroud)
            main_lo = list(reversed(seg(lo, 0, cove_lo)))
            pu = P(main_up)
            pl = P(main_lo)
            ctrl = P([(0.70, camber(0.70) - 0.01)])[0]
            d = "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in pu)
            d += f" Q {ctrl[0]:.1f},{ctrl[1]:.1f} {pl[0][0]:.1f},{pl[0][1]:.1f}"
            d += "".join(f" L {x:.1f},{y:.1f}" for x, y in pl[1:]) + " Z"
            fu, fl = naca(0.02, 0.4, 0.14, 40)
            fc = 0.32 if title == "SLOTTED FLAP" else 0.30
            flap = [(x * fc, y * fc) for x, y in fu] + [(x * fc, y * fc) for x, y in reversed(fl)]
            if title == "SLOTTED FLAP":
                le = (0.715, -0.045)
                defl = 30
            else:
                le = (0.87, -0.03)
                defl = 22
                # retracted position ghost
                ghost = [(0.64 + x, 0.0 + y) for x, y in flap]
                s += poly(P(ghost), "none", "#94a3b8", 2.5, ' stroke-dasharray="8 6"')
            flap = [rot((le[0] + x, le[1] + y), le, defl) for x, y in flap]
            s += poly(P(flap), moving, INK, 3)
            s += f'<path d="{d}" fill="{fixed}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>\n'
            if title == "SLOTTED FLAP":
                a = P([(0.60, -0.115)])[0]
                b = P([(0.735, -0.005)])[0]
                c = P([(0.86, 0.035)])[0]
                s += f'<path d="M {a[0]:.1f} {a[1]:.1f} Q {b[0]:.1f} {b[1]:.1f} {c[0]:.1f} {c[1]:.1f}" fill="none" stroke="{BLUE}" stroke-width="3.5" marker-end="url(#aBlue)"/>\n'
                s += t(a[0] - 8, a[1] + 16, "SLOT", 14, 800, BLUE, "end")
            else:
                a = P([(0.62, -0.19)])[0]
                b = P([(0.92, -0.19)])[0]
                s += line(a[0], a[1], b[0], b[1], BLUE, 3.5, "aBlue")
                s += t(a[0] - 8, a[1] + 5, "AFT", 14, 800, BLUE, "end")

    s += footer(FLAP_FOOTERS[answer])
    return s


# =====================================================================
# q2429 / q2454 truss fuselage longerons
# =====================================================================

def q2429():
    s = header("TRUSS FUSELAGE: LONGERONS")

    def y_top(x):
        return 195.0 if x <= 520 else 195.0 + (x - 520) / 510 * 55

    def y_bot(x):
        return 385.0 if x <= 520 else 385.0 - (x - 520) / 510 * 85

    stations = [150, 260, 370, 480, 590, 700, 810, 920, 1030]
    dx, dy = 26, -20
    # far-side longerons for depth
    for f in (y_top, y_bot):
        s += polyline([(x + dx, f(x) + dy) for x in (150, 520, 1030)], "#cbd5e1", 5)
    for x in stations:
        s += line(x, y_top(x), x + dx, y_top(x) + dy, "#cbd5e1", 3)
    # verticals and diagonals (Warren pattern)
    for i, x in enumerate(stations):
        s += line(x, y_top(x), x, y_bot(x), "#475569", 4)
        if i < len(stations) - 1:
            x2 = stations[i + 1]
            if i % 2 == 0:
                s += line(x, y_top(x), x2, y_bot(x2), "#475569", 4)
            else:
                s += line(x, y_bot(x), x2, y_top(x2), "#475569", 4)
    # longerons highlighted
    for f in (y_top, y_bot):
        pts = [(x, f(x)) for x in (150, 520, 1030)]
        s += polyline(pts, INK, 13)
        s += polyline(pts, GOLD, 7)
    for x in stations:
        for f in (y_top, y_bot):
            s += f'<circle cx="{x}" cy="{f(x):.1f}" r="5" fill="#ffffff" stroke="{INK}" stroke-width="2"/>\n'

    s += t(335, 165, "UPPER LONGERON", 18, 800, GOLD_DARK)
    s += line(335, 173, 335, 186, GOLD_DARK, 2.5, "aDark")
    s += t(335, 430, "LOWER LONGERON", 18, 800, GOLD_DARK)
    s += line(335, 407, 335, 395, GOLD_DARK, 2.5, "aDark")
    s += t(700, 172, "VERTICAL MEMBER")
    s += line(700, 180, 700, 207, marker="aDark", w=2.5)
    s += t(755, 430, "DIAGONAL (WEB) MEMBER")
    mx, my = (700 + 810) / 2, (y_bot(700) + y_top(810)) / 2
    s += line(752, 408, mx + 1, my + 1, marker="aDark", w=2.5)
    s += t(1060, 172, "FAR-SIDE", 14, 700, MUTED)
    s += t(1060, 190, "LONGERONS", 14, 700, MUTED)

    boxes = [
        (60, "LONGERONS", ["Main longitudinal members", "along the fuselage length;", "they carry the main loads."], True),
        (430, "VERTICALS & DIAGONALS", ["Tie the longerons into", "rigid triangles that", "resist bending and shear."], False),
        (800, "COVERING", ["Fabric or light panels give", "the streamlined shape but", "carry little structural load."], False),
    ]
    by = 452
    for bx, title, lines_, ans in boxes:
        if ans:
            s += f'<rect x="{bx}" y="{by}" width="340" height="136" rx="12" fill="#fff8e1" stroke="{GOLD}" stroke-width="4"/>\n'
            s += f'<rect x="{bx + 236}" y="{by + 14}" width="90" height="28" rx="14" fill="{GOLD}"/>\n'
            s += t(bx + 281, by + 33, "ANSWER", 14, 800, NAVY)
        else:
            s += f'<rect x="{bx}" y="{by}" width="340" height="136" rx="12" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2"/>\n'
        s += t(bx + 20, by + 34, title, 19, 800, INK, "start")
        for i, ln in enumerate(lines_):
            s += t(bx + 20, by + 66 + i * 25, ln, 17, 400, BODY, "start")

    s += footer("In a truss (girder) fuselage the longerons are the main longitudinal load-carrying members.")
    return s


# =====================================================================
# q2457 monocoque
# =====================================================================

def q2457():
    s = header("MONOCOQUE STRUCTURE")
    cy = 285

    def ry(x):
        return 95.0 if x <= 550 else 95.0 - (x - 550) / 500 * 65

    formers = [370, 700, 1030]
    for x in formers:
        s += f'<ellipse cx="{x}" cy="{cy}" rx="16" ry="{ry(x):.1f}" fill="none" stroke="#1f4e79" stroke-width="3" stroke-dasharray="7 5"/>\n'
    shell = [(150, cy - 95), (550, cy - 95), (1030, cy - ry(1030)), (1030, cy + ry(1030)), (550, cy + 95), (150, cy + 95)]
    s += poly(shell, "#cfe3f5", "#1f4e79", 7, ' fill-opacity="0.78"')
    s += f'<ellipse cx="150" cy="{cy}" rx="18" ry="95" fill="#94a3b8" stroke="{INK}" stroke-width="4"/>\n'
    s += f'<ellipse cx="1030" cy="{cy}" rx="16" ry="{ry(1030):.1f}" fill="#dbe7f3" stroke="#1f4e79" stroke-width="4"/>\n'
    # load paths in the skin
    for k in (1, -1):
        pts = [(230, cy - 95 * k), (550, cy - 95 * k), (930, cy - ry(930) * k)]
        s += polyline([(x, y + 16 * k) for x, y in pts], RED, 5, marker="aRed")

    s += t(600, 166, "SKIN CARRIES ALL THE FLIGHT LOADS", 18, 800, RED)
    s += line(600, 174, 600, 186, RED, 2.5, "aRedS")
    s += t(370, 422, "FORMERS ONLY HOLD THE SHAPE")
    s += line(370, 403, 370, 384, marker="aDark", w=2.5)
    s += t(830, 422, "NO STRINGERS OR LONGERONS")

    s += construction_boxes("MONOCOQUE")
    s += footer("Monocoque: the outer skin carries all the flight loads.")
    return s


# =====================================================================
# balance tab / trim tab shared geometry
# =====================================================================

SYM_UP, SYM_LO = naca(0, 0, 0.16)


def half_t(x):
    return interp(SYM_UP, x)


def tail_parts(hinge, tab_hinge, elev_deg, tab_rel_deg):
    """Return (stab, elevator, tab, elev_hinge_circle, tab_hinge_circle) in chord units."""
    stab = seg(SYM_UP, 0, hinge) + list(reversed(seg(SYM_LO, 0, hinge)))
    elev = seg(SYM_UP, hinge, tab_hinge) + list(reversed(seg(SYM_LO, hinge, tab_hinge)))
    tab = seg(SYM_UP, tab_hinge, 1.0) + list(reversed(seg(SYM_LO, tab_hinge, 1.0)))
    H = (hinge, 0.0)
    TH = (tab_hinge, 0.0)
    tab = [rot(p, TH, tab_rel_deg) for p in tab]
    tab = [rot(p, H, elev_deg) for p in tab]
    elev = [rot(p, H, elev_deg) for p in elev]
    th_pt = rot(TH, H, elev_deg)
    return stab, elev, tab, (H, half_t(hinge)), (th_pt, half_t(tab_hinge))


# =====================================================================
# q2426 balance tab
# =====================================================================

def q2426():
    s = header("BALANCE TAB OPERATION")
    C, X0, Y0 = 560, 92, 300
    P = lambda pts: to_px(pts, X0, Y0, C)
    hinge, tab_hinge = 0.58, 0.82
    elev_deg, tab_rel = 22, -40

    # neutral ghost
    _, g_elev, g_tab, _, _ = tail_parts(hinge, tab_hinge, 0, 0)
    s += poly(P(g_elev), "none", "#94a3b8", 2.5, ' stroke-dasharray="9 7"')
    s += poly(P(g_tab), "none", "#94a3b8", 2.5, ' stroke-dasharray="9 7"')

    stab, elev, tab, (H, hr), (TH, thr) = tail_parts(hinge, tab_hinge, elev_deg, tab_rel)
    s += poly(P(tab), GOLD, INK, 3)
    thp = P([TH])[0]
    s += f'<circle cx="{thp[0]:.1f}" cy="{thp[1]:.1f}" r="{thr * C:.1f}" fill="{GOLD}" stroke="{INK}" stroke-width="2.5"/>\n'
    s += poly(P(elev), MOVE, INK, 3)
    hp = P([H])[0]
    s += f'<circle cx="{hp[0]:.1f}" cy="{hp[1]:.1f}" r="{hr * C:.1f}" fill="{MOVE}" stroke="{INK}" stroke-width="3"/>\n'
    s += poly(P(stab), "#b8c0ca", INK, 3)
    s += f'<circle cx="{hp[0]:.1f}" cy="{hp[1]:.1f}" r="5" fill="{INK}"/>\n'
    s += f'<circle cx="{thp[0]:.1f}" cy="{thp[1]:.1f}" r="4" fill="{INK}"/>\n'

    # linkage: bracket on fixed stabiliser -> horn on tab
    bx = 0.50
    base = (bx, half_t(bx))
    top = (bx, half_t(bx) + 0.075)
    horn_rel = (tab_hinge + 0.004, 0.11)
    horn = rot(rot(horn_rel, (tab_hinge, 0.0), tab_rel), (hinge, 0.0), elev_deg)
    horn_base = rot(rot((tab_hinge + 0.004, half_t(tab_hinge) * 0.6), (tab_hinge, 0.0), tab_rel), (hinge, 0.0), elev_deg)
    b0, b1, h0, h1 = P([base, top, horn_base, horn])
    s += line(b0[0], b0[1], b1[0], b1[1], INK, 5)
    s += line(h0[0], h0[1], h1[0], h1[1], INK, 5)
    s += line(b1[0], b1[1], h1[0], h1[1], "#334155", 5)
    for p in (b1, h1):
        s += f'<circle cx="{p[0]:.1f}" cy="{p[1]:.1f}" r="6" fill="#ffffff" stroke="{INK}" stroke-width="2.5"/>\n'

    # airflow
    for yy in (262, 300, 338):
        s += line(38, yy, 80, yy, BLUE, 4, "aBlue")
    s += t(70, 244, "AIRFLOW", 14, 800, BLUE)

    # tab air load
    tc = rot(rot((tab_hinge + 0.07, 0.0), (tab_hinge, 0.0), tab_rel), (hinge, 0.0), elev_deg)
    tcp = P([tc])[0]
    s += line(tcp[0], tcp[1] + 14, tcp[0], tcp[1] + 72, RED, 6, "aRed")

    # labels
    s += t(250, 222, "STABILISER (FIXED)")
    mid = ((b1[0] + h1[0]) / 2, (b1[1] + h1[1]) / 2)
    s += t(mid[0] + 10, 200, "LINK TO FIXED STRUCTURE", 16, 800, "#334155")
    s += line(mid[0] + 4, 208, mid[0], mid[1] - 8, "#334155", 2, "aDark")
    s += t(690, 168, "Dashed outline = neutral position", 15, 400, MUTED, "end")

    def badge(x, y, n):
        return (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="15" fill="{NAVY}"/>\n'
                + t(x, y + 6, str(n), 17, 800, "#ffffff"))

    ep = P([rot((0.72, -half_t(0.72)), (hinge, 0.0), elev_deg)])[0]
    s += line(ep[0] - 40, ep[1] + 38, ep[0] - 4, ep[1] + 6, INK, 2, "aDark")
    s += badge(ep[0] - 52, ep[1] + 50, 1)
    tp = P([rot(rot((tab_hinge + 0.10, half_t(tab_hinge + 0.10)), (tab_hinge, 0.0), tab_rel), (hinge, 0.0), elev_deg)])[0]
    s += badge(tp[0] + 34, tp[1] - 34, 2)
    s += line(tp[0] + 22, tp[1] - 24, tp[0] + 5, tp[1] - 6, INK, 2, "aDark")
    s += badge(tcp[0] + 34, tcp[1] + 52, 3)

    legend = [
        "CONTROL SURFACE DEFLECTS DOWN",
        "BALANCE TAB DEFLECTS UP (OPPOSITE WAY)",
        "AIR LOAD ON THE TAB HELPS PUSH THE SURFACE DOWN",
    ]
    for i, txt in enumerate(legend):
        y = 492 + i * 36
        s += badge(66, y - 6, i + 1)
        s += t(92, y, txt, 17, 700, INK, "start")

    # fact column
    facts = [
        ("MOVES OPPOSITE", ["Surface down: tab up.", "Surface up: tab down."]),
        ("AERODYNAMIC ASSIST", ["The tab's air load creates a", "hinge moment that helps move", "the control surface."]),
        ("LIGHTER CONTROLS", ["Less stick force is needed", "from the pilot."]),
    ]
    for i, (title, lines_) in enumerate(facts):
        fy = 146 + i * 150
        s += f'<rect x="770" y="{fy}" width="378" height="138" rx="12" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2"/>\n'
        s += f'<rect x="770" y="{fy}" width="8" height="138" rx="4" fill="{GOLD}"/>\n'
        s += t(796, fy + 34, title, 19, 800, INK, "start")
        for j, ln in enumerate(lines_):
            s += t(796, fy + 66 + j * 25, ln, 17, 400, BODY, "start")

    s += footer("A balance tab moves opposite to its control surface, reducing the pilot's control force.")
    return s


# =====================================================================
# q2427 adjustable trim tab
# =====================================================================

def q2427():
    s = header("ADJUSTABLE TRIM TAB")
    hinge, tab_hinge = 0.60, 0.80
    tab_rel = 20
    panels = [(48, "ELEVATOR UP", -18), (420, "ELEVATOR NEUTRAL", 0), (792, "ELEVATOR DOWN", 18)]
    C = 330
    for px, title, ed in panels:
        py = 142
        s += f'<rect x="{px}" y="{py}" width="360" height="252" rx="12" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2"/>\n'
        s += t(px + 180, py + 34, title, 19, 800, INK)
        X0, Y0 = px + 14, py + 134
        P = lambda pts, X0=X0, Y0=Y0: to_px(pts, X0, Y0, C)
        stab, elev, tab, (H, hr), (TH, thr) = tail_parts(hinge, tab_hinge, ed, tab_rel)
        s += poly(P(tab), GOLD, INK, 2.5)
        thp = P([TH])[0]
        s += f'<circle cx="{thp[0]:.1f}" cy="{thp[1]:.1f}" r="{thr * C:.1f}" fill="{GOLD}" stroke="{INK}" stroke-width="2"/>\n'
        s += poly(P(elev), MOVE, INK, 2.5)
        hp = P([H])[0]
        s += f'<circle cx="{hp[0]:.1f}" cy="{hp[1]:.1f}" r="{hr * C:.1f}" fill="{MOVE}" stroke="{INK}" stroke-width="2.5"/>\n'
        s += poly(P(stab), "#b8c0ca", INK, 2.5)
        # elevator chord extension and tab angle arc
        ext = rot((tab_hinge + 0.19, 0.0), (hinge, 0.0), ed)
        e0, e1 = P([TH, ext])
        s += line(e0[0], e0[1], e1[0], e1[1], "#64748b", 2, dash="6 5")
        R = 40
        a0 = math.radians(ed)
        a1 = math.radians(ed + tab_rel)
        p0 = (e0[0] + R * math.cos(a0), e0[1] + R * math.sin(a0))
        p1 = (e0[0] + R * math.cos(a1), e0[1] + R * math.sin(a1))
        s += f'<path d="M {p0[0]:.1f} {p0[1]:.1f} A {R} {R} 0 0 1 {p1[0]:.1f} {p1[1]:.1f}" fill="none" stroke="{GOLD_DARK}" stroke-width="3"/>\n'
        s += t(px + 180, py + 232, "Tab angle to elevator: 20°", 16, 800, GOLD_DARK)

    # bottom strip
    by = 410
    s += f'<rect x="48" y="{by}" width="540" height="176" rx="12" fill="#fff8e1" stroke="{GOLD}" stroke-width="3"/>\n'
    wx, wy = 118, by + 90
    for k in range(16):
        a = 2 * math.pi * k / 16
        s += line(wx + 44 * math.cos(a), wy + 44 * math.sin(a), wx + 52 * math.cos(a), wy + 52 * math.sin(a), INK, 5, cap="butt")
    s += f'<circle cx="{wx}" cy="{wy}" r="45" fill="#e2e8f0" stroke="{INK}" stroke-width="4"/>\n'
    s += f'<circle cx="{wx}" cy="{wy}" r="11" fill="{INK}"/>\n'
    s += t(wx, by + 164, "TRIM WHEEL", 13, 800, INK)
    s += t(196, by + 42, "ONLY THE TRIM WHEEL MOVES THE TAB", 18, 800, INK, "start")
    for i, ln in enumerate(["The pilot sets the tab angle with the", "trim wheel. Moving the control column", "moves the elevator, not the tab setting."]):
        s += t(196, by + 78 + i * 27, ln, 17, 400, BODY, "start")

    s += f'<rect x="612" y="{by}" width="540" height="176" rx="12" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2"/>\n'
    s += t(632, by + 42, "TRIM TAB VS BALANCE TAB", 18, 800, INK, "start")
    rows = [
        ("Adjustable trim tab:", "stays at the selected angle"),
        ("", "as the elevator moves."),
        ("Balance tab:", "geared to move opposite to"),
        ("", "the surface every time it moves."),
    ]
    for i, (a, b) in enumerate(rows):
        y = by + 78 + i * 25
        if a:
            s += t(632, y, a, 17, 800, INK, "start")
        s += t(812, y, b, 17, 400, BODY, "start")

    s += footer("An adjustable trim tab keeps its selected angle whatever the elevator deflection.")
    return s


# =====================================================================
# batch 3 shared helpers
# =====================================================================

def badge(x, y, n):
    return (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="15" fill="{NAVY}"/>\n'
            + t(x, y + 6, str(n), 17, 800, "#ffffff"))


def legend_rows(items, y0=500):
    s = ""
    for i, txt in enumerate(items):
        y = y0 + i * 36
        s += badge(66, y - 6, i + 1)
        s += t(92, y, txt, 17, 700, INK, "start")
    return s


def fact_column(facts):
    s = ""
    for i, (title, lines_) in enumerate(facts):
        fy = 146 + i * 150
        s += f'<rect x="770" y="{fy}" width="378" height="138" rx="12" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2"/>\n'
        s += f'<rect x="770" y="{fy}" width="8" height="138" rx="4" fill="{GOLD}"/>\n'
        s += t(796, fy + 34, title, 19, 800, INK, "start")
        for j, ln in enumerate(lines_):
            s += t(796, fy + 66 + j * 25, ln, 17, 400, BODY, "start")
    return s


def three_boxes(boxes, answer, by=452, h=136):
    s = ""
    for bx, title, lines_ in boxes:
        if title == answer:
            s += f'<rect x="{bx}" y="{by}" width="340" height="{h}" rx="12" fill="#fff8e1" stroke="{GOLD}" stroke-width="4"/>\n'
            s += f'<rect x="{bx + 236}" y="{by + 14}" width="90" height="28" rx="14" fill="{GOLD}"/>\n'
            s += t(bx + 281, by + 33, "ANSWER", 14, 800, NAVY)
        else:
            s += f'<rect x="{bx}" y="{by}" width="340" height="{h}" rx="12" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2"/>\n'
        s += t(bx + 20, by + 34, title, 19, 800, INK, "start")
        for i, ln in enumerate(lines_):
            s += t(bx + 20, by + 66 + i * 25, ln, 17, 400, BODY, "start")
    return s


# =====================================================================
# wing structure (q2440 / q2458 main spar, q2461 ribs, q2430 rear spar)
# =====================================================================

WING_FOOTERS = {
    "MAIN SPAR": "The main spar is the primary load-carrying member of the wing.",
    "RIBS": "Ribs give the wing both its aerofoil shape and strength, passing loads to the spars.",
    "REAR SPAR": "Ailerons and flaps are usually attached to the rear (auxiliary) spar.",
}


def wing(answer):
    s = header(f"WING STRUCTURE: {answer}")
    up, lo = naca(0.02, 0.4, 0.12, 60)
    C, n = 300, 6
    X0, Y0, ddx, ddy = 110, 390, 92, -40

    def R(i, pts):
        return [(X0 + i * ddx + x * C, Y0 + i * ddy - y * C) for x, y in pts]

    def U(x):
        return (x, interp(up, x))

    def L(x):
        return (x, interp(lo, x))

    rib_shape = up + list(reversed(lo))
    rib_fill, rib_stroke, rib_w = ("#f4c542", GOLD_DARK, 3.5) if answer == "RIBS" else ("#e2e8f0", "#475569", 2.5)
    for i in reversed(range(n)):
        s += poly(R(i, rib_shape), rib_fill, rib_stroke, rib_w, ' fill-opacity="0.75"')
    # aileron / flap behind the rear spar on the outer bays
    ail = R(3, [U(0.72)]) + R(5, [U(0.72)]) + R(5, [(1.0, 0.0)]) + R(3, [(1.0, 0.0)])
    s += poly(ail, MOVE, "#1f4e79", 2.5, ' fill-opacity="0.9"')
    # spars
    for xs, name in ((0.25, "MAIN SPAR"), (0.70, "REAR SPAR")):
        band = R(0, [U(xs)]) + R(n - 1, [U(xs)]) + R(n - 1, [L(xs)]) + R(0, [L(xs)])
        fill = GOLD if answer == name else "#94a3b8"
        s += poly(band, fill, INK, 2.5, ' fill-opacity="0.9"')
    # stringers along the upper surface
    for x in (0.08, 0.45, 0.55, 0.85):
        a, b = R(0, [U(x)])[0], R(n - 1, [U(x)])[0]
        s += line(a[0], a[1], b[0], b[1], "#475569", 2.5)
    # leading and trailing edges
    for x in (0.0, 1.0):
        a, b = R(0, [(x, 0.0)])[0], R(n - 1, [(x, 0.0)])[0]
        s += line(a[0], a[1], b[0], b[1], INK, 3)

    def lbl(x, y, text, target, name):
        col = GOLD_DARK if name == answer else INK
        out = t(x, y, text, 18, 800, col)
        ty = y + 8 if target[1] > y else y - 20
        out += line(x, ty, target[0], target[1], col, 2.5, "aDark")
        return out

    ms = R(0, [L(0.25)])[0]
    rs = R(0, [L(0.70)])[0]
    s += lbl(150, 438, "MAIN SPAR", (ms[0] - 2, ms[1] + 6), "MAIN SPAR")
    s += lbl(345, 438, "REAR SPAR", (rs[0] + 2, rs[1] + 6), "REAR SPAR")
    rb = R(0, [(0.02, 0.0)])[0]
    s += lbl(70, 318, "RIBS", (rb[0] - 4, rb[1] - 6), "RIBS")
    st = R(3, [U(0.45)])[0]
    s += lbl(430, 176, "STRINGERS", (st[0], st[1] - 4), "STRINGERS")
    ap = R(5, [(0.92, 0.01)])[0]
    s += t(1000, 236, "AILERON / FLAP", 18, 800, "#1f4e79")
    s += t(1000, 258, "(HINGED TO REAR SPAR)", 14, 700, "#1f4e79")
    s += line(930, 240, ap[0] + 6, ap[1] + 2, "#1f4e79", 2.5, "aDark")

    boxes = [
        (60, "MAIN SPAR", ["Main spanwise beam that", "carries most of the wing's", "bending load."]),
        (430, "RIBS", ["Give the wing its aerofoil", "shape and add strength,", "passing loads to the spars."]),
        (800, "REAR SPAR", ["Second spanwise member;", "ailerons and flaps are", "usually hinged to it."]),
    ]
    s += three_boxes(boxes, answer)
    s += footer(WING_FOOTERS[answer])
    return s


# =====================================================================
# q2462 servo tab
# =====================================================================

def q2462():
    s = header("SERVO TAB")
    C, X0, Y0 = 560, 92, 290
    P = lambda pts: to_px(pts, X0, Y0, C)
    hinge, tab_hinge = 0.58, 0.82
    elev_deg, tab_rel = 18, -38
    T = lambda p: rot(rot(p, (tab_hinge, 0.0), tab_rel), (hinge, 0.0), elev_deg)

    _, g_elev, g_tab, _, _ = tail_parts(hinge, tab_hinge, 0, 0)
    s += poly(P(g_elev), "none", "#94a3b8", 2.5, ' stroke-dasharray="9 7"')
    s += poly(P(g_tab), "none", "#94a3b8", 2.5, ' stroke-dasharray="9 7"')
    stab, elev, tab, (H, hr), (TH, thr) = tail_parts(hinge, tab_hinge, elev_deg, tab_rel)
    s += poly(P(tab), GOLD, INK, 3)
    thp = P([TH])[0]
    s += f'<circle cx="{thp[0]:.1f}" cy="{thp[1]:.1f}" r="{thr * C:.1f}" fill="{GOLD}" stroke="{INK}" stroke-width="2.5"/>\n'
    s += poly(P(elev), MOVE, INK, 3)
    hp = P([H])[0]
    s += f'<circle cx="{hp[0]:.1f}" cy="{hp[1]:.1f}" r="{hr * C:.1f}" fill="{MOVE}" stroke="{INK}" stroke-width="3"/>\n'
    s += poly(P(stab), "#b8c0ca", INK, 3)
    s += f'<circle cx="{hp[0]:.1f}" cy="{hp[1]:.1f}" r="5" fill="{INK}"/>\n'
    s += f'<circle cx="{thp[0]:.1f}" cy="{thp[1]:.1f}" r="4" fill="{INK}"/>\n'

    # pilot's control rod to a horn under the tab
    h0, h1 = P([T((tab_hinge + 0.004, -half_t(tab_hinge) * 0.6)), T((tab_hinge + 0.004, -0.11))])
    s += line(h0[0], h0[1], h1[0], h1[1], INK, 5)
    st = (60, 424)
    s += line(st[0], st[1], h1[0], h1[1], "#1f4e79", 5)
    for p in (st, h1):
        s += f'<circle cx="{p[0]:.1f}" cy="{p[1]:.1f}" r="6" fill="#ffffff" stroke="{INK}" stroke-width="2.5"/>\n'
    s += t(52, 454, "FROM THE PILOT'S CONTROLS", 16, 800, "#1f4e79", "start")

    for yy in (252, 290, 328):
        s += line(38, yy, 80, yy, BLUE, 4, "aBlue")
    s += t(70, 234, "AIRFLOW", 14, 800, BLUE)

    tcp = P([T((tab_hinge + 0.07, 0.0))])[0]
    s += line(tcp[0], tcp[1] - 74, tcp[0], tcp[1] - 14, RED, 6, "aRed")

    s += t(250, 214, "STABILISER (FIXED)")
    s += t(740, 470, "Dashed outline = neutral position", 15, 400, MUTED, "end")

    mid = ((st[0] + h1[0]) / 2, (st[1] + h1[1]) / 2)
    s += badge(mid[0], mid[1] - 30, 1)
    s += badge(tcp[0] + 34, tcp[1] - 52, 2)
    ep = P([rot((0.72, half_t(0.72)), (hinge, 0.0), elev_deg)])[0]
    s += badge(ep[0] - 14, ep[1] - 50, 3)
    s += line(ep[0] - 10, ep[1] - 36, ep[0] - 2, ep[1] - 6, INK, 2, "aDark")

    s += legend_rows([
        "PILOT'S CONTROLS MOVE ONLY THE TAB (TAB UP)",
        "AIR LOAD ON THE TAB ACTS DOWNWARD",
        "FREE-HINGED SURFACE IS DRIVEN DOWN",
    ])
    s += fact_column([
        ("DIRECT TO THE TAB", ["The pilot's controls connect", "to the tab, not to the", "control surface."]),
        ("AERODYNAMIC DRIVE", ["The tab's air load moves the", "free-hinged control surface."]),
        ("LOW CONTROL FORCES", ["Used where moving the surface", "directly would be too heavy."]),
    ])
    s += footer("A servo tab is connected directly to the pilot's controls and drives the surface aerodynamically.")
    return s


# =====================================================================
# q2463 anti-balance (anti-servo) tab on a stabilator
# =====================================================================

def q2463():
    s = header("ANTI-BALANCE (ANTI-SERVO) TAB")
    C, X0, Y0 = 560, 92, 282
    P = lambda pts: to_px(pts, X0, Y0, C)
    pivot = (0.25, 0.0)
    tab_hinge = 0.80
    stab_deg, tab_rel = 12, 21  # 21 deg solves the fixed-length link for 12 deg of stabilator

    def parts(sd, tr):
        body = seg(SYM_UP, 0, tab_hinge) + list(reversed(seg(SYM_LO, 0, tab_hinge)))
        tab = seg(SYM_UP, tab_hinge, 1.0) + list(reversed(seg(SYM_LO, tab_hinge, 1.0)))
        tab = [rot(rot(p, (tab_hinge, 0.0), tr), pivot, sd) for p in tab]
        body = [rot(p, pivot, sd) for p in body]
        return body, tab

    T = lambda p: rot(rot(p, (tab_hinge, 0.0), tab_rel), pivot, stab_deg)
    gb, gt = parts(0, 0)
    s += poly(P(gb), "none", "#94a3b8", 2.5, ' stroke-dasharray="9 7"')
    s += poly(P(gt), "none", "#94a3b8", 2.5, ' stroke-dasharray="9 7"')
    # link from a fixed fuselage point near the pivot to a horn under the tab;
    # drawn first so it passes behind the stabilator section
    F = P([(0.35, 0.15)])[0]
    h0, h1 = P([T((tab_hinge + 0.004, -half_t(tab_hinge) * 0.6)), T((tab_hinge + 0.004, -0.11))])
    s += line(F[0], F[1], h1[0], h1[1], "#334155", 5)
    body, tab = parts(stab_deg, tab_rel)
    s += poly(P(tab), GOLD, INK, 3)
    thp = P([rot((tab_hinge, 0.0), pivot, stab_deg)])[0]
    s += f'<circle cx="{thp[0]:.1f}" cy="{thp[1]:.1f}" r="{half_t(tab_hinge) * C:.1f}" fill="{GOLD}" stroke="{INK}" stroke-width="2.5"/>\n'
    s += poly(P(body), MOVE, INK, 3)
    s += f'<circle cx="{thp[0]:.1f}" cy="{thp[1]:.1f}" r="4" fill="{INK}"/>\n'
    s += line(h0[0], h0[1], h1[0], h1[1], INK, 5)
    pp = P([pivot])[0]
    s += f'<circle cx="{pp[0]:.1f}" cy="{pp[1]:.1f}" r="9" fill="#ffffff" stroke="{INK}" stroke-width="3"/>\n'
    s += f'<circle cx="{pp[0]:.1f}" cy="{pp[1]:.1f}" r="3.5" fill="{INK}"/>\n'
    s += t(pp[0], 372, "PIVOT", 16, 800)
    s += line(pp[0], 356, pp[0], 344, INK, 2.5, "aDark")
    fx, fy = F
    s += f'<rect x="{fx - 26:.1f}" y="{fy - 30:.1f}" width="52" height="22" fill="#e2e8f0" stroke="{INK}" stroke-width="2.5"/>\n'
    for k in range(5):
        s += line(fx - 22 + k * 11, fy - 10, fx - 14 + k * 11, fy - 28, "#94a3b8", 2)
    s += line(fx, fy - 8, fx, fy, INK, 4)
    for q in (F, h1):
        s += f'<circle cx="{q[0]:.1f}" cy="{q[1]:.1f}" r="6" fill="#ffffff" stroke="{INK}" stroke-width="2.5"/>\n'
    s += t(fx, fy - 42, "FIXED TO FUSELAGE", 15, 800, "#334155")

    for yy in (244, 282, 320):
        s += line(38, yy, 80, yy, BLUE, 4, "aBlue")
    s += t(70, 226, "AIRFLOW", 14, 800, BLUE)
    s += t(60, 440, "STABILATOR (ALL-MOVING TAILPLANE)", 17, 800, INK, "start")

    tcp = P([T((tab_hinge + 0.08, 0.0))])[0]
    s += line(tcp[0] + 6, tcp[1] + 78, tcp[0] + 6, tcp[1] + 16, RED, 6, "aRed")
    s += t(745, 470, "Dashed outline = neutral position", 15, 400, MUTED, "end")

    bp = P([rot((0.55, -half_t(0.55)), pivot, stab_deg)])[0]
    s += badge(bp[0] - 40, bp[1] + 46, 1)
    s += line(bp[0] - 28, bp[1] + 36, bp[0] - 4, bp[1] + 6, INK, 2, "aDark")
    te = P([T((1.0, 0.0))])[0]
    s += badge(te[0] + 34, te[1] - 10, 2)
    s += badge(tcp[0] + 40, tcp[1] + 64, 3)

    s += legend_rows([
        "STABILATOR TRAILING EDGE MOVES DOWN",
        "ANTI-BALANCE TAB MOVES DOWN TOO (SAME WAY)",
        "AIR LOAD ON THE TAB RESISTS THE MOVEMENT",
    ])
    s += fact_column([
        ("SAME DIRECTION", ["The tab moves the same way", "as the stabilator."]),
        ("ADDS CONTROL FEEL", ["Its air load opposes the", "movement, increasing the", "stick force."]),
        ("PREVENTS OVER-CONTROL", ["A sensitive all-moving", "tailplane cannot be moved", "too easily."]),
    ])
    s += footer("An anti-balance tab moves with the stabilator, adding feel and preventing over-control.")
    return s


# =====================================================================
# batch 4: side-view aircraft helper
# =====================================================================

def plane(cx, cy, sc, deg=0.0, fill="#dfe5ec", ttail=False):
    """Light high-wing aircraft, nose to the left. Returns (svg, to_page)."""
    a = math.radians(deg)

    def pg(x, y):
        x, y = x * sc, y * sc
        return (cx + x * math.cos(a) - y * math.sin(a), cy + x * math.sin(a) + y * math.cos(a))

    ns = ' vector-effect="non-scaling-stroke"'
    g = f'<g transform="translate({cx:.1f},{cy:.1f}) rotate({deg:.2f}) scale({sc})">\n'
    fin = "M 66,-12 L 92,-60 L 108,-60 L 108,-8 Z" if ttail else "M 70,-12 L 90,-46 L 107,-46 L 108,-8 Z"
    g += f'<path d="{fin}" fill="{fill}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"{ns}/>\n'
    g += f'<path d="M -100,0 C -100,-17 -82,-24 -52,-24 L 40,-16 L 106,-9 L 108,3 L 40,9 L -52,15 C -86,15 -100,10 -100,0 Z" fill="{fill}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"{ns}/>\n'
    g += f'<path d="M -58,-23 Q -34,-40 2,-21 Z" fill="#bfdbfe" stroke="{INK}" stroke-width="2"{ns}/>\n'
    g += f'<ellipse cx="-14" cy="-27" rx="34" ry="5" fill="#94a3b8" stroke="{INK}" stroke-width="2.5"{ns}/>\n'
    sy = -61 if ttail else -5
    g += f'<ellipse cx="{98 if ttail else 94}" cy="{sy}" rx="18" ry="3.2" fill="#94a3b8" stroke="{INK}" stroke-width="2"{ns}/>\n'
    g += f'<line x1="-40" y1="-26" x2="-30" y2="8" stroke="{INK}" stroke-width="2"{ns}/>\n'
    g += f'<ellipse cx="-104" cy="0" rx="3.5" ry="27" fill="#64748b" stroke="{INK}" stroke-width="1.5"{ns}/>\n'
    g += f'<line x1="-58" y1="14" x2="-60" y2="26" stroke="{INK}" stroke-width="2.5"{ns}/>\n'
    g += f'<line x1="-22" y1="12" x2="-18" y2="25" stroke="{INK}" stroke-width="2.5"{ns}/>\n'
    for wx, wy in ((-60, 29), (-17, 28)):
        g += f'<circle cx="{wx}" cy="{wy}" r="5" fill="{INK}"/>\n'
    g += "</g>\n"
    return g, pg


def cg_mark(x, y, r=11):
    s = f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="#ffffff" stroke="{INK}" stroke-width="2.5"/>\n'
    s += f'<path d="M {x:.1f} {y - r:.1f} A {r} {r} 0 0 1 {x + r:.1f} {y:.1f} L {x:.1f} {y:.1f} Z" fill="{INK}"/>\n'
    s += f'<path d="M {x:.1f} {y + r:.1f} A {r} {r} 0 0 1 {x - r:.1f} {y:.1f} L {x:.1f} {y:.1f} Z" fill="{INK}"/>\n'
    return s


def force(x1, y1, x2, y2, label, col=RED, lx=None, ly=None, anchor="middle", size=15):
    s = line(x1, y1, x2, y2, col, 5, "aRed" if col == RED else ("aBlue" if col == BLUE else "aDark"))
    if label:
        s += t(lx if lx is not None else x2, ly if ly is not None else y2, label, size, 800, col, anchor)
    return s


# =====================================================================
# Newton's laws (q2465 first, q2433 second, q2447 third)
# =====================================================================

NEWTON = {
    "FIRST": ("NEWTON'S FIRST LAW", "Newton's first law: with no net force an object stays in equilibrium."),
    "SECOND": ("NEWTON'S SECOND LAW", "Newton's second law: a net force causes acceleration or deceleration (F = m × a)."),
    "THIRD": ("NEWTON'S THIRD LAW", "Newton's third law: every action has an equal and opposite reaction."),
}


def newton(answer):
    title, foot = NEWTON[answer]
    s = header(title)
    panels = [
        (48, "FIRST", "1ST LAW", "EQUILIBRIUM (INERTIA)",
         ["An object stays at rest or at", "constant velocity unless a", "net force acts on it."], "Forces balanced: no change"),
        (420, "SECOND", "2ND LAW", "ACCELERATION",
         ["A net force produces", "acceleration: speeding up,", "slowing down or turning."], "F = m × a"),
        (792, "THIRD", "3RD LAW", "ACTION AND REACTION",
         ["Every action has an equal", "and opposite reaction."], "Air pushed back, aircraft forward"),
    ]
    for px, key, head, sub, lines_, key_line in panels:
        ans = key == answer
        py, w, h = 142, 360, 444
        if ans:
            s += f'<rect x="{px}" y="{py}" width="{w}" height="{h}" rx="12" fill="#fff8e1" stroke="{GOLD}" stroke-width="4"/>\n'
            s += f'<rect x="{px + 256}" y="{py + 14}" width="90" height="28" rx="14" fill="{GOLD}"/>\n'
            s += t(px + 301, py + 33, "ANSWER", 14, 800, NAVY)
        else:
            s += f'<rect x="{px}" y="{py}" width="{w}" height="{h}" rx="12" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2"/>\n'
        s += t(px + 20, py + 36, head, 22, 800, INK, "start")
        s += t(px + 20, py + 64, sub, 16, 800, GOLD_DARK if ans else BODY, "start")
        cx, cy = px + 180, py + 196
        g, pg = plane(cx, cy, 0.95)
        s += g
        nose = pg(-107, 0)
        tail = pg(108, -2)
        if key == "FIRST":
            c = pg(-14, -30)
            s += force(c[0], c[1] - 4, c[0], c[1] - 56, "LIFT", ly=c[1] - 64)
            w0 = pg(-12, 30)
            s += force(w0[0], w0[1], w0[0], w0[1] + 50, "WEIGHT", ly=w0[1] + 72)
            s += force(nose[0], nose[1], nose[0] - 44, nose[1], "THRUST", lx=nose[0] - 18, ly=nose[1] + 44)
            s += force(tail[0], tail[1], tail[0] + 44, tail[1], "DRAG", lx=tail[0] + 20, ly=tail[1] + 42)
        elif key == "SECOND":
            s += force(nose[0], nose[1], nose[0] - 46, nose[1], "THRUST", lx=nose[0] - 18, ly=nose[1] + 44)
            s += force(tail[0], tail[1], tail[0] + 18, tail[1], "DRAG", lx=tail[0] + 8, ly=tail[1] + 42)
            s += line(cx + 60, cy - 78, cx - 60, cy - 78, GOLD_DARK, 7, "aDark")
            s += t(cx, cy - 94, "ACCELERATES", 16, 800, GOLD_DARK)
            s += t(cx, cy + 72, "THRUST > DRAG", 15, 800, INK)
        else:
            s += force(nose[0], nose[1], nose[0] - 44, nose[1], "")
            for dy in (-30, 30):
                s += line(nose[0] + 12, nose[1] + dy, nose[0] + 92, nose[1] + dy, BLUE, 5, "aBlue")
            s += t(cx, cy - 64, "REACTION: AIRCRAFT PUSHED FORWARD", 14, 800, RED)
            s += t(cx, cy + 66, "ACTION: AIR PUSHED BACK", 14, 800, BLUE)
        for i, ln in enumerate(lines_):
            s += t(px + 180, py + 332 + i * 25, ln, 17, 400, BODY)
        s += t(px + 180, py + 420, key_line, 18, 800, INK)
    s += footer(foot)
    return s


# =====================================================================
# q2432 / q2449 CG too far aft
# =====================================================================

def q2432():
    s = header("CG TOO FAR AFT")
    rows = [(142, "CG WITHIN LIMITS", -30, False), (368, "CG TOO FAR AFT", 7, True)]
    for py, title, cg_dx, bad in rows:
        if bad:
            s += f'<rect x="40" y="{py}" width="710" height="218" rx="12" fill="#fff8e1" stroke="{GOLD}" stroke-width="4"/>\n'
        else:
            s += f'<rect x="40" y="{py}" width="710" height="218" rx="12" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2"/>\n'
        s += t(60, py + 32, title, 19, 800, INK, "start")
        cx, cy = 320, py + 120
        g, pg = plane(cx, cy, 1.4)
        s += g
        ac = pg(-10, -12)
        s += force(ac[0], cy - 46, ac[0], cy - 86, "")
        s += t(ac[0] + 12, cy - 72, "LIFT / AERODYNAMIC CENTRE", 13, 800, RED, "start")
        s += f'<line x1="{ac[0]:.1f}" y1="{cy - 44:.1f}" x2="{ac[0]:.1f}" y2="{cy + 30:.1f}" stroke="{RED}" stroke-width="2" stroke-dasharray="5 4"/>\n'
        cgx = ac[0] + cg_dx
        s += cg_mark(cgx, ac[1] + 8, 9)
        tail = pg(94, -5)
        yb = cy + 66
        s += line(cgx, yb - 9, cgx, yb + 9, INK, 2)
        s += line(tail[0], yb - 9, tail[0], yb + 9, INK, 2)
        s += line(cgx + 3, yb, tail[0] - 3, yb, INK, 2.5)
        s += t((cgx + tail[0]) / 2, yb - 7, "TAIL ARM", 13, 800, INK)
        col = RED if bad else "#15803d"
        l1, l2 = (("CG AT / BEHIND THE", "AERODYNAMIC CENTRE") if bad else ("CG WELL AHEAD OF THE", "AERODYNAMIC CENTRE"))
        m1, m2 = (("SHORTER ARM, WEAK", "RESTORING MOMENT") if bad else ("LONGER ARM, STRONG", "RESTORING MOMENT"))
        s += t(530, cy - 14, l1, 15, 800, INK, "start")
        s += t(530, cy + 5, l2, 15, 800, INK, "start")
        s += t(530, cy + 40, m1, 15, 800, col, "start")
        s += t(530, cy + 59, m2, 15, 800, col, "start")
    s += fact_column([
        ("LESS STABLE", ["The CG is closer to the", "aerodynamic centre, so the", "restoring pitch moment is weak."]),
        ("PITCH-SENSITIVE", ["Small inputs give large", "pitch changes; the aircraft", "is easy to over-control."]),
        ("HARDER STALL RECOVERY", ["Less nose-down authority to", "unstall the wing; spin", "recovery may be difficult."]),
    ])
    s += footer("An aft CG reduces longitudinal stability and makes the aeroplane difficult to control in pitch.")
    return s


# =====================================================================
# q2467 power reduction: CG ahead of CP, nose drops
# =====================================================================

def q2467():
    s = header("WHY THE NOSE DROPS WITH LESS POWER")
    rows = [(142, "CRUISE POWER: PITCH BALANCED", 0, False), (368, "POWER REDUCED: NOSE DROPS", -7, True)]
    for py, title, deg, reduced in rows:
        if reduced:
            s += f'<rect x="40" y="{py}" width="710" height="218" rx="12" fill="#fff8e1" stroke="{GOLD}" stroke-width="4"/>\n'
        else:
            s += f'<rect x="40" y="{py}" width="710" height="218" rx="12" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2"/>\n'
        s += t(60, py + 32, title, 19, 800, INK, "start")
        cx, cy = 330, py + 122
        g, pg = plane(cx, cy, 1.4, deg)
        s += g
        cg = pg(-26, -4)
        cp = pg(-4, -30)
        s += cg_mark(cg[0], cg[1], 9)
        s += force(cg[0], cg[1] + 11, cg[0], cg[1] + 48, "WEIGHT", ly=cg[1] + 66, size=13)
        s += force(cp[0], cp[1] - 4, cp[0], cp[1] - 42, "")
        s += t(cp[0] + 10, cp[1] - 30, "LIFT (CP)", 13, 800, RED, "start")
        nose = pg(-108, 6)
        tail = pg(94, -5)
        dl = 22 if reduced else 36
        s += force(tail[0], tail[1] + 4, tail[0], tail[1] + 4 + dl, "")
        s += t(tail[0], tail[1] + dl + 24, "LESS TAIL DOWNLOAD" if reduced else "TAIL DOWNLOAD", 13, 800, RED)
        if reduced:
            s += force(nose[0] - 2, nose[1], nose[0] - 20, nose[1], "")
            s += t(nose[0] - 10, nose[1] + 30, "THRUST", 13, 800, RED, "end")
            s += t(nose[0] - 10, nose[1] + 46, "REDUCED", 13, 800, RED, "end")
            s += f'<path d="M {nose[0] + 36:.1f} {nose[1] - 58:.1f} Q {nose[0] - 22:.1f} {nose[1] - 54:.1f} {nose[0] - 30:.1f} {nose[1] - 10:.1f}" fill="none" stroke="{GOLD_DARK}" stroke-width="5" marker-end="url(#aDark)"/>\n'
            s += t(nose[0] - 20, nose[1] - 62, "NOSE DROPS", 15, 800, GOLD_DARK, "end")
            n1, n2, col = "LIFT-WEIGHT COUPLE", "NOW WINS: NOSE DOWN", GOLD_DARK
        else:
            s += force(nose[0] - 2, nose[1], nose[0] - 46, nose[1], "")
            s += t(nose[0] - 10, nose[1] + 30, "THRUST", 13, 800, RED, "end")
            n1, n2, col = "NOSE-DOWN COUPLE", "BALANCED BY POWER", "#15803d"
        s += t(560, cy - 6, n1, 14, 800, INK, "start")
        s += t(560, cy + 13, n2, 14, 800, col, "start")
    s += fact_column([
        ("CG AHEAD OF CP", ["Lift acts behind the weight,", "giving a nose-down couple."]),
        ("BALANCED BY POWER", ["In steady flight the thrust-", "drag couple and tail download", "hold the nose up."]),
        ("POWER REDUCED", ["The nose-up moment shrinks,", "so the nose drops until a", "new balance is reached."]),
    ])
    s += footer("With the CG ahead of the centre of pressure, reducing power lets the nose drop.")
    return s


# =====================================================================
# batch 5 drawn: T-tail (q2759), trim tab purpose (q2743), slats (q2434)
# =====================================================================

def two_panels(s, titles, answer_idx):
    for i, title in enumerate(titles):
        py = 142 + i * 226
        if i == answer_idx:
            s += f'<rect x="40" y="{py}" width="710" height="218" rx="12" fill="#fff8e1" stroke="{GOLD}" stroke-width="4"/>\n'
        else:
            s += f'<rect x="40" y="{py}" width="710" height="218" rx="12" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2"/>\n'
        s += t(60, py + 32, title, 19, 800, INK, "start")
    return s


def wake(pg, tail_y):
    s = ""
    band = [pg(22, -30), pg(135, tail_y - 11), pg(135, tail_y + 11), pg(22, -20)]
    s += poly(band, "#94a3b8", "none", 0, ' fill-opacity="0.28"')
    for k, off in enumerate((-7, 0, 7)):
        pts = []
        for i in range(0, 41):
            x = 22 + i * 113 / 40
            base = -25 + (x - 22) / 113 * (tail_y + 25)
            pts.append(pg(x, base + off + 2.2 * math.sin(i * 0.9 + k)))
        s += polyline(pts, "#64748b", 2)
    return s


def q2759():
    s = header("T-TAIL: TAILPLANE CLEAR OF THE WAKE")
    s = two_panels(s, ["CONVENTIONAL TAIL", "T-TAIL"], 1)
    for i, tt in enumerate((False, True)):
        py = 142 + i * 226
        cx, cy = 300, py + 132
        g_, pg = plane(cx, cy, 1.45, ttail=tt)
        s += g_
        s += wake(pg, -5)
        stab = pg(98, -61) if tt else pg(94, -5)
        if tt:
            s += t(540, cy - 44, "TAILPLANE IN", 15, 800, "#15803d", "start")
            s += t(540, cy - 25, "CLEANER AIRFLOW", 15, 800, "#15803d", "start")
            s += line(535, cy - 40, stab[0] + 30, stab[1] + 2, "#15803d", 2.5, "aDark")
        else:
            s += t(540, cy - 44, "TAILPLANE SITS IN", 15, 800, RED, "start")
            s += t(540, cy - 25, "THE WING WAKE", 15, 800, RED, "start")
            s += line(535, cy - 40, stab[0] + 28, stab[1] - 2, RED, 2.5, "aDark")
        wk = pg(60, -14)
        s += t(540, cy + 26, "WING WAKE /", 14, 700, MUTED, "start")
        s += t(540, cy + 44, "DOWNWASH", 14, 700, MUTED, "start")
        s += line(535, cy + 30, wk[0] + 6, wk[1] + 4, MUTED, 2, "aDark")
    s += fact_column([
        ("CLEANER AIRFLOW", ["The tailplane sits above", "most of the wing and", "fuselage wake."]),
        ("CONSISTENT PITCH CONTROL", ["Smoother flow over the", "tailplane in normal flight."]),
        ("WATCH: DEEP STALL", ["At very high angles of attack", "a stalled wing's wake can", "blanket a T-tail."]),
    ])
    s += footer("A T-tail can place the tailplane outside the wing's normal wake and turbulence.")
    return s


def q2743():
    s = header("PURPOSE OF A TRIM TAB")
    s = two_panels(s, ["BEFORE TRIMMING", "AFTER TRIMMING"], 1)
    hinge, tab_hinge, C = 0.58, 0.82, 360
    for i, trt in enumerate((0, 30)):
        py = 142 + i * 226
        X0, Y0 = 70, py + 124
        P = lambda pts, X0=X0, Y0=Y0: to_px(pts, X0, Y0, C)
        stab, elev, tab, (H, hr), (TH, thr) = tail_parts(hinge, tab_hinge, -16, trt)
        s += poly(P(tab), GOLD, INK, 2.5)
        thp = P([TH])[0]
        s += f'<circle cx="{thp[0]:.1f}" cy="{thp[1]:.1f}" r="{thr * C:.1f}" fill="{GOLD}" stroke="{INK}" stroke-width="2"/>\n'
        s += poly(P(elev), MOVE, INK, 2.5)
        hp = P([H])[0]
        s += f'<circle cx="{hp[0]:.1f}" cy="{hp[1]:.1f}" r="{hr * C:.1f}" fill="{MOVE}" stroke="{INK}" stroke-width="2.5"/>\n'
        s += poly(P(stab), "#b8c0ca", INK, 2.5)
        s += t(210, py + 196, "Elevator held up (nose-up attitude)", 14, 700, MUTED)
        if trt:
            tc = P([rot(rot((tab_hinge + 0.08, 0.0), (tab_hinge, 0.0), trt), (hinge, 0.0), -16)])[0]
            s += line(tc[0] + 4, tc[1] + 58, tc[0] + 4, tc[1] + 12, RED, 5, "aRed")
            s += t(tc[0] + 16, tc[1] + 52, "TAB AIR LOAD", 13, 800, RED, "start")
            s += t(tc[0] + 16, tc[1] + 68, "HOLDS ELEVATOR", 13, 800, RED, "start")
        # stick-force gauge
        gx, gy = 520, py + 84
        s += t(gx, gy - 12, "PILOT'S STICK FORCE", 14, 800, INK, "start")
        s += f'<rect x="{gx}" y="{gy}" width="200" height="26" rx="6" fill="#ffffff" stroke="{INK}" stroke-width="2"/>\n'
        if trt:
            s += t(gx, gy + 58, "ZERO: HANDS OFF", 16, 800, "#15803d", "start")
        else:
            s += f'<rect x="{gx + 3}" y="{gy + 3}" width="174" height="20" rx="4" fill="{RED}"/>\n'
            s += t(gx, gy + 58, "CONSTANT PULL NEEDED", 16, 800, RED, "start")
    s += fact_column([
        ("HOLDS THE SURFACE", ["The tab's air load holds the", "elevator where it is needed."]),
        ("RELIEVES THE PILOT", ["Sustained control forces", "are reduced or cancelled."]),
        ("RE-TRIM AFTER CHANGES", ["of speed, power, flap or", "loading."]),
    ])
    s += footer("A trim tab's primary purpose is to reduce or cancel sustained pilot control forces.")
    return s


def q2434():
    s = header("LEADING-EDGE SLATS")
    up, lo = naca(0.02, 0.4, 0.12, 80)
    C, X0, Y0, aoa = 420, 120, 360, 16
    piv = (0.25, 0.0)
    R_ = lambda pts: to_px([rot(p, piv, aoa) for p in pts], X0, Y0, C)

    def offset(pts, d):
        out = []
        for i in range(len(pts)):
            a, b = pts[max(0, i - 1)], pts[min(len(pts) - 1, i + 1)]
            nx, ny = -(b[1] - a[1]), (b[0] - a[0])
            n = math.hypot(nx, ny) or 1
            out.append((pts[i][0] + nx / n * d, pts[i][1] + ny / n * d))
        return out

    # left panel
    s += f'<rect x="40" y="142" width="560" height="444" rx="12" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2"/>\n'
    s += t(60, 174, "SLAT EXTENDED AT HIGH ANGLE OF ATTACK", 17, 800, INK, "start")
    le = [p for p in reversed(up) if p[0] <= 0.13] + [p for p in lo if 0 < p[0] <= 0.03]
    inner = offset(le, -0.022)
    outer = offset(le, -0.048)
    slat = outer + list(reversed(inner))
    s += poly(R_(up + list(reversed(lo))), "#b8c0ca", INK, 3)
    s += poly(R_(slat), GOLD, INK, 3)
    # free stream and slot flow
    for yy in (300, 340, 380, 420):
        s += line(52, yy, 96, yy, BLUE, 4, "aBlue")
    slot = R_([(-0.05, -0.07), (0.0, -0.035), (0.05, 0.035), (0.14, 0.085)])
    d = f"M {slot[0][0]:.1f} {slot[0][1]:.1f} C {slot[1][0]:.1f} {slot[1][1]:.1f} {slot[2][0]:.1f} {slot[2][1]:.1f} {slot[3][0]:.1f} {slot[3][1]:.1f}"
    s += f'<path d="{d}" fill="none" stroke="{BLUE}" stroke-width="4" marker-end="url(#aBlue)"/>\n'
    over = R_([(0.16, 0.11), (0.45, 0.13), (0.75, 0.09), (1.02, 0.04)])
    d = f"M {over[0][0]:.1f} {over[0][1]:.1f} C {over[1][0]:.1f} {over[1][1]:.1f} {over[2][0]:.1f} {over[2][1]:.1f} {over[3][0]:.1f} {over[3][1]:.1f}"
    s += f'<path d="{d}" fill="none" stroke="{BLUE}" stroke-width="4" marker-end="url(#aBlue)"/>\n'
    sp = R_([(0.02, 0.07)])[0]
    s += t(sp[0] - 10, sp[1] - 60, "SLAT", 17, 800, GOLD_DARK, "end")
    s += line(sp[0] - 34, sp[1] - 54, sp[0] - 6, sp[1] - 10, GOLD_DARK, 2.5, "aDark")
    s += t(slot[0][0] + 14, slot[0][1] + 44, "SLOT", 16, 800, BLUE, "start")
    op = R_([(0.55, 0.14)])[0]
    s += t(op[0] + 20, op[1] - 26, "ENERGISED FLOW STAYS ATTACHED", 14, 800, BLUE)
    s += t(320, 548, "Air through the slot re-energises the upper-surface", 15, 400, BODY)
    s += t(320, 568, "boundary layer and delays separation.", 15, 400, BODY)

    # right panel: CL vs AoA
    s += f'<rect x="620" y="142" width="530" height="444" rx="12" fill="#fff8e1" stroke="{GOLD}" stroke-width="4"/>\n'
    s += t(640, 174, "LIFT vs ANGLE OF ATTACK", 17, 800, INK, "start")
    ox, oy, gw, gh = 690, 500, 420, 280
    s += line(ox, oy, ox + gw, oy, INK, 2.5, "aDark")
    s += line(ox, oy, ox, oy - gh, INK, 2.5, "aDark")
    s += t(ox + gw / 2, oy + 40, "ANGLE OF ATTACK", 14, 800, INK)
    s += f'<text x="{ox - 22}" y="{oy - gh / 2}" text-anchor="middle" font-family="{F}" font-size="14" font-weight="800" fill="{INK}" transform="rotate(-90 {ox - 22} {oy - gh / 2})">LIFT COEFFICIENT</text>\n'
    def curve(a_crit, cl_max, col, w):
        pts = []
        for i in range(0, 61):
            a = i * 0.5
            if a <= a_crit:
                cl = cl_max * (a + 3) / (a_crit + 3) - 0.08 * cl_max * ((a / a_crit) ** 6)
            else:
                cl = cl_max * 0.92 - (a - a_crit) * 0.06
            pts.append((ox + a / 30 * gw * 0.95, oy - max(cl, 0) / 2.2 * gh))
        return polyline(pts, col, w)
    s += curve(15, 1.5, "#64748b", 4)
    s += curve(23, 2.0, GOLD_DARK, 5)
    s += t(ox + gw * 0.95, oy - 0.48 / 2.2 * gh + 28, "CLEAN WING", 14, 800, "#475569", "end")
    s += t(ox + 15 / 30 * gw * 0.95, oy + 18, "CLEAN STALL", 11, 800, "#475569")
    s += t(ox + 23 / 30 * gw * 0.95, oy + 18, "SLAT STALL", 11, 800, GOLD_DARK)
    s += t(ox + 23 / 30 * gw * 0.95, oy - 1.9 / 2.2 * gh - 16, "SLAT EXTENDED", 14, 800, GOLD_DARK)
    s += line(ox + 15 / 30 * gw * 0.95, oy, ox + 15 / 30 * gw * 0.95, oy - 8, INK, 2)
    s += line(ox + 23 / 30 * gw * 0.95, oy, ox + 23 / 30 * gw * 0.95, oy - 8, INK, 2)
    s += t(885, 556, "Higher critical angle of attack and", 15, 400, BODY)
    s += t(885, 576, "higher CL max: lower stalling speed.", 15, 400, BODY)
    s += footer("Slats delay the stall, allowing a higher angle of attack and a lower airspeed.")
    return s


# =====================================================================
# batch 6: stall warning (q2436), CP movement (q2439), adverse yaw (q2763), Frise (q2764)
# =====================================================================

CAMB_UP, CAMB_LO = naca(0.02, 0.4, 0.12, 100)


def camb_shape():
    return CAMB_UP + list(reversed(CAMB_LO))


def q2436():
    s = header("STALL WARNING DEVICE")
    s = two_panels(s, ["NORMAL ANGLE OF ATTACK: NO WARNING", "APPROACHING THE STALL: WARNING ON"], 1)
    C = 380
    for i, (aoa, stag_x, vane_deg) in enumerate(((3, 0.004, -35), (15, 0.06, 35))):
        py = 142 + i * 226
        X0, Y0 = 250, py + 118
        piv = (0.25, 0.0)
        R_ = lambda pts, X0=X0, Y0=Y0, aoa=aoa: to_px([rot(p, piv, aoa) for p in pts], X0, Y0, C)
        for yy in (-50, -20, 10, 40):
            s += line(58, Y0 + yy, 100, Y0 + yy, BLUE, 3.5, "aBlue")
        s += poly(R_(camb_shape()), "#b8c0ca", INK, 3)
        vb = (0.025, interp(CAMB_LO, 0.025))
        vt = rot((vb[0] - 0.075, vb[1]), vb, vane_deg)
        a, b = R_([vb, vt])
        s += line(a[0], a[1], b[0], b[1], INK, 7, cap="round")
        s += line(a[0], a[1], b[0], b[1], GOLD, 3.5, cap="round")
        sp = R_([(stag_x, interp(CAMB_LO, stag_x) if stag_x > 0.006 else 0.0)])[0]
        s += f'<circle cx="{sp[0]:.1f}" cy="{sp[1]:.1f}" r="7" fill="{RED}" stroke="#ffffff" stroke-width="2"/>\n'
        if i == 0:
            s += t(b[0] - 6, b[1] + 38, "VANE PUSHED DOWN", 14, 800, INK, "start")
            s += t(sp[0] + 10, sp[1] - 48, "STAGNATION POINT", 13, 800, RED, "start")
            s += line(sp[0] + 18, sp[1] - 42, sp[0] + 4, sp[1] - 8, RED, 2, "aRedS")
            s += t(560, py + 104, "NO WARNING", 18, 800, "#15803d", "start")
        else:
            s += t(b[0] - 10, b[1] - 12, "VANE LIFTED", 14, 800, GOLD_DARK, "end")
            s += t(120, py + 196, "STAGNATION POINT MOVES DOWN AND AFT, BELOW THE VANE", 13, 800, RED, "start")
            s += line(sp[0] - 30, py + 182, sp[0] - 2, sp[1] + 8, RED, 2, "aRedS")
            s += t(560, py + 96, "HORN / LIGHT", 18, 800, RED, "start")
            s += t(560, py + 118, "BEFORE THE STALL", 18, 800, RED, "start")
    s += fact_column([
        ("SET TO WARN EARLY", ["Activates a few knots", "before the critical angle", "of attack is reached."]),
        ("HOW IT WORKS", ["At high angles of attack the", "stagnation point moves below", "the vane and airflow lifts it."]),
        ("TIME TO RECOVER", ["The pilot can lower the", "angle of attack before the", "stall develops."]),
    ])
    s += footer("The stall warning is adjusted to activate just before the stall.")
    return s


def q2439():
    s = header("CENTRE OF PRESSURE MOVEMENT")
    s += f'<rect x="40" y="142" width="710" height="444" rx="12" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2"/>\n'
    C, X0 = 380, 250
    rows = [(2, 0.42, "SMALL ANGLE"), (7, 0.33, "MEDIUM ANGLE"), (13, 0.26, "LARGER ANGLE")]
    cps = []
    for i, (aoa, cp, label) in enumerate(rows):
        Y0 = 214 + i * 124
        piv = (0.25, 0.0)
        R_ = lambda pts, Y0=Y0, aoa=aoa: to_px([rot(p, piv, aoa) for p in pts], X0, Y0, C)
        s += t(60, Y0 - 4, label, 15, 800, BODY, "start")
        s += poly(R_(camb_shape()), "#b8c0ca", INK, 3)
        c = R_([(cp, (interp(CAMB_UP, cp) + interp(CAMB_LO, cp)) / 2)])[0]
        s += line(c[0], c[1] - 8, c[0], c[1] - 46, RED, 5, "aRed")
        s += f'<circle cx="{c[0]:.1f}" cy="{c[1]:.1f}" r="6" fill="{RED}" stroke="#ffffff" stroke-width="2"/>\n'
        s += t(c[0] + 12, c[1] - 30, "CP", 16, 800, RED, "start")
        cps.append(c)
        s += t(60, Y0 + 16, f"({aoa}°)" if i < 2 else f"({aoa}°, below stall)", 14, 700, MUTED, "start")
    s += polyline(cps, GOLD_DARK, 3, dash="8 6")
    s += line(cps[0][0] + 110, 560, cps[-1][0] - 10, 560, GOLD_DARK, 5, "aDark")
    s += t((cps[0][0] + cps[-1][0]) / 2 + 50, 548, "CP MOVES FORWARD", 16, 800, GOLD_DARK)
    s += fact_column([
        ("MOVES FORWARD", ["As the angle of attack", "increases in normal flight,", "the CP moves forward."]),
        ("PITCHING MOMENT CHANGES", ["The shift alters the balance", "of forces about the CG."]),
        ("AT THE STALL", ["The CP moves rapidly aft,", "helping the nose to drop."]),
    ])
    s += footer("As angle of attack increases (below the stall), the centre of pressure moves forward.")
    return s


def top_plane(cx, cy, sc):
    """Top view, nose up. Returns (svg, pg) with pg mapping local to page."""
    pg = lambda x, y: (cx + x * sc, cy + y * sc)
    s = ""
    wing = [(-150, -12), (150, -12), (150, 22), (-150, 22)]
    s += poly([pg(*p) for p in wing], "#dfe5ec", INK, 3)
    tail = [(-55, 118), (55, 118), (55, 138), (-55, 138)]
    s += poly([pg(*p) for p in tail], "#dfe5ec", INK, 3)
    fus = f"M {pg(0, -92)[0]:.1f} {pg(0, -92)[1]:.1f} C {pg(20, -88)[0]:.1f} {pg(20, -88)[1]:.1f} {pg(20, -40)[0]:.1f} {pg(20, -40)[1]:.1f} {pg(16, 20)[0]:.1f} {pg(16, 20)[1]:.1f} L {pg(6, 140)[0]:.1f} {pg(6, 140)[1]:.1f} L {pg(-6, 140)[0]:.1f} {pg(-6, 140)[1]:.1f} L {pg(-16, 20)[0]:.1f} {pg(-16, 20)[1]:.1f} C {pg(-20, -40)[0]:.1f} {pg(-20, -40)[1]:.1f} {pg(-20, -88)[0]:.1f} {pg(-20, -88)[1]:.1f} {pg(0, -92)[0]:.1f} {pg(0, -92)[1]:.1f} Z"
    s += f'<path d="{fus}" fill="#dfe5ec" stroke="{INK}" stroke-width="3"/>\n'
    s += line(*pg(-32, -95), *pg(32, -95), "#64748b", 5)
    return s, pg


def q2763():
    s = header("ADVERSE AILERON YAW")
    s += f'<rect x="40" y="142" width="710" height="444" rx="12" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2"/>\n'
    s += t(60, 174, "PILOT ROLLS LEFT (VIEW FROM ABOVE)", 17, 800, INK, "start")
    cx, cy, sc = 395, 372, 1.38
    g_, pg = top_plane(cx, cy, sc)
    s += g_
    # ailerons: left up, right down
    s += poly([pg(-150, 10), pg(-95, 10), pg(-95, 22), pg(-150, 22)], "#cbd5e1", INK, 2.5)
    s += poly([pg(95, 10), pg(150, 10), pg(150, 22), pg(95, 22)], GOLD, INK, 2.5)
    l = pg(-122, 16)
    r = pg(122, 16)
    s += t(l[0], l[1] + 50, "AILERON UP", 14, 800, INK)
    s += t(l[0], l[1] + 68, "less lift, less drag", 13, 400, BODY)
    s += t(r[0], r[1] + 50, "AILERON DOWN", 14, 800, GOLD_DARK)
    s += t(r[0], r[1] + 68, "more lift, MORE DRAG", 13, 800, RED)
    # drag arrows (rearward = down the page)
    s += line(l[0], l[1] - 58, l[0], l[1] - 34, RED, 4, "aRedS")
    s += line(r[0], r[1] - 88, r[0], r[1] - 34, RED, 7, "aRed")
    s += t(r[0] + 14, r[1] - 76, "DRAG", 14, 800, RED, "start")
    # yaw arrow at the nose
    n = pg(0, -92)
    s += f'<path d="M {n[0] - 40:.1f} {n[1] - 12:.1f} Q {n[0]:.1f} {n[1] - 44:.1f} {n[0] + 44:.1f} {n[1] - 14:.1f}" fill="none" stroke="{GOLD_DARK}" stroke-width="5" marker-end="url(#aDark)"/>\n'
    s += t(n[0] + 60, n[1] - 26, "NOSE YAWS RIGHT", 16, 800, GOLD_DARK, "start")
    s += t(n[0] - 60, n[1] - 26, "ROLL LEFT", 16, 800, INK, "end")
    s += fact_column([
        ("DOWN-GOING AILERON", ["Raises lift on that wing,", "and with it induced drag."]),
        ("NOSE YAWS OPPOSITE", ["The extra drag swings the", "nose away from the roll:", "roll left, yaw right."]),
        ("CORRECTION", ["Co-ordinated rudder; designs", "use differential or Frise", "ailerons to reduce it."]),
    ])
    s += footer("Rolling left without rudder, adverse aileron yaw initially swings the nose right.")
    return s


def q2764():
    s = header("FRISE AILERON")
    s = two_panels(s, ["UP-GOING AILERON (WING GOING DOWN)", "DOWN-GOING AILERON (WING GOING UP)"], 0)
    C = 500
    fu, fl = naca(0.0, 0.0, 0.14, 50)
    fc = 0.27
    ail = [(x * fc, y * fc) for x, y in fu] + [(x * fc, y * fc) for x, y in reversed(fl)]
    le = (0.735, -0.012)
    hinge = (le[0] + 0.05, le[1] - 0.012)
    for i, deg in enumerate((-22, 20)):
        py = 142 + i * 226
        X0, Y0 = 120, py + 108
        P = lambda pts, X0=X0, Y0=Y0: to_px(pts, X0, Y0, C)
        a = [rot((le[0] + x, le[1] + y), hinge, deg) for x, y in ail]
        s += poly(P(a), GOLD if i == 0 else MOVE, INK, 3)
        up_, lo_ = CAMB_UP, CAMB_LO
        main_up = seg(up_, 0, 0.77)
        main_lo = list(reversed(seg(lo_, 0, 0.70)))
        pu, pl = P(main_up), P(main_lo)
        ctrl = P([(0.715, 0.005)])[0]
        d = "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in pu)
        d += f" Q {ctrl[0]:.1f},{ctrl[1]:.1f} {pl[0][0]:.1f},{pl[0][1]:.1f}" + "".join(f" L {x:.1f},{y:.1f}" for x, y in pl[1:]) + " Z"
        s += f'<path d="{d}" fill="#b8c0ca" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>\n'
        hp = P([hinge])[0]
        s += f'<circle cx="{hp[0]:.1f}" cy="{hp[1]:.1f}" r="5" fill="{INK}"/>\n'
        for yy in (-40, 0, 40):
            s += line(52, Y0 + yy, 92, Y0 + yy, BLUE, 3.5, "aBlue")
        nose = P([rot(le, hinge, deg)])[0]
        if i == 0:
            s += t(nose[0] - 70, nose[1] + 70, "NOSE PROJECTS BELOW", 14, 800, RED, "middle")
            s += t(nose[0] - 70, nose[1] + 86, "THE WING: EXTRA DRAG", 14, 800, RED, "middle")
            s += line(nose[0] - 30, nose[1] + 56, nose[0] - 4, nose[1] + 10, RED, 2.5, "aRedS")
            s += t(hp[0] + 30, hp[1] - 58, "OFFSET HINGE", 14, 800, INK, "start")
            s += line(hp[0] + 28, hp[1] - 54, hp[0] + 4, hp[1] - 6, INK, 2, "aDark")
        else:
            s += t(nose[0] - 70, nose[1] + 70, "NOSE STAYS INSIDE", 14, 800, "#15803d", "middle")
            s += t(nose[0] - 70, nose[1] + 86, "THE WING CONTOUR", 14, 800, "#15803d", "middle")
            s += line(nose[0] - 34, nose[1] + 56, nose[0] - 4, nose[1] + 8, "#15803d", 2.5, "aDark")
    s += fact_column([
        ("OFFSET HINGE", ["The hinge is set behind the", "aileron's leading edge."]),
        ("DRAG ON THE DOWN WING", ["The raised aileron's nose", "projects into the airflow", "below the wing."]),
        ("REDUCES ADVERSE YAW", ["That drag balances the extra", "drag of the down-going", "aileron on the other wing."]),
    ])
    s += footer("A Frise aileron's raised nose projects below the wing, creating drag that opposes adverse yaw.")
    return s


BATCHES = {
    "airframes-batch-1": {
        "q2421-semi-monocoque-fuselage.svg": q2421,
        "q2424-torsion-load.svg": q2424,
        "q2425-split-flap.svg": lambda: flaps("SPLIT FLAP"),
        "q2426-balance-tab.svg": q2426,
        "q2427-adjustable-trim-tab.svg": q2427,
    },
    "airframes-batch-2": {
        "q2429-truss-longerons.svg": q2429,
        "q2443-slotted-flap.svg": lambda: flaps("SLOTTED FLAP"),
        "q2446-fowler-flap.svg": lambda: flaps("FOWLER FLAP"),
        "q2451-plain-flap.svg": lambda: flaps("PLAIN FLAP"),
        "q2457-monocoque-structure.svg": q2457,
    },
    "airframes-batch-3": {
        "q2440-wing-main-spar.svg": lambda: wing("MAIN SPAR"),
        "q2461-wing-ribs.svg": lambda: wing("RIBS"),
        "q2430-wing-rear-spar.svg": lambda: wing("REAR SPAR"),
        "q2462-servo-tab.svg": q2462,
        "q2463-anti-balance-tab.svg": q2463,
    },
    "airframes-batch-4": {
        "q2465-newton-first-law.svg": lambda: newton("FIRST"),
        "q2433-newton-second-law.svg": lambda: newton("SECOND"),
        "q2447-newton-third-law.svg": lambda: newton("THIRD"),
        "q2432-cg-too-far-aft.svg": q2432,
        "q2467-power-reduction-nose-drop.svg": q2467,
    },
    "airframes-batch-5": {
        "q2759-t-tail.svg": q2759,
        "q2743-trim-tab-purpose.svg": q2743,
        "q2434-leading-edge-slats.svg": q2434,
    },
    "airframes-batch-6": {
        "q2436-stall-warning-vane.svg": q2436,
        "q2439-centre-of-pressure-movement.svg": q2439,
        "q2763-adverse-aileron-yaw.svg": q2763,
        "q2764-frise-aileron.svg": q2764,
    },
}

if __name__ == "__main__":
    import sys
    for batch in sys.argv[1:] or BATCHES:
        out = OUT.parent / batch
        out.mkdir(parents=True, exist_ok=True)
        for name, fn in BATCHES[batch].items():
            (out / name).write_text(fn(), encoding="utf-8")
            print("wrote", batch, name)
