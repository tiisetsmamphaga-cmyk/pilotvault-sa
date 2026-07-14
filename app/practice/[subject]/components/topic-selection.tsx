"use client"

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
  return (
    <main className="min-h-screen bg-[#06111f] px-4 py-10 text-white sm:px-6">
      <div className="mx-auto max-w-5xl">
        <button
          onClick={onBack}
          className="text-sm font-medium text-[#f4b400] hover:text-white"
        >
          ← Back to Training Modes
        </button>

        <div className="mt-8 rounded-3xl border border-[#1e3a5f] bg-[#081726] p-6 sm:p-8">
          <p className="text-xs uppercase tracking-[0.25em] text-[#f4b400]">
            {formatSubjectName(subject)}
          </p>

          <h1 className="mt-3 text-3xl font-bold sm:text-4xl">
            Choose a topic
          </h1>

          <p className="mt-3 max-w-2xl text-gray-400">
            Every available question from the selected topic will be loaded.
          </p>
        </div>

        <div className="mt-8 grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
          {topics.map((topic) => (
            <button
              key={topic}
              onClick={() => onStartTopic(topic)}
              className="group rounded-2xl border border-[#1e3a5f] bg-[#081726] p-6 text-left transition-all hover:-translate-y-1 hover:border-[#f4b400]"
            >
              <h2 className="text-xl font-bold text-white">{topic}</h2>

              <p className="mt-3 text-sm text-gray-400">
                {topicQuestionCounts[topic]} question
                {topicQuestionCounts[topic] === 1 ? "" : "s"} available
              </p>

              <p className="mt-5 text-sm font-medium text-[#f4b400] transition group-hover:text-[#ffd24d]">
                Practice All Questions →
              </p>
            </button>
          ))}
        </div>
      </div>
    </main>
  )
}
