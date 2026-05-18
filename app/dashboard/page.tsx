"use client"

import {
  LayoutDashboard,
  BookOpen,
  ClipboardCheck,
  BarChart3,
  Settings,
  ChevronRight,
  Target,
  Flame,
} from "lucide-react"

import { Button } from "@/components/ui/button"

const subjects = [
  "Air Law",
  "Meteorology",
  "Navigation",
  "Human Performance",
  "Principles of Flight",
  "Aircraft Technical",
]

export default function DashboardPage() {
  return (
    <main className="min-h-screen bg-[#06111f] text-white flex">
      {/* Sidebar */}
      <aside className="hidden lg:flex w-72 border-r border-[#1e3a5f] bg-[#081726] p-6 flex-col">
        <div>
          <p className="text-[#f4b400] text-sm tracking-[0.3em] font-bold">
            PILOTVAULT SA
          </p>

          <div className="mt-10 space-y-2">
            <SidebarItem icon={<LayoutDashboard size={18} />} label="Dashboard" active />
            <SidebarItem icon={<BookOpen size={18} />} label="Practice" />
            <SidebarItem icon={<ClipboardCheck size={18} />} label="Mock Exams" />
            <SidebarItem icon={<BarChart3 size={18} />} label="Analytics" />
            <SidebarItem icon={<Settings size={18} />} label="Settings" />
          </div>
        </div>

        <div className="mt-auto rounded-2xl border border-[#1e3a5f] bg-[#0b1f35] p-5">
          <p className="text-sm text-gray-400">Current Plan</p>

          <h3 className="mt-2 text-xl font-bold text-[#f4b400]">
            Free Trial
          </h3>

          <p className="mt-2 text-sm text-gray-400">
            3 days remaining
          </p>

          <Button className="mt-4 w-full bg-[#f4b400] text-[#06111f] hover:bg-[#d9a000] font-bold">
            Upgrade Plan
          </Button>
        </div>
      </aside>

      {/* Main Content */}
      <section className="flex-1 p-6 lg:p-10">
        {/* Top */}
        <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-6">
          <div>
            <p className="text-[#f4b400] text-sm tracking-[0.25em] uppercase font-semibold">
              Dashboard
            </p>

            <h1 className="mt-3 text-4xl font-bold">
              Welcome back, pilot.
            </h1>

            <p className="mt-3 text-gray-400 max-w-2xl">
              Continue preparing for your SACAA exams with focused practice and realistic mock exams.
            </p>
          </div>

          {/* Score Ring */}
          <div className="rounded-3xl border border-[#1e3a5f] bg-[#0b1f35] p-6 w-full lg:w-[300px]">
            <p className="text-sm text-gray-400">
              Overall Progress
            </p>

            <div className="mt-5 flex items-center gap-5">
              <div className="relative w-24 h-24 rounded-full border-8 border-[#f4b400] flex items-center justify-center">
                <span className="text-2xl font-bold">
                  76%
                </span>
              </div>

              <div>
                <p className="text-2xl font-bold">
                  Good Progress
                </p>

                <p className="mt-1 text-sm text-gray-400">
                  Keep pushing toward 85%+
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Continue Studying */}
        <section className="mt-8 rounded-3xl border border-[#1e3a5f] bg-[#0b1f35] p-6 lg:p-8">
          <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-6">
            <div>
              <p className="text-sm uppercase tracking-[0.2em] text-[#f4b400]">
                Continue Studying
              </p>

              <h2 className="mt-3 text-3xl font-bold">
                Meteorology
              </h2>

              <p className="mt-3 text-gray-400">
                Focus on pressure systems, fronts, and cloud formation.
              </p>
            </div>

            <Button className="bg-[#f4b400] text-[#06111f] hover:bg-[#d9a000] font-bold px-8 py-6">
              Resume Practice
            </Button>
          </div>
        </section>

        {/* Stats */}
        <section className="mt-8 grid sm:grid-cols-2 xl:grid-cols-4 gap-4">
          <StatCard title="Questions Practised" value="124" icon={<BookOpen />} />
          <StatCard title="Average Score" value="76%" icon={<Target />} />
          <StatCard title="Study Streak" value="3 Days" icon={<Flame />} />
          <StatCard title="Mock Exams" value="4" icon={<ClipboardCheck />} />
        </section>

        {/* Subjects */}
        <section className="mt-10">
          <div className="flex items-center justify-between">
            <h2 className="text-2xl font-bold">
              Subjects
            </h2>

            <button className="text-sm text-[#f4b400] flex items-center gap-1">
              View All
              <ChevronRight size={16} />
            </button>
          </div>

          <div className="mt-5 grid md:grid-cols-2 xl:grid-cols-3 gap-4">
            {subjects.map((subject) => (
              <div
                key={subject}
                className="rounded-2xl border border-[#1e3a5f] bg-[#0b1f35] p-6 hover:border-[#f4b400]/60 transition cursor-pointer"
              >
                <div className="flex items-center justify-between">
                  <BookOpen className="text-[#f4b400]" />

                  <span className="text-sm text-gray-400">
                    120 Questions
                  </span>
                </div>

                <h3 className="mt-5 text-xl font-bold">
                  {subject}
                </h3>

                <p className="mt-2 text-sm text-gray-400">
                  Practice SACAA-style questions with explanations.
                </p>

                <div className="mt-5 h-2 rounded-full bg-[#06111f] overflow-hidden">
                  <div className="h-full w-[76%] bg-[#f4b400]" />
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
  icon,
  label,
  active = false,
}: {
  icon: React.ReactNode
  label: string
  active?: boolean
}) {
  return (
    <button
      className={`w-full flex items-center gap-3 rounded-xl px-4 py-3 transition ${
        active
          ? "bg-[#f4b400] text-[#06111f] font-bold"
          : "text-gray-300 hover:bg-[#0b1f35]"
      }`}
    >
      {icon}
      {label}
    </button>
  )
}

function StatCard({
  title,
  value,
  icon,
}: {
  title: string
  value: string
  icon: React.ReactNode
}) {
  return (
    <div className="rounded-2xl border border-[#1e3a5f] bg-[#0b1f35] p-5">
      <div className="flex items-center justify-between">
        <p className="text-sm text-gray-400">
          {title}
        </p>

        <div className="text-[#f4b400]">
          {icon}
        </div>
      </div>

      <h3 className="mt-4 text-3xl font-bold">
        {value}
      </h3>
    </div>
  )
}