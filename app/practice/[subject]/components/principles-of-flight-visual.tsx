"use client"

import type { Question } from "../types"

type Concept =
  | "axes-controls"
  | "stability"
  | "dihedral"
  | "cg-stability"
  | "aerofoil"
  | "angle-of-attack"
  | "boundary-layer"
  | "bernoulli"
  | "centre-pressure"
  | "aspect-ratio"
  | "lift-speed"
  | "drag-curves"
  | "power-required"
  | "force-equilibrium"
  | "flap-types"
  | "slat"
  | "ground-effect"
  | "differential-ailerons"
  | "asymmetric-flap"
  | "bank-load-factor"
  | "turn-forces"
  | "stall-speed-load"
  | "turn-radius"
  | "rolling-moment"
  | "propeller-pitch"
  | "propeller-twist"
  | "constant-speed-unit"
  | "propeller-thrust"
  | "p-factor"
  | "v-speeds"
  | "va-weight"
  | "vx-vy"
  | "critical-aoa"
  | "stall-progression"
  | "stall-recovery"
  | "spin"
  | "propwash"
  | "density-performance"
  | "wind-runway"
  | "soft-field"
  | "short-field"
  | "climb-gradient"

type Spec = { concept: Concept; title: string; note: string }

const NAVY = "#06111f"
const GOLD = "#f4b400"
const BLUE = "#1f4e79"
const GREY = "#64748b"
const LIGHT = "#e2e8f0"
const RED = "#b91c1c"

function text(question: Question) {
  return `${question.question} ${question.correctAnswer}`.toLowerCase()
}

function has(question: Question, ...terms: string[]) {
  const value = text(question)
  return terms.some((term) => value.includes(term.toLowerCase()))
}

