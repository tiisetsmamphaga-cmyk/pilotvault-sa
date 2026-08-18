"use client"

import { useEffect, useMemo, useState } from "react"

type ExplanationImageProps = {
  src: string
  alt: string
  priority?: boolean
}

export function ExplanationImage({
  src,
  alt,
  priority = false,
}: ExplanationImageProps) {
  const [status, setStatus] = useState<"loading" | "loaded" | "error">(
    "loading"
  )
  const [attempt, setAttempt] = useState(0)

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

      <img
        key={`${src}-${attempt}`}
        src={resolvedSrc}
        alt={alt}
        loading={priority ? "eager" : "lazy"}
        decoding="async"
        fetchPriority={priority ? "high" : "auto"}
        onLoad={() => setStatus("loaded")}
        onError={() => setStatus("error")}
        className={
          status === "loaded"
            ? "block max-h-[32rem] w-full object-contain"
            : "hidden"
        }
      />

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
