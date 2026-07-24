import { NextResponse } from "next/server"

import {
  getBillingProduct,
  type ProductCode,
} from "@/src/lib/billing-products"
import { initialisePaystackTransaction } from "@/src/lib/paystack"
import { supabaseAdmin } from "@/src/lib/supabase-admin"

export const runtime = "nodejs"

type InitialisePaymentBody = {
  productCode?: ProductCode
  subject?: string
}

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

    const transaction = await initialisePaystackTransaction({
      email: user.email,
      amount: product.amount,
      currency: product.currency,
      callbackUrl: `${getSiteUrl()}/api/paystack/callback`,
      metadata: {
        user_id: user.id,
        product_code: product.productCode,
        subject: product.subject,
      },
    })

    return NextResponse.json({
      authorizationUrl: transaction.authorization_url,
      reference: transaction.reference,
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
