"use client"

import Link from "next/link"
import Image from "next/image"
import { Instagram, Mail } from "lucide-react"
import { Button } from "@/components/ui/button"

function TikTokIcon({ className }: { className?: string }) {
  return (
    <svg
      viewBox="0 0 24 24"
      fill="currentColor"
      className={className}
      aria-hidden="true"
    >
      <path d="M16.6 5.82a4.45 4.45 0 0 1-1.09-2.92h-3.38v13.56a2.83 2.83 0 1 1-2.83-2.83c.29 0 .57.04.84.12v-3.45a6.2 6.2 0 1 0 5.37 6.16V9.58a7.8 7.8 0 0 0 4.56 1.46V7.66a4.48 4.48 0 0 1-3.47-1.84Z" />
    </svg>
  )
}

const quickLinks = [
  { name: "Home", href: "/" },
  { name: "Features", href: "/features" },
  { name: "Pricing", href: "/#pricing" },
  { name: "Subjects", href: "/subjects" },
]

const resources = [
  { name: "FAQ", href: "/faq" },
  { name: "Support", href: "mailto:contact@pilotvault.co.za" },
  {
    name: "Contact",
    href: "mailto:contact@pilotvault.co.za",
    detail: "contact@pilotvault.co.za",
  },
]

const socialLinks = [
  { icon: Instagram, label: "Instagram" },
  { icon: TikTokIcon, label: "TikTok" },
]

export function Footer() {
  return (
    <footer id="contact" className="border-t border-slate-800 bg-[#0f1720]">
      <div className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8 lg:py-16">
        <div className="grid grid-cols-1 gap-10 sm:grid-cols-2 lg:grid-cols-4 lg:gap-12">
          <div>
            <Link href="/" className="mb-4 flex">
              <Image
                src="/images/headerlogo.png"
                alt="PilotVault SA"
                width={180}
                height={45}
                className="h-14 w-auto lg:h-20"
              />
            </Link>

            <p className="mb-5 max-w-xs text-sm leading-relaxed text-slate-400">
              Pass your SACAA exams with confidence using realistic practice questions, mock exams and clear explanations.
            </p>

            <div className="flex gap-3">
              {socialLinks.map((social) => (
                <button
                  key={social.label}
                  type="button"
                  disabled
                  aria-label={`${social.label} profile link coming soon`}
                  title={`${social.label} link coming soon`}
                  className="flex h-10 w-10 cursor-default items-center justify-center rounded-lg border border-slate-700 bg-slate-800 text-slate-400"
                >
                  <social.icon className="h-4 w-4" />
                </button>
              ))}
            </div>
          </div>

          <div>
            <h3 className="mb-4 font-semibold text-white">Quick Links</h3>
            <ul className="space-y-3">
              {quickLinks.map((link) => (
                <li key={link.name}>
                  <Link
                    href={link.href}
                    className="text-sm text-slate-400 transition-colors hover:text-white"
                  >
                    {link.name}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h3 className="mb-4 font-semibold text-white">Resources</h3>
            <ul className="space-y-3">
              {resources.map((link) => (
                <li key={link.name}>
                  <Link
                    href={link.href}
                    className="inline-flex flex-wrap items-baseline gap-x-2 text-sm text-slate-400 transition-colors hover:text-white"
                  >
                    <span>{link.name}</span>
                    {"detail" in link && link.detail && (
                      <span className="text-xs text-slate-500">{link.detail}</span>
                    )}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h3 className="mb-4 font-semibold text-white">Newsletter</h3>
            <p className="mb-4 text-sm text-slate-400">Get study tips and PilotVault updates.</p>

            <div className="relative mb-3">
              <Mail className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-500" />
              <input
                type="email"
                placeholder="Your email"
                className="w-full rounded-lg border border-slate-700 bg-slate-800 py-3 pl-10 pr-4 text-sm text-white placeholder:text-slate-500 focus:border-[#1f4e79] focus:outline-none focus:ring-2 focus:ring-[#1f4e79]/25"
              />
            </div>

            <Button className="w-full bg-[#1f4e79] font-semibold text-white hover:bg-[#183d60]">
              Subscribe
            </Button>

            <a
              href="mailto:contact@pilotvault.co.za"
              className="mt-5 inline-flex items-center gap-2 text-sm text-slate-400 transition-colors hover:text-white"
            >
              <Mail className="h-4 w-4 text-blue-300" aria-hidden="true" />
              contact@pilotvault.co.za
            </a>
          </div>
        </div>

        <div className="mt-10 border-t border-slate-800 pt-8">
          <div className="flex flex-col items-center justify-between gap-4 text-center md:flex-row">
            <p className="text-sm text-slate-500">
              © {new Date().getFullYear()} PilotVault SA. All rights reserved.
            </p>

            <div className="flex gap-6">
              <Link href="/privacy" className="text-sm text-slate-500 transition-colors hover:text-slate-300">
                Privacy Policy
              </Link>
              <Link href="/terms" className="text-sm text-slate-500 transition-colors hover:text-slate-300">
                Terms of Service
              </Link>
            </div>
          </div>
        </div>
      </div>
    </footer>
  )
}
