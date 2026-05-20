"use client"

import { motion } from "framer-motion"
import { Brain, BarChart3, BookOpen, Monitor, Smartphone } from "lucide-react"

const features = [
  {
    icon: Brain,
    title: "Smart Practice",
    description: "AI-powered question selection based on your weak areas",
  },
  {
    icon: BarChart3,
    title: "Performance Tracking",
    description: "Detailed analytics to monitor your progress over time",
  },
  {
    icon: BookOpen,
    title: "Detailed Explanations",
    description: "Comprehensive explanations for every question",
  },
  {
    icon: Monitor,
    title: "Exam Simulation",
    description: "Full mock exams that mirror the real SACAA experience",
  },
  {
    icon: Smartphone,
    title: "Mobile Friendly",
    description: "Study anywhere with our responsive mobile interface",
  },
]

export function FeaturesSection() {
  return (
    <section id="features" className="bg-[#06111f] py-16 sm:py-20 lg:py-24">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 18 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          className="mx-auto mb-10 max-w-3xl text-center sm:mb-12"
        >
          <h2 className="mb-4 text-3xl font-bold leading-tight text-white sm:text-4xl">
            Everything You Need to{" "}
            <span className="text-[#f4b400]">Succeed</span>
          </h2>

          <p className="mx-auto max-w-2xl text-base leading-relaxed text-gray-400 sm:text-lg">
            Our platform is designed with one goal in mind: helping you pass
            your SACAA exams on the first attempt.
          </p>
        </motion.div>

        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-5 lg:gap-6">
          {features.map((feature, index) => (
            <motion.div
              key={feature.title}
              initial={{ opacity: 0, y: 24 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.4, delay: index * 0.08 }}
              className="group rounded-2xl border border-[#1e3a5f] bg-[#0b1f35] p-5 transition-all hover:border-[#f4b400]/50 sm:p-6"
            >
              <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-xl bg-[#f4b400]/10 transition-colors group-hover:bg-[#f4b400]/20">
                <feature.icon className="h-6 w-6 text-[#f4b400]" />
              </div>

              <h3 className="mb-2 text-base font-semibold text-white">
                {feature.title}
              </h3>

              <p className="text-sm leading-relaxed text-gray-400">
                {feature.description}
              </p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  )
}