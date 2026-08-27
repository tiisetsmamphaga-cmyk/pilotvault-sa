import { ExplanationImage } from "../practice/[subject]/components/explanation-image"

const visuals = [
  ["Batch 2 — Angle of attack", "/explanation-images/principles-of-flight/refined-batch-2/pof-angle-of-attack-definition-v3.webp"],
  ["Batch 2 — Chord line", "/explanation-images/principles-of-flight/refined-batch-2/pof-chord-line-v2.webp"],
  ["Batch 2 — Four forces equilibrium", "/explanation-images/principles-of-flight/refined-batch-2/pof-four-forces-level-flight-v2.webp"],
  ["Batch 2 — Lift relative airflow", "/explanation-images/principles-of-flight/refined-batch-2/pof-lift-relative-airflow-v2.webp"],
  ["Batch 2 — Venturi Bernoulli", "/explanation-images/principles-of-flight/refined-batch-2/pof-venturi-bernoulli-v2.webp"],
  ["Batch 3 — Angle of incidence", "/explanation-images/principles-of-flight/refined-batch-3/pof-angle-of-incidence-v5.webp"],
  ["Batch 3 — Centre of pressure", "/explanation-images/principles-of-flight/refined-batch-3/pof-centre-of-pressure-v1.webp"],
  ["Batch 3 — Relative airflow", "/explanation-images/principles-of-flight/refined-batch-3/pof-relative-airflow-v1.webp"],
  ["Batch 3 — Speed squared", "/explanation-images/principles-of-flight/refined-batch-3/pof-speed-squared-lift-drag-v1.webp"],
  ["Batch 3 — Wing area", "/explanation-images/principles-of-flight/refined-batch-3/pof-wing-area-lift-drag-v1.webp"],
  ["Batch 4 — Aircraft axes and controls", "/explanation-images/principles-of-flight/refined-batch-4/pof-aircraft-axes-controls-v1.webp"],
  ["Batch 4 — Critical angle of attack", "/explanation-images/principles-of-flight/refined-batch-4/pof-critical-aoa-stall-v4.webp"],
  ["Batch 4 — Stability types", "/explanation-images/principles-of-flight/refined-batch-4/pof-stability-types-v1.webp"],
  ["Batch 4 — Turn lift components", "/explanation-images/principles-of-flight/refined-batch-4/pof-turn-lift-components-v4.webp"],
  ["Batch 4 — Washout", "/explanation-images/principles-of-flight/refined-batch-4/pof-washout-wing-twist-v1.webp"],
] as const

export default function PofVisualQaPage() {
  return (
    <main className="min-h-screen bg-[#06111f] px-4 py-10 text-white sm:px-8">
      <div className="mx-auto max-w-6xl">
        <div className="mb-8 rounded-3xl border border-[#f4b400]/30 bg-[#091a2d] p-6">
          <div className="text-xs font-extrabold tracking-[0.24em] text-[#f4b400]">PILOTVAULT SA — PREVIEW QA</div>
          <h1 className="mt-2 text-3xl font-black">Principles of Flight — Batches 2–4</h1>
          <p className="mt-2 max-w-3xl text-sm text-slate-300">Temporary preview-only gallery using the same ExplanationImage component as the student practice experience. This route is removed before production merge.</p>
        </div>

        <div className="space-y-8">
          {visuals.map(([title, src], index) => (
            <section key={src} className="rounded-3xl border border-white/10 bg-[#0b1d31] p-4 shadow-2xl sm:p-6">
              <div className="mb-2 flex items-center justify-between gap-4">
                <h2 className="text-lg font-bold text-white">{title}</h2>
                <span className="rounded-full border border-[#f4b400]/40 px-3 py-1 text-xs font-bold text-[#f4b400]">{index + 1}/15</span>
              </div>
              <ExplanationImage src={src} alt={`Explanation diagram for ${title}`} priority={index < 2} />
            </section>
          ))}
        </div>
      </div>
    </main>
  )
}
