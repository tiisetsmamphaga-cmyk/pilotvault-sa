import { ExplanationImage } from "../practice/[subject]/components/explanation-image"

const visuals = [
  {
    title: "Minimum drag — point 3",
    src: "/explanation-images/principles-of-flight/refined-batch-6/pof-wing-polar-min-drag-v1.webp",
  },
  {
    title: "Best L/D — point 4",
    src: "/explanation-images/principles-of-flight/refined-batch-6/pof-wing-polar-best-ld-v1.webp",
  },
  {
    title: "Critical AoA — point 6",
    src: "/explanation-images/principles-of-flight/refined-batch-6/pof-wing-polar-critical-aoa-v1.webp",
  },
  {
    title: "Induced drag — pressure, vortex and force relationship",
    src: "/explanation-images/principles-of-flight/refined-batch-6/pof-induced-drag-vortex-origin-v1.webp",
  },
  {
    title: "Vertical fin — directional stability",
    src: "/explanation-images/principles-of-flight/refined-batch-6/pof-vertical-fin-directional-stability-v1.webp",
  },
]

export default function PofVisualQaPage() {
  return (
    <main className="min-h-screen bg-[#06111f] px-4 py-10 text-white sm:px-6 lg:px-8">
      <div className="mx-auto max-w-6xl">
        <div className="mb-8 border-b border-white/10 pb-6">
          <p className="text-xs font-extrabold uppercase tracking-[0.24em] text-[#f4b400]">PilotVault SA</p>
          <h1 className="mt-2 text-3xl font-extrabold tracking-tight sm:text-4xl">POF Batch 6 visual QA</h1>
          <p className="mt-3 max-w-3xl text-sm leading-6 text-slate-300">
            Preview-only route using the real production explanation-image component. Every asset below must load cleanly before database mapping.
          </p>
        </div>

        <div className="space-y-8">
          {visuals.map((visual) => (
            <section key={visual.src} className="rounded-3xl border border-white/10 bg-white/5 p-4 sm:p-6">
              <h2 className="text-lg font-bold text-white">{visual.title}</h2>
              <ExplanationImage src={visual.src} alt={visual.title} priority />
            </section>
          ))}
        </div>
      </div>
    </main>
  )
}
