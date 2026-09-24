"""Diagrams for the four ATG questions rewritten to match the textbook (q2464, q2507, q2592, q2616)."""
import math
import sys
from pathlib import Path
import os
REPO = Path(__file__).resolve().parents[2]
WORK = Path(os.environ.get("ATG_WORK", "/tmp/atg-work"))

import importlib.util

HERE = Path(__file__).parent
_spec = importlib.util.spec_from_file_location("g", HERE / "gen_airframes.py")
g = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(g)
_espec = importlib.util.spec_from_file_location("el", HERE / "gen_electrics.py")
el = importlib.util.module_from_spec(_espec)
_espec.loader.exec_module(el)
header, footer, t, line, poly, polyline = g.header, g.footer, g.t, g.line, g.poly, g.polyline
INK, BODY, MUTED, GOLD, GOLD_DARK, NAVY, RED, BLUE = g.INK, g.BODY, g.MUTED, g.GOLD, g.GOLD_DARK, g.NAVY, g.RED, g.BLUE
GREEN = "#15803d"
OUT = REPO / "public/explanation-images/aircraft-technical-and-general"


def panel(x=40, y=142, w=710, h=444, hl=False):
    fill, stroke, sw = ("#fff8e1", GOLD, 4) if hl else ("#f8fafc", "#cbd5e1", 2)
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>\n'


def method_boxes(items, y=424, h=146):
    """Three side-by-side boxes: (title lines, body lines, highlighted)."""
    s = ""
    for i, (head, body, hl) in enumerate(items):
        x = 56 + i * 230
        s += f'<rect x="{x}" y="{y}" width="218" height="{h}" rx="10" fill="{"#fde68a" if hl else "#ffffff"}" stroke="{GOLD if hl else "#cbd5e1"}" stroke-width="{4 if hl else 2}"/>\n'
        for k, ln in enumerate(head):
            s += t(x + 16, y + 28 + k * 19, ln, 15, 800, INK, "start")
        by = y + 36 + len(head) * 19
        for k, ln in enumerate(body):
            s += t(x + 16, by + k * 20, ln, 13, 400 if not hl else 700, BODY, "start")
    return s


# =====================================================================
# q2464 horizontal stabiliser: up or down force as required
# =====================================================================

def tailplane():
    s = header("HORIZONTAL STABILISER (TAILPLANE)")
    rows = [
        (142, "CG AHEAD OF THE CENTRE OF PRESSURE", (-26, -4), (-4, -30), "down",
         ("LIFT BEHIND THE CG:", "NOSE-DOWN MOMENT", "TAILPLANE FORCE: DOWN")),
        (368, "CG BEHIND THE CENTRE OF PRESSURE", (4, -4), (-22, -30), "up",
         ("LIFT AHEAD OF THE CG:", "NOSE-UP MOMENT", "TAILPLANE FORCE: UP")),
    ]
    for py, title, cgp, cpp, tail_dir, (n1, n2, n3) in rows:
        s += f'<rect x="40" y="{py}" width="710" height="218" rx="12" fill="#fff8e1" stroke="{GOLD}" stroke-width="4"/>\n'
        s += t(60, py + 32, title, 19, 800, INK, "start")
        cx, cy = 300, py + 124
        gs, pg = g.plane(cx, cy, 1.4)
        s += gs
        cg = pg(*cgp)
        cp = pg(*cpp)
        s += g.cg_mark(cg[0], cg[1], 9)
        s += g.force(cg[0], cg[1] + 11, cg[0], cg[1] + 46, "WEIGHT", ly=cg[1] + 64, size=13)
        s += g.force(cp[0], cp[1] - 4, cp[0], cp[1] - 44, "")
        s += t(cp[0] + 10, cp[1] - 24, "LIFT (CP)", 13, 800, RED, "start")
        tail = pg(94, -5)
        if tail_dir == "down":
            s += g.force(tail[0], tail[1] + 5, tail[0], tail[1] + 48, "", GOLD_DARK)
            s += t(tail[0] + 14, tail[1] + 44, "DOWN", 14, 800, GOLD_DARK, "start")
        else:
            s += g.force(tail[0], tail[1] + 50, tail[0], tail[1] + 7, "", GOLD_DARK)
            s += t(tail[0] + 14, tail[1] + 44, "UP", 14, 800, GOLD_DARK, "start")
        s += t(538, cy - 22, n1, 14, 800, INK, "start")
        s += t(538, cy - 2, n2, 14, 800, BODY, "start")
        s += t(538, cy + 30, n3, 15, 800, GOLD_DARK, "start")
    s += g.fact_column([
        ("LONGITUDINAL STABILITY", ["The tailplane keeps the", "aircraft balanced and stable", "in pitch."]),
        ("UP OR DOWN FORCE", ["It generates an upward or a", "downward force, whichever", "is required."]),
        ("NOT DIRECTIONAL", ["Directional (yaw) stability", "comes from the fin."]),
    ])
    s += footer("The horizontal stabiliser gives longitudinal stability, generating an up or down force as required.")
    return s


