"""Extracted-figure explanation images. Writes SVGs to scratch/ext-svg/<batch>/."""
import sys
from pathlib import Path
import os
REPO = Path(__file__).resolve().parents[2]
WORK = Path(os.environ.get("ATG_WORK", "/tmp/atg-work"))

from figframe import frame

HERE = Path(__file__).parent
FIGS = WORK / "figs"

ITEMS = {
    "airframes-batch-5": {
        "q2428-braced-monoplane": lambda: frame(
            FIGS / "p14-1.png",
            "SEMI-CANTILEVER (STRUT-BRACED) MONOPLANE",
            "A strut-braced monoplane: the struts carry part of the wing's flight and ground loads.",
            "A semi-cantilever wing is supported by struts running from the base of the fuselage to the wing.",
            notes=[
                ("BRACING STRUTS", (1045, 250), (640, 290), "middle"),
                ("STRUTS MEET THE\nFUSELAGE BASE", (1045, 430), (562, 402), "middle"),
            ],
        ),
        "q2762-mass-balance-flutter": lambda: frame(
            FIGS / "p23-1.png",
            "MASS BALANCE PREVENTS FLUTTER",
            "A mass balance ahead of the hinge moves the control surface's centre of gravity forward.",
            "Correct mass distribution (mass balancing) within the control surface helps prevent flutter.",
        ),
    },
    "lubrication-batch-1": {
        "q2530-dry-sump-scavenge-pump": lambda: frame(
            FIGS / "p93-1.png",
            "DRY SUMP: SCAVENGE PUMP",
            "The scavenge pump removes oil from the engine sump and returns it to the separate oil tank.",
            "In a dry-sump system the scavenge pump pumps oil from the sump back to the oil tank.",
            notes=[
                ("SCAVENGE PUMP", (1010, 520), (840, 915), "middle"),
                ("RETURNS OIL FROM\nTHE SUMP TO THE TANK", (1010, 350), (940, 620), "middle"),
                ("SEPARATE\nOIL TANK", (190, 230), (140, 250), "middle"),
                ("SUMP KEPT\nALMOST DRY", (190, 470), (520, 860), "middle"),
            ],
        ),
        "q2542-gear-type-oil-pump": lambda: frame(
            FIGS / "gearpump.png",
            "GEAR-TYPE OIL PUMP",
            "Meshing gears carry a fixed volume of oil round the outside of the gears from inlet to outlet.",
            "Piston-engine pressure lubrication uses a gear-type pump, backed up by splash lubrication.",
            notes=[
                ("MESHING GEARS\nCARRY THE OIL", (215, 330), (130, 470), "middle"),
                ("RELIEF VALVE", (1010, 300), (760, 380), "middle"),
            ],
        ),
        "q2552-oil-pressure-relief-valve": lambda: frame(
            FIGS / "gearpump.png",
            "OIL PRESSURE RELIEF VALVE",
            "When pressure exceeds the spring setting, the valve opens and returns excess oil to the inlet.",
            "The relief valve maintains a constant oil pressure over a range of engine power changes.",
            notes=[
                ("PRESSURE\nRELIEF VALVE", (1010, 250), (760, 380), "middle"),
                ("EXCESS OIL RETURNS\nTO THE INLET SIDE", (1010, 450), (840, 650), "middle"),
            ],
        ),
        "q2549-crankshaft-bearing-lubrication": lambda: frame(
            FIGS / "p91-1.png",
            "CRANKSHAFT AND BEARING LUBRICATION",
            "Pressure oil is fed through drillings to the main and big-end bearings; splash oils the rest.",
            "The main bearings and crankshaft are lubricated by high-pressure oil from the pump.",
            notes=[
                ("MAIN BEARINGS FED\nWITH PRESSURE OIL", (205, 250), (80, 300), "middle"),
                ("OIL DRILLINGS IN\nTHE CRANKSHAFT", (1010, 470), (560, 505), "middle"),
                ("SPLASH OILS THE CYLINDER\nWALLS AND PISTONS", (1010, 250), (None, None), "middle"),
            ],
        ),
        "q2533-oil-cooler-ram-air": lambda: frame(
            FIGS / "p88-1.png",
            "OIL COOLING: RAM AIR",
            "Ram air passing through the cooler's fins removes heat from the circulating oil.",
            "The primary method of cooling the oil is ram air through an oil cooler.",
            notes=[
                ("OIL COOLER\n(HEAT EXCHANGER)", (1010, 300), (440, 400), "middle"),
                ("RAM AIR FLOWS\nTHROUGH THE FINS", (205, 300), (410, 440), "middle"),
            ],
        ),
    },
    "lubrication-batch-2": {
        "q2773-no-oil-pressure-after-start": lambda: frame(
            FIGS / "p103-1.png",
            "NO OIL PRESSURE AFTER START",
            "Oil pressure must rise into the normal range within the time the manufacturer specifies.",
            "If oil pressure does not rise in time, shut the engine down promptly and investigate.",
            notes=[
                ("OIL PRESSURE\nNOT RISING", (1010, 280), (150, 150), "middle"),
                ("SHUT DOWN BEFORE\nTHE BEARINGS FAIL", (1010, 470), (None, None), "middle"),
            ],
        ),
    },
    "hydraulics-batch-1": {
        "q2559-pascals-law-hydraulic-brakes": lambda: frame(
            FIGS / "p48-1.png",
            "PASCAL'S LAW: HYDRAULIC BRAKES",
            "Pressure applied to a confined fluid is transmitted equally throughout the fluid.",
            "A hydraulic system works because pressure applied to a confined fluid is transmitted by it.",
            notes=[
                ("PEDAL FORCE PRESSURISES\nTHE CONFINED FLUID", (1000, 470), (390, 350), "middle"),
                ("THE SAME PRESSURE ACTS\nON THE SLAVE CYLINDER", (205, 470), (235, 350), "middle"),
            ],
        ),
    },
    "piston-batch-1": {
        "q2474-valve-lead": lambda: frame(
            FIGS / "p55-1.png",
            "VALVE LEAD",
            "Valve timing diagram: the inlet valve opens before the piston reaches top dead centre.",
            "Valve lead: the inlet valve opens before the piston reaches TDC on the exhaust stroke.",
            notes=[
                ("INLET VALVE OPENS\nBEFORE TDC", (215, 250), (250, 120), "middle"),
                ("VALVE LEAD\n(20\u00b0 IN THIS ENGINE)", (985, 250), (305, 76), "middle"),
            ],
        ),
        "q2560-valve-overlap": lambda: frame(
            FIGS / "p55-1.png",
            "VALVE OVERLAP",
            "Valve timing diagram: the inlet opens before TDC and the exhaust closes after TDC.",
            "Valve overlap: the short period around TDC when both inlet and exhaust valves are open.",
            notes=[
                ("INLET OPENS\nBEFORE TDC", (215, 250), (250, 120), "middle"),
                ("EXHAUST CLOSES\nAFTER TDC", (985, 230), (520, 108), "middle"),
                ("BOTH OPEN AROUND\nTDC: OVERLAP", (985, 440), (395, 92), "middle"),
            ],
        ),
        "q2525-cylinder-cooling-fins": lambda: frame(
            FIGS / "p82-1.png",
            "CYLINDER COOLING FINS",
            "Fins greatly increase the surface area from which the cylinder can lose heat to the airflow.",
            "Cylinders and barrels are finned to improve engine cooling.",
            notes=[
                ("COOLING FINS", (1000, 300), (560, 330), "middle"),
                ("MORE SURFACE AREA\n= MORE HEAT LOST", (205, 300), (None, None), "middle"),
            ],
        ),
        "q2564-engine-baffles": lambda: frame(
            FIGS / "p83-1.png",
            "ENGINE BAFFLES",
            "Baffles guide the incoming cooling air closely around the cylinders before it leaves the cowling.",
            "Baffles direct the airflow over the engine cylinders for better cooling.",
            notes=[
                ("INTER-CYLINDER\nBAFFLES", (170, 250), (410, 360), "middle"),
                ("COOLING AIR\nENTERS HERE", (1035, 470), (1120, 230), "middle"),
            ],
        ),
        "q2553-cowl-flaps": lambda: frame(
            FIGS / "p83-1.png",
            "COWL FLAPS",
            "Open cowl flaps for high power at low airspeed (climb); close them in cruise and descent.",
            "Cowl flaps control the airflow over the cylinders to keep the correct operating temperature.",
            notes=[
                ("COWL FLAP\nCONTROLS THE\nCOOLING AIRFLOW", (165, 450), (200, 700), "middle"),
            ],
        ),
    },
}

if __name__ == "__main__":
    for batch in sys.argv[1:] or ITEMS:
        out = WORK / "ext-svg" / batch
        out.mkdir(parents=True, exist_ok=True)
        for name, fn in ITEMS[batch].items():
            (out / f"{name}.svg").write_text(fn(), encoding="utf-8")
            print("wrote", batch, name)
