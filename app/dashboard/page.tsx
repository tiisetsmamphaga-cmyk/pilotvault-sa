"use client"

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
     <main className="min-h-screen bg-[#06111f] text-white flex relative">
      <Button
  onClick={() => {
    window.location.href = "/"
  }}
  variant="outline"
  className="mb-10 mt-4 border-[#1e3a5f] bg-[#0b1f35] text-white hover:bg-[#1e3a5f] rounded-xl w-full justify-start"
>
  ← Back to Home
</Button>

      <aside className="hidden lg:flex w-56 border-r border-[#1e3a5f] bg-[#081726] p-5 flex-col">
        <div className="space-y-2 mt-10">
          <SidebarItem label="Dashboard" active />
          <SidebarItem label="Practice" />
          <SidebarItem label="Mock Exams" />
          <SidebarItem label="Analytics" />
          <SidebarItem label="Settings" />
        </div>

        <div className="mt-auto rounded-xl border border-[#1e3a5f] bg-[#0b1f35] p-4">
          <p className="text-xs text-gray-400">Current Plan</p>
          <h3 className="mt-2 text-xl font-bold text-[#f4b400]">Free Trial</h3>
          <p className="mt-1 text-xs text-gray-400">3 days remaining</p>

          <Button className="mt-4 w-full h-9 bg-[#f4b400] text-[#06111f] hover:bg-[#d9a000] text-sm font-bold">
            Upgrade
          </Button>
        </div>
      </aside>

      <section className="flex-1 p-5 lg:p-8">
        <div className="grid xl:grid-cols-[1fr_320px] gap-5">
          <div>
            <h1 className="text-3xl lg:text-4xl font-bold">
              Welcome back, pilot.
            </h1>

            <p className="mt-3 text-sm lg:text-base text-gray-400 max-w-xl">
              Continue your SACAA exam preparation with focused practice,
              mock exams, and weak-topic tracking.
            </p>
          </div>

          <div className="rounded-2xl border border-[#1e3a5f] bg-[#0b1f35] p-5">
            <p className="text-sm text-gray-400">Overall Progress</p>

            <div className="mt-4 flex items-center gap-4">
              <div className="h-20 w-20 rounded-full border-[7px] border-[#f4b400] flex items-center justify-center">
                <span className="text-xl font-bold">76%</span>
              </div>

              <div>
                <h3 className="text-lg font-bold text-[#f4b400]">
                  Good Progress
                </h3>
                <p className="mt-1 text-sm text-gray-400">
                  Aim for 85%+
                </p>
              </div>
            </div>
          </div>
        </div>

        <section className="mt-6 rounded-2xl border border-[#1e3a5f] bg-[#0b1f35] p-5">
          <div className="grid lg:grid-cols-[1fr_320px_170px] gap-5 items-center">
            <div>
              <p className="text-[#f4b400] text-xs uppercase tracking-[0.18em]">
                Continue Studying
              </p>

              <h2 className="mt-2 text-2xl font-bold">Meteorology</h2>

              <p className="mt-2 text-sm text-gray-400">
                Pressure systems, fronts, and cloud formation.
              </p>
            </div>

            <div>
              <div className="flex items-center justify-between text-xs mb-2">
                <span className="text-gray-400">Progress</span>
                <span className="font-semibold">76%</span>
              </div>

              <div className="h-2 rounded-full bg-[#06111f] overflow-hidden">
                <div className="h-full w-[76%] bg-[#f4b400]" />
              </div>

              <p className="mt-2 text-xs text-gray-500">
                Last studied: 19 May 2026
              </p>
            </div>

            <Button className="h-11 bg-[#f4b400] text-[#06111f] hover:bg-[#d9a000] text-sm font-bold">
              Resume
            </Button>
          </div>
        </section>

        <section className="mt-6 grid sm:grid-cols-2 xl:grid-cols-4 gap-4">
          <StatCard title="Questions" value="124" subtitle="Attempted" />
          <StatCard title="Average Score" value="76%" subtitle="All subjects" />
          <StatCard title="Streak" value="3 Days" subtitle="Keep it going" />
          <StatCard title="Mock Exams" value="4" subtitle="Completed" />
        </section>

        <section className="mt-8">
          <div className="flex items-center justify-between">
            <h2 className="text-2xl font-bold">Your Subjects</h2>

            <button className="text-sm text-[#f4b400] hover:text-[#ffd24d] transition">
              View All →
            </button>
          </div>

          <div className="mt-4 grid md:grid-cols-2 xl:grid-cols-3 gap-4">
            {subjects.map((subject) => (
              <div
                key={subject.name}
                className="rounded-xl border border-[#1e3a5f] bg-[#0b1f35] p-4 hover:border-[#f4b400]/60 transition"
              >
                <div className="flex items-center justify-between">
                  <h3 className="text-lg font-bold">{subject.name}</h3>

                  <span className="text-[#f4b400] font-bold">
                    {subject.progress}%
                  </span>
                </div>

                <div className="mt-4 h-1.5 rounded-full bg-[#06111f] overflow-hidden">
                  <div
                    className="h-full bg-[#f4b400]"
                    style={{ width: `${subject.progress}%` }}
                  />
                </div>

                <div className="mt-4 flex items-center justify-between">
                  <p className="text-xs text-gray-400">120 Questions</p>

                  <Button
                    variant="outline"
                    className="h-8 px-4 border-[#f4b400]/50 text-[#f4b400] hover:bg-[#f4b400] hover:text-[#06111f] text-xs"
                  >
                    Practice
                  </Button>
                </div>
              </div>
            ))}
          </div>
        </section>
      </section>
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
      className={`w-full text-left rounded-lg px-4 py-3 text-sm transition ${
        active
          ? "bg-[#0b1f35] text-[#f4b400] border-l-4 border-[#f4b400] font-bold"
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
    <div className="rounded-xl border border-[#1e3a5f] bg-[#0b1f35] p-4">
      <p className="text-sm text-gray-400">{title}</p>
      <h3 className="mt-3 text-3xl font-bold">{value}</h3>
      <p className="mt-2 text-xs text-gray-500">{subtitle}</p>

      <div className="mt-4 h-1 rounded-full bg-[#06111f] overflow-hidden">
        <div className="h-full w-[78%] bg-[#f4b400]" />
      </div>
    </div>
  )
}