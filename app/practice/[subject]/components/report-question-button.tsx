"use client"

import { useEffect, useRef, useState } from "react"
import { Flag, X } from "lucide-react"

import { supabase } from "@/src/lib/supabase"

const REASONS = [
  { value: "wrong_answer", label: "The marked answer is wrong" },
  { value: "question_error", label: "Mistake in the question or options" },
  { value: "explanation", label: "Explanation is wrong or unclear" },
  { value: "diagram", label: "Problem with a diagram or image" },
  { value: "other", label: "Something else" },
] as const

type Reason = (typeof REASONS)[number]["value"]

export function ReportQuestionButton({
  questionId,
  className,
}: {
  questionId: number
  className?: string
}) {
  const [open, setOpen] = useState(false)
  const [reason, setReason] = useState<Reason | "">("")
  const [message, setMessage] = useState("")
  const [submitting, setSubmitting] = useState(false)
  const [status, setStatus] = useState<{ kind: "error" | "done"; text: string } | null>(null)
  const dialogRef = useRef<HTMLDivElement>(null)

  const close = () => {
    if (submitting) return
    setOpen(false)
  }

  useEffect(() => {
    if (!open) return

    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") close()
    }

    window.addEventListener("keydown", onKeyDown)
    dialogRef.current?.focus()

    return () => window.removeEventListener("keydown", onKeyDown)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [open])

  const openDialog = () => {
    setReason("")
    setMessage("")
    setStatus(null)
    setOpen(true)
  }

  const submit = async (event: React.FormEvent) => {
    event.preventDefault()

    if (!reason) {
      setStatus({ kind: "error", text: "Choose what is wrong with this question." })
      return
    }

    setSubmitting(true)
    setStatus(null)

    try {
      const { data } = await supabase.auth.getSession()
      const userId = data.session?.user.id

      if (!userId) {
        setStatus({ kind: "error", text: "Please log in again to report a question." })
        return
      }

      const { error } = await supabase.from("QuestionReports").insert({
        question_id: questionId,
        user_id: userId,
        reason,
        message: message.trim() || null,
      })

      if (error) {
        setStatus({
          kind: error.code === "23505" ? "done" : "error",
          text:
            error.code === "23505"
              ? "You have already reported this question. We are looking into it."
              : "Your report could not be sent. Please try again.",
        })
        return
      }

      setStatus({ kind: "done", text: "Thank you. We will review this question." })
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <>
      <button
        type="button"
        onClick={openDialog}
        className={
          className ??
          "inline-flex items-center gap-1.5 rounded-md border border-slate-300 bg-white px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-100"
        }
      >
        <Flag className="h-4 w-4" aria-hidden="true" />
        Report
      </button>

      {open && (
        <div
          className="fixed inset-0 z-50 flex items-end justify-center bg-slate-950/50 p-4 sm:items-center"
          role="presentation"
          onClick={close}
        >
          <div
            ref={dialogRef}
            role="dialog"
            aria-modal="true"
            aria-labelledby="report-question-title"
            tabIndex={-1}
            onClick={(event) => event.stopPropagation()}
            className="w-full max-w-md rounded-xl bg-white p-5 text-slate-900 shadow-xl outline-none sm:p-6"
          >
            <div className="flex items-start justify-between gap-3">
              <h2 id="report-question-title" className="text-lg font-semibold">
                Report this question
              </h2>
              <button
                type="button"
                onClick={close}
                aria-label="Close"
                className="rounded-md p-1 text-slate-500 hover:bg-slate-100 hover:text-slate-800"
              >
                <X className="h-5 w-5" />
              </button>
            </div>

            {status?.kind === "done" ? (
              <div className="mt-4">
                <p className="text-sm text-slate-700" role="status">
                  {status.text}
                </p>
                <button
                  type="button"
                  onClick={() => setOpen(false)}
                  className="mt-5 w-full rounded-md bg-[#1f4e79] px-4 py-2.5 text-sm font-semibold text-white hover:bg-[#183d60]"
                >
                  Back to the question
                </button>
              </div>
            ) : (
              <form onSubmit={submit} className="mt-3">
                <fieldset>
                  <legend className="text-sm text-slate-600">What is wrong?</legend>
                  <div className="mt-2 space-y-2">
                    {REASONS.map((option) => (
                      <label
                        key={option.value}
                        className={`flex cursor-pointer items-center gap-3 rounded-md border px-3 py-2.5 text-sm ${
                          reason === option.value ? "border-[#1f4e79] bg-blue-50" : "border-slate-200 hover:bg-slate-50"
                        }`}
                      >
                        <input
                          type="radio"
                          name="report-reason"
                          value={option.value}
                          checked={reason === option.value}
                          onChange={() => setReason(option.value)}
                          className="h-4 w-4 accent-[#1f4e79]"
                        />
                        {option.label}
                      </label>
                    ))}
                  </div>
                </fieldset>

                <label className="mt-4 block text-sm text-slate-600">
                  Details (optional)
                  <textarea
                    value={message}
                    onChange={(event) => setMessage(event.target.value.slice(0, 1000))}
                    rows={3}
                    placeholder="For example: the answer should be C because..."
                    className="mt-1.5 w-full rounded-md border border-slate-300 px-3 py-2 text-sm text-slate-900 outline-none focus:border-[#1f4e79]"
                  />
                </label>

                {status?.kind === "error" && (
                  <p className="mt-2 text-sm text-red-700" role="alert">
                    {status.text}
                  </p>
                )}

                <button
                  type="submit"
                  disabled={submitting}
                  className="mt-4 w-full rounded-md bg-[#1f4e79] px-4 py-2.5 text-sm font-semibold text-white hover:bg-[#183d60] disabled:opacity-60"
                >
                  {submitting ? "Sending..." : "Send report"}
                </button>
              </form>
            )}
          </div>
        </div>
      )}
    </>
  )
}
