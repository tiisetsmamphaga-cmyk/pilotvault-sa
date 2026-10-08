"""Flight Planning explanation pictures, phone-first (docs/EXPLANATION_ILLUSTRATION_STANDARD.md), built from scene.py.

Each picture shows the idea; the KEY FACT card on each question carries its own numbers (the questions map to
these pictures in scripts/question_audit/fp_pictures.py). Real objects are the measured parts: the trainer and
the airliner from aircraft.py, the airspeed indicator and the tyre from scene.py.
"""
import math

from common import Registry
from kit import template
from scene import (BLUE, CAPTION, COMMON_DEFS, GOLD, INK, NAVY_BLUE, RED, TXT_L, TXT_M, W, aircraft, aircraft_top,
                   airliner_side, asi_dial, circle, defs, flow, head, label, path, stack, stack_height, terrain, tree,
                   tyre)

R = Registry("flight-planning", "/explanation-images/flight-planning/refined-batch-1")

LINE_W = 5
GREEN = "#15803d"
SLATE = "#465569"
FP_DEFS = (head("nh_red", RED, 26), head("nh_navy", NAVY_BLUE, 26), head("nh_ink", INK, 26),
           head("nh_green", GREEN, 26), head("nh_gold", GOLD, 26))


def picture(panels):
    body, _ = stack(panels)
    return defs(*COMMON_DEFS, *FP_DEFS) + body


def line(a, b, color, mid=None, w=None, dash=""):
    w = w or LINE_W
    d = f"M {a[0]:.0f},{a[1]:.0f} L {b[0]:.0f},{b[1]:.0f}"
    extra = (f' stroke-dasharray="{dash}"' if dash else "")
    s = path(d, "none", "#ffffff", w + 4, ' stroke-opacity="0.85"' + extra)
    return s + path(d, "none", color, w, (f' marker-end="url(#{mid})"' if mid else "") + extra)


def polyline(pts, color, w=LINE_W, dash="", mid=None):
    d = "M " + " L ".join(f"{x:.0f},{y:.0f}" for x, y in pts)
    extra = (f' stroke-dasharray="{dash}"' if dash else "")
    s = path(d, "none", "#ffffff", w + 4, ' stroke-opacity="0.85"' + extra)
    return s + path(d, "none", color, w, (f' marker-end="url(#{mid})"' if mid else "") + extra)


def dim_h(x0, x1, y, color=INK, tick=14):
    """Horizontal dimension line with end ticks, white edge underneath."""
    d = f"M {x0:.0f},{y:.0f} L {x1:.0f},{y:.0f} M {x0:.0f},{y - tick:.0f} L {x0:.0f},{y + tick:.0f} M {x1:.0f},{y - tick:.0f} L {x1:.0f},{y + tick:.0f}"
    return path(d, "none", "#ffffff", 9, ' stroke-opacity="0.85"') + path(d, "none", color, 4)


def dim_v(x, y0, y1, color=INK, tick=14):
    d = f"M {x:.0f},{y0:.0f} L {x:.0f},{y1:.0f} M {x - tick:.0f},{y0:.0f} L {x + tick:.0f},{y0:.0f} M {x - tick:.0f},{y1:.0f} L {x + tick:.0f},{y1:.0f}"
    return path(d, "none", "#ffffff", 9, ' stroke-opacity="0.85"') + path(d, "none", color, 4)


def runway_side(x0, x1, y):
    """Runway seen from the side: a dark strip on the ground."""
    return f'<rect x="{x0:.0f}" y="{y:.0f}" width="{x1 - x0:.0f}" height="10" fill="{SLATE}"/>'


def screen(x, ground, top):
    """The 50 ft screen: an imaginary marker, drawn dashed with a bar at its top."""
    return (path(f"M {x},{ground} L {x},{top}", "none", RED, 4, ' stroke-dasharray="12 8"')
            + path(f"M {x - 22},{top} L {x + 22},{top}", "none", RED, 6))


def flat(y):
    return lambda x: y


def on_ground(x, ground, width, nose_right=True, pitch=0):
    """Trainer standing on `ground` (main wheels on it)."""
    return aircraft(x, ground - 116 * width / 660, width, pitch, nose_right=nose_right)


# ------------------------------------------------------------------ flight paths
# A path is drawn once as a smooth curve; the aircraft sits on it with its main wheels on the line, turned to
# the path's direction (or to a given attitude), and the arrowhead marks where the path ends.

