"use client"

import { useEffect, useRef } from "react"

import {
  clearClientDataCache,
  getCachedCurrentUser,
} from "@/src/lib/client-data-cache"
import {
  clearStoredSessionToken,
  getStoredSessionToken,
} from "@/src/lib/device-session"
import { supabase } from "@/src/lib/supabase"

/**
 * Enforces single-device login. Each login claims an active_session_id on
 * the user's Profile row (see /api/auth/claim-session); this component
 * watches for that value changing to something other than what this device
 * stored, which means another device signed in, and force-signs this one
 * out. Checked on mount, on tab focus, and pushed live via Realtime.
 */
export function SessionGuard() {
  const signedOutRef = useRef(false)

  useEffect(() => {
    let cancelled = false
    let channel: ReturnType<typeof supabase.channel> | null = null

    const forceSignOut = async () => {
      if (signedOutRef.current) return
      signedOutRef.current = true

      clearStoredSessionToken()
      clearClientDataCache()
      // scope: "local" only tears down this device's session. The
      // default ("global") revokes every session for the user, which
      // would also sign out the device that just logged in.
      await supabase.auth.signOut({ scope: "local" })
      window.location.href = "/?session-ended=1"
    }

    const checkAgainstServer = async (userId: string) => {
      const localToken = getStoredSessionToken()
      if (!localToken) return

      const { data, error } = await supabase
        .from("Profiles")
        .select("active_session_id")
        .eq("id", userId)
        .maybeSingle()

      if (error || !data) return

      if (data.active_session_id && data.active_session_id !== localToken) {
        await forceSignOut()
      }
    }

    const handleRealtimeUpdate = (payload: {
      new: { active_session_id?: string | null }
    }) => {
      const localToken = getStoredSessionToken()
      const newSessionId = payload.new.active_session_id

      if (localToken && newSessionId && newSessionId !== localToken) {
        void forceSignOut()
      }
    }

    const handleVisibility = (userId: string) => () => {
      if (document.visibilityState === "visible") {
        void checkAgainstServer(userId)
      }
    }

    let visibilityHandler: (() => void) | null = null

    const start = async () => {
      const user = await getCachedCurrentUser().catch(() => null)
      if (!user || cancelled) return

      await checkAgainstServer(user.id)
      if (cancelled) return

      channel = supabase
        .channel(`profile-session-${user.id}`)
        .on(
          "postgres_changes",
          {
            event: "UPDATE",
            schema: "public",
            table: "Profiles",
            filter: `id=eq.${user.id}`,
          },
          handleRealtimeUpdate
        )
        .subscribe()

      visibilityHandler = handleVisibility(user.id)
      document.addEventListener("visibilitychange", visibilityHandler)
    }

    void start()

    return () => {
      cancelled = true
      if (channel) supabase.removeChannel(channel)
      if (visibilityHandler) {
        document.removeEventListener("visibilitychange", visibilityHandler)
      }
    }
  }, [])

  return null
}
