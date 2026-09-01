import Image from "next/image"
import Link from "next/link"
import { Check } from "lucide-react"

import { PaystackPurchaseButton } from "@/components/paystack-purchase-button"

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

const plans = [
  {
    name: "Per Subject",
    description: "Ideal for focused study",
    price: "R89",
    period: "/month",
    badge: "",
    disabled: false,
    productCode: "subject" as const,
    features: [
      "Single Subject Access",
      "Mock Exams",
      "Performance Tracking",
      "Mobile Access",
      "Question Explanations",
      "Priority Support",
    ],
  },
  {
    name: "PPL Pack",
    description: "Perfect for Private Pilot Licence students",
    price: "R699",
    period: "/3 Months",
    badge: "MOST POPULAR",
    disabled: false,
    productCode: "ppl_pack" as const,
    features: [
      "All 8 PPL Subjects",
      "Mock Exams",
      "Topic-Based Practice",
      "Performance Tracking",
      "Mobile Access",
      "Email Support",
    ],
  },
  {
    name: "CPL Pack",
    description: "Commercial Pilot content currently being expanded",
    price: "Coming Soon",
    period: "",
    badge: "COMING SOON",
    disabled: true,
    productCode: null,
    features: [
      "CPL Question Bank",
      "Mock Exams",
      "Advanced Analytics",
      "Mobile Access",
      "Priority Support",
      "New Content Updates",
    ],
  },
] as const

type UpgradePageProps = {
  searchParams: Promise<{
    subject?: string | string[]
  }>
}

function isSubjectSlug(value: string): value is SubjectSlug {
  return value in subjectLabels
}

export default async function UpgradePage({
  searchParams,
}: UpgradePageProps) {
  const params = await searchParams
  const requestedSubject = Array.isArray(params.subject)
    ? params.subject[0]
    : params.subject
  const selectedSubject =
    requestedSubject && isSubjectSlug(requestedSubject)
      ? requestedSubject
      : null
  const selectedSubjectLabel = selectedSubject
    ? subjectLabels[selectedSubject]
    : null

  return (
    <main className="min-h-screen bg-[#eef3f8] text-slate-900">
      <header className="sticky top-0 z-50 border-b border-white/15 bg-[#1f4e79]/96 text-white backdrop-blur">
        <div className="mx-auto flex h-16 max-w-7xl items-center justify-between gap-4 px-4 sm:h-[72px] sm:px-6 lg:px-8">
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
              href="/practice"
              className="rounded-lg px-3 py-2 text-sm font-medium text-blue-50 transition hover:bg-white/10 hover:text-white"
            >
              Practice
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

          {selectedSubjectLabel && (
            <p className="mx-auto mt-5 w-fit rounded-full border border-[#1f4e79]/20 bg-[#d6e6f7] px-4 py-2 text-sm font-semibold text-[#1f4e79]">
              Selected subject: {selectedSubjectLabel}
            </p>
          )}
        </div>

        <div className="mt-10 grid gap-6 sm:mt-14 lg:grid-cols-3">
          {plans.map((plan) => (
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
                  {plan.productCode === "subject" && selectedSubjectLabel
                    ? selectedSubjectLabel
                    : plan.name}
                </h2>

                <p className="mt-3 min-h-0 text-sm leading-6 text-slate-600 sm:min-h-12">
                  {plan.productCode === "subject" && selectedSubjectLabel
                    ? `One month of full ${selectedSubjectLabel} access`
                    : plan.description}
                </p>

                <div className="mt-5 sm:mt-6">
                  {plan.disabled ? (
                    <p className="text-2xl font-bold text-slate-500 sm:text-3xl">
                      {plan.price}
                    </p>
                  ) : (
                    <p>
                      <span className="text-4xl font-bold text-slate-900 sm:text-5xl">
                        {plan.price}
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
                  Coming Soon
                </button>
              ) : plan.productCode === "subject" && !selectedSubject ? (
                <Link
                  href="/practice"
                  className="mt-7 flex w-full items-center justify-center rounded-xl bg-[#1f4e79] px-5 py-3 text-sm font-bold text-white transition hover:bg-[#183d60] sm:mt-8"
                >
                  Choose a Subject
                </Link>
              ) : (
                <PaystackPurchaseButton
                  productCode={plan.productCode}
                  subject={
                    plan.productCode === "subject"
                      ? selectedSubject ?? undefined
                      : undefined
                  }
                >
                  {plan.productCode === "subject"
                    ? `Purchase ${selectedSubjectLabel}`
                    : "Purchase PPL Pack"}
                </PaystackPurchaseButton>
              )}
            </div>
          ))}
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
