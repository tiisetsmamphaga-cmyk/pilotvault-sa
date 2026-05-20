"use client"

import { motion } from "framer-motion"
import { Button } from "@/components/ui/button"
import Image from "next/image"

export function CtaSection() {
  const openSignupModal = () => {
    window.dispatchEvent(new Event("open-signup-modal"))
  }

  return (
    <section className="relative overflow-hidden py-16 sm:py-24 lg:py-32">

      {/* Background */}

      <div className="absolute inset-0">
        <Image
          src="/images/runway.jpg"
          alt="Airport runway"
          fill
          className="object-cover"
        />

        <div className="absolute inset-0 bg-[#06111f]/85" />
      </div>

      <div className="relative mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">

        <motion.div
          initial={{ opacity: 0, y: 25 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="mx-auto max-w-4xl text-center"
        >

          <h2 className="mb-6 text-3xl font-bold leading-tight text-white sm:text-4xl lg:text-5xl">
            JOIN{" "}
            <span className="text-[#f4b400]">
              PILOTVAULT SA
            </span>{" "}
            TODAY
          </h2>

          <p className="mx-auto mb-8 max-w-2xl text-base leading-relaxed text-gray-300 sm:text-lg lg:text-xl">
            Thousands of student pilots are preparing smarter.
            Start your journey toward SACAA exam success.
          </p>

          <Button
            size="lg"
            onClick={openSignupModal}
            className="w-full bg-[#f4b400] px-8 py-6 text-base font-semibold text-[#06111f] hover:bg-[#d9a000] sm:w-auto sm:px-10 sm:text-lg"
          >
            Start Your Free Trial
          </Button>

          <p className="mt-5 text-sm text-gray-400">
            No credit card required • 3-day free trial
          </p>

        </motion.div>

      </div>

      <div className="pointer-events-none absolute left-[-120px] top-1/2 h-72 w-72 rounded-full bg-[#f4b400]/5 blur-3xl" />

      <div className="pointer-events-none absolute bottom-[-120px] right-[-120px] h-72 w-72 rounded-full bg-[#1e3a5f]/20 blur-3xl" />

    </section>
  )
}