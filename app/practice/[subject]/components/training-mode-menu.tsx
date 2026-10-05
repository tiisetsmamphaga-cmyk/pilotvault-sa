"use client"

import { useEffect, useRef, useState, type ReactNode } from "react"
import Link from "next/link"
import { ArrowLeft, ArrowRight, BookOpen, Download, X } from "lucide-react"

import {
  MOCK_QUESTION_COUNT,
  MOCK_QUESTION_COUNT_OPTIONS,
  PASS_MARK,
  formatSubjectName,
  formatTime,
  getMockTimeLimitSeconds,
  getReadinessStatus,
} from "../practice-utils"
import type { MockSettings } from "../types"

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
    // null for an untimed exam.
    timeLeft: number | null
  } | null
  mockSettings: MockSettings
  onStartMock: (settings: MockSettings) => void
  onContinueMock?: () => void
  onOpenTopics: () => void
}

export function TrainingModeMenu({
  subject,
  questionCount,
  isTrialAccount,
  canAccessTopics,
  mockAverageScore,
  mockAttemptCount,
  savedMockAttempt = null,
  mockSettings,
  onStartMock,
  onContinueMock,
  onOpenTopics,
}: TrainingModeMenuProps) {
  const manual = SUBJECT_MANUALS[subject]
  const subjectName = formatSubjectName(subject)
  const readinessStatus = getReadinessStatus(mockAverageScore)
  const averageProgress = mockAverageScore ?? 0
  const progressCircumference = 239
  const progressOffset =
    progressCircumference * (1 - averageProgress / 100)
  const [showMockInstructions, setShowMockInstructions] = useState(false)
  const [draftSettings, setDraftSettings] = useState<MockSettings>(mockSettings)

  // Trial accounts always sit the fixed 25-question trial set.
  const countOptions = isTrialAccount
    ? [Math.min(MOCK_QUESTION_COUNT, questionCount)]
    : (() => {
        const available = MOCK_QUESTION_COUNT_OPTIONS.filter(
          (count) => count <= questionCount
        )
        return available.length ? available : [questionCount]
      })()
  const selectedCount = countOptions.includes(draftSettings.questionCount)
    ? draftSettings.questionCount
    : countOptions.includes(MOCK_QUESTION_COUNT)
      ? MOCK_QUESTION_COUNT
      : countOptions[countOptions.length - 1]
  const timedMinutes = Math.ceil(getMockTimeLimitSeconds(selectedCount) / 60)

  const openMockInstructions = () => {
    setDraftSettings(mockSettings)
    setShowMockInstructions(true)
  }

  const beginMockExam = () => {
    setShowMockInstructions(false)
    onStartMock({ ...draftSettings, questionCount: selectedCount })
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
        <div className="mx-auto flex h-16 max-w-7xl items-center justify-between gap-3 px-4 sm:h-20 sm:px-6 lg:px-8">
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
          <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
            <div>
              <h2 className="text-2xl font-bold tracking-tight sm:text-3xl">
                Choose a training mode
              </h2>
              <p className="mt-2 text-sm leading-6 text-[#b8c7d9] sm:text-base">
                Pick an option and start practising.
              </p>
            </div>

            {isTrialAccount && (
              <div className="sm:max-w-xs sm:text-right">
                <p className="text-[10px] font-bold uppercase tracking-[0.2em] text-[#b8860a]">
                  Trial conditions
                </p>
                <p className="mt-1.5 text-sm leading-6 text-[#b8c7d9]">
                  A fixed 25-question mock exam per subject. Upgrade to unlock
                  topic-based practice and the full question bank.
                </p>
              </div>
            )}
          </div>

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
                className="inline-flex h-10 shrink-0 items-center justify-center gap-2 rounded-xl bg-[#f4b400] px-4 text-sm font-bold text-[#06111f] transition hover:opacity-90 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#f4b400]/70"
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
            onClick={openMockInstructions}
            className="group relative flex min-h-[210px] cursor-pointer flex-col rounded-2xl border border-[#29476d] bg-[#0b1d31] p-5 text-left shadow-[0_14px_40px_rgba(0,0,0,0.12)] transition-all hover:-translate-y-1 hover:border-[#f4b400] hover:bg-[#0d2238] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#f4b400]/70 sm:p-6"
          >
            {isTrialAccount && (
              <span className="text-[10px] font-bold uppercase tracking-[0.1em] text-[#b8860a]">
                Trial
              </span>
            )}

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
              <span className="inline-flex items-center gap-2 rounded-xl bg-[var(--pv-navy)] px-3 py-2 text-xs font-bold text-[#ffffff] transition group-hover:bg-[var(--pv-navy-soft)]">
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
              <h3 className="text-xl font-bold text-white sm:text-2xl">
                Practice by topic
              </h3>
              <p className="mt-2 text-sm leading-6 text-[#b8c7d9]">
                Focus on one subject area at a time.
              </p>

              <div className="mt-auto flex justify-end pt-5">
                <span className="inline-flex items-center gap-2 rounded-xl bg-[var(--pv-navy)] px-3 py-2 text-xs font-bold text-[#ffffff] transition group-hover:bg-[var(--pv-navy-soft)]">
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
              <span className="text-[10px] font-bold uppercase tracking-[0.1em] text-[#b8860a]">
                Locked
              </span>

              <h3 className="mt-5 text-xl font-bold text-white sm:text-2xl">
                Practice by topic
              </h3>
              <p className="mt-2 text-sm leading-6 text-[#b8c7d9]">
                Unlock focused topic practice.
              </p>

              <div className="mt-auto flex justify-end pt-5">
                <span className="inline-flex items-center gap-2 rounded-xl bg-[var(--pv-navy)] px-3 py-2 text-xs font-bold text-[#ffffff] transition group-hover:bg-[var(--pv-navy-soft)]">
                  Unlock now
                  <ArrowRight className="h-3.5 w-3.5 transition-transform group-hover:translate-x-0.5" />
                </span>
              </div>
            </Link>
          )}
        </div>
      </section>

      {showMockInstructions && (
        <MockSetupDialog
          subjectName={subjectName}
          isTrialAccount={isTrialAccount}
          countOptions={countOptions}
          selectedCount={selectedCount}
          timedMinutes={timedMinutes}
          settings={draftSettings}
          savedMockAttempt={onContinueMock ? savedMockAttempt : null}
          onChange={setDraftSettings}
          onClose={() => setShowMockInstructions(false)}
          onStart={beginMockExam}
          onContinue={continueMockExam}
        />
      )}
    </main>
  )
}

