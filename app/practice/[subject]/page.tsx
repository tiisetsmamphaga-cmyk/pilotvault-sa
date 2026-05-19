"use client"

import { useEffect, useState } from "react"
import { useParams } from "next/navigation"
import Link from "next/link"
import { questions } from "@/src/data/questions"

export default function SubjectPracticePage() {
  const params = useParams()
  const subject = String(params.subject)

  const filteredQuestions = questions.filter((q) => q.subject === subject)

  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0)
  const [answers, setAnswers] = useState<Record<number, string>>({})
  const [pinnedQuestions, setPinnedQuestions] = useState<number[]>([])
  const [shownAnswers, setShownAnswers] = useState<number[]>([])
  const [isSubmitted, setIsSubmitted] = useState(false)
  const [showFinishPrompt, setShowFinishPrompt] = useState(false)
  const [timeLeft, setTimeLeft] = useState(1500)

  const currentQuestion = filteredQuestions[currentQuestionIndex]
  const selectedAnswer = answers[currentQuestionIndex]

  useEffect(() => {
    if (isSubmitted) return

    const timer = setInterval(() => {
      setTimeLeft((prev) => {
        if (prev <= 1) {
          clearInterval(timer)
          setIsSubmitted(true)
          return 0
        }

        return prev - 1
      })
    }, 1000)

    return () => clearInterval(timer)
  }, [isSubmitted])

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60

    return `${mins}:${secs.toString().padStart(2, "0")}`
  }

  if (!currentQuestion) {
    return (
      <main className="min-h-screen bg-white text-slate-900 flex items-center justify-center px-6">
        <div className="text-center">
          <h1 className="text-2xl font-bold">No questions found.</h1>

          <Link
            href="/practice"
            className="mt-6 inline-block rounded-md bg-[#1f4e79] px-5 py-2 text-white hover:bg-[#183d60]"
          >
            Back to Practice
          </Link>
        </div>
      </main>
    )
  }

  const totalQuestions = filteredQuestions.length
  const unansweredCount = totalQuestions - Object.keys(answers).length

  const correctAnswers = filteredQuestions.filter(
    (question, index) => answers[index] === question.correctAnswer
  ).length

  const scorePercentage = Math.round((correctAnswers / totalQuestions) * 100)
  const passed = scorePercentage >= 75

  const wrongQuestions = filteredQuestions.filter(
    (question, index) => answers[index] !== question.correctAnswer
  )

  const handleAnswer = (option: string) => {
    if (isSubmitted) return

    setAnswers((prev) => ({
      ...prev,
      [currentQuestionIndex]: option,
    }))
  }

  const togglePin = (index: number) => {
    setPinnedQuestions((prev) =>
      prev.includes(index)
        ? prev.filter((item) => item !== index)
        : [...prev, index]
    )
  }

  const toggleAnswer = () => {
    setShownAnswers((prev) =>
      prev.includes(currentQuestionIndex)
        ? prev.filter((item) => item !== currentQuestionIndex)
        : [...prev, currentQuestionIndex]
    )
  }

  const goPrevious = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex((prev) => prev - 1)
    }
  }

  const goNext = () => {
    if (currentQuestionIndex < totalQuestions - 1) {
      setCurrentQuestionIndex((prev) => prev + 1)
    }
  }

  const finishExam = () => {
    setShowFinishPrompt(true)
  }

  const confirmSubmit = () => {
    setShowFinishPrompt(false)
    setIsSubmitted(true)
  }

  const restartExam = () => {
    setCurrentQuestionIndex(0)
    setAnswers({})
    setPinnedQuestions([])
    setShownAnswers([])
    setIsSubmitted(false)
    setShowFinishPrompt(false)
    setTimeLeft(1500)
  }

  if (isSubmitted) {
    return (
      <main className="min-h-screen bg-white text-slate-900">
        <header className="h-16 border-b border-slate-300 bg-[#1f4e79] px-6 text-white flex items-center justify-between">
          <div>
            <h1 className="text-base font-bold">PilotVault SA Exam Results</h1>
            <p className="text-xs uppercase tracking-wider text-blue-100">
              {subject.replaceAll("-", " ")}
            </p>
          </div>

          <Link
            href="/practice"
            className="rounded-md bg-white/10 px-4 py-2 text-sm hover:bg-white/20"
          >
            Exit
          </Link>
        </header>

        <section className="mx-auto max-w-5xl px-6 py-10">
          <div className="rounded-md border border-slate-300 bg-slate-50 p-6">
            <p className="text-sm uppercase tracking-wider text-slate-500">
              Final Score
            </p>

            <h2 className="mt-2 text-5xl font-bold text-slate-900">
              {scorePercentage}%
            </h2>

            <p
              className={`mt-3 text-lg font-semibold ${
                passed ? "text-green-700" : "text-red-700"
              }`}
            >
              {passed ? "Passed" : "Failed"}
            </p>

            <p className="mt-2 text-slate-600">
              You got {correctAnswers} out of {totalQuestions} questions correct.
            </p>

            <div className="mt-6 flex gap-3">
              <button
                onClick={restartExam}
                className="rounded-md bg-[#1f4e79] px-5 py-2 text-sm font-semibold text-white hover:bg-[#183d60]"
              >
                Restart
              </button>

              <Link
                href="/practice"
                className="rounded-md border border-slate-300 bg-white px-5 py-2 text-sm font-semibold text-slate-700 hover:bg-slate-100"
              >
                Back to Practice
              </Link>
            </div>
          </div>

          <div className="mt-10">
            <h3 className="text-2xl font-bold text-slate-900">
              Review Incorrect Answers
            </h3>

            {wrongQuestions.length === 0 ? (
              <p className="mt-4 text-green-700">
                Excellent. You got every question correct.
              </p>
            ) : (
              <div className="mt-6 space-y-6">
                {wrongQuestions.map((question) => {
                  const originalIndex = filteredQuestions.findIndex(
                    (item) => item.id === question.id
                  )

                  return (
                    <div
                      key={question.id}
                      className="border-b border-slate-300 pb-6"
                    >
                      <p className="text-sm font-semibold text-slate-500">
                        Question {originalIndex + 1}
                      </p>

                      <h4 className="mt-2 text-lg font-semibold text-slate-900">
                        {question.question}
                      </h4>

                      <p className="mt-4 text-red-700">
                        Your answer:{" "}
                        <span className="font-semibold">
                          {answers[originalIndex] || "Not answered"}
                        </span>
                      </p>

                      <p className="mt-2 text-green-700">
                        Correct answer:{" "}
                        <span className="font-semibold">
                          {question.correctAnswer}
                        </span>
                      </p>

                      <p className="mt-3 text-slate-700 leading-relaxed">
                        {question.explanation}
                      </p>
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

  return (
    <main className="min-h-screen bg-white text-slate-900">
      <header className="h-20 border-b border-slate-300 bg-[#1f4e79] px-6 text-white flex items-center justify-between">
        <div>
          <h1 className="text-base font-bold">PilotVault SA Exam Practice</h1>

          <p className="text-xs uppercase tracking-wider text-blue-100">
            {subject.replaceAll("-", " ")}
          </p>
        </div>

        <div className="flex items-center gap-3">
          <div className="rounded-md border border-white/20 bg-black/20 px-4 py-2 text-right">
            <p className="text-xs text-blue-100">Time Remaining</p>

            <p
              className={`font-bold ${
                timeLeft < 300 ? "text-red-300" : "text-white"
              }`}
            >
              {formatTime(timeLeft)}
            </p>
          </div>

          <Link
            href="/practice"
            className="rounded-md bg-white/10 px-4 py-2 text-sm hover:bg-white/20"
          >
            Exit
          </Link>
        </div>
      </header>

      <div className="flex min-h-[calc(100vh-80px)]">
        <aside className="hidden w-64 border-r border-slate-300 bg-slate-100 p-4 md:block">
          <h2 className="mb-4 font-semibold text-slate-700">Questions</h2>

          <div className="grid grid-cols-5 gap-2">
            {filteredQuestions.map((_, index) => {
              const isActive = index === currentQuestionIndex
              const isAnswered = Boolean(answers[index])
              const isPinned = pinnedQuestions.includes(index)
              const hasShownAnswer = shownAnswers.includes(index)

              return (
                <button
                  key={index}
                  onClick={() => setCurrentQuestionIndex(index)}
                  className={`relative h-10 rounded border text-sm font-medium ${
                    isActive
                      ? "border-[#1f4e79] bg-[#1f4e79] text-white"
                      : hasShownAnswer
                        ? "border-yellow-400 bg-yellow-100 text-yellow-900"
                        : isAnswered
                          ? "border-blue-300 bg-blue-100 text-blue-900"
                          : "border-red-300 bg-red-50 text-red-700"
                  }`}
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

        <section className="flex-1 p-6 md:p-10">
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

              <button
                onClick={() => togglePin(currentQuestionIndex)}
                className={`rounded-md border px-4 py-2 text-sm font-medium ${
                  pinnedQuestions.includes(currentQuestionIndex)
                    ? "border-yellow-500 bg-yellow-100 text-yellow-800"
                    : "border-slate-300 bg-white text-slate-700 hover:bg-slate-100"
                }`}
              >
                {pinnedQuestions.includes(currentQuestionIndex)
                  ? "Pinned"
                  : "Pin"}
              </button>
            </div>

            <div className="py-2">
              <p className="text-lg leading-relaxed text-slate-900">
                {currentQuestion.question}
              </p>
            </div>

            <div className="mt-8 space-y-2">
              {currentQuestion.options.map((option, index) => {
                const letter = String.fromCharCode(65 + index)
                const isSelected = selectedAnswer === option

                return (
                  <label
                    key={option}
                    className="flex cursor-pointer items-center gap-4 py-3"
                  >
                    <input
                      type="radio"
                      name={`question-${currentQuestion.id}`}
                      checked={isSelected}
                      onChange={() => handleAnswer(option)}
                      className="h-5 w-5 accent-[#1f4e79]"
                    />

                    <span className="font-semibold text-slate-700">
                      {letter}.
                    </span>

                    <span className="text-slate-800">{option}</span>
                  </label>
                )
              })}
            </div>

            {shownAnswers.includes(currentQuestionIndex) && (
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

                <p className="mt-2 leading-relaxed text-slate-700">
                  {currentQuestion.explanation}
                </p>
              </div>
            )}

            <div className="mt-12 flex flex-wrap items-center justify-between gap-3">
              <button
                onClick={toggleAnswer}
                className="rounded-md border border-[#1f4e79] bg-white px-5 py-2 text-sm font-semibold text-[#1f4e79] hover:bg-blue-50"
              >
                {shownAnswers.includes(currentQuestionIndex)
                  ? "Hide Answer"
                  : "Show Answer"}
              </button>

              <div className="flex flex-wrap items-center gap-3">
                <button
                  onClick={goPrevious}
                  disabled={currentQuestionIndex === 0}
                  className="rounded-md border border-slate-300 bg-white px-5 py-2 text-sm font-medium text-slate-700 disabled:opacity-40"
                >
                  Previous
                </button>

                <button
                  onClick={goNext}
                  disabled={currentQuestionIndex === totalQuestions - 1}
                  className="rounded-md bg-[#1f4e79] px-6 py-2 text-sm font-semibold text-white hover:bg-[#183d60] disabled:opacity-40"
                >
                  Next
                </button>

                <button
                  onClick={finishExam}
                  className="rounded-md bg-slate-900 px-6 py-2 text-sm font-semibold text-white hover:bg-slate-700"
                >
                  Finish
                </button>
              </div>
            </div>
          </div>
        </section>
      </div>

      {showFinishPrompt && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 px-6">
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

            <p className="mt-4 text-slate-700">
              Are you sure you want to finish and submit your answers?
            </p>

            <div className="mt-6 flex justify-end gap-3">
              <button
                onClick={() => setShowFinishPrompt(false)}
                className="rounded-md border border-slate-300 bg-white px-5 py-2 text-sm font-semibold text-slate-700 hover:bg-slate-100"
              >
                Return to Exam
              </button>

              <button
                onClick={confirmSubmit}
                className="rounded-md bg-[#1f4e79] px-5 py-2 text-sm font-semibold text-white hover:bg-[#183d60]"
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