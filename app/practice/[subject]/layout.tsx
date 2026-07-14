import type { ReactNode } from "react"
import Link from "next/link"
import { Download, FileText } from "lucide-react"

export default async function SubjectPracticeLayout({
  children,
  params,
}: Readonly<{
  children: ReactNode
  params: Promise<{ subject: string }>
}>) {
  const { subject } = await params
  const isMeteorology = subject === "meteorology"

  return (
    <>
      {isMeteorology && (
        <div className="bg-[#06111f] px-4 pt-5 text-white sm:px-6">
          <div className="mx-auto flex max-w-5xl items-center justify-between gap-4 rounded-xl border border-[#1e3a5f] bg-[#081726]/70 px-4 py-3">
            <div className="flex min-w-0 items-center gap-3">
              <FileText size={18} className="shrink-0 text-[#f4b400]" />

              <div className="min-w-0">
                <p className="text-sm font-semibold text-white">
                  PPL Meteorology Manual
                </p>
                <p className="truncate text-xs text-gray-500">
                  Reference for symbols, METARs, TAFs and weather charts.
                </p>
              </div>
            </div>

            <Link
              href="/manuals/meteorology"
              className="inline-flex shrink-0 items-center gap-2 rounded-lg border border-[#1e3a5f] px-3 py-2 text-xs font-semibold text-[#f4b400] transition hover:border-[#f4b400]/60 hover:bg-[#f4b400]/5"
            >
              <Download size={15} />
              Download
            </Link>
          </div>
        </div>
      )}

      {children}
    </>
  )
}