type MockSetupDialogProps = {
  subjectName: string
  isTrialAccount: boolean
  countOptions: number[]
  selectedCount: number
  timedMinutes: number
  settings: MockSettings
  savedMockAttempt: TrainingModeMenuProps["savedMockAttempt"]
  onChange: (update: (settings: MockSettings) => MockSettings) => void
  onClose: () => void
  onStart: () => void
  onContinue: () => void
}

// The mock exam set-up sheet: a bottom sheet on phones, a centred dialog on
// larger screens. The Start button stays pinned at the bottom.
function MockSetupDialog({
  subjectName,
  isTrialAccount,
  countOptions,
  selectedCount,
  timedMinutes,
  settings,
  savedMockAttempt,
  onChange,
  onClose,
  onStart,
  onContinue,
}: MockSetupDialogProps) {
  const dialogRef = useRef<HTMLDivElement>(null)
  const onCloseRef = useRef(onClose)

  useEffect(() => {
    onCloseRef.current = onClose
  }, [onClose])

  useEffect(() => {
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") onCloseRef.current()
    }

    window.addEventListener("keydown", onKeyDown)
    dialogRef.current?.focus()

    return () => window.removeEventListener("keydown", onKeyDown)
  }, [])

  return (
    <div
      className="fixed inset-0 z-50 flex items-end justify-center bg-slate-950/60 backdrop-blur-[2px] sm:items-center sm:p-6"
      role="presentation"
      onClick={onClose}
    >
      <div
        ref={dialogRef}
        role="dialog"
        aria-modal="true"
        aria-labelledby="mock-exam-title"
        tabIndex={-1}
        onClick={(event) => event.stopPropagation()}
        className="flex max-h-[92dvh] w-full max-w-md flex-col overflow-hidden rounded-t-3xl bg-white text-slate-900 shadow-2xl outline-none sm:rounded-3xl"
      >
        <div className="flex items-start justify-between gap-4 border-b border-slate-100 px-5 pb-4 pt-5 sm:px-6">
          <div className="min-w-0">
            <p className="text-[11px] font-bold uppercase tracking-[0.16em] text-slate-500">
              {subjectName}
            </p>
            <h2
              id="mock-exam-title"
              className="mt-1 text-xl font-bold tracking-tight text-slate-950"
            >
              Mock exam
            </h2>
          </div>
          <button
            type="button"
            onClick={onClose}
            aria-label="Close"
            className="-mr-1 rounded-full p-2 text-slate-400 transition hover:bg-slate-100 hover:text-slate-700"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        <div className="flex-1 space-y-5 overflow-y-auto px-5 py-5 sm:px-6">
          {savedMockAttempt && (
            <div className="flex items-center gap-3 rounded-2xl border border-slate-200 bg-slate-50 p-3.5">
              <div className="min-w-0 flex-1">
                <p className="text-sm font-bold text-slate-900">
                  Unfinished attempt
                </p>
                <p className="text-xs text-slate-500">
                  {savedMockAttempt.answeredCount} of{" "}
                  {savedMockAttempt.totalQuestions} answered
                  {savedMockAttempt.timeLeft !== null &&
                    ` · ${formatTime(savedMockAttempt.timeLeft)} left`}
                </p>
              </div>
              <button
                type="button"
                onClick={onContinue}
                className="shrink-0 rounded-xl border border-slate-300 bg-white px-3.5 py-2 text-sm font-semibold text-slate-800 transition hover:border-slate-400"
              >
                Continue
              </button>
            </div>
          )}

          <SettingSection
            label="Questions"
            note={isTrialAccount ? "Fixed at 25 on the trial." : undefined}
          >
            <Segmented
              label="Number of questions"
              disabled={isTrialAccount}
              options={countOptions.map((count) => ({
                value: String(count),
                label: String(count),
              }))}
              value={String(selectedCount)}
              onChange={(value) =>
                onChange((current) => ({ ...current, questionCount: Number(value) }))
              }
            />
          </SettingSection>

          <SettingSection label="Timer">
            <Segmented
              label="Timer"
              options={[
                { value: "timed", label: `${timedMinutes} min` },
                { value: "untimed", label: "Untimed" },
              ]}
              value={settings.timed ? "timed" : "untimed"}
              onChange={(value) =>
                onChange((current) => ({ ...current, timed: value === "timed" }))
              }
            />
          </SettingSection>

          <SettingSection label="Show answers">
            <Segmented
              label="Show answers"
              options={[
                { value: "on", label: "On" },
                { value: "off", label: "Off" },
              ]}
              value={settings.showAnswerButton ? "on" : "off"}
              onChange={(value) =>
                onChange((current) => ({
                  ...current,
                  showAnswerButton: value === "on",
                }))
              }
            />
          </SettingSection>

          <p className="text-xs leading-5 text-slate-500">
            Pass mark {PASS_MARK}%. Unanswered questions count as wrong.
          </p>
        </div>

        <div className="border-t border-slate-100 px-5 pb-[max(1rem,env(safe-area-inset-bottom))] pt-4 sm:px-6 sm:pb-5">
          <button
            type="button"
            onClick={onStart}
            className="w-full rounded-2xl bg-[var(--pv-navy)] px-5 py-3.5 text-base font-bold text-white transition hover:bg-[var(--pv-navy-soft)] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-slate-400"
          >
            {savedMockAttempt ? "Start new exam" : "Start exam"}
          </button>
        </div>
      </div>
    </div>
  )
}

