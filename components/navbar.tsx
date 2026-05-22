"use client"

import { useEffect, useState } from "react"
import Link from "next/link"
import { motion } from "framer-motion"
import Image from "next/image"
import { Menu, X } from "lucide-react"
import { Button } from "@/components/ui/button"

const navLinks = [
  { name: "Home", href: "#" },
  { name: "Features", href: "#features" },
  { name: "Subjects", href: "#subjects" },
  { name: "Pricing", href: "#pricing" },
  { name: "About", href: "#about" },
  { name: "Contact", href: "#contact" },
]

export function Navbar() {
  const [isOpen, setIsOpen] = useState(false)
  const [authOpen, setAuthOpen] = useState(false)
  const [authMode, setAuthMode] = useState<"login" | "signup">("signup")

  const openAuth = (mode: "login" | "signup") => {
    setAuthMode(mode)
    setAuthOpen(true)
    setIsOpen(false)
  }

  useEffect(() => {
    const openSignup = () => openAuth("signup")

    window.addEventListener("open-signup-modal", openSignup)

    return () => {
      window.removeEventListener("open-signup-modal", openSignup)
    }
  }, [])

  return (
    <>
      <motion.nav
        initial={{ y: -100 }}
        animate={{ y: 0 }}
        transition={{ duration: 0.5 }}
        className="fixed top-0 left-0 right-0 z-50 border-b border-[#1e3a5f] bg-[#06111f]/95 backdrop-blur-md"
      >
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="flex h-16 items-center justify-between lg:h-20">
            <Link href="#" className="flex items-center">
              <Image
                src="/images/logo.png"
                alt="PilotVault SA"
                width={200}
                height={50}
                className="h-12 w-auto sm:h-14 lg:h-20"
                priority
              />
            </Link>

            <div className="hidden items-center gap-8 lg:flex">
              {navLinks.map((link) => (
                <Link
                  key={link.name}
                  href={link.href}
                  className="text-sm font-medium text-gray-300 transition-colors hover:text-[#f4b400]"
                >
                  {link.name}
                </Link>
              ))}
            </div>

            <div className="hidden items-center gap-4 lg:flex">
              <Button
                type="button"
                onClick={() => openAuth("login")}
                variant="outline"
                className="border-[#1e3a5f] text-white hover:bg-[#1e3a5f] hover:text-white"
              >
                Login
              </Button>

              <Button
                type="button"
                onClick={() => openAuth("signup")}
                className="bg-[#f4b400] font-semibold text-[#06111f] hover:bg-[#d9a000]"
              >
                Start Free Trial
              </Button>
            </div>

            <button
              type="button"
              onClick={() => setIsOpen(!isOpen)}
              className="rounded-lg p-2 text-white transition hover:bg-[#0b1c30] lg:hidden"
              aria-label="Toggle navigation menu"
            >
              {isOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
            </button>
          </div>

          {isOpen && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: "auto" }}
              transition={{ duration: 0.25 }}
              className="border-t border-[#1e3a5f] px-2 py-5 lg:hidden"
            >
              <div className="flex flex-col gap-3">
                {navLinks.map((link) => (
                  <Link
                    key={link.name}
                    href={link.href}
                    onClick={() => setIsOpen(false)}
                    className="rounded-lg px-2 py-2 text-base text-gray-300 transition-colors hover:bg-[#0b1c30] hover:text-[#f4b400]"
                  >
                    {link.name}
                  </Link>
                ))}

                <div className="mt-3 flex flex-col gap-3 border-t border-[#1e3a5f] pt-5">
                  <Button
                    type="button"
                    onClick={() => openAuth("login")}
                    variant="outline"
                    className="w-full border-[#1e3a5f] text-white hover:bg-[#1e3a5f] hover:text-white"
                  >
                    Login
                  </Button>

                  <Button
                    type="button"
                    onClick={() => openAuth("signup")}
                    className="w-full bg-[#f4b400] font-semibold text-[#06111f] hover:bg-[#d9a000]"
                  >
                    Start Free Trial
                  </Button>
                </div>
              </div>
            </motion.div>
          )}
        </div>
      </motion.nav>

      {authOpen && (
        <div className="fixed inset-0 z-[100] flex items-center justify-center bg-black/70 px-4 py-6">
          <motion.div
            initial={{ opacity: 0, scale: 0.92, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
           className="relative w-full max-w-md rounded-3xl border border-[#1e3a5f] bg-[#081726] p-6 shadow-2xl"
          >
            <button
              type="button"
              onClick={() => setAuthOpen(false)}
              className="absolute right-4 top-4 text-gray-400 hover:text-white"
              aria-label="Close auth modal"
            >
              <X className="h-5 w-5" />
            </button>

            <p className="text-sm font-semibold uppercase tracking-[0.3em] text-[#f4b400]">
              PilotVault SA
            </p>

            <h2 className="mt-3 pr-8 text-2xl font-bold text-white">
              {authMode === "login"
                ? "Welcome back, pilot."
                : "Start your 3-day free trial."}
            </h2>

            <p className="mt-2 text-sm leading-6 text-gray-400">
              {authMode === "login"
                ? "Log in to continue your SACAA exam preparation."
                : "Create your account and start preparing with realistic SACAA-style questions, mock exams, and progress tracking."}
            </p>

            <div className="my-6 grid grid-cols-2 rounded-xl bg-[#0b1c30] p-1">
              <button
                type="button"
                onClick={() => setAuthMode("login")}
                className={`rounded-lg py-2 text-sm font-semibold transition ${
                  authMode === "login"
                    ? "bg-[#f4b400] text-[#06111f]"
                    : "text-gray-300 hover:text-white"
                }`}
              >
                Login
              </button>

              <button
                type="button"
                onClick={() => setAuthMode("signup")}
                className={`rounded-lg py-2 text-sm font-semibold transition ${
                  authMode === "signup"
                    ? "bg-[#f4b400] text-[#06111f]"
                    : "text-gray-300 hover:text-white"
                }`}
              >
                Free Trial
              </button>
            </div>

            <form className="space-y-4">
              {authMode === "signup" && (
                <input
                  type="text"
                  placeholder="Full name"
                  className="w-full rounded-xl border border-[#1e3a5f] bg-[#0b1c30] px-4 py-3 text-white placeholder:text-gray-500 focus:border-[#f4b400] focus:outline-none"
                />
              )}

              <input
                type="email"
                placeholder="Email address"
                className="w-full rounded-xl border border-[#1e3a5f] bg-[#0b1c30] px-4 py-3 text-white placeholder:text-gray-500 focus:border-[#f4b400] focus:outline-none"
              />

              <input
                type="password"
                placeholder="Password"
                className="w-full rounded-xl border border-[#1e3a5f] bg-[#0b1c30] px-4 py-3 text-white placeholder:text-gray-500 focus:border-[#f4b400] focus:outline-none"
              />

              {authMode === "signup" && (
                <input
                  type="password"
                  placeholder="Confirm password"
                  className="w-full rounded-xl border border-[#1e3a5f] bg-[#0b1c30] px-4 py-3 text-white placeholder:text-gray-500 focus:border-[#f4b400] focus:outline-none"
                />
              )}

              <Button
                type="button"
                onClick={() => {
                  window.location.href = "/dashboard"
                }}
                className="w-full bg-[#f4b400] py-6 font-bold text-[#06111f] hover:bg-[#d9a000]"
              >
                {authMode === "login" ? "Login" : "Start Free Trial"}
              </Button>
            </form>
          </motion.div>
        </div>
      )}
    </>
  )
}