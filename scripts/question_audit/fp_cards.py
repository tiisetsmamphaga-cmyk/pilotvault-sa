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
