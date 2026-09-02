"use client"

import { motion } from "framer-motion"
import { Button } from "@/components/ui/button"
import Image from "next/image"

export function CtaSection() {
  const openSignupModal = () => {
    window.dispatchEvent(new Event("open-signup-modal"))
  }

  return (
    <section className="relative overflow-hidden py-16 sm:py-24 lg:py-28">
      <div className="absolute inset-0">
        <Image src="/images/runway.jpg" alt="Airport runway" fill className="object-cover" />
        <div className="absolute inset-0 bg-[#06111f]/92" />
      </div>

      <div className="relative mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 25 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="mx-auto max-w-4xl text-center"
        >
          <p className="mb-3 text-xs font-bold uppercase tracking-[0.2em] text-blue-100">Your next exam starts here</p>

          <h2 className="mb-6 text-3xl font-bold leading-tight text-white sm:text-4xl lg:text-5xl">
            PASS YOUR NEXT SACAA EXAM WITH CONFIDENCE.
          </h2>

          <p className="mx-auto mb-8 max-w-2xl text-base leading-relaxed text-blue-50/90 sm:text-lg lg:text-xl">
            Practice realistically, understand every answer and track exactly where you need to improve.
          </p>

          <Button
            size="lg"
            onClick={openSignupModal}
            className="w-full bg-white px-8 py-6 text-base font-semibold text-[#1f4e79] shadow-sm hover:bg-[#f1f5f9] sm:w-auto sm:px-10 sm:text-lg"
          >
            Start Your Free Trial
          </Button>

          <p className="mt-5 text-sm text-blue-100">No credit card required • 3-day free trial</p>
        </motion.div>
      </div>
    </section>
  )
}
