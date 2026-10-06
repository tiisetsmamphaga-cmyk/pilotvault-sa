"use client"

import { useEffect, useRef, useState } from "react"
import Link from "next/link"
import Image from "next/image"
import { usePathname } from "next/navigation"
import { motion } from "framer-motion"
import { Menu, X } from "lucide-react"
import { PasswordInput } from "@/components/password-input"
import { Turnstile, TURNSTILE_SITE_KEY, type TurnstileHandle } from "@/components/turnstile"
import { Button } from "@/components/ui/button"
import { claimDeviceSession } from "@/src/lib/device-session"
import { supabase } from "@/src/lib/supabase"

const navLinks = [
  { name: "Home", href: "/" },
  { name: "Features", href: "/features" },
  { name: "Subjects", href: "/subjects" },
  { name: "Pricing", href: "/#pricing" },
  { name: "About", href: "/about" },
  { name: "FAQ", href: "/faq" },
  { name: "Contact", href: "/#contact" },
]

type AuthMode = "login" | "signup" | "reset"

export function Navbar() {
  const pathname = usePathname()
  const authDialogRef = useRef<HTMLDivElement>(null)
  const turnstileRef = useRef<TurnstileHandle>(null)
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
  const [authNotice, setAuthNotice] = useState("")
  const [signedIn, setSignedIn] = useState(false)
  const [captchaToken, setCaptchaToken] = useState<string | null>(null)
  const captchaRequired = Boolean(TURNSTILE_SITE_KEY) && authMode !== "reset"
  const captchaMissing = captchaRequired && !captchaToken

  const openAuth = (mode: "login" | "signup") => {
    setAuthMode(mode)
    setAuthOpen(true)
    setIsOpen(false)
    setAuthMessage("")
    setAuthNotice("")
  }

  const handlePasswordResetRequest = async () => {
    const normalizedEmail = email.trim()

    if (!normalizedEmail) {
      setAuthMessage("Enter your email address first, then select Forgot password.")
      return
    }

    if (captchaMissing) {
      setAuthMessage("Please complete the robot check first, then select Forgot password.")
      return
    }

    setAuthMessage("")
    setResetRequestLoading(true)

    const { error } = await supabase.auth.resetPasswordForEmail(normalizedEmail, {
      redirectTo: `${window.location.origin}/`,
      captchaToken: captchaToken ?? undefined,
    })

    setResetRequestLoading(false)
    turnstileRef.current?.reset()

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

      await claimDeviceSession()
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

    if (captchaMissing) {
      setAuthMessage("Please complete the robot check.")
      return
    }

    setLoading(true)

    const token = captchaToken ?? undefined
    const { error } =
      authMode === "login"
        ? await supabase.auth.signInWithPassword({ email, password, options: { captchaToken: token } })
        : await supabase.auth.signUp({
            email,
            password,
            options: {
              captchaToken: token,
              data: {
                full_name: fullName,
              },
            },
          })

    // A Turnstile token works once, so get a fresh one for the next try.
    turnstileRef.current?.reset()

    if (error) {
      setLoading(false)
      setAuthMessage(error.message)
      return
    }

    if (authMode === "signup") {
      // The Profiles row is created server-side by the on_auth_user_created
      // trigger, not here: right after signUp() there is no session yet
      // when email confirmation is required, so a client-side insert would
      // fail the "auth.uid() = id" RLS policy.
      setLoading(false)
      setAuthMessage("Account created. Please verify your email, then log in.")
      setAuthMode("login")
      setPassword("")
      setConfirmPassword("")
      return
    }

    await claimDeviceSession()

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
    let mounted = true

    void supabase.auth.getSession().then(({ data }) => {
      if (mounted) setSignedIn(Boolean(data.session))
    })

    const {
      data: { subscription },
    } = supabase.auth.onAuthStateChange((_event, session) => {
      setSignedIn(Boolean(session))
    })

    return () => {
      mounted = false
      subscription.unsubscribe()
    }
  }, [])

  useEffect(() => {
    setIsOpen(false)
  }, [pathname])

  useEffect(() => {
    const openSignup = () => openAuth("signup")
    window.addEventListener("open-signup-modal", openSignup)
    return () => window.removeEventListener("open-signup-modal", openSignup)
  }, [])

  useEffect(() => {
    const openLogin = (event: Event) => {
      const message = (event as CustomEvent<{ message?: string }>).detail
        ?.message

      openAuth("login")
      if (message) setAuthNotice(message)
    }
    window.addEventListener("open-login-modal", openLogin)
    return () => window.removeEventListener("open-login-modal", openLogin)
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

  const linkIsActive = (href: string) => {
    if (href === "/") return pathname === "/"
    if (href.startsWith("/#")) return pathname === "/"
    return pathname === href
  }

  return (
    <>
      <motion.nav
        initial={{ y: -100 }}
        animate={{ y: 0 }}
        transition={{ duration: 0.4 }}
        className="fixed left-0 right-0 top-0 z-50 border-b border-white/10 bg-[#1f4e79]/96 shadow-sm backdrop-blur-md"
      >
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="grid h-20 grid-cols-[minmax(150px,190px)_1fr_auto] items-center gap-3 xl:grid-cols-[210px_1fr_210px]">
            <Link href="/" className="flex items-center justify-start" aria-label="PilotVault SA home">
              <Image
                src="/images/Header logo.png"
                alt="PilotVault SA"
                width={300}
                height={90}
                className="h-14 w-auto object-contain sm:h-16"
                priority
              />
            </Link>

            <div className="hidden items-center justify-center gap-1 xl:flex">
              {navLinks.map((link) => {
                const active = linkIsActive(link.href)

                return (
                  <Link
                    key={link.name}
                    href={link.href}
                    aria-current={active ? "page" : undefined}
                    className={`rounded-lg px-3 py-2 text-sm transition-colors ${
                      active
                        ? "bg-white/12 font-semibold text-white"
                        : "font-medium text-blue-50 hover:bg-white/8 hover:text-white"
                    }`}
                  >
                    {link.name}
                  </Link>
                )
              })}
            </div>

            <div className="hidden items-center justify-end gap-2 xl:flex">
              {signedIn ? (
                <>
                  <Link
                    href="/profile"
                    className="rounded-lg px-3 py-2 text-sm font-medium text-blue-50 transition hover:bg-white/10 hover:text-white"
                  >
                    Profile
                  </Link>
                  <Link
                    href="/dashboard"
                    className="inline-flex h-10 items-center justify-center rounded-lg bg-white px-4 text-sm font-semibold text-[#1f4e79] transition hover:bg-[#f1f5f9]"
                  >
                    Dashboard
                  </Link>
                </>
              ) : (
                <>
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
                </>
              )}
            </div>

            <button
              type="button"
              onClick={() => setIsOpen((open) => !open)}
              className="justify-self-end rounded-lg p-2 text-white transition hover:bg-white/10 xl:hidden"
              aria-label="Toggle navigation menu"
              aria-expanded={isOpen}
              aria-controls="pilotvault-mobile-menu"
            >
              {isOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
            </button>
          </div>

          {isOpen && (
            <motion.div
              id="pilotvault-mobile-menu"
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: "auto" }}
              transition={{ duration: 0.2 }}
              className="border-t border-white/15 px-1 py-4 xl:hidden"
            >
              <div className="grid gap-1 sm:grid-cols-2 lg:grid-cols-3">
                {navLinks.map((link) => {
                  const active = linkIsActive(link.href)

                  return (
                    <Link
                      key={link.name}
                      href={link.href}
                      aria-current={active ? "page" : undefined}
                      onClick={() => setIsOpen(false)}
                      className={`rounded-lg px-3 py-2.5 text-sm transition-colors ${
                        active
                          ? "bg-white/12 font-semibold text-white"
                          : "text-blue-50 hover:bg-white/10 hover:text-white"
                      }`}
                    >
                      {link.name}
                    </Link>
                  )
                })}
              </div>

              <div className="mt-4 flex flex-col gap-2 border-t border-white/15 pt-4 sm:flex-row">
                {signedIn ? (
                  <>
                    <Link
                      href="/profile"
                      onClick={() => setIsOpen(false)}
                      className="inline-flex min-h-11 flex-1 items-center justify-center rounded-lg border border-white/30 px-4 text-sm font-semibold text-white transition hover:bg-white/10"
                    >
                      Profile
                    </Link>
                    <Link
                      href="/dashboard"
                      onClick={() => setIsOpen(false)}
                      className="inline-flex min-h-11 flex-1 items-center justify-center rounded-lg bg-white px-4 text-sm font-semibold text-[#1f4e79] transition hover:bg-[#f1f5f9]"
                    >
                      Dashboard
                    </Link>
                  </>
                ) : (
                  <>
                    <Button
                      type="button"
                      onClick={() => openAuth("login")}
                      variant="outline"
                      className="min-h-11 flex-1 border-white/35 bg-transparent text-white hover:bg-white/10 hover:text-white"
                    >
                      Login
                    </Button>
                    <Button
                      type="button"
                      onClick={() => openAuth("signup")}
                      className="min-h-11 flex-1 bg-white font-semibold text-[#1f4e79] hover:bg-[#f1f5f9]"
                    >
                      Start Free Trial
                    </Button>
                  </>
                )}
              </div>
            </motion.div>
          )}
        </div>
      </motion.nav>

      {authOpen && (
        <div
          className="fixed inset-0 z-[100] flex items-end justify-center bg-slate-950/60 backdrop-blur-[2px] sm:items-center sm:p-6"
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
            className="relative max-h-[92dvh] w-full max-w-md overflow-y-auto rounded-t-3xl bg-white px-5 pb-[max(1.25rem,env(safe-area-inset-bottom))] pt-5 text-slate-900 shadow-2xl outline-none sm:rounded-3xl sm:px-6 sm:pb-6"
            role="dialog"
            aria-modal="true"
            aria-labelledby="auth-title"
            tabIndex={-1}
          >
            <button
              type="button"
              onClick={() => setAuthOpen(false)}
              disabled={loading}
              className="absolute right-4 top-4 rounded-full p-2 text-slate-400 transition hover:bg-slate-100 hover:text-slate-700 disabled:opacity-40"
              aria-label="Close"
            >
              <X className="h-5 w-5" />
            </button>

            <p className="text-[11px] font-bold uppercase tracking-[0.16em] text-slate-500">
              PilotVault SA
            </p>
            <h2 id="auth-title" className="mt-1 pr-10 text-xl font-bold tracking-tight text-slate-950">
              {authMode === "login"
                ? "Log in"
                : authMode === "signup"
                  ? "3-day free trial"
                  : "New password"}
            </h2>

            {authNotice && (
              <p
                className="mt-4 rounded-xl border border-[#b8860a]/40 bg-[#fdf3d9] px-4 py-3 text-sm font-semibold text-[#b8860a]"
                role="status"
              >
                {authNotice}
              </p>
            )}

            {authMode !== "reset" && (
              <div
                role="tablist"
                aria-label="Log in or start a free trial"
                className="my-5 grid grid-cols-2 gap-1 rounded-2xl bg-slate-100 p-1"
              >
                <button
                  type="button"
                  disabled={loading}
                  onClick={() => {
                    setAuthMode("login")
                    setAuthMessage("")
                    setAuthNotice("")
                  }}
                  role="tab"
                  aria-selected={authMode === "login"}
                  className={`h-11 rounded-xl text-[15px] font-bold transition ${
                    authMode === "login"
                      ? "bg-white text-slate-950 shadow-[0_1px_3px_rgba(15,23,42,0.18)]"
                      : "text-slate-500 hover:text-slate-900"
                  } disabled:opacity-60`}
                >
                  Log in
                </button>
                <button
                  type="button"
                  disabled={loading}
                  onClick={() => {
                    setAuthMode("signup")
                    setAuthMessage("")
                    setAuthNotice("")
                  }}
                  role="tab"
                  aria-selected={authMode === "signup"}
                  className={`h-11 rounded-xl text-[15px] font-bold transition ${
                    authMode === "signup"
                      ? "bg-white text-slate-950 shadow-[0_1px_3px_rgba(15,23,42,0.18)]"
                      : "text-slate-500 hover:text-slate-900"
                  } disabled:opacity-60`}
                >
                  Free trial
                </button>
              </div>
            )}

            <form
              className={`space-y-3 ${authMode === "reset" ? "mt-5" : ""}`}
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

              <PasswordInput
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
                    {resetRequestLoading ? "Sending..." : "Forgot password?"}
                  </button>
                </div>
              )}

              {(authMode === "signup" || authMode === "reset") && (
                <PasswordInput
                  autoComplete="new-password"
                  aria-label={
                    authMode === "reset" ? "Confirm new password" : "Confirm password"
                  }
                  placeholder={
                    authMode === "reset" ? "Confirm new password" : "Confirm password"
                  }
                  value={confirmPassword}
                  onChange={(event) => setConfirmPassword(event.target.value)}
                  className="w-full rounded-xl border border-slate-300 bg-white px-4 py-3 text-slate-900 placeholder:text-slate-400 focus:border-[#1f4e79] focus:outline-none focus:ring-2 focus:ring-[#d6e6f7]"
                />
              )}

              {authMode !== "reset" && (
                <Turnstile
                  ref={turnstileRef}
                  onToken={setCaptchaToken}
                  onError={setAuthMessage}
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
                disabled={loading || resetRequestLoading || captchaMissing}
                className="h-auto w-full rounded-2xl bg-[var(--pv-navy)] py-3.5 text-base font-bold text-white hover:bg-[var(--pv-navy-soft)] disabled:opacity-60"
              >
                {loading
                  ? "Please wait..."
                  : authMode === "login"
                    ? "Log in"
                    : authMode === "signup"
                      ? "Start free trial"
                      : "Update password"}
              </Button>
            </form>
          </motion.div>
        </div>
      )}

    </>
  )
}
