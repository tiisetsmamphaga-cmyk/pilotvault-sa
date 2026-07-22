"use client"

import Link from "next/link"
import {
  ArrowLeft,
  ArrowRight,
  BookOpen,
  ClipboardList,
  Download,
  LockKeyhole,
} from "lucide-react"

import { MOCK_QUESTION_COUNT, formatSubjectName } from "../practice-utils"

type SubjectManual = {
  title: string
  description: string
  href: string
  downloadName: string
}

const SUBJECT_MANUALS: Record<string, SubjectManual> = {
  meteorology: {
    title: "PPL Meteorology Manual",
    description: "Review weather symbols, METARs, TAFs and aviation charts.",
    href: "/PPL-MET.pdf",
    downloadName: "PilotVault-PPL-Meteorology-Manual.pdf",
  },
  "flight-planning": {
    title: "PPL Flight Planning Manual",
    description:
      "Review mass and balance, performance, fuel and runway planning charts.",
    href: "/FPLAN(A).pdf",
    downloadName: "PilotVault-PPL-Flight-Planning-Manual.pdf",
  },
}

type TrainingModeMenuProps = {
  subject: string
  questionCount: number
  isTrialAccount: boolean
  canAccessTopics: boolean
  onStartMock: () => void
  onOpenTopics: () => void
}

