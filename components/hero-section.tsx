"use client"

import { motion } from "framer-motion"
import { Button } from "@/components/ui/button"
import { Check, BookOpen, BarChart3, ShieldCheck } from "lucide-react"
import Image from "next/image"

const features = [
  "SACAA Focused",
  "Real Exam Experience",
  "Up-to-date Questions",
  "Detailed Explanations",
]

const trustItems = [
  { icon: ShieldCheck, label: "SACAA-focused" },
  { icon: BookOpen, label: "Real explanations" },
  { icon: BarChart3, label: "Progress tracking" },
]

export function HeroSection() {
  const openSignupModal = () => {
    window.dispatchEvent(new Event("open-signup-modal"))
  }

  return (
    <section className="relative overflow-hidden bg-white pt-24 sm:pt-28 lg:pt-28">
      <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_75%_20%,rgba(214,230,247,0.7),transparent_32%)]" />

      <div className="relative z-10 mx-auto max-w-7xl px-4 py-12 sm:px-6 sm:py-16 lg:px-8 lg:py-20">
        <div className="grid grid-cols-1 items-center gap-10 lg:grid-cols-[1.02fr_0.98fr] lg:gap-14">
          <motion.div
            initial={{ opacity: 0, x: -30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6 }}
            className="space-y-7 text-center lg:text-left"
          >
            <div className="inline-flex items-center rounded-full border border-[#d6e6f7] bg-[#f8fafc] px-3 py-1.5 text-xs font-bold uppercase tracking-[0.18em] text-[#1f4e79]">
              Built by pilots. For pilots.
            </div>

            <div className="space-y-4">
              <h1 className="mx-auto max-w-4xl text-4xl font-bold leading-[1.03] tracking-tight text-slate-900 sm:text-5xl lg:mx-0 lg:text-6xl">
                PASS YOUR SACAA EXAMS WITH{" "}
                <span className="text-[#1f4e79]">CONFIDENCE.</span>
              </h1>

              <p className="mx-auto max-w-xl text-base font-semibold text-[#1f4e79] sm:text-lg lg:mx-0">
                Real Questions. Real Explanations. Real Results.
              </p>

              <p className="mx-auto max-w-xl text-base leading-relaxed text-slate-600 sm:text-lg lg:mx-0">
                Study smarter with realistic SACAA-style practice, mock exams,
                detailed explanations and progress tracking built for South
                African student pilots.
              </p>
            </div>

            <div className="mx-auto grid max-w-xl grid-cols-1 gap-3 sm:grid-cols-2 lg:mx-0">
              {features.map((feature, index) => (
                <motion.div
                  key={feature}
                  initial={{ opacity: 0, y: 16 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.4, delay: 0.15 + index * 0.08 }}
                  className="flex items-center justify-center gap-2 rounded-xl border border-slate-200 bg-[#f8fafc] px-3 py-3 shadow-sm sm:justify-start"
                >
                  <div className="flex h-5 w-5 flex-shrink-0 items-center justify-center rounded-full bg-[#d6e6f7]">
                    <Check className="h-3 w-3 text-[#1f4e79]" />
                  </div>
                  <span className="text-sm font-medium text-slate-700">{feature}</span>
                </motion.div>
              ))}
            </div>

            <motion.div
              initial={{ opacity: 0, y: 16 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.4, delay: 0.55 }}
              className="flex flex-col items-center gap-3 sm:flex-row sm:justify-center lg:justify-start"
            >
              <Button
                type="button"
                size="lg"
                onClick={openSignupModal}
                className="w-full bg-[#1f4e79] px-8 py-6 text-base font-semibold text-white shadow-sm hover:bg-[#183d60] sm:w-auto sm:text-lg"
              >
                Start Free Trial
              </Button>

              <Button
                type="button"
                size="lg"
                variant="outline"
                onClick={() => {
                  window.location.href = "/subjects"
                }}
                className="w-full border-[#1f4e79] bg-white px-8 py-6 text-base font-semibold text-[#1f4e79] hover:bg-[#f1f5f9] hover:text-[#183d60] sm:w-auto sm:text-lg"
              >
                Explore Subjects
              </Button>
            </motion.div>

            <p className="text-sm text-slate-500">3-day free trial • Cancel anytime</p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, x: 30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 0.25 }}
            className="relative mx-auto w-full max-w-xl lg:max-w-none"
          >
            <div className="relative aspect-[4/3] overflow-hidden rounded-3xl border border-slate-200 bg-slate-100 shadow-[0_24px_70px_rgba(15,23,42,0.14)]">
              <Image
                src="/images/hero-cockpit.jpg"
                alt="Cessna aircraft on apron"
                fill
                className="object-cover"
                priority
              />
              <div className="absolute inset-0 bg-gradient-to-t from-[#0f1720]/25 via-transparent to-transparent" />
            </div>

            <div className="relative -mt-5 mx-4 grid grid-cols-3 overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-xl sm:mx-8">
              {trustItems.map(({ icon: Icon, label }) => (
                <div key={label} className="flex flex-col items-center gap-2 border-r border-slate-200 px-2 py-4 text-center last:border-r-0 sm:px-4">
                  <Icon className="h-5 w-5 text-[#1f4e79]" />
                  <span className="text-[11px] font-semibold text-slate-700 sm:text-xs">{label}</span>
                </div>
              ))}
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  )
}
