"use client"

import { motion } from "framer-motion"
import { Button } from "@/components/ui/button"
import { Check } from "lucide-react"
import Image from "next/image"

const features = [
  "SACAA Focused",
  "Real Exam Experience",
  "Up-to-date Questions",
  "Detailed Explanations",
]

export function HeroSection() {
  const openSignupModal = () => {
    window.dispatchEvent(new Event("open-signup-modal"))
  }

  return (
    <section className="relative overflow-hidden bg-[#06111f] pt-24 sm:pt-28 lg:min-h-screen lg:pt-28">
      <div className="relative z-10 mx-auto max-w-7xl px-4 py-10 sm:px-6 sm:py-14 lg:px-8 lg:py-20">
        <div className="grid grid-cols-1 items-center gap-10 lg:grid-cols-2 lg:gap-16">
          <motion.div
            initial={{ opacity: 0, x: -35 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6 }}
            className="space-y-7 text-center lg:text-left"
          >
            <div className="space-y-4">
              <h1 className="mx-auto max-w-4xl text-4xl font-bold leading-[1.05] tracking-tight text-white sm:text-5xl lg:mx-0 lg:text-6xl">
                PASS YOUR SACAA EXAMS WITH{" "}
                <span className="text-[#f4b400]">CONFIDENCE.</span>
              </h1>

              <p className="mx-auto max-w-xl text-base leading-relaxed text-gray-300 sm:text-lg lg:mx-0">
                PilotVault SA is the most trusted exam preparation platform for
                student pilots in South Africa.
              </p>
            </div>

            <div className="mx-auto grid max-w-md grid-cols-1 gap-3 sm:grid-cols-2 lg:mx-0">
              {features.map((feature, index) => (
                <motion.div
                  key={feature}
                  initial={{ opacity: 0, y: 18 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.4, delay: 0.2 + index * 0.1 }}
                  className="flex items-center justify-center gap-2 rounded-xl border border-[#1e3a5f]/70 bg-white/[0.03] px-3 py-3 sm:justify-start"
                >
                  <div className="flex h-5 w-5 flex-shrink-0 items-center justify-center rounded-full bg-[#f4b400]">
                    <Check className="h-3 w-3 text-[#06111f]" />
                  </div>

                  <span className="text-sm font-medium text-gray-200">
                    {feature}
                  </span>
                </motion.div>
              ))}
            </div>

            <motion.div
              initial={{ opacity: 0, y: 18 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.4, delay: 0.6 }}
              className="flex flex-col items-center gap-4 sm:flex-row sm:justify-center lg:justify-start"
            >
              <Button
                type="button"
                size="lg"
                onClick={openSignupModal}
                className="w-full bg-[#f4b400] px-8 py-6 text-base font-semibold text-[#06111f] hover:bg-[#d9a000] sm:w-auto sm:text-lg"
              >
                Start Free Trial
              </Button>
            </motion.div>

            <p className="text-sm text-gray-400">
              3-day free trial • Cancel anytime
            </p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, x: 35 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 0.3 }}
            className="relative mx-auto w-full max-w-xl lg:max-w-none"
          >
            <div className="relative aspect-[4/3] overflow-hidden rounded-2xl border border-[#1e3a5f]/70 shadow-2xl">
              <Image
                src="/images/hero-cockpit.jpg"
                alt="Cessna aircraft on apron at sunset"
                fill
                className="object-cover"
                priority
              />

              <div className="absolute inset-0 bg-gradient-to-t from-[#06111f]/70 via-transparent to-transparent" />
              <div className="absolute inset-0 bg-gradient-to-r from-[#06111f]/35 to-transparent" />
            </div>
          </motion.div>
        </div>
      </div>

      <div className="pointer-events-none absolute left-[-120px] top-1/3 h-72 w-72 rounded-full bg-[#f4b400]/5 blur-3xl sm:h-96 sm:w-96" />
      <div className="pointer-events-none absolute bottom-[-120px] right-[-120px] h-72 w-72 rounded-full bg-[#1e3a5f]/30 blur-3xl sm:h-96 sm:w-96" />
    </section>
  )
}