"use client"

import { ArrowLeft, ArrowRight, BookOpen } from "lucide-react"

import { formatSubjectName } from "../practice-utils"

type TopicSelectionProps = {
  subject: string
  topics: string[]
  topicQuestionCounts: Record<string, number>
  onBack: () => void
  onStartTopic: (topic: string) => void
}

export function TopicSelection({
  subject,
  topics,
  topicQuestionCounts,
  onBack,
  onStartTopic,
}: TopicSelectionProps) {
  const subjectName = formatSubjectName(subject)

  return (
    <main className="min-h-screen bg-[#071522] text-white">
      <header className="border-b border-[#29476d] bg-[#081726]/95">
        <div className="mx-auto flex min-h-16 max-w-7xl items-center justify-between gap-3 px-4 sm:min-h-20 sm:px-6 lg:px-8">
          <div className="min-w-0">
            <p className="text-[10px] uppercase tracking-[0.22em] text-[#f4b400] sm:text-xs sm:tracking-[0.25em]">
              PilotVault SA
            </p>
            <h1 className="mt-1 truncate text-base font-bold sm:text-lg">
              {subjectName}
            </h1>
          </div>

          <button
            type="button"
            onClick={onBack}
            aria-label="Back to training modes"
            title="Back to training modes"
            className="inline-flex h-10 w-10 items-center justify-center rounded-full bg-white text-[#071426] shadow-[0_6px_18px_rgba(15,23,42,0.12)] transition hover:-translate-x-0.5 hover:bg-[#f4b400] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#f4b400]/70"
          >
            <ArrowLeft className="h-[19px] w-[19px]" />
          </button>
        </div>
      </header>

      <section className="mx-auto max-w-7xl px-4 py-8 sm:px-6 sm:py-10 lg:px-8">
        <div className="rounded-3xl border border-[#29476d] bg-[#0b1d31] p-5 shadow-[0_18px_50px_rgba(0,0,0,0.14)] sm:p-8">
          <h2 className="text-2xl font-bold tracking-tight sm:text-3xl">
            Choose a topic
          </h2>
          <p className="mt-2 text-sm leading-6 text-[#b8c7d9] sm:text-base">
            Select an area to begin focused practice.
          </p>
        </div>

        <div className="mt-5 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {topics.map((topic) => {
            const questionCount = topicQuestionCounts[topic]

            return (
              <button
                type="button"
                key={topic}
                onClick={() => onStartTopic(topic)}
                className="group flex min-h-[160px] flex-col rounded-2xl border border-[#29476d] bg-[#0b1d31] p-5 text-left shadow-[0_14px_40px_rgba(0,0,0,0.12)] transition-all hover:-translate-y-1 hover:border-[#f4b400] hover:bg-[#0d2238] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#f4b400]/70"
              >
                <div className="flex items-start justify-between gap-4">
                  <span className="flex h-10 w-10 items-center justify-center rounded-xl bg-[#f4b400]/20 text-[#f4b400]">
                    <BookOpen className="h-[18px] w-[18px]" />
                  </span>

                  <span className="rounded-full border border-[#29476d] bg-[#071522]/70 px-3 py-1.5 text-xs font-semibold text-[#b8c7d9]">
                    {questionCount} question{questionCount === 1 ? "" : "s"}
                  </span>
                </div>

                <div className="mt-auto flex items-end justify-between gap-4 pt-5">
                  <h3 className="text-lg font-bold leading-snug text-white sm:text-xl">
                    {topic}
                  </h3>

                  <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-[#f4b400] text-[#06111f] transition group-hover:bg-[#ffc62a]">
                    <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-0.5" />
                  </span>
                </div>
              </button>
            )
          })}
        </div>
      </section>
    </main>
  )
}
