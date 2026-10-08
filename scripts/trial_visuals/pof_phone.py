"""Principles of Flight explanation pictures, phone-first (docs/EXPLANATION_ILLUSTRATION_STANDARD.md).

Each picture redraws the textbook figure the question already used, with the same layout, at phone size. The
aerofoil is a NACA 2412 section from scene.aerofoil, not drawn freehand.
"""
from common import Registry
from kit import template

from scene import (COMMON_DEFS, GOLD, INK, NAVY_BLUE, RED, TXT_L, TXT_M, W, aerofoil, angle_arc, chord_point,
                   compass_xy, defs, head, label, path, stack, stack_height)

R = Registry("principles-of-flight", "/explanation-images/principles-of-flight/refined-batch-2")

VEC_W = 7                # force arrows
LINE_W = 4               # reference lines (chord, relative wind)
from scene import lg

POF_DEFS = (lg("pf_metal", [(0, "#e2e8f0"), (0.5, "#94a3b8"), (1, "#cbd5e1")]), head("pf_navy", NAVY_BLUE, 34), head("pf_gold", GOLD, 34), head("pf_ink", INK, 28), head("pf_red", RED, 26), head("pf_green", "#047857", 34))


def picture(panels):
    body, _ = stack(panels)
    return defs(*COMMON_DEFS, *POF_DEFS) + body


def arrow(a, b, color, mid, w=VEC_W):
    d = f"M {a[0]:.1f},{a[1]:.1f} L {b[0]:.1f},{b[1]:.1f}"
    return path(d, "none", "#ffffff", w + 5, ' stroke-opacity="0.9"') + path(d, "none", color, w, f' marker-end="url(#{mid})"')


def dashed(a, b, color=INK, w=3, dash="14 10"):
    return path(f"M {a[0]:.1f},{a[1]:.1f} L {b[0]:.1f},{b[1]:.1f}", "none", color, w, f' stroke-dasharray="{dash}"')


# ------------------------------------------------------------------ centre of pressure: lift, drag and the resultant

CP_H = 700
LE, CHORD, AOA = (270, 400), 560, 15     # leading edge, chord, angle of attack


def cp_panel():
    def draw(w, h):
        s = f'<rect x="0" y="0" width="{w}" height="{h}" fill="#ffffff"/>'
        te = chord_point(*LE, CHORD, AOA, 1.0)
        cp = chord_point(*LE, CHORD, AOA, 0.28)
        # relative wind: horizontal, meeting the leading edge
        s += arrow((25, LE[1]), (LE[0] - 18, LE[1]), INK, "pf_ink", LINE_W)
        s += aerofoil(*LE, CHORD, AOA)
        # chord line, dashed through the section and beyond both edges
        s += dashed(chord_point(*LE, CHORD, AOA, -0.42), chord_point(*LE, CHORD, AOA, 1.15), "#475569", 3, "18 10")
        # the angle of attack: between the relative wind and the chord line, at the leading edge
        s += angle_arc(*LE, 185, 270, 270 + AOA, RED, 6)
        # lift (square to the relative wind), drag (along it) and their resultant, all from the centre of pressure
        lift, drag = (cp[0], cp[1] - 290), (cp[0] + 160, cp[1])
        res = (drag[0], lift[1])
        s += dashed(lift, res) + dashed(drag, res)
        s += arrow(cp, lift, NAVY_BLUE, "pf_navy") + arrow(cp, drag, NAVY_BLUE, "pf_navy")
        s += arrow(cp, res, GOLD, "pf_gold")
        s += f'<circle cx="{cp[0]:.1f}" cy="{cp[1]:.1f}" r="11" fill="#ffffff" stroke="{INK}" stroke-width="5"/>'
        s += label(lift[0], lift[1] - 22, "Lift", TXT_L, NAVY_BLUE, "middle")
        s += label(res[0] + 22, res[1] + 20, "Resultant\nforce", TXT_L, "#b45309")
        s += label(drag[0] + 50, drag[1] + 12, "Drag", TXT_L, NAVY_BLUE)
        s += label(cp[0] - 50, cp[1] + 112, "Centre of pressure", TXT_L, INK, "middle")
        s += label(25, 300, "Angle of attack", TXT_M, RED)
        s += label(25, LE[1] + 60, "Relative wind", TXT_M, INK)
        s += label(te[0] - 175, te[1] + 55, "Chord line", TXT_M, "#475569")
        return s
    return dict(h=CP_H, sky="white", draw=draw, caption="LIFT ACTS AT THE CENTRE OF PRESSURE", color=NAVY_BLUE)


@R.add(1142, "centre-of-pressure-v1", "Centre of Pressure",
       template("TOTAL LIFT ACTS THROUGH THE CENTRE OF PRESSURE",
                "THE POINT ON THE CHORD WHERE THE RESULTANT FORCE ACTS",
                [("Lift", "Square to the relative wind"),
                 ("Drag", "Along the relative wind"),
                 ("Angle of attack", "Between the chord line and the relative wind")]),
       h=stack_height([CP_H]), w=W)
def _():
    return picture([cp_panel()])


# ------------------------------------------------------------------ shared pieces for the aerofoil pictures

import math

import numpy as np

import flow
from aircraft import aircraft_front
from scene import BLUE, aerofoil_pts

CELL_FILL, CELL_EDGE = "#f8fafc", "#cbd5e1"
SECTION = "#1e40af"                     # aerofoil in the airflow pictures (the textbook's dark blue)
SECTION_LIGHT = "#fcd9a8"               # aerofoil in the line drawings (the textbook's tan)


def grid(cells, cols, cell_w, cell_h, gap_x=40, gap_y=36, x0=0, y0=0):
    """Lay out cell draw functions draw(x, y, w, h) in rows."""
    s = ""
    for i, fn in enumerate(cells):
        r, c = divmod(i, cols)
        s += fn(x0 + c * (cell_w + gap_x), y0 + r * (cell_h + gap_y), cell_w, cell_h)
    return s


