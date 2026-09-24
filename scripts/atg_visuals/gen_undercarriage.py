"""Undercarriage explanation diagrams (ATG)."""
import base64
import io
import math
import sys
from pathlib import Path
import os
REPO = Path(__file__).resolve().parents[2]
WORK = Path(os.environ.get("ATG_WORK", "/tmp/atg-work"))

from PIL import Image

import importlib.util

HERE = Path(__file__).parent
_spec = importlib.util.spec_from_file_location("g", HERE / "gen_airframes.py")
g = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(g)
header, footer, t, line, poly, polyline = g.header, g.footer, g.t, g.line, g.poly, g.polyline
INK, BODY, MUTED, GOLD, GOLD_DARK, NAVY, RED, BLUE, MOVE = g.INK, g.BODY, g.MUTED, g.GOLD, g.GOLD_DARK, g.NAVY, g.RED, g.BLUE, g.MOVE
GREEN = "#15803d"
OUT = REPO / "public/explanation-images/aircraft-technical-and-general"


def embed(path, box, x, y, w):
    im = Image.open(path).convert("RGB").crop(box)
    h = w * im.height / im.width
    buf = io.BytesIO()
    im.save(buf, "PNG", optimize=True)
    data = base64.b64encode(buf.getvalue()).decode()
    return (f'<image x="{x}" y="{y}" width="{w}" height="{h:.1f}" href="data:image/png;base64,{data}" preserveAspectRatio="none"/>\n'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h:.1f}" fill="none" stroke="#cbd5e1" stroke-width="1.5"/>\n'), h


def dim_v(x, y0, y1, col):
    return line(x, y0 + 2, x, y1 - 2, col, 3, "aDark") + line(x, y1 - 2, x, y0 + 2, col, 3, "aDark") + \
        line(x - 12, y0, x + 12, y0, col, 2) + line(x - 12, y1, x + 12, y1, col, 2)


def dim_h(y, x0, x1, col):
    return line(x0 + 2, y, x1 - 2, y, col, 3, "aDark") + line(x1 - 2, y, x0 + 2, y, col, 3, "aDark") + \
        line(x0, y - 12, x0, y + 12, col, 2) + line(x1, y - 12, x1, y + 12, col, 2)


# =====================================================================
# tyre size 28 x 12.00-10 (q2459 OD, q2420 width, q2442 bead)
# =====================================================================

TYRE_PARTS = {
    "OD": ("28", "OUTSIDE DIAMETER", "q2459", "The first figure, 28, is the tyre's overall outside diameter in inches."),
    "WIDTH": ("12.00", "SECTION WIDTH", "q2420", "The middle figure, 12.00, is the tyre's section width in inches."),
    "BEAD": ("10", "BEAD (RIM) DIAMETER", "q2442", "The last figure, 10, is the bead (rim) diameter in inches."),
}


