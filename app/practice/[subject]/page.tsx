"use client"

import { useEffect, useMemo, useState } from "react"
import { useParams, useRouter } from "next/navigation"
import Link from "next/link"
import {
  BookOpen,
  ClipboardList,
  Crosshair,
  GraduationCap,
} from "lucide-react"

import { supabase } from "@/src/lib/supabase"

type Question = {
  id: number
  subject: string
  topic?: string
  question: string
  image_url?: string
  options: string[]
  correctAnswer: string
  explanation: string
}

type DatabaseQuestion = {
  id: number
  subject: string
  topic: string | null
  question: string
  image_url: string | null
  option_a: string | null
  option_b: string | null
  option_c: string | null
  option_d: string | null
  correct_answer: string
  explanation: string | null
  is_trial_question: boolean | null
}

type ExamMode = "menu" | "mock" | "topics" | "topic"

const MOCK_QUESTION_COUNT = 25
const MOCK_TIME_SECONDS = 25 * 60
const PASS_MARK = 75
const SUPABASE_PAGE_SIZE = 1000

function shuffleArray<T>(array: T[]) {
  const shuffled = [...array]

  for (let index = shuffled.length - 1; index > 0; index -= 1) {
    const randomIndex = Math.floor(Math.random() * (index + 1))

    ;[shuffled[index], shuffled[randomIndex]] = [
      shuffled[randomIndex],
      shuffled[index],
    ]
  }

  return shuffled
}

function formatSubjectName(value: string) {
  return value
    .split("-")
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(" ")
}

function formatTime(seconds: number) {
  const minutes = Math.floor(seconds / 60)
  const remainingSeconds = seconds % 60

  return `${minutes}:${remainingSeconds.toString().padStart(2, "0")}`
}

async function fetchAllSubjectQuestions(
  subject: string,
  trialOnly: boolean
): Promise<DatabaseQuestion[]> {
  const allQuestions: DatabaseQuestion[] = []
  let from = 0

  while (true) {
    const to = from + SUPABASE_PAGE_SIZE - 1

    let query = supabase
      .from("questions")
      .select(
        `
          id,
          subject,
          topic,
          question,
          image_url,
          option_a,
          option_b,
          option_c,
          option_d,
          correct_answer,
          explanation,
          is_trial_question
        `
      )
      .eq("subject", subject)
      .order("id", { ascending: true })
      .range(from, to)

    if (trialOnly) {
      query = query.eq("is_trial_question", true)
    }

    const { data, error } = await query

    if (error) {
      throw new Error(error.message)
    }

    const currentPage = (data ?? []) as DatabaseQuestion[]

    allQuestions.push(...currentPage)

    if (currentPage.length < SUPABASE_PAGE_SIZE) {
      break
    }

    from += SUPABASE_PAGE_SIZE
  }

  return allQuestions
}

