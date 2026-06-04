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
} from "lucide-react"
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

type Profile = {
  subscription_status: string | null
  subscription_plan: string | null
  payment_status: string | null
  trial_ends_at: string | null
}

type SubjectAccess = {
  subject: string
  access_status: string | null
  expires_at: string
}

export default function DashboardPage() {
  const router = useRouter()

  const [loading, setLoading] = useState(true)
  const [profile, setProfile] = useState<Profile | null>(null)
  const [subjectAccess, setSubjectAccess] = useState<SubjectAccess[]>([])

  useEffect(() => {
    const checkUser = async () => {
      const {
        data: { user },
      } = await supabase.auth.getUser()

      if (!user) {
        router.push("/")
        return
      }

      const { data: profileData } = await supabase
        .from("Profiles")
        .select(
          "subscription_status, subscription_plan, payment_status, trial_ends_at"
        )
        .eq("id", user.id)
        .single()

      const { data: accessData } = await supabase
        .from("SubjectAccess")
        .select("subject, access_status, expires_at")
        .eq("user_id", user.id)

      setProfile(profileData)
      setSubjectAccess(accessData || [])
      setLoading(false)
    }

    checkUser()
  }, [router])

  const handleLogout = async () => {
    await supabase.auth.signOut()
    router.push("/")
  }

  const isTrialUser =
    profile?.subscription_plan === "trial" &&
    profile?.trial_ends_at !== null &&
    new Date(profile.trial_ends_at) > new Date()

  const isPplUser =
    profile?.subscription_status === "active" &&
    profile?.subscription_plan === "ppl"

  const hasSubjectAccess = (slug: string) => {
    if (isTrialUser || isPplUser) return true

    return subjectAccess.some((access) => {
      const isSameSubject = access.subject === slug
      const isActive = access.access_status === "active"
      const isNotExpired = new Date(access.expires_at) > new Date()

      return isSameSubject && isActive && isNotExpired
    })
  }

  if (loading) {
    return (
      <main className="flex min-h-screen items-center justify-center bg-[#06111f] text-white">
        <p className="text-sm text-gray-400">Loading dashboard...</p>
      </main>
    )
  }

  return (
    <main className="min-h-screen bg-[#06111f] text-white">
      <header className="border-b border-[#1e3a5f] bg-[#06111f]/95">
        <div className="mx-auto flex min-h-20 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
          <div>
            <p className="text-xs uppercase tracking-[0.25em] text-[#f4b400]">
              PilotVault SA
            </p>
            <h1 className="mt-1 text-lg font-bold">Dashboard</h1>
          </div>

          <button
            onClick={handleLogout}
            className="flex items-center gap-2 rounded-xl border border-[#1e3a5f] px-4 py-3 text-sm text-gray-300 transition hover:border-[#f4b400] hover:text-[#f4b400]"
          >
            <LogOut className="h-4 w-4" />
            Logout
          </button>
        </div>
      </header>

      <section className="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8">
        <div className="mb-8 rounded-3xl border border-[#1e3a5f] bg-[#081726] p-6 sm:p-8">
          <p className="text-xs uppercase tracking-[0.25em] text-[#f4b400]">
            {isPplUser
              ? "Full Access"
              : isTrialUser
                ? "Trial Access"
                : "Subject Access"}
          </p>

          <h2 className="mt-3 text-3xl font-bold sm:text-4xl">
            {isPplUser
              ? "All PPL subjects unlocked."
              : isTrialUser
                ? "Explore every subject with limited trial access."
                : "Access your purchased subjects."}
          </h2>

          <p className="mt-3 max-w-2xl text-gray-400">
            {isPplUser
              ? "Your PPL Pack gives you access to all subjects, mock exams, topic practice, and the full question bank."
              : isTrialUser
                ? "Your 3-day trial gives you access to all SACAA subjects through a fixed 25-question mock exam set. Topic-based practice and the full question bank require an active subscription."
                : "You can access the subjects you have purchased. Purchase additional subjects whenever you're ready."}
          </p>

          {!isPplUser && (
            <Link
              href="/upgrade"
              className="mt-5 inline-flex rounded-xl bg-[#f4b400] px-5 py-3 text-sm font-bold text-[#06111f] transition hover:bg-[#d9a000]"
            >
              Upgrade to Full Access
            </Link>
          )}
        </div>

        <div className="mb-8 rounded-3xl border border-[#1e3a5f] bg-[#081726] p-6 sm:p-8">
          <p className="text-xs uppercase tracking-[0.25em] text-[#f4b400]">
            Practice Center
          </p>

          <h2 className="mt-3 text-3xl font-bold sm:text-4xl">
            Choose a subject
          </h2>

          <p className="mt-3 max-w-2xl text-gray-400">
            Select a subject to begin your SACAA exam preparation.
          </p>
        </div>

        <div className="grid grid-cols-2 gap-5 lg:grid-cols-4">
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
                className={`group rounded-2xl border bg-[#081726] p-6 transition-all hover:-translate-y-1 hover:border-[#f4b400] ${
                  unlocked ? "border-[#1e3a5f]" : "border-[#1e3a5f] opacity-80"
                }`}
              >
                <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-[#f4b400]/10 group-hover:bg-[#f4b400]/20">
                  <Icon className="h-6 w-6 text-[#f4b400]" />
                </div>

                <h3 className="mt-5 text-sm font-bold sm:text-lg">
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