def tyre_size(answer):
    s = header("TYRE SIZE: 28 x 12.00-10")
    s += f'<rect x="40" y="142" width="710" height="444" rx="12" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2"/>\n'
    cols = {k: (GOLD_DARK if k == answer else INK) for k in TYRE_PARTS}
    # size string
    parts = [("28", "OD"), (" x ", None), ("12.00", "WIDTH"), (" - ", None), ("10", "BEAD")]
    x = 395 - 150
    s += f'<text x="{x}" y="196" font-family="{g.F}" font-size="40" font-weight="800">'
    for txt, k in parts:
        fill = cols[k] if k else MUTED
        deco = ' text-decoration="underline"' if k == answer else ""
        s += f'<tspan fill="{fill}"{deco}>{txt}</tspan>'
    s += "</text>\n"
    # side view
    cx, cy, R = 255, 402, 150
    r_rim = R * 10 / 28
    s += f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="#334155" stroke="{INK}" stroke-width="3"/>\n'
    for k in range(1, 4):
        s += f'<circle cx="{cx}" cy="{cy}" r="{R - 12 * k}" fill="none" stroke="#475569" stroke-width="2"/>\n'
    s += f'<circle cx="{cx}" cy="{cy}" r="{r_rim + 12}" fill="#94a3b8" stroke="{INK}" stroke-width="3"/>\n'
    s += f'<circle cx="{cx}" cy="{cy}" r="{r_rim}" fill="#cbd5e1" stroke="{INK}" stroke-width="2.5"/>\n'
    s += f'<circle cx="{cx}" cy="{cy}" r="14" fill="#64748b" stroke="{INK}" stroke-width="2"/>\n'
    s += dim_v(cx - R - 26, cy - R, cy + R, cols["OD"])
    s += t(cx - R - 36, cy - R - 12, "28", 20, 800, cols["OD"], "start")
    s += dim_h(cy, cx - r_rim, cx + r_rim, cols["BEAD"])
    s += t(cx, cy - 16, "10", 20, 800, cols["BEAD"])
    s += t(cx, cy + R + 28, "SIDE VIEW", 14, 800, MUTED)
    # front view (section width)
    fx, fw, fh = 560, R * 2 * 12 / 28, 2 * R
    s += f'<rect x="{fx - fw / 2:.1f}" y="{cy - fh / 2}" width="{fw:.1f}" height="{fh}" rx="{fw / 2 - 6:.1f}" fill="#334155" stroke="{INK}" stroke-width="3"/>\n'
    for k in (-1, 0, 1):
        s += line(fx + k * fw / 4, cy - fh / 2 + 22, fx + k * fw / 4, cy + fh / 2 - 22, "#64748b", 3)
    s += dim_h(cy - fh / 2 - 18, fx - fw / 2, fx + fw / 2, cols["WIDTH"])
    s += t(fx, cy - fh / 2 - 30, "12.00", 20, 800, cols["WIDTH"])
    s += t(fx, cy + R + 28, "FRONT VIEW", 14, 800, MUTED)

    # right column: real sidewall + definitions
    img, h = embed(WORK / "figs" / "p43-2.png", (230, 60, 850, 235), 770, 146, 380)
    s += img
    s += t(960, 146 + h + 20, "Real sidewall marking: 26 x 7.55-13 (same format)", 13, 700, MUTED)
    by = 146 + h + 36
    bh = (586 - by - 16) / 3
    for i, key in enumerate(("OD", "WIDTH", "BEAD")):
        num, name, _, _ = TYRE_PARTS[key]
        y = by + i * (bh + 8)
        ans = key == answer
        fill, stroke, sw = ("#fff8e1", GOLD, 4) if ans else ("#f8fafc", "#cbd5e1", 2)
        s += f'<rect x="770" y="{y:.1f}" width="380" height="{bh:.1f}" rx="12" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>\n'
        s += t(790, y + bh / 2 + 9, num, 26, 800, GOLD_DARK if ans else INK, "start")
        s += t(880, y + bh / 2 + 7, name, 17, 800, INK, "start")
        if ans:
            s += f'<rect x="{1150 - 100}" y="{y + 10:.1f}" width="88" height="24" rx="12" fill="{GOLD}"/>\n'
            s += t(1094, y + 27, "ANSWER", 13, 800, NAVY)
    s += footer(TYRE_PARTS[answer][3])
    return s


# =====================================================================
# tyre wear vs inflation (q2431 under, q2460 over)
# =====================================================================

def tyre_section(cx, gy, kind):
    top = gy - 170
    if kind == "correct":
        d = f"M {cx - 55},{top} C {cx - 82},{top + 20} {cx - 80},{gy - 30} {cx - 62},{gy} L {cx + 62},{gy} C {cx + 80},{gy - 30} {cx + 82},{top + 20} {cx + 55},{top} Z"
        wear = [(cx - 58, cx + 58)]
    elif kind == "under":
        d = f"M {cx - 55},{top + 10} C {cx - 100},{top + 30} {cx - 98},{gy - 20} {cx - 70},{gy} Q {cx},{gy - 16} {cx + 70},{gy} C {cx + 98},{gy - 20} {cx + 100},{top + 30} {cx + 55},{top + 10} Z"
        wear = [(cx - 70, cx - 34), (cx + 34, cx + 70)]
    else:
        d = f"M {cx - 55},{top - 10} C {cx - 76},{top + 10} {cx - 74},{gy - 60} {cx - 40},{gy - 12} Q {cx},{gy + 8} {cx + 40},{gy - 12} C {cx + 74},{gy - 60} {cx + 76},{top + 10} {cx + 55},{top - 10} Z"
        wear = [(cx - 24, cx + 24)]
    s = f'<path d="{d}" fill="#334155" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>\n'
    s += f'<rect x="{cx - 60}" y="{top - 24}" width="120" height="26" rx="4" fill="#94a3b8" stroke="{INK}" stroke-width="2.5"/>\n'
    return s, wear


