"use client"

import Link from "next/link"
import {
  BookOpen,
  ClipboardList,
  Crosshair,
  Download,
  GraduationCap,
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

  return (
    <main className="min-h-screen bg-[#06111f] px-4 py-10 text-white sm:px-6">
      <div className="mx-auto max-w-5xl">
        <Link
          href="/dashboard"
          className="text-sm font-medium text-[#f4b400] hover:text-white"
        >
          ← Back to Dashboard
        </Link>

        <div className="mt-8 rounded-3xl border border-[#1e3a5f] bg-[#081726] p-6 sm:p-8">
          <p className="text-xs uppercase tracking-[0.25em] text-[#f4b400]">
            {formatSubjectName(subject)}
          </p>

          <h1 className="mt-3 text-3xl font-bold sm:text-4xl">
            Choose your training mode
          </h1>

          <p className="mt-3 max-w-2xl text-gray-400">
            Start a SACAA-style mock exam or focus on weak areas with
            topic-based practice.
          </p>

          {!isTrialAccount && (
            <p className="mt-4 text-sm font-semibold text-[#f4b400]">
              {questionCount} questions available
            </p>
          )}

          {manual && (
            <div className="mt-6 flex flex-col gap-4 rounded-2xl border border-[#1e3a5f] bg-[#06111f]/70 p-4 sm:flex-row sm:items-center sm:justify-between">
              <div className="flex min-w-0 items-start gap-3">
                <div className="rounded-xl border border-[#1e3a5f] bg-[#0b1d31] p-3 text-[#f4b400]">
                  <BookOpen size={21} />
                </div>

                <div className="min-w-0">
                  <p className="text-xs font-bold uppercase tracking-[0.2em] text-[#f4b400]">
                    Study Resource
                  </p>
                  <p className="mt-1 font-semibold text-white">
                    {manual.title}
                  </p>
                  <p className="mt-1 text-sm leading-6 text-gray-400">
                    {manual.description}
                  </p>
                </div>
              </div>

              <a
                href={manual.href}
                download={manual.downloadName}
                className="inline-flex shrink-0 items-center justify-center gap-2 rounded-xl border border-[#f4b400]/40 bg-[#f4b400]/10 px-4 py-3 text-sm font-semibold text-[#f4b400] transition hover:border-[#f4b400] hover:bg-[#f4b400] hover:text-[#06111f]"
              >
                <Download size={17} />
                Download Manual
              </a>
            </div>
          )}
        </div>

        <div className="mt-8 grid gap-5 md:grid-cols-2">
          <button
            onClick={onStartMock}
            className="group cursor-pointer rounded-2xl border border-[#1e3a5f] bg-gradient-to-br from-[#081726] to-[#06111f] p-4 text-left shadow-2xl transition-all hover:-translate-y-1 hover:border-[#f4b400] hover:shadow-[0_0_30px_rgba(244,180,0,0.12)]"
          >
            <div className="inline-flex items-center gap-2 rounded-md border border-[#1e3a5f] bg-white/5 px-3 py-1 text-[10px] font-bold uppercase tracking-wider text-[#f4b400]">
              <GraduationCap size={14} />
              {isTrialAccount ? "Trial Access" : "Full Access"}
            </div>

            <div className="mt-4 flex items-center justify-between gap-5">
              <div className="flex items-start gap-4">
                <div className="rounded-xl border border-[#1e3a5f] bg-[#0b1d31] p-3 text-[#9bb7ff]">
                  <ClipboardList size={28} />
                </div>

                <div>
                  <h2 className="text-xl font-bold text-white">Mock Exam</h2>
                  <p className="mt-2 max-w-sm text-sm leading-6 text-gray-400">
                    {isTrialAccount
                      ? "25 fixed SACAA-style trial questions for exam practice."
                      : "25 randomized SACAA-style questions from the full question bank."}
                  </p>
                </div>
              </div>

              <div className="hidden h-24 w-24 shrink-0 items-center justify-center rounded-full border border-[#1e3a5f] bg-[#06111f] md:flex">
                <div className="text-center">
                  <p className="text-3xl font-bold text-white">
                    {Math.min(MOCK_QUESTION_COUNT, questionCount)}
                  </p>
                  <p className="text-[10px] uppercase tracking-widest text-gray-400">
                    Questions
                  </p>
                </div>
              </div>
            </div>
          </button>

          {canAccessTopics ? (
            <button
              onClick={onOpenTopics}
              className="group cursor-pointer rounded-2xl border border-[#1e3a5f] bg-gradient-to-br from-[#081726] to-[#06111f] p-4 text-left shadow-2xl transition-all hover:-translate-y-1 hover:border-[#f4b400] hover:shadow-[0_0_30px_rgba(244,180,0,0.12)]"
            >
              <div className="inline-flex items-center gap-2 rounded-md border border-[#1e3a5f] bg-white/5 px-3 py-1 text-[10px] font-bold uppercase tracking-wider text-[#f4b400]">
                <Crosshair size={14} />
                Full Access
              </div>

              <div className="mt-4 flex items-center justify-between gap-5">
                <div className="flex items-start gap-4">
                  <div className="rounded-xl border border-[#1e3a5f] bg-[#0b1d31] p-3 text-[#9bb7ff]">
                    <BookOpen size={28} />
                  </div>

                  <div>
                    <h2 className="text-xl font-bold text-white">
                      Practice by Topic
                    </h2>
                    <p className="mt-2 max-w-sm text-sm leading-6 text-gray-400">
                      Practice every available question from a selected topic
                      with no question cap.
                    </p>
                  </div>
                </div>

                <div className="hidden h-24 w-24 shrink-0 items-center justify-center rounded-full border border-[#1e3a5f] bg-[#06111f] text-[#f4b400] md:flex">
                  <Crosshair size={38} />
                </div>
              </div>
            </button>
          ) : (
            <Link
              href={`/upgrade?subject=${subject}`}
              className="group cursor-pointer rounded-2xl border border-[#1e3a5f] bg-[#081726]/60 p-4 text-left opacity-75 transition-all hover:-translate-y-1 hover:border-[#f4b400]"
            >
              <p className="text-xs uppercase tracking-[0.25em] text-[#f4b400]">
                Subscription Feature
              </p>
              <h2 className="mt-3 text-xl font-bold text-white">
                Practice by Topic
              </h2>
              <p className="mt-2 text-sm leading-6 text-gray-400">
                Target weak areas by topic using the full PilotVault question
                bank.
              </p>
            </Link>
          )}
        </div>
      </div>
    </main>
  )
}
