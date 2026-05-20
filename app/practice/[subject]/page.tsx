"use client"

import { useEffect, useMemo, useState } from "react"
import { useParams } from "next/navigation"
import Link from "next/link"
import { questions } from "@/src/data/questions"
import {
  ArrowLeft,
  Clock,
  Flag,
  Home,
  Pin,
  RotateCcw,
  Trophy,
} from "lucide-react"

type Question = {
  id: number
  subject: string
  topic?: string
  question: string
  options: string[]
  correctAnswer: string
  explanation: string
}

type ExamMode = "menu" | "mock" | "topic"

const MOCK_QUESTION_COUNT = 25
const MOCK_TIME_SECONDS = 25 * 60
const TOPIC_TIME_SECONDS = 25 * 60
const PASS_MARK = 75

export default function SubjectPracticePage() {
  const params = useParams()
  const subject = String(params.subject)

  const subjectQuestions = useMemo(() => {
    return (questions as Question[]).filter(
      (q) => q.subject?.toLowerCase() === subject.toLowerCase()
    )
  }, [subject])

  const topics = useMemo(() => {
    return Array.from(
      new Set(subjectQuestions.map((q) => q.topic).filter(Boolean))
    ) as string[]
  }, [subjectQuestions])

  const [examMode, setExamMode] = useState<ExamMode>("menu")
  const [activeTopic, setActiveTopic] = useState("")
  const [examQuestions, setExamQuestions] = useState<Question[]>([])
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0)
  const [answers, setAnswers] = useState<Record<number, string>>({})
  const [pinnedQuestions, setPinnedQuestions] = useState<number[]>([])
  const [shownAnswers, setShownAnswers] = useState<number[]>([])
  const [isSubmitted, setIsSubmitted] = useState(false)
  const [showFinishPrompt, setShowFinishPrompt] = useState(false)
  const [timeLeft, setTimeLeft] = useState(MOCK_TIME_SECONDS)

  const currentQuestion = examQuestions[currentQuestionIndex]
  const selectedAnswer = answers[currentQuestionIndex]
  const totalQuestions = examQuestions.length
  const answeredCount = Object.keys(answers).length
  const unansweredCount = totalQuestions - answeredCount

  const correctAnswers = examQuestions.filter(
    (question, index) => answers[index] === question.correctAnswer
  ).length

  const scorePercentage =
    totalQuestions > 0 ? Math.round((correctAnswers / totalQuestions) * 100) : 0

  const passed = scorePercentage >= PASS_MARK

  const wrongQuestions = examQuestions.filter(
    (question, index) => answers[index] !== question.correctAnswer
  )

  useEffect(() => {
    if (examMode === "menu" || isSubmitted || examQuestions.length === 0) return

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
  }, [examMode, isSubmitted, examQuestions.length])

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60

    return `${mins}:${secs.toString().padStart(2, "0")}`
  }

  const resetExamState = () => {
    setCurrentQuestionIndex(0)
    setAnswers({})
    setPinnedQuestions([])
    setShownAnswers([])
    setIsSubmitted(false)
    setShowFinishPrompt(false)
  }

  const shuffleQuestions = (items: Question[]) => {
    return [...items].sort(() => Math.random() - 0.5)
  }

  const startMockExam = () => {
    resetExamState()

    const randomizedQuestions = shuffleQuestions(subjectQuestions).slice(
      0,
      MOCK_QUESTION_COUNT
    )

    setExamQuestions(randomizedQuestions)
    setActiveTopic("")
    setExamMode("mock")
    setTimeLeft(MOCK_TIME_SECONDS)
  }

  const startTopicPractice = (topic: string) => {
    resetExamState()

    const topicQuestions = subjectQuestions.filter((q) => q.topic === topic)

    setExamQuestions(topicQuestions)
    setActiveTopic(topic)
    setExamMode("topic")
    setTimeLeft(TOPIC_TIME_SECONDS)
  }

  const returnToMenu = () => {
    resetExamState()
    setExamMode("menu")
    setActiveTopic("")
    setExamQuestions([])
    setTimeLeft(MOCK_TIME_SECONDS)
  }

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

  const examLabel =
    examMode === "mock"
      ? "Mock Exam"
      : activeTopic
        ? `${activeTopic} Practice`
        : "Practice"

  if (subjectQuestions.length === 0) {
    return (
      <main className="min-h-screen bg-[#06111f] px-4 py-10 text-white">
        <div className="mx-auto max-w-4xl">
          <Link
            href="/practice"
            className="text-sm font-medium text-[#f4b400] hover:text-white"
          >
            ← Back to Practice
          </Link>

          <div className="mt-10 rounded-2xl border border-red-500/40 bg-red-500/10 p-6">
            <h1 className="text-2xl font-bold text-red-300">
              No questions found for this subject.
            </h1>

            <p className="mt-3 text-slate-300">
              Check that your questions use subject: "{subject}" inside
              src/data/questions.ts.
            </p>
          </div>
        </div>
      </main>
    )
  }

  if (examMode === "menu") {
    return (
      <main className="min-h-screen bg-[#06111f] text-white">
        <header className="border-b border-[#1e3a5f] bg-[#06111f]/95">
          <div className="mx-auto flex min-h-20 max-w-7xl flex-col gap-4 px-4 py-4 sm:flex-row sm:items-center sm:justify-between sm:px-6 lg:px-8">
            <div>
              <p className="text-xs uppercase tracking-[0.25em] text-[#f4b400]">
                PilotVault SA
              </p>

              <h1 className="mt-1 text-xl font-bold capitalize">
                {subject.replaceAll("-", " ")} Practice
              </h1>
            </div>

            <div className="flex gap-3">
              <Link
                href="/practice"
                className="rounded-xl border border-[#1e3a5f] bg-[#0b1f35] px-4 py-2 text-sm hover:bg-[#1e3a5f]"
              >
                Subjects
              </Link>

              <Link
                href="/dashboard"
                className="rounded-xl bg-[#f4b400] px-4 py-2 text-sm font-bold text-[#06111f] hover:bg-[#d9a000]"
              >
                Dashboard
              </Link>
            </div>
          </div>
        </header>

        <section className="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8">
          <div className="mb-8 rounded-3xl border border-[#1e3a5f] bg-[#0b1f35] p-6 sm:p-8">
            <h2 className="text-3xl font-bold">
              Choose your exam mode
            </h2>

            <p className="mt-3 max-w-2xl text-gray-400">
              Practice by topic or start a timed mock exam with 25 randomized
              questions.
            </p>
          </div>

          <div className="grid gap-6 lg:grid-cols-2">
            <button
              onClick={startMockExam}
              className="rounded-3xl border border-[#f4b400] bg-[#0b1f35] p-6 text-left shadow-lg shadow-[#f4b400]/10 transition hover:-translate-y-1 hover:bg-[#102942]"
            >
              <div className="mb-5 flex h-12 w-12 items-center justify-center rounded-xl bg-[#f4b400] text-[#06111f]">
                <Clock className="h-6 w-6" />
              </div>

              <h3 className="text-2xl font-bold">
                Start Mock Exam
              </h3>

              <p className="mt-3 text-gray-400">
                25 questions • 25 minutes • randomized each attempt
              </p>
            </button>

            <div className="rounded-3xl border border-[#1e3a5f] bg-[#0b1f35] p-6">
              <h3 className="text-2xl font-bold">
                Topic Practice
              </h3>

              <p className="mt-3 text-gray-400">
                Select a topic and focus on weak areas.
              </p>

              <div className="mt-6 grid gap-3 sm:grid-cols-2">
                {topics.length > 0 ? (
                  topics.map((topic) => (
                    <button
                      key={topic}
                      onClick={() => startTopicPractice(topic)}
                      className="rounded-xl border border-[#1e3a5f] bg-[#06111f] px-4 py-3 text-left text-sm font-semibold hover:border-[#f4b400] hover:text-[#f4b400]"
                    >
                      {topic}
                    </button>
                  ))
                ) : (
                  <button
                    onClick={() => startTopicPractice("")}
                    className="rounded-xl border border-[#1e3a5f] bg-[#06111f] px-4 py-3 text-left text-sm font-semibold hover:border-[#f4b400] hover:text-[#f4b400]"
                  >
                    All Questions
                  </button>
                )}
              </div>
            </div>
          </div>
        </section>
      </main>
    )
  }

  if (isSubmitted) {
    return (
      <main className="min-h-screen bg-[#f3f4f6] text-[#111827]">
        <header className="border-b bg-white">
          <div className="mx-auto flex min-h-16 max-w-7xl flex-col gap-3 px-4 py-4 sm:flex-row sm:items-center sm:justify-between sm:px-6 lg:px-8">
            <div>
              <p className="text-xs font-bold uppercase tracking-[0.2em] text-[#06111f]">
                PilotVault SA
              </p>

              <h1 className="text-lg font-bold">
                Exam Results
              </h1>
            </div>

            <button
              onClick={returnToMenu}
              className="rounded-lg bg-[#06111f] px-4 py-2 text-sm font-bold text-white"
            >
              Back to Practice
            </button>
          </div>
        </header>

        <section className="mx-auto max-w-5xl px-4 py-8 sm:px-6 lg:px-8">
          <div className="rounded-2xl bg-white p-6 shadow-sm sm:p-8">
            <div className="flex flex-col gap-6 sm:flex-row sm:items-center sm:justify-between">
              <div>
                <div className="mb-4 flex h-14 w-14 items-center justify-center rounded-full bg-[#f4b400]/20 text-[#06111f]">
                  <Trophy className="h-7 w-7" />
                </div>

                <h2 className="text-3xl font-bold">
                  {passed ? "Passed" : "Not Yet Passed"}
                </h2>

                <p className="mt-2 text-gray-600">
                  Pass mark: {PASS_MARK}%
                </p>
              </div>

              <div className="text-left sm:text-right">
                <p className="text-5xl font-bold text-[#06111f]">
                  {scorePercentage}%
                </p>

                <p className="mt-2 text-gray-600">
                  {correctAnswers} / {totalQuestions} correct
                </p>
              </div>
            </div>
          </div>

          <div className="mt-6 rounded-2xl bg-white p-6 shadow-sm">
            <h3 className="text-xl font-bold">
              Questions to Review
            </h3>

            <div className="mt-5 space-y-5">
              {wrongQuestions.length === 0 ? (
                <p className="text-green-700">
                  Perfect attempt. No incorrect questions.
                </p>
              ) : (
                wrongQuestions.map((question) => {
                  const originalIndex = examQuestions.indexOf(question)

                  return (
                    <div
                      key={question.id}
                      className="rounded-xl border border-red-200 bg-red-50 p-4"
                    >
                      <p className="text-sm font-bold text-red-700">
                        Question {originalIndex + 1}
                      </p>

                      <p className="mt-2 font-semibold">
                        {question.question}
                      </p>

                      <p className="mt-3 text-sm text-gray-700">
                        Your answer:{" "}
                        <span className="font-semibold">
                          {answers[originalIndex] || "Unanswered"}
                        </span>
                      </p>

                      <p className="mt-1 text-sm text-green-700">
                        Correct answer:{" "}
                        <span className="font-semibold">
                          {question.correctAnswer}
                        </span>
                      </p>

                      <p className="mt-3 text-sm text-gray-700">
                        {question.explanation}
                      </p>
                    </div>
                  )
                })
              )}
            </div>
          </div>
        </section>
      </main>
    )
  }

  return (
    <main className="min-h-screen bg-[#e5e7eb] text-[#111827]">
      <header className="sticky top-0 z-40 border-b bg-white shadow-sm">
        <div className="mx-auto flex min-h-16 max-w-7xl flex-col gap-3 px-4 py-3 sm:flex-row sm:items-center sm:justify-between sm:px-6 lg:px-8">
          <div>
            <p className="text-xs font-bold uppercase tracking-[0.2em] text-[#06111f]">
              PilotVault SA
            </p>

            <h1 className="text-sm font-semibold sm:text-base">
              {examLabel} • {subject.replaceAll("-", " ")}
            </h1>
          </div>

          <div className="flex flex-wrap items-center gap-2">
            <div className="flex items-center gap-2 rounded-lg border bg-gray-50 px-3 py-2 text-sm font-bold">
              <Clock className="h-4 w-4" />
              {formatTime(timeLeft)}
            </div>

            <button
              onClick={returnToMenu}
              className="rounded-lg border px-3 py-2 text-sm font-semibold hover:bg-gray-100"
            >
              Exit
            </button>

            <button
              onClick={() => setShowFinishPrompt(true)}
              className="rounded-lg bg-[#06111f] px-4 py-2 text-sm font-bold text-white hover:bg-[#0b1f35]"
            >
              Finish
            </button>
          </div>
        </div>
      </header>

      <section className="mx-auto grid max-w-7xl gap-4 px-4 py-4 sm:px-6 lg:grid-cols-[220px_1fr] lg:px-8">
        <aside className="rounded-xl bg-white p-4 shadow-sm lg:sticky lg:top-24 lg:h-fit">
          <div className="mb-4 flex items-center justify-between">
            <h2 className="font-bold">
              Questions
            </h2>

            <span className="text-xs text-gray-500">
              {answeredCount}/{totalQuestions}
            </span>
          </div>

          <div className="grid grid-cols-5 gap-2 lg:grid-cols-4">
            {examQuestions.map((_, index) => {
              const isActive = index === currentQuestionIndex
              const isAnswered = answers[index]
              const isPinned = pinnedQuestions.includes(index)

              return (
                <button
                  key={index}
                  onClick={() => setCurrentQuestionIndex(index)}
                  className={`relative flex h-10 items-center justify-center rounded-lg border text-sm font-bold ${
                    isActive
                      ? "border-[#06111f] bg-[#06111f] text-white"
                      : isAnswered
                        ? "border-green-600 bg-green-50 text-green-700"
                        : "border-gray-300 bg-white text-gray-700"
                  }`}
                >
                  {index + 1}

                  {isPinned && (
                    <span className="absolute -right-1 -top-1 h-3 w-3 rounded-full bg-[#f4b400]" />
                  )}
                </button>
              )
            })}
          </div>

          <div className="mt-4 text-xs text-gray-500">
            Unanswered: {unansweredCount}
          </div>
        </aside>

        <div className="rounded-xl bg-white shadow-sm">
          <div className="border-b p-4 sm:p-6">
            <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
              <div>
                <p className="text-sm font-semibold text-gray-500">
                  Question {currentQuestionIndex + 1} of {totalQuestions}
                </p>

                {currentQuestion?.topic && (
                  <p className="mt-1 text-xs text-gray-500">
                    Topic: {currentQuestion.topic}
                  </p>
                )}
              </div>

              <button
                onClick={() => togglePin(currentQuestionIndex)}
                className={`flex items-center gap-2 rounded-lg border px-3 py-2 text-sm font-semibold ${
                  pinnedQuestions.includes(currentQuestionIndex)
                    ? "border-[#f4b400] bg-[#f4b400]/20 text-[#06111f]"
                    : "hover:bg-gray-50"
                }`}
              >
                <Pin className="h-4 w-4" />
                Pin
              </button>
            </div>
          </div>

          <div className="p-4 sm:p-6">
            <h2 className="text-lg font-semibold leading-relaxed sm:text-xl">
              {currentQuestion?.question}
            </h2>

            <div className="mt-6 space-y-3">
              {currentQuestion?.options.map((option, index) => {
                const letter = String.fromCharCode(65 + index)
                const isSelected = selectedAnswer === option
                const showAnswer = shownAnswers.includes(currentQuestionIndex)
                const isCorrect = option === currentQuestion.correctAnswer

                return (
                  <button
                    key={option}
                    onClick={() => handleAnswer(option)}
                    className={`flex w-full items-start gap-3 rounded-xl border p-4 text-left transition ${
                      showAnswer && isCorrect
                        ? "border-green-600 bg-green-50"
                        : isSelected
                          ? "border-[#06111f] bg-[#06111f]/5"
                          : "border-gray-300 hover:border-[#06111f]"
                    }`}
                  >
                    <span
                      className={`flex h-7 w-7 flex-shrink-0 items-center justify-center rounded-full border text-sm font-bold ${
                        isSelected
                          ? "border-[#06111f] bg-[#06111f] text-white"
                          : "border-gray-400"
                      }`}
                    >
                      {letter}
                    </span>

                    <span className="text-sm leading-relaxed sm:text-base">
                      {option}
                    </span>
                  </button>
                )
              })}
            </div>

            {shownAnswers.includes(currentQuestionIndex) && (
              <div className="mt-6 rounded-xl border border-[#f4b400]/40 bg-[#f4b400]/10 p-4">
                <p className="font-bold text-[#06111f]">
                  Correct Answer: {currentQuestion.correctAnswer}
                </p>

                <p className="mt-2 text-sm text-gray-700">
                  {currentQuestion.explanation}
                </p>
              </div>
            )}
          </div>

          <div className="flex flex-col gap-3 border-t p-4 sm:flex-row sm:items-center sm:justify-between sm:p-6">
            <button
              onClick={toggleAnswer}
              className="rounded-lg border px-4 py-2 text-sm font-semibold hover:bg-gray-50"
            >
              {shownAnswers.includes(currentQuestionIndex)
                ? "Hide Answer"
                : "Show Answer"}
            </button>

            <div className="flex gap-3">
              <button
                onClick={goPrevious}
                disabled={currentQuestionIndex === 0}
                className="flex-1 rounded-lg border px-4 py-2 text-sm font-semibold disabled:cursor-not-allowed disabled:opacity-40 sm:flex-none"
              >
                Previous
              </button>

              <button
                onClick={goNext}
                disabled={currentQuestionIndex === totalQuestions - 1}
                className="flex-1 rounded-lg bg-[#06111f] px-4 py-2 text-sm font-bold text-white disabled:cursor-not-allowed disabled:opacity-40 sm:flex-none"
              >
                Next
              </button>
            </div>
          </div>
        </div>
      </section>

      {showFinishPrompt && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 px-4">
          <div className="w-full max-w-md rounded-2xl bg-white p-6 shadow-2xl">
            <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-[#f4b400]/20">
              <Flag className="h-6 w-6 text-[#06111f]" />
            </div>

            <h2 className="text-2xl font-bold">
              Finish exam?
            </h2>

            <p className="mt-3 text-gray-600">
              You still have {unansweredCount} unanswered question
              {unansweredCount === 1 ? "" : "s"}.
            </p>

            <div className="mt-6 flex flex-col gap-3 sm:flex-row">
              <button
                onClick={() => setShowFinishPrompt(false)}
                className="flex-1 rounded-lg border px-4 py-3 font-semibold"
              >
                Continue Exam
              </button>

              <button
                onClick={() => {
                  setShowFinishPrompt(false)
                  setIsSubmitted(true)
                }}
                className="flex-1 rounded-lg bg-[#06111f] px-4 py-3 font-bold text-white"
              >
                Submit
              </button>
            </div>
          </div>
        </div>
      )}
    </main>
  )
}