import Link from "next/link"
import { CheckCircle2 } from "lucide-react"

export default function PaymentSuccessPage() {
  return (
    <main className="flex min-h-screen items-center justify-center bg-[#f8fafc] px-4 py-10 text-slate-900 sm:px-6">
      <section className="w-full max-w-xl rounded-3xl border border-slate-200 bg-white p-6 text-center shadow-xl sm:p-10">
        <span className="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl bg-emerald-50">
          <CheckCircle2 className="h-9 w-9 text-emerald-600" />
        </span>

        <p className="mt-6 text-xs font-semibold uppercase tracking-[0.28em] text-[#1f4e79]">
          Payment successful
        </p>

        <h1 className="mt-3 text-3xl font-bold tracking-tight text-slate-900 sm:text-4xl">
          Your PilotVault access is active.
        </h1>

        <p className="mt-4 text-sm leading-7 text-slate-600 sm:text-base">
          Your payment was verified and your account has been updated. You can
          continue straight to your dashboard.
        </p>

        <Link
          href="/dashboard"
          className="mt-8 inline-flex w-full items-center justify-center rounded-xl bg-[#1f4e79] px-5 py-3 text-sm font-bold text-white transition hover:bg-[#183d60]"
        >
          Go to Dashboard
        </Link>
      </section>
    </main>
  )
}
