"use client"

import { motion } from "framer-motion"
import { Button } from "@/components/ui/button"

const plans = [
  {
    name: "Per Subject",
    price: "R89",
    period: "/month",
    description: "Focus on the one exam you're writing next",
    features: [
      "Full question bank for one subject",
      "Timed mock exams",
      "Topic-based practice",
      "Detailed answer explanations",
      "Track your mock exam scores",
      "Study on phone, tablet or laptop",
      "Email support",
    ],
    popular: false,
    comingSoon: false,
  },
  {
    name: "PPL Pack",
    price: "R699",
    period: "/3 months",
    description: "Everything you need for all 8 PPL exams",
    features: [
      "All 8 PPL subjects, full question banks",
      "Timed mock exams for every subject",
      "Topic-based practice",
      "Detailed answer explanations",
      "Track your mock exam scores",
      "Study on phone, tablet or laptop",
      "Email support",
    ],
    popular: true,
    comingSoon: false,
  },
  {
    name: "CPL Pack",
    price: "Coming Soon",
    period: "",
    description: "CPL content is being expanded. Full pack launches 1 January 2027",
    features: [
      "CPL question bank",
      "Timed mock exams",
      "Topic-based practice",
      "Detailed answer explanations",
      "Study on phone, tablet or laptop",
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
    <section id="pricing" className="border-y border-[#d7e1ea] bg-[#e5edf5] py-16 sm:py-20 lg:py-24">
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
              className={`relative rounded-2xl border bg-white p-6 shadow-[0_12px_32px_rgba(15,23,42,0.07)] transition-all hover:-translate-y-1 hover:shadow-[0_18px_42px_rgba(15,23,42,0.10)] lg:p-8 ${
                plan.popular
                  ? "border-[#1f4e79] ring-1 ring-[#1f4e79]/10 lg:-mt-4"
                  : plan.comingSoon
                    ? "border-slate-200 opacity-90"
                    : "border-slate-200"
              }`}
            >
              {plan.popular && (
                <div className="absolute left-1/2 top-0 -translate-x-1/2 -translate-y-1/2 rounded-full bg-[var(--pv-gold)] px-4 py-1 text-xs font-bold uppercase tracking-wide text-slate-900 shadow-sm">
                  Most students choose this
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

              <ul className="mb-8 space-y-3.5">
                {plan.features.map((feature) => (
                  <li key={feature} className="flex items-baseline gap-2.5">
                    <span className="text-sm font-bold leading-none text-[#b8860a]">
                      &#10003;
                    </span>
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
                {plan.comingSoon ? "Available 1 Jan 2027" : "Start Free Trial"}
              </Button>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  )
}
