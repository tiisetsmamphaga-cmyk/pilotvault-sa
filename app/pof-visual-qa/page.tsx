import { ExplanationImage } from "../practice/[subject]/components/explanation-image"

const visuals = [
  {
    src: "/explanation-images/principles-of-flight/refined-batch-9/pof-climb-force-components-v1.webp",
    alt: "Steady-climb force vectors and resolved weight components showing lift below weight and thrust above drag",
  },
  {
    src: "/explanation-images/principles-of-flight/refined-batch-9/pof-best-rate-excess-power-v1.webp",
    alt: "Power available and power required curves showing Vy at maximum excess power",
  },
  {
    src: "/explanation-images/principles-of-flight/refined-batch-9/pof-vx-obstacle-clearance-v1.webp",
    alt: "Vx climb path clearing an obstacle over the shortest horizontal distance",
  },
  {
    src: "/explanation-images/principles-of-flight/refined-batch-9/pof-wind-glide-ground-track-v1.webp",
    alt: "Headwind and tailwind comparison showing different ground-referenced glide paths",
  },
  {
    src: "/explanation-images/principles-of-flight/refined-batch-9/pof-elevator-trim-tab-setting-v1.webp",
    alt: "Conventional elevator trim tab retaining the selected angle relative to the elevator",
  },
]

export default function PofVisualQaPage() {
  return (
    <main className="min-h-screen bg-slate-100 px-4 py-10 sm:px-8">
      <div className="mx-auto max-w-6xl">
        <div className="mb-8 rounded-2xl border border-slate-200 bg-white p-6">
          <p className="text-xs font-bold uppercase tracking-[0.22em] text-[#b98700]">Internal visual QA</p>
          <h1 className="mt-2 text-3xl font-extrabold text-[#0b1b31]">POF Batch 9</h1>
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
