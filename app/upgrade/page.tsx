"use client"

import { Suspense, useEffect, useState } from "react"
import Image from "next/image"
import Link from "next/link"
import { useSearchParams } from "next/navigation"
import {
  Check,
  Cloud,
  Compass,
  Cpu,
  Gauge,
  Map,
  Plane,
  Radio,
  Scale,
} from "lucide-react"

import { PaystackPurchaseButton } from "@/components/paystack-purchase-button"
import {
  getCachedCurrentUser,
  getCachedProfile,
  getCachedSubjectAccess,
} from "@/src/lib/client-data-cache"
import {
  applyTrialDiscount,
  formatCountdown,
  getTrialDiscountEligibility,
  type TrialDiscountEligibility,
} from "@/src/lib/trial-discount"

const subjectLabels = {
  meteorology: "Meteorology",
  "air-law": "Air Law",
  navigation: "Navigation",
  "human-performance": "Human Performance",
  "principles-of-flight": "Principles of Flight",
  "aircraft-technical-and-general":
    "Aircraft Technical and General",
  "radio-telephony": "Radio Telephony",
  "flight-planning": "Flight Planning",
} as const

type SubjectSlug = keyof typeof subjectLabels

const SUBJECT_PRICE_CENTS = 8900

const subjects: { slug: SubjectSlug; name: string; icon: typeof Cloud }[] = [
  { slug: "meteorology", name: "Meteorology", icon: Cloud },
  { slug: "air-law", name: "Air Law", icon: Scale },
  { slug: "navigation", name: "Navigation", icon: Compass },
  { slug: "human-performance", name: "Human Performance", icon: Gauge },
  { slug: "principles-of-flight", name: "Principles of Flight", icon: Plane },
  {
    slug: "aircraft-technical-and-general",
    name: "Aircraft Technical and General",
    icon: Cpu,
  },
  { slug: "radio-telephony", name: "Radio Telephony", icon: Radio },
  { slug: "flight-planning", name: "Flight Planning", icon: Map },
]

const plans = [
  {
    name: "PPL Pack",
    description: "Everything you need for all 8 PPL exams",
    priceCents: 69900,
    period: "/3 months",
    badge: "MOST POPULAR",
    disabled: false,
    productCode: "ppl_pack" as const,
    features: [
      "All 8 PPL subjects, full question banks",
      "Timed mock exams for every subject",
      "Topic-based practice",
      "Detailed answer explanations",
      "Track your mock exam scores",
      "Study on phone, tablet or laptop",
      "Email support",
    ],
  },
  {
    name: "CPL Pack",
    description: "CPL content is being expanded. Full pack launches 1 January 2027",
    priceCents: null,
    period: "",
    badge: "COMING SOON",
    disabled: true,
    productCode: null,
    features: [
      "CPL question bank",
      "Timed mock exams",
      "Topic-based practice",
      "Detailed answer explanations",
      "Study on phone, tablet or laptop",
    ],
  },
] as const

function isSubjectSlug(value: string): value is SubjectSlug {
  return value in subjectLabels
}

function formatRand(cents: number) {
  const rand = cents / 100
  return Number.isInteger(rand) ? `R${rand}` : `R${rand.toFixed(2)}`
}

const COUNTDOWN_TICK_MS = 60 * 1000

export default function UpgradePage() {
  return (
    <Suspense fallback={null}>
      <UpgradePageContent />
    </Suspense>
  )
}

