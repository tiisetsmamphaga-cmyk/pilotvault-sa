"use client"

import { useEffect, useRef, useState } from "react"
import { createPortal } from "react-dom"
import { Maximize2, X } from "lucide-react"

type ImageViewerProps = {
  src: string
  alt: string
  onClose: () => void
}

// Full-screen view of an explanation diagram. Tap the picture to switch between
// fitting the screen and its full size (scroll to move around); pinch zoom also works.
export function ImageViewer({ src, alt, onClose }: ImageViewerProps) {
  const dialogRef = useRef<HTMLDivElement>(null)
  const onCloseRef = useRef(onClose)
  const [fullSize, setFullSize] = useState(false)

  useEffect(() => {
    onCloseRef.current = onClose
  }, [onClose])

  useEffect(() => {
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") onCloseRef.current()
    }
    const previousOverflow = document.body.style.overflow

    window.addEventListener("keydown", onKeyDown)
    document.body.style.overflow = "hidden"
    dialogRef.current?.focus()

    return () => {
      window.removeEventListener("keydown", onKeyDown)
      document.body.style.overflow = previousOverflow
    }
  }, [])

  return createPortal(
    <div
      ref={dialogRef}
      role="dialog"
      aria-modal="true"
      aria-label={alt}
      tabIndex={-1}
      className="fixed inset-0 z-[100] bg-slate-950/95 outline-none"
      onClick={onClose}
    >
      <div
        className={`flex h-full w-full overflow-auto ${fullSize ? "items-start justify-start" : "items-center justify-center p-3 sm:p-8"}`}
      >
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img
          src={src}
          alt={alt}
          onClick={(event) => {
            event.stopPropagation()
            setFullSize((value) => !value)
          }}
          className={
            fullSize
              ? "block h-auto w-auto max-w-none cursor-zoom-out bg-white"
              : "block h-auto max-h-full w-auto max-w-full cursor-zoom-in rounded-lg bg-white object-contain"
          }
        />
      </div>
      <button
        type="button"
        aria-label="Close"
        onClick={onClose}
        className="fixed right-3 top-3 flex h-11 w-11 items-center justify-center rounded-full bg-white/95 text-slate-900 shadow-lg hover:bg-white focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#f4b400]"
      >
        <X className="h-5 w-5" aria-hidden="true" />
      </button>
    </div>,
    document.body
  )
}

type EnlargeButtonProps = {
  onClick: () => void
}

// Small corner button over a diagram that opens the full-screen viewer.
export function EnlargeButton({ onClick }: EnlargeButtonProps) {
  return (
    <button
      type="button"
      aria-label="Enlarge diagram"
      onClick={onClick}
      className="absolute bottom-2 right-2 z-10 flex h-9 w-9 items-center justify-center rounded-full bg-white/90 text-slate-700 shadow ring-1 ring-slate-200 hover:bg-white focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#f4b400]"
    >
      <Maximize2 className="h-4 w-4" aria-hidden="true" />
    </button>
  )
}
