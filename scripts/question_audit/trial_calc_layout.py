"""Trial calculation explanations: one sum per line, a blank line between steps (2026-10-08).

The explanation display sets short sum lines as school-style maths (math-text.tsx: "a ÷ b" as a stacked fraction).
Three Flight Planning trial explanations buried their sums inside long sentences, or used "/" and "x", so the sums
could not be laid out. Same facts and numbers; only the layout changes.
"""
EXPLANATIONS = {
    2312: """GIVEN
Departure airfield elevation 1380 ft, QNH 1009 hPa, temperature standard
Cruise pressure altitude 7500 ft, temperature ISA +12°C
Find the distance covered during the climb

METHOD (SACAA-01 Figure 1-8, Time, Distance and Fuel to Climb)
Step 1: Departure pressure altitude and temperature
PA = 1380 + (1013 − 1009) × 30 = 1500 ft
ISA temperature = 15 − (2 × 1.5) = 12°C

Step 2: Cruise temperature at 7500 ft
ISA temperature = 15 − (2 × 7.5) = 0°C
Cruise OAT = 0 + 12 = 12°C

Step 3: Read the chart twice
Enter at +12°C and 1500 ft, go up to the DISTANCE (NM) line and read the distance at departure.
Enter again at +12°C and 7500 ft and read the distance at cruise.

Step 4: Subtract
Climb distance = cruise reading − departure reading

ANSWER
20 NM""",
    2320: """GIVEN
Pressure altitude 3500 ft, weight 2400 lb, temperature +20°C, 4 kt tailwind
Find the take-off ground roll

METHOD (SACAA-01 Figure 1-22)
Step 1: Enter the Take-off Performance Table at +20°C.
Step 2: Ground roll reads 1190 ft at PA 3000 ft and 1310 ft at PA 4000 ft. PA 3500 ft is exactly midway.
Step 3: Tailwind footnote: add 10% for each 2 kt of tailwind, so 4 kt adds 20%.

SOLVE
Ground roll at 3500 ft (midway)
(1190 + 1310) ÷ 2 = 1250 ft

With the 4 kt tailwind (+20%)
1250 × 1.20 = 1500 ft

ANSWER
1500 ft""",
    2389: """GIVEN
Weight 2400 lb, elevation 2650 ft, QNH 1018 hPa, OAT +24°C

SOLVE
Pressure altitude = 2650 + (1013 − 1018) × 30 = 2500 ft

Figure 1-24, halfway between 2000 ft and 3000 ft:
1367.5 ft at +20°C and 1402.5 ft at +30°C

+24°C is 0.4 of the way from +20°C to +30°C:
1367.5 + 0.4 × 35 = 1381.5 ft ≈ 1382 ft

ANSWER
1382 ft

Exam tip: Convert elevation to pressure altitude before entering a performance table.""",
}
