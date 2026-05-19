"use client"

import { useState } from "react"
import { useParams } from "next/navigation"
import Link from "next/link"

const questions = [
  {
    id: 1,
    subject: "meteorology",
    question: "What cloud type is most associated with thunderstorms?",
    options: ["Stratus", "Cumulonimbus", "Cirrus", "Altostratus"],
    correctAnswer: "Cumulonimbus",
    explanation:
      "Cumulonimbus clouds are associated with thunderstorms, heavy rain, turbulence, lightning, and strong vertical development.",
  },
  {
    id: 2,
    subject: "meteorology",
    question: "What does QNH allow the altimeter to read?",
    options: [
      "Height above the runway",
      "Flight level",
      "Altitude above mean sea level",
      "Density altitude",
    ],
    correctAnswer: "Altitude above mean sea level",
    explanation:
      "QNH is set so the altimeter reads altitude above mean sea level.",
  },
]

export default function SubjectPracticePage() {
  const params = useParams()
  const subject = String(params.subject)

  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0)
  const [selectedAnswer, setSelectedAnswer] = useState("")
  const [showExplanation, setShowExplanation] = useState(false)

  const filteredQuestions = questions.filter((q) => q.subject === subject)
  const currentQuestion = filteredQuestions[currentQuestionIndex]

  if (!currentQuestion) {
    return (
      <main className="min-h-screen bg-[#06111f] text-white flex items-center justify-center px-6">
        <div className="text-center">
          <h1 className="text-2xl font-bold">No questions found.</h1>
          <Link
            href="/practice"
            className="mt-6 inline-block text-[#f4b400] hover:text-white"
          >
            ← Back to Practice
          </Link>
        </div>
      </main>
    )
  }

  const handleAnswer = (option: string) => {
    setSelectedAnswer(option)
    setShowExplanation(true)
  }

  const nextQuestion = () => {
    setSelectedAnswer("")
    setShowExplanation(false)
    setCurrentQuestionIndex((prev) => prev + 1)
  }

  return (
    <main className="min-h-screen bg-[#06111f] text-white px-6 py-10">
      <div className="max-w-4xl mx-auto">
        <Link
          href="/practice"
          className="inline-block mb-8 text-sm text-[#f4b400] hover:text-white transition"
        >
          ← Back to Practice
        </Link>

        <p className="text-[#f4b400] text-xs uppercase tracking-[0.18em]">
          Practice Session
        </p>

        <h1 className="mt-3 text-4xl font-bold capitalize">
          {subject.replaceAll("-", " ")}
        </h1>

        <div className="mt-8 rounded-2xl border border-[#1e3a5f] bg-[#081726] p-6">
          <p className="mb-6 text-sm text-gray-400">
            Question {currentQuestionIndex + 1} of {filteredQuestions.length}
          </p>

          <h2 className="text-2xl font-semibold leading-relaxed">
            {currentQuestion.question}
          </h2>

          <div className="mt-8 space-y-4">
            {currentQuestion.options.map((option) => {
              const isCorrect = option === currentQuestion.correctAnswer
              const isSelected = option === selectedAnswer

              return (
                <button
                  key={option}
                  onClick={() => handleAnswer(option)}
                  disabled={showExplanation}
                  className={`w-full rounded-xl border p-4 text-left transition ${
                    showExplanation
                      ? isCorrect
                        ? "border-green-500 bg-green-500/10"
                        : isSelected
                          ? "border-red-500 bg-red-500/10"
                          : "border-[#1e3a5f] bg-[#0b1f35]"
                      : "border-[#1e3a5f] bg-[#0b1f35] hover:border-[#f4b400]"
                  }`}
                >
                  {option}
                </button>
              )
            })}
          </div>

          {showExplanation && (
            <div className="mt-8 rounded-xl border border-[#1e3a5f] bg-[#0b1f35] p-5">
              <p className="text-sm font-semibold text-[#f4b400]">
                Explanation
              </p>

              <p className="mt-3 text-gray-300 leading-relaxed">
                {currentQuestion.explanation}
              </p>

              {currentQuestionIndex < filteredQuestions.length - 1 && (
                <button
                  onClick={nextQuestion}
                  className="mt-6 rounded-xl bg-[#f4b400] px-6 py-3 font-bold text-[#06111f] hover:bg-[#d9a000] transition"
                >
                  Next Question
                </button>
              )}
            </div>
          )}
        </div>
      </div>
    </main>
  )
}