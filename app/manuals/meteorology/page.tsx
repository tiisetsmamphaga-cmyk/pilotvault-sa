import Link from "next/link"
import { ArrowLeft, Download, FileText } from "lucide-react"

export default function MeteorologyManualPage() {
  return (
    <main className="min-h-screen bg-[#f8fafc] px-4 py-10 text-slate-900 sm:px-6">
      <section className="mx-auto max-w-3xl">
        <Link
          href="/practice/meteorology"
          className="inline-flex items-center gap-2 text-sm font-semibold text-[#1f4e79] transition hover:text-[#183d60]"
        >
          <ArrowLeft size={16} />
          Back to Meteorology
        </Link>

        <div className="mt-8 rounded-3xl border border-slate-200 bg-white p-6 shadow-sm sm:p-8">
          <div className="inline-flex rounded-2xl border border-[#1f4e79]/20 bg-[#d6e6f7] p-3 text-[#1f4e79]">
            <FileText size={28} />
          </div>

          <p className="mt-6 text-xs font-semibold uppercase tracking-[0.25em] text-[#1f4e79]">
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
