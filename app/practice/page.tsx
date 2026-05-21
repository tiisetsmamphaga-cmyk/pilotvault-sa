import Link from "next/link"
import {
  Cloud,
  Scale,
  Compass,
  Brain,
  Plane,
  Wrench,
  Radio,
  Map,
} from "lucide-react"

const subjects = [
  {
    name: "Meteorology",
    slug: "meteorology",
    icon: Cloud,
    description: "Weather, pressure, clouds, fronts and South African weather.",
  },
  {
    name: "Air Law",
    slug: "air-law",
    icon: Scale,
    description: "Rules, regulations and airspace procedures.",
  },
  {
    name: "Navigation",
    slug: "navigation",
    icon: Compass,
    description: "Maps, headings, tracks and flight planning.",
  },
  {
    name: "Human Performance",
    slug: "human-performance",
    icon: Brain,
    description: "Physiology and pilot limitations.",
  },
  {
    name: "Principles of Flight",
    slug: "principles-of-flight",
    icon: Plane,
    description: "Lift, drag, stability and aircraft performance.",
  },
  {
    name: "Aircraft Technical and General",
    slug: "aircraft-technical-and-general",
    icon: Wrench,
    description: "Aircraft systems and instruments.",
  },
  {
    name: "Radio Telephony",
    slug: "radio-telephony",
    icon: Radio,
    description: "Radio phraseology and communication procedures.",
  },
  {
    name: "Flight Planning",
    slug: "flight-planning",
    icon: Map,
    description: "Fuel, navigation and route planning.",
  },
]

export default function PracticePage() {
  return (
    <main className="min-h-screen bg-[#06111f] text-white">
      <header className="sticky top-0 z-50 border-b border-[#1e3a5f] bg-[#06111f]/95 backdrop-blur">
        <div className="mx-auto flex min-h-20 max-w-7xl flex-col gap-4 px-4 py-4 sm:flex-row sm:items-center sm:justify-between sm:px-6 lg:px-8">
          <div>
            <p className="text-xs uppercase tracking-[0.25em] text-[#f4b400]">
              PilotVault SA
            </p>

            <h1 className="mt-1 text-lg font-bold">
              Practice Center
            </h1>
          </div>

          <div className="flex w-full gap-3 sm:w-auto">
            <Link
              href="/dashboard"
              className="flex-1 rounded-xl border border-[#1e3a5f] bg-[#0b1f35] px-4 py-2 text-center text-sm font-semibold hover:bg-[#1e3a5f] sm:flex-none sm:px-5"
            >
              Dashboard
            </Link>

            <Link
              href="/"
              className="flex-1 rounded-xl bg-[#f4b400] px-4 py-2 text-center text-sm font-bold text-[#06111f] hover:bg-[#d9a000] sm:flex-none sm:px-5"
            >
              Home
            </Link>
          </div>
        </div>
      </header>

      <section className="mx-auto max-w-7xl px-4 py-8 sm:px-6 sm:py-10 lg:px-8 lg:py-12">
        <div className="rounded-3xl border border-[#1e3a5f] bg-gradient-to-r from-[#081726] to-[#0b1f35] p-6 sm:p-8 lg:p-10">
          <p className="text-xs uppercase tracking-[0.25em] text-[#f4b400]">
            SACAA Exam Preparation
          </p>

          <h2 className="mt-4 text-3xl font-bold leading-tight sm:text-4xl lg:text-5xl">
            Choose Your Subject
          </h2>

          <p className="mt-4 max-w-2xl text-sm leading-6 text-gray-400 sm:text-base">
            Select a subject and start practicing with realistic SACAA-style
            questions, explanations and mock exams.
          </p>
        </div>
      </section>

      <section className="mx-auto max-w-7xl px-4 pb-12 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 xl:grid-cols-4">
          {subjects.map((subject) => (
            <Link
              key={subject.slug}
              href={`/practice/${subject.slug}`}
              className="group rounded-2xl border border-[#1e3a5f] bg-[#081726] p-5 transition duration-300 hover:-translate-y-1 hover:border-[#f4b400] sm:p-6"
            >
              <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-[#f4b400]/10">
  <subject.icon className="h-5 w-5 text-[#f4b400]" />
</div>

<h3 className="mt-5 text-lg font-bold text-white">
  {subject.name}
</h3>

              <p className="mt-5 text-xs uppercase tracking-wider text-[#f4b400]">
                Subject
              </p>

              <h3 className="mt-2 text-lg font-bold sm:text-xl">
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