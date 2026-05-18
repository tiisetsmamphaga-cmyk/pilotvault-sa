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
  },
  {
    name: "CPL Pack",
    price: "R449",
    period: "/month",
    description: "Ideal for Commercial Pilot License students",
    features: [
      "5000+ Questions",
      "All CPL Subjects",
      "Mock Exams",
      "Performance Tracking",
      "Mobile Access",
      "Priority Support",
    ],
    popular: true,
  },
  {
    name: "All Access",
    price: "R699",
    period: "/month",
    description: "Complete access to everything",
    features: [
      "5000+ Questions",
      "All 8 Subjects",
      "Unlimited Mock Exams",
      "Advanced Analytics",
      "Mobile Access",
      "24/7 Support",
    ],
    popular: false,
  },
]

export function PricingSection() {
  return (
    <section id="pricing" className="py-20 lg:py-24 bg-[#06111f]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          className="text-center mb-12"
        >
          <h2 className="text-3xl sm:text-4xl font-bold text-white mb-4 text-balance">
            Simple, Transparent <span className="text-[#f4b400]">Pricing</span>
          </h2>
          <p className="text-gray-400 max-w-2xl mx-auto">
            Choose the plan that fits your training goals. All plans include a 7-day free trial.
          </p>
        </motion.div>

        <div className="grid md:grid-cols-3 gap-6 lg:gap-8">
          {plans.map((plan, index) => (
            <motion.div
              key={plan.name}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.4, delay: index * 0.1 }}
              className={`relative bg-[#0b1f35] rounded-2xl p-6 lg:p-8 border ${
                plan.popular
                  ? "border-[#f4b400] shadow-lg shadow-[#f4b400]/10"
                  : "border-[#1e3a5f]"
              }`}
            >
              {plan.popular && (
                <div className="absolute -top-3 left-1/2 -translate-x-1/2 bg-[#f4b400] text-[#06111f] px-4 py-1 rounded-full text-xs font-bold">
                  MOST POPULAR
                </div>
              )}

              <div className="text-center mb-6">
                <h3 className="text-xl font-bold text-white mb-2">{plan.name}</h3>
                <p className="text-gray-400 text-sm mb-4">{plan.description}</p>
                <div className="flex items-baseline justify-center gap-1">
                  <span className="text-4xl font-bold text-white">{plan.price}</span>
                  <span className="text-gray-400">{plan.period}</span>
                </div>
              </div>

              <ul className="space-y-3 mb-8">
                {plan.features.map((feature) => (
                  <li key={feature} className="flex items-center gap-3">
                    <div className="flex-shrink-0 w-5 h-5 rounded-full bg-[#f4b400]/20 flex items-center justify-center">
                      <Check className="w-3 h-3 text-[#f4b400]" />
                    </div>
                    <span className="text-gray-300 text-sm">{feature}</span>
                  </li>
                ))}
              </ul>

              <Button
                className={`w-full ${
                  plan.popular
                    ? "bg-[#f4b400] text-[#06111f] hover:bg-[#d9a000]"
                    : "bg-[#1e3a5f] text-white hover:bg-[#2a4a6f]"
                } font-semibold`}
              >
                Start Free Trial
              </Button>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  )
}
