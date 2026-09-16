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

  let transaction

  try {
    transaction = await verifyPaystackTransaction(reference)
  } catch (error) {
    console.error("Paystack verification failed", error)

    return NextResponse.redirect(
      new URL("/payment/failed?reason=verification-failed", siteUrl)
    )
  }

  if (transaction.status !== "success") {
    return NextResponse.redirect(
      new URL("/payment/failed?reason=not-successful", siteUrl)
    )
  }

  try {
    await fulfilPaystackPayment(transaction)

    return NextResponse.redirect(
      new URL("/payment/success", siteUrl)
    )
  } catch (error) {
    // The charge succeeded on Paystack's side - this failed while granting
    // access, so the customer was charged even though this redirects to
    // the failure page. fulfilPaystackPayment already recorded the
    // payment as "error" for reconciliation, and the webhook (which fires
    // independently of this redirect) will usually retry and succeed.
    console.error(
      "Paystack fulfilment failed after a successful charge",
      error
    )

    return NextResponse.redirect(
      new URL(
        `/payment/failed?reason=fulfilment-error&reference=${encodeURIComponent(reference)}`,
        siteUrl
      )
    )
  }
}
