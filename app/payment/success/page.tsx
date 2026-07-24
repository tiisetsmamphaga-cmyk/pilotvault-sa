import Link from "next/link"
import { CheckCircle2 } from "lucide-react"

export default function PaymentSuccessPage() {
  return (
    <main className="flex min-h-screen items-center justify-center bg-[#06111f] px-4 py-10 text-white sm:px-6">
      <section className="w-full max-w-xl rounded-3xl border border-[#f4b400]/40 bg-[#081726] p-6 text-center shadow-2xl sm:p-10">
        <span className="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl bg-[#f4b400]/15">
          <CheckCircle2 className="h-9 w-9 text-[#f4b400]" />
        </span>

        <p className="mt-6 text-xs font-semibold uppercase tracking-[0.28em] text-[#f4b400]">
          Payment successful
        </p>

        <h1 className="mt-3 text-3xl font-bold sm:text-4xl">
          Your PilotVault access is active.
        </h1>

        <p className="mt-4 text-sm leading-7 text-gray-400 sm:text-base">
          Your payment was verified and your account has been updated. You can
          continue straight to your dashboard.
        </p>

        <Link
          href="/dashboard"
          className="mt-8 inline-flex w-full items-center justify-center rounded-xl bg-[#f4b400] px-5 py-3 text-sm font-bold text-[#06111f] transition hover:bg-[#d9a000]"
        >
          Go to Dashboard
        </Link>
      </section>
    </main>
  )
}
