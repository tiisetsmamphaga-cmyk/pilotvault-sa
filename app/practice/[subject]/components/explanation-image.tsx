"use client"

import { useEffect, useMemo, useRef, useState } from "react"

import { BankAngleLoadFactorVisual } from "./bank-angle-load-factor-visual"

type ExplanationImageProps = {
  src: string
  alt: string
  title?: string
  caption?: string
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

  const isPofVisual = src.includes("/explanation-images/principles-of-flight/")
  const isApprovedPofRaster =
    /\/explanation-images\/principles-of-flight\/refined-batch-(?:1|2|3|4|5|6|7|8|9|10|11|12)\//.test(src) &&
    /\.(png|jpe?g|webp)(?:\?|$)/i.test(src)

  // POF is fail-closed. Only individually QA-approved refined raster batches
  // may render. Legacy, bulk-generated, unmanifested and vector POF assets stay
  // blocked even when they exist on an old branch or deployment.
  if (isPofVisual && !isApprovedPofRaster) return null
  if (usesBankAngleVisual) return <BankAngleLoadFactorVisual />
  return <StandardExplanationImage src={src} alt={alt} priority={priority} />
}

function StandardExplanationImage({ src, alt, priority = false }: ExplanationImageProps) {
  const [status, setStatus] = useState<"loading" | "loaded" | "error">("loading")
  const [attempt, setAttempt] = useState(0)
  const imageRef = useRef<HTMLImageElement>(null)
  const usesNavigationTemplate = src.includes("/explanation-images/navigation/")
  const usesWebsiteTemplate = usesNavigationTemplate
  const diagramTitle = useMemo(() => formatDiagramTitle(src, alt), [src, alt])

  const resolvedSrc = useMemo(() => {
    if (attempt === 0) return src
    const separator = src.includes("?") ? "&" : "?"
    return `${src}${separator}pv_retry=${attempt}`
  }, [attempt, src])

  useEffect(() => {
    setStatus("loading")
    setAttempt(0)
  }, [src])

  // An eager image can finish downloading from the server-rendered markup before
  // React hydrates and attaches onLoad. Reconcile the native image state after
  // hydration so an already-decoded image never stays stuck on "Loading…".
  useEffect(() => {
    const image = imageRef.current
    if (!image || !image.complete) return
    setStatus(image.naturalWidth > 0 ? "loaded" : "error")
  }, [resolvedSrc])

  const imageClass = usesWebsiteTemplate
    ? "block max-h-[32rem] w-full object-contain transition-opacity duration-150"
    : "block h-auto max-h-[32rem] w-auto max-w-full object-contain transition-opacity duration-150"

  return (
    <figure
      className={
        usesWebsiteTemplate
          ? "mt-5 overflow-hidden rounded-2xl border border-slate-200 bg-white"
          : "mx-auto mt-5 w-fit max-w-full overflow-hidden border border-slate-200 bg-white"
      }
    >
      {status === "loaded" && usesNavigationTemplate && (
        <div className="bg-[#06111f] px-4 py-3 text-center sm:px-6 sm:py-4">
          <div className="text-[11px] font-extrabold tracking-[0.22em] text-[#f4b400] sm:text-xs">PILOTVAULT NAVIGATION</div>
          <div className="mt-1 text-lg font-extrabold uppercase tracking-[0.035em] text-white sm:text-2xl">{diagramTitle}</div>
        </div>
      )}

      <div
        className={
          usesWebsiteTemplate
            ? "relative min-h-40 min-w-64 overflow-hidden"
            : "relative flex min-h-40 min-w-64 max-w-full items-center justify-center overflow-hidden"
        }
      >
        {status === "loading" && (
          <div className="absolute inset-0 z-10 flex items-center justify-center px-4 text-center text-sm font-medium text-slate-500" aria-live="polite">
            <span className="animate-pulse">Loading explanation diagram…</span>
          </div>
        )}

        <img
          ref={imageRef}
          key={`${src}-${attempt}`}
          src={resolvedSrc}
          alt={alt}
          loading={priority ? "eager" : "lazy"}
          decoding="async"
          fetchPriority={priority ? "high" : "auto"}
          onLoad={() => setStatus("loaded")}
          onError={() => setStatus("error")}
          style={status === "loaded" && usesNavigationTemplate ? { marginTop: "-6%" } : undefined}
          className={`${imageClass} ${status === "loaded" ? "opacity-100" : "opacity-0"}`}
        />

        {status === "error" && (
          <div className="absolute inset-0 z-10 flex min-h-40 min-w-64 flex-col items-center justify-center gap-3 px-4 text-center" role="alert">
            <p className="text-sm font-medium text-slate-700">The explanation diagram could not be loaded.</p>
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
      </div>
    </figure>
  )
}
