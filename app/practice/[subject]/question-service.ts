import { supabase } from "@/src/lib/supabase"

import type { DatabaseQuestion, Question } from "./types"

const SUPABASE_PAGE_SIZE = 1000
const questionRequests = new Map<string, Promise<Question[]>>()

const LOCAL_METEOROLOGY_REFERENCE_IMAGE_DIRECTORY =
  "/question-images/meteorology/v1"
// These small, versioned chart crops are mirrored in /public so an exam does
// not depend on a slow cross-origin Storage request while the user is answering.
const METEOROLOGY_REFERENCE_IMAGE_NAMES = new Set([
  "metar-fagg.png",
  "metar-fagm.png",
  "metar-fajs.png",
  "metar-faup.png",
  "sigwx-pe-ct.png",
  "station-14.png",
  "station-2.png",
  "station-4.png",
  "station-5.png",
  "station-6.png",
  "taf-fadn.png",
  "taf-fagg.png",
  "taf-fape.png",
  "upper-winds-25s-15e.png",
  "upper-winds-30s-15e.png",
  "upper-winds-natal-north-coast-final.png",
])

function resolveQuestionImageUrl(
  subject: string,
  imageUrl: string | null
): string | undefined {
  if (!imageUrl) {
    return undefined
  }

  if (
    subject !== "meteorology" ||
    !imageUrl.includes(
      "/storage/v1/object/public/question-images/meteorology/"
    )
  ) {
    return imageUrl
  }

  const imageName = imageUrl.split("?")[0].split("/").pop()

  if (!imageName || !METEOROLOGY_REFERENCE_IMAGE_NAMES.has(imageName)) {
    return imageUrl
  }

  return `${LOCAL_METEOROLOGY_REFERENCE_IMAGE_DIRECTORY}/${imageName}`
}

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
          explanation_image_url,
          explanation_image_title,
          explanation_image_caption,
          explanation_visual_key,
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
    image_url: resolveQuestionImageUrl(question.subject, question.image_url),
    explanation_image_url: question.explanation_visual_key
      ? `pv-atg://${question.explanation_visual_key}`
      : question.explanation_image_url ?? undefined,
    explanation_image_title: question.explanation_image_title ?? undefined,
    explanation_image_caption: question.explanation_image_caption ?? undefined,
    explanation_visual_key: question.explanation_visual_key ?? undefined,
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
