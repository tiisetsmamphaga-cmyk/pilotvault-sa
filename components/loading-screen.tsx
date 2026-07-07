"use client"

import Image from "next/image"
import { motion } from "framer-motion"
import { Plane } from "lucide-react"
import { useEffect, useMemo, useState } from "react"

const loadingMessages = [
  "Loading SACAA Question Bank...",
  "Preparing Examination...",
  "Almost Ready...",
] as const

const particles = [
  { left: "12%", top: "24%", size: 3, delay: 0, duration: 7 },
  { left: "22%", top: "68%", size: 2, delay: 1.1, duration: 8 },
  { left: "34%", top: "18%", size: 2, delay: 0.4, duration: 6.8 },
  { left: "48%", top: "78%", size: 3, delay: 1.8, duration: 9 },
  { left: "63%", top: "28%", size: 2, delay: 0.8, duration: 7.6 },
  { left: "76%", top: "62%", size: 3, delay: 1.4, duration: 8.4 },
  { left: "88%", top: "36%", size: 2, delay: 0.2, duration: 7.2 },
  { left: "16%", top: "46%", size: 2, delay: 2.2, duration: 8.8 },
  { left: "58%", top: "12%", size: 3, delay: 1.7, duration: 7.8 },
  { left: "83%", top: "82%", size: 2, delay: 0.9, duration: 9.4 },
] as const

type LoadingScreenProps = {
  logoSrc?: string
  className?: string
}

export function LoadingScreen({
  logoSrc = "/images/logo.png",
  className = "",
}: LoadingScreenProps) {
  const [messageIndex, setMessageIndex] = useState(0)
  const [logoFailed, setLogoFailed] = useState(false)
  const activeMessage = loadingMessages[messageIndex]
  const radarRings = useMemo(() => [0, 1, 2], [])

  useEffect(() => {
    const messageTimer = window.setInterval(() => {
      setMessageIndex((current) => (current + 1) % loadingMessages.length)
    }, 1800)

    return () => window.clearInterval(messageTimer)
  }, [])

  return (
    <motion.main
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.45, ease: "easeOut" }}
      className={`fixed inset-0 z-[200] flex min-h-screen items-center justify-center overflow-hidden bg-[#06111f] px-6 text-white ${className}`}
      role="status"
      aria-busy="true"
      aria-live="polite"
      aria-label={activeMessage}
    >
      <div
        className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(30,58,95,0.5),rgba(6,17,31,0)_52%)]"
        aria-hidden="true"
      />
      <div
        className="absolute inset-0 bg-[linear-gradient(135deg,rgba(255,255,255,0.04),rgba(255,255,255,0)_34%,rgba(244,180,0,0.04))]"
        aria-hidden="true"
      />

      {particles.map((particle) => (
        <motion.span
          key={`${particle.left}-${particle.top}`}
          className="absolute rounded-full bg-[#f4b400]/60 shadow-[0_0_16px_rgba(244,180,0,0.55)]"
          style={{
            left: particle.left,
            top: particle.top,
            width: particle.size,
            height: particle.size,
          }}
          animate={{ y: [-10, 14, -10], opacity: [0.25, 0.75, 0.25] }}
          transition={{
            duration: particle.duration,
            delay: particle.delay,
            repeat: Infinity,
            ease: "easeInOut",
          }}
          aria-hidden="true"
        />
      ))}

      <section className="relative z-10 flex w-full max-w-md flex-col items-center text-center">
        <div className="relative flex h-56 w-56 items-center justify-center sm:h-64 sm:w-64">
          {radarRings.map((ring) => (
            <motion.div
              key={ring}
              className="absolute rounded-full border border-[#f4b400]/25"
              style={{ inset: `${ring * 18}px` }}
              animate={{
                opacity: [0.18, 0.5, 0.18],
                scale: [0.98, 1.02, 0.98],
              }}
              transition={{
                duration: 3.2,
                delay: ring * 0.35,
                repeat: Infinity,
                ease: "easeInOut",
              }}
              aria-hidden="true"
            />
          ))}

          <motion.div
            className="absolute h-full w-full rounded-full"
            animate={{ rotate: 360 }}
            transition={{ duration: 5.5, repeat: Infinity, ease: "linear" }}
            aria-hidden="true"
          >
            <div className="absolute left-1/2 top-1/2 h-1/2 w-[2px] origin-top bg-gradient-to-b from-[#f4b400] via-[#f4b400]/35 to-transparent" />
            <div className="absolute left-1/2 top-1/2 h-[1px] w-[44%] origin-left bg-gradient-to-r from-[#f4b400]/70 to-transparent" />
          </motion.div>

          <motion.div
            className="absolute h-32 w-32 rounded-full bg-[#f4b400]/12 blur-2xl sm:h-36 sm:w-36"
            animate={{
              scale: [0.9, 1.14, 0.9],
              opacity: [0.35, 0.7, 0.35],
            }}
            transition={{ duration: 2.4, repeat: Infinity, ease: "easeInOut" }}
            aria-hidden="true"
          />

          <motion.div
            className="relative flex h-28 w-28 items-center justify-center rounded-[2rem] border border-[#f4b400]/45 bg-[#081726]/90 shadow-[0_0_40px_rgba(244,180,0,0.22)] sm:h-32 sm:w-32"
            animate={{ y: [0, -5, 0] }}
            transition={{ duration: 3, repeat: Infinity, ease: "easeInOut" }}
          >
            {logoSrc && !logoFailed ? (
              <Image
                src={logoSrc}
                alt="PilotVault SA"
                width={96}
                height={96}
                className="h-20 w-20 object-contain sm:h-24 sm:w-24"
                priority
                onError={() => setLogoFailed(true)}
              />
            ) : (
              <div className="flex h-20 w-16 items-center justify-center rounded-b-3xl rounded-t-md border border-[#f4b400] bg-[#06111f] text-[#f4b400]">
                <Plane className="h-9 w-9" aria-hidden="true" />
              </div>
            )}
          </motion.div>
        </div>

        <p className="mt-2 text-xs font-semibold uppercase tracking-[0.35em] text-[#f4b400]">
          PilotVault SA
        </p>

        <motion.p
          key={activeMessage}
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.35, ease: "easeOut" }}
          className="mt-4 min-h-6 text-base font-medium text-white sm:text-lg"
        >
          {activeMessage}
        </motion.p>
      </section>
    </motion.main>
  )
}
