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
    <main className="min-h-screen bg-[#06111f] text-white">

      {/* NAVBAR */}

      <header className="sticky top-0 z-50 border-b border-[#1e3a5f] bg-[#06111f]/95 backdrop-blur">

        <div className="mx-auto flex h-20 max-w-7xl items-center justify-between px-6">

          <div>
            <p className="text-xs uppercase tracking-[0.2em] text-[#f4b400]">
              PilotVault SA
            </p>

            <h1 className="text-lg font-bold">
              Practice Center
            </h1>
          </div>

          <div className="flex items-center gap-3">

            <Link
              href="/dashboard"
              className="rounded-xl border border-[#1e3a5f] bg-[#0b1f35] px-5 py-2 text-sm hover:bg-[#1e3a5f]"
            >
              Dashboard
            </Link>

            <Link
              href="/"
              className="rounded-xl bg-[#f4b400] px-5 py-2 text-sm font-bold text-[#06111f] hover:bg-[#d9a000]"
            >
              Home
            </Link>

          </div>

        </div>

      </header>

      {/* HERO */}

      <section className="mx-auto max-w-7xl px-6 py-12">

        <div className="rounded-3xl border border-[#1e3a5f] bg-gradient-to-r from-[#081726] to-[#0b1f35] p-8">

          <p className="text-xs uppercase tracking-[0.2em] text-[#f4b400]">
            SACAA Exam Preparation
          </p>

          <h2 className="mt-4 text-4xl font-bold">
            Choose Your Subject
          </h2>

          <p className="mt-4 max-w-2xl text-gray-400">
            Select a subject and start practicing with realistic
            SACAA-style questions, explanations and mock exams.
          </p>

        </div>

      </section>

      {/* SUBJECTS */}

      <section className="mx-auto max-w-7xl px-6 pb-12">

        <div className="grid gap-6 sm:grid-cols-2 xl:grid-cols-4">

          {subjects.map((subject) => (

            <Link
              key={subject.slug}
              href={`/practice/${subject.slug}`}
              className="group rounded-2xl border border-[#1e3a5f] bg-[#081726] p-6 transition duration-300 hover:-translate-y-1 hover:border-[#f4b400]"
            >

              <div className="flex items-center justify-between">

                <p className="text-xs uppercase tracking-wider text-[#f4b400]">
                  Subject
                </p>

                <span className="text-gray-500 group-hover:text-[#f4b400]">
                  →
                </span>

              </div>

              <h3 className="mt-4 text-xl font-bold">
                {subject.name}
              </h3>

              <p className="mt-3 text-sm leading-6 text-gray-400">
                {subject.description}
              </p>

              <div className="mt-6 h-1 overflow-hidden rounded-full bg-[#06111f]">

                <div className="h-full w-[35%] bg-[#f4b400]" />

              </div>

            </Link>

          ))}

        </div>

      </section>

    </main>
  )
}