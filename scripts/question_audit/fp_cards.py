"""KEY FACT cards for the Flight Planning questions. Each headline states the answer to its own question; the blocks
carry the working. Table readings are the SACAA-01 values (checked 2026-10-07, see
data/question-audit/flight-planning-audit-2026-10-07.md); for the multi-panel graphs the card gives the reading
steps, not invented intermediate values.
"""
import json


def card(headline, subline, blocks, kicker="KEY FACT"):
    return json.dumps({"kicker": kicker, "headline": headline, "subline": subline,
                       "blocks": [{"label": a, "value": b} for a, b in blocks]}, ensure_ascii=False)


ISA = ("ISA", "15°C at sea level, minus 2°C per 1,000 ft")
PA = ("Pressure altitude", "Elevation + (1013 − QNH) × 30 ft")
DA = ("Density altitude", "Pressure altitude + 120 ft per °C above ISA")
TWICE = ("Climb or descent", "Read the chart at both ends and subtract")
USG = ("Units", "1 USG = 3.785 L; litres × SG = kg; 1 kg = 2.205 lb")
MOMENT = ("Moment", "Weight × arm; CG = total moment ÷ total weight")

CARDS = {}


def graph(result, figure, steps):
    return card(result, f"READ {figure}", steps)


# ------------------------------------------------------------------ climb and descent (Figures 1-7, 1-8, 1-15)
CARDS.update({
    2239: graph("DESCENT FUEL ABOUT 2 USG", "FIGURE 1-15 TWICE AND SUBTRACT",
                [("Cruise", "9,000 ft at +16°C: cumulative fuel"), ("Destination", "4,000 ft at ISA (+7°C)"), TWICE]),
    2296: graph("DESCENT TIME ABOUT 25 MINUTES", "FIGURE 1-15 TWICE AND SUBTRACT",
                [("Cruise", "9,500 ft at −5°C: cumulative time"), ("Destination", "2,500 ft at +15°C"), TWICE]),
    2348: graph("DESCENT TIME ABOUT 12 MINUTES", "FIGURE 1-15 TWICE AND SUBTRACT",
                [("Cruise", "8,500 ft at +14°C: cumulative time"), ("Destination", "5,000 ft at +26°C"), TWICE]),
    2257: graph("CLIMB FUEL ABOUT 3 USG", "FIGURE 1-8 TWICE AND SUBTRACT",
                [("Departure", "2,410 ft, QNH 1010 → PA 2,500 ft at ISA (+10°C)"), ("Cruise", "8,500 ft at −4°C"), TWICE]),
    2260: graph("CLIMB TIME ABOUT 20 MINUTES", "FIGURE 1-8 TWICE AND SUBTRACT",
                [("Departure", "2,000 ft at +20°C"), ("Cruise", "FL105 at ISA (−6°C)"), TWICE]),
    2271: graph("CLIMB FUEL ABOUT 3.5 USG", "FIGURE 1-8 TWICE AND SUBTRACT",
                [("Departure", "1,380 ft, QNH 1009 → PA 1,500 ft at ISA (+12°C)"), ("Cruise", "FL075 at ISA +12 (+12°C)"), TWICE]),
    2279: graph("CLIMB TIME ABOUT 13 MINUTES", "FIGURE 1-8 TWICE AND SUBTRACT",
                [("Departure", "4,000 ft at +15°C"), ("Cruise", "FL095 at ISA (−4°C)"), TWICE]),
    2312: graph("CLIMB DISTANCE ABOUT 20 NM", "FIGURE 1-8 TWICE AND SUBTRACT",
                [("Departure", "PA 1,500 ft at ISA (+12°C)"), ("Cruise", "7,500 ft at ISA +12 (+12°C)"), TWICE]),
    2329: graph("CLIMB TIME ABOUT 12 MINUTES", "FIGURE 1-8 TWICE AND SUBTRACT",
                [("Departure", "3,000 ft at ISA (+9°C)"), ("Cruise", "7,500 ft at ISA +12 (+12°C)"), TWICE]),
    2398: graph("CLIMB DISTANCE ABOUT 13 NM", "FIGURE 1-8 TWICE AND SUBTRACT",
                [("Departure", "3,000 ft at +30°C: about 9 NM"), ("Cruise", "FL095 at 0°C: about 22 NM"), ("Distance", "22 − 9 = 13 NM")]),
    2305: graph("RATE OF CLIMB ABOUT 540 FT/MIN", "FIGURE 1-7",
                [("Enter", "+10°C, up to the 4,000 ft line"), ("Read", "Across to the climb line, then the rate scale"),
                 ("Chart", "Full throttle, flaps up, 75 KIAS, 2,500 lb")]),
})

# ------------------------------------------------------------------ atmosphere
CARDS.update({
    2240: card("HIGHER DENSITY ALTITUDE REDUCES CLIMB PERFORMANCE", "THINNER AIR: LESS POWER, THRUST AND LIFT",
               [("Also", "Longer take-off and landing runs"), ("Caused by", "High elevation, high temperature, low pressure")]),
    2375: card("A HOTTER DAY INCREASES DENSITY ALTITUDE", "WARM AIR IS LESS DENSE", [DA, ("Effect", "Poorer take-off and climb")]),
    2374: card("DENSITY ALTITUDE ABOUT 4,560 FT", "PRESSURE ALTITUDE, THEN THE ISA DEVIATION",
               [("Pressure altitude", "3,210 + (1013 − 1020) × 30 = 3,000 ft"), ("ISA at 3,000 ft", "+9°C, so 22°C is ISA +13"),
                ("Density altitude", "3,000 + 120 × 13 = 4,560 ft")]),
    2283: card("AERODROME ELEVATION 2,500 FT", "WORK BACK FROM PRESSURE ALTITUDE",
               [("Working", "2,650 − (1013 − 1008) × 30 = 2,500 ft"), PA]),
    2371: card("PRESSURE ALTITUDE 1,500 FT", "QNH BELOW 1013: PRESSURE ALTITUDE IS HIGHER",
               [("Working", "1,200 + (1013 − 1003) × 30 = 1,500 ft"), PA]),
    2327: card("ISA AT FL055 IS +4°C", "15 − 2 × 5.5", [ISA]),
    2372: card("OAT ABOUT +5°C", "ISA AT THE LEVEL, THEN ADD THE DEVIATION",
               [("ISA at FL085", "15 − 17 = −2°C"), ("OAT", "−2 + 7 = +5°C")]),
    2373: card("ISA DEVIATION +9°C", "ACTUAL TEMPERATURE − ISA TEMPERATURE",
               [("ISA at FL095", "15 − 19 = −4°C"), ("Deviation", "5 − (−4) = +9°C")]),
})

