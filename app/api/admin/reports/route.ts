import { NextResponse } from "next/server"

import { requireAdmin } from "@/src/lib/admin-auth"
import { supabaseAdmin } from "@/src/lib/supabase-admin"

export const runtime = "nodejs"
export const dynamic = "force-dynamic"

type ReportRow = {
  id: number
  question_id: number
  user_id: string
  reason: string
  message: string | null
  status: string
  admin_note: string | null
  created_at: string
  resolved_at: string | null
}

type QuestionRow = {
  id: number
  subject: string
  topic: string | null
  question: string
  option_a: string | null
  option_b: string | null
  option_c: string | null
  option_d: string | null
  correct_answer: string
  explanation: string | null
  is_trial_question: boolean | null
}

const STATUSES = new Set(["open", "resolved", "dismissed"])

export async function GET(request: Request) {
  const auth = await requireAdmin(request)

  if ("response" in auth) return auth.response

  const { data: reports, error } = await supabaseAdmin
    .from("QuestionReports")
    .select("id, question_id, user_id, reason, message, status, admin_note, created_at, resolved_at")
    .order("created_at", { ascending: false })
    .limit(500)

  if (error) return NextResponse.json({ error: error.message }, { status: 500 })

  const rows = (reports ?? []) as ReportRow[]
  const questionIds = [...new Set(rows.map((row) => row.question_id))]
  const userIds = [...new Set(rows.map((row) => row.user_id))]

  const [questions, profiles] = await Promise.all([
    questionIds.length
      ? supabaseAdmin
          .from("questions")
          .select(
            "id, subject, topic, question, option_a, option_b, option_c, option_d, correct_answer, explanation, is_trial_question"
          )
          .in("id", questionIds)
      : Promise.resolve({ data: [], error: null }),
    userIds.length
      ? supabaseAdmin.from("Profiles").select("id, email, full_name, is_test_account").in("id", userIds)
      : Promise.resolve({ data: [], error: null }),
  ])

  if (questions.error) return NextResponse.json({ error: questions.error.message }, { status: 500 })
  if (profiles.error) return NextResponse.json({ error: profiles.error.message }, { status: 500 })

  const questionById = new Map(((questions.data ?? []) as QuestionRow[]).map((row) => [row.id, row]))
  const profileById = new Map(
    ((profiles.data ?? []) as { id: string; email: string | null; full_name: string | null; is_test_account: boolean | null }[]).map(
      (row) => [row.id, row]
    )
  )

  const tickets = rows.map((row) => {
    const question = questionById.get(row.question_id)
    const reporter = profileById.get(row.user_id)

    return {
      id: row.id,
      reason: row.reason,
      message: row.message,
      status: row.status,
      adminNote: row.admin_note,
      createdAt: row.created_at,
      resolvedAt: row.resolved_at,
      reporter: {
        email: reporter?.email ?? null,
        name: reporter?.full_name ?? null,
        isTestAccount: Boolean(reporter?.is_test_account),
      },
      question: question
        ? {
            id: question.id,
            subject: question.subject,
            topic: question.topic,
            text: question.question,
            options: [question.option_a, question.option_b, question.option_c, question.option_d].filter(
              (option): option is string => Boolean(option)
            ),
            correctAnswer: question.correct_answer,
            explanation: question.explanation,
            isTrialQuestion: Boolean(question.is_trial_question),
          }
        : null,
    }
  })

  return NextResponse.json({ tickets })
}

export async function POST(request: Request) {
  const auth = await requireAdmin(request)

  if ("response" in auth) return auth.response

  let body: { id?: unknown; status?: unknown; note?: unknown }

  try {
    body = await request.json()
  } catch {
    return NextResponse.json({ error: "Invalid request body." }, { status: 400 })
  }

  if (!Number.isInteger(body.id)) {
    return NextResponse.json({ error: "Choose a valid report." }, { status: 400 })
  }

  if (typeof body.status !== "string" || !STATUSES.has(body.status)) {
    return NextResponse.json({ error: "Choose open, resolved or dismissed." }, { status: 400 })
  }

  const note = typeof body.note === "string" ? body.note.trim().slice(0, 2000) : null
  const closing = body.status !== "open"

  const { data, error } = await supabaseAdmin
    .from("QuestionReports")
    .update({
      status: body.status,
      admin_note: note || null,
      resolved_at: closing ? new Date().toISOString() : null,
      resolved_by: closing ? auth.user.id : null,
    })
    .eq("id", body.id as number)
    .select("id")

  if (error) {
    // Re-opening fails if the same student already has another open report
    // for this question (one open report per student per question).
    const message =
      error.code === "23505"
        ? "This student already has an open report for this question."
        : error.message
    return NextResponse.json({ error: message }, { status: error.code === "23505" ? 409 : 500 })
  }

  if (!data?.length) return NextResponse.json({ error: "Report not found." }, { status: 404 })

  return NextResponse.json({ ok: true })
}
