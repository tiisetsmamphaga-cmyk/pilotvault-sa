"use client"

import { ArrowLeft } from "lucide-react"

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
        <div className="rounded-2xl border border-[#29476d] bg-[#0b1d31] p-4 sm:p-5">
          <h2 className="text-2xl font-bold tracking-tight">
            Choose a topic
          </h2>
          <div className="mt-2.5 h-0.5 w-10 rounded-full bg-[#f4b400]" />
        </div>

        <div className="mt-3 grid gap-3 md:grid-cols-2">
          {topics.map((topic) => {
            const questionCount = topicQuestionCounts[topic]

            return (
              <button
                type="button"
                key={topic}
                onClick={() => onStartTopic(topic)}
                className="group flex min-h-[70px] items-center justify-between gap-4 rounded-xl border border-[#29476d] bg-[#0b1d31] px-4 py-3.5 text-left transition-all hover:-translate-y-px hover:border-[#f4b400] hover:bg-[#0d2238] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#f4b400]/70"
              >
                <h3 className="text-base font-semibold leading-snug text-white transition group-hover:text-[#f4b400] sm:text-lg">
                  {topic}
                </h3>

                <span className="shrink-0 text-xs font-medium text-[#b8c7d9]">
                  {questionCount} question{questionCount === 1 ? "" : "s"}
                </span>
              </button>
            )
          })}
        </div>
      </section>
    </main>
  )
}