# ------------------------------------------------------------------ airspeed and stall speed
CAL = ("Order", "IAS → CAS: corrects instrument and position error")
CARDS.update({
    2249: card("58 KIAS WITH FLAPS 40° IS ABOUT 60 KCAS", "INTERPOLATE FIGURE 1-19",
               [("Flaps 40° row", "50 KIAS → 54 KCAS; 60 → 62"), ("Working", "54 + 0.8 × 8 = 60.4 KCAS")]),
    2291: card("77 KIAS WITH FLAPS 40° IS 78 KCAS", "INTERPOLATE FIGURE 1-19",
               [("Flaps 40° row", "70 KIAS → 71 KCAS; 80 → 81"), ("Working", "71 + 0.7 × 10 = 78 KCAS")]),
    2347: card("98 KIAS WITH FLAPS 10° IS ABOUT 97 KCAS", "INTERPOLATE FIGURE 1-19",
               [("Flaps 10° row", "90 KIAS → 91 KCAS; 100 → 99"), ("Working", "91 + 0.8 × 8 = 97.4 KCAS")]),
    2351: card("57 KIAS FLAPS UP IS ABOUT 61 KCAS", "INTERPOLATE FIGURE 1-19",
               [("Flaps up row", "50 KIAS → 56 KCAS; 60 → 63"), ("Working", "56 + 0.7 × 7 = 60.9 KCAS")]),
    2354: card("95 KIAS FLAPS UP IS 94 KCAS", "INTERPOLATE FIGURE 1-19",
               [("Flaps up row", "90 KIAS → 90 KCAS; 100 → 98"), ("Working", "90 + 0.5 × 8 = 94 KCAS")]),
    2323: card("120 KCAS FLAPS UP IS ABOUT 124 KIAS", "FIGURE 1-1 READ BACKWARDS",
               [("Read", "Across from 120 CAS to the 0° flaps line, down to IAS"), CAL]),
    2335: card("90 KIAS WITH 40° FLAP IS ABOUT 87 KCAS", "FIGURE 1-1",
               [("Read", "Up from 90 IAS to the 40° flaps line, across to CAS"), CAL]),
    2343: card("95 KIAS FLAPS UP IS ABOUT 96 KCAS", "FIGURE 1-1",
               [("Read", "Up from 95 IAS to the 0° flaps line, across to CAS"), CAL]),
    2357: card("100 KIAS FLAPS UP IS ABOUT 100 KCAS", "FIGURE 1-1",
               [("Read", "Up from 100 IAS to the 0° flaps line, across to CAS"), CAL]),
    2290: card("STALL SPEED 57 KIAS", "FIGURE 1-21: HALFWAY BETWEEN 2,400 AND 2,200 LB",
               [("Flaps 40°, 60° bank", "2,400 lb: 60 KIAS; 2,200 lb: 54 KIAS"), ("Working", "(60 + 54) ÷ 2 = 57 KIAS")]),
    2242: card("STALL SPEED ABOUT 48 KIAS", "FIGURE 1-2, WINGS LEVEL",
               [("Enter", "2,350 lb on the weight scale"), ("Follow", "The 40° flap line to the IAS scale")]),
    2292: card("STALL SPEED ABOUT 48.5 KIAS", "FIGURE 1-2: WEIGHT, THEN BANK",
               [("Enter", "2,250 lb, along the 25° flap line"), ("Bank", "Follow the guide curves out to 15°")]),
    2334: card("WEIGHT ABOUT 2,400 LB", "FIGURE 1-2 READ BACKWARDS",
               [("Bank", "54 KIAS at 40° bank back to wings level (about 48.5 KIAS)"),
                ("Weight", "Along the 40° flap line to the weight scale")]),
    2403: card("STALL SPEED ABOUT 54 KIAS", "FIGURE 1-2 AT 2,500 LB",
               [("Wings level", "25° flap at 2,500 lb: about 51 KIAS"), ("Bank", "Guide curves out to 30°: about 54 KIAS")]),
})

