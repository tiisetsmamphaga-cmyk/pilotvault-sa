"use client"

import { useEffect } from "react"
import Link from "next/link"
import { TriangleAlert } from "lucide-react"

export default function GlobalError({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  useEffect(() => {
    console.error(error)
  }, [error])

  return (
    <main className="relative flex min-h-screen items-center justify-center overflow-hidden bg-[#f8fafc] px-4 py-10 text-slate-900">
      <div className="pointer-events-none absolute -left-28 top-1/3 h-80 w-80 rounded-full bg-[#d6e6f7]/60 blur-3xl" />
      <div className="pointer-events-none absolute -right-24 bottom-0 h-96 w-96 rounded-full bg-slate-200/55 blur-3xl" />

      <section className="relative w-full max-w-md overflow-hidden rounded-[28px] border border-slate-200 bg-white p-7 text-center shadow-xl sm:p-9">
        <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl border border-[#1f4e79]/20 bg-[#d6e6f7] text-[#1f4e79]">
          <TriangleAlert className="h-8 w-8" />
        </div>

        <p className="mt-6 text-[10px] font-bold uppercase tracking-[0.3em] text-[#1f4e79]">
          Something went wrong
        </p>
        <h1 className="mt-3 text-2xl font-bold text-slate-900">
          We hit some turbulence.
        </h1>
        <p className="mt-3 text-sm leading-6 text-slate-600">
          An unexpected error occurred. You can try again, or head back home.
        </p>

        <div className="mt-6 space-y-3">
          <button
            onClick={reset}
            className="block w-full rounded-xl bg-[#1f4e79] px-5 py-3 text-sm font-bold text-white transition hover:bg-[#183d60]"
          >
            Try again
          </button>
          <Link
            href="/"
            className="block text-sm font-semibold text-[#1f4e79] transition hover:text-[#183d60]"
          >
            Return home
          </Link>
          <a
            href="mailto:contact@pilotvault.co.za?subject=PilotVault%20error%20report"
            className="block text-sm font-semibold text-[#1f4e79] transition hover:text-[#183d60]"
          >
            Contact support
          </a>
        </div>
      </section>
    </main>
  )
}
