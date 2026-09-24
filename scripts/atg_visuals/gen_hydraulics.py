"""Hydraulic-system explanation diagrams (ATG)."""
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
FLUID = "#dc2626"
OUT = REPO / "public/explanation-images/aircraft-technical-and-general"


def pipe(pts, ret=False):
    s = polyline(pts, INK, 10)
    s += polyline(pts, "#fca5a5" if ret else FLUID, 5)
    return s


def hl_box(x, y, w, h, on, fill="#e2e8f0", rx=8):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{GOLD if on else INK}" stroke-width="{5 if on else 2.5}"/>\n'


HYD = {
    "filter": ("LOW-PRESSURE FILTER",
               [("BETWEEN RESERVOIR AND PUMP", ["Fitted in the suction line", "feeding the pump."]),
                ("PROTECTS THE PUMP", ["Removes contamination before", "it can reach and damage", "the pump."]),
                ("MUST NOT RESTRICT FLOW", ["A clogged filter could starve", "the pump of fluid."])],
               "A low-pressure filter is usually fitted between the reservoir and the pump."),
    "accumulator": ("HYDRAULIC ACCUMULATOR",
                    [("STORES FLUID UNDER PRESSURE", ["System pressure compresses", "a gas charge above the fluid."]),
                     ("PEAK DEMAND", ["Supplies extra flow when", "several services operate", "at once."]),
                     ("EMERGENCY AND DAMPING", ["Can operate services briefly", "and smooths pump pressure", "pulses."])],
                    "An accumulator stores hydraulic fluid under pressure for peak demand or emergency use."),
    "light": ("LOW HYDRAULIC PRESSURE WARNING",
              [("PRESSURE SWITCH", ["Monitors the system", "pressure line."]),
               ("RED WARNING LIGHT", ["Illuminates when pressure", "falls below a safe value."]),
               ("ACTION", ["Follow the checklist for", "hydraulic failure."])],
              "Loss of hydraulic pressure is indicated by a warning light, usually red."),
    "vent": ("HYDRAULIC RESERVOIR VENT",
             [("PREVENTS A VACUUM", ["Air enters as the pump draws", "fluid out of the reservoir."]),
              ("LEVEL RISES AND FALLS", ["Air escapes as fluid returns", "or expands with heat."]),
              ("STEADY SUPPLY", ["The pump is never starved", "by low reservoir pressure."])],
             "The reservoir vent lets air in as fluid is drawn off, so no vacuum can form."),
}