def tyre_wear(answer):
    title = "UNDER-INFLATED TYRE WEAR" if answer == "under" else "OVER-INFLATED TYRE WEAR"
    s = header(title)
    cols = [("correct", "CORRECT PRESSURE", "Even tread wear", "Full, flat contact patch"),
            ("under", "UNDER-INFLATED", "Wear on both shoulders", "Sidewalls flex and overheat"),
            ("over", "OVER-INFLATED", "Wear in the tread centre", "Less shock absorption")]
    for i, (kind, head, l1, l2) in enumerate(cols):
        px = 48 + i * 372
        ans = kind == answer
        fill, stroke, sw = ("#fff8e1", GOLD, 4) if ans else ("#f8fafc", "#cbd5e1", 2)
        s += f'<rect x="{px}" y="142" width="356" height="444" rx="12" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>\n'
        s += t(px + 20, 178, head, 20, 800, INK, "start")
        if ans:
            s += f'<rect x="{px + 248}" y="158" width="92" height="28" rx="14" fill="{GOLD}"/>\n'
            s += t(px + 294, 177, "ANSWER", 14, 800, NAVY)
        cx, gy = px + 178, 410
        sec, wear = tyre_section(cx, gy, kind)
        s += line(px + 30, gy, px + 326, gy, "#64748b", 3)
        s += sec
        for a, b in wear:
            s += line(a, gy + 6, b, gy + 6, RED if kind != "correct" else GREEN, 8, cap="butt")
        # worn tread strip
        sy = 440
        s += f'<rect x="{cx - 90}" y="{sy}" width="180" height="40" rx="6" fill="#475569" stroke="{INK}" stroke-width="2"/>\n'
        for k in (-1, 0, 1):
            s += line(cx + k * 45, sy + 4, cx + k * 45, sy + 36, "#1e293b", 3)
        if kind == "under":
            for a in (cx - 90, cx + 54):
                s += f'<rect x="{a}" y="{sy}" width="36" height="40" fill="{RED}" fill-opacity="0.75"/>\n'
        elif kind == "over":
            s += f'<rect x="{cx - 24}" y="{sy}" width="48" height="40" fill="{RED}" fill-opacity="0.75"/>\n'
        s += t(cx, sy + 60, "TREAD WEAR PATTERN", 12, 800, MUTED)
        s += t(cx, 536, l1, 17, 800, RED if kind != "correct" else GREEN)
        s += t(cx, 560, l2, 15, 400, BODY)
    foot = ("Under-inflation concentrates wear on the outer edges (shoulders) of the tread."
            if answer == "under" else "Over-inflation concentrates wear in the centre of the tread.")
    s += footer(foot)
    return s


# =====================================================================
# tyre creep (q2437, q2438, q2455)
# =====================================================================

def radial_rect(cx, cy, r0, r1, ang, w, fill, stroke=INK):
    a = math.radians(ang)
    ux, uy = math.cos(a), math.sin(a)
    px, py = -uy * w / 2, ux * w / 2
    pts = [(cx + ux * r0 + px, cy + uy * r0 + py), (cx + ux * r1 + px, cy + uy * r1 + py),
           (cx + ux * r1 - px, cy + uy * r1 - py), (cx + ux * r0 - px, cy + uy * r0 - py)]
    return poly(pts, fill, stroke, 1.5)


def wheel_side(cx, cy, R, r_rim, tyre_mark, rim_mark, valve_bend):
    s = f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="#334155" stroke="{INK}" stroke-width="3"/>\n'
    s += f'<circle cx="{cx}" cy="{cy}" r="{R - 14}" fill="none" stroke="#475569" stroke-width="2"/>\n'
    s += f'<circle cx="{cx}" cy="{cy}" r="{r_rim}" fill="#cbd5e1" stroke="{INK}" stroke-width="3"/>\n'
    s += f'<circle cx="{cx}" cy="{cy}" r="16" fill="#64748b" stroke="{INK}" stroke-width="2"/>\n'
    s += radial_rect(cx, cy, r_rim + 6, R - 6, tyre_mark, 12, "#f8fafc")
    s += radial_rect(cx, cy, r_rim - 22, r_rim, rim_mark, 12, "#f8fafc")
    # valve stem through the rim
    va = math.radians(-35)
    bx, by = cx + math.cos(va) * (r_rim - 4), cy + math.sin(va) * (r_rim - 4)
    ex, ey = cx + math.cos(va) * (r_rim - 30), cy + math.sin(va) * (r_rim - 30)
    if valve_bend:
        s += f'<path d="M {bx:.1f} {by:.1f} Q {bx + 10:.1f} {by + 18:.1f} {bx + 26:.1f} {by + 24:.1f}" fill="none" stroke="{GOLD}" stroke-width="7" stroke-linecap="round"/>\n'
        s += line(ex, ey, bx, by, GOLD, 7)
    else:
        s += line(ex, ey, bx + math.cos(va) * 18, by + math.sin(va) * 18, GOLD, 7)
    return s, (bx, by)


