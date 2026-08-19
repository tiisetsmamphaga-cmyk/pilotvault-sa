"use client"

import type { Question } from "../types"

type DiagramKind =
  | "flow"
  | "compare"
  | "atmosphere"
  | "altitude"
  | "gas-exchange"
  | "blood-pressure"
  | "circulation"
  | "eye"
  | "refraction"
  | "runway"
  | "night-vision"
  | "autokinesis"
  | "ear"
  | "vestibular"
  | "boyle"
  | "gforce"
  | "circadian"
  | "information"
  | "checklist"
  | "cockpit-eye"
  | "motion-conflict"
  | "fatigue"

type VisualSpec = {
  title: string
  kind: DiagramKind
  left?: string
  center?: string
  right?: string
  note: string
}

const questionText = (question: Question) => question.question.toLowerCase()

function has(question: Question, ...terms: string[]) {
  const text = questionText(question)
  return terms.some((term) => text.includes(term.toLowerCase()))
}

function getVisualSpec(question: Question): VisualSpec {
  const answer = question.correctAnswer || "Key concept"

  if (has(question, "alveoli")) {
    return {
      title: "ALVEOLI GAS EXCHANGE",
      kind: "gas-exchange",
      note: "O₂ diffuses from alveolar air into the blood while CO₂ diffuses in the opposite direction.",
    }
  }

  if (has(question, "largest proportion", "percentage of the atmosphere", "composition of dry atmospheric", "percentage composition")) {
    return {
      title: "COMPOSITION OF DRY AIR",
      kind: "atmosphere",
      note: "Dry air is approximately 78% nitrogen, 21% oxygen and 1% other gases.",
    }
  }

  if (has(question, "time of useful consciousness", "tuc")) {
    return {
      title: "TIME OF USEFUL CONSCIOUSNESS",
      kind: "altitude",
      left: "Altitude increases",
      center: "TUC decreases",
      right: "Act early",
      note: `Key exam point: ${answer}`,
    }
  }

  if (has(question, "hypoxia", "cyanosis", "oxygen partial pressure", "oxygen available in each breath", "atmospheric pressure half", "36,000 ft")) {
    return {
      title: "HYPOXIA WITH ALTITUDE",
      kind: "altitude",
      left: "Altitude increases",
      center: "O₂ partial pressure falls",
      right: "Performance deteriorates",
      note: `Key exam point: ${answer}`,
    }
  }

  if (has(question, "hyperventilation", "carbon dioxide level", "normal breathing rate", "gas can the body store")) {
    return {
      title: "HYPERVENTILATION",
      kind: "flow",
      left: "Over-breathing",
      center: "CO₂ falls",
      right: "Dizziness / tingling",
      note: "Reduce unnecessary over-breathing and regain a controlled breathing pattern.",
    }
  }

  if (has(question, "carbon monoxide", "exhaust", "heater system", "dangerous gas")) {
    return {
      title: "CARBON MONOXIDE HAZARD",
      kind: "flow",
      left: "Exhaust leak",
      center: "CO enters cabin",
      right: "O₂ carriage impaired",
      note: `Key exam point: ${answer}`,
    }
  }

  if (has(question, "dalton")) {
    return {
      title: "DALTON’S LAW",
      kind: "atmosphere",
      note: "Total pressure is the sum of the partial pressures of the gases in the mixture.",
    }
  }

  if (has(question, "blood pressure", "higher reading", "lower reading", "hypertension", "low blood pressure")) {
    return {
      title: "BLOOD PRESSURE",
      kind: "blood-pressure",
      note: `Key exam point: ${answer}`,
    }
  }

  if (has(question, "heart", "pulse rate", "circulation", "fainting", "ventricles", "atria")) {
    return {
      title: "HEART AND CIRCULATION",
      kind: "circulation",
      note: `Key exam point: ${answer}`,
    }
  }

  if (has(question, "white blood cells")) {
    return {
      title: "WHITE BLOOD CELLS",
      kind: "flow",
      left: "Pathogen",
      center: "Immune response",
      right: "Defence",
      note: "White blood cells identify and fight infection.",
    }
  }

  if (has(question, "platelet", "clot")) {
    return {
      title: "PLATELETS AND CLOTTING",
      kind: "flow",
      left: "Vessel damaged",
      center: "Platelets gather",
      right: "Clot forms",
      note: "Platelets help form the initial plug that limits blood loss.",
    }
  }

  if (has(question, "haemoglobin", "iron", "anaemic", "anemia", "red blood cells", "arterial blood", "poorly oxygenated blood")) {
    return {
      title: "OXYGEN TRANSPORT IN BLOOD",
      kind: "flow",
      left: "Lungs",
      center: "Haemoglobin + O₂",
      right: "Body tissues",
      note: `Key exam point: ${answer}`,
    }
  }

  if (has(question, "angina", "severe chest pain", "mild chest pain", "heart attack")) {
    return {
      title: "ANGINA AND HEART ATTACK",
      kind: "compare",
      left: "ANGINA\nTemporary reduced coronary flow",
      right: "HEART ATTACK\nProlonged blocked coronary flow",
      note: `Key exam point: ${answer}`,
    }
  }

  if (has(question, "hypoglycaemia", "low blood glucose")) {
    return {
      title: "LOW BLOOD GLUCOSE",
      kind: "flow",
      left: "Glucose falls",
      center: "Sweating / shaking",
      right: "Treat if conscious",
      note: `Key exam point: ${answer}`,
    }
  }

  if (has(question, "iris", "light enters")) {
    return {
      title: "IRIS AND PUPIL CONTROL",
      kind: "eye",
      left: "Bright light",
      right: "Dim light",
      note: "The iris changes pupil diameter to control how much light enters the eye.",
    }
  }

  if (has(question, "visual acuity", "fovea", "retina", "rods and cones")) {
    return {
      title: "RETINA, FOVEA, RODS AND CONES",
      kind: "eye",
      left: "Rods: dim / peripheral",
      right: "Cones: colour / detail",
      note: `Key exam point: ${answer}`,
    }
  }

  if (has(question, "accommodation")) {
    return {
      title: "ACCOMMODATION",
      kind: "refraction",
      left: "Near object",
      right: "Lens changes shape",
      note: "Accommodation is the change in lens shape used to focus objects at different distances.",
    }
  }

  if (has(question, "myopia", "hypermetropia", "astigmatism", "long-sightedness", "short-sightedness")) {
    return {
      title: "REFRACTIVE ERRORS",
      kind: "refraction",
      left: "Myopia: focus before retina",
      right: "Hypermetropia: focus behind retina",
      note: `Key exam point: ${answer}`,
    }
  }

  if (has(question, "dark adaptation", "faint object", "off-centre", "off center", "night vision", "rods")) {
    return {
      title: "NIGHT VISION",
      kind: "night-vision",
      note: `Key exam point: ${answer}`,
    }
  }

  if (has(question, "autokinesis")) {
    return {
      title: "AUTOKINESIS",
      kind: "autokinesis",
      note: "A stationary point of light can appear to move when viewed against a dark, featureless background.",
    }
  }

  if (has(question, "empty-field myopia")) {
    return {
      title: "EMPTY-FIELD MYOPIA",
      kind: "refraction",
      left: "No distant visual detail",
      right: "Eyes focus too near",
      note: "Actively scan and refocus on distant objects to avoid missing distant traffic.",
    }
  }

  if (has(question, "runway", "sloping cloud", "hazy", "dark, featureless terrain", "black hole", "illusion")) {
    return {
      title: "VISUAL APPROACH ILLUSIONS",
      kind: "runway",
      note: `Key exam point: ${answer}`,
    }
  }

  if (has(question, "bright light", "uv", "ultraviolet")) {
    return {
      title: "BRIGHT LIGHT AND UV",
      kind: "flow",
      left: "Altitude / sunlight",
      center: "UV exposure",
      right: "Eye protection",
      note: "Use good-quality sunglasses that reduce glare and ultraviolet exposure.",
    }
  }

  if (has(question, "eustachian", "cochlea", "ossicles", "auditory nerve", "sections of the ear", "conductive hearing")) {
    return {
      title: "EAR ANATOMY AND HEARING",
      kind: "ear",
      note: `Key exam point: ${answer}`,
    }
  }

  if (has(question, "semicircular", "otolith", "vestibular", "vertigo", "spatial orientation")) {
    return {
      title: "VESTIBULAR SYSTEM",
      kind: "vestibular",
      note: `Key exam point: ${answer}`,
    }
  }

  if (has(question, "leans", "forward acceleration", "upward vertical acceleration", "spatial disorientation", "somatogravic")) {
    return {
      title: "SPATIAL DISORIENTATION",
      kind: "motion-conflict",
      left: "Body sensation",
      center: "May be false",
      right: "Trust instruments",
      note: `Key exam point: ${answer}`,
    }
  }

  if (has(question, "tinnitus", "presbycusis", "noise-induced", "audible frequency", "noise above", "hearing loss")) {
    return {
      title: "NOISE AND HEARING",
      kind: "flow",
      left: "Noise exposure",
      center: "Inner-ear damage",
      right: "Hearing loss / tinnitus",
      note: `Key exam point: ${answer}`,
    }
  }

  if (has(question, "blocked sinuses", "valsalva", "eustachian tube")) {
    return {
      title: "PRESSURE EQUALISATION",
      kind: "ear",
      note: `Key exam point: ${answer}`,
    }
  }

  if (has(question, "boyle")) {
    return {
      title: "BOYLE’S LAW",
      kind: "boyle",
      note: "At constant temperature, a decrease in pressure causes a trapped gas volume to increase.",
    }
  }

  if (has(question, "decompression sickness", "nitrogen bubbles", "bends", "chokes", "creeps")) {
    return {
      title: "DECOMPRESSION SICKNESS",
      kind: "flow",
      left: "Pressure falls",
      center: "N₂ bubbles form",
      right: "Symptoms appear",
      note: `Key exam point: ${answer}`,
    }
  }

  if (has(question, "negative g", "positive g", "grey-out", "black-out", "red-out", "tunnel vision")) {
    return {
      title: "G-FORCES AND BLOOD FLOW",
      kind: "gforce",
      note: `Key exam point: ${answer}`,
    }
  }

  if (has(question, "motion sickness")) {
    return {
      title: "MOTION SICKNESS",
      kind: "motion-conflict",
      left: "Visual input",
      center: "Conflict",
      right: "Vestibular input",
      note: `Key exam point: ${answer}`,
    }
  }

  if (has(question, "circadian", "jet lag", "body clock", "time zones", "free-running")) {
    return {
      title: "CIRCADIAN RHYTHM",
      kind: "circadian",
      note: `Key exam point: ${answer}`,
    }
  }

  if (has(question, "sleep", "insomnia", "fatigue", "acute stress", "chronic stress", "stressors", "arousal", "rem", "slow-wave")) {
    return {
      title: "FATIGUE, STRESS AND SLEEP",
      kind: "fatigue",
      note: `Key exam point: ${answer}`,
    }
  }

  if (has(question, "motor programme", "selective attention", "knowledge-based", "skill-based", "rule-based", "short-term memory", "long-term memory", "decision", "perception", "error", "judgement", "attention", "information processing")) {
    return {
      title: "INFORMATION PROCESSING",
      kind: "information",
      note: `Key exam point: ${answer}`,
    }
  }

  if (has(question, "checklist", "interrupted")) {
    return {
      title: "CHECKLIST DISCIPLINE",
      kind: "checklist",
      note: `Key exam point: ${answer}`,
    }
  }

  if (has(question, "eye-reference", "eye reference", "sits below", "seating height")) {
    return {
      title: "COCKPIT EYE-REFERENCE POSITION",
      kind: "cockpit-eye",
      note: `Key exam point: ${answer}`,
    }
  }

  if (has(question, "pilot in command", "responsible for the safety", "airmanship", "discipline", "competent pilot", "pre-take-off", "take-off clearance")) {
    return {
      title: "AIRMANSHIP AND COCKPIT DISCIPLINE",
      kind: "checklist",
      note: `Key exam point: ${answer}`,
    }
  }

  return {
    title: "HUMAN PERFORMANCE KEY CONCEPT",
    kind: "flow",
    left: "Recognise the condition",
    center: "Apply the principle",
    right: "Choose the safest action",
    note: `Key exam point: ${answer}`,
  }
}

