"use client"

import { useEffect, useMemo, useState } from "react"
import Link from "next/link"
import { useRouter } from "next/navigation"
import {
  ArrowLeft,
  BarChart3,
  CheckCircle2,
  ChevronRight,
  CreditCard,
  Edit3,
  KeyRound,
  LogOut,
  ShieldCheck,
  X,
} from "lucide-react"

import { LoadingScreen } from "@/components/loading-screen"
import { supabase } from "@/src/lib/supabase"

type LicenceLevel = "ppl" | "cpl" | "atpl"

type ProfileRecord = {
  full_name: string
  email: string | null
  licence_level: LicenceLevel | null
  subscription_status: string | null
  subscription_plan: string | null
  trial_ends_at: string | null
  subscription_expires_at: string | null
}

type ExamAttemptRecord = {
  score_percentage: number
}

function formatDate(value: string | null) {
  if (!value) return "Not available"

  return new Intl.DateTimeFormat("en-ZA", {
    day: "2-digit",
    month: "long",
    year: "numeric",
  }).format(new Date(value))
}

function formatPlan(plan: string | null) {
  switch (plan) {
    case "trial":
      return "Trial Access"
    case "ppl":
      return "PPL Pack"
    case "cpl":
      return "CPL Pack"
    case "all-access":
    case "all_access":
      return "All Access"
    default:
      return "Individual Subjects"
  }
}

function formatStatus(status: string | null, isTrial: boolean) {
  if (isTrial) return "Trial active"
  if (!status) return "Inactive"

  return status.charAt(0).toUpperCase() + status.slice(1)
}

