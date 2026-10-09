"""Radio Telephony trial set: fuller KEY FACT cards, 2026-10-09.

Thin cards (fewer than three points) get four or five, to the standard of atg_trial_cards.py: the neighbouring
facts (the CTR/TMA/CTA stack, the altimeter settings, the other ground signals) and the exam trap. Headlines stay;
explanations are unchanged. South African figures are the ones the explanations give.
"""
import json


def card(headline, subline, blocks, formula=None):
    d = {"kicker": "KEY FACT", "headline": headline, "subline": subline,
         "blocks": [{"label": a, "value": b} for a, b in blocks]}
    if formula:
        d["formula"] = formula
    return json.dumps(d, ensure_ascii=False)


SA_FIRS = ("SA FIRs", "Johannesburg (FAJA), Cape Town (FACA) and Johannesburg Oceanic (FAJO)")
CTR = ("CTR", "Controlled from the surface up, around an aerodrome")
TMA = ("TMA", "Controlled airspace around busy airports, above the CTRs")
CTA = ("CTA", "Controlled airspace higher up, above one or more TMAs")
VFR_EAST = ("000°–179°", "VFR: odd thousands + 500 ft (FL035, FL055, FL075 …)")
VFR_WEST = ("180°–359°", "VFR: even thousands + 500 ft (FL045, FL065, FL085 …)")

