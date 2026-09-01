import Image from "next/image"
import Link from "next/link"
import { ArrowLeft, Download, FileText } from "lucide-react"

export default function MeteorologyManualPage() {
  return (
    <main className="min-h-screen bg-[#eef3f8] text-slate-900">
      <header className="border-b border-white/15 bg-[#1f4e79] text-white">
        <div className="mx-auto flex h-16 max-w-7xl items-center justify-between gap-3 px-4 sm:h-[72px] sm:px-6 lg:px-8">
          <div className="flex min-w-0 items-center gap-3">
            <Link href="/dashboard" className="shrink-0" aria-label="PilotVault dashboard">
              <Image
                src="/images/Header logo.png"
                alt="PilotVault SA"
                width={180}
                height={54}
                className="h-auto w-[132px] object-contain sm:w-[154px]"
                priority
              />
            </Link>
            <span className="hidden h-7 w-px bg-white/20 sm:block" />
            <span className="hidden truncate text-sm font-medium text-blue-50/90 sm:block">
              Meteorology Manual
            </span>
          </div>

          <Link
            href="/practice/meteorology"
            aria-label="Back to Meteorology"
            className="inline-flex h-10 items-center justify-center gap-2 rounded-lg border border-white/20 bg-white/5 px-3 text-sm font-medium text-white transition hover:bg-white/10"
          >
            <ArrowLeft size={16} />
            <span className="hidden sm:inline">Meteorology</span>
          </Link>
        </div>
      </header>

      <section className="mx-auto max-w-3xl px-4 py-8 sm:px-6 sm:py-10">
        <div className="rounded-2xl border border-[#d2dde7] bg-[#f8fafc] p-6 shadow-sm sm:p-8">
          <div className="inline-flex rounded-xl border border-[#1f4e79]/20 bg-[#d6e6f7] p-3 text-[#1f4e79]">
            <FileText size={28} />
          </div>

          <p className="mt-6 text-xs font-semibold uppercase tracking-[0.22em] text-[#1f4e79]">
            Exam Reference Manual
          </p>

          <h1 className="mt-3 text-3xl font-bold tracking-tight text-slate-900 sm:text-4xl">
            PPL Meteorology Manual
          </h1>

          <p className="mt-4 leading-7 text-slate-600">
            Download the SACAA examination reference manual before attempting
            Meteorology questions involving synoptic symbols, station models,
            METARs, TAFs, significant-weather charts and upper winds.
          </p>

          <a
            href="/PPL-MET.pdf"
            download="PilotVault-PPL-Meteorology-Manual.pdf"
            className="mt-8 inline-flex w-full items-center justify-center gap-2 rounded-xl bg-[#1f4e79] px-5 py-3 text-sm font-bold text-white transition hover:bg-[#183d60] sm:w-auto"
          >
            <Download size={18} />
            Download Meteorology Manual
          </a>
        </div>
      </section>
    </main>
  )
}
