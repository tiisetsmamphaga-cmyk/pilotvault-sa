"use client"

import type { ReactNode } from "react"
import { useEffect, useState } from "react"
import Link from "next/link"
import { useParams } from "next/navigation"
import { createPortal } from "react-dom"
import { BookOpen, Download } from "lucide-react"

export default function SubjectPracticeLayout({
  children,
}: Readonly<{
  children: ReactNode
}>) {
  const params = useParams<{ subject: string }>()
  const isMeteorology = params.subject === "meteorology"
  const [manualTarget, setManualTarget] = useState<HTMLElement | null>(null)

  useEffect(() => {
    if (!isMeteorology) {
      setManualTarget(null)
      return
    }

    const findTrainingModeCard = () => {
      const trainingModeHeading = Array.from(
        document.querySelectorAll<HTMLHeadingElement>("h1")
      ).find(
        (heading) => heading.textContent?.trim() === "Choose your training mode"
      )

      setManualTarget(trainingModeHeading?.parentElement ?? null)
    }

    findTrainingModeCard()

    const observer = new MutationObserver(findTrainingModeCard)

    observer.observe(document.body, {
      childList: true,
      subtree: true,
    })

    return () => {
      observer.disconnect()
    }
  }, [isMeteorology])

  return (
    <>
      {children}

      {isMeteorology &&
        manualTarget &&
        createPortal(
          <div className="mt-6 flex flex-col gap-4 rounded-2xl border border-[#1e3a5f] bg-[#06111f]/70 p-4 sm:flex-row sm:items-center sm:justify-between">
            <div className="flex min-w-0 items-start gap-3">
              <div className="rounded-xl border border-[#1e3a5f] bg-[#0b1d31] p-3 text-[#f4b400]">
                <BookOpen size={21} />
              </div>

              <div className="min-w-0">
                <p className="text-xs font-bold uppercase tracking-[0.2em] text-[#f4b400]">
                  Study Resource
                </p>
                <p className="mt-1 font-semibold text-white">
                  PPL Meteorology Manual
                </p>
                <p className="mt-1 text-sm leading-6 text-gray-400">
                  Review weather symbols, METARs, TAFs and aviation charts.
                </p>
              </div>
            </div>

            <Link
              href="/manuals/meteorology"
              className="inline-flex shrink-0 items-center justify-center gap-2 rounded-xl border border-[#f4b400]/40 bg-[#f4b400]/10 px-4 py-3 text-sm font-semibold text-[#f4b400] transition hover:border-[#f4b400] hover:bg-[#f4b400] hover:text-[#06111f]"
            >
              <Download size={17} />
              Open Manual
            </Link>
          </div>,
          manualTarget
        )}
    </>
  )
}
