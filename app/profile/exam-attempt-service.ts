import { supabase } from "@/src/lib/supabase"

export type MockExamAttempt = {
  id: number
  subject: string
  totalQuestions: number
  correctAnswers: number
  scorePercentage: number
  completedAt: string
  durationSeconds: number | null
}

export async function fetchMockExamAttempts(
  userId: string
): Promise<MockExamAttempt[]> {
  const { data, error } = await supabase
    .from("ExamAttempts")
    .select(
      "id, subject, total_questions, correct_answers, score_percentage, completed_at, duration_seconds"
    )
    .eq("user_id", userId)
    .eq("exam_mode", "mock")
    .order("completed_at", { ascending: false })
    .limit(100)

  if (error) {
    throw new Error(error.message)
  }

  return (data ?? []).map((attempt) => ({
    id: Number(attempt.id),
    subject: String(attempt.subject),
    totalQuestions: Number(attempt.total_questions),
    correctAnswers: Number(attempt.correct_answers),
    scorePercentage: Number(attempt.score_percentage),
    completedAt: String(attempt.completed_at),
    durationSeconds:
      attempt.duration_seconds === null
        ? null
        : Number(attempt.duration_seconds),
  }))
}
