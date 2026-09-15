// Shared between server (Paystack amount) and client (upgrade page display),
// so the price a user sees is guaranteed to match what they're charged.
export const TRIAL_DISCOUNT_PERCENT = 15
export const TRIAL_DISCOUNT_WINDOW_HOURS = 24

export type TrialDiscountEligibility = {
  eligible: boolean
  msRemaining: number | null
}

// Eligible any time from signup through 24h after the trial ends - covers
// both "upgrade while still in the trial" and "upgrade shortly after it
// expired", as one continuous window rather than two separate offers.
export function getTrialDiscountEligibility(
  trialEndsAt: string | null | undefined,
  now: number = Date.now()
): TrialDiscountEligibility {
  if (!trialEndsAt) {
    return { eligible: false, msRemaining: null }
  }

  const trialEndsAtMs = new Date(trialEndsAt).getTime()

  if (Number.isNaN(trialEndsAtMs)) {
    return { eligible: false, msRemaining: null }
  }

  const windowEndsAt =
    trialEndsAtMs + TRIAL_DISCOUNT_WINDOW_HOURS * 60 * 60 * 1000
  const msRemaining = windowEndsAt - now

  return { eligible: msRemaining > 0, msRemaining: Math.max(msRemaining, 0) }
}

export function applyTrialDiscount(amountCents: number) {
  return Math.round(amountCents * (1 - TRIAL_DISCOUNT_PERCENT / 100))
}

export function formatCountdown(msRemaining: number) {
  const totalMinutes = Math.max(0, Math.floor(msRemaining / (60 * 1000)))
  const days = Math.floor(totalMinutes / (60 * 24))
  const hours = Math.floor((totalMinutes % (60 * 24)) / 60)
  const minutes = totalMinutes % 60

  if (days > 0) return `${days}d ${hours}h`
  if (hours > 0) return `${hours}h ${minutes}m`
  return `${minutes}m`
}
