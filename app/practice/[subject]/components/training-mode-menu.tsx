"use client"

import Link from "next/link"
import {
  ArrowLeft,
  ArrowRight,
  BookOpen,
  ClipboardList,
  Download,
  GraduationCap,
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

  return (
    <main className="min-h-screen bg-[#06111f] bg-[radial-gradient(circle_at_top,_rgba(30,58,95,0.28),_transparent_42%)] px-4 py-6 text-white sm:px-6 sm:py-10">
      <div className="mx-auto max-w-5xl">
        <Link
          href="/dashboard"
          className="group inline-flex items-center gap-2 rounded-full border border-[#1e3a5f] bg-[#081726]/80 px-3.5 py-2 text-sm font-medium text-gray-300 transition hover:border-[#f4b400]/60 hover:text-[#f4b400] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#f4b400]/70"
        >
          <ArrowLeft className="h-4 w-4 transition-transform group-hover:-translate-x-0.5" />
          Dashboard
        </Link>

        <section className="mt-5 overflow-hidden rounded-[28px] border border-[#1e3a5f] bg-gradient-to-br from-[#081726] to-[#06111f] shadow-[0_24px_80px_rgba(0,0,0,0.24)]">
          <div className="p-6 sm:p-8">
            <div className="flex flex-wrap items-center justify-between gap-3">
              <p className="text-xs font-bold uppercase tracking-[0.25em] text-[#f4b400]">
                {formatSubjectName(subject)}
              </p>

              <span className="inline-flex items-center gap-2 rounded-full border border-[#1e3a5f] bg-[#06111f]/70 px-3 py-1.5 text-xs font-semibold text-gray-300">
                <span className="h-1.5 w-1.5 rounded-full bg-[#f4b400]" />
                {isTrialAccount
                  ? `${mockQuestionCount} trial questions`
                  : `${questionCount} questions`}
              </span>
            </div>

            <h1 className="mt-4 max-w-3xl text-3xl font-bold tracking-tight sm:text-4xl">
              Choose how you want to train
            </h1>

            <p className="mt-3 max-w-2xl text-sm leading-6 text-gray-400 sm:text-base">
              Simulate the SACAA exam or work through a specific topic at your
              own pace.
            </p>
          </div>

          {manual && (
            <div className="grid gap-4 border-t border-[#1e3a5f] bg-[#06111f]/45 px-6 py-5 sm:grid-cols-[1fr_auto] sm:items-center sm:px-8">
              <div className="flex min-w-0 items-center gap-4">
                <span className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl border border-[#f4b400]/25 bg-[#f4b400]/10 text-[#f4b400]">
                  <BookOpen className="h-5 w-5" />
                </span>

                <div className="min-w-0">
                  <p className="text-[10px] font-bold uppercase tracking-[0.22em] text-[#f4b400]">
                    Included study resource
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
                className="inline-flex h-11 shrink-0 items-center justify-center gap-2 rounded-xl border border-[#f4b400]/35 bg-[#f4b400]/10 px-4 text-sm font-semibold text-[#f4b400] transition hover:border-[#f4b400] hover:bg-[#f4b400] hover:text-[#06111f] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#f4b400]/70"
              >
                <Download className="h-4 w-4" />
                Download manual
              </a>
            </div>
          )}
        </section>

        <div className="mt-6 grid gap-5 md:grid-cols-2">
          <button
            type="button"
            onClick={onStartMock}
            className="group flex min-h-[270px] cursor-pointer flex-col rounded-[26px] border border-[#1e3a5f] bg-[#081726] p-6 text-left shadow-[0_18px_50px_rgba(0,0,0,0.2)] transition duration-300 hover:-translate-y-1 hover:border-[#f4b400]/70 hover:shadow-[0_22px_60px_rgba(244,180,0,0.08)] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#f4b400]/70"
          >
            <div className="flex items-start justify-between gap-4">
              <span className="flex h-12 w-12 items-center justify-center rounded-2xl border border-[#f4b400]/25 bg-[#f4b400]/10 text-[#f4b400]">
                <ClipboardList className="h-6 w-6" />
              </span>

              <span className="inline-flex items-center gap-1.5 rounded-full border border-[#1e3a5f] bg-[#06111f]/70 px-3 py-1.5 text-[10px] font-bold uppercase tracking-[0.16em] text-gray-300">
                <GraduationCap className="h-3.5 w-3.5 text-[#f4b400]" />
                {isTrialAccount ? "Trial access" : "Full access"}
              </span>
            </div>

            <h2 className="mt-7 text-2xl font-bold tracking-tight text-white">
              Mock exam
            </h2>
            <p className="mt-2 max-w-md text-sm leading-6 text-gray-400">
              {isTrialAccount
                ? "Complete a fixed set of SACAA-style questions in an exam-focused session."
                : "Complete a randomized set of SACAA-style questions from the full question bank."}
            </p>

            <div className="mt-auto flex items-end justify-between gap-4 border-t border-[#1e3a5f]/80 pt-5">
              <div>
                <p className="text-2xl font-bold text-white">
                  {mockQuestionCount}
                </p>
                <p className="mt-0.5 text-[10px] font-semibold uppercase tracking-[0.18em] text-gray-500">
                  Questions
                </p>
              </div>

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
              className="group flex min-h-[270px] cursor-pointer flex-col rounded-[26px] border border-[#1e3a5f] bg-[#081726] p-6 text-left shadow-[0_18px_50px_rgba(0,0,0,0.2)] transition duration-300 hover:-translate-y-1 hover:border-[#f4b400]/70 hover:shadow-[0_22px_60px_rgba(244,180,0,0.08)] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#f4b400]/70"
            >
              <div className="flex items-start justify-between gap-4">
                <span className="flex h-12 w-12 items-center justify-center rounded-2xl border border-[#7aa2ff]/25 bg-[#7aa2ff]/10 text-[#9bb7ff]">
                  <BookOpen className="h-6 w-6" />
                </span>

                <span className="inline-flex items-center gap-1.5 rounded-full border border-[#1e3a5f] bg-[#06111f]/70 px-3 py-1.5 text-[10px] font-bold uppercase tracking-[0.16em] text-gray-300">
                  <GraduationCap className="h-3.5 w-3.5 text-[#f4b400]" />
                  Full access
                </span>
              </div>

              <h2 className="mt-7 text-2xl font-bold tracking-tight text-white">
                Practice by topic
              </h2>
              <p className="mt-2 max-w-md text-sm leading-6 text-gray-400">
                Target a weak area and work through every available question
                from that topic with no question cap.
              </p>

              <div className="mt-auto flex items-end justify-between gap-4 border-t border-[#1e3a5f]/80 pt-5">
                <div>
                  <p className="text-lg font-bold text-white">No limit</p>
                  <p className="mt-0.5 text-[10px] font-semibold uppercase tracking-[0.18em] text-gray-500">
                    Topic practice
                  </p>
                </div>

                <span className="inline-flex items-center gap-2 text-sm font-bold text-[#f4b400]">
                  Choose topic
                  <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-1" />
                </span>
              </div>
            </button>
          ) : (
            <Link
              href={`/upgrade?subject=${subject}`}
              className="group flex min-h-[270px] flex-col rounded-[26px] border border-[#1e3a5f] bg-[#081726]/70 p-6 text-left shadow-[0_18px_50px_rgba(0,0,0,0.16)] transition duration-300 hover:-translate-y-1 hover:border-[#f4b400]/60 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#f4b400]/70"
            >
              <div className="flex items-start justify-between gap-4">
                <span className="flex h-12 w-12 items-center justify-center rounded-2xl border border-[#1e3a5f] bg-[#06111f]/70 text-gray-400">
                  <LockKeyhole className="h-5 w-5" />
                </span>

                <span className="rounded-full border border-[#f4b400]/25 bg-[#f4b400]/10 px-3 py-1.5 text-[10px] font-bold uppercase tracking-[0.16em] text-[#f4b400]">
                  Upgrade required
                </span>
              </div>

              <h2 className="mt-7 text-2xl font-bold tracking-tight text-white">
                Practice by topic
              </h2>
              <p className="mt-2 max-w-md text-sm leading-6 text-gray-400">
                Target weak areas by topic using the full PilotVault question
                bank.
              </p>

              <div className="mt-auto flex items-center justify-end border-t border-[#1e3a5f]/80 pt-5">
                <span className="inline-flex items-center gap-2 text-sm font-bold text-[#f4b400]">
                  View access options
                  <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-1" />
                </span>
              </div>
            </Link>
          )}
        </div>
      </div>
    </main>
  )
}
