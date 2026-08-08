"use client"

import { useEffect, useRef, useState } from "react"
import Link from "next/link"
import { motion } from "framer-motion"
import Image from "next/image"
import {
  Apple,
  Gauge,
  Menu,
  PlaneTakeoff,
  Radar,
  ShieldCheck,
  X,
} from "lucide-react"
import { Button } from "@/components/ui/button"
import { supabase } from "@/src/lib/supabase"

const navLinks = [
  { name: "Home", href: "/" },
  { name: "Features", href: "/features" },
  { name: "Subjects", href: "/subjects" },
  { name: "Pricing", href: "/#pricing" },
  { name: "About", href: "/about" },
  { name: "Contact", href: "/#contact" },
]

export function Navbar() {
  const authDialogRef = useRef<HTMLDivElement>(null)
  const [isOpen, setIsOpen] = useState(false)
  const [authOpen, setAuthOpen] = useState(false)
  const [authMode, setAuthMode] = useState<"login" | "signup">("signup")
  const [fullName, setFullName] = useState("")
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [confirmPassword, setConfirmPassword] = useState("")
  const [loading, setLoading] = useState(false)
  const [socialLoading, setSocialLoading] = useState<
    "google" | "apple" | null
  >(null)
  const [authMessage, setAuthMessage] = useState("")

  const openAuth = (mode: "login" | "signup") => {
    setAuthMode(mode)
    setAuthOpen(true)
    setIsOpen(false)
    setAuthMessage("")
  }

  const handleSocialAuth = async (provider: "google" | "apple") => {
    setAuthMessage("")
    setSocialLoading(provider)

    const { error } = await supabase.auth.signInWithOAuth({
      provider,
      options: {
        redirectTo: `${window.location.origin}/auth/callback`,
      },
    })

    if (error) {
      setSocialLoading(null)
      setAuthMessage(error.message)
    }
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

        const { error: profileError } = await supabase.from("Profiles").insert({
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
      setAuthMessage("Account created. Please verify your email, then log in.")
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

  useEffect(() => {
    if (!authOpen) return

    const previousOverflow = document.body.style.overflow
    const closeOnEscape = (event: KeyboardEvent) => {
      if (event.key === "Escape") setAuthOpen(false)
    }

    document.body.style.overflow = "hidden"
    window.addEventListener("keydown", closeOnEscape)
    authDialogRef.current?.focus()

    return () => {
      document.body.style.overflow = previousOverflow
      window.removeEventListener("keydown", closeOnEscape)
    }
  }, [authOpen])

  return (
    <>
      <motion.nav
        initial={{ y: -100 }}
        animate={{ y: 0 }}
        transition={{ duration: 0.5 }}
        className="fixed left-0 right-0 top-0 z-50 border-b border-[#1e3a5f] bg-[#06111f]/95 backdrop-blur-md"
      >
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="grid h-20 grid-cols-[180px_1fr_auto] items-center gap-4 lg:grid-cols-[220px_1fr_220px]">
            <Link href="/" className="flex items-center justify-start">
              <Image
                src="/images/Header logo.png"
                alt="PilotVault SA"
                width={300}
                height={90}
                className="h-16 w-auto object-contain"
                priority
              />
            </Link>

            <div className="hidden items-center justify-center gap-8 lg:flex">
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

            <div className="hidden items-center justify-end gap-4 lg:flex">
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
              className="justify-self-end rounded-lg p-2 text-white transition hover:bg-[#0b1c30] lg:hidden"
              aria-label="Toggle navigation menu"
            >
              {isOpen ? (
                <X className="h-6 w-6" />
              ) : (
                <Menu className="h-6 w-6" />
              )}
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
        <div
          className="fixed inset-0 z-[100] flex items-center justify-center overflow-y-auto bg-[#020711]/85 px-4 py-6 backdrop-blur-sm"
          onMouseDown={() => setAuthOpen(false)}
          role="presentation"
        >
          <motion.div
            ref={authDialogRef}
            initial={{ opacity: 0, scale: 0.94, y: 24 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            transition={{ duration: 0.25, ease: "easeOut" }}
            onMouseDown={(event) => event.stopPropagation()}
            className="relative w-full max-w-lg overflow-hidden rounded-[28px] border border-[#2a496d] bg-[#081726] shadow-[0_30px_100px_rgba(0,0,0,0.65)]"
            role="dialog"
            aria-modal="true"
            aria-labelledby="auth-title"
            tabIndex={-1}
          >
            <div className="relative overflow-hidden border-b border-[#1e3a5f] bg-[#06111f] px-6 pb-5 pt-6 sm:px-8">
              <div className="pointer-events-none absolute -right-16 -top-20 h-48 w-48 rounded-full border border-[#f4b400]/20" />
              <div className="pointer-events-none absolute -right-8 -top-12 h-32 w-32 rounded-full border border-[#f4b400]/15" />

              <button
                type="button"
                onClick={() => setAuthOpen(false)}
                className="absolute right-4 top-4 z-10 rounded-full border border-white/10 bg-white/5 p-2 text-gray-400 transition hover:border-[#f4b400]/40 hover:text-white focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#f4b400]"
                aria-label="Close account window"
              >
                <X className="h-4 w-4" />
              </button>

              <div className="relative flex items-start gap-4 pr-10">
                <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl border border-[#f4b400]/30 bg-[#f4b400]/10 text-[#f4b400]">
                  <Radar className="h-6 w-6" />
                </div>
                <div>
                  <p className="text-[10px] font-bold uppercase tracking-[0.28em] text-[#f4b400]">
                    Pre-flight access
                  </p>
                  <h2 id="auth-title" className="mt-2 text-2xl font-bold text-white sm:text-[28px]">
                    {authMode === "login"
                      ? "Welcome back to the flight deck."
                      : "Your SACAA prep starts here."}
                  </h2>
                </div>
              </div>

              <div className="relative mt-5 flex items-center gap-3" aria-hidden="true">
                <span className="h-2 w-2 rounded-full bg-[#f4b400] shadow-[0_0_12px_rgba(244,180,0,0.9)]" />
                <span className="h-px flex-1 border-t border-dashed border-[#f4b400]/40" />
                <PlaneTakeoff className="h-5 w-5 text-[#f4b400]" />
              </div>
            </div>

            <div className="max-h-[calc(100vh-12rem)] overflow-y-auto px-6 py-6 sm:px-8">
              <div className="grid grid-cols-2 rounded-xl border border-[#1e3a5f] bg-[#06111f] p-1">
                <button
                  type="button"
                  onClick={() => {
                    setAuthMode("signup")
                    setAuthMessage("")
                  }}
                  className={`rounded-lg px-3 py-2.5 text-sm font-semibold transition focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#f4b400] ${
                    authMode === "signup"
                      ? "bg-[#f4b400] text-[#06111f] shadow-lg shadow-[#f4b400]/10"
                      : "text-gray-400 hover:text-white"
                  }`}
                >
                  Create account
                </button>

                <button
                  type="button"
                  onClick={() => {
                    setAuthMode("login")
                    setAuthMessage("")
                  }}
                  className={`rounded-lg px-3 py-2.5 text-sm font-semibold transition focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#f4b400] ${
                    authMode === "login"
                      ? "bg-[#f4b400] text-[#06111f] shadow-lg shadow-[#f4b400]/10"
                      : "text-gray-400 hover:text-white"
                  }`}
                >
                  Log in
                </button>
              </div>

              <p className="mt-4 text-sm leading-6 text-gray-400">
                {authMode === "login"
                  ? "Continue your training, mock exams, and progress tracking."
                  : "Create your account and unlock a 3-day trial—no card required."}
              </p>

              <div className="mt-5 grid gap-3 sm:grid-cols-2">
                <button
                  type="button"
                  onClick={() => handleSocialAuth("google")}
                  disabled={socialLoading !== null}
                  className="flex min-h-12 items-center justify-center gap-3 rounded-xl border border-[#284869] bg-white px-4 text-sm font-semibold text-[#06111f] transition hover:bg-gray-100 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#f4b400] disabled:cursor-wait disabled:opacity-60"
                >
                  <span className="flex h-6 w-6 items-center justify-center rounded-full border border-gray-200 bg-white text-base font-bold text-[#4285f4]">
                    G
                  </span>
                  {socialLoading === "google" ? "Connecting..." : "Continue with Google"}
                </button>

                <button
                  type="button"
                  onClick={() => handleSocialAuth("apple")}
                  disabled={socialLoading !== null}
                  className="flex min-h-12 items-center justify-center gap-3 rounded-xl border border-white/15 bg-[#020711] px-4 text-sm font-semibold text-white transition hover:border-white/30 hover:bg-black focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#f4b400] disabled:cursor-wait disabled:opacity-60"
                >
                  <Apple className="h-5 w-5" />
                  {socialLoading === "apple" ? "Connecting..." : "Continue with Apple"}
                </button>
              </div>

              <div className="my-5 flex items-center gap-3">
                <span className="h-px flex-1 bg-[#1e3a5f]" />
                <span className="text-[10px] font-bold uppercase tracking-[0.22em] text-gray-500">
                  Or use email
                </span>
                <span className="h-px flex-1 bg-[#1e3a5f]" />
              </div>

              <form
                className="space-y-4"
                onSubmit={(event) => {
                  event.preventDefault()
                  handleAuth()
                }}
              >
                {authMode === "signup" && (
                  <div>
                    <label htmlFor="auth-full-name" className="mb-1.5 block text-xs font-semibold text-gray-300">
                      Full name
                    </label>
                    <input
                      id="auth-full-name"
                      type="text"
                      autoComplete="name"
                      placeholder="Your full name"
                      value={fullName}
                      onChange={(event) => setFullName(event.target.value)}
                      className="w-full rounded-xl border border-[#1e3a5f] bg-[#06111f] px-4 py-3 text-white placeholder:text-gray-600 focus:border-[#f4b400] focus:outline-none focus:ring-1 focus:ring-[#f4b400]"
                    />
                  </div>
                )}

                <div>
                  <label htmlFor="auth-email" className="mb-1.5 block text-xs font-semibold text-gray-300">
                    Email address
                  </label>
                  <input
                    id="auth-email"
                    type="email"
                    autoComplete="email"
                    placeholder="pilot@example.com"
                    value={email}
                    onChange={(event) => setEmail(event.target.value)}
                    className="w-full rounded-xl border border-[#1e3a5f] bg-[#06111f] px-4 py-3 text-white placeholder:text-gray-600 focus:border-[#f4b400] focus:outline-none focus:ring-1 focus:ring-[#f4b400]"
                  />
                </div>

                <div>
                  <label htmlFor="auth-password" className="mb-1.5 block text-xs font-semibold text-gray-300">
                    Password
                  </label>
                  <input
                    id="auth-password"
                    type="password"
                    autoComplete={authMode === "login" ? "current-password" : "new-password"}
                    placeholder="Enter your password"
                    value={password}
                    onChange={(event) => setPassword(event.target.value)}
                    className="w-full rounded-xl border border-[#1e3a5f] bg-[#06111f] px-4 py-3 text-white placeholder:text-gray-600 focus:border-[#f4b400] focus:outline-none focus:ring-1 focus:ring-[#f4b400]"
                  />
                </div>

                {authMode === "signup" && (
                  <div>
                    <label htmlFor="auth-confirm-password" className="mb-1.5 block text-xs font-semibold text-gray-300">
                      Confirm password
                    </label>
                    <input
                      id="auth-confirm-password"
                      type="password"
                      autoComplete="new-password"
                      placeholder="Repeat your password"
                      value={confirmPassword}
                      onChange={(event) => setConfirmPassword(event.target.value)}
                      className="w-full rounded-xl border border-[#1e3a5f] bg-[#06111f] px-4 py-3 text-white placeholder:text-gray-600 focus:border-[#f4b400] focus:outline-none focus:ring-1 focus:ring-[#f4b400]"
                    />
                  </div>
                )}

                {authMessage && (
                  <p
                    className="rounded-xl border border-[#f4b400]/25 bg-[#f4b400]/5 px-4 py-3 text-sm leading-5 text-gray-200"
                    role="status"
                  >
                    {authMessage}
                  </p>
                )}

                <Button
                  type="submit"
                  disabled={loading || socialLoading !== null}
                  className="w-full bg-[#f4b400] py-6 font-bold text-[#06111f] hover:bg-[#d9a000] disabled:opacity-60"
                >
                  {loading
                    ? "Please wait..."
                    : authMode === "login"
                      ? "Enter the dashboard"
                      : "Create account & start trial"}
                </Button>
              </form>

              <div className="mt-5 grid grid-cols-2 gap-3 border-t border-[#1e3a5f] pt-5 text-xs text-gray-400">
                <span className="flex items-center gap-2">
                  <ShieldCheck className="h-4 w-4 text-[#f4b400]" />
                  Secure access
                </span>
                <span className="flex items-center justify-end gap-2">
                  <Gauge className="h-4 w-4 text-[#f4b400]" />
                  3-day trial
                </span>
              </div>

              <p className="mt-4 text-center text-[11px] leading-5 text-gray-500">
                By continuing, you agree to our{" "}
                <Link href="/terms" onClick={() => setAuthOpen(false)} className="text-gray-300 hover:text-[#f4b400]">
                  Terms
                </Link>{" "}
                and{" "}
                <Link href="/privacy" onClick={() => setAuthOpen(false)} className="text-gray-300 hover:text-[#f4b400]">
                  Privacy Policy
                </Link>
                .
              </p>
            </div>
          </motion.div>
        </div>
      )}
    </>
  )
}
