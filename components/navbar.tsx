"use client"

import { useEffect, useState } from "react"
import Link from "next/link"
import { motion } from "framer-motion"
import Image from "next/image"
import { Menu, X } from "lucide-react"
import { Button } from "@/components/ui/button"
import { supabase } from "@/src/lib/supabase"

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
  const [fullName, setFullName] = useState("")
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [confirmPassword, setConfirmPassword] = useState("")
  const [loading, setLoading] = useState(false)
  const [authMessage, setAuthMessage] = useState("")

  const openAuth = (mode: "login" | "signup") => {
    setAuthMode(mode)
    setAuthOpen(true)
    setIsOpen(false)
    setAuthMessage("")
  }

  const handleAuth = async () => {
    setAuthMessage("")

    if (!email || !password) {
      setAuthMessage("Please enter your email and password.")
      return
    }

    if (authMode === "signup") {
      if (!fullName) {
        setAuthMessage("Please enter your full name.")
        return
      }

      if (password !== confirmPassword) {
        setAuthMessage("Passwords do not match.")
        return
      }
    }

    setLoading(true)

    const { data, error } =
      authMode === "login"
        ? await supabase.auth.signInWithPassword({ email, password })
        : await supabase.auth.signUp({
            email,
            password,
            options: {
              data: {
                full_name: fullName,
              },
            },
          })

    if (error) {
      setLoading(false)
      setAuthMessage(error.message)
      return
    }

    if (authMode === "signup") {
      if (data.user) {
        const trialEndsAt = new Date(
          Date.now() + 3 * 24 * 60 * 60 * 1000
        ).toISOString()

        const { error: profileError } = await supabase
          .from("Profiles")
          .insert({
            id: data.user.id,
            full_name: fullName,
            email,
            subscription_status: "trial",
            subscription_plan: "trial",
            payment_status: "unpaid",
            trial_ends_at: trialEndsAt,
          })

        if (profileError) {
          setLoading(false)
          setAuthMessage(profileError.message)
          return
        }
      }

      setLoading(false)
      setAuthMessage("Account created. You can now log in.")
      setAuthMode("login")
      setPassword("")
      setConfirmPassword("")
      return
    }

    setLoading(false)
    window.location.href = "/dashboard"
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
        className="fixed left-0 right-0 top-0 z-50 border-b border-[#1e3a5f] bg-[#06111f]/95 backdrop-blur-md"
      >
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="flex h-20 items-center justify-between lg:h-24">
            <Link href="#" className="flex items-center">
              <Image
                src="/images/logo.png"
                alt="PilotVault SA"
                width={420}
                height={120}
                className="h-16 w-auto sm:h-20 lg:h-24"
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
            className="relative max-h-[90vh] w-full max-w-md overflow-y-auto rounded-3xl border border-[#1e3a5f] bg-[#081726] p-6 shadow-2xl"
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
                onClick={() => {
                  setAuthMode("login")
                  setAuthMessage("")
                }}
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
                onClick={() => {
                  setAuthMode("signup")
                  setAuthMessage("")
                }}
                className={`rounded-lg py-2 text-sm font-semibold transition ${
                  authMode === "signup"
                    ? "bg-[#f4b400] text-[#06111f]"
                    : "text-gray-300 hover:text-white"
                }`}
              >
                Free Trial
              </button>
            </div>

            <form
              className="space-y-4"
              onSubmit={(e) => {
                e.preventDefault()
                handleAuth()
              }}
            >
              {authMode === "signup" && (
                <input
                  type="text"
                  placeholder="Full name"
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                  className="w-full rounded-xl border border-[#1e3a5f] bg-[#0b1c30] px-4 py-3 text-white placeholder:text-gray-500 focus:border-[#f4b400] focus:outline-none"
                />
              )}

              <input
                type="email"
                placeholder="Email address"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full rounded-xl border border-[#1e3a5f] bg-[#0b1c30] px-4 py-3 text-white placeholder:text-gray-500 focus:border-[#f4b400] focus:outline-none"
              />

              <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full rounded-xl border border-[#1e3a5f] bg-[#0b1c30] px-4 py-3 text-white placeholder:text-gray-500 focus:border-[#f4b400] focus:outline-none"
              />

              {authMode === "signup" && (
                <input
                  type="password"
                  placeholder="Confirm password"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  className="w-full rounded-xl border border-[#1e3a5f] bg-[#0b1c30] px-4 py-3 text-white placeholder:text-gray-500 focus:border-[#f4b400] focus:outline-none"
                />
              )}

              {authMessage && (
                <p className="rounded-xl border border-[#1e3a5f] bg-[#06111f] px-4 py-3 text-sm text-gray-300">
                  {authMessage}
                </p>
              )}

              <Button
                type="submit"
                disabled={loading}
                className="w-full bg-[#f4b400] py-6 font-bold text-[#06111f] hover:bg-[#d9a000] disabled:opacity-60"
              >
                {loading
                  ? "Please wait..."
                  : authMode === "login"
                    ? "Login"
                    : "Start Free Trial"}
              </Button>
            </form>
          </motion.div>
        </div>
      )}
    </>
  )
}