function getSpec(question: Question): Spec {
  const topic = question.topic ?? ""

  if (has(question, "differential aileron", "adverse yaw")) return { concept: "differential-ailerons", title: "DIFFERENTIAL AILERONS & ADVERSE YAW", note: "The up-going aileron normally moves farther than the down-going aileron to reduce adverse yaw." }
  if (has(question, "asymmetric flap", "one flap", "flap asymmetry")) return { concept: "asymmetric-flap", title: "ASYMMETRIC FLAP EXTENSION", note: "Unequal flap deflection produces unequal lift and drag, creating a strong rolling and yawing tendency." }
  if (has(question, "slat", "slot", "leading-edge device")) return { concept: "slat", title: "SLATS & LEADING-EDGE SLOTS", note: "A slot feeds higher-energy air over the upper surface and delays flow separation at high angle of attack." }
  if (has(question, "ground effect")) return { concept: "ground-effect", title: "GROUND EFFECT", note: "Near the surface, downwash and wingtip-vortex strength reduce, so induced drag decreases." }
  if (has(question, "split flap", "fowler flap", "plain flap", "slotted flap", "flap")) return { concept: "flap-types", title: "HIGH-LIFT FLAP EFFECTS", note: "Extending flaps increases camber and usually lift and drag; the exact effect depends on flap type and deflection." }

  if (has(question, "dihedral")) return { concept: "dihedral", title: "DIHEDRAL EFFECT & LATERAL STABILITY", note: "A sideslip increases the effective angle of attack on the lower wing, producing a restoring rolling moment." }
  if (has(question, "centre of gravity", "center of gravity", "forward cg", "aft cg", "c.g.", " cg ", "trim")) return { concept: "cg-stability", title: "CENTRE OF GRAVITY & LONGITUDINAL STABILITY", note: "A forward CG generally increases longitudinal stability and control force; an aft CG reduces the stability margin." }
  if (has(question, "longitudinal stability", "lateral stability", "directional stability", "static stability", "dynamic stability", "restoring", "stability")) return { concept: "stability", title: "AIRCRAFT STABILITY", note: "Positive static stability creates an initial restoring tendency after a disturbance." }
  if (has(question, "rudder", "elevator", "aileron", "pitch axis", "roll axis", "yaw axis", "three axes", "vertical axis", "lateral axis", "longitudinal axis")) return { concept: "axes-controls", title: "AIRCRAFT AXES & PRIMARY CONTROLS", note: "Ailerons control roll about the longitudinal axis, elevator controls pitch about the lateral axis, and rudder controls yaw about the vertical axis." }

  if (has(question, "boundary layer", "laminar", "turbulent", "transition point", "flow separation")) return { concept: "boundary-layer", title: "BOUNDARY LAYER & FLOW SEPARATION", note: "The boundary layer changes from laminar to turbulent before separation; an adverse pressure gradient promotes separation." }
  if (has(question, "centre of pressure", "center of pressure")) return { concept: "centre-pressure", title: "CENTRE OF PRESSURE MOVEMENT", note: "The centre of pressure is the point through which the resultant aerodynamic force is treated as acting." }
  if (has(question, "bernoulli", "pressure decreases", "velocity increases", "pressure and velocity", "venturi")) return { concept: "bernoulli", title: "AIRFLOW VELOCITY & STATIC PRESSURE", note: "In subsonic flow, an increase in local airflow speed is associated with a decrease in static pressure." }
  if (has(question, "aspect ratio", "span squared", "wing span", "high aspect")) return { concept: "aspect-ratio", title: "WING ASPECT RATIO", note: "Aspect ratio compares span with chord; a higher aspect ratio generally reduces induced drag for a given lift." }
  if (has(question, "lift is proportional", "lift proportional", "doubling", "airspeed squared", "velocity squared", "lift equation")) return { concept: "lift-speed", title: "LIFT & AIRSPEED", note: "With other factors constant, lift varies with the square of true airspeed: L ∝ V²." }
  if (has(question, "angle of attack", "relative airflow", "relative air flow", "chord line")) return { concept: "angle-of-attack", title: "ANGLE OF ATTACK", note: "Angle of attack is the angle between the aerofoil chord line and the relative airflow." }
  if (has(question, "aerofoil", "airfoil", "camber", "thickness/chord", "thickness-to-chord", "trailing edge", "leading edge", "chord")) return { concept: "aerofoil", title: "AEROFOIL GEOMETRY", note: "Chord, camber, thickness and leading/trailing-edge geometry define the aerofoil section." }

  if (has(question, "power required", "power available")) return { concept: "power-required", title: "POWER REQUIRED", note: "Power required equals drag multiplied by true airspeed; its minimum occurs at a different speed from minimum drag." }
  if (has(question, "parasite drag", "induced drag", "total drag", "minimum drag", "l/d", "lift/drag", "lift-to-drag", "drag curve")) return { concept: "drag-curves", title: "INDUCED, PARASITE & TOTAL DRAG", note: "Induced drag dominates at low speed, parasite drag at high speed, and total drag is lowest where their sum is minimum." }
  if (has(question, "four forces", "equilibrium", "straight and level", "thrust equals drag", "lift equals weight")) return { concept: "force-equilibrium", title: "FORCES IN STEADY FLIGHT", note: "In steady straight-and-level flight, lift balances weight and thrust balances drag." }

  if (has(question, "60°", "60 degree", "60-degree", "2 g", "2g", "bank angle produces", "load factor of 2")) return { concept: "bank-load-factor", title: "BANK ANGLE & LOAD FACTOR", note: "In a balanced level turn, load factor is 1/cos(bank angle); at 60° bank it is approximately 2 G." }
  if (has(question, "centripetal", "horizontal component", "balanced level turn", "resultant lift", "lift vector")) return { concept: "turn-forces", title: "FORCES IN A BALANCED LEVEL TURN", note: "The vertical component of lift balances weight while the horizontal component provides centripetal force." }
  if (has(question, "stall speed", "load factor", "accelerated stall")) return { concept: "stall-speed-load", title: "STALL SPEED & LOAD FACTOR", note: "Stall speed increases with the square root of load factor: Vs(new) = Vs × √n." }
  if (has(question, "turn radius", "radius of turn", "rate of turn")) return { concept: "turn-radius", title: "TURN RADIUS & RATE", note: "At a given bank angle, increasing airspeed increases turn radius and reduces rate of turn." }
  if (has(question, "rolling moment", "difference in lift between", "one wing produces more lift")) return { concept: "rolling-moment", title: "ROLLING MOMENT FROM UNEQUAL LIFT", note: "A difference in lift between the wings creates a rolling moment about the longitudinal axis." }

  if (has(question, "constant-speed", "constant speed prop", "governor", "csu")) return { concept: "constant-speed-unit", title: "CONSTANT-SPEED PROPELLER GOVERNING", note: "The governor changes blade angle to oppose RPM changes and maintain the selected propeller speed." }
  if (has(question, "blade twist", "twisted blade", "washout", "geometric pitch varies")) return { concept: "propeller-twist", title: "PROPELLER BLADE TWIST", note: "Blade angle decreases toward the tip so each section works at a useful angle of attack despite increasing rotational speed." }
  if (has(question, "fine pitch", "coarse pitch", "blade angle", "propeller pitch", "pitch setting")) return { concept: "propeller-pitch", title: "FINE & COARSE PROPELLER PITCH", note: "Fine pitch uses a smaller blade angle; coarse pitch uses a larger blade angle for a greater distance advanced per revolution." }
  if (has(question, "p-factor", "asymmetric blade", "asymmetric thrust", "descending blade", "torque effect", "spiral slipstream")) return { concept: "p-factor", title: "ASYMMETRIC PROPELLER EFFECTS", note: "At high angle of attack, the descending blade can develop more thrust than the ascending blade, producing a yawing moment." }
  if (has(question, "windmilling", "rearward", "accelerat", "propeller produces thrust", "thrust from")) return { concept: "propeller-thrust", title: "PROPELLER THRUST & AIRFLOW", note: "The propeller accelerates a mass of air rearward; the reaction produces forward thrust. A windmilling propeller can create substantial drag." }

  if (has(question, "manoeuvring speed", "maneuvering speed", "va ", " va", "v-a")) return { concept: "va-weight", title: "MANOEUVRING SPEED & WEIGHT", note: "VA decreases as aircraft weight decreases because the wing reaches the critical angle of attack at a lower speed." }
  if (has(question, "best angle", "best rate", "vx", "vy")) return { concept: "vx-vy", title: "VX & VY", note: "VX gives the greatest altitude gain per unit horizontal distance; VY gives the greatest altitude gain per unit time." }
  if (has(question, "vno", "vne", "vfe", "vs0", "vso", "vr", "v-speed", "white arc", "green arc", "yellow arc", "never exceed", "flap operating range")) return { concept: "v-speeds", title: "AIRSPEED LIMITATIONS & V-SPEEDS", note: "Each V-speed identifies a defined operating speed or limitation; always use the aircraft-specific approved values." }

  if (has(question, "stall strip", "root first", "tip stall", "stall progression", "wing root")) return { concept: "stall-progression", title: "ROOT-TO-TIP STALL PROGRESSION", note: "Design features such as washout or stall strips encourage the root to stall first so aileron effectiveness is retained longer." }
  if (has(question, "recover", "recovery", "reduce angle", "nose down", "stall recovery")) return { concept: "stall-recovery", title: "STALL RECOVERY SEQUENCE", note: "First reduce angle of attack below critical, then apply power as required, level the wings and return smoothly to the desired flight path." }
  if (has(question, "spin", "autorotation", "incipient")) return { concept: "spin", title: "SPIN: STALLED WINGS + YAW", note: "A spin requires a stall plus yaw; the wings are stalled unequally, producing autorotation." }
  if (has(question, "propwash", "slipstream", "power-on stall", "power off stall")) return { concept: "propwash", title: "PROPELLER SLIPSTREAM & STALLING", note: "Propeller slipstream changes airflow over parts of the wing and tail, so power setting can alter stall behaviour and control effectiveness." }
  if (has(question, "critical angle", "critical aoa", "stall occurs")) return { concept: "critical-aoa", title: "CRITICAL ANGLE OF ATTACK", note: "A wing stalls when its critical angle of attack is exceeded, regardless of indicated airspeed." }

  if (has(question, "soft-field", "soft field")) return { concept: "soft-field", title: "SOFT-FIELD TAKE-OFF TECHNIQUE", note: "Keep weight off the nosewheel, lift off at the earliest safe speed, then accelerate in ground effect before climbing." }
  if (has(question, "short-field", "short field", "obstacle clearance", "50 ft obstacle")) return { concept: "short-field", title: "SHORT-FIELD & OBSTACLE PERFORMANCE", note: "Short-field technique uses the approved configuration and target speed to maximise acceleration and obstacle clearance." }
  if (has(question, "headwind", "tailwind", "wind component", "landing distance", "take-off distance", "takeoff distance")) return { concept: "wind-runway", title: "WIND EFFECT ON RUNWAY PERFORMANCE", note: "A headwind reduces groundspeed for a given airspeed and usually reduces take-off and landing distance; a tailwind does the opposite." }
  if (has(question, "density altitude", "air density", "humidity", "hot day", "high temperature", "pressure altitude", "high elevation")) return { concept: "density-performance", title: "AIR DENSITY & AIRCRAFT PERFORMANCE", note: "Lower air density reduces engine/propeller performance and aerodynamic force for a given true speed, increasing take-off distance and reducing climb." }
  if (has(question, "climb gradient", "gradient of climb", "height gained", "distance travelled")) return { concept: "climb-gradient", title: "CLIMB GRADIENT", note: "Climb gradient is vertical height gained divided by horizontal distance travelled, usually expressed as a percentage." }

  if (topic === "Aircraft Stability & Control") return { concept: "axes-controls", title: "STABILITY & FLIGHT CONTROLS", note: "Identify the disturbed axis, the restoring tendency and the control surface that produces the required moment." }
  if (topic === "Basic Aerodynamics & Lift") return { concept: "aerofoil", title: "BASIC AERODYNAMICS & LIFT", note: "Lift depends on air density, speed squared, wing area and lift coefficient." }
  if (topic === "Drag & Performance") return { concept: "drag-curves", title: "DRAG & AERODYNAMIC EFFICIENCY", note: "The balance between induced and parasite drag determines the total-drag curve and best aerodynamic efficiency." }
  if (topic === "Flaps, Slats & High-Lift Devices") return { concept: "flap-types", title: "HIGH-LIFT DEVICES", note: "High-lift devices alter aerofoil geometry and airflow to change maximum lift, drag and stall characteristics." }
  if (topic === "Load Factor, Turns & Stalls") return { concept: "turn-forces", title: "TURNING FLIGHT & LOAD FACTOR", note: "Banking tilts the lift vector; maintaining altitude requires more total lift and therefore increases load factor." }
  if (topic === "Propellers & Asymmetric Effects") return { concept: "propeller-pitch", title: "PROPELLER AERODYNAMICS", note: "A propeller blade is a rotating aerofoil whose local velocity and blade angle determine its angle of attack and thrust." }
  if (topic === "Speed Definitions & Limitations") return { concept: "v-speeds", title: "V-SPEEDS & OPERATING LIMITS", note: "Use the approved aircraft flight manual values and understand what each speed protects or optimises." }
  if (topic === "Stall Behaviour & Recognition") return { concept: "critical-aoa", title: "STALL BEHAVIOUR", note: "The fundamental cause of an aerodynamic stall is exceeding the critical angle of attack." }
  return { concept: "density-performance", title: "TAKE-OFF, CLIMB & LANDING PERFORMANCE", note: "Runway performance is strongly affected by air density, wind, surface, weight and the technique specified by the aircraft flight manual." }
}

