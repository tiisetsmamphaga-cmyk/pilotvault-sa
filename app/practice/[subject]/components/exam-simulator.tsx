"use client"

import { formatSubjectName, formatTime } from "../practice-utils"
import type { ExamAnswers, ExamMode, Question } from "../types"

type ExamSimulatorProps = {
  subject: string
  examLabel: string
  examMode: ExamMode
  timeLeft: number
  currentQuestion: Question
  currentQuestionIndex: number
  examQuestions: Question[]
  answers: ExamAnswers
  pinnedQuestions: number[]
  shownAnswers: number[]
  showMobileQuestionNav: boolean
  showFinishPrompt: boolean
  onExit: () => void
  onSelectQuestion: (index: number) => void
  onOpenMobileQuestionNav: () => void
  onCloseMobileQuestionNav: () => void
  onTogglePin: (index: number) => void
  onAnswer: (option: string) => void
  onToggleAnswer: () => void
  onPrevious: () => void
  onNext: () => void
  onOpenFinishPrompt: () => void
  onCloseFinishPrompt: () => void
  onSubmit: () => void
}

function getQuestionButtonClass({
  isActive,
  hasShownAnswer,
  isAnswered,
}: {
  isActive: boolean
  hasShownAnswer: boolean
  isAnswered: boolean
}) {
  if (isActive) {
    return "border-[#1f4e79] bg-[#1f4e79] text-white"
  }

  if (hasShownAnswer) {
    return "border-yellow-400 bg-yellow-100 text-yellow-900"
  }

  if (isAnswered) {
    return "border-blue-300 bg-blue-100 text-blue-900"
  }

  return "border-red-300 bg-red-50 text-red-700"
}

