"use client"

import { useEffect, useMemo, useState } from "react"
import Link from "next/link"
import { useRouter } from "next/navigation"
import {
  ArrowRight,
  BarChart3,
  BookOpen,
  Brain,
  ClipboardList,
  Cloud,
  Compass,
  LockKeyhole,
  LogOut,
  Map,
  Plane,
  Radio,
  Scale,
  Trophy,
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
  return subjects.find((subject) => subject.slug === slug)?.name ??
    slug
      .split("-")
      .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
      .join(" ")
}

function getFirstName(fullName: string | undefined) {
  return fullName?.trim().split(/\s+/)[0] || "Pilot"
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
        <div className="mx-auto max-w-xl rounded-3xl border border-red-200 bg-white p-6 shadow-sm sm:p-8">
          <p className="text-xs font-semibold uppercase tracking-[0.25em] text-red-600">
            Dashboard Error
          </p>
          <h1 className="mt-3 text-2xl font-bold">
            Your dashboard could not be loaded.
          </h1>
          <p className="mt-3 text-sm leading-6 text-slate-600">{loadError}</p>
          <button
            type="button"
            onClick={() => window.location.reload()}
            className="mt-6 rounded-xl bg-[#1f4e79] px-5 py-3 text-sm font-bold text-white transition hover:bg-[#183d60]"
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
      <header className="border-b border-white/15 bg-[#1f4e79] text-white shadow-sm">
        <div className="mx-auto flex min-h-16 max-w-7xl items-center justify-between gap-3 px-4 sm:min-h-20 sm:px-6 lg:px-8">
          <div className="min-w-0">
            <p className="text-[10px] font-semibold uppercase tracking-[0.22em] text-[#d6e6f7] sm:text-xs sm:tracking-[0.25em]">
              PilotVault SA
            </p>
            <h1 className="mt-1 truncate text-base font-bold sm:text-lg">
              Student Dashboard
            </h1>
          </div>

          <div className="flex shrink-0 items-center gap-2">
            <Link
              href="/profile"
              aria-label="Open profile"
              title="Open profile"
              className="group flex h-11 items-center gap-2 rounded-2xl border border-white/20 bg-white/10 p-1 text-sm font-semibold text-white transition hover:bg-white/15 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-white/60 sm:pr-4"
            >
              <span className="flex h-9 w-9 items-center justify-center rounded-xl bg-white text-[#1f4e79] shadow-sm">
                <UserRound className="h-4 w-4" />
              </span>
              <span className="hidden sm:inline">Profile</span>
            </Link>

            <button
              type="button"
              onClick={handleLogout}
              aria-label="Log out of PilotVault"
              title="Log out"
              className="group flex h-11 w-11 items-center justify-center rounded-2xl border border-white/20 bg-white/10 text-blue-50 transition hover:bg-white/15 hover:text-white focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-white/60"
            >
              <LogOut className="h-[18px] w-[18px] transition-transform group-hover:translate-x-0.5" />
            </button>
          </div>
        </div>
      </header>

      <section className="mx-auto max-w-7xl px-4 py-6 sm:px-6 sm:py-8 lg:px-8 lg:py-10">
        <div className="overflow-hidden rounded-3xl border border-[#c8d8e8] bg-[#dce8f3] shadow-[0_14px_40px_rgba(31,78,121,0.08)]">
          <div className="grid lg:grid-cols-[1.25fr_0.75fr]">
            <div className="p-5 sm:p-8 lg:p-10">
              <div className="flex flex-wrap gap-2">
                <span className="rounded-full border border-[#1f4e79]/15 bg-white/70 px-3 py-1 text-[10px] font-bold uppercase tracking-[0.18em] text-[#1f4e79]">
                  {licenceLabel}
                </span>
                <span className="rounded-full border border-[#1f4e79]/15 bg-white/70 px-3 py-1 text-[10px] font-bold uppercase tracking-[0.18em] text-slate-600">
                  {planLabel}
                </span>
              </div>

              <h2 className="mt-5 text-3xl font-bold tracking-tight text-slate-950 sm:text-4xl">
                Welcome back, {firstName}.
              </h2>
              <p className="mt-3 max-w-xl text-sm leading-6 text-slate-600 sm:text-base">
                Pick up where you left off, track your mock exam performance and focus your next study session.
              </p>

              <div className="mt-6 flex flex-col gap-3 sm:flex-row">
                <Link
                  href={
                    latestSubject && latestSubjectUnlocked
                      ? `/practice/${latestSubject}`
                      : "/practice"
                  }
                  className="inline-flex items-center justify-center gap-2 rounded-xl bg-[#1f4e79] px-5 py-3 text-sm font-bold text-white shadow-sm transition hover:bg-[#183d60]"
                >
                  {latestSubject ? "Continue training" : "Start practising"}
                  <ArrowRight className="h-4 w-4" />
                </Link>
                <Link
                  href="/profile"
                  className="inline-flex items-center justify-center gap-2 rounded-xl border border-[#1f4e79]/20 bg-white/70 px-5 py-3 text-sm font-bold text-[#1f4e79] transition hover:bg-white"
                >
                  <BarChart3 className="h-4 w-4" />
                  View performance
                </Link>
              </div>
            </div>

            <div className="border-t border-[#c8d8e8] bg-[#183d60] p-5 text-white sm:p-7 lg:border-l lg:border-t-0 lg:p-8">
              {dashboardStats.latestAttempt ? (
                <>
                  <p className="text-[10px] font-bold uppercase tracking-[0.2em] text-blue-200">
                    Latest mock exam
                  </p>
                  <p className="mt-3 text-xl font-bold">
                    {formatSubjectName(dashboardStats.latestAttempt.subject)}
                  </p>
                  <div className="mt-6 flex items-end justify-between gap-5">
                    <div>
                      <p className="text-4xl font-black tracking-tight">
                        {dashboardStats.latestAttempt.scorePercentage}%
                      </p>
                      <p className="mt-1 text-xs text-blue-100/80">Latest score</p>
                    </div>
                    <Link
                      href={
                        latestSubjectUnlocked
                          ? `/practice/${dashboardStats.latestAttempt.subject}`
                          : "/practice"
                      }
                      className="flex h-11 w-11 items-center justify-center rounded-xl bg-white text-[#183d60] transition hover:-translate-y-0.5"
                      aria-label="Open latest subject"
                    >
                      <ArrowRight className="h-5 w-5" />
                    </Link>
                  </div>
                </>
              ) : (
                <>
                  <p className="text-[10px] font-bold uppercase tracking-[0.2em] text-blue-200">
                    Your training record
                  </p>
                  <ClipboardList className="mt-5 h-9 w-9 text-blue-200" />
                  <p className="mt-4 text-xl font-bold">No mock exams yet</p>
                  <p className="mt-2 text-sm leading-6 text-blue-100/80">
                    Complete your first mock exam and your performance snapshot will appear here.
                  </p>
                </>
              )}
            </div>
          </div>
        </div>

        <div className="mt-5 grid grid-cols-2 gap-3 lg:grid-cols-4">
          <div className="rounded-2xl border border-slate-200/90 bg-white p-4 shadow-sm sm:p-5">
            <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-[#d6e6f7] text-[#1f4e79]">
              <BarChart3 className="h-4 w-4" />
            </div>
            <p className="mt-4 text-2xl font-black text-slate-950">
              {dashboardStats.overallAverage === null
                ? "—"
                : `${dashboardStats.overallAverage}%`}
            </p>
            <p className="mt-1 text-xs font-medium text-slate-500">Overall mock average</p>
          </div>

          <div className="rounded-2xl border border-slate-200/90 bg-white p-4 shadow-sm sm:p-5">
            <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-[#d6e6f7] text-[#1f4e79]">
              <ClipboardList className="h-4 w-4" />
            </div>
            <p className="mt-4 text-2xl font-black text-slate-950">{attempts.length}</p>
            <p className="mt-1 text-xs font-medium text-slate-500">Completed mock exams</p>
          </div>

          <div className="rounded-2xl border border-slate-200/90 bg-white p-4 shadow-sm sm:p-5">
            <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-[#d6e6f7] text-[#1f4e79]">
              <BookOpen className="h-4 w-4" />
            </div>
            <p className="mt-4 text-2xl font-black text-slate-950">
              {dashboardStats.practicedSubjects}/8
            </p>
            <p className="mt-1 text-xs font-medium text-slate-500">Subjects practised</p>
          </div>

          <div className="rounded-2xl border border-slate-200/90 bg-white p-4 shadow-sm sm:p-5">
            <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-[#d6e6f7] text-[#1f4e79]">
              <Trophy className="h-4 w-4" />
            </div>
            <p className="mt-4 truncate text-lg font-black text-slate-950 sm:text-xl">
              {dashboardStats.strongestSubject
                ? formatSubjectName(dashboardStats.strongestSubject[0])
                : "—"}
            </p>
            <p className="mt-1 text-xs font-medium text-slate-500">Strongest mock subject</p>
          </div>
        </div>

        <div className="mt-8 flex flex-col gap-2 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <p className="text-[10px] font-bold uppercase tracking-[0.22em] text-[#1f4e79]">
              Practice Center
            </p>
            <h2 className="mt-2 text-2xl font-bold tracking-tight text-slate-950 sm:text-3xl">
              Choose a subject
            </h2>
            <p className="mt-2 text-sm text-slate-600">
              Your mock performance is shown on each subject as you build your history.
            </p>
          </div>
        </div>

        <div className="mt-5 grid grid-cols-2 gap-3 sm:gap-5 lg:grid-cols-4">
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
                className={`group relative flex min-h-[165px] flex-col overflow-hidden rounded-2xl border p-4 shadow-[0_6px_18px_rgba(15,23,42,0.04)] transition-all hover:-translate-y-1 hover:shadow-[0_14px_30px_rgba(31,78,121,0.10)] sm:min-h-[205px] sm:p-5 ${
                  unlocked
                    ? "border-slate-200/90 bg-[#f7f9fc] hover:border-[#1f4e79]/45 hover:bg-white"
                    : "border-slate-200/80 bg-[#f4f6f8] opacity-65"
                }`}
              >
                <div className="flex items-start justify-between gap-3">
                  <div
                    className={`flex h-11 w-11 items-center justify-center rounded-xl sm:h-12 sm:w-12 ${
                      unlocked
                        ? "bg-[#cfe0f1] text-[#1f4e79]"
                        : "bg-slate-200 text-slate-400"
                    }`}
                  >
                    <Icon className="h-5 w-5 sm:h-6 sm:w-6" />
                  </div>

                  {unlocked ? (
                    <span className="rounded-full bg-[#e4edf6] px-2.5 py-1 text-[9px] font-bold uppercase tracking-[0.12em] text-[#1f4e79]">
                      Open
                    </span>
                  ) : (
                    <LockKeyhole className="h-4 w-4 text-slate-400" />
                  )}
                </div>

                <h3
                  className={`mt-4 text-sm font-bold leading-snug sm:text-lg ${
                    unlocked ? "text-slate-950" : "text-slate-500"
                  }`}
                >
                  {subject.name}
                </h3>

                <div className="mt-auto flex items-end justify-between gap-2 pt-5">
                  <div>
                    {stats?.count ? (
                      <>
                        <p className="text-lg font-black text-[#1f4e79]">
                          {stats.average}%
                        </p>
                        <p className="text-[10px] text-slate-500">
                          {stats.count} mock{stats.count === 1 ? "" : "s"}
                        </p>
                      </>
                    ) : (
                      <p className="text-[10px] font-medium text-slate-400">
                        No mock history yet
                      </p>
                    )}
                  </div>

                  {unlocked && (
                    <span className="flex h-8 w-8 items-center justify-center rounded-lg border border-slate-200 bg-white text-[#1f4e79] transition group-hover:border-[#1f4e79]/30 group-hover:bg-[#1f4e79] group-hover:text-white">
                      <ArrowRight className="h-4 w-4" />
                    </span>
                  )}
                </div>
              </Link>
            )
          })}
        </div>
      </section>
    </main>
  )
}
