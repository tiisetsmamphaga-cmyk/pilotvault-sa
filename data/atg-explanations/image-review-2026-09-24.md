# ATG explanation image review, 24 Sept 2026

Every ATG explanation image in use was reviewed, apart from the 64 PHAK-refined images in `phak-question-specific-v2`.
Images were removed if they were crude, cluttered, labelled over their own lines, text-only cards with no diagram, or not valid image files.
Clean drawings and figures extracted from the textbook were kept.

- Kept: 109 images
- Removed: 89 images, unlinked from 156 questions, which now show no image

The removed mappings (URL, title, caption) are backed up in `removed-images-2026-09-24.json`. The image files were deleted and remain in git history.

## Removed

| Image | Questions | Reason |
|---|---|---|
| `q2426-balance-tab` | 2426 | tangled linkage, numbered callouts crowd the drawing |
| `q2462-servo-tab` | 2462 | crude linkage geometry, cluttered callouts |
| `q2463-anti-balance-tab` | 2463 | awkward linkage from above, confusing geometry |
| `q2433-newton-second-law` | 2433 | cartoon planes with arrows drawn over them; generic |
| `q2447-newton-third-law` | 2447 | airflow arrows drawn across the aircraft; messy |
| `q2465-newton-first-law` | 2465 | same composite as the other Newton cards |
| `q2467-power-reduction-nose-drop` | 2467 | arrows and labels piled onto small aircraft |
| `q2434-leading-edge-slats` | 2434 | slat drawn as a hook, not a slat shape |
| `q2681-acceleration-error-southern` | 2681 | text boxes only, no diagram |
| `q2683-variation` | 2683 | text flow boxes only, no diagram |
| `q2704-deviation` | 2704 | text flow boxes only, no diagram |
| `q2728-deceleration-error-northern` | 2728 | mostly text boxes, tiny compass |
| `q2753-compass-turning-error` | 2727, 2753 | text-heavy, small unclear turn sketch |
| `q2569-magneto-rotating-magnet` | 2569, 2570 | one cramped schematic reused, tiny labels, left label clipped |
| `q2575-magneto-distributor` | 2575 | same cramped reused magneto schematic |
| `q2576-magneto-broken-earth-wire` | 2576, 2583 | same cramped reused magneto schematic |
| `q2591-magneto-condenser` | 2591 | same cramped reused magneto schematic |
| `q2595-magneto-impulse-coupling` | 2595 | same cramped reused magneto schematic |
| `q2751-magneto-high-voltage` | 2751 | same cramped reused magneto schematic |
| `q2568-reverse-current-cut-out` | 2568 | cramped reused generator schematic, tiny labels |
| `q2578-generator-commutator` | 2578 | cramped reused generator schematic, tiny labels |
| `q2594-voltage-regulator` | 2572, 2594 | cramped reused generator schematic, tiny labels |
| `q2599-generator-self-excited` | 2599 | cramped reused generator schematic, tiny labels |
| `q2600-alternator-reverse-current` | 2600 | labels collide with the wiring around the diodes |
| `q2571-blown-fuse` | 2571, 2587 | mostly text, crude fuse/breaker icons |
| `q2602-battery-40-ah` | 2581, 2602 | text boxes around a battery icon, no real diagram |
| `q2608-tripped-circuit-breaker` | 2608 | mostly text, crude fuse/breaker icons |
| `q2613-battery-20-ah` | 2613 | text boxes around a battery icon, no real diagram |
| `q2558-starter-solenoid` | 2558 | labels overprint the battery symbol and wiring |
| `q2723-starter-series-winding` | 2723 | labels overprint the battery symbol and wiring |
| `q2738-force-on-conductor` | 2738 | force arrow runs through the field label |
| `q2592-low-tension-booster-coil` | 2592 | cluttered: schematic plus three text cards crammed in |
| `q2494-refuelling-bonding` | 2494 | crude truck/aircraft, labels on the bonding wires |
| `q2517-wet-wing` | 2517, 2767 | wing shown as flat boxes, says nothing visually |
| `q2481-blocked-fuel-tank-vent-v2` | 2481 | X and label overprint the heading sentence |
| `q2505-fuel-tank-venting-v2` | 2505 | caption text overflows its box, soft render |
| `q2622-gyro-rigidity-precession` | 2622, 2662 | tiny crude gyro sketches, precession not shown clearly |
| `q2714-gyro-real-wander` | 2714 | text boxes only, no diagram |
| `q2532-hydraulic-accumulator` | 2532, 2540 | one cramped hydraulic schematic reused, tiny labels |
| `q2551-hydraulic-pressure-warning` | 2551 | same cramped reused hydraulic schematic |
| `q2555-hydraulic-reservoir-vent` | 2541, 2555 | same cramped reused hydraulic schematic |
| `q2565-hydraulic-lp-filter` | 2565 | same cramped reused hydraulic schematic |
| `q2666-mpi` | 2666 | text boxes only, no diagram |
| `q2694-logbook-48-hours` | 2694, 2718 | text boxes only, no diagram |
| `q2697-certificate-of-release-to-service` | 2697 | text boxes only, no diagram |
| `q2712-documents-to-carry` | 2712 | text checklist only, no diagram |
| `q2769-part-43-pilot-maintenance` | 2769 | text boxes only; label overflows its box |
| `q2521-engine-breather` | 2521 | crude cylinder/crankcase sketch |
| `attitude-indicator-v1` | 2684, 2685, 2696, 2699, 2716, 2736 | crude: stray 10 degree marks, meaningless gyro box |
| `earth-magnetic-field-v1` | 2670, 2677, 2690, 2698, 2708, 2713, 2715, 2717, 2721 | abstract ellipses and an arc; does not show the field or dip |
| `float-type-carburettor-v3` | 2477, 2487, 2493, 2506, 2512 | crude; nozzle label runs into the venturi outline |
| `heading-indicator-v2` | 2669, 2676, 2686, 2711, 2720 | bare compass circle plus a meaningless gyro box |
| `magnetic-compass-v1` | 2682, 2701, 2706 | bare circle and an abstract magnet box |
| `normal-combustion-vs-detonation-v2` | 2527, 2536 | abstract circles, does not show a cylinder or flame front |
| `pitot-static-system-v1` | 2626 | crude; static line runs through the VSI circle |
| `turn-coordinator-v1` | 2672, 2678, 2688, 2689, 2703, 2709 | crude aircraft symbol, meaningless gyro box |
| `vertical-speed-indicator-v2` | 2618, 2637, 2639, 2642, 2643, 2644, 2650, 2658 | blank dial, crude case sketch |
| `q2519-pre-ignition` | 2519, 2546, 2562 | crude cylinder: con rod floats, crank drawn as a dashed circle |
| `q2526-blue-exhaust-smoke` | 2526 | engine drawn as a featureless blob with puffs |
| `q2547-black-exhaust-smoke` | 2547 | engine drawn as a featureless blob with puffs |
| `q2749-run-on-glowing-carbon` | 2749 | same crude cylinder sketch |
| `q2524-unapproved-mogas` | 2524 | bullet-list text, no diagram |
| `q2550-higher-octane-fuel` | 2550 | bullet-list text, no diagram |
| `q2561-cht-hottest-cylinder` | 2561 | crude boxes for a flat-four engine |
| `q2491-flooded-engine-start` | 2491 | mostly text sequence, crude lever sketches |
| `q2503-alternate-air` | 2503 | labels overprint arrows; crude layout |
| `q2548-crankshaft-counterweights` | 2548 | counterweights float detached from the crank |
| `q2726-maximum-power-conditions` | 2726 | mostly text; dot panels say little |
| `q2634-true-airspeed` | 2634, 2659 | text flow boxes only, no diagram |
| `q2636-manoeuvre-induced-error` | 2636 | crude fuselage lozenges |
| `q2656-two-static-vents` | 2598, 2656 | crude fuselage outline |
| `q2657-calibrated-airspeed` | 2657 | text flow boxes only, no diagram |
| `q2661-alternate-static-source` | 2588, 2660, 2661 | crude fuselage oval plus text boxes |
| `q2702-isa-sea-level-density` | 2702 | value boxes with a tiny profile sketch |
| `q2707-isa-temperature-lapse-rate` | 2707 | value boxes with a tiny profile sketch |
| `q2758-vr-rotation-speed` | 2758 | tiny crude aircraft on a runway strip |
| `q2419-propeller-blade-angle` | 2419 | angle labels crowd and cross the lines |
| `q2422-propeller-torque-bending` | 2422 | bottom label runs into the propeller blade |
| `q2450-propeller-torque-reaction` | 2450 | bottom label runs into the propeller blade |
| `q2513-propeller-helix-angle` | 2513 | angle labels crowd and cross the lines |
| `q2452-take-off-swing-clockwise-propeller` | 2452 | crude plan view; slipstream spiral scribbled over it |
| `q2508-csu-constant-rpm` | 2508 | mostly text steps; arrow runs through the RPM labels |
| `q2423-propeller-blade-twist-v2` | 2423 | sections float above a fuselage-shaped blade and show no twist |
| `q2486-carburettor-icing-location-v2` | 2486 | crude venturi, ice drawn as a ring |
| `q2563-detonation-low-octane-v2` | 2563 | abstract squares with a starburst; no cylinder |
| `q2567-centre-zero-ammeter-v2` | 2567 | needle covers the AMPERES label; scale labels collide with ticks |
| `q2574-circuit-breaker-protection-v2` | 2574 | last label spills outside the panel |
| `four-stroke-cycle-v1` | 2471, 2473, 2476, 2489, 2496, 2498, 2535, 2539, 2760 | file is not a valid image: broken on the live site since 20 Aug |
| `reciprocating-engine-basic-parts-v1` | 2522, 2544, 2752, 2755, 2756, 2761, 2770 | file is not a valid image: broken on the live site since 20 Aug |

