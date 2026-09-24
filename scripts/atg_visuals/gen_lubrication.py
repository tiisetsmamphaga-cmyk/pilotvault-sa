"""Lubrication-system explanation diagrams (ATG)."""
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
header, footer, t, line, poly, polyline = g.header, g.footer, g.t, g.line, g.poly, g.polyline
INK, BODY, MUTED, GOLD, GOLD_DARK, NAVY, RED, BLUE = g.INK, g.BODY, g.MUTED, g.GOLD, g.GOLD_DARK, g.NAVY, g.RED, g.BLUE
GREEN = "#15803d"
OIL = "#d97706"
OUT = REPO / "public/explanation-images/aircraft-technical-and-general"


def pipe(pts, hl=False):
    s = polyline(pts, INK, 11)
    s += polyline(pts, "#fbbf24" if hl else "#f59e0b", 6)
    return s


def flow(x1, y1, x2, y2):
    return line(x1, y1, x2, y2, "#92400e", 3, "aDark")


def gauge(cx, cy, letter, label, hl, needle_deg=-40, face="#1f2937"):
    ring = GOLD if hl else "#94a3b8"
    s = f'<circle cx="{cx}" cy="{cy}" r="30" fill="{face}" stroke="{ring}" stroke-width="{5 if hl else 3}"/>\n'
    a = math.radians(needle_deg - 90)
    s += line(cx, cy, cx + 22 * math.cos(a), cy + 22 * math.sin(a), "#f8fafc", 3)
    s += t(cx, cy + 20, letter, 12, 800, "#f8fafc")
    s += t(cx, cy - 40, label, 13, 800, GOLD_DARK if hl else INK)
    return s


# =====================================================================
# wet sump schematic (q2543 sump, q2529 pressure gauge, q2531 cooler, q2534 temperature)
# =====================================================================

WET = {
    "sump": ("WET-SUMP LUBRICATION",
             [("OIL STORED IN THE SUMP", ["The engine's own sump is", "the oil reservoir."]),
              ("PRESSURE PUMP", ["A gear pump draws oil from", "the sump and feeds the", "engine's oil galleries."]),
              ("RETURNS BY GRAVITY", ["Oil drains back into the", "sump after lubricating."])],
             "In a wet-sump system oil is stored in the sump and distributed by a pressure pump."),
    "pressure": ("WHERE OIL PRESSURE IS MEASURED",
                 [("AFTER THE PUMP", ["The gauge is fed from the", "pressure side of the system."]),
                  ("BEFORE THE ENGINE", ["It shows the pressure being", "delivered to the bearings."]),
                  ("LOW READING WARNS OF", ["pump failure, low oil", "or very hot, thin oil."])],
                 "The oil pressure gauge is connected before the oil enters the engine components."),
    "cooler": ("OIL COOLER POSITION",
               [("COOLED BEFORE USE", ["Oil passes through the", "cooler before it reaches", "the engine components."]),
                ("RAM AIR", ["Air through the cooler", "removes heat from the oil."]),
                ("WHY", ["Cooler oil keeps its", "viscosity and can absorb", "more engine heat."])],
               "The oil passes through the oil cooler before being fed to the engine components."),
    "temp": ("WHERE OIL TEMPERATURE IS MEASURED",
             [("AFTER THE COOLER", ["The sensor reads oil that", "has just left the cooler."]),
              ("OIL ABOUT TO BE USED", ["It shows the temperature of", "the oil entering the engine."]),
              ("WATCH FOR", ["High temperature with low", "pressure: suspect low", "oil quantity."])],
             "Oil temperature is usually measured after the oil leaves the oil cooler."),
}