function TechnicalArrow() {
  return (
    <div className="hidden items-center sm:flex" aria-hidden="true">
      <div className="h-px w-8 bg-[#f4b400]" />
      <div className="h-0 w-0 border-y-[5px] border-l-[8px] border-y-transparent border-l-[#f4b400]" />
    </div>
  )
}

function FlowDiagram({ left, center, right }: Pick<VisualSpec, "left" | "center" | "right">) {
  const cells = [left, center, right].filter(Boolean) as string[]
  return (
    <div className="grid gap-3 sm:grid-cols-[1fr_auto_1fr_auto_1fr] sm:items-center">
      {cells.map((label, index) => (
        <div className="contents" key={`${label}-${index}`}>
          <div className={`border px-4 py-4 text-center text-sm font-semibold leading-relaxed ${index === 1 ? "border-[#06111f] bg-[#06111f] text-white" : "border-slate-300 bg-white text-slate-800"}`}>
            {label}
          </div>
          {index < cells.length - 1 && <TechnicalArrow />}
        </div>
      ))}
    </div>
  )
}

function CompareDiagram({ left, right }: Pick<VisualSpec, "left" | "right">) {
  return (
    <div className="grid overflow-hidden border border-slate-300 sm:grid-cols-2">
      <div className="whitespace-pre-line p-5 text-center text-sm font-semibold leading-relaxed text-slate-800">{left}</div>
      <div className="whitespace-pre-line border-t border-slate-300 bg-slate-50 p-5 text-center text-sm font-semibold leading-relaxed text-slate-800 sm:border-l sm:border-t-0">{right}</div>
    </div>
  )
}

