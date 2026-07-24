import { createHmac, timingSafeEqual } from "node:crypto"

import { fulfilPaystackPayment } from "@/src/lib/fulfil-payment"
import { verifyPaystackTransaction } from "@/src/lib/paystack"

export const runtime = "nodejs"

function signatureMatches(received: string, expected: string) {
  try {
    const receivedBuffer = Buffer.from(received, "hex")
    const expectedBuffer = Buffer.from(expected, "hex")

    return (
      receivedBuffer.length === expectedBuffer.length &&
      timingSafeEqual(receivedBuffer, expectedBuffer)
    )
  } catch {
    return false
  }
}

export async function POST(request: Request) {
  const secretKey = process.env.PAYSTACK_SECRET_KEY

  if (!secretKey) {
    console.error("PAYSTACK_SECRET_KEY is not configured")
    return new Response("Missing server configuration", { status: 500 })
  }

  const rawBody = await request.text()
  const receivedSignature =
    request.headers.get("x-paystack-signature") ?? ""
  const expectedSignature = createHmac("sha512", secretKey)
    .update(rawBody)
    .digest("hex")

  if (!signatureMatches(receivedSignature, expectedSignature)) {
    return new Response("Invalid signature", { status: 401 })
  }

  let event: {
    event?: string
    data?: {
      reference?: string
    }
  }

  try {
    event = JSON.parse(rawBody) as typeof event
  } catch {
    return new Response("Invalid payload", { status: 400 })
  }

  if (event.event !== "charge.success") {
    return Response.json({ received: true })
  }

  const reference = event.data?.reference

  if (!reference) {
    return new Response("Missing transaction reference", { status: 400 })
  }

  try {
    const transaction = await verifyPaystackTransaction(reference)

    await fulfilPaystackPayment(transaction)

    return Response.json({ received: true })
  } catch (error) {
    console.error("Paystack webhook fulfilment failed", error)
    return new Response("Webhook processing failed", { status: 500 })
  }
}
