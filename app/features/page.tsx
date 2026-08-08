import Link from "next/link"
import {
  ArrowRight,
  ArrowUpRight,
  BarChart3,
  BookOpen,
  Check,
  CheckCircle2,
  Clock3,
  LockKeyhole,
  Target,
  Timer,
} from "lucide-react"

import { Footer } from "@/components/footer"
import { Navbar } from "@/components/navbar"

const features = [
  {
    number: "01",
    icon: BookOpen,
    title: "SACAA Question Bank",
    text: "Practice with aviation theory questions structured around South African SACAA subjects.",
    detail: "SACAA-focused preparation",
    className: "lg:col-span-2",
  },
  {
    number: "02",
    icon: Timer,
    title: "25-Question Mock Exams",
    text: "Simulate exam conditions with timed mock exams, question navigation, and final scoring.",
    detail: "Timed exam conditions",
    className: "lg:col-span-1",
  },
  {
    number: "03",
    icon: Target,
    title: "Topic-Based Practice",
    text: "Focus on specific topics and strengthen weak areas. Available with subscription.",
    detail: "Focused subscriber practice",
    className: "lg:col-span-1",
  },
  {
    number: "04",
    icon: BarChart3,
    title: "Progress Tracking",
    text: "Track performance, review incorrect answers, and monitor your exam readiness.",
    detail: "Clear performance insights",
    className: "lg:col-span-2",
  },
  {
    number: "05",
    icon: CheckCircle2,
    title: "Clear Explanations",
    text: "Understand why answers are correct with simple, focused explanations.",
    detail: "Learn beyond the score",
    className: "lg:col-span-1",
  },
  {
    number: "06",
    icon: LockKeyhole,
    title: "Trial & Subscription Access",
    text: "Start with a limited trial, then unlock the full PilotVault experience with a paid plan.",
    detail: "Start before you subscribe",
    className: "lg:col-span-2",
  },
]

const studyFlow = [
  {
    number: "01",
    title: "Practice",
    text: "Build subject knowledge with SACAA-focused questions and topic-based sessions.",
    icon: BookOpen,
  },
  {
    number: "02",
    title: "Simulate",
    text: "Step into timed 25-question mock exams with navigation and final scoring.",
    icon: Clock3,
  },
  {
    number: "03",
    title: "Improve",
    text: "Review incorrect answers, learn from explanations, and track your readiness.",
    icon: BarChart3,
  },
]

const platformAccess = [
  "Limited trial mock exam",
  "Full question bank with a paid plan",
  "Topic-based practice for subscribers",
  "Progress and performance tracking",
]