def tyre_creep():
    s = header("TYRE CREEP AND CREEP MARKS")
    panels = [(48, "CREEP MARKS ALIGNED", False), (610, "TYRE HAS CREPT ON THE RIM", True)]
    for px, title, crept in panels:
        fill, stroke, sw = ("#fff8e1", GOLD, 4) if crept else ("#f8fafc", "#cbd5e1", 2)
        s += f'<rect x="{px}" y="142" width="542" height="262" rx="12" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>\n'
        s += t(px + 20, 174, title, 19, 800, INK, "start")
        cx, cy = px + 190, 290
        w, (vx, vy) = wheel_side(cx, cy, 100, 50, -90 + (28 if crept else 0), -90, crept)
        s += w
        if crept:
            a0, a1 = math.radians(-62), math.radians(-18)
            s += f'<path d="M {cx + 118 * math.cos(a0):.1f} {cy + 118 * math.sin(a0):.1f} A 118 118 0 0 1 {cx + 118 * math.cos(a1):.1f} {cy + 118 * math.sin(a1):.1f}" fill="none" stroke="{RED}" stroke-width="4" marker-end="url(#aRedS)"/>\n'
            s += t(px + 330, 224, "MARKS NO LONGER", 15, 800, RED, "start")
            s += t(px + 330, 243, "LINE UP", 15, 800, RED, "start")
            s += t(px + 330, 318, "VALVE STEM DRAGGED", 15, 800, RED, "start")
            s += t(px + 330, 337, "BY THE TUBE: CAN", 15, 800, RED, "start")
            s += t(px + 330, 356, "TEAR OFF", 15, 800, RED, "start")
            s += line(px + 326, 322, vx + 30, vy + 22, RED, 2.5, "aRedS")
        else:
            s += t(px + 330, 224, "PAINT MARK ON TYRE", 15, 800, INK, "start")
            s += t(px + 330, 243, "LINES UP WITH MARK", 15, 800, INK, "start")
            s += t(px + 330, 262, "ON THE WHEEL RIM", 15, 800, INK, "start")
            s += line(px + 326, 230, cx + 8, cy - 80, INK, 2.5, "aDark")
            s += t(px + 330, 318, "INNER-TUBE VALVE", 15, 800, GOLD_DARK, "start")
            s += t(px + 330, 337, "STEM UPRIGHT", 15, 800, GOLD_DARK, "start")
            s += line(px + 326, 322, vx + 16, vy - 8, GOLD_DARK, 2.5, "aDark")
    boxes = [
        ("CAUSE", ["Heavy braking on landing", "makes the tyre slip round", "the wheel rim."]),
        ("RISK", ["The inner tube moves with the", "tyre and its valve can be torn", "off: sudden deflation / blow-out."]),
        ("CHECK", ["Inspect creep marks before", "flight; if out of alignment,", "have the tyre inspected."]),
    ]
    for i, (title, lines_) in enumerate(boxes):
        bx = 48 + i * 372
        s += f'<rect x="{bx}" y="418" width="356" height="168" rx="12" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2"/>\n'
        s += f'<rect x="{bx}" y="418" width="8" height="168" rx="4" fill="{GOLD}"/>\n'
        s += t(bx + 26, 452, title, 19, 800, INK, "start")
        for j, ln in enumerate(lines_):
            s += t(bx + 26, 486 + j * 26, ln, 16, 400, BODY, "start")
    s += footer("Tyre creep (usually from heavy braking) can drag the tube valve until it breaks away.")
    return s


# =====================================================================
# oleo leg (q2448 operation, q2445 under-extension, q2453 over-extension)
# =====================================================================

OLEO = {
    "operation": ("OLEO LEG: HOW IT WORKS",
                  [("GAS SPRING", ["Compressed air or nitrogen", "in the upper chamber absorbs", "the landing load."]),
                   ("OIL DAMPING", ["Fluid forced through a small", "orifice controls the rate of", "compression and rebound."]),
                   ("RESULT", ["A cushioned touchdown", "without bouncing."])],
                  "An oleo leg has hydraulic fluid below and compressed air or nitrogen above."),
    "under": ("OLEO UNDER-EXTENSION",
              [("LOW GAS PRESSURE", ["Too little air or nitrogen", "to hold the leg out: it sits", "lower than normal."]),
               ("LESS TRAVEL", ["Less stroke is left to", "absorb landing shocks."]),
               ("FIX", ["Recharge to the specified", "pressure (and check fluid", "level)."])],
              "The most likely cause of an under-extended oleo leg is low air pressure."),
    "over": ("OLEO OVER-EXTENSION",
             [("HIGH GAS PRESSURE", ["Too much air or nitrogen", "pushes the leg out further", "than normal."]),
              ("HARSH RIDE", ["The strut is stiffer and", "absorbs shocks poorly."]),
              ("FIX", ["Release to the specified", "pressure."])],
             "The most likely cause of an over-extended oleo leg is high air pressure."),
}


def mini_strut(cx, top, exposed, hl):
    s = f'<rect x="{cx - 18}" y="{top}" width="36" height="110" rx="4" fill="#94a3b8" stroke="{INK}" stroke-width="2.5"/>\n'
    s += f'<rect x="{cx - 11}" y="{top + 110}" width="22" height="{exposed}" fill="#e2e8f0" stroke="{INK}" stroke-width="2.5"/>\n'
    wy = top + 110 + exposed + 22
    s += f'<circle cx="{cx}" cy="{wy}" r="24" fill="#334155" stroke="{INK}" stroke-width="2.5"/>\n'
    s += f'<circle cx="{cx}" cy="{wy}" r="8" fill="#cbd5e1"/>\n'
    col = GOLD_DARK if hl else INK
    s += line(cx + 30, top + 112, cx + 30, top + 108 + exposed, col, 2.5)
    s += line(cx + 24, top + 110, cx + 36, top + 110, col, 2)
    s += line(cx + 24, top + 110 + exposed, cx + 36, top + 110 + exposed, col, 2)
    return s


