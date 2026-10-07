"""Navigation explanation pictures, phone-first (docs/EXPLANATION_ILLUSTRATION_STANDARD.md), built from scene.py.

The aircraft is the measured top view in aircraft.py; the ground is scene.ground_above. Each picture shows the
idea; the KEY FACT card on each question carries its own numbers.
"""
from common import Registry
from kit import template
from scene import (BLUE, flow, town_above, CAPTION, COMMON_DEFS, GOLD, INK, NAVY_BLUE, RED, TXT_L, TXT_M, W, aircraft_top,
                   angle_arc, compass_xy, defs, ground_above, head, label, north_line, path, stack, stack_height)

R = Registry("navigation", "/explanation-images/navigation/refined-batch-2")

TRUE_C = INK          # true north: the chart's meridians
MAG_C = RED           # magnetic north: the red end of a compass needle
COMP_C = GOLD         # compass north: where this aircraft's compass settles
NAV_DEFS = (head("head_true", TRUE_C), head("head_mag", MAG_C), head("head_comp", COMP_C))


def picture(panels):
    body, _ = stack(panels)
    return defs(*COMMON_DEFS, *NAV_DEFS) + body


# ------------------------------------------------------------------ variation and deviation

NORTH_H = 470


def north_panel(kind):
    def draw(w, h):
        s = ground_above(w, h, seed=4 if kind == "var" else 9)
        cx, cy = 450, 330
        if kind == "var":
            s += north_line(cx, cy, 270, 0, TRUE_C, "head_true")
            s += north_line(cx, cy, 270, -20, MAG_C, "head_mag")
            s += angle_arc(cx, cy, 170, -20, 0, MAG_C)
            s += aircraft_top(cx, cy, 190, heading=60)
            s += label(480, 95, "True north", TXT_L, TRUE_C)
            s += label(330, 95, "Magnetic\nnorth", TXT_L, MAG_C, "end")
        else:
            s += north_line(cx, cy, 270, -20, MAG_C, "head_mag")
            s += north_line(cx, cy, 270, -32, COMP_C, "head_comp", dash="18 10")
            s += angle_arc(cx, cy, 170, -32, -20, COMP_C)
            # the aircraft's own magnetism: engine, radios and wiring
            ex, ey = compass_xy(cx, cy, 52, 60)
            s += f'<circle cx="{ex:.0f}" cy="{ey:.0f}" r="44" fill="{GOLD}" fill-opacity="0.35" filter="url(#glow)"/>'
            s += aircraft_top(cx, cy, 190, heading=60)
            s += label(395, 72, "Magnetic north", TXT_L, MAG_C)
            s += label(36, 175, "Compass\nnorth", TXT_L, "#9a5b00")
        return s
    if kind == "var":
        return dict(h=NORTH_H, sky="aerial", draw=draw, caption="VARIATION — the Earth's magnetism", color=MAG_C)
    return dict(h=NORTH_H, sky="aerial", draw=draw, caption="DEVIATION — the aircraft's magnetism", color="#9a5b00")


@R.add(1593, "variation-deviation-v1", "Variation and Deviation",
       template("VARIATION IS THE ANGLE BETWEEN TRUE NORTH AND MAGNETIC NORTH",
                "DEVIATION IS THE ANGLE BETWEEN MAGNETIC NORTH AND COMPASS NORTH",
                [("Variation", "Set by where you are on Earth; read it from the isogonals on the chart"),
                 ("Deviation", "Set by the aircraft's own magnetism; read it from the compass card"),
                 ("West", "Add west: variation west, magnetic best; deviation west, compass best")]),
       h=stack_height([NORTH_H, NORTH_H]), w=W)
def _():
    return picture([north_panel("var"), north_panel("dev")])


# ------------------------------------------------------------------ wind triangle: drift and heading into wind

WIND_H = 500


def wind_panel(corrected):
    def draw(w, h):
        s = ground_above(w, h, seed=12 if corrected else 7, river=False)
        # the wind: three streamlines blowing from the west (left)
        for y in (150, 255, 360):
            s += flow([(20, y), (260, y)], BLUE, "head_blue", 8)
        start = (470, 440)
        if corrected:
            end = (470, 95)
            s += town_above(470, 75, 110, seed=3)
            hdg = -12
        else:
            end = compass_xy(*start, 360, 14)
            hdg = 0
        s += path(f"M {start[0]},{start[1]} L {end[0]:.0f},{end[1]:.0f}", "none", "#ffffff", 15, ' stroke-opacity="0.8"')
        s += path(f"M {start[0]},{start[1]} L {end[0]:.0f},{end[1]:.0f}", "none", RED, 9, ' marker-end="url(#head_red)"')
        # the aircraft part-way along its track, nose on its heading; heading line ahead of the nose
        ax, ay = compass_xy(*start, 200, 0 if corrected else 14)
        nx, ny = compass_xy(ax, ay, 210, hdg)
        s += path(f"M {ax:.0f},{ay:.0f} L {nx:.0f},{ny:.0f}", "none", INK, 6, ' stroke-dasharray="16 12"')
        s += aircraft_top(ax, ay, 170, heading=hdg)
        if corrected:
            s += label(415, 75, "Heading", TXT_L, INK, "end")
            s += label(520, 420, "Track", TXT_L, RED)
        else:
            s += label(495, 75, "Heading", TXT_L, INK, "end")
            s += label(640, 160, "Track", TXT_L, RED)
        return s
    return dict(h=WIND_H, sky="aerial", draw=draw,
                caption="HEAD INTO WIND TO HOLD TRACK" if corrected else "WIND FROM THE LEFT: DRIFT RIGHT",
                color=NAVY_BLUE if corrected else RED)


