"use client"

import { useState } from "react"

import { supabase } from "@/src/lib/supabase"

type PaystackPurchaseButtonProps = {
  productCode: "ppl_pack" | "subject"
  subject?: string
  children: React.ReactNode
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
        error?: string
      }

      if (!response.ok || !result.authorizationUrl) {
        throw new Error(result.error || "Unable to open secure checkout.")
      }

      window.location.assign(result.authorizationUrl)
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
