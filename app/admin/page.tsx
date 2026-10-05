"use client"

import { useCallback, useEffect, useMemo, useState } from "react"
import Image from "next/image"
import Link from "next/link"
import { useRouter } from "next/navigation"
import { Eye, LayoutDashboard, LogOut, RefreshCw, Search, ShieldCheck } from "lucide-react"
import { PageSkeleton } from "@/components/page-skeleton"
import { clearClientDataCache } from "@/src/lib/client-data-cache"
import { supabase } from "@/src/lib/supabase"
import {
  ConversionFunnel,
  OverTimeCharts,
  TrialsEndingSoon,
  type FunnelCounts,
  type SeriesData,
} from "./insights"

const SUBJECTS = [
  { slug: "air-law", name: "Air Law" },
  { slug: "aircraft-technical-and-general", name: "Aircraft Technical and General" },
  { slug: "flight-planning", name: "Flight Planning" },
  { slug: "human-performance", name: "Human Performance" },
  { slug: "meteorology", name: "Meteorology" },
  { slug: "navigation", name: "Navigation" },
  { slug: "principles-of-flight", name: "Principles of Flight" },
  { slug: "radio-telephony", name: "Radio Telephony" },
]

type AdminUser = {
  id: string
  email: string | null
  fullName: string | null
  createdAt: string
  lastSignInAt: string | null
  emailConfirmed: boolean
  isAdmin: boolean
  isTestAccount: boolean
  licenceLevel: string | null
  subscriptionStatus: string | null
  subscriptionPlan: string | null
  paymentStatus: string | null
  trialEndsAt: string | null
  subscriptionExpiresAt: string | null
  subjectAccess: { subject: string; accessStatus: string | null; expiresAt: string | null }[]
  attemptCount: number
  lastAttemptAt: string | null
  subjectsTried: string[]
  fulfilledPayments: number
}

type Overview = {
  summary: {
    totalAccounts: number
    testAccounts: number
    signUps24h: number
    signUps7d: number
    signUps30d: number
    activeTrials: number
    activePplPacks: number
    fulfilledRevenueCents: number
  }
  funnel: FunnelCounts
  series: SeriesData
  users: AdminUser[]
  recentPayments: {
    reference: string
    email: string | null
    isTestOrAdmin: boolean
    productCode: string | null
    subject: string | null
    amountCents: number | null
    currency: string | null
    status: string | null
    paidAt: string | null
    createdAt: string
  }[]
}

type PreviewMode = "admin" | "ppl" | "trial" | "trial_expired" | "subject"

const PREVIEW_MODES: { mode: PreviewMode; label: string; detail: string }[] = [
  { mode: "admin", label: "Admin", detail: "Everything unlocked, no expiry" },
  { mode: "ppl", label: "Full PPL Pack", detail: "As a paying PPL Pack customer (3 months)" },
  { mode: "trial", label: "Trial", detail: "Fresh 3-day trial with trial mock questions" },
  { mode: "trial_expired", label: "Trial expired", detail: "Trial ended 1 hour ago: locked subjects, discount offer" },
  { mode: "subject", label: "Per subject", detail: "Only the ticked subjects (1 month each)" },
]

function currentPreviewMode(user: AdminUser | undefined): { mode: PreviewMode | null; label: string } {
  if (!user) return { mode: null, label: "Unknown" }
  if (user.paymentStatus === "admin") return { mode: "admin", label: "Admin" }

  if (user.subscriptionStatus === "active" && user.subscriptionPlan === "ppl") {
    return { mode: "ppl", label: "Full PPL Pack" }
  }

  if (user.subscriptionPlan === "trial") {
    return isFuture(user.trialEndsAt)
      ? { mode: "trial", label: "Trial" }
      : { mode: "trial_expired", label: "Trial expired" }
  }

  const owned = user.subjectAccess.filter(
    (access) => access.accessStatus === "active" && isFuture(access.expiresAt)
  )

  if (owned.length) {
    return {
      mode: "subject",
      label: `Per subject: ${owned.map((access) => subjectName(access.subject)).join(", ")}`,
    }
  }

  return { mode: null, label: "No access" }
}

