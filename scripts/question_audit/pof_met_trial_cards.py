"""Principles of Flight and Meteorology trial sets: the last thin KEY FACT cards, 2026-10-09.

These five cards had two long points (one for 721); each gets two or three more, to the standard of
atg_trial_cards.py. Kickers, headlines and the existing points stay; explanations are unchanged.
"""
import json


def card(kicker, headline, subline, blocks, formula=None):
    d = {"kicker": kicker, "headline": headline, "subline": subline,
         "blocks": [{"label": a, "value": b} for a, b in blocks]}
    if formula:
        d["formula"] = formula
    return json.dumps(d, ensure_ascii=False)


SUBJECT = {-3: "principles-of-flight", 1138: "principles-of-flight", 1345: "principles-of-flight",
           2025: "principles-of-flight", 721: "meteorology"}

CARDS = {
    -3: card("KEY RELATIONSHIP", "AT 60° BANK, LOAD FACTOR = 2.0 G",
             "LOAD FACTOR = 1 / cos(BANK ANGLE) - IT DEPENDS ONLY ON BANK ANGLE IN A LEVEL TURN",
             [("60° level turn", "Load factor = 1 / cos 60° = 2.0 G - the wings support twice the aircraft's gross weight"),
              ("What drives it", "In a level, coordinated turn, the extra load on the wings is a function of bank angle alone, not airspeed or aircraft type"),
              ("Other banks", "30° ≈ 1.15 G · 45° ≈ 1.41 G · 75° ≈ 3.9 G"),
              ("Stall speed", "Rises with √n: at 60°, × 1.41 (+41%)"),
              ("Limit", "Normal category aeroplanes: +3.8 G")],
             "LOAD FACTOR = 1 / cos(BANK ANGLE)"),
    1138: card("KEY DEFINITION", "POINT WHERE TOTAL WEIGHT ACTS",
               "THE AIRCRAFT BALANCES EXACTLY AS IF SUSPENDED FROM THIS POINT",
               [("Center of gravity (CG)", "The single point through which the aircraft's total weight acts"),
                ("Why it matters", "CG position relative to the wing's lift determines longitudinal stability"),
                ("Forward CG", "More stable, heavier elevator, higher stall speed"),
                ("Aft CG", "Less stable, light elevator, spin recovery harder"),
                ("Exam trap", "Lift acts through the centre of pressure; the datum is only the measuring point")]),
    1345: card("KEY RELATIONSHIP", "MOIST AIR IS LESS DENSE THAN DRY AIR",
               "WATER VAPOUR IS LIGHTER THAN THE AIR IT DISPLACES, SO LIFT AND PERFORMANCE FALL",
               [("Humid air", "Less dense than dry air at the same temperature and pressure"),
                ("Effect on performance", "Less lift for a given airspeed, longer take-off run, reduced rate of climb"),
                ("Why lighter", "Water vapour (18) weighs less than nitrogen (28) and oxygen (32)"),
                ("Worst case", "Hot, high and humid: the highest density altitude"),
                ("Exam trap", "Humid air feels heavy, but it is less dense")]),
    2025: card("KEY RELATIONSHIP", "TURN NEEDLE SHOWS ROTATION DIRECTION",
               "IT DEFLECTS TOWARD THE DIRECTION OF ROTATION AND STAYS RELIABLE THROUGHOUT THE SPIN",
               [("Turn needle", "Deflects fully toward the spin direction (L or R) throughout autorotation"),
                ("Why it's reliable", "Rate-based — unaffected by the extreme attitude that can tumble the attitude indicator"),
                ("Slip ball", "Unreliable in a spin: don't use it for the direction"),
                ("Recovery", "Power idle, ailerons neutral, full rudder against the needle, then stick forward"),
                ("Exam trap", "The attitude indicator and DI may topple")]),
    721: card("KEY FACT", "STATION 4: THICK ALTOSTRATUS OR NIMBOSTRATUS",
              "READ THE MIDDLE-CLOUD SYMBOL ON THE STATION MODEL",
              [("These clouds", "Extensive layers with possible continuous rain"),
               ("Altostratus", "Grey sheet: the sun shows as if through ground glass"),
               ("Nimbostratus", "Dark and thick: continuous rain or snow, low visibility"),
               ("Found with", "Warm fronts: widespread, gentle ascent"),
               ("Exam trap", "Altocumulus castellanus has its own symbol: turrets, instability")]),
}

assert set(CARDS) == set(SUBJECT)
