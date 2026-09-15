"use client"

import { useEffect, useMemo, useRef, useState } from "react"

import { BankAngleLoadFactorVisual } from "./bank-angle-load-factor-visual"

type ExplanationImageProps = {
  src: string
  alt: string
  title?: string
  caption?: string
  template?: string
  priority?: boolean
}

type PofVisualTemplate = {
  kicker?: string
  headline: string
  subline?: string
  blocks?: { label: string; value: string }[]
  formula?: string
}

function parsePofTemplate(template: string | undefined): PofVisualTemplate | null {
  if (!template) return null
  try {
    const parsed = JSON.parse(template)
    if (parsed && typeof parsed.headline === "string") return parsed as PofVisualTemplate
    return null
  } catch {
    return null
  }
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
  title,
  caption,
  template,
  priority = false,
}: ExplanationImageProps) {
  const usesBankAngleVisual =
    src.includes("/explanation-images/human-performance/load-factor-bank-")

  const isPofVisual = src.includes("/explanation-images/principles-of-flight/")
  const isApprovedPofRaster =
    /\/explanation-images\/principles-of-flight\/refined-batch-(?:1|2|3|4|5|6|7|8|9|10|11|12|13|14|16|17|18|19|20|21|22|23)\//.test(src) &&
    /\.(png|jpe?g|webp)(?:\?|$)/i.test(src)

  const isHpVisual = src.includes("/explanation-images/human-performance/refined-batch-")
  const isApprovedHpRaster =
    /\/explanation-images\/human-performance\/refined-batch-(?:1|2|3|4)\//.test(src) &&
    /\.(png|jpe?g|webp)(?:\?|$)/i.test(src)

  // POF and HP are fail-closed. Only individually QA-approved refined raster
  // batches may render. Legacy, bulk-generated, unmanifested and vector assets
  // stay blocked even when they exist on an old branch or deployment.
  if (isPofVisual && !isApprovedPofRaster) return null
  if (isHpVisual && !isApprovedHpRaster) return null
  if (usesBankAngleVisual) return <BankAngleLoadFactorVisual />

  const cardTemplate = isPofVisual || isHpVisual ? parsePofTemplate(template) : null
  if (cardTemplate) {
    return (
      <PofExplanationImage
        src={src}
        alt={alt}
        title={title}
        template={cardTemplate}
        priority={priority}
      />
    )
  }

  return <StandardExplanationImage src={src} alt={alt} priority={priority} />
}

function PofExplanationImage({
  src,
  alt,
  title,
  template,
  priority,
}: {
  src: string
  alt: string
  title?: string
  template: PofVisualTemplate
  priority: boolean
}) {
  const [status, setStatus] = useState<"loading" | "loaded" | "error">("loading")

  return (
    <figure className="mt-5 overflow-hidden rounded-2xl border border-slate-200 bg-white">
      <div className="flex items-center justify-center px-4 py-5 sm:px-6 sm:py-6" style={{ backgroundColor: "#06111f" }}>
        <img src="/images/pilotvault-banner-logo.png" alt="PilotVault SA" className="h-14 w-auto sm:h-16" />
      </div>
      <div className="h-1 bg-[#c9942f]" />

      <div className="grid gap-4 bg-[#f6f8fa] p-4 sm:p-6 lg:grid-cols-[1.4fr_1fr]">
        <div className="flex flex-col gap-3">
          {title && (
            <div className="text-lg font-extrabold uppercase tracking-[0.02em] text-[#0b1f33] sm:text-xl">
              {title}
            </div>
          )}
          <div className="relative flex min-h-40 items-center justify-center overflow-hidden rounded-xl border border-[#e2e7ed] bg-white p-3">
            {status === "loading" && (
              <div className="absolute inset-0 z-10 flex items-center justify-center px-4 text-center text-sm font-medium text-slate-500" aria-live="polite">
                <span className="animate-pulse">Loading explanation diagram…</span>
              </div>
            )}
            <img
              src={src}
              alt={alt}
              loading={priority ? "eager" : "lazy"}
              decoding="async"
              fetchPriority={priority ? "high" : "auto"}
              onLoad={() => setStatus("loaded")}
              onError={() => setStatus("error")}
              className={`block h-auto max-h-[28rem] w-auto max-w-full object-contain transition-opacity duration-150 ${status === "loaded" ? "opacity-100" : "opacity-0"}`}
            />
            {status === "error" && (
              <div className="absolute inset-0 z-10 flex flex-col items-center justify-center gap-2 px-4 text-center text-sm font-medium text-slate-700" role="alert">
                The explanation diagram could not be loaded.
              </div>
            )}
          </div>
        </div>

        <div className="flex flex-col rounded-xl border border-[#e2e7ed] bg-white p-5">
          <div className="text-xs font-extrabold uppercase tracking-[0.14em] text-[#c9942f]">
            {template.kicker ?? "KEY RELATIONSHIP"}
          </div>
          <div className="mt-2 text-2xl font-extrabold text-[#0b1f33]">{template.headline}</div>
          {template.subline && (
            <div className="mt-1 text-base font-bold leading-snug text-[#c9942f]">{template.subline}</div>
          )}

          {template.blocks && template.blocks.length > 0 && (
            <div className="mt-4 border-t border-[#e2e7ed] pt-4">
              <dl className="flex flex-col gap-3">
                {template.blocks.map((block) => (
                  <div key={block.label}>
                    <dt className="text-xs font-bold uppercase tracking-[0.08em] text-[#5b6b7a]">{block.label}</dt>
                    <dd className="mt-0.5 text-base font-bold text-[#0b1f33]">{block.value}</dd>
                  </div>
                ))}
              </dl>
            </div>
          )}
        </div>
      </div>

      {template.formula && (
        <div className="mx-4 mb-4 rounded-xl bg-[#0b1f33] px-4 py-3 text-center text-base font-extrabold text-white sm:mx-6 sm:mb-6">
          {template.formula}
        </div>
      )}
    </figure>
  )
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
        <div className="px-4 py-3 text-center sm:px-6 sm:py-4" style={{ backgroundColor: "#06111f" }}>
          <div className="text-[11px] font-extrabold tracking-[0.22em] sm:text-xs" style={{ color: "#f4b400" }}>PILOTVAULT NAVIGATION</div>
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