def wet_sump(answer):
    title, facts, foot = WET[answer]
    s = header(title)
    s += f'<rect x="40" y="142" width="710" height="444" rx="12" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2"/>\n'
    # engine and sump
    s += f'<rect x="80" y="200" width="250" height="220" rx="14" fill="#cbd5e1" stroke="{INK}" stroke-width="3"/>\n'
    for k in range(3):
        s += f'<rect x="{104 + k * 76}" y="222" width="54" height="92" rx="6" fill="#94a3b8" stroke="{INK}" stroke-width="2"/>\n'
    s += line(96, 356, 314, 356, "#64748b", 6)
    s += t(205, 386, "ENGINE BEARINGS", 13, 800, INK)
    sump_hl = answer == "sump"
    s += f'<path d="M 96,420 L 314,420 L 296,508 L 114,508 Z" fill="#e2e8f0" stroke="{GOLD if sump_hl else INK}" stroke-width="{5 if sump_hl else 3}"/>\n'
    s += f'<path d="M 104,456 L 306,456 L 296,504 L 114,504 Z" fill="{OIL}" fill-opacity="0.85"/>\n'
    s += t(205, 540, "SUMP: OIL RESERVOIR", 14, 800, GOLD_DARK if sump_hl else INK)
    for x in (140, 205, 270):
        s += line(x, 398, x, 446, "#92400e", 2.5, "aDark")
    # circuit: sump -> pump -> filter -> cooler -> T, P -> gallery
    s += pipe([(270, 490), (360, 490), (400, 490)])
    s += f'<circle cx="420" cy="490" r="20" fill="#475569" stroke="{INK}" stroke-width="2.5"/>\n'
    s += f'<circle cx="452" cy="490" r="20" fill="#475569" stroke="{INK}" stroke-width="2.5"/>\n'
    s += t(424, 536, "PRESSURE PUMP", 13, 800, INK)
    s += pipe([(472, 490), (520, 490), (520, 440)])
    s += f'<rect x="500" y="400" width="40" height="40" rx="6" fill="#fde68a" stroke="{INK}" stroke-width="2.5"/>\n'
    s += t(478, 424, "FILTER", 12, 800, INK, "end")
    s += pipe([(520, 400), (520, 360), (600, 360)])
    cool_hl = answer == "cooler"
    s += f'<rect x="600" y="320" width="76" height="80" rx="6" fill="#fbcfe8" stroke="{GOLD if cool_hl else INK}" stroke-width="{5 if cool_hl else 2.5}"/>\n'
    for k in range(6):
        s += line(610 + k * 11, 326, 610 + k * 11, 394, "#be185d", 2)
    s += t(638, 424, "OIL COOLER", 13, 800, GOLD_DARK if cool_hl else INK)
    for yy in (336, 360, 384):
        s += line(738, yy, 690, yy, BLUE, 3.5, "aBlue")
    s += t(716, 314, "RAM AIR", 12, 800, BLUE)
    s += pipe([(638, 320), (638, 260), (330, 260)])
    # sensors after the cooler, before the engine
    s += line(560, 260, 560, 232, INK, 3)
    s += gauge(560, 202, "T", "OIL TEMP", answer == "temp")
    s += line(430, 260, 430, 232, INK, 3)
    s += gauge(430, 202, "P", "OIL PRESS", answer == "pressure")
    for x1, y1, x2, y2 in ((330, 490, 368, 490), (520, 468, 520, 448), (560, 360, 590, 360), (638, 300, 638, 272), (500, 260, 470, 260), (390, 260, 350, 260)):
        s += flow(x1, y1 - 12 if y1 == y2 else y1, x2, y2 - 12 if y1 == y2 else y2) if y1 == y2 else flow(x1 + 12, y1, x2 + 12, y2)
    # relief valve returning to sump
    s += pipe([(505, 490), (505, 560), (300, 560), (300, 508)])
    s += f'<rect x="493" y="516" width="24" height="30" rx="4" fill="#e2e8f0" stroke="{INK}" stroke-width="2"/>\n'
    s += t(527, 568, "RELIEF VALVE", 11, 800, MUTED, "start")
    hl_note = {
        "pressure": ("MEASURED HERE: AFTER THE PUMP,", "BEFORE THE ENGINE COMPONENTS"),
        "cooler": ("OIL IS COOLED HERE, BEFORE", "IT IS FED TO THE ENGINE"),
        "temp": ("MEASURED HERE: AFTER", "LEAVING THE OIL COOLER"),
        "sump": ("OIL STORED IN THE SUMP;", "PUMP FEEDS THE ENGINE"),
    }[answer]
    s += t(60, 170, hl_note[0], 14, 800, GOLD_DARK, "start")
    s += t(60, 188, hl_note[1], 14, 800, GOLD_DARK, "start")
    s += g.fact_column(facts)
    s += footer(foot)
    return s


