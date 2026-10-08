"""Navigation explanation pictures, phone-first (docs/EXPLANATION_ILLUSTRATION_STANDARD.md), built from scene.py.

The aircraft is the measured top view in aircraft.py; the ground is scene.ground_above. Each picture shows the
idea; the KEY FACT card on each question carries its own numbers.
"""
from common import Registry
from kit import template
import math

import random

from scene import (BLUE, globe, globe_line, globe_xy, stars, dial, flow, heading_dial, runway_above, sun, aircraft, ndb_mast, vor_dme_station, ndb_symbol, terrain, vor_rose, CAPTION, COMMON_DEFS, GOLD, INK, NAVY_BLUE, RED, TXT_L, TXT_M, W, aircraft_top,
                   angle_arc, compass_xy, defs, ground_above, head, label, north_line, path, stack, stack_height)

R = Registry("navigation", "/explanation-images/navigation/refined-batch-2")

TRUE_C = INK          # true north: the chart's meridians
MAG_C = RED           # magnetic north: the red end of a compass needle
COMP_C = GOLD         # compass north: where this aircraft's compass settles
LINE_W = 5           # navigation lines and arrows: thinner than the 9 px airflow streamlines
HALO_W = 9           # white edge under a line so it reads on the ground
ARC_W = 4
NAV_DEFS = (head("head_true", TRUE_C, 26), head("head_mag", MAG_C, 26), head("head_comp", COMP_C, 26),
            head("nh_red", RED, 26), head("nh_blue", BLUE, 26), head("nh_navy", NAVY_BLUE, 26))


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
            s += north_line(cx, cy, 270, 0, TRUE_C, "head_true", LINE_W)
            s += north_line(cx, cy, 270, -20, MAG_C, "head_mag", LINE_W)
            s += angle_arc(cx, cy, 170, -20, 0, MAG_C, ARC_W)
            s += aircraft_top(cx, cy, 190, heading=60)
            s += label(480, 95, "True north", TXT_L, TRUE_C)
            s += label(330, 95, "Magnetic\nnorth", TXT_L, MAG_C, "end")
        else:
            s += north_line(cx, cy, 270, -20, MAG_C, "head_mag", LINE_W)
            s += north_line(cx, cy, 270, -32, COMP_C, "head_comp", LINE_W, dash="14 9")
            s += angle_arc(cx, cy, 170, -32, -20, COMP_C, ARC_W)
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
            s += flow([(20, y), (260, y)], BLUE, "nh_blue", LINE_W)
        start = (470, 440)
        if corrected:
            end = (470, 95)
            s += runway_above(470, 85, 150)
            hdg = -12
        else:
            end = compass_xy(*start, 360, 14)
            hdg = 0
        s += path(f"M {start[0]},{start[1]} L {end[0]:.0f},{end[1]:.0f}", "none", "#ffffff", HALO_W, ' stroke-opacity="0.8"')
        s += path(f"M {start[0]},{start[1]} L {end[0]:.0f},{end[1]:.0f}", "none", RED, LINE_W, ' marker-end="url(#nh_red)"')
        # the aircraft part-way along its track, nose on its heading; heading line ahead of the nose
        ax, ay = compass_xy(*start, 200, 0 if corrected else 14)
        nx, ny = compass_xy(ax, ay, 210, hdg)
        s += path(f"M {ax:.0f},{ay:.0f} L {nx:.0f},{ny:.0f}", "none", INK, 4, ' stroke-dasharray="12 9"')
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
        s += runway_above(*a, 120, 70) + runway_above(*b, 120, 70)
        s += path(f"M {a[0]},{a[1]} L {b[0]},{b[1]}", "none", "#ffffff", HALO_W, ' stroke-opacity="0.8"')
        s += path(f"M {a[0]},{a[1]} L {b[0]},{b[1]}", "none", INK, 4, ' stroke-dasharray="14 10"')
        err = 16
        ac = compass_xy(*a, 250 if not closing else 195, err)                      # the aircraft, off track
        s += path(f"M {a[0]},{a[1]} L {ac[0]:.0f},{ac[1]:.0f}", "none", "#ffffff", HALO_W, ' stroke-opacity="0.8"')
        s += path(f"M {a[0]},{a[1]} L {ac[0]:.0f},{ac[1]:.0f}", "none", RED, LINE_W)
        s += angle_arc(*a, 130, 0, err, RED, ARC_W)
        if closing:
            import math
            brg = math.degrees(math.atan2(b[0] - ac[0], -(b[1] + 45 - ac[1])))   # aircraft to destination
            s += path(f"M {ac[0]:.0f},{ac[1]:.0f} L {b[0]},{b[1] + 45}", "none", "#ffffff", HALO_W, ' stroke-opacity="0.8"')
            s += path(f"M {ac[0]:.0f},{ac[1]:.0f} L {b[0]},{b[1] + 45}", "none", NAVY_BLUE, LINE_W, ' marker-end="url(#nh_navy)"')
            s += angle_arc(b[0], b[1] + 45, 75, 180, 180 + brg, NAVY_BLUE, ARC_W)
            s += aircraft_top(*ac, 130, heading=brg)
            s += label(560, 400, "Track error", TXT_L, RED)
            s += label(560, 150, "Closing angle", TXT_L, NAVY_BLUE)
        else:
            s += aircraft_top(*ac, 130, heading=err)
            # the distance off track, measured square to the planned track
            s += path(f"M 456,{ac[1]:.0f} L {ac[0] - 8:.0f},{ac[1]:.0f}", "none", "#ffffff", HALO_W, ' stroke-opacity="0.85"')
            s += path(f"M 456,{ac[1]:.0f} L {ac[0] - 8:.0f},{ac[1]:.0f}", "none", GOLD, LINE_W)
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


# ------------------------------------------------------------------ helpers for the radio pictures

def bearing(a, b):
    """Compass bearing from point a to point b on the canvas (0 = up, clockwise)."""
    return math.degrees(math.atan2(b[0] - a[0], a[1] - b[1])) % 360


def line(a, b, color, mid=None, w=None, dash=""):
    w = w or LINE_W
    d = f"M {a[0]:.0f},{a[1]:.0f} L {b[0]:.0f},{b[1]:.0f}"
    extra = (f' stroke-dasharray="{dash}"' if dash else "")
    s = path(d, "none", "#ffffff", w + 4, ' stroke-opacity="0.85"' + extra)
    return s + path(d, "none", color, w, (f' marker-end="url(#{mid})"' if mid else "") + extra)


def toward(a, b, gap):
    """Point `gap` short of b on the way from a."""
    d = math.dist(a, b)
    return a[0] + (b[0] - a[0]) * (d - gap) / d, a[1] + (b[1] - a[1]) * (d - gap) / d


# ------------------------------------------------------------------ QDM and QDR

Q_H = 480