function AtmosphereDiagram() {
  return (
    <div>
      <div className="flex h-16 overflow-hidden border border-[#06111f] text-xs font-bold text-white sm:text-sm">
        <div className="flex items-center justify-center bg-[#06111f]" style={{ width: "78%" }}>N₂ 78%</div>
        <div className="flex items-center justify-center bg-[#1f4e79]" style={{ width: "21%" }}>O₂ 21%</div>
        <div className="min-w-10 flex-1 bg-[#f4b400]" aria-label="Other gases approximately 1 percent" />
      </div>
      <div className="mt-2 flex justify-between text-xs text-slate-500"><span>Nitrogen</span><span>Oxygen</span><span>Other ≈ 1%</span></div>
    </div>
  )
}

function AltitudeDiagram({ left, center, right }: Pick<VisualSpec, "left" | "center" | "right">) {
  return (
    <div className="grid gap-5 sm:grid-cols-[110px_1fr] sm:items-center">
      <div className="relative mx-auto h-56 w-20 border-l-2 border-slate-900">
        {[0, 1, 2, 3, 4].map((tick) => <div key={tick} className="absolute left-0 h-px w-4 bg-slate-900" style={{ bottom: `${tick * 25}%` }} />)}
        <div className="absolute -left-2 -top-1 text-xs font-bold text-[#f4b400]">HIGH</div>
        <div className="absolute -bottom-1 left-5 text-xs font-bold text-slate-500">LOW</div>
        <div className="absolute left-8 top-1/2 -translate-y-1/2 -rotate-90 whitespace-nowrap text-xs font-semibold text-slate-600">ALTITUDE</div>
      </div>
      <FlowDiagram left={left} center={center} right={right} />
    </div>
  )
}

