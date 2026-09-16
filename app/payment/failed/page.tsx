"use client"

import { Suspense } from "react"
import Link from "next/link"
import { useSearchParams } from "next/navigation"
import { AlertTriangle, XCircle } from "lucide-react"

function PaymentFailedContent() {
  const searchParams = useSearchParams()
  const reason = searchParams.get("reason")
  const reference = searchParams.get("reference")

  const wasCharged = reason === "fulfilment-error"

  return (
    <main className="flex min-h-screen items-center justify-center bg-[#f8fafc] px-4 py-10 text-slate-900 sm:px-6">
      <section
        className={`w-full max-w-xl rounded-3xl border bg-white p-6 text-center shadow-xl sm:p-10 ${
          wasCharged ? "border-amber-200" : "border-red-200"
        }`}
      >
        <span
          className={`mx-auto flex h-16 w-16 items-center justify-center rounded-2xl ${
            wasCharged ? "bg-amber-50" : "bg-red-50"
          }`}
        >
          {wasCharged ? (
            <AlertTriangle className="h-9 w-9 text-amber-600" />
          ) : (
            <XCircle className="h-9 w-9 text-red-600" />
          )}
        </span>

        <p
          className={`mt-6 text-xs font-semibold uppercase tracking-[0.28em] ${
            wasCharged ? "text-amber-600" : "text-red-600"
          }`}
        >
          {wasCharged ? "Payment received" : "Payment not completed"}
        </p>

        <h1 className="mt-3 text-3xl font-bold tracking-tight text-slate-900 sm:text-4xl">
          {wasCharged
            ? "We're still finishing setting up your access."
            : "Your account was not charged or unlocked."}
        </h1>

        <p className="mt-4 text-sm leading-7 text-slate-600 sm:text-base">
          {wasCharged
            ? "Your payment went through, but activating your access hit a snag on our side. This usually resolves itself within a few minutes as we automatically retry. If it's still locked after that, contact support with the reference below."
            : "The transaction could not be verified. You can safely return to the upgrade page and try again."}
        </p>

        {wasCharged && reference && (
          <p className="mt-3 rounded-xl bg-amber-50 px-4 py-2 text-xs font-medium text-amber-700">
            Reference: {reference}
          </p>
        )}

        <div className="mt-8 grid gap-3 sm:grid-cols-2">
          <Link
            href="/upgrade"
            className="inline-flex items-center justify-center rounded-xl bg-[#1f4e79] px-5 py-3 text-sm font-bold text-white transition hover:bg-[#183d60]"
          >
            {wasCharged ? "Back to Plans" : "Try Again"}
          </Link>

          <Link
            href="/dashboard"
            className="inline-flex items-center justify-center rounded-xl border border-slate-300 bg-white px-5 py-3 text-sm font-bold text-slate-700 transition hover:border-[#1f4e79] hover:text-[#1f4e79]"
          >
            Back to Dashboard
          </Link>
        </div>
      </section>
    </main>
  )
}

export default function PaymentFailedPage() {
  return (
    <Suspense fallback={null}>
      <PaymentFailedContent />
    </Suspense>
  )
}
