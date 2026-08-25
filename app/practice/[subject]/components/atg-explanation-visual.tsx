"use client"

import type { ReactNode } from "react"

type AtgExplanationVisualProps = {
  visualKey: string
  title?: string
  caption?: string
}

type VisualShellProps = {
  title: string
  caption?: string
  children: ReactNode
}

const NAVY = "#06111f"
const GOLD = "#f4b400"
const BLUE = "#1f6fba"
const RED = "#d62828"
const FUEL = "#e8b33d"
const WATER = "#6ab6e8"
const LINE = "#15202b"
const LIGHT = "#f8fafc"

const visualTitles: Record<string, string> = {
  "float-carburettor": "FLOAT-TYPE CARBURETTOR",
  "fuel-tank-baffles": "FUEL TANK BAFFLES",
  "fuel-tank-venting": "FUEL TANK VENTING",
  "fuel-tank-sump": "FUEL TANK SUMP & PICKUP",
  "refuelling-bonding": "REFUELLING BONDING",
  "fuel-pressure-gauge": "FUEL PRESSURE GAUGE",
  "avgas-100ll-blue": "AVGAS 100LL — BLUE",
  "cold-fuel-water": "COLD FUEL & WATER",
  "full-tank-condensation": "FULL TANKS & CONDENSATION",
  "wet-wing": "WET WING",
}

export function AtgExplanationVisual({
  visualKey,
  title,
  caption,
}: AtgExplanationVisualProps) {
  const visual = getVisual(visualKey)
  if (!visual) return null

  return (
    <VisualShell title={title?.trim() || visualTitles[visualKey] || "ATG DIAGRAM"} caption={caption}>
      {visual}
    </VisualShell>
  )
}

function VisualShell({ title, caption, children }: VisualShellProps) {
  return (
    <figure className="mx-auto mt-5 w-full max-w-[760px] overflow-hidden border border-slate-200 bg-white">
      <div className="border-b-4 border-[#f4b400] bg-[#06111f] px-4 py-3 text-center sm:px-6 sm:py-4">
        <div className="text-[10px] font-extrabold tracking-[0.2em] text-[#f4b400] sm:text-xs">
          PILOTVAULT AIRCRAFT TECHNICAL &amp; GENERAL
        </div>
        <div className="mt-1 text-lg font-extrabold uppercase tracking-[0.03em] text-white sm:text-2xl">
          {title}
        </div>
      </div>
      <div className="bg-white p-2 sm:p-4">{children}</div>
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
    <svg viewBox="0 0 900 540" role="img" className="block h-auto w-full" aria-hidden="true">
      <defs>
        <marker id="arrow-blue" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto" markerUnits="strokeWidth">
          <path d="M0,0 L0,6 L9,3 z" fill={BLUE} />
        </marker>
        <marker id="arrow-red" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto" markerUnits="strokeWidth">
          <path d="M0,0 L0,6 L9,3 z" fill={RED} />
        </marker>
      </defs>
      <rect x="0" y="0" width="900" height="540" fill="white" />
      {children}
    </svg>
  )
}

function Text({ x, y, children, size = 24, weight = 700, fill = LINE, anchor = "middle" }: { x: number; y: number; children: ReactNode; size?: number; weight?: number; fill?: string; anchor?: "start" | "middle" | "end" }) {
  return <text x={x} y={y} fontSize={size} fontWeight={weight} fill={fill} textAnchor={anchor} fontFamily="Arial, sans-serif">{children}</text>
}

function Tank({ x, y, w = 250, h = 220, fuelLevel = 0.55 }: { x: number; y: number; w?: number; h?: number; fuelLevel?: number }) {
  const fuelY = y + h * (1 - fuelLevel)
  return (
    <g>
      <rect x={x} y={y} width={w} height={h} rx="26" fill="white" stroke={LINE} strokeWidth="5" />
      <path d={`M ${x + 3} ${fuelY} Q ${x + w * 0.25} ${fuelY - 5} ${x + w * 0.5} ${fuelY} T ${x + w - 3} ${fuelY} L ${x + w - 3} ${y + h - 3} L ${x + 3} ${y + h - 3} Z`} fill={FUEL} opacity="0.9" />
      <rect x={x + w * 0.43} y={y - 18} width={w * 0.14} height="22" rx="5" fill="#d8dee6" stroke={LINE} strokeWidth="4" />
    </g>
  )
}

