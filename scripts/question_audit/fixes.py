"""Question-bank audit fixes (2026-09-26).

Each entry in FIXES maps a question id to the fields that change. Field names use the short
form of data/question-audit/questions-before-audit-2026-09-26.json:
q = question, a-d = option_a-option_d, ans = correct_answer (option text), e = explanation.
A callable value receives the old value and returns the new one.

Run `python3 scripts/question_audit/fixes.py` to validate every fix against the backup and write
the SQL to stdout.
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from met_distractors import M as MET_DISTRACTORS, Q736  # noqa: E402

FIXES = {
    # ---------------- CPL Air Law ----------------
    819: {"a": "The ATO that conducted the training"},

    # ---------------- Air Law ----------------
    772: {"q": "The release of an external sling load is a serious incident under what condition?"},
    929: {"c": "Portable voice recorder", "d": "All of these", "ans": "All of these"},
    992: {
        "b": "1 take-off and landing by day",
        "d": "5 night take-offs and landings with an instructor",
        "ans": "An instrument rating or 1 night take-off and landing as PF",
    },
    1003: {"e": (
        "Flight time is the total time from the moment the aircraft first moves under its own power for "
        "the purpose of taking off until it comes to rest at the end of the flight. It therefore includes "
        "taxiing out and in, so 'from taxi start until parking brake set' is the closest description. It "
        "is not only the airborne time (lift-off to the end of the landing roll), and it is not measured "
        "from engine start to shutdown, because time spent running the engine while stationary does not count."
    )},
    1021: {
        "b": "Land at this aerodrome",
        "d": "Follow me away from a prohibited area and to a landing terrain",
        "ans": "Follow me away from a prohibited area and to a landing terrain",
        "e": lambda e: e.replace("ANSWER\nFollow me to a landing terrain",
                                 "ANSWER\nFollow me away from a prohibited area and to a landing terrain"),
    },
    1040: {
        "q": "The period of validity of a Class 2 medical certificate for a private pilot aged 40 to 49 is what?",
        "ans": "24 months",
        "e": (
            "A Class 2 medical certificate for a private pilot is valid for 60 months if the holder is "
            "under 40, 24 months from age 40 to 49, and 12 months from age 50 (CAR Part 67). A pilot aged "
            "40 to 49 therefore holds a 24-month certificate, although the medical examiner may set a "
            "shorter period where closer monitoring of the pilot's fitness is needed."
        ),
    },
    1042: {
        "a": "Follow me away from a prohibited area and to a landing terrain",
        "ans": "Follow me away from a prohibited area and to a landing terrain",
    },
    1050: {
        "a": "A flight crossing an international boundary even if no landing will be made",
        "b": "A flight between two ATZs even if no controlled or advisory airspace is entered en route",
        "c": "A flight from a manned aerodrome to an ATZ in the stated circumstances",
        "d": "All of these",
        "ans": "All of these",
        "e": lambda e: e.replace("Correct answer: All of the above.", "Correct answer: All of these."),
    },
    1457: {"c": "An abrupt breakaway climbing turn of 90° or more",
           "ans": "An abrupt breakaway climbing turn of 90° or more"},

    # ---------------- Radio Telephony ----------------
    309: {"q": lambda q: q.replace("ATIS routes", "ATS routes").replace("which extend", "which extends")},
    322: {"q": "Which of these describes Class A airspace?"},
    325: {"q": (
        "Which airspace has the following separation rules: IFR flights are separated from all other "
        "flights, and VFR flights are separated from IFR flights and receive traffic information on "
        "other VFR flights?"
    )},
    347: {"a": "Yes - no permission is needed", "ans": "Yes - no permission is needed"},
    404: {"d": "Radar"},
    423: {
        "a": "Height above ground or water of the base of the lowest layer of cloud below 20 000 ft, covering more than 4 oktas.",
        "b": "Height above ground or water of the base of the lowest layer of cloud above 20 000 ft, covering more than 4 oktas.",
        "c": "Height above ground or water of the base of the lowest layer of cloud below 2 000 ft, covering less than 4 oktas.",
        "ans": "Height above ground or water of the base of the lowest layer of cloud below 20 000 ft, covering more than 4 oktas.",
    },
    465: {
        "d": "ETA changes by more than 2 minutes",
        "ans": "ETA changes by more than 2 minutes",
        "e": (
            "Correct answer: ETA changes by more than 2 minutes. If the estimated time at the next reporting "
            "point, FIR boundary or destination changes by more than 2 minutes, ATC must be told (CAR "
            "91.03.4 and ICAO; the Pilot's Radio Handbook confirms 2 minutes is the correct figure, although "
            "some older AIP text still quotes 3 minutes). A change in TAS must be reported when it varies "
            "by 5% or more, and being off track is corrected, not filed as an amendment."
        ),
    },
    473: {
        "c": "The time changes by more than 2 minutes",
        "ans": "The time changes by more than 2 minutes",
        "e": (
            "Correct answer: The time changes by more than 2 minutes. If the estimated time at the next "
            "reporting point, FIR boundary or destination changes by more than 2 minutes, ATC must be "
            "advised (CAR 91.03.4 and ICAO; the Pilot's Radio Handbook confirms 2 minutes is the correct "
            "figure, although some older AIP text still quotes 3 minutes). A 1-minute change is within "
            "tolerance, and TAS changes are reported when they reach 5% or more."
        ),
    },
    490: {
        "a": "Information",
        "e": (
            "The Area Control Centre's call sign is CONTROL (AREA is also used, e.g. \"Johannesburg Area\"), "
            "so Control is the answer here. It provides area control service to aircraft in a CTA, airway "
            "or other controlled part of the FIR. INFORMATION is the call sign of a flight information "
            "service, which gives information but no control."
        ),
    },
    493: {
        "a": "If the controller has used the full call sign and there is no ambiguity with another call sign.",
        "b": "If the controller has first used the abbreviated call sign, even if there is ambiguity with another call sign.",
        "c": "If the controller has first used the abbreviated call sign and there is no ambiguity with another call sign.",
        "ans": "If the controller has first used the abbreviated call sign and there is no ambiguity with another call sign.",
    },
    494: {
        "a": "WUN TOO SEVEN POINT SEVEN FIFE",
        "b": "WUN TOO SEVEN SEVEN FIFE",
        "c": "WUN TOO SEVEN DAYSEEMAL SEVEN FIFE",
        "ans": "WUN TOO SEVEN DAYSEEMAL SEVEN FIFE",
        "e": (
            "Frequencies are spoken digit by digit, with as many decimals as are specified, using ICAO "
            "pronunciation (WUN, TOO, TREE, FOW-er, FIFE, SIX, SEV-en, AIT, NIN-er), and the decimal point "
            "is spoken DAYSEEMAL, not \"point\". So 127.75 is WUN TOO SEVEN DAYSEEMAL SEVEN FIFE. This "
            "pronunciation exists to stop frequencies being misheard over a noisy or weak signal."
        ),
    },
    496: {
        "a": "WUN TOO FIVE DAYSEEMAL AIT",
        "b": "WUN TOO FIFE DAYSEEMAL AIT",
        "c": "WUN TOO FIFE POINT AIT",
        "ans": "WUN TOO FIFE DAYSEEMAL AIT",
        "e": (
            "Radio frequencies are spoken digit by digit using standard ICAO pronunciation (WUN, TOO, FIFE, "
            "AIT...), and the decimal is spoken DAYSEEMAL. Therefore 125.8 is transmitted as WUN TOO FIFE "
            "DAYSEEMAL AIT; FIVE and POINT are not ICAO radio pronunciation."
        ),
    },
    525: {
        "ans": "To alert ATC and other aircraft that the aircraft making the call is on an instruction flight.",
        "e": (
            "In South Africa (AIP ENR 1.8 and the Pilot's Radio Handbook) the prefix STUDENT is used on an "
            "ab-initio training flight with an instructor on board, telling ATC and other traffic that this "
            "is an instruction flight. A student flying solo uses the prefix SOLO STUDENT instead, so "
            "controllers can allow for limited experience."
        ),
    },
    547: {"a": "Time of day", "c": "Outside air temperature"},
    588: {"q": "How should an intercepted aircraft acknowledge an intercepting aircraft that rocks its wings and then makes a slow level turn?"},
    613: {
        "a": "Altitude above mean sea level",
        "ans": "Altitude above mean sea level",
        "e": (
            "Correct answer: Altitude above mean sea level. QNH is the actual pressure at a place corrected "
            "to sea level, so with QNH set the altimeter reads altitude - height above mean sea level - and "
            "shows the airfield elevation on the ground. Height above the airfield is given by QFE, and "
            "pressure altitude by the standard setting of 1013 hPa."
        ),
    },

    # ---------------- Human Performance ----------------
    2066: {"d": "Too much carbon dioxide in the blood"},
    2196: {
        "q": ("Two aircraft are closing head-on at a closing speed of 180 kt with a visibility of 3 km. "
              "Approximately how much time is available from first sighting to impact?"),
        "a": "32 seconds",
        "ans": "32 seconds",
        "e": (
            "GIVEN\nClosing speed 180 kt, sighting distance 3 km.\n\n"
            "SOLVE\n3 km ÷ 1.852 = 1.62 NM\nTime = 1.62 ÷ 180 = 0.009 h\n0.009 × 3600 = 32.4 s ≈ 32 seconds\n\n"
            "ANSWER\n32 seconds\n\n"
            "That is very little time to see the other aircraft, recognise the threat and take avoiding "
            "action, which is why a continuous, systematic lookout matters."
        ),
    },

    # ---------------- Flight Planning ----------------
    2282: {"e": (
        "GIVEN\nLoading graph line for pilot and front passenger (arm 77.8 in); moment/1000 = 24.\n\n"
        "FORMULA\nWeight = Moment ÷ Arm; 1 kg = 2.2046 lb\n\n"
        "SOLVE\nMoment = 24 × 1000 = 24 000 lb-in\n"
        "Weight = 24 000 ÷ 77.8 = 308.5 lb (the graph reads about 310 lb)\n"
        "Weight in kg = 308.5 ÷ 2.2046 ≈ 140 kg (310 lb ≈ 140.6 kg)\n\n"
        "The loading graph is in pounds only, so convert the result to kilograms; the closest option is 140.6 kg.\n\n"
        "ANSWER\n140.6 kg"
    )},
    2286: {"e": lambda e: e.replace("Groundspeed = 22.84 × 4.0 = 91.4 kt, rounded to 92 kt",
                                    "Groundspeed = 22.84 × 4.0 = 91.4 kt; the closest option is 92 kt")},
    2389: {
        "c": "1382 ft",
        "ans": "1382 ft",
        "e": (
            "GIVEN\nWeight 2400 lb, elevation 2650 ft, QNH 1018 hPa, OAT +24°C.\n\n"
            "SOLVE\nPressure altitude = 2650 + (1013 − 1018) × 30 = 2500 ft\n"
            "Figure 1-24, halfway between 2000 ft and 3000 ft: 1367.5 ft at +20°C and 1402.5 ft at +30°C\n"
            "+24°C is 0.4 of the way from +20°C to +30°C: 1367.5 + 0.4 × 35 = 1381.5 ft ≈ 1382 ft\n\n"
            "ANSWER\n1382 ft\n\n"
            "Exam tip: Convert elevation to pressure altitude before entering a performance table."
        ),
    },
    2406: {"q": "The zero fuel weight of an aircraft is the empty weight of the aircraft:"},

    # ---------------- Navigation ----------------
    1670: {"b": "6kt crosswind"},
    1685: {"b": "9kt crosswind"},
    1820: {"e": lambda e: e.replace(
        "Read GS ≈ 131 kt under the centre dot.\n",
        "Read GS ≈ 131 kt under the centre dot. True heading ≈ 235° − 9° = 226°T.\n"
        "Step 6: Magnetic heading = 226° + 23°W = 249°M.\n"
        "Step 7: Deviation east, compass least: 249° − 4°E = 245°C.\n",
    )},

    # ---------------- Principles of Flight ----------------
    1120: {"e": (
        "Ailerons primarily roll the aircraft about the longitudinal axis. Once banked, the aircraft "
        "sideslips towards the lower wing and the fin weathercocks the nose that way, so the further effect "
        "is yaw in the direction of the bank. The yaw speeds up the outer wing, which increases the bank, "
        "and if nothing is corrected the nose drops into a steepening spiral dive. (Adverse aileron yaw - a "
        "brief yaw opposite to the roll caused by the down-going aileron's extra drag - is a separate effect.)"
    )},
    1149: {"e": (
        "Applying aileron alone first rolls the aircraft. The bank then causes a sideslip towards the lower "
        "wing, and the fin yaws the nose towards the lower wing - the further effect. That yaw speeds up the "
        "outer wing, increasing the bank still further, and if left uncorrected the aircraft enters a "
        "steepening spiral dive."
    )},
    1154: {"e": (
        "Roll is the primary effect of aileron. Once the aircraft is banked, the lift is tilted and it "
        "starts to sideslip towards the lower wing; the fin, like a weathervane, then yaws the nose towards "
        "the lower wing, so the secondary (further) effect is yaw in the same direction as the roll. Left "
        "uncorrected, this leads to a spiral dive. (Adverse aileron yaw, a brief yaw opposite to the roll "
        "caused by aileron drag as the roll starts, is a separate effect.)"
    )},
    1133: {
        "d": "Very stable in pitch, with heavy elevator forces",
        "ans": "Very stable in pitch, with heavy elevator forces",
        "e": (
            "With the CG too far forward the tailplane has a long arm about the CG and the aircraft is very "
            "stable in pitch: it resists changes of attitude and the elevator forces become heavy. The tail "
            "must also produce a large download just to trim, which uses up nose-up elevator travel, so "
            "rotating on take-off and flaring for landing can become difficult - the reason for the forward "
            "CG limit. Reduced stability and a tendency to flat spin are effects of an aft CG."
        ),
    },
    1115: {"e": (
        "Of the choices, a forward CG (within limits) is best. With the CG forward the aircraft is stable in "
        "pitch and the tailplane has a long arm about the CG, so elevator inputs give firm, predictable "
        "changes of attitude. As the CG moves aft the aircraft becomes less stable and the elevator "
        "increasingly light and sensitive, until beyond the aft limit it may not be controllable. The forward "
        "limit still matters: too far forward, the elevator may not have enough nose-up authority for "
        "rotation and the flare."
    )},
    1307: {"e": (
        "Of the choices, a forward CG (within limits) is best. With the CG forward the aircraft is stable in "
        "pitch and the tailplane has a long arm about the CG, so elevator inputs give firm, predictable "
        "changes of attitude. Loading baggage aft or placing the CG behind the aft limit or the centre of "
        "pressure makes the aircraft less stable and the elevator over-sensitive. The forward limit still "
        "matters: too far forward, the elevator may not have enough nose-up authority for rotation and the flare."
    )},
    1214: {"e": (
        "In a descending (gliding) turn the inner wing, travelling on a steeper downward helix, meets the "
        "air at a slightly larger angle of attack than the outer wing. The extra lift on the inner wing tends "
        "to roll the aircraft out of the turn (underbanking), so some aileron into the turn may be needed to "
        "hold the bank angle."
    )},
    1216: {"e": (
        "In a climbing turn the outer wing travels faster and, on its shallower upward helix, meets the air "
        "at a slightly larger angle of attack than the inner wing. It therefore produces more lift and the "
        "aircraft tends to roll further into the turn (overbanking), so some opposite aileron may be needed "
        "to hold the bank angle."
    )},
    1251: {"e": (
        "In a climbing turn the outer wing travels faster and, on its shallower upward helix, meets the air "
        "at a slightly larger angle of attack than the inner wing. The extra lift on the outer wing tends to "
        "roll the aircraft further into the turn, so opposite aileron may be needed to stop it overbanking. "
        "In a gliding turn the effect reverses and the aircraft tends to underbank."
    )},
    1246: {"e": (
        "Increasing power strengthens the nose-up thrust-drag couple (the thrust line is normally below the "
        "drag line) and increases the slipstream over the tailplane, which increases its download. Both raise "
        "the nose, so in level flight an increase in thrust normally pitches the nose up and forward pressure "
        "or trim is needed to hold the attitude. Reducing power does the opposite."
    )},
    1259: {"e": (
        "Design manoeuvring speed (Va) is the highest speed at which a single full, abrupt control deflection "
        "will stall the wing before the structure reaches its limit load. It is roughly Vs × √(limit load "
        "factor) - about 1.9 × Vs for a normal-category aircraft limited to 3.8 g - and it is lower at "
        "lighter weights. Slowing to Va or below is also the usual advice in severe turbulence."
    )},
    1277: {"e": (
        "An anti-balance (anti-servo) tab moves in the same direction as the stabilator. Its air load opposes "
        "the stabilator's movement, adding feel so that a light, powerful all-moving tailplane is not "
        "over-controlled. On the pre-flight check, move the stabilator and confirm the tab moves the same "
        "way; a tab moving the opposite way would be acting as a balance tab and would lighten the controls."
    )},
    1954: {"q": "The ambient air pressure acting on an object immersed in the atmosphere:"},

    # ---------------- Round 2: the six items flagged for the owner ----------------
    875: {"ans": "10 hours", "e": (
        "Under SA-CATS 61, the holder of a helicopter licence, or an equivalent licence for a weight-shift "
        "controlled microlight, gyroplane or glider, who applies for a PPL(A) may be credited with a maximum "
        "of 10 hours. The larger 25-hour credit applies only to time on conventionally (three-axis) "
        "controlled microlights."
    )},
    958: {"d": "Class 2, Class 3 and Class 4", "ans": "Class 2, Class 3 and Class 4", "e": (
        "A Class 1 certificate is issued to the highest medical standard, so while it is valid the holder is "
        "also deemed to hold Class 2, Class 3 and Class 4 certificates - a CPL or ATPL holder can exercise "
        "PPL privileges on a Class 1. A Class 2 or Class 3 certificate only covers the classes below it."
    )},
    927: {"ans": "True", "e": (
        "True. Part 91 (91.01.9) prohibits portable electronic devices on board unless permitted, but it "
        "specifically exempts portable voice recorders, hearing aids, heart pacemakers, electric shavers and "
        "any other device the operator (or, on a non-commercial flight, the PIC) has determined will not "
        "interfere with the aircraft's systems. These devices are therefore not restricted by the rule, "
        "although the PIC can still stop the use of anything that is causing interference."
    )},
    1058: {"b": "12 months", "c": "18 months", "d": "36 months", "ans": "36 months", "e": (
        "The skills test must be completed within 36 months of passing the last theoretical knowledge "
        "examination (the examinations themselves must all be passed within 18 months of the first). "
        "Separately, the skills test must be taken within 30 days of the last dual instruction flight."
    )},
    1438: {
        "q": ("Under the Protected Areas Act, no aircraft may fly over a national park, special nature reserve "
              "or world heritage site lower than what height above its highest point, unless authorised?"),
        "a": "500 ft", "b": "1 500 ft", "c": "2 000 ft", "d": "2 500 ft", "ans": "2 500 ft",
        "e": (
            "Section 47 of the National Environmental Management: Protected Areas Act makes the airspace above "
            "a special nature reserve, national park or world heritage site, up to 2 500 ft above its highest "
            "point, part of the protected area. Aircraft may not fly below that level except where specifically "
            "allowed, for example in an emergency or when landing at an approved airstrip. Some areas have "
            "their own published limits, so always check the chart and the AIP."
        ),
    },
    532: {
        "c": "Remain in uncontrolled airspace, broadcast blind, squawk 7600, and land at an uncontrolled airfield",
        "ans": "Remain in uncontrolled airspace, broadcast blind, squawk 7600, and land at an uncontrolled airfield",
        "e": (
            "A General Flying Area is uncontrolled airspace. The Pilot's Radio Handbook (AIP ENR 1.5, SA-CATS "
            "91.06.16) says a VFR pilot whose radio fails in uncontrolled airspace must remain in uncontrolled "
            "airspace, squawk 7600, switch on the landing light and continue to an uncontrolled airfield, "
            "joining normally and prefixing calls with \"transmitting blind\". Returning to the departure field "
            "or heading for the nearest airfield could mean entering controlled airspace without a clearance. "
            "If a flight plan was filed or you were in contact with an ATSU, telephone the nearest ATSU after landing."
        ),
    },

    # ---------------- Aircraft Technical & General ----------------
    2518: {"c": "A low oil supply", "ans": "A low oil supply"},
    2566: {"a": "The capsule", "ans": "The capsule"},
    2634: {"q": "True airspeed is:"},
    2683: {"q": "The discrepancy between true bearings and magnetic bearings is caused by:"},
    2709: {"q": "Some aircraft use an electrically driven turn indicator because:"},
    2716: {"q": "When the axis of the gyro rotor of an air-driven artificial horizon is in the vertical:"},
}

# Meteorology: replace copied/duplicate distractors (keys keep their text and letter).
for _id, (_a, _b, _c, _d) in MET_DISTRACTORS.items():
    FIXES.setdefault(_id, {}).update({"a": _a, "b": _b, "c": _c, "d": _d})
FIXES.setdefault(736, {}).update({"q": Q736["question"], **dict(zip("abcd", Q736["options"]))})

COLUMNS = {"q": "question", "a": "option_a", "b": "option_b", "c": "option_c", "d": "option_d",
           "ans": "correct_answer", "e": "explanation"}


def load_backup():
    data = json.loads((ROOT / "data/question-audit/questions-before-audit-2026-09-26.json").read_text())
    return {r["id"]: r for rows in data.values() for r in rows}


def build():
    """Return {id: {short_field: new_value}} with callables resolved; raise on any inconsistency."""
    rows = load_backup()
    out = {}
    for qid, changes in FIXES.items():
        old = rows[qid]
        new = dict(old)
        resolved = {}
        for field, value in changes.items():
            if callable(value):
                value = value(old[field])
                if value == old[field]:
                    raise ValueError(f"{qid}.{field}: replace target not found")
            if value == old[field]:
                continue
            new[field] = resolved[field] = value
        if not resolved:
            raise ValueError(f"{qid}: nothing changes")
        opts = [new[k] for k in "abcd" if new[k]]
        if new["ans"] not in opts:
            raise ValueError(f"{qid}: answer {new['ans']!r} is not one of the options")
        if len(set(opts)) != len(opts):
            raise ValueError(f"{qid}: duplicate options {opts}")
        out[qid] = resolved
    return out


def sql_literal(text):
    tag = "$fx$"
    assert tag not in text
    return f"{tag}{text}{tag}"


def to_sql(resolved):
    stmts = []
    for qid, fields in sorted(resolved.items()):
        sets = ", ".join(f"{COLUMNS[f]} = {sql_literal(v)}" for f, v in fields.items())
        stmts.append(f"update questions set {sets} where id = {qid};")
    return "\n".join(stmts)


if __name__ == "__main__":
    resolved = build()
    print(to_sql(resolved))
    print(f"-- {len(resolved)} questions", file=sys.stderr)
