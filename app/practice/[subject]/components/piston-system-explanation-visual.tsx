"use client"

import type { ReactNode } from "react"

type Props = { visualKey: string; title?: string; caption?: string }

const BLUE = "#1f6fba"
const RED = "#d62828"
const LINE = "#15202b"

const TITLES: Record<string, string> = {
  "piston-system-valve-overlap": "VALVE OVERLAP",
  "piston-system-cht-probe": "CYLINDER HEAD TEMPERATURE",
  "piston-system-engine-baffles": "ENGINE COOLING BAFFLES",
  "piston-system-dense-air-power": "AIR DENSITY & ENGINE POWER",
}

export function PistonSystemExplanationVisual({ visualKey, title, caption }: Props) {
  const visual = getVisual(visualKey)
  if (!visual) return null
  return (
    <figure className="mx-auto mt-5 w-full max-w-[760px] overflow-hidden border border-slate-200 bg-white">
      <div className="border-b-4 border-[#f4b400] bg-[#06111f] px-4 py-3 text-center sm:px-6 sm:py-4">
        <div className="text-[10px] font-extrabold tracking-[0.2em] text-[#f4b400] sm:text-xs">PILOTVAULT AIRCRAFT TECHNICAL &amp; GENERAL</div>
        <div className="mt-1 text-lg font-extrabold uppercase tracking-[0.03em] text-white sm:text-2xl">{title?.trim() || TITLES[visualKey]}</div>
      </div>
      <div className="bg-white p-2 sm:p-4">{visual}</div>
      {caption && <figcaption className="border-t border-slate-200 bg-slate-50 px-4 py-3 text-center text-sm leading-relaxed text-slate-600 sm:px-6">{caption}</figcaption>}
    </figure>
  )
}

function Svg({ children }: { children: ReactNode }) {
  return (
    <svg viewBox="0 0 900 540" className="block h-auto w-full" aria-hidden="true">
      <defs>
        <marker id="ps-blue" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill={BLUE} /></marker>
        <marker id="ps-red" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill={RED} /></marker>
      </defs>
      <rect width="900" height="540" fill="white" />
      {children}
    </svg>
  )
}

function Text({ x, y, children, size = 24, fill = LINE, anchor = "middle" }: { x: number; y: number; children: ReactNode; size?: number; fill?: string; anchor?: "start" | "middle" | "end" }) {
  return <text x={x} y={y} fontSize={size} fontWeight={700} fill={fill} textAnchor={anchor} fontFamily="Arial, sans-serif">{children}</text>
}

function ValveOverlapVisual() {
  return (
    <Svg>
      <Text x={450} y={48} size={24}>BOTH VALVES ARE BRIEFLY OPEN AROUND TDC</Text>
      <rect x="270" y="110" width="360" height="320" rx="28" fill="#f8fafc" stroke={LINE} strokeWidth="6" />
      <rect x="320" y="155" width="70" height="135" rx="18" fill="#d8dee6" stroke={LINE} strokeWidth="5" />
      <rect x="510" y="155" width="70" height="135" rx="18" fill="#d8dee6" stroke={LINE} strokeWidth="5" />
      <line x1="355" y1="255" x2="355" y2="315" stroke={BLUE} strokeWidth="8" />
      <line x1="545" y1="255" x2="545" y2="315" stroke={RED} strokeWidth="8" />
      <Text x={355} y={140} size={19} fill={BLUE}>INLET OPEN</Text>
      <Text x={545} y={140} size={19} fill={RED}>EXHAUST OPEN</Text>
      <rect x="335" y="325" width="230" height="70" rx="18" fill="#e2e8f0" stroke={LINE} strokeWidth="5" />
      <Text x={450} y={372} size={22}>PISTON AT TDC</Text>
      <Text x={450} y={480} size={22}>Overlap improves scavenging and cylinder filling.</Text>
    </Svg>
  )
}

