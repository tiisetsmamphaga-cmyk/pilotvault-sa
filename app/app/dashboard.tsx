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
  const [authMode, setAuthMode] = useState<"login" | "signup">("login")

  const openAuth = (mode: "login" | "signup") => {
    setAuthMode(mode)
    setAuthOpen(true)
    setIsOpen(false)
  }

  useEffect(() => {
    const handleOpenSignup = () => openAuth("signup")

    window.addEventListener("open-signup-modal", handleOpenSignup)

    return () => {
      window.removeEventListener("open-signup-modal", handleOpenSignup)
    }
  }, [])

  return (
    <>
      <motion.nav
        initial={{ y: -100 }}
        animate={{ y: 0 }}
        transition={{ duration: 0.5 }}
        className="fixed top-0 left-0 right-0 z-50 bg-[#06111f]/95 backdrop-blur-md border-b border-[#1e3a5f]"
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16 lg:h-20">
            <Link href="#" className="flex items-center">
              <Image
                src="/images/logo.png"
                alt="PilotVault SA"
                width={200}
                height={50}
                className="h-[110px] w-auto"
                priority
              />
            </Link>

            <div className="hidden lg:flex items-center gap-8">
              {navLinks.map((link) => (
                <Link
                  key={link.name}
                  href={link.href}
                  className="text-sm font-medium text-gray-300 hover:text-[#f4b400] transition-colors"
                >
                  {link.name}
                </Link>
              ))}
            </div>

            <div className="hidden lg:flex items-center gap-4">
              <Button
                onClick={() => openAuth("login")}
                variant="outline"
                className="border-[#1e3a5f] text-white hover:bg-[#1e3a5f] hover:text-white"
              >
                Login
              </Button>

              <Button
                onClick={() => openAuth("signup")}
                className="bg-[#f4b400] text-[#06111f] hover:bg-[#d9a000] font-semibold"
              >
                Start Free Trial
              </Button>
            </div>

            <button
              onClick={() => setIsOpen(!isOpen)}
              className="lg:hidden p-2 text-white"
            >
              {isOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
            </button>
          </div>

          {isOpen && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: "auto" }}
              exit={{ opacity: 0, height: 0 }}
              className="lg:hidden py-4 border-t border-[#1e3a5f]"
            >
              <div className="flex flex-col gap-4">
                {navLinks.map((link) => (
                  <Link
                    key={link.name}
                    href={link.href}
                    onClick={() => setIsOpen(false)}
                    className="text-gray-300 hover:text-[#f4b400] transition-colors"
                  >
                    {link.name}
                  </Link>
                ))}

                <div className="flex flex-col gap-2 pt-4 border-t border-[#1e3a5f]">
                  <Button
                    onClick={() => openAuth("login")}
                    variant="outline"
                    className="border-[#1e3a5f] text-white hover:bg-[#1e3a5f] w-full"
                  >
                    Login
                  </Button>

                  <Button
                    onClick={() => openAuth("signup")}
                    className="bg-[#f4b400] text-[#06111f] hover:bg-[#d9a000] font-semibold w-full"
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
        <div className="fixed inset-0 z-[100] flex items-center justify-center bg-black/70 px-4">
          <motion.div
            initial={{ opacity: 0, scale: 0.92, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            className="relative w-full max-w-md rounded-2xl border border-[#1e3a5f] bg-[#06111f] p-6 shadow-2xl"
          >
            <button
              onClick={() => setAuthOpen(false)}
              className="absolute right-4 top-4 text-gray-400 hover:text-white"
            >
              <X className="h-5 w-5" />
            </button>

            <div className="mb-6">
              <p className="text-sm font-semibold uppercase tracking-[0.3em] text-[#f4b400]">
                PilotVault SA
              </p>

              <h2 className="mt-3 text-2xl font-bold text-white">
                {authMode === "login"
                  ? "Welcome back, pilot."
                  : "Start your 7-day free trial."}
              </h2>

              <p className="mt-2 text-sm text-gray-400">
                {authMode === "login"
                  ? "Log in to continue your SACAA exam preparation."
                  : "Create your account and start preparing with realistic SACAA-style questions, mock exams, and progress tracking."}
              </p>
            </div>

            <div className="mb-6 grid grid-cols-2 rounded-xl bg-[#0b1c30] p-1">
              <button
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