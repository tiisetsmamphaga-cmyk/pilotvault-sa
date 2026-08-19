"use client"

import { useEffect, useMemo, useState } from "react"

import { BankAngleLoadFactorVisual } from "./bank-angle-load-factor-visual"

type ExplanationImageProps = {
  src: string
  alt: string
  priority?: boolean
}

function formatDiagramTitle(src: string, alt: string) {
  const fileName = src
    .split("?")[0]
    .split("/")
    .pop()
    ?.replace(/\.(svg|png|jpe?g|webp)$/i, "")
    .replace(/-v\d+$/i, "")
    .replace(/[-_]+/g, " ")
    .trim()

  const fallback = alt
    .replace(/^Explanation diagram for\s+/i, "")
    .replace(/[-_]+/g, " ")
    .trim()

  return (fileName || fallback || "NAVIGATION").toUpperCase()
}

export function ExplanationImage({
  src,
  alt,
  priority = false,
}: ExplanationImageProps) {
  const usesBankAngleVisual =
    src.includes("/explanation-images/human-performance/load-factor-bank-")
  const isUnapprovedPofVisual =
    src.includes("/explanation-images/principles-of-flight/") &&
    !src.includes("/explanation-images/principles-of-flight/pdf-rebuild/")

  // Only the PDF-reference POF library is approved during staged QA. Older
  // POF explanation assets remain hidden; question-reference images are
  // rendered separately by QuestionReferenceImage and are unaffected.
  if (isUnapprovedPofVisual) {
    return null
  }

  if (usesBankAngleVisual) {
    return <BankAngleLoadFactorVisual />
  }

  return <StandardExplanationImage src={src} alt={alt} priority={priority} />
}

function StandardExplanationImage({
  src,
  alt,
  priority = false,
}: ExplanationImageProps) {
  const [status, setStatus] = useState<"loading" | "loaded" | "error">(
    "loading"
  )
  const [attempt, setAttempt] = useState(0)

  const usesNavigationTemplate = src.includes(
    "/explanation-images/navigation/"
  )
  const diagramTitle = useMemo(() => formatDiagramTitle(src, alt), [src, alt])

  useEffect(() => {
    setStatus("loading")
    setAttempt(0)
  }, [src])

  useEffect(() => {
    if (status !== "loading") {
      return
    }

    const timeout = window.setTimeout(() => {
      setStatus("error")
    }, 10000)

    return () => window.clearTimeout(timeout)
  }, [status, attempt, src])

  const resolvedSrc = useMemo(() => {
    if (attempt === 0) {
      return src
    }

    const separator = src.includes("?") ? "&" : "?"
    return `${src}${separator}pv_retry=${attempt}`
  }, [attempt, src])

  return (
    <figure className="mt-5 overflow-hidden border border-slate-200 bg-white p-2">
      {status === "loading" && (
        <div
          className="flex min-h-40 items-center justify-center px-4 text-center text-sm font-medium text-slate-500"
          aria-live="polite"
        >
          <span className="animate-pulse">Loading explanation diagram…</span>
        </div>
      )}

      {status === "loaded" && usesNavigationTemplate && (
        <div className="bg-[#06111f] px-4 py-3 text-center sm:px-6 sm:py-4">
          <div className="text-[11px] font-extrabold tracking-[0.22em] text-[#f4b400] sm:text-xs">
            PILOTVAULT NAVIGATION
          </div>
          <div className="mt-1 text-lg font-extrabold uppercase tracking-[0.035em] text-white sm:text-2xl">
            {diagramTitle}
          </div>
        </div>
      )}

      <div className={usesNavigationTemplate ? "overflow-hidden" : undefined}>
        <img
          key={`${src}-${attempt}`}
          src={resolvedSrc}
          alt={alt}
          loading={priority ? "eager" : "lazy"}
          decoding="async"
          fetchPriority={priority ? "high" : "auto"}
          onLoad={() => setStatus("loaded")}
          onError={() => setStatus("error")}
          style={
            status === "loaded" && usesNavigationTemplate
              ? { marginTop: "-6%" }
              : undefined
          }
          className={
            status === "loaded"
              ? "block max-h-[32rem] w-full object-contain"
              : "hidden"
          }
        />
      </div>

      {status === "error" && (
        <div
          className="flex min-h-40 flex-col items-center justify-center gap-3 px-4 text-center"
          role="alert"
        >
          <p className="text-sm font-medium text-slate-700">
            The explanation diagram could not be loaded.
          </p>
          <button
            type="button"
            onClick={() => {
              setStatus("loading")
              setAttempt((currentAttempt) => currentAttempt + 1)
            }}
            className="border border-[#1f4e79] bg-white px-4 py-2 text-sm font-semibold text-[#1f4e79] hover:bg-blue-50"
          >
            Retry diagram
          </button>
        </div>
      )}
    </figure>
  )
}
