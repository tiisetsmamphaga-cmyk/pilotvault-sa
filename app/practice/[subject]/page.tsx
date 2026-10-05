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
  MOCK_QUESTION_COUNT_OPTIONS,
  MOCK_TIME_SECONDS,
  PASS_MARK,
  formatSubjectName,
  getMockTimeLimitSeconds,
  shuffleArray,
} from "./practice-utils"
import { fetchSubjectQuestions } from "./question-service"
import type { ExamAnswers, ExamMode, MockSettings, Question } from "./types"

const EMPTY_MOCK_EXAM_STATS: MockExamStats = {
  averageScore: null,
  attemptCount: 0,
}

const SAVED_MOCK_ATTEMPT_VERSION = 2
const MAX_MOCK_TIME_SECONDS = getMockTimeLimitSeconds(
  Math.max(...MOCK_QUESTION_COUNT_OPTIONS)
)
const MOCK_SETTINGS_KEY = "pilotvault:mock-settings"

const DEFAULT_MOCK_SETTINGS: MockSettings = {
  questionCount: MOCK_QUESTION_COUNT,
  timed: true,
  showAnswerButton: true,
}

type SavedMockAttempt = {
  version: number
  subject: string
  questionIds: number[]
  currentQuestionIndex: number
  answers: ExamAnswers
  pinnedQuestions: number[]
  shownAnswers: number[]
  // Seconds left on a timed exam. Unused when timeLimit is null (untimed).
  timeLeft: number
  // Total seconds allowed, or null for an untimed exam.
  timeLimit: number | null
  elapsedSeconds: number
  showAnswerButton: boolean
}

type SavedMockAttemptSummary = {
  answeredCount: number
  totalQuestions: number
  // null for an untimed exam.
  timeLeft: number | null
}

function readMockSettings(): MockSettings {
  try {
    const raw = window.localStorage.getItem(MOCK_SETTINGS_KEY)
    if (!raw) return DEFAULT_MOCK_SETTINGS

    const parsed = JSON.parse(raw) as Partial<MockSettings>

    return {
      questionCount: MOCK_QUESTION_COUNT_OPTIONS.includes(
        Number(parsed.questionCount)
      )
        ? Number(parsed.questionCount)
        : DEFAULT_MOCK_SETTINGS.questionCount,
      timed:
        typeof parsed.timed === "boolean"
          ? parsed.timed
          : DEFAULT_MOCK_SETTINGS.timed,
      showAnswerButton:
        typeof parsed.showAnswerButton === "boolean"
          ? parsed.showAnswerButton
          : DEFAULT_MOCK_SETTINGS.showAnswerButton,
    }
  } catch {
    return DEFAULT_MOCK_SETTINGS
  }
}

function writeMockSettings(settings: MockSettings) {
  try {
    window.localStorage.setItem(MOCK_SETTINGS_KEY, JSON.stringify(settings))
  } catch {
    // Remembering the choice is a convenience only.
  }
}

function getSavedMockAttemptKey(subject: string) {
  return `pilotvault:mock-attempt:${subject}`
}

function removeSavedMockAttempt(subject: string) {
  try {
    window.localStorage.removeItem(getSavedMockAttemptKey(subject))
  } catch (error) {
    console.error("Saved mock attempt removal error:", error)
  }
}

function readSavedMockAttempt(subject: string): SavedMockAttempt | null {
  try {
    const rawAttempt = window.localStorage.getItem(
      getSavedMockAttemptKey(subject)
    )

    if (!rawAttempt) {
      return null
    }

    const parsedAttempt = JSON.parse(rawAttempt) as Partial<SavedMockAttempt>
    const answers = parsedAttempt.answers

    // Attempts saved before the mock settings existed were always timed at
    // 25 minutes with the Show Answer button.
    if (parsedAttempt.version === 1) {
      parsedAttempt.version = SAVED_MOCK_ATTEMPT_VERSION
      parsedAttempt.timeLimit = MOCK_TIME_SECONDS
      parsedAttempt.elapsedSeconds =
        MOCK_TIME_SECONDS - Number(parsedAttempt.timeLeft ?? 0)
      parsedAttempt.showAnswerButton = true
    }

    const timeLimit = parsedAttempt.timeLimit
    const timeIsValid =
      timeLimit === null
        ? true
        : typeof timeLimit === "number" &&
          timeLimit > 0 &&
          timeLimit <= MAX_MOCK_TIME_SECONDS &&
          typeof parsedAttempt.timeLeft === "number" &&
          parsedAttempt.timeLeft > 0 &&
          parsedAttempt.timeLeft <= timeLimit

    const isValid =
      parsedAttempt.version === SAVED_MOCK_ATTEMPT_VERSION &&
      parsedAttempt.subject === subject &&
      Array.isArray(parsedAttempt.questionIds) &&
      parsedAttempt.questionIds.length > 0 &&
      parsedAttempt.questionIds.every((id) => Number.isInteger(id)) &&
      typeof parsedAttempt.currentQuestionIndex === "number" &&
      Number.isInteger(parsedAttempt.currentQuestionIndex) &&
      parsedAttempt.currentQuestionIndex >= 0 &&
      answers !== null &&
      typeof answers === "object" &&
      !Array.isArray(answers) &&
      Object.values(answers).every((answer) => typeof answer === "string") &&
      Array.isArray(parsedAttempt.pinnedQuestions) &&
      parsedAttempt.pinnedQuestions.every((index) => Number.isInteger(index)) &&
      Array.isArray(parsedAttempt.shownAnswers) &&
      parsedAttempt.shownAnswers.every((index) => Number.isInteger(index)) &&
      typeof parsedAttempt.timeLeft === "number" &&
      typeof parsedAttempt.elapsedSeconds === "number" &&
      parsedAttempt.elapsedSeconds >= 0 &&
      typeof parsedAttempt.showAnswerButton === "boolean" &&
      timeIsValid

    if (!isValid) {
      removeSavedMockAttempt(subject)
      return null
    }

    return parsedAttempt as SavedMockAttempt
  } catch (error) {
    console.error("Saved mock attempt loading error:", error)
    removeSavedMockAttempt(subject)
    return null
  }
}