def qcode_panel(to_station):
    def draw(w, h):
        s = ground_above(w, h, seed=31 if to_station else 33)
        st, ac = (230, 360), (650, 150)
        s += vor_rose(*st, 95, numbers=False)
        if to_station:
            brg = bearing(ac, st)
            s += north_line(*ac, 150, 0, MAG_C, "head_mag", LINE_W)
            s += line(ac, toward(ac, st, 100), RED, "nh_red")
            s += angle_arc(*ac, 80, 0, brg, RED, ARC_W, clockwise=True)
            s += aircraft_top(*ac, 120, heading=brg)
            s += label(630, 45, "Magnetic north", TXT_M, MAG_C, "end")
            s += label(420, 240, "QDM", TXT_L, RED, "end")
        else:
            brg = bearing(st, ac)
            s += north_line(*st, 230, 0, MAG_C, "head_mag", LINE_W)
            s += line(compass_xy(*st, 100, brg), toward(st, ac, 75), NAVY_BLUE, "nh_navy")
            s += angle_arc(*st, 150, 0, brg, NAVY_BLUE, ARC_W)
            s += aircraft_top(*ac, 120, heading=brg)
            s += label(255, 75, "Magnetic north", TXT_M, MAG_C)
            s += label(420, 175, "QDR", TXT_L, NAVY_BLUE)
        return s
    return dict(h=Q_H, sky="aerial", draw=draw,
                caption="QDM — magnetic bearing TO the station" if to_station else "QDR — magnetic bearing FROM it",
                color=RED if to_station else NAVY_BLUE)


@R.add(1751, "qdm-qdr-v1", "QDM and QDR",
       template("QDM IS THE MAGNETIC BEARING TO THE STATION; QDR IS THE MAGNETIC BEARING FROM IT",
                "QDM AND QDR ARE RECIPROCALS: THEY DIFFER BY 180°",
                [("QDM", "Magnetic, to the station: the heading to steer in still air"),
                 ("QDR", "Magnetic, from the station: the radial you are on"),
                 ("QTE / QUJ", "The same two bearings measured from true north")]),
       h=stack_height([Q_H, Q_H]), w=W)
def _():
    return picture([qcode_panel(True), qcode_panel(False)])


# ------------------------------------------------------------------ relative bearing (ADF)

RB_H = 480


def rb_panel(magnetic):
    def draw(w, h):
        s = ground_above(w, h, seed=41 if magnetic else 43, road=False)
        ac, ndb, hdg = (300, 330), (740, 300), 35
        brg = bearing(ac, ndb)
        s += ndb_symbol(*ndb, 46)
        if magnetic:
            s += north_line(*ac, 230, 0, MAG_C, "head_mag", LINE_W)
            s += line(ac, toward(ac, ndb, 60), RED, "nh_red")
            s += angle_arc(*ac, 150, 0, brg, RED, ARC_W)
            s += aircraft_top(*ac, 140, heading=hdg)
            s += label(325, 75, "Magnetic north", TXT_M, MAG_C)
            s += label(470, 200, "QDM", TXT_L, RED)
        else:
            nx, ny = compass_xy(*ac, 250, hdg)
            s += path(f"M {ac[0]},{ac[1]} L {nx:.0f},{ny:.0f}", "none", INK, 4, ' stroke-dasharray="12 9"')
            s += line(ac, toward(ac, ndb, 60), GOLD, None)
            s += angle_arc(*ac, 150, hdg, brg, GOLD, ARC_W)
            s += aircraft_top(*ac, 140, heading=hdg)
            s += label(470, 105, "Nose", TXT_L, INK)
            s += label(475, 260, "Relative\nbearing", TXT_L, "#9a5b00")
        return s
    return dict(h=RB_H, sky="aerial", draw=draw,
                caption="QDM = HEADING + RELATIVE BEARING" if magnetic else "ADF: MEASURED FROM THE NOSE",
                color=RED if magnetic else "#9a5b00")


@R.add(1752, "relative-bearing-v1", "Relative Bearing",
       template("THE ADF SHOWS THE RELATIVE BEARING: THE ANGLE FROM THE NOSE TO THE NDB",
                "MAGNETIC BEARING TO THE NDB (QDM) = MAGNETIC HEADING + RELATIVE BEARING",
                [("Relative bearing", "Measured clockwise from the aircraft's nose"),
                 ("Over 360°", "Subtract 360°"),
                 ("To plot from the NDB", "Take the reciprocal (± 180°), then apply variation")]),
       h=stack_height([RB_H, RB_H]), w=W)
def _():
    return picture([rb_panel(False), rb_panel(True)])


# ------------------------------------------------------------------ VOR radials

VOR_H = 480


def vor_panel(inbound):
    def draw(w, h):
        s = ground_above(w, h, seed=51 if inbound else 53, river=False)
        st, rad = (250, 330), 60
        s += vor_rose(*st, 120)
        far = compass_xy(*st, 760, rad)
        s += path(f"M {compass_xy(*st, 120, rad)[0]:.0f},{compass_xy(*st, 120, rad)[1]:.0f} L {far[0]:.0f},{far[1]:.0f}",
                  "none", "#1e3a8a", 4, ' stroke-dasharray="4 10"')
        ac = compass_xy(*st, 430, rad)
        if inbound:
            s += line(ac, compass_xy(*st, 160, rad), NAVY_BLUE, "nh_navy")
            s += aircraft_top(*ac, 130, heading=rad + 180)
            s += label(560, 95, "060 radial", TXT_L, INK)
            s += label(440, 360, "Track 240°\nto the VOR", TXT_L, NAVY_BLUE)
        else:
            s += line(compass_xy(*st, 160, rad), compass_xy(*st, 330, rad), RED, "nh_red")
            s += aircraft_top(*ac, 130, heading=rad)
            s += label(560, 95, "060 radial", TXT_L, INK)
            s += label(470, 380, "Outbound 060°", TXT_L, RED)
        return s
    return dict(h=VOR_H, sky="aerial", draw=draw,
                caption="INBOUND: FLY THE RECIPROCAL" if inbound else "A RADIAL POINTS AWAY FROM THE VOR",
                color=NAVY_BLUE if inbound else RED)


@R.add(1756, "vor-radial-v1", "VOR Radials",
       template("A VOR RADIAL IS THE MAGNETIC BEARING FROM THE STATION",
                "THE 060 RADIAL RUNS OUT FROM THE VOR ON 060° MAGNETIC",
                [("Outbound", "Track the radial: 060°"),
                 ("Inbound", "Track the reciprocal: 240° to the VOR"),
                 ("To plot it", "Apply the station's variation, not the aircraft's")]),
       h=stack_height([VOR_H, VOR_H]), w=W)
def _():
    return picture([vor_panel(False), vor_panel(True)])


# ------------------------------------------------------------------ DME slant range

DME_H = 460
GROUND = 400