# ------------------------------------------------------------------ cruise, range and endurance
CRUISE = ("Figure 1-23", "2,300 lb, mixture leaned, zero wind, 48 USG, no reserve")
CARDS.update({
    2252: card("ENDURANCE 7.2 HOURS", "FIGURE 1-23 AT 2,400 RPM, HALFWAY BETWEEN ROWS",
               [("8,000 ft / 10,000 ft", "6.8 h / 7.6 h"), ("9,000 ft", "(6.8 + 7.6) ÷ 2 = 7.2 h"), CRUISE]),
    2337: card("TAS 121 KT", "FIGURE 1-23 AT 2,600 RPM, HALFWAY BETWEEN ROWS",
               [("6,000 ft / 8,000 ft", "123 / 119 KTAS"), ("7,000 ft", "(123 + 119) ÷ 2 = 121 KTAS")]),
    2345: card("62% BHP", "FIGURE 1-23 AT 2,300 RPM, HALFWAY BETWEEN ROWS",
               [("2,000 ft / 4,000 ft", "64% / 60%"), ("3,000 ft", "(64 + 60) ÷ 2 = 62%")]),
    2386: card("RANGE ABOUT 785 NM", "FIGURE 1-23 AT 2,400 RPM, HALFWAY BETWEEN ROWS",
               [("4,000 ft / 6,000 ft", "780 / 790 NM"), ("5,000 ft", "(780 + 790) ÷ 2 = 785 NM"), CRUISE]),
    2387: card("FUEL FLOW ABOUT 7.5 GPH", "FIGURE 1-23 AT 2,400 RPM, HALFWAY BETWEEN ROWS",
               [("2,000 ft / 4,000 ft", "7.7 / 7.3 GPH"), ("3,000 ft", "(7.7 + 7.3) ÷ 2 = 7.5 GPH")]),
    2388: card("ABOUT 72% BHP", "FIGURE 1-23 AT 2,500 RPM, HALFWAY BETWEEN ROWS",
               [("4,000 ft / 6,000 ft", "74% / 70%"), ("5,000 ft", "(74 + 70) ÷ 2 = 72%")]),
    2261: graph("ABOUT 2,490 RPM", "FIGURE 1-9",
                [("Enter", "8,500 ft at ISA +2 (0°C)"), ("Read", "Up to the 65% power curve, across to RPM")]),
    2294: graph("ABOUT 2,380 RPM", "FIGURE 1-9",
                [("Enter", "6,500 ft at +10°C"), ("Read", "Up to the 60% power curve, across to RPM")]),
    2399: graph("ABOUT 2,480 RPM", "FIGURE 1-9",
                [("Enter", "4,500 ft at ISA (+6°C)"), ("Read", "Up to the 70% power curve, across to RPM")]),
    2272: graph("65% POWER", "FIGURE 1-10",
                [("Enter", "6,500 ft at +11°C"), ("Read", "Across to 116 KTAS: the power curve through it")]),
    2376: graph("TAS ABOUT 117 KT", "FIGURE 1-10",
                [("Enter", "7,500 ft at +5°C"), ("Read", "To the 65% curve, then the TAS scale")]),
    2377: graph("ABOUT 75% POWER", "FIGURE 1-10 WITH TAS, NOT GROUNDSPEED",
                [("TAS", "111 + 9 headwind = 120 kt"), ("Enter", "2,500 ft at ISA +4 (+14°C), across to 120 KTAS")]),
    2378: graph("TAS ABOUT 103 KT", "FIGURE 1-11",
                [("Enter", "10,500 ft at 0°C"), ("Read", "To the 55% curve, then the TAS scale")]),
    2379: graph("65% POWER", "FIGURE 1-11",
                [("Enter", "4,000 ft at ISA (+7°C)"), ("Read", "Across to 110 KTAS: the power curve through it")]),
    2280: graph("55% POWER", "FIGURE 1-12, RANGE WITH RESERVE",
                [("Enter", "8,000 ft at ISA −7 (−8°C)"), ("Read", "Across to 580 NM: the power curve through it")]),
    2284: graph("RANGE ABOUT 680 NM", "FIGURE 1-12, NO RESERVE",
                [("Enter", "8,000 ft at ISA +11 (+10°C)"), ("Read", "To the 55% curve, then the range scale")]),
    2302: graph("RANGE ABOUT 605 NM", "FIGURE 1-12, NO RESERVE",
                [("Enter", "7,500 ft at +5°C"), ("Read", "To the 75% curve, then the range scale")]),
    2322: graph("65% POWER", "FIGURE 1-12, RANGE WITH RESERVE",
                [("Enter", "3,000 ft at +26°C"), ("Read", "Across to 550 NM: the power curve through it")]),
    2324: graph("RANGE ABOUT 585 NM", "FIGURE 1-12, NO RESERVE",
                [("Enter", "5,500 ft at ISA (+4°C)"), ("Read", "To the 75% curve, then the range scale")]),
    2414: graph("65% POWER", "FIGURE 1-12, NO RESERVE",
                [("Enter", "4,000 ft at ISA +5 (+12°C)"), ("Read", "Across to 620 NM: the power curve through it")]),
    2338: graph("RANGE ABOUT 735 NM", "FIGURE 1-13, NO RESERVE",
                [("Enter", "3,500 ft at ISA +7 (+15°C)"), ("Read", "To the 55% curve, then the range scale")]),
    2359: graph("65% POWER", "FIGURE 1-13, NO RESERVE",
                [("Enter", "6,500 ft at +15°C"), ("Read", "Across to 720 NM: the power curve through it")]),
    2400: graph("RANGE ABOUT 765 NM", "FIGURE 1-13, NO RESERVE",
                [("Enter", "10,500 ft at ISA (−6°C)"), ("Read", "To the 55% curve, then the no-reserve scale")]),
})

# ------------------------------------------------------------------ fuel planning
CARDS.update({
    2243: card("RESERVE FUEL 12.6 USG", "TOTAL − TRIP − TAXI, TAKE-OFF AND CLIMB",
               [("Trip", "225 ÷ 100 = 2.25 h × 8.5 = 19.1 USG"), ("Reserve", "35 − 19.1 − 3.3 = 12.6 USG")]),
    2262: card("RESERVE FUEL 6 USG", "TOTAL − TRIP FUEL",
               [("Trip", "135 ÷ 90 = 1.5 h × 8 = 12 USG"), ("Reserve", "18 − 12 = 6 USG")]),
    2256: card("ABOUT 37 MINUTES HOLDING", "ONLY THE FUEL ABOVE TRIP AND RESERVE",
               [("Spare fuel", "27 − 14 − 9 = 4 USG"), ("Time", "4 ÷ 6.5 = 0.615 h ≈ 37 min")]),
    2332: card("TOTAL FUEL 19.4 USG", "TAXI AND CLIMB + TRIP + RESERVE",
               [("Trip", "107 ÷ 92 = 1.163 h × 7.2 = 8.4 USG"), ("Total", "3 + 8.4 + 8 = 19.4 USG")]),
    2268: card("FUEL FLOW 10.6 USG/HR", "FUEL USED ÷ TIME",
               [("Time", "180 ÷ 100 = 1.8 h"), ("Flow", "19 ÷ 1.8 = 10.6 USG/h")]),
    2318: card("FUEL FLOW 10.9 USG/HR", "FUEL USED ÷ TIME",
               [("Time", "120 ÷ 90 = 1.333 h"), ("Flow", "14.5 ÷ 1.333 = 10.9 USG/h")]),
    2408: card("FUEL FLOW ABOUT 7.5 USG/HR", "FUEL USED ÷ TIME",
               [("Time", "158 ÷ 95 = 1.663 h"), ("Flow", "12.5 ÷ 1.663 = 7.5 USG/h")]),
    2265: card("42 USG AT SG 0.72 WEIGHS ABOUT 114 KG", "LITRES × SG = KILOGRAMS",
               [("Litres", "42 × 3.785 = 159 L"), ("Mass", "159 × 0.72 = 114.5 kg")]),
    2310: card("ABOUT 67 USG", "KILOGRAMS ÷ SG = LITRES",
               [("Litres", "185 ÷ 0.73 = 253 L"), ("USG", "253 ÷ 3.785 = 66.9 USG")]),
    2341: card("300 L AT SG 0.72 WEIGHS ABOUT 476 LB", "LITRES × SG = KILOGRAMS",
               [("Mass", "300 × 0.72 = 216 kg"), ("Pounds", "216 × 2.205 = 476 lb")]),
    2404: card("108 KG AT SG 0.73 IS ABOUT 148 LITRES", "KILOGRAMS ÷ SG = LITRES", [("Working", "108 ÷ 0.73 = 147.9 L"), USG]),
    2286: card("GROUNDSPEED ABOUT 92 KT", "NM PER KG × KG PER HOUR = NM PER HOUR",
               [("Mass flow", "8.5 × 3.785 × 0.71 = 22.8 kg/h"), ("Groundspeed", "22.8 × 4.0 = 91.4 kt")]),
    2405: card("TAS ABOUT 109 KT", "GROUND NM PER LB GIVES GROUNDSPEED; ADD THE HEADWIND",
               [("Mass flow", "22.8 kg/h = 50.4 lb/h"), ("Groundspeed", "50.4 × 2.0 = 100.8 kt"), ("TAS", "100.8 + 8 = 108.8 kt")]),
    2353: card("GROUNDSPEED ABOUT 120 KT", "AIR NM PER LITRE GIVES TAS; ADD THE TAILWIND",
               [("Flow", "8.5 × 3.785 = 32.2 L/h"), ("TAS", "32.2 × 3.5 = 112.6 kt"), ("Groundspeed", "112.6 + 7 = 119.6 kt")]),
    2416: card("TAS ABOUT 112 KT", "AIR NM PER LITRE × LITRES PER HOUR",
               [("Flow", "7.8 × 3.785 = 29.5 L/h"), ("TAS", "29.5 × 3.8 = 112.2 kt")]),
})

