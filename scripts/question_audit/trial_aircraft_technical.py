"""Aircraft Technical and General trial set (the fixed 25-question trial mock), 2026-10-08.

Every trial question shows a strong picture and an answer-first KEY FACT card (the cards were already
answer-first). Twelve questions whose only picture was a flat drawn diagram (shimmy damper, torque links,
semi-monocoque, propeller twist, tank baffles, throttle handling, fuel and hydraulic fluid colours, alternator,
battery, deviation card, inverter) were swapped for questions with textbook figures; they stay in the full bank.
The manual's diagrams (valve timing, gear pump, hydraulic brake, engine cooling, oil pressure gauge) are redrawn
from its figures in HD; its two photographs (strut-braced monoplane, finned cylinder) are upscaled to HD
(atg_figures.py); deviation uses the Navigation scene; all in aircraft-technical-and-general/refined-batch-1
(atg_phone.py). The load-factor question moves to the textbook chart.
"""
TRIAL = [2428, 2474, 2500, 2520, 2525, 2566, 2584, 2673, 2675, 2701, 2768, 2771, 2773,
         2553, 2559, 2564, 2464, 2629, 2740, 2724, 2466, 2450, 2634, 2707, 2432]

ATG = "/explanation-images/aircraft-technical-and-general/refined-batch-1/"

# id -> (picture url, title); only questions whose picture changes
PICTURE = {
    2428: (ATG + "semi-cantilever-struts-v1.webp", "Semi-cantilever Monoplane"),
    2474: (ATG + "valve-lead-v1.webp", "Valve Lead"),
    2520: (ATG + "gear-oil-pump-v1.webp", "Gear-type Oil Pump"),
    2525: (ATG + "cylinder-cooling-fins-v1.webp", "Cylinder Cooling Fins"),
    2773: (ATG + "oil-pressure-not-rising-v1.webp", "No Oil Pressure After Start"),
    2701: (ATG + "compass-deviation-v1.webp", "Compass Deviation"),
    2553: (ATG + "cowl-flap-v1.webp", "Cowl Flap"),
    2559: (ATG + "hydraulic-brake-pascal-v1.webp", "Hydraulic Brakes: Pascal's Law"),
    2564: (ATG + "engine-baffles-v1.webp", "Engine Baffles"),
    2673: ("/explanation-images/principles-of-flight/refined-batch-1/pof-bank-load-factor-v2.webp",
           "Bank Angle and Load Factor"),
}

# id -> card; only questions whose card changes
CARDS = {}
