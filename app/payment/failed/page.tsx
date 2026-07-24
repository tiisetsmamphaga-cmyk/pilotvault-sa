import Link from "next/link"
import { XCircle } from "lucide-react"

export default function PaymentFailedPage() {
  return (
    <main className="flex min-h-screen items-center justify-center bg-[#06111f] px-4 py-10 text-white sm:px-6">
      <section className="w-full max-w-xl rounded-3xl border border-red-500/30 bg-[#081726] p-6 text-center shadow-2xl sm:p-10">
        <span className="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl bg-red-500/10">
          <XCircle className="h-9 w-9 text-red-300" />
        </span>

        <p className="mt-6 text-xs font-semibold uppercase tracking-[0.28em] text-red-300">
          Payment not completed
        </p>

        <h1 className="mt-3 text-3xl font-bold sm:text-4xl">
          Your account was not charged or unlocked.
        </h1>

        <p className="mt-4 text-sm leading-7 text-gray-400 sm:text-base">
          The transaction could not be verified. You can safely return to the
          upgrade page and try again.
        </p>

        <div className="mt-8 grid gap-3 sm:grid-cols-2">
          <Link
            href="/upgrade"
            className="inline-flex items-center justify-center rounded-xl bg-[#f4b400] px-5 py-3 text-sm font-bold text-[#06111f] transition hover:bg-[#d9a000]"
          >
            Try Again
          </Link>

          <Link
            href="/dashboard"
            className="inline-flex items-center justify-center rounded-xl border border-[#1e3a5f] px-5 py-3 text-sm font-bold text-gray-200 transition hover:border-[#f4b400] hover:text-[#f4b400]"
          >
            Back to Dashboard
          </Link>
        </div>
      </section>
    </main>
  )
}
