"use client"

import { useEffect, useState } from "react"
import Link from "next/link"
import { useRouter } from "next/navigation"
import {
  Cloud,
  Scale,
  Compass,
  Brain,
  Plane,
  Wrench,
  Radio,
  Map,
  LogOut,
  UserRound,
} from "lucide-react"
import { PageSkeleton } from "@/components/page-skeleton"
import {
  clearClientDataCache,
  getCachedCurrentUser,
  getCachedProfile,
  getCachedSubjectAccess,
  type CachedProfile,
  type CachedSubjectAccess,
} from "@/src/lib/client-data-cache"
import { supabase } from "@/src/lib/supabase"

// Production deployment trigger. No visual or functional changes.
const subjects = [
  { name: "Meteorology", slug: "meteorology", icon: Cloud },
  { name: "Air Law", slug: "air-law", icon: Scale },
  { name: "Navigation", slug: "navigation", icon: Compass },
  { name: "Human Performance", slug: "human-performance", icon: Brain },
  { name: "Principles of Flight", slug: "principles-of-flight", icon: Plane },
  {
    name: "Aircraft Technical and General",
    slug: "aircraft-technical-and-general",
    icon: Wrench,
  },
  { name: "Radio Telephony", slug: "radio-telephony", icon: Radio },
  { name: "Flight Planning", slug: "flight-planning", icon: Map },
]