# ------------------------------------------------------------------ mass and balance (definitions, floor load, Figures 2-2, 2-3)
WEIGHTS = ("Order", "Basic empty → zero fuel → take-off → ramp")
CARDS.update({
    2244: card("MAXIMUM RAMP WEIGHT = MTOW + TAXI FUEL", "THE TAXI FUEL IS BURNT BEFORE BRAKE RELEASE", [WEIGHTS]),
    2246: card("MTOW MAY BE EXCEEDED ONLY BY THE TAXI FUEL", "AT OR BELOW MTOW WHEN THE TAKE-OFF ROLL STARTS",
               [("Limit on the ramp", "Maximum ramp weight")]),
    2308: card("MAXIMUM RAMP WEIGHT 2,585 LB", "MTOW + TAXI FUEL", [("Working", "2,580 + 5 = 2,585 lb"), WEIGHTS]),
    2316: card("MAXIMUM TAKE-OFF WEIGHT 2,440 LB", "RAMP WEIGHT − TAXI FUEL", [("Working", "2,445 − 5 = 2,440 lb"), WEIGHTS]),
    2270: card("THAT IS THE ZERO FUEL WEIGHT", "EVERYTHING EXCEPT USABLE FUEL", [("Includes", "Aircraft, crew, passengers, baggage, cargo"), WEIGHTS]),
    2406: card("ZERO FUEL WEIGHT = EMPTY WEIGHT + CREW, PASSENGERS, BAGGAGE AND CARGO", "NO USABLE FUEL", [WEIGHTS]),
    2392: card("MAXIMUM ZERO FUEL WEIGHT: THE LIMIT WITH NO USABLE FUEL ABOARD", "PROTECTS THE WING ROOTS FROM PAYLOAD BENDING",
               [("Zero fuel weight", "The actual figure; it must not exceed this limit")]),
    2370: card("THAT IS THE BASIC EMPTY WEIGHT", "THE STARTING POINT OF EVERY LOADING SUM",
               [("Includes", "Fixed equipment, unusable fuel, full operating fluids"), ("Excludes", "Usable fuel, people, baggage")]),
    2415: card("BASIC EMPTY WEIGHT INCLUDES UNUSABLE FUEL, FULL OIL AND FIXED EQUIPMENT", "NO USABLE FUEL, PEOPLE OR BAGGAGE", [WEIGHTS]),
    2275: card("108 LB CAN GO IN THE BOX", "FLOOR LIMIT × AREA, MINUS THE BOX",
               [("Floor load", "20 × (2 × 3) = 120 lb"), ("Contents", "120 − 12 = 108 lb")]),
    2289: card("41.4 KG MAY BE LOADED", "FLOOR LIMIT × AREA", [("Working", "23 × (1.2 × 1.5) = 41.4 kg")]),
    2311: card("UTILITY CATEGORY: SPINS ALLOWED INSIDE THE UTILITY ENVELOPE", "WEIGHT AND CG MUST BOTH BE IN IT",
               [("Figure 2-3", "Utility: up to about 2,040 lb, CG no further aft than 87 in")]),
    2325: card("UTILITY CATEGORY: 1,920 LB AT 84.6 IN", "PLOT WEIGHT AND CG ON FIGURE 2-3",
               [("Total", "1,920 lb; moment 162,393 lb-in"), ("CG", "162,393 ÷ 1,920 = 84.58 in"),
                ("Utility envelope", "About 82–87 in at this weight")]),
    2410: card("UTILITY CATEGORY: 2,020 LB AT 84.2 IN", "PLOT WEIGHT AND CG ON FIGURE 2-3",
               [("Total", "2,020 lb; moment 170,173 lb-in"), ("CG", "170,173 ÷ 2,020 = 84.24 in"),
                ("Utility envelope", "Up to about 2,040 lb, 83–87 in here")]),
    2282: card("ABOUT 140.6 KG", "FIGURE 2-2, PILOT AND FRONT PASSENGER LINE",
               [("Weight", "24,000 ÷ 77.8 = 308.5 lb (graph about 310 lb)"), ("Kilograms", "310 ÷ 2.205 = 140.6 kg")]),
    2309: card("MOMENT/1000 ABOUT 24.8", "FIGURE 2-2 IS IN POUNDS",
               [("Weight", "145 kg × 2.205 = 320 lb"), ("Moment", "320 × 77.8 = 24,870 lb-in")]),
    2346: card("MOMENT/1000 ABOUT 24", "FIGURE 2-2, BAGGAGE LINE", [("Working", "170 × 140.5 = 23,885 lb-in"), MOMENT]),
    2407: card("MOMENT/1000 ABOUT 19.5", "FIGURE 2-2, FUEL LINE (6 LB/USG)",
               [("Weight", "35 × 6 = 210 lb"), ("Moment", "210 × 93 = 19,530 lb-in")]),
})

# ------------------------------------------------------------------ V-speeds without a picture
CARDS.update({
    2321: card("VA IS THE DESIGN MANOEUVRING SPEED", "AT OR BELOW VA A FULL CONTROL INPUT STALLS THE WING FIRST",
               [("Lighter aircraft", "Lower VA"), ("Not marked", "VA has no arc on the ASI")]),
    2344: card("VLO: MAXIMUM SPEED TO OPERATE THE LANDING GEAR", "EXTENDING OR RETRACTING",
               [("VLE", "Maximum speed with the gear already extended")]),
})