function GasExchangeDiagram() {
  return (
    <svg viewBox="0 0 720 250" className="h-auto w-full" role="img" aria-label="Alveolus and capillary gas exchange">
      <rect x="30" y="30" width="660" height="190" fill="#fff" stroke="#cbd5e1" strokeWidth="2" />
      <circle cx="220" cy="115" r="65" fill="#f8fafc" stroke="#06111f" strokeWidth="4" />
      <text x="220" y="108" textAnchor="middle" fontSize="20" fontWeight="700" fill="#06111f">ALVEOLUS</text>
      <text x="220" y="136" textAnchor="middle" fontSize="15" fill="#475569">higher O₂ partial pressure</text>
      <path d="M320 92 H480" stroke="#f4b400" strokeWidth="5" />
      <polygon points="480,92 464,82 464,102" fill="#f4b400" />
      <text x="400" y="78" textAnchor="middle" fontSize="16" fontWeight="700" fill="#92400e">O₂</text>
      <path d="M480 150 H320" stroke="#1f4e79" strokeWidth="4" />
      <polygon points="320,150 336,140 336,160" fill="#1f4e79" />
      <text x="400" y="176" textAnchor="middle" fontSize="16" fontWeight="700" fill="#1f4e79">CO₂</text>
      <rect x="500" y="70" width="150" height="95" fill="#f8fafc" stroke="#06111f" strokeWidth="3" />
      <text x="575" y="110" textAnchor="middle" fontSize="18" fontWeight="700" fill="#06111f">CAPILLARY</text>
      <text x="575" y="136" textAnchor="middle" fontSize="14" fill="#475569">blood</text>
    </svg>
  )
}

function BloodPressureDiagram() {
  return (
    <div className="grid gap-4 sm:grid-cols-2">
      <div className="border border-slate-300 p-5 text-center">
        <div className="mx-auto mb-3 h-32 w-10 border border-slate-400 p-1"><div className="h-[80%] w-full bg-[#1f4e79]" /></div>
        <div className="font-bold text-[#06111f]">SYSTOLIC</div><div className="mt-1 text-sm text-slate-600">heart contracts</div>
      </div>
      <div className="border border-slate-300 p-5 text-center">
        <div className="mx-auto mb-3 h-32 w-10 border border-slate-400 p-1"><div className="mt-[45%] h-[55%] w-full bg-[#f4b400]" /></div>
        <div className="font-bold text-[#06111f]">DIASTOLIC</div><div className="mt-1 text-sm text-slate-600">heart relaxes</div>
      </div>
    </div>
  )
}

