import Link from "next/link"
import { XCircle } from "lucide-react"

export default function PaymentFailedPage() {
  return (
    <main className="flex min-h-screen items-center justify-center bg-[#f8fafc] px-4 py-10 text-slate-900 sm:px-6">
      <section className="w-full max-w-xl rounded-3xl border border-red-200 bg-white p-6 text-center shadow-xl sm:p-10">
        <span className="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl bg-red-50">
          <XCircle className="h-9 w-9 text-red-600" />
        </span>

        <p className="mt-6 text-xs font-semibold uppercase tracking-[0.28em] text-red-600">
          Payment not completed
        </p>

        <h1 className="mt-3 text-3xl font-bold tracking-tight text-slate-900 sm:text-4xl">
          Your account was not charged or unlocked.
        </h1>

        <p className="mt-4 text-sm leading-7 text-slate-600 sm:text-base">
          The transaction could not be verified. You can safely return to the
          upgrade page and try again.
        </p>

        <div className="mt-8 grid gap-3 sm:grid-cols-2">
          <Link
            href="/upgrade"
            className="inline-flex items-center justify-center rounded-xl bg-[#1f4e79] px-5 py-3 text-sm font-bold text-white transition hover:bg-[#183d60]"
          >
            Try Again
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
