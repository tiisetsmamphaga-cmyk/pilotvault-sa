"use client"
import { BookOpen, BarChart3, Flame, Target, Clock, Plane } from "lucide-react"
import { Button } from "@/components/ui/button"

const subjects = [
  "Air Law",
  "Meteorology",
  "Navigation",
  "Human Performance",
  "Principles of Flight",
  "Aircraft Technical",
  "Radio Telephony",
  "Flight Planning",
]

export default function DashboardPage() {
  return (
    <main className="min-h-screen bg-[#06111f] text-white px-4 py-8">
      <div className="max-w-7xl mx-auto space-y-8">
        <section className="rounded-3xl border border-[#1e3a5f] bg-[#0b1f35] p-6 md:p-8">
          <p className="text-[#f4b400] text-sm font-semibold uppercase tracking-[0.25em]">
            PilotVault SA
          </p>

          <h1 className="mt-4 text-3xl md:text-5xl font-bold">
            Welcome back, pilot.
          </h1>

          <p className="mt-3 max-w-2xl text-gray-300">
            Continue your SACAA exam preparation with focused practice, mock exams, and weak-topic tracking.
          </p>

          <div className="mt-6 flex flex-col sm:flex-row gap-3">
            <Button className="bg-[#f4b400] text-[#06111f] hover:bg-[#d9a000] font-bold">
              Start Practice
            </Button>

            <Button variant="outline" className="border-[#1e3a5f] text-white hover:bg-[#1e3a5f]">
              Start Mock Exam
            </Button>
          </div>
        </section>

        <section className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          <StatCard icon={<BookOpen />} label="Questions Practised" value="124" />
          <StatCard icon={<Target />} label="Average Score" value="76%" />
          <StatCard icon={<Flame />} label="Study Streak" value="3 days" />
          <StatCard icon={<Clock />} label="Mock Exams" value="4" />
        </section>

        <section>
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-2xl font-bold">Subjects</h2>
            <p className="text-sm text-gray-400">Choose a subject to practise</p>
          </div>

          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
            {subjects.map((subject) => (
              <div
                key={subject}
                className="rounded-2xl border border-[#1e3a5f] bg-[#0b1f35] p-5 hover:border-[#f4b400]/70 transition"
              >
                <Plane className="h-6 w-6 text-[#f4b400] mb-4" />
                <h3 className="font-semibold">{subject}</h3>
                <p className="mt-2 text-sm text-gray-400">
                  Practice questions and review explanations.
                </p>
              </div>
            ))}
          </div>
        </section>

        <section className="grid lg:grid-cols-2 gap-4">
          <div className="rounded-2xl border border-[#1e3a5f] bg-[#0b1f35] p-6">
            <BarChart3 className="h-7 w-7 text-[#f4b400] mb-4" />
            <h2 className="text-xl font-bold">Recent Performance</h2>
            <p className="mt-2 text-gray-400">
              Your latest mock exam score was 76%. Keep pushing toward 85%+ before booking.
            </p>
          </div>

          <div className="rounded-2xl border border-[#1e3a5f] bg-[#0b1f35] p-6">
            <Target className="h-7 w-7 text-[#f4b400] mb-4" />
            <h2 className="text-xl font-bold">Weak Topics</h2>
            <p className="mt-2 text-gray-400">
              Focus areas: Meteorology, Navigation calculations, and Air Law procedures.
            </p>
          </div>
        </section>
      </div>
    </main>
  )
}

function StatCard({
  icon,
  label,
  value,
}: {
  icon: React.ReactNode
  label: string
  value: string
}) {
  return (
    <div className="rounded-2xl border border-[#1e3a5f] bg-[#0b1f35] p-5">
      <div className="text-[#f4b400] mb-4">{icon}</div>
      <p className="text-2xl font-bold">{value}</p>
      <p className="mt-1 text-sm text-gray-400">{label}</p>
    </div>
  )
}