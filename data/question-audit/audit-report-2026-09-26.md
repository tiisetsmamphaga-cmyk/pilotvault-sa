# Question bank audit — 26 Sep 2026

All 2,542 questions in 9 subjects were read, checking the answer key, the explanation and the distractors.
Calculations were recomputed: wind triangles, TAS, density altitude, 1-in-60 and fuel. FPLAN table and graph
answers were checked against the SACAA-01 manual. Regulatory answers were checked against the Pilot's Radio
Handbook (24th ed.), the AGK, PPL Meteorology and Oxford Human Performance texts where these covered the point.

- Backup of every question before the changes: `questions-before-audit-2026-09-26.json`
- Fixes, validated against the backup: `scripts/question_audit/fixes.py` and `met_distractors.py`
- 126 questions changed in the first pass and 6 in the second pass (132 in total). After applying: each answer key matches one of its options, and no question has duplicate options.

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

## Flagged items — resolved in a second pass
| ID | Subject | Decision | Basis |
|---|---|---|---|
| 875 | CPL Air Law | Weight-shift microlight credit toward PPL(A) is **10 h** (was 25 h); now agrees with 843 | SA-CATS 61 (Gazette 35398, 2012) |
| 958 | CPL Air Law | A valid Class 1 is deemed to be **Class 2, 3 and 4** (was 3 and 4 only) | Class 1 is the highest standard; agrees with 954. Part 67 text could not be fetched here |
| 927 | Air Law | Keyed **True** (was False) | The listed devices are exempt from the 91.01.9 prohibition; agrees with 929 and 1409 |
| 1058 | Air Law | Skills test within **36 months** of the last theory exam (was 6 months); now agrees with 893 | SACAA examinations guidance |
| 1438 | Air Law | Rewritten to the verifiable rule: **2 500 ft** above the highest point of a national park, special nature reserve or world heritage site (was "500 m over a game reserve") | NEM: Protected Areas Act s47 |
| 532 | Radio Telephony | Key: **remain in uncontrolled airspace, squawk 7600 and land at an uncontrolled airfield** (was "return to departure field") | Pilot's Radio Handbook 10.2.1 |

No wrong keys were found in Navigation (405), Principles of Flight (365) or ATG (356). All navigation calculations agree with the keys.
