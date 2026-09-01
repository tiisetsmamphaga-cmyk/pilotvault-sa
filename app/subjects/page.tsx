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

import { Footer } from "@/components/footer"
import { Navbar } from "@/components/navbar"

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
    <main className="min-h-screen bg-[#eef3f8] text-slate-900">
      <Navbar />

      <section className="mx-auto max-w-7xl px-4 pb-12 pt-32 sm:px-6 sm:pb-16 lg:px-8">
        <div className="mx-auto max-w-3xl text-center">
          <p className="text-xs font-semibold uppercase tracking-[0.3em] text-[#1f4e79]">
            SACAA Theory Subjects
          </p>
          <h1 className="mt-4 text-4xl font-bold tracking-tight text-slate-900 sm:text-5xl">
            Everything you need to pass your exams.
          </h1>
          <p className="mt-5 text-lg leading-8 text-slate-600">
            PilotVault SA provides preparation material across the core SACAA
            Private Pilot Licence subjects, with additional CPL content planned
            for future releases.
          </p>
        </div>

        <div className="mt-12 grid gap-6 md:grid-cols-2 lg:grid-cols-4">
          {subjects.map((subject) => (
            <div
              key={subject.name}
              className="rounded-2xl border border-slate-200 bg-[#f8fafc] p-6 transition hover:border-[#1f4e79]/40 hover:bg-white"
            >
              <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-[#d6e6f7]">
                <subject.icon className="h-6 w-6 text-[#1f4e79]" />
              </div>
              <h2 className="mt-5 text-lg font-bold text-slate-900">
                {subject.name}
              </h2>
              <p className="mt-3 text-sm leading-6 text-slate-600">
                {subject.description}
              </p>
            </div>
          ))}
        </div>

        <div className="mt-12 rounded-2xl border border-[#1f4e79]/20 bg-[#d6e6f7]/55 p-6 text-center sm:p-8">
          <h2 className="text-2xl font-bold text-slate-900">
            Ready to start preparing?
          </h2>
          <p className="mx-auto mt-3 max-w-2xl text-slate-600">
            Access SACAA-focused mock exams, explanations, and structured
            practice designed for South African student pilots.
          </p>
          <Link
            href="/#pricing"
            className="mt-6 inline-flex min-h-11 items-center justify-center rounded-lg bg-[#1f4e79] px-6 py-3 text-sm font-bold text-white transition hover:bg-[#183d60]"
          >
            View access options
          </Link>
        </div>
      </section>

      <Footer />
    </main>
  )
}