# =====================================================================
# q2518 high oil temperature with low oil pressure
# =====================================================================

def dial(cx, cy, title, lo, hi, marks, green, needle, red_zone=None):
    s = f'<rect x="{cx - 130}" y="{cy - 110}" width="260" height="190" rx="14" fill="#1f2937" stroke="{INK}" stroke-width="3"/>\n'
    R = 90

    def pt(v, r):
        a = math.radians(210 - (v - lo) / (hi - lo) * 240)
        return cx + r * math.cos(a), cy - r * math.sin(a)

    def arc(v0, v1, col, w):
        a = pt(v0, R)
        b = pt(v1, R)
        large = 1 if (v1 - v0) / (hi - lo) * 240 > 180 else 0
        return f'<path d="M {a[0]:.1f} {a[1]:.1f} A {R} {R} 0 {large} 1 {b[0]:.1f} {b[1]:.1f}" fill="none" stroke="{col}" stroke-width="{w}"/>\n'

    s += arc(lo, hi, "#475569", 10)
    s += arc(green[0], green[1], "#22c55e", 12)
    if red_zone:
        s += arc(red_zone[0], red_zone[1], "#ef4444", 12)
    for v in marks:
        a, b = pt(v, R - 14), pt(v, R + 6)
        s += line(a[0], a[1], b[0], b[1], "#e2e8f0", 2)
        p = pt(v, R - 32)
        s += t(p[0], p[1] + 5, str(v), 13, 700, "#e2e8f0")
    n = pt(needle, R - 12)
    s += line(cx, cy, n[0], n[1], "#f8fafc", 5)
    s += f'<circle cx="{cx}" cy="{cy}" r="8" fill="#f8fafc"/>\n'
    s += t(cx, cy + 56, title, 15, 800, "#f8fafc")
    return s


def q2518():
    s = header("HIGH OIL TEMPERATURE + LOW OIL PRESSURE")
    s += f'<rect x="40" y="142" width="710" height="444" rx="12" fill="#fff8e1" stroke="{GOLD}" stroke-width="4"/>\n'
    s += dial(215, 300, "OIL TEMP", 50, 250, [50, 100, 150, 200, 250], (100, 200), 238, (220, 250))
    s += dial(575, 300, "OIL PRESS", 0, 100, [0, 25, 50, 75, 100], (60, 90), 12)
    s += t(215, 416, "RISING: HIGH", 17, 800, RED)
    s += t(575, 416, "FALLING: LOW", 17, 800, RED)
    s += t(395, 470, "TOGETHER THESE POINT TO", 18, 800, INK)
    s += t(395, 500, "A LOW OIL SUPPLY", 26, 800, GOLD_DARK)
    s += t(395, 540, "Less oil to carry the heat away, and the pump", 15, 400, BODY)
    s += t(395, 562, "starts to draw air so pressure cannot be held.", 15, 400, BODY)
    s += g.fact_column([
        ("HIGH TEMPERATURE", ["Less oil is circulating to", "absorb and carry away", "engine heat."]),
        ("LOW PRESSURE", ["The pump cannot maintain", "flow; hot oil also thins."]),
        ("ACTION", ["Reduce power, land as soon", "as possible and be ready", "for engine failure."]),
    ])
    s += footer("High oil temperature together with low oil pressure indicates a low oil supply.")
    return s


