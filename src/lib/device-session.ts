"use client"

import { supabase } from "@/src/lib/supabase"

const SESSION_TOKEN_STORAGE_KEY = "pv_active_session_token"

export function getStoredSessionToken(): string | null {
  if (typeof window === "undefined") return null
  return window.localStorage.getItem(SESSION_TOKEN_STORAGE_KEY)
}

export function clearStoredSessionToken() {
  if (typeof window === "undefined") return
  window.localStorage.removeItem(SESSION_TOKEN_STORAGE_KEY)
}

/**
 * Registers this device as the account's active session, replacing any
 * other device that was previously signed in. Best-effort: a failure here
 * should never block login, so callers don't need to check the result.
 */
export async function claimDeviceSession(): Promise<void> {
  try {
    const { data } = await supabase.auth.getSession()
    const accessToken = data.session?.access_token

    if (!accessToken) return

    const response = await fetch("/api/auth/claim-session", {
      method: "POST",
      headers: { Authorization: `Bearer ${accessToken}` },
    })

    if (!response.ok) return

    const body = (await response.json()) as { sessionToken?: string }

    if (body.sessionToken) {
      window.localStorage.setItem(SESSION_TOKEN_STORAGE_KEY, body.sessionToken)
    }
  } catch {
    // Non-critical: the user stays logged in on this device even if the
    // other-device kick-out couldn't be armed.
  }
}
