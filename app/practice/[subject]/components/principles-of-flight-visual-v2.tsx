"use client"

import type { ReactNode } from "react"
import type { Question } from "../types"

type Concept =
  | "wing-polar"
  | "axes-controls"
  | "control-effects"
  | "stability"
  | "dihedral"
  | "directional-stability"
  | "longitudinal-dihedral"
  | "cg-stability"
  | "cg-cp"
  | "aerofoil"
  | "angle-of-attack"
  | "incidence-washout"
  | "boundary-layer"
  | "bernoulli"
  | "newton-laws"
  | "dynamic-pressure"
  | "lift-pressure"
  | "centre-pressure"
  | "aspect-ratio"
  | "lift-speed"
  | "drag-curves"
  | "skin-friction"
  | "induced-drag"
  | "four-forces"
  | "climb-forces"
  | "descent-power"
  | "flap-effects"
  | "fowler-flap"
  | "slat"
  | "glide-flap"
  | "glide-wind"
  | "adverse-yaw"
  | "trim-tab"
  | "balance-tab"
  | "anti-balance-tab"
  | "mass-balance"
  | "horn-balance"
  | "flutter"
  | "bank-load-factor"
  | "turn-forces"
  | "slip-skid"
  | "stall-speed-load"
  | "critical-aoa"
  | "stall-warning"
  | "stall-progression"
  | "spin"
  | "spin-recovery"
  | "airspeed-chain"
  | "v-speeds"
  | "va"
  | "vx-vy"
  | "isa"
  | "humidity-density"
  | "pressure-temp-density"
  | "propeller-effects"
  | "weight-cg"

type Spec = { concept: Concept; title: string; note: string }

const NAVY = "#06111f"
const GOLD = "#f4b400"
const BLUE = "#1f4e79"
const GREY = "#64748b"
const LIGHT = "#d7e0ea"
const PALE = "#f8fafc"
const RED = "#b91c1c"
const GREEN = "#166534"

function text(question: Question) {
  return `${question.question} ${question.correctAnswer}`.toLowerCase()
}

function has(question: Question, ...terms: string[]) {
  const value = text(question)
  return terms.some((term) => value.includes(term.toLowerCase()))
}