def dme_panel(close):
    def draw(w, h):
        s = terrain(lambda x: GROUND, w, h, "url(#ground_day)")
        station, top = vor_dme_station(190, GROUND, 300)
        s += station
        ac = (390, 110) if close else (760, 300)
        base = GROUND + 14
        s += line((ac[0], base), (top[0], base), INK, None, 4, "12 9")
        s += path(f"M {ac[0]},{ac[1] + 25} L {ac[0]},{base}", "none", "#64748b", 3, ' stroke-dasharray="6 8"')
        s += line(top, toward(top, ac, 50), GOLD, None)
        s += aircraft(*ac, 150, 0, nose_right=True)
        if close:
            s += label(490, 90, "Slant range", TXT_L, "#9a5b00")
            s += label(330, 448, "Ground distance", TXT_M, INK, halo="#cfe0b8")
        else:
            s += label(440, 200, "Slant range", TXT_L, "#9a5b00")
            s += label(330, 448, "Ground distance", TXT_M, INK, halo="#cfe0b8")
        return s
    return dict(h=DME_H, sky="sky_day", draw=draw,
                caption="CLOSE AND HIGH: DME OVER-READS" if close else "FAR AWAY: ALMOST THE SAME",
                color=RED if close else NAVY_BLUE)


@R.add(1758, "dme-slant-range-v1", "DME Slant Range",
       template("DME MEASURES SLANT RANGE: THE STRAIGHT LINE FROM THE AIRCRAFT TO THE STATION",
                "IT IS LONGER THAN THE GROUND DISTANCE, MOST OF ALL WHEN CLOSE AND HIGH",
                [("How", "Times radio pulses out to the station and back"),
                 ("Overhead", "DME shows your height in nautical miles, not zero"),
                 ("Far away", "Slant range and ground distance are almost equal")]),
       h=stack_height([DME_H, DME_H]), w=W)
def _():
    return picture([dme_panel(True), dme_panel(False)])


# ------------------------------------------------------------------ NDB: ground wave and night effect

NDB_H = 460


def ndb_panel(night):
    def draw(w, h):
        s = ""
        if night:
            s += f'<rect x="0" y="40" width="{w}" height="70" fill="#a78bfa" fill-opacity="0.28" filter="url(#glow)"/>'
        s += terrain(lambda x: GROUND, w, h, "url(#ground_day)" if not night else "url(#ground_night)")
        s += ndb_mast(120, GROUND, 250, night)
        for k, y in enumerate((GROUND - 25, GROUND - 60, GROUND - 95)):
            s += flow([(190, y), (640, y)], BLUE if not night else "#7cc4ff", "nh_blue", LINE_W, 1 - k * 0.2)
        s += aircraft(760, 250, 150, 0, nose_right=False)
        if night:
            sky = [(130, 160), (280, 105), (420, 85), (560, 140), (700, 230)]
            s += flow(sky, "#f59e0b", "head_comp", LINE_W)
            s += label(460, 60, "Sky wave", TXT_L, "#fbbf24", halo="#0f1d3d")
            s += label(250, 445, "Ground wave", TXT_M, "#ffffff", halo="#0f1d3d")
        else:
            s += label(250, 445, "Ground wave", TXT_M, INK, halo="#cfe0b8")
            s += label(36, 70, "NDB", TXT_L, INK)
        return s
    return dict(h=NDB_H, sky="sky_night" if night else "sky_day", draw=draw,
                caption="NIGHT — SKY WAVE ADDS ERROR" if night else "DAY — GROUND WAVE", color=NAVY_BLUE if night else INK)


@R.add(1738, "ndb-night-effect-v1", "NDB Ground Wave and Night Effect",
       template("AT NIGHT, NDB SKY WAVES CAN INTERFERE WITH THE GROUND WAVE",
                "NDBs USE LF/MF: BY DAY THE SIGNAL FOLLOWS THE GROUND",
                [("Ground wave", "Follows the Earth's surface; the useful signal"),
                 ("Night effect", "The ionosphere reflects sky waves back down, making the needle wander"),
                 ("Coastal refraction", "The signal bends crossing a coast at a shallow angle")]),
       h=stack_height([NDB_H, NDB_H]), w=W)
def _():
    return picture([ndb_panel(False), ndb_panel(True)])


# ------------------------------------------------------------------ compass acceleration errors (Southern Hemisphere)

ACC_H = 480


def acc_panel(faster):
    def draw(w, h):
        s = ground_above(w, h, seed=61 if faster else 63, road=False)
        ac = (620, 250)
        # speed streaks behind the aircraft: long when accelerating, short when slowing
        for dy in (-60, -20, 20, 60):
            ln = 230 if faster else 90
            s += path(f"M {ac[0] - 90},{ac[1] + dy} L {ac[0] - 90 - ln},{ac[1] + dy}", "none", "#ffffff", 5,
                      ' stroke-opacity="0.75"')
        s += aircraft_top(*ac, 170, heading=90)
        s += heading_dial(225, 245, 190, 105 if faster else 75)
        s += label(860, 420, "Flying 090°", TXT_L, INK, "end")
        s += label(860, 70, "Compass " + ("105°" if faster else "075°"), TXT_L, RED if faster else NAVY_BLUE, "end")
        return s
    return dict(h=ACC_H, sky="aerial", draw=draw,
                caption="ACCELERATE: APPARENT TURN SOUTH" if faster else "SLOW DOWN: APPARENT TURN NORTH",
                color=RED if faster else NAVY_BLUE)


@R.add(1604, "compass-acceleration-v1", "Compass Errors (Southern Hemisphere)",
       template("IN THE SOUTHERN HEMISPHERE, ACCELERATING ON EAST OR WEST SHOWS A TURN SOUTH",
                "SLOWING DOWN SHOWS A TURN NORTH; ON NORTH OR SOUTH THERE IS NO ERROR",
                [("Acceleration error", "Largest on east and west headings; none on north or south"),
                 ("Turning error", "Largest turning through north or south; none on east or west"),
                 ("Southern Hemisphere roll-out", "Overshoot north, undershoot south (the reverse of UNOS)")]),
       h=stack_height([ACC_H, ACC_H]), w=W)
def _():
    return picture([acc_panel(True), acc_panel(False)])


# ------------------------------------------------------------------ runway wind components

XW_H = 500


def xw_panel(behind):
    def draw(w, h):
        s = ground_above(w, h, seed=71 if behind else 73, river=False, road=False)
        c = (450, 260)
        s += runway_above(*c, 420, 0)
        s += aircraft_top(450, 420, 110, heading=0)
        wind_from = 150 if behind else 330
        blow = (wind_from + 180) % 360
        a = compass_xy(*c, 230, wind_from)                     # upwind start of the wind arrow
        s += flow([a, compass_xy(*c, 30, wind_from)], BLUE, "nh_blue", LINE_W + 2)
        # components: along the runway and across it, drawn from the upwind point
        along = (a[0], c[1] - 30 * (1 if behind else -1))
        s += line(a, along, RED if behind else NAVY_BLUE, "nh_red" if behind else "nh_navy", LINE_W, "12 8")
        s += line(along, compass_xy(*c, 30, wind_from) if False else (c[0] - 30 if a[0] < c[0] else c[0] + 30, along[1]),
                  GOLD, "head_comp", LINE_W, "12 8")
        if behind:
            s += label(a[0] + 20, 150, "Tailwind", TXT_L, RED)
            s += label(560, 330, "Crosswind", TXT_L, "#9a5b00")
        else:
            s += label(a[0] - 20, 150, "Headwind", TXT_L, NAVY_BLUE, "end")
            s += label(40, 330, "Crosswind", TXT_L, "#9a5b00")
        return s
    return dict(h=XW_H, sky="aerial", draw=draw,
                caption="WIND BEHIND: TAILWIND + CROSSWIND" if behind else "WIND AHEAD: HEADWIND + CROSSWIND",
                color=RED if behind else NAVY_BLUE)


