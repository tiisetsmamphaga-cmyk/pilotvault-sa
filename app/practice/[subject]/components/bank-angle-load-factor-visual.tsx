"use client"

const CESSNA_172_LINE_DRAWING =
  "https://commons.wikimedia.org/wiki/Special:Redirect/file/Cessna_172_line_drawing_oblique.svg"

export function BankAngleLoadFactorVisual() {
  return (
    <figure className="mt-5 overflow-hidden border border-slate-200 bg-white">
      <div className="bg-[#06111f] px-5 py-4 text-center sm:px-8 sm:py-5">
        <p className="text-[11px] font-extrabold uppercase tracking-[0.24em] text-[#f4b400] sm:text-xs">
          PILOTVAULT HUMAN PERFORMANCE
        </p>
        <h3 className="mt-1 text-xl font-black uppercase tracking-[0.025em] text-white sm:text-3xl">
          Bank Angle and Load Factor
        </h3>
      </div>

      <div className="relative overflow-hidden bg-[#f8fafc] px-3 pb-4 pt-5 sm:px-6 sm:pb-6 sm:pt-7">
        <div className="relative mx-auto aspect-[16/9] w-full max-w-4xl overflow-hidden rounded-2xl border-2 border-slate-200 bg-white">
          <svg
            viewBox="0 0 1000 560"
            className="absolute inset-0 h-full w-full"
            aria-hidden="true"
          >
            <path
              d="M95 425 A405 315 0 0 1 905 425"
              fill="none"
              stroke="#94a3b8"
              strokeWidth="3"
            />
            <line x1="95" y1="425" x2="905" y2="425" stroke="#06111f" strokeWidth="4" />

            <g stroke="#cbd5e1" strokeWidth="2" strokeDasharray="10 10">
              <line x1="500" y1="425" x2="500" y2="105" />
              <line x1="500" y1="425" x2="300" y2="150" />
              <line x1="500" y1="425" x2="700" y2="150" />
              <line x1="500" y1="425" x2="850" y2="250" />
            </g>

            <g fill="#06111f">
              <circle cx="95" cy="425" r="7" />
              <circle cx="300" cy="425" r="7" />
              <circle cx="500" cy="425" r="7" />
            </g>
            <circle cx="800" cy="425" r="9" fill="#f4b400" />

            <g
              fill="#06111f"
              fontFamily="Arial, sans-serif"
              fontSize="20"
              fontWeight="700"
              textAnchor="middle"
            >
              <text x="95" y="462">0°</text>
              <text x="300" y="462">30°</text>
              <text x="500" y="462">45°</text>
              <text x="800" y="462" fill="#b77900">60°</text>
            </g>

            <line x1="800" y1="290" x2="800" y2="398" stroke="#f4b400" strokeWidth="7" strokeLinecap="round" />
            <polygon points="800,421 784,393 816,393" fill="#f4b400" />
            <text
              x="827"
              y="350"
              fill="#9a6700"
              fontFamily="Arial, sans-serif"
              fontSize="17"
              fontWeight="800"
            >
              LOAD
            </text>
          </svg>

          <div className="absolute right-[5%] top-[5%] z-10 text-right sm:right-[7%] sm:top-[7%]">
            <p className="text-lg font-black text-[#06111f] sm:text-2xl">
              60° BANK ≈ <span className="text-[#d69d00]">2 G</span>
            </p>
          </div>

          <div className="absolute right-[10%] top-[23%] z-10 w-[36%] max-w-[330px] origin-center -rotate-[26deg] sm:right-[12%] sm:top-[21%]">
            <img
              src={CESSNA_172_LINE_DRAWING}
              alt="Cessna 172 training aircraft"
              className="block h-auto w-full mix-blend-multiply drop-shadow-[0_8px_7px_rgba(6,17,31,0.12)]"
              loading="eager"
              decoding="async"
            />
          </div>

          <div className="absolute bottom-[6%] left-1/2 z-10 w-[66%] -translate-x-1/2 rounded-xl border border-slate-200 bg-white/95 px-4 py-3 shadow-sm sm:w-[58%] sm:px-5 sm:py-4">
            <p className="text-center text-sm font-semibold text-[#06111f] sm:text-base">
              In a balanced level turn, <span className="text-[#b77900]">load factor rises rapidly</span> as bank angle increases.
            </p>
          </div>
        </div>

        <div className="mx-auto mt-4 grid max-w-4xl gap-2 text-center text-xs font-semibold text-slate-600 sm:grid-cols-4 sm:text-sm">
          <span>Load factor = 1 ÷ cos(bank angle)</span>
          <span>30° ≈ 1.15 G</span>
          <span>45° ≈ 1.41 G</span>
          <span className="text-[#b77900]">60° ≈ 2.00 G</span>
        </div>
      </div>
    </figure>
  )
}