## Kept

- `q2421-semi-monocoque-fuselage`
- `q2424-torsion-load`
- `q2425-split-flap`
- `q2427-adjustable-trim-tab`
- `q2429-truss-longerons`
- `q2443-slotted-flap`
- `q2446-fowler-flap`
- `q2451-plain-flap`
- `q2457-monocoque-structure`
- `q2430-wing-rear-spar`
- `q2440-wing-main-spar`
- `q2461-wing-ribs`
- `q2432-cg-too-far-aft`
- `q2428-braced-monoplane`
- `q2743-trim-tab-purpose`
- `q2759-t-tail`
- `q2762-mass-balance-flutter`
- `q2436-stall-warning-vane`
- `q2439-centre-of-pressure-movement`
- `q2763-adverse-aileron-yaw`
- `q2764-frise-aileron`
- `q2464-tailplane-up-or-down-force`
- `q2674-deviation-card`
- `q2596-low-tension-transformer`
- `q2585-alternator-stator`
- `q2589-alternator-vs-generator-low-rpm`
- `q2610-alternator-rectifier`
- `q2614-alternator-purpose`
- `q2577-left-zero-ammeter`
- `q2579-centre-zero-ammeter`
- `q2582-ammeter-voltmeter`
- `q2609-battery-electrolyte`
- `q2611-voltmeter`
- `q2612-battery-24v-cells`
- `q2590-capacitor`
- `q2604-resistor`
- `q2607-inverter`
- `q2725-constant-speed-drive`
- `q2488-fuel-outlet-above-sump`
- `q2504-avgas-100ll-blue`
- `q2510-full-tanks-condensation`
- `q2507-warm-fuel-absorbs-water`
- `q2468-float-type-carburettor-v2`
- `q2469-fuel-tank-baffles-v2`
- `q2502-fuel-pressure-gauge-v2`
- `q2505-fuel-tank-venting`
- `q2663-gyro-rigidity-factors`
- `q2673-load-factor-level-turn`
- `q2559-pascals-law-hydraulic-brakes`
- `q2523-hydraulic-fluid-phosphate-purple`
- `q2537-hydraulic-fluid-vegetable-blue`
- `q2538-hydraulic-fluid-mineral-red`
- `q2545-hydraulic-fluids-never-mix`
- `q2692-afm-supplements`
- `q2530-dry-sump-scavenge-pump`
- `q2533-oil-cooler-ram-air`
- `q2542-gear-type-oil-pump`
- `q2549-crankshaft-bearing-lubrication`
- `q2552-oil-pressure-relief-valve`
- `q2529-oil-pressure-gauge-position`
- `q2531-oil-cooler-position`
- `q2534-oil-temperature-position`
- `q2543-wet-sump-system`
- `q2773-no-oil-pressure-after-start`
- `q2518-high-temp-low-pressure`
- `q2528-spark-plug-normal`
- `q2557-spark-plug-rich-mixture`
- `carburettor-icing-v1`
- `q2474-valve-lead`
- `q2525-cylinder-cooling-fins`
- `q2553-cowl-flaps`
- `q2560-valve-overlap`
- `q2564-engine-baffles`
- `q2470-mixture-rich`
- `q2472-mixture-lean`
- `q2511-accelerator-pump`
- `q2744-carburettor-fuel-strainer`
- `q2747-mixture-richens-with-altitude`
- `q2772-spark-plug-oil-fouling`
- `q2554-ignition-timing-fixed`
- `q2556-ignition-timing-btdc`
- `q2482-engine-primer`
- `q2499-smooth-throttle-handling`
- `q2500-carburettor-icing-symptoms`
- `q2729-over-leaning`
- `q2730-otto-cycle`
- `q2741-wastegate-stuck-closed`
- `q2742-power-torque-angular-speed`
- `q2733-dynamic-pressure`
- `q2771-asi-calibration`
- `q2616-ivsi-no-lag`
- `q2435-propeller-helical-twist`
- `q2475-fine-pitch-take-off`
- `q2497-coarse-pitch-cruise`
- `q2514-fixed-pitch-dive-rpm`
- `q2484-power-increase-sequence`
- `q2420-tyre-size-section-width`
- `q2431-under-inflated-tyre-wear`
- `q2442-tyre-size-bead-diameter`
- `q2459-tyre-size-outside-diameter`
- `q2460-over-inflated-tyre-wear`
- `q2437-tyre-creep`
- `q2445-oleo-under-extension`
- `q2448-oleo-leg-operation`
- `q2453-oleo-over-extension`
- `q2757-tubeless-tyre`
- `q2418-shimmy-damper`
- `q2441-torque-links`
- `q2444-shimmy-worn-torque-links`