def curve(pts, n=40):
    """Dense points along a Catmull-Rom spline through pts."""
    out = []
    for i in range(len(pts) - 1):
        p0, p1, p2 = pts[max(i - 1, 0)], pts[i], pts[i + 1]
        p3 = pts[min(i + 2, len(pts) - 1)]
        for k in range(n):
            t = k / n
            out.append(tuple(0.5 * ((2 * p1[j]) + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t * t
                                    + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t ** 3) for j in (0, 1)))
    return out + [pts[-1]]


def track(dense, color, mid=None, w=LINE_W, dash=""):
    d = "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in dense)
    extra = (f' stroke-dasharray="{dash}"' if dash else "")
    s = path(d, "none", "#ffffff", w + 4, ' stroke-opacity="0.85"' + extra)
    return s + path(d, "none", color, w, (f' marker-end="url(#{mid})"' if mid else "") + extra)


def at(dense, f):
    """Point and direction (degrees, nose-up positive, moving right) a fraction f of the way along a path."""
    seg = [math.dist(a, b) for a, b in zip(dense[:-1], dense[1:])]
    goal, run, i = f * sum(seg), 0.0, 0
    while i < len(seg) - 1 and run + seg[i] < goal:
        run += seg[i]
        i += 1
    (x0, y0), (x1, y1) = dense[i], dense[i + 1]
    t = (goal - run) / seg[i] if seg[i] else 0
    return (x0 + (x1 - x0) * t, y0 + (y1 - y0) * t), math.degrees(math.atan2(y0 - y1, x1 - x0))


def plane_on(dense, f, width=120, pitch=None, prop=True):
    """Trainer flying right along the path, main wheels on it; pitch defaults to the path direction."""
    (x, y), ang = at(dense, f)
    p = math.radians(ang if pitch is None else pitch)
    k = width / 660
    a, b = 53 * k, 116 * k   # main wheel from the aircraft centre
    return aircraft(x - (a * math.cos(p) + b * math.sin(p)), y - (-a * math.sin(p) + b * math.cos(p)), width,
                    ang if pitch is None else pitch, prop=prop)


def straight(a, b):
    return [a, b]


# ------------------------------------------------------------------ take-off distance

TO_H, TO_G = 440, 330
LIFT, SCREEN = 440, (720, 160)
CLIMB = curve([(LIFT, TO_G), (LIFT + 90, TO_G - 22), (SCREEN[0], SCREEN[1]), (860, 70)])