@R.add(1882, "wind-drift-v1", "Heading, Track and Drift",
       template("DRIFT IS THE ANGLE BETWEEN HEADING AND TRACK",
                "THE WIND CARRIES THE AIRCRAFT FROM WHERE IT POINTS TO WHERE IT GOES",
                [("Heading", "Where the nose points, through the air"),
                 ("Track", "The path over the ground"),
                 ("To hold a track", "Point the nose into wind by the drift angle")]),
       h=stack_height([WIND_H, WIND_H]), w=W)
def _():
    return picture([wind_panel(False), wind_panel(True)])


# ------------------------------------------------------------------ 1 in 60: track error and closing angle

SIXTY_H = 500


def sixty_panel(closing):
    def draw(w, h):
        s = ground_above(w, h, seed=21 if closing else 17)
        a, b = (450, 455), (450, 70)
        s += town_above(*a, 100, seed=5) + town_above(*b, 100, seed=6)
        s += path(f"M {a[0]},{a[1]} L {b[0]},{b[1]}", "none", "#ffffff", 14, ' stroke-opacity="0.8"')
        s += path(f"M {a[0]},{a[1]} L {b[0]},{b[1]}", "none", INK, 7, ' stroke-dasharray="20 14"')
        err = 16
        ac = compass_xy(*a, 250 if not closing else 195, err)                      # the aircraft, off track
        s += path(f"M {a[0]},{a[1]} L {ac[0]:.0f},{ac[1]:.0f}", "none", "#ffffff", 15, ' stroke-opacity="0.8"')
        s += path(f"M {a[0]},{a[1]} L {ac[0]:.0f},{ac[1]:.0f}", "none", RED, 9)
        s += angle_arc(*a, 130, 0, err, RED, 8)
        if closing:
            import math
            brg = math.degrees(math.atan2(b[0] - ac[0], -(b[1] + 45 - ac[1])))   # aircraft to destination
            s += path(f"M {ac[0]:.0f},{ac[1]:.0f} L {b[0]},{b[1] + 45}", "none", "#ffffff", 15, ' stroke-opacity="0.8"')
            s += path(f"M {ac[0]:.0f},{ac[1]:.0f} L {b[0]},{b[1] + 45}", "none", NAVY_BLUE, 9, ' marker-end="url(#head_blue)"')
            s += angle_arc(b[0], b[1] + 45, 75, 180, 180 + brg, NAVY_BLUE, 8)
            s += aircraft_top(*ac, 130, heading=brg)
            s += label(560, 400, "Track error", TXT_L, RED)
            s += label(560, 150, "Closing angle", TXT_L, NAVY_BLUE)
        else:
            s += aircraft_top(*ac, 130, heading=err)
            # the distance off track, measured square to the planned track
            s += path(f"M 456,{ac[1]:.0f} L {ac[0] - 8:.0f},{ac[1]:.0f}", "none", "#ffffff", 13, ' stroke-opacity="0.85"')
            s += path(f"M 456,{ac[1]:.0f} L {ac[0] - 8:.0f},{ac[1]:.0f}", "none", GOLD, 7)
            s += label(560, 400, "Track error", TXT_L, RED)
            s += label(600, 205, "Off track", TXT_L, "#9a5b00")
        return s
    return dict(h=SIXTY_H, sky="aerial", draw=draw,
                caption="TURN BY BOTH ANGLES TO REACH IT" if closing else "1 NM OFF IN 60 NM = 1°",
                color=NAVY_BLUE if closing else RED)


@R.add(1786, "one-in-sixty-v1", "The 1 in 60 Rule",
       template("1 NM OFF TRACK AFTER 60 NM IS A 1° TRACK ERROR",
                "TRACK ERROR = DISTANCE OFF × 60 ÷ DISTANCE FLOWN",
                [("Parallel the track", "Turn back by the track error"),
                 ("Reach the destination", "Turn by the track error plus the closing angle"),
                 ("Closing angle", "Distance off × 60 ÷ distance to go")]),
       h=stack_height([SIXTY_H, SIXTY_H]), w=W)
def _():
    return picture([sixty_panel(False), sixty_panel(True)])