def hyd_system(answer):
    title, facts, foot = HYD[answer]
    s = header(title)
    s += f'<rect x="40" y="142" width="710" height="444" rx="12" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2"/>\n'
    # reservoir with vent
    s += hl_box(80, 200, 120, 100, answer == "vent", "#ffffff")
    s += f'<rect x="84" y="236" width="112" height="60" fill="{FLUID}" fill-opacity="0.8"/>\n'
    s += t(140, 226, "RESERVOIR", 13, 800, INK)
    s += f'<rect x="126" y="186" width="28" height="14" fill="#94a3b8" stroke="{INK}" stroke-width="2"/>\n'
    s += line(140, 186, 140, 160, "#64748b", 4)
    if answer == "vent":
        s += line(118, 158, 118, 184, BLUE, 3, "aBlue")
        s += line(162, 184, 162, 158, BLUE, 3, "aBlue")
        s += t(210, 172, "VENT: AIR IN / OUT", 13, 800, GOLD_DARK, "start")
    else:
        s += t(152, 164, "VENT", 11, 800, MUTED, "start")
    # suction line, LP filter, pump
    s += pipe([(140, 300), (140, 470)])
    s += hl_box(118, 340, 44, 40, answer == "filter", "#fde68a", 6)
    s += t(172, 366, "LP FILTER", 13, 800, GOLD_DARK if answer == "filter" else INK, "start")
    s += f'<circle cx="140" cy="480" r="26" fill="#475569" stroke="{INK}" stroke-width="3"/>\n'
    s += t(140, 486, "P", 16, 800, "#ffffff")
    s += t(140, 532, "PUMP", 13, 800, INK)
    # pressure line
    s += pipe([(166, 480), (620, 480), (620, 400)])
    s += line(200, 468, 240, 468, "#7f1d1d", 3, "aDark")
    # relief valve back to reservoir (dashed return)
    s += f'<rect x="232" y="500" width="26" height="30" rx="4" fill="#e2e8f0" stroke="{INK}" stroke-width="2"/>\n'
    s += line(245, 480, 245, 500, INK, 3)
    s += polyline([(245, 530), (245, 560), (60, 560), (60, 250), (80, 250)], "#fca5a5", 4, dash="8 6")
    s += t(266, 522, "RELIEF VALVE", 11, 800, MUTED, "start")
    # accumulator
    acc = answer == "accumulator"
    s += line(330, 480, 330, 440, INK, 4)
    s += f'<rect x="300" y="300" width="60" height="140" rx="30" fill="#ffffff" stroke="{GOLD if acc else INK}" stroke-width="{5 if acc else 2.5}"/>\n'
    s += f'<rect x="304" y="304" width="52" height="64" rx="26" fill="#bfdbfe"/>\n'
    s += f'<rect x="304" y="372" width="52" height="64" rx="26" fill="{FLUID}" fill-opacity="0.85"/>\n'
    s += line(304, 370, 356, 370, INK, 4)
    s += t(330, 342, "GAS", 12, 800, "#1d4ed8")
    s += t(330, 412, "FLUID", 12, 800, "#ffffff")
    s += t(330, 290, "ACCUMULATOR", 13, 800, GOLD_DARK if acc else INK)
    # pressure switch + warning light
    lt = answer == "light"
    s += line(440, 480, 440, 440, INK, 4)
    s += hl_box(424, 410, 32, 30, lt, "#e2e8f0", 4)
    s += line(440, 410, 440, 370, "#475569", 2.5, dash="5 4")
    s += f'<circle cx="440" cy="352" r="18" fill="{RED}" stroke="{GOLD if lt else INK}" stroke-width="{5 if lt else 2.5}"/>\n'
    s += t(440, 322, "HYD PRESS", 12, 800, RED)
    s += t(466, 432, "PRESSURE", 11, 800, MUTED, "start")
    s += t(466, 446, "SWITCH", 11, 800, MUTED, "start")
    # selector and actuator
    s += f'<rect x="596" y="360" width="48" height="40" rx="4" fill="#e2e8f0" stroke="{INK}" stroke-width="2.5"/>\n'
    s += t(656, 386, "SELECTOR", 11, 800, MUTED, "start")
    s += pipe([(620, 360), (620, 300)])
    s += f'<rect x="570" y="200" width="100" height="100" rx="6" fill="#ffffff" stroke="{INK}" stroke-width="2.5"/>\n'
    s += f'<rect x="574" y="250" width="92" height="46" fill="{FLUID}" fill-opacity="0.8"/>\n'
    s += f'<rect x="574" y="238" width="92" height="12" fill="#475569"/>\n'
    s += line(620, 238, 620, 186, "#475569", 8)
    s += t(690, 232, "ACTUATOR", 12, 800, INK, "start")
    s += polyline([(570, 220), (220, 220), (200, 220)], "#fca5a5", 4, dash="8 6")
    s += t(390, 212, "RETURN TO RESERVOIR", 12, 800, MUTED)
    note = {
        "filter": "FILTERS FLUID BEFORE THE PUMP",
        "accumulator": "STORES FLUID UNDER PRESSURE",
        "light": "RED LIGHT = LOW PRESSURE",
        "vent": "",
    }[answer]
    if note:
        s += t(736, 170, note, 14, 800, GOLD_DARK, "end")
    s += g.fact_column(facts)
    s += footer(foot)
    return s


