"""Hand fixes for the trial set after dashfix.py: (id, field e=explanation c=card, text after the automatic pass, final text)."""
# Hand fixes applied after the automatic pass: (id, field, text after the pass, final text). field e = explanation, c = card JSON.
OVERRIDES = [
 (1100, "e", "(A related but different signal (a red square with only a single yellow diagonal stripe, not a full cross) warns",
             "(A related but different signal, a red square with only a single yellow diagonal stripe rather than a full cross, warns"),
 (2629, "e", "from VS1 - the clean (flaps up) stalling speed at maximum weight, at its lower end,",
             "from VS1 (the clean, flaps-up stalling speed at maximum weight) at its lower end,"),
 (2224, "e", "successful past experience, confidence built", "successful past experience: confidence built"),
 (2119, "e", "adjusts accordingly, exactly how a pilot", "adjusts accordingly. This is exactly how a pilot"),
 (40, "e", "where the stratosphere warms with height, and in both cases the layer", "where the stratosphere warms with height. In both cases the layer"),
 (626, "e", "so an aircraft sitting exactly at that reference level, on the ground, has, by definition, zero height above it.",
            "so an aircraft on the ground at that reference level has, by definition, zero height above it."),
 (1111, "e", "relative to the centre of pressure, the further forward", "relative to the centre of pressure: the further forward"),
 (1138, "e", "considered to act, if you could suspend", "considered to act. If you could suspend"),
 (1140, "e", "has to decrease to compensate, the two trade off", "has to decrease to compensate. The two trade off"),
 (1537, "c", "rough, milky and brittle: lighter and easier to remove", "rough, milky and brittle; lighter and easier to remove"),
 (304, "e", "The three FIRs (Cape Town (FACA), Johannesburg (FAJA) and Johannesburg Oceanic (FAJO)) are",
            "The three FIRs, Cape Town (FACA), Johannesburg (FAJA) and Johannesburg Oceanic (FAJO), are"),
 (610, "e", "South Africa's three FIRs (Cape Town (FACA), Johannesburg (FAJA) and Johannesburg Oceanic (FAJO)) extend",
            "South Africa's three FIRs, Cape Town (FACA), Johannesburg (FAJA) and Johannesburg Oceanic (FAJO), extend"),
 (308, "e", "etc. , still one TMA", "etc., still one TMA"),
 (506, "e", "against the landing/take-off direction. Used, for example, when", "against the landing/take-off direction, used, for example, when"),
 (576, "e", "reverses this. Take-off and land on runways only", "reverses this: take off and land on runways only"),
]
