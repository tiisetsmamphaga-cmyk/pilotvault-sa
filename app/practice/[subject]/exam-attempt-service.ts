import { supabase } from "@/src/lib/supabase"

export type MockExamStats = {
  averageScore: number | null
  attemptCount: number
}

type SaveMockExamAttemptInput = {
  subject: string
  totalQuestions: number
  correctAnswers: number
  scorePercentage: number
}

async function getCurrentUserId() {
  const {
    data: { user },
    error,
  } = await supabase.auth.getUser()

  if (error) {
    throw new Error(error.message)
  }

  if (!user) {
    throw new Error("You must be signed in to access exam attempts.")
  }

  return user.id
}

export async function fetchMockExamStats(
  subject: string
): Promise<MockExamStats> {
  const userId = await getCurrentUserId()
  const { data, error } = await supabase
    .from("ExamAttempts")
    .select("score_percentage")
    .eq("user_id", userId)
    .eq("subject", subject)
    .eq("exam_mode", "mock")

  if (error) {
    throw new Error(error.message)
  }

  if (!data || data.length === 0) {
    return {
      averageScore: null,
      attemptCount: 0,
    }
  }

  const scoreTotal = data.reduce(
    (total, attempt) => total + Number(attempt.score_percentage),
    0
  )

  return {
    averageScore: Math.round(scoreTotal / data.length),
    attemptCount: data.length,
  }
}

export async function saveMockExamAttempt({
  subject,
  totalQuestions,
  correctAnswers,
  scorePercentage,
}: SaveMockExamAttemptInput) {
  const userId = await getCurrentUserId()

  const { error } = await supabase.from("ExamAttempts").insert({
    user_id: userId,
    subject,
    exam_mode: "mock",
    total_questions: totalQuestions,
    correct_answers: correctAnswers,
    score_percentage: scorePercentage,
  })

  if (error) {
    throw new Error(error.message)
  }
}
