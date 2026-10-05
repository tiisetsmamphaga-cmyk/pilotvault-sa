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
    const [authUsers, profiles, access, attempts, payments, admins] =
      await Promise.all([
        listAllAuthUsers(),
        supabaseAdmin
          .from("Profiles")
          .select(
            "id, full_name, email, licence_level, subscription_status, subscription_plan, payment_status, trial_ends_at, subscription_expires_at"
          ),
        supabaseAdmin
          .from("SubjectAccess")
          .select("user_id, subject, access_status, expires_at"),
        supabaseAdmin
          .from("ExamAttempts")
          .select("user_id, subject, completed_at")
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
      ])

    for (const result of [profiles, access, attempts, payments, admins]) {
      if (result.error) throw new Error(result.error.message)
    }

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

        return {
          id: authUser.id,
          email: authUser.email ?? profile?.email ?? null,
          fullName: profile?.full_name ?? null,
          createdAt: authUser.created_at,
          lastSignInAt: authUser.last_sign_in_at ?? null,
          emailConfirmed: Boolean(authUser.email_confirmed_at),
          isAdmin: adminIds.has(authUser.id),
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
          fulfilledPayments: userPayments.filter((row) => row.status === "fulfilled").length,
        }
      })
      .sort((a, b) => b.createdAt.localeCompare(a.createdAt))

    const now = Date.now()
    const day = 24 * 60 * 60 * 1000
    const students = users.filter((user) => !user.isAdmin)
    const signedUpWithin = (ms: number) =>
      students.filter((user) => now - new Date(user.createdAt).getTime() < ms).length

    const summary = {
      totalAccounts: students.length,
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
      fulfilledRevenueCents: paymentRows
        .filter((row) => row.status === "fulfilled" && !adminIds.has(row.user_id))
        .reduce((sum, row) => sum + (row.amount ?? 0), 0),
    }

    const emailById = new Map(users.map((user) => [user.id, user.email]))
    const recentPayments = paymentRows.slice(0, 50).map((row) => ({
      reference: row.reference,
      email: emailById.get(row.user_id) ?? null,
      productCode: row.product_code,
      subject: row.subject,
      amountCents: row.amount,
      currency: row.currency,
      status: row.status,
      paidAt: row.paid_at,
      createdAt: row.created_at,
    }))

    return NextResponse.json({ summary, users, recentPayments })
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