function getSpec(question: Question): Spec {
  const topic = question.topic ?? ""

  if (has(question, "wing polar", "polar diagram")) return { concept: "wing-polar", title: "READING A WING POLAR", note: "Use the supplied polar to identify the marked operating point. The critical angle of attack occurs at CLmax; minimum drag and best L/D occur at different points unless the figure shows otherwise." }

  if (topic === "Trim & Balance Tabs") {
    if (has(question, "anti-balance", "anti-servo")) return { concept: "anti-balance-tab", title: "ANTI-BALANCE / ANTI-SERVO TAB", note: "An anti-balance tab moves in the same direction as the main surface, increasing control force and feel." }
    if (has(question, "mass balance", "flutter")) return { concept: has(question, "flutter") ? "flutter" : "mass-balance", title: has(question, "flutter") ? "CONTROL FLUTTER" : "MASS BALANCE", note: has(question, "flutter") ? "Flutter is a self-excited aeroelastic oscillation. Correct mass balance and approved structural condition are critical to preventing it." : "A mass balance places mass ahead of the hinge line to reduce the tendency of a control surface to flutter." }
    if (has(question, "horn balance", "hinge set back", "aerodynamically balanced")) return { concept: "horn-balance", title: "AERODYNAMIC / HORN BALANCE", note: "Placing part of the control area ahead of the hinge line reduces the hinge moment and therefore pilot control force." }
    if (has(question, "balance tab")) return { concept: "balance-tab", title: "BALANCE TAB MOVEMENT", note: "A balance tab moves opposite to the main control surface so aerodynamic force on the tab assists movement of the main surface." }
    return { concept: "trim-tab", title: "TRIM TAB PRINCIPLE", note: "A trim tab is set relative to the control surface to remove sustained pilot force while the main surface finds the position required for the trimmed condition." }
  }

  if (topic === "Flight Controls & Axes") {
    if (has(question, "primary and further", "followed by spiral", "further effects")) return { concept: "control-effects", title: "PRIMARY & FURTHER CONTROL EFFECTS", note: "A control first produces its primary rotation; aerodynamic coupling can then produce secondary motion and, if uncorrected, a spiral tendency." }
    return { concept: "axes-controls", title: "AIRCRAFT AXES & PRIMARY CONTROLS", note: "Roll is about the longitudinal axis and controlled by ailerons; pitch is about the lateral axis and controlled by elevator; yaw is about the vertical axis and controlled by rudder." }
  }

  if (topic === "Aileron Drag") return { concept: "adverse-yaw", title: "ADVERSE AILERON YAW", note: "The down-going aileron increases lift and induced drag on its wing, tending to yaw the aircraft opposite the intended roll. Differential or Frise ailerons help reduce this effect." }

  if (topic === "Stability") {
    if (has(question, "dihedral", "sideslip", "lower wing")) return { concept: "dihedral", title: "DIHEDRAL & LATERAL STABILITY", note: "In a sideslip, dihedral gives the lower wing a greater effective angle of attack, creating a restoring rolling moment." }
    if (has(question, "vertical fin", "directional stability", "yawing plane", "keel surface")) return { concept: "directional-stability", title: "DIRECTIONAL STABILITY", note: "Side area behind the centre of gravity, especially the vertical fin, produces a weathercock restoring moment after a yaw disturbance." }
    if (has(question, "longitudinal dihedral", "tailplane", "pitching plane")) return { concept: "longitudinal-dihedral", title: "LONGITUDINAL DIHEDRAL & PITCH STABILITY", note: "The incidence relationship between wing and tailplane contributes to a restoring pitching moment after a disturbance." }
    if (has(question, "centre of gravity", "center of gravity", "cg ", " c.g", "forward limit", "aft limit")) return { concept: "cg-stability", title: "CENTRE OF GRAVITY & STABILITY", note: "A forward CG normally increases longitudinal stability and control force; an aft CG reduces the stability margin and can reduce spin recovery effectiveness." }
    return { concept: "stability", title: "STATIC & DYNAMIC STABILITY", note: "Static stability describes the initial tendency after a disturbance; dynamic stability describes how the motion changes with time." }
  }

  if (topic === "Four Forces") {
    if (has(question, "centre of gravity", "center of gravity", "centre of pressure", "center of pressure", "power causes", "nose pitches")) return { concept: "cg-cp", title: "CG, CENTRE OF PRESSURE & PITCHING MOMENTS", note: "In a conventional light aircraft the CG is normally ahead of the centre of pressure. Changes in the force couples can therefore create a pitching moment." }
    return { concept: "four-forces", title: "FOUR FORCES IN LEVEL FLIGHT", note: "In steady straight-and-level flight at constant speed, lift equals weight and thrust equals drag." }
  }

  if (topic === "Aerofoils & Lift") {
    if (has(question, "boundary layer", "laminar", "turbulent", "transition point")) return { concept: "boundary-layer", title: "BOUNDARY LAYER & TRANSITION", note: "The boundary layer begins at the surface, may transition from laminar to turbulent flow, and can eventually separate under an adverse pressure gradient." }
    if (has(question, "centre of pressure", "center of pressure")) return { concept: "centre-pressure", title: "CENTRE OF PRESSURE", note: "The centre of pressure is the point through which the resultant aerodynamic force is treated as acting; its position changes with angle of attack on a conventional aerofoil." }
    if (has(question, "angle of attack", "relative airflow", "relative air flow")) return { concept: "angle-of-attack", title: "ANGLE OF ATTACK", note: "Angle of attack is the acute angle between the chord line and the relative airflow. The airflow direction is opposite the aircraft's motion through the air mass." }
    if (has(question, "chord line", "camber", "aerofoil", "airfoil")) return { concept: "aerofoil", title: "AEROFOIL GEOMETRY", note: "The chord line joins the leading and trailing edges. Camber and thickness describe the shape of the aerofoil around that reference line." }
    if (has(question, "doubled", "four times", "airspeed", "v squared", "v²")) return { concept: "lift-speed", title: "LIFT & AIRSPEED SQUARED", note: "With density, wing area and lift coefficient unchanged, lift varies with the square of true airspeed: L ∝ V²." }
    return { concept: "lift-pressure", title: "LIFT, PRESSURE & RELATIVE AIRFLOW", note: "The resultant lift force acts perpendicular to the relative airflow and is produced by the pressure distribution around the aerofoil." }
  }

  if (topic === "Basic Aerodynamics") {
    if (has(question, "newton")) return { concept: "newton-laws", title: "NEWTON'S LAWS IN FLIGHT", note: "First law: inertia/equilibrium. Second law: force produces acceleration. Third law: every action has an equal and opposite reaction." }
    if (has(question, "venturi", "bernoulli", "continuity", "cross-sectional area")) return { concept: "bernoulli", title: "VENTURI: CONTINUITY & BERNOULLI", note: "For steady subsonic flow through a narrowing passage, velocity increases while static pressure decreases; mass flow remains constant." }
    if (has(question, "dynamic pressure", "total pressure", "static pressure", "q =", "q=")) return { concept: "dynamic-pressure", title: "STATIC, DYNAMIC & TOTAL PRESSURE", note: "Dynamic pressure q = ½ρV². At a stagnation point, total pressure equals static pressure plus dynamic pressure." }
    if (has(question, "relative airflow")) return { concept: "angle-of-attack", title: "RELATIVE AIRFLOW", note: "Relative airflow is parallel and opposite to the aircraft's flight path through the surrounding air mass." }
    if (has(question, "torque", "asymmetric blade", "right rudder", "p-factor")) return { concept: "propeller-effects", title: "PROPELLER ASYMMETRIC EFFECTS", note: "Torque reaction tends to roll the aircraft opposite propeller rotation, while asymmetric blade effect at high power and angle of attack can create yaw." }
    if (has(question, "laminar", "boundary layer")) return { concept: "boundary-layer", title: "LAMINAR & TURBULENT FLOW", note: "Laminar flow is orderly with smooth streamlines; a real boundary layer can contain both laminar and turbulent regions." }
    return { concept: "dynamic-pressure", title: "AIRFLOW ENERGY & PRESSURE", note: "Aerodynamic forces arise from air mass, pressure and motion. Dynamic pressure is the kinetic-pressure term used throughout the lift and drag equations." }
  }

  if (topic === "Drag") {
    if (has(question, "skin friction", "dust", "viscosity")) return { concept: "skin-friction", title: "SKIN-FRICTION DRAG", note: "Air viscosity slows the airflow immediately adjacent to the surface. Surface roughness and wetted area increase this component of parasite drag." }
    if (has(question, "washout", "wingtip", "pressure difference", "induced drag")) return { concept: "induced-drag", title: "INDUCED DRAG & WINGTIP FLOW", note: "Pressure difference between the lower and upper wing drives spanwise flow and wingtip vortices. Induced drag is greatest when high lift is required at low speed." }
    if (has(question, "aspect ratio", "low aspect", "high aspect", "planform")) return { concept: "aspect-ratio", title: "ASPECT RATIO & INDUCED DRAG", note: "For comparable lift, a higher aspect-ratio wing generally produces less induced drag than a lower aspect-ratio wing." }
    return { concept: "drag-curves", title: "INDUCED, PARASITE & TOTAL DRAG", note: "Induced drag falls as speed increases; parasite drag rises rapidly with speed. Their sum gives the total-drag curve and its minimum-drag speed." }
  }

  if (topic === "Wing Design") {
    if (has(question, "aspect ratio")) return { concept: "aspect-ratio", title: "WING ASPECT RATIO", note: "Aspect ratio compares span with mean chord. Higher aspect ratio generally reduces induced drag for a given lift." }
    return { concept: "incidence-washout", title: "INCIDENCE, WASHOUT & ANHEDRAL", note: "Angle of incidence is measured between chord and the aircraft longitudinal reference. Washout reduces incidence toward the tip; anhedral slopes the wings downward from root to tip." }
  }

  if (topic === "Flaps & Glide") {
    if (has(question, "fowler")) return { concept: "fowler-flap", title: "FOWLER FLAP", note: "A Fowler flap moves aft and then down, increasing wing area as well as camber." }
    if (has(question, "slot", "leading-edge")) return { concept: "slat", title: "LEADING-EDGE SLOT", note: "The slot allows higher-energy air to reach the upper surface, delaying separation and permitting a higher usable angle of attack." }
    if (has(question, "headwind", "tailwind", "ground glide")) return { concept: "glide-wind", title: "WIND EFFECT ON GLIDE OVER THE GROUND", note: "Wind changes the glide path over the ground by changing groundspeed; for the same configuration and airspeed it does not directly change the rate of descent through the air mass." }
    if (has(question, "glide", "l/d", "lift/drag", "rate of descent", "gliding angle")) return { concept: "glide-flap", title: "GLIDE PATH & FLAP EFFECT", note: "Extending flap normally reduces best L/D, steepens the glide path and increases rate of descent at the relevant glide condition." }
    return { concept: "flap-effects", title: "TRAILING-EDGE FLAP EFFECTS", note: "Trailing-edge flaps increase camber and CLmax but also increase drag. The required angle of attack for a given lift is reduced after flap extension." }
  }

  if (topic === "Climb Performance") {
    if (has(question, "best angle", "best rate", "vx", "vy", "shortest distance", "shortest time")) return { concept: "vx-vy", title: "VX & VY", note: "VX gives the greatest height gain per horizontal distance; VY gives the greatest height gain per unit time." }
    return { concept: "climb-forces", title: "FORCES IN A STEADY CLIMB", note: "In a steady climb at constant speed, thrust exceeds drag while lift is less than weight because part of the weight acts along the flight path." }
  }

  if (topic === "Descent Performance") return { concept: "descent-power", title: "POWER & RATE OF DESCENT", note: "At constant airspeed, increasing power reduces the required rate of descent; reducing power increases it." }

  if (topic === "Turns & Load Factor") {
    if (has(question, "ball", "slipping", "skidding", "slip indicator")) return { concept: "slip-skid", title: "BALANCED, SLIPPING & SKIDDING TURNS", note: "Ball centred indicates a coordinated turn. In a left turn, ball left indicates a slip and ball right indicates a skid." }
    if (has(question, "stall speed", "stalls at", "square root", "wing loading", "minimum speed")) return { concept: "stall-speed-load", title: "STALL SPEED & LOAD FACTOR", note: "For unchanged configuration and weight, stall speed varies with the square root of load factor: Vs₂ = Vs₁√n." }
    if (has(question, "60", "load factor", "bank angle", "gross weight", "structure support", "2.5 g", "3.8 g")) return { concept: "bank-load-factor", title: "BANK ANGLE & LOAD FACTOR", note: "In a coordinated level turn, n = 1/cosφ. The load factor rises rapidly beyond about 45° of bank and equals 2 G at 60°." }
    return { concept: "turn-forces", title: "LIFT COMPONENTS IN A LEVEL TURN", note: "The vertical component of lift balances weight while the horizontal component provides centripetal force. Maintaining altitude requires greater total lift." }
  }

  if (topic === "Stalls") {
    if (has(question, "warning", "buffeting", "control effectiveness")) return { concept: "stall-warning", title: "STALL APPROACH & WARNING", note: "As the critical angle is approached, control effectiveness reduces and buffet or the installed warning system should provide warning before the full stall." }
    if (has(question, "washout", "wingtip", "root")) return { concept: "stall-progression", title: "ROOT-FIRST STALL PROGRESSION", note: "Washout reduces incidence toward the wingtip so the root reaches the stall first, preserving aileron effectiveness for longer." }
    if (has(question, "stall speed", "wing loading", "weight", "turn", "flap", "power")) return { concept: "stall-speed-load", title: "FACTORS AFFECTING STALL SPEED", note: "The critical angle of attack remains essentially fixed for a given configuration, but the IAS at which it is reached changes with load factor, weight, flap and power effects." }
    return { concept: "critical-aoa", title: "CRITICAL ANGLE OF ATTACK", note: "A wing stalls because the critical angle of attack is exceeded. The critical angle is fundamentally an aerodynamic angle, not a particular indicated airspeed." }
  }

  if (topic === "Spins") {
    if (has(question, "recovery", "rudder is applied", "rudder before")) return { concept: "spin-recovery", title: "SPIN RECOVERY CONTROL SEQUENCE", note: "Use the aircraft's approved procedure. The aerodynamic principle is to stop yaw with opposite rudder and reduce angle of attack to unstall the wings." }
    return { concept: "spin", title: "SPIN AUTOROTATION", note: "A spin requires a stall plus yaw. The inner wing is more deeply stalled than the outer wing, sustaining autorotation." }
  }

  if (topic === "Airspeed") return { concept: "airspeed-chain", title: "IAS → CAS/RAS → TAS", note: "CAS/RAS corrects IAS for instrument and position error. TAS then corrects CAS/RAS for the actual atmospheric density/temperature-altitude condition." }

  if (topic === "Airspeed Limitations") {
    if (has(question, "manoeuvring", "maneuvering", "va")) return { concept: "va", title: "DESIGN MANOEUVRING SPEED VA", note: "At or below VA, a full abrupt single-axis control input is intended to stall the wing before the positive limit load is exceeded. VA decreases with decreasing weight." }
    if (has(question, "vx", "vy", "best angle", "best rate")) return { concept: "vx-vy", title: "VX & VY", note: "VX is best angle of climb; VY is best rate of climb." }
    return { concept: "v-speeds", title: "V-SPEEDS & OPERATING LIMITS", note: "V-speeds identify approved limitations or performance reference speeds. Their exact values are aircraft-specific and must come from approved data." }
  }

  if (topic === "ISA & Air Density") {
    if (has(question, "humidity", "humid")) return { concept: "humidity-density", title: "HUMIDITY & AIR DENSITY", note: "At the same pressure and temperature, humid air is less dense than dry air because water-vapour molecules have lower molecular mass than the nitrogen/oxygen molecules they displace." }
    if (has(question, "pressure", "temperature", "density") && !has(question, "sea-level density", "sea level density")) return { concept: "pressure-temp-density", title: "PRESSURE, TEMPERATURE & DENSITY", note: "For a fixed gas composition, density increases with pressure and decreases as absolute temperature increases." }
    return { concept: "isa", title: "INTERNATIONAL STANDARD ATMOSPHERE", note: "ISA uses MSL temperature 15°C, standard pressure 1013.25 hPa and a tropospheric lapse rate of about 1.98°C per 1000 ft." }
  }

  if (topic === "Weight & Balance") return { concept: "weight-cg", title: "CENTRE OF GRAVITY", note: "The centre of gravity is the point through which the aircraft's total weight is considered to act." }

  return { concept: "four-forces", title: "PRINCIPLES OF FLIGHT", note: "Use the force directions and aerodynamic relationships shown here together with the exact wording of the question." }
}

