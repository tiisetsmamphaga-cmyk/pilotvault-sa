import { supabase } from "@/src/lib/supabase"

import type { DatabaseQuestion, Question } from "./types"

const SUPABASE_PAGE_SIZE = 1000
const questionRequests = new Map<string, Promise<Question[]>>()

async function loadSubjectQuestions(
  subject: string,
  trialOnly: boolean
): Promise<Question[]> {
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

  return allQuestions.map((question) => ({
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
  }))
}

export async function fetchSubjectQuestions(
  subject: string,
  trialOnly: boolean
): Promise<Question[]> {
  const cacheKey = `${subject}:${trialOnly ? "trial" : "full"}`
  const cachedRequest = questionRequests.get(cacheKey)

  if (cachedRequest) {
    return cachedRequest
  }

  const request = loadSubjectQuestions(subject, trialOnly).catch((error) => {
    questionRequests.delete(cacheKey)
    throw error
  })

  questionRequests.set(cacheKey, request)
  return request
}