# =====================================================================
# spark plug deposits (q2528 normal, q2557 rich)
# =====================================================================

def plug(cx, top, deposit, wet=False):
    s = f'<path d="M {cx - 52},{top} L {cx + 52},{top} L {cx + 52},{top + 150} L {cx - 52},{top + 150} Z" fill="#94a3b8" stroke="{INK}" stroke-width="3"/>\n'
    for k in range(6):
        s += line(cx - 52, top + 18 + k * 22, cx + 52, top + 8 + k * 22, "#64748b", 3)
    s += f'<path d="M {cx - 36},{top + 150} L {cx - 36},{top + 176} L {cx + 36},{top + 176} L {cx + 36},{top + 150} Z" fill="#94a3b8" stroke="{INK}" stroke-width="2.5"/>\n'
    s += f'<path d="M {cx - 26},{top + 176} L {cx - 12},{top + 236} L {cx + 12},{top + 236} L {cx + 26},{top + 176} Z" fill="{deposit}" stroke="{INK}" stroke-width="2.5"/>\n'
    s += f'<rect x="{cx - 5}" y="{top + 236}" width="10" height="16" fill="#cbd5e1" stroke="{INK}" stroke-width="2"/>\n'
    s += f'<path d="M {cx + 36},{top + 176} L {cx + 36},{top + 266} L {cx - 2},{top + 266}" fill="none" stroke="#475569" stroke-width="8" stroke-linejoin="round"/>\n'
    if wet:
        for dx, dy in ((-18, 196), (10, 214), (-4, 228)):
            s += f'<ellipse cx="{cx + dx}" cy="{top + dy}" rx="5" ry="8" fill="#0f172a" fill-opacity="0.8"/>\n'
    return s


def spark_plugs(answer):
    title = {"normal": "SPARK PLUG: NORMAL CONDITION", "rich": "SPARK PLUG: RICH MIXTURE", "oil": "SPARK PLUG: OIL FOULING"}[answer]
    s = header(title)
    cols = [("normal", "NORMAL", "#d6cbb8", False, "Light grey / tan", "coating"),
            ("rich", "RICH MIXTURE", "#1f2937", False, "Dry, black, powdery", "carbon (soot)"),
            ("oil", "OIL FOULED", "#0b0f19", True, "Wet, black, oily", "deposits")]
    for i, (key, head, dep, wet, l1, l2) in enumerate(cols):
        px = 48 + i * 372
        ans = key == answer
        fill, stroke, sw = ("#fff8e1", GOLD, 4) if ans else ("#f8fafc", "#cbd5e1", 2)
        s += f'<rect x="{px}" y="142" width="356" height="444" rx="12" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>\n'
        s += t(px + 20, 178, head, 20, 800, INK, "start")
        if ans:
            s += f'<rect x="{px + 248}" y="158" width="92" height="28" rx="14" fill="{GOLD}"/>\n'
            s += t(px + 294, 177, "ANSWER", 14, 800, NAVY)
        s += plug(px + 178, 196, dep, wet)
        s += t(px + 178, 500, l1, 17, 800, GOLD_DARK if ans else INK)
        s += t(px + 178, 522, l2, 17, 800, GOLD_DARK if ans else INK)
        cause = {"normal": "Correct mixture and temperature", "rich": "Incomplete combustion", "oil": "Worn rings or guides"}[key]
        s += t(px + 178, 556, cause, 14, 400, BODY)
    foot = {"normal": "A light grey coating on the firing end indicates normal engine operation.",
            "rich": "Dry, black, powdery carbon on the firing end indicates an excessively rich mixture.",
            "oil": "Black, oily deposits on the firing end indicate oil entering the combustion chamber and burning."}[answer]
    s += footer(foot)
    return s