CARDS = {
    303: card("FA = SOUTH AFRICA IN ICAO LOCATION INDICATORS", "EVERY SOUTH AFRICAN INDICATOR STARTS WITH FA",
              [("Aerodromes", "FAOR O.R. Tambo · FACT Cape Town · FALE King Shaka"),
               SA_FIRS,
               ("Format", "Four letters: FA + two for the place"),
               ("Neighbours", "FY Namibia · FB Botswana · FQ Mozambique"),
               ("Exam trap", "Egypt is HE; South American codes start with S")]),
    304: card("THESE REGIONS ARE FLIGHT INFORMATION REGIONS (FIRs)", "FLIGHT INFORMATION AND ALERTING SERVICES ARE PROVIDED IN EACH",
              [SA_FIRS,
               ("Centres", "Flight Information Centres at Johannesburg and Cape Town"),
               ("Sectors", "Each FIR is split into sectors (FAJA North, South-West, East)"),
               ("Why", "Each centre gets a manageable workload"),
               ("Exam trap", "UIR: upper region · UTA: upper control area · IFR: a set of flight rules")]),
    307: card("A CTA IS NORMALLY ESTABLISHED ABOVE ONE OR MORE TMAs", "THE HIGHER LAYER OF CONTROLLED AIRSPACE",
              [CTR, TMA,
               ("SA CTA base", "About FL105 to FL145"),
               ("SA CTA top", "Usually FL195 or FL200"),
               ("The stack", "CTR from the surface → TMA → CTA, each layer higher")]),
    308: card("TMA: CONTROLLED AIRSPACE AROUND A BUSY AIRPORT", "WHERE SEVERAL ROUTES MEET NEAR ONE OR MORE MAJOR AERODROMES",
              [CTR, CTA,
               ("Service", "Approach control, often with radar"),
               ("Class", "All South African TMAs are Class C"),
               ("Shape", "Sectors with different bases (TMA A, B …): an upside-down wedding cake")]),
    314: card("SURFACE TO A SPECIFIED UPPER LIMIT: A CONTROL ZONE (CTR)", "CONTROLLED AIRSPACE AROUND AN AERODROME",
              [TMA, CTA,
               ("Inside a CTR", "One or more ATZs"),
               ("Purpose", "Protects IFR traffic arriving and departing"),
               ("Exam trap", "Only the CTR starts at the surface; a CTA starts higher up")]),
    315: card("ATZ = AERODROME TRAFFIC ZONE", "AIRSPACE AROUND AN AERODROME TO PROTECT AERODROME TRAFFIC",
              [CTR,
               ("Protects", "Take-offs, landings and the circuit"),
               ("Height", "From the ground to at least 700 ft AGL, often 1,000–1,500 ft"),
               ("Class", "C, D or G, depending on the aerodrome"),
               ("Class G ATZ", "Served by AFIS, not by air traffic control")]),
    316: card("CONTROL ZONES ARE ESTABLISHED AROUND AERODROMES", "FROM THE SURFACE UP TO A SPECIFIED LIMIT",
              [TMA, CTA,
               ("Purpose", "Protects IFR traffic near the larger airfields"),
               ("Inside", "One or more ATZs (Class C or D)"),
               ("Exam trap", "Above the TMAs is the CTA, not a CTR")]),
    416: card("THE SEMI-CIRCULAR RULE APPLIES AT AND ABOVE 1500 FT AGL", "CRUISING LEVEL IS CHOSEN BY MAGNETIC TRACK",
              [VFR_EAST, VFR_WEST,
               ("Where", "Cruising in uncontrolled airspace"),
               ("IFR", "Whole thousands: odd 000°–179°, even 180°–359°"),
               ("Based on", "Magnetic track, not heading")]),
    419: card("TRACK 090° MAGNETIC, VFR: FL075 IS CORRECT", "000°–179° TAKES ODD THOUSANDS PLUS 500 FT",
              [VFR_EAST, VFR_WEST,
               ("FL075", "7,500 ft on 1013.25 hPa, not 7,500 ft above the ground"),
               ("Based on", "Magnetic track, not compass heading"),
               ("Applies", "At and above 1,500 ft AGL")]),
    438: card("QNE (1013.25 hPa) SET: THE ALTIMETER SHOWS PRESSURE ALTITUDE", "READ AS A FLIGHT LEVEL",
              [("QNH", "Altitude above mean sea level"),
               ("QFE", "Height above the aerodrome"),
               ("Example", "Pressure altitude 7,500 ft = FL075"),
               ("Why", "All cruising traffic on one setting, so separation holds"),
               ("Exam trap", "Not altitude, height or elevation: pressure altitude")]),
    441: card("QFE SET: THE ALTIMETER SHOWS HEIGHT ABOVE THE AERODROME", "IT READS ZERO ON THE RUNWAY",
              [("QNH", "Altitude above mean sea level"),
               ("1013.25 hPa (QNE)", "Pressure altitude: flight levels"),
               ("On the runway", "QFE reads zero; QNH reads the aerodrome elevation"),
               ("Used for", "Circuits and local flying"),
               ("Rule of thumb", "1 hPa ≈ 30 ft")],
              "QFE ≈ QNH − elevation (ft) ÷ 30"),
    448: card("THE TRANSITION LEVEL IS ALWAYS ABOVE THE TRANSITION ALTITUDE", "THE GAP BETWEEN THEM IS THE TRANSITION LAYER",
              [("Climbing", "QNH → 1013.25 hPa at the transition altitude"),
               ("Descending", "1013.25 hPa → QNH at the transition level"),
               ("Transition altitude", "The highest altitude flown on QNH"),
               ("Transition level", "The lowest flight level above it"),
               ("Transition layer", "The buffer between them: no cruising in it")]),
    451: card("CLIMBING THROUGH THE TRANSITION ALTITUDE: SET 1013.25 hPa", "FROM ALTITUDES ON QNH TO FLIGHT LEVELS",
              [("Descending", "1013.25 hPa → QNH at the transition level"),
               ("Below it", "QNH: altitude above sea level, for terrain clearance"),
               ("Above it", "Flight levels, the same reference as other cruising traffic"),
               ("Remember", "Change at the first one you meet: the altitude going up, the level coming down")]),
    506: card("BACKTRACK = TAXI ON THE RUNWAY AGAINST THE DIRECTION IN USE", "USED WHEN THERE IS NO PARALLEL TAXIWAY TO REACH THE THRESHOLD",
              [("WHERE", "On the active runway — follow the clearance exactly"),
               ("THEN", "Turn around at the end and line up, or vacate, as cleared"),
               ("Read back", "Runway instructions are always read back in full"),
               ("Be quick", "Nobody else can use the runway while you are on it"),
               ("Exam trap", "Not reversing the route, not an ILS back course")]),
    570: card("V = REQUIRE ASSISTANCE", "WHITE STRIPS LAID ON THE GROUND FOR A SEARCH AIRCRAFT TO READ",
              [("X", "Require medical assistance"),
               ("N / Y", "No (negative) / Yes (affirmative)"),
               ("Arrow", "Proceeding in this direction"),
               ("Size", "Each symbol at least 2.5 m long, in a colour that contrasts with the ground"),
               ("Remember", "X looks like a medical cross")]),
    576: card("WHITE DUMBBELL: USE ONLY THE RUNWAYS AND TAXIWAYS", "NO MOVEMENT ON THE GRASS",
              [("Dumbbell with black bars", "Land and take off on runways only; taxi anywhere"),
               ("Double white cross", "Gliding in progress"),
               ("Red square, yellow cross", "Landing prohibited"),
               ("Red square, one yellow diagonal", "Take special care when landing"),
               ("Where", "The signal area, near the tower or windsock")]),
    578: card("WHITE CROSS AT THE THRESHOLD: THE RUNWAY IS UNSAFE TO USE", "IT IS CLOSED: NO LANDING, TAKE-OFF OR TAXIING",
              [("Where", "A cross at each end of the closed runway or section"),
               ("Colour", "White or yellow"),
               ("At night", "Red lights mark the unserviceable area"),
               ("Typical causes", "Waterlogging, soft ground, works"),
               ("Exam trap", "A double white cross in the signal area means gliding, not closed")]),
    610: card("FIR = FLIGHT INFORMATION REGION", "AIRSPACE WITH A FLIGHT INFORMATION AND ALERTING SERVICE",
              [SA_FIRS,
               ("Extent", "From the surface to FL650; sectors capped at FL460"),
               ("Services", "Flight information and alerting, from a Flight Information Centre"),
               ("Centres", "Johannesburg and Cape Town"),
               ("Exam trap", "Not a route or a report: a region")]),
}

TRIAL = [303, 304, 307, 308, 314, 315, 316, 416, 419, 438, 441, 448, 451, 506, 570, 576, 578, 610]
assert set(CARDS) == set(TRIAL)
