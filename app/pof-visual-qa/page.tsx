import { ExplanationImage } from "../practice/[subject]/components/explanation-image"

const visuals = [
  {
    src: "/explanation-images/principles-of-flight/refined-batch-12/pof-rudder-further-effects-v1.webp",
    alt: "Rudder primary and further effects showing yaw first, then roll, then possible spiral dive if uncorrected",
  },
  {
    src: "/explanation-images/principles-of-flight/refined-batch-12/pof-aileron-further-effects-v1.webp",
    alt: "Aileron primary and further effects showing roll first, then yaw, then possible spiral dive if uncorrected",
  },
  {
    src: "/explanation-images/principles-of-flight/refined-batch-12/pof-control-column-forward-left-v1.webp",
    alt: "Control column forward and left with left aileron up, right aileron down and elevator down",
  },
  {
    src: "/explanation-images/principles-of-flight/refined-batch-12/pof-aspect-ratio-induced-drag-v1.webp",
    alt: "High and low aspect ratio wing comparison showing longer span shorter chord and reduced induced drag for high aspect ratio",
  },
  {
    src: "/explanation-images/principles-of-flight/refined-batch-12/pof-anhedral-wing-geometry-v1.webp",
    alt: "Front view of anhedral wing geometry with wingtips lower than wing roots",
  },
]

export default function PofVisualQaPage() {
  return (
    <main className="min-h-screen bg-slate-100 px-4 py-10 sm:px-8">
      <div className="mx-auto max-w-6xl">
        <div className="mb-8 rounded-2xl border border-slate-200 bg-white p-6">
          <p className="text-xs font-bold uppercase tracking-[0.22em] text-[#b98700]">Internal visual QA</p>
          <h1 className="mt-2 text-3xl font-extrabold text-[#0b1b31]">POF Batch 12</h1>
          <p className="mt-2 text-sm text-slate-600">Real ExplanationImage renderer · five QA-approved raster candidates · no Batch 12 database mapping</p>
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
