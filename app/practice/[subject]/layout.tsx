import Link from "next/link"
import { Download, FileText } from "lucide-react"

export default async function SubjectPracticeLayout({
  children,
  params,
}: Readonly<{
  children: React.ReactNode
  params: Promise<{ subject: string }>
}>) {
  const { subject } = await params
  const isMeteorology = subject === "meteorology"

  return (
    <>
      {isMeteorology && (
        <div className="bg-[#06111f] px-4 pt-6 text-white sm:px-6">
          <div className="mx-auto flex max-w-5xl flex-col gap-4 rounded-2xl border border-[#f4b400]/30 bg-gradient-to-r from-[#081726] to-[#0b1d31] p-5 shadow-2xl sm:flex-row sm:items-center sm:justify-between">
            <div className="flex items-start gap-4">
              <div className="rounded-xl border border-[#f4b400]/30 bg-[#f4b400]/10 p-3 text-[#f4b400]">
                <FileText size={24} />
              </div>

              <div>
                <p className="text-xs font-bold uppercase tracking-[0.2em] text-[#f4b400]">
                  Exam Reference Manual
                </p>
                <h2 className="mt-1 text-lg font-bold text-white">
                  PPL Meteorology Manual
                </h2>
                <p className="mt-1 max-w-2xl text-sm leading-6 text-gray-400">
                  Some Meteorology questions use the official synoptic symbols,
                  station models, TAFs, METARs and weather charts in this manual.
                </p>
              </div>
            </div>

            <Link
              href="/manuals/meteorology"
              className="inline-flex shrink-0 items-center justify-center gap-2 rounded-xl bg-[#f4b400] px-5 py-3 text-sm font-bold text-[#06111f] transition hover:bg-[#ffd24d]"
            >
              <Download size={18} />
              Get Manual
            </Link>
          </div>
        </div>
      )}

      {children}
    </>
  )
}