type AccessRequest =
  | { action: "extend_trial"; days: number }
  | { action: "grant_ppl"; days: number }
  | { action: "grant_subject"; days: number; subject: string }
  | { action: "end_trial" }
  | { action: "revoke_ppl" }
  | { action: "revoke_subject"; subject: string }
  | { action: "set_test_account"; value: boolean }

function subjectName(slug: string) {
  return SUBJECTS.find((subject) => subject.slug === slug)?.name ?? slug
}

function formatDate(value: string | null, withTime = false) {
  if (!value) return "—"

  return new Intl.DateTimeFormat("en-ZA", {
    day: "2-digit",
    month: "short",
    year: "numeric",
    ...(withTime ? { hour: "2-digit", minute: "2-digit" } : {}),
    timeZone: "Africa/Johannesburg",
  }).format(new Date(value))
}

function formatRand(cents: number | null) {
  return new Intl.NumberFormat("en-ZA", {
    style: "currency",
    currency: "ZAR",
    maximumFractionDigits: 0,
  }).format((cents ?? 0) / 100)
}

function isFuture(value: string | null) {
  return Boolean(value) && new Date(value!).getTime() > Date.now()
}

function accessBadge(user: AdminUser) {
  if (user.isAdmin) return { label: "Admin", className: "bg-[#1f4e79] text-white" }

  if (
    user.subscriptionStatus === "active" &&
    user.subscriptionPlan === "ppl" &&
    isFuture(user.subscriptionExpiresAt)
  ) {
    return {
      label: `PPL Pack · until ${formatDate(user.subscriptionExpiresAt)}`,
      className: "bg-emerald-50 text-emerald-800 ring-1 ring-emerald-200",
    }
  }

  if (user.subscriptionPlan === "trial") {
    return isFuture(user.trialEndsAt)
      ? {
          label: `Trial · ends ${formatDate(user.trialEndsAt)}`,
          className: "bg-[#fdf3d9] text-[#8a6508] ring-1 ring-[#f4b400]/40",
        }
      : {
          label: `Trial ended ${formatDate(user.trialEndsAt)}`,
          className: "bg-slate-100 text-slate-600 ring-1 ring-slate-200",
        }
  }

  return { label: "No plan", className: "bg-slate-100 text-slate-600 ring-1 ring-slate-200" }
}

