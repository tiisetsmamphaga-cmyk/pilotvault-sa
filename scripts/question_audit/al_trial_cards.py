"""Air Law trial set: fuller KEY FACT cards, 2026-10-09.

Thin cards (fewer than three points) get four or five, to the standard of atg_trial_cards.py: the neighbouring
signals and settings, the minima, the exam trap. Headlines stay (1412 gains the subline it lacked); explanations
are unchanged.
"""
import json


def card(headline, subline, blocks, formula=None):
    d = {"kicker": "KEY FACT", "headline": headline, "subline": subline,
         "blocks": [{"label": a, "value": b} for a, b in blocks]}
    if formula:
        d["formula"] = formula
    return json.dumps(d, ensure_ascii=False)


SIGNALS = ("Signal area", "Red square, yellow cross: no landing · Dumbbell: runways and taxiways only · "
                          "Double cross: gliders · A: agricultural flights")

CARDS = {
    1048: card("ATZ: CONTROLLED AIRSPACE WITH AERODROME CONTROL IN OPERATION", "AIRSPACE OF DEFINED SIZE AROUND AN AERODROME",
               [("Class G ATZ", "Uncontrolled, with an information service only"),
                ("Classes", "An ATZ can be Class C, D or G"),
                ("Class C or D", "Controlled: the tower gives clearances"),
                ("Protects", "Take-offs, landings and the circuit"),
                ("Exam trap", "Not every ATZ is controlled, and none is a prohibited area")]),
    1073: card("SPECIAL VFR: ONLY IN A CONTROL ZONE (CTR)", "AND ONLY WITH ATC APPROVAL",
               [("Minimum", "600 ft cloud base and 1,500 m visibility"),
                ("Not in", "An ATZ"),
                ("When", "The CTR is below VFR minima but you want to fly VFR"),
                ("Stay", "Clear of cloud and in sight of the surface"),
                ("Exam trap", "Not in an FIR, a prohibited area or on an advisory route")]),
    1085: card("CRUISING LEVEL BY MAGNETIC TRACK", "THE SEMI-CIRCULAR RULE",
               [("000°–179°", "Odd thousands; VFR adds 500 ft"),
                ("180°–359°", "Even thousands; VFR adds 500 ft"),
                ("Applies", "Cruising at or above 1,500 ft AGL"),
                ("Example", "Track 090°M, VFR: FL055 or FL075"),
                ("Exam trap", "Not true heading, compass heading or airspeed")]),
    1086: card("NO FLIGHT CREW DUTIES WITHIN 24 HOURS OF SCUBA DIVING", "DISSOLVED NITROGEN CAN FORM BUBBLES AT LOWER CABIN PRESSURE",
               [("RISK", "Decompression sickness ('the bends') at altitude"),
                ("RULE", "Wait at least 24 hours after diving before acting as crew"),
                ("Pressure", "Every 10 m of water adds one atmosphere"),
                ("Even pressurised", "The cabin is still below sea-level pressure"),
                ("Symptoms", "Joint pain, chest pain, tingling, itching")]),
    1098: card("A LETTER A: AGRICULTURAL FLIGHTS IN OPERATION", "EXPECT CROP-SPRAYING AIRCRAFT FLYING LOW",
               [SIGNALS,
                ("The A", "Large and black, in the signal area"),
                ("Expect", "Aircraft working low over the surrounding fields"),
                ("Action", "A sharp lookout when joining or overflying"),
                ("Exam trap", "Gliders are the double cross, not the A")]),
    1100: card("RED SQUARE, YELLOW CROSS: LANDINGS PROHIBITED", "DISPLAYED IN THE SIGNAL AREA",
               [("One yellow diagonal stripe", "Take special care when landing"),
                SIGNALS,
                ("Runway closed", "Shown by crosses at each end of the runway, not in the signal area"),
                ("Where", "The signal area, visible from the air"),
                ("Exam trap", "Full cross: no landing. Single stripe: land with care")]),
    1102: card("WHITE DUMBBELL: RUNWAYS AND TAXIWAYS ONLY", "FOR LANDING, TAKE-OFF AND TAXIING",
               [("Dumbbell with black bars", "Land and take off on runways; taxi anywhere"),
                SIGNALS,
                ("Why", "The grass may be soft or waterlogged"),
                ("Where", "The signal area, visible from the air"),
                ("Exam trap", "Black bars allow taxiing on the grass; a plain dumbbell doesn't")]),
    1103: card("CROSSES MARK AN UNSERVICEABLE RUNWAY OR TAXIWAY", "A WHITE OR YELLOW CROSS AT EACH END MEANS: DO NOT USE",
               [("Meaning", "No landing, take-off or taxiing on the marked surface"),
                ("Colour", "White or yellow"),
                ("At night", "Red lights mark the area; the lights between them are off"),
                ("Typical causes", "Waterlogging, ground undermined by moles, works"),
                ("Exam trap", "A red square with one yellow stripe means 'take care', not 'closed'")]),
    1104: card("DOUBLE WHITE CROSS: GLIDER FLIGHTS IN OPERATION", "EXPECT GLIDERS AND TOW-PLANES",
               [SIGNALS,
                ("Expect", "Gliders and tow-planes in the circuit, and winch launches"),
                ("Right of way", "Powered aircraft give way to gliders"),
                ("Gliders", "Can't go around: give them room"),
                ("Exam trap", "The A is agricultural flights; the red square is no landing")]),
    1379: card("AT THE TRANSITION ALTITUDE IN THE CLIMB: SET 1013 HPA", "FROM ALTITUDE ON QNH TO FLIGHT LEVELS",
               [("In the descent", "Set QNH at the transition level"),
                ("Below it", "QNH: altitude above sea level"),
                ("Transition level", "The lowest flight level above the transition altitude"),
                ("Remember", "Climbing, change at the altitude; descending, at the level"),
                ("Exam trap", "The destination QNH is set in the descent, not here")]),
    1396: card("TRANSITION LEVEL: THE LOWEST FLIGHT LEVEL ABOVE THE TRANSITION ALTITUDE", "BELOW IT YOU FLY ON QNH, ABOVE IT ON 1013 HPA",
               [("Transition layer", "Between the transition altitude and the transition level"),
                ("Climbing", "Set 1013 hPa at the transition altitude"),
                ("Descending", "Set QNH at the transition level"),
                ("It moves", "Changes with the QNH: a low QNH raises it"),
                ("Exam trap", "Not always FL180, and nothing to do with the circuit")]),
    1403: card("ABOVE FL100: 8 KM, 1.5 KM AND 1000 FT", "VISIBILITY, THEN DISTANCE FROM CLOUD",
               [("Below FL100", "5 km visibility, same distance from cloud"),
                ("From cloud", "1.5 km horizontally, 1,000 ft vertically"),
                ("Why more", "Higher speeds up there: less time to see and avoid"),
                ("Day or night", "The same minima"),
                ("Exam trap", "5 km is the figure below FL100")]),
    1412: card("A SLICING MOTION ACROSS THE THROAT MEANS: CUT ENGINE(S)", "MARSHALLING SIGNAL",
               [("GESTURE", "One arm raised; the other drawn from the shoulder across the throat"),
                ("MEANING", "Shut down the engine(s) indicated"),
                ("Stop", "Arms crossed above the head"),
                ("Chocks inserted", "Arms extended, palms facing in, moved inwards"),
                ("Brakes", "Fist clenched: brakes on · Hand opened: brakes off")]),
    1444: card("ROTATING BEACON, NAVIGATION LIGHTS, LANDING LIGHTS", "ALL THREE ARE NEEDED TO FLY AT NIGHT",
               [("Navigation lights", "Red left, green right, white tail"),
                ("Arcs", "Red and green 110° each; white 140° to the rear"),
                ("Beacon", "Anti-collision: makes the aircraft easy to see"),
                ("Landing light", "For the approach and landing"),
                ("Reading them", "See red on your right: it is crossing from the right, give way")]),
}

TRIAL = [1048, 1073, 1085, 1086, 1098, 1100, 1102, 1103, 1104, 1379, 1396, 1403, 1412, 1444]
assert set(CARDS) == set(TRIAL)
