import { supabase } from "@/src/lib/supabase"

type SaveMockExamAttemptInput = {
  subject: string
  totalQuestions: number
  correctAnswers: number
  scorePercentage: number
}

export async function saveMockExamAttempt({
  subject,
  totalQuestions,
  correctAnswers,
  scorePercentage,
}: SaveMockExamAttemptInput) {
  const {
    data: { user },
    error: userError,
  } = await supabase.auth.getUser()

  if (userError) {
    throw new Error(userError.message)
  }

  if (!user) {
    throw new Error("You must be signed in to save an exam attempt.")
  }

  const { error } = await supabase.from("ExamAttempts").insert({
    user_id: user.id,
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