function Pipe({ d, color = BLUE, dashed = false, width = 7, arrow = false }: { d: string; color?: string; dashed?: boolean; width?: number; arrow?: boolean }) {
  return <path d={d} fill="none" stroke={color} strokeWidth={width} strokeLinecap="round" strokeLinejoin="round" strokeDasharray={dashed ? "14 12" : undefined} markerEnd={arrow ? `url(#arrow-${color === RED ? "red" : "blue"})` : undefined} />
}

function FloatCarburettorVisual() {
  return (
    <Svg>
      <Text x={185} y={48}>AIR IN</Text>
      <Pipe d="M185 65 L185 185" arrow />
      <path d="M95 95 L275 95 L235 275 L135 275 Z" fill={LIGHT} stroke={LINE} strokeWidth="5" />
      <ellipse cx="185" cy="240" rx="62" ry="18" fill="#d7a52d" stroke={LINE} strokeWidth="4" />
      <Text x={75} y={190} size={21} anchor="start">VENTURI</Text>
      <line x1="158" y1="184" x2="135" y2="184" stroke={LINE} strokeWidth="3" />
      <Text x={92} y={326} size={21} anchor="start">THROTTLE VALVE</Text>
      <line x1="180" y1="301" x2="180" y2="253" stroke={LINE} strokeWidth="3" />
      <rect x="475" y="120" width="300" height="250" rx="24" fill="#fff7dd" stroke={LINE} strokeWidth="5" />
      <rect x="495" y="235" width="260" height="115" rx="10" fill={FUEL} opacity="0.85" />
      <rect x="555" y="215" width="150" height="55" rx="26" fill="#e2e8f0" stroke={LINE} strokeWidth="4" />
      <line x1="705" y1="238" x2="735" y2="194" stroke={LINE} strokeWidth="5" />
      <circle cx="736" cy="191" r="8" fill="#d7a52d" stroke={LINE} strokeWidth="3" />
      <line x1="736" y1="191" x2="736" y2="152" stroke={LINE} strokeWidth="5" />
      <Pipe d="M815 150 L736 150" color={RED} arrow />
      <Text x={818} y={140} size={21} fill={RED} anchor="end">FUEL IN</Text>
      <Text x={625} y={300} size={22}>FLOAT</Text>
      <Text x={625} y={405} size={21}>FLOAT CHAMBER</Text>
      <Text x={750} y={125} size={20} anchor="start">NEEDLE VALVE</Text>
      <line x1="745" y1="132" x2="737" y2="150" stroke={LINE} strokeWidth="3" />
      <Pipe d="M475 255 C400 255 370 210 300 210" color={RED} arrow />
      <Text x={350} y={185} size={20}>METERED FUEL</Text>
      <Text x={185} y={500} size={22} fill={BLUE}>AIR TO ENGINE</Text>
      <Pipe d="M185 300 L185 470" arrow />
    </Svg>
  )
}

