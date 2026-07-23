"use client"

import { useState } from "react"
import Link from "next/link"
import {
  ArrowLeft,
  ArrowRight,
  BookOpen,
  ClipboardList,
  Download,
  LockKeyhole,
} from "lucide-react"

import {
  MOCK_QUESTION_COUNT,
  MOCK_TIME_SECONDS,
  PASS_MARK,
  formatSubjectName,
  formatTime,
} from "../practice-utils"

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
  mockAverageScore: number | null
  mockAttemptCount: number
  savedMockAttempt?: {
    answeredCount: number
    totalQuestions: number
    timeLeft: number
  } | null
  onStartMock: () => void
  onContinueMock?: () => void
  onOpenTopics: () => void
}

function getReadinessStatus(averageScore: number | null) {
  if (averageScore === null) {
    return {
      label: "No attempts yet",
      className: "text-[#8fa7c2]",
    }
  }

  if (averageScore >= 85) {
    return {
      label: "Highly ready",
      className: "text-emerald-400",
    }
  }

  if (averageScore >= PASS_MARK) {
    return {
      label: "Exam ready",
      className: "text-emerald-400",
    }
  }

  if (averageScore >= 60) {
    return {
      label: "Almost ready",
      className: "text-[#f4b400]",
    }
  }

  return {
    label: "Keep practising",
    className: "text-orange-400",
  }
}