function CirculationDiagram() {
  return (
    <svg viewBox="0 0 720 250" className="h-auto w-full" role="img" aria-label="Heart lungs and body circulation loop">
      <rect x="60" y="85" width="140" height="80" fill="#fff" stroke="#06111f" strokeWidth="3" />
      <rect x="290" y="75" width="140" height="100" fill="#06111f" />
      <rect x="520" y="85" width="140" height="80" fill="#fff" stroke="#06111f" strokeWidth="3" />
      <text x="130" y="132" textAnchor="middle" fontSize="20" fontWeight="700" fill="#06111f">LUNGS</text>
      <text x="360" y="132" textAnchor="middle" fontSize="20" fontWeight="700" fill="#fff">HEART</text>
      <text x="590" y="132" textAnchor="middle" fontSize="20" fontWeight="700" fill="#06111f">BODY</text>
      <path d="M200 105 H290" stroke="#1f4e79" strokeWidth="4" /><polygon points="290,105 275,96 275,114" fill="#1f4e79" />
      <path d="M430 105 H520" stroke="#f4b400" strokeWidth="4" /><polygon points="520,105 505,96 505,114" fill="#f4b400" />
      <path d="M520 155 H430" stroke="#1f4e79" strokeWidth="4" /><polygon points="430,155 445,146 445,164" fill="#1f4e79" />
      <path d="M290 155 H200" stroke="#f4b400" strokeWidth="4" /><polygon points="200,155 215,146 215,164" fill="#f4b400" />
    </svg>
  )
}

function EyeDiagram({ left, right }: Pick<VisualSpec, "left" | "right">) {
  return (
    <svg viewBox="0 0 720 260" className="h-auto w-full" role="img" aria-label="Simplified eye anatomy">
      <path d="M70 130 C180 35 500 35 650 130 C500 225 180 225 70 130Z" fill="#fff" stroke="#06111f" strokeWidth="4" />
      <circle cx="330" cy="130" r="58" fill="#dce7f2" stroke="#06111f" strokeWidth="3" />
      <circle cx="330" cy="130" r="22" fill="#06111f" />
      <path d="M495 72 Q565 130 495 188" fill="none" stroke="#1f4e79" strokeWidth="5" />
      <circle cx="522" cy="130" r="7" fill="#f4b400" />
      <text x="330" y="225" textAnchor="middle" fontSize="15" fill="#475569">IRIS / PUPIL</text>
      <text x="540" y="214" textAnchor="middle" fontSize="15" fill="#475569">RETINA / FOVEA</text>
      {left && <text x="125" y="35" fontSize="14" fontWeight="700" fill="#06111f">{left}</text>}
      {right && <text x="480" y="35" fontSize="14" fontWeight="700" fill="#06111f">{right}</text>}
    </svg>
  )
}

function RefractionDiagram({ left, right }: Pick<VisualSpec, "left" | "right">) {
  return (
    <div className="grid gap-4 sm:grid-cols-2">
      {[left || "Near focus", right || "Distant focus"].map((label, index) => (
        <div key={label} className="border border-slate-300 p-4">
          <svg viewBox="0 0 320 150" className="h-auto w-full" aria-hidden="true">
            <ellipse cx="200" cy="75" rx="85" ry="58" fill="#fff" stroke="#06111f" strokeWidth="3" />
            <ellipse cx="150" cy="75" rx={index === 0 ? 18 : 12} ry={index === 0 ? 38 : 30} fill="#dce7f2" stroke="#1f4e79" strokeWidth="3" />
            <path d="M20 45 L150 75 L265 75 M20 105 L150 75 L265 75" fill="none" stroke="#f4b400" strokeWidth="3" />
            <path d="M270 30 V120" stroke="#06111f" strokeWidth="4" />
          </svg>
          <div className="mt-2 text-center text-sm font-semibold text-slate-700">{label}</div>
        </div>
      ))}
    </div>
  )
}

function RunwayDiagram() {
  return (
    <svg viewBox="0 0 720 280" className="h-auto w-full" role="img" aria-label="Runway perspective and approach path">
      <rect width="720" height="280" fill="#f8fafc" />
      <polygon points="250,245 470,245 405,70 315,70" fill="#e2e8f0" stroke="#06111f" strokeWidth="3" />
      <line x1="360" y1="230" x2="360" y2="90" stroke="#fff" strokeWidth="6" strokeDasharray="24 20" />
      <path d="M95 210 Q210 140 315 110" fill="none" stroke="#f4b400" strokeWidth="5" />
      <polygon points="315,110 298,108 307,124" fill="#f4b400" />
      <text x="95" y="235" fontSize="15" fontWeight="700" fill="#06111f">APPROACH CUE</text>
      <text x="485" y="90" fontSize="14" fill="#475569">Runway width / slope / darkness</text>
      <text x="485" y="112" fontSize="14" fill="#475569">can distort perceived glide path</text>
    </svg>
  )
}

