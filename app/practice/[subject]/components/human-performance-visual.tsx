"use client"

import {
  Activity,
  AlertTriangle,
  Brain,
  CircleGauge,
  Clock3,
  Ear,
  Eye,
  Gauge,
  HeartPulse,
  ListChecks,
  Moon,
  Plane,
  ShieldCheck,
  Sparkles,
  Sun,
  Target,
  Waves,
  Wind,
} from "lucide-react"

import type { Question } from "../types"

type VisualFamily =
  | "air"
  | "blood"
  | "vision"
  | "hearing"
  | "stress"
  | "pressure"
  | "gforce"
  | "motion"
  | "cockpit"
  | "fitness"
  | "co"
  | "circadian"
  | "information"
  | "airmanship"

type VisualSpec = {
  title: string
  family: VisualFamily
  left: string
  center: string
  right: string
  footer: string
}

const q = (question: Question) => question.question.toLowerCase()

function has(question: Question, ...terms: string[]) {
  const text = q(question)
  return terms.some((term) => text.includes(term.toLowerCase()))
}

function getVisualSpec(question: Question): VisualSpec {
  const answer = question.correctAnswer || "Key concept"

  if (has(question, "alveoli")) {
    return {
      title: "ALVEOLI GAS EXCHANGE",
      family: "air",
      left: "Alveoli\nHigh O₂ partial pressure",
      center: "DIFFUSION",
      right: "Blood\nO₂ binds to haemoglobin",
      footer: "Oxygen moves down its partial-pressure gradient from the alveoli into the blood.",
    }
  }

  if (has(question, "dalton")) {
    return {
      title: "DALTON’S LAW OF PARTIAL PRESSURES",
      family: "air",
      left: "Nitrogen\npartial pressure",
      center: "TOTAL PRESSURE",
      right: "Oxygen + other gases\npartial pressures",
      footer: "Total pressure equals the sum of the partial pressures of all gases present.",
    }
  }

  if (has(question, "largest proportion", "percentage of the atmosphere", "composition of dry atmospheric", "percentage composition")) {
    return {
      title: "ATMOSPHERIC COMPOSITION",
      family: "air",
      left: "N₂ ≈ 78%",
      center: "O₂ ≈ 21%",
      right: "Other gases ≈ 1%",
      footer: "The percentage composition stays nearly constant with altitude; total pressure falls.",
    }
  }

  if (has(question, "time of useful consciousness", "tuc")) {
    return {
      title: "TIME OF USEFUL CONSCIOUSNESS",
      family: "air",
      left: "Higher altitude",
      center: "LESS USABLE TIME",
      right: "Physical effort\nshortens TUC",
      footer: `Key exam answer: ${answer}`,
    }
  }

  if (has(question, "hypoxia", "cyanosis", "oxygen partial pressure", "oxygen available in each breath", "atmospheric pressure half", "36,000 ft")) {
    return {
      title: "HYPOXIA AND ALTITUDE",
      family: "air",
      left: "Altitude ↑",
      center: "O₂ PARTIAL PRESSURE ↓",
      right: "Brain performance ↓",
      footer: `Key exam answer: ${answer}`,
    }
  }

  if (has(question, "hyperventilation", "carbon dioxide level", "normal breathing rate", "gas can the body store")) {
    return {
      title: "HYPERVENTILATION AND CO₂",
      family: "air",
      left: "Breathing too fast / deep",
      center: "CO₂ FALLS",
      right: "Tingling · dizziness\nlight-headedness",
      footer: "Slow and control the breathing pattern; avoid unnecessary over-breathing.",
    }
  }

  if (has(question, "carbon monoxide", "exhaust", "heater system", "dangerous gas")) {
    return {
      title: "CARBON MONOXIDE HAZARD",
      family: "co",
      left: "Engine / exhaust leak",
      center: "CO ENTERS CABIN",
      right: "CO binds strongly\nto haemoglobin",
      footer: `Key exam answer: ${answer}`,
    }
  }

  if (has(question, "white blood cells")) {
    return {
      title: "WHITE BLOOD CELLS",
      family: "blood",
      left: "Pathogens",
      center: "IMMUNE DEFENCE",
      right: "White blood cells",
      footer: "White blood cells protect the body by identifying and fighting infection.",
    }
  }

  if (has(question, "clot", "platelet")) {
    return {
      title: "PLATELETS AND CLOTTING",
      family: "blood",
      left: "Damaged vessel",
      center: "PLATELETS",
      right: "Clot forms",
      footer: "Platelets help stop bleeding by forming the initial plug in a damaged blood vessel.",
    }
  }

  if (has(question, "haemoglobin", "iron", "anaemic", "anemia")) {
    return {
      title: "HAEMOGLOBIN AND OXYGEN TRANSPORT",
      family: "blood",
      left: "Iron-containing\nhaemoglobin",
      center: "CARRIES O₂",
      right: "Body tissues",
      footer: `Key exam answer: ${answer}`,
    }
  }

  if (has(question, "red blood cells", "arterial blood", "poorly oxygenated blood")) {
    return {
      title: "RED BLOOD CELLS AND OXYGEN",
      family: "blood",
      left: "Lungs",
      center: "RED BLOOD CELLS",
      right: "Body tissues",
      footer: `Key exam answer: ${answer}`,
    }
  }

  if (has(question, "blood pressure", "higher reading", "lower reading", "hypertension", "low blood pressure")) {
    return {
      title: "BLOOD PRESSURE",
      family: "blood",
      left: "Systolic\nheart contracts",
      center: "mmHg",
      right: "Diastolic\nheart relaxes",
      footer: `Key exam answer: ${answer}`,
    }
  }

  if (has(question, "heart", "pulse rate", "circulation", "fainting")) {
    return {
      title: "HEART AND CIRCULATION",
      family: "blood",
      left: "Right heart → lungs",
      center: "HEART",
      right: "Left heart → body",
      footer: `Key exam answer: ${answer}`,
    }
  }

  if (has(question, "angina", "severe chest pain", "mild chest pain")) {
    return {
      title: "CHEST PAIN: ANGINA VS HEART ATTACK",
      family: "blood",
      left: "Angina\ntemporary reduced flow",
      center: "CHEST PAIN",
      right: "Heart attack\nprolonged blockage",
      footer: `Key exam answer: ${answer}`,
    }
  }

  if (has(question, "hypoglycaemia", "low blood glucose")) {
    return {
      title: "LOW BLOOD GLUCOSE",
      family: "fitness",
      left: "Shaking · sweating",
      center: "GLUCOSE LOW",
      right: "Give fast-acting sugar\nif conscious",
      footer: `Key exam answer: ${answer}`,
    }
  }

  if (has(question, "iris", "light enters")) {
    return {
      title: "IRIS AND PUPIL CONTROL",
      family: "vision",
      left: "Bright light",
      center: "PUPIL SIZE",
      right: "Dim light",
      footer: "The iris changes pupil diameter to regulate the amount of light entering the eye.",
    }
  }

  if (has(question, "visual acuity", "fovea")) {
    return {
      title: "FOVEA AND VISUAL ACUITY",
      family: "vision",
      left: "Peripheral retina",
      center: "FOVEA\nsharpest vision",
      right: "Fine detail",
      footer: `Key exam answer: ${answer}`,
    }
  }

  if (has(question, "accommodation")) {
    return {
      title: "ACCOMMODATION",
      family: "vision",
      left: "Near object",
      center: "LENS CHANGES SHAPE",
      right: "Image focused\non retina",
      footer: "Accommodation is the eye changing lens shape to focus at different distances.",
    }
  }

  if (has(question, "retina", "rods and cones")) {
    return {
      title: "RETINA: RODS AND CONES",
      family: "vision",
      left: "Rods\ndim light / peripheral",
      center: "RETINA",
      right: "Cones\ncolour / fine detail",
      footer: `Key exam answer: ${answer}`,
    }
  }

  if (has(question, "myopia", "hypermetropia", "astigmatism", "long-sightedness", "short-sightedness")) {
    return {
      title: "REFRACTIVE ERRORS",
      family: "vision",
      left: "Myopia\nfocus before retina",
      center: "CORRECTIVE LENS",
      right: "Hypermetropia\nfocus behind retina",
      footer: `Key exam answer: ${answer}`,
    }
  }

  if (has(question, "dark adaptation", "faint object", "night", "rods")) {
    return {
      title: "NIGHT VISION AND DARK ADAPTATION",
      family: "vision",
      left: "Avoid bright light",
      center: "RODS ADAPT",
      right: "Use off-centre viewing",
      footer: `Key exam answer: ${answer}`,
    }
  }

  if (has(question, "autokinesis")) {
    return {
      title: "AUTOKINESIS",
      family: "vision",
      left: "Single fixed light",
      center: "DARK FEATURELESS VIEW",
      right: "Light appears to move",
      footer: "Use reliable external references and instruments rather than trusting the illusion.",
    }
  }

  if (has(question, "empty-field myopia")) {
    return {
      title: "EMPTY-FIELD MYOPIA",
      family: "vision",
      left: "No visual texture",
      center: "EYES FOCUS NEAR",
      right: "Distant traffic\nmay be missed",
      footer: "Actively scan and refocus on distant references.",
    }
  }

  if (has(question, "runway", "sloping cloud", "hazy", "dark, featureless terrain", "illusion")) {
    return {
      title: "VISUAL APPROACH ILLUSIONS",
      family: "vision",
      left: "Runway / terrain cue",
      center: "FALSE PERCEPTION",
      right: "Incorrect approach path",
      footer: `Key exam answer: ${answer}`,
    }
  }

  if (has(question, "bright light", "uv")) {
    return {
      title: "BRIGHT LIGHT AND UV EXPOSURE",
      family: "vision",
      left: "Altitude ↑",
      center: "UV EXPOSURE ↑",
      right: "Eye tissue risk ↑",
      footer: "Quality sunglasses reduce glare and ultraviolet exposure.",
    }
  }

  if (has(question, "eustachian", "cochlea", "ossicles", "auditory nerve", "sections of the ear", "conductive hearing")) {
    return {
      title: "EAR ANATOMY AND HEARING",
      family: "hearing",
      left: "Outer / middle ear",
      center: "COCHLEA",
      right: "Auditory nerve\n→ brain",
      footer: `Key exam answer: ${answer}`,
    }
  }

  if (has(question, "semicircular", "otolith", "vestibular", "vertigo", "spatial orientation")) {
    return {
      title: "VESTIBULAR SYSTEM",
      family: "hearing",
      left: "Semicircular canals\nangular acceleration",
      center: "INNER EAR",
      right: "Otolith organs\nlinear acceleration",
      footer: `Key exam answer: ${answer}`,
    }
  }

  if (has(question, "leans", "forward acceleration", "upward vertical acceleration", "spatial disorientation")) {
    return {
      title: "SPATIAL DISORIENTATION",
      family: "motion",
      left: "Body sensation",
      center: "CAN BE MISLEADING",
      right: "Trust instruments",
      footer: `Key exam answer: ${answer}`,
    }
  }

  if (has(question, "tinnitus", "presbycusis", "noise-induced", "audible frequency", "noise above")) {
    return {
      title: "HEARING AND NOISE EXPOSURE",
      family: "hearing",
      left: "Noise exposure",
      center: "INNER-EAR DAMAGE",
      right: "Hearing loss / tinnitus",
      footer: `Key exam answer: ${answer}`,
    }
  }

  if (has(question, "blocked sinuses", "valsalva")) {
    return {
      title: "PRESSURE EQUALISATION",
      family: "pressure",
      left: "Cabin pressure changes",
      center: "EQUALISE PRESSURE",
      right: "Ear / sinus discomfort ↓",
      footer: `Key exam answer: ${answer}`,
    }
  }

  if (has(question, "boyle")) {
    return {
      title: "BOYLE’S LAW",
      family: "pressure",
      left: "Pressure ↓",
      center: "GAS VOLUME ↑",
      right: "Temperature constant",
      footer: "For a fixed mass of gas at constant temperature, pressure and volume vary inversely.",
    }
  }

  if (has(question, "decompression sickness", "nitrogen bubbles", "bends", "chokes", "creeps")) {
    return {
      title: "DECOMPRESSION SICKNESS",
      family: "pressure",
      left: "Pressure falls",
      center: "N₂ BUBBLES FORM",
      right: "Skin · joints · lungs",
      footer: `Key exam answer: ${answer}`,
    }
  }

  if (has(question, "negative g", "positive g", "grey-out", "black-out", "red-out", "tunnel vision")) {
    return {
      title: "G-FORCES AND BLOOD FLOW",
      family: "gforce",
      left: "+G\nblood away from head",
      center: "BLOOD FLOW SHIFTS",
      right: "−G\nblood toward head",
      footer: `Key exam answer: ${answer}`,
    }
  }

  if (has(question, "motion sickness")) {
    return {
      title: "MOTION SICKNESS",
      family: "motion",
      left: "Eyes",
      center: "SENSORY CONFLICT",
      right: "Inner ear",
      footer: `Key exam answer: ${answer}`,
    }
  }

  if (has(question, "circadian", "jet lag", "body clock", "time zones", "24")) {
    return {
      title: "CIRCADIAN RHYTHM AND JET LAG",
      family: "circadian",
      left: "Light / darkness",
      center: "BODY CLOCK",
      right: "Sleep / alertness",
      footer: `Key exam answer: ${answer}`,
    }
  }

  if (has(question, "sleep", "insomnia", "fatigue", "acute stress", "chronic stress", "stressors", "arousal")) {
    return {
      title: "STRESS, FATIGUE AND SLEEP",
      family: "stress",
      left: "Too little arousal",
      center: "OPTIMUM PERFORMANCE",
      right: "Too much arousal",
      footer: `Key exam answer: ${answer}`,
    }
  }

  if (has(question, "selective attention", "chunking", "working memory", "perception", "mental overload", "memory", "judgement", "semantic", "episodic", "skill-based", "rule-based", "knowledge-based", "motor programme", "reflex")) {
    return {
      title: "HUMAN INFORMATION PROCESSING",
      family: "information",
      left: "Sense / perceive",
      center: "THINK + REMEMBER",
      right: "Decide / act",
      footer: `Key exam answer: ${answer}`,
    }
  }

  if (has(question, "confirmation bias", "hazardous attitude", "wrong physical action", "omits the final check", "pilot error")) {
    return {
      title: "ERROR TRAPS AND BIAS",
      family: "information",
      left: "Expectation",
      center: "CHECK THE EVIDENCE",
      right: "Correct action",
      footer: `Key exam answer: ${answer}`,
    }
  }

  if (has(question, "checklist")) {
    return {
      title: "CHECKLIST DISCIPLINE",
      family: "cockpit",
      left: "Stop / identify point",
      center: "RESTART SAFELY",
      right: "Complete before next phase",
      footer: `Key exam answer: ${answer}`,
    }
  }

  if (has(question, "instrument", "standard flight-instrument")) {
    return {
      title: "STANDARD FLIGHT-INSTRUMENT T",
      family: "cockpit",
      left: "Airspeed · attitude",
      center: "PRIMARY T",
      right: "Altimeter · heading",
      footer: `Key exam answer: ${answer}`,
    }
  }

  if (has(question, "eye-reference", "sits below", "sitting too high")) {
    return {
      title: "COCKPIT EYE-REFERENCE POSITION",
      family: "cockpit",
      left: "Too low",
      center: "CORRECT EYE LINE",
      right: "Too high",
      footer: `Key exam answer: ${answer}`,
    }
  }

  if (has(question, "aircraft controls", "analogue display", "design and arrangement")) {
    return {
      title: "COCKPIT DISPLAY AND CONTROL DESIGN",
      family: "cockpit",
      left: "Clear layout",
      center: "STANDARD + INTUITIVE",
      right: "Lower workload",
      footer: `Key exam answer: ${answer}`,
    }
  }

  if (has(question, "bmi", "body mass index", "obesity")) {
    return {
      title: "BODY MASS INDEX",
      family: "fitness",
      left: "Mass (kg)",
      center: "BMI = kg ÷ m²",
      right: "Height² (m²)",
      footer: `Key exam answer: ${answer}`,
    }
  }

  if (has(question, "donating blood", "scuba", "alcohol")) {
    return {
      title: "FITNESS-TO-FLY WAITING TIMES",
      family: "fitness",
      left: "Medical / dive / alcohol event",
      center: "WAIT THE REQUIRED TIME",
      right: "Return to flying safely",
      footer: `Key exam answer: ${answer}`,
    }
  }

  if (has(question, "gastroenteritis", "cold", "influenza", "fit or seizure", "nervous passenger")) {
    return {
      title: "FIT TO FLY",
      family: "fitness",
      left: "Assess condition",
      center: "SAFE TO OPERATE?",
      right: "Delay if impaired",
      footer: `Key exam answer: ${answer}`,
    }
  }

  if (has(question, "closed-loop", "feedback", "safest decision", "marginal", "crosswind")) {
    return {
      title: "AERONAUTICAL DECISION MAKING",
      family: "airmanship",
      left: "Plan",
      center: "ASSESS → ACT → REVIEW",
      right: "Feedback",
      footer: `Key exam answer: ${answer}`,
    }
  }

  if (has(question, "responsible for the safety", "competent pilot", "leadership quality", "dangerous")) {
    return {
      title: "AIRMANSHIP AND COMMAND RESPONSIBILITY",
      family: "airmanship",
      left: "Situational awareness",
      center: "PIC RESPONSIBILITY",
      right: "Assertive safe action",
      footer: `Key exam answer: ${answer}`,
    }
  }

  if (has(question, "head-on", "closing head-on", "time is available")) {
    return {
      title: "CLOSING TRAFFIC",
      family: "airmanship",
      left: "Aircraft A →",
      center: "CLOSURE RATE",
      right: "← Aircraft B",
      footer: `Key exam answer: ${answer}`,
    }
  }

  return {
    title: (question.topic || "HUMAN PERFORMANCE").toUpperCase(),
    family: "airmanship",
    left: "Recognise",
    center: answer.toUpperCase(),
    right: "Apply safely",
    footer: question.explanation.split("\n")[0] || `Key exam answer: ${answer}`,
  }
}

