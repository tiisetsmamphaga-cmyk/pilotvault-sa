"use client"

import { motion } from "framer-motion"
import { Button } from "@/components/ui/button"
import Image from "next/image"

export function CtaSection() {
  return (
    <section className="relative py-24 lg:py-32 overflow-hidden">
      {/* Background Image */}
      <div className="absolute inset-0">
        <Image
          src="/images/runway.jpg"
          alt="Airport runway"
          fill
          className="object-cover"
        />
        <div className="absolute inset-0 bg-[#06111f]/85" />
      </div>

      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center"
        >
          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold text-white mb-6 text-balance">
            JOIN <span className="text-[#f4b400]">PILOTVAULT SA</span> TODAY
          </h2>
          <p className="text-xl text-gray-300 mb-8 max-w-2xl mx-auto">
            Thousands of pilots are already preparing smarter. Start your journey to success.
          </p>
          <Button
            size="lg"
            className="bg-[#f4b400] text-[#06111f] hover:bg-[#d9a000] font-semibold px-10 py-6 text-lg"
          >
            Start Your Free Trial
          </Button>
          <p className="mt-4 text-gray-400 text-sm">
            No credit card required • 7-day free trial
          </p>
        </motion.div>
      </div>
    </section>
  )
}
