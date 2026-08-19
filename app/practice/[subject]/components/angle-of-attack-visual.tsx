"use client"

import type { Question } from "../types"

const NAVY = "#06111f"
const GOLD = "#f4b400"
const BLUE = "#1f4e79"
const GREY = "#64748b"
const LIGHT = "#d7e0ea"
const PALE = "#f8fafc"

function ArrowHead({ x, y, direction, color }: { x: number; y: number; direction: "left" | "right"; color: string }) {
  const points = direction === "left"
    ? `${x},${y} ${x + 16},${y - 9} ${x + 16},${y + 9}`
    : `${x},${y} ${x - 16},${y - 9} ${x - 16},${y + 9}`

  return <polygon points={points} fill={color} />
}

export function AngleOfAttackVisual({ question }: { question: Question }) {
  const wording = `${question.question} ${question.correctAnswer}`.toLowerCase()
  const relativeAirflowOnly = wording.includes("relative airflow") && !wording.includes("angle of attack")

  return (
    <figure className="mt-5 overflow-hidden border border-slate-200 bg-white">
      <div className="bg-[#06111f] px-4 py-4 text-center sm:px-6 sm:py-5">
        <div className="text-[11px] font-extrabold tracking-[0.24em] text-[#f4b400] sm:text-xs">
          PILOTVAULT PRINCIPLES OF FLIGHT
        </div>
        <div className="mt-1 text-lg font-extrabold uppercase tracking-[0.025em] text-white sm:text-2xl">
          {relativeAirflowOnly ? "RELATIVE AIRFLOW" : "ANGLE OF ATTACK"}
        </div>
      </div>

      <div className="bg-[#f8fafc] p-3 sm:p-5">
        <div className="mx-auto max-w-4xl border border-slate-200 bg-white px-2 py-3 sm:px-4 sm:py-4">
          <svg
            viewBox="0 0 900 440"
            className="block w-full"
            role="img"
            aria-label="Aerofoil showing leading edge, trailing edge, chord line, relative airflow and angle of attack"
            preserveAspectRatio="xMidYMid meet"
          >
            <rect x="18" y="18" width="864" height="404" fill="white" />

            {/* Aircraft motion and relative airflow — deliberately separated. */}
            <line x1="95" y1="315" x2="305" y2="315" stroke={GREY} strokeWidth="4" strokeLinecap="round" />
            <ArrowHead x={305} y={315} direction="right" color={GREY} />
            <text x="200" y="292" textAnchor="middle" fontFamily="Arial, sans-serif" fontSize="15" fontWeight="700" fill={GREY}>
              AIRCRAFT FLIGHT PATH
            </text>

            <line x1="305" y1="355" x2="95" y2="355" stroke={BLUE} strokeWidth="5" strokeLinecap="round" />
            <ArrowHead x={95} y={355} direction="left" color={BLUE} />
            <text x="200" y="385" textAnchor="middle" fontFamily="Arial, sans-serif" fontSize="15" fontWeight="700" fill={BLUE}>
              RELATIVE AIRFLOW
            </text>

            {/* Aerofoil section. Leading edge at left, trailing edge at right. */}
            <path
              d="M345 256 C390 185 490 150 615 167 C690 177 748 211 795 245 C715 237 640 232 565 231 C485 230 410 239 345 256 Z"
              fill={PALE}
              stroke={NAVY}
              strokeWidth="4"
            />

            {/* Chord line. */}
            <line x1="345" y1="256" x2="795" y2="245" stroke={GOLD} strokeWidth="4" />

            {/* Relative airflow extended under the aerofoil to make the AoA unambiguous. */}
            <line x1="795" y1="318" x2="330" y2="318" stroke={BLUE} strokeWidth="4" strokeLinecap="round" />
            <ArrowHead x={330} y={318} direction="left" color={BLUE} />

            {/* AoA arc at the leading edge — no label crosses geometry. */}
            <path d="M405 316 A88 88 0 0 1 398 254" fill="none" stroke={GOLD} strokeWidth="7" strokeLinecap="round" />
            <circle cx="438" cy="286" r="26" fill="white" stroke={GOLD} strokeWidth="2" />
            <text x="438" y="294" textAnchor="middle" fontFamily="Arial, sans-serif" fontSize="23" fontWeight="800" fill={GOLD}>α</text>
            <text x="475" y="289" textAnchor="start" fontFamily="Arial, sans-serif" fontSize="14" fontWeight="700" fill={NAVY}>
              ANGLE OF ATTACK
            </text>

            {/* Clear callouts inspired by conventional training-manual diagrams. */}
            <line x1="358" y1="245" x2="320" y2="205" stroke={GREY} strokeWidth="2" />
            <text x="300" y="196" textAnchor="middle" fontFamily="Arial, sans-serif" fontSize="14" fontWeight="700" fill={NAVY}>LEADING EDGE</text>

            <line x1="570" y1="232" x2="550" y2="110" stroke={GREY} strokeWidth="2" />
            <text x="550" y="94" textAnchor="middle" fontFamily="Arial, sans-serif" fontSize="14" fontWeight="700" fill={NAVY}>CHORD LINE</text>

            <line x1="615" y1="168" x2="665" y2="115" stroke={GREY} strokeWidth="2" />
            <text x="690" y="105" textAnchor="middle" fontFamily="Arial, sans-serif" fontSize="14" fontWeight="700" fill={NAVY}>UPPER CAMBER</text>

            <line x1="555" y1="231" x2="585" y2="365" stroke={GREY} strokeWidth="2" />
            <text x="610" y="392" textAnchor="middle" fontFamily="Arial, sans-serif" fontSize="14" fontWeight="700" fill={NAVY}>LOWER CAMBER</text>

            <line x1="792" y1="245" x2="818" y2="205" stroke={GREY} strokeWidth="2" />
            <text x="805" y="190" textAnchor="middle" fontFamily="Arial, sans-serif" fontSize="14" fontWeight="700" fill={NAVY}>TRAILING EDGE</text>

            <rect x="315" y="338" width="520" height="50" rx="5" fill="white" stroke={LIGHT} />
            <text x="575" y="359" textAnchor="middle" fontFamily="Arial, sans-serif" fontSize="13" fontWeight="700" fill={NAVY}>
              RELATIVE AIRFLOW IS OPPOSITE TO THE AIRCRAFT&apos;S MOTION THROUGH THE AIR MASS
            </text>
            <text x="575" y="379" textAnchor="middle" fontFamily="Arial, sans-serif" fontSize="12" fontWeight="600" fill={GREY}>
              Angle of attack is measured between the chord line and the relative airflow.
            </text>
          </svg>

          <div className="mx-auto mt-2 max-w-3xl border-t border-slate-200 px-3 pt-3 text-center text-sm leading-relaxed text-slate-700">
            {relativeAirflowOnly
              ? "Relative airflow is parallel and opposite to the aircraft's direction of movement through the surrounding air mass."
              : "Angle of attack is the angle between the aerofoil chord line and the relative airflow — not the angle between the wing and the horizon."}
          </div>
        </div>
      </div>
    </figure>
  )
}
