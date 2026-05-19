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
  const [correctCount, setCorrectCount] = useState(0)
  const [wrongCount, setWrongCount] = useState(0)
  const [isFinished, setIsFinished] = useState(false)

  const filteredQuestions = questions.filter((q) => q.subject === subject)
  const currentQuestion = filteredQuestions[currentQuestionIndex]

  const totalAnswered = correctCount + wrongCount
  const score =
    totalAnswered === 0 ? 0 : Math.round((correctCount / totalAnswered) * 100)

  if (!currentQuestion && !isFinished) {
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
    if (showExplanation) return

    setSelectedAnswer(option)
    setShowExplanation(true)

    if (option === currentQuestion.correctAnswer) {
      setCorrectCount((prev) => prev + 1)
    } else {
      setWrongCount((prev) => prev + 1)
    }
  }

  const nextQuestion = () => {
    if (currentQuestionIndex === filteredQuestions.length - 1) {
      setIsFinished(true)
      return
    }

    setSelectedAnswer("")
    setShowExplanation(false)
    setCurrentQuestionIndex((prev) => prev + 1)
  }

  const restartPractice = () => {
    setCurrentQuestionIndex(0)
    setSelectedAnswer("")
    setShowExplanation(false)
    setCorrectCount(0)
    setWrongCount(0)
    setIsFinished(false)
  }

  if (isFinished) {
    return (
      <main className="min-h-screen bg-[#06111f] text-white px-6 py-10">
        <div className="max-w-4xl mx-auto">
          <Link
            href="/practice"
            className="inline-block mb-8 text-sm text-[#f4b400] hover:text-white transition"
          >
            ← Back to Practice
          </Link>

          <div className="rounded-3xl border border-[#1e3a5f] bg-[#081726] p-8 text-center">
            <p className="text-[#f4b400] text-xs uppercase tracking-[0.18em]">
              Practice Complete
            </p>

            <h1 className="mt-4 text-4xl font-bold capitalize">
              {subject.replaceAll("-", " ")}
            </h1>

            <div className="mt-8 mx-auto h-32 w-32 rounded-full border-[10px] border-[#f4b400] flex items-center justify-center">
              <span className="text-3xl font-bold">{score}%</span>
            </div>

            <div className="mt-8 grid grid-cols-2 gap-4 max-w-md mx-auto">
              <div className="rounded-xl border border-[#1e3a5f] bg-[#0b1f35] p-4">
                <p className="text-xs text-gray-400">Correct</p>
                <h3 className="mt-2 text-2xl font-bold text-green-400">
                  {correctCount}
                </h3>
              </div>

              <div className="rounded-xl border border-[#1e3a5f] bg-[#0b1f35] p-4">
                <p className="text-xs text-gray-400">Wrong</p>
                <h3 className="mt-2 text-2xl font-bold text-red-400">
                  {wrongCount}
                </h3>
              </div>
            </div>

            <div className="mt-8 flex flex-col sm:flex-row gap-3 justify-center">
              <button
                onClick={restartPractice}
                className="rounded-xl bg-[#f4b400] px-6 py-3 font-bold text-[#06111f] hover:bg-[#d9a000] transition"
              >
                Retry Practice
              </button>

              <Link
                href="/practice"
                className="rounded-xl border border-[#1e3a5f] bg-[#0b1f35] px-6 py-3 font-bold text-white hover:border-[#f4b400] transition"
              >
                Choose Another Subject
              </Link>
            </div>
          </div>
        </div>
      </main>
    )
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

        <div className="mt-6 grid grid-cols-3 gap-3">
          <div className="rounded-xl border border-[#1e3a5f] bg-[#0b1f35] px-4 py-3">
            <p className="text-xs text-gray-400">Score</p>
            <h3 className="mt-1 text-xl font-bold text-[#f4b400]">{score}%</h3>
          </div>

          <div className="rounded-xl border border-[#1e3a5f] bg-[#0b1f35] px-4 py-3">
            <p className="text-xs text-gray-400">Correct</p>
            <h3 className="mt-1 text-xl font-bold text-green-400">
              {correctCount}
            </h3>
          </div>

          <div className="rounded-xl border border-[#1e3a5f] bg-[#0b1f35] px-4 py-3">
            <p className="text-xs text-gray-400">Wrong</p>
            <h3 className="mt-1 text-xl font-bold text-red-400">
              {wrongCount}
            </h3>
          </div>
        </div>

        <div className="mt-8 rounded-2xl border border-[#1e3a5f] bg-[#081726] p-6">
          <div className="mb-6">
            <div className="flex items-center justify-between text-sm text-gray-400">
              <span>
                Question {currentQuestionIndex + 1} of{" "}
                {filteredQuestions.length}
              </span>

              <span>{Math.round(((currentQuestionIndex + 1) / filteredQuestions.length) * 100)}%</span>
            </div>

            <div className="mt-3 h-2 rounded-full bg-[#06111f] overflow-hidden">
              <div
                className="h-full bg-[#f4b400] transition-all"
                style={{
                  width: `${((currentQuestionIndex + 1) / filteredQuestions.length) * 100}%`,
                }}
              />
            </div>
          </div>

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
              <p
                className={`text-sm font-semibold ${
                  selectedAnswer === currentQuestion.correctAnswer
                    ? "text-green-400"
                    : "text-red-400"
                }`}
              >
                {selectedAnswer === currentQuestion.correctAnswer
                  ? "Correct"
                  : "Incorrect"}
              </p>

              <p className="mt-3 text-sm text-gray-400">
                Correct answer:{" "}
                <span className="font-semibold text-[#f4b400]">
                  {currentQuestion.correctAnswer}
                </span>
              </p>

              <p className="mt-4 text-gray-300 leading-relaxed">
                {currentQuestion.explanation}
              </p>

              <button
                onClick={nextQuestion}
                className="mt-6 rounded-xl bg-[#f4b400] px-6 py-3 font-bold text-[#06111f] hover:bg-[#d9a000] transition"
              >
                {currentQuestionIndex === filteredQuestions.length - 1
                  ? "Finish Practice"
                  : "Next Question"}
              </button>
            </div>
          )}
        </div>
      </div>
    </main>
  )
}