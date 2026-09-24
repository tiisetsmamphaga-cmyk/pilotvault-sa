R = {
    2591: {
        "e": "The condenser is connected across (in parallel with) the contact-breaker points. As the points open, the primary current tries to keep flowing and would jump the gap as an arc, burning the points and slowing the collapse of the magnetic field. The condenser absorbs that surge instead, so the points last longer and the field collapses quickly, giving a strong spark. The distributor sends the high voltage to the plugs, and the impulse coupling looks after starting.",
    },
    2592: {
        "e": "At cranking speed (about 120 rpm) a magneto cannot produce a strong enough spark, so the spark is augmented during the start. The battery-powered low-tension booster coil supplies the magneto's primary coil with a low voltage and is switched off once the engine is running. High-voltage impulses to a trailing brush come from a high-tension booster coil, and the spring mechanism is the impulse coupling.",
    },
    2594: {
        "a": "Prevent current flowing from the battery into the generator",
        "e": "A generator's output voltage would otherwise rise with engine speed and fall with electrical load. The voltage regulator senses the system voltage and adjusts the current in the generator's field winding to keep the output within limits (about 14 V in a 12 V system, 28 V in a 24 V system), preventing both overcharging and undercharging of the battery. Stopping reverse current is the cut-out's job, routing the spark is the distributor's, and stepping up voltage is a transformer's.",
    },
    2595: {
        "e": "At cranking speed the magnet turns too slowly to produce a strong spark, and at the normal advanced timing the engine could kick back. The impulse coupling holds the magnet back while a spring winds up, then releases it to flick round quickly: this gives a strong spark, and because it fires later than normal it is retarded, near TDC, so the engine cannot kick back. Once the engine runs, centrifugal force holds the pawls clear and the coupling has no further effect.",
    },
    2596: {
        "c": "Convert the magneto's AC output into DC",
        "d": "Reduce the voltage to protect the spark plugs",
        "e": "In a low-tension ignition system the magneto produces a low voltage, which is sent along the ignition leads to a small transformer (coil) mounted close to each spark plug. The transformer steps it up to the high voltage needed to jump the plug gap just before it reaches the plug. Keeping the long leads at low voltage greatly reduces flash-over and leakage, which get worse at altitude. The transformer raises the voltage; it does not reduce it or convert AC to DC.",
    },
    2597: {
        "b": "Control the alternator's output voltage",
        "c": "Store electrical charge",
        "d": "Prevent arcing across the contact points",
        "e": "An alternator generates alternating current in its stator, but the aircraft's bus and battery need direct current. The rectifier - a set of diodes built into the alternator - lets current pass in one direction only and so converts the AC output to DC; the diodes also stop the battery discharging back into the alternator. The voltage regulator controls the output, a capacitor stores charge, and the magneto's condenser prevents arcing.",
    },
    2599: {
        "e": "A DC generator is self-exciting: its field poles keep a little residual magnetism, so as soon as the armature turns it produces a small voltage, which is fed back to the field winding to strengthen the field, and the output builds up until the regulator takes control. It therefore needs no battery power to start generating, unlike an alternator, whose field must be energised from the battery. Its commutator gives DC, not AC, at the terminals.",
    },
    2600: {
        "e": "An alternator's rectifier diodes let current flow only from the alternator to the bus. If the alternator's output falls below battery voltage - at low RPM, or when it fails - the diodes block any current trying to flow back from the battery, so no separate reverse-current cut-out is needed. The field switch turns the alternator on and off, the voltage regulator controls its output, and the ammeter only indicates the current.",
    },
    2602: {
        "e": "Battery capacity in ampere-hours is current multiplied by time. For 40 Ah, 4 A for 10 hours gives 40 Ah, so that is the answer; the others work out at only 20 Ah (10 A for 2 hours, 4 A for 5 hours and 20 A for 1 hour). In practice a battery delivers less than its rating, especially at high currents and low temperatures, so after an alternator failure the pilot should shed electrical load to make the battery last.",
    },
    2604: {
        "a": "Store electrical charge",
        "b": "Convert AC to DC",
        "d": "Increase the current in the circuit",
        "e": "A resistor opposes the flow of current, and by Ohm's law (V = I × R) a voltage drop appears across it. Fixed resistors set the voltage or current in part of a circuit, and variable resistors (rheostats) let it be adjusted - for example to dim the panel lights. A resistor does not store charge (a capacitor does) or convert AC to DC (a rectifier does), and adding resistance reduces the current rather than increasing it.",
    },
    2607: {
        "d": "Convert alternating current to direct current",
        "e": "An inverter changes direct current into alternating current. Light aircraft have DC electrical systems, but some instruments and avionics need AC, so an inverter provides it. The reverse process, AC to DC, is done by a rectifier such as the diodes in an alternator, and changing DC to DC or AC to AC at a different voltage is the job of converters and transformers.",
    },
    2608: {
        "c": "It should be held in by hand until the fault clears itself",
        "d": "It should be reset as many times as necessary until it stays in",
        "e": "A circuit breaker trips when the current in its circuit has been too high, which usually means there is a fault. The accepted practice is to wait a short time for it to cool and then reset it once, if the equipment is needed; if it trips again the fault is still there and it must be left out. Resetting it before it has cooled, holding it in or resetting it repeatedly can overheat the wiring and start a fire.",
    },
    2609: {
        "a": "Potassium hydroxide and water",
        "c": "Nitric acid and water",
        "e": "The electrolyte in a lead-acid battery is dilute sulphuric acid: sulphuric acid mixed with pure (distilled) water. As the battery discharges, the acid combines with the plates and the electrolyte becomes weaker, which is why its specific gravity shows the state of charge. Potassium hydroxide is the alkaline electrolyte of a nickel-cadmium battery, and the two battery types must never be serviced with each other's fluids or tools.",
    },
    2610: {
        "a": "Commutator",
        "b": "Voltage regulator",
        "c": "Inverter",
        "e": "An alternator's stator produces AC, and a rectifier - a set of diodes, usually built into the alternator - converts it to DC for the bus and battery. A commutator does a similar job mechanically in a DC generator, the voltage regulator controls the output voltage, and an inverter does the opposite conversion, from DC to AC.",
    },
    2611: {
        "e": "A voltmeter measures electrical potential - voltage - so in the aircraft it shows the bus or battery voltage. It lets the pilot check that the alternator is charging (about 14 V in a 12 V system, 28 V in a 24 V system) and spot a low voltage after an alternator failure or a high voltage from a faulty regulator. Current into and out of the battery is shown by a centre-zero ammeter, and overload protection comes from fuses and circuit breakers.",
    },
    2612: {
        "b": "six cells",
        "c": "eight cells",
        "d": "twenty-four cells",
        "e": "Each lead-acid cell produces about 2 volts, whatever its size, and the cells are connected in series so their voltages add. A 12 V battery therefore has six cells and a 24 V battery twelve. The size of the cells (their plate area) affects the capacity in ampere-hours, not the voltage.",
    },
    2613: {
        "a": "1 amp for 2 hours",
        "c": "2 amps for 20 hours",
        "d": "20 amps for 20 hours",
        "e": "A battery's capacity in ampere-hours is current multiplied by time, so a 20 Ah battery could in theory provide 20 amps for 1 hour, 10 amps for 2 hours or 1 amp for 20 hours. The other options work out at 2 Ah, 40 Ah and 400 Ah. In practice the usable capacity is lower, particularly at high discharge rates and in cold weather.",
    },
    2614: {
        "b": "Convert the battery's DC into AC for the instruments",
        "c": "Provide the spark for the ignition system",
        "d": "Turn the engine over for starting",
        "e": "The engine-driven alternator is the aircraft's main source of electrical power in flight: it supplies all the electrical loads and recharges the battery after the engine start. The battery then only has to provide power for starting and act as a reserve if the alternator fails. The ignition spark comes from the independent magnetos, the starter motor turns the engine, and converting DC to AC is an inverter's job.",
    },
    2723: {
        "e": "A starter motor has to turn a cold, stiff engine from rest, so it needs very high torque at low speed. In a series-wound DC motor the field winding carries the full armature current, so the torque is greatest at the start, when the current is highest - ideal for starting. Shunt-wound motors give a more constant speed but less starting torque, and an alternator winding is for generating, not driving.",
    },
    2725: {
        "e": "An AC generator's frequency depends on its speed, and aircraft AC equipment needs a constant frequency (usually 400 Hz). Engine speed varies with the phase of flight, so a constant-speed drive (CSD) between the engine and the generator varies its drive ratio automatically so the generator always turns at almost the same speed. It does not change the engine RPM, and a fixed ratio would let the frequency drift with engine speed.",
    },
    2734: {
        "e": "An inverter converts DC into AC, and it is used in DC-powered aircraft to supply instruments and avionics that need AC. A rectifier does the opposite, converting AC to DC, and a transformer-rectifier unit changes the AC voltage and then rectifies it to DC. A thermistor is a temperature-sensitive resistor used in temperature probes.",
    },
    2738: {
        "e": "A current-carrying conductor has its own magnetic field. When it lies across an external magnetic field the two fields interact and push the conductor sideways: a force is exerted on it, in a direction given by Fleming's left-hand rule. This is the motor principle, used in the starter motor. The conductor does not need to be moving already - moving a conductor through a field to induce a current is the generator principle.",
    },
    2751: {
        "e": "As the magnet rotates, current builds up in the magneto's primary winding (a few turns of thick wire). At the moment of ignition the contact-breaker points open, the primary current stops and the magnetic flux collapses very rapidly. That rapid change induces a very high voltage in the secondary winding, which has thousands of turns of fine wire, and the distributor sends it to the plug. No battery is involved, and the spark needs high voltage, not high current.",
    },
}
