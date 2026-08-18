"use client"

import { formatSubjectName } from "../practice-utils"
import type { ExamAnswers, ExamMode, Question } from "../types"

import { ExplanationImage } from "./explanation-image"
import { HumanPerformanceVisual } from "./human-performance-visual"

type ExamResultsProps = {
  subject: string
  examLabel: string
  examMode: ExamMode
  scorePercentage: number
  passed: boolean
  correctAnswers: number
  totalQuestions: number
  wrongQuestions: Question[]
  examQuestions: Question[]
  answers: ExamAnswers
  onReturnToMenu: () => void
  onReturnToTopics: () => void
  onRestartMock: () => void
}

export function ExamResults({
  subject,
  examLabel,
  examMode,
  scorePercentage,
  passed,
  correctAnswers,
  totalQuestions,
  wrongQuestions,
  examQuestions,
  answers,
  onReturnToMenu,
  onReturnToTopics,
  onRestartMock,
}: ExamResultsProps) {
  const isHumanPerformance = subject === "human-performance"

  return (
    <main className="min-h-screen bg-white text-slate-900">
      <header className="flex min-h-16 items-center justify-between border-b border-slate-300 bg-[#1f4e79] px-4 py-4 text-white sm:px-6">
        <div>
          <h1 className="text-base font-bold">PilotVault SA Exam Results</h1>
          <p className="text-xs uppercase tracking-wider text-blue-100">
            {formatSubjectName(subject)} · {examLabel}
          </p>
        </div>

        <button onClick={onReturnToMenu} className="rounded-md bg-white/10 px-4 py-2 text-sm hover:bg-white/20">
          Exit
        </button>
      </header>

      <section className="mx-auto max-w-5xl px-4 py-8 sm:px-6 sm:py-10">
        <div className="rounded-md border border-slate-300 bg-slate-50 p-5 sm:p-6">
          <p className="text-sm uppercase tracking-wider text-slate-500">Final Score</p>
          <h2 className="mt-2 text-5xl font-bold text-slate-900">{scorePercentage}%</h2>
          <p className={`mt-3 text-lg font-semibold ${passed ? "text-green-700" : "text-red-700"}`}>
            {passed ? "Passed" : "Failed"}
          </p>
          <p className="mt-2 text-slate-600">You got {correctAnswers} out of {totalQuestions} questions correct.</p>

          <div className="mt-6 flex flex-col gap-3 sm:flex-row">
            <button
              onClick={examMode === "topic" ? onReturnToTopics : onRestartMock}
              className="rounded-md bg-[#1f4e79] px-5 py-3 text-sm font-semibold text-white hover:bg-[#183d60] sm:py-2"
            >
              {examMode === "topic" ? "Back to Topics" : "Restart"}
            </button>
            <button
              onClick={onReturnToMenu}
              className="rounded-md border border-slate-300 bg-white px-5 py-3 text-sm font-semibold text-slate-700 hover:bg-slate-100 sm:py-2"
            >
              Back to Practice Modes
            </button>
          </div>
        </div>

        <div className="mt-10">
          <h3 className="text-2xl font-bold text-slate-900">Review Incorrect Answers</h3>

          {wrongQuestions.length === 0 ? (
            <p className="mt-4 text-green-700">Excellent. You got every question correct.</p>
          ) : (
            <div className="mt-6 space-y-6">
              {wrongQuestions.map((question) => {
                const originalIndex = examQuestions.findIndex((item) => item.id === question.id)
                const usesApprovedBankVisual = isHumanPerformance && question.id === 2207

                return (
                  <div key={question.id} className="border-b border-slate-300 pb-6">
                    <p className="text-sm font-semibold text-slate-500">Question {originalIndex + 1}</p>
                    <h4 className="mt-2 text-lg font-semibold text-slate-900">{question.question}</h4>
                    <p className="mt-4 text-red-700">
                      Your answer: <span className="font-semibold">{answers[originalIndex] || "Not answered"}</span>
                    </p>
                    <p className="mt-2 text-green-700">
                      Correct answer: <span className="font-semibold">{question.correctAnswer}</span>
                    </p>
                    <p className="mt-3 whitespace-pre-line leading-relaxed text-slate-700">{question.explanation}</p>

                    {isHumanPerformance && !usesApprovedBankVisual ? (
                      <HumanPerformanceVisual question={question} />
                    ) : question.explanation_image_url ? (
                      <ExplanationImage
                        src={question.explanation_image_url}
                        alt={`Explanation diagram for ${question.topic ?? formatSubjectName(subject)}`}
                      />
                    ) : null}
                  </div>
                )
              })}
            </div>
          )}
        </div>
      </section>
    </main>
  )
}