# =====================================================================
# q2521 crankcase breather
# =====================================================================

def q2521():
    s = header("ENGINE BREATHER")
    s += f'<rect x="40" y="142" width="710" height="444" rx="12" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2"/>\n'
    # crankcase with one cylinder
    s += f'<rect x="150" y="190" width="120" height="170" rx="6" fill="#cbd5e1" stroke="{INK}" stroke-width="3"/>\n'
    s += f'<rect x="164" y="250" width="92" height="64" rx="6" fill="#64748b" stroke="{INK}" stroke-width="2.5"/>\n'
    for yy in (260, 272):
        s += line(164, yy, 256, yy, "#1f2937", 3)
    s += line(210, 314, 240, 400, "#475569", 12)
    s += f'<path d="M 90,360 L 370,360 L 370,500 Q 230,560 90,500 Z" fill="#e2e8f0" stroke="{INK}" stroke-width="3"/>\n'
    s += f'<path d="M 100,470 L 360,470 L 360,496 Q 230,548 100,496 Z" fill="{OIL}" fill-opacity="0.85"/>\n'
    s += f'<circle cx="240" cy="410" r="30" fill="none" stroke="#475569" stroke-width="6"/>\n'
    s += t(230, 466, "CRANKCASE / SUMP", 13, 800, INK)
    # blow-by
    for x in (158, 262):
        s += line(x, 268, x, 350, RED, 3.5, "aRedS")
    s += t(284, 226, "BLOW-BY GASES", 13, 800, RED, "start")
    s += t(284, 243, "PAST THE RINGS", 13, 800, RED, "start")
    s += line(282, 250, 266, 290, RED, 2, "aRedS")
    # breather pipe
    s += pipe([(350, 380), (440, 380), (440, 300), (600, 300), (600, 480)], hl=True)
    s += line(600, 488, 600, 540, "#64748b", 4, "aDark")
    s += t(612, 540, "VENTED OVERBOARD", 14, 800, INK, "start")
    s += t(520, 274, "BREATHER PIPE", 16, 800, GOLD_DARK)
    for (x1, y1, x2, y2) in ((372, 368, 420, 368), (470, 288, 530, 288)):
        s += line(x1, y1, x2, y2, "#64748b", 3, "aDark")
    s += t(395, 420, "Keeps crankcase pressure", 15, 400, BODY, "start")
    s += t(395, 440, "close to atmospheric", 15, 400, BODY, "start")
    s += g.fact_column([
        ("RELIEVES SUMP PRESSURE", ["Blow-by gases that leak past", "the piston rings are vented", "away."]),
        ("PROTECTS THE SEALS", ["Without it, pressure would", "force oil out past seals and", "gaskets."]),
        ("CHECK", ["A blocked breather (e.g. by", "ice) can cause oil loss."]),
    ])
    s += footer("The breather pipe relieves excess pressure in the sump (crankcase).")
    return s


BATCHES = {
    "lubrication-batch-2": {
        "q2543-wet-sump-system": lambda: wet_sump("sump"),
        "q2529-oil-pressure-gauge-position": lambda: wet_sump("pressure"),
        "q2531-oil-cooler-position": lambda: wet_sump("cooler"),
        "q2534-oil-temperature-position": lambda: wet_sump("temp"),
    },
    "lubrication-batch-3": {
        "q2518-high-temp-low-pressure": q2518,
        "q2528-spark-plug-normal": lambda: spark_plugs("normal"),
        "q2557-spark-plug-rich-mixture": lambda: spark_plugs("rich"),
        "q2521-engine-breather": q2521,
    },
}

if __name__ == "__main__":
    for batch in sys.argv[1:] or BATCHES:
        pub = OUT / batch
        pub.mkdir(parents=True, exist_ok=True)
        for name, fn in BATCHES[batch].items():
            (pub / f"{name}.svg").write_text(fn(), encoding="utf-8")
            print("wrote", batch, name)
