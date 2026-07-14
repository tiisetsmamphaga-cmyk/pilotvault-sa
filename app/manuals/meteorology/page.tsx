import { Download, FileText } from "lucide-react"

export default function MeteorologyManualPage() {
  return (
    <main className="min-h-screen bg-[#06111f] px-4 py-10 text-white sm:px-6">
      <section className="mx-auto max-w-3xl rounded-3xl border border-[#1e3a5f] bg-[#081726] p-6 shadow-2xl sm:p-8">
        <div className="inline-flex rounded-2xl border border-[#f4b400]/30 bg-[#f4b400]/10 p-3 text-[#f4b400]">
          <FileText size={28} />
        </div>

        <p className="mt-6 text-xs font-semibold uppercase tracking-[0.25em] text-[#f4b400]">
          Exam Reference Manual
        </p>

        <h1 className="mt-3 text-3xl font-bold sm:text-4xl">
          PPL Meteorology Manual
        </h1>

        <p className="mt-4 leading-7 text-gray-400">
          Download the SACAA examination reference manual before attempting
          Meteorology questions involving synoptic symbols, station models,
          METARs, TAFs, significant-weather charts and upper winds.
        </p>

        <a
          href="/manuals/ppl-meteorology-manual.pdf"
          download="PilotVault-PPL-Meteorology-Manual.pdf"
          className="mt-8 inline-flex w-full items-center justify-center gap-2 rounded-xl bg-[#f4b400] px-5 py-3 text-sm font-bold text-[#06111f] transition hover:bg-[#ffd24d] sm:w-auto"
        >
          <Download size={18} />
          Download Meteorology Manual
        </a>
      </section>
    </main>
  )
}
