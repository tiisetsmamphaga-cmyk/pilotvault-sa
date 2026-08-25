"use client"

import type { ReactNode } from "react"

type PistonExplanationVisualProps = {
  visualKey: string
  title?: string
  caption?: string
}

const BLUE = "#1f6fba"
const RED = "#d62828"
const LINE = "#15202b"
const FUEL = "#e8b33d"

const TITLES: Record<string, string> = {
  "piston-mixture-rich-lean": "RICH VS LEAN MIXTURE",
  "piston-valve-lead": "VALVE LEAD",
  "piston-primer": "MANUAL PRIMER",
  "piston-flooded-start": "FLOODED ENGINE START",
  "piston-smooth-throttle": "SMOOTH THROTTLE MOVEMENT",
  "piston-carb-icing": "CARBURETTOR ICING",
  "piston-alternate-air": "FUEL INJECTION — ALTERNATE AIR",
  "piston-accelerator-pump": "ACCELERATOR PUMP",
}

export function PistonExplanationVisual({ visualKey, title, caption }: PistonExplanationVisualProps) {
  const visual = getVisual(visualKey)
  if (!visual) return null

  return (
    <figure className="mx-auto mt-5 w-full max-w-[760px] overflow-hidden border border-slate-200 bg-white">
      <div className="border-b-4 border-[#f4b400] bg-[#06111f] px-4 py-3 text-center sm:px-6 sm:py-4">
        <div className="text-[10px] font-extrabold tracking-[0.2em] text-[#f4b400] sm:text-xs">
          PILOTVAULT AIRCRAFT TECHNICAL &amp; GENERAL
        </div>
        <div className="mt-1 text-lg font-extrabold uppercase tracking-[0.03em] text-white sm:text-2xl">
          {title?.trim() || TITLES[visualKey] || "PISTON ENGINE"}
        </div>
      </div>
      <div className="bg-white p-2 sm:p-4">{visual}</div>
      {caption && (
        <figcaption className="border-t border-slate-200 bg-slate-50 px-4 py-3 text-center text-sm leading-relaxed text-slate-600 sm:px-6">
          {caption}
        </figcaption>
      )}
    </figure>
  )
}

function Svg({ children }: { children: ReactNode }) {
  return (
    <svg viewBox="0 0 900 540" className="block h-auto w-full" aria-hidden="true">
      <defs>
        <marker id="piston-arrow-blue" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto">
          <path d="M0,0 L0,6 L9,3 z" fill={BLUE} />
        </marker>
        <marker id="piston-arrow-red" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto">
          <path d="M0,0 L0,6 L9,3 z" fill={RED} />
        </marker>
      </defs>
      <rect x="0" y="0" width="900" height="540" fill="white" />
      {children}
    </svg>
  )
}

function Text({ x, y, children, size = 24, fill = LINE, anchor = "middle" }: { x: number; y: number; children: ReactNode; size?: number; fill?: string; anchor?: "start" | "middle" | "end" }) {
  return <text x={x} y={y} fontSize={size} fontWeight={700} fill={fill} textAnchor={anchor} fontFamily="Arial, sans-serif">{children}</text>
}

function MixtureVisual() {
  return (
    <Svg>
      <Text x={240} y={52} size={24} fill={RED}>RICH</Text>
      <Text x={660} y={52} size={24} fill={BLUE}>LEAN</Text>
      <rect x="115" y="125" width="250" height="225" rx="26" fill="#f8fafc" stroke={LINE} strokeWidth="5" />
      <rect x="535" y="125" width="250" height="225" rx="26" fill="#f8fafc" stroke={LINE} strokeWidth="5" />
      <path d="M150 180 L330 180" stroke={BLUE} strokeWidth="8" markerEnd="url(#piston-arrow-blue)" />
      <path d="M150 250 L330 250" stroke={RED} strokeWidth="15" markerEnd="url(#piston-arrow-red)" />
      <Text x={240} y={160} size={19} fill={BLUE}>AIR</Text>
      <Text x={240} y={305} size={19} fill={RED}>MORE FUEL</Text>
      <path d="M570 180 L750 180" stroke={BLUE} strokeWidth="8" markerEnd="url(#piston-arrow-blue)" />
      <path d="M570 250 L750 250" stroke={RED} strokeWidth="7" markerEnd="url(#piston-arrow-red)" />
      <Text x={660} y={160} size={19} fill={BLUE}>AIR</Text>
      <Text x={660} y={305} size={19} fill={RED}>LESS FUEL</Text>
      <Text x={240} y={405} size={20}>Fuel-to-air ratio increases</Text>
      <Text x={660} y={405} size={20}>Fuel-to-air ratio decreases</Text>
      <Text x={450} y={485} size={22}>Mixture control changes fuel flow for the available airflow.</Text>
    </Svg>
  )
}

