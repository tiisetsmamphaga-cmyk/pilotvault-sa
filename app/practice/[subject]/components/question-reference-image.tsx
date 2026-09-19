"use client"

import { useState } from "react"

type QuestionReferenceImageProps = {
  src: string
  alt?: string
}

const isMetVisual = (src: string) =>
  src.includes("/explanation-images/meteorology/refined-batch-")

const isApprovedMetRaster = (src: string) =>
  /\/explanation-images\/meteorology\/refined-batch-(?:1)\//.test(src) &&
  /\.(png|jpe?g|webp)(?:\?|$)/i.test(src)

// Station-model crops are small standalone symbols, not a full-width report
// page, so they skip the grey report-card chrome and stay compact.
const isStationVisual = (src: string) =>
  /\/explanation-images\/meteorology\/refined-batch-\d+\/station-\d+-/.test(src)

export function QuestionReferenceImage({
  src,
  alt = "Question reference",
}: QuestionReferenceImageProps) {
  const [status, setStatus] = useState<"loading" | "loaded" | "error">(
    "loading"
  )
  const [attempt, setAttempt] = useState(0)

  // Fail-closed for the meteorology extraction pipeline: only individually
  // QA-approved refined-batch crops may render. Anything else under that
  // path (unmanifested, superseded) stays blocked even if it exists.
  if (isMetVisual(src) && !isApprovedMetRaster(src)) return null

  const bare = isStationVisual(src)

  return (
    <figure
      className={
        bare
          ? "mx-auto mt-6 w-fit max-w-full"
          : "mx-auto mt-6 w-full max-w-2xl border border-slate-300 bg-slate-50 p-2"
      }
    >
      {status === "loading" && (
        <div
          className="flex min-h-36 items-center justify-center px-4 text-center text-sm font-medium text-slate-600"
          aria-live="polite"
        >
          Loading reference chart…
        </div>
      )}

      <img
        key={`${src}-${attempt}`}
        src={src}
        alt={alt}
        loading="eager"
        decoding="async"
        fetchPriority="high"
        onLoad={() => setStatus("loaded")}
        onError={() => setStatus("error")}
        className={
          status === "loaded"
            ? bare
              ? "block max-w-[280px]"
              : "block"
            : "hidden"
        }
      />

      {status === "error" && (
        <div
          className="flex min-h-36 flex-col items-center justify-center gap-3 px-4 text-center"
          role="alert"
        >
          <p className="text-sm font-medium text-red-700">
            The reference chart could not be loaded.
          </p>
          <button
            type="button"
            onClick={() => {
              setStatus("loading")
              setAttempt((currentAttempt) => currentAttempt + 1)
            }}
            className="border border-[#1f4e79] bg-white px-4 py-2 text-sm font-semibold text-[#1f4e79] hover:bg-blue-50"
          >
            Retry chart
          </button>
        </div>
      )}
    </figure>
  )
}