# =====================================================================
# q2592 low-tension booster coil (spark augmentation)
# =====================================================================

def booster_coil():
    s = header("LOW-TENSION BOOSTER COIL")
    s += panel(hl=True)
    s += t(60, 174, "DURING ENGINE START ONLY", 14, 800, GOLD_DARK, "start")
    wy = 272
    s += el.battery_sym(100, wy)
    s += el.wire([(126, wy), (180, wy)])
    # start switch, closed for the start
    s += f'<circle cx="184" cy="{wy}" r="4" fill="{INK}"/>\n'
    s += line(184, wy, 222, wy - 4, INK, 4)
    s += f'<circle cx="226" cy="{wy}" r="4" fill="{INK}"/>\n'
    s += t(205, wy + 44, "START", 12, 800, INK)
    s += el.wire([(230, wy), (262, wy)])
    # booster coil
    s += f'<rect x="262" y="{wy - 34}" width="128" height="68" rx="10" fill="#fde68a" stroke="{GOLD}" stroke-width="4"/>\n'
    s += t(326, wy - 6, "LOW-TENSION", 13, 800, INK)
    s += t(326, wy + 13, "BOOSTER COIL", 13, 800, INK)
    s += el.wire([(390, wy), (470, wy)], "#b45309", 4)
    s += t(430, wy - 14, "LOW", 12, 800, "#b45309")
    s += t(430, wy + 24, "VOLTAGE", 12, 800, "#b45309")
    # magneto: primary and secondary windings
    s += f'<rect x="470" y="200" width="176" height="144" rx="12" fill="#e2e8f0" stroke="{INK}" stroke-width="3"/>\n'
    s += t(558, 222, "MAGNETO", 13, 800, INK)
    s += line(484, wy, 632, wy, "#94a3b8", 12)
    for k in range(5):
        s += f'<ellipse cx="{492 + k * 10}" cy="{wy}" rx="5" ry="15" fill="none" stroke="#b45309" stroke-width="4"/>\n'
    for k in range(9):
        s += f'<ellipse cx="{580 + k * 5}" cy="{wy}" rx="2.5" ry="21" fill="none" stroke="#1d4ed8" stroke-width="2"/>\n'
    s += t(512, wy + 46, "PRIMARY", 11, 800, "#b45309")
    s += t(600, wy + 46, "SECONDARY", 11, 800, "#1d4ed8")
    s += f'<rect x="478" y="{wy - 26}" width="68" height="52" rx="8" fill="none" stroke="{GOLD}" stroke-width="4"/>\n'
    # to the plug
    s += el.wire([(646, wy), (676, wy)], "#1d4ed8", 3)
    s += f'<rect x="676" y="{wy - 9}" width="30" height="18" rx="3" fill="#94a3b8" stroke="{INK}" stroke-width="2"/>\n'
    for aa in range(0, 360, 60):
        r = math.radians(aa)
        s += line(720 + 3 * math.cos(r), wy + 3 * math.sin(r), 720 + 11 * math.cos(r), wy + 11 * math.sin(r), "#eab308", 2.5)
    s += t(691, wy + 36, "PLUG", 12, 800, INK)
    s += t(395, 388, "Switched off once the engine is running", 14, 700, BODY)
    s += t(56, 414, "THREE METHODS OF SPARK AUGMENTATION", 14, 800, INK, "start")
    s += method_boxes([
        (["LOW-TENSION", "BOOSTER COIL"], ["Low voltage to the", "magneto's primary coil."], True),
        (["HIGH-TENSION", "BOOSTER COIL"], ["High-voltage impulses to", "a trailing brush on the", "distributor rotor."], False),
        (["IMPULSE", "COUPLING"], ["A spring briefly speeds", "up the magneto: a strong,", "retarded spark."], False),
    ])
    s += g.fact_column([
        ("WHY IT IS NEEDED", ["At cranking speed (about", "120 rpm) the magneto's spark", "is too weak."]),
        ("BOOSTER COIL", ["Battery-powered: feeds a low", "voltage into the magneto's", "primary coil."]),
        ("SWITCHED OFF", ["Once the engine starts, the", "magneto's own spark is", "strong enough."]),
    ])
    s += footer("The low-tension booster coil feeds the magneto's primary coil with a low voltage during the start.")
    return s