def oleo(answer):
    title, facts, foot = OLEO[answer]
    s = header(title)
    hl_sec = answer == "operation"
    fill, stroke, sw = ("#fff8e1", GOLD, 4) if hl_sec else ("#f8fafc", "#cbd5e1", 2)
    s += f'<rect x="40" y="142" width="370" height="444" rx="12" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>\n'
    s += t(60, 172, "CROSS-SECTION", 17, 800, INK, "start")
    x0, x1 = 118, 218
    s += f'<rect x="{x0 + 30}" y="182" width="40" height="18" fill="#64748b" stroke="{INK}" stroke-width="2"/>\n'
    s += f'<rect x="{x0}" y="200" width="{x1 - x0}" height="260" rx="6" fill="#94a3b8" stroke="{INK}" stroke-width="3"/>\n'
    s += f'<rect x="{x0 + 8}" y="206" width="{x1 - x0 - 16}" height="96" fill="#bfdbfe"/>\n'
    s += f'<rect x="{x0 + 8}" y="302" width="{x1 - x0 - 16}" height="152" fill="#f59e0b" fill-opacity="0.75"/>\n'
    px0, px1 = x0 + 16, x1 - 16
    s += f'<rect x="{px0}" y="352" width="{px1 - px0}" height="180" fill="#e2e8f0" stroke="{INK}" stroke-width="3"/>\n'
    s += f'<rect x="{px0 + 6}" y="366" width="{px1 - px0 - 12}" height="120" fill="#f59e0b" fill-opacity="0.75"/>\n'
    s += f'<rect x="{px0}" y="352" width="{(px1 - px0) / 2 - 7:.1f}" height="14" fill="#475569"/>\n'
    s += f'<rect x="{(px0 + px1) / 2 + 7:.1f}" y="352" width="{(px1 - px0) / 2 - 7:.1f}" height="14" fill="#475569"/>\n'
    s += line((x0 + x1) / 2, 206, (x0 + x1) / 2, 380, "#334155", 5)
    for dx in (-30, 30):
        s += line((x0 + x1) / 2 + dx, 344, (x0 + x1) / 2 + dx, 318, "#b45309", 3, "aDark")
    s += line((x0 + x1) / 2 + 6, 400, (x0 + x1) / 2 + 6, 372, "#b45309", 3, "aDark")
    s += f'<circle cx="{(x0 + x1) / 2}" cy="548" r="34" fill="#334155" stroke="{INK}" stroke-width="3"/>\n'
    s += f'<circle cx="{(x0 + x1) / 2}" cy="548" r="11" fill="#cbd5e1"/>\n'
    lab = GOLD_DARK if hl_sec else INK
    s += t(234, 238, "AIR / NITROGEN", 14, 800, "#1d4ed8", "start")
    s += t(234, 256, "(SPRING)", 13, 700, "#1d4ed8", "start")
    s += t(234, 300, "HYDRAULIC FLUID", 14, 800, "#b45309", "start")
    s += t(234, 318, "(DAMPING)", 13, 700, "#b45309", "start")
    s += t(234, 366, "ORIFICE", 14, 800, lab, "start")
    s += line(230, 362, (x0 + x1) / 2 + 12, 358, lab, 2, "aDark")
    s += t(234, 432, "PISTON", 14, 800, INK, "start")
    s += t(234, 450, "(SLIDING TUBE)", 13, 700, MUTED, "start")

    # extension states
    fill2, stroke2 = "#f8fafc", "#cbd5e1"
    s += f'<rect x="420" y="142" width="330" height="444" rx="12" fill="{fill2}" stroke="{stroke2}" stroke-width="2"/>\n'
    s += t(440, 172, "EXTENSION ON THE GROUND", 16, 800, INK, "start")
    states = [("NORMAL", 58, None), ("LOW AIR", 22, "under"), ("HIGH AIR", 96, "over")]
    for i, (name, ex, key) in enumerate(states):
        cx = 480 + i * 104
        hl = key == answer
        if hl:
            s += f'<rect x="{cx - 46}" y="190" width="92" height="388" rx="10" fill="#fff8e1" stroke="{GOLD}" stroke-width="3"/>\n'
        s += mini_strut(cx, 206, ex, hl)
        s += t(cx, 520, name, 14, 800, GOLD_DARK if hl else INK)
        sub = {"NORMAL": "correct", "LOW AIR": "under-", "HIGH AIR": "over-"}[name]
        s += t(cx, 540, sub, 13, 700, MUTED)
        s += t(cx, 558, "extension" if name != "NORMAL" else "extension", 13, 700, MUTED)
    s += g.fact_column(facts)
    s += footer(foot)
    return s


# =====================================================================
# tubeless tyre (q2757)
# =====================================================================