export function ExamSimulator({
  subject,
  examLabel,
  examMode,
  timeLeft,
  currentQuestion,
  currentQuestionIndex,
  examQuestions,
  answers,
  pinnedQuestions,
  shownAnswers,
  showMobileQuestionNav,
  showFinishPrompt,
  onExit,
  onSelectQuestion,
  onOpenMobileQuestionNav,
  onCloseMobileQuestionNav,
  onTogglePin,
  onAnswer,
  onToggleAnswer,
  onPrevious,
  onNext,
  onOpenFinishPrompt,
  onCloseFinishPrompt,
  onSubmit,
}: ExamSimulatorProps) {
  const selectedAnswer = answers[currentQuestionIndex]
  const totalQuestions = examQuestions.length
  const answeredCount = Object.keys(answers).length
  const unansweredCount = totalQuestions - answeredCount
  const answerIsShown = shownAnswers.includes(currentQuestionIndex)
  const questionIsPinned = pinnedQuestions.includes(currentQuestionIndex)

  return (
    <main className="min-h-screen bg-white text-slate-900">
      <header className="flex min-h-20 flex-col gap-4 border-b border-slate-300 bg-[#1f4e79] px-4 py-4 text-white sm:flex-row sm:items-center sm:justify-between sm:px-6">
        <div>
          <h1 className="text-base font-bold">PilotVault SA Exam Practice</h1>
          <p className="text-xs uppercase tracking-wider text-blue-100">
            {formatSubjectName(subject)} · {examLabel}
          </p>
        </div>

        <div className="flex items-center gap-3">
          <div className="rounded-md border border-white/20 bg-black/20 px-4 py-2 text-right">
            {examMode === "mock" ? (
              <>
                <p className="text-xs text-blue-100">Time Remaining</p>
                <p
                  className={`font-bold ${
                    timeLeft < 300 ? "text-red-300" : "text-white"
                  }`}
                >
                  {formatTime(timeLeft)}
                </p>
              </>
            ) : (
              <>
                <p className="text-xs text-blue-100">Practice Mode</p>
                <p className="font-bold text-white">Untimed</p>
              </>
            )}
          </div>

          <button
            onClick={onExit}
            className="rounded-md bg-white/10 px-4 py-2 text-sm hover:bg-white/20"
          >
            Exit
          </button>
        </div>
      </header>

      <div className="flex min-h-[calc(100vh-80px)]">
        <aside className="hidden w-64 border-r border-slate-300 bg-slate-100 p-4 md:block">
          <h2 className="mb-4 font-semibold text-slate-700">Questions</h2>

          <div className="grid grid-cols-5 gap-2">
            {examQuestions.map((_, index) => {
              const isActive = index === currentQuestionIndex
              const isAnswered = Boolean(answers[index])
              const isPinned = pinnedQuestions.includes(index)
              const hasShownAnswer = shownAnswers.includes(index)

              return (
                <button
                  key={index}
                  onClick={() => onSelectQuestion(index)}
                  className={`relative h-10 rounded border text-sm font-medium ${getQuestionButtonClass(
                    { isActive, hasShownAnswer, isAnswered }
                  )}`}
                >
                  {index + 1}
                  {isPinned && (
                    <span className="absolute -right-1 -top-2 text-yellow-600">
                      ⚑
                    </span>
                  )}
                </button>
              )
            })}
          </div>

          <div className="mt-6 space-y-2 text-xs text-slate-600">
            <p>Blue: current question</p>
            <p>Light blue: answered</p>
            <p>Red: not answered</p>
            <p>Yellow: answer viewed</p>
            <p>⚑: pinned</p>
          </div>
        </aside>

        <section className="flex-1 p-4 sm:p-6 md:p-10">
          <div className="mx-auto max-w-4xl">
            <div className="mb-8 flex items-center justify-between gap-4">
              <div>
                <p className="text-sm text-slate-500">
                  Question {currentQuestionIndex + 1} of {totalQuestions}
                </p>
                <h2 className="mt-1 text-xl font-semibold text-slate-800">
                  Exam Question
                </h2>
              </div>

              <div className="flex items-center gap-2">
                <button
                  onClick={onOpenMobileQuestionNav}
                  className="rounded-md border border-slate-300 bg-white px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-100 md:hidden"
                >
                  Questions
                </button>

                <button
                  onClick={() => onTogglePin(currentQuestionIndex)}
                  className={`rounded-md border px-4 py-2 text-sm font-medium ${
                    questionIsPinned
                      ? "border-yellow-500 bg-yellow-100 text-yellow-800"
                      : "border-slate-300 bg-white text-slate-700 hover:bg-slate-100"
                  }`}
                >
                  {questionIsPinned ? "Pinned" : "Pin"}
                </button>
              </div>
            </div>

            <div>
              <p className="text-lg leading-relaxed text-slate-900">
                {currentQuestion.question}
              </p>

              {currentQuestion.image_url && (
                <img
                  src={currentQuestion.image_url}
                  alt="Question reference"
                  className="mt-6 w-full max-w-2xl rounded-lg border border-slate-300"
                />
              )}
            </div>

            <div className="mt-8 space-y-2">
              {currentQuestion.options.map((option, index) => {
                const letter = String.fromCharCode(65 + index)

                return (
                  <label
                    key={`${currentQuestion.id}-${index}`}
                    className="flex cursor-pointer items-center gap-4 py-3"
                  >
                    <input
                      type="radio"
                      name={`question-${currentQuestion.id}`}
                      checked={selectedAnswer === option}
                      onChange={() => onAnswer(option)}
                      className="h-5 w-5 accent-[#1f4e79]"
                    />
                    <span className="font-semibold">{letter}.</span>
                    <span>{option}</span>
                  </label>
                )
              })}
            </div>

            {answerIsShown && (
              <div className="mt-8 border-l-4 border-[#1f4e79] bg-slate-50 p-5">
                <p className="text-sm font-semibold text-[#1f4e79]">
                  Correct Answer
                </p>
                <p className="mt-2 font-semibold text-slate-900">
                  {currentQuestion.correctAnswer}
                </p>
                <p className="mt-4 text-sm font-semibold text-[#1f4e79]">
                  Explanation
                </p>
                <p className="mt-2 whitespace-pre-line leading-relaxed text-slate-700">
                  {currentQuestion.explanation}
                </p>
                {currentQuestion.explanation_image_url && (
                  <figure className="mt-5 border border-slate-200 bg-white p-2">
                    <img
                      src={currentQuestion.explanation_image_url}
                      alt={`Explanation diagram for ${currentQuestion.topic ?? formatSubjectName(subject)}`}
                      loading="lazy"
                      decoding="async"
                      className="max-h-[32rem] w-full object-contain"
                    />
                  </figure>
                )}
              </div>
            )}

            <div className="mt-12 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
              <button
                onClick={onToggleAnswer}
                className="rounded-md border border-[#1f4e79] bg-white px-5 py-3 text-sm font-semibold text-[#1f4e79] hover:bg-blue-50 sm:py-2"
              >
                {answerIsShown ? "Hide Answer" : "Show Answer"}
              </button>

              <div className="grid grid-cols-3 gap-3 sm:flex">
                <button
                  onClick={onPrevious}
                  disabled={currentQuestionIndex === 0}
                  className="rounded-md border border-slate-300 bg-white px-4 py-3 text-sm font-medium text-slate-700 disabled:opacity-40 sm:px-5 sm:py-2"
                >
                  Previous
                </button>

                <button
                  onClick={onNext}
                  disabled={currentQuestionIndex === totalQuestions - 1}
                  className="rounded-md bg-[#1f4e79] px-4 py-3 text-sm font-semibold text-white hover:bg-[#183d60] disabled:opacity-40 sm:px-6 sm:py-2"
                >
                  Next
                </button>

                <button
                  onClick={onOpenFinishPrompt}
                  className="rounded-md bg-slate-900 px-4 py-3 text-sm font-semibold text-white hover:bg-slate-700 sm:px-6 sm:py-2"
                >
                  Finish
                </button>
              </div>
            </div>
          </div>
        </section>
      </div>

      {showMobileQuestionNav && (
        <div className="fixed inset-0 z-50 bg-black/50 md:hidden">
          <div className="absolute bottom-0 left-0 right-0 max-h-[75vh] overflow-y-auto rounded-t-2xl bg-white p-5 text-slate-900 shadow-2xl">
            <div className="mx-auto mb-5 h-1.5 w-16 rounded-full bg-slate-300" />

            <div className="mb-4 flex items-center justify-between">
              <div>
                <h2 className="text-xl font-bold">Questions</h2>
                <p className="mt-1 text-sm text-slate-500">
                  {answeredCount} answered / {totalQuestions}
                </p>
              </div>

              <button
                onClick={onCloseMobileQuestionNav}
                className="rounded-md border border-slate-300 px-4 py-2 text-sm font-semibold text-slate-700"
              >
                Close
              </button>
            </div>

            <div className="grid grid-cols-5 gap-2">
              {examQuestions.map((_, index) => {
                const isActive = index === currentQuestionIndex
                const isAnswered = Boolean(answers[index])
                const isPinned = pinnedQuestions.includes(index)
                const hasShownAnswer = shownAnswers.includes(index)

                return (
                  <button
                    key={index}
                    onClick={() => {
                      onSelectQuestion(index)
                      onCloseMobileQuestionNav()
                    }}
                    className={`relative h-11 rounded border text-sm font-medium ${getQuestionButtonClass(
                      { isActive, hasShownAnswer, isAnswered }
                    )}`}
                  >
                    {index + 1}
                    {isPinned && (
                      <span className="absolute -right-1 -top-2 text-yellow-600">
                        ⚑
                      </span>
                    )}
                  </button>
                )
              })}
            </div>
          </div>
        </div>
      )}

      {showFinishPrompt && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 px-4 sm:px-6">
          <div className="w-full max-w-md rounded-md bg-white p-6 shadow-xl">
            <h2 className="text-xl font-bold text-slate-900">
              Finish Examination
            </h2>

            <p className="mt-4 text-slate-700">
              You are about to submit your examination. Once submitted, your
              answers cannot be changed.
            </p>

            {unansweredCount > 0 && (
              <p className="mt-4 font-semibold text-red-700">
                You have {unansweredCount} unanswered question
                {unansweredCount === 1 ? "" : "s"}.
              </p>
            )}

            <div className="mt-6 flex flex-col gap-3 sm:flex-row sm:justify-end">
              <button
                onClick={onCloseFinishPrompt}
                className="rounded-md border border-slate-300 bg-white px-5 py-3 text-sm font-semibold text-slate-700 hover:bg-slate-100 sm:py-2"
              >
                Return to Exam
              </button>

              <button
                onClick={onSubmit}
                className="rounded-md bg-[#1f4e79] px-5 py-3 text-sm font-semibold text-white hover:bg-[#183d60] sm:py-2"
              >
                Submit Examination
              </button>
            </div>
          </div>
        </div>
      )}
    </main>
  )
}
