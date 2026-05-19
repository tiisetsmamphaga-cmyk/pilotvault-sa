import Link from "next/link"

const subjects = [
  {
    name: "Meteorology",
    slug: "meteorology",
    description: "Weather, pressure, clouds, fronts and South African weather.",
  },
  {
    name: "Air Law",
    slug: "air-law",
    description: "Rules, regulations, airspace and SACAA procedures.",
  },
  {
    name: "Navigation",
    slug: "navigation",
    description: "Charts, tracks, headings, drift and flight planning basics.",
  },
  {
    name: "Human Performance",
    slug: "human-performance",
    description: "Physiology, decision-making, hypoxia and pilot limitations.",
  },
  {
    name: "Principles of Flight",
    slug: "principles-of-flight",
    description: "Lift, drag, stability, stalls and aircraft performance.",
  },
  {
    name: "Aircraft Technical and General",
    slug: "aircraft-technical-and-general",
    description: "Aircraft systems, engines, instruments and limitations.",
  },
  {
    name: "Radio Telephony",
    slug: "radio-telephony",
    description: "Radio calls, phraseology and communication procedures.",
  },
  {
    name: "Flight Planning",
    slug: "flight-planning",
    description: "Fuel, weight, balance, endurance and route planning.",
  },
]

export default function PracticePage() {
  return (
    <main className="min-h-screen bg-[#06111f] px-6 py-10 text-white">
      <div className="mx-auto max-w-6xl">
        <Link
          href="/dashboard"
          className="text-sm font-medium text-[#f4b400] hover:text-white"
        >
          ← Back to Dashboard
        </Link>

        <div className="mt-10">
          <p className="text-xs uppercase tracking-[0.18em] text-[#f4b400]">
            Practice
          </p>

          <h1 className="mt-3 text-4xl font-bold">
            Choose a Subject
          </h1>

          <p className="mt-4 max-w-2xl text-slate-300">
            Select a SACAA subject to start practicing by topic or full exam mode.
          </p>
        </div>

        <div className="mt-10 grid gap-5 md:grid-cols-2 lg:grid-cols-3">
          {subjects.map((subject) => (
            <Link
              key={subject.slug}
              href={`/practice/${subject.slug}`}
              className="rounded-2xl border border-[#1e3a5f] bg-[#081726] p-6 transition hover:-translate-y-1 hover:border-[#f4b400]"
            >
              <p className="text-sm uppercase tracking-wider text-[#f4b400]">
                Subject
              </p>

              <h2 className="mt-3 text-2xl font-bold">
                {subject.name}
              </h2>

              <p className="mt-3 text-sm text-slate-300">
                {subject.description}
              </p>
            </Link>
          ))}
        </div>
      </div>
    </main>
  )
}