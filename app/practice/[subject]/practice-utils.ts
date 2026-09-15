export const MOCK_QUESTION_COUNT = 25
export const MOCK_TIME_SECONDS = 25 * 60
export const PASS_MARK = 75

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
    className: "text-orange-500",
  }
}