# ------------------------------------------------------------------ batch 2: questions with the new pictures
TO_NOTES = ("Figure 1-22 notes", "Grass: add 10% of the ground roll; headwind −10% per 5 kt; tailwind +10% per 2 kt")
LDG_NOTES = ("Figure 1-24 notes", "Grass: add 25% of the ground roll; wind ±10% per 10 kt")

# take-off: Figure 1-22 table
CARDS.update({
    2247: card("2,265 FT TO CLEAR 50 FT", "FIGURE 1-22, PA 4,000 FT, MIDWAY +10°C TO +20°C",
               [("Table", "2,185 ft at +10°C; 2,345 ft at +20°C"), ("+15°C", "(2,185 + 2,345) ÷ 2 = 2,265 ft")]),
    2317: card("2,235 FT TO CLEAR 50 FT", "FIGURE 1-22, +20°C, MIDWAY PA 3,000 TO 4,000 FT",
               [("Table", "2,125 ft at 3,000 ft; 2,345 ft at 4,000 ft"), ("3,500 ft", "(2,125 + 2,345) ÷ 2 = 2,235 ft")]),
    2320: card("GROUND ROLL 1,500 FT", "FIGURE 1-22, THEN THE TAILWIND NOTE",
               [("3,500 ft, +20°C", "(1,190 + 1,310) ÷ 2 = 1,250 ft"), ("4 kt tailwind", "+20%: 1,250 × 1.2 = 1,500 ft")]),
    2330: card("2,306 FT TO CLEAR 50 FT", "FIGURE 1-22, THEN GRASS AND TAILWIND",
               [("3,000 ft, +10°C", "Ground roll 1,110 ft; total 1,985 ft"), ("Grass", "1,985 + 111 = 2,096 ft"),
                ("2 kt tailwind", "+10%: 2,096 × 1.1 = 2,306 ft")]),
    2358: card("2,160 FT TO CLEAR 50 FT", "PRESSURE ALTITUDE FIRST, THEN FIGURE 1-22",
               [("Pressure altitude", "3,650 + (1013 − 1018) × 30 = 3,500 ft"),
                ("3,500 ft", "2,085 ft at +10°C; 2,235 ft at +20°C"), ("+15°C", "(2,085 + 2,235) ÷ 2 = 2,160 ft")]),
    2381: card("GROUND ROLL ABOUT 1,223 FT", "FIGURE 1-22, THEN GRASS AND HEADWIND",
               [("5,000 ft, +15°C", "(1,340 + 1,440) ÷ 2 = 1,390 ft"), ("Grass", "1,390 × 1.1 = 1,529 ft"),
                ("10 kt headwind", "−20%: 1,529 × 0.8 = 1,223 ft")]),
    2382: card("ABOUT 2,650 FT TO CLEAR 50 FT", "FIGURE 1-22, THEN GRASS AND HEADWIND",
               [("5,000 ft, +30°C", "Ground roll 1,550 ft; total 2,790 ft"), ("Grass", "2,790 + 155 = 2,945 ft"),
                ("5 kt headwind", "−10%: 2,945 × 0.9 = 2,650 ft")]),
    2383: card("2,428 FT TO CLEAR 50 FT", "FIGURE 1-22, THEN THE GRASS NOTE",
               [("4,500 ft, +10°C", "Ground roll 1,280 ft; total 2,300 ft"), ("Grass", "2,300 + 10% of 1,280 = 2,428 ft")]),
    2384: card("ABOUT 1,490 FT TO CLEAR 50 FT", "FIGURE 1-22, THEN THE HEADWIND NOTE",
               [("1,000 ft, +10°C", "1,655 ft"), ("5 kt headwind", "−10%: 1,655 × 0.9 = 1,490 ft")]),
    2385: card("GROUND ROLL ABOUT 885 FT", "FIGURE 1-22, +10°C, MIDWAY SEA LEVEL TO 1,000 FT",
               [("Table", "845 ft at sea level; 925 ft at 1,000 ft"), ("500 ft", "(845 + 925) ÷ 2 = 885 ft")]),
})


def tgraph(result, figure, steps):
    return card(result, f"READ {figure}", steps)


