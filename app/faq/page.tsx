import Link from "next/link"
import {
  ArrowRight,
  BookOpenCheck,
  Check,
  Mail,
  Plus,
  ShieldCheck,
} from "lucide-react"

import { Footer } from "@/components/footer"
import { Navbar } from "@/components/navbar"

const faqGroups = [
  {
    number: "01",
    label: "Platform basics",
    title: "Understanding PilotVault",
    faqs: [
      {
        question: "What is PilotVault SA?",
        answer:
          "PilotVault SA is a SACAA-focused aviation exam preparation platform designed to help South African student pilots prepare for their theory exams through mock exams, question banks, and explanations.",
      },
      {
        question: "Is PilotVault SA affiliated with SACAA?",
        answer:
          "No. PilotVault SA is an independent educational platform and is not affiliated with, endorsed by, or operated by the South African Civil Aviation Authority (SACAA).",
      },
      {
        question: "What subjects are available?",
        answer:
          "Current subjects include Air Law, Meteorology, Navigation, Human Performance, Principles of Flight, Aircraft Technical and General, Radio Telephony, and Flight Planning.",
      },
    ],
  },
  {
    number: "02",
    label: "Access & plans",
    title: "Trials and subscriptions",
    faqs: [
      {
        question: "How does the free trial work?",
        answer:
          "New users receive a 3-day trial with access to all available subjects and a fixed 25-question mock exam for each subject.",
      },
      {
        question: "What happens when my trial expires?",
        answer:
          "When your trial expires, access to practice content will be restricted until you upgrade to a paid subscription.",
      },
      {
        question: "What do I get with a subscription?",
        answer:
          "Subscribers unlock topic-based practice, expanded mock exams, full question banks, detailed explanations, and future premium features.",
      },
      {
        question: "Can I practice specific topics?",
        answer:
          "Yes. Topic-based practice is available to active subscribers and helps you focus on weak areas within each subject.",
      },
    ],
  },
  {
    number: "03",
    label: "Exam preparation",
    title: "Mock exams and progress",
    faqs: [
      {
        question: "Do mock exams have a timer?",
        answer:
          "Yes. Mock exams simulate exam conditions with timed sessions, question navigation, scoring, and answer review.",
      },
      {
        question: "Will my progress be saved?",
        answer:
          "PilotVault SA is being developed with progress tracking features that will allow students to monitor performance and identify weak areas.",
      },
    ],
  },
  {
    number: "04",
    label: "Direct support",
    title: "Getting help",
    faqs: [
      {
        question: "How do I contact support?",
        answer:
          "Email our support team at support@pilotvault.co.za. We aim to respond to all enquiries as quickly as possible.",
        email: true,
      },
    ],
  },
]