function FamilyIcon({ family }: { family: VisualFamily }) {
  const cls = "h-8 w-8"
  switch (family) {
    case "air": return <Wind className={cls} />
    case "blood": return <HeartPulse className={cls} />
    case "vision": return <Eye className={cls} />
    case "hearing": return <Ear className={cls} />
    case "stress": return <Brain className={cls} />
    case "pressure": return <Gauge className={cls} />
    case "gforce": return <Activity className={cls} />
    case "motion": return <Waves className={cls} />
    case "cockpit": return <ListChecks className={cls} />
    case "fitness": return <ShieldCheck className={cls} />
    case "co": return <AlertTriangle className={cls} />
    case "circadian": return <Clock3 className={cls} />
    case "information": return <Brain className={cls} />
    default: return <Plane className={cls} />
  }
}

function Diagram({ family }: { family: VisualFamily }) {
  if (family === "vision") {
    return (
      <svg viewBox="0 0 360 150" className="h-36 w-full" aria-hidden="true">
        <path d="M24 75 C86 12 274 12 336 75 C274 138 86 138 24 75Z" fill="#fff" stroke="#06111f" strokeWidth="5" />
        <circle cx="180" cy="75" r="43" fill="#dce7f2" stroke="#06111f" strokeWidth="4" />
        <circle cx="180" cy="75" r="20" fill="#06111f" />
        <circle cx="173" cy="68" r="6" fill="#fff" opacity=".9" />
        <path d="M275 75 H337" stroke="#f4b400" strokeWidth="7" strokeLinecap="round" />
      </svg>
    )
  }

  if (family === "blood") {
    return (
      <svg viewBox="0 0 360 150" className="h-36 w-full" aria-hidden="true">
        <path d="M180 126 C148 99 90 66 102 33 C113 3 151 13 180 42 C209 13 247 3 258 33 C270 66 212 99 180 126Z" fill="#06111f" />
        <path d="M24 75 H105 M255 75 H336" stroke="#f4b400" strokeWidth="8" strokeLinecap="round" />
        <path d="M91 62 L108 75 L91 88 M269 62 L252 75 L269 88" fill="none" stroke="#f4b400" strokeWidth="6" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    )
  }

  if (family === "hearing") {
    return (
      <svg viewBox="0 0 360 150" className="h-36 w-full" aria-hidden="true">
        <path d="M140 30 C90 25 70 62 83 95 C94 122 122 112 124 91 C126 74 112 66 102 73" fill="none" stroke="#06111f" strokeWidth="7" strokeLinecap="round" />
        <circle cx="230" cy="72" r="34" fill="none" stroke="#f4b400" strokeWidth="7" />
        <circle cx="250" cy="52" r="27" fill="none" stroke="#f4b400" strokeWidth="7" />
        <circle cx="250" cy="92" r="27" fill="none" stroke="#f4b400" strokeWidth="7" />
        <path d="M124 80 H194" stroke="#06111f" strokeWidth="6" strokeLinecap="round" />
      </svg>
    )
  }

  if (family === "circadian") {
    return (
      <div className="relative mx-auto flex h-36 w-36 items-center justify-center rounded-full border-[6px] border-[#06111f] bg-white">
        <Sun className="absolute -right-5 top-3 h-8 w-8 text-[#f4b400]" />
        <Moon className="absolute -left-5 bottom-3 h-8 w-8 text-[#06111f]" />
        <div className="absolute h-12 w-1 origin-bottom -translate-y-6 rotate-[35deg] rounded bg-[#06111f]" />
        <div className="absolute h-9 w-1 origin-bottom -translate-y-4 -rotate-[55deg] rounded bg-[#f4b400]" />
        <div className="h-3 w-3 rounded-full bg-[#06111f]" />
      </div>
    )
  }

  if (family === "gforce") {
    return (
      <svg viewBox="0 0 360 150" className="h-36 w-full" aria-hidden="true">
        <circle cx="180" cy="34" r="19" fill="#06111f" />
        <rect x="161" y="57" width="38" height="62" rx="16" fill="#06111f" />
        <path d="M145 28 V116 M145 116 L134 98 M145 116 L156 98" stroke="#f4b400" strokeWidth="7" strokeLinecap="round" strokeLinejoin="round" />
        <path d="M215 116 V28 M215 28 L204 46 M215 28 L226 46" stroke="#f4b400" strokeWidth="7" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    )
  }

  if (family === "pressure") {
    return (
      <svg viewBox="0 0 360 150" className="h-36 w-full" aria-hidden="true">
        <circle cx="105" cy="76" r="34" fill="#dce7f2" stroke="#06111f" strokeWidth="4" />
        <circle cx="255" cy="76" r="55" fill="#fff" stroke="#06111f" strokeWidth="4" />
        <path d="M145 75 H210" stroke="#f4b400" strokeWidth="7" strokeLinecap="round" />
        <path d="M196 62 L212 75 L196 88" fill="none" stroke="#f4b400" strokeWidth="6" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    )
  }

  if (family === "co") {
    return (
      <div className="flex h-36 items-center justify-center gap-5">
        <Plane className="h-14 w-14 text-[#06111f]" />
        <div className="text-3xl font-black text-[#f4b400]">CO</div>
        <HeartPulse className="h-14 w-14 text-[#06111f]" />
      </div>
    )
  }

  if (family === "cockpit") {
    return (
      <div className="grid h-36 grid-cols-3 gap-3 rounded-2xl bg-[#06111f] p-4">
        {[CircleGauge, Gauge, Target, CircleGauge, ListChecks, Gauge].map((Icon, index) => (
          <div key={index} className="flex items-center justify-center rounded-xl border border-white/15 bg-white/5 text-white">
            <Icon className={index === 4 ? "h-8 w-8 text-[#f4b400]" : "h-8 w-8"} />
          </div>
        ))}
      </div>
    )
  }

  if (family === "motion") {
    return (
      <div className="grid h-36 grid-cols-[1fr_auto_1fr] items-center gap-4">
        <div className="flex flex-col items-center gap-2 rounded-2xl border border-slate-200 bg-white p-4"><Eye className="h-9 w-9 text-[#06111f]" /><span className="text-xs font-bold text-slate-600">VISUAL</span></div>
        <AlertTriangle className="h-9 w-9 text-[#f4b400]" />
        <div className="flex flex-col items-center gap-2 rounded-2xl border border-slate-200 bg-white p-4"><Ear className="h-9 w-9 text-[#06111f]" /><span className="text-xs font-bold text-slate-600">VESTIBULAR</span></div>
      </div>
    )
  }

  if (family === "information" || family === "stress") {
    return (
      <svg viewBox="0 0 360 150" className="h-36 w-full" aria-hidden="true">
        <path d="M35 118 C90 112 109 45 176 60 C230 71 261 25 326 33" fill="none" stroke="#06111f" strokeWidth="6" strokeLinecap="round" />
        <circle cx="176" cy="60" r="11" fill="#f4b400" />
        <path d="M35 125 H326" stroke="#cbd5e1" strokeWidth="3" />
        <path d="M35 20 V125" stroke="#cbd5e1" strokeWidth="3" />
      </svg>
    )
  }

  return (
    <div className="flex h-36 items-center justify-center">
      <div className="flex h-24 w-24 items-center justify-center rounded-full bg-[#06111f] text-[#f4b400] shadow-sm">
        <FamilyIcon family={family} />
      </div>
    </div>
  )
}

