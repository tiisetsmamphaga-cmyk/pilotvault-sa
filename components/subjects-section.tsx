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
  Map 
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
    <section id="subjects" className="py-20 lg:py-24 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          className="text-center mb-12"
        >
          <h2 className="text-3xl sm:text-4xl font-bold text-[#06111f] mb-4 text-balance">
            Everything You Need to Pass
          </h2>
          <p className="text-gray-600 max-w-2xl mx-auto">
            Comprehensive coverage of all 8 SACAA subjects with thousands of practice questions.
          </p>
        </motion.div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 lg:gap-6">
          {subjects.map((subject, index) => (
            <motion.div
              key={subject.name}
              initial={{ opacity: 0, scale: 0.95 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true }}
              transition={{ duration: 0.4, delay: index * 0.05 }}
              className="bg-gray-50 rounded-xl p-6 border border-gray-100 hover:border-[#f4b400] hover:shadow-lg transition-all cursor-pointer group"
            >
              <div className="w-12 h-12 rounded-xl bg-[#06111f] flex items-center justify-center mb-4 group-hover:bg-[#f4b400] transition-colors">
                <subject.icon className="w-6 h-6 text-white group-hover:text-[#06111f] transition-colors" />
              </div>
              <h3 className="text-[#06111f] font-semibold mb-1">{subject.name}</h3>
              <p className="text-gray-500 text-sm">{subject.questions} questions</p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  )
}