export default function SubjectPracticePage() {
  const params = useParams()
  const router = useRouter()
  const subject = String(params.subject)

  const [subjectQuestions, setSubjectQuestions] = useState<Question[]>([])
  const [isLoadingQuestions, setIsLoadingQuestions] = useState(true)
  const [loadingError, setLoadingError] = useState("")

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

  const [canAccessTopics, setCanAccessTopics] = useState(false)
  const [isTrialAccount, setIsTrialAccount] = useState(false)
  const [activeTopic, setActiveTopic] = useState("")

  useEffect(() => {
    let cancelled = false

    const checkUserAndFetchQuestions = async () => {
      try {
        setIsLoadingQuestions(true)
        setLoadingError("")

        const {
          data: { user },
          error: userError,
        } = await supabase.auth.getUser()

        if (userError) {
          throw new Error(userError.message)
        }

        if (!user) {
          router.push("/")
          return
        }

        const { data: profile, error: profileError } = await supabase
          .from("Profiles")
          .select(
            `
              subscription_status,
              subscription_plan,
              trial_ends_at
            `
          )
          .eq("id", user.id)
          .maybeSingle()

        if (profileError) {
          throw new Error(profileError.message)
        }

        if (!profile) {
          router.push("/upgrade")
          return
        }

        const isPplUser =
          profile.subscription_status === "active" &&
          profile.subscription_plan === "ppl"

        const isTrialUser = profile.subscription_plan === "trial"

        if (!cancelled) {
          setIsTrialAccount(isTrialUser)
          setCanAccessTopics(isPplUser)
        }

        if (isTrialUser) {
          const trialExpired =
            !profile.trial_ends_at ||
            new Date(profile.trial_ends_at) < new Date()

          if (trialExpired) {
            router.push(`/upgrade?subject=${subject}`)
            return
          }
        }

        if (!isTrialUser && !isPplUser) {
          const { data: subjectAccess, error: subjectAccessError } =
            await supabase
              .from("SubjectAccess")
              .select("access_status, expires_at")
              .eq("user_id", user.id)
              .eq("subject", subject)
              .eq("access_status", "active")
              .maybeSingle()

          if (subjectAccessError) {
            throw new Error(subjectAccessError.message)
          }

          const hasValidAccess =
            Boolean(subjectAccess) &&
            Boolean(subjectAccess?.expires_at) &&
            new Date(subjectAccess!.expires_at) > new Date()

          if (!hasValidAccess) {
            router.push(`/upgrade?subject=${subject}`)
            return
          }

          if (!cancelled) {
            setCanAccessTopics(true)
          }
        }

        const databaseQuestions = await fetchAllSubjectQuestions(
          subject,
          isTrialUser
        )

        const formattedQuestions: Question[] = databaseQuestions.map(
          (question) => ({
            id: question.id,
            subject: question.subject,
            topic: question.topic ?? undefined,
            question: question.question,
            image_url: question.image_url ?? undefined,
            options: [
              question.option_a,
              question.option_b,
              question.option_c,
              question.option_d,
            ].filter(
              (option): option is string =>
                typeof option === "string" && option.trim() !== ""
            ),
            correctAnswer: question.correct_answer,
            explanation: question.explanation ?? "",
          })
        )

        if (!cancelled) {
          setSubjectQuestions(formattedQuestions)
        }
      } catch (error) {
        console.error("Question loading error:", error)

        if (!cancelled) {
          setSubjectQuestions([])
          setLoadingError(
            error instanceof Error
              ? error.message
              : "The questions could not be loaded."
          )
        }
      } finally {
        if (!cancelled) {
          setIsLoadingQuestions(false)
        }
      }
    }

    checkUserAndFetchQuestions()

    return () => {
      cancelled = true
    }
  }, [subject, router])

  useEffect(() => {
    if (
      examMode !== "mock" ||
      isSubmitted ||
      examQuestions.length === 0
    ) {
      return
    }

    const timer = window.setInterval(() => {
      setTimeLeft((previousTime) => {
        if (previousTime <= 1) {
          window.clearInterval(timer)
          setIsSubmitted(true)

          return 0
        }

        return previousTime - 1
      })
    }, 1000)

    return () => {
      window.clearInterval(timer)
    }
  }, [examMode, isSubmitted, examQuestions.length])

  const topicQuestionCounts = useMemo(() => {
    return subjectQuestions.reduce<Record<string, number>>(
      (counts, question) => {
        if (!question.topic) {
          return counts
        }

        counts[question.topic] = (counts[question.topic] ?? 0) + 1

        return counts
      },
      {}
    )
  }, [subjectQuestions])

  const topics = useMemo(() => {
    return Object.keys(topicQuestionCounts).sort((first, second) =>
      first.localeCompare(second)
    )
  }, [topicQuestionCounts])

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

    const selectedQuestions = isTrialAccount
      ? subjectQuestions.slice(0, MOCK_QUESTION_COUNT)
      : shuffleArray(subjectQuestions).slice(0, MOCK_QUESTION_COUNT)

    setExamQuestions(selectedQuestions)
    setExamMode("mock")
    setActiveTopic("")
    setTimeLeft(MOCK_TIME_SECONDS)
  }

  const startTopicPractice = (topic: string) => {
    resetExamState()

    const topicQuestions = subjectQuestions.filter(
      (question) => question.topic === topic
    )

    setExamQuestions(shuffleArray(topicQuestions))
    setActiveTopic(topic)
    setExamMode("topic")
    setTimeLeft(MOCK_TIME_SECONDS)
  }

  const returnToMenu = () => {
    resetExamState()
    setExamMode("menu")
    setActiveTopic("")
    setExamQuestions([])
    setTimeLeft(MOCK_TIME_SECONDS)
  }

  const returnToTopics = () => {
    resetExamState()
    setExamMode("topics")
    setActiveTopic("")
    setExamQuestions([])
    setTimeLeft(MOCK_TIME_SECONDS)
  }

  const handleAnswer = (option: string) => {
    if (isSubmitted) {
      return
    }

    setAnswers((previousAnswers) => ({
      ...previousAnswers,
      [currentQuestionIndex]: option,
    }))
  }

  const togglePin = (index: number) => {
    setPinnedQuestions((previousPinnedQuestions) =>
      previousPinnedQuestions.includes(index)
        ? previousPinnedQuestions.filter((item) => item !== index)
        : [...previousPinnedQuestions, index]
    )
  }

  const toggleAnswer = () => {
    setShownAnswers((previousShownAnswers) =>
      previousShownAnswers.includes(currentQuestionIndex)
        ? previousShownAnswers.filter(
            (item) => item !== currentQuestionIndex
          )
        : [...previousShownAnswers, currentQuestionIndex]
    )
  }

  const goPrevious = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex((previousIndex) => previousIndex - 1)
    }
  }

  const goNext = () => {
    if (currentQuestionIndex < examQuestions.length - 1) {
      setCurrentQuestionIndex((previousIndex) => previousIndex + 1)
    }
  }

  const currentQuestion = examQuestions[currentQuestionIndex]
  const selectedAnswer = answers[currentQuestionIndex]
  const totalQuestions = examQuestions.length

  const answeredCount = Object.keys(answers).length
  const unansweredCount = totalQuestions - answeredCount

  const correctAnswers = examQuestions.filter(
    (question, index) => answers[index] === question.correctAnswer
  ).length

  const scorePercentage =
    totalQuestions > 0
      ? Math.round((correctAnswers / totalQuestions) * 100)
      : 0

  const passed = scorePercentage >= PASS_MARK

  const wrongQuestions = examQuestions.filter(
    (question, index) => answers[index] !== question.correctAnswer
  )

  const examLabel =
    examMode === "topic" && activeTopic
      ? `${activeTopic} Practice`
      : "Mock Exam"

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

  if (loadingError) {
    return (
      <main className="min-h-screen bg-[#06111f] px-4 py-10 text-white sm:px-6">
        <div className="mx-auto max-w-4xl">
          <Link
            href="/dashboard"
            className="text-sm font-medium text-[#f4b400] hover:text-white"
          >
            ← Back to Dashboard
          </Link>

          <div className="mt-8 rounded-3xl border border-red-500/30 bg-[#081726] p-8">
            <p className="text-xs uppercase tracking-[0.25em] text-red-400">
              Loading Error
            </p>

            <h1 className="mt-3 text-3xl font-bold">
              Questions could not be loaded.
            </h1>

            <p className="mt-3 text-gray-400">{loadingError}</p>
          </div>
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
              No Questions
            </p>

            <h1 className="mt-3 text-3xl font-bold">
              No questions found for {formatSubjectName(subject)}.
            </h1>

            <p className="mt-3 text-gray-400">
              Make sure the subject slug matches the subject value stored
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
              Start a SACAA-style mock exam or focus on weak areas with
              topic-based practice.
            </p>

            {!isTrialAccount && (
              <p className="mt-4 text-sm font-semibold text-[#f4b400]">
                {subjectQuestions.length} questions available
              </p>
            )}
          </div>

          <div className="mt-8 grid gap-5 md:grid-cols-2">
            <button
              onClick={startMockExam}
              className="group cursor-pointer rounded-2xl border border-[#1e3a5f] bg-gradient-to-br from-[#081726] to-[#06111f] p-4 text-left shadow-2xl transition-all hover:-translate-y-1 hover:border-[#f4b400] hover:shadow-[0_0_30px_rgba(244,180,0,0.12)]"
            >
              <div className="inline-flex items-center gap-2 rounded-md border border-[#1e3a5f] bg-white/5 px-3 py-1 text-[10px] font-bold uppercase tracking-wider text-[#f4b400]">
                <GraduationCap size={14} />
                {isTrialAccount ? "Trial Access" : "Full Access"}
              </div>

              <div className="mt-4 flex items-center justify-between gap-5">
                <div className="flex items-start gap-4">
                  <div className="rounded-xl border border-[#1e3a5f] bg-[#0b1d31] p-3 text-[#9bb7ff]">
                    <ClipboardList size={28} />
                  </div>

                  <div>
                    <h2 className="text-xl font-bold text-white">
                      Mock Exam
                    </h2>

                    <p className="mt-2 max-w-sm text-sm leading-6 text-gray-400">
                      {isTrialAccount
                        ? "25 fixed SACAA-style trial questions for exam practice."
                        : "25 randomized SACAA-style questions from the full question bank."}
                    </p>
                  </div>
                </div>

                <div className="hidden h-24 w-24 shrink-0 items-center justify-center rounded-full border border-[#1e3a5f] bg-[#06111f] md:flex">
                  <div className="text-center">
                    <p className="text-3xl font-bold text-white">
                      {Math.min(
                        MOCK_QUESTION_COUNT,
                        subjectQuestions.length
                      )}
                    </p>

                    <p className="text-[10px] uppercase tracking-widest text-gray-400">
                      Questions
                    </p>
                  </div>
                </div>
              </div>
            </button>

            {canAccessTopics ? (
              <button
                onClick={() => setExamMode("topics")}
                className="group cursor-pointer rounded-2xl border border-[#1e3a5f] bg-gradient-to-br from-[#081726] to-[#06111f] p-4 text-left shadow-2xl transition-all hover:-translate-y-1 hover:border-[#f4b400] hover:shadow-[0_0_30px_rgba(244,180,0,0.12)]"
              >
                <div className="inline-flex items-center gap-2 rounded-md border border-[#1e3a5f] bg-white/5 px-3 py-1 text-[10px] font-bold uppercase tracking-wider text-[#f4b400]">
                  <Crosshair size={14} />
                  Full Access
                </div>

                <div className="mt-4 flex items-center justify-between gap-5">
                  <div className="flex items-start gap-4">
                    <div className="rounded-xl border border-[#1e3a5f] bg-[#0b1d31] p-3 text-[#9bb7ff]">
                      <BookOpen size={28} />
                    </div>

                    <div>
                      <h2 className="text-xl font-bold text-white">
                        Practice by Topic
                      </h2>

                      <p className="mt-2 max-w-sm text-sm leading-6 text-gray-400">
                        Practice every available question from a selected
                        topic with no question cap.
                      </p>
                    </div>
                  </div>

                  <div className="hidden h-24 w-24 shrink-0 items-center justify-center rounded-full border border-[#1e3a5f] bg-[#06111f] text-[#f4b400] md:flex">
                    <Crosshair size={38} />
                  </div>
                </div>
              </button>
            ) : (
              <Link
                href={`/upgrade?subject=${subject}`}
                className="group cursor-pointer rounded-2xl border border-[#1e3a5f] bg-[#081726]/60 p-4 text-left opacity-75 transition-all hover:-translate-y-1 hover:border-[#f4b400]"
              >
                <p className="text-xs uppercase tracking-[0.25em] text-[#f4b400]">
                  Subscription Feature
                </p>

                <h2 className="mt-3 text-xl font-bold text-white">
                  Practice by Topic
                </h2>

                <p className="mt-2 text-sm leading-6 text-gray-400">
                  Target weak areas by topic using the full PilotVault
                  question bank.
                </p>
              </Link>
            )}
          </div>
        </div>
      </main>
    )
  }

  if (examMode === "topics") {
    return (
      <main className="min-h-screen bg-[#06111f] px-4 py-10 text-white sm:px-6">
        <div className="mx-auto max-w-5xl">
          <button
            onClick={returnToMenu}
            className="text-sm font-medium text-[#f4b400] hover:text-white"
          >
            ← Back to Training Modes
          </button>

          <div className="mt-8 rounded-3xl border border-[#1e3a5f] bg-[#081726] p-6 sm:p-8">
            <p className="text-xs uppercase tracking-[0.25em] text-[#f4b400]">
              {formatSubjectName(subject)}
            </p>

            <h1 className="mt-3 text-3xl font-bold sm:text-4xl">
              Choose a topic
            </h1>

            <p className="mt-3 max-w-2xl text-gray-400">
              Every available question from the selected topic will be
              loaded.
            </p>
          </div>

          <div className="mt-8 grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
            {topics.map((topic) => (
              <button
                key={topic}
                onClick={() => startTopicPractice(topic)}
                className="group rounded-2xl border border-[#1e3a5f] bg-[#081726] p-6 text-left transition-all hover:-translate-y-1 hover:border-[#f4b400]"
              >
                <h2 className="text-xl font-bold text-white">{topic}</h2>

                <p className="mt-3 text-sm text-gray-400">
                  {topicQuestionCounts[topic]} question
                  {topicQuestionCounts[topic] === 1 ? "" : "s"} available
                </p>

                <p className="mt-5 text-sm font-medium text-[#f4b400] transition group-hover:text-[#ffd24d]">
                  Practice All Questions →
                </p>
              </button>
            ))}
          </div>
        </div>
      </main>
    )
  }

  if (isSubmitted) {
    return (
      <main className="min-h-screen bg-white text-slate-900">
        <header className="flex min-h-16 items-center justify-between border-b border-slate-300 bg-[#1f4e79] px-4 py-4 text-white sm:px-6">
          <div>
            <h1 className="text-base font-bold">
              PilotVault SA Exam Results
            </h1>

            <p className="text-xs uppercase tracking-wider text-blue-100">
              {formatSubjectName(subject)} · {examLabel}
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
                onClick={
                  examMode === "topic"
                    ? returnToTopics
                    : startMockExam
                }
                className="rounded-md bg-[#1f4e79] px-5 py-3 text-sm font-semibold text-white hover:bg-[#183d60] sm:py-2"
              >
                {examMode === "topic"
                  ? "Back to Topics"
                  : "Restart"}
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

                      <p className="mt-3 whitespace-pre-line leading-relaxed text-slate-700">
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
      <header className="flex min-h-20 flex-col gap-4 border-b border-slate-300 bg-[#1f4e79] px-4 py-4 text-white sm:flex-row sm:items-center sm:justify-between sm:px-6">
        <div>
          <h1 className="text-base font-bold">
            PilotVault SA Exam Practice
          </h1>

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
            onClick={returnToMenu}
            className="rounded-md bg-white/10 px-4 py-2 text-sm hover:bg-white/20"
          >
            Exit
          </button>
        </div>
      </header>

      <div className="flex min-h-[calc(100vh-80px)]">
        <aside className="hidden w-64 border-r border-slate-300 bg-slate-100 p-4 md:block">
          <h2 className="mb-4 font-semibold text-slate-700">
            Questions
          </h2>

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
                  Question {currentQuestionIndex + 1} of{" "}
                  {totalQuestions}
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
                      onChange={() => handleAnswer(option)}
                      className="h-5 w-5 accent-[#1f4e79]"
                    />

                    <span className="font-semibold">{letter}.</span>

                    <span>{option}</span>
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

                <p className="mt-2 whitespace-pre-line leading-relaxed text-slate-700">
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
                  disabled={
                    currentQuestionIndex === totalQuestions - 1
                  }
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
                  {answeredCount} answered / {totalQuestions}
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
                const hasShownAnswer =
                  shownAnswers.includes(index)

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
              You are about to submit your examination. Once submitted,
              your answers cannot be changed.
            </p>

            {unansweredCount > 0 && (
              <p className="mt-4 font-semibold text-red-700">
                You have {unansweredCount} unanswered question
                {unansweredCount === 1 ? "" : "s"}.
              </p>
            )}

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