@R.add(1671, "runway-wind-components-v1", "Runway Wind Components",
       template("SPLIT THE WIND INTO A PART ALONG THE RUNWAY AND A PART ACROSS IT",
                "ALONG = WIND × COS(ANGLE); ACROSS = WIND × SIN(ANGLE)",
                [("Angle", "Between the wind direction and the runway direction"),
                 ("30°", "Crosswind half the wind; headwind about 0.9 of it"),
                 ("Wind from behind", "More than 90° off the runway: a tailwind component")]),
       h=stack_height([XW_H, XW_H]), w=W)
def _():
    return picture([xw_panel(False), xw_panel(True)])


# ------------------------------------------------------------------ groundspeed and fuel

GS_H = 480


def gs_panel():
    def draw(w, h):
        s = ground_above(w, h, seed=81, river=False, road=False)
        # two line features crossing the track at right angles: a river and a road
        s += path("M -10,400 C 300,385 600,415 910,398", "none", "#5f86a8", 22, ' stroke-opacity="0.55"')
        s += path("M -10,400 C 300,385 600,415 910,398", "none", "#8fb6d6", 12)
        s += path("M -10,105 L 910,112", "none", "#d6d0bf", 12) + path("M -10,105 L 910,112", "none", "#9a937f", 2, ' stroke-dasharray="14 12"')
        s += line((450, 470), (450, 40), RED, "nh_red")
        s += aircraft_top(450, 110, 150, heading=0)
        s += path("M 560,108 L 560,398 M 545,108 L 575,108 M 545,398 L 575,398", "none", "#ffffff", 9, ' stroke-opacity="0.85"')
        s += path("M 560,108 L 560,398 M 545,108 L 575,108 M 545,398 L 575,398", "none", INK, 4)
        s += label(590, 270, "Distance\nflown", TXT_L, INK)
        return s
    return dict(h=GS_H, sky="aerial", draw=draw, caption="GROUNDSPEED = DISTANCE ÷ TIME", color=RED)


def fuel_panel():
    def draw(w, h):
        s = dial(260, 250, 170, 12, lo=0, hi=40, numbers=(0, 20, 40), unit="USG")
        s += label(500, 200, "Fuel used =", TXT_L, INK)
        s += label(500, 290, "flow × time", TXT_L, NAVY_BLUE)
        return s
    return dict(h=GS_H, sky="sky_day", draw=draw, caption="FUEL USED = FLOW × TIME", color=NAVY_BLUE)


@R.add(1775, "groundspeed-fuel-v1", "Groundspeed, Time and Fuel",
       template("GROUNDSPEED = DISTANCE ÷ TIME; FUEL = FUEL FLOW × TIME",
                "TIME IN HOURS: MINUTES ÷ 60",
                [("Groundspeed", "Distance between two fixes ÷ time between them"),
                 ("Wind", "TAS = GS + headwind, or GS − tailwind"),
                 ("Fuel", "Trip fuel = time × flow; add taxi, climb and reserve fuel")]),
       h=stack_height([GS_H, GS_H]), w=W)
def _():
    return picture([gs_panel(), fuel_panel()])


# ------------------------------------------------------------------ climb and descent

CD_H = 460


def cd_panel(descent):
    def draw(w, h):
        ground = lambda x: 400
        s = terrain(ground, w, h, "url(#ground_day)")
        if descent:
            tod, fld = (300, 110), (820, 392)
            s += path(f"M 0,110 L {tod[0]},{tod[1]}", "none", INK, 4, ' stroke-dasharray="12 9"')
            s += line(tod, toward(tod, fld, 40), RED, "nh_red")
            s += f'<rect x="760" y="396" width="140" height="8" fill="#465569"/>'
            s += aircraft(150, 105, 140, 0, nose_right=True)
            s += path("M 860,110 L 860,388", "none", "#ffffff", 9, ' stroke-opacity="0.8"')
            s += path("M 860,110 L 860,388 M 845,110 L 875,110 M 845,388 L 875,388", "none", INK, 4)
            s += label(300, 70, "Top of descent", TXT_L, RED)
            s += label(840, 260, "Height\nto lose", TXT_M, INK, "end")
        else:
            toc = (620, 110)
            s += f'<rect x="0" y="396" width="160" height="8" fill="#465569"/>'
            s += line((120, 392), toc, NAVY_BLUE, "nh_navy")
            s += path(f"M {toc[0]},110 L 900,110", "none", INK, 4, ' stroke-dasharray="12 9"')
            s += aircraft(760, 105, 140, 0, nose_right=True)
            s += path("M 120,412 L 620,412 M 120,402 L 120,422 M 620,402 L 620,422", "none", INK, 4)
            s += label(370, 225, "Climb", TXT_L, NAVY_BLUE, "end")
            s += label(370, 440, "Distance = GS × time", TXT_M, INK, "middle", halo="#cfe0b8")
        return s
    return dict(h=CD_H, sky="sky_day", draw=draw,
                caption="DESCENT TIME = HEIGHT ÷ RATE" if descent else "CLIMB TIME = HEIGHT ÷ RATE",
                color=RED if descent else NAVY_BLUE)


@R.add(1824, "climb-descent-v1", "Climb and Descent Planning",
       template("TIME = HEIGHT TO CHANGE ÷ RATE; DISTANCE = GROUNDSPEED × TIME",
                "WORK OUT THE TIME FIRST, THEN THE DISTANCE",
                [("Rate needed", "Height to change ÷ time available"),
                 ("Time available", "Distance ÷ groundspeed × 60 (minutes)"),
                 ("Top of descent", "Descent distance back from the destination")]),
       h=stack_height([CD_H, CD_H]), w=W)
def _():
    return picture([cd_panel(True), cd_panel(False)])


# ------------------------------------------------------------------ pressure altitude

PA_H = 480


def land(x):
    return 330 if x < 300 else (200 if x > 520 else 330 - 130 * (1 - math.cos(math.pi * (x - 300) / 220)) / 2)


