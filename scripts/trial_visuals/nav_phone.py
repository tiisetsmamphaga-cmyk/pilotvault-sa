"""Navigation explanation pictures, phone-first (docs/EXPLANATION_ILLUSTRATION_STANDARD.md), built from scene.py.

The aircraft is the measured top view in aircraft.py; the ground is scene.ground_above. Each picture shows the
idea; the KEY FACT card on each question carries its own numbers.
"""
from common import Registry
from kit import template
import math

from scene import (BLUE, flow, runway_above, aircraft, beacon_side, ndb_symbol, terrain, vor_rose, CAPTION, COMMON_DEFS, GOLD, INK, NAVY_BLUE, RED, TXT_L, TXT_M, W, aircraft_top,
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
        bx = 200
        s += beacon_side(bx, GROUND, 80)
        ac = (300, 120) if close else (760, 300)
        top = (bx, GROUND - 80)
        s += line((ac[0], GROUND - 6), (bx + 14, GROUND - 6), INK, None, 4, "12 9")
        s += path(f"M {ac[0]},{ac[1] + 25} L {ac[0]},{GROUND - 10}", "none", "#64748b", 3, ' stroke-dasharray="6 8"')
        s += line(top, toward(top, ac, 50), GOLD, None)
        s += aircraft(*ac, 150, 0, nose_right=True)
        if close:
            s += label(420, 90, "Slant range", TXT_L, "#9a5b00")
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
        s += beacon_side(130, GROUND, 90)
        for k, y in enumerate((GROUND - 25, GROUND - 60, GROUND - 95)):
            s += flow([(190, y), (640, y)], BLUE if not night else "#7cc4ff", "nh_blue", LINE_W, 1 - k * 0.2)
        s += aircraft(760, 250, 150, 0, nose_right=False)
        if night:
            sky = [(150, GROUND - 100), (300, 200), (420, 95), (560, 150), (700, 230)]
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