export function TrainingModeMenu({
  subject,
  questionCount,
  isTrialAccount,
  canAccessTopics,
  mockAverageScore,
  mockAttemptCount,
  savedMockAttempt = null,
  onStartMock,
  onContinueMock,
  onOpenTopics,
}: TrainingModeMenuProps) {
  const manual = SUBJECT_MANUALS[subject]
  const mockQuestionCount = Math.min(MOCK_QUESTION_COUNT, questionCount)
  const subjectName = formatSubjectName(subject)
  const mockDurationMinutes = Math.ceil(MOCK_TIME_SECONDS / 60)
  const readinessStatus = getReadinessStatus(mockAverageScore)
  const averageProgress = mockAverageScore ?? 0
  const progressCircumference = 239
  const progressOffset =
    progressCircumference * (1 - averageProgress / 100)
  const [showMockInstructions, setShowMockInstructions] = useState(false)

  const beginMockExam = () => {
    setShowMockInstructions(false)
    onStartMock()
  }

  const continueMockExam = () => {
    if (!onContinueMock) {
      return
    }

    setShowMockInstructions(false)
    onContinueMock()
  }

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
            onClick={() => setShowMockInstructions(true)}
            className="group relative flex min-h-[210px] cursor-pointer flex-col rounded-2xl border border-[#29476d] bg-[#0b1d31] p-5 text-left shadow-[0_14px_40px_rgba(0,0,0,0.12)] transition-all hover:-translate-y-1 hover:border-[#f4b400] hover:bg-[#0d2238] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#f4b400]/70 sm:p-6"
          >
            <div className="flex items-center gap-3">
              <span className="flex h-11 w-11 items-center justify-center rounded-xl bg-[#f4b400]/20 text-[#f4b400]">
                <ClipboardList className="h-5 w-5" />
              </span>

              {isTrialAccount && (
                <span className="text-[10px] font-bold uppercase tracking-[0.18em] text-[#f4b400]">
                  Trial
                </span>
              )}
            </div>

            <div
              role="img"
              className="absolute right-5 top-5 flex flex-col items-center sm:right-6 sm:top-6"
              aria-label={
                mockAverageScore === null
                  ? "No completed mock exams yet"
                  : `${mockAverageScore}% average from ${mockAttemptCount} completed mock ${
                      mockAttemptCount === 1 ? "exam" : "exams"
                    }. ${readinessStatus.label}.`
              }
            >
              <div className="relative h-[88px] w-[88px]">
                <svg
                  aria-hidden="true"
                  className="h-full w-full -rotate-90"
                  viewBox="0 0 88 88"
                >
                  <circle
                    cx="44"
                    cy="44"
                    r="38"
                    fill="#071522"
                    stroke="#244667"
                    strokeWidth="6"
                  />
                  <circle
                    cx="44"
                    cy="44"
                    r="38"
                    fill="none"
                    stroke="#3b82f6"
                    strokeDasharray={progressCircumference}
                    strokeDashoffset={progressOffset}
                    strokeLinecap="round"
                    strokeWidth="6"
                  />
                </svg>

                <div className="absolute inset-0 flex flex-col items-center justify-center">
                  <span className="text-xl font-extrabold leading-none text-white">
                    {mockAverageScore === null
                      ? "—"
                      : `${mockAverageScore}%`}
                  </span>
                  <span className="mt-1 text-[9px] font-bold uppercase tracking-[0.16em] text-[#8fa7c2]">
                    Average
                  </span>
                </div>
              </div>

              <span
                className={`mt-2 text-[10px] font-bold uppercase tracking-[0.13em] ${readinessStatus.className}`}
              >
                {readinessStatus.label}
              </span>
            </div>

            <h3 className="mt-5 pr-28 text-xl font-bold text-white sm:text-2xl">
              Mock exam
            </h3>
            <p className="mt-2 pr-28 text-sm leading-6 text-[#b8c7d9]">
              {isTrialAccount
                ? "A fixed SACAA-style question set."
                : "Randomized SACAA-style exam questions."}
            </p>

            <div className="mt-auto flex justify-end pt-5">
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

              <div className="mt-auto flex justify-end pt-5">
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

      {showMockInstructions && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 px-4 py-6 sm:px-6"
          role="dialog"
          aria-modal="true"
          aria-labelledby="mock-exam-title"
          onClick={() => setShowMockInstructions(false)}
        >
          <div
            className="w-full max-w-lg overflow-hidden bg-white text-slate-900 shadow-2xl"
            onClick={(event) => event.stopPropagation()}
          >
            <div className="bg-[#1f4e79] px-6 py-5 text-white">
              <p className="text-xs font-semibold uppercase tracking-[0.16em] text-blue-100">
                PilotVault SA Exam Practice
              </p>
              <h2 id="mock-exam-title" className="mt-1 text-2xl font-bold">
                Ready to start?
              </h2>
            </div>

            <div className="p-6">
              <div className="grid grid-cols-3 gap-2">
                <div className="rounded-md border border-slate-200 bg-slate-50 p-3 text-center">
                  <p className="text-xl font-bold text-[#1f4e79]">
                    {mockQuestionCount}
                  </p>
                  <p className="mt-1 text-[10px] font-semibold uppercase tracking-wide text-slate-500">
                    Questions
                  </p>
                </div>
                <div className="rounded-md border border-slate-200 bg-slate-50 p-3 text-center">
                  <p className="text-xl font-bold text-[#1f4e79]">
                    {mockDurationMinutes}
                  </p>
                  <p className="mt-1 text-[10px] font-semibold uppercase tracking-wide text-slate-500">
                    Minutes
                  </p>
                </div>
                <div className="rounded-md border border-slate-200 bg-slate-50 p-3 text-center">
                  <p className="text-xl font-bold text-[#1f4e79]">
                    {PASS_MARK}%
                  </p>
                  <p className="mt-1 text-[10px] font-semibold uppercase tracking-wide text-slate-500">
                    Pass mark
                  </p>
                </div>
              </div>

              <h3 className="mt-6 font-bold text-slate-900">
                Before you begin
              </h3>
              <ul className="mt-3 space-y-3 text-sm leading-6 text-slate-700">
                <li className="flex gap-3">
                  <span className="mt-2 h-1.5 w-1.5 shrink-0 rounded-full bg-[#1f4e79]" />
                  The timer starts as soon as you enter the simulator.
                </li>
                <li className="flex gap-3">
                  <span className="mt-2 h-1.5 w-1.5 shrink-0 rounded-full bg-[#1f4e79]" />
                  You can move between questions and pin any question for
                  review.
                </li>
                <li className="flex gap-3">
                  <span className="mt-2 h-1.5 w-1.5 shrink-0 rounded-full bg-[#1f4e79]" />
                  Unanswered questions count as incorrect, and the exam submits
                  automatically when time expires.
                </li>
              </ul>

              {savedMockAttempt && onContinueMock && (
                <div className="mt-6 border border-[#1f4e79]/25 bg-blue-50 px-4 py-3">
                  <p className="text-sm font-bold text-[#1f4e79]">
                    Unfinished attempt available
                  </p>
                  <p className="mt-1 text-sm text-slate-600">
                    {savedMockAttempt.answeredCount} of{" "}
                    {savedMockAttempt.totalQuestions} answered ·{" "}
                    {formatTime(savedMockAttempt.timeLeft)} remaining
                  </p>
                </div>
              )}

              <div className="mt-7 flex flex-col-reverse gap-3 sm:flex-row sm:flex-wrap sm:justify-end">
                <button
                  type="button"
                  onClick={() => setShowMockInstructions(false)}
                  className="rounded-md border border-slate-300 bg-white px-5 py-3 text-sm font-semibold text-slate-700 transition hover:bg-slate-100 sm:py-2.5"
                >
                  Cancel
                </button>

                {savedMockAttempt && onContinueMock && (
                  <button
                    type="button"
                    onClick={continueMockExam}
                    className="rounded-md border border-[#1f4e79] bg-white px-5 py-3 text-sm font-semibold text-[#1f4e79] transition hover:bg-blue-50 sm:py-2.5"
                  >
                    Continue last attempt
                  </button>
                )}

                <button
                  type="button"
                  onClick={beginMockExam}
                  className="rounded-md bg-[#1f4e79] px-5 py-3 text-sm font-semibold text-white transition hover:bg-[#183d60] sm:py-2.5"
                >
                  {savedMockAttempt ? "Start new exam" : "Start mock exam"}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </main>
  )
}
