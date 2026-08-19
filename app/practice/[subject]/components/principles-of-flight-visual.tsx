"use client"

import type { Question } from "../types"

type StaticVisual = {
  src: string
  alt: string
}

const ROOT = "/explanation-images/principles-of-flight/static-v4"

function visual(file: string, alt: string): StaticVisual {
  return { src: `${ROOT}/${file}`, alt }
}

function wording(question: Question) {
  return `${question.question} ${question.correctAnswer}`.toLowerCase()
}

function has(text: string, ...terms: string[]) {
  return terms.some((term) => text.includes(term.toLowerCase()))
}

/**
 * Curated Principles of Flight visual mapping.
 *
 * Important: this deliberately does NOT force an image onto every question.
 * A visual is returned only when a finished static training graphic directly
 * teaches the concept being tested. Question-reference figures remain separate.
 */
function getStaticPofVisual(question: Question): StaticVisual | null {
  const q = wording(question)
  const topic = question.topic ?? ""

  if (has(q, "wing polar", "polar diagram")) {
    return visual("wing-polar-v4.png", "PilotVault wing polar training diagram")
  }

  if (topic === "Aerofoils & Lift") {
    if (
      (has(q, "angle between") && has(q, "chord line") && has(q, "relative airflow")) ||
      has(q, "angle of attack of an aeroplane is the angle") ||
      has(q, "angle of attack is defined as")
    ) {
      return visual("angle-of-attack-ref-v4.svg", "PilotVault angle of attack training diagram")
    }

    if (has(q, "chord line") && !has(q, "angle of attack")) {
      return visual("aerofoil-geometry-ref-v2.svg", "PilotVault aerofoil geometry diagram")
    }

    if (has(q, "boundary layer", "transition point", "laminar-flow", "laminar flow")) {
      return visual("boundary-layer-transition-v5.png", "PilotVault boundary layer and transition diagram")
    }

    if (has(q, "centre of pressure", "center of pressure")) {
      if (has(q, "move forward", "moves forward", "increased", "increased in normal", "increased, the centre")) {
        return visual("centre-pressure-shift-v5.png", "PilotVault centre of pressure shift diagram")
      }
      return visual("centre-of-pressure-v4.png", "PilotVault centre of pressure diagram")
    }

    if (has(q, "pressure along the upper", "pressure distribution", "high pressure below", "higher air pressure below", "lower air pressure above")) {
      return visual("lift-pressure-distribution-ref-v1.svg", "PilotVault pressure distribution and lift diagram")
    }

    if (has(q, "perpendicular to the relative airflow", "definition of lift", "lift force produced", "lift acts perpendicular", "drag acts parallel")) {
      return visual("lift-drag-directions-ref-v2.svg", "PilotVault lift and drag direction diagram")
    }

    if (has(q, "airspeed is doubled", "speed is doubled", "v squared", "v²", "cl and v squared", "constant angle of attack, what happens to lift and drag when airspeed decreases")) {
      return visual("lift-speed-squared-v4.png", "PilotVault lift and airspeed squared diagram")
    }

    if (has(q, "clmax", "critical angle", "stalling angle", "16°", "-4°")) {
      return visual("critical-angle-stall-ref-v4.svg", "PilotVault critical angle of attack diagram")
    }

    if (has(q, "reducing speed", "indicated airspeed is reduced") && has(q, "angle of attack")) {
      return visual("angle-of-attack-ref-v4.svg", "PilotVault angle of attack training diagram")
    }

    return null
  }

  if (topic === "Aileron Drag") {
    if (has(q, "differential aileron")) {
      return visual("differential-ailerons-v4.png", "PilotVault differential ailerons diagram")
    }
    if (has(q, "frise")) {
      return visual("frise-aileron-v4.png", "PilotVault Frise aileron diagram")
    }
    return visual("adverse-yaw-v4.png", "PilotVault adverse aileron yaw diagram")
  }

  if (topic === "Airspeed") {
    return visual("airspeed-chain-v4.png", "PilotVault IAS CAS RAS TAS relationship diagram")
  }

  if (topic === "Airspeed Limitations") {
    if (has(q, "va ", " va", "manoeuvring", "maneuvering")) {
      return visual("va-envelope-v4.png", "PilotVault design manoeuvring speed VA diagram")
    }
    if (has(q, "vx", "vy", "best angle", "best rate")) {
      return visual("vx-vy-v7.png", "PilotVault Vx and Vy climb diagram")
    }
    return visual("v-speeds-v5.png", "PilotVault common V-speeds diagram")
  }

  if (topic === "Basic Aerodynamics") {
    if (has(q, "newton")) {
      return visual("newtons-laws-v4.png", "PilotVault Newton laws in flight diagram")
    }
    if (has(q, "venturi", "bernoulli", "continuity", "cross-sectional area")) {
      return visual("venturi-bernoulli-ref-v2.svg", "PilotVault Venturi and Bernoulli diagram")
    }
    if (has(q, "torque reaction")) {
      return visual("propeller-torque-reaction-v4.png", "PilotVault propeller torque reaction diagram")
    }
    if (has(q, "asymmetric blade", "p-factor", "right rudder")) {
      return visual("p-factor-v4.png", "PilotVault asymmetric blade effect P-factor diagram")
    }
    if (has(q, "relative airflow")) {
      return visual("relative-airflow-ref-v3.svg", "PilotVault relative airflow diagram")
    }
    if (has(q, "pitch, roll and yaw", "pitch roll and yaw", "axes that pass", "centre of gravity") && has(q, "rotat")) {
      return visual("aircraft-axes-controls-ref-v2.svg", "PilotVault aircraft axes diagram")
    }
    if (has(q, "laminar flow", "boundary layer")) {
      return visual("boundary-layer-transition-v5.png", "PilotVault boundary layer and transition diagram")
    }
    if (has(q, "dynamic pressure", "total pressure", "static pressure", "stagnation point", "symbol is normally used for dynamic pressure")) {
      return visual("dynamic-pressure-v4.png", "PilotVault static dynamic and total pressure diagram")
    }
    return null
  }

  if (topic === "Climb Performance") {
    if (has(q, "vx", "vy", "best angle", "best rate", "shortest distance", "shortest time", "clear obstacles", "obstacle")) {
      return visual("vx-vy-v7.png", "PilotVault Vx and Vy climb diagram")
    }
    if (has(q, "lift is less than weight", "thrust is greater than drag", "forces acting", "arrangement of the four forces", "steady climb")) {
      return visual("steady-climb-forces-ref-v1.svg", "PilotVault steady climb force diagram")
    }
    return null
  }

  if (topic === "Descent Performance") {
    return visual("power-rate-of-descent-v4.png", "PilotVault power and rate of descent diagram")
  }

  if (topic === "Drag") {
    if (has(q, "figure below", "curve a", "curve b", "curve c", "position d", "position b", "minimum drag speed", "vmd", "total drag", "induced drag decreases", "parasite drag increases")) {
      return visual("drag-curves-ref-v1.svg", "PilotVault induced parasite and total drag curves")
    }
    if (has(q, "skin friction", "dust", "viscosity", "immediate contact with the surface")) {
      return visual("skin-friction-ref-v1.svg", "PilotVault form drag and skin friction diagram")
    }
    if (has(q, "pressure difference", "wingtip", "vortices", "produced as a result of", "lift produced by the wings")) {
      return visual("wingtip-vortices-induced-drag-v6.png", "PilotVault wingtip vortices and induced drag diagram")
    }
    if (has(q, "aspect ratio", "rectangular")) {
      return visual("aspect-ratio-v4.png", "PilotVault aspect ratio and induced drag diagram")
    }
    if (has(q, "washout")) {
      return visual("washout-v4.png", "PilotVault wing washout diagram")
    }
    if (has(q, "doubled", "50 kt to 100 kt", "four times", "fourfold")) {
      return visual("lift-speed-squared-v4.png", "PilotVault speed squared relationship diagram")
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
      return visual("leading-edge-slot-v4.png", "PilotVault leading-edge slot airflow diagram")
    }
    if (has(q, "headwind", "tailwind", "glide path over the ground")) {
      return visual("wind-glide-groundpath-v7.png", "PilotVault wind effect on glide over the ground diagram")
    }
    if (has(q, "centre of pressure", "center of pressure", "pitching tendency")) {
      return visual("flap-centre-pressure-pitch-v4.png", "PilotVault flap centre of pressure and pitch diagram")
    }
    if (has(q, "flapless", "no-flap", "no flap", "nose position", "landing speed")) {
      return visual("flap-vs-no-flap-approach-v4.png", "PilotVault flap versus no-flap approach diagram")
    }
    if (has(q, "glide", "lift-to-drag", "lift/drag", "l/d", "gliding distance", "gliding angle", "rate of descent")) {
      return visual("glide-forces-ref-v1.svg", "PilotVault power-off glide force diagram")
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
    if (has(q, "centre of gravity", "center of gravity", "centre of pressure", "center of pressure", "nose to drop", "nose pitches", "pitch effect")) {
      return visual("cg-longitudinal-stability-ref-v1.svg", "PilotVault CG centre of pressure and pitch diagram")
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
    if (has(q, "humidity", "humid")) {
      return visual("humidity-density-v4.png", "PilotVault humidity and air density diagram")
    }
    if (has(q, "nitrogen", "oxygen", "argon", "carbon dioxide", "gases in dry air")) {
      return visual("dry-air-composition-v4.png", "PilotVault dry air composition diagram")
    }
    if (has(q, "static pressure", "acts in all directions", "ambient air pressure")) {
      return visual("static-pressure-v7.png", "PilotVault static pressure diagram")
    }
    if (has(q, "pressure is kept constant", "temperature is increased", "pressure increases", "density will decrease", "density increases")) {
      return visual("pressure-temperature-density-v4.png", "PilotVault pressure temperature density relationship diagram")
    }
    if (has(q, "isa", "standard atmosphere", "sea-level", "sea level", "lapse rate", "15°c", "1.98°c", "4,000 ft")) {
      return visual("isa-v4.png", "PilotVault International Standard Atmosphere diagram")
    }
    return null
  }

  if (topic === "Spins") {
    if (has(q, "recovery", "rudder is applied before elevator", "rudder before elevator")) {
      return visual("spin-recovery-v4.png", "PilotVault spin recovery aerodynamic principle diagram")
    }
    if (has(q, "autorotation", "inner wing", "outer wing", "left wing", "ailerons to the right", "delay spin")) {
      return visual("spin-autorotation-v5.png", "PilotVault spin autorotation diagram")
    }
    return null
  }

  if (topic === "Stability") {
    if (has(q, "dutch-roll", "dutch roll")) {
      return visual("dutch-roll-v4.png", "PilotVault Dutch roll diagram")
    }
    if (has(q, "longitudinal dihedral", "tailplane at a lower angle", "mainplane")) {
      return visual("longitudinal-dihedral-v4.png", "PilotVault longitudinal dihedral diagram")
    }
    if (has(q, "vertical fin", "directional stability", "keel surface", "normal axis")) {
      return visual("directional-stability-ref-v1.svg", "PilotVault vertical fin directional stability diagram")
    }
    if (has(q, "dihedral", "sideslip", "rolling plane", "lateral stability", "lower wing")) {
      return visual("dihedral-lateral-stability-v4.png", "PilotVault dihedral and lateral stability diagram")
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
      return visual("root-first-stall-washout-v4.png", "PilotVault root-first stall and washout diagram")
    }
    if (has(q, "stall warning", "buffet", "buffeting", "control effectiveness")) {
      return visual("stall-warning-v4.png", "PilotVault approaching stall and warning diagram")
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
      return visual("anti-servo-tab-v4.png", "PilotVault anti-servo tab diagram")
    }
    if (has(q, "mass balance", "flutter")) {
      return visual("mass-balance-flutter-v4.png", "PilotVault mass balance and flutter diagram")
    }
    if (has(q, "horn balance", "hinge set back", "hinge set", "aerodynamically balanced")) {
      return visual("horn-balance-v4.png", "PilotVault aerodynamic horn balance diagram")
    }
    if (has(q, "balance tab")) {
      return visual("balance-tab-v4.png", "PilotVault balance tab movement diagram")
    }
    if (has(q, "trim tab", "adjustable trim", "selected angle relative")) {
      return visual("trim-tab-ref-v1.svg", "PilotVault trim tab principle diagram")
    }
    return null
  }

  if (topic === "Turns & Load Factor") {
    if (has(q, "ball", "slipping", "skidding", "slip indicator")) {
      return visual("slip-skid-indicator-v4.png", "PilotVault slip skid indicator diagram")
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
      return visual("aspect-ratio-v4.png", "PilotVault aspect ratio diagram")
    }
    if (has(q, "washout", "angle of incidence")) {
      return visual("washout-v4.png", "PilotVault washout and incidence diagram")
    }
    if (has(q, "anhedral", "slopes downward")) {
      return visual("anhedral-v4.png", "PilotVault anhedral diagram")
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
