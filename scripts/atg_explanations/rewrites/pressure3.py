R = {
    2654: {
        "a": "Remain constant",
        "e": "With the pitot tube and its drain blocked, the capsule keeps the pitot pressure from the altitude where the blockage occurred. As the aircraft climbs, the static pressure in the case falls, so the difference between capsule and case grows and the ASI over-reads, showing an increasing speed even though the real speed may be falling. A pilot following it could raise the nose towards a stall. In a descent it would under-read.",
    },
    2655: {
        "b": "The correct altitude at all times",
        "d": "Zero until the aircraft levels off",
        "e": "An altimeter's capsule and mechanism take a moment to respond, so in a rapid climb the indication lags behind and shows an altitude lower than the aircraft's actual altitude; in a rapid descent it shows a higher one. The lag is small in a normal climb and disappears once the aircraft levels off. The altimeter responds all the time: it is neither perfectly accurate at once nor stuck at zero.",
    },
    2656: {
        "a": "Position error will be doubled",
        "c": "The ASI will no longer need a pitot tube",
        "d": "Instrument error will be removed",
        "e": "In a sideslip or yaw, the vent on the side facing the airflow senses a pressure that is too high and the one on the sheltered side a pressure that is too low. Connecting a vent on each side of the fuselage averages the two, so the errors largely cancel and position error is reduced. Instrument error is a separate, manufacturing error, and the ASI still needs its pitot tube.",
    },
    2657: {
        "c": "Indicated airspeed corrected for temperature and density",
        "d": "True airspeed corrected for wind",
        "e": "Indicated airspeed (IAS) is what the ASI shows. Correcting it for instrument error (manufacturing imperfections) and position error (the static vent not sensing the exact ambient pressure) gives calibrated, or rectified, airspeed (CAS or RAS); the POH lists these corrections. Correcting CAS for density - altitude and temperature - then gives true airspeed, and allowing for the wind gives groundspeed.",
    },
    2658: {
        "c": "Remain the same",
        "d": "Become equal to the case pressure",
        "e": "The VSI capsule is connected directly to the static line. In a descent the outside pressure rises, so the capsule pressure increases immediately, while the case pressure rises more slowly through the calibrated leak. The capsule, now at a higher pressure than the case, expands and the pointer shows a rate of descent.",
    },
    2659: {
        "a": "CAS/RAS corrected for instrument and position error",
        "b": "CAS/RAS corrected for wind",
        "c": "CAS/RAS corrected for compressibility only",
        "e": "The ASI is calibrated for ISA sea-level density, but as altitude increases, or the temperature rises, the air becomes less dense and the ASI shows less than the true speed through the air. Correcting CAS (RAS) for altitude and temperature - that is, for density - gives true airspeed; a flight computer does this, or allow roughly 2% per 1,000 ft. Instrument and position error are corrected going from IAS to CAS, and the wind gives groundspeed.",
    },
    2660: {
        "e": "In many light aircraft the alternate static source is simply a valve that opens the static system to the air inside the cockpit. The cockpit is protected from external icing, so it provides a usable static pressure if the external vents ice up or become blocked. The pressure inside is usually slightly lower than outside static pressure, so the altimeter and ASI read a little high. It does not use the pitot tube or the vacuum system.",
    },
    2661: {
        "a": "Remain unaffected",
        "e": "The cockpit pressure is usually a little lower than the true outside static pressure, because air flowing over the fuselage creates a slight suction. With the alternate source selected, that lower pressure is fed to the ASI case, so the difference between the pitot pressure in the capsule and the case is larger than it should be, and the ASI over-reads. The altimeter over-reads for the same reason.",
    },
    2665: {
        "a": "Contract causing the instrument to show an increase in altitude",
        "b": "Expand causing the instrument to show a decrease in altitude",
        "c": "Contract causing the instrument to show a decrease in altitude",
        "ans": "Contract causing the instrument to show a decrease in altitude",
        "d": "Expand causing the instrument to show an increase in altitude",
        "e": "As the aircraft descends, the static pressure in the altimeter case increases and squeezes the sealed, partly evacuated capsule, so it contracts. The mechanism converts the contraction into a lower altitude reading. Climbing does the opposite: the falling pressure lets the capsule expand and the reading rises. Contraction always means a lower reading and expansion a higher one.",
    },
    2702: {
        "e": "The International Standard Atmosphere defines mean sea-level conditions as 1013.25 hPa, 15 °C and a density of 1.225 kg/m³. Density decreases with height, to roughly half its sea-level value at about 22,000 ft, and ISA sea-level density is the value the ASI is calibrated for. Real air is rarely exactly standard: warm, high or humid conditions reduce density and aircraft performance.",
    },
    2707: {
        "e": "In the ISA the mean sea-level temperature is +15 °C, and it falls at about 1.98 °C per 1,000 ft (6.5 °C per km, usually rounded to 2 °C per 1,000 ft) up to the tropopause at 36,090 ft (11 km), above which it stays constant at -56.5 °C. The 3 °C per 1,000 ft figure is the dry adiabatic lapse rate, not the ISA value.",
    },
    2722: {
        "e": "VNO is the maximum structural cruising speed: the top of the green arc and the maximum speed for normal operations. Above it, in the yellow caution arc, the aircraft may be flown only in smooth air. VNE is the never-exceed speed (red line), VFE the maximum flap-extended speed, and VA the manoeuvring speed, above which full, abrupt control deflections could overstress the aircraft.",
    },
    2724: {
        "e": "VSO is the stalling speed (or minimum steady flight speed) in the landing configuration - full flap and, if retractable, gear down - and it is shown by the lower end of the white arc. VS1 is the stalling speed in a specified configuration, normally clean, at the bottom of the green arc. VNO is the maximum structural cruising speed and VFE the maximum flap-extended speed.",
    },
    2733: {
        "e": "Dynamic pressure is the pressure of the air due to its motion: q = ½ρV², where ρ is the air density and V the airspeed. Doubling the speed therefore quadruples the dynamic pressure, which is why lift, drag and control forces rise so quickly with speed, and it is what the ASI measures. Lift and drag coefficients describe the wing, not the air, and static pressure is a separate quantity.",
    },
    2739: {
        "e": "The yellow arc on the ASI marks the caution range, between VNO and VNE. The aircraft may be flown in it only in smooth air and with care, because a strong gust at that speed could overstress the structure. Green is the normal operating range, white the flap operating range, and the red radial line is VNE, the never-exceed speed.",
    },
    2740: {
        "e": "VFE is the maximum speed at which the flaps may be extended or flown extended, shown by the upper end of the white arc; above it the air loads could damage the flaps and their mechanism. VLE is the maximum speed with the landing gear extended, VNO the maximum structural cruising speed and VSO the stalling speed in the landing configuration.",
    },
    2745: {
        "e": "VS1 is the stalling speed (or minimum steady flight speed) in a specified configuration, normally clean with the flaps up, and it is the lower end of the green arc on the ASI. VSO is the stalling speed in the landing configuration, at the bottom of the white arc. VNE is the never-exceed speed and VX the best angle-of-climb speed.",
    },
    2748: {
        "e": "QFE is the atmospheric pressure at the airfield datum, usually the airfield elevation or runway threshold. With QFE set the altimeter reads zero on the ground there and shows height above the airfield in flight, which is useful in the circuit. QNH gives altitude above mean sea level, so the altimeter reads the airfield elevation on the ground, and 1013.25 hPa gives pressure altitude and flight levels.",
    },
    2754: {
        "e": "The altimeter must be set before every flight and updated whenever a new setting is needed: when the QNH changes, when entering another altimeter-setting region, when passing the transition altitude or level, or when ATC passes a new setting. Pressure changes through the day, and an out-of-date setting can put the aircraft hundreds of feet lower than indicated - 'high to low, look out below'.",
    },
    2758: {
        "e": "VR is the rotation speed: the speed at which the pilot raises the nose wheel and rotates the aeroplane to the take-off attitude. V1 is the take-off decision speed used on multi-engine and larger aircraft, VX the best angle-of-climb speed (the most height for distance, for clearing obstacles) and VY the best rate-of-climb speed (the most height for time).",
    },
    2771: {
        "e": "A simple ASI measures dynamic pressure (½ρV²) and converts it to a speed assuming the air has the ISA sea-level density of 1.225 kg/m³. At that density IAS equals TAS; higher up, or in warmer air, the density is lower, so the ASI reads less than the true airspeed. That is why TAS must be worked out from CAS using altitude and temperature, while stalling speeds stay much the same in IAS.",
    },
}
