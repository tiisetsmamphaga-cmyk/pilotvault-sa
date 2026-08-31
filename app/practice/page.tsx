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

export default function PracticePage() {
  return (
    <main className="min-h-screen bg-[#f8fafc] text-slate-900">
      <header className="sticky top-0 z-50 border-b border-white/15 bg-[#1f4e79]/95 text-white shadow-sm backdrop-blur">
        <div className="mx-auto flex min-h-20 max-w-7xl flex-col gap-4 px-4 py-4 sm:flex-row sm:items-center sm:justify-between sm:px-6 lg:px-8">
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.25em] text-[#d6e6f7]">
              PilotVault SA
            </p>
            <h1 className="mt-1 text-lg font-bold">Practice Center</h1>
          </div>

          <div className="flex w-full gap-3 sm:w-auto">
            <Link
              href="/dashboard"
              className="flex-1 rounded-xl border border-white/25 bg-white/10 px-4 py-2 text-center text-sm font-semibold text-white transition hover:bg-white/15 sm:flex-none sm:px-5"
            >
              Dashboard
            </Link>
            <Link
              href="/"
              className="flex-1 rounded-xl bg-white px-4 py-2 text-center text-sm font-bold text-[#1f4e79] transition hover:bg-[#f1f5f9] sm:flex-none sm:px-5"
            >
              Home
            </Link>
          </div>
        </div>
      </header>

      <section className="mx-auto max-w-7xl px-4 py-8 sm:px-6 sm:py-10 lg:px-8 lg:py-12">
        <div className="mb-8 rounded-3xl border border-slate-200 bg-white p-6 shadow-sm sm:p-8">
          <p className="text-xs font-semibold uppercase tracking-[0.25em] text-[#1f4e79]">
            SACAA Exam Preparation
          </p>
          <h2 className="mt-3 text-3xl font-bold tracking-tight text-slate-900 sm:text-4xl">
            Choose a subject
          </h2>
          <p className="mt-3 max-w-2xl text-slate-600">
            Select a subject and begin practicing SACAA exam questions.
          </p>
        </div>

        <div className="grid grid-cols-2 gap-4 sm:gap-5 lg:grid-cols-4">
          {subjects.map((subject) => (
            <Link
              key={subject.slug}
              href={`/practice/${subject.slug}`}
              className="group rounded-2xl border border-slate-200 bg-white p-5 shadow-sm transition-all hover:-translate-y-1 hover:border-[#1f4e79]/50 hover:shadow-md sm:p-6"
            >
              <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-[#d6e6f7] transition group-hover:bg-[#c7def3]">
                <subject.icon className="h-6 w-6 text-[#1f4e79]" />
              </div>
              <h3 className="mt-5 text-sm font-bold leading-snug text-slate-900 sm:text-lg">
                {subject.name}
              </h3>
            </Link>
          ))}
        </div>
      </section>
    </main>
  )
}