function UpgradePageContent() {
  const searchParams = useSearchParams()
  const requestedSubject = searchParams.get("subject")
  const selectedSubject =
    requestedSubject && isSubjectSlug(requestedSubject)
      ? requestedSubject
      : null

  const [discount, setDiscount] = useState<TrialDiscountEligibility>({
    eligible: false,
    msRemaining: null,
  })
  const [hasActivePpl, setHasActivePpl] = useState(false)
  const [ownedSubjects, setOwnedSubjects] = useState<Set<string>>(new Set())

  useEffect(() => {
    let cancelled = false

    const loadAccountState = async () => {
      try {
        const user = await getCachedCurrentUser()
        if (!user) return

        const [profile, subjectAccess] = await Promise.all([
          getCachedProfile(user.id),
          getCachedSubjectAccess(user.id).catch(() => []),
        ])

        if (cancelled) return

        setDiscount(getTrialDiscountEligibility(profile.trial_ends_at))

        setHasActivePpl(
          profile.subscription_status === "active" &&
            profile.subscription_plan === "ppl" &&
            Boolean(profile.subscription_expires_at) &&
            new Date(profile.subscription_expires_at as string) > new Date()
        )

        setOwnedSubjects(
          new Set(
            subjectAccess
              .filter(
                (access) =>
                  access.access_status === "active" &&
                  new Date(access.expires_at) > new Date()
              )
              .map((access) => access.subject)
          )
        )
      } catch {
        // Not logged in, or profile unavailable - just show standard pricing.
      }
    }

    loadAccountState()

    return () => {
      cancelled = true
    }
  }, [])

  useEffect(() => {
    if (!discount.eligible) return

    const interval = window.setInterval(() => {
      setDiscount((previous) => {
        if (previous.msRemaining === null) return previous
        const next = previous.msRemaining - COUNTDOWN_TICK_MS
        return next > 0
          ? { eligible: true, msRemaining: next }
          : { eligible: false, msRemaining: null }
      })
    }, COUNTDOWN_TICK_MS)

    return () => window.clearInterval(interval)
  }, [discount.eligible])

  return (
    <main className="min-h-screen bg-[#eef3f8] text-slate-900">
      <header className="sticky top-0 z-50 border-b border-white/15 bg-[#1f4e79] text-white">
        <div className="mx-auto flex h-16 max-w-7xl items-center justify-between gap-4 px-4 sm:h-20 sm:px-6 lg:px-8">
          <div className="flex min-w-0 items-center gap-3">
            <Link href="/dashboard" className="shrink-0" aria-label="PilotVault dashboard">
              <Image
                src="/images/Header logo.png"
                alt="PilotVault SA"
                width={180}
                height={54}
                className="h-auto w-[132px] object-contain sm:w-[154px]"
                priority
              />
            </Link>
            <span className="hidden h-7 w-px bg-white/20 sm:block" />
            <span className="hidden text-sm font-medium text-blue-50/90 sm:block">
              Plans
            </span>
          </div>

          <nav aria-label="Plans navigation" className="hidden items-center gap-1 md:flex">
            <Link
              href="/dashboard"
              className="rounded-lg px-3 py-2 text-sm font-medium text-blue-50 transition hover:bg-white/10 hover:text-white"
            >
              Dashboard
            </Link>
            <Link
              href="/upgrade"
              aria-current="page"
              className="rounded-lg bg-white/12 px-3 py-2 text-sm font-semibold text-white"
            >
              Plans
            </Link>
            <Link
              href="/profile"
              className="rounded-lg px-3 py-2 text-sm font-medium text-blue-50 transition hover:bg-white/10 hover:text-white"
            >
              Profile
            </Link>
          </nav>
        </div>
      </header>

      <section className="mx-auto max-w-7xl px-4 py-10 sm:px-6 sm:py-12 lg:px-8">
        <div className="mx-auto max-w-3xl text-center">
          <p className="text-[10px] font-semibold uppercase tracking-[0.3em] text-[#1f4e79] sm:text-xs">
            Continue your preparation
          </p>

          <h1 className="mt-4 text-3xl font-bold leading-tight tracking-tight text-slate-900 sm:text-5xl">
            Unlock the full PilotVault experience.
          </h1>

          <p className="mt-5 text-sm leading-7 text-slate-600 sm:text-lg sm:leading-8">
            Your trial gives you a limited 25-question mock exam set. Upgrade to
            unlock the full SACAA question bank, topic-based practice, mock
            exams, explanations, and progress tracking.
          </p>

          {discount.eligible && discount.msRemaining !== null && (
            <div className="mx-auto mt-6 w-fit rounded-full border border-[#f0d488] bg-[#fdf3d9] px-5 py-2.5 text-sm font-bold text-[#8a6d1f]">
              15% off ends in {formatCountdown(discount.msRemaining)} - upgrade now
            </div>
          )}
        </div>

        <div className="mx-auto mt-10 grid max-w-3xl gap-6 sm:mt-14 md:grid-cols-2">
          {plans.map((plan) => {
            const discountedCents =
              plan.priceCents !== null && discount.eligible
                ? applyTrialDiscount(plan.priceCents)
                : plan.priceCents

            return (
              <div
                key={plan.name}
                className={`relative rounded-3xl border bg-white p-6 shadow-sm sm:p-8 ${
                  plan.badge === "MOST POPULAR"
                    ? "border-[#1f4e79] shadow-md"
                    : "border-slate-200"
                }`}
              >
                {plan.badge && (
                  <div className="absolute -top-3 left-1/2 -translate-x-1/2 rounded-full bg-[#1f4e79] px-4 py-1 text-[10px] font-bold text-white sm:-top-4 sm:px-5 sm:text-xs">
                    {plan.badge}
                  </div>
                )}

                <div className="text-center">
                  <h2 className="text-xl font-bold text-slate-900 sm:text-2xl">
                    {plan.name}
                  </h2>

                  <p className="mt-3 min-h-0 text-sm leading-6 text-slate-600 sm:min-h-12">
                    {plan.description}
                  </p>

                  <div className="mt-5 sm:mt-6">
                    {plan.priceCents === null ? (
                      <p className="text-2xl font-bold text-slate-500 sm:text-3xl">
                        Coming Soon
                      </p>
                    ) : (
                      <p>
                        {discount.eligible && discountedCents !== null && (
                          <span className="mr-2 text-lg text-slate-400 line-through sm:text-xl">
                            {formatRand(plan.priceCents)}
                          </span>
                        )}
                        <span className="text-4xl font-bold text-slate-900 sm:text-5xl">
                          {formatRand(discountedCents ?? plan.priceCents)}
                        </span>
                        <span className="text-sm text-slate-500 sm:text-base">
                          {" "}
                          {plan.period}
                        </span>
                      </p>
                    )}
                  </div>
                </div>

                <div className="mt-7 space-y-3 sm:mt-8 sm:space-y-4">
                  {plan.features.map((feature) => (
                    <div key={feature} className="flex items-center gap-3">
                      <span className="flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-[#d6e6f7]">
                        <Check className="h-3.5 w-3.5 text-[#1f4e79]" />
                      </span>
                      <p className="text-sm text-slate-700">{feature}</p>
                    </div>
                  ))}
                </div>

                {plan.disabled ? (
                  <button
                    disabled
                    className="mt-7 w-full rounded-xl bg-slate-100 px-5 py-3 text-sm font-bold text-slate-400 sm:mt-8"
                  >
                    Available 1 Jan 2027
                  </button>
                ) : (
                  <>
                    {plan.productCode === "ppl_pack" && hasActivePpl && (
                      <p className="mb-2 text-xs font-medium text-[#1f4e79]">
                        You already have an active PPL Pack - purchasing
                        extends it from your current expiry date.
                      </p>
                    )}
                    <PaystackPurchaseButton productCode={plan.productCode}>
                      {plan.productCode === "ppl_pack" && hasActivePpl
                        ? "Renew PPL Pack"
                        : "Purchase PPL Pack"}
                    </PaystackPurchaseButton>
                  </>
                )}
              </div>
            )
          })}
        </div>

        <div className="mt-14 sm:mt-20">
          <div className="mx-auto max-w-2xl text-center">
            <h2 className="text-2xl font-bold text-slate-900 sm:text-3xl">
              Or unlock one subject at a time
            </h2>
            <p className="mt-3 text-sm leading-6 text-slate-600 sm:text-base">
              Full question bank, mock exams and topic-based practice for a
              single subject - pick a card to purchase it directly.
            </p>
          </div>

          <div className="mt-8 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
            {subjects.map((subject) => {
              const Icon = subject.icon
              const isDeepLinked = selectedSubject === subject.slug
              const isOwned = ownedSubjects.has(subject.slug)
              const discountedCents = discount.eligible
                ? applyTrialDiscount(SUBJECT_PRICE_CENTS)
                : null

              return (
                <div
                  key={subject.slug}
                  className={`flex flex-col rounded-2xl border bg-white p-5 shadow-sm transition ${
                    isDeepLinked
                      ? "border-[#1f4e79] ring-2 ring-[#1f4e79]/25"
                      : "border-slate-200"
                  }`}
                >
                  {isDeepLinked && (
                    <span className="mb-3 inline-flex w-fit items-center rounded-full bg-[#d6e6f7] px-2.5 py-1 text-[10px] font-bold uppercase tracking-wide text-[#1f4e79]">
                      You were viewing this
                    </span>
                  )}

                  {isOwned && (
                    <span className="mb-3 inline-flex w-fit items-center rounded-full bg-[#fdf3d9] px-2.5 py-1 text-[10px] font-bold uppercase tracking-wide text-[#b8860a]">
                      Active
                    </span>
                  )}

                  <span className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-[#d6e6f7] text-[#1f4e79]">
                    <Icon className="h-5 w-5" />
                  </span>

                  <h3 className="mt-4 text-base font-bold text-slate-900">
                    {subject.name}
                  </h3>

                  <p className="mt-2">
                    {discount.eligible && discountedCents !== null && (
                      <span className="mr-1.5 text-sm text-slate-400 line-through">
                        {formatRand(SUBJECT_PRICE_CENTS)}
                      </span>
                    )}
                    <span className="text-2xl font-bold text-slate-900">
                      {formatRand(discountedCents ?? SUBJECT_PRICE_CENTS)}
                    </span>
                    <span className="text-sm text-slate-500">/month</span>
                  </p>

                  <div className="mt-auto">
                    <PaystackPurchaseButton
                      productCode="subject"
                      subject={subject.slug}
                    >
                      {isOwned ? "Renew" : "Purchase"}
                    </PaystackPurchaseButton>
                  </div>
                </div>
              )
            })}
          </div>
        </div>

        <div className="mt-10 rounded-3xl border border-slate-200 bg-white p-5 text-center shadow-sm sm:mt-12 sm:p-8">
          <p className="text-sm leading-6 text-slate-600">
            Payments are processed securely by Paystack. Access is activated
            only after PilotVault verifies the completed transaction.
          </p>
        </div>
      </section>
    </main>
  )
}