function ValveLeadVisual() {
  return (
    <Svg>
      <Text x={450} y={46} size={24}>INLET VALVE OPENS BEFORE TDC</Text>
      <rect x="270" y="115" width="360" height="305" rx="28" fill="#f8fafc" stroke={LINE} strokeWidth="6" />
      <circle cx="450" cy="265" r="115" fill="white" stroke="#94a3b8" strokeWidth="4" />
      <line x1="450" y1="265" x2="450" y2="170" stroke={LINE} strokeWidth="10" />
      <circle cx="450" cy="265" r="18" fill="#64748b" />
      <Text x={450} y={135} size={21}>TDC</Text>
      <rect x="335" y="90" width="48" height="90" rx="12" fill="#d8dee6" stroke={LINE} strokeWidth="5" />
      <line x1="359" y1="170" x2="359" y2="215" stroke={RED} strokeWidth="7" />
      <path d="M350 212 L368 212 L359 232 Z" fill={RED} />
      <Text x={315} y={75} size={20} anchor="start">INLET VALVE</Text>
      <path d="M450 95 A170 170 0 0 0 320 150" fill="none" stroke={BLUE} strokeWidth="7" markerEnd="url(#piston-arrow-blue)" />
      <Text x={575} y={105} size={19} fill={BLUE}>BEFORE TDC</Text>
      <Text x={450} y={465} size={22}>Opening slightly early helps establish induction flow for the next stroke.</Text>
    </Svg>
  )
}

function PrimerVisual() {
  return (
    <Svg>
      <Text x={450} y={48} size={24}>PRIMER BYPASSES NORMAL CARBURETTOR METERING</Text>
      <rect x="90" y="150" width="190" height="210" rx="28" fill="#fff8e7" stroke={LINE} strokeWidth="5" />
      <rect x="105" y="245" width="160" height="95" fill={FUEL} opacity="0.9" />
      <Text x={185} y={385} size={20}>FUEL TANK</Text>
      <path d="M280 275 L380 275" stroke={RED} strokeWidth="8" markerEnd="url(#piston-arrow-red)" />
      <rect x="380" y="210" width="105" height="130" rx="18" fill="#f1f5f9" stroke={LINE} strokeWidth="5" />
      <line x1="432" y1="210" x2="432" y2="145" stroke={LINE} strokeWidth="7" />
      <rect x="405" y="118" width="54" height="32" rx="8" fill="#d8dee6" stroke={LINE} strokeWidth="4" />
      <Text x={432} y={385} size={20}>MANUAL PRIMER</Text>
      <path d="M485 275 C560 275 575 230 640 230" stroke={RED} strokeWidth="8" fill="none" markerEnd="url(#piston-arrow-red)" />
      <rect x="640" y="155" width="170" height="210" rx="22" fill="#f8fafc" stroke={LINE} strokeWidth="5" />
      <rect x="675" y="225" width="100" height="80" rx="12" fill="#d8dee6" stroke={LINE} strokeWidth="4" />
      <line x1="725" y1="205" x2="725" y2="150" stroke={LINE} strokeWidth="8" />
      <Text x={725} y={400} size={20}>INLET VALVE AREA</Text>
      <Text x={450} y={485} size={22}>Primer fuel is delivered close to the inlet valves for cold starting.</Text>
    </Svg>
  )
}