function NightVisionDiagram() {
  return (
    <svg viewBox="0 0 720 260" className="h-auto w-full" role="img" aria-label="Off-centre viewing at night">
      <rect width="720" height="260" fill="#06111f" />
      <circle cx="500" cy="110" r="7" fill="#fff" />
      <circle cx="430" cy="155" r="7" fill="#f4b400" />
      <line x1="430" y1="155" x2="500" y2="110" stroke="#f4b400" strokeWidth="2" strokeDasharray="7 7" />
      <text x="315" y="168" textAnchor="end" fontSize="15" fill="#f4b400">LOOK SLIGHTLY OFF-CENTRE</text>
      <text x="515" y="115" fontSize="14" fill="#fff">faint target</text>
      <text x="360" y="225" textAnchor="middle" fontSize="15" fill="#cbd5e1">Rods are more effective away from the central fovea in low light.</text>
    </svg>
  )
}

function AutokinesisDiagram() {
  return (
    <svg viewBox="0 0 720 250" className="h-auto w-full" role="img" aria-label="Autokinesis illusion">
      <rect width="720" height="250" fill="#06111f" />
      <circle cx="355" cy="120" r="8" fill="#fff" />
      <path d="M355 120 C410 80 440 150 500 95 C545 55 585 120 620 90" fill="none" stroke="#f4b400" strokeWidth="3" strokeDasharray="7 8" />
      <text x="355" y="155" textAnchor="middle" fontSize="15" fill="#fff">actual fixed light</text>
      <text x="520" y="190" textAnchor="middle" fontSize="15" fill="#f4b400">perceived movement</text>
    </svg>
  )
}

function EarDiagram() {
  return (
    <svg viewBox="0 0 720 250" className="h-auto w-full" role="img" aria-label="Simplified ear pathway">
      <path d="M80 115 C80 55 150 45 185 95 C210 130 185 180 145 170" fill="none" stroke="#06111f" strokeWidth="6" />
      <line x1="190" y1="115" x2="270" y2="115" stroke="#1f4e79" strokeWidth="5" />
      <circle cx="295" cy="115" r="18" fill="#f4b400" stroke="#06111f" strokeWidth="3" />
      <path d="M330 115 C365 75 430 80 430 125 C430 175 355 175 355 130 C355 100 405 100 405 128" fill="none" stroke="#06111f" strokeWidth="5" />
      <line x1="430" y1="125" x2="555" y2="90" stroke="#1f4e79" strokeWidth="4" />
      <line x1="295" y1="135" x2="265" y2="205" stroke="#06111f" strokeWidth="4" />
      <text x="125" y="220" textAnchor="middle" fontSize="14" fill="#475569">outer ear</text>
      <text x="295" y="220" textAnchor="middle" fontSize="14" fill="#475569">middle ear / Eustachian tube</text>
      <text x="405" y="220" textAnchor="middle" fontSize="14" fill="#475569">cochlea</text>
      <text x="565" y="82" fontSize="14" fill="#475569">auditory nerve</text>
    </svg>
  )
}

function VestibularDiagram() {
  return (
    <svg viewBox="0 0 720 260" className="h-auto w-full" role="img" aria-label="Semicircular canals and otolith organs">
      <circle cx="250" cy="125" r="70" fill="none" stroke="#06111f" strokeWidth="5" />
      <ellipse cx="250" cy="125" rx="30" ry="80" fill="none" stroke="#1f4e79" strokeWidth="5" transform="rotate(50 250 125)" />
      <ellipse cx="250" cy="125" rx="30" ry="80" fill="none" stroke="#f4b400" strokeWidth="5" transform="rotate(-50 250 125)" />
      <rect x="430" y="85" width="165" height="80" fill="#fff" stroke="#06111f" strokeWidth="3" />
      <circle cx="470" cy="125" r="13" fill="#f4b400" />
      <circle cx="510" cy="125" r="13" fill="#f4b400" />
      <circle cx="550" cy="125" r="13" fill="#f4b400" />
      <text x="250" y="225" textAnchor="middle" fontSize="15" fontWeight="700" fill="#06111f">SEMICIRCULAR CANALS</text>
      <text x="512" y="205" textAnchor="middle" fontSize="15" fontWeight="700" fill="#06111f">OTOLITH ORGANS</text>
      <text x="250" y="246" textAnchor="middle" fontSize="13" fill="#475569">angular acceleration</text>
      <text x="512" y="226" textAnchor="middle" fontSize="13" fill="#475569">linear acceleration / gravity</text>
    </svg>
  )
}

