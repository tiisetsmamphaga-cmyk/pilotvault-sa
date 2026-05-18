"use client"

import { motion } from "framer-motion"
import { Button } from "@/components/ui/button"
import { ArrowRight, Clock, Check } from "lucide-react"

export function ExamPreviewSection() {
  return (
    <section className="py-20 lg:py-32 bg-[#0b1f35]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid lg:grid-cols-2 gap-12 lg:gap-16 items-center">
          {/* Quiz Card */}
          <motion.div
            initial={{ opacity: 0, x: -50 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            className="bg-[#06111f] rounded-2xl p-6 lg:p-8 shadow-2xl border border-[#1e3a5f]"
          >
            {/* Quiz Header */}
            <div className="flex items-center justify-between mb-6">
              <div>
                <h3 className="text-xl font-bold text-white">Meteorology</h3>
                <p className="text-gray-400 text-sm">Question 12 of 25</p>
              </div>
              <div className="flex items-center gap-2 bg-[#1e3a5f] rounded-lg px-3 py-2">
                <Clock className="w-4 h-4 text-[#f4b400]" />
                <span className="text-white font-mono text-sm"></span>
              </div>
            </div>

            {/* Progress Bar */}
            <div className="h-2 bg-[#1e3a5f] rounded-full mb-8">
              <div className="h-full w-[48%] bg-[#f4b400] rounded-full" />
            </div>

            {/* Question */}
            <div className="mb-6">
              <p className="text-white text-lg leading-relaxed">
                Which of the following is the most characteristic of a stable atmosphere?
              </p>
            </div>

            {/* Options */}
            <div className="space-y-3 mb-6">
              {[
                { label: "A", text: "Cumulus clouds and good visibility", correct: false },
                { label: "B", text: "Stratiform clouds and restricted visibility", correct: true },
                { label: "C", text: "Thunderstorms and heavy precipitation", correct: false },
                { label: "D", text: "Strong surface winds and clear skies", correct: false },
              ].map((option) => (
                <div
                  key={option.label}
                  className={`flex items-center gap-4 p-4 rounded-xl border transition-all cursor-pointer ${
                    option.correct
                      ? "bg-green-500/10 border-green-500"
                      : "bg-[#1e3a5f]/30 border-[#1e3a5f] hover:border-[#f4b400]/50"
                  }`}
                >
                  <div
                    className={`w-8 h-8 rounded-full flex items-center justify-center font-semibold ${
                      option.correct
                        ? "bg-green-500 text-white"
                        : "bg-[#1e3a5f] text-gray-300"
                    }`}
                  >
                    {option.correct ? <Check className="w-4 h-4" /> : option.label}
                  </div>
                  <span className={option.correct ? "text-green-400" : "text-gray-300"}>
                    {option.text}
                  </span>
                </div>
              ))}
            </div>

            {/* View Explanation */}
            <button className="text-[#f4b400] hover:text-[#d9a000] font-medium flex items-center gap-2 transition-colors">
              View Explanation
              <ArrowRight className="w-4 h-4" />
            </button>
          </motion.div>

          {/* Right Content */}
          <motion.div
            initial={{ opacity: 0, x: 50 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="space-y-8"
          >
            <div className="space-y-4">
              <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold text-white leading-tight text-balance">
                Real Questions.
                <br />
                Real Explanations.
                <br />
                <span className="text-[#f4b400]">Real Results.</span>
              </h2>
              <p className="text-gray-300 text-lg max-w-md leading-relaxed">
                Practice with questions that mirror the actual SACAA exams. Get detailed explanations for every answer.
              </p>
            </div>

            {/* Stats */}
            <div className="grid grid-cols-3 gap-6">
              {[
                { value: "5000+", label: "Questions" },
                { value: "8", label: "Subjects" },
                { value: "98%", label: "Pass Rate" },
              ].map((stat, index) => (
                <motion.div
                  key={stat.label}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ duration: 0.4, delay: 0.4 + index * 0.1 }}
                  className="text-center"
                >
                  <p className="text-3xl lg:text-4xl font-bold text-[#f4b400]">{stat.value}</p>
                  <p className="text-gray-400 text-sm">{stat.label}</p>
                </motion.div>
              ))}
            </div>

            {/* CTA */}
            <Button
              size="lg"
              className="bg-[#f4b400] text-[#06111f] hover:bg-[#d9a000] font-semibold px-8"
            >
              Explore Features
              <ArrowRight className="w-5 h-5 ml-2" />
            </Button>
          </motion.div>
        </div>
      </div>
    </section>
  )
}