function ChtProbeVisual() {
  return (
    <Svg>
      <Text x={450} y={48} size={24}>MONITOR THE CYLINDER THAT RUNS HOTTEST</Text>
      {[170, 340, 510, 680].map((x, i) => (
        <g key={x}>
          <rect x={x - 55} y="170" width="110" height="200" rx="22" fill={i === 2 ? "#fff1f1" : "#f8fafc"} stroke={i === 2 ? RED : LINE} strokeWidth="5" />
          {[205, 240, 275, 310].map((y) => <line key={y} x1={x - 70} y1={y} x2={x + 70} y2={y} stroke="#94a3b8" strokeWidth="5" />)}
          <Text x={x} y={405} size={18}>CYL {i + 1}</Text>
        </g>
      ))}
      <circle cx="510" cy="150" r="16" fill={RED} />
      <line x1="510" y1="150" x2="510" y2="210" stroke={RED} strokeWidth="6" />
      <Text x={510} y={120} size={19} fill={RED}>CHT PROBE</Text>
      <Text x={450} y={475} size={21}>The hottest known cylinder provides the limiting temperature reference.</Text>
    </Svg>
  )
}

function EngineBafflesVisual() {
  return (
    <Svg>
      <Text x={450} y={48} size={24}>BAFFLES FORCE COOLING AIR THROUGH THE CYLINDER FINS</Text>
      <rect x="210" y="135" width="480" height="270" rx="28" fill="#f8fafc" stroke={LINE} strokeWidth="6" />
      <rect x="310" y="180" width="115" height="175" rx="22" fill="#d8dee6" stroke={LINE} strokeWidth="5" />
      <rect x="475" y="180" width="115" height="175" rx="22" fill="#d8dee6" stroke={LINE} strokeWidth="5" />
      {[210, 245, 280, 315].map((y) => <line key={y} x1="290" y1={y} x2="445" y2={y} stroke="#94a3b8" strokeWidth="5" />)}
      {[210, 245, 280, 315].map((y) => <line key={y} x1="455" y1={y} x2="610" y2={y} stroke="#94a3b8" strokeWidth="5" />)}
      <path d="M105 190 L250 190 L300 220" fill="none" stroke={BLUE} strokeWidth="8" markerEnd="url(#ps-blue)" />
      <path d="M105 265 L250 265 L300 280" fill="none" stroke={BLUE} strokeWidth="8" markerEnd="url(#ps-blue)" />
      <path d="M105 340 L250 340 L300 330" fill="none" stroke={BLUE} strokeWidth="8" markerEnd="url(#ps-blue)" />
      <path d="M260 145 L260 395" stroke={RED} strokeWidth="8" />
      <Text x={230} y={425} size={18} fill={RED}>BAFFLE</Text>
      <Text x={450} y={480} size={22}>Air is directed over and between the fins instead of bypassing them.</Text>
    </Svg>
  )
}

function DenseAirVisual() {
  return (
    <Svg>
      <Text x={450} y={48} size={24}>DENSER AIR DELIVERS MORE OXYGEN TO THE CYLINDERS</Text>
      <rect x="105" y="125" width="275" height="250" rx="26" fill="#eef7ff" stroke={BLUE} strokeWidth="5" />
      {[150, 190, 230, 270, 310, 345].flatMap((x) => [180, 230, 280, 330].map((y) => <circle key={`${x}-${y}`} cx={x} cy={y} r="7" fill={BLUE} />))}
      <Text x={242} y={405} size={20} fill={BLUE}>COLD • DRY • HIGH PRESSURE</Text>
      <path d="M395 250 L505 250" stroke={BLUE} strokeWidth="9" markerEnd="url(#ps-blue)" />
      <rect x="525" y="150" width="250" height="210" rx="28" fill="#f8fafc" stroke={LINE} strokeWidth="6" />
      <Text x={650} y={225} size={25}>MORE OXYGEN</Text>
      <Text x={650} y={280} size={32} fill={RED}>MORE POWER</Text>
      <Text x={450} y={480} size={22}>A normally aspirated engine produces its best power in dense air.</Text>
    </Svg>
  )
}

function getVisual(key: string) {
  switch (key) {
    case "piston-system-valve-overlap": return <ValveOverlapVisual />
    case "piston-system-cht-probe": return <ChtProbeVisual />
    case "piston-system-engine-baffles": return <EngineBafflesVisual />
    case "piston-system-dense-air-power": return <DenseAirVisual />
    default: return null
  }
}
