R = {
    2558: {
        "a": "The ignition switch contacts directly",
        "b": "A circuit breaker in the starter cable",
        "d": "The alternator's voltage regulator",
        "e": "A starter motor draws a very large current, often a few hundred amps - far more than a cockpit switch or thin wiring could carry. So the starter switch only energises a solenoid, a heavy-duty electromagnetic relay mounted near the starter, which closes the contacts in the short, thick cable from the battery to the motor. Switch contacts carrying that current would burn out, and the voltage regulator controls only the alternator's output.",
    },
    2567: {
        "b": "Indicate the alternator's total output only",
        "c": "Indicate the battery's state of charge in ampere-hours",
        "e": "A centre-zero ammeter is fitted in the battery lead, so it shows current flowing into or out of the battery. A needle to the right (+) means the alternator is charging the battery; to the left (-) means the battery is discharging and supplying the load, which in flight warns of an alternator failure. Voltage is shown by a voltmeter, and a left-zero ammeter (loadmeter) shows the alternator's output only.",
    },
    2568: {
        "a": "Prevent the generator from being overloaded",
        "c": "Regulate the generator's output voltage",
        "d": "Convert the generator's output to DC",
        "e": "When the engine is idling or stopped, the generator's voltage falls below the battery's. Without protection the battery would then drive current backwards through the generator, discharging itself and trying to run the generator as a motor. The reverse-current cut-out disconnects the generator whenever its output falls below battery voltage and reconnects it when it rises. The voltage regulator controls the output, and the commutator produces the DC.",
    },
    2569: {
        "e": "A magneto is a self-contained generator: a permanent magnet, driven by the engine, rotates between the poles of a soft-iron core carrying the coils. The constantly reversing magnetic flux induces current in the primary winding, and interrupting that current induces the high voltage for the plugs. Because it depends only on the rotating magnet, the ignition keeps working even if the battery and alternator fail. The distributor merely routes the high voltage to the plugs.",
    },
    2570: {
        "e": "The magneto makes its own electricity by electromagnetic induction: as the engine turns the permanent magnet, the flux through the coil keeps reversing, inducing a current in the primary winding. When the contact-breaker points open, the collapsing flux induces a very high voltage in the secondary winding for the spark plugs. It needs no battery, alternator or starter, which is why the engine keeps running after a total electrical failure.",
    },
    2571: {
        "a": "It should be replaced with a fuse of a higher rating to stop it blowing again",
        "c": "It may be replaced as many times as necessary until it holds",
        "d": "It should be bypassed with a piece of wire until after landing",
        "e": "A fuse blows because the current in its circuit has exceeded its rating, which usually means there is a fault. It may be replaced once with a fuse of the same rating; if the new one also blows, the fault is still there and the circuit must be left off. A higher-rated fuse, repeated replacement or bypassing it with wire would let the wiring overheat and could start an electrical fire.",
    },
    2572: {
        "a": "Reverse-current cut-out",
        "b": "Rectifier",
        "d": "Commutator",
        "e": "A generator's output voltage rises with its speed and falls with load. The voltage regulator keeps it within limits by varying the current through the generator's field winding: more field current strengthens the magnetic field and raises the output, less reduces it. The reverse-current cut-out stops the battery discharging through the generator, and the commutator converts the armature's AC into DC.",
    },
    2573: {
        "a": "Regulate the output voltage",
        "c": "Store electrical energy",
        "d": "Protect the circuit from overloads",
        "e": "An alternator's stator windings produce alternating current, but the aircraft's system and battery need direct current. Diodes let current flow in one direction only, so a set of them (the rectifier) inside the alternator converts the AC output to DC; they also stop the battery discharging back through the alternator, so no reverse-current cut-out is needed. Voltage is controlled by the regulator, and overload protection by fuses and circuit breakers.",
    },
    2574: {
        "a": "As a means of regulating the alternator's voltage",
        "b": "As a means of measuring the current in each circuit",
        "c": "As a means of converting AC to DC",
        "e": "A circuit breaker protects a circuit's wiring from overheating: if the current exceeds its rating, a bimetallic element heats up and trips the breaker, opening the circuit. Unlike a fuse it can be reset, but a tripped breaker should be reset only once, after a short cooling period, and never held in. It does not regulate voltage, measure current or convert AC to DC.",
    },
    2575: {
        "a": "Produce the high voltage in the secondary winding",
        "b": "Open the primary circuit at the correct moment",
        "c": "Retard the spark during engine start",
        "e": "The magneto's secondary winding produces the high voltage, and the distributor sends it to the right place: a rotor turning at half engine speed passes each high-tension lead in turn, so each spark plug receives its spark in the engine's firing order. The contact-breaker points open the primary circuit to create the spark, and the impulse coupling provides the retarded spark for starting.",
    },
    2576: {
        "a": "Stopping the engine immediately",
        "b": "Making the magneto produce no sparks at all",
        "d": "Causing a large drop in RPM on the magneto check",
        "e": "The magneto is switched off by earthing (grounding) its primary circuit through the P-lead, which stops it producing sparks. If the P-lead is broken or disconnected, turning the switch to OFF no longer earths the magneto, so it stays live and the engine keeps running. Worse, anyone moving the propeller of a parked aircraft could start it, so every propeller must be treated as live. The dead-cut check after start shows whether each magneto can be switched off.",
    },
    2577: {
        "b": "Indicate current flowing into and out of the battery",
        "d": "Indicate the battery's state of charge",
        "e": "A left-zero ammeter, or loadmeter, is connected in the alternator (or generator) output lead, so it reads from zero upwards and shows only how much current the alternator is producing to supply the loads and charge the battery; it cannot show a discharge. A centre-zero ammeter in the battery lead is the one that shows current flowing into and out of the battery, and voltage needs a voltmeter.",
    },
    2578: {
        "a": "The field winding",
        "c": "The voltage regulator",
        "e": "The armature coils of a DC generator rotate in a magnetic field, so the voltage induced in them reverses every half-turn: it is alternating. The commutator, a ring of copper segments on the armature shaft with carbon brushes riding on it, reverses the connections to each coil at the right moment, so the output at the brushes is direct current. An alternator does the same job electronically, with diodes.",
    },
    2579: {
        "c": "Are that zero is at the left-hand end of the scale",
        "d": "Are that the scale is marked in volts",
        "e": "A centre-zero ammeter has zero in the middle of its scale. A reading to the right, on the positive side, means current is flowing into the battery (it is being charged); a reading to the left, on the negative side, means the battery is discharging, and a steady discharge in flight usually means the alternator has failed. Zero at the left-hand end describes a loadmeter, and the scale is in amperes, not volts.",
    },
    2580: {
        "a": "Needs no voltage regulator",
        "b": "Produces direct current without the need for diodes",
        "d": "Can recharge a completely flat battery by itself",
        "e": "An alternator produces useful output even at low RPM, such as at idle or while taxiing, whereas an old-style DC generator produces little until the engine speed is fairly high; it is also lighter for the same output. It still needs a voltage regulator, relies on diodes to convert its AC to DC, and needs battery power to energise its field, so it cannot bring a completely flat battery back to life on its own.",
    },
    2581: {
        "a": "Volts",
        "b": "Watts",
        "c": "Ohms",
        "e": "A battery's capacity is the amount of charge it can store, expressed in ampere-hours: current multiplied by time. A 24 Ah battery could in theory supply 24 A for one hour or 2 A for 12 hours, although in practice it delivers less at high currents and low temperatures. Volts measure its electrical pressure, watts power and ohms resistance, none of which describes its capacity.",
    },
    2582: {
        "a": "Measure the system voltage",
        "c": "Measure the resistance of a circuit",
        "d": "Measure the electrical power being used",
        "e": "An ammeter measures electrical current - the rate of flow of charge - in amperes. In aircraft it is either a centre-zero type in the battery lead, showing charge and discharge, or a left-zero loadmeter showing the alternator's output. Voltage is measured by a voltmeter, resistance by an ohmmeter, and power in watts.",
    },
    2583: {
        "a": "The engine will stop immediately",
        "c": "The magneto will not produce any sparks",
        "d": "The alternator will stop charging the battery",
        "e": "The magneto earth (P-) lead connects the magneto's primary circuit to the ignition switch. Selecting OFF earths the primary circuit so no sparks are produced; if the wire is broken the magneto cannot be earthed and remains live. The engine will keep running with the switch OFF, and a stationary engine can fire if the propeller is turned by hand, so always treat a propeller as live. A broken P-lead has no effect on the alternator.",
    },
    2585: {
        "a": "Rotates inside the magnetic field",
        "c": "Converts AC to DC",
        "d": "Regulates the output voltage",
        "e": "In an alternator the stator is the fixed set of windings around the inside of the casing, while the rotor - an electromagnet fed through slip rings - spins inside it. The rotating magnetic field induces alternating current in the stationary stator windings, so the heavy output current does not have to pass through brushes. The diodes convert the AC to DC, and the voltage regulator controls the field current.",
    },
    2586: {
        "c": "Tap water",
        "d": "Sulphuric acid only",
        "e": "During charging, some of the water in the electrolyte is split into hydrogen and oxygen and escapes, but the sulphuric acid stays in the battery. So only water needs to be replaced, and it must be distilled water, because the minerals in tap water would contaminate the plates; adding acid would make the electrolyte too strong. The hydrogen given off is explosive, so batteries must be kept well ventilated.",
    },
    2587: {
        "a": "Watts",
        "d": "Ohms",
        "e": "A fuse is a thin wire or strip that melts when the current through it exceeds its rating, so it is rated in amperes: the current it can carry continuously without blowing. The rating is chosen to protect the wiring of that circuit, which is why a blown fuse must only be replaced with one of the same ampere rating. Volts, watts and ohms describe other electrical quantities.",
    },
    2589: {
        "b": "An alternator cannot be used to charge a lead-acid battery",
        "c": "An alternator does not need a voltage regulator",
        "e": "Compared with a DC generator, an alternator gives useful output at a much lower RPM - it will charge the battery even at idle or while taxiing - and it is lighter for the same output, which is why modern light aircraft use alternators. An alternator still needs a voltage regulator, and it charges the lead-acid battery normally through diodes that convert its AC output to DC.",
    },
    2590: {
        "a": "Limit the current in the circuit",
        "c": "Convert AC to DC",
        "d": "Measure the voltage of the circuit",
        "e": "A capacitor (condenser) is two conducting plates separated by an insulator. When a voltage is applied, charge builds up on the plates and is stored there until the circuit lets it discharge. In a magneto the condenser absorbs the surge as the points open, preventing arcing and speeding the collapse of the magnetic field; elsewhere capacitors smooth voltage and suppress radio interference. Limiting current is a resistor's job, and diodes convert AC to DC.",
    },
}
