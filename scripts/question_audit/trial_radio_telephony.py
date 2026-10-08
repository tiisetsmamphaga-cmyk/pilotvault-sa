"""Radio Telephony trial set (the fixed 25-question trial mock), 2026-10-08.

Every trial question shows a strong picture and an answer-first KEY FACT card. Questions whose only picture
was a flat box or timeline diagram (IFR/VFR, SVFR ceiling, local time to UTC, flight-plan lead time, item 10
equipment, SAR phases, contaminated runway) and the second "park in this bay" marshalling question were swapped
for questions with textbook figures; they stay in the full bank. Backtrack, line up and wait and the V ground
signal are redrawn as aerial scenes (radio-telephony/refined-batch-2); QDR uses the Navigation QDM/QDR picture.
The FIR cards said South Africa has two FIRs; the map shows three (FAJA, FACA and the oceanic FAJO).
"""
import json


def card(headline, subline, blocks=()):
    d = {"kicker": "KEY FACT", "headline": headline, "subline": subline}
    if blocks:
        d["blocks"] = [{"label": a, "value": b} for a, b in blocks]
    return json.dumps(d, ensure_ascii=False)


RT2 = "/explanation-images/radio-telephony/refined-batch-2/"

TRIAL = [304, 307, 314, 316, 410, 419, 438, 448, 506, 518, 570, 576, 577, 578, 585, 610, 615,
         303, 308, 315, 318, 416, 441, 451, 587]

# id -> (picture url, title); only questions whose picture changes
PICTURE = {
    410: ("/explanation-images/navigation/refined-batch-2/qdm-qdr-v1.webp", "QDM and QDR"),
    506: (RT2 + "backtrack-v1.webp", "Backtrack"),
    518: (RT2 + "line-up-and-wait-v1.webp", "Line Up and Wait"),
    570: (RT2 + "ground-signals-v-x-v1.webp", "Ground Signals: V and X"),
}

FIRS = ("SA FIRs", "Johannesburg (FAJA), Cape Town (FACA) and Johannesburg Oceanic (FAJO)")
CTR = ("CTR", "Controlled from the surface up, around an aerodrome")
TMA = ("TMA", "Controlled airspace around busy airports, above the CTRs")
CTA = ("CTA", "Controlled airspace higher up, above one or more TMAs")
ATZ = ("ATZ", "Small zone around an aerodrome, for aerodrome traffic")
SETTINGS = [("QNH", "Altitude above mean sea level"), ("QFE", "Height above the aerodrome"),
            ("1013.25 hPa (QNE)", "Pressure altitude: flight levels")]
TRANSITION = [("Climbing", "QNH → 1013.25 hPa at the transition altitude"),
              ("Descending", "1013.25 hPa → QNH at the transition level")]
SEMI = [("000°–179°", "VFR: odd thousands + 500 ft (FL035, FL055, FL075 …)"),
        ("180°–359°", "VFR: even thousands + 500 ft (FL045, FL065, FL085 …)")]

# id -> card; only questions whose card changes
CARDS = {
    304: card("THESE REGIONS ARE FLIGHT INFORMATION REGIONS (FIRs)", "FLIGHT INFORMATION AND ALERTING SERVICES ARE PROVIDED IN EACH",
              [FIRS]),
    610: card("FIR = FLIGHT INFORMATION REGION", "AIRSPACE WITH A FLIGHT INFORMATION AND ALERTING SERVICE", [FIRS]),
    303: card("FA = SOUTH AFRICA IN ICAO LOCATION INDICATORS", "EVERY SOUTH AFRICAN INDICATOR STARTS WITH FA",
              [("Aerodromes", "FAOR O.R. Tambo · FACT Cape Town · FALE King Shaka"), FIRS]),
    307: card("A CTA IS NORMALLY ESTABLISHED ABOVE ONE OR MORE TMAs", "THE HIGHER LAYER OF CONTROLLED AIRSPACE", [TMA, CTR]),
    314: card("SURFACE TO A SPECIFIED UPPER LIMIT: A CONTROL ZONE (CTR)", "CONTROLLED AIRSPACE AROUND AN AERODROME", [TMA, CTA]),
    316: card("CONTROL ZONES ARE ESTABLISHED AROUND AERODROMES", "FROM THE SURFACE UP TO A SPECIFIED LIMIT", [TMA, CTA]),
    308: card("TMA: CONTROLLED AIRSPACE AROUND A BUSY AIRPORT", "WHERE SEVERAL ROUTES MEET NEAR ONE OR MORE MAJOR AERODROMES",
              [CTR, CTA]),
    315: card("ATZ = AERODROME TRAFFIC ZONE", "AIRSPACE AROUND AN AERODROME TO PROTECT AERODROME TRAFFIC", [CTR]),
    318: card("CTR, CTA AND TMA NEED A CLEARANCE BEFORE ENTERING", "THEY ARE CONTROLLED AIRSPACE",
              [("FAD / FAR", "Danger and restricted areas: special-use airspace, not controlled airspace")]),
    419: card("TRACK 090° MAGNETIC, VFR: FL075 IS CORRECT", "000°–179° TAKES ODD THOUSANDS PLUS 500 FT", SEMI),
    416: card("THE SEMI-CIRCULAR RULE APPLIES AT AND ABOVE 1500 FT AGL", "CRUISING LEVEL IS CHOSEN BY MAGNETIC TRACK", SEMI),
    438: card("QNE (1013.25 hPa) SET: THE ALTIMETER SHOWS PRESSURE ALTITUDE", "READ AS A FLIGHT LEVEL", SETTINGS[:2]),
    441: card("QFE SET: THE ALTIMETER SHOWS HEIGHT ABOVE THE AERODROME", "IT READS ZERO ON THE RUNWAY",
              [SETTINGS[0], SETTINGS[2]]),
    448: card("THE TRANSITION LEVEL IS ALWAYS ABOVE THE TRANSITION ALTITUDE", "THE GAP BETWEEN THEM IS THE TRANSITION LAYER",
              TRANSITION),
    451: card("CLIMBING THROUGH THE TRANSITION ALTITUDE: SET 1013.25 hPa", "FROM ALTITUDES ON QNH TO FLIGHT LEVELS",
              TRANSITION[1:]),
    570: card("V = REQUIRE ASSISTANCE", "WHITE STRIPS LAID ON THE GROUND FOR A SEARCH AIRCRAFT TO READ",
              [("X", "Require medical assistance"), ("N / Y", "No (negative) / Yes (affirmative)")]),
    576: card("WHITE DUMBBELL: USE ONLY THE RUNWAYS AND TAXIWAYS", "NO MOVEMENT ON THE GRASS",
              [("Dumbbell with black bars", "Land and take off on runways only; taxi anywhere")]),
    578: card("WHITE CROSS AT THE THRESHOLD: THE RUNWAY IS UNSAFE TO USE", "IT IS CLOSED: NO LANDING, TAKE-OFF OR TAXIING",
              [("Where", "A cross at each end of the closed runway or section")]),
}
