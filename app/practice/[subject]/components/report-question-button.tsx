"use client"

import { useEffect, useRef, useState } from "react"
import { X } from "lucide-react"

import { supabase } from "@/src/lib/supabase"

const REASONS = [
  { value: "wrong_answer", label: "Wrong answer" },
  { value: "question_error", label: "Error in question or options" },
  { value: "explanation", label: "Explanation" },
  { value: "diagram", label: "Diagram or image" },
  { value: "other", label: "Other" },
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
      setStatus({ kind: "error", text: "Choose what is wrong." })
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
              ? "You already reported this question."
              : "Could not send. Please try again.",
        })
        return
      }

      setStatus({ kind: "done", text: "Thanks. We'll review it." })
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
        Report
      </button>

      {open && (
        <div
          className="fixed inset-0 z-50 flex items-end justify-center bg-slate-950/60 backdrop-blur-[2px] sm:items-center sm:p-6"
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
            className="max-h-[92dvh] w-full max-w-md overflow-y-auto rounded-t-3xl bg-white px-5 pb-[max(1.25rem,env(safe-area-inset-bottom))] pt-5 text-slate-900 shadow-2xl outline-none sm:rounded-3xl sm:px-6 sm:pb-6"
          >
            <div className="flex items-start justify-between gap-4">
              <h2 id="report-question-title" className="text-xl font-bold tracking-tight text-slate-950">
                Report question
              </h2>
              <button
                type="button"
                onClick={close}
                aria-label="Close"
                className="-mr-1 -mt-1 rounded-full p-2 text-slate-400 transition hover:bg-slate-100 hover:text-slate-700"
              >
                <X className="h-5 w-5" />
              </button>
            </div>

            {status?.kind === "done" ? (
              <div className="mt-3">
                <p className="text-sm text-slate-600" role="status">
                  {status.text}
                </p>
                <button
                  type="button"
                  onClick={() => setOpen(false)}
                  className="mt-5 w-full rounded-2xl bg-[var(--pv-navy)] px-5 py-3.5 text-base font-bold text-white transition hover:bg-[var(--pv-navy-soft)]"
                >
                  Done
                </button>
              </div>
            ) : (
              <form onSubmit={submit} className="mt-4">
                <fieldset>
                  <legend className="mb-2 text-sm font-bold text-slate-900">What is wrong?</legend>
                  <div className="space-y-1.5">
                    {REASONS.map((option) => (
                      <label
                        key={option.value}
                        className={`flex min-h-11 cursor-pointer items-center gap-3 rounded-xl border px-3.5 text-[15px] font-semibold transition ${
                          reason === option.value
                            ? "border-[var(--pv-navy)] bg-slate-50 text-slate-950"
                            : "border-slate-200 text-slate-700 hover:border-slate-300"
                        }`}
                      >
                        <input
                          type="radio"
                          name="report-reason"
                          value={option.value}
                          checked={reason === option.value}
                          onChange={() => {
                            setReason(option.value)
                            setStatus(null)
                          }}
                          className="h-4 w-4 accent-[var(--pv-navy)]"
                        />
                        {option.label}
                      </label>
                    ))}
                  </div>
                </fieldset>

                <textarea
                  aria-label="Details (optional)"
                  value={message}
                  onChange={(event) => setMessage(event.target.value.slice(0, 1000))}
                  rows={3}
                  placeholder="Details (optional)"
                  className="mt-4 w-full rounded-xl border border-slate-300 px-3.5 py-3 text-sm text-slate-900 outline-none placeholder:text-slate-400 focus:border-[var(--pv-navy)]"
                />

                {status?.kind === "error" && (
                  <p className="mt-2 text-sm text-red-700" role="alert">
                    {status.text}
                  </p>
                )}

                <button
                  type="submit"
                  disabled={submitting}
                  className="mt-4 w-full rounded-2xl bg-[var(--pv-navy)] px-5 py-3.5 text-base font-bold text-white transition hover:bg-[var(--pv-navy-soft)] disabled:opacity-60"
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
