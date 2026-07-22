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
    <main className="min-h-screen bg-[#06111f] text-white">
      <header className="border-b border-[#1e3a5f] bg-[#06111f]/95">
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
            className="group flex h-11 items-center gap-2 rounded-2xl border border-[#1e3a5f] bg-[#081726] px-3 text-sm font-semibold text-gray-300 transition hover:border-[#f4b400]/60 hover:text-[#f4b400] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#f4b400]/70 sm:px-4"
          >
            <ArrowLeft className="h-4 w-4 transition-transform group-hover:-translate-x-0.5" />
            <span className="hidden sm:inline">Dashboard</span>
          </Link>
        </div>
      </header>

      <section className="mx-auto max-w-7xl px-4 py-8 sm:px-6 sm:py-10 lg:px-8">
        <div className="rounded-3xl border border-[#1e3a5f] bg-[#081726] p-5 sm:p-8">
          <div className="flex flex-wrap items-start justify-between gap-4">
            <div>
              <p className="text-xs uppercase tracking-[0.25em] text-[#f4b400]">
                Training Center
              </p>

              <h2 className="mt-3 text-2xl font-bold leading-tight sm:text-4xl">
                Choose your training mode
              </h2>

              <p className="mt-3 max-w-2xl text-sm leading-6 text-gray-400 sm:text-base">
                Simulate the SACAA exam or work through a specific topic at your
                own pace.
              </p>
            </div>

            <span className="inline-flex items-center gap-2 rounded-xl border border-[#1e3a5f] bg-[#06111f]/60 px-3 py-2 text-xs font-semibold text-gray-300">
              <span className="h-1.5 w-1.5 rounded-full bg-[#f4b400]" />
              {isTrialAccount
                ? `${mockQuestionCount} trial questions`
                : `${questionCount} questions available`}
            </span>
          </div>

          {manual && (
            <div className="mt-6 flex flex-col gap-4 border-t border-[#1e3a5f] pt-5 sm:flex-row sm:items-center sm:justify-between">
              <div className="flex min-w-0 items-center gap-4">
                <span className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-[#f4b400]/20 text-[#f4b400]">
                  <BookOpen className="h-5 w-5" />
                </span>

                <div className="min-w-0">
                  <p className="text-[10px] font-bold uppercase tracking-[0.22em] text-[#f4b400]">
                    Study resource
                  </p>
                  <p className="mt-1 font-semibold text-white">{manual.title}</p>
                  <p className="mt-1 text-sm leading-5 text-gray-400">
                    {manual.description}
                  </p>
                </div>
              </div>

              <a
                href={manual.href}
                download={manual.downloadName}
                className="inline-flex h-11 shrink-0 items-center justify-center gap-2 rounded-xl bg-[#f4b400] px-4 text-sm font-bold text-[#06111f] transition hover:bg-[#d9a000] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#f4b400]/70"
              >
                <Download className="h-4 w-4" />
                Download manual
              </a>
            </div>
          )}
        </div>

        <div className="mt-6 grid gap-3 sm:gap-5 md:grid-cols-2">
          <button
            type="button"
            onClick={onStartMock}
            className="group flex min-h-[230px] cursor-pointer flex-col rounded-2xl border border-[#f4b400]/40 bg-[#081726] p-5 text-left transition-all hover:-translate-y-1 hover:border-[#f4b400] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#f4b400]/70 sm:p-6"
          >
            <div className="flex items-start justify-between gap-4">
              <span className="flex h-10 w-10 items-center justify-center rounded-xl bg-[#f4b400]/20 text-[#f4b400] sm:h-12 sm:w-12">
                <ClipboardList className="h-5 w-5 sm:h-6 sm:w-6" />
              </span>

              <span className="text-[10px] font-bold uppercase tracking-[0.18em] text-[#f4b400]">
                {isTrialAccount ? "Trial access" : "Full access"}
              </span>
            </div>

            <h3 className="mt-5 text-xl font-bold text-white sm:text-2xl">
              Mock exam
            </h3>
            <p className="mt-2 max-w-md text-sm leading-6 text-gray-400">
              {isTrialAccount
                ? "Complete a fixed set of SACAA-style questions in an exam-focused session."
                : "Complete a randomized set of SACAA-style questions from the full question bank."}
            </p>

            <div className="mt-auto flex items-center justify-between gap-4 pt-6">
              <span className="text-sm font-semibold text-gray-400">
                {mockQuestionCount} questions
              </span>
              <span className="inline-flex items-center gap-2 text-sm font-bold text-[#f4b400]">
                Start exam
                <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-1" />
              </span>
            </div>
          </button>

          {canAccessTopics ? (
            <button
              type="button"
              onClick={onOpenTopics}
              className="group flex min-h-[230px] cursor-pointer flex-col rounded-2xl border border-[#f4b400]/40 bg-[#081726] p-5 text-left transition-all hover:-translate-y-1 hover:border-[#f4b400] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#f4b400]/70 sm:p-6"
            >
              <div className="flex items-start justify-between gap-4">
                <span className="flex h-10 w-10 items-center justify-center rounded-xl bg-[#f4b400]/20 text-[#f4b400] sm:h-12 sm:w-12">
                  <BookOpen className="h-5 w-5 sm:h-6 sm:w-6" />
                </span>

                <span className="text-[10px] font-bold uppercase tracking-[0.18em] text-[#f4b400]">
                  Full access
                </span>
              </div>

              <h3 className="mt-5 text-xl font-bold text-white sm:text-2xl">
                Practice by topic
              </h3>
              <p className="mt-2 max-w-md text-sm leading-6 text-gray-400">
                Target a weak area and work through every available question
                from that topic with no question cap.
              </p>

              <div className="mt-auto flex items-center justify-between gap-4 pt-6">
                <span className="text-sm font-semibold text-gray-400">
                  No question limit
                </span>
                <span className="inline-flex items-center gap-2 text-sm font-bold text-[#f4b400]">
                  Choose topic
                  <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-1" />
                </span>
              </div>
            </button>
          ) : (
            <Link
              href={`/upgrade?subject=${subject}`}
              className="group flex min-h-[230px] flex-col rounded-2xl border border-[#1e3a5f] bg-[#081726] p-5 text-left opacity-60 transition-all hover:-translate-y-1 hover:border-[#f4b400] hover:opacity-100 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#f4b400]/70 sm:p-6"
            >
              <div className="flex items-start justify-between gap-4">
                <span className="flex h-10 w-10 items-center justify-center rounded-xl bg-[#f4b400]/10 text-[#f4b400]/60 sm:h-12 sm:w-12">
                  <LockKeyhole className="h-5 w-5" />
                </span>

                <span className="text-[10px] font-bold uppercase tracking-[0.18em] text-[#f4b400]">
                  Upgrade required
                </span>
              </div>

              <h3 className="mt-5 text-xl font-bold text-white sm:text-2xl">
                Practice by topic
              </h3>
              <p className="mt-2 max-w-md text-sm leading-6 text-gray-400">
                Target weak areas by topic using the full PilotVault question
                bank.
              </p>

              <div className="mt-auto flex justify-end pt-6">
                <span className="inline-flex items-center gap-2 text-sm font-bold text-[#f4b400]">
                  View access options
                  <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-1" />
                </span>
              </div>
            </Link>
          )}
        </div>
      </section>
    </main>
  )
}