def tyre_xsec(cx, cy, tube):
    s = ""
    rim = f"M {cx - 92},{cy + 18} Q {cx - 100},{cy + 28} {cx - 88},{cy + 34} L {cx - 78},{cy + 60} L {cx + 78},{cy + 60} L {cx + 88},{cy + 34} Q {cx + 100},{cy + 28} {cx + 92},{cy + 18}"
    s += f'<path d="{rim}" fill="none" stroke="#475569" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>\n'
    tyre = f"M {cx - 84},{cy + 28} C {cx - 150},{cy - 10} {cx - 130},{cy - 128} {cx},{cy - 128} C {cx + 130},{cy - 128} {cx + 150},{cy - 10} {cx + 84},{cy + 28}"
    s += f'<path d="{tyre}" fill="none" stroke="#1f2937" stroke-width="22" stroke-linecap="round"/>\n'
    for k in (-1, 0, 1):
        s += line(cx + k * 40, cy - 142, cx + k * 40, cy - 130, "#94a3b8", 3)
    if tube:
        s += f'<ellipse cx="{cx}" cy="{cy - 44}" rx="92" ry="64" fill="none" stroke="#b45309" stroke-width="7"/>\n'
        s += line(cx, cy + 20, cx, cy + 86, GOLD, 7)
    else:
        s += line(cx + 40, cy + 60, cx + 40, cy + 92, GOLD, 7)
        for sx in (-1, 1):
            s += f'<circle cx="{cx + sx * 88}" cy="{cy + 30}" r="10" fill="none" stroke="{GREEN}" stroke-width="4"/>\n'
        s += f'<circle cx="{cx}" cy="{cy + 60}" r="7" fill="{GREEN}"/>\n'
    return s