export default function AdminPage() {
  const router = useRouter()
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")
  const [forbidden, setForbidden] = useState(false)
  const [overview, setOverview] = useState<Overview | null>(null)
  const [query, setQuery] = useState("")
  const [showAdmins, setShowAdmins] = useState(false)
  const [showTest, setShowTest] = useState(false)
  const [busyUserId, setBusyUserId] = useState<string | null>(null)
  const [notice, setNotice] = useState("")
  const [myUserId, setMyUserId] = useState<string | null>(null)
  const [previewSubjects, setPreviewSubjects] = useState<string[]>(["air-law", "meteorology"])
  const [previewBusy, setPreviewBusy] = useState(false)
  const [previewNotice, setPreviewNotice] = useState("")

  const authorisedFetch = useCallback(
    async (input: string, init?: RequestInit) => {
      const { data } = await supabase.auth.getSession()
      const accessToken = data.session?.access_token

      if (!accessToken) {
        router.replace("/?login-required=1")
        return null
      }

      setMyUserId(data.session?.user.id ?? null)

      return fetch(input, {
        ...init,
        headers: {
          ...(init?.headers ?? {}),
          Authorization: `Bearer ${accessToken}`,
          "Content-Type": "application/json",
        },
      })
    },
    [router]
  )

  const loadOverview = useCallback(async () => {
    setError("")

    try {
      const response = await authorisedFetch("/api/admin/overview", { cache: "no-store" })

      if (!response) return

      if (response.status === 403) {
        setForbidden(true)
        return
      }

      const body = await response.json()

      if (!response.ok) throw new Error(body.error ?? "Could not load the admin overview.")

      setOverview(body as Overview)
    } catch (loadError) {
      setError(loadError instanceof Error ? loadError.message : "Could not load the admin overview.")
    } finally {
      setLoading(false)
    }
  }, [authorisedFetch])

  useEffect(() => {
    void loadOverview()
  }, [loadOverview])

  const handleLogout = async () => {
    clearClientDataCache()
    await supabase.auth.signOut()
    router.replace("/")
  }

  const runAction = async (user: AdminUser, request: AccessRequest, description: string) => {
    if (request.action !== "set_test_account" && !window.confirm(`${description} for ${user.email ?? "this account"}?`)) {
      return
    }

    setBusyUserId(user.id)
    setNotice("")

    try {
      const response = await authorisedFetch("/api/admin/access", {
        method: "POST",
        body: JSON.stringify({ ...request, userId: user.id }),
      })

      if (!response) return

      const body = await response.json()

      if (!response.ok) throw new Error(body.error ?? "The change could not be saved.")

      await loadOverview()
      setNotice(`${description} for ${user.email ?? "the account"}: done.`)
    } catch (actionError) {
      setNotice(actionError instanceof Error ? actionError.message : "The change could not be saved.")
    } finally {
      setBusyUserId(null)
    }
  }

  const switchPreview = async (mode: PreviewMode) => {
    setPreviewBusy(true)
    setPreviewNotice("")

    try {
      const response = await authorisedFetch("/api/admin/preview", {
        method: "POST",
        body: JSON.stringify({ mode, subjects: previewSubjects }),
      })

      if (!response) return

      const body = await response.json()

      if (!response.ok) throw new Error(body.error ?? "Could not switch the preview.")

      // The dashboard and practice pages cache the profile; drop it so they
      // pick up the new access straight away.
      clearClientDataCache()
      await loadOverview()
      setPreviewNotice(
        `Your account now has ${PREVIEW_MODES.find((item) => item.mode === mode)?.label ?? mode} access. Open the dashboard to try it.`
      )
    } catch (previewError) {
      setPreviewNotice(previewError instanceof Error ? previewError.message : "Could not switch the preview.")
    } finally {
      setPreviewBusy(false)
    }
  }

  const visibleUsers = useMemo(() => {
    const needle = query.trim().toLowerCase()

    return (overview?.users ?? []).filter((user) => {
      if (!showAdmins && user.isAdmin) return false
      if (!showTest && user.isTestAccount && !user.isAdmin) return false
      if (!needle) return true

      return [user.email, user.fullName].some((value) => value?.toLowerCase().includes(needle))
    })
  }, [overview, query, showAdmins, showTest])

  const trialUsers = useMemo(
    () =>
      (overview?.users ?? []).filter(
        (user) => !user.isAdmin && (showTest || !user.isTestAccount) && user.subscriptionPlan === "trial"
      ),
    [overview, showTest]
  )

  if (loading) return <PageSkeleton variant="dashboard" />

  if (forbidden) {
    return (
      <main className="flex min-h-screen items-center justify-center bg-[#f8fafc] px-4 text-slate-900">
        <div className="max-w-md rounded-xl border border-slate-200 bg-white p-6 text-center sm:p-8">
          <ShieldCheck className="mx-auto h-8 w-8 text-slate-400" />
          <h1 className="mt-3 text-xl font-bold">Admins only</h1>
          <p className="mt-2 text-sm text-slate-600">This page is only available to PilotVault admin accounts.</p>
          <Link
            href="/dashboard"
            className="mt-5 inline-flex min-h-11 items-center justify-center rounded-lg bg-[#1f4e79] px-5 text-sm font-semibold text-white hover:bg-[#183d60]"
          >
            Back to dashboard
          </Link>
        </div>
      </main>
    )
  }

  const summary = overview?.summary

  return (
    <main className="min-h-screen bg-[#f8fafc] text-slate-900">
      <header className="border-b border-white/15 bg-[#1f4e79] text-white">
        <div className="mx-auto flex h-16 max-w-7xl items-center justify-between gap-3 px-4 sm:h-20 sm:px-6 lg:px-8">
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
            <span className="hidden text-sm font-medium text-blue-50/90 sm:block">Admin</span>
          </div>

          <div className="flex shrink-0 items-center gap-2">
            <Link
              href="/dashboard"
              title="Dashboard"
              className="flex h-11 min-w-11 items-center justify-center gap-2 rounded-lg border border-white/20 px-3 text-sm font-medium text-white transition hover:bg-white/10"
            >
              <LayoutDashboard className="h-[18px] w-[18px]" />
              <span className="hidden md:inline">Dashboard</span>
            </Link>
            <button
              type="button"
              onClick={handleLogout}
              aria-label="Log out"
              title="Log out"
              className="flex h-11 w-11 items-center justify-center rounded-lg border border-white/20 text-blue-50 transition hover:bg-white/10 hover:text-white"
            >
              <LogOut className="h-[18px] w-[18px]" />
            </button>
          </div>
        </div>
      </header>

      <div className="mx-auto max-w-7xl px-4 pb-12 pt-6 sm:px-6 sm:pt-8 lg:px-8">
        <div className="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <h1 className="text-[28px] font-bold leading-tight tracking-tight text-slate-950 sm:text-3xl">
              Admin
            </h1>
            <p className="mt-1 text-sm text-slate-600">
              Sign-ups, access and payments. Numbers count real students only: admin and test accounts are left out
              {summary ? ` (${summary.testAccounts} test account${summary.testAccounts === 1 ? "" : "s"} hidden)` : ""}.
            </p>
          </div>
          <button
            type="button"
            onClick={() => {
              setLoading(true)
              void loadOverview()
            }}
            className="inline-flex min-h-10 items-center justify-center gap-2 rounded-lg border border-slate-300 bg-white px-3 text-sm font-semibold text-slate-700 hover:bg-slate-50"
          >
            <RefreshCw className="h-4 w-4" />
            Refresh
          </button>
        </div>

        {error && (
          <p className="mt-4 rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">{error}</p>
        )}

        {summary && (
          <section aria-label="Summary" className="mt-6 grid grid-cols-2 gap-3 sm:grid-cols-4 lg:grid-cols-7">
            {[
              ["Accounts", summary.totalAccounts],
              ["Sign-ups 24 h", summary.signUps24h],
              ["Sign-ups 7 days", summary.signUps7d],
              ["Sign-ups 30 days", summary.signUps30d],
              ["Active trials", summary.activeTrials],
              ["Active PPL Packs", summary.activePplPacks],
              ["Revenue (paid)", formatRand(summary.fulfilledRevenueCents)],
            ].map(([label, value]) => (
              <div key={label} className="rounded-xl border border-slate-200 bg-white p-4">
                <p className="text-[11px] font-semibold uppercase tracking-[0.12em] text-slate-500">{label}</p>
                <p className="mt-1 text-2xl font-bold tabular-nums text-slate-950">{value}</p>
              </div>
            ))}
          </section>
        )}

        {overview && (
          <>
            <div className="mt-6 grid gap-4 lg:grid-cols-2">
              <ConversionFunnel funnel={overview.funnel} />
              <TrialsEndingSoon users={trialUsers} subjectName={subjectName} />
            </div>
            <div className="mt-4">
              <OverTimeCharts series={overview.series} />
            </div>
          </>
        )}

        <section
          id="preview"
          aria-labelledby="preview-heading"
          className="mt-8 rounded-xl border border-slate-200 bg-white p-4 sm:p-5"
        >
          <div className="flex flex-col gap-1 sm:flex-row sm:items-center sm:justify-between">
            <h2 id="preview-heading" className="flex items-center gap-2 text-base font-semibold text-slate-950">
              <Eye className="h-4 w-4 text-[#1f4e79]" />
              Preview access
            </h2>
            <p className="text-sm text-slate-600">
              Your account now:{" "}
              <span className="font-semibold text-slate-950">
                {currentPreviewMode(overview?.users.find((user) => user.id === myUserId)).label}
              </span>
            </p>
          </div>
          <p className="mt-1 text-sm text-slate-600">
            Switch your own account to see the site exactly as each type of student does. Only your
            account changes. Switch back to Admin when you are done.
          </p>

          <div className="mt-4 grid gap-2 sm:grid-cols-2 lg:grid-cols-5">
            {PREVIEW_MODES.map((item) => {
              const active =
                currentPreviewMode(overview?.users.find((user) => user.id === myUserId)).mode === item.mode

              return (
                <button
                  key={item.mode}
                  type="button"
                  disabled={previewBusy || (item.mode === "subject" && !previewSubjects.length)}
                  onClick={() => void switchPreview(item.mode)}
                  className={`rounded-lg border p-3 text-left transition disabled:opacity-50 ${
                    active
                      ? "border-[#f4b400] bg-[#fdf3d9]"
                      : "border-slate-200 bg-white hover:border-[#1f4e79]/40 hover:bg-slate-50"
                  }`}
                >
                  <span className="block text-sm font-semibold text-slate-950">{item.label}</span>
                  <span className="mt-0.5 block text-xs leading-5 text-slate-600">{item.detail}</span>
                </button>
              )
            })}
          </div>

          <fieldset className="mt-3">
            <legend className="text-xs font-semibold text-slate-500">Subjects for the Per subject view</legend>
            <div className="mt-2 flex flex-wrap gap-x-4 gap-y-2">
              {SUBJECTS.map((option) => (
                <label key={option.slug} className="flex items-center gap-2 text-sm text-slate-700">
                  <input
                    type="checkbox"
                    checked={previewSubjects.includes(option.slug)}
                    onChange={(event) =>
                      setPreviewSubjects((current) =>
                        event.target.checked
                          ? [...current, option.slug]
                          : current.filter((slug) => slug !== option.slug)
                      )
                    }
                    className="h-4 w-4 accent-[#1f4e79]"
                  />
                  {option.name}
                </label>
              ))}
            </div>
          </fieldset>

          {previewNotice && (
            <p className="mt-3 flex flex-wrap items-center gap-3 text-sm text-slate-700" role="status">
              {previewNotice}
              <Link href="/dashboard" className="font-semibold text-[#1f4e79] underline">
                Open dashboard
              </Link>
            </p>
          )}
        </section>

        <section aria-labelledby="accounts-heading" className="mt-8">
          <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
            <h2 id="accounts-heading" className="text-base font-semibold text-slate-950">
              Accounts <span className="font-normal text-slate-500">({visibleUsers.length})</span>
            </h2>
            <div className="flex flex-col gap-2 sm:flex-row sm:items-center">
              <label className="relative">
                <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
                <input
                  type="search"
                  value={query}
                  onChange={(event) => setQuery(event.target.value)}
                  placeholder="Search name or email"
                  className="min-h-10 w-full rounded-lg border border-slate-300 bg-white pl-9 pr-3 text-sm sm:w-64"
                />
              </label>
              <label className="flex items-center gap-2 text-sm text-slate-600">
                <input
                  type="checkbox"
                  checked={showAdmins}
                  onChange={(event) => setShowAdmins(event.target.checked)}
                  className="h-4 w-4 accent-[#1f4e79]"
                />
                Show admin accounts
              </label>
              <label className="flex items-center gap-2 text-sm text-slate-600">
                <input
                  type="checkbox"
                  checked={showTest}
                  onChange={(event) => setShowTest(event.target.checked)}
                  className="h-4 w-4 accent-[#1f4e79]"
                />
                Show test accounts
              </label>
            </div>
          </div>

          {notice && (
            <p className="mt-3 rounded-lg border border-slate-200 bg-white px-4 py-3 text-sm text-slate-700" role="status">
              {notice}
            </p>
          )}

          <div className="mt-3 space-y-3">
            {visibleUsers.map((user) => (
              <AccountCard
                key={user.id}
                user={user}
                busy={busyUserId === user.id}
                onAction={(request, description) => void runAction(user, request, description)}
              />
            ))}
            {!visibleUsers.length && <p className="text-sm text-slate-500">No accounts match.</p>}
          </div>
        </section>

        {overview && (
          <section aria-labelledby="payments-heading" className="mt-10">
            <h2 id="payments-heading" className="text-base font-semibold text-slate-950">
              Recent payments
            </h2>
            {overview.recentPayments.length ? (
              <div className="mt-3 overflow-x-auto rounded-xl border border-slate-200 bg-white">
                <table className="w-full min-w-[640px] text-left text-sm">
                  <thead className="bg-slate-50 text-xs uppercase tracking-wide text-slate-500">
                    <tr>
                      <th className="px-4 py-3 font-semibold">Date</th>
                      <th className="px-4 py-3 font-semibold">Account</th>
                      <th className="px-4 py-3 font-semibold">Product</th>
                      <th className="px-4 py-3 font-semibold">Amount</th>
                      <th className="px-4 py-3 font-semibold">Status</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {overview.recentPayments.map((payment) => (
                      <tr key={payment.reference}>
                        <td className="px-4 py-3 text-slate-600">{formatDate(payment.paidAt ?? payment.createdAt, true)}</td>
                        <td className="px-4 py-3">
                          {payment.email ?? "—"}
                          {payment.isTestOrAdmin && (
                            <span className="ml-2 rounded bg-slate-100 px-1.5 py-0.5 text-[10px] font-semibold uppercase text-slate-500">
                              test
                            </span>
                          )}
                        </td>
                        <td className="px-4 py-3">
                          {payment.productCode === "ppl_pack"
                            ? "PPL Pack"
                            : payment.subject
                              ? subjectName(payment.subject)
                              : payment.productCode ?? "—"}
                        </td>
                        <td className="px-4 py-3 tabular-nums">{formatRand(payment.amountCents)}</td>
                        <td className="px-4 py-3 capitalize">{payment.status ?? "—"}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <p className="mt-2 text-sm text-slate-500">No payments yet.</p>
            )}
          </section>
        )}
      </div>
    </main>
  )
}

function AccountCard({
  user,
  busy,
  onAction,
}: {
  user: AdminUser
  busy: boolean
  onAction: (request: AccessRequest, description: string) => void
}) {
  const [subject, setSubject] = useState(SUBJECTS[0].slug)
  const [subjectDays, setSubjectDays] = useState(30)
  const badge = accessBadge(user)
  const activeSubjects = user.subjectAccess.filter(
    (access) => access.accessStatus === "active" && isFuture(access.expiresAt)
  )
  const buttonClass =
    "inline-flex min-h-9 items-center justify-center rounded-lg border border-slate-300 bg-white px-3 text-xs font-semibold text-slate-700 hover:bg-slate-50 disabled:opacity-50"
  const dangerClass =
    "inline-flex min-h-9 items-center justify-center rounded-lg border border-red-200 bg-white px-3 text-xs font-semibold text-red-700 hover:bg-red-50 disabled:opacity-50"

  return (
    <article className="rounded-xl border border-slate-200 bg-white p-4 sm:p-5">
      <div className="flex flex-col gap-2 sm:flex-row sm:items-start sm:justify-between">
        <div className="min-w-0">
          <h3 className="truncate text-sm font-semibold text-slate-950">{user.fullName?.trim() || "—"}</h3>
          <p className="truncate text-sm text-slate-600">{user.email ?? "—"}</p>
        </div>
        <div className="flex shrink-0 flex-wrap items-center gap-2">
          {user.isTestAccount && !user.isAdmin && (
            <span className="rounded-full bg-slate-800 px-2.5 py-1 text-xs font-semibold text-white">Test account</span>
          )}
          <span className={`w-fit rounded-full px-2.5 py-1 text-xs font-semibold ${badge.className}`}>
            {badge.label}
          </span>
        </div>
      </div>

      <dl className="mt-3 grid grid-cols-2 gap-x-4 gap-y-2 text-xs sm:grid-cols-4">
        <div>
          <dt className="text-slate-500">Signed up</dt>
          <dd className="font-medium text-slate-800">{formatDate(user.createdAt, true)}</dd>
        </div>
        <div>
          <dt className="text-slate-500">Last login</dt>
          <dd className="font-medium text-slate-800">{formatDate(user.lastSignInAt, true)}</dd>
        </div>
        <div>
          <dt className="text-slate-500">Mock exams</dt>
          <dd className="font-medium text-slate-800">
            {user.attemptCount}
            {user.lastAttemptAt ? ` · last ${formatDate(user.lastAttemptAt)}` : ""}
          </dd>
        </div>
        <div>
          <dt className="text-slate-500">Payments</dt>
          <dd className="font-medium text-slate-800">{user.fulfilledPayments}</dd>
        </div>
      </dl>

      {activeSubjects.length > 0 && (
        <div className="mt-2 flex flex-wrap items-center gap-2 text-xs text-slate-600">
          <span className="text-slate-500">Subjects owned:</span>
          {activeSubjects.map((access) => (
            <span
              key={access.subject}
              className="inline-flex items-center gap-1.5 rounded-full bg-slate-100 py-0.5 pl-2.5 pr-1 text-slate-700"
            >
              {subjectName(access.subject)} · until {formatDate(access.expiresAt)}
              {!user.isAdmin && (
                <button
                  type="button"
                  disabled={busy}
                  onClick={() =>
                    onAction(
                      { action: "revoke_subject", subject: access.subject },
                      `Revoke ${subjectName(access.subject)}`
                    )
                  }
                  className="rounded-full px-1.5 py-0.5 font-semibold text-red-700 hover:bg-red-50 disabled:opacity-50"
                  aria-label={`Revoke ${subjectName(access.subject)}`}
                >
                  Revoke
                </button>
              )}
            </span>
          ))}
        </div>
      )}

      {!user.isAdmin && (
        <div className="mt-4 flex flex-wrap items-center gap-2 border-t border-slate-100 pt-3">
          <button
            type="button"
            disabled={busy}
            className={buttonClass}
            onClick={() => onAction({ action: "extend_trial", days: 3 }, "Extend the trial by 3 days")}
          >
            Trial +3 days
          </button>
          <button
            type="button"
            disabled={busy}
            className={buttonClass}
            onClick={() => onAction({ action: "grant_ppl", days: 30 }, "Grant the PPL Pack for 30 days")}
          >
            PPL Pack 30 days
          </button>
          <button
            type="button"
            disabled={busy}
            className={buttonClass}
            onClick={() => onAction({ action: "grant_ppl", days: 365 }, "Grant the PPL Pack for 1 year")}
          >
            PPL Pack 1 year
          </button>
          <span className="mx-1 hidden h-6 w-px bg-slate-200 sm:block" />
          <select
            value={subject}
            onChange={(event) => setSubject(event.target.value)}
            disabled={busy}
            aria-label="Subject to grant"
            className="min-h-9 rounded-lg border border-slate-300 bg-white px-2 text-xs"
          >
            {SUBJECTS.map((option) => (
              <option key={option.slug} value={option.slug}>
                {option.name}
              </option>
            ))}
          </select>
          <select
            value={subjectDays}
            onChange={(event) => setSubjectDays(Number(event.target.value))}
            disabled={busy}
            aria-label="Days of subject access"
            className="min-h-9 rounded-lg border border-slate-300 bg-white px-2 text-xs"
          >
            {[7, 30, 90, 365].map((days) => (
              <option key={days} value={days}>
                {days === 365 ? "1 year" : `${days} days`}
              </option>
            ))}
          </select>
          <button
            type="button"
            disabled={busy}
            className={buttonClass}
            onClick={() =>
              onAction(
                { action: "grant_subject", subject, days: subjectDays },
                `Grant ${subjectName(subject)} for ${subjectDays === 365 ? "1 year" : `${subjectDays} days`}`
              )
            }
          >
            Grant subject
          </button>
        </div>
      )}

      {!user.isAdmin && (
        <div className="mt-2 flex flex-wrap items-center gap-2">
          {user.subscriptionPlan === "trial" && isFuture(user.trialEndsAt) && (
            <button
              type="button"
              disabled={busy}
              className={dangerClass}
              onClick={() => onAction({ action: "end_trial" }, "End the trial now")}
            >
              End trial
            </button>
          )}
          {user.subscriptionPlan === "ppl" && user.subscriptionStatus === "active" && (
            <button
              type="button"
              disabled={busy}
              className={dangerClass}
              onClick={() => onAction({ action: "revoke_ppl" }, "Revoke the PPL Pack")}
            >
              Revoke PPL Pack
            </button>
          )}
          <button
            type="button"
            disabled={busy}
            className="ml-auto inline-flex min-h-9 items-center justify-center rounded-lg px-3 text-xs font-semibold text-slate-500 hover:bg-slate-50 hover:text-slate-800 disabled:opacity-50"
            onClick={() =>
              onAction(
                { action: "set_test_account", value: !user.isTestAccount },
                user.isTestAccount ? "Mark as a real student" : "Mark as a test account"
              )
            }
          >
            {user.isTestAccount ? "Mark as real student" : "Mark as test account"}
          </button>
        </div>
      )}
    </article>
  )
}
