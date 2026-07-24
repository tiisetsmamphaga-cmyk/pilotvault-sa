import "server-only"

export const PILOTVAULT_SUBJECTS = [
  "meteorology",
  "air-law",
  "navigation",
  "human-performance",
  "principles-of-flight",
  "aircraft-technical-and-general",
  "radio-telephony",
  "flight-planning",
] as const

export type PilotVaultSubject =
  (typeof PILOTVAULT_SUBJECTS)[number]

export type ProductCode = "ppl_pack" | "subject"

export type BillingProduct = {
  productCode: ProductCode
  subject: PilotVaultSubject | null
  amount: number
  currency: "ZAR"
  accessMonths: number
  label: string
}

const SUBJECT_LABELS: Record<PilotVaultSubject, string> = {
  meteorology: "Meteorology",
  "air-law": "Air Law",
  navigation: "Navigation",
  "human-performance": "Human Performance",
  "principles-of-flight": "Principles of Flight",
  "aircraft-technical-and-general":
    "Aircraft Technical and General",
  "radio-telephony": "Radio Telephony",
  "flight-planning": "Flight Planning",
}

function readAmount(variableName: string, fallback: number) {
  const value = process.env[variableName]

  if (!value) return fallback

  const amount = Number(value)

  if (!Number.isInteger(amount) || amount <= 0) {
    throw new Error(`${variableName} must be a positive integer in cents.`)
  }

  return amount
}

export function isPilotVaultSubject(
  value: string
): value is PilotVaultSubject {
  return PILOTVAULT_SUBJECTS.includes(value as PilotVaultSubject)
}

export function getBillingProduct(
  productCode: string,
  subject?: string
): BillingProduct {
  if (productCode === "ppl_pack") {
    return {
      productCode,
      subject: null,
      amount: readAmount("PPL_PACK_PRICE_CENTS", 69900),
      currency: "ZAR",
      accessMonths: 3,
      label: "PilotVault PPL Pack",
    }
  }

  if (productCode !== "subject") {
    throw new Error("Select a valid PilotVault product.")
  }

  if (!subject || !isPilotVaultSubject(subject)) {
    throw new Error("Select a valid PilotVault subject.")
  }

  return {
    productCode,
    subject,
    amount: readAmount("SUBJECT_PRICE_CENTS", 8900),
    currency: "ZAR",
    accessMonths: 1,
    label: `PilotVault ${SUBJECT_LABELS[subject]}`,
  }
}