export default function FeaturesPage() {
  return (
    <div className="min-h-screen overflow-hidden bg-[#06111f] text-white">
      <Navbar />

      <main className="pt-20">
        <section className="relative border-b border-[#1e3a5f]/70">
          <div
            aria-hidden="true"
            className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_12%_18%,rgba(244,180,0,0.12),transparent_29%),radial-gradient(circle_at_88%_72%,rgba(30,58,95,0.38),transparent_36%)]"
          />
          <div
            aria-hidden="true"
            className="pointer-events-none absolute inset-0 opacity-[0.035] [background-image:linear-gradient(rgba(255,255,255,0.5)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.5)_1px,transparent_1px)] [background-size:72px_72px]"
          />

          <div className="relative mx-auto grid min-h-[680px] max-w-7xl items-center gap-16 px-4 py-20 sm:px-6 lg:grid-cols-[1.08fr_0.92fr] lg:px-8 lg:py-28">
            <div className="max-w-3xl">
              <p className="text-xs font-semibold uppercase tracking-[0.3em] text-[#f4b400]">
                Built for focused exam preparation
              </p>

              <h1 className="mt-6 text-5xl font-semibold leading-[0.98] tracking-[-0.055em] sm:text-6xl lg:text-[5.25rem]">
                Everything you need to prepare{" "}
                <span className="text-white/42">smarter.</span>
              </h1>

              <p className="mt-8 max-w-2xl text-base leading-7 text-slate-300 sm:text-lg sm:leading-8">
                PilotVault SA combines mock exams, question banks,
                explanations, and progress tools into one clean SACAA-focused
                study platform.
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
              <div className="overflow-hidden rounded-[2rem] border border-[#1e3a5f] bg-[#081726]/82 shadow-[0_28px_90px_rgba(0,0,0,0.24)] backdrop-blur-sm">
                <div className="flex items-start justify-between gap-6 border-b border-[#1e3a5f] px-6 py-6 sm:px-8">
                  <div>
                    <p className="text-[0.65rem] font-semibold uppercase tracking-[0.25em] text-[#f4b400]">
                      Mock exam format
                    </p>
                    <p className="mt-2 text-sm text-slate-400">
                      A focused SACAA-style study session
                    </p>
                  </div>
                  <span className="rounded-full border border-[#f4b400]/20 bg-[#f4b400]/10 px-3 py-1 text-[0.65rem] font-semibold uppercase tracking-[0.18em] text-[#f4b400]">
                    PilotVault
                  </span>
                </div>

                <div className="grid border-b border-[#1e3a5f] sm:grid-cols-[0.75fr_1.25fr]">
                  <div className="flex flex-col justify-between border-b border-[#1e3a5f] p-6 sm:border-b-0 sm:border-r sm:p-8">
                    <span className="text-7xl font-light tracking-[-0.08em] text-white">
                      25
                    </span>
                    <span className="mt-8 text-xs font-semibold uppercase leading-5 tracking-[0.2em] text-slate-500">
                      Questions per
                      <br />
                      mock exam
                    </span>
                  </div>

                  <div className="p-6 sm:p-8">
                    <p className="text-xs font-semibold uppercase tracking-[0.23em] text-slate-500">
                      Inside every attempt
                    </p>
                    <ul className="mt-5 space-y-4">
                      {[
                        "Timed exam conditions",
                        "Question navigation",
                        "Final scoring and review",
                      ].map((item) => (
                        <li
                          key={item}
                          className="flex items-center gap-3 text-sm text-slate-200"
                        >
                          <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-[#f4b400]/10 text-[#f4b400]">
                            <Check className="h-3.5 w-3.5" aria-hidden="true" />
                          </span>
                          {item}
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>

                <div className="flex items-center justify-between gap-6 px-6 py-5 sm:px-8">
                  <span className="text-sm text-slate-400">
                    Practice. Review. Improve.
                  </span>
                  <Target className="h-5 w-5 text-[#f4b400]" aria-hidden="true" />
                </div>
              </div>
            </div>
          </div>
        </section>

        <section className="mx-auto max-w-7xl px-4 py-24 sm:px-6 lg:px-8 lg:py-32">
          <div className="grid gap-8 lg:grid-cols-[0.8fr_1.2fr] lg:items-end">
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.3em] text-[#f4b400]">
                The complete toolkit
              </p>
              <h2 className="mt-5 max-w-xl text-4xl font-semibold tracking-[-0.04em] sm:text-5xl">
                Six tools. One focused platform.
              </h2>
            </div>
            <p className="max-w-2xl text-base leading-7 text-slate-400 lg:justify-self-end lg:text-lg">
              Every feature is designed around the same goal: helping South
              African student pilots prepare with more structure, clarity, and
              confidence.
            </p>
          </div>

          <div className="mt-14 grid gap-5 lg:grid-cols-3">
            {features.map((feature) => {
              const Icon = feature.icon

              return (
                <article
                  key={feature.number}
                  className={`group relative min-h-[310px] overflow-hidden rounded-[2rem] border border-[#1e3a5f] bg-[#081726]/72 p-7 transition duration-300 hover:-translate-y-1 hover:border-[#f4b400]/45 hover:bg-[#0a1a2c] sm:p-9 ${feature.className}`}
                >
                  <div
                    aria-hidden="true"
                    className="absolute -right-16 -top-20 h-52 w-52 rounded-full border border-white/[0.035] transition duration-500 group-hover:border-[#f4b400]/10"
                  />

                  <div className="relative flex h-full flex-col">
                    <div className="flex items-start justify-between gap-6">
                      <span className="text-sm font-semibold tracking-[0.18em] text-white/25 transition group-hover:text-[#f4b400]/55">
                        {feature.number}
                      </span>
                      <span className="flex h-11 w-11 items-center justify-center rounded-full border border-[#f4b400]/20 bg-[#f4b400]/10 text-[#f4b400]">
                        <Icon className="h-5 w-5" aria-hidden="true" />
                      </span>
                    </div>

                    <div className="mt-auto pt-16">
                      <p className="text-[0.65rem] font-semibold uppercase tracking-[0.22em] text-[#f4b400]">
                        {feature.detail}
                      </p>
                      <h3 className="mt-3 text-2xl font-semibold tracking-[-0.03em]">
                        {feature.title}
                      </h3>
                      <p className="mt-4 max-w-2xl text-sm leading-7 text-slate-400">
                        {feature.text}
                      </p>
                    </div>
                  </div>
                </article>
              )
            })}
          </div>
        </section>

        <section className="border-y border-[#1e3a5f]/70 bg-[#081726]/45">
          <div className="mx-auto max-w-7xl px-4 py-24 sm:px-6 lg:px-8 lg:py-32">
            <div className="mx-auto max-w-2xl text-center">
              <p className="text-xs font-semibold uppercase tracking-[0.3em] text-[#f4b400]">
                A smarter study loop
              </p>
              <h2 className="mt-5 text-4xl font-semibold tracking-[-0.04em] sm:text-5xl">
                Practice. Simulate. Improve.
              </h2>
              <p className="mt-5 text-base leading-7 text-slate-400 sm:text-lg">
                Move from focused preparation to realistic exam practice, then
                use every result to guide what comes next.
              </p>
            </div>

            <ol className="mt-14 overflow-hidden rounded-[2rem] border border-[#1e3a5f] bg-[#06111f]/55 lg:grid lg:grid-cols-3">
              {studyFlow.map((step, index) => {
                const Icon = step.icon

                return (
                  <li
                    key={step.number}
                    className={`relative p-7 sm:p-9 ${
                      index > 0
                        ? "border-t border-[#1e3a5f] lg:border-l lg:border-t-0"
                        : ""
                    }`}
                  >
                    <div className="flex items-center justify-between gap-5">
                      <span className="text-xs font-semibold uppercase tracking-[0.22em] text-slate-500">
                        Step {step.number}
                      </span>
                      <Icon className="h-5 w-5 text-[#f4b400]" aria-hidden="true" />
                    </div>
                    <h3 className="mt-12 text-3xl font-semibold tracking-[-0.04em]">
                      {step.title}
                    </h3>
                    <p className="mt-4 text-sm leading-7 text-slate-400">
                      {step.text}
                    </p>
                  </li>
                )
              })}
            </ol>
          </div>
        </section>

        <section className="mx-auto grid max-w-7xl gap-14 px-4 py-24 sm:px-6 lg:grid-cols-[0.9fr_1.1fr] lg:items-center lg:gap-24 lg:px-8 lg:py-32">
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.3em] text-[#f4b400]">
              Trial &amp; subscription access
            </p>
            <h2 className="mt-5 text-4xl font-semibold leading-tight tracking-[-0.04em] sm:text-5xl">
              Start small. Unlock the full experience when you&apos;re ready.
            </h2>
            <p className="mt-6 max-w-xl text-base leading-8 text-slate-400">
              Start with a limited trial, then upgrade to unlock the full
              question bank and topic-based practice.
            </p>

            <Link
              href="/dashboard"
              className="mt-8 inline-flex min-h-12 items-center justify-center gap-2 rounded-full bg-[#f4b400] px-7 text-sm font-bold text-[#06111f] transition hover:-translate-y-0.5 hover:bg-[#ffd054] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#f4b400] focus-visible:ring-offset-2 focus-visible:ring-offset-[#06111f]"
            >
              Start Practicing
              <ArrowRight className="h-4 w-4" aria-hidden="true" />
            </Link>
          </div>

          <div className="border-t border-[#355274]">
            {platformAccess.map((item, index) => (
              <div
                key={item}
                className="grid grid-cols-[auto_1fr_auto] items-center gap-4 border-b border-[#1e3a5f] py-5 sm:py-6"
              >
                <span className="text-xs font-semibold tracking-[0.18em] text-white/25">
                  {String(index + 1).padStart(2, "0")}
                </span>
                <span className="text-sm font-medium text-slate-200 sm:text-base">
                  {item}
                </span>
                <Check className="h-4 w-4 text-[#f4b400]" aria-hidden="true" />
              </div>
            ))}
          </div>
        </section>

        <section className="relative mx-auto max-w-7xl px-4 pb-24 sm:px-6 lg:px-8 lg:pb-32">
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
              Built to help you pass
            </p>
            <h2 className="mx-auto mt-5 max-w-4xl text-4xl font-semibold leading-tight tracking-[-0.045em] sm:text-5xl lg:text-6xl">
              Prepare for your next SACAA exam with confidence.
            </h2>
            <p className="mx-auto mt-6 max-w-2xl text-base leading-7 text-slate-300 sm:text-lg">
              Start with a trial mock exam, then unlock the full PilotVault
              experience when you are ready to go further.
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