export default function FAQPage() {
  return (
    <div className="min-h-screen overflow-hidden bg-[#06111f] text-white">
      <Navbar />

      <main className="pt-20">
        <section className="relative border-b border-[#1e3a5f]/70">
          <div
            aria-hidden="true"
            className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_12%_20%,rgba(244,180,0,0.12),transparent_30%),radial-gradient(circle_at_88%_72%,rgba(30,58,95,0.4),transparent_38%)]"
          />
          <div
            aria-hidden="true"
            className="pointer-events-none absolute inset-0 opacity-[0.035] [background-image:linear-gradient(rgba(255,255,255,0.5)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.5)_1px,transparent_1px)] [background-size:72px_72px]"
          />

          <div className="relative mx-auto grid min-h-[640px] max-w-7xl items-center gap-16 px-4 py-20 sm:px-6 lg:grid-cols-[1.08fr_0.92fr] lg:px-8 lg:py-28">
            <div className="max-w-3xl">
              <p className="text-xs font-semibold uppercase tracking-[0.3em] text-[#f4b400]">
                PilotVault help centre
              </p>
              <h1 className="mt-6 text-5xl font-semibold leading-[0.98] tracking-[-0.055em] sm:text-6xl lg:text-[5.25rem]">
                Questions answered.{" "}
                <span className="text-white/40">Confidence restored.</span>
              </h1>
              <p className="mt-8 max-w-2xl text-base leading-7 text-slate-300 sm:text-lg sm:leading-8">
                Everything you need to know about PilotVault SA, trial access,
                subscriptions, mock exams, and SACAA-focused preparation.
              </p>
            </div>

            <div className="lg:pl-8">
              <div className="overflow-hidden rounded-[2rem] border border-[#1e3a5f] bg-[#081726]/82 shadow-[0_28px_90px_rgba(0,0,0,0.24)] backdrop-blur-sm">
                <div className="border-b border-[#1e3a5f] px-6 py-6 sm:px-8">
                  <p className="text-[0.65rem] font-semibold uppercase tracking-[0.25em] text-[#f4b400]">
                    Quick answers
                  </p>
                  <p className="mt-2 text-sm text-slate-400">
                    Clear guidance before your next study session.
                  </p>
                </div>

                <div className="divide-y divide-[#1e3a5f]">
                  {[
                    { value: "10", label: "Common questions", icon: Check },
                    { value: "08", label: "SACAA PPL subjects", icon: BookOpenCheck },
                    { value: "01", label: "Direct support email", icon: ShieldCheck },
                  ].map((item) => {
                    const Icon = item.icon

                    return (
                      <div
                        key={item.label}
                        className="grid grid-cols-[auto_1fr_auto] items-center gap-5 px-6 py-5 sm:px-8"
                      >
                        <span className="text-3xl font-light tracking-[-0.05em] text-white">
                          {item.value}
                        </span>
                        <span className="text-sm text-slate-400">{item.label}</span>
                        <Icon className="h-4 w-4 text-[#f4b400]" aria-hidden="true" />
                      </div>
                    )
                  })}
                </div>

                <a
                  href="mailto:support@pilotvault.co.za"
                  className="flex min-h-16 items-center justify-between gap-5 bg-[#f4b400] px-6 text-sm font-bold text-[#06111f] transition hover:bg-[#ffd054] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-white focus-visible:ring-inset sm:px-8"
                >
                  Email support@pilotvault.co.za
                  <Mail className="h-4 w-4" aria-hidden="true" />
                </a>
              </div>
            </div>
          </div>
        </section>

        <section className="mx-auto max-w-7xl px-4 py-24 sm:px-6 lg:px-8 lg:py-32">
          <div className="grid gap-8 lg:grid-cols-[0.8fr_1.2fr] lg:items-end">
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.3em] text-[#f4b400]">
                Frequently asked questions
              </p>
              <h2 className="mt-5 max-w-xl text-4xl font-semibold tracking-[-0.04em] sm:text-5xl">
                Find what you need, fast.
              </h2>
            </div>
            <p className="max-w-2xl text-base leading-7 text-slate-400 lg:justify-self-end lg:text-lg">
              Browse the sections below for straightforward answers about the
              platform and your access. Select any question to reveal the
              answer.
            </p>
          </div>

          <div className="mt-16 space-y-20 lg:space-y-24">
            {faqGroups.map((group) => (
              <section
                key={group.number}
                className="grid gap-8 lg:grid-cols-[0.72fr_1.28fr] lg:gap-20"
              >
                <div>
                  <div className="flex items-center gap-4">
                    <span className="text-xs font-semibold tracking-[0.2em] text-white/25">
                      {group.number}
                    </span>
                    <span className="h-px w-10 bg-[#f4b400]/50" />
                    <span className="text-[0.65rem] font-semibold uppercase tracking-[0.23em] text-[#f4b400]">
                      {group.label}
                    </span>
                  </div>
                  <h3 className="mt-5 max-w-sm text-3xl font-semibold tracking-[-0.04em] sm:text-4xl">
                    {group.title}
                  </h3>
                </div>

                <div className="border-t border-[#355274]">
                  {group.faqs.map((faq, index) => (
                    <details
                      key={faq.question}
                      className="group border-b border-[#1e3a5f]"
                      open={group.number === "01" && index === 0}
                    >
                      <summary className="flex cursor-pointer list-none items-center justify-between gap-6 py-6 text-left marker:content-none sm:py-7 [&::-webkit-details-marker]:hidden">
                        <span className="text-base font-semibold text-slate-100 transition group-hover:text-[#f4b400] sm:text-lg">
                          {faq.question}
                        </span>
                        <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full border border-[#355274] text-[#f4b400] transition group-hover:border-[#f4b400]/60 group-open:rotate-45 group-open:border-[#f4b400]/60 group-open:bg-[#f4b400]/10">
                          <Plus className="h-4 w-4" aria-hidden="true" />
                        </span>
                      </summary>

                      <div className="max-w-2xl pb-7 pr-14 text-sm leading-7 text-slate-400 sm:text-base sm:leading-8">
                        {"email" in faq && faq.email ? (
                          <p>
                            Email our support team at{" "}
                            <a
                              href="mailto:support@pilotvault.co.za"
                              className="font-semibold text-[#f4b400] underline decoration-[#f4b400]/35 underline-offset-4 transition hover:text-[#ffd054]"
                            >
                              support@pilotvault.co.za
                            </a>
                            . We aim to respond to all enquiries as quickly as
                            possible.
                          </p>
                        ) : (
                          <p>{faq.answer}</p>
                        )}
                      </div>
                    </details>
                  ))}
                </div>
              </section>
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
            <p className="text-xs font-semibold uppercase tracking-[0.3em] text-[#f4b400]">
              Still need help?
            </p>
            <h2 className="mx-auto mt-5 max-w-4xl text-4xl font-semibold leading-tight tracking-[-0.045em] sm:text-5xl lg:text-6xl">
              Speak directly to PilotVault support.
            </h2>
            <p className="mx-auto mt-6 max-w-2xl text-base leading-7 text-slate-300 sm:text-lg">
              Send us your question and we&apos;ll help you get back to focused
              exam preparation.
            </p>
            <div className="mt-9 flex flex-col items-center justify-center gap-3 sm:flex-row">
              <a
                href="mailto:support@pilotvault.co.za"
                className="inline-flex min-h-12 items-center justify-center gap-2 rounded-full bg-[#f4b400] px-7 text-sm font-bold text-[#06111f] transition hover:-translate-y-0.5 hover:bg-[#ffd054] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-white focus-visible:ring-offset-2 focus-visible:ring-offset-[#081726]"
              >
                Email Support
                <Mail className="h-4 w-4" aria-hidden="true" />
              </a>
              <Link
                href="/features"
                className="inline-flex min-h-12 items-center justify-center gap-2 rounded-full border border-[#355274] bg-white/[0.025] px-7 text-sm font-semibold text-white transition hover:-translate-y-0.5 hover:border-[#f4b400]/70 hover:text-[#f4b400] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#f4b400] focus-visible:ring-offset-2 focus-visible:ring-offset-[#081726]"
              >
                Explore Features
                <ArrowRight className="h-4 w-4" aria-hidden="true" />
              </Link>
            </div>
          </div>
        </section>
      </main>

      <Footer />
    </div>
  )
}
