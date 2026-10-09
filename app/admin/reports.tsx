"use client"

import { useCallback, useEffect, useState } from "react"
import { Flag } from "lucide-react"

type Ticket = {
  id: number
  reason: string
  message: string | null
  status: "open" | "resolved" | "dismissed"
  adminNote: string | null
  createdAt: string
  resolvedAt: string | null
  reporter: { email: string | null; name: string | null; isTestAccount: boolean }
  question: {
    id: number
    subject: string
    topic: string | null
    text: string
    options: string[]
    correctAnswer: string
    explanation: string | null
    isTrialQuestion: boolean
  } | null
}

const REASON_LABELS: Record<string, string> = {
  wrong_answer: "Marked answer is wrong",
  question_error: "Mistake in question or options",
  explanation: "Explanation wrong or unclear",
  diagram: "Diagram or image problem",
  other: "Something else",
}

const TABS: { status: Ticket["status"]; label: string }[] = [
  { status: "open", label: "Open" },
  { status: "resolved", label: "Resolved" },
  { status: "dismissed", label: "Dismissed" },
]

function formatDate(value: string | null) {
  if (!value) return "—"
  return new Intl.DateTimeFormat("en-ZA", {
    day: "2-digit",
    month: "short",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
    timeZone: "Africa/Johannesburg",
  }).format(new Date(value))
}

export function QuestionReports({
  authorisedFetch,
  subjectName,
}: {
  authorisedFetch: (input: string, init?: RequestInit) => Promise<Response | null>
  subjectName: (slug: string) => string
}) {
  const [tickets, setTickets] = useState<Ticket[]>([])
  const [tab, setTab] = useState<Ticket["status"]>("open")
  const [error, setError] = useState("")
  const [loaded, setLoaded] = useState(false)

  const load = useCallback(async () => {
    setError("")
    try {
      const response = await authorisedFetch("/api/admin/reports", { cache: "no-store" })
      if (!response) return
      const body = await response.json()
      if (!response.ok) throw new Error(body.error ?? "Could not load question reports.")
      setTickets(body.tickets as Ticket[])
    } catch (loadError) {
      setError(loadError instanceof Error ? loadError.message : "Could not load question reports.")
    } finally {
      setLoaded(true)
    }
  }, [authorisedFetch])

  useEffect(() => {
    void load()
  }, [load])

  const update = async (ticket: Ticket, status: Ticket["status"], note: string) => {
    const response = await authorisedFetch("/api/admin/reports", {
      method: "POST",
      body: JSON.stringify({ id: ticket.id, status, note }),
    })
    if (!response) return
    const body = await response.json()
    if (!response.ok) throw new Error(body.error ?? "The report could not be updated.")
    await load()
  }

  const counts = Object.fromEntries(
    TABS.map((item) => [item.status, tickets.filter((ticket) => ticket.status === item.status).length])
  ) as Record<Ticket["status"], number>
  const visible = tickets.filter((ticket) => ticket.status === tab)

  return (
    <section aria-labelledby="reports-heading" className="rounded-xl border border-slate-200 bg-white p-4 sm:p-5">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <h2 id="reports-heading" className="flex items-center gap-2 text-base font-semibold text-slate-950">
          <Flag className="h-4 w-4 text-[#1f4e79]" />
          Question reports
          {counts.open > 0 && (
            <span className="rounded-full bg-red-600 px-2 py-0.5 text-xs font-bold text-white">{counts.open} open</span>
          )}
        </h2>
        <div className="flex rounded-lg border border-slate-300 p-0.5 text-xs font-semibold" role="tablist">
          {TABS.map((item) => (
            <button
              key={item.status}
              type="button"
              role="tab"
              aria-selected={tab === item.status}
              onClick={() => setTab(item.status)}
              className={`min-h-8 rounded-md px-3 ${
                tab === item.status ? "bg-[#1f4e79] text-white" : "text-slate-600 hover:bg-slate-50"
              }`}
            >
              {item.label} ({counts[item.status]})
            </button>
          ))}
        </div>
      </div>
      <p className="mt-1 text-xs text-slate-500">
        Students report questions with the Report button during practice. Fix the question in the question bank, then
        resolve the ticket.
      </p>

      {error && <p className="mt-3 text-sm text-red-700">{error}</p>}

      {loaded && !visible.length && !error && (
        <p className="mt-3 text-sm text-slate-500">
          {tab === "open" ? "No open reports." : `No ${tab} reports.`}
        </p>
      )}

      <div className="mt-3 space-y-3">
        {visible.map((ticket) => (
          <TicketCard key={ticket.id} ticket={ticket} subjectName={subjectName} onUpdate={update} />
        ))}
      </div>
    </section>
  )
}

