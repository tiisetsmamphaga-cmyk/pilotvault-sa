import { ExplanationImage } from "../practice/[subject]/components/explanation-image"

const visuals = [
  {
    src: "/explanation-images/principles-of-flight/refined-batch-7/pof-airspeed-indicator-limits-v1.webp",
    alt: "Standard colour-coded airspeed indicator showing VFE, VNO and VNE limit positions",
  },
  {
    src: "/explanation-images/principles-of-flight/refined-batch-7/pof-skin-friction-boundary-layer-v1.webp",
    alt: "Wing surface airflow showing slower near-surface air and skin-friction parasite drag",
  },
  {
    src: "/explanation-images/principles-of-flight/refined-batch-7/pof-induced-drag-speed-aoa-v1.webp",
    alt: "Induced drag increasing as speed decreases and required angle of attack increases",
  },
  {
    src: "/explanation-images/principles-of-flight/refined-batch-7/pof-air-density-performance-v1.webp",
    alt: "Air density decreasing with altitude temperature and humidity and reducing aircraft performance",
  },
  {
    src: "/explanation-images/principles-of-flight/refined-batch-7/pof-adverse-yaw-aileron-drag-v1.webp",
    alt: "Adverse yaw during a left roll caused by greater induced drag on the lowered right aileron",
  },
]

export default function PofVisualQaPage() {
  return (
    <main className="min-h-screen bg-slate-100 px-4 py-10 sm:px-8">
      <div className="mx-auto max-w-6xl">
        <div className="mb-8 rounded-2xl border border-slate-200 bg-white p-6">
          <p className="text-xs font-bold uppercase tracking-[0.22em] text-[#b98700]">Internal visual QA</p>
          <h1 className="mt-2 text-3xl font-extrabold text-[#0b1b31]">POF Batch 7</h1>
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