export default function DashboardPage() {
  const router = useRouter()
  const [loading, setLoading] = useState(true)
  const [loadError, setLoadError] = useState("")
  const [profile, setProfile] = useState<CachedProfile | null>(null)
  const [subjectAccess, setSubjectAccess] = useState<CachedSubjectAccess[]>([])

  useEffect(() => {
    let cancelled = false

    const loadDashboard = async () => {
      try {
        setLoading(true)
        setLoadError("")

        const user = await getCachedCurrentUser()

        if (!user) {
          router.replace("/")
          return
        }

        const [profileData, accessData] = await Promise.all([
          getCachedProfile(user.id),
          getCachedSubjectAccess(user.id),
        ])

        if (!cancelled) {
          setProfile(profileData)
          setSubjectAccess(accessData)
        }
      } catch (error) {
        if (!cancelled) {
          setLoadError(
            error instanceof Error
              ? error.message
              : "Your dashboard could not be loaded."
          )
        }
      } finally {
        if (!cancelled) {
          setLoading(false)
        }
      }
    }

    loadDashboard()

    return () => {
      cancelled = true
    }
  }, [router])

  const handleLogout = async () => {
    clearClientDataCache()
    await supabase.auth.signOut()
    router.replace("/")
  }

  const isTrialUser =
    profile?.subscription_plan === "trial" &&
    profile?.trial_ends_at !== null &&
    new Date(profile.trial_ends_at) > new Date()

  const isPplUser =
    profile?.subscription_status === "active" &&
    profile?.subscription_plan === "ppl" &&
    profile?.subscription_expires_at !== null &&
    new Date(profile.subscription_expires_at) > new Date()

  const hasSubjectAccess = (slug: string) => {
    if (isTrialUser || isPplUser) return true

    return subjectAccess.some((access) => {
      const isSameSubject = access.subject === slug
      const isActive = access.access_status === "active"
      const isNotExpired = new Date(access.expires_at) > new Date()

      return isSameSubject && isActive && isNotExpired
    })
  }

  if (loading || (!profile && !loadError)) {
    return <PageSkeleton variant="dashboard" />
  }

  if (loadError) {
    return (
      <main className="min-h-screen bg-[#06111f] px-4 py-10 text-white sm:px-6">
        <div className="mx-auto max-w-xl rounded-3xl border border-red-500/30 bg-[#081726] p-6 sm:p-8">
          <p className="text-xs uppercase tracking-[0.25em] text-red-400">
            Dashboard Error
          </p>
          <h1 className="mt-3 text-2xl font-bold">
            Your dashboard could not be loaded.
          </h1>
          <p className="mt-3 text-sm leading-6 text-gray-400">{loadError}</p>
          <button
            type="button"
            onClick={() => window.location.reload()}
            className="mt-6 rounded-xl bg-[#f4b400] px-5 py-3 text-sm font-bold text-[#06111f] hover:bg-[#d9a000]"
          >
            Try again
          </button>
        </div>
      </main>
    )
  }

  return (
    <main className="min-h-screen bg-[#06111f] text-white">
      <header className="border-b border-[#1e3a5f] bg-[#06111f]/95">
        <div className="mx-auto flex min-h-16 max-w-7xl items-center justify-between gap-3 px-4 sm:min-h-20 sm:px-6 lg:px-8">
          <div className="min-w-0">
            <p className="text-[10px] uppercase tracking-[0.22em] text-[#f4b400] sm:text-xs sm:tracking-[0.25em]">
              PilotVault SA
            </p>
            <h1 className="mt-1 truncate text-base font-bold sm:text-lg">
              Dashboard
            </h1>
          </div>

          <div className="flex shrink-0 items-center gap-2">
            <Link
              href="/profile"
              aria-label="Open profile"
              title="Open profile"
              className="group flex h-11 items-center gap-2 rounded-2xl border border-[#f4b400]/30 bg-[#f4b400]/10 p-1 text-sm font-semibold text-white shadow-[0_10px_30px_rgba(0,0,0,0.18)] transition hover:border-[#f4b400]/60 hover:bg-[#f4b400]/15 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#f4b400]/70 sm:pr-4"
            >
              <span className="flex h-9 w-9 items-center justify-center rounded-xl bg-[#f4b400] text-[#06111f] shadow-[0_6px_16px_rgba(244,180,0,0.22)]">
                <UserRound className="h-4 w-4" />
              </span>
              <span className="hidden sm:inline">Profile</span>
            </Link>

            <button
              type="button"
              onClick={handleLogout}
              aria-label="Log out of PilotVault"
              title="Log out"
              className="group flex h-11 w-11 items-center justify-center rounded-2xl border border-[#1e3a5f] bg-[#081726] text-gray-400 shadow-[0_10px_30px_rgba(0,0,0,0.18)] transition hover:border-[#f4b400]/50 hover:bg-[#0b1d30] hover:text-[#f4b400] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#f4b400]/70"
            >
              <LogOut className="h-[18px] w-[18px] transition-transform group-hover:translate-x-0.5" />
            </button>
          </div>
        </div>
      </header>

      <section className="mx-auto max-w-7xl px-4 py-8 sm:px-6 sm:py-10 lg:px-8">
        <div className="mb-6 rounded-3xl border border-[#1e3a5f] bg-[#081726] p-5 sm:mb-8 sm:p-8">
          <p className="text-xs uppercase tracking-[0.25em] text-[#f4b400]">
            Practice Center
          </p>

          <h2 className="mt-3 text-2xl font-bold leading-tight sm:text-4xl">
            Choose a subject
          </h2>

          <p className="mt-3 max-w-2xl text-sm leading-6 text-gray-400 sm:text-base">
            Select a subject to begin your SACAA exam preparation.
          </p>
        </div>

        <div className="grid grid-cols-2 gap-3 sm:gap-5 lg:grid-cols-4">
          {subjects.map((subject) => {
            const Icon = subject.icon
            const unlocked = hasSubjectAccess(subject.slug)

            return (
              <Link
                key={subject.slug}
                href={
                  unlocked
                    ? `/practice/${subject.slug}`
                    : `/upgrade?subject=${subject.slug}`
                }
                className={`group min-h-[142px] rounded-2xl border bg-[#081726] p-4 transition-all hover:-translate-y-1 hover:border-[#f4b400] sm:min-h-[178px] sm:p-6 ${
                  unlocked
                    ? "border-[#f4b400]/40"
                    : "border-[#1e3a5f] opacity-50"
                }`}
              >
                <div
                  className={`flex h-10 w-10 items-center justify-center rounded-xl sm:h-12 sm:w-12 ${
                    unlocked ? "bg-[#f4b400]/20" : "bg-[#f4b400]/10"
                  }`}
                >
                  <Icon
                    className={`h-5 w-5 sm:h-6 sm:w-6 ${
                      unlocked ? "text-[#f4b400]" : "text-[#f4b400]/50"
                    }`}
                  />
                </div>

                <h3
                  className={`mt-4 text-sm font-bold leading-snug sm:mt-5 sm:text-lg ${
                    unlocked ? "text-white" : "text-gray-500"
                  }`}
                >
                  {subject.name}
                </h3>
              </Link>
            )
          })}
        </div>
      </section>
    </main>
  )
}