def takeoff_panel(full):
    def draw(w, h):
        s = terrain(flat(TO_G), w, h, "url(#ground_day)") + runway_side(0, w, TO_G)
        s += track([(70, TO_G - 2), (LIFT, TO_G - 2)], INK, w=4, dash="12 9")
        if full:
            s += screen(SCREEN[0], TO_G, SCREEN[1])
            s += track(CLIMB, NAVY_BLUE, "nh_navy")
            s += plane_on(CLIMB, 0.8)
            s += label(SCREEN[0] + 26, 270, "50 ft", TXT_L, RED)
            s += dim_h(70, SCREEN[0], TO_G + 36)
            s += label(395, TO_G + 84, "Take-off distance", TXT_M, INK, "middle", halo="#cfe0b8")
        else:
            part = CLIMB[:len(CLIMB) // 2]
            s += track(part, NAVY_BLUE, "nh_navy")
            s += plane_on(CLIMB, 0.0, pitch=8)
            s += dim_h(70, LIFT, TO_G + 36)
            s += label(255, TO_G + 84, "Ground roll", TXT_M, INK, "middle", halo="#cfe0b8")
            s += label(LIFT - 40, 250, "Lift-off", TXT_L, NAVY_BLUE, "end")
        return s
    return dict(h=TO_H, sky="sky_day", draw=draw, color=NAVY_BLUE if full else INK,
                caption="TAKE-OFF DISTANCE: TO 50 FT" if full else "GROUND ROLL: TO LIFT-OFF")


@R.add(2247, "takeoff-distance-v1", "Take-off Distance",
       template("TAKE-OFF DISTANCE = GROUND ROLL + CLIMB TO 50 FT",
                "LONGER WHEN HOT, HIGH, HEAVY, WITH A TAILWIND OR ON GRASS"),
       h=stack_height([TO_H, TO_H]), w=W)
def _():
    return picture([takeoff_panel(False), takeoff_panel(True)])


# ------------------------------------------------------------------ landing distance

SCR_L, TD, STOP = (140, 160), 450, 780
APPROACH = curve([(0, 160 - 140 * 170 / 310), SCR_L, (TD - 70, TO_G - 18), (TD, TO_G)])


def landing_panel(full):
    def draw(w, h):
        s = terrain(flat(TO_G), w, h, "url(#ground_day)") + runway_side(0, w, TO_G)
        s += track(APPROACH, NAVY_BLUE, "nh_navy")
        s += track([(TD + 20, TO_G - 2), (STOP - 40, TO_G - 2)], INK, w=4, dash="12 9")
        if full:
            s += screen(SCR_L[0], TO_G, SCR_L[1])
            s += plane_on(APPROACH, 0.3, pitch=-2)
            s += label(SCR_L[0] + 26, 270, "50 ft", TXT_L, RED)
            s += dim_h(SCR_L[0], STOP + 20, TO_G + 36)
            s += label(470, TO_G + 84, "Landing distance", TXT_M, INK, "middle", halo="#cfe0b8")
        else:
            s += on_ground(STOP, TO_G, 130)
            s += dim_h(TD, STOP + 20, TO_G + 36)
            s += label(625, TO_G + 84, "Ground roll", TXT_M, INK, "middle", halo="#cfe0b8")
            s += label(TD + 10, 250, "Touchdown", TXT_L, NAVY_BLUE)
        return s
    return dict(h=TO_H, sky="sky_day", draw=draw, color=NAVY_BLUE if full else INK,
                caption="LANDING DISTANCE: FROM 50 FT" if full else "GROUND ROLL: TOUCHDOWN TO STOP")


def toward(a, b, gap):
    d = math.dist(a, b)
    return a[0] + (b[0] - a[0]) * (d - gap) / d, a[1] + (b[1] - a[1]) * (d - gap) / d


@R.add(2389, "landing-distance-v1", "Landing Distance",
       template("LANDING DISTANCE = FROM 50 FT TO A STOP",
                "LONGER WHEN HOT, HIGH, HEAVY, WITH A TAILWIND OR ON GRASS"),
       h=stack_height([TO_H, TO_H]), w=W)
def _():
    return picture([landing_panel(True), landing_panel(False)])


# ------------------------------------------------------------------ declared distances (seen from above)

RW_H = 340
RW_Y, RW_W = 175, 80          # runway centre line and width on the canvas
RW_X0, RW_X1 = 50, 700        # runway ends; stopway and clearway beyond the far end


def runway_top(x0, x1, displaced=0, stopway=0):
    """Runway from above, left to right: centre line, threshold bars, optional displaced threshold (white arrows
    before a white bar) and stopway (yellow chevrons) beyond the far end."""
    y0 = RW_Y - RW_W / 2
    s = ""
    if stopway:
        s += f'<rect x="{x1}" y="{y0}" width="{stopway}" height="{RW_W}" fill="#8a94a3" stroke="#2f3a49" stroke-width="2"/>'
        for k in range(2):
            cx = x1 + stopway * (0.3 + 0.4 * k)
            s += path(f"M {cx - 14},{y0 + 12} L {cx + 14},{RW_Y} L {cx - 14},{y0 + RW_W - 12}", "none", "#facc15", 6)
    s += f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{RW_W}" fill="{SLATE}" stroke="#2f3a49" stroke-width="2"/>'
    start = x0 + displaced
    for k in range(4):
        by = y0 + RW_W * (0.12 + k * 0.22)
        s += f'<rect x="{start + 10}" y="{by:.0f}" width="34" height="{RW_W * 0.1:.0f}" fill="#ffffff"/>'
        s += f'<rect x="{x1 - 44}" y="{by:.0f}" width="34" height="{RW_W * 0.1:.0f}" fill="#ffffff"/>'
    xx = start + 70
    while xx + 34 < x1 - 60:
        s += f'<rect x="{xx}" y="{RW_Y - 3}" width="34" height="6" fill="#ffffff"/>'
        xx += 62
    if displaced:
        s += f'<rect x="{start - 2}" y="{y0 + 4}" width="6" height="{RW_W - 8}" fill="#ffffff"/>'
        for k in range(2):
            ax = x0 + 18 + k * (displaced - 40) / 1.6
            s += path(f"M {ax},{RW_Y} L {ax + 34},{RW_Y} M {ax + 22},{RW_Y - 11} L {ax + 34},{RW_Y} L {ax + 22},{RW_Y + 11}",
                      "none", "#ffffff", 5)
    return s


def bracket(x0, x1, y, color, text, above=True, size=TXT_M):
    s = dim_h(x0, x1, y, color)
    ty = y - 18 if above else y + 46
    return s + label((x0 + x1) / 2, ty, text, size, color, "middle", halo="#dfe8cf")


def declared_panel(clearway):
    def draw(w, h):
        s = f'<rect x="0" y="0" width="{w}" height="{h}" fill="url(#aerial)"/>'
        if clearway:
            s += (f'<rect x="{RW_X1}" y="{RW_Y - 80}" width="{w - RW_X1 + 10}" height="160" fill="#ffffff" fill-opacity="0.18" '
                  f'stroke="#ffffff" stroke-width="4" stroke-dasharray="14 9"/>')
        s += runway_top(RW_X0, RW_X1, stopway=90)
        s += aircraft_top(RW_X0 + 70, RW_Y, 90, heading=90)
        if clearway:
            s += bracket(RW_X0, w - 30, RW_Y + 98, NAVY_BLUE, "TODA", above=False)
            s += label(RW_X1 + 20, RW_Y - 96, "Clearway", TXT_M, INK, halo="#dfe8cf")
        else:
            s += bracket(RW_X0, RW_X1, RW_Y - 70, INK, "TORA")
            s += bracket(RW_X0, RW_X1 + 90, RW_Y + 70, RED, "ASDA = TORA + stopway", above=False)
        return s
    return dict(h=RW_H, sky="aerial", draw=draw, color=NAVY_BLUE if clearway else RED,
                caption="CLEARWAY: FOR THE CLIMB-OUT" if clearway else "STOPWAY: FOR A REJECTED TAKE-OFF")


@R.add(2298, "declared-distances-v1", "Declared Distances",
       template("TORA: THE RUNWAY FOR THE GROUND RUN",
                "ASDA ADDS THE STOPWAY, TODA ADDS THE CLEARWAY"),
       h=stack_height([RW_H, RW_H]), w=W)
def _():
    return picture([declared_panel(False), declared_panel(True)])


def threshold_panel(landing):
    def draw(w, h):
        s = f'<rect x="0" y="0" width="{w}" height="{h}" fill="url(#aerial)"/>'
        disp = 170
        s += runway_top(RW_X0, RW_X1, displaced=disp, stopway=90)
        if landing:
            s += aircraft_top(RW_X0 + disp + 100, RW_Y, 90, heading=90)
            s += bracket(RW_X0 + disp, RW_X1, RW_Y - 70, NAVY_BLUE, "LDA")
            s += label(RW_X0 + 10, RW_Y + 110, "Displaced threshold", TXT_M, INK, halo="#dfe8cf")
        else:
            s += aircraft_top(RW_X0 + 70, RW_Y, 90, heading=90)
            s += bracket(RW_X0, RW_X1, RW_Y - 70, INK, "TORA: the whole runway")
        return s
    return dict(h=RW_H, sky="aerial", draw=draw, color=NAVY_BLUE if landing else INK,
                caption="LANDING STARTS AT THE THRESHOLD" if landing else "TAKE-OFF CAN USE THE WHOLE RUNWAY")


@R.add(2350, "displaced-threshold-v1", "Displaced Threshold",
       template("A DISPLACED THRESHOLD SHORTENS THE LDA ONLY",
                "LDA = RUNWAY LENGTH − DISPLACEMENT; A STOPWAY IS NEVER PART OF THE LDA"),
       h=stack_height([RW_H, RW_H]), w=W)
def _():
    return picture([threshold_panel(True), threshold_panel(False)])


# ------------------------------------------------------------------ runway slope

SL_H = 500


def slope_panel():
    def draw(w, h):
        lo, hi = (60, 400), (780, 250)
        ground = lambda x: lo[1] + (hi[1] - lo[1]) * min(max((x - lo[0]) / (hi[0] - lo[0]), 0), 1)  # noqa: E731
        s = terrain(ground, w, h, "url(#ground_day)")
        s += path(f"M {lo[0]},{lo[1]} L {hi[0]},{hi[1]}", "none", SLATE, 12)
        ang = math.degrees(math.atan2(lo[1] - hi[1], hi[0] - lo[0]))
        ax, aw = 250, 160
        d = 116 * aw / 660    # centre to wheels, turned with the slope
        s += aircraft(ax - d * math.sin(math.radians(ang)), ground(ax) - d * math.cos(math.radians(ang)), aw, ang)
        s += path(f"M {lo[0]},{lo[1]} L {hi[0] + 40},{lo[1]}", "none", INK, 3, ' stroke-dasharray="10 8"')
        s += dim_v(hi[0] + 30, hi[1], lo[1], RED)
        s += label(hi[0] + 6, 190, "Height\ndifference", TXT_M, RED, "middle")
        s += label(420, lo[1] + 60, "Runway length", TXT_M, INK, "middle", halo="#cfe0b8")
        return s
    return dict(h=SL_H, sky="sky_day", draw=draw, color=RED, caption="SLOPE % = HEIGHT ÷ LENGTH × 100")


@R.add(2255, "runway-slope-v1", "Runway Slope",
       template("SLOPE % = ELEVATION DIFFERENCE ÷ RUNWAY LENGTH × 100",
                "UP OR DOWN IN THE DIRECTION OF THE RUNWAY NAMED"),
       h=stack_height([SL_H]), w=W)
def _():
    return picture([slope_panel()])


# ------------------------------------------------------------------ centre of gravity

CG_H = 420
AC_X, AC_Y, AC_W = 470, 230, 640       # trainer, nose on the left
K = AC_W / 660


def ac_x(local):
    """Canvas x of a point on the trainer (aircraft.py local x, nose on the left)."""
    return AC_X + (local - 385) * K


def cg_mark(x, y, r=22):
    """Centre of gravity symbol: a circle with opposite quarters filled."""
    return (circle(x, y, r + 4, "#ffffff") + circle(x, y, r, "#ffffff", INK, 4)
            + path(f"M {x},{y} L {x + r},{y} A {r},{r} 0 0 1 {x},{y + r} Z M {x},{y} L {x - r},{y} A {r},{r} 0 0 1 {x},{y - r} Z", INK))


def weight_arrow(x, y, length=110, color=RED):
    return line((x, y), (x, y + length), color, "nh_red" if color == RED else "nh_navy", 6)


def cg_panel(shift):
    def draw(w, h):
        s = aircraft(AC_X, AC_Y, AC_W, 0, nose_right=False)
        datum, bag = ac_x(58), ac_x(470)
        if not shift:
            s += path(f"M {datum},{40} L {datum},{h - 30}", "none", INK, 4, ' stroke-dasharray="14 9"')
            s += label(datum + 14, 70, "Datum", TXT_M, INK)
            s += dim_h(datum, bag, 100, RED)
            s += label((datum + bag) / 2 + 40, 86, "Arm", TXT_L, RED, "middle")
            s += circle(bag, AC_Y, 12, RED, "#ffffff", 3) + weight_arrow(bag, AC_Y + 14)
        else:
            old, new = ac_x(280), ac_x(400)
            s += circle(bag, AC_Y, 12, RED, "#ffffff", 3) + weight_arrow(bag, AC_Y + 14)
            s += label(bag + 26, AC_Y + 110, "Bag", TXT_M, RED)
            s += cg_mark(old, 90) + line((old + 30, 90), (new - 30, 90), INK, "nh_ink")
            s += cg_mark(new, 90)
            s += label(old - 34, 104, "CG", TXT_L, INK, "end")
        return s
    return dict(h=CG_H, sky="sky_day", draw=draw, color=RED if not shift else INK,
                caption="MOMENT = WEIGHT × ARM" if not shift else "LOAD BEHIND THE CG MOVES IT AFT")


@R.add(2355, "cg-moment-v1", "Moment and Centre of Gravity",
       template("MOMENT = WEIGHT × ARM", "CG = TOTAL MOMENT ÷ TOTAL WEIGHT"),
       h=stack_height([CG_H, CG_H]), w=W)
def _():
    return picture([cg_panel(False), cg_panel(True)])


# ------------------------------------------------------------------ wind shear

WS_H = 460


def shear_panel(more_headwind):
    def draw(w, h):
        g, td = 400, 690
        s = terrain(flat(g), w, h, "url(#ground_day)") + runway_side(620, w, g)
        gy = lambda x: 160 + (g - 160) * x / td  # noqa: E731  (the glide path, 0 to touchdown)
        s += track([(0, gy(0)), (td, g)], INK, w=4, dash="14 10")
        s += label(30, 120, "Glide path", TXT_M, INK)
        x0 = 230
        if more_headwind:   # balloons above the path and floats past the touchdown point
            pts = [(x0, gy(x0)), (x0 + 140, gy(x0 + 140) - 22), (x0 + 300, gy(x0 + 300) - 62), (x0 + 470, gy(x0 + 470) - 92)]
            col, mk = NAVY_BLUE, "nh_navy"
        else:               # sinks below the path and lands short
            pts = [(x0, gy(x0)), (x0 + 110, gy(x0 + 110) + 26), (x0 + 220, gy(x0 + 220) + 66), (x0 + 300, g - 6)]
            col, mk = RED, "nh_red"
        dense = curve(pts)
        s += track(dense, col, mk)
        s += plane_on(dense, 0.02, pitch=-3)
        if more_headwind:
            for k, y in enumerate((70, 130)):
                s += flow([(880, y), (730, y)], BLUE, "head_blue", 7 - 2 * k)
            s += label(880, 190, "More headwind", TXT_M, BLUE, "end")
        else:
            for k, y in enumerate((70, 130)):
                s += flow([(580, y), (730, y)], RED, "head_red", 7 - 2 * k)
            s += label(880, 190, "More tailwind\nor less headwind", TXT_M, RED, "end")
        return s
    return dict(h=WS_H, sky="sky_day", draw=draw, color=NAVY_BLUE if more_headwind else RED,
                caption="ABOVE THE PATH: OVERSHOOT" if more_headwind else "BELOW THE PATH: UNDERSHOOT")


@R.add(2264, "windshear-v1", "Wind Shear",
       template("MORE HEADWIND: OVERSHOOT; LESS HEADWIND OR MORE TAILWIND: UNDERSHOOT",
                "AIRSPEED AND LIFT CHANGE BEFORE THE AIRCRAFT CAN ADJUST"),
       h=stack_height([WS_H, WS_H]), w=W)
def _():
    return picture([shear_panel(True), shear_panel(False)])


# ------------------------------------------------------------------ wake turbulence

WK_H = 480


def vortex(x, y, r=16):
    """A wingtip vortex seen end-on: a small spiral."""
    d = f"M {x + r:.1f},{y:.1f}"
    for k in range(1, 15):
        a = k * math.pi / 3
        rr = r * (1 - k / 16)
        d += f" L {x + rr * math.cos(a):.1f},{y + rr * math.sin(a):.1f}"
    return path(d, "none", "#475569", 3.5, ' stroke-opacity="0.75"')


def wake(pts, sink=26, every=70):
    """Vortices along a path, sinking behind it."""
    s = ""
    for (x0, y0), (x1, y1) in zip(pts[:-1], pts[1:]):
        n = max(1, int(math.dist((x0, y0), (x1, y1)) / every))
        for k in range(n):
            t = (k + 0.5) / n
            s += vortex(x0 + (x1 - x0) * t, y0 + (y1 - y0) * t + sink)
    return s


def wake_panel(departing):
    def draw(w, h):
        g = 380
        s = terrain(flat(g), w, h, "url(#ground_day)") + runway_side(0, w, g)
        if not departing:
            td = 330
            heavy = [(0, 170), (td, g)]
            s += track(heavy, "#64748b", w=4, dash="12 9")
            s += wake([(0, 170), (td - 70, g - 45)], sink=24)
            s += airliner_side(td, g, 360, 0, facing_right=True)
            light = curve([(0, 50), (420, 230), (640, g - 4)])
            s += track(light, NAVY_BLUE, "nh_navy")
            s += plane_on(light, 0.3, 110, pitch=-3)
            s += path(f"M {td},{g + 6} L {td},{g + 40}", "none", INK, 5)
            s += label(td, g + 76, "Heavy's touchdown", TXT_M, INK, "middle", halo="#cfe0b8")
            s += label(870, 240, "Land\nbeyond", TXT_L, NAVY_BLUE, "end")
        else:
            lo = 560
            heavy = [(lo, g), (w + 40, g - 75)]
            s += track(heavy, "#64748b", w=4, dash="12 9")
            s += wake([(lo + 40, g - 8), (w, g - 64)], sink=22)
            s += airliner_side(lo + 170, g - 34, 300, 12, facing_right=True)
            s += track([(60, g - 2), (300, g - 2)], INK, w=4, dash="12 9")
            light = curve([(300, g), (380, g - 30), (600, 170)])
            s += track(light, NAVY_BLUE, "nh_navy")
            s += plane_on(light, 0.55, 110)
            s += path(f"M {lo},{g + 6} L {lo},{g + 40}", "none", INK, 5)
            s += label(lo, g + 76, "Heavy's lift-off", TXT_M, INK, "middle", halo="#cfe0b8")
            s += label(40, 120, "Lift off\nbefore", TXT_L, NAVY_BLUE)
        return s
    return dict(h=WK_H, sky="sky_day", draw=draw, color=NAVY_BLUE,
                caption="BEHIND A LANDING HEAVY" if not departing else "BEHIND A DEPARTING HEAVY")


@R.add(2363, "wake-turbulence-v1", "Wake Turbulence",
       template("STAY ABOVE THE HEAVY AIRCRAFT'S FLIGHT PATH",
                "ITS VORTICES SINK BEHIND IT FROM ROTATION TO TOUCHDOWN"),
       h=stack_height([WK_H, WK_H]), w=W)
def _():
    return picture([wake_panel(False), wake_panel(True)])


# ------------------------------------------------------------------ VX and VY

VX_H = 440
# Illustrative numbers, spread so the two climbs separate on a phone: VX 55 kt at 600 ft/min (655 ft per NM),
# VY 80 kt at 700 ft/min (525 ft per NM). VX gains more height per mile, VY more per minute.
VX = (55, 600)
VY = (80, 700)
PX_NM, PX_FT, X0, G0 = 520, 0.42, 110, 380


def climb_xy(speed, rate, minutes):
    return X0 + PX_NM * speed / 60 * minutes, G0 - PX_FT * rate * minutes


def vxvy_panel(same_time):
    def draw(w, h):
        s = terrain(flat(G0), w, h, "url(#ground_day)") + runway_side(0, 300, G0)
        px, py = climb_xy(*VX, 1.0)
        if same_time:
            qx, qy = climb_xy(*VY, 1.0)
        else:
            qx, qy = climb_xy(*VY, (px - X0) / PX_NM * 60 / VY[0])
            s += path(f"M {px:.0f},{G0} L {px:.0f},{py - 60:.0f}", "none", INK, 3, ' stroke-dasharray="10 8"')
            s += tree(px - 40, G0, 1.6) + tree(px + 10, G0, 2.0)
        vx_path, vy_path = [(X0, G0), (px, py)], [(X0, G0), (qx, qy)]
        s += track(vy_path, NAVY_BLUE) + track(vx_path, RED)
        s += plane_on(vy_path, 0.99, 100) + plane_on(vx_path, 0.99, 100)
        s += label(px - 70, py - 40, "VX", TXT_L, RED, "end")
        s += label(qx + 20, qy + 70, "VY", TXT_L, NAVY_BLUE)
        return s
    return dict(h=VX_H, sky="sky_day", draw=draw, color=RED if not same_time else NAVY_BLUE,
                caption="SAME DISTANCE: VX CLIMBS MORE" if not same_time else "SAME TIME: VY CLIMBS MORE")


@R.add(2342, "vx-vy-v1", "VX and VY",
       template("VX: BEST ANGLE OF CLIMB; VY: BEST RATE OF CLIMB",
                "VX GIVES THE MOST HEIGHT PER DISTANCE, VY THE MOST HEIGHT PER MINUTE"),
       h=stack_height([VX_H, VX_H]), w=W)
def _():
    return picture([vxvy_panel(False), vxvy_panel(True)])


# ------------------------------------------------------------------ airspeed indicator

ASI_H = 760


def asi_panel():
    def draw(w, h):
        from scene import asi_angle, compass_xy
        cx, cy, r = 450, 370, 300
        s = asi_dial(cx, cy, r, needle=90)
        vfe = compass_xy(cx, cy, r * 0.77, asi_angle(100))
        vno = compass_xy(cx, cy, r * 0.88, asi_angle(165))
        s += line(vfe, (790, 600), INK, w=4) + label(800, 640, "VFE", TXT_L, INK)
        s += line(vno, (120, 690), INK, w=4) + label(110, 730, "VNO", TXT_L, INK, "end")
        return s
    return dict(h=ASI_H, sky="sky_grey", draw=draw, color=RED, caption="RED LINE: VNE, NEVER EXCEED")


@R.add(2254, "asi-arcs-v1", "Airspeed Indicator Markings",
       template("WHITE ARC TOP: VFE; GREEN ARC TOP: VNO; RED LINE: VNE"),
       h=stack_height([ASI_H]), w=W)
def _():
    return picture([asi_panel()])


# ------------------------------------------------------------------ glide range

GL_H = 520


def glide_panel():
    def draw(w, h):
        g = 400
        hill = lambda x: g - 70 * math.exp(-((x - 520) / 90) ** 2)  # noqa: E731
        s = terrain(hill, w, h, "url(#ground_day)")
        start, end = (170, 130), (830, g - 2)
        glide = [start, end]
        s += track(glide, NAVY_BLUE, "nh_navy", dash="14 10")
        s += plane_on(glide, 0.02, 130, pitch=-3, prop=False)
        s += dim_v(70, start[1], g, RED)
        s += label(90, 260, "Height\nabove terrain", TXT_M, RED)
        s += dim_h(start[0], end[0], g + 50)
        s += label((start[0] + end[0]) / 2, g + 100, "Glide range", TXT_M, INK, "middle", halo="#cfe0b8")
        return s
    return dict(h=GL_H, sky="sky_day", draw=draw, color=RED, caption="HEIGHT = CRUISE PA − TERRAIN PA")


@R.add(2250, "glide-range-v1", "Glide Range",
       template("GLIDE RANGE DEPENDS ON THE HEIGHT ABOVE THE TERRAIN",
                "CONVERT THE TERRAIN ELEVATION TO PRESSURE ALTITUDE FIRST"),
       h=stack_height([GL_H]), w=W)
def _():
    return picture([glide_panel()])


# ------------------------------------------------------------------ aquaplaning

AQ_H = 460


def aqua_panel(fast):
    def draw(w, h):
        surf, water = 380, 22
        s = f'<rect x="0" y="{surf}" width="{w}" height="{h - surf}" fill="{SLATE}"/>'
        cx, r = 430, 150
        lift = 26 if fast else 0
        cy = surf - r + 10 - lift
        s += f'<rect x="{cx - 34}" y="-10" width="68" height="{cy + 10}" fill="url(#ac_blue)" stroke="#334155" stroke-width="3"/>'
        if fast:
            s += path(f"M {cx - 220},{surf - water} L {cx + 40},{surf - water} Q {cx + 120},{surf - water} {cx + 150},{surf - water - 34} "
                      f"Q {cx + 180},{surf - water - 4} {w},{surf - water} L {w},{surf} L {cx - 220},{surf} Z", "#4aa3e8", extra=' fill-opacity="0.85"')
            s += path(f"M 0,{surf - water} L {cx - 220},{surf - water} L {cx - 220},{surf} L 0,{surf} Z", "#4aa3e8", extra=' fill-opacity="0.85"')
            s += path(f"M {cx - 120},{surf} L {cx + 120},{surf} L {cx + 20},{surf - water - lift} Z", "#2b8fd6")
        else:
            s += path(f"M 0,{surf - water} L {cx - 120},{surf - water} L {cx - 60},{surf} L 0,{surf} Z", "#4aa3e8", extra=' fill-opacity="0.85"')
            s += path(f"M {cx + 160},{surf - water - 10} Q {cx + 200},{surf - water} {w},{surf - water} L {w},{surf} L {cx + 60},{surf} Z",
                      "#4aa3e8", extra=' fill-opacity="0.85"')
        s += tyre(cx, cy, r, flat=0.0 if fast else 0.07)
        for k in range(3 if fast else 2):
            sx = cx + r * 0.9 + k * 34
            s += path(f"M {sx},{surf - water} q 30,-{60 + 30 * k} 70,-{40 + 40 * k}", "none", "#4aa3e8", 6)
        s += flow([(120, 90), (300, 90)], GOLD, "head_gold", 11 if fast else 7)
        if fast:
            s += label(330, 104, "Fast", TXT_L, GOLD)
            s += label(870, surf - 110, "Water\nwedge", TXT_M, "#0d4f8b", "end")
        else:
            s += label(330, 104, "Slow", TXT_L, GOLD)
            s += label(870, surf - 110, "Water\npushed away", TXT_M, "#0d4f8b", "end")
        return s
    return dict(h=AQ_H, sky="sky_grey", draw=draw, color=RED if fast else INK,
                caption="FAST: THE TYRE RIDES ON WATER" if fast else "SLOW: THE TYRE GRIPS THE RUNWAY")


@R.add(2300, "aquaplaning-v1", "Aquaplaning",
       template("AQUAPLANING: THE TYRE RIDES ON A FILM OF WATER",
                "MORE LIKELY AT HIGH SPEED, IN STANDING WATER AND WITH LOW TYRE PRESSURE"),
       h=stack_height([AQ_H, AQ_H]), w=W)
def _():
    return picture([aqua_panel(False), aqua_panel(True)])