function FloodedStartVisual() {
  return (
    <Svg>
      <Text x={450} y={50} size={24}>TOO MUCH FUEL → RESTORE A COMBUSTIBLE MIXTURE</Text>
      <rect x="90" y="125" width="220" height="230" rx="26" fill="#fff4f4" stroke={RED} strokeWidth="5" />
      <Text x={200} y={185} size={24} fill={RED}>FLOODED</Text>
      {[130, 165, 200, 235, 270].map((x) => <circle key={x} cx={x} cy={260} r="14" fill={FUEL} />)}
      <Text x={200} y={325} size={20}>Excess fuel</Text>
      <path d="M330 240 L435 240" stroke={BLUE} strokeWidth="8" markerEnd="url(#piston-arrow-blue)" />
      <rect x="445" y="145" width="170" height="190" rx="24" fill="#f8fafc" stroke={LINE} strokeWidth="5" />
      <Text x={530} y={205} size={22}>MIXTURE</Text>
      <Text x={530} y={255} size={28} fill={BLUE}>FULL LEAN</Text>
      <Text x={530} y={300} size={18}>until engine fires</Text>
      <path d="M630 240 L735 240" stroke={BLUE} strokeWidth="8" markerEnd="url(#piston-arrow-blue)" />
      <rect x="745" y="145" width="120" height="190" rx="24" fill="#f0fdf4" stroke={LINE} strokeWidth="5" />
      <Text x={805} y={210} size={22}>FIRE</Text>
      <Text x={805} y={255} size={22} fill={RED}>RICHEN</Text>
      <Text x={805} y={292} size={18}>slowly</Text>
      <Text x={450} y={455} size={21}>Use the aircraft's published flooded-start procedure.</Text>
    </Svg>
  )
}

function SmoothThrottleVisual() {
  return (
    <Svg>
      <Text x={450} y={48} size={24}>CHANGE ENGINE LOAD PROGRESSIVELY</Text>
      <rect x="110" y="120" width="270" height="250" rx="26" fill="#fff4f4" stroke={RED} strokeWidth="5" />
      <Text x={245} y={170} size={22} fill={RED}>RAPID MOVEMENT</Text>
      <line x1="190" y1="290" x2="300" y2="195" stroke={RED} strokeWidth="12" />
      <circle cx="190" cy="290" r="18" fill="#64748b" />
      <path d="M155 330 C205 275 235 320 285 265 C320 228 340 245 360 210" fill="none" stroke={RED} strokeWidth="7" />
      <Text x={245} y={345} size={18}>Abrupt torque change</Text>
      <rect x="520" y="120" width="270" height="250" rx="26" fill="#f0fdf4" stroke={BLUE} strokeWidth="5" />
      <Text x={655} y={170} size={22} fill={BLUE}>SMOOTH MOVEMENT</Text>
      <line x1="595" y1="290" x2="705" y2="215" stroke={BLUE} strokeWidth="12" />
      <circle cx="595" cy="290" r="18" fill="#64748b" />
      <path d="M560 330 C590 310 620 295 650 275 C685 250 720 230 755 210" fill="none" stroke={BLUE} strokeWidth="7" />
      <Text x={655} y={345} size={18}>Progressive load change</Text>
      <Text x={450} y={465} size={22}>Smooth throttle movement reduces sudden stress on the crankshaft and engine.</Text>
    </Svg>
  )
}

function CarbIcingVisual() {
  return (
    <Svg>
      <Text x={245} y={48} size={22} fill={BLUE}>NORMAL</Text>
      <Text x={655} y={48} size={22} fill={RED}>ICE BUILD-UP</Text>
      <path d="M120 120 L370 120 L320 380 L170 380 Z" fill="#f8fafc" stroke={LINE} strokeWidth="5" />
      <path d="M170 255 C220 215 270 215 320 255" fill="none" stroke={BLUE} strokeWidth="8" markerEnd="url(#piston-arrow-blue)" />
      <ellipse cx="245" cy="300" rx="60" ry="16" fill="#d7a52d" stroke={LINE} strokeWidth="4" />
      <Text x={245} y={430} size={19}>Clear venturi</Text>
      <path d="M530 120 L780 120 L730 380 L580 380 Z" fill="#f8fafc" stroke={LINE} strokeWidth="5" />
      <path d="M565 245 C615 220 665 220 715 245" fill="none" stroke={BLUE} strokeWidth="6" markerEnd="url(#piston-arrow-blue)" />
      <path d="M585 210 Q655 165 725 210 L710 285 Q655 245 600 285 Z" fill="#dff3ff" stroke="#8ed0f0" strokeWidth="5" />
      <ellipse cx="655" cy="300" rx="60" ry="16" fill="#d7a52d" stroke={LINE} strokeWidth="4" />
      <Text x={655} y={430} size={19} fill={RED}>Airflow restricted</Text>
      <Text x={450} y={490} size={22}>Carburettor ice builds gradually, causing rough running and power loss.</Text>
    </Svg>
  )
}

