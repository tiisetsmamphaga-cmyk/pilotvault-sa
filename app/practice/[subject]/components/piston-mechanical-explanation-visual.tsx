"use client"

import type { ReactNode } from "react"

type Props = { visualKey: string; title?: string; caption?: string }

const BLUE = "#1f6fba"
const RED = "#d62828"
const LINE = "#15202b"
const GOLD = "#d7a52d"

const TITLES: Record<string, string> = {
  "piston-mech-counterweights": "CRANKSHAFT COUNTERWEIGHTS",
  "piston-mech-lead-fouling": "LEAD-FOULED SPARK PLUG",
  "piston-mech-cowl-flaps": "COWL FLAPS",
  "piston-mech-ignition-timing": "IGNITION TIMING",
}

export function PistonMechanicalExplanationVisual({ visualKey, title, caption }: Props) {
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
        <marker id="pm-blue" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill={BLUE} /></marker>
        <marker id="pm-red" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill={RED} /></marker>
      </defs>
      <rect width="900" height="540" fill="white" />
      {children}
    </svg>
  )
}

function Text({ x, y, children, size = 24, fill = LINE, anchor = "middle" }: { x: number; y: number; children: ReactNode; size?: number; fill?: string; anchor?: "start" | "middle" | "end" }) {
  return <text x={x} y={y} fontSize={size} fontWeight={700} fill={fill} textAnchor={anchor} fontFamily="Arial, sans-serif">{children}</text>
}

function CounterweightsVisual() {
  return (
    <Svg>
      <Text x={450} y={48} size={24}>COUNTERWEIGHTS BALANCE ROTATING FORCES</Text>
      <line x1="180" y1="270" x2="720" y2="270" stroke={LINE} strokeWidth="22" strokeLinecap="round" />
      {[260, 450, 640].map((x) => <circle key={x} cx={x} cy="270" r="42" fill="#cbd5e1" stroke={LINE} strokeWidth="5" />)}
      <rect x="220" y="160" width="80" height="85" rx="20" fill="#94a3b8" stroke={LINE} strokeWidth="5" />
      <rect x="600" y="295" width="80" height="85" rx="20" fill="#94a3b8" stroke={LINE} strokeWidth="5" />
      <Text x={260} y={135} size={19}>COUNTERWEIGHT</Text>
      <Text x={640} y={415} size={19}>COUNTERWEIGHT</Text>
      <path d="M150 210 C115 245 115 295 150 330" fill="none" stroke={RED} strokeWidth="7" />
      <path d="M750 210 C785 245 785 295 750 330" fill="none" stroke={BLUE} strokeWidth="7" />
      <Text x={450} y={475} size={22}>Balancing reduces vibration loads on the crankshaft and bearings.</Text>
    </Svg>
  )
}

function LeadFoulingVisual() {
  return (
    <Svg>
      <Text x={450} y={48} size={24}>EXCESS LEAD DEPOSITS CAN FOUL THE PLUG</Text>
      <rect x="300" y="110" width="300" height="330" rx="34" fill="#f8fafc" stroke={LINE} strokeWidth="6" />
      <rect x="390" y="125" width="120" height="170" rx="24" fill="#e2e8f0" stroke={LINE} strokeWidth="5" />
      <line x1="450" y1="295" x2="450" y2="365" stroke={LINE} strokeWidth="12" />
      <line x1="395" y1="355" x2="425" y2="355" stroke={LINE} strokeWidth="10" />
      <circle cx="425" cy="355" r="18" fill="#b5651d" />
      <circle cx="470" cy="350" r="13" fill="#b5651d" />
      <circle cx="500" cy="370" r="10" fill="#b5651d" />
      <Text x={610} y={360} size={20} fill={RED} anchor="start">LEAD DEPOSITS</Text>
      <line x1="600" y1="350" x2="510" y2="355" stroke={RED} strokeWidth="4" />
      <Text x={450} y={485} size={22}>Use only the fuel grade approved for the engine.</Text>
    </Svg>
  )
}

function CowlFlapsVisual() {
  return (
    <Svg>
      <Text x={240} y={48} size={22} fill={BLUE}>OPEN</Text>
      <Text x={660} y={48} size={22} fill={RED}>CLOSED</Text>
      <rect x="100" y="135" width="280" height="245" rx="30" fill="#f8fafc" stroke={LINE} strokeWidth="5" />
      {[160, 220, 280, 340].map((y) => <path key={y} d={`M125 ${y} L330 ${y}`} stroke={BLUE} strokeWidth="8" markerEnd="url(#pm-blue)" />)}
      <line x1="335" y1="145" x2="370" y2="110" stroke={LINE} strokeWidth="9" />
      <Text x={240} y={425} size={20} fill={BLUE}>MORE COOLING AIR</Text>
      <rect x="520" y="135" width="280" height="245" rx="30" fill="#f8fafc" stroke={LINE} strokeWidth="5" />
      {[160, 220, 280, 340].map((y) => <path key={y} d={`M545 ${y} L725 ${y}`} stroke={BLUE} strokeWidth="5" />)}
      <line x1="735" y1="145" x2="770" y2="195" stroke={LINE} strokeWidth="9" />
      <Text x={660} y={425} size={20} fill={RED}>LESS COOLING AIR</Text>
      <Text x={450} y={490} size={22}>Cowl flaps regulate cooling airflow through the engine compartment.</Text>
    </Svg>
  )
}

function IgnitionTimingVisual() {
  return (
    <Svg>
      <Text x={450} y={48} size={24}>SPARK OCCURS AT A FIXED ANGLE BEFORE TDC</Text>
      <circle cx="450" cy="285" r="155" fill="#f8fafc" stroke={LINE} strokeWidth="6" />
      <line x1="450" y1="285" x2="450" y2="130" stroke={LINE} strokeWidth="6" />
      <Text x={450} y={105} size={20}>TDC</Text>
      <line x1="450" y1="285" x2="392" y2="142" stroke={RED} strokeWidth="8" />
      <circle cx="392" cy="142" r="12" fill={RED} />
      <Text x={320} y={145} size={21} fill={RED}>20–25° BTDC</Text>
      <path d="M420 125 A165 165 0 0 0 365 150" fill="none" stroke={RED} strokeWidth="6" markerEnd="url(#pm-red)" />
      <Text x={690} y={215} size={20} fill={BLUE}>RPM ↑</Text>
      <Text x={690} y={250} size={20}>spark angle unchanged</Text>
      <Text x={450} y={485} size={22}>Higher RPM increases spark frequency, not the specified crankshaft angle.</Text>
    </Svg>
  )
}

function getVisual(key: string) {
  switch (key) {
    case "piston-mech-counterweights": return <CounterweightsVisual />
    case "piston-mech-lead-fouling": return <LeadFoulingVisual />
    case "piston-mech-cowl-flaps": return <CowlFlapsVisual />
    case "piston-mech-ignition-timing": return <IgnitionTimingVisual />
    default: return null
  }
}