def pa_panel(low_qnh):
    def draw(w, h):
        s = terrain(land, w, h, "url(#ground_day)")
        s += f'<rect x="0" y="330" width="300" height="{h - 330}" fill="url(#sea)"/>'
        s += aircraft(690, 200 - 116 * 150 / 660, 150, 0, nose_right=False)  # parked on the aerodrome
        datum = 400 if low_qnh else 270
        s += path(f"M 0,{datum} L {w},{datum}", "none", RED, 4, ' stroke-dasharray="14 10"')
        s += path(f"M 820,200 L 820,{datum}", "none", "#ffffff", 10, ' stroke-opacity="0.85"')
        s += path(f"M 820,200 L 820,{datum} M 805,200 L 835,200 M 805,{datum} L 835,{datum}", "none", RED, 5)
        s += label(24, datum - 14, "1013 hPa level", TXT_M, RED)
        s += label(36, 300, "Sea level (QNH)", TXT_M, "#ffffff", halo="#0d4f8b") if low_qnh else \
            label(36, 380, "Sea level (QNH)", TXT_M, "#ffffff", halo="#0d4f8b")
        return s
    return dict(h=PA_H, sky="sky_day", draw=draw,
                caption="QNH BELOW 1013: PA IS HIGHER" if low_qnh else "QNH ABOVE 1013: PA IS LOWER",
                color=RED if low_qnh else NAVY_BLUE)


@R.add(1651, "pressure-altitude-v1", "Pressure Altitude",
       template("PRESSURE ALTITUDE = ELEVATION + (1013 − QNH) × 30 FT",
                "IT IS THE HEIGHT ABOVE THE 1013 hPa LEVEL",
                [("QNH below 1013", "Pressure altitude is higher than the elevation"),
                 ("QNH above 1013", "Pressure altitude is lower than the elevation"),
                 ("Density altitude", "Pressure altitude + 120 ft per °C above ISA")]),
       h=stack_height([PA_H, PA_H]), w=W)
def _():
    return picture([pa_panel(True), pa_panel(False)])


# ------------------------------------------------------------------ official day and night

DN_H = 460
HORIZON = 330


def hills(x):
    return HORIZON + 14 * math.sin(x / 95) + 8 * math.sin(x / 37)


def dn_panel(rise):
    def draw(w, h):
        r = 55
        cy = hills(450) + r - (22 if rise else 12)   # only the top edge of the sun shows
        s = sun(450, cy, r)
        s += terrain(hills, w, h, "url(#ground_day)")
        y0, y1 = (cy - r - 20, cy - r - 95) if rise else (cy - r - 95, cy - r - 20)
        s += path(f"M 560,{y0:.0f} L 560,{y1:.0f}", "none", "#7c2d12", LINE_W, ' marker-end="url(#head_comp)"')
        if rise:
            s += label(450, 230, "Sunrise", TXT_L, "#7c2d12", "middle", halo="#fde7c2")
            s += label(36, 70, "Day starts\n15 min before", TXT_L, "#ffffff", halo="#2a3560")
        else:
            s += label(450, 230, "Sunset", TXT_L, "#7c2d12", "middle", halo="#fde7c2")
            s += label(36, 70, "Night starts\n15 min after", TXT_L, "#ffffff", halo="#2a3560")
        return s
    return dict(h=DN_H, sky="sky_dawn", draw=draw,
                caption="OFFICIAL DAY: 15 MIN BEFORE SUNRISE" if rise else "OFFICIAL NIGHT: 15 MIN AFTER SUNSET",
                color="#b45309" if rise else NAVY_BLUE)


@R.add(1625, "official-day-night-v1", "Official Day and Night",
       template("OFFICIAL DAY RUNS FROM 15 MIN BEFORE SUNRISE TO 15 MIN AFTER SUNSET",
                "SUNRISE: THE FIRST EDGE OF THE SUN APPEARS; SUNSET: THE LAST EDGE DISAPPEARS",
                [("Day starts", "Sunrise − 15 min"),
                 ("Night starts", "Sunset + 15 min"),
                 ("UTC to SAST", "Add 2 hours")]),
       h=stack_height([DN_H, DN_H]), w=W)
def _():
    return picture([dn_panel(True), dn_panel(False)])


# ------------------------------------------------------------------ longitude and time

LT_H = 480


def lt_panel(sun_side):
    def draw(w, h):
        rnd = random.Random(7)
        s = stars(rnd, (0, 0, w, h), 40)
        cx, cy, r = (430, 250, 200)
        s += globe(cx, cy, r, tilt=-15, lon0=20)
        if not sun_side:
            for lon, col in ((20, RED), (35, RED)):
                s += globe_line(cx, cy, r, [(lat, lon) for lat in range(-90, 91, 3)], col, 5, "", -15, 20)
            eq = [globe_xy(cx, cy, r + 26, 0, lon, -15, 20)[:2] for lon in range(-40, 81, 10)]
            s += flow(eq, GOLD, "head_comp", LINE_W)
            s += label(620, 420, "West to east", TXT_L, "#fbbf24", halo="#0f1d3d")
            s += label(40, 70, "15° = 1 hour", TXT_L, "#ffffff", halo="#0f1d3d")
        else:
            s += f'<path d="M {cx},{cy - r} A {r},{r} 0 0 0 {cx},{cy + r} Z" fill="#0b1430" fill-opacity="0.55"/>'
            s += sun(820, 250, 45)
            for lon, col in ((0, "#ffffff"), (45, GOLD)):
                x, y, _ = globe_xy(cx, cy, r, -28, lon, -15, 20)
                s += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="11" fill="{col}" stroke="#111827" stroke-width="3"/>'
            s += label(40, 70, "East sees the\nsun first", TXT_L, "#fbbf24", halo="#0f1d3d")
            s += label(40, 440, "4 min per degree", TXT_L, "#ffffff", halo="#0f1d3d")
        return s
    return dict(h=LT_H, sky="sky_night", draw=draw,
                caption="EAST IS AHEAD IN LOCAL TIME" if sun_side else "THE EARTH TURNS 15° AN HOUR",
                color=NAVY_BLUE)


@R.add(1788, "longitude-time-v1", "Longitude and Time",
       template("THE EARTH TURNS 360° IN 24 HOURS: 15° AN HOUR, 4 MINUTES PER DEGREE",
                "PLACES FURTHER EAST HAVE A LATER LOCAL MEAN TIME",
                [("Time from longitude", "Degrees × 4 min + minutes of arc × 4 s"),
                 ("UTC", "LMT − longitude time when east of Greenwich"),
                 ("South Africa", "SAST = UTC + 2 all year")]),
       h=stack_height([LT_H, LT_H]), w=W)
def _():
    return picture([lt_panel(False), lt_panel(True)])


# ------------------------------------------------------------------ chart scale

SC_H = 480


