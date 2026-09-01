"use client"

import { useEffect, useMemo, useState } from "react"
import Image from "next/image"
import Link from "next/link"
import { useRouter } from "next/navigation"
import {
  Brain,
  ChevronRight,
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

function scoreClassName(score: number) {
  if (score >= 75) return "text-emerald-700"
  if (score >= 65) return "text-amber-700"
  return "text-slate-900"
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
        <div className="mx-auto max-w-xl rounded-xl border border-red-200 bg-[#f8fafc] p-6 sm:p-8">
          <p className="text-xs font-semibold uppercase tracking-[0.16em] text-red-600">
            Dashboard error
          </p>
          <h1 className="mt-3 text-2xl font-bold">
            Your dashboard could not be loaded.
          </h1>
          <p className="mt-3 text-sm leading-6 text-slate-600">{loadError}</p>
          <button
            type="button"
            onClick={() => window.location.reload()}
            className="mt-6 min-h-11 rounded-lg bg-[#1f4e79] px-5 py-2.5 text-sm font-semibold text-white transition hover:bg-[#183d60]"
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
        <div className="mx-auto flex h-16 max-w-7xl items-center justify-between gap-3 px-4 sm:h-[72px] sm:px-6 lg:px-8">
          <div className="flex min-w-0 items-center gap-3">
            <Link href="/dashboard" className="shrink-0" aria-label="PilotVault dashboard">
              <Image
                src="/images/Header logo.png"
                alt="PilotVault SA"
                width={180}
                height={54}
                className="h-auto w-[132px] object-contain sm:w-[154px]"
                priority
              />
            </Link>
            <span className="hidden h-7 w-px bg-white/20 sm:block" />
            <span className="hidden text-sm font-medium text-blue-50/90 sm:block">
              Dashboard
            </span>
          </div>

          <div className="flex shrink-0 items-center gap-2">
            <Link
              href="/profile"
              aria-label="Open profile"
              title="Profile"
              className="flex h-11 min-w-11 items-center justify-center gap-2 rounded-lg border border-white/20 px-3 text-sm font-medium text-white transition hover:bg-white/10 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-white/70"
            >
              <UserRound className="h-[18px] w-[18px]" />
              <span className="hidden md:inline">Profile</span>
            </Link>
            <button
              type="button"
              onClick={handleLogout}
              aria-label="Log out"
              title="Log out"
              className="flex h-11 w-11 items-center justify-center rounded-lg border border-white/20 text-blue-50 transition hover:bg-white/10 hover:text-white focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-white/70"
            >
              <LogOut className="h-[18px] w-[18px]" />
            </button>
          </div>
        </div>
      </header>

      <div className="mx-auto max-w-7xl px-4 pb-[max(2rem,env(safe-area-inset-bottom))] pt-6 sm:px-6 sm:pt-8 lg:px-8 lg:pt-9">
        <section aria-labelledby="dashboard-heading">
          <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
            <div className="min-w-0">
              <p className="text-sm font-medium text-slate-500">Welcome back, {firstName}</p>
              <h1
                id="dashboard-heading"
                className="mt-1 text-[28px] font-bold leading-tight tracking-tight text-slate-950 sm:text-3xl"
              >
                Practice centre
              </h1>
              <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-600">
                Choose a subject, continue studying, or review your latest mock exam results.
              </p>
            </div>

            <div className="flex items-center gap-2 text-xs text-slate-600 sm:justify-end">
              <span className="font-semibold text-slate-900">{licenceLabel}</span>
              <span className="text-slate-400">•</span>
              <span>{planLabel}</span>
            </div>
          </div>

          {dashboardStats.latestAttempt && latestSubjectUnlocked && (
            <div className="mt-6 flex flex-col gap-4 rounded-xl border border-[#c9d8e6] bg-[#e4edf5] p-4 sm:flex-row sm:items-center sm:justify-between sm:p-5">
              <div className="min-w-0">
                <p className="text-[11px] font-semibold uppercase tracking-[0.12em] text-[#1f4e79]">
                  Continue studying
                </p>
                <div className="mt-1 flex min-w-0 flex-wrap items-baseline gap-x-3 gap-y-1">
                  <h2 className="truncate text-base font-semibold text-slate-950 sm:text-lg">
                    {formatSubjectName(latestSubject)}
                  </h2>
                  <span className={`text-sm font-semibold ${scoreClassName(dashboardStats.latestAttempt.scorePercentage)}`}>
                    Last mock {dashboardStats.latestAttempt.scorePercentage}%
                  </span>
                </div>
              </div>
              <Link
                href={`/practice/${latestSubject}`}
                className="inline-flex min-h-11 w-full shrink-0 items-center justify-center gap-1.5 rounded-lg bg-[#1f4e79] px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-[#183d60] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#1f4e79]/40 sm:w-auto"
              >
                Open subject
                <ChevronRight className="h-4 w-4" />
              </Link>
            </div>
          )}

          <dl className="mt-5 grid grid-cols-3 overflow-hidden rounded-xl border border-[#cfdae5] bg-[#f4f7fa]">
            <div className="min-w-0 px-3 py-3.5 sm:px-5 sm:py-4">
              <dt className="truncate text-[10px] font-medium uppercase tracking-[0.08em] text-slate-500 sm:text-[11px]">
                Mock avg
              </dt>
              <dd className="mt-1 text-xl font-bold tabular-nums text-slate-950 sm:text-2xl">
                {dashboardStats.overallAverage === null
                  ? "—"
                  : `${dashboardStats.overallAverage}%`}
              </dd>
            </div>
            <div className="min-w-0 border-l border-[#cfdae5] px-3 py-3.5 sm:px-5 sm:py-4">
              <dt className="truncate text-[10px] font-medium uppercase tracking-[0.08em] text-slate-500 sm:text-[11px]">
                Mocks
              </dt>
              <dd className="mt-1 text-xl font-bold tabular-nums text-slate-950 sm:text-2xl">
                {attempts.length}
              </dd>
            </div>
            <div className="min-w-0 border-l border-[#cfdae5] px-3 py-3.5 sm:px-5 sm:py-4">
              <dt className="truncate text-[10px] font-medium uppercase tracking-[0.08em] text-slate-500 sm:text-[11px]">
                Subjects
              </dt>
              <dd className="mt-1 text-xl font-bold tabular-nums text-slate-950 sm:text-2xl">
                {dashboardStats.practicedSubjects}/8
              </dd>
            </div>
          </dl>
        </section>

        <div className="mt-7 grid gap-8 lg:grid-cols-[minmax(0,1fr)_20rem] lg:items-start">
          <section aria-labelledby="subjects-heading">
            <div className="mb-3 flex items-end justify-between gap-4">
              <div>
                <h2 id="subjects-heading" className="text-base font-semibold text-slate-950">
                  Subjects
                </h2>
                <p className="mt-1 text-xs text-slate-500">Select a subject to start training.</p>
              </div>
            </div>

            <div className="grid grid-cols-1 gap-2.5 sm:grid-cols-2">
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
                    className={`group flex min-h-[88px] items-center gap-3 rounded-xl border px-3.5 py-3.5 transition focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#1f4e79]/35 sm:px-4 ${
                      unlocked
                        ? "border-[#d2dde7] bg-[#f8fafc] hover:border-[#9fb6ca] hover:bg-white"
                        : "border-[#dbe3ea] bg-[#f1f4f7] opacity-65"
                    }`}
                  >
                    <div
                      className={`flex h-11 w-11 shrink-0 items-center justify-center rounded-lg ${
                        unlocked
                          ? "bg-[#d6e6f7] text-[#1f4e79]"
                          : "bg-slate-200 text-slate-400"
                      }`}
                    >
                      <Icon className="h-5 w-5" />
                    </div>

                    <div className="min-w-0 flex-1">
                      <h3
                        className={`text-sm font-semibold leading-snug ${
                          unlocked ? "text-slate-950" : "text-slate-500"
                        }`}
                      >
                        {subject.name}
                      </h3>
                      <p className="mt-1 text-[11px] leading-4 text-slate-500">
                        {stats?.count
                          ? `${stats.average}% average · ${stats.count} mock${stats.count === 1 ? "" : "s"}`
                          : unlocked
                            ? "No mock history yet"
                            : "Upgrade required"}
                      </p>
                    </div>

                    {unlocked ? (
                      <ChevronRight className="h-4 w-4 shrink-0 text-slate-400 transition group-hover:translate-x-0.5 group-hover:text-[#1f4e79]" />
                    ) : (
                      <LockKeyhole className="h-4 w-4 shrink-0 text-slate-400" />
                    )}
                  </Link>
                )
              })}
            </div>
          </section>

          <aside className="space-y-4 lg:sticky lg:top-5" aria-label="Dashboard summary">
            <section className="rounded-xl border border-[#d2dde7] bg-[#f8fafc] p-4 sm:p-5">
              <div className="flex items-center justify-between gap-3">
                <h2 className="text-sm font-semibold text-slate-950">Recent mocks</h2>
                <Link
                  href="/profile"
                  className="min-h-10 px-1 py-2 text-xs font-semibold text-[#1f4e79] hover:text-[#183d60]"
                >
                  View all
                </Link>
              </div>

              {attempts.length ? (
                <div className="mt-2 divide-y divide-slate-200">
                  {attempts.slice(0, 4).map((attempt) => (
                    <div
                      key={attempt.id}
                      className="flex min-h-[52px] items-center justify-between gap-3 py-2.5"
                    >
                      <div className="min-w-0">
                        <p className="truncate text-xs font-medium text-slate-800">
                          {formatSubjectName(attempt.subject)}
                        </p>
                        <p className="mt-0.5 text-[10px] text-slate-500">
                          {formatShortDate(attempt.completedAt)}
                        </p>
                      </div>
                      <p className={`shrink-0 text-sm font-semibold tabular-nums ${scoreClassName(attempt.scorePercentage)}`}>
                        {attempt.scorePercentage}%
                      </p>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="mt-3 text-xs leading-5 text-slate-500">
                  Completed mock exams will appear here.
                </p>
              )}
            </section>

            <section className="rounded-xl border border-[#cbd8e4] bg-[#e4edf5] p-4 sm:p-5">
              <h2 className="text-sm font-semibold text-slate-950">Performance summary</h2>
              <dl className="mt-3 divide-y divide-[#cbd8e4] text-xs">
                <div className="flex items-center justify-between gap-3 py-2 first:pt-0">
                  <dt className="text-slate-500">Overall average</dt>
                  <dd className="font-semibold tabular-nums text-slate-900">
                    {dashboardStats.overallAverage === null
                      ? "—"
                      : `${dashboardStats.overallAverage}%`}
                  </dd>
                </div>
                <div className="flex items-center justify-between gap-3 py-2">
                  <dt className="text-slate-500">Strongest subject</dt>
                  <dd className="max-w-[158px] truncate text-right font-semibold text-slate-900">
                    {dashboardStats.strongestSubject
                      ? formatSubjectName(dashboardStats.strongestSubject[0])
                      : "—"}
                  </dd>
                </div>
                <div className="flex items-center justify-between gap-3 py-2 last:pb-0">
                  <dt className="text-slate-500">Latest mock</dt>
                  <dd className="font-semibold tabular-nums text-slate-900">
                    {dashboardStats.latestAttempt
                      ? `${dashboardStats.latestAttempt.scorePercentage}%`
                      : "—"}
                  </dd>
                </div>
              </dl>
            </section>
          </aside>
        </div>
      </div>
    </main>
  )
}
