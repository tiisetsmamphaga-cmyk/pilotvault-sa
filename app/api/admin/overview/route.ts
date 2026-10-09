import { NextResponse } from "next/server"

import { requireAdmin } from "@/src/lib/admin-auth"
import { supabaseAdmin } from "@/src/lib/supabase-admin"

export const runtime = "nodejs"
export const dynamic = "force-dynamic"

type ProfileRow = {
  id: string
  full_name: string | null
  email: string | null
  licence_level: string | null
  subscription_status: string | null
  subscription_plan: string | null
  payment_status: string | null
  trial_ends_at: string | null
  subscription_expires_at: string | null
  is_test_account: boolean | null
}

type AccessRow = {
  user_id: string
  subject: string
  access_status: string | null
  expires_at: string | null
}

type AttemptRow = {
  user_id: string
  subject: string
  completed_at: string
  score_percentage: number
  correct_answers: number
  total_questions: number
}

type SessionRow = {
  user_id: string
  session_count: number
  last_active_at: string | null
}

type PaymentRow = {
  reference: string
  user_id: string
  product_code: string | null
  subject: string | null
  amount: number | null
  currency: string | null
  status: string | null
  paid_at: string | null
  created_at: string
}

async function listAllAuthUsers() {
  const users = []

  for (let page = 1; page < 50; page += 1) {
    const { data, error } = await supabaseAdmin.auth.admin.listUsers({
      page,
      perPage: 1000,
    })

    if (error) throw new Error(`Could not list accounts: ${error.message}`)

    users.push(...data.users)

    if (data.users.length < 1000) break
  }

  return users
}