def scale_panel(km):
    def draw(w, h):
        s = ground_above(w, h, seed=91 if km == 10 else 93, road=False)
        s += '<rect x="40" y="26" width="820" height="170" rx="6" fill="url(#chart_paper)" stroke="#b8ad95" stroke-width="3"/>'
        for x in range(100, 860, 120):
            s += f'<line x1="{x}" y1="26" x2="{x}" y2="196" stroke="#c9bfa6" stroke-width="2"/>'
        # ruler with centimetre marks; one centimetre drawn 70 units long
        s += '<rect x="80" y="120" width="740" height="60" rx="4" fill="#f6d77a" stroke="#a37b12" stroke-width="3"/>'
        for k in range(11):
            x = 100 + k * 70
            s += f'<line x1="{x}" y1="120" x2="{x}" y2="{150 if k % 5 else 162}" stroke="#5b4300" stroke-width="3"/>'
        s += '<rect x="380" y="112" width="70" height="76" fill="none" stroke="#b91c1c" stroke-width="6"/>'
        gw = 300 if km == 10 else 150
        x0 = 450 - gw / 2 + 35 - 35
        s += path(f"M 380,188 L {450 - gw / 2:.0f},400 M 450,188 L {450 + gw / 2:.0f},400", "none", "#b91c1c", 3, ' stroke-dasharray="10 8"')
        s += path(f"M {450 - gw / 2:.0f},400 L {450 + gw / 2:.0f},400", "none", "#ffffff", 13, ' stroke-opacity="0.85"')
        s += path(f"M {450 - gw / 2:.0f},400 L {450 + gw / 2:.0f},400 M {450 - gw / 2:.0f},385 L {450 - gw / 2:.0f},415 "
                  f"M {450 + gw / 2:.0f},385 L {450 + gw / 2:.0f},415", "none", "#b91c1c", 6)
        s += label(470, 90, "1 cm", TXT_L, "#b91c1c")
        s += label(450, 455, f"{km} km", TXT_L, "#b91c1c", "middle")
        return s
    return dict(h=SC_H, sky="aerial", draw=draw,
                caption="1 : 1 000 000 — 1 CM = 10 KM" if km == 10 else "1 : 500 000 — 1 CM = 5 KM",
                color="#b91c1c" if km == 10 else NAVY_BLUE)


@R.add(1771, "chart-scale-v1", "Chart Scale",
       template("A SCALE OF 1 : 1 000 000 MEANS 1 CM ON THE CHART IS 1 000 000 CM (10 KM) ON THE GROUND",
                "GROUND DISTANCE = CHART DISTANCE × SCALE DENOMINATOR",
                [("1 : 1 000 000", "1 cm = 10 km"),
                 ("1 : 500 000", "1 cm = 5 km"),
                 ("Kilometres to NM", "Divide by 1.852")]),
       h=stack_height([SC_H, SC_H]), w=W)
def _():
    return picture([scale_panel(10), scale_panel(5)])


# ------------------------------------------------------------------ Lambert conformal conic

LC_H = 500


def lc_panel(flat):
    def draw(w, h):
        if not flat:
            rnd = random.Random(9)
            s = stars(rnd, (0, 0, w, h), 30)
            cx, cy, r = 450, 230, 180
            s += globe(cx, cy, r, tilt=-35, lon0=25)
            # secant cone through the 15°S and 45°S parallels, apex beyond the South Pole
            a, b = -15, -45
            pa = [globe_xy(cx, cy, r, a, lon, -35, 25) for lon in (-65, 115)]
            pb = [globe_xy(cx, cy, r, b, lon, -35, 25) for lon in (-65, 115)]
            apex = (cx, cy + r * 1.75)
            top_l = (pa[0][0] - (apex[0] - pa[0][0]) * 0.35, pa[0][1] - (apex[1] - pa[0][1]) * 0.35)
            top_r = (pa[1][0] + (pa[1][0] - apex[0]) * 0.35, pa[1][1] - (apex[1] - pa[1][1]) * 0.35)
            s += (f'<path d="M {top_l[0]:.0f},{top_l[1]:.0f} L {apex[0]:.0f},{apex[1]:.0f} L {top_r[0]:.0f},{top_r[1]:.0f} Z" '
                  f'fill="#fbbf24" fill-opacity="0.22" stroke="#f59e0b" stroke-width="4"/>')
            for lat in (a, b):
                s += globe_line(cx, cy, r, [(lat, lon) for lon in range(-180, 181, 3)], GOLD, 6, "", -35, 25)
            s += label(40, 70, "Cone", TXT_L, "#fbbf24", halo="#0f1d3d")
            s += label(860, 300, "Standard\nparallels", TXT_L, "#fbbf24", "end", halo="#0f1d3d")
            return s
        s = '<rect x="0" y="0" width="900" height="500" fill="url(#chart_paper)"/>'
        apex = (450, 1500)
        for k in range(-4, 5):
            x, y = compass_xy(*apex, 1600, k * 6)
            s += path(f"M {apex[0]},{apex[1]} L {x:.0f},{y:.0f}", "none", "#94a3b8", 3)
        for rr in (1150, 1300, 1450):
            s += path(f"M {compass_xy(*apex, rr, -30)[0]:.0f},{compass_xy(*apex, rr, -30)[1]:.0f} A {rr},{rr} 0 0 1 "
                      f"{compass_xy(*apex, rr, 30)[0]:.0f},{compass_xy(*apex, rr, 30)[1]:.0f}", "none", "#94a3b8", 3)
        s += line((150, 330), (760, 150), RED, "nh_red")
        s += label(40, 470, "Meridians meet towards the pole", TXT_M, INK)
        s += label(450, 120, "Straight line ≈ great circle", TXT_M, RED, "middle")
        return s
    return dict(h=LC_H, sky="sky_night" if not flat else "aerial", draw=draw,
                caption="A CONE CUTS THE EARTH AT 2 PARALLELS" if not flat else "LAMBERT: SCALE TRUE ON THE 2 PARALLELS",
                color="#b45309" if not flat else NAVY_BLUE)


@R.add(1579, "lambert-conic-v1", "Lambert Conformal Conic Chart",
       template("A LAMBERT CHART IS PROJECTED ONTO A CONE THAT CUTS THE EARTH AT TWO STANDARD PARALLELS",
                "IT IS CONFORMAL (ORTHOMORPHIC): ANGLES ARE TRUE AND MERIDIANS CROSS PARALLELS AT 90°",
                [("Scale", "Correct only on the two standard parallels"),
                 ("Meridians", "Straight lines converging towards the nearer pole"),
                 ("Straight line", "Close to a great circle; measure its track at the mid-meridian")]),
       h=stack_height([LC_H, LC_H]), w=W)
def _():
    return picture([lc_panel(False), lc_panel(True)])


# ------------------------------------------------------------------ great circle and rhumb line

def _vec(lat, lon):
    la, lo = math.radians(lat), math.radians(lon)
    return (math.cos(la) * math.cos(lo), math.cos(la) * math.sin(lo), math.sin(la))


def great_circle(a, b, n=60):
    va, vb = _vec(*a), _vec(*b)
    om = math.acos(sum(p * q for p, q in zip(va, vb)))
    out = []
    for k in range(n + 1):
        t = k / n
        f1, f2 = math.sin((1 - t) * om) / math.sin(om), math.sin(t * om) / math.sin(om)
        x, y, z = (f1 * p + f2 * q for p, q in zip(va, vb))
        out.append((math.degrees(math.asin(z)), math.degrees(math.atan2(y, x))))
    return out


