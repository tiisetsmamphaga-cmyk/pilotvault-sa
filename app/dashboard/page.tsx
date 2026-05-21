"use client"

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
  { name: "Meteorology", slug: "meteorology", icon: Cloud },
  { name: "Air Law", slug: "air-law", icon: Scale },
  { name: "Navigation", slug: "navigation", icon: Compass },
  { name: "Human Performance", slug: "human-performance", icon: Brain },
  {
    name: "Principles of Flight",
    slug: "principles-of-flight",
    icon: Plane,
  },
  {
    name: "Aircraft Technical and General",
    slug: "aircraft-technical-and-general",
    icon: Wrench,
  },
  { name: "Radio Telephony", slug: "radio-telephony", icon: Radio },
  { name: "Flight Planning", slug: "flight-planning", icon: Map },
]

export default function DashboardPage() {
  return (
    <main className="min-h-screen bg-[#06111f] text-white">
      <header className="border-b border-[#1e3a5f] bg-[#06111f]/95">
        <div className="mx-auto flex min-h-20 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
          <div>
            <p className="text-xs uppercase tracking-[0.25em] text-[#f4b400]">
              PilotVault SA
            </p>

            <h1 className="mt-1 text-lg font-bold">
              Dashboard
            </h1>
          </div>

          <Link
            href="/"
            className="rounded-xl bg-[#f4b400] px-4 py-2 text-sm font-bold text-[#06111f] hover:bg-[#d9a000]"
          >
            Home
          </Link>
        </div>
      </header>

      <section className="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8">
        <div className="mb-8 rounded-3xl border border-[#1e3a5f] bg-[#081726] p-6 sm:p-8">
          <p className="text-xs uppercase tracking-[0.25em] text-[#f4b400]">
            Practice Center
          </p>

          <h2 className="mt-3 text-3xl font-bold sm:text-4xl">
            Choose a subject
          </h2>

          <p className="mt-3 max-w-2xl text-gray-400">
            Select the subject you want to study and start practicing with
            SACAA-style questions.
          </p>
        </div>

        <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
          {subjects.map((subject) => (
            <Link
              key={subject.slug}
              href={`/practice/${subject.slug}`}
              className="group rounded-2xl border border-[#1e3a5f] bg-[#081726] p-6 transition hover:-translate-y-1 hover:border-[#f4b400]"
            >
              <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-[#f4b400]/10 group-hover:bg-[#f4b400]/20">
                <subject.icon className="h-6 w-6 text-[#f4b400]" />
              </div>

              <h3 className="mt-5 text-lg font-bold">
                {subject.name}
              </h3>
            </Link>
          ))}
        </div>
      </section>
    </main>
  )
}