function BafflesVisual() {
  return (
    <Svg>
      <Text x={235} y={42} size={22} fill={RED}>WITHOUT BAFFLES</Text>
      <Text x={665} y={42} size={22} fill={BLUE}>WITH BAFFLES</Text>
      <g transform="rotate(8 235 260)"><Tank x={85} y={115} w={300} h={240} fuelLevel={0.62} /></g>
      <Pipe d="M110 210 C155 160 205 170 255 210 C310 250 345 210 365 175" color={RED} arrow />
      <Text x={235} y={410} size={22} fill={RED}>FUEL SURGES</Text>
      <Tank x={515} y={115} w={300} h={240} fuelLevel={0.62} />
      {[585, 665, 745].map((x) => <rect key={x} x={x} y={160} width="14" height="175" fill="#d8dee6" stroke={LINE} strokeWidth="3" />)}
      <Pipe d="M545 240 C575 205 605 205 630 240" arrow />
      <Pipe d="M665 240 C695 205 725 205 750 240" arrow />
      <Text x={665} y={410} size={22} fill={BLUE}>SURGE REDUCED</Text>
      <Text x={450} y={492} size={21}>Baffles restrict rapid fuel movement inside the tank.</Text>
    </Svg>
  )
}

function VentingVisual() {
  return (
    <Svg>
      <Text x={235} y={42} size={22} fill={BLUE}>NORMAL VENTING</Text>
      <Text x={665} y={42} size={22} fill={RED}>BLOCKED VENT</Text>
      <Tank x={85} y={130} w={300} h={230} fuelLevel={0.45} />
      <Pipe d="M235 90 L235 145" arrow />
      <Text x={235} y={85} size={19} fill={BLUE}>ATMOSPHERIC AIR</Text>
      <Pipe d="M235 360 L235 430 L390 430" arrow />
      <Text x={355} y={460} size={19} anchor="end">TO ENGINE</Text>
      <Tank x={515} y={130} w={300} h={230} fuelLevel={0.45} />
      <line x1="650" y1="88" x2="680" y2="118" stroke={RED} strokeWidth="9" />
      <line x1="680" y1="88" x2="650" y2="118" stroke={RED} strokeWidth="9" />
      <Text x={665} y={90} size={19} fill={RED}>VENT BLOCKED</Text>
      <Text x={665} y={205} size={22} fill={RED}>VACUUM FORMS</Text>
      <Pipe d="M665 235 L665 300" color={RED} arrow />
      <Pipe d="M665 360 L665 430 L820 430" color={RED} dashed />
      <Text x={805} y={462} size={18} fill={RED} anchor="end">FUEL FLOW DECREASES</Text>
    </Svg>
  )
}

function SumpVisual() {
  return (
    <Svg>
      <Tank x={185} y={70} w={530} h={360} fuelLevel={0.72} />
      <rect x="190" y="340" width="520" height="55" fill={WATER} opacity="0.92" />
      <path d="M190 395 L710 395 L690 425 L210 425 Z" fill="#6b4e32" opacity="0.9" />
      <Pipe d="M560 250 L760 250" arrow />
      <rect x="500" y="235" width="78" height="30" rx="12" fill="#d7a52d" stroke={LINE} strokeWidth="4" />
      <Text x={775} y={240} size={21} anchor="start">FUEL PICKUP</Text>
      <Text x={775} y={270} size={18} anchor="start">above the sump</Text>
      <Text x={450} y={330} size={24}>FUEL</Text>
      <Text x={450} y={375} size={22}>WATER</Text>
      <Text x={450} y={418} size={20} fill="white">SEDIMENT</Text>
      <Pipe d="M450 430 L450 495" color={RED} arrow />
      <Text x={475} y={495} size={20} fill={RED} anchor="start">SUMP DRAIN</Text>
    </Svg>
  )
}