# take-off: Figures 1-3 to 1-6 (graphs)
CARDS.update({
    2248: tgraph("GROUND ROLL ABOUT 1,900 FT", "FIGURE 1-3 (FLAPS UP)",
                 [("Temperature", "ISA at 3,500 ft is +8°C, so ISA +22 = +30°C"),
                  ("Enter", "+30°C, up to 3,500 ft, across to the reference line"), ("2,500 lb, no wind", "Straight on to the scale")]),
    2393: tgraph("GROUND ROLL ABOUT 1,475 FT", "FIGURE 1-3 (FLAPS UP)",
                 [("Enter", "+20°C, up to 5,000 ft, across to the reference line"), ("Weight", "Follow the lines down to 2,400 lb"),
                  ("Wind", "Follow the headwind lines out to 10 kt")]),
    2394: tgraph("MAXIMUM WEIGHT ABOUT 2,500 LB", "FIGURE 1-3 BACKWARDS",
                 [("Ground roll", "1,200 ft, down to the 10 kt headwind line"), ("Conditions", "+30°C at 2,500 ft from the left"),
                  ("Weight", "Where the two meet: about 2,500 lb")]),
    2395: tgraph("GROUND ROLL ABOUT 1,350 FT", "FIGURE 1-3 (FLAPS UP)",
                 [PA, ("Here", "650 + (1013 − 1018) × 30 = 500 ft"), ("Enter", "+25°C, 500 ft, 2,500 lb, tailwind 5 kt")]),
    2288: tgraph("MAXIMUM WEIGHT ABOUT 1,920 LB", "FIGURE 1-4 BACKWARDS",
                 [("Distance", "1,850 ft, down to the zero-wind reference line"), ("Conditions", "+26°C at 5,000 ft from the left"),
                  ("Weight", "Where the two meet: about 1,920 lb")]),
    2293: tgraph("ABOUT 1,700 FT OVER 50 FT", "FIGURE 1-4 (FLAPS UP)",
                 [("Pressure altitude", "4,090 + (1013 − 1016) × 30 = 4,000 ft"), ("Enter", "−2°C, 4,000 ft, then 2,360 lb"),
                  ("No wind", "Straight up to the distance scale")]),
    2269: tgraph("GROUND ROLL ABOUT 1,350 FT", "FIGURE 1-5 (25° FLAPS)",
                 [("Enter", "+25°C, 4,500 ft, across to the reference line"), ("Weight", "Down to 2,450 lb"),
                  ("Wind", "Headwind lines out to 5 kt")]),
    2306: tgraph("GROUND ROLL ABOUT 950 FT", "FIGURE 1-5 (25° FLAPS)",
                 [("Pressure altitude", "3,450 + (1013 − 1008) × 30 = 3,600 ft"), ("Enter", "−2°C, 3,600 ft, then 2,350 lb"),
                  ("Wind", "Tailwind lines out to 3 kt")]),
    2336: tgraph("GROUND ROLL ABOUT 650 FT", "FIGURE 1-5 (25° FLAPS)",
                 [("Pressure altitude", "1,910 + (1013 − 1010) × 30 = 2,000 ft"), ("Enter", "+4°C, 2,000 ft, then 2,440 lb"),
                  ("No wind", "Straight up to the ground-roll scale")]),
    2339: tgraph("MAXIMUM TEMPERATURE ABOUT +27°C", "FIGURE 1-5 BACKWARDS",
                 [("Ground roll", "1,500 ft, down to the zero-wind reference line"), ("2,500 lb", "Across to the 4,000 ft line"),
                  ("Temperature", "Down to the scale: about +27°C")]),
    2326: tgraph("ABOUT 1,900 FT OVER 50 FT", "FIGURE 1-6 (25° FLAPS)",
                 [("Pressure altitude", "4,880 + (1013 − 1009) × 30 = 5,000 ft"), ("Enter", "−5°C, 5,000 ft, then 2,260 lb"),
                  ("Wind", "Tailwind lines out to 4 kt")]),
    2352: tgraph("ABOUT 2,275 FT OVER 50 FT", "FIGURE 1-6 (25° FLAPS)",
                 [("Temperature", "ISA at 3,500 ft is +8°C"), ("Enter", "+8°C, 3,500 ft, 2,500 lb"), ("Wind", "Tailwind lines out to 3 kt")]),
    2396: tgraph("MAXIMUM WEIGHT ABOUT 2,300 LB", "FIGURE 1-6 BACKWARDS",
                 [("Distance", "1,650 ft, down to the 5 kt headwind line"), ("Conditions", "+20°C at 4,000 ft from the left"),
                  ("Weight", "Where the two meet: about 2,300 lb")]),
    2397: tgraph("ABOUT 1,125 FT OVER 50 FT", "FIGURE 1-6 (25° FLAPS)",
                 [("Pressure altitude", "1,410 + (1013 − 1010) × 30 = 1,500 ft"), ("Enter", "+24°C, 1,500 ft, then 2,340 lb"),
                  ("Wind", "Headwind lines out to 7 kt")]),
})

# landing: Figure 1-24 table, Figures 1-17 and 1-18 graphs
CARDS.update({
    2266: card("ABOUT 1,615 FT TO CLEAR 50 FT", "FIGURE 1-24, THEN GRASS AND TAILWIND",
               [("2,000 ft, +35°C", "Ground roll 605 ft; total 1,402.5 ft"), ("Grass", "1,402.5 + 25% of 605 = 1,553.8 ft"),
                ("4 kt tailwind", "+4%: 1,553.8 × 1.04 = 1,615 ft")]),
    2281: card("GROUND ROLL ABOUT 617 FT", "PRESSURE ALTITUDE FIRST, THEN FIGURE 1-24",
               [("Pressure altitude", "4,350 + (1013 − 1008) × 30 = 4,500 ft"), ("4,500 ft", "607.5 ft at +10°C; 630 ft at +20°C"),
                ("+14°C", "607.5 + 0.4 × 22.5 = 617 ft")]),
    2313: card("GROUND ROLL ABOUT 695 FT", "FIGURE 1-24, THEN GRASS AND HEADWIND",
               [("2,500 ft, +20°C", "(575 + 595) ÷ 2 = 585 ft"), ("Grass", "585 × 1.25 = 731 ft"), ("5 kt headwind", "−5%: 731 × 0.95 = 695 ft")]),
    2389: card("ABOUT 1,382 FT TO CLEAR 50 FT", "PRESSURE ALTITUDE FIRST, THEN FIGURE 1-24",
               [("Pressure altitude", "2,650 + (1013 − 1018) × 30 = 2,500 ft"), ("2,500 ft", "1,367.5 ft at +20°C; 1,402.5 ft at +30°C"),
                ("+24°C", "1,367.5 + 0.4 × 35 = 1,382 ft")]),
    2315: tgraph("ABOUT 1,100 FT OVER 50 FT", "FIGURE 1-17",
                 [("Pressure altitude", "940 + (1013 − 1011) × 30 = 1,000 ft"), ("Enter", "+26°C, 1,000 ft, then 2,150 lb"),
                  ("Wind", "Headwind lines out to 7 kt")]),
    2380: tgraph("ABOUT 1,290 FT OVER 50 FT", "FIGURE 1-17",
                 [("Enter", "+32°C, 5,000 ft, across the reference lines (2,500 lb)"), ("Wind", "Headwind lines out to 13 kt")]),
    2301: tgraph("GROUND ROLL ABOUT 750 FT", "FIGURE 1-18",
                 [("Enter", "+25°C, 3,500 ft, across to the reference line"), ("Weight", "Down to 2,300 lb"), ("No wind", "Straight up to the scale")]),
    2356: tgraph("GROUND ROLL ABOUT 675 FT", "FIGURE 1-18",
                 [("Pressure altitude", "2,800 + (1013 − 1023) × 30 = 2,500 ft"), ("Enter", "+10°C, 2,500 ft, then 2,250 lb"),
                  ("No wind", "Straight up to the scale")]),
})

# glide range: Figure 1-16
GLIDE = ("Figure 1-16", "Height above the terrain in, glide range out")
CARDS.update({
    2250: card("GLIDE RANGE ABOUT 19 NM", "HEIGHT = 10,500 − 1,500 = 9,000 FT", [GLIDE]),
    2253: card("GLIDE RANGE ABOUT 10 NM", "HEIGHT = 8,500 − 4,000 = 4,500 FT",
               [("Terrain", "4,300 + (1013 − 1023) × 30 = 4,000 ft pressure altitude"), GLIDE]),
    2274: card("GLIDE RANGE ABOUT 14 NM", "HEIGHT = 9,000 − 2,500 = 6,500 FT",
               [("Terrain", "2,620 + (1013 − 1017) × 30 = 2,500 ft pressure altitude"), GLIDE]),
    2304: card("GLIDE RANGE ABOUT 13 NM", "HEIGHT = 9,500 − 3,500 = 6,000 FT", [GLIDE]),
    2360: card("GLIDE RANGE ABOUT 22.5 NM", "HEIGHT = 11,500 − 500 = 11,000 FT",
               [("Terrain", "440 + (1013 − 1011) × 30 = 500 ft pressure altitude"), GLIDE]),
})