export function TrainingModeMenu({
  subject,
  questionCount,
  isTrialAccount,
  canAccessTopics,
  onStartMock,
  onOpenTopics,
}: TrainingModeMenuProps) {
  const manual = SUBJECT_MANUALS[subject]
  const mockQuestionCount = Math.min(MOCK_QUESTION_COUNT, questionCount)
  const subjectName = formatSubjectName(subject)

  return (
    <main className="min-h-screen bg-[#071522] text-white">
      <header className="border-b border-[#29476d] bg-[#081726]/95">
        <div className="mx-auto flex min-h-16 max-w-7xl items-center justify-between gap-3 px-4 sm:min-h-20 sm:px-6 lg:px-8">
          <div className="min-w-0">
            <p className="text-[10px] uppercase tracking-[0.22em] text-[#f4b400] sm:text-xs sm:tracking-[0.25em]">
              PilotVault SA
            </p>
            <h1 className="mt-1 truncate text-base font-bold sm:text-lg">
              {subjectName}
            </h1>
          </div>

          <Link
            href="/dashboard"
            aria-label="Back to dashboard"
            title="Back to dashboard"
            className="inline-flex h-10 w-10 items-center justify-center rounded-full bg-white text-[#071426] shadow-[0_6px_18px_rgba(15,23,42,0.12)] transition hover:-translate-x-0.5 hover:bg-[#f4b400] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#f4b400]/70"
          >
            <ArrowLeft className="h-[19px] w-[19px]" />
          </Link>
        </div>
      </header>

      <section className="mx-auto max-w-7xl px-4 py-8 sm:px-6 sm:py-10 lg:px-8">
        <div className="rounded-3xl border border-[#29476d] bg-[#0b1d31] p-5 shadow-[0_18px_50px_rgba(0,0,0,0.14)] sm:p-8">
          <h2 className="text-2xl font-bold tracking-tight sm:text-3xl">
            Choose a training mode
          </h2>
          <p className="mt-2 text-sm leading-6 text-[#b8c7d9] sm:text-base">
            Pick an option and start practising.
          </p>

          {manual && (
            <div className="mt-6 flex flex-col gap-4 border-t border-[#29476d] pt-5 sm:flex-row sm:items-center sm:justify-between">
              <div className="flex min-w-0 items-center gap-3">
                <span className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-[#f4b400]/20 text-[#f4b400]">
                  <BookOpen className="h-5 w-5" />
                </span>

                <div className="min-w-0">
                  <p className="text-[10px] font-bold uppercase tracking-[0.2em] text-[#f4b400]">
                    Study manual
                  </p>
                  <p className="mt-1 truncate font-semibold text-white">
                    {manual.title}
                  </p>
                </div>
              </div>

              <a
                href={manual.href}
                download={manual.downloadName}
                className="inline-flex h-10 shrink-0 items-center justify-center gap-2 rounded-xl border border-[#f4b400]/35 bg-[#f4b400]/10 px-4 text-sm font-bold text-[#f4b400] transition hover:border-[#f4b400] hover:bg-[#f4b400] hover:text-[#06111f] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#f4b400]/70"
              >
                <Download className="h-4 w-4" />
                Download
              </a>
            </div>
          )}
        </div>

        <div className="mt-5 grid gap-4 md:grid-cols-2">
          <button
            type="button"
            onClick={onStartMock}
            className="group flex min-h-[210px] cursor-pointer flex-col rounded-2xl border border-[#29476d] bg-[#0b1d31] p-5 text-left shadow-[0_14px_40px_rgba(0,0,0,0.12)] transition-all hover:-translate-y-1 hover:border-[#f4b400] hover:bg-[#0d2238] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#f4b400]/70 sm:p-6"
          >
            <div className="flex items-start justify-between gap-4">
              <span className="flex h-11 w-11 items-center justify-center rounded-xl bg-[#f4b400]/20 text-[#f4b400]">
                <ClipboardList className="h-5 w-5" />
              </span>

              {isTrialAccount && (
                <span className="text-[10px] font-bold uppercase tracking-[0.18em] text-[#f4b400]">
                  Trial
                </span>
              )}
            </div>

            <h3 className="mt-5 text-xl font-bold text-white sm:text-2xl">
              Mock exam
            </h3>
            <p className="mt-2 text-sm leading-6 text-[#b8c7d9]">
              {isTrialAccount
                ? "A fixed SACAA-style question set."
                : "Randomized SACAA-style exam questions."}
            </p>

            <div className="mt-auto flex items-center justify-between gap-4 pt-5">
              <span className="text-sm font-semibold text-[#b8c7d9]">
                {mockQuestionCount} questions
              </span>
              <span className="inline-flex items-center gap-2 rounded-xl bg-[#f4b400] px-3 py-2 text-xs font-bold text-[#06111f] transition group-hover:bg-[#ffc62a]">
                Start exam
                <ArrowRight className="h-3.5 w-3.5 transition-transform group-hover:translate-x-0.5" />
              </span>
            </div>
          </button>

          {canAccessTopics ? (
            <button
              type="button"
              onClick={onOpenTopics}
              className="group flex min-h-[210px] cursor-pointer flex-col rounded-2xl border border-[#29476d] bg-[#0b1d31] p-5 text-left shadow-[0_14px_40px_rgba(0,0,0,0.12)] transition-all hover:-translate-y-1 hover:border-[#f4b400] hover:bg-[#0d2238] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#f4b400]/70 sm:p-6"
            >
              <span className="flex h-11 w-11 items-center justify-center rounded-xl bg-[#f4b400]/20 text-[#f4b400]">
                <BookOpen className="h-5 w-5" />
              </span>

              <h3 className="mt-5 text-xl font-bold text-white sm:text-2xl">
                Practice by topic
              </h3>
              <p className="mt-2 text-sm leading-6 text-[#b8c7d9]">
                Focus on one subject area at a time.
              </p>

              <div className="mt-auto flex items-center justify-between gap-4 pt-5">
                <span className="text-sm font-semibold text-[#b8c7d9]">
                  No question limit
                </span>
                <span className="inline-flex items-center gap-2 rounded-xl bg-[#f4b400] px-3 py-2 text-xs font-bold text-[#06111f] transition group-hover:bg-[#ffc62a]">
                  Choose topic
                  <ArrowRight className="h-3.5 w-3.5 transition-transform group-hover:translate-x-0.5" />
                </span>
              </div>
            </button>
          ) : (
            <Link
              href={`/upgrade?subject=${subject}`}
              className="group flex min-h-[210px] flex-col rounded-2xl border border-[#29476d] bg-[#0b1d31] p-5 text-left shadow-[0_14px_40px_rgba(0,0,0,0.12)] transition-all hover:-translate-y-1 hover:border-[#f4b400] hover:bg-[#0d2238] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#f4b400]/70 sm:p-6"
            >
              <span className="flex h-11 w-11 items-center justify-center rounded-xl bg-[#f4b400]/10 text-[#f4b400]">
                <LockKeyhole className="h-5 w-5" />
              </span>

              <h3 className="mt-5 text-xl font-bold text-white sm:text-2xl">
                Practice by topic
              </h3>
              <p className="mt-2 text-sm leading-6 text-[#b8c7d9]">
                Unlock focused topic practice.
              </p>

              <div className="mt-auto flex justify-end pt-5">
                <span className="inline-flex items-center gap-2 rounded-xl border border-[#f4b400]/40 bg-[#f4b400]/10 px-3 py-2 text-xs font-bold text-[#f4b400] transition group-hover:bg-[#f4b400] group-hover:text-[#06111f]">
                  View access
                  <ArrowRight className="h-3.5 w-3.5 transition-transform group-hover:translate-x-0.5" />
                </span>
              </div>
            </Link>
          )}
        </div>
      </section>
    </main>
  )
}