def merc_y(lat):
    return math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))


def rhumb(a, b, n=60):
    ya, yb = merc_y(a[0]), merc_y(b[0])
    return [(math.degrees(2 * math.atan(math.exp(ya + (yb - ya) * k / n)) - math.pi / 2), a[1] + (b[1] - a[1]) * k / n)
            for k in range(n + 1)]


GR_H = 500
GA, GB = (-40, -35), (-40, 90)


def gr_panel(chart):
    def draw(w, h):
        if not chart:
            rnd = random.Random(13)
            s = stars(rnd, (0, 0, w, h), 30)
            cx, cy, r = 450, 250, 215
            s += globe(cx, cy, r, tilt=-40, lon0=28)
            s += globe_line(cx, cy, r, rhumb(GA, GB), BLUE, LINE_W + 1, ' stroke-dasharray="14 9"', -40, 28)
            s += globe_line(cx, cy, r, great_circle(GA, GB), RED, LINE_W + 1, "", -40, 28)
            for p in (GA, GB):
                x, y, _ = globe_xy(cx, cy, r, *p, -40, 28)
                s += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="10" fill="#ffffff" stroke="#111827" stroke-width="3"/>'
            rx, ry, _ = globe_xy(cx, cy, r, *rhumb(GA, GB)[30], -40, 28)
            gx, gy, _ = globe_xy(cx, cy, r, *great_circle(GA, GB)[30], -40, 28)
            s += label(rx, ry - 22, "Rhumb line", TXT_L, "#bfdbfe", "middle", halo="#0f1d3d")
            s += label(gx, gy + 52, "Great circle", TXT_L, "#fecaca", "middle", halo="#0f1d3d")
            return s
        s = '<rect x="0" y="0" width="900" height="500" fill="url(#chart_paper)"/>'
        X = lambda lon: 450 + (lon - 27.5) * 5.6   # noqa: E731
        Y = lambda lat: 120 - (merc_y(lat) - merc_y(-40)) * 330   # noqa: E731
        for lon in range(-30, 91, 15):
            s += path(f"M {X(lon):.0f},0 L {X(lon):.0f},500", "none", "#94a3b8", 3)
        for lat in (-20, -35, -50, -60):
            s += path(f"M 0,{Y(lat):.0f} L 900,{Y(lat):.0f}", "none", "#94a3b8", 3)
        s += path("M " + " L ".join(f"{X(lo):.0f},{Y(la):.0f}" for la, lo in rhumb(GA, GB)), "none", BLUE, LINE_W + 1, ' stroke-dasharray="14 9"')
        s += path("M " + " L ".join(f"{X(lo):.0f},{Y(la):.0f}" for la, lo in great_circle(GA, GB)), "none", RED, LINE_W + 1)
        s += label(450, 90, "Rhumb line: straight", TXT_M, NAVY_BLUE, "middle")
        s += label(450, 470, "Great circle: curves to the pole", TXT_M, RED, "middle")
        return s
    return dict(h=GR_H, sky="sky_night" if not chart else "aerial", draw=draw,
                caption="GREAT CIRCLE: THE SHORTEST WAY" if not chart else "MERCATOR: RHUMB LINES ARE STRAIGHT",
                color=RED if not chart else NAVY_BLUE)


@R.add(1782, "great-circle-rhumb-v1", "Great Circles and Rhumb Lines",
       template("A GREAT CIRCLE IS THE SHORTEST ROUTE; A RHUMB LINE KEEPS A CONSTANT TRACK",
                "A RHUMB LINE CUTS EVERY MERIDIAN AT THE SAME ANGLE",
                [("Great circle", "Its plane passes through the Earth's centre; the track keeps changing"),
                 ("Both", "The equator and every meridian"),
                 ("Parallels", "Rhumb lines, but small circles (except the equator)")]),
       h=stack_height([GR_H, GR_H]), w=W)
def _():
    return picture([gr_panel(False), gr_panel(True)])


# ------------------------------------------------------------------ latitude and longitude

LL_H = 480


def ll_panel(distance):
    def draw(w, h):
        rnd = random.Random(17 if distance else 19)
        s = stars(rnd, (0, 0, w, h), 30)
        cx, cy, r, t, l0 = 450, 245, 210, -20, 25
        s += globe(cx, cy, r, t, l0)
        if not distance:
            s += globe_line(cx, cy, r, [(0, lon) for lon in range(-180, 181, 3)], GOLD, 7, "", t, l0)
            s += globe_line(cx, cy, r, [(lat, 0) for lat in range(-90, 91, 3)], RED, 7, "", t, l0)
            s += label(860, 320, "Equator", TXT_L, "#fbbf24", "end", halo="#0f1d3d")
            s += label(40, 70, "Greenwich\nmeridian", TXT_L, "#fca5a5", halo="#0f1d3d")
        else:
            s += globe_line(cx, cy, r, [(lat, 25) for lat in range(-30, -9, 1)], GOLD, 9, "", t, l0)
            s += globe_line(cx, cy, r, [(-62, lon) for lon in range(5, 46, 1)], "#93c5fd", 9, "", t, l0)
            s += label(860, 200, "Along a meridian:\n1° = 60 NM", TXT_L, "#fbbf24", "end", halo="#0f1d3d")
            s += label(40, 460, "Shorter near the poles", TXT_M, "#93c5fd", halo="#0f1d3d")
        return s
    return dict(h=LL_H, sky="sky_night", draw=draw,
                caption="LATITUDE N/S, LONGITUDE E/W" if not distance else "1 MINUTE OF LATITUDE = 1 NM",
                color=NAVY_BLUE)


@R.add(1565, "latitude-longitude-v1", "Latitude and Longitude",
       template("LATITUDE IS MEASURED FROM THE EQUATOR; LONGITUDE FROM THE GREENWICH MERIDIAN",
                "1 MINUTE OF LATITUDE = 1 NM, SO 1° OF LATITUDE = 60 NM",
                [("Latitude", "0° to 90° north or south"),
                 ("Longitude", "0° to 180° east or west"),
                 ("1° of longitude", "60 NM only on the equator; less towards the poles")]),
       h=stack_height([LL_H, LL_H]), w=W)
def _():
    return picture([ll_panel(False), ll_panel(True)])


# ------------------------------------------------------------------ cardinal and quadrantal points

CR_H = 480


