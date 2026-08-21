export type Question = {
  id: number
  subject: string
  topic?: string
  question: string
  image_url?: string
  explanation_image_url?: string
  explanation_image_title?: string
  explanation_image_caption?: string
  options: string[]
  correctAnswer: string
  explanation: string
}

export type DatabaseQuestion = {
  id: number
  subject: string
  topic: string | null
  question: string
  image_url: string | null
  explanation_image_url: string | null
  explanation_image_title: string | null
  explanation_image_caption: string | null
  option_a: string | null
  option_b: string | null
  option_c: string | null
  option_d: string | null
  correct_answer: string
  explanation: string | null
  is_trial_question: boolean | null
}

export type ExamMode = "menu" | "mock" | "topics" | "topic"
export type ExamAnswers = Record<number, string>
