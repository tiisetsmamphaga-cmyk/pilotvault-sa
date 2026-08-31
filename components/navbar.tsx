"use client"

import { useEffect, useRef, useState } from "react"
import Link from "next/link"
import Image from "next/image"
import { motion } from "framer-motion"
import { Menu, X } from "lucide-react"
import { Button } from "@/components/ui/button"
import { VaultLoadingScreen } from "@/components/vault-loading-screen"
import { supabase } from "@/src/lib/supabase"

const navLinks = [
  { name: "Home", href: "/" },
  { name: "Features", href: "/features" },
  { name: "Subjects", href: "/subjects" },
  { name: "Pricing", href: "/#pricing" },
  { name: "About", href: "/about" },
  { name: "Contact", href: "/#contact" },
]

type AuthMode = "login" | "signup" | "reset"

const LOGIN_ANIMATION_MIN_MS = 1650

export function Navbar() {
  const authDialogRef = useRef<HTMLDivElement>(null)
  const [isOpen, setIsOpen] = useState(false)
  const [authOpen, setAuthOpen] = useState(false)
  const [authMode, setAuthMode] = useState<AuthMode>("signup")
  const [fullName, setFullName] = useState("")
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [confirmPassword, setConfirmPassword] = useState("")
  const [loading, setLoading] = useState(false)
  const [resetRequestLoading, setResetRequestLoading] = useState(false)
  const [authMessage, setAuthMessage] = useState("")

  const openAuth = (mode: "login" | "signup") => {
    setAuthMode(mode)
    setAuthOpen(true)
    setIsOpen(false)
    setAuthMessage("")
  }

  const handlePasswordResetRequest = async () => {
    const normalizedEmail = email.trim()

    if (!normalizedEmail) {
      setAuthMessage("Enter your email address first, then select Forgot password.")
      return
    }

    setAuthMessage("")
    setResetRequestLoading(true)

    const { error } = await supabase.auth.resetPasswordForEmail(normalizedEmail, {
      redirectTo: `${window.location.origin}/`,
    })

    setResetRequestLoading(false)

    if (error) {
      setAuthMessage(error.message)
      return
    }

    setAuthMessage(
      "Password reset email sent. Check your inbox and follow the link to choose a new password."
    )
  }

  const handleAuth = async () => {
    setAuthMessage("")

    if (authMode === "reset") {
      if (!password || !confirmPassword) {
        setAuthMessage("Please enter and confirm your new password.")
        return
      }

      if (password !== confirmPassword) {
        setAuthMessage("Passwords do not match.")
        return
      }

      setLoading(true)
      const { error } = await supabase.auth.updateUser({ password })
      setLoading(false)

      if (error) {
        setAuthMessage(error.message)
        return
      }

      window.location.href = "/dashboard"
      return
    }

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

    const loginStartedAt = authMode === "login" ? Date.now() : 0
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
        const trialEndsAt = new Date(Date.now() + 3 * 24 * 60 * 60 * 1000).toISOString()

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

    const elapsed = Date.now() - loginStartedAt
    if (elapsed < LOGIN_ANIMATION_MIN_MS) {
      await new Promise((resolve) => setTimeout(resolve, LOGIN_ANIMATION_MIN_MS - elapsed))
    }

    window.location.href = "/dashboard"
  }

  useEffect(() => {
    const showPasswordRecovery = () => {
      setAuthMode("reset")
      setAuthOpen(true)
      setIsOpen(false)
      setPassword("")
      setConfirmPassword("")
      setAuthMessage("")
    }

    if (window.location.hash.includes("type=recovery")) {
      showPasswordRecovery()
    }

    const {
      data: { subscription },
    } = supabase.auth.onAuthStateChange((event) => {
      if (event === "PASSWORD_RECOVERY") showPasswordRecovery()
    })

    return () => subscription.unsubscribe()
  }, [])

  useEffect(() => {
    const openSignup = () => openAuth("signup")
    window.addEventListener("open-signup-modal", openSignup)
    return () => window.removeEventListener("open-signup-modal", openSignup)
  }, [])

  useEffect(() => {
    if (!authOpen) return

    const previousOverflow = document.body.style.overflow
    const closeOnEscape = (event: KeyboardEvent) => {
      if (event.key === "Escape" && !loading) setAuthOpen(false)
    }

    document.body.style.overflow = "hidden"
    window.addEventListener("keydown", closeOnEscape)
    authDialogRef.current?.focus()

    return () => {
      document.body.style.overflow = previousOverflow
      window.removeEventListener("keydown", closeOnEscape)
    }
  }, [authOpen, loading])

  return (
    <>
      <motion.nav
        initial={{ y: -100 }}
        animate={{ y: 0 }}
        transition={{ duration: 0.5 }}
        className="fixed left-0 right-0 top-0 z-50 border-b border-white/10 bg-[#1f4e79]/95 shadow-sm backdrop-blur-md"
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
                  className="text-sm font-medium text-blue-50 transition-colors hover:text-white"
                >
                  {link.name}
                </Link>
              ))}
            </div>

            <div className="hidden items-center justify-end gap-3 lg:flex">
              <Button
                type="button"
                onClick={() => openAuth("login")}
                variant="outline"
                className="border-white/35 bg-transparent text-white hover:bg-white/10 hover:text-white"
              >
                Login
              </Button>
              <Button
                type="button"
                onClick={() => openAuth("signup")}
                className="bg-white font-semibold text-[#1f4e79] hover:bg-[#f1f5f9]"
              >
                Start Free Trial
              </Button>
            </div>

            <button
              type="button"
              onClick={() => setIsOpen(!isOpen)}
              className="justify-self-end rounded-lg p-2 text-white transition hover:bg-white/10 lg:hidden"
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
              className="border-t border-white/15 px-2 py-5 lg:hidden"
            >
              <div className="flex flex-col gap-2">
                {navLinks.map((link) => (
                  <Link
                    key={link.name}
                    href={link.href}
                    onClick={() => setIsOpen(false)}
                    className="rounded-lg px-3 py-2 text-base text-blue-50 transition-colors hover:bg-white/10 hover:text-white"
                  >
                    {link.name}
                  </Link>
                ))}

                <div className="mt-3 flex flex-col gap-3 border-t border-white/15 pt-5">
                  <Button
                    type="button"
                    onClick={() => openAuth("login")}
                    variant="outline"
                    className="w-full border-white/35 bg-transparent text-white hover:bg-white/10 hover:text-white"
                  >
                    Login
                  </Button>
                  <Button
                    type="button"
                    onClick={() => openAuth("signup")}
                    className="w-full bg-white font-semibold text-[#1f4e79] hover:bg-[#f1f5f9]"
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
          className="fixed inset-0 z-[100] flex items-center justify-center bg-slate-950/65 px-4 py-6 backdrop-blur-sm"
          onMouseDown={() => {
            if (!loading) setAuthOpen(false)
          }}
          role="presentation"
        >
          <motion.div
            ref={authDialogRef}
            initial={{ opacity: 0, scale: 0.92, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            onMouseDown={(event) => event.stopPropagation()}
            className="relative max-h-[90vh] w-full max-w-md overflow-y-auto rounded-3xl border border-slate-200 bg-white p-6 text-slate-900 shadow-2xl"
            role="dialog"
            aria-modal="true"
            aria-labelledby="auth-title"
            tabIndex={-1}
          >
            <button
              type="button"
              onClick={() => setAuthOpen(false)}
              disabled={loading}
              className="absolute right-4 top-4 rounded-lg p-1 text-slate-400 hover:bg-slate-100 hover:text-slate-700 disabled:opacity-40"
              aria-label="Close auth modal"
            >
              <X className="h-5 w-5" />
            </button>

            <p className="text-sm font-semibold uppercase tracking-[0.25em] text-[#1f4e79]">
              PilotVault SA
            </p>
            <h2 id="auth-title" className="mt-3 pr-8 text-2xl font-bold text-slate-900">
              {authMode === "login"
                ? "Welcome back, pilot."
                : authMode === "signup"
                  ? "Start your 3-day free trial."
                  : "Choose a new password."}
            </h2>
            <p className="mt-2 text-sm leading-6 text-slate-600">
              {authMode === "login"
                ? "Log in to continue your SACAA exam preparation."
                : authMode === "signup"
                  ? "Create your account and start preparing with realistic SACAA-style questions, mock exams, and progress tracking."
                  : "Enter a new password for your PilotVault account."}
            </p>

            {authMode !== "reset" && (
              <div className="my-6 grid grid-cols-2 rounded-xl bg-[#f1f5f9] p-1">
                <button
                  type="button"
                  disabled={loading}
                  onClick={() => {
                    setAuthMode("login")
                    setAuthMessage("")
                  }}
                  className={`rounded-lg py-2 text-sm font-semibold transition ${
                    authMode === "login"
                      ? "bg-[#1f4e79] text-white shadow-sm"
                      : "text-slate-600 hover:text-slate-900"
                  } disabled:opacity-60`}
                >
                  Login
                </button>
                <button
                  type="button"
                  disabled={loading}
                  onClick={() => {
                    setAuthMode("signup")
                    setAuthMessage("")
                  }}
                  className={`rounded-lg py-2 text-sm font-semibold transition ${
                    authMode === "signup"
                      ? "bg-[#1f4e79] text-white shadow-sm"
                      : "text-slate-600 hover:text-slate-900"
                  } disabled:opacity-60`}
                >
                  Free Trial
                </button>
              </div>
            )}

            <form
              className={`space-y-4 ${authMode === "reset" ? "mt-6" : ""}`}
              onSubmit={(event) => {
                event.preventDefault()
                handleAuth()
              }}
            >
              {authMode === "signup" && (
                <input
                  type="text"
                  autoComplete="name"
                  aria-label="Full name"
                  placeholder="Full name"
                  value={fullName}
                  onChange={(event) => setFullName(event.target.value)}
                  className="w-full rounded-xl border border-slate-300 bg-white px-4 py-3 text-slate-900 placeholder:text-slate-400 focus:border-[#1f4e79] focus:outline-none focus:ring-2 focus:ring-[#d6e6f7]"
                />
              )}

              {authMode !== "reset" && (
                <input
                  type="email"
                  autoComplete="email"
                  aria-label="Email address"
                  placeholder="Email address"
                  value={email}
                  onChange={(event) => setEmail(event.target.value)}
                  className="w-full rounded-xl border border-slate-300 bg-white px-4 py-3 text-slate-900 placeholder:text-slate-400 focus:border-[#1f4e79] focus:outline-none focus:ring-2 focus:ring-[#d6e6f7]"
                />
              )}

              <input
                type="password"
                autoComplete={authMode === "login" ? "current-password" : "new-password"}
                aria-label={authMode === "reset" ? "New password" : "Password"}
                placeholder={authMode === "reset" ? "New password" : "Password"}
                value={password}
                onChange={(event) => setPassword(event.target.value)}
                className="w-full rounded-xl border border-slate-300 bg-white px-4 py-3 text-slate-900 placeholder:text-slate-400 focus:border-[#1f4e79] focus:outline-none focus:ring-2 focus:ring-[#d6e6f7]"
              />

              {authMode === "login" && (
                <div className="flex justify-end">
                  <button
                    type="button"
                    onClick={handlePasswordResetRequest}
                    disabled={resetRequestLoading || loading}
                    className="text-sm font-semibold text-[#1f4e79] transition hover:text-[#183d60] disabled:cursor-wait disabled:opacity-60"
                  >
                    {resetRequestLoading ? "Sending reset email..." : "Forgot password?"}
                  </button>
                </div>
              )}

              {(authMode === "signup" || authMode === "reset") && (
                <input
                  type="password"
                  autoComplete="new-password"
                  aria-label={authMode === "reset" ? "Confirm new password" : "Confirm password"}
                  placeholder={authMode === "reset" ? "Confirm new password" : "Confirm password"}
                  value={confirmPassword}
                  onChange={(event) => setConfirmPassword(event.target.value)}
                  className="w-full rounded-xl border border-slate-300 bg-white px-4 py-3 text-slate-900 placeholder:text-slate-400 focus:border-[#1f4e79] focus:outline-none focus:ring-2 focus:ring-[#d6e6f7]"
                />
              )}

              {authMessage && (
                <p
                  className="rounded-xl border border-slate-200 bg-[#f8fafc] px-4 py-3 text-sm text-slate-700"
                  role="status"
                >
                  {authMessage}
                </p>
              )}

              <Button
                type="submit"
                disabled={loading || resetRequestLoading}
                className="w-full bg-[#1f4e79] py-6 font-bold text-white hover:bg-[#183d60] disabled:opacity-60"
              >
                {loading
                  ? "Please wait..."
                  : authMode === "login"
                    ? "Login"
                    : authMode === "signup"
                      ? "Start Free Trial"
                      : "Update Password"}
              </Button>
            </form>
          </motion.div>
        </div>
      )}

      {loading && authMode === "login" && (
        <VaultLoadingScreen message="Unlocking your dashboard..." />
      )}
    </>
  )
}
