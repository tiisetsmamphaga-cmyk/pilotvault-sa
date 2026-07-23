"use client"

import { useEffect, useMemo, useRef, useState } from "react"
import Link from "next/link"
import { useParams, useRouter } from "next/navigation"

import { PageSkeleton } from "@/components/page-skeleton"
import {
  getCachedCurrentUser,
  getCachedProfile,
  getCachedSubjectAccess,
} from "@/src/lib/client-data-cache"

import { ExamResults } from "./components/exam-results"
import { ExamSimulator } from "./components/exam-simulator"
import { TopicSelection } from "./components/topic-selection"
import { TrainingModeMenu } from "./components/training-mode-menu"
import {
  fetchMockExamStats,
  saveMockExamAttempt,
} from "./exam-attempt-service"
import type { MockExamStats } from "./exam-attempt-service"
import {
  MOCK_QUESTION_COUNT,
  MOCK_TIME_SECONDS,
  PASS_MARK,
  formatSubjectName,
  shuffleArray,
} from "./practice-utils"
import { fetchSubjectQuestions } from "./question-service"
import type { ExamAnswers, ExamMode, Question } from "./types"

const EMPTY_MOCK_EXAM_STATS: MockExamStats = {
  averageScore: null,
  attemptCount: 0,
}

export default function SubjectPracticePage() {
  const params = useParams<{ subject: string }>()
  const router = useRouter()
  const subject = String(params.subject)

  const [subjectQuestions, setSubjectQuestions] = useState<Question[]>([])
  const [isLoadingQuestions, setIsLoadingQuestions] = useState(true)
  const [isRedirecting, setIsRedirecting] = useState(false)
  const [loadingError, setLoadingError] = useState("")

  const [examMode, setExamMode] = useState<ExamMode>("menu")
  const [examQuestions, setExamQuestions] = useState<Question[]>([])
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0)

  const [answers, setAnswers] = useState<ExamAnswers>({})
  const [pinnedQuestions, setPinnedQuestions] = useState<number[]>([])
  const [shownAnswers, setShownAnswers] = useState<number[]>([])

  const [isSubmitted, setIsSubmitted] = useState(false)
  const [showFinishPrompt, setShowFinishPrompt] = useState(false)
  const [showMobileQuestionNav, setShowMobileQuestionNav] = useState(false)

  const [timeLeft, setTimeLeft] = useState(MOCK_TIME_SECONDS)

  const [canAccessTopics, setCanAccessTopics] = useState(false)
  const [isTrialAccount, setIsTrialAccount] = useState(false)
  const [mockExamStats, setMockExamStats] = useState<MockExamStats>(
    EMPTY_MOCK_EXAM_STATS
  )
  const [activeTopic, setActiveTopic] = useState("")
  const attemptSavedRef = useRef(false)

  useEffect(() => {
    let cancelled = false

    const redirectTo = (href: string) => {
      if (!cancelled) {
        setIsRedirecting(true)
      }
      router.replace(href)
    }

    const checkUserAndFetchQuestions = async () => {
      try {
        setIsLoadingQuestions(true)
        setIsRedirecting(false)
        setLoadingError("")
        setMockExamStats(EMPTY_MOCK_EXAM_STATS)

        const user = await getCachedCurrentUser()

        if (!user) {
          redirectTo("/")
          return
        }

        const profile = await getCachedProfile(user.id)

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
            redirectTo(`/upgrade?subject=${subject}`)
            return
          }
        }

        if (!isTrialUser && !isPplUser) {
          const accessData = await getCachedSubjectAccess(user.id)
          const subjectAccess = accessData.find(
            (access) =>
              access.subject === subject &&
              access.access_status === "active"
          )

          const hasValidAccess =
            Boolean(subjectAccess?.expires_at) &&
            new Date(subjectAccess!.expires_at) > new Date()

          if (!hasValidAccess) {
            redirectTo(`/upgrade?subject=${subject}`)
            return
          }

          if (!cancelled) {
            setCanAccessTopics(true)
          }
        }

        const [questions, examStats] = await Promise.all([
          fetchSubjectQuestions(subject, isTrialUser),
          fetchMockExamStats(subject).catch((error) => {
            console.error("Mock exam stats loading error:", error)
            return EMPTY_MOCK_EXAM_STATS
          }),
        ])

        if (!cancelled) {
          setSubjectQuestions(questions)
          setMockExamStats(examStats)
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
    attemptSavedRef.current = false
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
  const totalQuestions = examQuestions.length

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

  useEffect(() => {
    if (
      !isSubmitted ||
      examMode !== "mock" ||
      totalQuestions === 0 ||
      attemptSavedRef.current
    ) {
      return
    }

    attemptSavedRef.current = true

    void saveMockExamAttempt({
      subject,
      totalQuestions,
      correctAnswers,
      scorePercentage,
    })
      .then(() => fetchMockExamStats(subject))
      .then(setMockExamStats)
      .catch((error) => {
        console.error("Exam attempt save error:", error)
      })
  }, [
    correctAnswers,
    examMode,
    isSubmitted,
    scorePercentage,
    subject,
    totalQuestions,
  ])

  if (isLoadingQuestions || isRedirecting) {
    return <PageSkeleton variant="practice" />
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
              Make sure the subject slug matches the subject value stored in
              Supabase.
            </p>
          </div>
        </div>
      </main>
    )
  }

  if (examMode === "menu") {
    return (
      <TrainingModeMenu
        subject={subject}
        questionCount={subjectQuestions.length}
        isTrialAccount={isTrialAccount}
        canAccessTopics={canAccessTopics}
        mockAverageScore={mockExamStats.averageScore}
        mockAttemptCount={mockExamStats.attemptCount}
        onStartMock={startMockExam}
        onOpenTopics={() => setExamMode("topics")}
      />
    )
  }

  if (examMode === "topics") {
    return (
      <TopicSelection
        subject={subject}
        topics={topics}
        topicQuestionCounts={topicQuestionCounts}
        onBack={returnToMenu}
        onStartTopic={startTopicPractice}
      />
    )
  }

  if (isSubmitted) {
    return (
      <ExamResults
        subject={subject}
        examLabel={examLabel}
        examMode={examMode}
        scorePercentage={scorePercentage}
        passed={passed}
        correctAnswers={correctAnswers}
        totalQuestions={totalQuestions}
        wrongQuestions={wrongQuestions}
        examQuestions={examQuestions}
        answers={answers}
        onReturnToMenu={returnToMenu}
        onReturnToTopics={returnToTopics}
        onRestartMock={startMockExam}
      />
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
    <ExamSimulator
      subject={subject}
      examLabel={examLabel}
      examMode={examMode}
      timeLeft={timeLeft}
      currentQuestion={currentQuestion}
      currentQuestionIndex={currentQuestionIndex}
      examQuestions={examQuestions}
      answers={answers}
      pinnedQuestions={pinnedQuestions}
      shownAnswers={shownAnswers}
      showMobileQuestionNav={showMobileQuestionNav}
      showFinishPrompt={showFinishPrompt}
      onExit={returnToMenu}
      onSelectQuestion={setCurrentQuestionIndex}
      onOpenMobileQuestionNav={() => setShowMobileQuestionNav(true)}
      onCloseMobileQuestionNav={() => setShowMobileQuestionNav(false)}
      onTogglePin={togglePin}
      onAnswer={handleAnswer}
      onToggleAnswer={toggleAnswer}
      onPrevious={goPrevious}
      onNext={goNext}
      onOpenFinishPrompt={() => setShowFinishPrompt(true)}
      onCloseFinishPrompt={() => setShowFinishPrompt(false)}
      onSubmit={() => {
        setShowFinishPrompt(false)
        setIsSubmitted(true)
      }}
    />
  )
}
