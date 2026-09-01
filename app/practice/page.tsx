import Image from "next/image"
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
    <main className="min-h-screen bg-[#eef3f8] text-slate-900">
      <header className="sticky top-0 z-50 border-b border-white/15 bg-[#1f4e79]/96 text-white backdrop-blur">
        <div className="mx-auto flex h-16 max-w-7xl items-center justify-between gap-4 px-4 sm:h-[72px] sm:px-6 lg:px-8">
          <div className="flex min-w-0 items-center gap-3">
            <Link href="/dashboard" className="shrink-0" aria-label="PilotVault dashboard">
              <Image
                src="/images/Header logo.png"
                alt="PilotVault SA"
                width={180}
                height={54}
                className="h-auto w-[132px] object-contain sm:w-[154px]"
                priority
              />
            </Link>
            <span className="hidden h-7 w-px bg-white/20 sm:block" />
            <span className="hidden text-sm font-medium text-blue-50/90 sm:block">
              Practice
            </span>
          </div>

          <nav aria-label="Practice navigation" className="hidden items-center gap-1 md:flex">
            <Link
              href="/dashboard"
              className="rounded-lg px-3 py-2 text-sm font-medium text-blue-50 transition hover:bg-white/10 hover:text-white"
            >
              Dashboard
            </Link>
            <Link
              href="/practice"
              aria-current="page"
              className="rounded-lg bg-white/12 px-3 py-2 text-sm font-semibold text-white"
            >
              Practice
            </Link>
            <Link
              href="/upgrade"
              className="rounded-lg px-3 py-2 text-sm font-medium text-blue-50 transition hover:bg-white/10 hover:text-white"
            >
              Plans
            </Link>
            <Link
              href="/profile"
              className="rounded-lg px-3 py-2 text-sm font-medium text-blue-50 transition hover:bg-white/10 hover:text-white"
            >
              Profile
            </Link>
          </nav>
        </div>
      </header>

      <section className="mx-auto max-w-7xl px-4 py-8 sm:px-6 sm:py-10 lg:px-8 lg:py-12">
        <div className="mb-8 border-b border-[#d5e0ea] pb-6">
          <p className="text-xs font-semibold uppercase tracking-[0.22em] text-[#1f4e79]">
            SACAA Exam Preparation
          </p>
          <h1 className="mt-3 text-3xl font-bold tracking-tight text-slate-900 sm:text-4xl">
            Choose a subject
          </h1>
          <p className="mt-3 max-w-2xl text-slate-600">
            Select a subject and begin practising SACAA exam questions.
          </p>
        </div>

        <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-4">
          {subjects.map((subject) => (
            <Link
              key={subject.slug}
              href={`/practice/${subject.slug}`}
              className="group flex min-h-[88px] items-center gap-3 rounded-xl border border-[#d2dde7] bg-[#f8fafc] px-4 py-4 transition hover:border-[#9fb6ca] hover:bg-white focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#1f4e79]/35"
            >
              <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-lg bg-[#d6e6f7]">
                <subject.icon className="h-5 w-5 text-[#1f4e79]" />
              </div>
              <h2 className="text-sm font-semibold leading-snug text-slate-950 sm:text-base">
                {subject.name}
              </h2>
            </Link>
          ))}
        </div>
      </section>
    </main>
  )
}
