"use client"

import { Suspense, useEffect } from "react"
import { useRouter, useSearchParams } from "next/navigation"

function SessionEndedBannerContent() {
  const router = useRouter()
  const searchParams = useSearchParams()

  const sessionEnded = searchParams.get("session-ended") === "1"
  const loginRequired = searchParams.get("login-required") === "1"

  useEffect(() => {
    if (sessionEnded || loginRequired) {
      window.dispatchEvent(new Event("open-login-modal"))
    }
  }, [sessionEnded, loginRequired])

  if (!sessionEnded && !loginRequired) return null

  return (
    <div className="fixed inset-x-0 top-20 z-40 border-b border-[#f4b400]/40 bg-[#fdf3d9] px-4 py-3 text-center text-sm font-medium text-[#183d60]">
      {sessionEnded
        ? "You were signed out because your PilotVault account was logged in on another device."
        : "Please log in to continue."}{" "}
      <button
        type="button"
        onClick={() => router.replace("/")}
        className="font-bold underline underline-offset-2"
      >
        Dismiss
      </button>
    </div>
  )
}

export function SessionEndedBanner() {
  return (
    <Suspense fallback={null}>
      <SessionEndedBannerContent />
    </Suspense>
  )
}
