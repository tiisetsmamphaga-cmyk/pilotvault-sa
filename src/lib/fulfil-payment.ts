import "server-only"

import {
  getBillingProduct,
  type ProductCode,
} from "@/src/lib/billing-products"
import type { PaystackTransaction } from "@/src/lib/paystack"
import { supabaseAdmin } from "@/src/lib/supabase-admin"
import { applyTrialDiscount } from "@/src/lib/trial-discount"

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

  // Record that Paystack confirmed this charge before attempting to grant
  // access. If anything below throws, the payment still has a row here
  // (status "pending" or "error") instead of a paid customer having zero
  // trace of their charge in our own database.
  const { data: existingPayment, error: existingPaymentError } =
    await supabaseAdmin
      .from("Payments")
      .select("status")
      .eq("reference", transaction.reference)
      .maybeSingle()

  if (existingPaymentError) {
    throw new Error(
      `Could not check the existing payment record: ${existingPaymentError.message}`
    )
  }

  // Already fully processed (e.g. a duplicate webhook delivery for the same
  // reference, or the callback and webhook racing each other) - do nothing
  // further so a retry can never grant an extra renewal period.
  if (existingPayment?.status === "fulfilled") {
    return
  }

  const { error: recordError } = await supabaseAdmin.from("Payments").upsert(
    {
      reference: transaction.reference,
      user_id: metadata.user_id,
      product_code: metadata.product_code,
      subject: metadata.subject ?? null,
      amount: transaction.amount,
      currency: transaction.currency,
      status: "pending",
      paystack_transaction_id: String(transaction.id),
      updated_at: new Date().toISOString(),
    },
    { onConflict: "reference" }
  )

  if (recordError) {
    throw new Error(`Could not record the payment: ${recordError.message}`)
  }

  try {
    const product = getBillingProduct(
      metadata.product_code,
      metadata.subject ?? undefined
    )

    // Trial-expiry discount: the initialize route may have charged 15% off
    // for a user within 24h of their trial ending, so accept either the
    // full price or exactly that discounted price - never anything else.
    const validAmounts = [product.amount, applyTrialDiscount(product.amount)]

    if (
      !validAmounts.includes(transaction.amount) ||
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

    const now = new Date().toISOString()

    if (product.productCode === "ppl_pack") {
      const { data: currentProfile, error: profileReadError } =
        await supabaseAdmin
          .from("Profiles")
          .select("subscription_expires_at")
          .eq("id", metadata.user_id)
          .maybeSingle()

      if (profileReadError) {
        throw new Error(
          `Could not read the current subscription: ${profileReadError.message}`
        )
      }

      const currentExpiry = currentProfile?.subscription_expires_at
        ? new Date(currentProfile.subscription_expires_at)
        : null
      // Renewing early extends from whatever is later - the current expiry
      // if it's still in the future, otherwise the payment date - so time
      // already paid for is never forfeited.
      const extendsFrom =
        currentExpiry && currentExpiry > paidAt ? currentExpiry : paidAt
      const expiresAt = addCalendarMonths(extendsFrom, product.accessMonths)

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
      const { data: currentAccess, error: accessReadError } =
        await supabaseAdmin
          .from("SubjectAccess")
          .select("expires_at")
          .eq("user_id", metadata.user_id)
          .eq("subject", product.subject)
          .maybeSingle()

      if (accessReadError) {
        throw new Error(
          `Could not read the current subject access: ${accessReadError.message}`
        )
      }

      const currentExpiry = currentAccess?.expires_at
        ? new Date(currentAccess.expires_at)
        : null
      const extendsFrom =
        currentExpiry && currentExpiry > paidAt ? currentExpiry : paidAt
      const expiresAt = addCalendarMonths(extendsFrom, product.accessMonths)

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

    const { error: fulfilledError } = await supabaseAdmin
      .from("Payments")
      .update({
        status: "fulfilled",
        paid_at: paidAt.toISOString(),
        fulfilled_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      })
      .eq("reference", transaction.reference)

    if (fulfilledError) {
      throw new Error(
        `Could not record the payment: ${fulfilledError.message}`
      )
    }
  } catch (error) {
    // The charge already has a row from above; mark it so it can be
    // reconciled against Paystack's dashboard instead of vanishing.
    await supabaseAdmin
      .from("Payments")
      .update({ status: "error", updated_at: new Date().toISOString() })
      .eq("reference", transaction.reference)

    throw error
  }
}
