"use client"

import { useEffect, useMemo, useState } from "react"
import Link from "next/link"
import { useRouter } from "next/navigation"
import {
  ArrowLeft,
  CalendarDays,
  CheckCircle2,
  ChevronRight,
  CreditCard,
  Edit3,
  GraduationCap,
  KeyRound,
  LogOut,
  Mail,
  ShieldCheck,
  UserRound,
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

        const { data, error } = await supabase
          .from("Profiles")
          .select(
            "full_name, email, licence_level, subscription_status, subscription_plan, trial_ends_at, subscription_expires_at"
          )
          .eq("id", user.id)
          .single()

        if (error) throw new Error(error.message)

        if (!cancelled) {
          const loadedProfile = data as ProfileRecord

          setAuthEmail(user.email ?? loadedProfile.email ?? "")
          setProfile(loadedProfile)
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
      <main className="min-h-screen bg-[#06111f] px-4 py-10 text-[#071426] sm:px-6">
        <div className="mx-auto max-w-xl">
          <Link
            href="/dashboard"
            className="inline-flex items-center gap-2 text-sm font-semibold text-white transition hover:opacity-60"
          >
            <ArrowLeft size={16} />
            Back to Dashboard
          </Link>

          <div className="mt-8 rounded-[24px] border border-red-200 bg-white p-7 shadow-[0_12px_36px_rgba(15,23,42,0.08)]">
            <p className="text-xs font-semibold uppercase tracking-[0.2em] text-red-600">
              Profile Error
            </p>
            <h1 className="mt-3 text-3xl font-bold">
              Your profile could not be loaded.
            </h1>
            <p className="mt-3 text-[#707782]">{loadError}</p>
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
    <main className="min-h-screen bg-[#06111f] text-[#071426]">
      <section className="mx-auto max-w-xl px-4 pb-12 pt-6 sm:px-6 sm:pb-16 sm:pt-10">
        <div className="flex items-center justify-between gap-4">
          <Link
            href="/dashboard"
            aria-label="Back to dashboard"
            className="inline-flex h-10 w-10 items-center justify-center rounded-full bg-white text-[#071426] shadow-[0_6px_18px_rgba(15,23,42,0.08)] transition hover:-translate-x-0.5 hover:bg-[#f8f9fa]"
          >
            <ArrowLeft size={19} />
          </Link>

          <p className="text-xs font-semibold uppercase tracking-[0.18em] text-[#7b828c]">
            PilotVault SA
          </p>
        </div>

        <h1 className="mt-8 text-[34px] font-bold tracking-[-0.035em] text-white sm:text-[40px]">
          Profile
        </h1>

        <div className="mt-5 flex min-w-0 items-center gap-4 px-1">
          <div className="flex h-16 w-16 shrink-0 items-center justify-center rounded-full bg-[#071426] text-xl font-bold text-white shadow-[0_8px_22px_rgba(7,20,38,0.2)]">
            {initials}
          </div>

          <div className="min-w-0 flex-1">
            <h2 className="truncate text-xl font-bold tracking-[-0.02em] text-white">
              {profile.full_name}
            </h2>
            <p className="mt-1 truncate text-sm text-[#7b828c]">
              {formatPlan(profile.subscription_plan)}
            </p>
            <div className="mt-2 flex flex-wrap gap-2">
              <span className="rounded-full bg-[#dfe4e9] px-2.5 py-1 text-[11px] font-semibold uppercase tracking-wide text-[#071426]">
                {(profile.licence_level ?? "ppl").toUpperCase()} Student
              </span>
              <span className="inline-flex items-center gap-1.5 rounded-full bg-white px-2.5 py-1 text-[11px] font-semibold text-[#071426]">
                <CheckCircle2 size={12} />
                {formatStatus(profile.subscription_status, isTrialUser)}
              </span>
            </div>
          </div>
        </div>

        {(actionMessage || actionError) && (
          <div
            role="status"
            aria-live="polite"
            className={`mt-6 rounded-2xl border px-4 py-3 text-sm ${
              actionError
                ? "border-red-200 bg-red-50 text-red-700"
                : "border-emerald-200 bg-emerald-50 text-emerald-700"
            }`}
          >
            {actionError || actionMessage}
          </div>
        )}

        <div className="mt-8 space-y-4 sm:mt-10">
          <section
            aria-labelledby="access-heading"
            className="overflow-hidden rounded-[24px] bg-white px-5 shadow-[0_12px_36px_rgba(15,23,42,0.07)] sm:px-6"
          >
            <h3 id="access-heading" className="sr-only">
              Access and billing
            </h3>

            <div className="divide-y divide-[#e6e9ed]">
              <div className="flex min-h-[70px] items-center gap-4 py-4">
                <CreditCard size={20} className="shrink-0 text-[#071426]" />
                <div className="min-w-0 flex-1">
                  <p className="text-sm font-medium">Current plan</p>
                  <p className="mt-0.5 text-xs text-[#7b828c]">
                    {formatPlan(profile.subscription_plan)}
                  </p>
                </div>
              </div>

              <div className="flex min-h-[70px] items-center gap-4 py-4">
                <ShieldCheck size={20} className="shrink-0 text-[#071426]" />
                <div className="min-w-0 flex-1">
                  <p className="text-sm font-medium">Subscription status</p>
                  <p className="mt-0.5 text-xs text-[#7b828c]">
                    {formatStatus(profile.subscription_status, isTrialUser)}
                  </p>
                </div>
              </div>

              <div className="flex min-h-[70px] items-center gap-4 py-4">
                <CalendarDays size={20} className="shrink-0 text-[#071426]" />
                <div className="min-w-0 flex-1">
                  <p className="text-sm font-medium">{expiryLabel}</p>
                  <p className="mt-0.5 text-xs text-[#7b828c]">
                    {formatDate(expiryValue)}
                  </p>
                </div>
              </div>

              <Link
                href="/upgrade"
                className="group flex min-h-[70px] items-center gap-4 py-4 transition hover:text-[#24364e]"
              >
                <CreditCard size={20} className="shrink-0 text-[#071426]" />
                <span className="flex-1 text-sm font-medium">
                  Manage subscription
                </span>
                <ChevronRight
                  size={18}
                  className="shrink-0 text-[#8b929c] transition group-hover:translate-x-0.5 group-hover:text-[#071426]"
                />
              </Link>
            </div>
          </section>

          <section
            aria-labelledby="details-heading"
            className="overflow-hidden rounded-[24px] bg-white px-5 shadow-[0_12px_36px_rgba(15,23,42,0.07)] sm:px-6"
          >
            <h3 id="details-heading" className="sr-only">
              Profile information
            </h3>

            <div className="divide-y divide-[#e6e9ed]">
              <div className="flex min-h-[70px] items-center gap-4 py-4">
                <UserRound size={20} className="shrink-0 text-[#071426]" />
                <div className="min-w-0 flex-1">
                  <p className="text-sm font-medium">Full name</p>
                  <p className="mt-0.5 break-words text-xs text-[#7b828c]">
                    {profile.full_name}
                  </p>
                </div>
              </div>

              <div className="flex min-h-[70px] items-center gap-4 py-4">
                <Mail size={20} className="shrink-0 text-[#071426]" />
                <div className="min-w-0 flex-1">
                  <p className="text-sm font-medium">Email address</p>
                  <p className="mt-0.5 break-all text-xs text-[#7b828c]">
                    {authEmail}
                  </p>
                </div>
              </div>

              <div className="flex min-h-[70px] items-center gap-4 py-4">
                <GraduationCap size={20} className="shrink-0 text-[#071426]" />
                <div className="min-w-0 flex-1">
                  <p className="text-sm font-medium">Current licence level</p>
                  <p className="mt-0.5 text-xs uppercase text-[#7b828c]">
                    {profile.licence_level ?? "ppl"}
                  </p>
                </div>
              </div>

              <button
                type="button"
                onClick={openProfileEditor}
                className="group flex min-h-[70px] w-full items-center gap-4 py-4 text-left transition hover:text-[#24364e]"
              >
                <Edit3 size={20} className="shrink-0 text-[#071426]" />
                <span className="flex-1 text-sm font-medium">Edit profile</span>
                <ChevronRight
                  size={18}
                  className="shrink-0 text-[#8b929c] transition group-hover:translate-x-0.5 group-hover:text-[#071426]"
                />
              </button>
            </div>
          </section>

          <section
            aria-labelledby="security-heading"
            className="overflow-hidden rounded-[24px] bg-white px-5 shadow-[0_12px_36px_rgba(15,23,42,0.07)] sm:px-6"
          >
            <h3 id="security-heading" className="sr-only">
              Account actions
            </h3>

            <div className="divide-y divide-[#e6e9ed]">
              <button
                type="button"
                onClick={openPasswordEditor}
                className="group flex min-h-[70px] w-full items-center gap-4 py-4 text-left transition hover:text-[#24364e]"
              >
                <KeyRound size={20} className="shrink-0 text-[#071426]" />
                <span className="flex-1 text-sm font-medium">
                  Change password
                </span>
                <ChevronRight
                  size={18}
                  className="shrink-0 text-[#8b929c] transition group-hover:translate-x-0.5 group-hover:text-[#071426]"
                />
              </button>

              <button
                type="button"
                onClick={handleSignOut}
                className="group flex min-h-[70px] w-full items-center gap-4 py-4 text-left text-[#071426] transition hover:text-red-600"
              >
                <LogOut size={20} className="shrink-0" />
                <span className="flex-1 text-sm font-medium">Sign out</span>
                <ChevronRight
                  size={18}
                  className="shrink-0 text-[#8b929c] transition group-hover:translate-x-0.5 group-hover:text-red-500"
                />
              </button>
            </div>
          </section>
        </div>
      </section>

      {editProfileOpen && (
        <div className="fixed inset-0 z-50 flex items-end justify-center bg-[#071426]/45 px-0 pt-10 backdrop-blur-[2px] sm:items-center sm:px-4 sm:py-6">
          <div className="max-h-[90vh] w-full max-w-md overflow-y-auto rounded-t-[28px] border border-[#e2e6eb] bg-white p-5 text-[#071426] shadow-2xl sm:rounded-[28px] sm:p-6">
            <div className="flex items-center justify-between gap-4">
              <div>
                <p className="text-xs font-semibold uppercase tracking-[0.18em] text-[#7b828c]">
                  Edit Profile
                </p>
                <h2 className="mt-2 text-2xl font-bold">Personal details</h2>
              </div>
              <button
                type="button"
                aria-label="Close edit profile"
                onClick={() => setEditProfileOpen(false)}
                className="rounded-full border border-[#e2e6eb] p-2 text-[#7b828c] transition hover:bg-[#f2f4f6] hover:text-[#071426]"
              >
                <X size={18} />
              </button>
            </div>

            <div className="mt-6 space-y-5">
              <label className="block">
                <span className="text-sm font-medium text-[#4f5660]">
                  Full name
                </span>
                <input
                  value={fullNameDraft}
                  onChange={(event) => setFullNameDraft(event.target.value)}
                  className="mt-2 w-full rounded-xl border border-[#d9dee5] bg-[#f5f6f8] px-4 py-3 text-base text-[#071426] outline-none transition focus:border-[#071426] focus:bg-white"
                />
              </label>

              <label className="block">
                <span className="text-sm font-medium text-[#4f5660]">
                  Current licence level
                </span>
                <select
                  value={licenceDraft}
                  onChange={(event) =>
                    setLicenceDraft(event.target.value as LicenceLevel)
                  }
                  className="mt-2 w-full rounded-xl border border-[#d9dee5] bg-[#f5f6f8] px-4 py-3 text-base text-[#071426] outline-none transition focus:border-[#071426] focus:bg-white"
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
                className="rounded-xl border border-[#d9dee5] bg-white px-4 py-3 text-sm font-semibold text-[#4f5660] transition hover:bg-[#f5f6f8]"
              >
                Cancel
              </button>
              <button
                type="button"
                onClick={handleProfileSave}
                disabled={savingProfile}
                className="rounded-xl bg-[#071426] px-4 py-3 text-sm font-bold text-white transition hover:bg-[#12243c] disabled:opacity-60"
              >
                {savingProfile ? "Saving..." : "Save Changes"}
              </button>
            </div>
          </div>
        </div>
      )}

      {passwordOpen && (
        <div className="fixed inset-0 z-50 flex items-end justify-center bg-[#071426]/45 px-0 pt-10 backdrop-blur-[2px] sm:items-center sm:px-4 sm:py-6">
          <div className="max-h-[90vh] w-full max-w-md overflow-y-auto rounded-t-[28px] border border-[#e2e6eb] bg-white p-5 text-[#071426] shadow-2xl sm:rounded-[28px] sm:p-6">
            <div className="flex items-center justify-between gap-4">
              <div>
                <p className="text-xs font-semibold uppercase tracking-[0.18em] text-[#7b828c]">
                  Account Security
                </p>
                <h2 className="mt-2 text-2xl font-bold">Change password</h2>
              </div>
              <button
                type="button"
                aria-label="Close password form"
                onClick={() => setPasswordOpen(false)}
                className="rounded-full border border-[#e2e6eb] p-2 text-[#7b828c] transition hover:bg-[#f2f4f6] hover:text-[#071426]"
              >
                <X size={18} />
              </button>
            </div>

            <div className="mt-6 space-y-5">
              <label className="block">
                <span className="text-sm font-medium text-[#4f5660]">
                  New password
                </span>
                <input
                  type="password"
                  value={newPassword}
                  onChange={(event) => setNewPassword(event.target.value)}
                  className="mt-2 w-full rounded-xl border border-[#d9dee5] bg-[#f5f6f8] px-4 py-3 text-base text-[#071426] outline-none transition focus:border-[#071426] focus:bg-white"
                />
              </label>

              <label className="block">
                <span className="text-sm font-medium text-[#4f5660]">
                  Confirm new password
                </span>
                <input
                  type="password"
                  value={confirmPassword}
                  onChange={(event) => setConfirmPassword(event.target.value)}
                  className="mt-2 w-full rounded-xl border border-[#d9dee5] bg-[#f5f6f8] px-4 py-3 text-base text-[#071426] outline-none transition focus:border-[#071426] focus:bg-white"
                />
              </label>
            </div>

            <div className="mt-7 grid grid-cols-2 gap-3">
              <button
                type="button"
                onClick={() => setPasswordOpen(false)}
                className="rounded-xl border border-[#d9dee5] bg-white px-4 py-3 text-sm font-semibold text-[#4f5660] transition hover:bg-[#f5f6f8]"
              >
                Cancel
              </button>
              <button
                type="button"
                onClick={handlePasswordChange}
                disabled={savingPassword}
                className="rounded-xl bg-[#071426] px-4 py-3 text-sm font-bold text-white transition hover:bg-[#12243c] disabled:opacity-60"
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
