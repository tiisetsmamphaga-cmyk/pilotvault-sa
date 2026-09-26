# Question bank audit — 26 Sep 2026

All 2,542 questions in 9 subjects were read, checking the answer key, the explanation and the distractors.
Calculations were recomputed: wind triangles, TAS, density altitude, 1-in-60 and fuel. FPLAN table and graph
answers were checked against the SACAA-01 manual. Regulatory answers were checked against the Pilot's Radio
Handbook (24th ed.), the AGK, PPL Meteorology and Oxford Human Performance texts where these covered the point.

- Backup of every question before the changes: `questions-before-audit-2026-09-26.json`
- Fixes, validated against the backup: `scripts/question_audit/fixes.py` and `met_distractors.py`
- 126 questions changed. After applying: each answer key matches one of its options, and no question has duplicate options.

## Fixes applied

### Answer key changed
| ID | Subject | Change |
|---|---|---|
| 525 | Radio Telephony | STUDENT prefix is used on an instruction flight with an instructor (solo is SOLO STUDENT) |
| 465, 473 | Radio Telephony | Report ETA change of **more than 2 minutes** (was 3); matches Air Law 1064 and the Radio Handbook |
| 992 | Air Law | Night passengers: IR **or** 1 night take-off/landing as PF (was "Either B or C") |
| 1040 | Air Law | Class 2 validity: stem now says aged 40–49, key 24 months |
| 2196 | Human Performance | 3 km at 180 kt closing = **32 s** (was 34 s); stem now says closing speed |
| 2389 | Flight Planning | Fig 1-24 interpolation gives **1382 ft** (was 1372 ft) |
| 1133 | Principles of Flight | CG too far forward = very stable, heavy elevator (was "easy to control in pitch") |

### A second option was also correct (distractor replaced)
- Radio Telephony: 490 ("Area" is also valid), 547 (mountains/antennae do affect VHF range)
- Human Performance: 2066
- Navigation: 1670, 1685 (the crosswind value was also true)
- Meteorology: 629, 632, 635, 640, 646 and others
- Meteorology total: 71 questions had copied or junk distractors replaced, e.g. "Stratosphere" offered as a percentage, or two identical options in 1486.

### Wording, key text or explanation corrected
- **Air Law:** 772, 929/1050 ("All of these" moved to D), 1003, 1021/1042 (full meaning of the First Series signal), 1457
- **CPL Air Law:** 819 (duplicate option)
- **Radio Telephony:** 309, 322, 325, 347, 404, 423, 493, 494, 496 (ICAO WUN/TOO), 588, 613 (QNH gives altitude, not height)
- **Flight Planning:** 2282 (graph has no kg scale), 2286, 2406
- **Meteorology:** 736 (asks for ISA deviation)
- **Navigation:** 1820 (added the variation/deviation steps)
- **Principles of Flight:**
  - 1154: the explanation contradicted its own key
  - 1120, 1149: further effect of aileron
  - 1115, 1307: forward CG
  - 1214, 1216, 1251: over/underbanking
  - 1246: power and pitch
  - 1259: Va is about 1.9 Vs, not 1.7
  - 1277: the explanation described a trim tab instead of the anti-balance tab
  - 1954: stem wording
- **ATG:** 2518, 2566, 2634, 2683, 2709, 2716 (typos and stem wording)

## Flagged for the owner — could not be verified from the sources on hand
| ID | Subject | Question |
|---|---|---|
| 843 vs 875 | CPL Air Law | Weight-shift microlight credit given as 10 h in one and 25 h in the other |
| 958 | CPL Air Law | Says a Class 1 medical deems Class 3/4 only; confirm against Part 67 |
| 927 | Air Law | Keyed False; probably True |
| 1058 vs 893 | Air Law | 6 months in one and 36 months in the other for the same requirement |
| 1438 | Air Law | Minimum height over a game reserve keyed as 500 m; confirm against the current AIP/CAR |
| 532 | Radio Telephony | Radio failure in the GFA keyed "return to departure field"; the Handbook says land at an uncontrolled aerodrome |

No wrong keys were found in Navigation (405), Principles of Flight (365) or ATG (356). All navigation calculations agree with the keys.
