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
    name: "Air Law",
    icon: Scale,
    description:
      "Rules, regulations, airspace classifications, licensing requirements, and operational procedures.",
  },
  {
    name: "Meteorology",
    icon: Cloud,
    description:
      "Weather systems, forecasts, METARs, TAFs, clouds, wind, and aviation weather interpretation.",
  },
  {
    name: "Navigation",
    icon: Compass,
    description:
      "Maps, charts, headings, tracks, magnetic variation, flight calculations, and navigation principles.",
  },
  {
    name: "Human Performance",
    icon: Brain,
    description:
      "Aviation physiology, fatigue, hypoxia, vision, decision-making, and human factors.",
  },
  {
    name: "Principles of Flight",
    icon: Plane,
    description:
      "Aerodynamics, lift, drag, stability, stalls, controls, and aircraft performance.",
  },
  {
    name: "Aircraft Technical & General",
    icon: Wrench,
    description:
      "Aircraft systems, engines, instruments, electrics, hydraulics, and maintenance knowledge.",
  },
  {
    name: "Radio Telephony",
    icon: Radio,
    description:
      "Standard phraseology, radio procedures, emergencies, and communication techniques.",
  },
  {
    name: "Flight Planning",
    icon: Map,
    description:
      "Mass and balance, fuel planning, performance calculations, and flight preparation.",
  },
]

export default function SubjectsPage() {
  return (
    <main className="min-h-screen bg-[#06111f] text-white">
      <header className="border-b border-[#1e3a5f] bg-[#06111f]/95">
        <div className="mx-auto flex min-h-20 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
          <div>
            <p className="text-xs uppercase tracking-[0.25em] text-[#f4b400]">
              PilotVault SA
            </p>
            <h1 className="mt-1 text-lg font-bold">
              Subjects
            </h1>
          </div>

          <Link
            href="/"
            className="rounded-xl border border-[#1e3a5f] px-4 py-3 text-sm text-gray-300 transition hover:border-[#f4b400] hover:text-[#f4b400]"
          >
            Back Home
          </Link>
        </div>
      </header>

      <section className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-3xl text-center">
          <p className="text-xs uppercase tracking-[0.3em] text-[#f4b400]">
            SACAA Theory Subjects
          </p>

          <h2 className="mt-4 text-4xl font-bold sm:text-5xl">
            Everything you need to pass your exams.
          </h2>

          <p className="mt-5 text-lg leading-8 text-gray-400">
            PilotVault SA provides preparation material across the core SACAA
            Private Pilot Licence subjects, with additional CPL content planned
            for future releases.
          </p>
        </div>

        <div className="mt-12 grid gap-6 md:grid-cols-2 lg:grid-cols-4">
          {subjects.map((subject) => (
            <div
              key={subject.name}
              className="rounded-3xl border border-[#1e3a5f] bg-[#081726] p-6 transition hover:-translate-y-1 hover:border-[#f4b400]"
            >
              <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-[#f4b400]/10">
                <subject.icon className="h-6 w-6 text-[#f4b400]" />
              </div>

              <h3 className="mt-5 text-lg font-bold">
                {subject.name}
              </h3>

              <p className="mt-3 text-sm leading-6 text-gray-400">
                {subject.description}
              </p>
            </div>
          ))}
        </div>

        <div className="mt-12 rounded-3xl border border-[#f4b400]/30 bg-[#f4b400]/10 p-6 text-center sm:p-8">
          <h3 className="text-2xl font-bold">
            Ready to start preparing?
          </h3>

          <p className="mx-auto mt-3 max-w-2xl text-gray-300">
            Access SACAA-focused mock exams, explanations, and structured
            practice designed for South African student pilots.
          </p>

          <Link
            href="/dashboard"
            className="mt-6 inline-flex rounded-xl bg-[#f4b400] px-6 py-3 text-sm font-bold text-[#06111f] transition hover:bg-[#d9a000]"
          >
            Start Practicing
          </Link>
        </div>
      </section>
    </main>
  )
}