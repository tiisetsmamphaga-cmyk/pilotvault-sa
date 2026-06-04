import Link from "next/link"
import {
  BookOpen,
  Timer,
  BarChart3,
  Target,
  Lock,
  CheckCircle,
} from "lucide-react"

const features = [
  {
    icon: BookOpen,
    title: "SACAA Question Bank",
    text: "Practice with aviation theory questions structured around South African SACAA subjects.",
  },
  {
    icon: Timer,
    title: "25-Question Mock Exams",
    text: "Simulate exam conditions with timed mock exams, question navigation, and final scoring.",
  },
  {
    icon: Target,
    title: "Topic-Based Practice",
    text: "Focus on specific topics and strengthen weak areas. Available with subscription.",
  },
  {
    icon: BarChart3,
    title: "Progress Tracking",
    text: "Track performance, review incorrect answers, and monitor your exam readiness.",
  },
  {
    icon: CheckCircle,
    title: "Clear Explanations",
    text: "Understand why answers are correct with simple, focused explanations.",
  },
  {
    icon: Lock,
    title: "Trial & Subscription Access",
    text: "Start with a limited trial, then unlock the full PilotVault experience with a paid plan.",
  },
]

export default function FeaturesPage() {
  return (
    <main className="min-h-screen bg-[#06111f] text-white">
      <header className="border-b border-[#1e3a5f] bg-[#06111f]/95">
        <div className="mx-auto flex min-h-20 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
          <div>
            <p className="text-xs uppercase tracking-[0.25em] text-[#f4b400]">
              PilotVault SA
            </p>
            <h1 className="mt-1 text-lg font-bold">Features</h1>
          </div>

          <Link
            href="/"
            className="rounded-xl border border-[#1e3a5f] px-4 py-3 text-sm text-gray-300 transition hover:border-[#f4b400] hover:text-[#f4b400]"
          >
            Back Home
          </Link>
        </div>
      </header>

      <section className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-3xl text-center">
          <p className="text-xs uppercase tracking-[0.3em] text-[#f4b400]">
            Built for focused exam preparation
          </p>

          <h2 className="mt-4 text-4xl font-bold sm:text-5xl">
            Everything you need to prepare smarter.
          </h2>

          <p className="mt-5 text-lg leading-8 text-gray-400">
            PilotVault SA combines mock exams, question banks, explanations,
            and progress tools into one clean SACAA-focused study platform.
          </p>
        </div>

        <div className="mt-12 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {features.map((feature) => (
            <div
              key={feature.title}
              className="rounded-3xl border border-[#1e3a5f] bg-[#081726] p-6 transition hover:-translate-y-1 hover:border-[#f4b400]"
            >
              <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-[#f4b400]/10">
                <feature.icon className="h-6 w-6 text-[#f4b400]" />
              </div>

              <h3 className="mt-5 text-xl font-bold">{feature.title}</h3>

              <p className="mt-3 text-sm leading-6 text-gray-400">
                {feature.text}
              </p>
            </div>
          ))}
        </div>

        <div className="mt-12 rounded-3xl border border-[#f4b400]/30 bg-[#f4b400]/10 p-6 text-center sm:p-8">
          <h3 className="text-2xl font-bold">
            Built to help you pass with confidence.
          </h3>

          <p className="mx-auto mt-3 max-w-2xl text-gray-300">
            Start with a trial mock exam, then upgrade to unlock the full
            question bank and topic-based practice.
          </p>

          <Link
            href="/dashboard"
            className="mt-6 inline-flex rounded-xl bg-[#f4b400] px-6 py-3 text-sm font-bold text-[#06111f] transition hover:bg-[#d9a000]"
          >
            Start Practicing
          </Link>
        </div>
      </section>
    </main>
  )
}