FLUIDS = {
    "mineral": "Mineral-based hydraulic fluid is coloured red.",
    "vegetable": "Vegetable-based hydraulic fluid is coloured blue.",
    "phosphate": "Phosphate-ester (synthetic) hydraulic fluid is coloured purple.",
    "never": "Vegetable-based and mineral-based hydraulic fluids must never be mixed.",
}


def fluid_colours(answer):
    s = header("HYDRAULIC FLUID IDENTIFICATION")
    cols = [("mineral", "MINERAL BASED", "#dc2626", "RED"),
            ("vegetable", "VEGETABLE BASED", "#2563eb", "BLUE"),
            ("phosphate", "PHOSPHATE ESTER", "#7c3aed", "PURPLE")]
    for i, (key, name, col, cname) in enumerate(cols):
        px = 48 + i * 372
        ans = key == answer
        fill, stroke, sw = ("#fff8e1", GOLD, 4) if ans else ("#f8fafc", "#cbd5e1", 2)
        s += f'<rect x="{px}" y="142" width="356" height="300" rx="12" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>\n'
        s += t(px + 178, 180, name, 19, 800, INK)
        if ans:
            s += f'<rect x="{px + 132}" y="398" width="92" height="28" rx="14" fill="{GOLD}"/>\n'
            s += t(px + 178, 417, "ANSWER", 14, 800, NAVY)
        cx = px + 178
        s += f'<path d="M {cx - 44},212 L {cx + 44},212 L {cx + 44},226 L {cx + 60},244 L {cx + 60},352 Q {cx + 60},368 {cx + 44},368 L {cx - 44},368 Q {cx - 60},368 {cx - 60},352 L {cx - 60},244 L {cx - 44},226 Z" fill="#ffffff" stroke="{INK}" stroke-width="3"/>\n'
        s += f'<rect x="{cx - 56}" y="270" width="112" height="94" rx="10" fill="{col}"/>\n'
        s += t(cx, 326, cname, 22, 800, "#ffffff")
    nv = answer == "never"
    fill, stroke, sw = ("#fff8e1", GOLD, 4) if nv else ("#fef2f2", RED, 2)
    s += f'<rect x="48" y="458" width="1100" height="128" rx="12" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>\n'
    s += t(78, 502, "NEVER MIX FLUID TYPES", 24, 800, RED, "start")
    s += t(78, 536, "Incompatible fluids attack seals, change viscosity and form deposits.", 17, 400, BODY, "start")
    s += t(78, 562, "Always use the fluid type specified for the aircraft.", 17, 400, BODY, "start")
    if nv:
        s += f'<rect x="1034" y="478" width="92" height="28" rx="14" fill="{GOLD}"/>\n'
        s += t(1080, 497, "ANSWER", 14, 800, NAVY)
    s += footer(FLUIDS[answer])
    return s


BATCHES = {
    "hydraulics-batch-1": {
        "q2565-hydraulic-lp-filter": lambda: hyd_system("filter"),
        "q2532-hydraulic-accumulator": lambda: hyd_system("accumulator"),
        "q2551-hydraulic-pressure-warning": lambda: hyd_system("light"),
        "q2555-hydraulic-reservoir-vent": lambda: hyd_system("vent"),
    },
    "hydraulics-batch-2": {
        "q2538-hydraulic-fluid-mineral-red": lambda: fluid_colours("mineral"),
        "q2537-hydraulic-fluid-vegetable-blue": lambda: fluid_colours("vegetable"),
        "q2523-hydraulic-fluid-phosphate-purple": lambda: fluid_colours("phosphate"),
        "q2545-hydraulic-fluids-never-mix": lambda: fluid_colours("never"),
    },
}

if __name__ == "__main__":
    for batch in sys.argv[1:] or BATCHES:
        pub = OUT / batch
        pub.mkdir(parents=True, exist_ok=True)
        for name, fn in BATCHES[batch].items():
            (pub / f"{name}.svg").write_text(fn(), encoding="utf-8")
            print("wrote", batch, name)