function AlternateAirVisual() {
  return (
    <Svg>
      <Text x={450} y={48} size={24}>ALTERNATE AIR BYPASSES A BLOCKED NORMAL INTAKE</Text>
      <rect x="105" y="145" width="180" height="120" rx="18" fill="#f1f5f9" stroke={LINE} strokeWidth="5" />
      <Text x={195} y={210} size={20}>AIR FILTER</Text>
      <path d="M285 205 L450 205" stroke={BLUE} strokeWidth="8" markerEnd="url(#piston-arrow-blue)" />
      <line x1="330" y1="165" x2="370" y2="245" stroke={RED} strokeWidth="8" />
      <line x1="370" y1="165" x2="330" y2="245" stroke={RED} strokeWidth="8" />
      <Text x={350} y={145} size={18} fill={RED}>BLOCKED</Text>
      <rect x="450" y="145" width="185" height="170" rx="22" fill="#f8fafc" stroke={LINE} strokeWidth="5" />
      <Text x={542} y={225} size={20}>INDUCTION</Text>
      <Text x={542} y={255} size={20}>SYSTEM</Text>
      <path d="M775 205 C700 205 685 260 635 260" stroke={BLUE} strokeWidth="8" fill="none" markerEnd="url(#piston-arrow-blue)" />
      <Text x={775} y={170} size={20} fill={BLUE}>WARMER AIR</Text>
      <Text x={775} y={198} size={18}>from cowling</Text>
      <Text x={450} y={410} size={21}>Alternate air restores airflow when the normal intake is blocked or iced.</Text>
    </Svg>
  )
}

function AcceleratorPumpVisual() {
  return (
    <Svg>
      <Text x={450} y={48} size={24}>RAPID THROTTLE OPENING NEEDS EXTRA FUEL</Text>
      <rect x="110" y="150" width="230" height="220" rx="24" fill="#f8fafc" stroke={LINE} strokeWidth="5" />
      <ellipse cx="225" cy="260" rx="75" ry="20" fill="#d7a52d" stroke={LINE} strokeWidth="4" />
      <line x1="225" y1="260" x2="295" y2="195" stroke={BLUE} strokeWidth="10" />
      <Text x={225} y={405} size={20}>THROTTLE OPENS</Text>
      <path d="M340 260 L470 260" stroke={BLUE} strokeWidth="8" markerEnd="url(#piston-arrow-blue)" />
      <rect x="470" y="185" width="160" height="150" rx="22" fill="#fff8e7" stroke={LINE} strokeWidth="5" />
      <circle cx="550" cy="260" r="42" fill={FUEL} stroke={LINE} strokeWidth="4" />
      <Text x={550} y={365} size={20}>ACCELERATOR PUMP</Text>
      <path d="M630 260 C690 260 710 235 775 235" stroke={RED} strokeWidth="9" fill="none" markerEnd="url(#piston-arrow-red)" />
      <Text x={760} y={205} size={19} fill={RED}>EXTRA FUEL</Text>
      <Text x={760} y={325} size={19}>to venturi</Text>
      <Text x={450} y={475} size={21}>The extra fuel prevents a momentary lean hesitation as airflow rises.</Text>
    </Svg>
  )
}

function getVisual(visualKey: string) {
  switch (visualKey) {
    case "piston-mixture-rich-lean": return <MixtureVisual />
    case "piston-valve-lead": return <ValveLeadVisual />
    case "piston-primer": return <PrimerVisual />
    case "piston-flooded-start": return <FloodedStartVisual />
    case "piston-smooth-throttle": return <SmoothThrottleVisual />
    case "piston-carb-icing": return <CarbIcingVisual />
    case "piston-alternate-air": return <AlternateAirVisual />
    case "piston-accelerator-pump": return <AcceleratorPumpVisual />
    default: return null
  }
}
