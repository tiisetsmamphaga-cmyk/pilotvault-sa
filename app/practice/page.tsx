import Link from "next/link"

const subjects = [
  {
    name: "Meteorology",
    slug: "meteorology",
    description:
      "Weather, pressure, clouds, fronts and South African weather.",
  },

  {
    name: "Air Law",
    slug: "air-law",
    description:
      "Rules, regulations and airspace procedures.",
  },

  {
    name: "Navigation",
    slug: "navigation",
    description:
      "Maps, headings, tracks and flight planning.",
  },

  {
    name: "Human Performance",
    slug: "human-performance",
    description:
      "Physiology and pilot limitations.",
  },

  {
    name: "Principles of Flight",
    slug: "principles-of-flight",
    description:
      "Lift, drag, stability and aircraft performance.",
  },

  {
    name: "Aircraft Technical and General",
    slug: "aircraft-technical-and-general",
    description:
      "Aircraft systems and instruments.",
  },

  {
    name: "Radio Telephony",
    slug: "radio-telephony",
    description:
      "Radio phraseology and communication procedures.",
  },

  {
    name: "Flight Planning",
    slug: "flight-planning",
    description:
      "Fuel, navigation and route planning.",
  },
]

export default function PracticePage() {
  return (
    <main className="min-h-screen bg-[#06111f] text-white px-6 py-10">
      <div className="mx-auto max-w-6xl">

        <Link
          href="/dashboard"
          className="text-[#f4b400] hover:text-white"
        >
          ← Back to Dashboard
        </Link>

        <div className="mt-10">

          <p className="text-[#f4b400] uppercase text-xs tracking-[0.2em]">
            Practice
          </p>

          <h1 className="mt-3 text-4xl font-bold">
            Choose a Subject
          </h1>

          <p className="mt-4 text-slate-300">
            Select a SACAA subject to begin practicing.
          </p>

        </div>

        <div className="grid gap-5 mt-10 md:grid-cols-2 lg:grid-cols-3">

          {subjects.map((subject) => (
            <Link
              key={subject.slug}
              href={`/practice/${subject.slug}`}
              className="rounded-2xl border border-[#1e3a5f] bg-[#081726] p-6 hover:border-[#f4b400] transition"
            >

              <p className="text-xs uppercase tracking-wider text-[#f4b400]">
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