import "server-only"

const PAYSTACK_API_URL = "https://api.paystack.co"

type PaystackApiResponse<T> = {
  status: boolean
  message: string
  data: T
}

export type PaystackTransaction = {
  id: number
  status: string
  reference: string
  amount: number
  currency: string
  paid_at: string | null
  metadata: unknown
  customer?: {
    email?: string
  }
}

type InitialiseTransactionInput = {
  email: string
  amount: number
  currency: "ZAR"
  callbackUrl: string
  metadata: Record<string, string | null>
}

function getPaystackSecretKey() {
  const secretKey = process.env.PAYSTACK_SECRET_KEY

  if (!secretKey) {
    throw new Error("PAYSTACK_SECRET_KEY is not configured.")
  }

  return secretKey
}

async function readPaystackResponse<T>(response: Response) {
  const result = (await response.json()) as PaystackApiResponse<T>

  if (!response.ok || !result.status) {
    throw new Error(result.message || "Paystack request failed.")
  }

  return result.data
}

export async function initialisePaystackTransaction(
  input: InitialiseTransactionInput
) {
  const response = await fetch(
    `${PAYSTACK_API_URL}/transaction/initialize`,
    {
      method: "POST",
      headers: {
        Authorization: `Bearer ${getPaystackSecretKey()}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        email: input.email,
        amount: String(input.amount),
        currency: input.currency,
        callback_url: input.callbackUrl,
        metadata: JSON.stringify(input.metadata),
      }),
      cache: "no-store",
    }
  )

  return readPaystackResponse<{
    authorization_url: string
    access_code: string
    reference: string
  }>(response)
}

export async function verifyPaystackTransaction(
  reference: string
): Promise<PaystackTransaction> {
  const response = await fetch(
    `${PAYSTACK_API_URL}/transaction/verify/${encodeURIComponent(reference)}`,
    {
      headers: {
        Authorization: `Bearer ${getPaystackSecretKey()}`,
      },
      cache: "no-store",
    }
  )

  return readPaystackResponse<PaystackTransaction>(response)
}
