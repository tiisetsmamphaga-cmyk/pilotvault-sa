export const MOCK_QUESTION_COUNT = 25
export const MOCK_TIME_SECONDS = 25 * 60
export const PASS_MARK = 75

// Question counts a student can pick for a mock exam. Trial accounts always
// get the fixed 25-question trial set.
export const MOCK_QUESTION_COUNT_OPTIONS = [10, 20, 25, 30, 40]

// A timed mock allows one minute per question (25 questions = 25 minutes).
export const SECONDS_PER_MOCK_QUESTION = MOCK_TIME_SECONDS / MOCK_QUESTION_COUNT

export function getMockTimeLimitSeconds(questionCount: number) {
  return questionCount * SECONDS_PER_MOCK_QUESTION
}

export function shuffleArray<T>(array: T[]) {
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

export function formatSubjectName(value: string) {
  return value
    .split("-")
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(" ")
}

export function formatTime(seconds: number) {
  const minutes = Math.floor(seconds / 60)
  const remainingSeconds = seconds % 60

  return `${minutes}:${remainingSeconds.toString().padStart(2, "0")}`
}

export function getReadinessStatus(averageScore: number | null) {
  if (averageScore === null) {
    return {
      label: "No attempts yet",
      className: "text-[#8fa7c2]",
    }
  }

  if (averageScore >= 85) {
    return {
      label: "Highly ready",
      className: "text-emerald-600",
    }
  }

  if (averageScore >= PASS_MARK) {
    return {
      label: "Exam ready",
      className: "text-emerald-600",
    }
  }

  if (averageScore >= 60) {
    return {
      label: "Almost ready",
      className: "text-[#f4b400]",
    }
  }

  return {
    label: "Keep practising",
    className: "text-[#b8860a]",
  }
}