export default function ProfilePage() {
  const router = useRouter()

  const [loading, setLoading] = useState(true)
  const [loadError, setLoadError] = useState("")
  const [authEmail, setAuthEmail] = useState("")
  const [profile, setProfile] = useState<ProfileRecord | null>(null)
  const [examAttempts, setExamAttempts] = useState<ExamAttemptRecord[]>([])

  const [editProfileOpen, setEditProfileOpen] = useState(false)
  const [passwordOpen, setPasswordOpen] = useState(false)
  const [fullNameDraft, setFullNameDraft] = useState("")
  const [licenceDraft, setLicenceDraft] = useState<LicenceLevel>("ppl")
  const [newPassword, setNewPassword] = useState("")
  const [confirmPassword, setConfirmPassword] = useState("")
  const [savingProfile, setSavingProfile] = useState(false)
  const [savingPassword, setSavingPassword] = useState(false)
  const [actionMessage, setActionMessage] = useState("")
  const [actionError, setActionError] = useState("")

  useEffect(() => {
    let cancelled = false

    const loadProfile = async () => {
      try {
        setLoading(true)
        setLoadError("")

        const {
          data: { user },
          error: userError,
        } = await supabase.auth.getUser()

        if (userError) throw new Error(userError.message)

        if (!user) {
          router.push("/")
          return
        }

        const [profileResponse, attemptsResponse] = await Promise.all([
          supabase
            .from("Profiles")
            .select(
              "full_name, email, licence_level, subscription_status, subscription_plan, trial_ends_at, subscription_expires_at"
            )
            .eq("id", user.id)
            .single(),
          supabase
            .from("ExamAttempts")
            .select("score_percentage")
            .eq("user_id", user.id)
            .eq("exam_mode", "mock"),
        ])

        if (profileResponse.error) {
          throw new Error(profileResponse.error.message)
        }

        if (attemptsResponse.error) {
          throw new Error(attemptsResponse.error.message)
        }

        if (!cancelled) {
          const loadedProfile = profileResponse.data as ProfileRecord

          setAuthEmail(user.email ?? loadedProfile.email ?? "")
          setProfile(loadedProfile)
          setExamAttempts(
            (attemptsResponse.data ?? []) as ExamAttemptRecord[]
          )
          setFullNameDraft(loadedProfile.full_name)
          setLicenceDraft(loadedProfile.licence_level ?? "ppl")
        }
      } catch (error) {
        if (!cancelled) {
          setLoadError(
            error instanceof Error
              ? error.message
              : "Your profile could not be loaded."
          )
        }
      } finally {
        if (!cancelled) setLoading(false)
      }
    }

    loadProfile()

    return () => {
      cancelled = true
    }
  }, [router])

  const isTrialUser =
    profile?.subscription_plan === "trial" &&
    Boolean(profile.trial_ends_at) &&
    new Date(profile.trial_ends_at as string) > new Date()

  const averageScore = useMemo(() => {
    if (examAttempts.length === 0) return 0

    const total = examAttempts.reduce(
      (sum, attempt) => sum + attempt.score_percentage,
      0
    )

    return Math.round(total / examAttempts.length)
  }, [examAttempts])

  const initials = useMemo(() => {
    const name = profile?.full_name?.trim()
    if (!name) return "PV"

    return name
      .split(/\s+/)
      .slice(0, 2)
      .map((part) => part.charAt(0).toUpperCase())
      .join("")
  }, [profile?.full_name])

  const handleProfileSave = async () => {
    setActionMessage("")
    setActionError("")

    if (!fullNameDraft.trim()) {
      setActionError("Full name is required.")
      return
    }

    try {
      setSavingProfile(true)

      const { error } = await supabase.rpc("update_own_profile", {
        p_full_name: fullNameDraft.trim(),
        p_licence_level: licenceDraft,
      })

      if (error) throw new Error(error.message)

      setProfile((currentProfile) =>
        currentProfile
          ? {
              ...currentProfile,
              full_name: fullNameDraft.trim(),
              licence_level: licenceDraft,
            }
          : currentProfile
      )
      setEditProfileOpen(false)
      setActionMessage("Profile updated successfully.")
    } catch (error) {
      setActionError(
        error instanceof Error ? error.message : "Profile update failed."
      )
    } finally {
      setSavingProfile(false)
    }
  }

  const handlePasswordChange = async () => {
    setActionMessage("")
    setActionError("")

    if (newPassword.length < 8) {
      setActionError("Your new password must contain at least 8 characters.")
      return
    }

    if (newPassword !== confirmPassword) {
      setActionError("The passwords do not match.")
      return
    }

    try {
      setSavingPassword(true)

      const { error } = await supabase.auth.updateUser({
        password: newPassword,
      })

      if (error) throw new Error(error.message)

      setNewPassword("")
      setConfirmPassword("")
      setPasswordOpen(false)
      setActionMessage("Password changed successfully.")
    } catch (error) {
      setActionError(
        error instanceof Error ? error.message : "Password change failed."
      )
    } finally {
      setSavingPassword(false)
    }
  }

  const handleSignOut = async () => {
    await supabase.auth.signOut()
    router.push("/")
  }

  if (loading) return <LoadingScreen />

  if (loadError || !profile) {
    return (
      <main className="min-h-screen bg-[#06111f] px-4 py-10 text-white sm:px-6">
        <div className="mx-auto max-w-4xl">
          <Link
            href="/dashboard"
            className="inline-flex items-center gap-2 text-sm font-medium text-[#f4b400] hover:text-white"
          >
            <ArrowLeft size={16} />
            Back to Dashboard
          </Link>

          <div className="mt-8 rounded-3xl border border-red-500/30 bg-[#081726] p-8">
            <p className="text-xs uppercase tracking-[0.25em] text-red-400">
              Profile Error
            </p>
            <h1 className="mt-3 text-3xl font-bold">
              Your profile could not be loaded.
            </h1>
            <p className="mt-3 text-gray-400">{loadError}</p>
          </div>
        </div>
      </main>
    )
  }

  const expiryLabel = isTrialUser ? "Trial expiry" : "Renewal date"
  const expiryValue = isTrialUser
    ? profile.trial_ends_at
    : profile.subscription_expires_at

  const openProfileEditor = () => {
    setActionMessage("")
    setActionError("")
    setFullNameDraft(profile.full_name)
    setLicenceDraft(profile.licence_level ?? "ppl")
    setEditProfileOpen(true)
  }

  const openPasswordEditor = () => {
    setActionMessage("")
    setActionError("")
    setPasswordOpen(true)
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
              Student Profile
            </h1>
          </div>

          <Link
            href="/dashboard"
            className="inline-flex shrink-0 items-center gap-2 rounded-xl border border-[#1e3a5f] px-3 py-2.5 text-sm text-gray-300 transition hover:border-[#f4b400] hover:text-[#f4b400] sm:px-4 sm:py-3"
          >
            <ArrowLeft size={16} />
            <span className="hidden sm:inline">Dashboard</span>
            <span className="sm:hidden">Back</span>
          </Link>
        </div>
      </header>

      <section className="mx-auto max-w-7xl px-4 py-6 sm:px-6 sm:py-10 lg:px-8">
        {(actionMessage || actionError) && (
          <div
            className={`mb-5 rounded-2xl border px-4 py-3 text-sm sm:mb-6 sm:px-5 sm:py-4 ${
              actionError
                ? "border-red-500/30 bg-red-500/10 text-red-200"
                : "border-green-500/30 bg-green-500/10 text-green-200"
            }`}
          >
            {actionError || actionMessage}
          </div>
        )}

        <div className="overflow-hidden rounded-3xl border border-[#1e3a5f] bg-[#081726] shadow-2xl shadow-black/10">
          <div className="relative overflow-hidden border-b border-[#1e3a5f] px-5 py-6 sm:px-8 sm:py-8">
            <div className="pointer-events-none absolute inset-y-0 right-0 w-2/3 bg-[radial-gradient(circle_at_top_right,rgba(244,180,0,0.12),transparent_55%)]" />

            <div className="relative flex flex-col gap-5 sm:flex-row sm:items-center sm:justify-between">
              <div className="flex min-w-0 items-center gap-4 sm:gap-5">
                <div className="flex h-16 w-16 shrink-0 items-center justify-center rounded-2xl border border-[#f4b400]/30 bg-[#f4b400]/10 text-xl font-bold text-[#f4b400] sm:h-20 sm:w-20 sm:text-2xl">
                  {initials}
                </div>

                <div className="min-w-0">
                  <p className="text-[10px] font-semibold uppercase tracking-[0.22em] text-[#f4b400] sm:text-xs">
                    Student Account
                  </p>
                  <h2 className="mt-1 truncate text-2xl font-bold sm:mt-2 sm:text-3xl">
                    {profile.full_name}
                  </h2>
                  <p className="mt-1 truncate text-sm text-gray-400 sm:mt-2 sm:text-base">
                    {authEmail}
                  </p>
                </div>
              </div>

              <div className="flex flex-wrap gap-2 sm:justify-end">
                <span className="inline-flex items-center rounded-full border border-[#f4b400]/30 bg-[#f4b400]/10 px-3 py-1.5 text-xs font-bold uppercase tracking-wider text-[#f4b400]">
                  {(profile.licence_level ?? "ppl").toUpperCase()} Student
                </span>
                <span className="inline-flex items-center gap-1.5 rounded-full border border-[#1e3a5f] bg-[#06111f]/60 px-3 py-1.5 text-xs font-semibold text-gray-200">
                  <CheckCircle2 size={14} className="text-[#f4b400]" />
                  {formatStatus(profile.subscription_status, isTrialUser)}
                </span>
              </div>
            </div>
          </div>

          <div className="lg:grid lg:grid-cols-[minmax(0,1fr)_340px]">
            <div className="min-w-0">
              <section className="px-5 py-6 sm:px-8 sm:py-8">
                <div className="flex items-center justify-between gap-4">
                  <div>
                    <p className="text-xs uppercase tracking-[0.22em] text-[#f4b400]">
                      Profile Information
                    </p>
                    <h3 className="mt-2 text-xl font-bold">Personal details</h3>
                  </div>

                  <button
                    type="button"
                    onClick={openProfileEditor}
                    className="inline-flex shrink-0 items-center gap-2 rounded-xl border border-[#1e3a5f] px-3 py-2 text-sm font-semibold text-gray-300 transition hover:border-[#f4b400] hover:text-[#f4b400] sm:px-4"
                  >
                    <Edit3 size={16} />
                    <span className="hidden sm:inline">Edit</span>
                  </button>
                </div>

                <dl className="mt-6 divide-y divide-[#1e3a5f] border-y border-[#1e3a5f]">
                  <div className="grid gap-1 py-4 sm:grid-cols-[180px_minmax(0,1fr)] sm:items-center sm:gap-6">
                    <dt className="text-sm text-gray-500">Full name</dt>
                    <dd className="break-words font-semibold text-white sm:text-right">
                      {profile.full_name}
                    </dd>
                  </div>
                  <div className="grid gap-1 py-4 sm:grid-cols-[180px_minmax(0,1fr)] sm:items-center sm:gap-6">
                    <dt className="text-sm text-gray-500">Email address</dt>
                    <dd className="break-all font-semibold text-white sm:text-right">
                      {authEmail}
                    </dd>
                  </div>
                  <div className="grid gap-1 py-4 sm:grid-cols-[180px_minmax(0,1fr)] sm:items-center sm:gap-6">
                    <dt className="text-sm text-gray-500">
                      Current licence level
                    </dt>
                    <dd className="font-semibold uppercase text-white sm:text-right">
                      {profile.licence_level ?? "ppl"}
                    </dd>
                  </div>
                </dl>
              </section>

              <section className="border-t border-[#1e3a5f] px-5 py-6 sm:px-8 sm:py-8">
                <div className="flex items-center gap-3">
                  <BarChart3 size={21} className="text-[#f4b400]" />
                  <div>
                    <p className="text-xs uppercase tracking-[0.22em] text-[#f4b400]">
                      Performance
                    </p>
                    <h3 className="mt-1 text-xl font-bold">
                      Mock exam progress
                    </h3>
                  </div>
                </div>

                <div className="mt-6 grid grid-cols-2 divide-x divide-[#1e3a5f] border-y border-[#1e3a5f] py-5">
                  <div className="pr-4 sm:pr-8">
                    <p className="text-xs text-gray-500 sm:text-sm">
                      Exams completed
                    </p>
                    <p className="mt-2 text-3xl font-bold text-white sm:text-4xl">
                      {examAttempts.length}
                    </p>
                  </div>
                  <div className="pl-4 sm:pl-8">
                    <p className="text-xs text-gray-500 sm:text-sm">
                      Average score
                    </p>
                    <p className="mt-2 text-3xl font-bold text-[#f4b400] sm:text-4xl">
                      {averageScore}%
                    </p>
                  </div>
                </div>
              </section>
            </div>

            <aside className="border-t border-[#1e3a5f] lg:border-l lg:border-t-0">
              <section className="px-5 py-6 sm:px-8 sm:py-8 lg:px-6">
                <div className="flex items-center gap-3">
                  <ShieldCheck size={21} className="text-[#f4b400]" />
                  <div>
                    <p className="text-xs uppercase tracking-[0.22em] text-[#f4b400]">
                      Account
                    </p>
                    <h3 className="mt-1 text-xl font-bold">
                      Access and billing
                    </h3>
                  </div>
                </div>

                <dl className="mt-6 divide-y divide-[#1e3a5f] border-y border-[#1e3a5f]">
                  <div className="py-4">
                    <dt className="text-sm text-gray-500">Current plan</dt>
                    <dd className="mt-1 font-semibold">
                      {formatPlan(profile.subscription_plan)}
                    </dd>
                  </div>
                  <div className="py-4">
                    <dt className="text-sm text-gray-500">
                      Subscription status
                    </dt>
                    <dd className="mt-1 inline-flex items-center gap-2 font-semibold">
                      <CheckCircle2 size={16} className="text-[#f4b400]" />
                      {formatStatus(profile.subscription_status, isTrialUser)}
                    </dd>
                  </div>
                  <div className="py-4">
                    <dt className="text-sm text-gray-500">{expiryLabel}</dt>
                    <dd className="mt-1 font-semibold">
                      {formatDate(expiryValue)}
                    </dd>
                  </div>
                </dl>
              </section>

              <section className="border-t border-[#1e3a5f] px-5 py-6 sm:px-8 sm:py-8 lg:px-6">
                <p className="text-xs uppercase tracking-[0.22em] text-[#f4b400]">
                  Account Actions
                </p>
                <h3 className="mt-2 text-xl font-bold">Manage your account</h3>

                <div className="mt-5 divide-y divide-[#1e3a5f] border-y border-[#1e3a5f]">
                  <button
                    type="button"
                    onClick={openProfileEditor}
                    className="group flex min-h-14 w-full items-center gap-3 py-3.5 text-left transition hover:text-[#f4b400]"
                  >
                    <Edit3 size={19} className="text-[#f4b400]" />
                    <span className="flex-1 text-sm font-semibold">
                      Edit Profile
                    </span>
                    <ChevronRight
                      size={18}
                      className="text-gray-600 transition group-hover:translate-x-0.5 group-hover:text-[#f4b400]"
                    />
                  </button>

                  <button
                    type="button"
                    onClick={openPasswordEditor}
                    className="group flex min-h-14 w-full items-center gap-3 py-3.5 text-left transition hover:text-[#f4b400]"
                  >
                    <KeyRound size={19} className="text-[#f4b400]" />
                    <span className="flex-1 text-sm font-semibold">
                      Change Password
                    </span>
                    <ChevronRight
                      size={18}
                      className="text-gray-600 transition group-hover:translate-x-0.5 group-hover:text-[#f4b400]"
                    />
                  </button>

                  <Link
                    href="/upgrade"
                    className="group flex min-h-14 items-center gap-3 py-3.5 transition hover:text-[#f4b400]"
                  >
                    <CreditCard size={19} className="text-[#f4b400]" />
                    <span className="flex-1 text-sm font-semibold">
                      Manage Subscription
                    </span>
                    <ChevronRight
                      size={18}
                      className="text-gray-600 transition group-hover:translate-x-0.5 group-hover:text-[#f4b400]"
                    />
                  </Link>

                  <button
                    type="button"
                    onClick={handleSignOut}
                    className="group flex min-h-14 w-full items-center gap-3 py-3.5 text-left text-gray-300 transition hover:text-red-300"
                  >
                    <LogOut size={19} />
                    <span className="flex-1 text-sm font-semibold">
                      Sign Out
                    </span>
                    <ChevronRight
                      size={18}
                      className="text-gray-600 transition group-hover:translate-x-0.5 group-hover:text-red-300"
                    />
                  </button>
                </div>
              </section>
            </aside>
          </div>
        </div>
      </section>

      {editProfileOpen && (
        <div className="fixed inset-0 z-50 flex items-end justify-center bg-black/70 px-0 pt-10 sm:items-center sm:px-4 sm:py-6">
          <div className="max-h-[90vh] w-full max-w-md overflow-y-auto rounded-t-3xl border border-[#1e3a5f] bg-[#081726] p-5 shadow-2xl sm:rounded-3xl sm:p-6">
            <div className="flex items-center justify-between gap-4">
              <div>
                <p className="text-xs uppercase tracking-[0.2em] text-[#f4b400]">
                  Edit Profile
                </p>
                <h2 className="mt-2 text-2xl font-bold">Personal details</h2>
              </div>
              <button
                type="button"
                aria-label="Close edit profile"
                onClick={() => setEditProfileOpen(false)}
                className="rounded-xl border border-[#1e3a5f] p-2 text-gray-400 hover:text-white"
              >
                <X size={18} />
              </button>
            </div>

            <div className="mt-6 space-y-5">
              <label className="block">
                <span className="text-sm font-medium text-gray-300">
                  Full name
                </span>
                <input
                  value={fullNameDraft}
                  onChange={(event) => setFullNameDraft(event.target.value)}
                  className="mt-2 w-full rounded-xl border border-[#1e3a5f] bg-[#06111f] px-4 py-3 text-base text-white outline-none focus:border-[#f4b400]"
                />
              </label>

              <label className="block">
                <span className="text-sm font-medium text-gray-300">
                  Current licence level
                </span>
                <select
                  value={licenceDraft}
                  onChange={(event) =>
                    setLicenceDraft(event.target.value as LicenceLevel)
                  }
                  className="mt-2 w-full rounded-xl border border-[#1e3a5f] bg-[#06111f] px-4 py-3 text-base text-white outline-none focus:border-[#f4b400]"
                >
                  <option value="ppl">PPL</option>
                  <option value="cpl">CPL</option>
                  <option value="atpl">ATPL</option>
                </select>
              </label>
            </div>

            <div className="mt-7 grid grid-cols-2 gap-3">
              <button
                type="button"
                onClick={() => setEditProfileOpen(false)}
                className="rounded-xl border border-[#1e3a5f] px-4 py-3 text-sm font-semibold text-gray-300"
              >
                Cancel
              </button>
              <button
                type="button"
                onClick={handleProfileSave}
                disabled={savingProfile}
                className="rounded-xl bg-[#f4b400] px-4 py-3 text-sm font-bold text-[#06111f] disabled:opacity-60"
              >
                {savingProfile ? "Saving..." : "Save Changes"}
              </button>
            </div>
          </div>
        </div>
      )}

      {passwordOpen && (
        <div className="fixed inset-0 z-50 flex items-end justify-center bg-black/70 px-0 pt-10 sm:items-center sm:px-4 sm:py-6">
          <div className="max-h-[90vh] w-full max-w-md overflow-y-auto rounded-t-3xl border border-[#1e3a5f] bg-[#081726] p-5 shadow-2xl sm:rounded-3xl sm:p-6">
            <div className="flex items-center justify-between gap-4">
              <div>
                <p className="text-xs uppercase tracking-[0.2em] text-[#f4b400]">
                  Account Security
                </p>
                <h2 className="mt-2 text-2xl font-bold">Change password</h2>
              </div>
              <button
                type="button"
                aria-label="Close password form"
                onClick={() => setPasswordOpen(false)}
                className="rounded-xl border border-[#1e3a5f] p-2 text-gray-400 hover:text-white"
              >
                <X size={18} />
              </button>
            </div>

            <div className="mt-6 space-y-5">
              <label className="block">
                <span className="text-sm font-medium text-gray-300">
                  New password
                </span>
                <input
                  type="password"
                  value={newPassword}
                  onChange={(event) => setNewPassword(event.target.value)}
                  className="mt-2 w-full rounded-xl border border-[#1e3a5f] bg-[#06111f] px-4 py-3 text-base text-white outline-none focus:border-[#f4b400]"
                />
              </label>

              <label className="block">
                <span className="text-sm font-medium text-gray-300">
                  Confirm new password
                </span>
                <input
                  type="password"
                  value={confirmPassword}
                  onChange={(event) => setConfirmPassword(event.target.value)}
                  className="mt-2 w-full rounded-xl border border-[#1e3a5f] bg-[#06111f] px-4 py-3 text-base text-white outline-none focus:border-[#f4b400]"
                />
              </label>
            </div>

            <div className="mt-7 grid grid-cols-2 gap-3">
              <button
                type="button"
                onClick={() => setPasswordOpen(false)}
                className="rounded-xl border border-[#1e3a5f] px-4 py-3 text-sm font-semibold text-gray-300"
              >
                Cancel
              </button>
              <button
                type="button"
                onClick={handlePasswordChange}
                disabled={savingPassword}
                className="rounded-xl bg-[#f4b400] px-4 py-3 text-sm font-bold text-[#06111f] disabled:opacity-60"
              >
                {savingPassword ? "Updating..." : "Update Password"}
              </button>
            </div>
          </div>
        </div>
      )}
    </main>
  )
}
