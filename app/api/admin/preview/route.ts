import { NextResponse } from "next/server"

import { requireAdmin } from "@/src/lib/admin-auth"
import { isPilotVaultSubject } from "@/src/lib/billing-products"
import { supabaseAdmin } from "@/src/lib/supabase-admin"

export const runtime = "nodejs"

// Lets an admin switch their OWN account between the access types students
// can have, so they can see the site exactly as that student would. Admin
// accounts are excluded from the admin stats, so previews never skew them.
type PreviewMode = "admin" | "ppl" | "trial" | "trial_expired" | "subject"

const HOUR_MS = 60 * 60 * 1000
const DAY_MS = 24 * HOUR_MS

function inMonths(months: number) {
  const date = new Date()
  date.setUTCMonth(date.getUTCMonth() + months)
  return date.toISOString()
}

export async function POST(request: Request) {
  const auth = await requireAdmin(request)

  if ("response" in auth) return auth.response

  let body: { mode?: PreviewMode; subjects?: unknown }

  try {
    body = await request.json()
  } catch {
    return NextResponse.json({ error: "Invalid request body." }, { status: 400 })
  }

  const mode = body.mode
  const userId = auth.user.id
  const now = Date.now()
  const nowIso = new Date(now).toISOString()

  const subjects = Array.isArray(body.subjects)
    ? [...new Set(body.subjects.filter((value): value is string => typeof value === "string"))]
    : []

  if (mode === "subject" && (!subjects.length || !subjects.every(isPilotVaultSubject))) {
    return NextResponse.json({ error: "Tick at least one valid subject." }, { status: 400 })
  }

  let profileUpdate: Record<string, string | null>

  switch (mode) {
    case "admin":
      profileUpdate = {
        subscription_status: "active",
        subscription_plan: "ppl",
        payment_status: "admin",
        subscription_expires_at: "2099-12-31T23:59:59Z",
        trial_ends_at: null,
      }
      break
    case "ppl":
      profileUpdate = {
        subscription_status: "active",
        subscription_plan: "ppl",
        payment_status: "admin_preview",
        subscription_expires_at: inMonths(3),
        trial_ends_at: null,
      }
      break
    case "trial":
      profileUpdate = {
        subscription_status: "trial",
        subscription_plan: "trial",
        payment_status: "admin_preview",
        subscription_expires_at: null,
        trial_ends_at: new Date(now + 3 * DAY_MS).toISOString(),
      }
      break
    case "trial_expired":
      profileUpdate = {
        subscription_status: "trial",
        subscription_plan: "trial",
        payment_status: "admin_preview",
        subscription_expires_at: null,
        trial_ends_at: new Date(now - HOUR_MS).toISOString(),
      }
      break
    case "subject":
      // A subject buyer's trial has ended (buying a subject ends blanket trial
      // access); the end date is set outside the discount window.
      profileUpdate = {
        subscription_status: "inactive",
        subscription_plan: null,
        payment_status: "admin_preview",
        subscription_expires_at: null,
        trial_ends_at: new Date(now - 2 * DAY_MS).toISOString(),
      }
      break
    default:
      return NextResponse.json({ error: "Unknown preview mode." }, { status: 400 })
  }

  // Start every preview from a clean slate of subject access (own account only).
  const { error: clearError } = await supabaseAdmin
    .from("SubjectAccess")
    .delete()
    .eq("user_id", userId)

  if (clearError) return NextResponse.json({ error: clearError.message }, { status: 500 })

  const { error: profileError } = await supabaseAdmin
    .from("Profiles")
    .update({ ...profileUpdate, updated_at: nowIso })
    .eq("id", userId)

  if (profileError) return NextResponse.json({ error: profileError.message }, { status: 500 })

  if (mode === "subject") {
    const { error: accessError } = await supabaseAdmin.from("SubjectAccess").insert(
      subjects.map((subject) => ({
        user_id: userId,
        subject,
        access_status: "active",
        starts_at: nowIso,
        expires_at: inMonths(1),
      }))
    )

    if (accessError) return NextResponse.json({ error: accessError.message }, { status: 500 })
  }

  return NextResponse.json({ ok: true, mode })
}
