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
    <section className="relative min-h-screen pt-20 lg:pt-24 overflow-hidden bg-[#06111f]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 lg:py-20">
        <div className="grid lg:grid-cols-2 gap-12 lg:gap-16 items-center">
          <motion.div
            initial={{ opacity: 0, x: -50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6 }}
            className="space-y-8"
          >
            <div className="space-y-4">
              <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold leading-tight text-white text-balance">
                PASS YOUR SACAA EXAMS WITH{" "}
                <span className="text-[#f4b400]">CONFIDENCE.</span>
              </h1>
              <p className="text-lg text-gray-300 max-w-lg leading-relaxed">
                PilotVault SA is the most trusted exam preparation platform for student pilots in South Africa.
              </p>
            </div>

            <div className="grid grid-cols-2 gap-4">
              {features.map((feature, index) => (
                <motion.div
                  key={feature}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.4, delay: 0.2 + index * 0.1 }}
                  className="flex items-center gap-2"
                >
                  <div className="flex-shrink-0 w-5 h-5 rounded-full bg-[#f4b400] flex items-center justify-center">
                    <Check className="w-3 h-3 text-[#06111f]" />
                  </div>
                  <span className="text-gray-200 text-sm font-medium">{feature}</span>
                </motion.div>
              ))}
            </div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.4, delay: 0.6 }}
              className="flex flex-col sm:flex-row gap-4"
            >
              <Button
                type="button"
                size="lg"
                onClick={openSignupModal}
                className="bg-[#f4b400] text-[#06111f] hover:bg-[#d9a000] font-semibold px-8 py-6 text-lg"
              >
                Start Free Trial
              </Button>

             
            </motion.div>

            <p className="text-sm text-gray-400">
              3-day free trial • Cancel anytime
            </p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, x: 50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 0.3 }}
            className="relative"
          >
            <div className="relative aspect-[4/3] rounded-2xl overflow-hidden shadow-2xl">
              <Image
                src="/images/hero-cockpit.jpg"
                alt="Cessna aircraft on apron at sunset"
                fill
                className="object-cover"
                priority
              />
              <div className="absolute inset-0 bg-gradient-to-t from-[#06111f]/60 via-transparent to-transparent" />
              <div className="absolute inset-0 bg-gradient-to-r from-[#06111f]/30 to-transparent" />
            </div>

            
          </motion.div>
        </div>
      </div>

      <div className="absolute top-1/2 left-0 w-96 h-96 bg-[#f4b400]/5 rounded-full blur-3xl -translate-y-1/2 pointer-events-none" />
      <div className="absolute bottom-0 right-0 w-96 h-96 bg-[#1e3a5f]/30 rounded-full blur-3xl pointer-events-none" />
    </section>
  )
}
