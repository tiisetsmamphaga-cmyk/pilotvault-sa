import { ExplanationImage } from "../practice/[subject]/components/explanation-image"

const visuals = [
  ["Batch 5 — 20° bank load factor", "/explanation-images/principles-of-flight/refined-batch-5/pof-load-factor-20deg-v2.webp"],
  ["Batch 5 — 50° bank load factor", "/explanation-images/principles-of-flight/refined-batch-5/pof-load-factor-50deg-v1.webp"],
  ["Batch 5 — +2.5 G bank limit", "/explanation-images/principles-of-flight/refined-batch-5/pof-load-limit-2-5g-bank-v1.webp"],
  ["Batch 5 — +3.8 G bank limit", "/explanation-images/principles-of-flight/refined-batch-5/pof-load-limit-3-8g-bank-v1.webp"],
  ["Batch 5 — Fowler flap wing area", "/explanation-images/principles-of-flight/refined-batch-5/pof-fowler-flap-area-v1.webp"],
] as const

export default function PofVisualQaPage() {
  return (
    <main className="min-h-screen bg-[#06111f] px-4 py-10 text-white sm:px-8">
      <div className="mx-auto max-w-6xl">
        <div className="mb-8 rounded-3xl border border-[#f4b400]/30 bg-[#091a2d] p-6">
          <div className="text-xs font-extrabold tracking-[0.24em] text-[#f4b400]">PILOTVAULT SA — PREVIEW QA</div>
          <h1 className="mt-2 text-3xl font-black">Principles of Flight — Batch 5</h1>
          <p className="mt-2 max-w-3xl text-sm text-slate-300">
            Temporary preview-only gallery using the same ExplanationImage component as the student practice experience. This route is removed before production merge.
          </p>
        </div>

        <div className="space-y-8">
          {visuals.map(([title, src], index) => (
            <section key={src} className="rounded-3xl border border-white/10 bg-[#0b1d31] p-4 shadow-2xl sm:p-6">
              <div className="mb-2 flex items-center justify-between gap-4">
                <h2 className="text-lg font-bold text-white">{title}</h2>
                <span className="rounded-full border border-[#f4b400]/40 px-3 py-1 text-xs font-bold text-[#f4b400]">{index + 1}/5</span>
              </div>
              <ExplanationImage src={src} alt={`Explanation diagram for ${title}`} priority={index < 2} />
            </section>
          ))}
        </div>
      </div>
    </main>
  )
}
