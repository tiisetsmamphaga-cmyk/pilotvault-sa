import "server-only"

import {
  getBillingProduct,
  type ProductCode,
} from "@/src/lib/billing-products"
import type { PaystackTransaction } from "@/src/lib/paystack"
import { supabaseAdmin } from "@/src/lib/supabase-admin"

type PaymentMetadata = {
  user_id?: string
  product_code?: ProductCode
  subject?: string | null
}

function parseMetadata(value: unknown): PaymentMetadata {
  if (typeof value === "string") {
    try {
      return JSON.parse(value) as PaymentMetadata
    } catch {
      return {}
    }
  }

  if (value && typeof value === "object") {
    return value as PaymentMetadata
  }

  return {}
}

function addCalendarMonths(date: Date, months: number) {
  const result = new Date(date)
  const originalDay = result.getUTCDate()

  result.setUTCDate(1)
  result.setUTCMonth(result.getUTCMonth() + months)

  const lastDayOfTargetMonth = new Date(
    Date.UTC(result.getUTCFullYear(), result.getUTCMonth() + 1, 0)
  ).getUTCDate()

  result.setUTCDate(Math.min(originalDay, lastDayOfTargetMonth))

  return result
}

export async function fulfilPaystackPayment(
  transaction: PaystackTransaction
) {
  if (transaction.status !== "success") {
    throw new Error("The Paystack transaction is not successful.")
  }

  if (!transaction.reference) {
    throw new Error("The Paystack transaction has no reference.")
  }

  const metadata = parseMetadata(transaction.metadata)

  if (!metadata.user_id || !metadata.product_code) {
    throw new Error("The payment metadata is incomplete.")
  }

  const product = getBillingProduct(
    metadata.product_code,
    metadata.subject ?? undefined
  )

  if (
    transaction.amount !== product.amount ||
    transaction.currency !== product.currency
  ) {
    throw new Error("The payment amount or currency does not match.")
  }

  const paidAt = transaction.paid_at
    ? new Date(transaction.paid_at)
    : new Date()

  if (Number.isNaN(paidAt.getTime())) {
    throw new Error("The Paystack paid date is invalid.")
  }

  const expiresAt = addCalendarMonths(paidAt, product.accessMonths)
  const now = new Date().toISOString()

  if (product.productCode === "ppl_pack") {
    const { error } = await supabaseAdmin
      .from("Profiles")
      .update({
        subscription_status: "active",
        subscription_plan: "ppl",
        payment_status: "paid",
        subscription_expires_at: expiresAt.toISOString(),
        updated_at: now,
      })
      .eq("id", metadata.user_id)
      .select("id")
      .single()

    if (error) {
      throw new Error(`Could not activate the PPL Pack: ${error.message}`)
    }
  } else {
    const { error } = await supabaseAdmin
      .from("SubjectAccess")
      .upsert(
        {
          user_id: metadata.user_id,
          subject: product.subject,
          access_status: "active",
          starts_at: paidAt.toISOString(),
          expires_at: expiresAt.toISOString(),
        },
        {
          onConflict: "user_id,subject",
        }
      )

    if (error) {
      throw new Error(`Could not activate subject access: ${error.message}`)
    }
  }

  const { error: paymentError } = await supabaseAdmin
    .from("Payments")
    .upsert(
      {
        reference: transaction.reference,
        user_id: metadata.user_id,
        product_code: product.productCode,
        subject: product.subject,
        amount: transaction.amount,
        currency: transaction.currency,
        status: "fulfilled",
        paystack_transaction_id: String(transaction.id),
        paid_at: paidAt.toISOString(),
        fulfilled_at: now,
        updated_at: now,
      },
      {
        onConflict: "reference",
      }
    )

  if (paymentError) {
    throw new Error(`Could not record the payment: ${paymentError.message}`)
  }
}
