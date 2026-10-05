"use client"

import { forwardRef, useEffect, useImperativeHandle, useRef } from "react"

// Cloudflare Turnstile ("I am not a robot" check) for the login and sign-up
// form. It is switched on by setting NEXT_PUBLIC_TURNSTILE_SITE_KEY; with no
// key the widget renders nothing and the forms work as before.
export const TURNSTILE_SITE_KEY = process.env.NEXT_PUBLIC_TURNSTILE_SITE_KEY ?? ""

const SCRIPT_SRC = "https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit"

type TurnstileApi = {
  render: (
    container: HTMLElement,
    options: {
      sitekey: string
      callback: (token: string) => void
      "expired-callback": () => void
      "error-callback": () => void
      theme?: "light" | "dark" | "auto"
      size?: "normal" | "flexible" | "compact"
      action?: string
    }
  ) => string
  reset: (widgetId: string) => void
  remove: (widgetId: string) => void
}

declare global {
  interface Window {
    turnstile?: TurnstileApi
  }
}

let scriptPromise: Promise<TurnstileApi> | null = null

function loadTurnstile() {
  if (window.turnstile) return Promise.resolve(window.turnstile)

  if (!scriptPromise) {
    scriptPromise = new Promise((resolve, reject) => {
      const script = document.createElement("script")
      script.src = SCRIPT_SRC
      script.async = true
      script.defer = true
      script.onload = () => (window.turnstile ? resolve(window.turnstile) : reject(new Error("Turnstile did not load")))
      script.onerror = () => {
        scriptPromise = null
        reject(new Error("Turnstile did not load"))
      }
      document.head.appendChild(script)
    })
  }

  return scriptPromise
}

export type TurnstileHandle = {
  // Tokens are single use, so the widget is reset after every attempt.
  reset: () => void
}

type TurnstileProps = {
  onToken: (token: string | null) => void
  onError?: (message: string) => void
  action?: string
}

export const Turnstile = forwardRef<TurnstileHandle, TurnstileProps>(function Turnstile(
  { onToken, onError, action },
  ref
) {
  const containerRef = useRef<HTMLDivElement>(null)
  const widgetIdRef = useRef<string | null>(null)
  const onTokenRef = useRef(onToken)
  const onErrorRef = useRef(onError)

  onTokenRef.current = onToken
  onErrorRef.current = onError

  useImperativeHandle(ref, () => ({
    reset: () => {
      onTokenRef.current(null)
      if (widgetIdRef.current && window.turnstile) window.turnstile.reset(widgetIdRef.current)
    },
  }))

  useEffect(() => {
    if (!TURNSTILE_SITE_KEY) return

    let cancelled = false

    loadTurnstile()
      .then((turnstile) => {
        if (cancelled || !containerRef.current) return

        widgetIdRef.current = turnstile.render(containerRef.current, {
          sitekey: TURNSTILE_SITE_KEY,
          theme: "light",
          size: "flexible",
          action,
          callback: (token) => onTokenRef.current(token),
          "expired-callback": () => onTokenRef.current(null),
          "error-callback": () => {
            onTokenRef.current(null)
            onErrorRef.current?.("The robot check could not load. Refresh the page and try again.")
          },
        })
      })
      .catch(() => {
        onErrorRef.current?.("The robot check could not load. Check your connection and refresh the page.")
      })

    return () => {
      cancelled = true
      if (widgetIdRef.current && window.turnstile) window.turnstile.remove(widgetIdRef.current)
      widgetIdRef.current = null
      onTokenRef.current(null)
    }
  }, [action])

  if (!TURNSTILE_SITE_KEY) return null

  return <div ref={containerRef} className="min-h-[65px] w-full" />
})
