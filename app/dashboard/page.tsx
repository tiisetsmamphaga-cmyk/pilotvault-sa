"use client"

import Link from "next/link"
import { Button } from "@/components/ui/button"

const subjects = [
  { name: "Air Law", progress: 72 },
  { name: "Meteorology", progress: 76 },
  { name: "Navigation", progress: 68 },
  { name: "Human Performance", progress: 70 },
  { name: "Principles of Flight", progress: 65 },
  { name: "Aircraft Technical", progress: 74 },
]

export default function DashboardPage() {
  return (
    <main className="min-h-screen bg-[#06111f] text-white">
      <header className="sticky top-0 z-40 border-b border-[#1e3a5f] bg-[#06111f]/95 backdrop-blur">
        <div className="flex h-20 items-center justify-between px-6 lg:px-8">
          <div>
            <p className="text-xs uppercase tracking-[0.2em] text-[#f4b400]">
              PilotVault SA
            </p>
            <h1 className="text-xl font-bold">Student Dashboard</h1>
          </div>

          <div className="flex items-center gap-3">
            <Link href="/">
              <Button
                variant="outline"
                className="rounded-xl border-[#1e3a5f] bg-[#0b1f35] text-white hover:bg-[#1e3a5f] hover:text-white"
              >
                Home
              </Button>
            </Link>

            <Button className="rounded-xl bg-[#f4b400] text-[#06111f] hover:bg-[#d9a000] font-bold">
              Upgrade
            </Button>
          </div>
        </div>
      </header>

      <div className="flex">
        <aside className="hidden lg:flex w-64 border-r border-[#1e3a5f] bg-[#081726] p-5 flex-col min-h-[calc(100vh-80px)]">
          <div className="space-y-2">
            <SidebarItem label="Dashboard" active />

            <Link href="/practice" className="block">
              <SidebarItem label="Practice" />
            </Link>

            <SidebarItem label="Mock Exams" />
            <SidebarItem label="Analytics" />
            <SidebarItem label="Settings" />
          </div>

          <div className="mt-auto rounded-2xl border border-[#1e3a5f] bg-[#0b1f35] p-5">
            <p className="text-xs text-gray-400">Current Plan</p>
            <h3 className="mt-2 text-xl font-bold text-[#f4b400]">
              Free Trial
            </h3>
            <p className="mt-1 text-xs text-gray-400">3 days remaining</p>
          </div>
        </aside>

        <section className="flex-1 p-6 lg:p-8">
          <div className="grid gap-5 xl:grid-cols-[1fr_320px]">
            <div className="rounded-2xl border border-[#1e3a5f] bg-[#081726] p-6">
              <p className="text-xs uppercase tracking-[0.2em] text-[#f4b400]">
                Welcome Back
              </p>

              <h2 className="mt-3 text-3xl lg:text-4xl font-bold">
                Ready to keep building exam confidence?
              </h2>

              <p className="mt-4 max-w-2xl text-sm lg:text-base text-gray-400">
                Continue your SACAA exam preparation with focused practice, mock
                exams, explanations, and progress tracking.
              </p>
            </div>

            <div className="rounded-2xl border border-[#1e3a5f] bg-[#0b1f35] p-6">
              <p className="text-sm text-gray-400">Overall Progress</p>

              <div className="mt-5 flex items-center gap-4">
                <div className="flex h-24 w-24 items-center justify-center rounded-full border-[8px] border-[#f4b400]">
                  <span className="text-2xl font-bold">76%</span>
                </div>

                <div>
                  <h3 className="text-lg font-bold text-[#f4b400]">
                    Good Progress
                  </h3>
                  <p className="mt-1 text-sm text-gray-400">Aim for 85%+</p>
                </div>
              </div>
            </div>
          </div>

          <section className="mt-6 rounded-2xl border border-[#1e3a5f] bg-[#0b1f35] p-6">
            <div className="grid gap-5 lg:grid-cols-[1fr_320px_170px] lg:items-center">
              <div>
                <p className="text-[#f4b400] text-xs uppercase tracking-[0.18em]">
                  Continue Studying
                </p>

                <h2 className="mt-2 text-2xl font-bold">Meteorology</h2>

                <p className="mt-2 text-sm text-gray-400">
                  Pressure systems, fronts, clouds, South African weather, METAR
                  and TAF.
                </p>
              </div>

              <div>
                <div className="mb-2 flex items-center justify-between text-xs">
                  <span className="text-gray-400">Progress</span>
                  <span className="font-semibold">76%</span>
                </div>

                <div className="h-2 overflow-hidden rounded-full bg-[#06111f]">
                  <div className="h-full w-[76%] bg-[#f4b400]" />
                </div>

                <p className="mt-2 text-xs text-gray-500">
                  Last studied: 19 May 2026
                </p>
              </div>

              <Link href="/practice/meteorology">
                <Button className="h-11 w-full rounded-xl bg-[#f4b400] text-[#06111f] hover:bg-[#d9a000] text-sm font-bold">
                  Resume
                </Button>
              </Link>
            </div>
          </section>

          <section className="mt-6 grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
            <StatCard title="Questions" value="174" subtitle="Meteorology bank" />
            <StatCard title="Average Score" value="76%" subtitle="All subjects" />
            <StatCard title="Streak" value="3 Days" subtitle="Keep it going" />
            <StatCard title="Mock Exams" value="4" subtitle="Completed" />
          </section>

          <section className="mt-6 rounded-2xl border border-[#1e3a5f] bg-[#081726] p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-xs uppercase tracking-[0.18em] text-[#f4b400]">
                  Subjects
                </p>
                <h2 className="mt-2 text-2xl font-bold">Progress Overview</h2>
              </div>
            </div>

            <div className="mt-6 grid gap-4 md:grid-cols-2 xl:grid-cols-3">
              {subjects.map((subject) => (
                <div
                  key={subject.name}
                  className="rounded-xl border border-[#1e3a5f] bg-[#0b1f35] p-4"
                >
                  <div className="flex items-center justify-between">
                    <h3 className="font-bold">{subject.name}</h3>
                    <span className="text-sm text-[#f4b400]">
                      {subject.progress}%
                    </span>
                  </div>

                  <div className="mt-4 h-2 overflow-hidden rounded-full bg-[#06111f]">
                    <div
                      className="h-full bg-[#f4b400]"
                      style={{ width: `${subject.progress}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </section>
        </section>
      </div>
    </main>
  )
}

function SidebarItem({
  label,
  active = false,
}: {
  label: string
  active?: boolean
}) {
  return (
    <button
      className={`w-full rounded-xl px-4 py-3 text-left text-sm transition ${
        active
          ? "border-l-4 border-[#f4b400] bg-[#0b1f35] font-bold text-[#f4b400]"
          : "text-gray-300 hover:bg-[#0b1f35]"
      }`}
    >
      {label}
    </button>
  )
}

function StatCard({
  title,
  value,
  subtitle,
}: {
  title: string
  value: string
  subtitle: string
}) {
  return (
    <div className="rounded-2xl border border-[#1e3a5f] bg-[#0b1f35] p-5">
      <p className="text-sm text-gray-400">{title}</p>
      <h3 className="mt-3 text-3xl font-bold">{value}</h3>
      <p className="mt-2 text-xs text-gray-500">{subtitle}</p>

      <div className="mt-4 h-1 overflow-hidden rounded-full bg-[#06111f]">
        <div className="h-full w-[78%] bg-[#f4b400]" />
      </div>
    </div>
  )
}