# mass and balance
CARDS.update({
    2263: card("NEW CG 91.65 IN", "ADD THE MOMENTS, THEN DIVIDE",
               [("Moments", "195,800 + 20,405 + 4,215 = 220,420 lb-in"), ("Weight", "2,200 + 175 + 30 = 2,405 lb (under 2,500)"),
                ("CG", "220,420 ÷ 2,405 = 91.65 in")]),
    2295: card("LANDING CG 89.4 IN", "TAKE AWAY THE FUEL'S MOMENT",
               [("Moment", "224,250 − 208 × 93 = 204,906 lb-in"), ("Weight", "2,500 − 208 = 2,292 lb"), ("CG", "204,906 ÷ 2,292 = 89.4 in")]),
    2299: card("LOADED CG 86.01 IN", "ADD THE MOMENTS, THEN DIVIDE",
               [("Moments", "116,610 + 24,118 + 25,850 + 9,320 = 175,898 lb-in"), ("Weight", "1,380 + 310 + 275 + 80 = 2,045 lb"),
                ("CG", "175,898 ÷ 2,045 = 86.01 in")]),
    2303: card("LANDING CG 88.35 IN", "TAKE AWAY THE FUEL'S MOMENT",
               [("Moment", "208,445 − 175 × 93 = 192,170 lb-in"), ("Weight", "2,350 − 175 = 2,175 lb"), ("CG", "192,170 ÷ 2,175 = 88.35 in")]),
    2331: card("THE CG MOVES FORWARD", "FUEL BURNT BEHIND THE CG (93 IN > 89.2 IN)",
               [("Moment", "220,324 − 173 × 93 = 204,235 lb-in"), ("CG", "204,235 ÷ 2,297 = 88.91 in, forward of 89.2")]),
    2340: card("NEW CG 91.4 IN", "ADD THE PASSENGER'S MOMENT",
               [("Moment", "201,328.8 + 180 × 116.6 = 222,316.8 lb-in"), ("Weight", "2,252 + 180 = 2,432 lb"), ("CG", "222,316.8 ÷ 2,432 = 91.4 in")]),
    2355: card("MOMENT = WEIGHT × ARM", "THE TURNING EFFECT ABOUT THE DATUM", [MOMENT]),
    2368: card("WEIGHT = MOMENT ÷ ARM", "REARRANGE MOMENT = WEIGHT × ARM", [MOMENT]),
    2369: card("ARM = MOMENT ÷ WEIGHT", "REARRANGE MOMENT = WEIGHT × ARM", [MOMENT]),
    2401: card("NEW CG ABOUT 89.0 IN", "FUEL WEIGHT FIRST: 22 × 6 = 132 LB",
               [("Moment", "204,240 + 132 × 93 = 216,516 lb-in"), ("Weight", "2,300 + 132 = 2,432 lb"), ("CG", "216,516 ÷ 2,432 = 89.03 in")]),
    2402: card("LANDING CG ABOUT 87.7 IN", "TAKE AWAY THE FUEL'S MOMENT",
               [("Moment", "216,335 − 280 × 93 = 190,295 lb-in"), ("Weight", "2,450 − 280 = 2,170 lb"), ("CG", "190,295 ÷ 2,170 = 87.7 in")]),
    2411: card("LOADED CG ABOUT 85.87 IN", "ADD THE MOMENTS, THEN DIVIDE",
               [("Moments", "126,203 + 27,230 + 19,530 + 11,660 = 184,623 lb-in"), ("Weight", "1,490 + 350 + 210 + 100 = 2,150 lb"),
                ("CG", "184,623 ÷ 2,150 = 85.87 in")]),
    2417: card("NEW CG ABOUT 92.0 IN", "THE SWAP MOVES 60 LB AFT BY 38.8 IN",
               [("Swap", "60 × 38.8 = +2,328 lb-in"), ("Fuel", "50 × 93 = +4,650 lb-in"),
                ("CG", "225,378 ÷ 2,450 = 91.99 in")]),
})

# runway distances and slope
SLOPE = ("Slope", "Elevation difference ÷ runway length × 100, same units")
LDA = ("LDA", "From the landing threshold to the end of the runway")
CARDS.update({
    2245: card("A DISPLACED THRESHOLD DOES NOT REDUCE TODA", "THE PAVEMENT BEFORE IT IS STILL USED FOR TAKE-OFF", [LDA]),
    2251: card("TODA 1,550 M", "THE DISPLACED THRESHOLD ONLY AFFECTS LANDING", [("LDA", "1,550 − 30 = 1,520 m")]),
    2366: card("TAKE OFF FROM THE START OF THE RUNWAY", "IF THE PAVEMENT IS MARKED AND SUITABLE",
               [("The displacement", "Is not used for landing in that direction")]),
    2267: card("LDA 1,125 M", "RUNWAY − DISPLACEMENT; THE STOPWAY IS NOT INCLUDED", [("Working", "1,150 − 25 = 1,125 m")]),
    2273: card("A DISPLACED THRESHOLD DECREASES THE LDA", "LANDING STARTS AT THE THRESHOLD", [LDA]),
    2278: card("LDA 1,055 M", "RUNWAY − DISPLACEMENT", [("Working", "1,080 − 25 = 1,055 m")]),
    2333: card("A DISPLACED THRESHOLD REDUCES THE LDA", "LANDING STARTS AT THE THRESHOLD", [LDA]),
    2350: card("LDA 1,428 M", "RUNWAY − DISPLACEMENT", [("Working", "1,480 − 52 = 1,428 m")]),
    2314: card("LDA 1,020 M", "A STOPWAY IS NEVER PART OF THE LDA", [("Stopway", "Adds to ASDA only")]),
    2412: card("A STOPWAY DOES NOT AFFECT THE LDA", "IT IS FOR STOPPING AFTER A REJECTED TAKE-OFF", [("Stopway", "Adds to ASDA only")]),
    2297: card("A CLEARWAY MAY INCLUDE A STOPWAY", "CLEARWAY: THE AIRBORNE CLIMB; STOPWAY: A REJECTED TAKE-OFF",
               [("TODA", "TORA + clearway"), ("ASDA", "TORA + stopway")]),
    2298: card("TORA: THE RUNWAY DECLARED FOR THE GROUND RUN", "NO STOPWAY OR CLEARWAY",
               [("ASDA", "TORA + stopway"), ("TODA", "TORA + clearway")]),
    2391: card("STOPWAY: PREPARED AREA FOR STOPPING AFTER A REJECTED TAKE-OFF", "BEYOND THE TAKE-OFF RUN",
               [("ASDA", "TORA + stopway"), ("LDA", "Never includes the stopway")]),
    2255: card("RUNWAY 18 SLOPES 1.45% DOWN", "5,180 FT AT ITS START, 5,125 FT AT ITS END",
               [("Working", "55 ÷ 3,800 × 100 = 1.45%"), SLOPE]),
    2277: card("RUNWAY 24 SLOPES 1.42% DOWN", "1,520 FT AT ITS START, 1,450 FT AT ITS END",
               [("Length", "1,500 m × 3.2808 = 4,921 ft"), ("Working", "70 ÷ 4,921 × 100 = 1.42%")]),
    2319: card("RUNWAY 16 SLOPES 1.13% DOWN", "2,400 FT AT ITS START, 2,350 FT AT ITS END",
               [("Length", "1,350 m × 3.2808 = 4,429 ft"), ("Working", "50 ÷ 4,429 × 100 = 1.13%")]),
    2409: card("RUNWAY 27 SLOPES 1.16% UP", "2,200 FT AT ITS START, 2,250 FT AT ITS END",
               [("Working", "50 ÷ 4,300 × 100 = 1.16%"), SLOPE]),
    2413: card("RUNWAY 13 SLOPES 2.2% DOWN", "800 FT AT ITS START, 725 FT AT ITS END",
               [("Working", "75 ÷ 3,400 × 100 = 2.2%"), SLOPE]),
})