export async function GET(request: Request) {
  const auth = await requireAdmin(request)

  if ("response" in auth) return auth.response

  try {
    const [authUsers, profiles, access, attempts, payments, admins, sessions] =
      await Promise.all([
        listAllAuthUsers(),
        supabaseAdmin
          .from("Profiles")
          .select(
            "id, full_name, email, licence_level, subscription_status, subscription_plan, payment_status, trial_ends_at, subscription_expires_at, is_test_account"
          ),
        supabaseAdmin
          .from("SubjectAccess")
          .select("user_id, subject, access_status, expires_at"),
        supabaseAdmin
          .from("ExamAttempts")
          .select("user_id, subject, completed_at, score_percentage, correct_answers, total_questions")
          .order("completed_at", { ascending: false })
          .limit(10000),
        supabaseAdmin
          .from("Payments")
          .select(
            "reference, user_id, product_code, subject, amount, currency, status, paid_at, created_at"
          )
          .order("created_at", { ascending: false })
          .limit(1000),
        supabaseAdmin.from("Admins").select("user_id"),
        supabaseAdmin.rpc("admin_session_activity"),
      ])

    for (const result of [profiles, access, attempts, payments, admins]) {
      if (result.error) throw new Error(result.error.message)
    }

    // Session activity is a nice-to-have: if the function is missing, the
    // rest of the overview still loads and the page shows sessions as unknown.
    if (sessions.error) console.error("Could not read session activity", sessions.error)
    const sessionsAvailable = !sessions.error
    const sessionByUser = new Map(
      ((sessions.data ?? []) as SessionRow[]).map((row) => [row.user_id, row])
    )

    const adminIds = new Set((admins.data ?? []).map((row) => row.user_id as string))
    const profileById = new Map(
      ((profiles.data ?? []) as ProfileRow[]).map((row) => [row.id, row])
    )

    const accessByUser = new Map<string, AccessRow[]>()
    for (const row of (access.data ?? []) as AccessRow[]) {
      const list = accessByUser.get(row.user_id) ?? []
      list.push(row)
      accessByUser.set(row.user_id, list)
    }

    const attemptsByUser = new Map<string, AttemptRow[]>()
    for (const row of (attempts.data ?? []) as AttemptRow[]) {
      const list = attemptsByUser.get(row.user_id) ?? []
      list.push(row)
      attemptsByUser.set(row.user_id, list)
    }

    const paymentRows = (payments.data ?? []) as PaymentRow[]
    const paymentsByUser = new Map<string, PaymentRow[]>()
    for (const row of paymentRows) {
      const list = paymentsByUser.get(row.user_id) ?? []
      list.push(row)
      paymentsByUser.set(row.user_id, list)
    }

    const users = authUsers
      .map((authUser) => {
        const profile = profileById.get(authUser.id)
        const userAttempts = attemptsByUser.get(authUser.id) ?? []
        const userPayments = paymentsByUser.get(authUser.id) ?? []
        const session = sessionByUser.get(authUser.id)
        const trialEndsAt = profile?.trial_ends_at ?? null
        // A checkout that was started but never paid: its row is still
        // "initialized" and the same product wasn't bought afterwards either
        // (a second, completed attempt makes the first one irrelevant).
        const fulfilled = userPayments.filter((row) => row.status === "fulfilled")
        const unpaidCheckouts = userPayments.filter(
          (row) =>
            row.status === "initialized" &&
            !fulfilled.some(
              (paid) =>
                paid.product_code === row.product_code &&
                paid.subject === row.subject &&
                Date.parse(paid.created_at) >= Date.parse(row.created_at)
            )
        )

        return {
          id: authUser.id,
          email: authUser.email ?? profile?.email ?? null,
          fullName: profile?.full_name ?? null,
          createdAt: authUser.created_at,
          lastSignInAt: authUser.last_sign_in_at ?? null,
          emailConfirmed: Boolean(authUser.email_confirmed_at),
          isAdmin: adminIds.has(authUser.id),
          isTestAccount: Boolean(profile?.is_test_account),
          licenceLevel: profile?.licence_level ?? null,
          subscriptionStatus: profile?.subscription_status ?? null,
          subscriptionPlan: profile?.subscription_plan ?? null,
          paymentStatus: profile?.payment_status ?? null,
          trialEndsAt: profile?.trial_ends_at ?? null,
          subscriptionExpiresAt: profile?.subscription_expires_at ?? null,
          subjectAccess: (accessByUser.get(authUser.id) ?? []).map((row) => ({
            subject: row.subject,
            accessStatus: row.access_status,
            expiresAt: row.expires_at,
          })),
          attemptCount: userAttempts.length,
          lastAttemptAt: userAttempts[0]?.completed_at ?? null,
          subjectsTried: [...new Set(userAttempts.map((row) => row.subject))].sort(),
          // Mocks finished before the trial ended, oldest first.
          trialMocks: trialEndsAt
            ? userAttempts
                .filter((row) => Date.parse(row.completed_at) <= Date.parse(trialEndsAt))
                .map((row) => ({
                  subject: row.subject,
                  scorePercentage: row.score_percentage,
                  correctAnswers: row.correct_answers,
                  totalQuestions: row.total_questions,
                  completedAt: row.completed_at,
                }))
                .reverse()
            : [],
          hasSession: sessionsAvailable ? Boolean(session) : null,
          lastActiveAt: session?.last_active_at ?? null,
          unpaidCheckouts: unpaidCheckouts.map((row) => ({
            productCode: row.product_code,
            subject: row.subject,
            amountCents: row.amount,
            startedAt: row.created_at,
          })),
          fulfilledPayments: fulfilled.length,
        }
      })
      .sort((a, b) => b.createdAt.localeCompare(a.createdAt))

    const now = Date.now()
    const day = 24 * 60 * 60 * 1000
    // Real students only: admin and test accounts never count towards totals.
    const students = users.filter((user) => !user.isAdmin && !user.isTestAccount)
    const studentIds = new Set(students.map((user) => user.id))
    const signedUpWithin = (ms: number) =>
      students.filter((user) => now - new Date(user.createdAt).getTime() < ms).length
    const studentPayments = paymentRows.filter(
      (row) => row.status === "fulfilled" && studentIds.has(row.user_id)
    )

    const summary = {
      totalAccounts: students.length,
      testAccounts: users.filter((user) => !user.isAdmin && user.isTestAccount).length,
      signUps24h: signedUpWithin(day),
      signUps7d: signedUpWithin(7 * day),
      signUps30d: signedUpWithin(30 * day),
      activeTrials: students.filter(
        (user) =>
          user.subscriptionPlan === "trial" &&
          user.trialEndsAt !== null &&
          new Date(user.trialEndsAt).getTime() > now
      ).length,
      activePplPacks: students.filter(
        (user) =>
          user.subscriptionStatus === "active" &&
          user.subscriptionPlan === "ppl" &&
          user.subscriptionExpiresAt !== null &&
          new Date(user.subscriptionExpiresAt).getTime() > now
      ).length,
      fulfilledRevenueCents: studentPayments.reduce((sum, row) => sum + (row.amount ?? 0), 0),
    }

    const funnel = {
      signedUp: students.length,
      tookMock: students.filter((user) => user.attemptCount > 0).length,
      paid: students.filter((user) => user.fulfilledPayments > 0).length,
    }

    // Raw points for the over-time charts; the page buckets them by week or month.
    const series = {
      signUps: students.map((user) => user.createdAt),
      payments: studentPayments.map((row) => ({
        at: row.paid_at ?? row.created_at,
        product: row.product_code === "ppl_pack" ? "ppl_pack" : "subject",
        amountCents: row.amount ?? 0,
      })),
    }

    const emailById = new Map(users.map((user) => [user.id, user.email]))
    // Checkout attempts that never got paid are listed per account instead.
    const recentPayments = paymentRows
      .filter((row) => row.status !== "initialized")
      .slice(0, 50)
      .map((row) => ({
        reference: row.reference,
        email: emailById.get(row.user_id) ?? null,
        isTestOrAdmin: !studentIds.has(row.user_id),
        productCode: row.product_code,
        subject: row.subject,
        amountCents: row.amount,
        currency: row.currency,
        status: row.status,
        paidAt: row.paid_at,
        createdAt: row.created_at,
      }))

    return NextResponse.json({ summary, funnel, series, users, recentPayments, sessionsAvailable })
  } catch (error) {
    return NextResponse.json(
      {
        error:
          error instanceof Error ? error.message : "Could not load the admin overview.",
      },
      { status: 500 }
    )
  }
}