def tubeless():
    s = header("TUBELESS TYRE")
    for i, (title, tube) in enumerate((("TUBE-TYPE TYRE", True), ("TUBELESS TYRE", False))):
        px = 48 + i * 562
        ans = not tube
        fill, stroke, sw = ("#fff8e1", GOLD, 4) if ans else ("#f8fafc", "#cbd5e1", 2)
        s += f'<rect x="{px}" y="142" width="542" height="262" rx="12" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>\n'
        s += t(px + 20, 174, title, 19, 800, INK, "start")
        cx, cy, k = px + 170, 318, 0.8
        S = lambda dx, dy, cx=cx, cy=cy: (cx + k * dx, cy + k * dy)
        s += f'<g transform="translate({cx},{cy}) scale({k}) translate({-cx},{-cy})">\n' + tyre_xsec(cx, cy, tube) + "</g>\n"
        if tube:
            s += t(px + 340, 230, "INNER TUBE HOLDS", 15, 800, "#b45309", "start")
            s += t(px + 340, 249, "THE AIR", 15, 800, "#b45309", "start")
            s += line(px + 336, 236, *S(88, -60), "#b45309", 2.5, "aDark")
            s += t(px + 340, 330, "VALVE ON THE TUBE", 15, 800, GOLD_DARK, "start")
            s += line(px + 336, 334, *S(8, 76), GOLD_DARK, 2.5, "aDark")
        else:
            s += t(px + 340, 230, "NO INNER TUBE", 15, 800, INK, "start")
            s += t(px + 340, 290, "BEADS SEAL AIRTIGHT", 15, 800, GREEN, "start")
            s += t(px + 340, 309, "AGAINST THE RIM", 15, 800, GREEN, "start")
            s += line(px + 336, 296, *S(98, 30), GREEN, 2.5, "aDark")
            s += t(px + 340, 360, "SEALED RIM + VALVE", 15, 800, GOLD_DARK, "start")
            s += line(px + 336, 364, *S(48, 84), GOLD_DARK, 2.5, "aDark")
    rows = [
        ("1", "The wheel rim must provide an airtight seal", True),
        ("2", "An inner tube is required to retain pressure", False),
        ("3", "No friction between an inner tube and the tyre", True),
        ("4", "Damage to the rim sealing surface can cause leakage", True),
    ]
    for i, (n, txt, ok) in enumerate(rows):
        bx = 48 + (i % 2) * 562
        by = 418 + (i // 2) * 86
        s += f'<rect x="{bx}" y="{by}" width="542" height="76" rx="12" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2"/>\n'
        s += g.badge(bx + 32, by + 38, n)
        s += t(bx + 60, by + 44, txt, 15, 700, INK, "start")
        col = GREEN if ok else RED
        s += f'<rect x="{bx + 446}" y="{by + 24}" width="80" height="28" rx="14" fill="{col}"/>\n'
        s += t(bx + 486, by + 43, "TRUE" if ok else "FALSE", 14, 800, "#ffffff")
    s += footer("Statements 1, 3 and 4 are correct: a tubeless tyre seals against an airtight rim.")
    return s


# =====================================================================
# nose leg: torque links (q2441, q2766), worn links -> shimmy (q2444), shimmy damper (q2418)
# =====================================================================

NOSE = {
    "torque": ("TORQUE (SCISSOR) LINKS",
               [("JOIN THE STRUT PARTS", ["Upper link on the cylinder,", "lower link on the piston", "and fork."]),
                ("STOP ROTATION", ["The piston and nose wheel", "cannot turn inside the", "cylinder."]),
                ("KEEP ALIGNMENT", ["The wheel stays aligned while", "the oleo still compresses", "up and down."])],
               "Torque links stop the shock-strut piston and nose wheel rotating within the cylinder."),
    "worn": ("SHIMMY: WORN TORQUE LINKS",
             [("PLAY IN THE LINKS", ["Worn pins or bushes let the", "wheel twist on the strut."]),
              ("SHIMMY BUILDS UP", ["The nose wheel oscillates", "rapidly side to side while", "taxying."]),
              ("ACTION", ["Have the torque links and", "shimmy damper inspected."])],
             "Nose-wheel shimmy whilst taxying indicates the torque links are worn or have failed."),
    "damper": ("SHIMMY DAMPER",
               [("WHAT IT IS", ["A small hydraulic damper", "between the fixed strut and", "the steerable part."]),
                ("HOW IT WORKS", ["Fluid through an orifice resists", "rapid movement but allows", "normal steering."]),
                ("RESULT", ["Side-to-side oscillation", "(shimmy) cannot build up."])],
               "Nose-wheel shimmy is controlled by a shimmy damper."),
}


def nose_leg(answer):
    title, facts, foot = NOSE[answer]
    s = header(title)
    s += f'<rect x="40" y="142" width="710" height="444" rx="12" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2"/>\n'
    s += t(60, 172, "NOSE LEG (SIDE VIEW)", 16, 800, INK, "start")
    # fuselage structure
    s += f'<rect x="90" y="186" width="330" height="20" fill="#e2e8f0" stroke="{INK}" stroke-width="2.5"/>\n'
    for k in range(12):
        s += line(96 + k * 27, 204, 110 + k * 27, 188, "#94a3b8", 2)
    cx = 260
    s += f'<rect x="{cx - 22}" y="206" width="44" height="170" rx="4" fill="#94a3b8" stroke="{INK}" stroke-width="3"/>\n'
    s += f'<rect x="{cx - 28}" y="236" width="56" height="16" rx="3" fill="#64748b" stroke="{INK}" stroke-width="2"/>\n'
    s += f'<rect x="{cx - 13}" y="376" width="26" height="92" fill="#e2e8f0" stroke="{INK}" stroke-width="3"/>\n'
    s += f'<path d="M {cx - 40},{520} L {cx - 40},{470} L {cx + 40},{470} L {cx + 40},{520}" fill="none" stroke="#475569" stroke-width="9" stroke-linejoin="round"/>\n'
    s += f'<circle cx="{cx}" cy="520" r="58" fill="#334155" stroke="{INK}" stroke-width="3"/>\n'
    s += f'<circle cx="{cx}" cy="520" r="20" fill="#cbd5e1" stroke="{INK}" stroke-width="2"/>\n'
    # torque links
    tl = answer in ("torque", "worn")
    col = GOLD if tl else "#64748b"
    p1, p2, p3 = (cx + 22, 356), (cx + 78, 408), (cx + 22, 462)
    for a, b in ((p1, p2), (p2, p3)):
        s += line(a[0], a[1], b[0], b[1], INK, 15)
        s += line(a[0], a[1], b[0], b[1], col, 9)
    for p in (p1, p2, p3):
        s += f'<circle cx="{p[0]}" cy="{p[1]}" r="7" fill="#ffffff" stroke="{INK}" stroke-width="2.5"/>\n'
    if answer == "worn":
        s += f'<circle cx="{p2[0]}" cy="{p2[1]}" r="18" fill="none" stroke="{RED}" stroke-width="3" stroke-dasharray="5 4"/>\n'
        s += t(p2[0] + 28, p2[1] + 50, "WORN PINS:", 14, 800, RED, "start")
        s += t(p2[0] + 28, p2[1] + 68, "FREE PLAY", 14, 800, RED, "start")
    s += t(cx + 100, 352, "TORQUE", 15, 800, GOLD_DARK if tl else INK, "start")
    s += t(cx + 100, 370, "LINKS", 15, 800, GOLD_DARK if tl else INK, "start")
    s += line(cx + 104, 376, p2[0] + 4, p2[1] - 10, GOLD_DARK if tl else INK, 2.5, "aDark")
    # shimmy damper between fixed structure and steering collar
    dm = answer == "damper"
    dcol = GOLD if dm else "#64748b"
    s += f'<rect x="120" y="236" width="64" height="18" rx="6" fill="{dcol}" stroke="{INK}" stroke-width="2.5"/>\n'
    s += line(184, 245, cx - 28, 245, INK, 5)
    s += line(110, 206, 120, 245, INK, 4)
    s += t(92, 294, "SHIMMY DAMPER", 15, 800, GOLD_DARK if dm else INK, "start")
    s += line(140, 276, 150, 258, GOLD_DARK if dm else INK, 2.5, "aDark")
    s += t(cx + 36, 232, "STEERING COLLAR", 13, 700, MUTED, "start")
    s += t(cx + 30, 300, "OLEO CYLINDER", 13, 700, MUTED, "start")
    s += t(cx - 30, 448, "PISTON", 13, 700, MUTED, "end")

    # plan-view inset
    ix, iy = 590, 370
    s += f'<rect x="460" y="190" width="272" height="380" rx="10" fill="#ffffff" stroke="#cbd5e1" stroke-width="2"/>\n'
    s += t(596, 216, "VIEW FROM ABOVE", 14, 800, MUTED)
    if answer == "torque":
        s += f'<circle cx="{ix}" cy="{iy - 40}" r="34" fill="#94a3b8" stroke="{INK}" stroke-width="3"/>\n'
        s += f'<circle cx="{ix}" cy="{iy - 40}" r="18" fill="#e2e8f0" stroke="{INK}" stroke-width="2.5"/>\n'
        a0, a1 = math.radians(200), math.radians(340)
        s += f'<path d="M {ix + 54 * math.cos(a0):.1f} {iy - 40 + 54 * math.sin(a0):.1f} A 54 54 0 0 1 {ix + 54 * math.cos(a1):.1f} {iy - 40 + 54 * math.sin(a1):.1f}" fill="none" stroke="{RED}" stroke-width="4" marker-end="url(#aRedS)"/>\n'
        s += line(ix - 42, iy - 112, ix + 42, iy - 70, RED, 5)
        s += t(ix, iy + 34, "PISTON CANNOT ROTATE", 15, 800, RED)
        s += t(ix, iy + 54, "IN THE CYLINDER", 15, 800, RED)
        s += t(ix, iy + 110, "Wheel stays aligned with", 14, 400, BODY)
        s += t(ix, iy + 130, "the steering input", 14, 400, BODY)
    else:
        for ang, op in ((-16, 0.35), (16, 0.35), (0, 1)):
            a = math.radians(ang)
            s += f'<rect x="{ix - 15}" y="{iy - 70}" width="30" height="100" rx="12" fill="#334155" fill-opacity="{op}" stroke="{INK}" stroke-opacity="{op}" stroke-width="2.5" transform="rotate({ang} {ix} {iy - 20})"/>\n'
        s += f'<path d="M {ix - 46},{iy - 92} Q {ix},{iy - 118} {ix + 46},{iy - 92}" fill="none" stroke="{RED}" stroke-width="4" marker-end="url(#aRedS)"/>\n'
        s += f'<path d="M {ix + 46},{iy - 100} Q {ix},{iy - 126} {ix - 46},{iy - 100}" fill="none" stroke="{RED}" stroke-width="4" marker-end="url(#aRedS)"/>\n'
        pts = [(ix + 14 * math.sin(k * 1.1), iy + 40 + k * 7) for k in range(0, 16)]
        s += polyline(pts, "#64748b", 3)
        s += t(ix, iy + 170, "SHIMMY: RAPID SIDE-TO-", 14, 800, RED)
        s += t(ix, iy + 188, "SIDE OSCILLATION", 14, 800, RED)
    s += g.fact_column(facts)
    s += footer(foot)
    return s


BATCHES = {
    "undercarriage-batch-1": {
        "q2459-tyre-size-outside-diameter": lambda: tyre_size("OD"),
        "q2420-tyre-size-section-width": lambda: tyre_size("WIDTH"),
        "q2442-tyre-size-bead-diameter": lambda: tyre_size("BEAD"),
        "q2431-under-inflated-tyre-wear": lambda: tyre_wear("under"),
        "q2460-over-inflated-tyre-wear": lambda: tyre_wear("over"),
    },
    "undercarriage-batch-2": {
        "q2437-tyre-creep": tyre_creep,
        "q2448-oleo-leg-operation": lambda: oleo("operation"),
        "q2445-oleo-under-extension": lambda: oleo("under"),
        "q2453-oleo-over-extension": lambda: oleo("over"),
        "q2757-tubeless-tyre": tubeless,
    },
    "undercarriage-batch-3": {
        "q2441-torque-links": lambda: nose_leg("torque"),
        "q2444-shimmy-worn-torque-links": lambda: nose_leg("worn"),
        "q2418-shimmy-damper": lambda: nose_leg("damper"),
    },
}

EMBEDS_IMAGE = {"q2459-tyre-size-outside-diameter", "q2420-tyre-size-section-width", "q2442-tyre-size-bead-diameter"}

if __name__ == "__main__":
    for batch in sys.argv[1:] or BATCHES:
        pub = OUT / batch
        ext = WORK / "ext-svg" / batch
        pub.mkdir(parents=True, exist_ok=True)
        ext.mkdir(parents=True, exist_ok=True)
        for name, fn in BATCHES[batch].items():
            (ext if name in EMBEDS_IMAGE else pub).joinpath(f"{name}.svg").write_text(fn(), encoding="utf-8")
            print("wrote", batch, name)