function BondingVisual() {
  return (
    <Svg>
      <Text x={450} y={45} size={24}>SAFE REFUELLING</Text>
      <path d="M120 265 L250 220 L430 235 L520 285 L420 300 L270 295 Z" fill="#e2e8f0" stroke={LINE} strokeWidth="5" />
      <line x1="250" y1="230" x2="165" y2="155" stroke={LINE} strokeWidth="7" />
      <line x1="250" y1="230" x2="360" y2="145" stroke={LINE} strokeWidth="7" />
      <circle cx="235" cy="305" r="28" fill="#94a3b8" stroke={LINE} strokeWidth="4" />
      <circle cx="405" cy="305" r="28" fill="#94a3b8" stroke={LINE} strokeWidth="4" />
      <Text x={300} y={355} size={21}>AIRCRAFT</Text>
      <rect x="610" y="185" width="185" height="120" rx="12" fill="#d8dee6" stroke={LINE} strokeWidth="5" />
      <circle cx="650" cy="325" r="26" fill="#94a3b8" stroke={LINE} strokeWidth="4" />
      <circle cx="755" cy="325" r="26" fill="#94a3b8" stroke={LINE} strokeWidth="4" />
      <Text x={705} y={355} size={21}>FUEL TRUCK</Text>
      <path d="M610 230 C555 215 530 205 485 220" fill="none" stroke={FUEL} strokeWidth="9" strokeLinecap="round" />
      <Text x={550} y={190} size={18}>FUEL HOSE</Text>
      <line x1="630" y1="380" x2="420" y2="380" stroke={GOLD} strokeWidth="8" />
      <circle cx="630" cy="380" r="9" fill={GOLD} stroke={LINE} strokeWidth="3" />
      <circle cx="420" cy="380" r="9" fill={GOLD} stroke={LINE} strokeWidth="3" />
      <Text x={525} y={418} size={21} fill="#8a6500">BONDING LEAD</Text>
      <line x1="705" y1="380" x2="705" y2="455" stroke={LINE} strokeWidth="5" />
      <line x1="665" y1="455" x2="745" y2="455" stroke={LINE} strokeWidth="4" />
      <line x1="678" y1="470" x2="732" y2="470" stroke={LINE} strokeWidth="4" />
      <line x1="690" y1="485" x2="720" y2="485" stroke={LINE} strokeWidth="4" />
      <Text x={705} y={520} size={20}>EARTH / GROUND</Text>
      <Text x={205} y={500} size={20} fill={RED} anchor="start">Equal potential prevents a static spark.</Text>
    </Svg>
  )
}

function PressureGaugeVisual() {
  return (
    <Svg>
      <Tank x={70} y={115} w={220} h={210} fuelLevel={0.62} />
      <Text x={180} y={360} size={21}>FUEL TANK</Text>
      <circle cx="420" cy="255" r="58" fill="#f1f5f9" stroke={LINE} strokeWidth="5" />
      <Text x={420} y={262} size={21}>PUMP</Text>
      <Pipe d="M290 255 L362 255" arrow />
      <Pipe d="M478 255 L630 255" arrow />
      <circle cx="555" cy="135" r="70" fill="white" stroke={LINE} strokeWidth="5" />
      <path d="M515 155 A48 48 0 0 1 595 155" fill="none" stroke={LINE} strokeWidth="4" />
      <line x1="555" y1="155" x2="575" y2="105" stroke={RED} strokeWidth="6" />
      <Text x={555} y={190} size={18}>PSI</Text>
      <line x1="555" y1="205" x2="555" y2="255" stroke={LINE} strokeWidth="5" />
      <Text x={555} y={45} size={22}>FUEL PRESSURE GAUGE</Text>
      <rect x="655" y="200" width="165" height="110" rx="18" fill="#e2e8f0" stroke={LINE} strokeWidth="5" />
      <Text x={737} y={255} size={22}>CARBURETTOR</Text>
      <Text x={737} y={285} size={18}>INLET</Text>
      <Text x={450} y={440} size={22}>Gauge measures pressure at the carburettor inlet.</Text>
    </Svg>
  )
}

function AvgasVisual() {
  return (
    <Svg>
      <Text x={450} y={55} size={28}>100LL AVGAS</Text>
      <rect x="285" y="110" width="330" height="315" rx="38" fill="#eaf5ff" stroke={LINE} strokeWidth="6" />
      <rect x="305" y="225" width="290" height="180" rx="12" fill="#2d83d8" opacity="0.92" />
      <rect x="350" y="80" width="200" height="52" rx="12" fill="#111827" />
      <Text x={450} y={113} size={22} fill="white">100LL</Text>
      <Text x={450} y={305} size={54} fill="white">BLUE</Text>
      <Text x={450} y={470} size={22} fill={BLUE}>100LL is identified by its blue dye.</Text>
    </Svg>
  )
}

