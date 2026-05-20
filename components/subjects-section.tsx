"use client"

import { motion } from "framer-motion"
import {
  Scale,
  Cloud,
  Compass,
  Brain,
  Plane,
  Wrench,
  Radio,
  Map,
} from "lucide-react"

const subjects = [
  { icon: Scale, name: "Air Law", questions: "600+" },
  { icon: Cloud, name: "Meteorology", questions: "750+" },
  { icon: Compass, name: "Navigation", questions: "800+" },
  { icon: Brain, name: "Human Performance", questions: "500+" },
  { icon: Plane, name: "Principles of Flight", questions: "650+" },
  { icon: Wrench, name: "Aircraft General", questions: "700+" },
  { icon: Radio, name: "Radio Telephony", questions: "400+" },
  { icon: Map, name: "Flight Planning", questions: "600+" },
]

export function SubjectsSection() {
  return (
    <section
      id="subjects"
      className="bg-white py-16 sm:py-20 lg:py-24"
    >
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">

        <motion.div
          initial={{ opacity: 0, y: 18 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          className="mx-auto mb-10 max-w-3xl text-center sm:mb-12"
        >
          <h2 className="mb-4 text-3xl font-bold text-[#06111f] sm:text-4xl">
            Everything You Need to Pass
          </h2>

          <p className="mx-auto max-w-2xl text-base leading-relaxed text-gray-600 sm:text-lg">
            Comprehensive coverage of all 8 SACAA subjects with
            thousands of practice questions.
          </p>
        </motion.div>

        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4 lg:gap-6">

          {subjects.map((subject, index) => (
            <motion.div
              key={subject.name}
              initial={{ opacity: 0, scale: 0.96 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true }}
              transition={{
                duration: 0.35,
                delay: index * 0.05,
              }}
              className="group cursor-pointer rounded-2xl border border-gray-100 bg-gray-50 p-5 transition-all hover:border-[#f4b400] hover:shadow-xl sm:p-6"
            >
              <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-xl bg-[#06111f] transition-colors group-hover:bg-[#f4b400]">
                <subject.icon className="h-6 w-6 text-white transition-colors group-hover:text-[#06111f]" />
              </div>

              <h3 className="mb-2 text-base font-semibold text-[#06111f]">
                {subject.name}
              </h3>

              <p className="text-sm text-gray-500">
                {subject.questions} questions
              </p>
            </motion.div>
          ))}

        </div>
      </div>
    </section>
  )
}