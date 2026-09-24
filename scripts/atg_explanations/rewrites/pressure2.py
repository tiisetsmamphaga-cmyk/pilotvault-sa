R = {
    2629: {
        "e": "The ASI's colour markings show the key speeds. The green arc is the normal operating range, from VS1 - the clean (flaps up) stalling speed at maximum weight - at its lower end, up to VNO, the maximum structural cruising speed, at its upper end. The white arc is the flap operating range, the yellow arc the caution range (smooth air only), and the red line VNE, the never-exceed speed.",
    },
    2631: {
        "e": "The VSI works by comparing the static pressure in its capsule with the delayed static pressure in its case. If the only static vent is blocked, neither can change any more: the small difference present at the time quickly leaks away through the calibrated leak, and the VSI settles at zero whatever the aircraft does. Together with a frozen altimeter, a VSI stuck at zero during a climb or descent is a strong clue to a static blockage.",
    },
    2634: {
        "a": "Calibrated airspeed corrected for instrument and position error",
        "b": "Calibrated airspeed corrected for compressibility only",
        "d": "Calibrated airspeed corrected for wind speed and direction",
        "e": "Calibrated (rectified) airspeed is IAS corrected for instrument and position error. The ASI is calibrated for ISA sea-level air density, but at altitude or in warm air the air is less dense, so the ASI under-reads the aircraft's true speed through the air. Correcting CAS for density - using pressure altitude and temperature - gives TAS, roughly 2% more than CAS for every 1,000 ft. Wind affects groundspeed, not TAS.",
    },
    2635: {
        "b": "Remain constant",
        "e": "When the static vent blocks, the ASI case keeps the lower static pressure from the higher altitude where the blockage occurred. As the aircraft descends, the real static pressure - and with it the pitot pressure fed to the capsule - increases, but the case pressure does not, so the capsule sees too large a pressure difference and the ASI over-reads. In a climb with a blocked static vent it under-reads, which could lead a pilot towards a stall.",
    },
    2636: {
        "a": "An error caused by the pitot tube being misaligned with the airflow",
        "b": "An error caused by temperature changes in the instrument mechanism",
        "d": "An error caused by the delay in the VSI's calibrated leak",
        "e": "Manoeuvre-induced error is a temporary false reading caused by the changing airflow around the static vent during rapid changes of attitude or altitude. The disturbed airflow makes the pressure at the vent fluctuate, so the pressure instruments - particularly the VSI - briefly show a false climb or descent, which disappears once the manoeuvre is complete. A misaligned pitot tube is a position error, and the VSI's normal delay is time lag.",
    },
    2637: {
        "e": "The VSI capsule is connected directly to the static line, so it always holds the current static pressure, while the case is fed through a calibrated leak (a fine restriction), so its pressure lags behind. In level flight both are equal and the pointer reads zero; in a climb or descent the capsule pressure changes first, and the difference between capsule and case, proportional to the rate of climb or descent, drives the pointer. No pitot pressure or vacuum is used.",
    },
    2638: {
        "q": "If the static vent becomes blocked during level flight at a constant airspeed, the ASI will:",
        "a": "Read zero",
        "b": "Over-read",
        "c": "Under-read",
        "e": "When the static vent blocks in level flight, the pressure trapped in the ASI case equals the actual static pressure at that altitude. As long as the aircraft stays at that level the ASI remains accurate, so at a constant airspeed its reading remains constant. The errors appear only when the altitude changes: it under-reads in a climb and over-reads in a descent.",
    },
    2639: {
        "e": "The IVSI adds an accelerometer: a small piston held by springs in a cylinder connected to the capsule line. When a descent begins, the downward acceleration makes the piston rise in its cylinder, immediately increasing the pressure in the capsule, so the pointer shows a descent at once instead of waiting for the static pressure difference to build up. In a climb the piston falls and decreases the capsule pressure. It does not act on pitot pressure or on the case.",
    },
    2640: {
        "b": "The airspeed indicator only",
        "c": "The altimeter only",
        "d": "The attitude indicator and heading indicator",
        "e": "The altimeter and VSI work entirely on static pressure, and the ASI compares pitot pressure with static pressure, so a static blockage affects all three: the altimeter freezes, the VSI reads zero and the ASI gives wrong readings once the altitude changes (under-reading in a climb, over-reading in a descent). Selecting the alternate static source restores them. The gyro instruments, such as the attitude and heading indicators, are unaffected.",
    },
    2641: {
        "a": "Read zero",
        "b": "Over-read",
        "d": "Fluctuate",
        "e": "At the moment of blockage the static pressure trapped in the ASI case equals the real static pressure, and as long as the aircraft stays at the same level it continues to do so. The ASI therefore still shows the correct indicated airspeed and responds normally to changes in speed. Errors appear only when the altitude changes: it under-reads in a climb and over-reads in a descent.",
    },
    2642: {
        "a": "Remain constant while the capsule pressure increases",
        "c": "Increase at a higher rate than that inside the capsule",
        "e": "In a VSI the capsule receives static pressure directly, while the case is fed through a calibrated leak. In a descent the outside pressure rises, so the capsule pressure increases immediately and the case pressure follows more slowly. With the capsule pressure higher than the case pressure, the capsule expands and the pointer shows a descent, at a rate proportional to the pressure difference.",
    },
    2643: {
        "a": "The capsule pressure increases faster than the case pressure, so the capsule expands and the mechanism indicates a climb",
        "c": "The case pressure decreases faster than the capsule pressure, so the capsule expands and the mechanism indicates a descent",
        "d": "Both pressures remain equal, so the pointer stays at zero throughout the climb",
        "e": "In a climb the static pressure falls. The capsule, connected directly to the static line, loses pressure straight away, while the case, fed through the calibrated leak, loses pressure more slowly. With the capsule pressure now lower than the case pressure the capsule contracts, and the linkage moves the pointer to show a rate of climb; the faster the climb, the larger the difference.",
    },
    2644: {
        "e": "When a climb begins, the upward acceleration makes the IVSI's accelerometer piston fall in its cylinder, which immediately reduces the pressure in the capsule. The capsule contracts and the pointer shows a climb at once, without waiting for the normal static-pressure difference to develop. As the acceleration stops the piston slowly returns, by which time the normal VSI pressure difference has taken over. It acts on the capsule, not the case, and pitot pressure is not used.",
    },
    2645: {
        "a": "Under-read for a brief period",
        "c": "Read correctly at once",
        "d": "Freeze at the altitude from which the descent began",
        "e": "An altimeter's mechanism has some friction and lag, so during a rapid descent it cannot quite keep up and shows an altitude slightly higher than the aircraft's actual altitude. When the aircraft levels off it takes a moment to catch up, so for a brief period it continues to over-read. This matters most when levelling off at a minimum altitude close to terrain, where the aircraft is actually a little lower than indicated.",
    },
    2647: {
        "a": "A green arc",
        "b": "A white arc",
        "c": "A red radial line",
        "e": "The yellow arc on the ASI is the caution range, from VNO (the maximum structural cruising speed) up to VNE, the red never-exceed line. Flight in the yellow arc is permitted only in smooth air and with care, because gusts could overstress the airframe. The green arc is the normal operating range and the white arc the flap operating range.",
    },
    2648: {
        "b": "The static vent is also blocked",
        "d": "The alternate static source has been selected",
        "e": "A blocked pitot line normally traps the pressure in the ASI capsule, so the reading freezes rather than falling. If it falls to zero, the trapped pitot pressure must be escaping through a leak until it equals the static pressure in the case, leaving no pressure difference. A static blockage or the alternate static source would not make the ASI read zero in level flight.",
    },
    2649: {
        "c": "The lower end of the green arc",
        "d": "The red radial line",
        "e": "The white arc is the flap operating range. Its lower end is VSO, the stalling speed in the landing configuration (full flap and gear down) at maximum weight, and its upper end is VFE, the maximum speed with flaps extended. The lower end of the green arc is VS1, the clean stalling speed, and the red line is VNE.",
    },
    2650: {
        "a": "Remain constant while the capsule pressure decreases",
        "d": "Decrease at a higher rate than that inside the capsule",
        "e": "In a climb the outside static pressure falls. The VSI capsule, connected directly to the static line, loses pressure immediately, while the case pressure falls more slowly because it can only change through the calibrated leak. So the case pressure decreases at a slower rate than the capsule pressure, the capsule ends up at a lower pressure than the case and contracts, and the pointer shows a climb.",
    },
    2651: {"keep": True},
    2652: {
        "a": "1023 hpa",
        "c": "1013 hpa",
        "d": "993 hpa",
        "e": "GIVEN\nPressure altitude 2800 ft; airfield elevation 2500 ft.\n\nFORMULA\nPressure altitude = elevation + (1013 - QNH) x 30 ft/hPa\n\nSOLVE\nPressure altitude - elevation = 2800 - 2500 = 300 ft\n300 ft ÷ 30 ft per hPa = 10 hPa\nPressure altitude is above the elevation, so QNH is below 1013 hPa\nQNH = 1013 - 10 = 1003 hPa\n\nANSWER\n1003 hPa",
    },
    2653: {"keep": True},
}
