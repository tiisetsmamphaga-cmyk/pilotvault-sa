"use client"

import { useEffect, useState } from "react"
import { useParams } from "next/navigation"
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

type ExamMode = "menu" | "mock" | "topic"

const MOCK_QUESTION_COUNT = 25
const MOCK_TIME_SECONDS = 25 * 60
const TOPIC_TIME_SECONDS = 25 * 60
const PASS_MARK = 75

export default function SubjectPracticePage() {
  const params = useParams()
  const subject = String(params.subject)

  const [subjectQuestions, setSubjectQuestions] = useState<Question[]>([])

useEffect(() => {
  const fetchQuestions = async () => {
    const { data, error } = await supabase
      .from("questions")
      .select("*")
      .eq("subject", subject)

    if (error) {
      console.log(error)
      return
    }

    const formattedQuestions =
      data?.map((q) => ({
        id: q.id,
        subject: q.subject,
        topic: q.topic,
        question: q.question,
        options: [
          q.option_a,
          q.option_b,
          q.option_c,
          q.option_d,
        ],
        correctAnswer: q.correct_answer,
        explanation: q.explanation,
      })) || []

    setSubjectQuestions(formattedQuestions)
  }

  fetchQuestions()
}, [subject])

 const topics = Array.from(
  new Set(
    subjectQuestions
      .map((q) => q.topic)
      .filter(Boolean)
  )
) as string[]

  const [examMode, setExamMode] = useState<ExamMode>("menu")
  const [activeTopic, setActiveTopic] = useState("")
  const [examQuestions, setExamQuestions] = useState<Question[]>([])
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0)
  const [answers, setAnswers] = useState<Record<number, string>>({})
  const [pinnedQuestions, setPinnedQuestions] = useState<number[]>([])
  const [shownAnswers, setShownAnswers] = useState<number[]>([])
  const [isSubmitted, setIsSubmitted] = useState(false)
  const [showFinishPrompt, setShowFinishPrompt] = useState(false)
  const [showStartMockPrompt, setShowStartMockPrompt] = useState(false)
  const [showMobileQuestionNav, setShowMobileQuestionNav] = useState(false)
  const [timeLeft, setTimeLeft] = useState(MOCK_TIME_SECONDS)

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
    setShowMobileQuestionNav(false)
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
    setShowStartMockPrompt(false)
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
    setShowStartMockPrompt(false)
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
      <main className="min-h-screen bg-[#06111f] px-4 py-10 text-white sm:px-6">
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
        <header className="sticky top-0 z-50 border-b border-[#1e3a5f] bg-[#06111f]/95 backdrop-blur">
          <div className="mx-auto flex min-h-20 max-w-7xl flex-col gap-4 px-4 py-4 sm:flex-row sm:items-center sm:justify-between sm:px-6 lg:px-8">
            <div>
              <p className="text-xs uppercase tracking-[0.2em] text-[#f4b400]">
                PilotVault SA
              </p>

              <h1 className="text-lg font-bold capitalize">
                {subject.replaceAll("-", " ")} Practice
              </h1>
            </div>

            <Link
              href="/practice"
              className="rounded-xl border border-[#1e3a5f] bg-[#0b1f35] px-5 py-2 text-center text-sm hover:bg-[#1e3a5f]"
            >
              Subjects
            </Link>
          </div>
        </header>

        <section className="mx-auto max-w-7xl px-4 py-8 sm:px-6 sm:py-10 lg:px-8 lg:py-12">
          <button
            onClick={() => setShowStartMockPrompt(true)}
            className="w-full rounded-3xl border border-[#f4b400]/50 bg-[#081726] p-6 text-left transition hover:-translate-y-1 hover:border-[#f4b400] sm:p-8"
          >
            <p className="text-sm uppercase tracking-wider text-[#f4b400]">
              Mock Exam
            </p>

            <h2 className="mt-3 text-2xl font-bold sm:text-3xl">
              Start Mock Exam
            </h2>

            <p className="mt-4 max-w-2xl text-sm leading-6 text-slate-300 sm:text-base">
              Simulate a SACAA-style exam with timing, question navigation,
              finish confirmation and final score.
            </p>

            <div className="mt-6 flex flex-wrap gap-3 text-sm text-slate-300">
              <span className="rounded-full border border-[#1e3a5f] px-4 py-2">
                25 minutes
              </span>

              <span className="rounded-full border border-[#1e3a5f] px-4 py-2">
                75% pass mark
              </span>
            </div>
          </button>

          <div className="mt-10">
            <p className="text-sm uppercase tracking-wider text-[#f4b400]">
              Practice by Topic
            </p>

            <h2 className="mt-3 text-2xl font-bold">
              Choose a Topic
            </h2>

            <p className="mt-3 text-sm leading-6 text-slate-300">
              Focus on weak areas and review explanations while practicing.
            </p>

            <div className="mt-6 grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
              {topics.length > 0 ? (
                topics.map((topic) => (
                  <button
                    key={topic}
                    onClick={() => startTopicPractice(topic)}
                    className="rounded-2xl border border-[#1e3a5f] bg-[#081726] p-5 text-left transition hover:-translate-y-1 hover:border-[#f4b400]"
                  >
                    <h3 className="text-lg font-bold text-white">
                      {topic}
                    </h3>
                  </button>
                ))
              ) : (
                <button
                  onClick={() => startTopicPractice("")}
                  className="rounded-2xl border border-[#1e3a5f] bg-[#081726] p-5 text-left transition hover:-translate-y-1 hover:border-[#f4b400]"
                >
                  <h3 className="text-lg font-bold text-white">
                    All Questions
                  </h3>
                </button>
              )}
            </div>
          </div>
        </section>

        {showStartMockPrompt && (
          <>
            <div className="fixed inset-0 z-50 bg-black/60 sm:hidden">
              <div className="absolute bottom-0 left-0 right-0 rounded-t-3xl bg-white p-6 text-slate-900 shadow-2xl">
                <div className="mx-auto mb-5 h-1.5 w-16 rounded-full bg-slate-300" />

                <h2 className="text-xl font-bold">Start Mock Exam</h2>

                <p className="mt-3 text-sm text-slate-600">
                  Ready to begin your SACAA mock exam?
                </p>

                <div className="mt-5 space-y-3">
                  <div className="rounded-xl bg-slate-100 p-3">
                    25 Minutes
                  </div>

                  <div className="rounded-xl bg-slate-100 p-3">
                    75% Pass Mark
                  </div>
                </div>

                <div className="mt-6 flex flex-col gap-3">
                  <button
                    onClick={startMockExam}
                    className="rounded-xl bg-[#1f4e79] py-4 font-semibold text-white hover:bg-[#183d60]"
                  >
                    Start Exam
                  </button>

                  <button
                    onClick={() => setShowStartMockPrompt(false)}
                    className="rounded-xl border border-slate-300 py-4 font-semibold text-slate-700"
                  >
                    Cancel
                  </button>
                </div>
              </div>
            </div>

            <div className="fixed inset-0 z-50 hidden items-center justify-center bg-black/60 px-4 sm:flex">
              <div className="w-full max-w-lg rounded-2xl border border-[#1e3a5f] bg-white p-6 text-slate-900 shadow-2xl">
                <h2 className="text-2xl font-bold">Start Mock Exam</h2>

                <p className="mt-4 text-slate-700">
                  You are about to start a timed mock examination.
                </p>

                <div className="mt-5 rounded-xl border border-slate-300 bg-slate-50 p-4">
                  <p className="font-semibold text-slate-900">
                    Exam Information
                  </p>

                  <ul className="mt-3 space-y-2 text-sm text-slate-700">
                    <li>Time allowed: 25 minutes</li>
                    <li>Pass mark: 75%</li>
                    <li>Navigate between questions</li>
                    <li>Score shown after finishing</li>
                  </ul>
                </div>

                <div className="mt-6 flex justify-end gap-3">
                  <button
                    onClick={() => setShowStartMockPrompt(false)}
                    className="rounded-md border border-slate-300 px-5 py-2 text-sm font-semibold hover:bg-slate-100"
                  >
                    Cancel
                  </button>

                  <button
                    onClick={startMockExam}
                    className="rounded-md bg-[#1f4e79] px-5 py-2 text-sm font-semibold text-white hover:bg-[#183d60]"
                  >
                    Start Exam
                  </button>
                </div>
              </div>
            </div>
          </>
        )}
      </main>
    )
  }

  if (isSubmitted) {
    return (
      <main className="min-h-screen bg-white text-slate-900">
        <header className="flex h-auto min-h-16 items-center justify-between gap-4 border-b border-slate-300 bg-[#1f4e79] px-4 py-4 text-white sm:px-6">
          <div>
            <h1 className="text-base font-bold">PilotVault SA Exam Results</h1>

            <p className="text-xs uppercase tracking-wider text-blue-100">
              {subject.replaceAll("-", " ")} · {examLabel}
            </p>
          </div>

          <button
            onClick={returnToMenu}
            className="rounded-md bg-white/10 px-4 py-2 text-sm hover:bg-white/20"
          >
            Exit
          </button>
        </header>

        <section className="mx-auto max-w-5xl px-4 py-8 sm:px-6 sm:py-10">
          <div className="rounded-md border border-slate-300 bg-slate-50 p-5 sm:p-6">
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
              You got {correctAnswers} out of {totalQuestions} questions
              correct.
            </p>

            <div className="mt-6 flex flex-col gap-3 sm:flex-row">
              <button
                onClick={() =>
                  examMode === "mock"
                    ? startMockExam()
                    : startTopicPractice(activeTopic)
                }
                className="rounded-md bg-[#1f4e79] px-5 py-3 text-sm font-semibold text-white hover:bg-[#183d60] sm:py-2"
              >
                Restart
              </button>

              <button
                onClick={returnToMenu}
                className="rounded-md border border-slate-300 bg-white px-5 py-3 text-sm font-semibold text-slate-700 hover:bg-slate-100 sm:py-2"
              >
                Back to Practice Modes
              </button>
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
                  const originalIndex = examQuestions.findIndex(
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

                      <p className="mt-3 leading-relaxed text-slate-700">
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

  if (!currentQuestion) {
    return (
      <main className="flex min-h-screen items-center justify-center bg-white px-4 text-slate-900">
        <div className="text-center">
          <h1 className="text-2xl font-bold">No questions found.</h1>

          <button
            onClick={returnToMenu}
            className="mt-6 inline-block rounded-md bg-[#1f4e79] px-5 py-2 text-white hover:bg-[#183d60]"
          >
            Back to Practice Modes
          </button>
        </div>
      </main>
    )
  }

  return (
    <main className="min-h-screen bg-white text-slate-900">
      <header className="flex h-auto min-h-20 flex-col gap-4 border-b border-slate-300 bg-[#1f4e79] px-4 py-4 text-white sm:flex-row sm:items-center sm:justify-between sm:px-6">
        <div>
          <h1 className="text-base font-bold">PilotVault SA Exam Practice</h1>

          <p className="text-xs uppercase tracking-wider text-blue-100">
            {subject.replaceAll("-", " ")} · {examLabel}
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

          <button
            onClick={returnToMenu}
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
                  onClick={() => setShowMobileQuestionNav(true)}
                  className="rounded-md border border-slate-300 bg-white px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-100 md:hidden"
                >
                  Questions
                </button>

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
            </div>

            <p className="text-lg leading-relaxed text-slate-900">
              {currentQuestion.question}
            </p>

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

            <div className="mt-12 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
              <button
                onClick={toggleAnswer}
                className="rounded-md border border-[#1f4e79] bg-white px-5 py-3 text-sm font-semibold text-[#1f4e79] hover:bg-blue-50 sm:py-2"
              >
                {shownAnswers.includes(currentQuestionIndex)
                  ? "Hide Answer"
                  : "Show Answer"}
              </button>

              <div className="grid grid-cols-3 gap-3 sm:flex">
                <button
                  onClick={goPrevious}
                  disabled={currentQuestionIndex === 0}
                  className="rounded-md border border-slate-300 bg-white px-4 py-3 text-sm font-medium text-slate-700 disabled:opacity-40 sm:px-5 sm:py-2"
                >
                  Previous
                </button>

                <button
                  onClick={goNext}
                  disabled={currentQuestionIndex === totalQuestions - 1}
                  className="rounded-md bg-[#1f4e79] px-4 py-3 text-sm font-semibold text-white hover:bg-[#183d60] disabled:opacity-40 sm:px-6 sm:py-2"
                >
                  Next
                </button>

                <button
                  onClick={() => setShowFinishPrompt(true)}
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
                  {totalQuestions - unansweredCount} answered / {totalQuestions}
                </p>
              </div>

              <button
                onClick={() => setShowMobileQuestionNav(false)}
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
                      setCurrentQuestionIndex(index)
                      setShowMobileQuestionNav(false)
                    }}
                    className={`relative h-11 rounded border text-sm font-medium ${
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

            <div className="mt-5 grid grid-cols-2 gap-2 text-xs text-slate-600">
              <p>Blue: current</p>
              <p>Light blue: answered</p>
              <p>Red: unanswered</p>
              <p>Yellow: answer viewed</p>
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

            <p className="mt-4 text-slate-700">
              Are you sure you want to finish and submit your answers?
            </p>

            <div className="mt-6 flex flex-col gap-3 sm:flex-row sm:justify-end">
              <button
                onClick={() => setShowFinishPrompt(false)}
                className="rounded-md border border-slate-300 bg-white px-5 py-3 text-sm font-semibold text-slate-700 hover:bg-slate-100 sm:py-2"
              >
                Return to Exam
              </button>

              <button
                onClick={() => {
                  setShowFinishPrompt(false)
                  setIsSubmitted(true)
                }}
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