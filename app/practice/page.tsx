"use client"

import { useState } from "react"
import { useParams } from "next/navigation"
import Link from "next/link"
import { questions } from "@/src/data/questions"

export default function TopicExamPage() {
  const params = useParams()

  const subject = String(params.subject)
  const topic = String(params.topic)

  const filteredQuestions =
    topic === "exam"
      ? questions.filter(
          (q) => q.subject === subject
        )
      : questions.filter(
          (q) =>
            q.subject === subject &&
            q.topic
              .toLowerCase()
              .replaceAll(" ", "-") === topic
        )

  const [currentQuestionIndex, setCurrentQuestionIndex] =
    useState(0)

  const [answers, setAnswers] =
    useState<Record<number, string>>({})

  const currentQuestion =
    filteredQuestions[currentQuestionIndex]

  if (!currentQuestion) {
    return (
      <main className="min-h-screen bg-white flex items-center justify-center">
        <div className="text-center">

          <h1 className="text-3xl font-bold">
            No questions found
          </h1>

          <Link
            href={`/practice/${subject}`}
            className="mt-6 inline-block rounded-md bg-[#1f4e79] px-5 py-2 text-white"
          >
            Back to Topics
          </Link>

        </div>
      </main>
    )
  }

  const handleAnswer = (
    option: string
  ) => {
    setAnswers({
      ...answers,
      [currentQuestionIndex]:
        option,
    })
  }

  const goNext = () => {
    if (
      currentQuestionIndex <
      filteredQuestions.length - 1
    ) {
      setCurrentQuestionIndex(
        currentQuestionIndex + 1
      )
    }
  }

  const goPrevious = () => {
    if (
      currentQuestionIndex > 0
    ) {
      setCurrentQuestionIndex(
        currentQuestionIndex - 1
      )
    }
  }

  return (
    <main className="min-h-screen bg-white">

      <header className="bg-[#1f4e79] text-white px-6 py-4 flex justify-between">

        <div>

          <h1 className="font-bold">
            PilotVault SA
          </h1>

          <p className="text-sm">

            {subject
              .replaceAll(
                "-",
                " "
              )}{" "}

            •{" "}

            {topic === "exam"
              ? "Full Exam"
              : topic.replaceAll(
                  "-",
                  " "
                )}

          </p>

        </div>

        <Link
          href={`/practice/${subject}`}
          className="bg-white/10 px-4 py-2 rounded"
        >
          Exit
        </Link>

      </header>

      <div className="flex">

        <aside className="w-56 border-r p-4">

          <h2 className="font-bold mb-4">
            Questions
          </h2>

          <div className="grid grid-cols-5 gap-2">

            {filteredQuestions.map(
              (_, index) => (
                <button
                  key={index}
                  onClick={() =>
                    setCurrentQuestionIndex(
                      index
                    )
                  }
                  className={`h-10 rounded border
                  ${
                    currentQuestionIndex ===
                    index
                      ? "bg-[#1f4e79] text-white"
                      : answers[index]
                      ? "bg-blue-100"
                      : "bg-red-50"
                  }`}
                >
                  {index + 1}
                </button>
              )
            )}

          </div>

        </aside>

        <section className="flex-1 p-10">

          <p className="text-sm text-gray-500">

            Question{" "}
            {currentQuestionIndex + 1}

            {" "}of{" "}

            {filteredQuestions.length}

          </p>

          <h2 className="mt-6 text-2xl font-bold">

            {currentQuestion.question}

          </h2>

          <div className="mt-8 space-y-4">

            {currentQuestion.options.map(
              (option) => (
                <label
                  key={option}
                  className="flex items-center gap-4"
                >

                  <input
                    type="radio"
                    checked={
                      answers[
                        currentQuestionIndex
                      ] === option
                    }
                    onChange={() =>
                      handleAnswer(
                        option
                      )
                    }
                  />

                  {option}

                </label>
              )
            )}

          </div>

          <div className="mt-10 flex justify-between">

            <button
              onClick={
                goPrevious
              }
              disabled={
                currentQuestionIndex ===
                0
              }
              className="rounded border px-6 py-2"
            >
              Previous
            </button>

            <button
              onClick={
                goNext
              }
              disabled={
                currentQuestionIndex ===
                filteredQuestions.length -
                  1
              }
              className="rounded bg-[#1f4e79] px-6 py-2 text-white"
            >
              Next
            </button>

          </div>

        </section>

      </div>

    </main>
  )
}