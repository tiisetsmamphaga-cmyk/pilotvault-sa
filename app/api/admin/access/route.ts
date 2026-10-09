import { NextResponse } from "next/server"

import { requireAdmin } from "@/src/lib/admin-auth"
import { isPilotVaultSubject } from "@/src/lib/billing-products"
import { supabaseAdmin } from "@/src/lib/supabase-admin"

export const runtime = "nodejs"

type AccessAction =
  | { action: "extend_trial"; userId: string; days: number }
  | { action: "grant_ppl"; userId: string; days: number }
  | { action: "grant_subject"; userId: string; days: number; subject: string }
  | { action: "end_trial"; userId: string }
  | { action: "revoke_ppl"; userId: string }
  | { action: "revoke_subject"; userId: string; subject: string }
  | { action: "set_test_account"; userId: string; value: boolean }

const GRANT_ACTIONS = new Set(["extend_trial", "grant_ppl", "grant_subject"])

const UUID_PATTERN =
  /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i

const DAY_MS = 24 * 60 * 60 * 1000

function badRequest(message: string) {
  return NextResponse.json({ error: message }, { status: 400 })
}

function serverError(message: string) {
  return NextResponse.json({ error: message }, { status: 500 })
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

  if (GRANT_ACTIONS.has(body.action)) {
    const days = (body as { days?: unknown }).days

    if (!Number.isInteger(days) || (days as number) < 1 || (days as number) > 3650) {
      return badRequest("Days must be a whole number from 1 to 3650.")
    }
  }

  const { data: target, error: adminCheckError } = await supabaseAdmin
    .from("Admins")
    .select("user_id")
    .eq("user_id", body.userId)
    .maybeSingle()

  if (adminCheckError) return serverError(adminCheckError.message)

  if (target) {
    return badRequest("Admin accounts are changed from the Preview access panel, not here.")
  }

  const { data: profile, error: profileError } = await supabaseAdmin
    .from("Profiles")
    .select("subscription_status, subscription_plan, trial_ends_at, subscription_expires_at")
    .eq("id", body.userId)
    .maybeSingle()

  if (profileError) return serverError(profileError.message)

  if (!profile) {
    return NextResponse.json({ error: "That account has no profile." }, { status: 404 })
  }

  const now = new Date().toISOString()

  switch (body.action) {
    case "extend_trial": {
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

      if (error) return serverError(error.message)
      break
    }

    case "grant_ppl": {
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

      if (error) return serverError(error.message)
      break
    }

    case "grant_subject": {
      if (typeof body.subject !== "string" || !isPilotVaultSubject(body.subject)) {
        return badRequest("Choose a valid subject.")
      }

      const { data: current, error: readError } = await supabaseAdmin
        .from("SubjectAccess")
        .select("expires_at, access_status")
        .eq("user_id", body.userId)
        .eq("subject", body.subject)
        .maybeSingle()

      if (readError) return serverError(readError.message)

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

      if (error) return serverError(error.message)
      break
    }

    case "end_trial": {
      if (profile.subscription_plan !== "trial") {
        return badRequest("This account is not on a trial.")
      }

      // The plan stays "trial" with an end date of now, exactly like a trial
      // that ran out on its own, so the student sees the normal expired flow.
      const { error } = await supabaseAdmin
        .from("Profiles")
        .update({ trial_ends_at: now, updated_at: now })
        .eq("id", body.userId)

      if (error) return serverError(error.message)
      break
    }

    case "revoke_ppl": {
      if (profile.subscription_plan !== "ppl") {
        return badRequest("This account does not have the PPL Pack.")
      }

      const { error } = await supabaseAdmin
        .from("Profiles")
        .update({
          subscription_status: "inactive",
          subscription_plan: null,
          subscription_expires_at: now,
          updated_at: now,
        })
        .eq("id", body.userId)

      if (error) return serverError(error.message)
      break
    }

    case "revoke_subject": {
      if (typeof body.subject !== "string" || !isPilotVaultSubject(body.subject)) {
        return badRequest("Choose a valid subject.")
      }

      const { data, error } = await supabaseAdmin
        .from("SubjectAccess")
        .update({ access_status: "revoked", expires_at: now })
        .eq("user_id", body.userId)
        .eq("subject", body.subject)
        .select("subject")

      if (error) return serverError(error.message)
      if (!data?.length) return badRequest("This account does not own that subject.")
      break
    }

    case "set_test_account": {
      if (typeof body.value !== "boolean") return badRequest("Choose test or real.")

      const { error } = await supabaseAdmin
        .from("Profiles")
        .update({ is_test_account: body.value, updated_at: now })
        .eq("id", body.userId)

      if (error) return serverError(error.message)
      break
    }

    default:
      return badRequest("Unknown action.")
  }

  return NextResponse.json({ ok: true })
}