function Arrow({ x1, y1, x2, y2, color = GOLD, width = 4 }: { x1: number; y1: number; x2: number; y2: number; color?: string; width?: number }) {
  const a = Math.atan2(y2 - y1, x2 - x1)
  const h = 11
  const p1 = `${x2},${y2}`
  const p2 = `${x2 - h * Math.cos(a - Math.PI / 6)},${y2 - h * Math.sin(a - Math.PI / 6)}`
  const p3 = `${x2 - h * Math.cos(a + Math.PI / 6)},${y2 - h * Math.sin(a + Math.PI / 6)}`
  return <g><line x1={x1} y1={y1} x2={x2} y2={y2} stroke={color} strokeWidth={width} strokeLinecap="round"/><polygon points={`${p1} ${p2} ${p3}`} fill={color}/></g>
}

function T({ x, y, children, size = 14, anchor = "middle", weight = 700, fill = NAVY }: { x: number; y: number; children: ReactNode; size?: number; anchor?: "start" | "middle" | "end"; weight?: number; fill?: string }) {
  return <text x={x} y={y} textAnchor={anchor} fontSize={size} fontWeight={weight} fill={fill} fontFamily="Arial, sans-serif">{children}</text>
}

function Label({ x, y, w, text, fill = NAVY, bg = "white" }: { x: number; y: number; w: number; text: string; fill?: string; bg?: string }) {
  return <g><rect x={x - w / 2} y={y - 18} width={w} height={28} rx="3" fill={bg}/><T x={x} y={y} size={13} fill={fill}>{text}</T></g>
}

function TwoLine({ x, y, first, second, width = 190, accent = false }: { x: number; y: number; first: string; second: string; width?: number; accent?: boolean }) {
  return <g><rect x={x - width / 2} y={y - 28} width={width} height={52} rx="4" fill="white" stroke={LIGHT}/><T x={x} y={y - 6} size={12} fill={accent ? BLUE : NAVY}>{first}</T><T x={x} y={y + 13} size={11} weight={600} fill={GREY}>{second}</T></g>
}

