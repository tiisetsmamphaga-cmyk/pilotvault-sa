import Link from "next/link"
import {
  ArrowRight,
  ArrowUpRight,
  BarChart3,
  BookOpenCheck,
  Check,
  Gauge,
  Target,
} from "lucide-react"

import { Footer } from "@/components/footer"
import { Navbar } from "@/components/navbar"

const coreValues = [
  {
    number: "01",
    label: "Mission",
    title: "Pass with confidence",
    description:
      "Help SACAA students prepare through realistic exam practice, explanations, and progress-focused learning.",
  },
  {
    number: "02",
    label: "Focus",
    title: "SACAA exam prep",
    description:
      "Built around South African aviation theory subjects, from PPL to future CPL and ATPL preparation.",
  },
  {
    number: "03",
    label: "Standard",
    title: "Premium and practical",
    description:
      "A clean, focused platform designed to feel professional, trustworthy, and useful from the first session.",
  },
]

const platformHighlights = [
  {
    title: "Realistic mock exams",
    description: "25-question exams built for focused SACAA preparation.",
    icon: Target,
  },
  {
    title: "Focused practice",
    description: "Prepare by subject or work through individual topics.",
    icon: BookOpenCheck,
  },
  {
    title: "Clear explanations",
    description: "Understand the answer, not only the result.",
    icon: Gauge,
  },
  {
    title: "Progress tracking",
    description: "See performance clearly and know where to improve.",
    icon: BarChart3,
  },
]

const offering = [
  "SACAA-focused question banks",
  "25-question mock exams",
  "Detailed answer explanations",
  "Subject-based preparation",
  "Topic-based practice for subscribers",
  "Progress and performance tracking",
]

