import Link from "next/link"
import { Check } from "lucide-react"

const plans = [
  {
    name: "Per Subject",
    description: "Ideal for focused study",
    price: "R89",
    period: "/month",
    badge: "",
    disabled: false,
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
    description: "Perfect for Private Pilot License students",
    price: "R699",
    period: "/3 Months",
    badge: "MOST POPULAR",
    disabled: false,
    features: [
      "PPL Subject Questions",
      "Mock Exams",
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
    features: [
      "CPL Question Bank",
      "Mock Exams",
      "Advanced Analytics",
      "Mobile Access",
      "Priority Support",
      "New Content Updates",
    ],
  },
]

export default function UpgradePage() {
  return (
    <main className="min-h-screen bg-[#06111f] text-white">
      <header className="border-b border-[#1e3a5f] bg-[#06111f]/95">
        <div className="mx-auto flex min-h-20 max-w-7xl items-center justify-between gap-4 px-4 py-4 sm:px-6 lg:px-8">
          <div>
            <p className="text-[10px] uppercase tracking-[0.25em] text-[#f4b400] sm:text-xs">
              PilotVault SA
            </p>
            <h1 className="mt-1 text-base font-bold sm:text-lg">
              Upgrade Access
            </h1>
          </div>

          <Link
            href="/dashboard"
            className="rounded-xl border border-[#1e3a5f] px-3 py-2 text-xs text-gray-300 transition hover:border-[#f4b400] hover:text-[#f4b400] sm:px-4 sm:py-3 sm:text-sm"
          >
            Dashboard
          </Link>
        </div>
      </header>

      <section className="mx-auto max-w-7xl px-4 py-10 sm:px-6 sm:py-12 lg:px-8">
        <div className="mx-auto max-w-3xl text-center">
          <p className="text-[10px] uppercase tracking-[0.3em] text-[#f4b400] sm:text-xs">
            Continue your preparation
          </p>

          <h2 className="mt-4 text-3xl font-bold leading-tight sm:text-5xl">
            Unlock the full PilotVault experience.
          </h2>

          <p className="mt-5 text-sm leading-7 text-gray-400 sm:text-lg sm:leading-8">
            Your trial gives you a limited 25-question mock exam set. Upgrade to
            unlock the full SACAA question bank, topic-based practice, mock
            exams, explanations, and progress tracking.
          </p>
        </div>

        <div className="mt-10 grid gap-6 sm:mt-14 lg:grid-cols-3">
          {plans.map((plan) => (
            <div
              key={plan.name}
              className={`relative rounded-3xl border bg-[#081726] p-6 sm:p-8 ${
                plan.badge === "MOST POPULAR"
                  ? "border-[#f4b400]"
                  : "border-[#1e3a5f]"
              }`}
            >
              {plan.badge && (
                <div className="absolute -top-3 left-1/2 -translate-x-1/2 rounded-full border border-[#f4b400] bg-[#f4b400] px-4 py-1 text-[10px] font-bold text-[#06111f] sm:-top-4 sm:px-5 sm:text-xs">
                  {plan.badge}
                </div>
              )}

              <div className="text-center">
                <h3 className="text-xl font-bold sm:text-2xl">{plan.name}</h3>

                <p className="mt-3 min-h-0 text-sm leading-6 text-gray-400 sm:min-h-12">
                  {plan.description}
                </p>

                <div className="mt-5 sm:mt-6">
                  {plan.disabled ? (
                    <p className="text-2xl font-bold text-gray-300 sm:text-3xl">
                      {plan.price}
                    </p>
                  ) : (
                    <p>
                      <span className="text-4xl font-bold sm:text-5xl">
                        {plan.price}
                      </span>
                      <span className="text-sm text-gray-400 sm:text-base">
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
                    <span className="flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-[#f4b400]/20">
                      <Check className="h-3.5 w-3.5 text-[#f4b400]" />
                    </span>
                    <p className="text-sm text-gray-200">{feature}</p>
                  </div>
                ))}
              </div>

              {plan.disabled ? (
                <button
                  disabled
                  className="mt-7 w-full rounded-xl bg-gray-700/50 px-5 py-3 text-sm font-bold text-gray-400 sm:mt-8"
                >
                  Coming Soon
                </button>
              ) : (
                <button className="mt-7 w-full rounded-xl bg-[#f4b400] px-5 py-3 text-sm font-bold text-[#06111f] transition hover:bg-[#d9a000] sm:mt-8">
                  Upgrade Now
                </button>
              )}
            </div>
          ))}
        </div>

        <div className="mt-10 rounded-3xl border border-[#1e3a5f] bg-[#081726] p-5 text-center sm:mt-12 sm:p-8">
          <p className="text-sm leading-6 text-gray-400">
            After upgrading, your account will unlock topic-based practice,
            expanded mock exams, and full access to the PilotVault question
            bank.
          </p>
        </div>
      </section>
    </main>
  )
}