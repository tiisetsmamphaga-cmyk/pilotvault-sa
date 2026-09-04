import { ExplanationImage } from "../practice/[subject]/components/explanation-image"

const visuals = [
  {
    src: "/explanation-images/principles-of-flight/refined-batch-11/pof-trailing-edge-flap-lift-drag-v1.webp",
    alt: "Trailing-edge flap comparison showing increased camber, lift and drag at the same angle of attack and airspeed",
  },
  {
    src: "/explanation-images/principles-of-flight/refined-batch-11/pof-flap-stall-speed-v1.webp",
    alt: "Flap stall-speed comparison showing increased maximum lift capability and reduced stall speed at the same weight and load factor",
  },
  {
    src: "/explanation-images/principles-of-flight/refined-batch-11/pof-fowler-flap-wing-area-v1.webp",
    alt: "Fowler flap comparison showing rearward extension, downward deflection and increased effective wing area",
  },
  {
    src: "/explanation-images/principles-of-flight/refined-batch-11/pof-static-dynamic-stability-response-v1.webp",
    alt: "Static and dynamic stability response traces showing initial restoring tendency, damped oscillations and growing oscillations",
  },
  {
    src: "/explanation-images/principles-of-flight/refined-batch-11/pof-directional-fin-weathercock-v1.webp",
    alt: "Directional stability diagram showing a fin behind the centre of gravity producing lateral sideforce and a restoring yawing moment",
  },
]

export default function PofVisualQaPage() {
  return (
    <main className="min-h-screen bg-slate-100 px-4 py-10 sm:px-8">
      <div className="mx-auto max-w-6xl">
        <div className="mb-8 rounded-2xl border border-slate-200 bg-white p-6">
          <p className="text-xs font-bold uppercase tracking-[0.22em] text-[#b98700]">Internal visual QA</p>
          <h1 className="mt-2 text-3xl font-extrabold text-[#0b1b31]">POF Batch 11</h1>
          <p className="mt-2 text-sm text-slate-600">Real ExplanationImage renderer · five QA-approved raster candidates · no new Batch 11 database mapping</p>
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
