"use client"

import { useEffect, useMemo, useState } from "react"
import Link from "next/link"
import { useRouter } from "next/navigation"
import {
  ArrowLeft,
  BarChart3,
  Brain,
  CheckCircle2,
  Cloud,
  Compass,
  CreditCard,
  Edit3,
  KeyRound,
  LogOut,
  Map,
  Plane,
  Radio,
  Scale,
  ShieldCheck,
  UserRound,
  Wrench,
  X,
} from "lucide-react"

import { LoadingScreen } from "@/components/loading-screen"
import { supabase } from "@/src/lib/supabase"

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

type SubjectAccessRecord = {
  subject: string
  access_status: string | null
  expires_at: string
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
  const [userId, setUserId] = useState("")
  const [authEmail, setAuthEmail] = useState("")
  const [profile, setProfile] = useState<ProfileRecord | null>(null)
  const [subjectAccess, setSubjectAccess] = useState<SubjectAccessRecord[]>([])
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

        const [profileResponse, accessResponse, attemptsResponse] =
          await Promise.all([
            supabase
              .from("Profiles")
              .select(
                "full_name, email, licence_level, subscription_status, subscription_plan, trial_ends_at, subscription_expires_at"
              )
              .eq("id", user.id)
              .single(),
            supabase
              .from("SubjectAccess")
              .select("subject, access_status, expires_at")
              .eq("user_id", user.id),
            supabase
              .from("ExamAttempts")
              .select("score_percentage")
              .eq("user_id", user.id)
              .eq("exam_mode", "mock"),
          ])

        if (profileResponse.error) {
          throw new Error(profileResponse.error.message)
        }

        if (accessResponse.error) {
          throw new Error(accessResponse.error.message)
        }

        if (attemptsResponse.error) {
          throw new Error(attemptsResponse.error.message)
        }

        if (!cancelled) {
          const loadedProfile = profileResponse.data as ProfileRecord
          setUserId(user.id)
          setAuthEmail(user.email ?? loadedProfile.email ?? "")
          setProfile(loadedProfile)
          setSubjectAccess(
            (accessResponse.data ?? []) as SubjectAccessRecord[]
          )
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
    new Date(profile!.trial_ends_at!) > new Date()

  const isPplUser =
    profile?.subscription_status === "active" &&
    profile?.subscription_plan === "ppl" &&
    Boolean(profile.subscription_expires_at) &&
    new Date(profile!.subscription_expires_at!) > new Date()

  const activeSubjects = useMemo(() => {
    if (isTrialUser || isPplUser) return subjects

    return subjects.filter((subject) =>
      subjectAccess.some(
        (access) =>
          access.subject === subject.slug &&
          access.access_status === "active" &&
          new Date(access.expires_at) > new Date()
      )
    )
  }, [isPplUser, isTrialUser, subjectAccess])

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

  if (loadError || !profile || !userId) {
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

  return (
    <main className="min-h-screen bg-[#06111f] text-white">
      <header className="border-b border-[#1e3a5f] bg-[#06111f]/95">
        <div className="mx-auto flex min-h-20 max-w-7xl items-center justify-between gap-4 px-4 sm:px-6 lg:px-8">
          <div>
            <p className="text-xs uppercase tracking-[0.25em] text-[#f4b400]">
              PilotVault SA
            </p>
            <h1 className="mt-1 text-lg font-bold">Student Profile</h1>
          </div>

          <Link
            href="/dashboard"
            className="inline-flex items-center gap-2 rounded-xl border border-[#1e3a5f] px-4 py-3 text-sm text-gray-300 transition hover:border-[#f4b400] hover:text-[#f4b400]"
          >
            <ArrowLeft size={16} />
            Dashboard
          </Link>
        </div>
      </header>

      <section className="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8">
        <div className="rounded-3xl border border-[#1e3a5f] bg-[#081726] p-6 sm:p-8">
          <div className="flex flex-col gap-5 sm:flex-row sm:items-center">
            <div className="flex h-20 w-20 shrink-0 items-center justify-center rounded-2xl border border-[#f4b400]/30 bg-[#f4b400]/10 text-2xl font-bold text-[#f4b400]">
              {initials}
            </div>

            <div className="min-w-0">
              <p className="text-xs uppercase tracking-[0.25em] text-[#f4b400]">
                Student Account
              </p>
              <h2 className="mt-2 truncate text-3xl font-bold">
                {profile.full_name}
              </h2>
              <p className="mt-2 truncate text-gray-400">{authEmail}</p>
            </div>
          </div>
        </div>

        {(actionMessage || actionError) && (
          <div
            className={`mt-6 rounded-2xl border px-5 py-4 text-sm ${
              actionError
                ? "border-red-500/30 bg-red-500/10 text-red-200"
                : "border-green-500/30 bg-green-500/10 text-green-200"
            }`}
          >
            {actionError || actionMessage}
          </div>
        )}

        <div className="mt-8 grid gap-6 lg:grid-cols-2">
          <section className="rounded-3xl border border-[#1e3a5f] bg-[#081726] p-6 sm:p-8">
            <div className="flex items-center gap-3">
              <div className="rounded-xl bg-[#f4b400]/10 p-3 text-[#f4b400]">
                <UserRound size={22} />
              </div>
              <div>
                <p className="text-xs uppercase tracking-[0.2em] text-[#f4b400]">
                  Profile Information
                </p>
                <h2 className="mt-1 text-xl font-bold">Personal details</h2>
              </div>
            </div>

            <dl className="mt-6 space-y-5">
              <div className="border-b border-[#1e3a5f] pb-4">
                <dt className="text-sm text-gray-500">Full name</dt>
                <dd className="mt-1 font-semibold">{profile.full_name}</dd>
              </div>
              <div className="border-b border-[#1e3a5f] pb-4">
                <dt className="text-sm text-gray-500">Email address</dt>
                <dd className="mt-1 break-all font-semibold">{authEmail}</dd>
              </div>
              <div>
                <dt className="text-sm text-gray-500">Current licence level</dt>
                <dd className="mt-1 font-semibold uppercase">
                  {profile.licence_level ?? "ppl"}
                </dd>
              </div>
            </dl>
          </section>

          <section className="rounded-3xl border border-[#1e3a5f] bg-[#081726] p-6 sm:p-8">
            <div className="flex items-center gap-3">
              <div className="rounded-xl bg-[#f4b400]/10 p-3 text-[#f4b400]">
                <ShieldCheck size={22} />
              </div>
              <div>
                <p className="text-xs uppercase tracking-[0.2em] text-[#f4b400]">
                  Account Information
                </p>
                <h2 className="mt-1 text-xl font-bold">Access and billing</h2>
              </div>
            </div>

            <dl className="mt-6 space-y-5">
              <div className="border-b border-[#1e3a5f] pb-4">
                <dt className="text-sm text-gray-500">Current plan</dt>
                <dd className="mt-1 font-semibold">
                  {formatPlan(profile.subscription_plan)}
                </dd>
              </div>
              <div className="border-b border-[#1e3a5f] pb-4">
                <dt className="text-sm text-gray-500">Subscription status</dt>
                <dd className="mt-1 inline-flex items-center gap-2 font-semibold">
                  <CheckCircle2 size={16} className="text-[#f4b400]" />
                  {formatStatus(profile.subscription_status, isTrialUser)}
                </dd>
              </div>
              <div>
                <dt className="text-sm text-gray-500">{expiryLabel}</dt>
                <dd className="mt-1 font-semibold">{formatDate(expiryValue)}</dd>
              </div>
            </dl>
          </section>
        </div>

        <section className="mt-8 rounded-3xl border border-[#1e3a5f] bg-[#081726] p-6 sm:p-8">
          <p className="text-xs uppercase tracking-[0.25em] text-[#f4b400]">
            My Subjects
          </p>
          <h2 className="mt-3 text-2xl font-bold">Subjects you can access</h2>

          {activeSubjects.length > 0 ? (
            <div className="mt-6 grid grid-cols-2 gap-4 lg:grid-cols-4">
              {activeSubjects.map((subject) => {
                const Icon = subject.icon

                return (
                  <Link
                    key={subject.slug}
                    href={`/practice/${subject.slug}`}
                    className="rounded-2xl border border-[#1e3a5f] bg-[#06111f]/60 p-5 transition hover:-translate-y-1 hover:border-[#f4b400]"
                  >
                    <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-[#f4b400]/10 text-[#f4b400]">
                      <Icon size={21} />
                    </div>
                    <h3 className="mt-4 text-sm font-bold sm:text-base">
                      {subject.name}
                    </h3>
                  </Link>
                )
              })}
            </div>
          ) : (
            <div className="mt-6 rounded-2xl border border-[#1e3a5f] bg-[#06111f]/60 p-6">
              <p className="text-gray-400">
                You do not currently have an active subject.
              </p>
              <Link
                href="/upgrade"
                className="mt-4 inline-flex rounded-xl bg-[#f4b400] px-5 py-3 text-sm font-bold text-[#06111f] transition hover:bg-[#d9a000]"
              >
                View Subscription Options
              </Link>
            </div>
          )}
        </section>

        <section className="mt-8 rounded-3xl border border-[#1e3a5f] bg-[#081726] p-6 sm:p-8">
          <div className="flex items-center gap-3">
            <div className="rounded-xl bg-[#f4b400]/10 p-3 text-[#f4b400]">
              <BarChart3 size={22} />
            </div>
            <div>
              <p className="text-xs uppercase tracking-[0.2em] text-[#f4b400]">
                Performance
              </p>
              <h2 className="mt-1 text-xl font-bold">Mock exam progress</h2>
            </div>
          </div>

          <div className="mt-6 grid gap-4 sm:grid-cols-2">
            <div className="rounded-2xl border border-[#1e3a5f] bg-[#06111f]/60 p-6">
              <p className="text-sm text-gray-500">Exams completed</p>
              <p className="mt-2 text-4xl font-bold text-white">
                {examAttempts.length}
              </p>
            </div>
            <div className="rounded-2xl border border-[#1e3a5f] bg-[#06111f]/60 p-6">
              <p className="text-sm text-gray-500">Average score</p>
              <p className="mt-2 text-4xl font-bold text-[#f4b400]">
                {averageScore}%
              </p>
            </div>
          </div>
        </section>

        <section className="mt-8 rounded-3xl border border-[#1e3a5f] bg-[#081726] p-6 sm:p-8">
          <p className="text-xs uppercase tracking-[0.25em] text-[#f4b400]">
            Account Actions
          </p>
          <h2 className="mt-3 text-2xl font-bold">Manage your account</h2>

          <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            <button
              type="button"
              onClick={() => {
                setActionMessage("")
                setActionError("")
                setFullNameDraft(profile.full_name)
                setLicenceDraft(profile.licence_level ?? "ppl")
                setEditProfileOpen(true)
              }}
              className="flex items-center gap-3 rounded-2xl border border-[#1e3a5f] bg-[#06111f]/60 p-5 text-left transition hover:border-[#f4b400]"
            >
              <Edit3 size={20} className="text-[#f4b400]" />
              <span className="font-semibold">Edit Profile</span>
            </button>

            <button
              type="button"
              onClick={() => {
                setActionMessage("")
                setActionError("")
                setPasswordOpen(true)
              }}
              className="flex items-center gap-3 rounded-2xl border border-[#1e3a5f] bg-[#06111f]/60 p-5 text-left transition hover:border-[#f4b400]"
            >
              <KeyRound size={20} className="text-[#f4b400]" />
              <span className="font-semibold">Change Password</span>
            </button>

            <Link
              href="/upgrade"
              className="flex items-center gap-3 rounded-2xl border border-[#1e3a5f] bg-[#06111f]/60 p-5 transition hover:border-[#f4b400]"
            >
              <CreditCard size={20} className="text-[#f4b400]" />
              <span className="font-semibold">Manage Subscription</span>
            </Link>

            <button
              type="button"
              onClick={handleSignOut}
              className="flex items-center gap-3 rounded-2xl border border-[#1e3a5f] bg-[#06111f]/60 p-5 text-left transition hover:border-red-400 hover:text-red-300"
            >
              <LogOut size={20} />
              <span className="font-semibold">Sign Out</span>
            </button>
          </div>
        </section>
      </section>

      {editProfileOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 px-4 py-6">
          <div className="w-full max-w-md rounded-3xl border border-[#1e3a5f] bg-[#081726] p-6 shadow-2xl">
            <div className="flex items-center justify-between gap-4">
              <div>
                <p className="text-xs uppercase tracking-[0.2em] text-[#f4b400]">
                  Edit Profile
                </p>
                <h2 className="mt-2 text-2xl font-bold">Personal details</h2>
              </div>
              <button
                type="button"
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
                  className="mt-2 w-full rounded-xl border border-[#1e3a5f] bg-[#06111f] px-4 py-3 text-white outline-none focus:border-[#f4b400]"
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
                  className="mt-2 w-full rounded-xl border border-[#1e3a5f] bg-[#06111f] px-4 py-3 text-white outline-none focus:border-[#f4b400]"
                >
                  <option value="ppl">PPL</option>
                  <option value="cpl">CPL</option>
                  <option value="atpl">ATPL</option>
                </select>
              </label>
            </div>

            <div className="mt-7 flex flex-col gap-3 sm:flex-row sm:justify-end">
              <button
                type="button"
                onClick={() => setEditProfileOpen(false)}
                className="rounded-xl border border-[#1e3a5f] px-5 py-3 text-sm font-semibold text-gray-300"
              >
                Cancel
              </button>
              <button
                type="button"
                onClick={handleProfileSave}
                disabled={savingProfile}
                className="rounded-xl bg-[#f4b400] px-5 py-3 text-sm font-bold text-[#06111f] disabled:opacity-60"
              >
                {savingProfile ? "Saving..." : "Save Changes"}
              </button>
            </div>
          </div>
        </div>
      )}

      {passwordOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 px-4 py-6">
          <div className="w-full max-w-md rounded-3xl border border-[#1e3a5f] bg-[#081726] p-6 shadow-2xl">
            <div className="flex items-center justify-between gap-4">
              <div>
                <p className="text-xs uppercase tracking-[0.2em] text-[#f4b400]">
                  Account Security
                </p>
                <h2 className="mt-2 text-2xl font-bold">Change password</h2>
              </div>
              <button
                type="button"
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
                  className="mt-2 w-full rounded-xl border border-[#1e3a5f] bg-[#06111f] px-4 py-3 text-white outline-none focus:border-[#f4b400]"
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
                  className="mt-2 w-full rounded-xl border border-[#1e3a5f] bg-[#06111f] px-4 py-3 text-white outline-none focus:border-[#f4b400]"
                />
              </label>
            </div>

            <div className="mt-7 flex flex-col gap-3 sm:flex-row sm:justify-end">
              <button
                type="button"
                onClick={() => setPasswordOpen(false)}
                className="rounded-xl border border-[#1e3a5f] px-5 py-3 text-sm font-semibold text-gray-300"
              >
                Cancel
              </button>
              <button
                type="button"
                onClick={handlePasswordChange}
                disabled={savingPassword}
                className="rounded-xl bg-[#f4b400] px-5 py-3 text-sm font-bold text-[#06111f] disabled:opacity-60"
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
