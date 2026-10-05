import { NextResponse } from "next/server"

import { requireAdmin } from "@/src/lib/admin-auth"
import { isPilotVaultSubject } from "@/src/lib/billing-products"
import { supabaseAdmin } from "@/src/lib/supabase-admin"

export const runtime = "nodejs"

type AccessAction =
  | { action: "extend_trial"; userId: string; days: number }
  | { action: "grant_ppl"; userId: string; days: number }
  | { action: "grant_subject"; userId: string; days: number; subject: string }

const UUID_PATTERN =
  /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i

const DAY_MS = 24 * 60 * 60 * 1000

function badRequest(message: string) {
  return NextResponse.json({ error: message }, { status: 400 })
}

// Extends from whichever is later - the current expiry or now - so granted
// time is added on top of any time the user already has.
function extendFrom(current: string | null | undefined, days: number) {
  const now = Date.now()
  const currentMs = current ? new Date(current).getTime() : Number.NaN
  const base = Number.isFinite(currentMs) && currentMs > now ? currentMs : now

  return new Date(base + days * DAY_MS).toISOString()
}

export async function POST(request: Request) {
  const auth = await requireAdmin(request)

  if ("response" in auth) return auth.response

  let body: AccessAction

  try {
    body = (await request.json()) as AccessAction
  } catch {
    return badRequest("Invalid request body.")
  }

  if (!body || typeof body.userId !== "string" || !UUID_PATTERN.test(body.userId)) {
    return badRequest("Choose a valid account.")
  }

  if (!Number.isInteger(body.days) || body.days < 1 || body.days > 3650) {
    return badRequest("Days must be a whole number from 1 to 3650.")
  }

  const { data: profile, error: profileError } = await supabaseAdmin
    .from("Profiles")
    .select("subscription_status, subscription_plan, trial_ends_at, subscription_expires_at")
    .eq("id", body.userId)
    .maybeSingle()

  if (profileError) {
    return NextResponse.json({ error: profileError.message }, { status: 500 })
  }

  if (!profile) {
    return NextResponse.json({ error: "That account has no profile." }, { status: 404 })
  }

  const now = new Date().toISOString()

  if (body.action === "extend_trial") {
    if (profile.subscription_status === "active" && profile.subscription_plan === "ppl") {
      return badRequest("This account already has the PPL Pack, so a trial would reduce its access.")
    }

    const { error } = await supabaseAdmin
      .from("Profiles")
      .update({
        subscription_status: "trial",
        subscription_plan: "trial",
        trial_ends_at: extendFrom(profile.trial_ends_at, body.days),
        updated_at: now,
      })
      .eq("id", body.userId)

    if (error) return NextResponse.json({ error: error.message }, { status: 500 })
  } else if (body.action === "grant_ppl") {
    const { error } = await supabaseAdmin
      .from("Profiles")
      .update({
        subscription_status: "active",
        subscription_plan: "ppl",
        subscription_expires_at: extendFrom(
          profile.subscription_plan === "ppl" ? profile.subscription_expires_at : null,
          body.days
        ),
        updated_at: now,
      })
      .eq("id", body.userId)

    if (error) return NextResponse.json({ error: error.message }, { status: 500 })
  } else if (body.action === "grant_subject") {
    if (typeof body.subject !== "string" || !isPilotVaultSubject(body.subject)) {
      return badRequest("Choose a valid subject.")
    }

    const { data: current, error: readError } = await supabaseAdmin
      .from("SubjectAccess")
      .select("expires_at, access_status")
      .eq("user_id", body.userId)
      .eq("subject", body.subject)
      .maybeSingle()

    if (readError) return NextResponse.json({ error: readError.message }, { status: 500 })

    const { error } = await supabaseAdmin.from("SubjectAccess").upsert(
      {
        user_id: body.userId,
        subject: body.subject,
        access_status: "active",
        starts_at: now,
        expires_at: extendFrom(
          current?.access_status === "active" ? current.expires_at : null,
          body.days
        ),
      },
      { onConflict: "user_id,subject" }
    )

    if (error) return NextResponse.json({ error: error.message }, { status: 500 })
  } else {
    return badRequest("Unknown action.")
  }

  return NextResponse.json({ ok: true })
}
