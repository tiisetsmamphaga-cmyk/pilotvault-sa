"use client"

import { Suspense } from "react"
import { useRouter, useSearchParams } from "next/navigation"

function SessionEndedBannerContent() {
  const router = useRouter()
  const searchParams = useSearchParams()

  if (searchParams.get("session-ended") !== "1") return null

  return (
    <div className="fixed inset-x-0 top-20 z-40 border-b border-[#f4b400]/40 bg-[#fdf3d9] px-4 py-3 text-center text-sm font-medium text-[#183d60]">
      You were signed out because your PilotVault account was logged in on
      another device.{" "}
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
