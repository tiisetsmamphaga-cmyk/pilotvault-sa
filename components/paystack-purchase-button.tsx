"use client"

import { useState } from "react"

import { supabase } from "@/src/lib/supabase"

type PaystackPurchaseButtonProps = {
  productCode: "ppl_pack" | "subject"
  subject?: string
  children: React.ReactNode
}

const PAYSTACK_INLINE_SRC = "https://js.paystack.co/v1/inline.js"

type PaystackPopHandler = {
  openIframe: () => void
}

type PaystackPopStatic = {
  setup: (options: {
    key: string
    email: string
    amount: number
    currency?: string
    ref: string
    metadata?: unknown
    callback: (response: { reference: string }) => void
    onClose: () => void
  }) => PaystackPopHandler
}

declare global {
  interface Window {
    PaystackPop?: PaystackPopStatic
  }
}

let inlineScriptPromise: Promise<void> | null = null

function loadPaystackInlineScript(): Promise<void> {
  if (window.PaystackPop) return Promise.resolve()

  if (!inlineScriptPromise) {
    inlineScriptPromise = new Promise((resolve, reject) => {
      const existing = document.querySelector<HTMLScriptElement>(
        `script[src="${PAYSTACK_INLINE_SRC}"]`
      )

      if (existing) {
        existing.addEventListener("load", () => resolve())
        existing.addEventListener("error", () =>
          reject(new Error("Failed to load Paystack checkout."))
        )
        return
      }

      const script = document.createElement("script")
      script.src = PAYSTACK_INLINE_SRC
      script.async = true
      script.onload = () => resolve()
      script.onerror = () =>
        reject(new Error("Failed to load Paystack checkout."))
      document.head.appendChild(script)
    })
  }

  return inlineScriptPromise
}

export function PaystackPurchaseButton({
  productCode,
  subject,
  children,
}: PaystackPurchaseButtonProps) {
  const [loading, setLoading] = useState(false)
  const [errorMessage, setErrorMessage] = useState("")

  const startPayment = async () => {
    setLoading(true)
    setErrorMessage("")

    try {
      const {
        data: { session },
        error: sessionError,
      } = await supabase.auth.getSession()

      if (sessionError || !session?.access_token) {
        throw new Error("Please log in again before making a payment.")
      }

      const response = await fetch("/api/paystack/initialize", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${session.access_token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          productCode,
          subject,
        }),
      })

      const result = (await response.json()) as {
        authorizationUrl?: string
        reference?: string
        amount?: number
        email?: string
        currency?: string
        error?: string
      }

      if (!response.ok || !result.authorizationUrl || !result.reference) {
        throw new Error(result.error || "Unable to open secure checkout.")
      }

      const { authorizationUrl, reference, amount, email, currency } = result
      const publicKey = process.env.NEXT_PUBLIC_PAYSTACK_PUBLIC_KEY

      const goToCallback = () => {
        window.location.assign(
          `/api/paystack/callback?reference=${encodeURIComponent(reference)}`
        )
      }

      // Keep checkout on pilotvault.co.za via Paystack's inline popup when
      // possible. Falls back to the full-page redirect if the popup script
      // can't load or doesn't behave as expected - payment must never be
      // blocked by this being unavailable.
      if (publicKey && amount && email) {
        try {
          await loadPaystackInlineScript()

          if (!window.PaystackPop) {
            throw new Error(
              "window.PaystackPop is not defined after the script loaded."
            )
          }

          const handler = window.PaystackPop.setup({
            key: publicKey,
            email,
            amount,
            currency,
            ref: reference,
            callback: () => goToCallback(),
            onClose: () => setLoading(false),
          })

          handler.openIframe()
          return
        } catch (inlineError) {
          console.error(
            "Paystack inline checkout unavailable, falling back to redirect",
            inlineError
          )
        }
      }

      window.location.assign(authorizationUrl)
    } catch (error) {
      setErrorMessage(
        error instanceof Error
          ? error.message
          : "Unable to start the payment."
      )
      setLoading(false)
    }
  }

  return (
    <div className="mt-7 sm:mt-8">
      <button
        type="button"
        onClick={startPayment}
        disabled={loading}
        className="w-full rounded-xl bg-[#1f4e79] px-5 py-3 text-sm font-bold text-white transition hover:bg-[#183d60] disabled:cursor-not-allowed disabled:opacity-60"
      >
        {loading ? "Opening secure checkout..." : children}
      </button>

      {errorMessage && (
        <p className="mt-3 rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm leading-6 text-red-700">
          {errorMessage}
        </p>
      )}
    </div>
  )
}
