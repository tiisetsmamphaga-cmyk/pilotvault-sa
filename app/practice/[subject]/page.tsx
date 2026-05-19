"use client"

import { useState } from "react"
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

  const currentQuestion = filteredQuestions[currentQuestionIndex]
  const selectedAnswer = answers[currentQuestionIndex]

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

  const handleAnswer = (option: string) => {
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

  const goPrevious = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex((prev) => prev - 1)
    }
  }

  const goNext = () => {
    if (currentQuestionIndex < filteredQuestions.length - 1) {
      setCurrentQuestionIndex((prev) => prev + 1)
    }
  }

  return (
    <main className="min-h-screen bg-white text-slate-900">
      <header className="h-16 border-b border-slate-300 bg-[#1f4e79] px-6 text-white flex items-center justify-between">
        <div>
          <h1 className="text-base font-bold">PilotVault SA Exam Practice</h1>
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

      <div className="flex min-h-[calc(100vh-64px)]">
        <aside className="hidden w-64 border-r border-slate-300 bg-slate-100 p-4 md:block">
          <h2 className="mb-4 font-semibold text-slate-700">Questions</h2>

          <div className="grid grid-cols-5 gap-2">
            {filteredQuestions.map((_, index) => {
              const isActive = index === currentQuestionIndex
              const isAnswered = Boolean(answers[index])
              const isPinned = pinnedQuestions.includes(index)

              return (
                <button
                  key={index}
                  onClick={() => setCurrentQuestionIndex(index)}
                  className={`relative h-10 rounded border text-sm font-medium ${
                    isActive
                      ? "border-[#1f4e79] bg-[#1f4e79] text-white"
                      : isAnswered
                        ? "border-blue-300 bg-blue-100 text-blue-900"
                        : "border-slate-300 bg-white text-slate-700"
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
            <p>⚑: pinned</p>
          </div>
        </aside>

        <section className="flex-1 p-6 md:p-10">
          <div className="mx-auto max-w-4xl">
            <div className="mb-8 flex items-center justify-between gap-4">
              <div>
                <p className="text-sm text-slate-500">
                  Question {currentQuestionIndex + 1} of{" "}
                  {filteredQuestions.length}
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

            <div className="mt-12 flex items-center justify-end gap-3">
              <button
                onClick={goPrevious}
                disabled={currentQuestionIndex === 0}
                className="rounded-md border border-slate-300 bg-white px-5 py-2 text-sm font-medium text-slate-700 disabled:opacity-40"
              >
                Previous
              </button>

              <button
                onClick={goNext}
                disabled={currentQuestionIndex === filteredQuestions.length - 1}
                className="rounded-md bg-[#1f4e79] px-6 py-2 text-sm font-semibold text-white hover:bg-[#183d60] disabled:opacity-40"
              >
                Next
              </button>
            </div>
          </div>
        </section>
      </div>
    </main>
  )
}