function LabelCard({ label, dark = false }: { label: string; dark?: boolean }) {
  return (
    <div className={dark ? "rounded-2xl bg-[#06111f] p-4 text-center text-white" : "rounded-2xl border border-slate-200 bg-white p-4 text-center text-slate-800"}>
      {label.split("\n").map((line, index) => (
        <div key={index} className={index === 0 ? "font-extrabold" : "mt-1 text-sm opacity-75"}>{line}</div>
      ))}
    </div>
  )
}

export function HumanPerformanceVisual({ question }: { question: Question }) {
  const spec = getVisualSpec(question)

  return (
    <figure className="mt-5 overflow-hidden border border-slate-200 bg-white">
      <div className="bg-[#06111f] px-4 py-4 text-center sm:px-6 sm:py-5">
        <div className="text-[11px] font-extrabold tracking-[0.28em] text-[#f4b400] sm:text-xs">
          PILOTVAULT HUMAN PERFORMANCE
        </div>
        <div className="mt-1 text-lg font-black uppercase tracking-[0.03em] text-white sm:text-2xl">
          {spec.title}
        </div>
      </div>

      <div className="bg-[#f8fafc] p-4 sm:p-6">
        <div className="mx-auto max-w-3xl rounded-3xl border border-slate-200 bg-white p-4 shadow-sm sm:p-6">
          <Diagram family={spec.family} />

          <div className="mt-5 grid gap-3 sm:grid-cols-3">
            <LabelCard label={spec.left} />
            <LabelCard label={spec.center} dark />
            <LabelCard label={spec.right} />
          </div>

          <div className="mt-5 flex items-start gap-3 rounded-2xl border border-amber-200 bg-amber-50 px-4 py-3 text-sm leading-relaxed text-slate-700">
            <Sparkles className="mt-0.5 h-5 w-5 shrink-0 text-[#b77900]" />
            <span>{spec.footer}</span>
          </div>
        </div>
      </div>
    </figure>
  )
}