function BoyleDiagram() {
  return (
    <div className="grid gap-4 sm:grid-cols-2 sm:items-center">
      <div className="text-center">
        <div className="mx-auto flex h-24 w-24 items-center justify-center rounded-full border-4 border-[#06111f] text-sm font-bold">HIGH P</div>
        <div className="mt-2 text-sm text-slate-600">smaller gas volume</div>
      </div>
      <div className="text-center">
        <div className="mx-auto flex h-40 w-40 items-center justify-center rounded-full border-4 border-[#f4b400] text-sm font-bold">LOW P</div>
        <div className="mt-2 text-sm text-slate-600">larger gas volume</div>
      </div>
    </div>
  )
}

function GForceDiagram() {
  return (
    <div className="grid gap-4 sm:grid-cols-2">
      {[{ title: "+G", arrow: "↓", text: "blood shifts away from the head" }, { title: "−G", arrow: "↑", text: "blood shifts toward the head" }].map((item, index) => (
        <div key={item.title} className={`border p-5 text-center ${index === 0 ? "border-slate-300 bg-white" : "border-[#06111f] bg-[#06111f] text-white"}`}>
          <div className={`text-xl font-black ${index === 1 ? "text-[#f4b400]" : "text-[#06111f]"}`}>{item.title}</div>
          <div className="relative mx-auto my-4 h-32 w-16">
            <div className={`absolute left-1/2 top-0 h-10 w-10 -translate-x-1/2 rounded-full ${index === 0 ? "bg-[#06111f]" : "bg-white"}`} />
            <div className={`absolute left-1/2 top-11 h-20 w-8 -translate-x-1/2 ${index === 0 ? "bg-[#06111f]" : "bg-white"}`} />
            <div className="absolute left-[70%] top-9 text-5xl font-black text-[#f4b400]">{item.arrow}</div>
          </div>
          <div className="text-sm font-semibold">{item.text}</div>
        </div>
      ))}
    </div>
  )
}

function CircadianDiagram() {
  return (
    <div className="overflow-hidden border border-slate-300">
      <div className="grid grid-cols-4 text-center text-xs font-bold text-slate-600"><div className="p-2">00:00</div><div className="p-2">06:00</div><div className="p-2">12:00</div><div className="p-2">18:00</div></div>
      <div className="grid h-20 grid-cols-4"><div className="bg-[#06111f]" /><div className="bg-amber-100" /><div className="bg-amber-50" /><div className="bg-[#06111f]" /></div>
      <div className="border-t border-slate-300 p-3 text-center text-sm font-semibold text-slate-700">LIGHT / DARKNESS SYNCHRONISE THE BODY CLOCK</div>
    </div>
  )
}

function InformationDiagram() {
  return <FlowDiagram left="STIMULUS" center="PERCEPTION → DECISION" right="ACTION" />
}

function ChecklistDiagram() {
  return (
    <div className="border border-slate-300 p-4">
      {["1  Complete item", "2  Cross-check", "3  Continue sequence", "4  If interrupted: re-establish position"].map((item, index) => (
        <div key={item} className={`flex items-center gap-3 border-b border-slate-200 py-3 text-sm font-semibold last:border-b-0 ${index === 3 ? "text-[#92400e]" : "text-slate-800"}`}>
          <div className={`h-4 w-4 border ${index < 3 ? "border-[#1f4e79] bg-[#1f4e79]" : "border-[#f4b400]"}`} />
          <span>{item}</span>
        </div>
      ))}
    </div>
  )
}

function CockpitEyeDiagram() {
  return (
    <svg viewBox="0 0 720 260" className="h-auto w-full" role="img" aria-label="Cockpit eye reference and sight line">
      <path d="M80 210 H650" stroke="#06111f" strokeWidth="4" />
      <rect x="180" y="135" width="95" height="75" fill="#e2e8f0" stroke="#06111f" strokeWidth="3" />
      <circle cx="235" cy="98" r="18" fill="#06111f" />
      <line x1="253" y1="98" x2="620" y2="98" stroke="#f4b400" strokeWidth="4" strokeDasharray="10 8" />
      <line x1="620" y1="60" x2="620" y2="140" stroke="#1f4e79" strokeWidth="5" />
      <text x="235" y="240" textAnchor="middle" fontSize="14" fill="#475569">seat / eye position</text>
      <text x="535" y="83" textAnchor="middle" fontSize="14" fontWeight="700" fill="#92400e">correct sight line</text>
    </svg>
  )
}

