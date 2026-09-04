import { ExplanationImage } from "../practice/[subject]/components/explanation-image"

const visuals = [
  {
    src: "/explanation-images/principles-of-flight/refined-batch-10/pof-pressure-distribution-lift-v1.webp",
    alt: "Pressure distribution around an aerofoil showing lower pressure above, higher pressure below and the resulting lift force",
  },
  {
    src: "/explanation-images/principles-of-flight/refined-batch-10/pof-adverse-yaw-high-aoa-v1.webp",
    alt: "Adverse yaw comparison showing the drag imbalance becoming more pronounced at higher angle of attack",
  },
  {
    src: "/explanation-images/principles-of-flight/refined-batch-10/pof-venturi-continuity-v1.webp",
    alt: "Venturi diagram showing constant mass flow, increased velocity and reduced static pressure through the throat",
  },
  {
    src: "/explanation-images/principles-of-flight/refined-batch-10/pof-level-turn-force-balance-v1.webp",
    alt: "Level coordinated turn force diagram showing banked lift split into vertical and horizontal components",
  },
  {
    src: "/explanation-images/principles-of-flight/refined-batch-10/pof-propeller-left-turning-tendencies-v1.webp",
    alt: "Propeller left-turning tendencies showing torque reaction and asymmetric blade effect with the required right-rudder correction",
  },
]

export default function PofVisualQaPage() {
  return (
    <main className="min-h-screen bg-slate-100 px-4 py-10 sm:px-8">
      <div className="mx-auto max-w-6xl">
        <div className="mb-8 rounded-2xl border border-slate-200 bg-white p-6">
          <p className="text-xs font-bold uppercase tracking-[0.22em] text-[#b98700]">Internal visual QA</p>
          <h1 className="mt-2 text-3xl font-extrabold text-[#0b1b31]">POF Batch 10</h1>
          <p className="mt-2 text-sm text-slate-600">Real ExplanationImage renderer · five QA-approved raster candidates · no new Batch 10 database mapping</p>
        </div>

        <div className="space-y-10">
          {visuals.map((visual, index) => (
            <section key={visual.src} className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
              <div className="mb-3 text-sm font-bold text-slate-700">Visual {index + 1} of {visuals.length}</div>
              <ExplanationImage src={visual.src} alt={visual.alt} priority />
            </section>
          ))}
        </div>
      </div>
    </main>
  )
}
