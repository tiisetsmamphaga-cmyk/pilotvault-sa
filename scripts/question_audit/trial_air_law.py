"""Air Law trial set (the fixed 25-question trial mock), 2026-10-08.

Every trial question shows a strong picture and an answer-first KEY FACT card. Questions whose only picture
was a flat timeline or box diagram (pure numbers or lists: 24 h notification, 36 months, documents, logbook ...)
were swapped for questions with textbook figures or manual-based pictures; they stay in the full bank.
"""
import json


def card(headline, subline, blocks=()):
    d = {"kicker": "KEY FACT", "headline": headline, "subline": subline}
    if blocks:
        d["blocks"] = [{"label": a, "value": b} for a, b in blocks]
    return json.dumps(d, ensure_ascii=False)


AL = "/explanation-images/air-law/refined-batch-1/"
AL2 = "/explanation-images/air-law/refined-batch-2/"
SEMI = "/explanation-images/radio-telephony/refined-batch-1/rt-semi-circular-rule-v1.webp"
PANEL = AL + "al-visual-ground-signals-panel-v1.webp"
SIGNALS = ("Signal area", "Red square, yellow cross: no landing · Dumbbell: runways and taxiways only · "
                          "Double cross: gliders · A: agricultural flights")

TRIAL = [1094, 1098, 1396, 1404, 1412, 2810, 1049, 1062, 1080, 1019, 1086, 1028, 910,
         1100, 1102, 1103, 1104, 2811, 2812, 1379, 1048, 1403, 1085, 1073, 1444]

# id -> (picture url, title); only questions whose picture changes
PICTURE = {
    1049: (AL2 + "vfr-minima-low-v1.webp", "VFR Minima at Low Level"),
    1062: (AL2 + "vfr-minima-below-fl100-v1.webp", "VFR Minima Below FL100"),
    1403: (AL2 + "vfr-minima-above-fl100-v1.webp", "VFR Minima Above FL100"),
    1028: (AL2 + "head-on-turn-right-v1.webp", "Head-on: Both Turn Right"),
    910: (AL2 + "ppl-long-nav-v1.webp", "PPL Long Navigation Flight"),
    1080: (SEMI, "Semi-circular Rule"),
    1085: (SEMI, "Semi-circular Rule"),
    1019: ("/explanation-images/navigation/refined-batch-2/official-day-night-v1.webp", "Official Day and Night"),
    1086: ("/explanation-images/human-performance/refined-batch-10/hp-scuba-pressure-depth-v1.webp",
           "Scuba Diving and Flying"),
    1073: (AL + "al-airspace-division-v1.webp", "Airspace Division"),
    1444: (AL + "al-visual-navigation-lights-v1.webp", "Navigation Lights"),
}

# id -> card; only questions whose card changes
CARDS = {
    1098: card("A LETTER A: AGRICULTURAL FLIGHTS IN OPERATION", "EXPECT CROP-SPRAYING AIRCRAFT FLYING LOW", [SIGNALS]),
    1100: card("RED SQUARE, YELLOW CROSS: LANDINGS PROHIBITED", "DISPLAYED IN THE SIGNAL AREA",
               [("One yellow diagonal stripe", "Take special care when landing"), SIGNALS]),
    1102: card("WHITE DUMBBELL: RUNWAYS AND TAXIWAYS ONLY", "FOR LANDING, TAKE-OFF AND TAXIING",
               [("Dumbbell with black bars", "Land and take off on runways; taxi anywhere"), SIGNALS]),
    1104: card("DOUBLE WHITE CROSS: GLIDER FLIGHTS IN OPERATION", "EXPECT GLIDERS AND TOW-PLANES", [SIGNALS]),
    1396: card("TRANSITION LEVEL: THE LOWEST FLIGHT LEVEL ABOVE THE TRANSITION ALTITUDE",
               "BELOW IT YOU FLY ON QNH, ABOVE IT ON 1013 HPA",
               [("Transition layer", "Between the transition altitude and the transition level")]),
    1379: card("AT THE TRANSITION ALTITUDE IN THE CLIMB: SET 1013 HPA", "FROM ALTITUDE ON QNH TO FLIGHT LEVELS",
               [("In the descent", "Set QNH at the transition level")]),
    1048: card("ATZ: CONTROLLED AIRSPACE WITH AERODROME CONTROL IN OPERATION", "AIRSPACE OF DEFINED SIZE AROUND AN AERODROME",
               [("Class G ATZ", "Uncontrolled, with an information service only")]),
    1073: card("SPECIAL VFR: ONLY IN A CONTROL ZONE (CTR)", "AND ONLY WITH ATC APPROVAL",
               [("Minimum", "600 ft cloud base and 1,500 m visibility"), ("Not in", "An ATZ")]),
    1085: card("CRUISING LEVEL BY MAGNETIC TRACK", "THE SEMI-CIRCULAR RULE",
               [("000°–179°", "Odd thousands; VFR adds 500 ft"), ("180°–359°", "Even thousands; VFR adds 500 ft")]),
    1403: card("ABOVE FL100: 8 KM, 1.5 KM AND 1000 FT", "VISIBILITY, THEN DISTANCE FROM CLOUD",
               [("Below FL100", "5 km visibility, same distance from cloud")]),
    1444: card("ROTATING BEACON, NAVIGATION LIGHTS, LANDING LIGHTS", "ALL THREE ARE NEEDED TO FLY AT NIGHT",
               [("Navigation lights", "Red left, green right, white tail")]),
}