def polyline(pts, color, w, extra=""):
    return path("M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in pts), "none", color, w, extra)


def section_frame(n=60):
    """NACA 2412 outline in chord units: (u along the chord from the leading edge, v up), upper then lower."""
    return [(x, -y) for x, y in aerofoil_pts(0, 0, 1, 0, n=n)]


def place(pts, le, chord, deg):
    """Chord-frame points (u, v up) to canvas: leading edge at `le`, nose up by `deg` (trailing edge drops)."""
    a = math.radians(deg)
    return [(le[0] + chord * (u * math.cos(a) + v * math.sin(a)), le[1] + chord * (u * math.sin(a) - v * math.cos(a)))
            for u, v in pts]


def closed(pts, fill, stroke="#334155", w=3):
    return path("M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z", fill, stroke, w)


def curl(cx, cy, r, turns=1.3, color="#334155", w=2.5):
    """A small eddy: a spiral opening clockwise from its centre."""
    pts = []
    for i in range(41):
        t = i / 40 * turns * 2 * math.pi
        rr = r * (0.25 + 0.75 * i / 40)
        pts.append((cx + rr * math.cos(t), cy + rr * math.sin(t)))
    return polyline(pts, color, w)


# ------------------------------------------------------------------ #2 angle of attack from cruise to the stall

AOA_STEPS = [(4, "1 Normal cruise"), (8, "2 Cruise climb"), (10, "3 Climb"), (14, "4 Slow flight"),
             (16, "5 Min controllable speed"), (20, "6 Stall")]
SEPARATION = {14: 0.72, 16: 0.45, 20: 0.12}       # where the flow leaves the upper surface (fraction of chord)


def flow_cell(alpha, caption):
    def draw(x, y, w, h):
        box_h = h - 52
        k = w / 7.4
        X0, Y0 = x + w / 2 + 6, y + box_h / 2 + 4

        def cv(p):
            return X0 + p.real * k, Y0 - p.imag * k

        s = (f'<rect x="{x}" y="{y}" width="{w}" height="{box_h}" rx="10" fill="{CELL_FILL}" stroke="{CELL_EDGE}" '
             f'stroke-width="2"/>')
        s += f'<clipPath id="fc{alpha}"><rect x="{x}" y="{y}" width="{w}" height="{box_h}" rx="10"/></clipPath>'
        s += f'<g clip-path="url(#fc{alpha})">'
        le, te = flow.chord_ends(alpha)
        outline = flow.aerofoil_outline(alpha)
        sep = SEPARATION.get(alpha)
        offs = [o for o in np.arange(-2.1, 2.2, 0.3)]
        if sep is not None:
            sp = le + (te - le) * sep                               # separation point on the chord
            upper = outline[np.argmin(np.abs(outline - (sp + 0.25j)))]
            ys = upper.imag + 0.04
        for line_ in flow.streamlines(alpha, offs, extent=(-3.7, 3.7, -2.4, 2.4)):
            if line_[-1].real - line_[0].real < 6.4:                # only lines crossing the whole box
                continue
            pts = [cv(p) for p in line_[::3]]
            if sep is not None and line_.imag.max() > upper.imag - 0.05 and line_[len(line_) // 2].imag > 0.05:
                # flow above a stalled wing cannot follow the surface past the separation point
                pts = [(px, min(py, Y0 - (ys + 0.06 * max(0.0, (px - X0) / k - sp.real)) * k)
                        if px > X0 + sp.real * k else py) for px, py in pts]
            s += polyline(pts, "#475569", 2.4)
        if sep is not None:
            # eddies in the dead air between the surface and the separated flow, growing downstream
            n = {14: 3, 16: 4, 20: 5}[alpha]
            for i in range(n):
                f = (i + 0.5) / n
                px = sp.real + 0.25 + f * (te.real + 1.1 - sp.real - 0.25)
                near = outline[(outline.imag > -0.6)]
                below = near[np.argmin(np.abs(near.real - px))].imag if px < te.real else te.imag
                top = ys + 0.06 * max(0.0, px - sp.real)
                gap = max(0.12, top - below)
                s += curl(X0 + px * k, Y0 - (below + gap * 0.5) * k, min(gap * k * 0.42, 22))
        s += closed([cv(p) for p in outline], SECTION, "#0f172a", 2)
        s += "</g>"
        # the flight path (red, the way the wing is going) and the chord line carried forward
        tx, ty = cv(te)
        s += arrow((x + w - 8, ty), (x + 26, ty), RED, "pf_red", 4)
        lx, ly = cv(le)
        fx, fy = lx + (lx - tx) * 0.22, ly + (ly - ty) * 0.22
        s += dashed((tx, ty), (fx, fy), INK, 3, "12 8")
        r = math.hypot(fx - tx, fy - ty) * 0.97
        s += angle_arc(tx, ty, r, 270, 270 + alpha, INK, 4)
        s += label(x + 4, min(fy, ty) - 14, f"{alpha}°", TXT_M, INK)
        s += label(x + w / 2, y + h - 10, caption, 32, INK, "middle")
        return s
    return draw


def aoa_stall_panel():
    def draw(w, h):
        s = f'<rect x="0" y="0" width="{w}" height="{h}" fill="#ffffff"/>'
        return s + grid([flow_cell(a, c) for a, c in AOA_STEPS], 2, 420, 290, gap_x=24, gap_y=26, x0=18, y0=22)
    return dict(h=22 + 3 * 290 + 2 * 26 + 18, sky="white", draw=draw,
                caption="THE WING STALLS AT THE CRITICAL ANGLE", color=RED)


@R.add(1205, "aoa-to-stall-v1", "Angle of Attack to the Stall",
       template("THE WING STALLS AT THE SAME ANGLE OF ATTACK WHATEVER ITS WEIGHT",
                "A HEAVIER AEROPLANE REACHES THAT ANGLE AT A HIGHER SPEED",
                [("Stall", "Airflow breaks away at the critical angle (about 16°)"),
                 ("More weight", "Higher stall speed, same stalling angle")]),
       h=stack_height([22 + 3 * 290 + 2 * 26 + 18]), w=W)
def _():
    return picture([aoa_stall_panel()])


# ------------------------------------------------------------------ #12 angle of incidence

INC_H = 560


def incidence_panel():
    def draw(w, h):
        s = f'<rect x="0" y="0" width="{w}" height="{h}" fill="#ffffff"/>'
        le, chord, inc = (150, 250), 620, 8          # incidence drawn larger than the real 2-4° so it can be seen
        te = chord_point(*le, chord, inc, 1.0)
        s += closed(place(section_frame(), le, chord, inc), SECTION_LIGHT, "#334155", 4)
        s += dashed(chord_point(*le, chord, inc, -0.18), chord_point(*le, chord, inc, 1.08), INK, 3, "16 10")
        # the line parallel to the longitudinal axis, through the trailing edge
        s += path(f"M 40,{te[1]:.1f} L {w - 30},{te[1]:.1f}", "none", NAVY_BLUE, 5)
        s += angle_arc(*te, chord + 20, 270, 270 + inc, RED, 6)
        s += label(le[0] - 40, le[1] - 50, "Leading edge", TXT_M, INK)
        s += label(te[0] + 10, te[1] - 70, "Trailing\nedge", TXT_M, INK, "middle")
        s += label(470, le[1] - 50, "Chord line", TXT_M, "#475569")
        s += label(30, te[1] + 70, "Angle of incidence", TXT_L, RED)
        s += label(w / 2, te[1] + 135, "Line parallel to the longitudinal axis", TXT_M, NAVY_BLUE, "middle")
        return s
    return dict(h=INC_H, sky="white", draw=draw, caption="CHORD LINE TO LONGITUDINAL AXIS", color=RED)


@R.add(1152, "angle-of-incidence-v1", "Angle of Incidence",
       template("ANGLE OF INCIDENCE: CHORD LINE TO LONGITUDINAL AXIS",
                "FIXED WHEN THE WING IS BUILT ONTO THE FUSELAGE",
                [("Angle of incidence", "Chord line to the longitudinal axis: fixed"),
                 ("Angle of attack", "Chord line to the relative airflow: changes in flight")]),
       h=stack_height([INC_H]), w=W)
def _():
    return picture([incidence_panel()])


# ------------------------------------------------------------------ #14 lift acts at right angles to the relative airflow

LIFT_H = 480


def lift_front_panel():
    def draw(w, h):
        s = f'<rect x="0" y="0" width="{w}" height="{h}" fill="#ffffff"/>'
        cx, cy = 450, 300
        s += path(f"M 30,{cy + 120} L {w - 30},{cy + 120}", "none", "#94a3b8", 4)
        s += aircraft_front(cx, cy, 760)
        s += arrow((cx, cy - 20), (cx, 70), NAVY_BLUE, "pf_navy", 8)
        s += angle_arc(cx, cy + 40, 120, 270, 360, RED, 5)
        s += label(cx + 30, 95, "Lift", TXT_L, NAVY_BLUE)
        s += label(40, 200, "90° to the wingspan", TXT_M, RED)
        return s
    return dict(h=LIFT_H, sky="white", draw=draw, caption="LIFT: AT 90° TO THE WINGSPAN", color=NAVY_BLUE)


def lift_section_panel():
    def draw(w, h):
        s = f'<rect x="0" y="0" width="{w}" height="{h}" fill="#ffffff"/>'
        le, chord, aoa = (250, 300), 540, 14
        cp = chord_point(*le, chord, aoa, 0.3)
        s += arrow((25, le[1]), (le[0] - 16, le[1]), INK, "pf_ink", 4)
        s += closed(place(section_frame(), le, chord, aoa), SECTION_LIGHT, "#334155", 4)
        s += arrow(cp, (cp[0], cp[1] - 250), NAVY_BLUE, "pf_navy")
        s += arrow(cp, (cp[0] + 200, cp[1]), NAVY_BLUE, "pf_navy")
        # right-angle mark between lift and the relative airflow
        s += path(f"M {cp[0]:.1f},{cp[1] - 40:.1f} L {cp[0] + 40:.1f},{cp[1] - 40:.1f} L {cp[0] + 40:.1f},{cp[1]:.1f}",
                  "none", RED, 4)
        s += label(cp[0] + 20, cp[1] - 215, "Lift", TXT_L, NAVY_BLUE)
        s += label(cp[0] + 215, cp[1] + 12, "Drag", TXT_L, NAVY_BLUE)
        s += label(25, le[1] + 60, "Relative airflow", TXT_M, INK)
        return s
    return dict(h=LIFT_H, sky="white", draw=draw, caption="AND AT 90° TO THE RELATIVE AIRFLOW", color=NAVY_BLUE)


@R.add(1113, "lift-perpendicular-v1", "Lift Acts at 90° to the Relative Airflow",
       template("LIFT ACTS AT 90° TO THE RELATIVE AIRFLOW",
                "AND AT 90° TO THE WINGSPAN",
                [("Drag", "Along the relative airflow"),
                 ("In a bank", "Lift tilts with the wings")]),
       h=stack_height([LIFT_H, LIFT_H]), w=W)
def _():
    return picture([lift_front_panel(), lift_section_panel()])


# ------------------------------------------------------------------ #11 flap types

FLAP_HINGE = 0.72                       # flaps take the aft 28% of the chord


def flap_parts(kind):
    """Main section and flap outlines in chord units (u, v up)."""
    sec = section_frame(80)
    n = len(sec) // 2 + 1
    upper, lower = sec[:n][::-1], sec[n - 1:]              # both leading edge -> trailing edge
    def cut(line, keep_front):
        return [p for p in line if (p[0] <= FLAP_HINGE) == keep_front]
    hinge_v = np.interp(FLAP_HINGE, [p[0] for p in lower], [p[1] for p in lower])

    def turn(pts, about, deg, shift=(0.0, 0.0)):
        a = math.radians(-deg)
        return [(about[0] + shift[0] + (u - about[0]) * math.cos(a) - (v - about[1]) * math.sin(a),
                 about[1] + shift[1] + (u - about[0]) * math.sin(a) + (v - about[1]) * math.cos(a)) for u, v in pts]

    main = cut(upper, True) + cut(lower, True)[::-1]
    # the flap: its own rounded nose (a half circle the depth of the section at the hinge) and the aft surfaces
    top_v = np.interp(FLAP_HINGE, [p[0] for p in upper], [p[1] for p in upper])
    mid, rad = (FLAP_HINGE, (top_v + hinge_v) / 2), (top_v - hinge_v) / 2
    nose = [(mid[0] - rad * math.sin(t), mid[1] + rad * math.cos(t)) for t in np.linspace(0, math.pi, 14)]
    shape = [(u, v) for u, v in nose] + cut(lower, False) + cut(upper, False)[::-1]
    if kind == "Plain":
        return [turn(shape, mid, 25), main]
    if kind == "Split":
        plate = [(FLAP_HINGE - 0.04, hinge_v), (1.0, hinge_v * 0.2), (1.0, hinge_v * 0.2 - 0.012),
                 (FLAP_HINGE - 0.04, hinge_v - 0.012)]
        return [upper[:] + [(1.0, 0.0)] + lower[::-1], turn(plate, (FLAP_HINGE - 0.04, hinge_v), 35)]
    if kind == "Fowler":
        return [main, turn(shape, mid, 12, (0.13, -0.035))]
    return [main, turn(shape, mid, 25, (0.03, -0.022))]                  # slotted


def flaps_panel():
    def draw(w, h):
        s = f'<rect x="0" y="0" width="{w}" height="{h}" fill="#ffffff"/>'
        for i, kind in enumerate(["Plain", "Split", "Fowler", "Slotted"]):
            y = 95 + i * 190
            hi = kind == "Fowler"
            for part in flap_parts(kind):
                s += closed(place(part, (300, y), 470, 0), "#bfdbfe" if hi else SECTION_LIGHT, "#334155", 3)
            s += label(40, y + 14, kind, TXT_L, NAVY_BLUE if hi else INK)
        return s
    return dict(h=820, sky="white", draw=draw, caption="FOWLER: SLIDES BACK, ADDING WING AREA", color=NAVY_BLUE)


@R.add(1201, "flap-types-v1", "Types of Flap",
       template("FOWLER FLAPS INCREASE THE WING AREA",
                "THEY SLIDE BACK ON TRACKS, THEN DOWN",
                [("Plain", "Hinged trailing edge: more camber"),
                 ("Split", "Lower surface only: lots of drag"),
                 ("Slotted", "A slot re-energises the airflow over the flap")]),
       h=stack_height([820]), w=W)
def _():
    return picture([flaps_panel()])


# ------------------------------------------------------------------ #13 angle of attack is measured from the flight path

AOA_CASES = [(20, 0, "Level, 20°"), (10, 0, "Level, 10°"), (5, 0, "Level, 5°"),
             (10, -14, "Descending, 10°"), (10, 0, "Level, 10°"), (10, 14, "Climbing, 10°")]


def aoa_cell(aoa, path_deg, caption):
    def draw(x, y, w, h):
        chord = w * 0.7
        cy = y + h * 0.52
        a_path = math.radians(path_deg)
        te = (x + w * 0.88, cy + chord * 0.5 * math.sin(a_path))
        # the flight path: a broad arrow pointing the way the wing is going
        dx, dy = -math.cos(a_path), -math.sin(a_path)
        tail, tip = te, (te[0] + dx * w * 0.86, te[1] + dy * w * 0.86)
        s = path(f"M {tail[0]:.1f},{tail[1]:.1f} L {tip[0]:.1f},{tip[1]:.1f}", "none", "#93c5fd", 16)
        s += f'<path d="M {tip[0] + dx * 24:.1f},{tip[1] + dy * 24:.1f} l {-dy * 20 - dx * 34:.1f},{dx * 20 - dy * 34:.1f} l {2 * dy * 20:.1f},{-2 * dx * 20:.1f} Z" fill="#93c5fd"/>'
        # the section: chord at aoa above the flight path, trailing edge on the path
        nose_up = aoa + path_deg
        le = (te[0] - chord * math.cos(math.radians(nose_up)), te[1] - chord * math.sin(math.radians(nose_up)))
        wedge = (te[0] - chord * math.cos(a_path), te[1] - chord * math.sin(a_path))
        s += f'<path d="M {te[0]:.1f},{te[1]:.1f} L {le[0]:.1f},{le[1]:.1f} L {wedge[0]:.1f},{wedge[1]:.1f} Z" fill="#cbd5e1"/>'
        s += closed(place(section_frame(), le, chord, -nose_up if False else nose_up), SECTION_LIGHT, "#334155", 3)
        s += dashed(te, (le[0] - (te[0] - le[0]) * 0.12, le[1] - (te[1] - le[1]) * 0.12), INK, 3, "10 7")
        s += label(x + w / 2, y + h - 6, caption, 32, INK, "middle")
        return s
    return draw


def aoa_examples_panel():
    def draw(w, h):
        s = f'<rect x="0" y="0" width="{w}" height="{h}" fill="#ffffff"/>'
        return s + grid([aoa_cell(*c) for c in AOA_CASES], 2, 420, 250, gap_x=24, gap_y=24, x0=18, y0=10)
    return dict(h=10 + 3 * 250 + 2 * 24 + 10, sky="white", draw=draw, caption="CHORD LINE TO THE RELATIVE AIRFLOW",
                color=RED)


@R.add(1300, "aoa-examples-v1", "Angle of Attack",
       template("ANGLE OF ATTACK: CHORD LINE TO THE RELATIVE AIRFLOW",
                "MEASURED FROM THE FLIGHT PATH, NOT FROM THE HORIZON",
                [("Same angle", "Can be flown climbing, level or descending"),
                 ("Relative airflow", "Opposite to the flight path")]),
       h=stack_height([10 + 3 * 250 + 2 * 24 + 10]), w=W)
def _():
    return picture([aoa_examples_panel()])


# ------------------------------------------------------------------ charts: drawn from the formulas, not traced

PLOT = dict(x0=150, x1=760, y0=60, y1=600)          # plot area inside the panel


def chart_frame(xticks, yticks, xlab, ylab, xmap, ymap, grid_color="#dbeafe", rticks=None, rmap=None, rlab=None):
    p = PLOT
    s = f'<rect x="{p["x0"]}" y="{p["y0"]}" width="{p["x1"] - p["x0"]}" height="{p["y1"] - p["y0"]}" fill="#f8fbff" stroke="#94a3b8" stroke-width="2"/>'
    for v in xticks:
        x = xmap(v)
        s += path(f"M {x:.1f},{p['y0']} L {x:.1f},{p['y1']}", "none", grid_color, 2)
        s += label(x, p["y1"] + 52, str(v), 32, INK, "middle", halo=None)
    for v in yticks:
        y = ymap(v)
        s += path(f"M {p['x0']},{y:.1f} L {p['x1']},{y:.1f}", "none", grid_color, 2)
        s += label(p["x0"] - 12, y + 11, str(v), 32, INK, "end", halo=None)
    if rticks:
        for v in rticks:
            s += label(p["x1"] + 12, rmap(v) + 11, str(v), 32, INK, halo=None)
    s += label((p["x0"] + p["x1"]) / 2, p["y1"] + 100, xlab, TXT_M, INK, "middle", halo=None)
    s += f'<g transform="rotate(-90 40 {(p["y0"] + p["y1"]) / 2})">' + label(40, (p["y0"] + p["y1"]) / 2 + 10, ylab, TXT_M, INK, "middle", halo=None) + "</g>"
    if rlab:
        s += f'<g transform="rotate(90 868 {(p["y0"] + p["y1"]) / 2})">' + label(868, (p["y0"] + p["y1"]) / 2 + 10, rlab, TXT_M, INK, "middle", halo=None) + "</g>"
    return s


# #9 load factor and stall speed against bank (PPL PoF-1)

def load_factor_panel(bank, caption):
    xmap = lambda b: PLOT["x0"] + b / 90 * (PLOT["x1"] - PLOT["x0"])                      # noqa: E731
    ymap = lambda pct: PLOT["y1"] - pct / 100 * (PLOT["y1"] - PLOT["y0"])                  # noqa: E731
    gmap = lambda n: ymap((n - 1) / 12 * 100)                                              # 1 G .. 13 G on the right  # noqa: E731

    def draw(w, h):
        s = f'<rect x="0" y="0" width="{w}" height="{h}" fill="#ffffff"/>'
        s += chart_frame(range(0, 91, 10), range(0, 101, 20), "Bank angle, degrees", "Stall speed increase %",
                         xmap, ymap, rticks=range(1, 14, 2), rmap=gmap, rlab="Load factor, G")
        s += f'<clipPath id="lfc"><rect x="{PLOT["x0"]}" y="{PLOT["y0"]}" width="{PLOT["x1"] - PLOT["x0"]}" height="{PLOT["y1"] - PLOT["y0"]}"/></clipPath><g clip-path="url(#lfc)">'
        bs = np.linspace(0, 89.3, 300)
        n = 1 / np.cos(np.radians(bs))
        s += polyline([(xmap(b), gmap(v)) for b, v in zip(bs, n)], NAVY_BLUE, 6)
        s += polyline([(xmap(b), ymap((math.sqrt(v) - 1) * 100)) for b, v in zip(bs, n)], RED, 6)
        s += "</g>"
        s += path(f"M {PLOT['x0'] + 24},{PLOT['y0'] + 40} l 50,0", "none", NAVY_BLUE, 6)
        s += label(PLOT["x0"] + 86, PLOT["y0"] + 52, "Load factor", TXT_M, NAVY_BLUE)
        s += path(f"M {PLOT['x0'] + 24},{PLOT['y0'] + 92} l 50,0", "none", RED, 6)
        s += label(PLOT["x0"] + 86, PLOT["y0"] + 104, "Stall speed", TXT_M, RED)
        # the reading for this question
        nb = 1 / math.cos(math.radians(bank))
        px, py = xmap(bank), gmap(nb)
        s += dashed((px, PLOT["y1"]), (px, py), GOLD, 5, "12 8") + dashed((px, py), (PLOT["x1"], py), GOLD, 5, "12 8")
        s += f'<circle cx="{px:.1f}" cy="{py:.1f}" r="10" fill="#ffffff" stroke="{GOLD}" stroke-width="5"/>'
        s += label(px + 16, py - 18, f"{nb:.2f} G".replace(".00", ".0"), TXT_L, "#b45309")
        return s
    return dict(h=PLOT["y1"] + 130, sky="white", draw=draw, caption=caption, color="#b45309")


@R.add(-3, "load-factor-60deg-v1", "Load Factor and Bank Angle",
       template("60° OF BANK: LOAD FACTOR 2 G", "LOAD FACTOR = 1 ÷ COS (BANK ANGLE)",
                [("30°", "1.15 G"), ("45°", "1.41 G"), ("60°", "2 G, stall speed +41%")]),
       h=stack_height([PLOT["y1"] + 130]), w=W)
def _():
    return picture([load_factor_panel(60, "60° OF BANK: 2 G")])


@R.add(-5, "load-factor-50deg-v1", "Load Factor and Bank Angle",
       template("50° OF BANK: LOAD FACTOR ABOUT 1.56 G", "4,600 LB × 1.56 ≈ 7,160 LB",
                [("Load factor", "1 ÷ cos (bank angle)"), ("Structure carries", "Weight × load factor")]),
       h=stack_height([PLOT["y1"] + 130]), w=W)
def _():
    return picture([load_factor_panel(50, "50° OF BANK: 1.56 G")])


# #19 drag against speed: A induced, B parasite, C total, D minimum drag

def drag_panel():
    vs = np.linspace(0.62, 2.3, 200)                   # speed in units of the minimum drag speed
    induced, parasite = 1 / vs ** 2, vs ** 2
    total = induced + parasite
    xmap = lambda v: PLOT["x0"] + (v - 0.45) / (2.35 - 0.45) * (PLOT["x1"] - PLOT["x0"])  # noqa: E731
    ymap = lambda d: PLOT["y1"] - d / 5.6 * (PLOT["y1"] - PLOT["y0"])                     # noqa: E731

    def draw(w, h):
        s = f'<rect x="0" y="0" width="{w}" height="{h}" fill="#ffffff"/>'
        p = PLOT
        s += f'<rect x="{p["x0"]}" y="{p["y0"]}" width="{p["x1"] - p["x0"]}" height="{p["y1"] - p["y0"]}" fill="#f8fbff" stroke="#94a3b8" stroke-width="2"/>'
        s += label((p["x0"] + p["x1"]) / 2, p["y1"] + 50, "Speed →", TXT_M, INK, "middle", halo=None)
        s += f'<g transform="rotate(-90 90 {(p["y0"] + p["y1"]) / 2})">' + label(90, (p["y0"] + p["y1"]) / 2 + 10, "Drag →", TXT_M, INK, "middle", halo=None) + "</g>"
        s += f'<clipPath id="dc"><rect x="{p["x0"]}" y="{p["y0"]}" width="{p["x1"] - p["x0"]}" height="{p["y1"] - p["y0"]}"/></clipPath><g clip-path="url(#dc)">'
        # the stall: no flight at lower speeds
        xs = xmap(0.62)
        s += f'<rect x="{p["x0"]}" y="{p["y0"]}" width="{xs - p["x0"]:.1f}" height="{p["y1"] - p["y0"]}" fill="#e2e8f0"/>'
        s += polyline([(xmap(v), ymap(d)) for v, d in zip(vs, induced)], NAVY_BLUE, 6)
        s += polyline([(xmap(v), ymap(d)) for v, d in zip(vs, parasite)], RED, 6)
        s += polyline([(xmap(v), ymap(d)) for v, d in zip(vs, total)], "#7c3aed", 7)
        s += "</g>"
        s += f'<g transform="rotate(-90 {xs - 30:.1f} 380)">' + label(xs - 30, 392, "Stall", TXT_M, "#475569", "middle", halo=None) + "</g>"
        s += label(xmap(1.22), ymap(0.95), "A Induced", TXT_M, NAVY_BLUE)
        s += label(xmap(2.05), ymap(2.6), "B Parasite", TXT_M, RED, "end")
        s += label(xmap(0.68), ymap(3.45), "C Total", TXT_M, "#7c3aed")
        dx, dy = xmap(1.0), ymap(2.0)
        s += f'<circle cx="{dx:.1f}" cy="{dy:.1f}" r="11" fill="#ffffff" stroke="#7c3aed" stroke-width="5"/>'
        s += label(dx, dy - 26, "D", TXT_L, "#7c3aed", "middle")
        return s
    return dict(h=PLOT["y1"] + 80, sky="white", draw=draw, caption="B: PARASITE DRAG RISES WITH SPEED", color=RED)


@R.add(1153, "drag-curves-v1", "Drag and Speed",
       template("CURVE B IS PARASITE DRAG: IT RISES WITH SPEED", "A INDUCED · C TOTAL · D MINIMUM DRAG SPEED",
                [("A Induced drag", "Highest at low speed, falls as speed rises"),
                 ("C Total drag", "A + B, lowest at D (Vmd, best lift/drag)")]),
       h=stack_height([PLOT["y1"] + 80]), w=W)
def _():
    return picture([drag_panel()])


# ------------------------------------------------------------------ instruments: black face, white markings

def instrument(cx, cy, r):
    s = f'<circle cx="{cx}" cy="{cy}" r="{r + 18}" fill="#334155" stroke="#0f172a" stroke-width="4"/>'
    return s + f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#0b0f14"/>'


# #10 airspeed indicator: white, green and yellow arcs, red line at VNE

ASI = dict(lo=40, hi=200, sweep=320, VS0=45, VFE=100, VS1=50, VNO=130, VNE=165)


def asi_panel():
    def ang(v):
        return -ASI["sweep"] / 2 + (v - ASI["lo"]) / (ASI["hi"] - ASI["lo"]) * ASI["sweep"]

    def draw(w, h):
        cx, cy, r = 450, 400, 330
        s = f'<rect x="0" y="0" width="{w}" height="{h}" fill="#ffffff"/>' + instrument(cx, cy, r)
        def band(a, b, color, rad, width):
            return angle_arc(cx, cy, rad, ang(a), ang(b), color, width) if b - a < 90 else (
                angle_arc(cx, cy, rad, ang(a), ang((a + b) / 2), color, width) + angle_arc(cx, cy, rad, ang((a + b) / 2), ang(b), color, width))
        s += band(ASI["VS0"], ASI["VFE"], "#f8fafc", r - 62, 16)
        s += band(ASI["VS1"], ASI["VNO"], "#16a34a", r - 36, 26)
        s += band(ASI["VNO"], ASI["VNE"], "#facc15", r - 36, 26)
        a = math.radians(ang(ASI["VNE"]))
        s += path(f"M {cx + (r - 6) * math.sin(a):.1f},{cy - (r - 6) * math.cos(a):.1f} L {cx + (r - 80) * math.sin(a):.1f},{cy - (r - 80) * math.cos(a):.1f}",
                  "none", "#ef4444", 12)
        for v in range(ASI["lo"], ASI["hi"] + 1, 10):
            a = math.radians(ang(v))
            r2 = r - (100 if v % 20 == 0 else 88)
            s += path(f"M {cx + (r - 76) * math.sin(a):.1f},{cy - (r - 76) * math.cos(a):.1f} L {cx + r2 * math.sin(a):.1f},{cy - r2 * math.cos(a):.1f}",
                      "none", "#ffffff", 4)
            if v % 20 == 0:
                s += label(cx + (r - 140) * math.sin(a), cy - (r - 140) * math.cos(a) + 14, str(v), TXT_L, "#ffffff", "middle", halo=None)
        s += label(cx, cy + 120, "KNOTS", 32, "#cbd5e1", "middle", halo=None)
        a = math.radians(ang(112))
        s += (f'<path d="M {cx - 40 * math.sin(a) + 10 * math.cos(a):.1f},{cy + 40 * math.cos(a) + 10 * math.sin(a):.1f} '
              f'L {cx + (r - 90) * math.sin(a):.1f},{cy - (r - 90) * math.cos(a):.1f} '
              f'L {cx - 40 * math.sin(a) - 10 * math.cos(a):.1f},{cy + 40 * math.cos(a) - 10 * math.sin(a):.1f} Z" fill="#ffffff"/>')
        s += f'<circle cx="{cx}" cy="{cy}" r="20" fill="#475569"/>'
        a = math.radians(ang(ASI["VNE"]))
        s += label(cx + r + 26, cy - r * math.cos(a) + 14, "VNE", TXT_L, "#dc2626")
        return s
    return dict(h=790, sky="white", draw=draw, caption="RED LINE: VNE, NEVER EXCEED", color="#dc2626")


@R.add(1264, "asi-vne-v1", "Airspeed Indicator: VNE",
       template("VNE: NEVER EXCEED, IN ANY OPERATION", "THE RED LINE ON THE AIRSPEED INDICATOR",
                [("Yellow arc", "Caution: smooth air only, VNO to VNE"),
                 ("Green arc", "Normal operating range, VS1 to VNO"),
                 ("White arc", "Flap operating range, VS0 to VFE")]),
       h=stack_height([790]), w=W)
def _():
    return picture([asi_panel()])


# #18 turn coordinator: the needle (miniature aeroplane) shows the direction of turn, the ball shows balance

def tc_panel():
    def draw(w, h):
        cx, cy, r = 450, 400, 300
        s = f'<rect x="0" y="0" width="{w}" height="{h}" fill="#ffffff"/>' + instrument(cx, cy, r)
        # standard-rate marks: level and 3° per second either way
        for deg in (-90, 90, -70, 70):
            a = math.radians(deg)
            x1, y1 = cx + (r - 20) * math.sin(a), cy - (r - 20) * math.cos(a)
            x2, y2 = cx + (r - 70) * math.sin(a), cy - (r - 70) * math.cos(a)
            s += path(f"M {x1:.1f},{y1:.1f} L {x2:.1f},{y2:.1f}", "none", "#ffffff", 14)
        # the inclinometer: a curved glass tube with the ball centred
        s += f'<path d="M {cx - 150},{cy + 120} Q {cx},{cy + 210} {cx + 150},{cy + 120}" fill="none" stroke="#e2e8f0" stroke-width="62" stroke-linecap="round"/>'
        s += f'<path d="M {cx - 34},{cy + 140} L {cx - 34},{cy + 200} M {cx + 34},{cy + 140} L {cx + 34},{cy + 200}" stroke="#0b0f14" stroke-width="6"/>'
        s += f'<circle cx="{cx}" cy="{cy + 165}" r="26" fill="#0b0f14"/>'
        s += label(cx - 210, cy + 120, "L", TXT_L, "#ffffff", "middle", halo=None)
        s += label(cx + 210, cy + 120, "R", TXT_L, "#ffffff", "middle", halo=None)
        s += label(cx, cy + 85, "2 MIN", 32, "#ffffff", "middle", halo=None)
        # the miniature aeroplane, banked left: a left turn (or a spin to the left)
        s += f'<g transform="rotate(-20 {cx} {cy - 10})">'
        s += path(f"M {cx - 230},{cy - 10} L {cx + 230},{cy - 10}", "none", "#ffffff", 16)
        s += f'<circle cx="{cx}" cy="{cy - 10}" r="34" fill="#ffffff"/>'
        s += path(f"M {cx},{cy - 44} L {cx},{cy - 84}", "none", "#ffffff", 12) + "</g>"
        s += label(cx, 50, "Turn coordinator", TXT_M, INK, "middle")
        return s
    return dict(h=760, sky="white", draw=draw, caption="SPIN: THE TURN NEEDLE SHOWS DIRECTION", color=NAVY_BLUE)


@R.add(2025, "turn-coordinator-spin-v1", "Turn Coordinator in a Spin",
       template("IN A SPIN, THE TURN NEEDLE SHOWS THE DIRECTION OF ROTATION",
                "THE BALL AND THE ATTITUDE INDICATOR ARE UNRELIABLE",
                [("Recovery", "Full rudder against the needle's direction")]),
       h=stack_height([760]), w=W)
def _():
    return picture([tc_panel()])


# ------------------------------------------------------------------ aircraft pictures: the measured trainer from aircraft.py

from aircraft import aircraft, aircraft_top
from atg_phone import ac_point
from fp_phone import curve, flat, on_ground, plane_on, runway_side, track
from scene import cg_mark, terrain

AC_W = 600                               # side-view trainer length on the canvas


def ghost(*args, **kw):
    """The trainer drawn faded, so force arrows read over it (as the textbook greys its aircraft)."""
    return '<g opacity="0.45">' + aircraft(*args, **kw) + "</g>"


def force(a, vec, length, color, mid, w=VEC_W):
    """Force arrow from a along unit vector vec."""
    return arrow(a, (a[0] + vec[0] * length, a[1] + vec[1] * length), color, mid, w)


# #3 lift, weight and tail force (CG ahead of the centre of pressure)

def balance_panel():
    def draw(w, h):
        cx, cy = 450, 270
        s = f'<rect x="0" y="0" width="{w}" height="{h}" fill="#ffffff"/>' + ghost(cx, cy, AC_W)
        cg = ac_point(cx, cy, 0, 300, 158, AC_W)
        cp = ac_point(cx, cy, 0, 360, 158, AC_W)
        tail = ac_point(cx, cy, 0, 690, 137, AC_W)
        s += force(cp, (0, -1), 210, NAVY_BLUE, "pf_navy")
        s += force(cg, (0, 1), 200, RED, "pf_red", 8)
        s += force(tail, (0, 1), 120, RED, "pf_red", 8)
        s += cg_mark(*cg, 16)
        s += label(cp[0] + 20, cp[1] - 175, "Lift", TXT_L, NAVY_BLUE)
        s += label(cg[0] + 22, cg[1] + 190, "Weight", TXT_L, RED)
        s += label(tail[0], tail[1] + 170, "Tail force", TXT_L, RED, "middle")
        return s
    return dict(h=560, sky="white", draw=draw, caption="CG AHEAD OF LIFT: THE TAIL PUSHES DOWN", color=NAVY_BLUE)


@R.add(1126, "lift-weight-tail-v1", "Lift, Weight and Tail Force",
       template("THE CG IS AHEAD OF THE CENTRE OF PRESSURE", "SO THE NOSE DROPS WHEN POWER IS REDUCED",
                [("Tail force", "Down, balancing the nose-down pitch"),
                 ("CG moved aft", "Shorter arm, less longitudinal stability")]),
       h=stack_height([560]), w=W)
def _():
    return picture([balance_panel()])


# #7 forces in a steady climb

def climb_panel():
    def draw(w, h):
        th = math.radians(10)                                           # climb angle
        cx, cy, aw = 430, 340, 460
        s = f'<rect x="0" y="0" width="{w}" height="{h}" fill="#ffffff"/>'
        p0, p1 = (cx - 430 * math.cos(th), cy + 430 * math.sin(th)), (cx + 430 * math.cos(th), cy - 430 * math.sin(th))
        s += dashed(p0, p1, "#94a3b8", 3, "14 10")
        s += ghost(cx, cy, aw, pitch=12)
        cg = ac_point(cx, cy, 12, 300, 150, aw)
        fwd, up = (math.cos(th), -math.sin(th)), (-math.sin(th), -math.cos(th))
        s += force(cg, up, 210, NAVY_BLUE, "pf_navy")                   # lift: square to the flight path
        s += force(cg, (0, 1), 235, RED, "pf_red", 8)                    # weight: straight down, bigger than lift
        s += force(cg, fwd, 300, "#047857", "pf_green")                  # thrust, bigger than drag
        s += force(cg, (-fwd[0], -fwd[1]), 290 * 0.0 + 230, "#475569", "pf_ink")
        tail = ac_point(cx, cy, 12, 690, 137, aw)
        s += force(tail, (-up[0], -up[1]), 90, RED, "pf_red", 6)
        s += label(cg[0] - 50, cg[1] - 200, "Lift", TXT_L, NAVY_BLUE, "end")
        s += label(cg[0] + 22, cg[1] + 245, "Weight", TXT_L, RED)
        s += label(cg[0] + 300 * math.cos(th) - 10, cg[1] - 300 * math.sin(th) - 30, "Thrust", TXT_L, "#047857", "end")
        s += label(cg[0] - 230 * math.cos(th), cg[1] + 230 * math.sin(th) + 55, "Drag", TXT_L, "#475569", "middle")
        s += label(tail[0] + 10, tail[1] + 140, "Tail down force", TXT_M, RED, "middle")
        return s
    return dict(h=640, sky="white", draw=draw, caption="CLIMB: THRUST &gt; DRAG, LIFT &lt; WEIGHT", color=NAVY_BLUE)


@R.add(1219, "climb-forces-v1", "Forces in a Steady Climb",
       template("IN A STEADY CLIMB THRUST IS MORE THAN DRAG AND LIFT IS LESS THAN WEIGHT",
                "PART OF THE WEIGHT ACTS BACK ALONG THE FLIGHT PATH",
                [("Thrust", "Balances drag plus the rearward part of weight"),
                 ("Lift", "Balances only the part of weight square to the path")]),
       h=stack_height([640]), w=W)
def _():
    return picture([climb_panel()])


# #5 the glide: lift/drag = 7 gives a glide angle of atan(1/7), about 8°

def glide_panel():
    def draw(w, h):
        ld = 5.0
        th = math.atan(1 / ld)                                          # 11.3°
        cx, cy, aw = 400, 370, 380
        s = f'<rect x="0" y="0" width="{w}" height="{h}" fill="#ffffff"/>'
        ground = 680
        s += path(f"M 0,{ground} L {w},{ground}", "none", "#94a3b8", 4)
        gx = cx + (ground - cy) / math.tan(th)
        s += dashed((cx - 450 * math.cos(th), cy - 450 * math.sin(th)), (gx, ground), "#94a3b8", 3, "14 10")
        s += ghost(cx, cy, aw, pitch=-math.degrees(th) + 2)
        cg = (cx + 6, cy + 6)
        fwd, up = (math.cos(th), math.sin(th)), (math.sin(th), -math.cos(th))
        L = 300
        s += force(cg, up, L, NAVY_BLUE, "pf_navy")
        s += force(cg, (-fwd[0], -fwd[1]), L / ld + 200 * 0, "#475569", "pf_ink", 6)
        s += force(cg, (0, 1), math.hypot(L, L / ld), RED, "pf_red", 8)
        tip_l = (cg[0] + up[0] * L, cg[1] + up[1] * L)
        top = (cg[0], cg[1] - math.hypot(L, L / ld))
        s += dashed(tip_l, top, "#475569", 3, "10 8")
        s += dashed((cg[0] - fwd[0] * L / ld, cg[1] - fwd[1] * L / ld), top, "#475569", 3, "10 8")
        s += label(tip_l[0] + 20, tip_l[1] + 20, "Lift", TXT_L, NAVY_BLUE)
        s += label(cg[0] - 90, cg[1] - 40, "Drag", TXT_L, "#475569", "end")
        s += label(cg[0] + 22, cg[1] + 250, "Weight", TXT_L, RED)
        # the glide angle: between the horizontal and the glide path
        s += dashed(cg, (w - 20, cg[1]), INK, 3, "8 8")
        s += angle_arc(*cg, 380, 90, 90 + math.degrees(th), INK, 5)
        s += label(w - 20, cg[1] - 20, "Glide angle", TXT_M, INK, "end")
        return s
    return dict(h=720, sky="white", draw=draw, caption="HIGH LIFT/DRAG: SHALLOW GLIDE", color=NAVY_BLUE)


@R.add(1239, "glide-forces-v1", "Forces in a Glide",
       template("HIGH LIFT/DRAG RATIO: SHALLOW GLIDE ANGLE", "GLIDE RATIO = LIFT/DRAG: AT 10 IT GOES 10 MILES PER MILE OF HEIGHT",
                [("Lift + drag", "Together exactly balance the weight"),
                 ("Best glide", "At the speed for the best lift/drag ratio")]),
       h=stack_height([720]), w=W)
def _():
    return picture([glide_panel()])


# #6 the three axes, all through the centre of gravity

def axes_panel():
    def draw(w, h):
        cx, cy = 450, 380
        s = f'<rect x="0" y="0" width="{w}" height="{h}" fill="#ffffff"/>'
        s += dashed((cx, 40), (cx, 720), NAVY_BLUE, 5, "18 10")             # longitudinal
        s += dashed((60, cy), (840, cy), "#047857", 5, "18 10")             # lateral
        s += aircraft_top(cx, cy, 560)
        s += cg_mark(cx, cy, 18)
        s += angle_arc(cx, cy, 70, 30, 330, RED, 6, clockwise=True)
        s += label(cx + 22, 70, "Longitudinal axis: roll", TXT_M, NAVY_BLUE)
        s += label(40, cy + 95, "Lateral axis: pitch", TXT_M, "#047857")
        s += label(cx + 90, cy + 110, "Normal axis: yaw", TXT_M, RED)
        return s
    return dict(h=760, sky="white", draw=draw, caption="BANK: ROLL ABOUT THE LONGITUDINAL AXIS", color=NAVY_BLUE)


@R.add(1308, "three-axes-v1", "The Three Axes",
       template("A CHANGE OF BANK IS A ROLL ABOUT THE LONGITUDINAL AXIS",
                "ALL THREE AXES PASS THROUGH THE CENTRE OF GRAVITY",
                [("Longitudinal", "Nose to tail: roll, by the ailerons"),
                 ("Lateral", "Wingtip to wingtip: pitch, by the elevator"),
                 ("Normal", "Vertical: yaw, by the rudder")]),
       h=stack_height([760]), w=W)
def _():
    return picture([axes_panel()])


# #1 dihedral

def dihedral_panel():
    def draw(w, h):
        cx, cy, span = 450, 300, 780
        k = span / 1300
        s = f'<rect x="0" y="0" width="{w}" height="{h}" fill="#ffffff"/>' + aircraft_front(cx, cy, span)
        root, tip = (cx + 78 * k, cy + 72 * k), (cx + 648 * k, cy + 12 * k)
        s += dashed(root, (w - 20, root[1]), INK, 3, "14 9")
        s += dashed((w - 20 - (w - 20 - 40), root[1]), (cx - 78 * k, root[1]), INK, 3, "14 9")
        deg = math.degrees(math.atan2(root[1] - tip[1], tip[0] - root[0]))
        s += f'<path d="M {root[0]:.1f},{root[1]:.1f} L {tip[0]:.1f},{tip[1]:.1f} L {tip[0]:.1f},{root[1]:.1f} Z" fill="{RED}" fill-opacity="0.22"/>'
        s += angle_arc(*root, 330, 90 - deg, 90, RED, 6)
        s += label(w - 30, root[1] + 70, "Dihedral angle", TXT_L, RED, "end")
        return s
    return dict(h=480, sky="white", draw=draw, caption="DIHEDRAL: LATERAL STABILITY", color=RED)


@R.add(1168, "dihedral-v1", "Dihedral",
       template("DIHEDRAL IMPROVES LATERAL STABILITY", "WINGS TILTED UP FROM ROOT TO TIP",
                [("In a sideslip", "The lower wing meets the air at a bigger angle of attack"),
                 ("Result", "More lift on the lower wing rolls the aeroplane level")]),
       h=stack_height([480]), w=W)
def _():
    return picture([dihedral_panel()])


# #4 ailerons: one up, one down; the aeroplane rolls

def aileron_sections_panel():
    def draw(w, h):
        s = f'<rect x="0" y="0" width="{w}" height="{h}" fill="#ffffff"/>'
        for i, (deflect, name) in enumerate([(-22, "Aileron up"), (0, "Neutral"), (22, "Aileron down")]):
            y = 80 + i * 140
            main, ail = flap_parts("Plain")                       # the plain-flap geometry: a hinged trailing edge
            mid_u = FLAP_HINGE
            sec = section_frame(80)
            n = len(sec) // 2 + 1
            up_, lo_ = sec[:n][::-1], sec[n - 1:]
            vt = np.interp(mid_u, [p[0] for p in up_], [p[1] for p in up_])
            vb = np.interp(mid_u, [p[0] for p in lo_], [p[1] for p in lo_])
            about = (mid_u, (vt + vb) / 2)
            a0 = math.radians(25)                                 # undo the flap's 25° and set this deflection
            a1 = math.radians(-deflect)
            def turn(pts):
                out = []
                for u, v in pts:
                    du, dv = u - about[0], v - about[1]
                    du, dv = du * math.cos(a0) - dv * math.sin(a0), du * math.sin(a0) + dv * math.cos(a0)
                    du, dv = du * math.cos(a1) - dv * math.sin(a1), du * math.sin(a1) + dv * math.cos(a1)
                    out.append((about[0] + du, about[1] + dv))
                return out
            s += closed(place(turn(main), (330, y), 480, 0), RED, "#334155", 3)
            s += closed(place(ail, (330, y), 480, 0), SECTION_LIGHT, "#334155", 3)
            s += label(40, y + 12, name, TXT_M, RED if deflect else INK)
        return s
    return dict(h=470, sky="white", draw=draw, caption="AILERONS MOVE IN OPPOSITE DIRECTIONS", color=RED)


def aileron_roll_panel():
    def draw(w, h):
        cx, cy = 450, 250
        s = f'<rect x="0" y="0" width="{w}" height="{h}" fill="#ffffff"/>'
        s += f'<g transform="rotate(14 {cx} {cy})">' + aircraft_front(cx, cy, 700) + "</g>"
        s += force((115, 230), (0, -1), 120, NAVY_BLUE, "pf_navy")
        s += force((785, 250), (0, 1), 120, NAVY_BLUE, "pf_navy")
        s += label(150, 90, "Down aileron:\nwing rises", TXT_M, NAVY_BLUE)
        s += label(w - 140, 400, "Up aileron:\nwing drops", TXT_M, NAVY_BLUE, "end")
        return s
    return dict(h=470, sky="white", draw=draw, caption="ROLL FIRST, THEN YAW THE SAME WAY", color=NAVY_BLUE)


@R.add(1154, "aileron-roll-v1", "Ailerons: Roll",
       template("AILERONS: ROLL, THEN YAW IN THE SAME DIRECTION",
                "THE BANKED LIFT SIDESLIPS THE AEROPLANE INTO THE TURN",
                [("Primary effect", "Roll about the longitudinal axis"),
                 ("Further effect", "Sideslip, then yaw the same way as the roll")]),
       h=stack_height([470, 470]), w=W)
def _():
    return picture([aileron_sections_panel(), aileron_roll_panel()])


# #8 venturi: narrower, faster, lower pressure

def venturi_half(x, cy, h0=150, ht=70, xc=450, s=150):
    return h0 - (h0 - ht) * math.exp(-((x - xc) / s) ** 2)


def gauge(cx, cy, r, reading):
    """Round pressure gauge: white face, scale over 240°, needle at `reading` (0 low .. 1 high)."""
    s = f'<circle cx="{cx}" cy="{cy}" r="{r + 9}" fill="url(#pf_metal)" stroke="#334155" stroke-width="3"/>'
    s += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#ffffff" stroke="#94a3b8" stroke-width="2"/>'
    s += angle_arc(cx, cy, r - 10, -120, -40, "#16a34a", 8)                 # low end of the scale
    for i in range(9):
        a = math.radians(-120 + i * 30)
        s += path(f"M {cx + (r - 4) * math.sin(a):.1f},{cy - (r - 4) * math.cos(a):.1f} L {cx + (r - 18) * math.sin(a):.1f},{cy - (r - 18) * math.cos(a):.1f}",
                  "none", "#334155", 3)
    a = math.radians(-120 + reading * 240)
    s += path(f"M {cx},{cy} L {cx + (r - 14) * math.sin(a):.1f},{cy - (r - 14) * math.cos(a):.1f}", "none", RED, 6)
    return s + f'<circle cx="{cx}" cy="{cy}" r="8" fill="#334155"/>'


def venturi_panel(show):
    def draw(w, h):
        cy = 400 if show == "pressure" else 220
        s = f'<rect x="0" y="0" width="{w}" height="{h}" fill="#ffffff"/>'
        xs = np.linspace(30, 870, 140)
        inner = lambda x, sign: cy + sign * venturi_half(x, cy)             # noqa: E731
        # the air inside the pipe, then the metal walls
        s += closed([(x, inner(x, -1)) for x in xs] + [(x, inner(x, 1)) for x in xs[::-1]], "#e0f2fe", "none", 0)
        for f in (-0.7, -0.35, 0, 0.35, 0.7):
            s += polyline([(x, cy + f * venturi_half(x, cy)) for x in xs], "#38bdf8", 3)
        for sign in (-1, 1):
            wall = [(x, inner(x, sign)) for x in xs] + [(x, inner(x, sign) + sign * 30) for x in xs[::-1]]
            s += closed(wall, "url(#pf_metal)", "#334155", 3)
        if show == "speed":
            for x in (120, 450, 780):                                   # arrows sized by the local speed
                v = 150 / venturi_half(x, cy)
                s += arrow((x - 34 * v, cy), (x + 34 * v, cy), NAVY_BLUE, "pf_navy", 8)
            s += label(120, cy + 235, "Slow", TXT_L, INK, "middle")
            s += label(450, cy + 235, "Fast", TXT_L, RED, "middle")
            s += label(780, cy + 235, "Slow", TXT_L, INK, "middle")
        else:
            for x, reading in ((150, 0.82), (450, 0.22), (750, 0.76)):
                top = inner(x, -1) - 30
                s += f'<rect x="{x - 9}" y="{top - 70}" width="18" height="70" fill="url(#pf_metal)" stroke="#334155" stroke-width="3"/>'
                s += gauge(x, top - 135, 62, reading)
            for x in (120, 450, 780):
                v = 150 / venturi_half(x, cy)
                s += arrow((x - 30 * v, cy), (x + 30 * v, cy), NAVY_BLUE, "pf_navy", 7)
            s += label(150, cy + 235, "Higher", TXT_L, INK, "middle")
            s += label(450, cy + 235, "Lower", TXT_L, RED, "middle")
            s += label(750, cy + 235, "Higher", TXT_L, INK, "middle")
        return s
    if show == "speed":
        return dict(h=500, sky="white", draw=draw, caption="NARROWER: THE AIR SPEEDS UP", color=NAVY_BLUE)
    return dict(h=680, sky="white", draw=draw, caption="FASTER AIR: LOWER PRESSURE", color=RED)


@R.add(1110, "venturi-speed-v1", "Venturi: Speed",
       template("NARROWER VENTURI: THE AIR SPEEDS UP", "EQUATION OF CONTINUITY: THE SAME MASS FLOW PASSES EVERY POINT",
                [("Area × velocity", "Stays the same"), ("Half the area", "Twice the speed")]),
       h=stack_height([500]), w=W)
def _():
    return picture([venturi_panel("speed")])


@R.add(1140, "venturi-pressure-v1", "Venturi: Pressure",
       template("FASTER AIR HAS LOWER PRESSURE", "BERNOULLI: PRESSURE ENERGY + KINETIC ENERGY STAYS THE SAME",
                [("Throat", "Fastest air, lowest pressure"), ("Over a wing", "The same effect makes lift")]),
       h=stack_height([680]), w=W)
def _():
    return picture([venturi_panel("pressure")])


# #15 centre of gravity: the aeroplane hangs level from a hook at its CG

def cg_hook_panel():
    def draw(w, h):
        cx, cy = 470, 430
        s = f'<rect x="0" y="0" width="{w}" height="{h}" fill="#ffffff"/>'
        s += path(f"M 0,{h - 40} L {w},{h - 40}", "none", "#94a3b8", 4)
        cg = ac_point(cx, cy, 0, 300, 140, AC_W)
        # a simple crane: mast, boom, cable down to the hook at the CG
        s += path(f"M 60,{h - 40} L 60,120 L {cg[0]:.1f},70", "none", "#475569", 14)
        s += path(f"M {cg[0]:.1f},70 L {cg[0]:.1f},{cg[1] - 40:.1f}", "none", INK, 4)
        s += path(f"M {cg[0]:.1f},{cg[1] - 40:.1f} q -18,0 -18,18 q 0,18 18,18", "none", INK, 5)
        s += aircraft(cx, cy, AC_W)
        s += cg_mark(*cg, 18)
        s += force((cg[0], cg[1] + 30), (0, 1), 150, RED, "pf_red", 8)
        s += label(cg[0] + 32, cg[1] + 14, "CG", TXT_L, INK)
        s += label(cg[0] + 22, cg[1] + 170, "Total weight", TXT_L, RED)
        return s
    return dict(h=680, sky="white", draw=draw, caption="TOTAL WEIGHT ACTS THROUGH THE CG", color=RED)


@R.add(1138, "centre-of-gravity-v1", "Centre of Gravity",
       template("THE CENTRE OF GRAVITY: WHERE THE TOTAL WEIGHT ACTS",
                "HUNG FROM THAT POINT, THE AEROPLANE BALANCES LEVEL",
                [("Centre of pressure", "Where the total lift acts"),
                 ("CG limits", "Set by the manufacturer; check before every flight")]),
       h=stack_height([680]), w=W)
def _():
    return picture([cg_hook_panel()])


# #16 trim tab: it keeps its angle to the elevator

def trim_panel():
    def draw(w, h):
        s = f'<rect x="0" y="0" width="{w}" height="{h}" fill="#ffffff"/>'
        sym = [(x, -y) for x, y in aerofoil_pts(0, 0, 1, 0, m=0.0, p=0.4, t=0.12, n=60)]
        hinge, tab_at, tab_deg = 0.62, 0.88, 18
        for i, (deflect, name) in enumerate([(0, "Neutral"), (-20, "Elevator up"), (20, "Elevator down")]):
            y = 100 + i * 185
            fixed = [p for p in sym if p[0] <= hinge]
            elev = [p for p in sym if hinge - 0.01 <= p[0] <= tab_at]
            tab = [p for p in sym if p[0] >= tab_at - 0.01]
            def rot(pts, about, deg):
                a = math.radians(-deg)
                return [(about[0] + (u - about[0]) * math.cos(a) - (v - about[1]) * math.sin(a),
                         about[1] + (u - about[0]) * math.sin(a) + (v - about[1]) * math.cos(a)) for u, v in pts]
            tab = rot(tab, (tab_at, 0), tab_deg)                  # set on the tab hinge
            elev, tab = rot(elev, (hinge, 0), deflect), rot(tab, (hinge, 0), deflect)
            s += closed(place(tab, (330, y), 500, 0), RED, "#334155", 3)
            s += closed(place(elev, (330, y), 500, 0), "#93c5fd", "#334155", 3)
            s += closed(place(fixed, (330, y), 500, 0), SECTION_LIGHT, "#334155", 3)
            s += label(40, y + 12, name, TXT_M, INK)
        return s
    return dict(h=620, sky="white", draw=draw, caption="THE TAB KEEPS ITS ANGLE TO THE ELEVATOR", color=RED)


@R.add(1190, "trim-tab-v1", "Elevator Trim Tab",
       template("THE TRIM TAB STAYS AT ITS SET ANGLE TO THE ELEVATOR",
                "IT MOVES WITH THE ELEVATOR; ONLY THE TRIM WHEEL CHANGES ITS ANGLE",
                [("Tab down", "Pushes the elevator up: nose-up trim"),
                 ("Tab up", "Pushes the elevator down: nose-down trim")]),
       h=stack_height([620]), w=W)
def _():
    return picture([trim_panel()])


# #17 humidity: humid air is less dense, so the take-off run is longer and the climb poorer

def humid_panel(humid):
    def draw(w, h):
        g = 330
        s = terrain(flat(g), w, h, "url(#ground_day)") + runway_side(0, w, g)
        lift = 470 if humid else 330
        climb = curve([(lift, g), (lift + 80, g - 14), (860, g - (110 if humid else 230))])
        s += track([(60, g - 2), (lift, g - 2)], INK, w=4, dash="12 9")
        s += track(climb, NAVY_BLUE, w=5)
        s += on_ground(70, g, 110)
        s += plane_on(climb, 0.62, 120)
        s += label(40, 60, "Humid air" if humid else "Dry air", TXT_L, RED if humid else NAVY_BLUE)
        return s
    return dict(h=420, sky="sky_day", draw=draw,
                caption="HUMID: LONGER RUN, POORER CLIMB" if humid else "DRY AIR: SHORTER RUN, BETTER CLIMB",
                color=RED if humid else NAVY_BLUE)


@R.add(1345, "humidity-density-v1", "Humidity and Air Density",
       template("HUMID AIR IS LESS DENSE THAN DRY AIR", "WATER VAPOUR IS LIGHTER THAN THE AIR IT REPLACES",
                [("Effect", "Longer take-off run, poorer climb"),
                 ("Worst case", "Hot, high and humid")]),
       h=stack_height([420, 420]), w=W)
def _():
    return picture([humid_panel(False), humid_panel(True)])
