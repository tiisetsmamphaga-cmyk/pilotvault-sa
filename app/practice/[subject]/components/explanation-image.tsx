"use client"

import { useEffect, useMemo, useState } from "react"

import { BankAngleLoadFactorVisual } from "./bank-angle-load-factor-visual"

type ExplanationImageProps = {
  src: string
  alt: string
  title?: string
  caption?: string
  priority?: boolean
}

const POF_IMAGE_ROOT = "/explanation-images/principles-of-flight/"
const APPROVED_POF_BATCH_DIRECTORIES = [
  `${POF_IMAGE_ROOT}refined-batch-1/`,
  `${POF_IMAGE_ROOT}refined-batch-2/`,
  `${POF_IMAGE_ROOT}refined-batch-3/`,
  `${POF_IMAGE_ROOT}refined-batch-4/`,
] as const

const NEW_POF_WEBSITE_TEMPLATE_DIRECTORIES = [
  `${POF_IMAGE_ROOT}refined-batch-2/`,
  `${POF_IMAGE_ROOT}refined-batch-3/`,
  `${POF_IMAGE_ROOT}refined-batch-4/`,
] as const

function formatDiagramTitle(src: string, alt: string, explicitTitle?: string) {
  const requestedTitle = explicitTitle?.trim()
  if (requestedTitle) return requestedTitle.toUpperCase()

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

  return (fileName || fallback || "DIAGRAM").toUpperCase()
}

function matchesApprovedPofDirectory(src: string) {
  return APPROVED_POF_BATCH_DIRECTORIES.some((directory) => src.includes(directory))
}

function usesNewPofWebsiteTemplate(src: string) {
  return NEW_POF_WEBSITE_TEMPLATE_DIRECTORIES.some((directory) => src.includes(directory))
}

export function ExplanationImage({
  src,
  alt,
  title,
  caption,
  priority = false,
}: ExplanationImageProps) {
  const usesBankAngleVisual =
    src.includes("/explanation-images/human-performance/load-factor-bank-")

  const isPofVisual = src.includes(POF_IMAGE_ROOT)
  const isApprovedPofRaster =
    matchesApprovedPofDirectory(src) &&
    /\.(png|jpe?g|webp)(?:\?|$)/i.test(src)

  // POF remains fail-closed. Each newly approved batch must be added to the
  // explicit allow-list above after source, visual and QA approval. There is
  // intentionally no wildcard for future refined-batch-* directories.
  if (isPofVisual && !isApprovedPofRaster) return null
  if (usesBankAngleVisual) return <BankAngleLoadFactorVisual />

  return (
    <StandardExplanationImage
      src={src}
      alt={alt}
      title={title}
      caption={caption}
      priority={priority}
    />
  )
}

function StandardExplanationImage({
  src,
  alt,
  title,
  caption,
  priority = false,
}: ExplanationImageProps) {
  const [status, setStatus] = useState<"loading" | "loaded" | "error">("loading")
  const [attempt, setAttempt] = useState(0)
  const usesNavigationTemplate = src.includes("/explanation-images/navigation/")
  const usesPofTemplate = usesNewPofWebsiteTemplate(src)
  const usesWebsiteTemplate = usesNavigationTemplate || usesPofTemplate
  const diagramTitle = useMemo(
    () => formatDiagramTitle(src, alt, title),
    [src, alt, title],
  )

  useEffect(() => {
    setStatus("loading")
    setAttempt(0)
  }, [src])

  useEffect(() => {
    if (status !== "loading") return
    const timeout = window.setTimeout(() => setStatus("error"), 10000)
    return () => window.clearTimeout(timeout)
  }, [status, attempt, src])

  const resolvedSrc = useMemo(() => {
    if (attempt === 0) return src
    const separator = src.includes("?") ? "&" : "?"
    return `${src}${separator}pv_retry=${attempt}`
  }, [attempt, src])

  return (
    <figure
      className={
        usesWebsiteTemplate
          ? "mt-5 overflow-hidden rounded-2xl border border-slate-200 bg-white"
          : "mx-auto mt-5 w-fit max-w-full overflow-hidden border border-slate-200 bg-white"
      }
    >
      {status === "loading" && (
        <div
          className="flex min-h-40 min-w-64 items-center justify-center px-4 text-center text-sm font-medium text-slate-500"
          aria-live="polite"
        >
          <span className="animate-pulse">Loading explanation diagram…</span>
        </div>
      )}

      {status === "loaded" && usesWebsiteTemplate && (
        <div className="bg-[#06111f] px-4 py-3 text-center sm:px-6 sm:py-4">
          <div className="text-[11px] font-extrabold tracking-[0.22em] text-[#f4b400] sm:text-xs">
            {usesPofTemplate ? "PILOTVAULT PRINCIPLES OF FLIGHT" : "PILOTVAULT NAVIGATION"}
          </div>
          <div className="mt-1 text-lg font-extrabold uppercase tracking-[0.035em] text-white sm:text-2xl">
            {diagramTitle}
          </div>
        </div>
      )}

      <div
        className={
          usesWebsiteTemplate
            ? "overflow-hidden"
            : "flex max-w-full items-center justify-center overflow-hidden"
        }
      >
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
              ? usesWebsiteTemplate
                ? "block max-h-[32rem] w-full object-contain"
                : "block h-auto max-h-[32rem] w-auto max-w-full object-contain"
              : "hidden"
          }
        />
      </div>

      {status === "loaded" && caption?.trim() && (
        <figcaption className="px-4 pb-4 pt-2 text-center text-sm leading-6 text-slate-500 sm:px-6">
          {caption}
        </figcaption>
      )}

      {status === "error" && (
        <div
          className="flex min-h-40 min-w-64 flex-col items-center justify-center gap-3 px-4 text-center"
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