function SettingSection({
  label,
  note,
  children,
}: {
  label: string
  note?: string
  children: ReactNode
}) {
  return (
    <section>
      <h3 className="mb-2 text-sm font-bold text-slate-900">{label}</h3>
      {children}
      {note && <p className="mt-1.5 text-xs text-slate-500">{note}</p>}
    </section>
  )
}

function Segmented({
  label,
  options,
  value,
  disabled = false,
  onChange,
}: {
  label: string
  options: { value: string; label: string }[]
  value: string
  disabled?: boolean
  onChange: (value: string) => void
}) {
  return (
    <div
      role="radiogroup"
      aria-label={label}
      className="grid gap-1 rounded-2xl bg-slate-100 p-1"
      style={{ gridTemplateColumns: `repeat(${options.length}, minmax(0, 1fr))` }}
    >
      {options.map((option) => {
        const selected = option.value === value

        return (
          <button
            key={option.value}
            type="button"
            role="radio"
            aria-checked={selected}
            disabled={disabled}
            onClick={() => onChange(option.value)}
            className={`h-11 rounded-xl text-[15px] font-bold tabular-nums transition disabled:cursor-default ${
              selected
                ? "bg-white text-slate-950 shadow-[0_1px_3px_rgba(15,23,42,0.18)]"
                : "text-slate-500 hover:text-slate-900"
            }`}
          >
            {option.label}
          </button>
        )
      })}
    </div>
  )
}
