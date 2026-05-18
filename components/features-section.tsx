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
    <section id="features" className="py-20 lg:py-24 bg-[#06111f]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          className="text-center mb-12"
        >
          <h2 className="text-3xl sm:text-4xl font-bold text-white mb-4 text-balance">
            Everything You Need to <span className="text-[#f4b400]">Succeed</span>
          </h2>
          <p className="text-gray-400 max-w-2xl mx-auto">
            Our platform is designed with one goal in mind: helping you pass your SACAA exams on the first attempt.
          </p>
        </motion.div>

        <div className="grid grid-cols-2 lg:grid-cols-5 gap-4 lg:gap-6">
          {features.map((feature, index) => (
            <motion.div
              key={feature.title}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.4, delay: index * 0.1 }}
              className="bg-[#0b1f35] rounded-xl p-6 border border-[#1e3a5f] hover:border-[#f4b400]/50 transition-all group"
            >
              <div className="w-12 h-12 rounded-xl bg-[#f4b400]/10 flex items-center justify-center mb-4 group-hover:bg-[#f4b400]/20 transition-colors">
                <feature.icon className="w-6 h-6 text-[#f4b400]" />
              </div>
              <h3 className="text-white font-semibold mb-2">{feature.title}</h3>
              <p className="text-gray-400 text-sm leading-relaxed">{feature.description}</p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  )
}
