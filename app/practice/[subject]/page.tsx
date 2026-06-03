"use client"

import { useEffect, useState } from "react"
import { useParams, useRouter } from "next/navigation"
import Link from "next/link"
import { supabase } from "@/src/lib/supabase"

type Question = {
  id: number
  subject: string
  topic?: string
  question: string
  options: string[]
  correctAnswer: string
  explanation: string
}

type ExamMode = "menu" | "mock"

const MOCK_QUESTION_COUNT = 25
const MOCK_TIME_SECONDS = 25 * 60
const PASS_MARK = 75

export default function SubjectPracticePage() {
  const params = useParams()
  const router = useRouter()
  const subject = String(params.subject)

  const [subjectQuestions, setSubjectQuestions] = useState<Question[]>([])
  const [isLoadingQuestions, setIsLoadingQuestions] = useState(true)

  const [examMode, setExamMode] = useState<ExamMode>("menu")
  const [examQuestions, setExamQuestions] = useState<Question[]>([])
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0)
  const [answers, setAnswers] = useState<Record<number, string>>({})
  const [pinnedQuestions, setPinnedQuestions] = useState<number[]>([])
  const [shownAnswers, setShownAnswers] = useState<number[]>([])
  const [isSubmitted, setIsSubmitted] = useState(false)
  const [showFinishPrompt, setShowFinishPrompt] = useState(false)
  const [showMobileQuestionNav, setShowMobileQuestionNav] = useState(false)
  const [timeLeft, setTimeLeft] = useState(MOCK_TIME_SECONDS)

  useEffect(() => {
    const checkUserAndFetchQuestions = async () => {
      setIsLoadingQuestions(true)

      const {
        data: { user },
      } = await supabase.auth.getUser()

      if (!user) {
        router.push("/")
        return
      }

      const { data, error } = await supabase
        .from("questions")
        .select("*")
        .eq("is_trial_question", true)

      if (error) {
        console.log("Supabase error:", error)
        setSubjectQuestions([])
        setIsLoadingQuestions(false)
        return
      }

      const formattedQuestions =
        data
          ?.filter((q) => {
            const dbSubject = normalizeText(String(q.subject || ""))
            const routeSubject = normalizeText(subject)

            return dbSubject === routeSubject
          })
          .slice(0, MOCK_QUESTION_COUNT)
          .map((q) => ({
            id: q.id,
            subject: q.subject,
            topic: q.topic,
            question: q.question,
            options: [q.option_a, q.option_b, q.option_c, q.option_d],
            correctAnswer: q.correct_answer,
            explanation: q.explanation,
          })) || []

      setSubjectQuestions(formattedQuestions)
      setIsLoadingQuestions(false)
    }

    checkUserAndFetchQuestions()
  }, [subject, router])

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

  const normalizeText = (value: string) => {
    return value.toLowerCase().trim().replace(/-/g, " ")
  }

  const formatSubjectName = (value: string) => {
    return value
      .split("-")
      .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
      .join(" ")
  }

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
    setShowMobileQuestionNav(false)
  }

  const startMockExam = () => {
    resetExamState()
    setExamQuestions(subjectQuestions.slice(0, MOCK_QUESTION_COUNT))
    setExamMode("mock")
    setTimeLeft(MOCK_TIME_SECONDS)
  }

  const returnToMenu = () => {
    resetExamState()
    setExamMode("menu")
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
    if (currentQuestionIndex < examQuestions.length - 1) {
      setCurrentQuestionIndex((prev) => prev + 1)
    }
  }

  const currentQuestion = examQuestions[currentQuestionIndex]
  const selectedAnswer = answers[currentQuestionIndex]
  const totalQuestions = examQuestions.length
  const unansweredCount = totalQuestions - Object.keys(answers).length

  const correctAnswers = examQuestions.filter(
    (question, index) => answers[index] === question.correctAnswer
  ).length

  const scorePercentage =
    totalQuestions > 0 ? Math.round((correctAnswers / totalQuestions) * 100) : 0

  const passed = scorePercentage >= PASS_MARK

  const wrongQuestions = examQuestions.filter(
    (question, index) => answers[index] !== question.correctAnswer
  )

  if (isLoadingQuestions) {
    return (
      <main className="min-h-screen bg-[#06111f] px-4 py-10 text-white sm:px-6">
        <div className="mx-auto max-w-4xl">
          <p className="text-sm font-medium text-[#f4b400]">
            Loading questions...
          </p>
        </div>
      </main>
    )
  }

  if (subjectQuestions.length === 0) {
    return (
      <main className="min-h-screen bg-[#06111f] px-4 py-10 text-white sm:px-6">
        <div className="mx-auto max-w-4xl">
          <Link
            href="/dashboard"
            className="text-sm font-medium text-[#f4b400] hover:text-white"
          >
            ← Back to Dashboard
          </Link>

          <div className="mt-8 rounded-3xl border border-[#1e3a5f] bg-[#081726] p-8">
            <p className="text-xs uppercase tracking-[0.25em] text-[#f4b400]">
              No Trial Questions
            </p>

            <h1 className="mt-3 text-3xl font-bold">
              No trial questions found for {formatSubjectName(subject)}.
            </h1>

            <p className="mt-3 text-gray-400">
              Make sure this subject has 25 questions marked as trial questions
              in Supabase.
            </p>
          </div>
        </div>
      </main>
    )
  }

  if (examMode === "menu") {
    return (
      <main className="min-h-screen bg-[#06111f] px-4 py-10 text-white sm:px-6">
        <div className="mx-auto max-w-5xl">
          <Link
            href="/dashboard"
            className="text-sm font-medium text-[#f4b400] hover:text-white"
          >
            ← Back to Dashboard
          </Link>

          <div className="mt-8 rounded-3xl border border-[#1e3a5f] bg-[#081726] p-6 sm:p-8">
            <p className="text-xs uppercase tracking-[0.25em] text-[#f4b400]">
              {formatSubjectName(subject)}
            </p>

            <h1 className="mt-3 text-3xl font-bold sm:text-4xl">
              Choose your training mode
            </h1>

            <p className="mt-3 max-w-2xl text-gray-400">
              Trial users can start the fixed 25-question mock exam. Practice by
              topic is available with an active subscription.
            </p>
          </div>

          <div className="mt-8 grid gap-5 md:grid-cols-2">
            <button
              onClick={startMockExam}
              className="group rounded-2xl border border-[#1e3a5f] bg-[#081726] p-6 text-left transition-all hover:-translate-y-1 hover:border-[#f4b400]"
            >
              <p className="text-xs uppercase tracking-[0.25em] text-[#f4b400]">
                Trial Access
              </p>

              <h2 className="mt-3 text-2xl font-bold text-white">
                Mock Exam
              </h2>

              <p className="mt-3 text-sm leading-6 text-gray-400">
                Start the fixed 25-question trial mock exam for this subject.
              </p>

              <p className="mt-5 text-sm font-medium text-[#f4b400] transition group-hover:text-[#ffd24d]">
                Start Mock Exam →
              </p>
            </button>

            <div className="rounded-2xl border border-[#1e3a5f] bg-[#081726]/60 p-6 opacity-75">
              <p className="text-xs uppercase tracking-[0.25em] text-[#f4b400]">
                Subscription Feature
              </p>

              <h2 className="mt-3 text-2xl font-bold text-white">
                Practice by Topic
              </h2>

              <p className="mt-3 text-sm leading-6 text-gray-400">
                Target weak areas by topic and build confidence faster with the
                full PilotVault question bank.
              </p>

              <Link
                href="/upgrade"
                className="mt-5 inline-flex text-sm font-medium text-[#f4b400] hover:text-[#ffd24d]"
              >
                Upgrade to Unlock →
              </Link>
            </div>
          </div>
        </div>
      </main>
    )
  }

  if (isSubmitted) {
    return (
      <main className="min-h-screen bg-[#06111f] px-4 py-10 text-white sm:px-6">
        <div className="mx-auto max-w-5xl">
          <div className="rounded-3xl border border-[#1e3a5f] bg-[#081726] p-6 sm:p-8">
            <p className="text-xs uppercase tracking-[0.25em] text-[#f4b400]">
              Mock Exam Complete
            </p>

            <h1 className="mt-3 text-4xl font-bold">
              {scorePercentage}%
            </h1>

            <p className="mt-3 text-gray-400">
              You answered {correctAnswers} out of {totalQuestions} questions
              correctly.
            </p>

            <p
              className={`mt-4 text-lg font-bold ${
                passed ? "text-[#f4b400]" : "text-red-400"
              }`}
            >
              {passed ? "Passed" : "Not yet passed"}
            </p>

            <div className="mt-6 flex flex-wrap gap-3">
              <button
                onClick={returnToMenu}
                className="rounded-xl border border-[#1e3a5f] px-5 py-3 text-sm font-semibold text-gray-300 hover:border-[#f4b400] hover:text-[#f4b400]"
              >
                Back to Subject
              </button>

              <button
                onClick={startMockExam}
                className="rounded-xl bg-[#f4b400] px-5 py-3 text-sm font-bold text-[#06111f] hover:bg-[#d9a000]"
              >
                Restart Mock Exam
              </button>
            </div>
          </div>

          {wrongQuestions.length > 0 && (
            <div className="mt-8 rounded-3xl border border-[#1e3a5f] bg-[#081726] p-6 sm:p-8">
              <h2 className="text-2xl font-bold">
                Review incorrect questions
              </h2>

              <div className="mt-6 space-y-5">
                {wrongQuestions.map((question, index) => {
                  const originalIndex = examQuestions.findIndex(
                    (item) => item.id === question.id
                  )

                  return (
                    <div
                      key={question.id}
                      className="rounded-2xl border border-[#1e3a5f] bg-[#06111f] p-5"
                    >
                      <p className="text-sm text-[#f4b400]">
                        Question {originalIndex + 1}
                      </p>

                      <p className="mt-2 font-semibold text-white">
                        {question.question}
                      </p>

                      <p className="mt-3 text-sm text-gray-400">
                        Your answer: {answers[originalIndex] || "Not answered"}
                      </p>

                      <p className="mt-1 text-sm text-[#f4b400]">
                        Correct answer: {question.correctAnswer}
                      </p>

                      <p className="mt-3 text-sm leading-6 text-gray-400">
                        {question.explanation}
                      </p>
                    </div>
                  )
                })}
              </div>
            </div>
          )}
        </div>
      </main>
    )
  }

  return (
    <main className="min-h-screen bg-[#06111f] text-white">
      <header className="border-b border-[#1e3a5f] bg-[#06111f]/95">
        <div className="mx-auto flex min-h-20 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
          <div>
            <p className="text-xs uppercase tracking-[0.25em] text-[#f4b400]">
              {formatSubjectName(subject)}
            </p>

            <h1 className="mt-1 text-lg font-bold">Mock Exam</h1>
          </div>

          <div className="flex items-center gap-3">
            <p className="rounded-xl border border-[#1e3a5f] px-4 py-3 text-sm font-bold text-[#f4b400]">
              {formatTime(timeLeft)}
            </p>

            <button
              onClick={() => setShowFinishPrompt(true)}
              className="rounded-xl bg-[#f4b400] px-5 py-3 text-sm font-bold text-[#06111f] hover:bg-[#d9a000]"
            >
              Finish
            </button>
          </div>
        </div>
      </header>

      <section className="mx-auto grid max-w-7xl gap-6 px-4 py-8 sm:px-6 lg:grid-cols-[260px_1fr] lg:px-8">
        <aside className="hidden rounded-3xl border border-[#1e3a5f] bg-[#081726] p-5 lg:block">
          <p className="text-xs uppercase tracking-[0.25em] text-[#f4b400]">
            Questions
          </p>

          <div className="mt-5 grid grid-cols-5 gap-2">
            {examQuestions.map((_, index) => (
              <button
                key={index}
                onClick={() => setCurrentQuestionIndex(index)}
                className={`h-10 rounded-lg border text-sm font-semibold transition ${
                  currentQuestionIndex === index
                    ? "border-[#f4b400] bg-[#f4b400] text-[#06111f]"
                    : answers[index]
                      ? "border-[#f4b400]/40 bg-[#f4b400]/10 text-[#f4b400]"
                      : "border-[#1e3a5f] text-gray-300 hover:border-[#f4b400]"
                }`}
              >
                {index + 1}
              </button>
            ))}
          </div>
        </aside>

        <div>
          <div className="mb-4 flex items-center justify-between lg:hidden">
            <button
              onClick={() => setShowMobileQuestionNav(!showMobileQuestionNav)}
              className="rounded-xl border border-[#1e3a5f] px-4 py-3 text-sm text-gray-300"
            >
              Questions
            </button>

            <p className="text-sm text-gray-400">
              {currentQuestionIndex + 1} / {totalQuestions}
            </p>
          </div>

          {showMobileQuestionNav && (
            <div className="mb-5 grid grid-cols-5 gap-2 rounded-2xl border border-[#1e3a5f] bg-[#081726] p-4 lg:hidden">
              {examQuestions.map((_, index) => (
                <button
                  key={index}
                  onClick={() => {
                    setCurrentQuestionIndex(index)
                    setShowMobileQuestionNav(false)
                  }}
                  className={`h-10 rounded-lg border text-sm font-semibold ${
                    currentQuestionIndex === index
                      ? "border-[#f4b400] bg-[#f4b400] text-[#06111f]"
                      : answers[index]
                        ? "border-[#f4b400]/40 bg-[#f4b400]/10 text-[#f4b400]"
                        : "border-[#1e3a5f] text-gray-300"
                  }`}
                >
                  {index + 1}
                </button>
              ))}
            </div>
          )}

          <div className="rounded-3xl border border-[#1e3a5f] bg-[#081726] p-6 sm:p-8">
            <div className="flex items-start justify-between gap-4">
              <div>
                <p className="text-xs uppercase tracking-[0.25em] text-[#f4b400]">
                  Question {currentQuestionIndex + 1} of {totalQuestions}
                </p>

                <h2 className="mt-4 text-xl font-bold leading-8 text-white">
                  {currentQuestion.question}
                </h2>
              </div>

              <button
                onClick={() => togglePin(currentQuestionIndex)}
                className={`rounded-xl border px-3 py-2 text-xs font-semibold ${
                  pinnedQuestions.includes(currentQuestionIndex)
                    ? "border-[#f4b400] text-[#f4b400]"
                    : "border-[#1e3a5f] text-gray-400"
                }`}
              >
                Pin
              </button>
            </div>

            <div className="mt-6 space-y-3">
              {currentQuestion.options.map((option, index) => (
                <button
                  key={index}
                  onClick={() => handleAnswer(option)}
                  className={`w-full rounded-2xl border p-4 text-left text-sm transition ${
                    selectedAnswer === option
                      ? "border-[#f4b400] bg-[#f4b400]/10 text-white"
                      : "border-[#1e3a5f] bg-[#06111f] text-gray-300 hover:border-[#f4b400]"
                  }`}
                >
                  {option}
                </button>
              ))}
            </div>

            {shownAnswers.includes(currentQuestionIndex) && (
              <div className="mt-6 rounded-2xl border border-[#f4b400]/30 bg-[#f4b400]/10 p-5">
                <p className="text-sm font-bold text-[#f4b400]">
                  Correct Answer: {currentQuestion.correctAnswer}
                </p>

                <p className="mt-3 text-sm leading-6 text-gray-300">
                  {currentQuestion.explanation}
                </p>
              </div>
            )}

            <div className="mt-8 flex flex-wrap items-center justify-between gap-3">
              <button
                onClick={toggleAnswer}
                className="rounded-xl border border-[#1e3a5f] px-5 py-3 text-sm font-semibold text-gray-300 hover:border-[#f4b400] hover:text-[#f4b400]"
              >
                {shownAnswers.includes(currentQuestionIndex)
                  ? "Hide Answer"
                  : "Show Answer"}
              </button>

              <div className="flex gap-3">
                <button
                  onClick={goPrevious}
                  disabled={currentQuestionIndex === 0}
                  className="rounded-xl border border-[#1e3a5f] px-5 py-3 text-sm font-semibold text-gray-300 disabled:opacity-40"
                >
                  Previous
                </button>

                <button
                  onClick={goNext}
                  disabled={currentQuestionIndex === totalQuestions - 1}
                  className="rounded-xl bg-[#f4b400] px-5 py-3 text-sm font-bold text-[#06111f] disabled:opacity-40"
                >
                  Next
                </button>
              </div>
            </div>
          </div>

          <p className="mt-4 text-sm text-gray-500">
            {unansweredCount} unanswered questions remaining.
          </p>
        </div>
      </section>

      {showFinishPrompt && (
        <div className="fixed inset-0 z-[100] flex items-center justify-center bg-black/70 px-4">
          <div className="w-full max-w-md rounded-3xl border border-[#1e3a5f] bg-[#081726] p-6">
            <p className="text-xs uppercase tracking-[0.25em] text-[#f4b400]">
              Finish Exam
            </p>

            <h2 className="mt-3 text-2xl font-bold">
              Submit your mock exam?
            </h2>

            <p className="mt-3 text-sm text-gray-400">
              You still have {unansweredCount} unanswered questions.
            </p>

            <div className="mt-6 flex gap-3">
              <button
                onClick={() => setShowFinishPrompt(false)}
                className="flex-1 rounded-xl border border-[#1e3a5f] px-5 py-3 text-sm font-semibold text-gray-300"
              >
                Continue
              </button>

              <button
                onClick={() => {
                  setShowFinishPrompt(false)
                  setIsSubmitted(true)
                }}
                className="flex-1 rounded-xl bg-[#f4b400] px-5 py-3 text-sm font-bold text-[#06111f]"
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