"use client"

import { useEffect, useMemo, useState } from "react"
import Link from "next/link"
import { useRouter } from "next/navigation"
import {
  Brain,
  Cloud,
  Compass,
  LockKeyhole,
  LogOut,
  Map,
  Plane,
  Radio,
  Scale,
  UserRound,
  Wrench,
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
import {
  fetchMockExamAttempts,
  type MockExamAttempt,
} from "../profile/exam-attempt-service"

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

function formatSubjectName(slug: string) {
  return (
    subjects.find((subject) => subject.slug === slug)?.name ??
    slug
      .split("-")
      .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
      .join(" ")
  )
}

function getFirstName(fullName: string | undefined) {
  return fullName?.trim().split(/\s+/)[0] || "Pilot"
}

function formatShortDate(value: string) {
  return new Intl.DateTimeFormat("en-ZA", {
    day: "2-digit",
    month: "short",
  }).format(new Date(value))
}

export default function DashboardPage() {
  const router = useRouter()
  const [loading, setLoading] = useState(true)
  const [loadError, setLoadError] = useState("")
  const [profile, setProfile] = useState<CachedProfile | null>(null)
  const [subjectAccess, setSubjectAccess] = useState<CachedSubjectAccess[]>([])
  const [attempts, setAttempts] = useState<MockExamAttempt[]>([])

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

        const [profileData, accessData, attemptData] = await Promise.all([
          getCachedProfile(user.id),
          getCachedSubjectAccess(user.id),
          fetchMockExamAttempts(user.id).catch(() => []),
        ])

        if (!cancelled) {
          setProfile(profileData)
          setSubjectAccess(accessData)
          setAttempts(attemptData)
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

  const dashboardStats = useMemo(() => {
    const overallAverage = attempts.length
      ? Math.round(
          attempts.reduce((sum, attempt) => sum + attempt.scorePercentage, 0) /
            attempts.length
        )
      : null

    const practicedSubjects = new Set(attempts.map((attempt) => attempt.subject)).size

    const perSubject = Object.fromEntries(
      subjects.map((subject) => {
        const subjectAttempts = attempts.filter(
          (attempt) => attempt.subject === subject.slug
        )
        const average = subjectAttempts.length
          ? Math.round(
              subjectAttempts.reduce(
                (sum, attempt) => sum + attempt.scorePercentage,
                0
              ) / subjectAttempts.length
            )
          : null

        return [
          subject.slug,
          {
            count: subjectAttempts.length,
            average,
          },
        ]
      })
    ) as Record<string, { count: number; average: number | null }>

    const strongestSubject = Object.entries(perSubject)
      .filter(([, stats]) => stats.average !== null)
      .sort((a, b) => (b[1].average ?? 0) - (a[1].average ?? 0))[0]

    return {
      overallAverage,
      practicedSubjects,
      perSubject,
      strongestSubject,
      latestAttempt: attempts[0] ?? null,
    }
  }, [attempts])

  if (loading || (!profile && !loadError)) {
    return <PageSkeleton variant="dashboard" />
  }

  if (loadError) {
    return (
      <main className="min-h-screen bg-[#eef3f8] px-4 py-10 text-slate-900 sm:px-6">
        <div className="mx-auto max-w-xl rounded-2xl border border-red-200 bg-[#f8fafc] p-6 sm:p-8">
          <p className="text-xs font-semibold uppercase tracking-[0.18em] text-red-600">
            Dashboard error
          </p>
          <h1 className="mt-3 text-2xl font-bold">
            Your dashboard could not be loaded.
          </h1>
          <p className="mt-3 text-sm leading-6 text-slate-600">{loadError}</p>
          <button
            type="button"
            onClick={() => window.location.reload()}
            className="mt-6 rounded-lg bg-[#1f4e79] px-5 py-2.5 text-sm font-semibold text-white transition hover:bg-[#183d60]"
          >
            Try again
          </button>
        </div>
      </main>
    )
  }

  const firstName = getFirstName(profile?.full_name)
  const licenceLabel = profile?.licence_level?.toUpperCase() ?? "STUDENT"
  const planLabel = isTrialUser
    ? "Free Trial"
    : isPplUser
      ? "PPL Pack"
      : profile?.subscription_plan
        ? profile.subscription_plan.toUpperCase()
        : "Student Access"

  const latestSubject = dashboardStats.latestAttempt?.subject
  const latestSubjectUnlocked = latestSubject
    ? hasSubjectAccess(latestSubject)
    : false

  return (
    <main className="min-h-screen bg-[#eef3f8] text-slate-900">
      <header className="border-b border-white/15 bg-[#1f4e79] text-white">
        <div className="mx-auto flex h-16 max-w-7xl items-center justify-between gap-3 px-4 sm:h-18 sm:px-6 lg:px-8">
          <div className="min-w-0">
            <p className="text-[10px] font-semibold uppercase tracking-[0.2em] text-[#d6e6f7] sm:text-xs">
              PilotVault SA
            </p>
            <h1 className="mt-0.5 truncate text-base font-semibold sm:text-lg">
              Dashboard
            </h1>
          </div>

          <div className="flex shrink-0 items-center gap-2">
            <Link
              href="/profile"
              aria-label="Open profile"
              className="flex h-10 items-center gap-2 rounded-lg border border-white/20 px-3 text-sm font-medium text-white transition hover:bg-white/10"
            >
              <UserRound className="h-4 w-4" />
              <span className="hidden sm:inline">Profile</span>
            </Link>
            <button
              type="button"
              onClick={handleLogout}
              aria-label="Log out"
              className="flex h-10 w-10 items-center justify-center rounded-lg border border-white/20 text-blue-50 transition hover:bg-white/10 hover:text-white"
            >
              <LogOut className="h-4 w-4" />
            </button>
          </div>
        </div>
      </header>

      <section className="mx-auto max-w-7xl px-4 py-7 sm:px-6 sm:py-9 lg:px-8">
        <div className="mb-6 flex flex-col gap-4 border-b border-[#d5e0ea] pb-6 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <p className="text-sm text-slate-500">Welcome back, {firstName}</p>
            <h2 className="mt-1 text-2xl font-bold tracking-tight text-slate-950 sm:text-3xl">
              Practice centre
            </h2>
          </div>

          <div className="flex flex-wrap items-center gap-x-5 gap-y-2 text-xs text-slate-600">
            <span><strong className="font-semibold text-slate-900">{licenceLabel}</strong> licence</span>
            <span className="hidden h-4 w-px bg-slate-300 sm:block" />
            <span><strong className="font-semibold text-slate-900">{planLabel}</strong></span>
            {latestSubject && latestSubjectUnlocked && (
              <Link
                href={`/practice/${latestSubject}`}
                className="font-semibold text-[#1f4e79] hover:text-[#183d60]"
              >
                Continue {formatSubjectName(latestSubject)}
              </Link>
            )}
          </div>
        </div>

        <div className="mb-7 grid grid-cols-3 overflow-hidden rounded-xl border border-[#cfdae5] bg-[#e5edf5]">
          <div className="px-4 py-3 sm:px-5 sm:py-4">
            <p className="text-[10px] uppercase tracking-[0.12em] text-slate-500">Mock average</p>
            <p className="mt-1 text-lg font-bold text-slate-950 sm:text-xl">
              {dashboardStats.overallAverage === null ? "—" : `${dashboardStats.overallAverage}%`}
            </p>
          </div>
          <div className="border-l border-[#cfdae5] px-4 py-3 sm:px-5 sm:py-4">
            <p className="text-[10px] uppercase tracking-[0.12em] text-slate-500">Mock exams</p>
            <p className="mt-1 text-lg font-bold text-slate-950 sm:text-xl">{attempts.length}</p>
          </div>
          <div className="border-l border-[#cfdae5] px-4 py-3 sm:px-5 sm:py-4">
            <p className="text-[10px] uppercase tracking-[0.12em] text-slate-500">Subjects used</p>
            <p className="mt-1 text-lg font-bold text-slate-950 sm:text-xl">
              {dashboardStats.practicedSubjects}/8
            </p>
          </div>
        </div>

        <div className="grid gap-7 lg:grid-cols-[minmax(0,1fr)_310px]">
          <div>
            <div className="mb-3 flex items-baseline justify-between gap-3">
              <h3 className="text-sm font-semibold text-slate-900">Subjects</h3>
              <p className="text-xs text-slate-500">Select a subject to study</p>
            </div>

            <div className="grid grid-cols-1 gap-2 sm:grid-cols-2 xl:grid-cols-3">
              {subjects.map((subject) => {
                const Icon = subject.icon
                const unlocked = hasSubjectAccess(subject.slug)
                const stats = dashboardStats.perSubject[subject.slug]

                return (
                  <Link
                    key={subject.slug}
                    href={
                      unlocked
                        ? `/practice/${subject.slug}`
                        : `/upgrade?subject=${subject.slug}`
                    }
                    className={`group flex min-h-[92px] items-center gap-3 rounded-xl border px-4 py-4 transition ${
                      unlocked
                        ? "border-[#d5e0ea] bg-[#f7f9fc] hover:border-[#9eb8cf] hover:bg-white"
                        : "border-[#dbe3ea] bg-[#f1f4f7] opacity-60"
                    }`}
                  >
                    <div
                      className={`flex h-10 w-10 shrink-0 items-center justify-center rounded-lg ${
                        unlocked
                          ? "bg-[#d6e6f7] text-[#1f4e79]"
                          : "bg-slate-200 text-slate-400"
                      }`}
                    >
                      <Icon className="h-5 w-5" />
                    </div>

                    <div className="min-w-0 flex-1">
                      <h4 className={`text-sm font-semibold leading-snug ${unlocked ? "text-slate-950" : "text-slate-500"}`}>
                        {subject.name}
                      </h4>
                      <p className="mt-1 text-[11px] text-slate-500">
                        {stats?.count
                          ? `${stats.average}% avg · ${stats.count} mock${stats.count === 1 ? "" : "s"}`
                          : "No mock history"}
                      </p>
                    </div>

                    {!unlocked && <LockKeyhole className="h-4 w-4 shrink-0 text-slate-400" />}
                  </Link>
                )
              })}
            </div>
          </div>

          <aside className="space-y-4">
            <section className="rounded-xl border border-[#d5e0ea] bg-[#f7f9fc] p-4">
              <div className="flex items-center justify-between gap-3">
                <h3 className="text-sm font-semibold text-slate-900">Recent mocks</h3>
                <Link href="/profile" className="text-xs font-medium text-[#1f4e79] hover:text-[#183d60]">
                  View all
                </Link>
              </div>

              {attempts.length ? (
                <div className="mt-3 divide-y divide-slate-200">
                  {attempts.slice(0, 4).map((attempt) => (
                    <div key={attempt.id} className="flex items-center justify-between gap-3 py-3 first:pt-1 last:pb-1">
                      <div className="min-w-0">
                        <p className="truncate text-xs font-medium text-slate-800">
                          {formatSubjectName(attempt.subject)}
                        </p>
                        <p className="mt-0.5 text-[10px] text-slate-500">
                          {formatShortDate(attempt.completedAt)}
                        </p>
                      </div>
                      <p className={`text-sm font-semibold ${attempt.scorePercentage >= 75 ? "text-emerald-700" : "text-slate-900"}`}>
                        {attempt.scorePercentage}%
                      </p>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="mt-3 text-xs leading-5 text-slate-500">
                  Your completed mock exams will appear here.
                </p>
              )}
            </section>

            <section className="rounded-xl border border-[#d5e0ea] bg-[#e5edf5] p-4">
              <h3 className="text-sm font-semibold text-slate-900">Performance</h3>
              <dl className="mt-3 space-y-2 text-xs">
                <div className="flex items-center justify-between gap-3">
                  <dt className="text-slate-500">Overall average</dt>
                  <dd className="font-semibold text-slate-900">
                    {dashboardStats.overallAverage === null ? "—" : `${dashboardStats.overallAverage}%`}
                  </dd>
                </div>
                <div className="flex items-center justify-between gap-3">
                  <dt className="text-slate-500">Strongest subject</dt>
                  <dd className="max-w-[150px] truncate text-right font-semibold text-slate-900">
                    {dashboardStats.strongestSubject
                      ? formatSubjectName(dashboardStats.strongestSubject[0])
                      : "—"}
                  </dd>
                </div>
                <div className="flex items-center justify-between gap-3">
                  <dt className="text-slate-500">Last mock</dt>
                  <dd className="font-semibold text-slate-900">
                    {dashboardStats.latestAttempt
                      ? `${dashboardStats.latestAttempt.scorePercentage}%`
                      : "—"}
                  </dd>
                </div>
              </dl>
            </section>
          </aside>
        </div>
      </section>
    </main>
  )
}