# =====================================================================
# q2507 warm fuel absorbs more water
# =====================================================================

def thermometer(x, top, bottom, frac, col):
    s = f'<rect x="{x - 9}" y="{top}" width="18" height="{bottom - top}" rx="9" fill="#ffffff" stroke="{INK}" stroke-width="2.5"/>\n'
    s += f'<circle cx="{x}" cy="{bottom + 10}" r="16" fill="{col}" stroke="{INK}" stroke-width="2.5"/>\n'
    lvl = bottom - (bottom - top - 8) * frac
    s += f'<rect x="{x - 4}" y="{lvl:.1f}" width="8" height="{bottom + 4 - lvl:.1f}" fill="{col}"/>\n'
    return s


def water_in_fuel():
    s = header("WARM FUEL ABSORBS MORE WATER")
    specs = [("WARM FUEL", True), ("THE SAME FUEL, COOLED", False)]
    for i, (head, warm) in enumerate(specs):
        px = 48 + i * 362
        s += panel(px, 142, 346, 444, hl=warm)
        s += t(px + 20, 176, head, 16, 800, INK, "start")
        x0, y0, w, h = px + 34, 206, 220, 240
        s += f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" rx="10" fill="#ffffff" stroke="{INK}" stroke-width="4"/>\n'
        s += f'<rect x="{x0 + 4}" y="{y0 + 40}" width="{w - 8}" height="{h - 44}" fill="#93c5fd" fill-opacity="0.5"/>\n'
        # dissolved water: fine, evenly spread
        n = 0
        for r in range(7):
            for c in range(9):
                if warm or (r + c) % 3 == 0:
                    s += f'<circle cx="{x0 + 18 + c * 23 + (r % 2) * 10}" cy="{y0 + 56 + r * 24}" r="2" fill="#1d4ed8" fill-opacity="0.8"/>\n'
                    n += 1
        if warm:
            s += thermometer(px + 296, 226, 410, 0.85, RED)
            s += t(px + 173, 490, "Can hold more dissolved", 15, 800, GOLD_DARK)
            s += t(px + 173, 512, "water: absorbs more", 15, 800, GOLD_DARK)
        else:
            for dx, dy, r in ((60, 120, 6), (120, 160, 7), (170, 110, 5), (90, 200, 7)):
                s += f'<circle cx="{x0 + dx}" cy="{y0 + dy}" r="{r}" fill="#0369a1"/>\n'
                s += line(x0 + dx, y0 + dy + r + 3, x0 + dx, y0 + dy + r + 15, "#0369a1", 2, "aBlue")
            s += f'<rect x="{x0 + 4}" y="{y0 + h - 30}" width="{w - 8}" height="26" fill="#0369a1" fill-opacity="0.85"/>\n'
            s += t(x0 + w / 2, y0 + h - 12, "FREE WATER", 12, 800, "#ffffff")
            s += thermometer(px + 296, 226, 410, 0.2, BLUE)
            s += t(px + 173, 490, "Water comes out of", 15, 800, RED)
            s += t(px + 173, 512, "suspension as droplets", 15, 800, RED)
        s += t(px + 173, 548, "dots = dissolved water", 12, 400, MUTED)
    s += g.fact_column([
        ("WARM FUEL", ["Can hold more dissolved", "water: absorption is more", "likely."]),
        ("AS IT COOLS", ["Overnight or at altitude, the", "water comes out as free", "droplets."]),
        ("THE RISK", ["Free water settles in the", "sump or freezes: drain the", "tanks before flight."]),
    ])
    s += footer("Warm fuel absorbs more water; as it cools, the water comes out of suspension as free droplets.")
    return s