export default function AboutPage() {
  return (
    <div className="min-h-screen overflow-hidden bg-[#06111f] text-white">
      <Navbar />

      <main className="pt-20">
        <section className="relative border-b border-[#1e3a5f]/70">
          <div
            aria-hidden="true"
            className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_12%_12%,rgba(244,180,0,0.11),transparent_30%),radial-gradient(circle_at_88%_72%,rgba(30,58,95,0.34),transparent_35%)]"
          />
          <div
            aria-hidden="true"
            className="pointer-events-none absolute inset-0 opacity-[0.035] [background-image:linear-gradient(rgba(255,255,255,0.5)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.5)_1px,transparent_1px)] [background-size:72px_72px]"
          />

          <div className="relative mx-auto grid min-h-[660px] max-w-7xl items-center gap-16 px-4 py-20 sm:px-6 lg:grid-cols-[1.15fr_0.85fr] lg:px-8 lg:py-28">
            <div className="max-w-3xl">
              <p className="text-xs font-semibold uppercase tracking-[0.3em] text-[#f4b400]">
                Our mission
              </p>

              <h1 className="mt-6 text-5xl font-semibold leading-[0.98] tracking-[-0.055em] sm:text-6xl lg:text-[5.25rem]">
                Helping SACAA students prepare{" "}
                <span className="text-white/42">with confidence.</span>
              </h1>

              <p className="mt-8 max-w-2xl text-base leading-7 text-slate-300 sm:text-lg sm:leading-8">
                PilotVault SA was created to help South African student pilots
                prepare for SACAA exams using realistic mock exams, focused
                practice, clear explanations, and a clean study experience.
              </p>

              <div className="mt-9 flex flex-col gap-3 sm:flex-row">
                <Link
                  href="/dashboard"
                  className="inline-flex min-h-12 items-center justify-center gap-2 rounded-full bg-[#f4b400] px-6 text-sm font-bold text-[#06111f] transition hover:-translate-y-0.5 hover:bg-[#ffd054] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#f4b400] focus-visible:ring-offset-2 focus-visible:ring-offset-[#06111f]"
                >
                  Start Practicing
                  <ArrowRight className="h-4 w-4" aria-hidden="true" />
                </Link>

                <Link
                  href="/subjects"
                  className="inline-flex min-h-12 items-center justify-center gap-2 rounded-full border border-[#355274] bg-white/[0.025] px-6 text-sm font-semibold text-white transition hover:-translate-y-0.5 hover:border-[#f4b400]/70 hover:bg-[#f4b400]/5 hover:text-[#f4b400] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#f4b400] focus-visible:ring-offset-2 focus-visible:ring-offset-[#06111f]"
                >
                  Explore Subjects
                  <ArrowUpRight className="h-4 w-4" aria-hidden="true" />
                </Link>
              </div>
            </div>

            <div className="lg:pl-8">
              <div className="border-t border-[#355274]">
                {platformHighlights.map((item) => {
                  const Icon = item.icon

                  return (
                    <div
                      key={item.title}
                      className="group grid grid-cols-[auto_1fr_auto] items-start gap-4 border-b border-[#1e3a5f] py-5"
                    >
                      <span className="mt-0.5 flex h-9 w-9 items-center justify-center rounded-full border border-[#f4b400]/25 bg-[#f4b400]/10 text-[#f4b400]">
                        <Icon className="h-4 w-4" aria-hidden="true" />
                      </span>
                      <div>
                        <h2 className="text-sm font-semibold text-white">
                          {item.title}
                        </h2>
                        <p className="mt-1 text-sm leading-6 text-slate-400">
                          {item.description}
                        </p>
                      </div>
                      <ArrowUpRight
                        className="mt-1 h-4 w-4 text-slate-600 transition group-hover:-translate-y-0.5 group-hover:translate-x-0.5 group-hover:text-[#f4b400]"
                        aria-hidden="true"
                      />
                    </div>
                  )
                })}
              </div>
            </div>
          </div>
        </section>

        <section className="mx-auto max-w-7xl px-4 py-24 sm:px-6 lg:px-8 lg:py-32">
          <div className="mx-auto max-w-2xl text-center">
            <p className="text-xs font-semibold uppercase tracking-[0.3em] text-[#f4b400]">
              At our core
            </p>
            <h2 className="mt-5 text-4xl font-semibold tracking-[-0.04em] sm:text-5xl">
              Built around the student pilot.
            </h2>
            <p className="mt-5 text-base leading-7 text-slate-400 sm:text-lg">
              A focused platform with one purpose: make aviation exam
              preparation more structured, realistic, and easier to track.
            </p>
          </div>

          <div className="mt-14 overflow-hidden rounded-[2rem] border border-[#1e3a5f] bg-[#081726]/80 shadow-[0_28px_90px_rgba(0,0,0,0.2)] lg:grid lg:grid-cols-3">
            {coreValues.map((value, index) => (
              <article
                key={value.number}
                className={`group p-7 sm:p-9 ${
                  index > 0
                    ? "border-t border-[#1e3a5f] lg:border-l lg:border-t-0"
                    : ""
                }`}
              >
                <div className="flex items-start justify-between gap-4">
                  <span className="text-5xl font-light tracking-[-0.06em] text-white/12 transition group-hover:text-[#f4b400]/40">
                    {value.number}
                  </span>
                  <span className="rounded-full border border-[#f4b400]/20 bg-[#f4b400]/8 px-3 py-1 text-[0.65rem] font-semibold uppercase tracking-[0.22em] text-[#f4b400]">
                    {value.label}
                  </span>
                </div>
                <h3 className="mt-10 text-xl font-semibold tracking-[-0.02em]">
                  {value.title}
                </h3>
                <p className="mt-4 text-sm leading-7 text-slate-400">
                  {value.description}
                </p>
              </article>
            ))}
          </div>
        </section>

        <section className="border-y border-[#1e3a5f]/70 bg-[#081726]/45">
          <div className="mx-auto grid max-w-7xl gap-14 px-4 py-24 sm:px-6 lg:grid-cols-[0.8fr_1.2fr] lg:gap-24 lg:px-8 lg:py-32">
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.3em] text-[#f4b400]">
                Built from experience
              </p>
              <h2 className="mt-5 text-4xl font-semibold leading-tight tracking-[-0.04em] sm:text-5xl">
                From inside the student pilot journey.
              </h2>
              <p className="mt-6 text-base leading-8 text-slate-400">
                We understand the pressure of aviation exams because PilotVault
                SA is built from inside the student pilot journey. The goal is
                simple: give pilots a trusted platform that makes exam
                preparation more structured, more realistic, and easier to
                track.
              </p>
            </div>

            <div>
              <div className="flex items-end justify-between gap-6 border-b border-[#355274] pb-6">
                <div>
                  <p className="text-xs uppercase tracking-[0.24em] text-slate-500">
                    What PilotVault SA offers
                  </p>
                  <h3 className="mt-3 text-2xl font-semibold tracking-[-0.03em]">
                    Everything needed for focused preparation.
                  </h3>
                </div>
                <span className="hidden text-right text-xs font-semibold uppercase tracking-[0.24em] text-[#f4b400] sm:block">
                  PPL today
                  <br />
                  CPL &amp; ATPL next
                </span>
              </div>

              <ul className="grid sm:grid-cols-2">
                {offering.map((item, index) => (
                  <li
                    key={item}
                    className={`flex min-h-24 items-center gap-4 border-b border-[#1e3a5f] py-5 text-sm font-medium text-slate-200 sm:px-5 ${
                      index % 2 === 0 ? "sm:border-r sm:pl-0" : "sm:pr-0"
                    }`}
                  >
                    <span className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-[#f4b400]/10 text-[#f4b400]">
                      <Check className="h-3.5 w-3.5" aria-hidden="true" />
                    </span>
                    {item}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </section>

        <section className="relative mx-auto max-w-7xl px-4 py-24 sm:px-6 lg:px-8 lg:py-32">
          <div
            aria-hidden="true"
            className="absolute inset-x-20 top-1/2 h-64 -translate-y-1/2 rounded-full bg-[#f4b400]/5 blur-3xl"
          />
          <div className="relative overflow-hidden rounded-[2rem] border border-[#f4b400]/25 bg-[linear-gradient(135deg,rgba(244,180,0,0.13),rgba(8,23,38,0.95)_46%,rgba(30,58,95,0.62))] px-6 py-16 text-center shadow-[0_28px_100px_rgba(0,0,0,0.28)] sm:px-12 lg:py-20">
            <div
              aria-hidden="true"
              className="absolute -right-20 -top-20 h-64 w-64 rounded-full border border-[#f4b400]/15"
            />
            <div
              aria-hidden="true"
              className="absolute -right-10 -top-10 h-44 w-44 rounded-full border border-[#f4b400]/10"
            />

            <p className="text-xs font-semibold uppercase tracking-[0.3em] text-[#f4b400]">
              The PilotVault standard
            </p>
            <h2 className="mx-auto mt-5 max-w-4xl text-4xl font-semibold leading-tight tracking-[-0.045em] sm:text-5xl lg:text-6xl">
              Real Questions. Real Explanations. Real Results.
            </h2>
            <p className="mx-auto mt-6 max-w-2xl text-base leading-7 text-slate-300 sm:text-lg">
              PilotVault SA exists to make SACAA exam preparation more focused,
              more realistic, and more accessible for South African student
              pilots.
            </p>
            <Link
              href="/dashboard"
              className="mt-9 inline-flex min-h-12 items-center justify-center gap-2 rounded-full bg-[#f4b400] px-7 text-sm font-bold text-[#06111f] transition hover:-translate-y-0.5 hover:bg-[#ffd054] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-white focus-visible:ring-offset-2 focus-visible:ring-offset-[#081726]"
            >
              Start Practicing
              <ArrowRight className="h-4 w-4" aria-hidden="true" />
            </Link>
          </div>
        </section>
      </main>

      <Footer />
    </div>
  )
}
