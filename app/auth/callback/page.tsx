"use client"

import { useEffect, useState } from "react"
import Link from "next/link"
import { useRouter } from "next/navigation"
import { PlaneTakeoff, Radar } from "lucide-react"

import { supabase } from "@/src/lib/supabase"

export default function AuthCallbackPage() {
  const router = useRouter()
  const [errorMessage, setErrorMessage] = useState("")

  useEffect(() => {
    let cancelled = false

    const completeSignIn = async () => {
      try {
        const {
          data: { session },
          error: sessionError,
        } = await supabase.auth.getSession()

        if (sessionError) throw sessionError
        if (!session?.user) {
          throw new Error("We could not complete your sign-in. Please try again.")
        }

        const user = session.user
        const { data: existingProfile, error: profileLookupError } = await supabase
          .from("Profiles")
          .select("id")
          .eq("id", user.id)
          .maybeSingle()

        if (profileLookupError) throw profileLookupError

        if (!existingProfile) {
          const fullName =
            user.user_metadata.full_name ||
            user.user_metadata.name ||
            user.email?.split("@")[0] ||
            "Student Pilot"
          const trialEndsAt = new Date(
            Date.now() + 3 * 24 * 60 * 60 * 1000
          ).toISOString()

          const { error: profileCreateError } = await supabase
            .from("Profiles")
            .insert({
              id: user.id,
              full_name: fullName,
              email: user.email ?? null,
              subscription_status: "trial",
              subscription_plan: "trial",
              payment_status: "unpaid",
              trial_ends_at: trialEndsAt,
            })

          if (profileCreateError) throw profileCreateError
        }

        if (!cancelled) router.replace("/dashboard")
      } catch (error) {
        if (!cancelled) {
          setErrorMessage(
            error instanceof Error
              ? error.message
              : "We could not complete your sign-in. Please try again."
          )
        }
      }
    }

    completeSignIn()

    return () => {
      cancelled = true
    }
  }, [router])

  return (
    <main className="relative flex min-h-screen items-center justify-center overflow-hidden bg-[#06111f] px-4 py-10 text-white">
      <div className="pointer-events-none absolute -left-28 top-1/3 h-80 w-80 rounded-full bg-[#f4b400]/5 blur-3xl" />
      <div className="pointer-events-none absolute -right-24 bottom-0 h-96 w-96 rounded-full bg-[#1e3a5f]/30 blur-3xl" />

      <section className="relative w-full max-w-md overflow-hidden rounded-[28px] border border-[#1e3a5f] bg-[#081726] p-7 text-center shadow-2xl sm:p-9">
        <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl border border-[#f4b400]/30 bg-[#f4b400]/10 text-[#f4b400]">
          {errorMessage ? (
            <Radar className="h-8 w-8" />
          ) : (
            <PlaneTakeoff className="h-8 w-8 animate-pulse" />
          )}
        </div>

        <p className="mt-6 text-[10px] font-bold uppercase tracking-[0.3em] text-[#f4b400]">
          PilotVault access
        </p>
        <h1 className="mt-3 text-2xl font-bold">
          {errorMessage ? "Sign-in needs another approach." : "Preparing your flight deck..."}
        </h1>
        <p className="mt-3 text-sm leading-6 text-gray-400">
          {errorMessage ||
            "Your account is secure. We’re loading your trial and taking you to the dashboard."}
        </p>

        {errorMessage && (
          <div className="mt-6 space-y-3">
            <Link
              href="/"
              className="block rounded-xl bg-[#f4b400] px-5 py-3 text-sm font-bold text-[#06111f] transition hover:bg-[#d9a000]"
            >
              Return and try again
            </Link>
            <a
              href="mailto:contact@pilotvault.co.za?subject=PilotVault%20sign-in%20help"
              className="block text-sm font-semibold text-gray-300 transition hover:text-[#f4b400]"
            >
              Contact support
            </a>
          </div>
        )}
      </section>
    </main>
  )
}
