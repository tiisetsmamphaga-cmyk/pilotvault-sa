"use client"

import type { ReactNode } from "react"

type PistonExplanationVisualProps = {
  visualKey: string
  title?: string
  caption?: string
}

const NAVY = "#06111f"
const GOLD = "#f4b400"
const BLUE = "#1f6fba"
const RED = "#d62828"
const LINE = "#15202b"

const TITLES: Record<string, string> = {
  "piston-mixture-rich-lean": "RICH VS LEAN MIXTURE",
  "piston-valve-lead": "VALVE LEAD",
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

function getVisual(visualKey: string) {
  switch (visualKey) {
    case "piston-mixture-rich-lean": return <MixtureVisual />
    case "piston-valve-lead": return <ValveLeadVisual />
    default: return null
  }
}