function ColdFuelWaterVisual() {
  return (
    <Svg>
      <Text x={245} y={48} size={22}>WARMER FUEL</Text>
      <Text x={655} y={48} size={22} fill={BLUE}>COLD FUEL</Text>
      <Tank x={95} y={120} w={300} h={250} fuelLevel={0.65} />
      <Text x={245} y={420} size={20}>Less free water visible</Text>
      <Tank x={505} y={120} w={300} h={250} fuelLevel={0.65} />
      <rect x="508" y="325" width="294" height="42" fill={WATER} />
      {[550, 600, 655, 710, 760].map((x) => <circle key={x} cx={x} cy={315} r="9" fill={WATER} />)}
      <Text x={655} y={410} size={20} fill={BLUE}>Water separates / condenses</Text>
      <Text x={450} y={490} size={22}>Cold fuel is more likely to reveal water contamination.</Text>
    </Svg>
  )
}

function CondensationVisual() {
  return (
    <Svg>
      <Text x={240} y={46} size={22} fill={RED}>PARTLY FULL</Text>
      <Text x={660} y={46} size={22} fill={BLUE}>FULL TANK</Text>
      <Tank x={90} y={115} w={300} h={260} fuelLevel={0.42} />
      <Text x={240} y={175} size={19}>LARGE AIR SPACE</Text>
      {[135, 190, 250, 315, 350].map((x) => <circle key={x} cx={x} cy={205} r="8" fill={WATER} />)}
      <Pipe d="M150 195 L150 245" color={BLUE} arrow />
      <Pipe d="M325 195 L325 245" color={BLUE} arrow />
      <Text x={240} y={420} size={20} fill={RED}>More condensation possible</Text>
      <Tank x={510} y={115} w={300} h={260} fuelLevel={0.9} />
      <Text x={660} y={165} size={19}>SMALL AIR SPACE</Text>
      <Text x={660} y={420} size={20} fill={BLUE}>Less moisture available</Text>
      <Text x={450} y={495} size={22}>Filling after flight reduces the moist air space overnight.</Text>
    </Svg>
  )
}

function WetWingVisual() {
  return (
    <Svg>
      <Text x={450} y={46} size={24}>SEALED WING STRUCTURE HOLDS THE FUEL</Text>
      <path d="M80 285 C230 190 470 155 820 205 L820 325 C480 300 250 330 80 385 Z" fill="#e2e8f0" stroke={LINE} strokeWidth="6" />
      <path d="M165 290 C300 230 470 215 690 238 L690 302 C470 285 300 305 165 350 Z" fill={FUEL} opacity="0.9" stroke="#a87400" strokeWidth="4" />
      {[260, 390, 520, 650].map((x) => <line key={x} x1={x} y1={235} x2={x} y2={315} stroke={LINE} strokeWidth="5" />)}
      <Text x={420} y={275} size={28}>FUEL</Text>
      <Text x={450} y={410} size={22}>No separate removable tank or bladder.</Text>
      <Text x={450} y={450} size={21}>Wing skin, ribs and spars form the sealed tank.</Text>
    </Svg>
  )
}

function getVisual(visualKey: string) {
  switch (visualKey) {
    case "float-carburettor": return <FloatCarburettorVisual />
    case "fuel-tank-baffles": return <BafflesVisual />
    case "fuel-tank-venting": return <VentingVisual />
    case "fuel-tank-sump": return <SumpVisual />
    case "refuelling-bonding": return <BondingVisual />
    case "fuel-pressure-gauge": return <PressureGaugeVisual />
    case "avgas-100ll-blue": return <AvgasVisual />
    case "cold-fuel-water": return <ColdFuelWaterVisual />
    case "full-tank-condensation": return <CondensationVisual />
    case "wet-wing": return <WetWingVisual />
    default: return null
  }
}
