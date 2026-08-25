"use client"

import type { ReactNode } from "react"

type Props = { visualKey: string; title?: string; caption?: string }

const BLUE = "#1f6fba"
const RED = "#d62828"
const LINE = "#15202b"
const FUEL = "#e8b33d"

const TITLES: Record<string, string> = {
  "piston-combustion-preignition": "PRE-IGNITION",
  "piston-combustion-fuel-approval": "APPROVED AVIATION FUEL",
  "piston-cooling-fins": "CYLINDER COOLING FINS",
  "piston-blue-smoke": "BLUE EXHAUST SMOKE",
}

export function PistonCombustionExplanationVisual({ visualKey, title, caption }: Props) {
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
        <marker id="pc-blue" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill={BLUE} /></marker>
        <marker id="pc-red" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill={RED} /></marker>
      </defs>
      <rect width="900" height="540" fill="white" />
      {children}
    </svg>
  )
}

function Text({ x, y, children, size = 24, fill = LINE, anchor = "middle" }: { x: number; y: number; children: ReactNode; size?: number; fill?: string; anchor?: "start" | "middle" | "end" }) {
  return <text x={x} y={y} fontSize={size} fontWeight={700} fill={fill} textAnchor={anchor} fontFamily="Arial, sans-serif">{children}</text>
}

function PreIgnitionVisual() {
  return (
    <Svg>
      <Text x={450} y={48} size={24}>HOT SPOT IGNITES THE CHARGE TOO EARLY</Text>
      <rect x="270" y="105" width="360" height="330" rx="28" fill="#f8fafc" stroke={LINE} strokeWidth="6" />
      <rect x="315" y="185" width="270" height="190" rx="18" fill="#eef2f7" stroke={LINE} strokeWidth="4" />
      <circle cx="385" cy="165" r="17" fill={RED} />
      <Text x={385} y={135} size={18} fill={RED}>HOT SPOT</Text>
      <path d="M385 182 C410 210 430 225 455 245" fill="none" stroke={RED} strokeWidth="7" markerEnd="url(#pc-red)" />
      <path d="M455 245 C500 215 535 225 565 255" fill="none" stroke="#ff8c42" strokeWidth="10" />
      <Text x={450} y={330} size={20}>COMBUSTION STARTS BEFORE THE SPARK</Text>
      <Text x={260} y={485} size={20} fill={BLUE}>COOL ENGINE + ENRICH MIXTURE → LOWER TEMPERATURE</Text>
    </Svg>
  )
}

function FuelApprovalVisual() {
  return (
    <Svg>
      <Text x={235} y={48} size={22} fill={BLUE}>APPROVED AVGAS</Text>
      <Text x={665} y={48} size={22} fill={RED}>UNAPPROVED MOGAS</Text>
      <rect x="120" y="120" width="230" height="250" rx="30" fill="#eaf5ff" stroke={BLUE} strokeWidth="6" />
      <rect x="145" y="225" width="180" height="120" fill="#2d83d8" opacity="0.88" />
      <Text x={235} y={205} size={24}>USE POH/AFM</Text>
      <Text x={235} y={405} size={20} fill={BLUE}>Correct grade & approval</Text>
      <rect x="550" y="120" width="230" height="250" rx="30" fill="#fff4f4" stroke={RED} strokeWidth="6" />
      <rect x="575" y="225" width="180" height="120" fill={FUEL} opacity="0.9" />
      <Text x={665} y={205} size={24}>ONLY IF APPROVED</Text>
      <Text x={665} y={405} size={20} fill={RED}>Detonation / vapour issues possible</Text>
      <Text x={450} y={485} size={21}>Use only fuel grades specifically approved for the aircraft and engine.</Text>
    </Svg>
  )
}

function CoolingFinsVisual() {
  return (
    <Svg>
      <Text x={450} y={48} size={24}>FINS INCREASE SURFACE AREA EXPOSED TO AIR</Text>
      <rect x="330" y="145" width="240" height="260" rx="28" fill="#d8dee6" stroke={LINE} strokeWidth="6" />
      {[165, 195, 225, 255, 285, 315, 345, 375].map((y) => <rect key={y} x="250" y={y} width="400" height="12" rx="4" fill="#94a3b8" stroke={LINE} strokeWidth="2" />)}
      <path d="M105 210 L240 210" stroke={BLUE} strokeWidth="8" markerEnd="url(#pc-blue)" />
      <path d="M105 280 L240 280" stroke={BLUE} strokeWidth="8" markerEnd="url(#pc-blue)" />
      <path d="M105 350 L240 350" stroke={BLUE} strokeWidth="8" markerEnd="url(#pc-blue)" />
      <Text x={135} y={185} size={20} fill={BLUE}>COOLING AIR</Text>
      <Text x={450} y={455} size={22}>More metal surface area transfers heat to the passing airflow.</Text>
    </Svg>
  )
}

function BlueSmokeVisual() {
  return (
    <Svg>
      <Text x={450} y={48} size={24}>OIL ENTERS THE COMBUSTION CHAMBER</Text>
      <rect x="150" y="135" width="300" height="245" rx="28" fill="#f8fafc" stroke={LINE} strokeWidth="6" />
      <rect x="205" y="235" width="190" height="95" rx="14" fill="#d8dee6" stroke={LINE} strokeWidth="4" />
      <path d="M250 215 C280 185 320 185 350 215" fill="none" stroke="#5b4636" strokeWidth="9" />
      <Text x={300} y={420} size={20}>CYLINDER</Text>
      <path d="M450 255 L590 255" stroke={LINE} strokeWidth="8" />
      <path d="M590 255 C650 235 700 250 760 215" fill="none" stroke="#4f88c6" strokeWidth="18" opacity="0.75" />
      <path d="M600 285 C660 265 720 285 790 250" fill="none" stroke="#79a7d8" strokeWidth="14" opacity="0.7" />
      <Text x={690} y={185} size={22} fill={BLUE}>BLUE SMOKE</Text>
      <Text x={450} y={475} size={22}>Blue exhaust smoke is a classic sign that the engine is burning oil.</Text>
    </Svg>
  )
}

function getVisual(key: string) {
  switch (key) {
    case "piston-combustion-preignition": return <PreIgnitionVisual />
    case "piston-combustion-fuel-approval": return <FuelApprovalVisual />
    case "piston-cooling-fins": return <CoolingFinsVisual />
    case "piston-blue-smoke": return <BlueSmokeVisual />
    default: return null
  }
}