# =====================================================================
# q2616 instantaneous VSI removes the lag
# =====================================================================

def ivsi():
    s = header("INSTANTANEOUS VSI: NO LAG")
    s += panel(hl=True)
    s += t(60, 174, "ENTERING A DESCENT: WHAT EACH INSTRUMENT SHOWS", 14, 800, INK, "start")
    X0, X1, Y0, Y1 = 110, 720, 364, 214
    t0, top = 190, 238
    s += line(X0, Y0, X1, Y0, INK, 2.5, "aDark")
    s += line(X0, Y0, X0, Y1 - 8, INK, 2.5, "aDark")
    s += t(X1 - 4, Y0 + 20, "TIME", 12, 800, MUTED, "end")
    ym = (Y0 + Y1) / 2
    s += t(X0 - 14, ym, "RATE SHOWN", 12, 800, MUTED, "middle", f' transform="rotate(-90 {X0 - 14} {ym:.1f})"')
    s += line(t0, Y0 + 6, t0, Y1 + 6, "#94a3b8", 2, dash="5 4")
    s += t(t0, Y0 + 20, "DESCENT BEGINS", 12, 800, MUTED)

    def curve(tau, x_end):
        pts = [(X0 + 2, Y0 - 2), (t0, Y0 - 2)]
        for k in range(1, 81):
            x = t0 + (x_end - t0) * k / 80
            f = 1 - math.exp(-(x - t0) / tau)
            pts.append((x, Y0 - 2 - (Y0 - 2 - top) * f))
        return pts

    s += polyline(curve(95, X1 - 20), RED, 4)
    s += polyline(curve(9, X1 - 20), GOLD_DARK, 5)
    # actual rate: a step, drawn on top
    s += polyline([(X0 + 2, Y0 - 2), (t0, Y0 - 2), (t0, top), (X1 - 20, top)], INK, 2.5, dash="9 6")
    s += t(X1 - 20, top - 10, "ACTUAL RATE", 12, 800, INK, "end")
    s += t(t0 + 26, top - 10, "IVSI: ALMOST INSTANT", 13, 800, GOLD_DARK, "start")
    s += t(410, 326, "CONVENTIONAL VSI: LAGS", 13, 800, RED, "start")
    s += t(410, 344, "FOR A FEW SECONDS", 13, 800, RED, "start")
    s += t(56, 414, "VSI ERRORS", 14, 800, INK, "start")
    s += method_boxes([
        (["TIME LAG"], ["Conventional VSI: a few", "seconds' delay. The IVSI's", "accelerometer removes it."], True),
        (["MANOEUVRE-", "INDUCED ERROR"], ["Still present: an IVSI", "can even read falsely in", "steep turns."], False),
        (["POSITION ERROR"], ["Still present: both", "instruments use the", "static vent."], False),
    ])
    s += g.fact_column([
        ("CONVENTIONAL VSI", ["The pressure difference", "takes a few seconds to build", "up: the reading lags."]),
        ("IVSI ACCELEROMETER", ["A vertical-acceleration pump", "changes capsule pressure at", "once: instant indication."]),
        ("OTHER ERRORS REMAIN", ["Position and manoeuvre-", "induced errors still apply."]),
    ])
    s += footer("The IVSI's accelerometer overcomes the time lag of the conventional VSI.")
    return s


BATCHES = {
    "airframes-batch-7": {"q2464-tailplane-up-or-down-force": tailplane},
    "electrics-batch-5": {"q2592-low-tension-booster-coil": booster_coil},
    "fuel-batch-3": {"q2507-warm-fuel-absorbs-water": water_in_fuel},
    "pressure-batch-3": {"q2616-ivsi-no-lag": ivsi},
}

if __name__ == "__main__":
    for batch in sys.argv[1:] or BATCHES:
        pub = OUT / batch
        pub.mkdir(parents=True, exist_ok=True)
        for name, fn in BATCHES[batch].items():
            (pub / f"{name}.svg").write_text(fn(), encoding="utf-8")
            print("wrote", batch, name)
