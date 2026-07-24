import { NextResponse } from "next/server"

import { fulfilPaystackPayment } from "@/src/lib/fulfil-payment"
import { verifyPaystackTransaction } from "@/src/lib/paystack"

export const runtime = "nodejs"

function getSiteUrl() {
  const configuredUrl = process.env.NEXT_PUBLIC_SITE_URL

  if (configuredUrl) {
    return configuredUrl.replace(/\/$/, "")
  }

  const productionUrl = process.env.VERCEL_PROJECT_PRODUCTION_URL

  if (productionUrl) {
    return `https://${productionUrl.replace(/\/$/, "")}`
  }

  return "https://pilotvault.co.za"
}

export async function GET(request: Request) {
  const siteUrl = getSiteUrl()
  const requestUrl = new URL(request.url)
  const reference =
    requestUrl.searchParams.get("reference") ??
    requestUrl.searchParams.get("trxref")

  if (!reference) {
    return NextResponse.redirect(
      new URL("/payment/failed?reason=invalid-reference", siteUrl)
    )
  }

  try {
    const transaction = await verifyPaystackTransaction(reference)

    await fulfilPaystackPayment(transaction)

    return NextResponse.redirect(
      new URL("/payment/success", siteUrl)
    )
  } catch (error) {
    console.error("Paystack callback failed", error)

    return NextResponse.redirect(
      new URL("/payment/failed", siteUrl)
    )
  }
}
