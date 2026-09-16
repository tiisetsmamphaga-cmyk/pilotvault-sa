"use client"

import { Suspense, useEffect } from "react"
import { useRouter, useSearchParams } from "next/navigation"

const MESSAGES = {
  "session-ended":
    "You were signed out because your PilotVault account was logged in on another device. Log in again to continue.",
  "login-required": "Please log in to continue.",
} as const

function SessionEndedBannerContent() {
  const router = useRouter()
  const searchParams = useSearchParams()

  const reason = searchParams.get("session-ended") === "1"
    ? "session-ended"
    : searchParams.get("login-required") === "1"
      ? "login-required"
      : null

  useEffect(() => {
    if (!reason) return

    window.dispatchEvent(
      new CustomEvent("open-login-modal", {
        detail: { message: MESSAGES[reason] },
      })
    )
    router.replace("/")
  }, [reason, router])

  return null
}

export function SessionEndedBanner() {
  return (
    <Suspense fallback={null}>
      <SessionEndedBannerContent />
    </Suspense>
  )
}