def cr_panel(quad):
    def draw(w, h):
        s = ground_above(w, h, seed=101 if quad else 103, river=False, road=False)
        c = (450, 240)
        s += f'<circle cx="{c[0]}" cy="{c[1]}" r="165" fill="#ffffff" fill-opacity="0.8" stroke="#111827" stroke-width="3"/>'
        for k in range(36):
            x0, y0 = compass_xy(*c, 165, k * 10)
            x1, y1 = compass_xy(*c, 165 - (22 if k % 9 == 0 else 12), k * 10)
            s += f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" stroke="#111827" stroke-width="3"/>'
        pts = ((45, "NE 045"), (135, "SE 135"), (225, "SW 225"), (315, "NW 315")) if quad else \
              ((0, "N 360"), (90, "E 090"), (180, "S 180"), (270, "W 270"))
        col = NAVY_BLUE if quad else RED
        for deg, txt in pts:
            s += line(c, compass_xy(*c, 130, deg), col, "nh_navy" if quad else "nh_red")
            tx, ty = compass_xy(*c, 280 if deg % 180 else 200, deg)
            s += label(tx, ty + 14, txt, TXT_M, col, "middle")
        return s
    return dict(h=CR_H, sky="aerial", draw=draw,
                caption="QUADRANTAL: HALFWAY BETWEEN" if quad else "CARDINAL: N, E, S, W",
                color=NAVY_BLUE if quad else RED)


@R.add(1557, "compass-points-v1", "Cardinal and Quadrantal Points",
       template("CARDINAL POINTS: 360° 090° 180° 270°; QUADRANTAL: 045° 135° 225° 315°",
                "DIRECTIONS ARE MEASURED CLOCKWISE FROM NORTH",
                [("Cardinal", "North, east, south, west"),
                 ("Quadrantal", "North-east, south-east, south-west, north-west"),
                 ("Each step", "90° between cardinals; quadrantals 45° from each")]),
       h=stack_height([CR_H, CR_H]), w=W)
def _():
    return picture([cr_panel(False), cr_panel(True)])


# ------------------------------------------------------------------ measuring a track on the chart

MT_H = 520


def mt_panel():
    def draw(w, h):
        s = '<rect x="0" y="0" width="900" height="520" fill="url(#chart_paper)"/>'
        for x in (150, 450, 750):
            s += path(f"M {x},0 L {x + (x - 450) * 0.04:.0f},520", "none", "#94a3b8", 3)
        for y in (130, 390):
            s += path(f"M 0,{y} L 900,{y}", "none", "#94a3b8", 3)
        a, b = (140, 430), (760, 110)
        for p in (a, b):
            s += f'<circle cx="{p[0]}" cy="{p[1]}" r="16" fill="#ffffff" stroke="#111827" stroke-width="4"/>'
        s += line(a, toward(a, b, 18), RED, "nh_red")
        m = (450, a[1] + (b[1] - a[1]) * (450 - a[0]) / (b[0] - a[0]))
        # square protractor centred on the mid meridian
        s += (f'<rect x="{m[0] - 120:.0f}" y="{m[1] - 120:.0f}" width="240" height="240" rx="8" fill="#e0f2fe" '
              f'fill-opacity="0.55" stroke="#0369a1" stroke-width="3"/>')
        for k in range(36):
            x0, y0 = compass_xy(*m, 110, k * 10)
            x1, y1 = compass_xy(*m, 110 - (16 if k % 9 == 0 else 8), k * 10)
            s += f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" stroke="#0369a1" stroke-width="2"/>'
        s += angle_arc(*m, 80, 0, bearing(a, b), RED, ARC_W)
        s += label(470, 60, "Mid meridian", TXT_L, INK)
        s += label(620, 330, "True track", TXT_L, RED)
        return s
    return dict(h=MT_H, sky="aerial", draw=draw, caption="MEASURE FROM THE NEAREST MERIDIAN", color=RED)


@R.add(1816, "measure-track-v1", "Measuring a Track on the Chart",
       template("MEASURE A TRUE TRACK FROM A MERIDIAN, NEAR THE MIDDLE OF THE ROUTE",
                "MERIDIANS POINT TO TRUE NORTH; ON A LAMBERT CHART THEY CONVERGE",
                [("Protractor", "Line it up with the meridian nearest the middle of the track"),
                 ("Magnetic track", "True track + west variation (− east)"),
                 ("Distance", "Measure with the chart scale or the latitude scale (1′ = 1 NM)")]),
       h=stack_height([MT_H]), w=W)
def _():
    return picture([mt_panel()])


# ------------------------------------------------------------------ triangle of velocities (the manual's figure, redrawn)

TV_H = 1000
TV_BOT, TV_TOP = (330, 930), (330, 175)  # the track: straight up the page, as in the manual
TV_HDG_END = (575, 75)                   # heading/TAS: out to the right of the track
TV_DRIFT = math.degrees(math.atan2(TV_HDG_END[0] - TV_BOT[0], TV_BOT[1] - TV_HDG_END[1]))


def vector(a, b, color, mid, at=0.55, w=None):
    """A velocity vector a to b: haloed line with its arrowhead part-way along, as in the manual's figure."""
    w = w or LINE_W
    d = f"M {a[0]:.0f},{a[1]:.0f} L {b[0]:.0f},{b[1]:.0f}"
    s = path(d, "none", "#ffffff", w + 4, ' stroke-opacity="0.85"') + path(d, "none", color, w)
    m = (a[0] + (b[0] - a[0]) * at, a[1] + (b[1] - a[1]) * at)
    return s + path(f"M {a[0]:.0f},{a[1]:.0f} L {m[0]:.0f},{m[1]:.0f}", "none", "none", w, f' marker-end="url(#{mid})"')


def tv_panel():
    def draw(w, h):
        s = f'<rect x="0" y="0" width="{w}" height="{h}" fill="#ffffff"/>'
        s += vector(TV_BOT, TV_HDG_END, INK, "head_true", 0.62)          # HDG/TAS
        s += vector(TV_HDG_END, TV_TOP, BLUE, "nh_blue", 0.3)            # W/V
        s += vector(TV_BOT, TV_TOP, RED, "nh_red", 0.55)                 # TR/GS
        s += angle_arc(*TV_BOT, 330, 0, TV_DRIFT, RED, ARC_W)
        for y in (900, 650, 370):                                        # along its track, nose on its heading
            s += aircraft_top(TV_BOT[0], y, 120, heading=TV_DRIFT)
        s += label(TV_HDG_END[0] - 140, 105, "W/V", TXT_L, BLUE, "middle")
        s += label(300, 530, "TR/GS", TXT_L, RED, "end")
        s += label(525, 420, "HDG/TAS", TXT_L, INK)
        s += label(450, 630, "Drift", TXT_L, RED)
        return s
    return dict(h=TV_H, sky="aerial", draw=draw, caption="HDG/TAS + W/V = TR/GS", color=NAVY_BLUE)


@R.add(1841, "triangle-of-velocities-v2", "Triangle of Velocities",
       template("THE TRIANGLE: HEADING/TAS, TRACK/GS AND W/V",
                "THE WIND JOINS WHERE THE AIRCRAFT POINTS TO WHERE IT GOES",
                [("Air vector", "Heading and TAS"),
                 ("Wind vector", "Wind direction and speed (W/V)"),
                 ("Ground vector", "Track and groundspeed"),
                 ("Drift", "The angle between heading and track")]),
       h=stack_height([TV_H]), w=W)
def _():
    return picture([tv_panel()])
