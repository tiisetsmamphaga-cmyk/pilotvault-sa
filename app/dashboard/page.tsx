"use client"

import Link from "next/link"

const subjects = [
  { name: "Meteorology", progress: 76 },
  { name: "Air Law", progress: 72 },
  { name: "Navigation", progress: 68 },
  { name: "Principles of Flight", progress: 65 },
]

export default function DashboardPage() {
  return (
    <main className="min-h-screen bg-[#06111f] text-white">

      {/* Header */}

      <header className="border-b border-[#1e3a5f] bg-[#06111f]/95 backdrop-blur sticky top-0 z-40">

        <div className="mx-auto flex min-h-20 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">

          <div>
            <p className="text-xs uppercase tracking-[0.25em] text-[#f4b400]">
              PilotVault SA
            </p>

            <h1 className="mt-1 text-lg font-bold">
              Dashboard
            </h1>
          </div>

          <Link
            href="/"
            className="rounded-xl bg-[#f4b400] px-4 py-2 text-sm font-bold text-[#06111f] hover:bg-[#d9a000]"
          >
            Home
          </Link>

        </div>

      </header>

      <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">

        {/* Welcome */}

        <div className="rounded-3xl border border-[#1e3a5f] bg-[#081726] p-6 lg:p-8">

          <p className="text-xs uppercase tracking-[0.25em] text-[#f4b400]">
            Welcome Back
          </p>

          <h2 className="mt-3 text-3xl font-bold">
            Continue your SACAA preparation
          </h2>

          <p className="mt-4 max-w-2xl text-gray-400">
            Keep building confidence with realistic questions,
            mock exams and progress tracking.
          </p>

          <div className="mt-6 flex flex-col gap-4 sm:flex-row">

            <Link
              href="/practice/meteorology"
              className="rounded-xl bg-[#f4b400] px-6 py-3 text-center font-bold text-[#06111f] hover:bg-[#d9a000]"
            >
              Resume Meteorology
            </Link>

            <Link
              href="/practice/meteorology"
              className="rounded-xl border border-[#1e3a5f] bg-[#0b1f35] px-6 py-3 text-center font-semibold hover:bg-[#1e3a5f]"
            >
              Start Mock Exam
            </Link>

          </div>

        </div>

        {/* Subjects */}

        <div className="mt-8">

          <h3 className="mb-5 text-xl font-bold">
            Subjects
          </h3>

          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">

            {subjects.map((subject) => (

              <Link
                key={subject.name}
                href={`/practice/${subject.name.toLowerCase().replaceAll(" ","-")}`}
                className="rounded-2xl border border-[#1e3a5f] bg-[#081726] p-5 hover:border-[#f4b400]"
              >
                <h4 className="font-bold">
                  {subject.name}
                </h4>

                <div className="mt-4 h-2 overflow-hidden rounded-full bg-[#06111f]">

                  <div
                    className="h-full bg-[#f4b400]"
                    style={{
                      width: `${subject.progress}%`,
                    }}
                  />

                </div>

                <p className="mt-3 text-sm text-gray-400">
                  {subject.progress}% complete
                </p>

              </Link>

            ))}

          </div>

        </div>

        {/* Progress */}

        <div className="mt-8 rounded-2xl border border-[#1e3a5f] bg-[#081726] p-6">

          <h3 className="text-xl font-bold">
            Progress Summary
          </h3>

          <div className="mt-6 grid gap-4 sm:grid-cols-3">

            <div className="rounded-xl bg-[#0b1f35] p-5">
              <p className="text-sm text-gray-400">
                Questions Answered
              </p>

              <p className="mt-2 text-3xl font-bold text-[#f4b400]">
                124
              </p>
            </div>

            <div className="rounded-xl bg-[#0b1f35] p-5">
              <p className="text-sm text-gray-400">
                Average Score
              </p>

              <p className="mt-2 text-3xl font-bold text-[#f4b400]">
                82%
              </p>
            </div>

            <div className="rounded-xl bg-[#0b1f35] p-5">
              <p className="text-sm text-gray-400">
                Weak Topic
              </p>

              <p className="mt-2 text-lg font-bold text-[#f4b400]">
                Weather Fronts
              </p>
            </div>

          </div>

        </div>

      </div>

    </main>
  )
}