function MotionConflictDiagram({ left, center, right }: Pick<VisualSpec, "left" | "center" | "right">) {
  return (
    <div className="grid gap-4 sm:grid-cols-[1fr_150px_1fr] sm:items-center">
      <div className="border border-slate-300 p-5 text-center"><div className="text-xs font-bold tracking-widest text-slate-500">INPUT 1</div><div className="mt-2 font-bold">{left}</div></div>
      <div className="border-2 border-[#f4b400] bg-amber-50 p-5 text-center text-sm font-black text-[#06111f]">{center}</div>
      <div className="border border-slate-300 p-5 text-center"><div className="text-xs font-bold tracking-widest text-slate-500">INPUT 2 / RESPONSE</div><div className="mt-2 font-bold">{right}</div></div>
    </div>
  )
}

function FatigueDiagram() {
  return (
    <div>
      <div className="relative h-44 border-b-2 border-l-2 border-slate-800">
        <svg viewBox="0 0 600 160" className="absolute inset-0 h-full w-full" preserveAspectRatio="none" aria-hidden="true">
          <path d="M0 40 C90 35 130 55 210 65 C300 75 350 95 430 110 C500 123 555 130 600 145" fill="none" stroke="#1f4e79" strokeWidth="5" />
        </svg>
        <div className="absolute left-2 top-2 text-xs font-bold text-slate-500">ALERTNESS</div>
        <div className="absolute bottom-2 right-3 text-xs font-bold text-slate-500">TIME / FATIGUE LOAD →</div>
      </div>
      <div className="mt-3 text-center text-sm font-semibold text-slate-700">Sleep loss, workload and circadian effects reduce sustained alertness.</div>
    </div>
  )
}

function renderDiagram(spec: VisualSpec) {
  switch (spec.kind) {
    case "compare": return <CompareDiagram left={spec.left} right={spec.right} />
    case "atmosphere": return <AtmosphereDiagram />
    case "altitude": return <AltitudeDiagram left={spec.left} center={spec.center} right={spec.right} />
    case "gas-exchange": return <GasExchangeDiagram />
    case "blood-pressure": return <BloodPressureDiagram />
    case "circulation": return <CirculationDiagram />
    case "eye": return <EyeDiagram left={spec.left} right={spec.right} />
    case "refraction": return <RefractionDiagram left={spec.left} right={spec.right} />
    case "runway": return <RunwayDiagram />
    case "night-vision": return <NightVisionDiagram />
    case "autokinesis": return <AutokinesisDiagram />
    case "ear": return <EarDiagram />
    case "vestibular": return <VestibularDiagram />
    case "boyle": return <BoyleDiagram />
    case "gforce": return <GForceDiagram />
    case "circadian": return <CircadianDiagram />
    case "information": return <InformationDiagram />
    case "checklist": return <ChecklistDiagram />
    case "cockpit-eye": return <CockpitEyeDiagram />
    case "motion-conflict": return <MotionConflictDiagram left={spec.left} center={spec.center} right={spec.right} />
    case "fatigue": return <FatigueDiagram />
    default: return <FlowDiagram left={spec.left} center={spec.center} right={spec.right} />
  }
}

export function HumanPerformanceVisual({ question }: { question: Question }) {
  const spec = getVisualSpec(question)

  return (
    <figure className="mt-5 overflow-hidden border border-slate-200 bg-white">
      <div className="bg-[#06111f] px-4 py-4 text-center sm:px-6 sm:py-5">
        <div className="text-[11px] font-extrabold tracking-[0.22em] text-[#f4b400] sm:text-xs">PILOTVAULT HUMAN PERFORMANCE</div>
        <div className="mt-1 text-lg font-extrabold uppercase tracking-[0.035em] text-white sm:text-2xl">{spec.title}</div>
      </div>

      <div className="bg-white p-4 sm:p-6">
        <div className="mx-auto max-w-3xl border border-slate-200 bg-[#f8fafc] p-4 sm:p-6">
          {renderDiagram(spec)}

          <div className="mt-5 border-t-2 border-[#f4b400] bg-white px-4 py-3 text-sm leading-relaxed text-slate-700">
            <span className="font-bold text-[#06111f]">EXAM NOTE: </span>{spec.note}
          </div>
        </div>
      </div>
    </figure>
  )
}
