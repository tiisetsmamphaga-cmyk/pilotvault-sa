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

export default function DashboardPage() {
  const router = useRouter()
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const checkUser = async () => {
      const {
        data: { user },
      } = await supabase.auth.getUser()

      if (!user) {
        router.push("/")
        return
      }

      setLoading(false)
    }

    checkUser()
  }, [router])

  const handleLogout = async () => {
    await supabase.auth.signOut()
    router.push("/")
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

          <div className="flex items-center gap-3">
            <div className="rounded-xl border border-[#f4b400]/30 bg-[#f4b400]/10 px-4 py-3">
              <p className="text-[10px] uppercase tracking-wider text-[#f4b400]">
                Trial Account
              </p>
              <p className="mt-1 text-sm font-bold text-white">
                3 days remaining
              </p>
            </div>

            <button
              onClick={handleLogout}
              className="flex items-center gap-2 rounded-xl border border-[#1e3a5f] px-4 py-3 text-sm text-gray-300 transition hover:border-[#f4b400] hover:text-[#f4b400]"
            >
              <LogOut className="h-4 w-4" />
              Logout
            </button>
          </div>
        </div>
      </header>

      <section className="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8">
        <div className="mb-8 rounded-3xl border border-[#1e3a5f] bg-[#081726] p-6 sm:p-8">
          <p className="text-xs uppercase tracking-[0.25em] text-[#f4b400]">
            Trial Access
          </p>

          <h2 className="mt-3 text-3xl font-bold sm:text-4xl">
            All subjects unlocked. Limited trial questions.
          </h2>

          <p className="mt-3 max-w-2xl text-gray-400">
            Your 3-day trial includes access to all SACAA subjects with a fixed
            25-question mock exam set. Topic-based practice and the full
            question bank unlock after upgrading.
          </p>

          <Link
            href="/upgrade"
            className="mt-5 inline-flex rounded-xl bg-[#f4b400] px-5 py-3 text-sm font-bold text-[#06111f] transition hover:bg-[#d9a000]"
          >
            Upgrade to Full Access
          </Link>
        </div>

        <div className="mb-8 rounded-3xl border border-[#1e3a5f] bg-[#081726] p-6 sm:p-8">
          <p className="text-xs uppercase tracking-[0.25em] text-[#f4b400]">
            Practice Center
          </p>

          <h2 className="mt-3 text-3xl font-bold sm:text-4xl">
            Choose a subject
          </h2>

          <p className="mt-3 max-w-2xl text-gray-400">
            Select a subject and begin practicing SACAA exam questions.
          </p>
        </div>

        <div className="grid grid-cols-2 gap-5 lg:grid-cols-4">
          {subjects.map((subject) => (
            <Link
              key={subject.slug}
              href={`/practice/${subject.slug}`}
              className="group rounded-2xl border border-[#1e3a5f] bg-[#081726] p-6 transition-all hover:-translate-y-1 hover:border-[#f4b400]"
            >
              <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-[#f4b400]/10 group-hover:bg-[#f4b400]/20">
                <subject.icon className="h-6 w-6 text-[#f4b400]" />
              </div>

              <h3 className="mt-5 text-sm font-bold sm:text-lg">
                {subject.name}
              </h3>
            </Link>
          ))}
        </div>
      </section>
    </main>
  )
}