function TicketCard({
  ticket,
  subjectName,
  onUpdate,
}: {
  ticket: Ticket
  subjectName: (slug: string) => string
  onUpdate: (ticket: Ticket, status: Ticket["status"], note: string) => Promise<void>
}) {
  const [note, setNote] = useState(ticket.adminNote ?? "")
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState("")
  const question = ticket.question

  const act = async (status: Ticket["status"]) => {
    setBusy(true)
    setError("")
    try {
      await onUpdate(ticket, status, note)
    } catch (updateError) {
      setError(updateError instanceof Error ? updateError.message : "The report could not be updated.")
    } finally {
      setBusy(false)
    }
  }

  return (
    <article className="rounded-lg border border-slate-200 p-4">
      <div className="flex flex-wrap items-center gap-x-3 gap-y-1 text-xs text-slate-500">
        <span className="font-semibold text-slate-900">#{ticket.id}</span>
        <span className="rounded-full bg-amber-50 px-2 py-0.5 font-semibold text-amber-800 ring-1 ring-amber-200">
          {REASON_LABELS[ticket.reason] ?? ticket.reason}
        </span>
        <span>{formatDate(ticket.createdAt)}</span>
        <span>
          by {ticket.reporter.name?.trim() || "—"} ({ticket.reporter.email ?? "unknown"})
        </span>
        {ticket.reporter.isTestAccount && (
          <span className="rounded bg-slate-100 px-1.5 py-0.5 text-[10px] font-semibold uppercase">test</span>
        )}
      </div>

      {ticket.message && (
        <p className="mt-2 rounded-md bg-slate-50 px-3 py-2 text-sm text-slate-800">&ldquo;{ticket.message}&rdquo;</p>
      )}

      {question ? (
        <div className="mt-3 text-sm">
          <p className="text-xs text-slate-500">
            Question {question.id} · {subjectName(question.subject)}
            {question.topic ? ` · ${question.topic}` : ""}
            {question.isTrialQuestion ? " · in the trial mock" : ""}
          </p>
          <p className="mt-1 font-medium text-slate-900">{question.text}</p>
          <ul className="mt-2 space-y-1">
            {question.options.map((option, index) => {
              const correct = option === question.correctAnswer
              return (
                <li
                  key={index}
                  className={`rounded px-2 py-1 ${correct ? "bg-emerald-50 font-semibold text-emerald-900" : "text-slate-700"}`}
                >
                  {String.fromCharCode(65 + index)}. {option}
                  {correct && <span className="ml-2 text-xs font-semibold">(marked correct)</span>}
                </li>
              )
            })}
          </ul>
          {question.explanation && (
            <details className="mt-2">
              <summary className="cursor-pointer text-xs font-semibold text-[#1f4e79]">Explanation</summary>
              <p className="mt-1 whitespace-pre-line text-xs leading-5 text-slate-700">{question.explanation}</p>
            </details>
          )}
        </div>
      ) : (
        <p className="mt-3 text-sm text-slate-500">This question has been deleted.</p>
      )}

      <div className="mt-3 border-t border-slate-100 pt-3">
        <label className="block text-xs font-semibold text-slate-500">
          Admin note
          <textarea
            value={note}
            onChange={(event) => setNote(event.target.value)}
            rows={2}
            placeholder="What was changed, or why no change was needed"
            className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2 text-sm font-normal text-slate-900 outline-none focus:border-[#1f4e79]"
          />
        </label>
        {ticket.status !== "open" && (
          <p className="mt-1 text-xs text-slate-500">
            {ticket.status === "resolved" ? "Resolved" : "Dismissed"} {formatDate(ticket.resolvedAt)}
          </p>
        )}
        {error && <p className="mt-1 text-xs text-red-700">{error}</p>}
        <div className="mt-2 flex flex-wrap gap-2">
          {ticket.status === "open" ? (
            <>
              <button
                type="button"
                disabled={busy}
                onClick={() => void act("resolved")}
                className="inline-flex min-h-9 items-center rounded-lg bg-[#1f4e79] px-3 text-xs font-semibold text-white hover:bg-[#183d60] disabled:opacity-50"
              >
                Mark resolved
              </button>
              <button
                type="button"
                disabled={busy}
                onClick={() => void act("dismissed")}
                className="inline-flex min-h-9 items-center rounded-lg border border-slate-300 bg-white px-3 text-xs font-semibold text-slate-700 hover:bg-slate-50 disabled:opacity-50"
              >
                Dismiss (no change needed)
              </button>
            </>
          ) : (
            <>
              <button
                type="button"
                disabled={busy}
                onClick={() => void act(ticket.status)}
                className="inline-flex min-h-9 items-center rounded-lg border border-slate-300 bg-white px-3 text-xs font-semibold text-slate-700 hover:bg-slate-50 disabled:opacity-50"
              >
                Save note
              </button>
              <button
                type="button"
                disabled={busy}
                onClick={() => void act("open")}
                className="inline-flex min-h-9 items-center rounded-lg border border-slate-300 bg-white px-3 text-xs font-semibold text-slate-700 hover:bg-slate-50 disabled:opacity-50"
              >
                Reopen
              </button>
            </>
          )}
        </div>
      </div>
    </article>
  )
}