function getSavedMockAttemptSummary(
  attempt: SavedMockAttempt
): SavedMockAttemptSummary {
  return {
    answeredCount: Object.keys(attempt.answers).length,
    totalQuestions: attempt.questionIds.length,
    timeLeft: attempt.timeLimit === null ? null : attempt.timeLeft,
  }
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
  // Seconds allowed for the current mock, or null when it is untimed.
  const [timeLimit, setTimeLimit] = useState<number | null>(MOCK_TIME_SECONDS)
  const [elapsedSeconds, setElapsedSeconds] = useState(0)
  const [showAnswerButton, setShowAnswerButton] = useState(true)
  const [mockSettings, setMockSettings] = useState<MockSettings>(
    DEFAULT_MOCK_SETTINGS
  )

  const [canAccessTopics, setCanAccessTopics] = useState(false)
  const [isTrialAccount, setIsTrialAccount] = useState(false)
  const [mockExamStats, setMockExamStats] = useState<MockExamStats>(
    EMPTY_MOCK_EXAM_STATS
  )
  const [activeTopic, setActiveTopic] = useState("")
  const [savedMockAttemptSummary, setSavedMockAttemptSummary] =
    useState<SavedMockAttemptSummary | null>(null)
  const [isMockAttemptStorageReady, setIsMockAttemptStorageReady] =
    useState(false)
  const attemptSavedRef = useRef(false)
  const mockStartedAtRef = useRef<number | null>(null)

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
    setIsMockAttemptStorageReady(false)

    const savedAttempt = readSavedMockAttempt(subject)

    setSavedMockAttemptSummary(
      savedAttempt ? getSavedMockAttemptSummary(savedAttempt) : null
    )
    setMockSettings(readMockSettings())
    setIsMockAttemptStorageReady(true)
  }, [subject])

  useEffect(() => {
    const referenceImageUrls = Array.from(
      new Set(
        subjectQuestions
          .map((question) => question.image_url)
          .filter((imageUrl): imageUrl is string => Boolean(imageUrl))
      )
    ).slice(0, 24)

    const preloadedImages = referenceImageUrls.map((imageUrl) => {
      const image = new window.Image()
      image.decoding = "async"
      image.src = imageUrl
      return image
    })

    return () => {
      preloadedImages.forEach((image) => {
        image.onload = null
        image.onerror = null
      })
    }
  }, [subjectQuestions])

  useEffect(() => {
    if (!isMockAttemptStorageReady || examMode !== "mock") {
      return
    }

    if (isSubmitted) {
      removeSavedMockAttempt(subject)
      setSavedMockAttemptSummary(null)
      return
    }

    if (examQuestions.length === 0) {
      return
    }

    const savedAttempt: SavedMockAttempt = {
      version: SAVED_MOCK_ATTEMPT_VERSION,
      subject,
      questionIds: examQuestions.map((question) => question.id),
      currentQuestionIndex,
      answers,
      pinnedQuestions,
      shownAnswers,
      timeLeft,
      timeLimit,
      elapsedSeconds,
      showAnswerButton,
    }

    try {
      window.localStorage.setItem(
        getSavedMockAttemptKey(subject),
        JSON.stringify(savedAttempt)
      )
      setSavedMockAttemptSummary(getSavedMockAttemptSummary(savedAttempt))
    } catch (error) {
      console.error("Mock attempt save error:", error)
    }
  }, [
    answers,
    currentQuestionIndex,
    examMode,
    examQuestions,
    isMockAttemptStorageReady,
    isSubmitted,
    pinnedQuestions,
    shownAnswers,
    subject,
    timeLeft,
    timeLimit,
    elapsedSeconds,
    showAnswerButton,
  ])

  useEffect(() => {
    if (
      examMode !== "mock" ||
      isSubmitted ||
      examQuestions.length === 0
    ) {
      return
    }

    if (timeLimit === null) {
      // Untimed: count up so the student can see how long they have spent.
      const stopwatch = window.setInterval(() => {
        setElapsedSeconds((previousSeconds) => previousSeconds + 1)
      }, 1000)

      return () => {
        window.clearInterval(stopwatch)
      }
    }

    const timer = window.setInterval(() => {
      setElapsedSeconds((previousSeconds) => previousSeconds + 1)
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
  }, [examMode, isSubmitted, examQuestions.length, timeLimit])

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
    mockStartedAtRef.current = null
    setCurrentQuestionIndex(0)
    setAnswers({})
    setPinnedQuestions([])
    setShownAnswers([])
    setIsSubmitted(false)
    setShowFinishPrompt(false)
    setShowMobileQuestionNav(false)
  }

  const startMockExam = (settings: MockSettings = mockSettings) => {
    removeSavedMockAttempt(subject)
    setSavedMockAttemptSummary(null)
    resetExamState()

    // Trial accounts always get the fixed 25-question trial set.
    const questionCount = isTrialAccount
      ? MOCK_QUESTION_COUNT
      : settings.questionCount
    const selectedQuestions = isTrialAccount
      ? subjectQuestions.slice(0, questionCount)
      : shuffleArray(subjectQuestions).slice(0, questionCount)
    const limit = settings.timed
      ? getMockTimeLimitSeconds(selectedQuestions.length)
      : null

    setMockSettings(settings)
    writeMockSettings(settings)
    setExamQuestions(selectedQuestions)
    setExamMode("mock")
    setActiveTopic("")
    setTimeLimit(limit)
    setTimeLeft(limit ?? 0)
    setElapsedSeconds(0)
    setShowAnswerButton(settings.showAnswerButton)
    mockStartedAtRef.current = Date.now()
  }

  const resumeMockExam = () => {
    const savedAttempt = readSavedMockAttempt(subject)

    if (!savedAttempt) {
      setSavedMockAttemptSummary(null)
      startMockExam()
      return
    }

    const questionsById = new Map(
      subjectQuestions.map((question) => [question.id, question])
    )
    const restoredQuestions = savedAttempt.questionIds
      .map((id) => questionsById.get(id))
      .filter((question): question is Question => Boolean(question))

    if (restoredQuestions.length !== savedAttempt.questionIds.length) {
      removeSavedMockAttempt(subject)
      setSavedMockAttemptSummary(null)
      startMockExam()
      return
    }

    const restoredLimit = savedAttempt.timeLimit
    const restoredTime =
      restoredLimit === null
        ? 0
        : Math.max(1, Math.min(restoredLimit, savedAttempt.timeLeft))
    const restoredElapsed =
      restoredLimit === null
        ? savedAttempt.elapsedSeconds
        : restoredLimit - restoredTime
    const restoredIndex = Math.min(
      savedAttempt.currentQuestionIndex,
      restoredQuestions.length - 1
    )

    resetExamState()
    setExamQuestions(restoredQuestions)
    setCurrentQuestionIndex(restoredIndex)
    setAnswers(savedAttempt.answers)
    setPinnedQuestions(savedAttempt.pinnedQuestions)
    setShownAnswers(savedAttempt.shownAnswers)
    setExamMode("mock")
    setActiveTopic("")
    setTimeLimit(restoredLimit)
    setTimeLeft(restoredTime)
    setElapsedSeconds(restoredElapsed)
    setShowAnswerButton(savedAttempt.showAnswerButton)
    mockStartedAtRef.current = Date.now() - restoredElapsed * 1000
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
    setShowAnswerButton(true)
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
    const measuredSeconds =
      mockStartedAtRef.current === null
        ? elapsedSeconds
        : Math.max(
            0,
            Math.round((Date.now() - mockStartedAtRef.current) / 1000)
          )
    const durationSeconds =
      timeLimit === null ? measuredSeconds : Math.min(timeLimit, measuredSeconds)

    void saveMockExamAttempt({
      subject,
      totalQuestions,
      correctAnswers,
      scorePercentage,
      durationSeconds,
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
        savedMockAttempt={savedMockAttemptSummary}
        mockSettings={mockSettings}
        onStartMock={startMockExam}
        onContinueMock={resumeMockExam}
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
        onRestartMock={() => startMockExam()}
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
      timeLimit={timeLimit}
      elapsedSeconds={elapsedSeconds}
      showAnswerButton={showAnswerButton}
      currentQuestion={currentQuestion}
      currentQuestionIndex={currentQuestionIndex}
      examQuestions={examQuestions}
      answers={answers}
      pinnedQuestions={pinnedQuestions}
      shownAnswers={shownAnswers}
      showMobileQuestionNav={showMobileQuestionNav}
      showFinishPrompt={showFinishPrompt}
      onExit={examMode === "topic" ? returnToTopics : returnToMenu}
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