function TechnicalDiagram({ concept }: { concept: Concept }) {
  const common = { viewBox: "0 0 800 360", className: "block w-full", role: "img" as const, preserveAspectRatio: "xMidYMid meet" }

  switch (concept) {
    case "wing-polar": return <svg {...common}><line x1="110" y1="285" x2="700" y2="285" stroke={NAVY} strokeWidth="3"/><line x1="110" y1="285" x2="110" y2="55" stroke={NAVY} strokeWidth="3"/><path d="M135 275 C205 220 285 160 375 120 C470 78 560 72 650 105" fill="none" stroke={BLUE} strokeWidth="5"/><circle cx="550" cy="79" r="7" fill={GOLD}/><Label x={550} y={50} w={150} text="CLmax / critical AoA"/><circle cx="315" cy="145" r="7" fill={GOLD}/><Label x={315} y={114} w={130} text="best L/D region"/><T x={405} y={325}>ANGLE OF ATTACK →</T><T x={62} y={175}>CL</T></svg>
    case "axes-controls": return <svg {...common}><path d="M310 170 L490 170 L550 185 L490 200 L310 200 L250 185Z" fill={PALE} stroke={NAVY} strokeWidth="3"/><circle cx="400" cy="185" r="7" fill={GOLD}/><Label x={400} y={150} w={60} text="CG"/><Arrow x1={125} y1={185} x2={675} y2={185} color={BLUE}/><Label x={650} y={155} w={185} text="LONGITUDINAL — ROLL"/><Arrow x1={400} y1={300} x2={400} y2={65} color={BLUE}/><Label x={505} y={80} w={175} text="VERTICAL — YAW"/><Arrow x1={260} y1={290} x2={540} y2={80} color={GREY}/><Label x={245} y={315} w={190} text="LATERAL — PITCH"/><T x={400} y={340} size={12} fill={GREY}>AILERONS · ELEVATOR · RUDDER</T></svg>
    case "control-effects": return <svg {...common}><TwoLine x={155} y={150} first="AILERON" second="ROLL → YAW"/><TwoLine x={400} y={150} first="RUDDER" second="YAW → ROLL"/><TwoLine x={645} y={150} first="ELEVATOR" second="PITCH"/><Arrow x1={155} y1={205} x2={155} y2={270} color={BLUE}/><Arrow x1={400} y1={205} x2={400} y2={270} color={BLUE}/><TwoLine x={277} y={300} first="IF UNCORRECTED" second="spiral tendency" width={220}/><T x={400} y={70} size={16}>PRIMARY EFFECT FIRST — COUPLED EFFECTS FOLLOW</T></svg>
    case "stability": return <svg {...common}><line x1="90" y1="205" x2="710" y2="205" stroke={LIGHT} strokeWidth="2"/><path d="M100 205 C165 95 225 95 290 205 C350 270 410 245 470 205 C525 170 580 186 650 205" fill="none" stroke={BLUE} strokeWidth="4"/><Arrow x1={180} y1={92} x2={225} y2={165}/><Label x={190} y={65} w={175} text="restoring tendency"/><Label x={575} y={250} w={170} text="oscillation decays"/><T x={400} y={315} size={13} fill={GREY}>POSITIVE STATIC + POSITIVE DYNAMIC STABILITY</T></svg>
    case "dihedral": return <svg {...common}><line x1="400" y1="195" x2="225" y2="130" stroke={NAVY} strokeWidth="8"/><line x1="400" y1="195" x2="575" y2="130" stroke={NAVY} strokeWidth="8"/><Arrow x1={105} y1={250} x2={250} y2={190} color={BLUE}/><Label x={135} y={286} w={135} text="SIDESLIP"/><Arrow x1={250} y1={170} x2={250} y2={90}/><Label x={250} y={68} w={145} text="MORE LIFT"/><Arrow x1={550} y1={170} x2={550} y2={120} color={GREY}/><Label x={550} y={98} w={135} text="LESS LIFT"/><path d="M330 260 Q400 300 470 260" fill="none" stroke={GOLD} strokeWidth="5"/><Label x={400} y={325} w={190} text="RESTORING ROLL"/></svg>
    case "directional-stability": return <svg {...common}><path d="M185 190 L520 190 L600 210 L520 230 L185 230 L120 210Z" fill={PALE} stroke={NAVY} strokeWidth="3"/><path d="M505 190 L555 95 L585 100 L575 195Z" fill="white" stroke={NAVY} strokeWidth="3"/><circle cx="335" cy="210" r="7" fill={GOLD}/><Label x={335} y={173} w={55} text="CG"/><Arrow x1={675} y1={120} x2={585} y2={170} color={BLUE}/><Label x={660} y={90} w={150} text="SIDE GUST"/><path d="M375 285 A90 90 0 0 0 470 265" fill="none" stroke={GOLD} strokeWidth="5"/><Label x={515} y={300} w={205} text="WEATHERCOCK MOMENT"/></svg>
    case "longitudinal-dihedral": return <svg {...common}><line x1="170" y1="170" x2="490" y2="150" stroke={NAVY} strokeWidth="8"/><line x1="545" y1="220" x2="690" y2="235" stroke={BLUE} strokeWidth="7"/><line x1="115" y1="255" x2="710" y2="255" stroke={LIGHT} strokeWidth="2"/><Label x={320} y={120} w={175} text="MAINPLANE INCIDENCE"/><Label x={618} y={275} w={170} text="TAILPLANE INCIDENCE"/><Arrow x1={620} y1={205} x2={620} y2={145}/><Label x={620} y={120} w={160} text="TAIL FORCE CHANGE"/></svg>
    case "cg-stability": return <svg {...common}><line x1="120" y1="190" x2="680" y2="190" stroke={NAVY} strokeWidth="5"/><circle cx="305" cy="190" r="10" fill={GOLD}/><circle cx="455" cy="190" r="10" fill={BLUE}/><Label x={305} y={150} w={110} text="FORWARD CG"/><Label x={455} y={230} w={95} text="AFT CG"/><Arrow x1={305} y1={115} x2={305} y2={70} color={BLUE}/><Label x={220} y={55} w={205} text="MORE STABILITY / FORCE"/><Arrow x1={455} y1={270} x2={455} y2={315} color={GREY}/><Label x={565} y={330} w={215} text="LESS STABILITY MARGIN"/></svg>
    case "cg-cp": return <svg {...common}><path d="M170 190 Q380 130 635 185 Q400 235 170 190Z" fill={PALE} stroke={NAVY} strokeWidth="3"/><circle cx="335" cy="190" r="9" fill={GOLD}/><circle cx="455" cy="185" r="9" fill={BLUE}/><Label x={335} y={145} w={70} text="CG"/><Label x={455} y={145} w={70} text="CP"/><Arrow x1={455} y1={175} x2={455} y2={80}/><Label x={500} y={65} w={95} text="LIFT"/><Arrow x1={335} y1={200} x2={335} y2={295} color={GREY}/><Label x={280} y={315} w={110} text="WEIGHT"/><T x={400} y={340} size={12} fill={GREY}>CONVENTIONAL ARRANGEMENT: CG NORMALLY AHEAD OF CP</T></svg>
    case "aerofoil": return <svg {...common}><path d="M135 200 Q330 90 665 190 Q360 245 135 200Z" fill={PALE} stroke={NAVY} strokeWidth="4"/><line x1="135" y1="200" x2="665" y2="190" stroke={BLUE} strokeWidth="2" strokeDasharray="8 6"/><Label x={400} y={238} w={125} text="CHORD LINE"/><line x1="360" y1="120" x2="360" y2="215" stroke={GOLD} strokeWidth="3"/><Label x={360} y={90} w={150} text="MAX THICKNESS"/><Label x={155} y={165} w={120} text="LEADING EDGE"/><Label x={650} y={160} w={120} text="TRAILING EDGE"/></svg>
    case "angle-of-attack": return <svg {...common}><line x1="155" y1="255" x2="655" y2="255" stroke={BLUE} strokeWidth="4"/><polygon points="155,255 171,246 171,264" fill={BLUE}/><line x1="205" y1="220" x2="630" y2="155" stroke={NAVY} strokeWidth="5"/><path d="M255 248 A65 65 0 0 1 270 211" fill="none" stroke={GOLD} strokeWidth="6"/><circle cx="287" cy="231" r="23" fill="white" stroke={GOLD} strokeWidth="2"/><T x={287} y={237} size={18} fill={GOLD}>α</T><Label x={535} y={125} w={120} text="CHORD LINE"/><Label x={405} y={295} w={190} text="RELATIVE AIRFLOW ←"/><T x={400} y={335} size={12} fill={GREY}>α IS THE ACUTE ANGLE BETWEEN THE TWO REFERENCE LINES</T></svg>
    case "incidence-washout": return <svg {...common}><line x1="105" y1="270" x2="695" y2="270" stroke={LIGHT} strokeWidth="2"/><line x1="150" y1="215" x2="385" y2="175" stroke={NAVY} strokeWidth="6"/><path d="M185 268 A65 65 0 0 1 203 207" fill="none" stroke={GOLD} strokeWidth="4"/><Label x={270} y={140} w={160} text="ANGLE OF INCIDENCE"/><line x1="470" y1="180" x2="690" y2="210" stroke={NAVY} strokeWidth="7"/><line x1="470" y1="180" x2="470" y2="120" stroke={GREY} strokeWidth="2"/><line x1="690" y1="210" x2="690" y2="160" stroke={GREY} strokeWidth="2"/><Label x={580} y={110} w={170} text="WASHOUT: INCIDENCE ↓"/><T x={400} y={330} size={12} fill={GREY}>ANHEDRAL = WING SLOPES DOWNWARD FROM ROOT TO TIP</T></svg>
    case "boundary-layer": return <svg {...common}><path d="M100 245 Q360 125 690 220" fill="none" stroke={NAVY} strokeWidth="5"/><path d="M105 225 Q235 177 345 170" fill="none" stroke={BLUE} strokeWidth="2"/><path d="M105 205 Q235 145 350 150" fill="none" stroke={BLUE} strokeWidth="2"/><path d="M360 155 Q455 130 525 168" fill="none" stroke={GOLD} strokeWidth="3" strokeDasharray="7 5"/><path d="M540 175 Q615 140 690 170" fill="none" stroke={RED} strokeWidth="3"/><Label x={215} y={115} w={135} text="LAMINAR"/><Label x={440} y={105} w={155} text="TRANSITION"/><Label x={625} y={125} w={135} text="SEPARATION"/><Arrow x1={120} y1={290} x2={670} y2={290} color={GREY}/><Label x={400} y={325} w={160} text="FLOW DIRECTION"/></svg>
    case "bernoulli": return <svg {...common}><path d="M90 120 L310 120 L385 165 L310 210 L90 210Z" fill={PALE} stroke={NAVY} strokeWidth="3"/><path d="M710 120 L490 120 L415 165 L490 210 L710 210Z" fill={PALE} stroke={NAVY} strokeWidth="3"/><Arrow x1={125} y1={165} x2={675} y2={165} color={BLUE}/><TwoLine x={180} y={275} first="WIDE SECTION" second="lower V · higher static P" width={190}/><TwoLine x={400} y={80} first="THROAT" second="higher V · lower static P" width={210}/><TwoLine x={620} y={275} first="WIDE SECTION" second="velocity falls · P recovers" width={190}/></svg>
    case "newton-laws": return <svg {...common}><TwoLine x={155} y={145} first="1st LAW" second="inertia / equilibrium" width={190}/><TwoLine x={400} y={145} first="2nd LAW" second="F = m a" width={190}/><TwoLine x={645} y={145} first="3rd LAW" second="action ↔ reaction" width={190}/><Arrow x1={120} y1={245} x2={190} y2={245} color={BLUE}/><Arrow x1={610} y1={245} x2={680} y2={245} color={BLUE}/><T x={400} y={250} size={15}>FORCES CHANGE MOTION — REACTIONS ARE OPPOSITE</T></svg>
    case "dynamic-pressure": return <svg {...common}><rect x="115" y="125" width="180" height="105" fill="white" stroke={NAVY} strokeWidth="3"/><T x={205} y={165}>STATIC PRESSURE</T><T x={205} y={195} size={12} fill={GREY}>ambient pressure</T><rect x="505" y="125" width="180" height="105" fill="white" stroke={NAVY} strokeWidth="3"/><T x={595} y={165}>TOTAL PRESSURE</T><T x={595} y={195} size={12} fill={GREY}>stagnation pressure</T><Arrow x1={305} y1={178} x2={490} y2={178}/><Label x={400} y={140} w={145} text="+ DYNAMIC q"/><T x={400} y={285} size={18} fill={BLUE}>q = ½ ρ V²</T><T x={400} y={320} size={12} fill={GREY}>TOTAL = STATIC + DYNAMIC</T></svg>
    case "lift-pressure": return <svg {...common}><path d="M160 205 Q355 105 650 195 Q390 245 160 205Z" fill={PALE} stroke={NAVY} strokeWidth="3"/><Arrow x1={110} y1={285} x2={680} y2={285} color={BLUE}/><Label x={400} y={325} w={190} text="RELATIVE AIRFLOW →"/><Arrow x1={405} y1={190} x2={405} y2={70}/><Label x={470} y={60} w={100} text="LIFT"/><T x={400} y={130} size={12} fill={GREY}>LOWER STATIC PRESSURE ABOVE</T><T x={400} y={250} size={12} fill={GREY}>HIGHER STATIC PRESSURE BELOW</T></svg>
    case "centre-pressure": return <svg {...common}><path d="M145 205 Q350 105 660 195 Q380 245 145 205Z" fill={PALE} stroke={NAVY} strokeWidth="3"/><line x1="145" y1="205" x2="660" y2="195" stroke={LIGHT} strokeWidth="2"/><circle cx="430" cy="200" r="9" fill={GOLD}/><Arrow x1={430} y1={190} x2={430} y2={75}/><Label x={430} y={55} w={170} text="RESULTANT FORCE"/><Label x={430} y={245} w={170} text="CENTRE OF PRESSURE"/><Arrow x1={515} y1={285} x2={350} y2={285} color={BLUE}/><Label x={585} y={290} w={180} text="AoA ↑ : CP FORWARD"/></svg>
    case "aspect-ratio": return <svg {...common}><rect x="95" y="125" width="270" height="85" fill={PALE} stroke={NAVY} strokeWidth="3"/><rect x="485" y="105" width="120" height="125" fill={PALE} stroke={NAVY} strokeWidth="3"/><Label x={230} y={95} w={180} text="HIGH ASPECT RATIO"/><Label x={545} y={75} w={180} text="LOW ASPECT RATIO"/><Arrow x1={135} y1={250} x2={325} y2={250} color={BLUE}/><Label x={230} y={285} w={160} text="LESS INDUCED DRAG"/><Arrow x1={500} y1={270} x2={590} y2={270} color={RED}/><Label x={545} y={310} w={165} text="MORE INDUCED DRAG"/></svg>
    case "lift-speed": return <svg {...common}><line x1="120" y1="285" x2="690" y2="285" stroke={NAVY} strokeWidth="3"/><line x1="120" y1="285" x2="120" y2="60" stroke={NAVY} strokeWidth="3"/><path d="M135 270 Q305 245 430 180 Q565 110 665 70" fill="none" stroke={GOLD} strokeWidth="5"/><circle cx="290" cy="226" r="7" fill={BLUE}/><circle cx="505" cy="143" r="7" fill={BLUE}/><Label x={395} y={105} w={135} text="L ∝ V²"/><Label x={400} y={330} w={190} text="TRUE AIRSPEED V"/><T x={70} y={175}>LIFT</T></svg>
    case "drag-curves": return <svg {...common}><line x1="110" y1="285" x2="700" y2="285" stroke={NAVY} strokeWidth="3"/><line x1="110" y1="285" x2="110" y2="55" stroke={NAVY} strokeWidth="3"/><path d="M130 75 Q250 175 390 255 Q500 280 680 280" fill="none" stroke={BLUE} strokeWidth="4"/><path d="M130 280 Q360 278 500 195 Q605 130 680 75" fill="none" stroke={GOLD} strokeWidth="4"/><path d="M130 105 Q330 260 470 220 Q585 180 680 110" fill="none" stroke={NAVY} strokeWidth="5"/><Label x={215} y={90} w={120} text="INDUCED"/><Label x={615} y={90} w={125} text="PARASITE"/><Label x={510} y={185} w={105} text="TOTAL"/><T x={405} y={330}>AIRSPEED →</T><T x={65} y={175}>DRAG</T></svg>
    case "skin-friction": return <svg {...common}><line x1="95" y1="215" x2="705" y2="215" stroke={NAVY} strokeWidth="6"/><path d="M115 205 C220 195 330 195 440 195 C550 195 625 188 690 178" fill="none" stroke={BLUE} strokeWidth="3"/><path d="M115 185 C240 165 355 165 475 162 C575 160 635 150 690 138" fill="none" stroke={BLUE} strokeWidth="2"/><Arrow x1={125} y1={120} x2={675} y2={120} color={GREY}/><Label x={400} y={90} w={165} text="FREE-STREAM FLOW"/><Label x={245} y={250} w={215} text="VELOCITY → 0 AT SURFACE"/><Label x={585} y={250} w={155} text="SKIN FRICTION"/></svg>
    case "induced-drag": return <svg {...common}><line x1="160" y1="175" x2="640" y2="175" stroke={NAVY} strokeWidth="10"/><path d="M160 185 C115 205 110 265 160 285 C210 305 235 250 200 220" fill="none" stroke={BLUE} strokeWidth="4"/><path d="M640 185 C685 205 690 265 640 285 C590 305 565 250 600 220" fill="none" stroke={BLUE} strokeWidth="4"/><Arrow x1={255} y1={115} x2={545} y2={115} color={GREY}/><Label x={400} y={80} w={210} text="LOW PRESSURE ABOVE"/><Label x={400} y={225} w={220} text="HIGH PRESSURE BELOW"/><T x={400} y={330} size={13} fill={GREY}>SPANWISE FLOW → WINGTIP VORTICES → INDUCED DRAG</T></svg>
    case "four-forces": return <svg {...common}><path d="M280 175 L515 175 L565 190 L515 205 L280 205 L230 190Z" fill={PALE} stroke={NAVY} strokeWidth="3"/><Arrow x1={400} y1={175} x2={400} y2={65}/><Label x={455} y={55} w={85} text="LIFT"/><Arrow x1={400} y1={205} x2={400} y2={315} color={BLUE}/><Label x={455} y={330} w={100} text="WEIGHT"/><Arrow x1={515} y1={190} x2={700} y2={190}/><Label x={625} y={155} w={100} text="THRUST"/><Arrow x1={280} y1={190} x2={95} y2={190} color={BLUE}/><Label x={175} y={155} w={85} text="DRAG"/></svg>
    case "climb-forces": return <svg {...common}><line x1="105" y1="285" x2="695" y2="285" stroke={LIGHT} strokeWidth="2"/><line x1="190" y1="250" x2="610" y2="115" stroke={GREY} strokeWidth="3" strokeDasharray="8 6"/><path d="M315 205 L500 145" stroke={NAVY} strokeWidth="8"/><Arrow x1={455} y1={160} x2={625} y2={105}/><Label x={645} y={80} w={105} text="THRUST"/><Arrow x1={355} y1={190} x2={215} y2={235} color={BLUE}/><Label x={190} y={260} w={85} text="DRAG"/><Arrow x1={405} y1={175} x2={405} y2={70}/><Label x={455} y={55} w={85} text="LIFT"/><Arrow x1={405} y1={195} x2={405} y2={320} color={GREY}/><Label x={455} y={335} w={100} text="WEIGHT"/></svg>
    case "descent-power": return <svg {...common}><line x1="105" y1="95" x2="695" y2="285" stroke={LIGHT} strokeWidth="3"/><path d="M205 135 L390 195" stroke={NAVY} strokeWidth="8"/><Arrow x1={390} y1={195} x2={545} y2={245}/><Label x={585} y={270} w={125} text="FLIGHT PATH"/><TwoLine x={250} y={300} first="POWER ↓" second="rate of descent ↑" width={180}/><TwoLine x={550} y={110} first="POWER ↑" second="rate of descent ↓" width={180}/></svg>
    case "flap-effects": return <svg {...common}><T x={210} y={60}>CLEAN</T><path d="M95 155 Q220 105 345 150 Q220 185 95 155Z" fill={PALE} stroke={NAVY} strokeWidth="3"/><T x={590} y={60}>FLAP EXTENDED</T><path d="M455 155 Q575 105 685 150 Q580 187 455 155Z" fill={PALE} stroke={NAVY} strokeWidth="3"/><line x1="615" y1="153" x2="690" y2="205" stroke={GOLD} strokeWidth="10"/><TwoLine x={590} y={270} first="CAMBER & CLmax ↑" second="drag ↑ · AoA for same lift ↓" width={245}/><TwoLine x={210} y={270} first="CLEAN WING" second="higher best L/D" width={210}/></svg>
    case "fowler-flap": return <svg {...common}><path d="M120 180 Q325 105 570 170 Q360 210 120 180Z" fill={PALE} stroke={NAVY} strokeWidth="3"/><path d="M520 172 L645 205" fill="none" stroke={GOLD} strokeWidth="12" strokeLinecap="round"/><Arrow x1={525} y1={245} x2={625} y2={245} color={BLUE}/><Label x={575} y={285} w={185} text="MOVES AFT + DOWN"/><Label x={400} y={75} w={225} text="WING AREA & CAMBER INCREASE"/></svg>
    case "slat": return <svg {...common}><path d="M185 205 Q370 95 655 185 Q405 235 185 205Z" fill={PALE} stroke={NAVY} strokeWidth="3"/><path d="M145 198 Q165 150 215 150" fill="none" stroke={GOLD} strokeWidth="11" strokeLinecap="round"/><Arrow x1={85} y1={145} x2={215} y2={170} color={BLUE}/><Arrow x1={220} y1={170} x2={390} y2={125} color={BLUE}/><Label x={245} y={100} w={195} text="ENERGISED SLOT FLOW"/><Label x={520} y={270} w={225} text="SEPARATION DELAYED"/></svg>
    case "glide-flap": return <svg {...common}><line x1="100" y1="90" x2="700" y2="300" stroke={LIGHT} strokeWidth="2"/><line x1="120" y1="105" x2="680" y2="230" stroke={BLUE} strokeWidth="4"/><line x1="120" y1="105" x2="585" y2="285" stroke={GOLD} strokeWidth="5"/><Label x={590} y={210} w={160} text="CLEAN: SHALLOWER"/><Label x={500} y={305} w={180} text="FLAP: STEEPER"/><T x={400} y={55} size={13} fill={GREY}>FLAP EXTENSION REDUCES BEST L/D</T></svg>
    case "glide-wind": return <svg {...common}><line x1="105" y1="285" x2="695" y2="285" stroke={NAVY} strokeWidth="3"/><path d="M140 85 L410 260" fill="none" stroke={GOLD} strokeWidth="4"/><path d="M140 85 L635 260" fill="none" stroke={BLUE} strokeWidth="4"/><Arrow x1={300} y1={60} x2={170} y2={60} color={GREY}/><Label x={235} y={35} w={130} text="HEADWIND"/><Label x={355} y={245} w={155} text="STEEPER OVER GROUND"/><Label x={590} y={245} w={165} text="TAILWIND: SHALLOWER"/></svg>
    case "adverse-yaw": return <svg {...common}><line x1="110" y1="170" x2="690" y2="170" stroke={NAVY} strokeWidth="9"/><line x1="110" y1="170" x2="200" y2="120" stroke={GOLD} strokeWidth="10"/><line x1="600" y1="170" x2="690" y2="198" stroke={GOLD} strokeWidth="10"/><Label x={160} y={90} w={165} text="UP AILERON: LESS DRAG"/><Label x={640} y={235} w={190} text="DOWN AILERON: MORE DRAG"/><Arrow x1={470} y1={285} x2={315} y2={285} color={RED}/><Label x={545} y={290} w={210} text="YAW OPPOSITE ROLL"/></svg>
    case "trim-tab": return <svg {...common}><line x1="130" y1="175" x2="610" y2="175" stroke={NAVY} strokeWidth="12"/><line x1="545" y1="175" x2="665" y2="205" stroke={GOLD} strokeWidth="9"/><Label x={365} y={125} w={180} text="MAIN CONTROL SURFACE"/><Label x={630} y={240} w={120} text="TRIM TAB"/><Arrow x1={630} y1={270} x2={630} y2={315} color={BLUE}/><T x={400} y={330} size={12} fill={GREY}>TAB AERODYNAMIC FORCE HOLDS THE MAIN SURFACE AT THE TRIMMED POSITION</T></svg>
    case "balance-tab": return <svg {...common}><line x1="120" y1="175" x2="610" y2="205" stroke={NAVY} strokeWidth="12"/><line x1="545" y1="200" x2="675" y2="150" stroke={GOLD} strokeWidth="9"/><Arrow x1={300} y1={115} x2={300} y2={165} color={BLUE}/><Arrow x1={630} y1={230} x2={630} y2={170}/><Label x={300} y={85} w={160} text="SURFACE DOWN"/><Label x={630} y={270} w={170} text="TAB OPPOSITE"/></svg>
    case "anti-balance-tab": return <svg {...common}><line x1="120" y1="175" x2="610" y2="205" stroke={NAVY} strokeWidth="12"/><line x1="545" y1="200" x2="675" y2="230" stroke={GOLD} strokeWidth="9"/><Arrow x1={300} y1={115} x2={300} y2={165} color={BLUE}/><Arrow x1={630} y1={165} x2={630} y2={220}/><Label x={300} y={85} w={160} text="SURFACE DOWN"/><Label x={630} y={275} w={180} text="TAB SAME DIRECTION"/></svg>
    case "mass-balance": return <svg {...common}><line x1="170" y1="180" x2="650" y2="180" stroke={NAVY} strokeWidth="12"/><line x1="335" y1="110" x2="335" y2="250" stroke={BLUE} strokeWidth="3"/><circle cx="270" cy="180" r="24" fill={GOLD}/><Label x={335} y={85} w={110} text="HINGE LINE"/><Label x={230} y={245} w={150} text="MASS AHEAD"/><T x={500} y={245} size={13} fill={GREY}>REDUCES FLUTTER TENDENCY</T></svg>
    case "horn-balance": return <svg {...common}><line x1="245" y1="115" x2="245" y2="285" stroke={BLUE} strokeWidth="3"/><path d="M245 135 L650 175 L650 235 L245 215Z" fill={PALE} stroke={NAVY} strokeWidth="3"/><path d="M190 120 L275 135 L260 190 L195 175Z" fill="white" stroke={GOLD} strokeWidth="4"/><Label x={245} y={90} w={105} text="HINGE"/><Label x={170} y={220} w={155} text="AREA AHEAD"/><T x={470} y={300} size={13} fill={GREY}>AERODYNAMIC FORCE AHEAD OF HINGE REDUCES PILOT EFFORT</T></svg>
    case "flutter": return <svg {...common}><line x1="120" y1="185" x2="680" y2="185" stroke={NAVY} strokeWidth="9"/><path d="M480 185 C505 100 535 265 560 120 C585 260 615 105 650 180" fill="none" stroke={RED} strokeWidth="4"/><Label x={565} y={80} w={170} text="OSCILLATION GROWS"/><Arrow x1={180} y1={265} x2={300} y2={265} color={BLUE}/><Label x={240} y={305} w={170} text="AIRFLOW / ENERGY"/><T x={400} y={55} size={13} fill={GREY}>AEROELASTIC COUPLING CAN BECOME SELF-EXCITING</T></svg>
    case "bank-load-factor": return <svg {...common}><line x1="110" y1="285" x2="690" y2="285" stroke={NAVY} strokeWidth="3"/><line x1="110" y1="285" x2="110" y2="55" stroke={NAVY} strokeWidth="3"/><path d="M125 275 C350 270 470 240 555 175 C610 130 650 85 675 55" fill="none" stroke={GOLD} strokeWidth="5"/><line x1="555" y1="175" x2="555" y2="285" stroke={BLUE} strokeWidth="2" strokeDasharray="6 5"/><Label x={555} y={145} w={105} text="60° = 2 G"/><T x={405} y={330}>BANK ANGLE φ →</T><T x={60} y={175}>LOAD n</T><T x={250} y={80} size={15} fill={BLUE}>n = 1 / cos φ</T></svg>
    case "turn-forces": return <svg {...common}><circle cx="390" cy="200" r="7" fill={NAVY}/><Arrow x1={390} y1={200} x2={525} y2={75}/><Label x={585} y={65} w={125} text="TOTAL LIFT"/><Arrow x1={390} y1={200} x2={390} y2={75} color={BLUE}/><Label x={320} y={65} w={175} text="VERTICAL COMPONENT"/><Arrow x1={390} y1={200} x2={525} y2={200}/><Label x={590} y={205} w={135} text="CENTRIPETAL"/><Arrow x1={390} y1={200} x2={390} y2={315} color={GREY}/><Label x={450} y={330} w={100} text="WEIGHT"/></svg>
    case "slip-skid": return <svg {...common}><path d="M135 210 Q205 120 275 210Z" fill="PALE" stroke={NAVY} strokeWidth="3"/><line x1="160" y1="205" x2="250" y2="205" stroke={GREY} strokeWidth="3"/><circle cx="205" cy="205" r="12" fill={GOLD}/><Label x={205} y={260} w={120} text="BALANCED"/><path d="M330 210 Q400 120 470 210Z" fill="PALE" stroke={NAVY} strokeWidth="3"/><line x1="355" y1="205" x2="445" y2="205" stroke={GREY} strokeWidth="3"/><circle cx="365" cy="205" r="12" fill={GOLD}/><Label x={400} y={260} w={105} text="SLIP"/><path d="M525 210 Q595 120 665 210Z" fill="PALE" stroke={NAVY} strokeWidth="3"/><line x1="550" y1="205" x2="640" y2="205" stroke={GREY} strokeWidth="3"/><circle cx="630" cy="205" r="12" fill={GOLD}/><Label x={595} y={260} w={105} text="SKID"/><T x={400} y={70} size={13} fill={GREY}>BALL CENTRED = COORDINATED TURN</T></svg>
    case "stall-speed-load": return <svg {...common}><line x1="120" y1="285" x2="690" y2="285" stroke={NAVY} strokeWidth="3"/><line x1="120" y1="285" x2="120" y2="55" stroke={NAVY} strokeWidth="3"/><path d="M140 260 Q315 225 450 165 Q575 110 665 75" fill="none" stroke={GOLD} strokeWidth="5"/><Label x={505} y={105} w={150} text="Vs ∝ √n"/><T x={405} y={330}>LOAD FACTOR n →</T><T x={60} y={175}>STALL SPEED</T></svg>
    case "critical-aoa": return <svg {...common}><line x1="160" y1="270" x2="660" y2="270" stroke={BLUE} strokeWidth="4"/><line x1="210" y1="245" x2="625" y2="145" stroke={NAVY} strokeWidth="5"/><path d="M270 263 A75 75 0 0 1 291 226" fill="none" stroke={GOLD} strokeWidth="5"/><Label x={335} y={215} w={165} text="CRITICAL AoA" fill={RED}/><path d="M350 135 Q470 70 625 130" fill="none" stroke={RED} strokeWidth="3" strokeDasharray="7 5"/><Label x={520} y={75} w={185} text="FLOW SEPARATION GROWS"/><T x={400} y={325} size={12} fill={GREY}>STALL OCCURS WHEN THE CRITICAL ANGLE IS EXCEEDED</T></svg>
    case "stall-warning": return <svg {...common}><path d="M145 210 Q350 110 660 195 Q390 245 145 210Z" fill={PALE} stroke={NAVY} strokeWidth="3"/><path d="M420 135 Q520 95 650 145" fill="none" stroke={RED} strokeWidth="3" strokeDasharray="7 5"/><Arrow x1={150} y1={285} x2={665} y2={285} color={BLUE}/><Label x={520} y={95} w={160} text="BUFFET / SEPARATION"/><TwoLine x={235} y={80} first="APPROACHING STALL" second="controls become less effective" width={240}/><T x={400} y={330} size={12} fill={GREY}>STALL WARNING SHOULD OCCUR BEFORE THE FULL STALL</T></svg>
    case "stall-progression": return <svg {...common}><path d="M115 185 L685 185 L625 235 L175 235Z" fill={PALE} stroke={NAVY} strokeWidth="3"/><rect x="330" y="175" width="140" height="70" fill="#fee2e2" stroke={RED} strokeWidth="2"/><Label x={400} y={150} w={165} text="ROOT STALLS FIRST"/><Label x={185} y={280} w={170} text="TIP STILL FLYING"/><Label x={615} y={280} w={170} text="AILERON EFFECT RETAINED"/><T x={400} y={330} size={12} fill={GREY}>WASHOUT REDUCES INCIDENCE TOWARD THE TIP</T></svg>
    case "spin": return <svg {...common}><circle cx="400" cy="190" r="95" fill="none" stroke={LIGHT} strokeWidth="3" strokeDasharray="7 5"/><path d="M315 170 L485 215" stroke={NAVY} strokeWidth="10"/><Arrow x1={480} y1={95} x2={535} y2={145} color={GOLD}/><Arrow x1={525} y1={240} x2={470} y2={285} color={GOLD}/><Label x={250} y={110} w={165} text="INNER WING"/><Label x={250} y={140} w={190} text="MORE DEEPLY STALLED" fill={RED}/><Label x={575} y={300} w={160} text="AUTOROTATION"/><T x={400} y={335} size={12} fill={GREY}>STALL + YAW = SPIN</T></svg>
    case "spin-recovery": return <svg {...common}><TwoLine x={150} y={160} first="1 · POWER" second="as approved" width={180}/><Arrow x1={245} y1={160} x2={305} y2={160}/><TwoLine x={400} y={160} first="2 · OPPOSITE RUDDER" second="stop yaw" width={200}/><Arrow x1={505} y1={160} x2={565} y2={160}/><TwoLine x={650} y={160} first="3 · REDUCE AoA" second="unstall wings" width={190}/><T x={400} y={260} size={13} fill={GREY}>THEN CENTRALISE / RECOVER SMOOTHLY AS REQUIRED BY THE APPROVED PROCEDURE</T></svg>
    case "airspeed-chain": return <svg {...common}><TwoLine x={130} y={165} first="IAS" second="instrument reading" width={150}/><Arrow x1={210} y1={165} x2={285} y2={165}/><TwoLine x={380} y={165} first="CAS / RAS" second="instrument + position corrected" width={210}/><Arrow x1={490} y1={165} x2={565} y2={165}/><TwoLine x={660} y={165} first="TAS" second="density / temp-alt corrected" width={200}/><T x={400} y={280} size={13} fill={GREY}>TAS = AIRCRAFT SPEED RELATIVE TO THE SURROUNDING AIR MASS</T></svg>
    case "v-speeds": return <svg {...common}><line x1="100" y1="185" x2="700" y2="185" stroke={NAVY} strokeWidth="8"/><line x1="180" y1="160" x2="180" y2="210" stroke={BLUE} strokeWidth="5"/><line x1="350" y1="160" x2="350" y2="210" stroke={GREEN} strokeWidth="5"/><line x1="525" y1="160" x2="525" y2="210" stroke={GOLD} strokeWidth="5"/><line x1="650" y1="150" x2="650" y2="220" stroke={RED} strokeWidth="6"/><Label x={180} y={130} w={90} text="VFE"/><Label x={350} y={130} w={90} text="VNO"/><Label x={525} y={130} w={90} text="VLO"/><Label x={650} y={115} w={90} text="VNE"/><T x={400} y={275} size={13} fill={GREY}>EXACT LIMITS AND COLOUR ARCS ARE AIRCRAFT-SPECIFIC</T></svg>
    case "va": return <svg {...common}><line x1="120" y1="285" x2="690" y2="285" stroke={NAVY} strokeWidth="3"/><line x1="120" y1="285" x2="120" y2="55" stroke={NAVY} strokeWidth="3"/><path d="M150 270 Q310 210 470 135" fill="none" stroke={BLUE} strokeWidth="4"/><line x1="470" y1="135" x2="630" y2="135" stroke={RED} strokeWidth="4"/><Label x={470} y={105} w={165} text="VA INTERSECTION"/><Label x={570} y={170} w={150} text="LIMIT LOAD"/><T x={405} y={330}>AIRSPEED →</T><T x={65} y={175}>LOAD</T><T x={305} y={70} size={12} fill={GREY}>LOWER WEIGHT → LOWER VA</T></svg>
    case "vx-vy": return <svg {...common}><line x1="105" y1="285" x2="695" y2="285" stroke={NAVY} strokeWidth="3"/><rect x="570" y="105" width="20" height="180" fill={GREY}/><path d="M125 270 Q275 260 370 220 Q470 175 555 115" fill="none" stroke={GOLD} strokeWidth="5"/><path d="M125 270 Q290 225 455 120" fill="none" stroke={BLUE} strokeWidth="5"/><Label x={485} y={95} w={135} text="VX: ANGLE"/><Label x={305} y={185} w={130} text="VY: RATE"/><Label x={580} y={80} w={110} text="OBSTACLE"/><T x={400} y={330} size={12} fill={GREY}>VX = HEIGHT / DISTANCE · VY = HEIGHT / TIME</T></svg>
    case "isa": return <svg {...common}><line x1="400" y1="300" x2="400" y2="65" stroke={NAVY} strokeWidth="4"/><line x1="210" y1="275" x2="590" y2="105" stroke={GOLD} strokeWidth="5"/><Label x={210} y={305} w={160} text="MSL: 15°C"/><Label x={590} y={80} w={210} text="−1.98°C / 1000 ft"/><TwoLine x={610} y={250} first="MSL PRESSURE" second="1013.25 hPa" width={185}/><TwoLine x={190} y={110} first="MSL DENSITY" second="1.225 kg/m³" width={185}/></svg>
    case "humidity-density": return <svg {...common}><rect x="105" y="100" width="245" height="160" fill={PALE} stroke={NAVY} strokeWidth="3"/><rect x="450" y="100" width="245" height="160" fill={PALE} stroke={NAVY} strokeWidth="3"/><T x={228} y={135}>DRY AIR</T><T x={572} y={135}>HUMID AIR</T><g fill={BLUE}>{[150,195,240,285].map((x)=><circle key={x} cx={x} cy="190" r="12"/>)}</g><g fill={GOLD}><circle cx="495" cy="190" r="9"/><circle cx="545" cy="190" r="9"/><circle cx="595" cy="190" r="9"/><circle cx="645" cy="190" r="9"/></g><Label x={228} y={300} w={165} text="MORE DENSE"/><Label x={572} y={300} w={165} text="LESS DENSE"/></svg>
    case "pressure-temp-density": return <svg {...common}><TwoLine x={185} y={160} first="PRESSURE ↑" second="density ↑ if T constant" width={220}/><TwoLine x={615} y={160} first="TEMPERATURE ↑" second="density ↓ if P constant" width={220}/><Arrow x1={305} y1={160} x2={495} y2={160} color={GREY}/><T x={400} y={265} size={18} fill={BLUE}>ρ ∝ P / T</T><T x={400} y={305} size={12} fill={GREY}>T MUST BE ABSOLUTE TEMPERATURE IN THE GAS RELATIONSHIP</T></svg>
    case "propeller-effects": return <svg {...common}><circle cx="400" cy="180" r="78" fill="none" stroke={NAVY} strokeWidth="4"/><line x1="400" y1="80" x2="400" y2="280" stroke={GOLD} strokeWidth="14" strokeLinecap="round"/><Arrow x1={510} y1={95} x2={575} y2={135} color={BLUE}/><Label x={610} y={105} w={160} text="PROP ROTATION"/><Arrow x1={290} y1={265} x2={225} y2={225} color={RED}/><Label x={180} y={290} w={175} text="TORQUE REACTION"/><T x={400} y={330} size={12} fill={GREY}>HIGH POWER + HIGH AoA CAN ALSO PRODUCE ASYMMETRIC BLADE EFFECT</T></svg>
    case "weight-cg": return <svg {...common}><path d="M180 180 L620 180 L670 200 L620 220 L180 220 L130 200Z" fill={PALE} stroke={NAVY} strokeWidth="3"/><circle cx="400" cy="200" r="10" fill={GOLD}/><Arrow x1={400} y1={210} x2={400} y2={315} color={BLUE}/><Label x={400} y={160} w={165} text="CENTRE OF GRAVITY"/><Label x={460} y={320} w={100} text="WEIGHT"/></svg>
  }
}

export function PrinciplesOfFlightVisualV2({ question }: { question: Question }) {
  const spec = getSpec(question)

  return (
    <figure className="mt-5 overflow-hidden border border-slate-200 bg-white">
      <div className="bg-[#06111f] px-4 py-4 text-center sm:px-6 sm:py-5">
        <div className="text-[11px] font-extrabold tracking-[0.24em] text-[#f4b400] sm:text-xs">PILOTVAULT PRINCIPLES OF FLIGHT</div>
        <div className="mt-1 text-lg font-extrabold uppercase tracking-[0.025em] text-white sm:text-2xl">{spec.title}</div>
      </div>
      <div className="bg-[#f8fafc] p-3 sm:p-5">
        <div className="mx-auto max-w-4xl border border-slate-200 bg-white px-2 py-3 sm:px-4 sm:py-4">
          <TechnicalDiagram concept={spec.concept} />
          <div className="mx-auto mt-2 max-w-3xl border-t border-slate-200 px-3 pt-3 text-center text-sm leading-relaxed text-slate-700">{spec.note}</div>
        </div>
      </div>
    </figure>
  )
}
