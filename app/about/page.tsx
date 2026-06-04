import Link from "next/link"

export default function AboutPage() {
  return (
    <main className="min-h-screen bg-[#06111f] text-white">
      <header className="border-b border-[#1e3a5f] bg-[#06111f]/95">
        <div className="mx-auto flex min-h-20 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
          <div>
            <p className="text-xs uppercase tracking-[0.25em] text-[#f4b400]">
              PilotVault SA
            </p>
            <h1 className="mt-1 text-lg font-bold">About</h1>
          </div>

          <Link
            href="/"
            className="rounded-xl border border-[#1e3a5f] px-4 py-3 text-sm text-gray-300 transition hover:border-[#f4b400] hover:text-[#f4b400]"
          >
            Back Home
          </Link>
        </div>
      </header>

      <section className="mx-auto max-w-5xl px-4 py-12 sm:px-6 lg:px-8">
        <div className="rounded-3xl border border-[#1e3a5f] bg-[#081726] p-6 sm:p-10">
          <p className="text-xs uppercase tracking-[0.3em] text-[#f4b400]">
            Built for South African student pilots
          </p>

          <h2 className="mt-4 text-4xl font-bold leading-tight sm:text-5xl">
            Helping SACAA students prepare with confidence.
          </h2>

          <p className="mt-6 text-lg leading-8 text-gray-400">
            PilotVault SA was created to help South African student pilots
            prepare for SACAA exams using realistic mock exams, focused
            practice, clear explanations, and a clean study experience.
          </p>

          <p className="mt-5 text-lg leading-8 text-gray-400">
            We understand the pressure of aviation exams because PilotVault SA
            is built from inside the student pilot journey. The goal is simple:
            give pilots a trusted platform that makes exam preparation more
            structured, more realistic, and easier to track.
          </p>
        </div>

        <div className="mt-8 grid gap-6 md:grid-cols-3">
          <div className="rounded-3xl border border-[#1e3a5f] bg-[#081726] p-6">
            <p className="text-xs uppercase tracking-[0.25em] text-[#f4b400]">
              Mission
            </p>
            <h3 className="mt-3 text-xl font-bold">Pass with confidence</h3>
            <p className="mt-3 text-sm leading-6 text-gray-400">
              Help SACAA students prepare through realistic exam practice,
              explanations, and progress-focused learning.
            </p>
          </div>

          <div className="rounded-3xl border border-[#1e3a5f] bg-[#081726] p-6">
            <p className="text-xs uppercase tracking-[0.25em] text-[#f4b400]">
              Focus
            </p>
            <h3 className="mt-3 text-xl font-bold">SACAA exam prep</h3>
            <p className="mt-3 text-sm leading-6 text-gray-400">
              Built around South African aviation theory subjects, from PPL to
              future CPL and ATPL preparation.
            </p>
          </div>

          <div className="rounded-3xl border border-[#1e3a5f] bg-[#081726] p-6">
            <p className="text-xs uppercase tracking-[0.25em] text-[#f4b400]">
              Standard
            </p>
            <h3 className="mt-3 text-xl font-bold">Premium and practical</h3>
            <p className="mt-3 text-sm leading-6 text-gray-400">
              A clean, focused platform designed to feel professional,
              trustworthy, and useful from the first session.
            </p>
          </div>
        </div>

        <div className="mt-8 rounded-3xl border border-[#1e3a5f] bg-[#081726] p-6 sm:p-10">
          <p className="text-xs uppercase tracking-[0.3em] text-[#f4b400]">
            What PilotVault SA offers
          </p>

          <div className="mt-6 grid gap-4 sm:grid-cols-2">
            {[
              "SACAA-focused question banks",
              "25-question mock exams",
              "Detailed answer explanations",
              "Subject-based preparation",
              "Topic-based practice for subscribers",
              "Progress and performance tracking",
            ].map((item) => (
              <div
                key={item}
                className="rounded-2xl border border-[#1e3a5f] bg-[#06111f] p-4 text-sm text-gray-300"
              >
                {item}
              </div>
            ))}
          </div>
        </div>

        <div className="mt-8 rounded-3xl border border-[#f4b400]/30 bg-[#f4b400]/10 p-6 text-center sm:p-8">
          <h3 className="text-2xl font-bold">
            Real Questions. Real Explanations. Real Results.
          </h3>

          <p className="mx-auto mt-3 max-w-2xl text-gray-300">
            PilotVault SA exists to make SACAA exam preparation more focused,
            more realistic, and more accessible for South African student
            pilots.
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