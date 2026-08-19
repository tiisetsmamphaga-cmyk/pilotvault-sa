"use client"

import type { Question } from "../types"

type StaticVisual = { src: string; alt: string }

const ROOT = "/explanation-images/principles-of-flight/static-v4"
const visual = (file: string, alt: string): StaticVisual => ({ src: `${ROOT}/${file}`, alt })
const wording = (question: Question) => `${question.question} ${question.correctAnswer}`.toLowerCase()
const has = (text: string, ...terms: string[]) => terms.some((term) => text.includes(term.toLowerCase()))

/**
 * Curated, question-specific Principles of Flight explanation visuals.
 *
 * Every asset returned here is a finished static training graphic. The mapper
 * intentionally returns null when a diagram would be generic filler or could
 * misrepresent the concept being tested.
 */
function getStaticPofVisual(question: Question): StaticVisual | null {
  const q = wording(question)
  const topic = question.topic ?? ""

  if (has(q, "wing polar", "polar diagram")) {
    return visual("wing-polar-ref-v1.svg", "PilotVault wing polar lift and drag diagram")
  }

  if (topic === "Aerofoils & Lift") {
    if (
      (has(q, "angle between") && has(q, "chord line") && has(q, "relative airflow")) ||
      has(q, "angle of attack of an aeroplane is the angle", "angle of attack is defined as")
    ) {
      return visual("angle-of-attack-ref-v4.svg", "PilotVault angle of attack training diagram")
    }
    if (has(q, "chord line") && !has(q, "angle of attack")) {
      return visual("aerofoil-geometry-ref-v2.svg", "PilotVault aerofoil geometry diagram")
    }
    if (has(q, "boundary layer", "transition point", "laminar-flow", "laminar flow")) {
      return visual("boundary-layer-transition-ref-v1.svg", "PilotVault boundary layer and transition diagram")
    }
    if (has(q, "centre of pressure", "center of pressure")) {
      if (has(q, "move forward", "moves forward", "move aft", "moves aft", "increased", "high angles of attack")) {
        return visual("centre-pressure-shift-ref-v1.svg", "PilotVault centre of pressure shift diagram")
      }
      return visual("centre-of-pressure-ref-v2.svg", "PilotVault centre of pressure diagram")
    }
    if (has(q, "pressure along the upper", "pressure distribution", "high pressure below", "higher air pressure below", "lower air pressure above")) {
      return visual("lift-pressure-distribution-ref-v1.svg", "PilotVault pressure distribution and lift diagram")
    }
    if (has(q, "perpendicular to the relative airflow", "definition of lift", "lift force produced", "lift acts perpendicular", "drag acts parallel")) {
      return visual("lift-drag-directions-ref-v2.svg", "PilotVault lift and drag direction diagram")
    }
    if (has(q, "airspeed is doubled", "speed is doubled", "v squared", "v²", "four times", "fourfold")) {
      return visual("lift-speed-squared-ref-v1.svg", "PilotVault airspeed effect on lift and drag diagram")
    }
    if (has(q, "clmax", "critical angle", "stalling angle", "16°", "10° to 18°")) {
      return visual("critical-angle-stall-ref-v4.svg", "PilotVault critical angle of attack and stall diagram")
    }
    if (has(q, "reducing speed", "indicated airspeed is reduced") && has(q, "angle of attack")) {
      return visual("angle-of-attack-ref-v4.svg", "PilotVault angle of attack training diagram")
    }
    return null
  }

  if (topic === "Aileron Drag") {
    if (has(q, "differential aileron")) {
      return visual("differential-ailerons-ref-v1.svg", "PilotVault differential ailerons diagram")
    }
    if (has(q, "frise")) {
      return visual("frise-aileron-ref-v1.svg", "PilotVault Frise aileron diagram")
    }
    return visual("adverse-yaw-ref-v1.svg", "PilotVault adverse aileron yaw diagram")
  }

  if (topic === "Airspeed") {
    return visual("airspeed-chain-ref-v1.svg", "PilotVault IAS CAS RAS TAS relationship diagram")
  }

  if (topic === "Airspeed Limitations") {
    if (has(q, "va ", " va", "manoeuvring", "maneuvering")) {
      return visual("va-manoeuvring-speed-ref-v1.svg", "PilotVault design manoeuvring speed VA diagram")
    }
    if (has(q, "vx", "vy", "best angle", "best rate")) {
      return visual("vx-vy-ref-v2.svg", "PilotVault Vx and Vy climb-speed diagram")
    }
    return visual("airspeed-limitations-ref-v1.svg", "PilotVault common V-speeds and airspeed limitations diagram")
  }

  if (topic === "Basic Aerodynamics") {
    if (has(q, "newton's third", "newtons third", "newton third")) {
      return visual("newton-third-law-lift-ref-v1.svg", "PilotVault Newton third law action and reaction diagram")
    }
    if (has(q, "newton")) {
      return visual("newtons-laws-ref-v1.svg", "PilotVault Newton laws in flight diagram")
    }
    if (has(q, "venturi", "bernoulli", "continuity", "cross-sectional area")) {
      return visual("venturi-bernoulli-ref-v2.svg", "PilotVault Venturi and Bernoulli diagram")
    }
    if (has(q, "torque reaction")) {
      return visual("torque-reaction-ref-v1.svg", "PilotVault propeller torque reaction diagram")
    }
    if (has(q, "asymmetric blade", "p-factor", "right rudder")) {
      return visual("p-factor-ref-v1.svg", "PilotVault asymmetric propeller loading P-factor diagram")
    }
    if (has(q, "relative airflow")) {
      return visual("relative-airflow-ref-v3.svg", "PilotVault flight path and relative airflow diagram")
    }
    if (has(q, "pitch, roll and yaw", "pitch roll and yaw", "axes that pass", "centre of gravity") && has(q, "rotat")) {
      return visual("aircraft-axes-controls-ref-v2.svg", "PilotVault aircraft axes diagram")
    }
    if (has(q, "laminar flow", "boundary layer")) {
      return visual("boundary-layer-transition-ref-v1.svg", "PilotVault boundary layer and transition diagram")
    }
    if (has(q, "dynamic pressure", "total pressure", "static pressure", "stagnation point", "symbol is normally used for dynamic pressure")) {
      return visual("pressure-components-ref-v1.svg", "PilotVault static dynamic and total pressure diagram")
    }
    return null
  }

  if (topic === "Climb Performance") {
    if (has(q, "vx", "vy", "best angle", "best rate", "shortest distance", "shortest time", "clear obstacles", "obstacle")) {
      return visual("vx-vy-ref-v2.svg", "PilotVault Vx and Vy climb-speed diagram")
    }
    if (has(q, "lift is less than weight", "thrust is greater than drag", "forces acting", "arrangement of the four forces", "steady climb")) {
      return visual("steady-climb-forces-ref-v1.svg", "PilotVault steady climb forces diagram")
    }
    return null
  }

  if (topic === "Descent Performance") {
    if (has(q, "power", "rate of descent", "speed is kept constant", "constant speed", "reduce power", "reduced during a descent")) {
      return visual("power-rate-descent-ref-v1.svg", "PilotVault power and rate of descent diagram")
    }
    return null
  }

  if (topic === "Drag") {
    if (has(q, "figure below", "curve a", "curve b", "curve c", "position d", "position b", "minimum drag speed", "vmd", "total drag", "induced drag decreases", "parasite drag increases")) {
      return visual("drag-curves-ref-v1.svg", "PilotVault induced parasite and total drag curves")
    }
    if (has(q, "skin friction", "dust", "viscosity", "immediate contact with the surface")) {
      return visual("skin-friction-ref-v1.svg", "PilotVault skin friction and boundary layer diagram")
    }
    if (has(q, "pressure difference", "wingtip", "vortices", "produced as a result of", "lift produced by the wings")) {
      return visual("wingtip-vortices-ref-v1.svg", "PilotVault wingtip vortices and induced drag diagram")
    }
    if (has(q, "aspect ratio", "rectangular")) {
      return visual("aspect-ratio-ref-v1.svg", "PilotVault wing aspect ratio diagram")
    }
    if (has(q, "washout")) {
      return visual("washout-root-stall-ref-v1.svg", "PilotVault wing washout and root-first stall diagram")
    }
    if (has(q, "doubled", "50 kt to 100 kt", "four times", "fourfold")) {
      return visual("lift-speed-squared-ref-v1.svg", "PilotVault airspeed squared relationship diagram")
    }
    if (has(q, "induced drag", "parasite drag", "profile drag")) {
      return visual("drag-curves-ref-v1.svg", "PilotVault induced parasite and total drag curves")
    }
    return null
  }

  if (topic === "Flaps & Glide") {
    if (has(q, "fowler")) {
      return visual("fowler-flap-ref-v1.svg", "PilotVault Fowler flap diagram")
    }
    if (has(q, "slot", "leading-edge")) {
      return visual("leading-edge-slot-ref-v1.svg", "PilotVault leading-edge slot airflow diagram")
    }
    if (has(q, "headwind", "tailwind", "glide path over the ground", "gliding into wind")) {
      return visual("wind-glide-groundpath-ref-v1.svg", "PilotVault wind effect on glide over the ground diagram")
    }
    if (has(q, "centre of pressure", "center of pressure")) {
      return visual("flap-centre-pressure-ref-v1.svg", "PilotVault flap centre of pressure movement diagram")
    }
    if (has(q, "flapless", "no-flap", "no flap", "nose position", "landing speed")) {
      return visual("flap-vs-no-flap-ref-v1.svg", "PilotVault flap versus no-flap approach diagram")
    }
    if (has(q, "glide", "lift-to-drag", "lift/drag", "l/d", "gliding distance", "gliding angle", "rate of descent")) {
      return visual("glide-forces-ref-v1.svg", "PilotVault power-off glide forces diagram")
    }
    if (has(q, "flap", "wing surface area", "camber", "clmax", "critical angle")) {
      return visual("trailing-edge-flaps-ref-v1.svg", "PilotVault trailing-edge flap effects diagram")
    }
    return null
  }

  if (topic === "Flight Controls & Axes") {
    if (has(q, "rudder") && !has(q, "primary and further", "spiral dive", "followed by")) {
      return visual("rudder-effect-ref-v1.svg", "PilotVault rudder and yaw control diagram")
    }
    if (has(q, "aileron") && !has(q, "primary and further", "spiral dive", "followed by", "control column is moved forward and left")) {
      return visual("aileron-effect-ref-v1.svg", "PilotVault aileron and roll control diagram")
    }
    if (has(q, "axis", "axes", "pitch", "roll", "yaw") && !has(q, "control column is moved forward and left")) {
      return visual("aircraft-axes-controls-ref-v2.svg", "PilotVault aircraft axes and primary controls diagram")
    }
    return null
  }

  if (topic === "Four Forces") {
    if (has(q, "centre of gravity", "center of gravity", "centre of pressure", "center of pressure")) {
      return visual("cg-longitudinal-stability-ref-v1.svg", "PilotVault CG centre of pressure and pitch-stability diagram")
    }
    if (has(q, "lift equals weight", "thrust equals drag", "four forces", "equilibrium", "straight and level")) {
      return visual("four-forces-ref-v1.svg", "PilotVault four forces in level flight diagram")
    }
    if (has(q, "angle of attack")) {
      return visual("angle-of-attack-ref-v4.svg", "PilotVault angle of attack training diagram")
    }
    return null
  }

  if (topic === "ISA & Air Density") {
    if (has(q, "humidity", "humid", "water vapour", "water vapor")) {
      return visual("humidity-density-ref-v1.svg", "PilotVault humidity and air density diagram")
    }
    if (has(q, "nitrogen", "oxygen", "argon", "carbon dioxide", "gases in dry air")) {
      return visual("dry-air-composition-ref-v1.svg", "PilotVault dry air composition diagram")
    }
    if (has(q, "static pressure", "acts in all directions", "ambient air pressure", "immersed")) {
      return visual("static-pressure-ref-v1.svg", "PilotVault static pressure acts in all directions diagram")
    }
    if (has(q, "pressure is kept constant", "temperature is increased", "pressure increases", "density will decrease", "density increases", "temperature of a dry parcel")) {
      return visual("pressure-temperature-density-ref-v1.svg", "PilotVault pressure temperature density relationship diagram")
    }
    if (has(q, "isa", "standard atmosphere", "sea-level", "sea level", "lapse rate", "15°c", "1.98°c", "4,000 ft", "1225 grammes")) {
      return visual("isa-ref-v1.svg", "PilotVault International Standard Atmosphere diagram")
    }
    return null
  }

  if (topic === "Spins") {
    if (has(q, "recovery", "rudder is applied before elevator", "rudder before elevator")) {
      return visual("spin-recovery-sequence-ref-v1.svg", "PilotVault spin recovery aerodynamic principle diagram")
    }
    if (has(q, "autorotation", "inner wing", "outer wing", "left wing", "ailerons to the right", "delay spin")) {
      return visual("spin-autorotation-ref-v1.svg", "PilotVault spin autorotation diagram")
    }
    return null
  }

  if (topic === "Stability") {
    if (has(q, "dutch-roll", "dutch roll")) {
      return visual("dutch-roll-ref-v1.svg", "PilotVault Dutch roll diagram")
    }
    if (has(q, "longitudinal dihedral", "tailplane at a lower angle", "mainplane")) {
      return visual("longitudinal-dihedral-ref-v1.svg", "PilotVault longitudinal dihedral diagram")
    }
    if (has(q, "vertical fin", "directional stability", "keel surface", "normal axis")) {
      return visual("directional-stability-ref-v1.svg", "PilotVault vertical fin directional stability diagram")
    }
    if (has(q, "dihedral", "sideslip", "rolling plane", "lateral stability", "lower wing")) {
      return visual("dihedral-lateral-stability-ref-v1.svg", "PilotVault dihedral and lateral stability diagram")
    }
    if (has(q, "centre of gravity", "center of gravity", "cg too far", "cg is moved", "c of g") && !has(q, "landing must be checked")) {
      return visual("cg-longitudinal-stability-ref-v1.svg", "PilotVault centre of gravity and longitudinal stability diagram")
    }
    if (has(q, "positive stability", "negative stability", "neutral stability", "neutral static")) {
      return visual("static-stability-types-ref-v1.svg", "PilotVault positive neutral and negative static stability diagram")
    }
    if (has(q, "dynamically stable", "dynamic stability", "statically", "static stability", "oscillat")) {
      return visual("static-dynamic-stability-ref-v1.svg", "PilotVault static and dynamic stability diagram")
    }
    if (has(q, "centre of pressure", "center of pressure", "aerodynamic centre")) {
      return visual("cg-longitudinal-stability-ref-v1.svg", "PilotVault CG and centre of pressure pitch relationship diagram")
    }
    return null
  }

  if (topic === "Stalls") {
    if (has(q, "washout", "wingtip", "wing root", "root stall", "angle of incidence toward the wingtip")) {
      return visual("washout-root-stall-ref-v1.svg", "PilotVault root-first stall and washout diagram")
    }
    if (has(q, "stall warning", "buffet", "buffeting", "control effectiveness", "approach to a power off stall")) {
      return visual("stall-warning-ref-v1.svg", "PilotVault approaching stall and warning diagram")
    }
    if (has(q, "wing loading", "weight is increased", "stall at a higher ias", "turn", "stall speed", "stalling speed")) {
      return visual("bank-load-factor-ref-v2.svg", "PilotVault stall speed and load factor diagram")
    }
    if (has(q, "critical angle", "stalling angle", "will stall as a result", "stalls as a result", "10° to 18°", "centre of pressure tends")) {
      return visual("critical-angle-stall-ref-v4.svg", "PilotVault critical angle of attack and stall diagram")
    }
    return null
  }

  if (topic === "Trim & Balance Tabs") {
    if (has(q, "anti-balance", "anti-servo")) {
      return visual("anti-balance-tab-ref-v1.svg", "PilotVault anti-servo tab diagram")
    }
    if (has(q, "mass balance", "flutter")) {
      return visual("mass-balance-flutter-ref-v1.svg", "PilotVault mass balance and flutter diagram")
    }
    if (has(q, "horn balance", "hinge set back", "hinge set", "aerodynamically balanced")) {
      return visual("horn-balance-ref-v1.svg", "PilotVault aerodynamic horn balance diagram")
    }
    if (has(q, "balance tab")) {
      return visual("balance-tab-ref-v1.svg", "PilotVault balance tab movement diagram")
    }
    if (has(q, "trim tab", "adjustable trim", "selected angle relative")) {
      return visual("trim-tab-ref-v1.svg", "PilotVault trim tab principle diagram")
    }
    return null
  }

  if (topic === "Turns & Load Factor") {
    if (has(q, "ball", "slipping", "skidding", "slip indicator")) {
      return visual("slip-skid-ref-v1.svg", "PilotVault slip and skid indicator diagram")
    }
    if (has(q, "stall speed", "stalls at", "square root", "wing loading", "minimum speed")) {
      return visual("bank-load-factor-ref-v2.svg", "PilotVault stall speed and load factor diagram")
    }
    if (has(q, "bank angle", "60°", "60 degrees", "load factor", "gross weight", "structure support", "2.5 g", "3.8 g", "20°", "50°", "66°", "75°")) {
      return visual("bank-load-factor-ref-v2.svg", "PilotVault bank angle and load factor diagram")
    }
    if (has(q, "centripetal", "total lift", "vertical component", "horizontal component", "maintain altitude")) {
      return visual("turn-lift-components-ref-v2.svg", "PilotVault lift components in a level turn diagram")
    }
    return null
  }

  if (topic === "Weight & Balance") {
    return visual("centre-of-gravity-ref-v1.svg", "PilotVault centre of gravity diagram")
  }

  if (topic === "Wing Design") {
    if (has(q, "aspect ratio")) {
      return visual("aspect-ratio-ref-v1.svg", "PilotVault wing aspect ratio diagram")
    }
    if (has(q, "washout", "angle of incidence")) {
      return visual("washout-root-stall-ref-v1.svg", "PilotVault wing washout and root-first stall diagram")
    }
    if (has(q, "anhedral", "slopes downward")) {
      return visual("anhedral-ref-v1.svg", "PilotVault anhedral diagram")
    }
    return null
  }

  return null
}

export function PrinciplesOfFlightVisual({ question }: { question: Question }) {
  const asset = getStaticPofVisual(question)
  if (!asset) return null

  return (
    <figure className="mt-5 overflow-hidden border border-slate-200 bg-white">
      <img
        src={asset.src}
        alt={asset.alt}
        className="block h-auto w-full"
        loading="lazy"
        decoding="async"
      />
    </figure>
  )
}
