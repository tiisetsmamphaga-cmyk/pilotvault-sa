"use client"

import { motion } from "framer-motion"
import { Button } from "@/components/ui/button"
import { Check } from "lucide-react"

const plans = [
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
    popular: false,
    comingSoon: false,
  },
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
  return (
    <section
      id="pricing"
      className="bg-[#06111f] py-16 sm:py-20 lg:py-24"
    >
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 18 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          className="mx-auto mb-10 max-w-3xl text-center sm:mb-12"
        >
          <h2 className="mb-4 text-3xl font-bold text-white sm:text-4xl">
            Simple, Transparent{" "}
            <span className="text-[#f4b400]">Pricing</span>
          </h2>

          <p className="mx-auto max-w-2xl text-base leading-relaxed text-gray-400 sm:text-lg">
            Choose the plan that fits your training goals. Available plans
            include a 3-day free trial.
          </p>
        </motion.div>

        <div className="grid grid-cols-1 gap-6 lg:grid-cols-3 lg:gap-8">
          {plans.map((plan, index) => (
            <motion.div
              key={plan.name}
              initial={{ opacity: 0, y: 24 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{
                duration: 0.4,
                delay: index * 0.1,
              }}
              className={`relative rounded-2xl border p-6 lg:p-8 ${
                plan.popular
                  ? "border-[#f4b400] bg-[#0b1f35] shadow-lg shadow-[#f4b400]/10"
                  : plan.comingSoon
                    ? "border-[#1e3a5f]/70 bg-[#0b1f35]/70 opacity-90"
                    : "border-[#1e3a5f] bg-[#0b1f35]"
              }`}
            >
              {plan.popular && (
                <div className="absolute left-1/2 top-0 -translate-x-1/2 -translate-y-1/2 rounded-full bg-[#f4b400] px-4 py-1 text-xs font-bold text-[#06111f]">
                  MOST POPULAR
                </div>
              )}

              {plan.comingSoon && (
                <div className="absolute left-1/2 top-0 -translate-x-1/2 -translate-y-1/2 rounded-full border border-[#1e3a5f] bg-[#06111f] px-4 py-1 text-xs font-bold text-gray-300">
                  COMING SOON
                </div>
              )}

              <div className="mb-6 text-center">
                <h3 className="mb-2 text-xl font-bold text-white">
                  {plan.name}
                </h3>

                <p className="mb-4 text-sm text-gray-400">
                  {plan.description}
                </p>

                <div className="flex items-end justify-center gap-1">
                  <span
                    className={`font-bold ${
                      plan.comingSoon
                        ? "text-3xl text-gray-300"
                        : "text-4xl text-white"
                    }`}
                  >
                    {plan.price}
                  </span>

                  {plan.period && (
                    <span className="mb-1 text-gray-400">
                      {plan.period}
                    </span>
                  )}
                </div>
              </div>

              <ul className="mb-8 space-y-4">
                {plan.features.map((feature) => (
                  <li key={feature} className="flex items-center gap-3">
                    <div className="flex h-5 w-5 flex-shrink-0 items-center justify-center rounded-full bg-[#f4b400]/20">
                      <Check className="h-3 w-3 text-[#f4b400]" />
                    </div>

                    <span className="text-sm text-gray-300">
                      {feature}
                    </span>
                  </li>
                ))}
              </ul>

              <Button
                disabled={plan.comingSoon}
                className={`w-full font-semibold ${
                  plan.comingSoon
                    ? "cursor-not-allowed bg-gray-700 text-gray-400 hover:bg-gray-700"
                    : plan.popular
                      ? "bg-[#f4b400] text-[#06111f] hover:bg-[#d9a000]"
                      : "bg-[#1e3a5f] text-white hover:bg-[#2a4a6f]"
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
