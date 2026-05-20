"use client"

import { motion } from "framer-motion"
import { Button } from "@/components/ui/button"
import { ArrowRight, Clock, Check } from "lucide-react"

export function ExamPreviewSection() {
  return (
    <section className="bg-[#0b1f35] py-16 sm:py-20 lg:py-32">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 items-center gap-10 lg:grid-cols-2 lg:gap-16">

          {/* Exam Card */}

          <motion.div
            initial={{ opacity: 0, x: -35 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            className="rounded-2xl border border-[#1e3a5f] bg-[#06111f] p-5 shadow-2xl sm:p-6 lg:p-8"
          >
            <div className="mb-6 flex items-center justify-between">
              <div>
                <h3 className="text-lg font-bold text-white sm:text-xl">
                  Meteorology
                </h3>

                <p className="text-sm text-gray-400">
                  Question 12 of 25
                </p>
              </div>

              <div className="flex items-center gap-2 rounded-lg bg-[#1e3a5f] px-3 py-2">
                <Clock className="h-4 w-4 text-[#f4b400]" />
                <span className="font-mono text-sm text-white">
                  08:42
                </span>
              </div>
            </div>

            <div className="mb-8 h-2 rounded-full bg-[#1e3a5f]">
              <div className="h-full w-[48%] rounded-full bg-[#f4b400]" />
            </div>

            <div className="mb-6">
              <p className="text-base leading-relaxed text-white sm:text-lg">
                Which of the following is the most characteristic of a stable atmosphere?
              </p>
            </div>

            <div className="mb-6 space-y-3">
              {[
                {
                  label: "A",
                  text: "Cumulus clouds and good visibility",
                  correct: false,
                },
                {
                  label: "B",
                  text: "Stratiform clouds and restricted visibility",
                  correct: true,
                },
                {
                  label: "C",
                  text: "Thunderstorms and heavy precipitation",
                  correct: false,
                },
                {
                  label: "D",
                  text: "Strong surface winds and clear skies",
                  correct: false,
                },
              ].map((option) => (
                <div
                  key={option.label}
                  className={`flex cursor-pointer items-start gap-3 rounded-xl border p-4 transition-all ${
                    option.correct
                      ? "border-green-500 bg-green-500/10"
                      : "border-[#1e3a5f] bg-[#1e3a5f]/30 hover:border-[#f4b400]/50"
                  }`}
                >
                  <div
                    className={`flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full font-semibold ${
                      option.correct
                        ? "bg-green-500 text-white"
                        : "bg-[#1e3a5f] text-gray-300"
                    }`}
                  >
                    {option.correct ? (
                      <Check className="h-4 w-4" />
                    ) : (
                      option.label
                    )}
                  </div>

                  <span
                    className={`text-sm sm:text-base ${
                      option.correct
                        ? "text-green-400"
                        : "text-gray-300"
                    }`}
                  >
                    {option.text}
                  </span>
                </div>
              ))}
            </div>

            <button className="flex items-center gap-2 font-medium text-[#f4b400] transition-colors hover:text-[#d9a000]">
              View Explanation
              <ArrowRight className="h-4 w-4" />
            </button>
          </motion.div>

          {/* Right Content */}

          <motion.div
            initial={{ opacity: 0, x: 35 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            className="space-y-8 text-center lg:text-left"
          >
            <div className="space-y-4">
              <h2 className="text-3xl font-bold leading-tight text-white sm:text-4xl lg:text-5xl">
                Real Questions.
                <br />
                Real Explanations.
                <br />
                <span className="text-[#f4b400]">
                  Real Results.
                </span>
              </h2>

              <p className="mx-auto max-w-md text-base leading-relaxed text-gray-300 sm:text-lg lg:mx-0">
                Practice with questions that mirror the actual SACAA exams.
                Get detailed explanations for every answer.
              </p>
            </div>

            <div className="grid grid-cols-3 gap-3 sm:gap-6">
              {[
                { value: "5000+", label: "Questions" },
                { value: "8", label: "Subjects" },
                { value: "98%", label: "Pass Rate" },
              ].map((stat, index) => (
                <motion.div
                  key={stat.label}
                  initial={{ opacity: 0, y: 15 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{
                    duration: 0.4,
                    delay: 0.3 + index * 0.1,
                  }}
                  className="rounded-xl border border-[#1e3a5f]/40 bg-white/[0.02] p-4"
                >
                  <p className="text-2xl font-bold text-[#f4b400] sm:text-3xl">
                    {stat.value}
                  </p>

                  <p className="mt-1 text-xs text-gray-400 sm:text-sm">
                    {stat.label}
                  </p>
                </motion.div>
              ))}
            </div>

            <Button
              size="lg"
              className="w-full bg-[#f4b400] font-semibold text-[#06111f] hover:bg-[#d9a000] sm:w-auto"
            >
              Explore Features
              <ArrowRight className="ml-2 h-5 w-5" />
            </Button>
          </motion.div>

        </div>
      </div>
    </section>
  )
}