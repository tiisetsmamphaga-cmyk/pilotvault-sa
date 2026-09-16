"use client"

import { useEffect } from "react"
import { useRouter } from "next/navigation"

import { getCachedCurrentUser } from "@/src/lib/client-data-cache"

export function HomeAuthRedirect() {
  const router = useRouter()

  useEffect(() => {
    let cancelled = false

    getCachedCurrentUser()
      .then((user) => {
        if (!cancelled && user) {
          router.replace("/dashboard")
        }
      })
      .catch(() => {
        // Not logged in, or the session check failed - stay on the
        // marketing page rather than blocking it on an auth error.
      })

    return () => {
      cancelled = true
    }
  }, [router])

  return null
}
