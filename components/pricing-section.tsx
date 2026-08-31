"use client"

import { motion } from "framer-motion"
import { Button } from "@/components/ui/button"
import { Check } from "lucide-react"

const plans = [
  {
    name: "Per Subject",
    price: "R89",
    period: "/month",
    description: "Ideal for focused study",
    features: [
      "Single Subject Access",
      "Mock Exams",
      "Performance Tracking",
      "Mobile Access",
      "Question Explanations",
      "Priority Support",
    ],
    popular: false,
    comingSoon: false,
  },
  {
    name: "PPL Pack",
    price: "R699",
    period: "/3 Months",
    description: "Perfect for Private Pilot License students",
    features: [
      "PPL Subject Questions",
      "Mock Exams",
      "Performance Tracking",
      "Mobile Access",
      "Email Support",
    ],
    popular: true,
    comingSoon: false,
  },
  {
    name: "CPL Pack",
    price: "Coming Soon",
    period: "",
    description: "Commercial Pilot content currently being expanded",
    features: [
      "CPL Question Bank",
      "Mock Exams",
      "Advanced Analytics",
      "Mobile Access",
      "Priority Support",
      "New Content Updates",
    ],
    popular: false,
    comingSoon: true,
  },
]

export function PricingSection() {
  const openSignupModal = () => {
    window.dispatchEvent(new Event("open-signup-modal"))
  }

  return (
    <section id="pricing" className="border-y border-slate-200 bg-[#f8fafc] py-16 sm:py-20 lg:py-24">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 18 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          className="mx-auto mb-10 max-w-3xl text-center sm:mb-12"
        >
          <p className="mb-3 text-xs font-bold uppercase tracking-[0.2em] text-[#1f4e79]">Simple, transparent pricing</p>
          <h2 className="mb-4 text-3xl font-bold text-slate-900 sm:text-4xl">
            Choose the plan that fits your training
          </h2>
          <p className="mx-auto max-w-2xl text-base leading-relaxed text-slate-600 sm:text-lg">
            Focus on one subject or prepare across your licence. Available plans include a 3-day free trial.
          </p>
        </motion.div>

        <div className="grid grid-cols-1 gap-6 lg:grid-cols-3 lg:gap-8">
          {plans.map((plan, index) => (
            <motion.div
              key={plan.name}
              initial={{ opacity: 0, y: 24 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.4, delay: index * 0.1 }}
              className={`relative rounded-2xl border bg-white p-6 shadow-sm transition-shadow hover:shadow-md lg:p-8 ${
                plan.popular
                  ? "border-[#1f4e79] ring-1 ring-[#1f4e79]/10 lg:-mt-4"
                  : plan.comingSoon
                    ? "border-slate-200 opacity-90"
                    : "border-slate-200"
              }`}
            >
              {plan.popular && (
                <div className="absolute left-1/2 top-0 -translate-x-1/2 -translate-y-1/2 rounded-full bg-[#1f4e79] px-4 py-1 text-xs font-bold text-white shadow-sm">
                  MOST POPULAR
                </div>
              )}

              {plan.comingSoon && (
                <div className="absolute left-1/2 top-0 -translate-x-1/2 -translate-y-1/2 rounded-full border border-slate-300 bg-white px-4 py-1 text-xs font-bold text-slate-600">
                  COMING SOON
                </div>
              )}

              <div className="mb-6 text-center">
                <h3 className="mb-2 text-xl font-bold text-slate-900">{plan.name}</h3>
                <p className="mb-4 text-sm text-slate-500">{plan.description}</p>
                <div className="flex items-end justify-center gap-1">
                  <span className={`font-bold ${plan.comingSoon ? "text-3xl text-slate-500" : "text-4xl text-slate-900"}`}>
                    {plan.price}
                  </span>
                  {plan.period && <span className="mb-1 text-slate-500">{plan.period}</span>}
                </div>
              </div>

              <ul className="mb-8 space-y-4">
                {plan.features.map((feature) => (
                  <li key={feature} className="flex items-center gap-3">
                    <div className="flex h-5 w-5 flex-shrink-0 items-center justify-center rounded-full bg-[#d6e6f7]">
                      <Check className="h-3 w-3 text-[#1f4e79]" />
                    </div>
                    <span className="text-sm text-slate-700">{feature}</span>
                  </li>
                ))}
              </ul>

              <Button
                disabled={plan.comingSoon}
                type="button"
                onClick={plan.comingSoon ? undefined : openSignupModal}
                className={`w-full font-semibold ${
                  plan.comingSoon
                    ? "cursor-not-allowed bg-slate-200 text-slate-500 hover:bg-slate-200"
                    : plan.popular
                      ? "bg-[#1f4e79] text-white hover:bg-[#183d60]"
                      : "border border-[#1f4e79] bg-white text-[#1f4e79] hover:bg-[#f1f5f9]"
                }`}
              >
                {plan.comingSoon ? "Coming Soon" : "Start Free Trial"}
              </Button>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  )
}
