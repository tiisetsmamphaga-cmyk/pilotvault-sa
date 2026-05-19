"use client"

import Link from "next/link"
import { useParams } from "next/navigation"
import { questions } from "@/src/data/questions"

export default function SubjectTopicsPage() {
  const params = useParams()
  const subject = String(params.subject)

  const subjectQuestions = questions.filter((q) => q.subject === subject)

  const topics = Array.from(
    new Set(subjectQuestions.map((q) => q.topic))
  ).filter(Boolean)

  return (
    <main className="min-h-screen bg-[#06111f] px-6 py-10 text-white">
      <div className="mx-auto max-w-6xl">
        <Link
          href="/practice"
          className="text-sm font-medium text-[#f4b400] hover:text-white"
        >
          ← Back to Practice
        </Link>

        <div className="mt-10">
          <p className="text-xs uppercase tracking-[0.18em] text-[#f4b400]">
            Practice Mode
          </p>

          <h1 className="mt-3 text-4xl font-bold capitalize">
            {subject.replaceAll("-", " ")}
          </h1>

          <p className="mt-4 max-w-2xl text-slate-300">
            Choose a full exam simulation or focus on a specific topic.
          </p>
        </div>

        <div className="mt-10 grid gap-5 md:grid-cols-2 lg:grid-cols-3">
          <Link
            href={`/practice/${subject}/exam`}
            className="rounded-2xl border border-[#f4b400]/40 bg-[#081726] p-6 transition hover:-translate-y-1 hover:border-[#f4b400]"
          >
            <p className="text-sm uppercase tracking-wider text-[#f4b400]">
              Full Exam
            </p>

            <h2 className="mt-3 text-2xl font-bold">All Topics</h2>

            <p className="mt-3 text-sm text-slate-300">
              Practice all available questions for this subject in one exam
              session.
            </p>

            <p className="mt-6 text-sm text-slate-400">
              {subjectQuestions.length} questions available
            </p>
          </Link>

          {topics.map((topic) => {
            const topicSlug = topic.toLowerCase().replaceAll(" ", "-")
            const count = subjectQuestions.filter(
              (q) => q.topic === topic
            ).length

            return (
              <Link
                key={topic}
                href={`/practice/${subject}/${topicSlug}`}
                className="rounded-2xl border border-[#1e3a5f] bg-[#081726] p-6 transition hover:-translate-y-1 hover:border-[#f4b400]"
              >
                <p className="text-sm uppercase tracking-wider text-[#f4b400]">
                  Topic Practice
                </p>

                <h2 className="mt-3 text-2xl font-bold">{topic}</h2>

                <p className="mt-3 text-sm text-slate-300">
                  Focus only on {topic.toLowerCase()} questions.
                </p>

                <p className="mt-6 text-sm text-slate-400">
                  {count} questions available
                </p>
              </Link>
            )
          })}
        </div>
      </div>
    </main>
  )
}