# aquaplaning, wind shear, wake turbulence, V-speeds
CARDS.update({
    2276: card("THE LANDING DISTANCE INCREASES", "LESS TYRE CONTACT, POOR BRAKING", [("Plan for", "A longer landing roll")]),
    2285: card("UNDER-INFLATED TYRES MAKE AQUAPLANING MORE LIKELY", "ALSO HIGH SPEED AND STANDING WATER",
               [("Rule of thumb", "Aquaplaning speed (kt) ≈ 9 × √tyre pressure (psi)")]),
    2300: card("AQUAPLANING IS MORE LIKELY AT HIGH GROUNDSPEED", "THE TYRE CANNOT PUSH THE WATER AWAY IN TIME",
               [("Also", "Standing water, low tyre pressure, worn tread")]),
    2367: card("MAKE A FIRM, POSITIVE TOUCHDOWN", "SO THE TYRES BREAK THROUGH THE WATER",
               [("Avoid", "Floating and bouncing")]),
    2241: card("MORE HEADWIND ON THE CLIMB-OUT: OVERSHOOT", "AIRSPEED AND LIFT RISE, THE AIRCRAFT GOES ABOVE ITS PATH",
               [("Opposite", "Less headwind or more tailwind: undershoot")]),
    2264: card("MORE HEADWIND ON FINAL: OVERSHOOT", "AIRSPEED AND LIFT RISE, THE AIRCRAFT GOES ABOVE THE GLIDE PATH",
               [("Opposite", "Less headwind or more tailwind: undershoot")]),
    2259: card("MORE TAILWIND ON THE CLIMB-OUT: UNDERSHOOT", "AIRSPEED AND LIFT FALL, THE AIRCRAFT SINKS BELOW ITS PATH",
               [("Same effect", "A sudden loss of headwind")]),
    2307: card("MORE TAILWIND ON FINAL: UNDERSHOOT", "AIRSPEED AND LIFT FALL, THE AIRCRAFT SINKS BELOW THE GLIDE PATH",
               [("Same effect", "A sudden loss of headwind")]),
    2328: card("LESS HEADWIND ON THE CLIMB-OUT: UNDERSHOOT", "AIRSPEED AND LIFT FALL, THE AIRCRAFT SINKS BELOW ITS PATH",
               [("Same effect", "A sudden increase in tailwind")]),
    2361: card("LESS HEADWIND ON FINAL: UNDERSHOOT", "AIRSPEED AND LIFT FALL, THE AIRCRAFT SINKS BELOW THE GLIDE PATH",
               [("Same effect", "A sudden increase in tailwind")]),
    2287: card("LIFT OFF BEFORE THE HEAVY AIRCRAFT'S LIFT-OFF POINT", "ITS WAKE STARTS WHERE IT ROTATES",
               [("Then", "Climb above and upwind of its path")]),
    2362: card("STAY ABOVE THE HEAVY AIRCRAFT'S FLIGHT PATH", "ITS VORTICES SINK BEHIND AND BELOW IT",
               [("Landing", "Touch down beyond its touchdown point")]),
    2363: card("TOUCH DOWN BEYOND THE HEAVY AIRCRAFT'S TOUCHDOWN POINT", "ITS WAKE ENDS WHERE IT TOUCHED DOWN",
               [("On the approach", "Stay above its flight path")]),
    2364: card("TOUCH DOWN BEFORE THE HEAVY AIRCRAFT'S LIFT-OFF POINT", "ITS WAKE STARTS WHERE IT LIFTED OFF",
               [("Taking off behind it", "Lift off before that point too")]),
    2254: card("VFE: MAXIMUM SPEED WITH FLAPS EXTENDED", "TOP OF THE WHITE ARC", [("Bottom of the white arc", "VS0, stall with full flap")]),
    2258: card("VNO: MAXIMUM STRUCTURAL CRUISING SPEED", "TOP OF THE GREEN ARC",
               [("Yellow arc", "Smooth air only, with caution"), ("Red line", "VNE, never exceed")]),
    2365: card("VNE: NEVER EXCEED, IN ANY OPERATION", "THE RED LINE ON THE AIRSPEED INDICATOR", [("Below it", "The yellow caution arc")]),
    2342: card("VX: BEST ANGLE OF CLIMB", "MOST HEIGHT FOR THE DISTANCE: CLEARS OBSTACLES", [("VY", "Best rate: most height per minute")]),
    2349: card("VY: BEST RATE OF CLIMB", "MOST HEIGHT PER MINUTE", [("VX", "Best angle: most height for the distance")]),
    2390: card("VX GIVES THE MOST HEIGHT FOR THE DISTANCE", "BEST ANGLE OF CLIMB: USE IT TO CLEAR OBSTACLES",
               [("VY", "Best rate: most height per minute")]),
})