function Arrow({ x1, y1, x2, y2, color = GOLD, width = 4 }: { x1: number; y1: number; x2: number; y2: number; color?: string; width?: number }) {
  const angle = Math.atan2(y2 - y1, x2 - x1)
  const size = 10
  const ax = x2 - size * Math.cos(angle - Math.PI / 6)
  const ay = y2 - size * Math.sin(angle - Math.PI / 6)
  const bx = x2 - size * Math.cos(angle + Math.PI / 6)
  const by = y2 - size * Math.sin(angle + Math.PI / 6)
  return <g><line x1={x1} y1={y1} x2={x2} y2={y2} stroke={color} strokeWidth={width} strokeLinecap="round"/><polygon points={`${x2},${y2} ${ax},${ay} ${bx},${by}`} fill={color}/></g>
}

function T({ x, y, children, size = 15, anchor = "middle", weight = 600, fill = NAVY }: { x: number; y: number; children: React.ReactNode; size?: number; anchor?: "start" | "middle" | "end"; weight?: number; fill?: string }) {
  return <text x={x} y={y} textAnchor={anchor} fontSize={size} fontWeight={weight} fill={fill} fontFamily="Arial, sans-serif">{children}</text>
}

function TechnicalDiagram({ concept }: { concept: Concept }) {
  const common = { viewBox: "0 0 760 320", className: "block w-full", role: "img" as const }

  switch (concept) {
    case "axes-controls": return <svg {...common}><T x={380} y={38} size={16}>AIRCRAFT BODY AXES THROUGH CG</T><circle cx="380" cy="160" r="10" fill={GOLD}/><T x={397} y={154} anchor="start" size={13}>CG</T><Arrow x1={125} y1={160} x2={635} y2={160} color={BLUE}/><T x={620} y={145} size={13}>LONGITUDINAL</T><T x={620} y={184} size={13}>ROLL · AILERONS</T><Arrow x1={380} y1={270} x2={380} y2={60} color={BLUE}/><T x={395} y={75} anchor="start" size={13}>VERTICAL</T><T x={395} y={96} anchor="start" size={13}>YAW · RUDDER</T><Arrow x1={230} y1={245} x2={530} y2={75} color={GREY}/><T x={248} y={238} anchor="start" size={13}>LATERAL</T><T x={248} y={258} anchor="start" size={13}>PITCH · ELEVATOR</T></svg>
    case "stability": return <svg {...common}><line x1="80" y1="210" x2="680" y2="210" stroke={LIGHT} strokeWidth="2"/><path d="M100 210 C170 95 235 95 300 210 C365 270 430 245 485 210 C535 178 585 190 650 210" fill="none" stroke={BLUE} strokeWidth="4"/><T x={100} y={238} anchor="start" size={13}>DISTURBANCE</T><Arrow x1={170} y1={90} x2={215} y2={170}/><T x={205} y={75} size={14}>RESTORING TENDENCY</T><T x={550} y={258} size={14}>OSCILLATIONS DECAY</T><T x={380} y={40} size={16}>POSITIVE STATIC + POSITIVE DYNAMIC STABILITY</T></svg>
    case "dihedral": return <svg {...common}><T x={380} y={38} size={16}>FRONT VIEW</T><path d="M170 175 L365 120 L395 120 L590 175" fill="none" stroke={NAVY} strokeWidth="7" strokeLinecap="round"/><line x1="380" y1="120" x2="380" y2="220" stroke={NAVY} strokeWidth="5"/><Arrow x1={90} y1={215} x2={250} y2={215} color={GREY}/><T x={115} y={242} anchor="start" size={13}>SIDESLIP</T><Arrow x1={235} y1={170} x2={235} y2={85}/><Arrow x1={525} y1={170} x2={525} y2={120} color={BLUE}/><T x={225} y={68} size={13}>MORE LIFT</T><T x={525} y={104} size={13}>LESS LIFT</T><path d="M320 250 Q380 285 440 250" fill="none" stroke={GOLD} strokeWidth="4"/><T x={380} y={300} size={14}>RESTORING ROLL</T></svg>
    case "cg-stability": return <svg {...common}><path d="M115 168 Q220 118 520 145 L650 165 L520 186 Q230 205 115 168Z" fill="white" stroke={NAVY} strokeWidth="4"/><line x1="250" y1="80" x2="250" y2="235" stroke={GREY} strokeWidth="2" strokeDasharray="6 6"/><line x1="470" y1="80" x2="470" y2="235" stroke={GREY} strokeWidth="2" strokeDasharray="6 6"/><circle cx="300" cy="166" r="10" fill={GOLD}/><T x={300} y={65} size={14}>FORWARD CG</T><circle cx="420" cy="166" r="10" fill={BLUE}/><T x={420} y={255} size={14}>AFT CG</T><T x={250} y={285} size={13}>MORE STABLE</T><Arrow x1={305} y1={280} x2={455} y2={280} color={GREY}/><T x={505} y={285} size={13}>LESS STABLE</T></svg>
    case "aerofoil": return <svg {...common}><path d="M115 165 Q310 60 650 150 Q430 205 115 165Z" fill="white" stroke={NAVY} strokeWidth="4"/><line x1="115" y1="165" x2="650" y2="150" stroke={GREY} strokeWidth="2" strokeDasharray="8 6"/><path d="M115 165 Q350 123 650 150" fill="none" stroke={GOLD} strokeWidth="3"/><T x={380} y={210} size={13}>CHORD LINE</T><T x={390} y={105} size={13}>MEAN CAMBER LINE</T><T x={112} y={190} anchor="start" size={12}>LEADING EDGE</T><T x={655} y={176} anchor="end" size={12}>TRAILING EDGE</T><line x1="345" y1="108" x2="345" y2="181" stroke={BLUE} strokeWidth="3"/><T x={360} y={145} anchor="start" size={12}>THICKNESS</T></svg>
    case "angle-of-attack": return <svg {...common}><line x1="140" y1="205" x2="620" y2="145" stroke={NAVY} strokeWidth="5"/><Arrow x1={625} y1={235} x2={150} y2={235} color={BLUE}/><T x={395} y={263} size={14}>RELATIVE AIRFLOW</T><path d="M210 226 A80 80 0 0 1 225 195" fill="none" stroke={GOLD} strokeWidth="5"/><T x={250} y={193} size={15}>α = ANGLE OF ATTACK</T><T x={495} y={127} size={13}>CHORD LINE</T></svg>
    case "boundary-layer": return <svg {...common}><line x1="80" y1="220" x2="680" y2="220" stroke={NAVY} strokeWidth="5"/><path d="M90 205 C220 205 300 190 380 165" fill="none" stroke={BLUE} strokeWidth="3"/><path d="M380 165 C450 140 485 105 530 140 C575 175 600 105 660 155" fill="none" stroke={BLUE} strokeWidth="3"/><line x1="380" y1="90" x2="380" y2="235" stroke={GOLD} strokeWidth="3" strokeDasharray="6 5"/><T x={230} y={90} size={14}>LAMINAR</T><T x={475} y={90} size={14}>TURBULENT</T><T x={380} y={72} size={13}>TRANSITION</T><T x={590} y={198} size={13} fill={RED}>SEPARATION</T></svg>
    case "bernoulli": return <svg {...common}><path d="M90 110 C250 110 300 75 380 85 C470 95 500 115 670 115" fill="none" stroke={BLUE} strokeWidth="3"/><path d="M90 160 C250 160 300 120 380 125 C470 130 500 160 670 160" fill="none" stroke={BLUE} strokeWidth="3"/><path d="M90 215 C250 215 300 205 380 205 C470 205 500 215 670 215" fill="none" stroke={BLUE} strokeWidth="3"/><path d="M220 190 Q370 85 550 180 Q390 220 220 190Z" fill="white" stroke={NAVY} strokeWidth="4"/><T x={390} y={58} size={14}>FASTER FLOW · LOWER STATIC PRESSURE</T><T x={390} y={270} size={14}>SLOWER FLOW · HIGHER STATIC PRESSURE</T><Arrow x1={130} y1={135} x2={260} y2={135}/></svg>
    case "centre-pressure": return <svg {...common}><path d="M95 170 Q260 80 575 155 Q365 205 95 170Z" fill="white" stroke={NAVY} strokeWidth="4"/><circle cx="300" cy="163" r="9" fill={BLUE}/><Arrow x1={300} y1={160} x2={300} y2={75}/><T x={300} y={55} size={13}>CP AT LOWER α</T><circle cx="380" cy="160" r="9" fill={GOLD}/><Arrow x1={380} y1={158} x2={380} y2={95}/><T x={465} y={90} size={13}>CP POSITION CHANGES</T><Arrow x1={315} y1={235} x2={365} y2={235} color={GREY}/><T x={380} y={265} size={13}>CHORDWISE MOVEMENT</T></svg>
    case "aspect-ratio": return <svg {...common}><rect x="90" y="95" width="250" height="110" rx="55" fill="white" stroke={NAVY} strokeWidth="4"/><rect x="430" y="125" width="250" height="50" rx="25" fill="white" stroke={NAVY} strokeWidth="4"/><T x={215} y={235} size={13}>LOWER ASPECT RATIO</T><T x={555} y={235} size={13}>HIGHER ASPECT RATIO</T><line x1="430" y1="85" x2="680" y2="85" stroke={GOLD} strokeWidth="3"/><T x={555} y={68} size={12}>SPAN</T><line x1="700" y1="125" x2="700" y2="175" stroke={BLUE} strokeWidth="3"/><T x={712} y={155} anchor="start" size={12}>CHORD</T><T x={380} y={286} size={14}>AR = SPAN² / WING AREA</T></svg>
    case "lift-speed": return <svg {...common}><line x1="110" y1="255" x2="650" y2="255" stroke={NAVY} strokeWidth="3"/><line x1="110" y1="255" x2="110" y2="55" stroke={NAVY} strokeWidth="3"/><path d="M120 245 Q300 225 450 155 Q555 105 635 65" fill="none" stroke={GOLD} strokeWidth="5"/><T x={380} y={295} size={13}>AIRSPEED V</T><T x={66} y={155} size={13}>LIFT</T><T x={480} y={115} size={15}>L ∝ V²</T><circle cx="260" cy="218" r="7" fill={BLUE}/><circle cx="410" cy="174" r="7" fill={BLUE}/><T x={335} y={245} size={12}>DOUBLE V → FOUR TIMES LIFT*</T><T x={380} y={316} size={10} fill={GREY}>*if ρ, S and CL are unchanged</T></svg>
    case "drag-curves": return <svg {...common}><line x1="105" y1="255" x2="665" y2="255" stroke={NAVY} strokeWidth="3"/><line x1="105" y1="255" x2="105" y2="55" stroke={NAVY} strokeWidth="3"/><path d="M120 75 Q225 155 355 225 Q430 246 640 250" fill="none" stroke={BLUE} strokeWidth="4"/><path d="M120 248 Q350 245 470 185 Q570 125 645 75" fill="none" stroke={GOLD} strokeWidth="4"/><path d="M120 98 Q330 245 465 188 Q560 145 645 100" fill="none" stroke={NAVY} strokeWidth="5"/><T x={220} y={105} size={12}>INDUCED</T><T x={565} y={78} size={12}>PARASITE</T><T x={470} y={165} size={12}>TOTAL</T><T x={390} y={294} size={13}>AIRSPEED</T><T x={54} y={155} size={13}>DRAG</T></svg>
    case "power-required": return <svg {...common}><line x1="105" y1="255" x2="665" y2="255" stroke={NAVY} strokeWidth="3"/><line x1="105" y1="255" x2="105" y2="55" stroke={NAVY} strokeWidth="3"/><path d="M125 95 Q300 235 410 205 Q535 160 645 70" fill="none" stroke={GOLD} strokeWidth="5"/><line x1="395" y1="205" x2="395" y2="255" stroke={BLUE} strokeWidth="3" strokeDasharray="6 5"/><T x={395} y={190} size={12}>MIN POWER</T><T x={390} y={294} size={13}>AIRSPEED</T><T x={60} y={155} size={13}>POWER</T><T x={520} y={245} size={13}>P = D × V</T></svg>
    case "force-equilibrium": return <svg {...common}><path d="M260 165 L500 165 L555 185 L500 198 L260 198 L205 185Z" fill="white" stroke={NAVY} strokeWidth="4"/><Arrow x1={380} y1={165} x2={380} y2={60}/><T x={395} y={72} anchor="start" size={13}>LIFT</T><Arrow x1={380} y1={198} x2={380} y2={295} color={BLUE}/><T x={395} y={285} anchor="start" size={13}>WEIGHT</T><Arrow x1={500} y1={182} x2={670} y2={182}/><T x={610} y={166} size={13}>THRUST</T><Arrow x1={260} y1={182} x2={90} y2={182} color={BLUE}/><T x={145} y={166} size={13}>DRAG</T></svg>
    case "flap-types": return <svg {...common}><T x={190} y={45} size={14}>CLEAN</T><path d="M75 110 Q190 70 310 105 Q190 135 75 110Z" fill="white" stroke={NAVY} strokeWidth="3"/><T x={570} y={45} size={14}>FLAP EXTENDED</T><path d="M430 110 Q545 70 665 105 Q555 135 430 110Z" fill="white" stroke={NAVY} strokeWidth="3"/><path d="M590 108 L690 148" fill="none" stroke={GOLD} strokeWidth="8"/><Arrow x1={545} y1={235} x2={545} y2={145}/><T x={545} y={270} size={13}>CAMBER ↑ · CLmax ↑ · DRAG ↑</T></svg>
    case "slat": return <svg {...common}><path d="M180 185 Q360 80 610 165 Q400 215 180 185Z" fill="white" stroke={NAVY} strokeWidth="4"/><path d="M145 177 Q170 130 210 133" fill="none" stroke={GOLD} strokeWidth="12" strokeLinecap="round"/><Arrow x1={95} y1={130} x2={220} y2={152} color={BLUE}/><Arrow x1={220} y1={152} x2={350} y2={116} color={BLUE}/><T x={185} y={95} size={14}>ENERGISED AIR THROUGH SLOT</T><T x={480} y={260} size={13}>SEPARATION DELAYED TO HIGHER α</T></svg>
    case "ground-effect": return <svg {...common}><line x1="70" y1="250" x2="690" y2="250" stroke={NAVY} strokeWidth="5"/><T x={650} y={277} size={12}>GROUND</T><path d="M250 125 L510 125 L560 145 L510 160 L250 160 L200 145Z" fill="white" stroke={NAVY} strokeWidth="4"/><path d="M245 175 Q190 220 145 215" fill="none" stroke={BLUE} strokeWidth="4"/><path d="M515 175 Q570 220 615 215" fill="none" stroke={BLUE} strokeWidth="4"/><Arrow x1={380} y1={205} x2={380} y2={170}/><T x={380} y={65} size={15}>WING CLOSE TO SURFACE</T><T x={380} y={300} size={14}>DOWNWASH ↓ · WINGTIP VORTICES ↓ · INDUCED DRAG ↓</T></svg>
    case "differential-ailerons": return <svg {...common}><line x1="100" y1="155" x2="660" y2="155" stroke={NAVY} strokeWidth="8"/><line x1="100" y1="155" x2="180" y2="105" stroke={GOLD} strokeWidth="9"/><line x1="580" y1="155" x2="660" y2="180" stroke={GOLD} strokeWidth="9"/><T x={140} y={82} size={13}>UP MORE</T><T x={620} y={213} size={13}>DOWN LESS</T><Arrow x1={380} y1={245} x2={275} y2={245} color={GREY}/><T x={470} y={250} size={13}>ADVERSE YAW REDUCED</T></svg>
    case "asymmetric-flap": return <svg {...common}><line x1="100" y1="145" x2="660" y2="145" stroke={NAVY} strokeWidth="8"/><line x1="100" y1="145" x2="190" y2="195" stroke={GOLD} strokeWidth="10"/><line x1="570" y1="145" x2="660" y2="145" stroke={GREY} strokeWidth="10"/><Arrow x1={175} y1={215} x2={175} y2={95}/><Arrow x1={585} y1={215} x2={585} y2={150} color={BLUE}/><T x={175} y={78} size={13}>MORE LIFT + DRAG</T><T x={585} y={132} size={13}>LESS</T><path d="M300 250 Q380 290 460 250" fill="none" stroke={RED} strokeWidth="5"/><T x={380} y={304} size={14} fill={RED}>ROLL / YAW TENDENCY</T></svg>
    case "bank-load-factor": return <svg {...common}><path d="M140 245 A240 240 0 0 1 620 245" fill="none" stroke={LIGHT} strokeWidth="3"/><line x1="140" y1="245" x2="620" y2="245" stroke={NAVY} strokeWidth="3"/><line x1="380" y1="245" x2="380" y2="65" stroke={GREY} strokeWidth="2" strokeDasharray="6 5"/><line x1="380" y1="245" x2="535" y2="155" stroke={BLUE} strokeWidth="5"/><path d="M430 245 A50 50 0 0 0 405 202" fill="none" stroke={GOLD} strokeWidth="4"/><T x={450} y={218} size={14}>60°</T><Arrow x1={535} y1={155} x2={535} y2={75}/><T x={580} y={70} size={15}>n ≈ 2 G</T><T x={380} y={294} size={14}>n = 1 / cos φ</T></svg>
    case "turn-forces": return <svg {...common}><line x1="125" y1="245" x2="635" y2="245" stroke={LIGHT} strokeWidth="2"/><circle cx="380" cy="185" r="8" fill={NAVY}/><Arrow x1={380} y1={185} x2={505} y2={70}/><T x={520} y={66} anchor="start" size={13}>TOTAL LIFT</T><Arrow x1={380} y1={185} x2={380} y2={65} color={BLUE}/><T x={365} y={55} anchor="end" size={12}>VERTICAL COMPONENT</T><Arrow x1={380} y1={185} x2={505} y2={185}/><T x={520} y={190} anchor="start" size={12}>CENTRIPETAL</T><Arrow x1={380} y1={185} x2={380} y2={285} color={GREY}/><T x={395} y={282} anchor="start" size={12}>WEIGHT</T></svg>
    case "stall-speed-load": return <svg {...common}><line x1="110" y1="255" x2="650" y2="255" stroke={NAVY} strokeWidth="3"/><line x1="110" y1="255" x2="110" y2="55" stroke={NAVY} strokeWidth="3"/><path d="M130 230 Q300 200 430 145 Q545 95 635 70" fill="none" stroke={GOLD} strokeWidth="5"/><T x={410} y={110} size={15}>Vs ∝ √n</T><line x1="450" y1="145" x2="450" y2="255" stroke={BLUE} strokeWidth="2" strokeDasharray="6 5"/><T x={450} y={280} size={12}>2 G</T><T x={60} y={155} size={12}>STALL SPEED</T><T x={380} y={305} size={13}>LOAD FACTOR n</T></svg>
    case "turn-radius": return <svg {...common}><circle cx="380" cy="165" r="115" fill="none" stroke={LIGHT} strokeWidth="4"/><circle cx="380" cy="165" r="7" fill={NAVY}/><line x1="380" y1="165" x2="485" y2="115" stroke={GREY} strokeWidth="3"/><T x={445} y={156} size={13}>RADIUS</T><Arrow x1={485} y1={115} x2={555} y2={155}/><T x={575} y={158} anchor="start" size={13}>VELOCITY</T><T x={380} y={305} size={14}>R ∝ V² / tan φ</T></svg>
    case "rolling-moment": return <svg {...common}><line x1="110" y1="160" x2="650" y2="160" stroke={NAVY} strokeWidth="8"/><Arrow x1={200} y1={160} x2={200} y2={70}/><Arrow x1={560} y1={160} x2={560} y2={115} color={BLUE}/><T x={200} y={55} size={13}>LIFT 1</T><T x={560} y={100} size={13}>LIFT 2</T><path d="M300 240 Q380 285 460 240" fill="none" stroke={GOLD} strokeWidth="5"/><T x={380} y={300} size={14}>UNEQUAL LIFT → ROLLING MOMENT</T></svg>
    case "propeller-pitch": return <svg {...common}><line x1="80" y1="225" x2="330" y2="225" stroke={GREY} strokeWidth="2"/><line x1="150" y1="210" x2="280" y2="145" stroke={GOLD} strokeWidth="10" strokeLinecap="round"/><path d="M205 225 A55 55 0 0 0 195 190" fill="none" stroke={NAVY} strokeWidth="3"/><T x={205} y={125} size={14}>FINE PITCH</T><line x1="430" y1="225" x2="680" y2="225" stroke={GREY} strokeWidth="2"/><line x1="500" y1="200" x2="600" y2="105" stroke={GOLD} strokeWidth="10" strokeLinecap="round"/><path d="M555 225 A70 70 0 0 0 520 170" fill="none" stroke={NAVY} strokeWidth="3"/><T x={555} y={80} size={14}>COARSE PITCH</T><T x={380} y={292} size={13}>BLADE ANGLE MEASURED TO PLANE OF ROTATION</T></svg>
    case "propeller-twist": return <svg {...common}><path d="M165 255 Q250 160 360 65" fill="none" stroke={NAVY} strokeWidth="16" strokeLinecap="round"/><line x1="170" y1="245" x2="225" y2="195" stroke={GOLD} strokeWidth="8"/><line x1="255" y1="175" x2="310" y2="140" stroke={GOLD} strokeWidth="8"/><line x1="330" y1="95" x2="365" y2="82" stroke={GOLD} strokeWidth="8"/><T x={150} y={285} size={13}>ROOT: HIGHER BLADE ANGLE</T><T x={520} y={90} size={13}>TIP: LOWER BLADE ANGLE</T><Arrow x1={400} y1={235} x2={620} y2={235} color={BLUE}/><T x={510} y={270} size={13}>ROTATIONAL SPEED ↑ TOWARD TIP</T></svg>
    case "constant-speed-unit": return <svg {...common}><rect x="75" y="110" width="160" height="90" rx="6" fill="white" stroke={NAVY} strokeWidth="3"/><T x={155} y={145} size={13}>RPM ERROR</T><T x={155} y={170} size={12}>selected vs actual</T><Arrow x1={235} y1={155} x2={320} y2={155}/><rect x="320" y="110" width="150" height="90" rx="6" fill="white" stroke={NAVY} strokeWidth="3"/><T x={395} y={145} size={13}>GOVERNOR</T><T x={395} y={170} size={12}>oil control</T><Arrow x1={470} y1={155} x2={555} y2={155}/><rect x="555" y="110" width="135" height="90" rx="6" fill="white" stroke={NAVY} strokeWidth="3"/><T x={622} y={145} size={13}>BLADE</T><T x={622} y={170} size={12}>ANGLE</T><Arrow x1={620} y1={215} x2={250} y2={245} color={BLUE}/><T x={430} y={278} size={13}>FEEDBACK OPPOSES RPM CHANGE</T></svg>
    case "propeller-thrust": return <svg {...common}><ellipse cx="380" cy="160" rx="20" ry="120" fill="none" stroke={NAVY} strokeWidth="6"/><Arrow x1={330} y1={95} x2={150} y2={95} color={GOLD}/><Arrow x1={330} y1={160} x2={120} y2={160} color={GOLD}/><Arrow x1={330} y1={225} x2={150} y2={225} color={GOLD}/><Arrow x1={430} y1={160} x2={620} y2={160} color={BLUE}/><T x={205} y={75} size={13}>AIR ACCELERATED REARWARD</T><T x={555} y={142} size={14}>THRUST</T><T x={380} y={300} size={13}>ACTION ON AIR ↔ REACTION ON PROPELLER</T></svg>
    case "p-factor": return <svg {...common}><circle cx="380" cy="160" r="125" fill="none" stroke={LIGHT} strokeWidth="3"/><line x1="380" y1="35" x2="380" y2="285" stroke={NAVY} strokeWidth="8"/><Arrow x1={505} y1={95} x2={585} y2={95}/><Arrow x1={255} y1={225} x2={300} y2={225} color={BLUE}/><T x={545} y={72} size={13}>DESCENDING BLADE</T><T x={545} y={118} size={12}>MORE THRUST</T><T x={230} y={252} size={12}>ASCENDING BLADE</T><Arrow x1={380} y1={300} x2={300} y2={300} color={GOLD}/><T x={455} y={305} size={13}>YAWING MOMENT</T></svg>
    case "v-speeds": return <svg {...common}><line x1="180" y1="255" x2="580" y2="255" stroke={NAVY} strokeWidth="8"/><line x1="245" y1="240" x2="245" y2="270" stroke={BLUE} strokeWidth="4"/><T x={245} y={225} size={12}>VS0</T><line x1="340" y1="240" x2="340" y2="270" stroke={BLUE} strokeWidth="4"/><T x={340} y={225} size={12}>VFE</T><line x1="425" y1="240" x2="425" y2="270" stroke={GOLD} strokeWidth="4"/><T x={425} y={225} size={12}>VNO</T><line x1="540" y1="235" x2="540" y2="275" stroke={RED} strokeWidth="5"/><T x={540} y={220} size={12} fill={RED}>VNE</T><T x={380} y={300} size={13}>INDICATED AIRSPEED →</T><rect x="110" y="70" width="540" height="85" rx="6" fill="#f8fafc" stroke={LIGHT}/><T x={380} y={105} size={13}>OTHER KEY SPEEDS: VR · VX · VY · VA</T><T x={380} y={132} size={12} fill={GREY}>USE AIRCRAFT-SPECIFIC AFM / POH VALUES</T></svg>
    case "va-weight": return <svg {...common}><line x1="110" y1="250" x2="650" y2="250" stroke={NAVY} strokeWidth="3"/><line x1="110" y1="250" x2="110" y2="55" stroke={NAVY} strokeWidth="3"/><line x1="150" y1="215" x2="620" y2="85" stroke={GOLD} strokeWidth="5"/><T x={515} y={70} size={14}>HIGHER WEIGHT → HIGHER VA</T><T x={380} y={292} size={13}>AIRCRAFT WEIGHT</T><T x={72} y={155} size={13}>VA</T></svg>
    case "vx-vy": return <svg {...common}><line x1="80" y1="255" x2="680" y2="255" stroke={NAVY} strokeWidth="3"/><path d="M120 255 L395 80" fill="none" stroke={GOLD} strokeWidth="5"/><path d="M120 255 Q395 205 650 80" fill="none" stroke={BLUE} strokeWidth="5"/><T x={330} y={100} size={14}>VX</T><T x={550} y={120} size={14}>VY</T><T x={260} y={220} size={12}>BEST ANGLE / DISTANCE</T><T x={545} y={235} size={12}>BEST RATE / TIME</T></svg>
    case "critical-aoa": return <svg {...common}><Arrow x1={650} y1={235} x2={130} y2={235} color={BLUE}/><line x1="175" y1="205" x2="590" y2="120" stroke={NAVY} strokeWidth="6"/><path d="M180 210 A70 70 0 0 1 205 187" fill="none" stroke={GOLD} strokeWidth="5"/><T x={250} y={182} size={14}>αCRIT</T><path d="M300 120 C390 80 470 92 555 130" fill="none" stroke={RED} strokeWidth="4" strokeDasharray="9 6"/><T x={455} y={72} size={13} fill={RED}>SEPARATED FLOW</T><T x={380} y={290} size={14}>STALL WHEN α &gt; αCRIT</T></svg>
    case "stall-progression": return <svg {...common}><path d="M100 120 L660 120 L590 200 L170 200Z" fill="white" stroke={NAVY} strokeWidth="4"/><rect x="305" y="120" width="150" height="80" fill="#fef3c7"/><line x1="380" y1="100" x2="380" y2="220" stroke={NAVY} strokeWidth="4"/><T x={380} y={85} size={13}>FUSELAGE / ROOT</T><T x={380} y={165} size={14}>STALL FIRST</T><T x={145} y={230} size={12}>TIP RETAINS FLOW</T><T x={615} y={230} size={12}>TIP RETAINS FLOW</T><T x={380} y={285} size={13}>ROOT-FIRST STALL PRESERVES AILERON CONTROL LONGER</T></svg>
    case "stall-recovery": return <svg {...common}><circle cx="120" cy="145" r="35" fill="white" stroke={NAVY} strokeWidth="3"/><T x={120} y={151} size={18}>1</T><Arrow x1={160} y1={145} x2={280} y2={145}/><circle cx="340" cy="145" r="35" fill="white" stroke={NAVY} strokeWidth="3"/><T x={340} y={151} size={18}>2</T><Arrow x1={380} y1={145} x2={500} y2={145}/><circle cx="560" cy="145" r="35" fill="white" stroke={NAVY} strokeWidth="3"/><T x={560} y={151} size={18}>3</T><T x={120} y={210} size={12}>REDUCE α</T><T x={340} y={210} size={12}>POWER AS REQUIRED</T><T x={560} y={210} size={12}>LEVEL + RECOVER</T><T x={380} y={278} size={13}>UNSTALL THE WING FIRST</T></svg>
    case "spin": return <svg {...common}><path d="M380 60 C520 90 535 180 430 190 C320 200 275 125 360 105 C445 85 480 155 405 165 C340 173 330 130 375 125" fill="none" stroke={GOLD} strokeWidth="5"/><Arrow x1={410} y1={182} x2={395} y2={245} color={BLUE}/><T x={530} y={95} size={13}>YAW + STALL</T><T x={440} y={260} size={13}>DESCENDING AUTOROTATION</T><line x1="375" y1="125" x2="435" y2="150" stroke={NAVY} strokeWidth="9"/><T x={185} y={285} size={12}>WINGS STALLED UNEQUALLY</T></svg>
    case "propwash": return <svg {...common}><ellipse cx="190" cy="160" rx="16" ry="100" fill="none" stroke={NAVY} strokeWidth="5"/><path d="M220 85 Q390 115 610 125" fill="none" stroke={BLUE} strokeWidth="3"/><path d="M220 235 Q390 205 610 195" fill="none" stroke={BLUE} strokeWidth="3"/><path d="M470 150 L650 150 L690 170 L650 188 L470 188Z" fill="white" stroke={NAVY} strokeWidth="4"/><Arrow x1={240} y1={160} x2={430} y2={160}/><T x={330} y={140} size={13}>SLIPSTREAM</T><T x={565} y={235} size={13}>TAIL / INNER WING IN ENERGISED FLOW</T></svg>
    case "density-performance": return <svg {...common}><rect x="80" y="80" width="250" height="155" rx="6" fill="white" stroke={NAVY} strokeWidth="3"/><T x={205} y={112} size={14}>DENSER AIR</T>{[0,1,2,3,4,5].map(i=><circle key={`d${i}`} cx={125+(i%3)*75} cy={150+Math.floor(i/3)*50} r="8" fill={BLUE}/>) }<rect x="430" y="80" width="250" height="155" rx="6" fill="white" stroke={NAVY} strokeWidth="3"/><T x={555} y={112} size={14}>LESS DENSE AIR</T>{[0,1,2].map(i=><circle key={`l${i}`} cx={480+i*75} cy={170} r="8" fill={GOLD}/>) }<T x={205} y={270} size={12}>SHORTER ROLL · BETTER CLIMB</T><T x={555} y={270} size={12}>LONGER ROLL · LOWER CLIMB</T></svg>
    case "wind-runway": return <svg {...common}><rect x="140" y="130" width="480" height="70" fill="#f8fafc" stroke={NAVY} strokeWidth="3"/><line x1="380" y1="130" x2="380" y2="200" stroke={LIGHT} strokeWidth="3" strokeDasharray="12 10"/><Arrow x1={90} y1={100} x2={270} y2={100}/><T x={180} y={78} size={13}>HEADWIND</T><Arrow x1={670} y1={235} x2={490} y2={235} color={RED}/><T x={580} y={265} size={13} fill={RED}>TAILWIND</T><T x={380} y={235} size={13}>RUNWAY</T><T x={380} y={300} size={13}>HEADWIND ↓ GROUND SPEED / DISTANCE · TAILWIND ↑</T></svg>
    case "soft-field": return <svg {...common}><line x1="70" y1="245" x2="690" y2="245" stroke={NAVY} strokeWidth="4"/><path d="M145 210 Q260 205 330 180" fill="none" stroke={BLUE} strokeWidth="4"/><path d="M330 180 Q445 165 560 135" fill="none" stroke={GOLD} strokeWidth="5"/><T x={210} y={195} size={12}>NOSE LIGHT · KEEP ROLLING</T><T x={390} y={150} size={12}>EARLY LIFT-OFF</T><T x={555} y={115} size={12}>ACCELERATE IN GROUND EFFECT</T><T x={380} y={292} size={13}>MINIMISE WHEEL DRAG ON SOFT SURFACE</T></svg>
    case "short-field": return <svg {...common}><line x1="65" y1="250" x2="695" y2="250" stroke={NAVY} strokeWidth="4"/><rect x="590" y="130" width="22" height="120" fill={GREY}/><T x={600} y={112} size={12}>OBSTACLE</T><path d="M110 240 Q250 235 330 205 Q455 160 575 95" fill="none" stroke={GOLD} strokeWidth="5"/><T x={220} y={215} size={12}>MAX ACCELERATION</T><T x={470} y={130} size={12}>TARGET VX TO CLEAR OBSTACLE</T><T x={380} y={295} size={13}>USE AFM SHORT-FIELD CONFIGURATION + SPEED</T></svg>
    case "climb-gradient": return <svg {...common}><line x1="140" y1="245" x2="630" y2="245" stroke={NAVY} strokeWidth="4"/><line x1="630" y1="245" x2="630" y2="80" stroke={BLUE} strokeWidth="4"/><line x1="140" y1="245" x2="630" y2="80" stroke={GOLD} strokeWidth="5"/><T x={380} y={270} size={12}>HORIZONTAL DISTANCE</T><T x={650} y={165} anchor="start" size={12}>HEIGHT</T><T x={380} y={65} size={14}>GRADIENT = HEIGHT GAIN / HORIZONTAL DISTANCE × 100%</T></svg>
  }
}

export function PrinciplesOfFlightVisual({ question }: { question: Question }) {
  const spec = getSpec(question)

  return (
    <figure className="mt-5 overflow-hidden border border-slate-200 bg-white">
      <div className="bg-[#06111f] px-4 py-4 text-center sm:px-6 sm:py-5">
        <div className="text-[11px] font-extrabold tracking-[0.24em] text-[#f4b400] sm:text-xs">
          PILOTVAULT PRINCIPLES OF FLIGHT
        </div>
        <div className="mt-1 text-lg font-extrabold uppercase tracking-[0.025em] text-white sm:text-2xl">
          {spec.title}
        </div>
      </div>

      <div className="bg-[#f8fafc] p-3 sm:p-5">
        <div className="mx-auto max-w-4xl border border-slate-200 bg-white px-2 py-3 sm:px-4 sm:py-4">
          <TechnicalDiagram concept={spec.concept} />
          <div className="mx-auto mt-2 max-w-3xl border-t border-slate-200 px-3 pt-3 text-center text-sm leading-relaxed text-slate-700">
            {spec.note}
          </div>
        </div>
      </div>
    </figure>
  )
}
