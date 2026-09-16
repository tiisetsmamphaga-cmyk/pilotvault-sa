import { NextResponse } from "next/server"

import {
  getBillingProduct,
  type ProductCode,
} from "@/src/lib/billing-products"
import { initialisePaystackTransaction } from "@/src/lib/paystack"
import { supabaseAdmin } from "@/src/lib/supabase-admin"
import {
  applyTrialDiscount,
  getTrialDiscountEligibility,
} from "@/src/lib/trial-discount"

export const runtime = "nodejs"

type InitialisePaymentBody = {
  productCode?: ProductCode
  subject?: string
}

function readBearerToken(request: Request) {
  const authorization = request.headers.get("authorization") ?? ""
  const match = authorization.match(/^Bearer\s+(.+)$/i)

  return match?.[1] ?? null
}

export async function POST(request: Request) {
  try {
    const accessToken = readBearerToken(request)

    if (!accessToken) {
      return NextResponse.json(
        { error: "Log in before purchasing access." },
        { status: 401 }
      )
    }

    const {
      data: { user },
      error: userError,
    } = await supabaseAdmin.auth.getUser(accessToken)

    if (userError || !user?.email) {
      return NextResponse.json(
        { error: "Your session has expired. Please log in again." },
        { status: 401 }
      )
    }

    const body = (await request.json()) as InitialisePaymentBody

    if (!body.productCode) {
      return NextResponse.json(
        { error: "Select a PilotVault product." },
        { status: 400 }
      )
    }

    const product = getBillingProduct(
      body.productCode,
      body.subject
    )

    const { data: profile } = await supabaseAdmin
      .from("Profiles")
      .select("trial_ends_at")
      .eq("id", user.id)
      .maybeSingle()

    const discount = getTrialDiscountEligibility(profile?.trial_ends_at)
    const amount = discount.eligible
      ? applyTrialDiscount(product.amount)
      : product.amount

    // Use the origin this request actually came in on (production, a
    // preview deployment, or localhost) so Paystack redirects back to
    // wherever the purchase was started, not always the production domain.
    const siteUrl = new URL(request.url).origin

    const transaction = await initialisePaystackTransaction({
      email: user.email,
      amount,
      currency: product.currency,
      callbackUrl: `${siteUrl}/api/paystack/callback`,
      metadata: {
        user_id: user.id,
        product_code: product.productCode,
        subject: product.subject,
        discount_applied: discount.eligible,
        original_amount: product.amount,
      },
    })

    return NextResponse.json({
      authorizationUrl: transaction.authorization_url,
      accessCode: transaction.access_code,
      reference: transaction.reference,
      amount,
      email: user.email,
      currency: product.currency,
    })
  } catch (error) {
    console.error("Paystack initialisation failed", error)

    return NextResponse.json(
      {
        error:
          error instanceof Error
            ? error.message
            : "Unable to start the payment.",
      },
      { status: 500 }
    )
  }
}
