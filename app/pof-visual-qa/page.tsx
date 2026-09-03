import { ExplanationImage } from "../practice/[subject]/components/explanation-image"

const visuals = [
  {
    src: "/explanation-images/principles-of-flight/refined-batch-8/pof-balance-tab-opposite-v1.webp",
    alt: "Balance tab moving opposite the primary control surface to reduce pilot control force",
  },
  {
    src: "/explanation-images/principles-of-flight/refined-batch-8/pof-antiservo-tab-same-direction-v1.webp",
    alt: "Anti-servo tab moving in the same direction as an all-moving stabilator to increase control feel",
  },
  {
    src: "/explanation-images/principles-of-flight/refined-batch-8/pof-spin-differential-stall-v1.webp",
    alt: "Left spin showing the descending inner wing more deeply stalled than the rising outer wing",
  },
  {
    src: "/explanation-images/principles-of-flight/refined-batch-8/pof-spin-recovery-control-order-v1.webp",
    alt: "Generic FAA spin recovery sequence emphasizing opposite rudder before forward elevator",
  },
  {
    src: "/explanation-images/principles-of-flight/refined-batch-8/pof-flaps-steepen-glide-v1.webp",
    alt: "Clean and flaps-down glide paths showing flap extension creates a steeper shorter glide",
  },
]

export default function PofVisualQaPage() {
  return (
    <main className="min-h-screen bg-slate-100 px-4 py-10 sm:px-8">
      <div className="mx-auto max-w-6xl">
        <div className="mb-8 rounded-2xl border border-slate-200 bg-white p-6">
          <p className="text-xs font-bold uppercase tracking-[0.22em] text-[#b98700]">Internal visual QA</p>
          <h1 className="mt-2 text-3xl font-extrabold text-[#0b1b31]">POF Batch 8</h1>
          <p className="mt-2 text-sm text-slate-600">Real ExplanationImage renderer · five QA-approved raster candidates · no database mapping</p>
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
