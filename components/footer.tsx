"use client"

import Link from "next/link"
import Image from "next/image"
import {
  Facebook,
  Instagram,
  Linkedin,
  Mail,
} from "lucide-react"
import { Button } from "@/components/ui/button"

const quickLinks = [
  { name: "Home", href: "#" },
  { name: "Features", href: "#features" },
  { name: "Pricing", href: "#pricing" },
  { name: "Subjects", href: "#subjects" },
]

const resources = [
  { name: "FAQ", href: "#" },
  { name: "Support", href: "#" },
  { name: "Contact", href: "#contact" },
]

const socialLinks = [
  { icon: Facebook, href: "#", label: "Facebook" },
  { icon: Instagram, href: "#", label: "Instagram" },
  { icon: Linkedin, href: "#", label: "LinkedIn" },
]

export function Footer() {
  return (
    <footer
      id="contact"
      className="border-t border-[#1e3a5f] bg-[#06111f]"
    >
      <div className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8 lg:py-16">

        <div className="grid grid-cols-1 gap-10 sm:grid-cols-2 lg:grid-cols-4 lg:gap-12">

          {/* Brand */}

          <div>
            <Link href="#" className="mb-4 flex">
              <Image
                src="/images/headerlogo.png"
                alt="PilotVault SA"
                width={180}
                height={45}
                className="h-14 w-auto lg:h-20"
              />
            </Link>

            <p className="mb-5 max-w-xs text-sm leading-relaxed text-gray-400">
              Pass your SACAA exams with confidence using realistic practice questions and mock exams.
            </p>

            <div className="flex gap-3">
              {socialLinks.map((social) => (
                <a
                  key={social.label}
                  href={social.href}
                  aria-label={social.label}
                  className="flex h-10 w-10 items-center justify-center rounded-lg bg-[#1e3a5f] text-gray-400 transition-all hover:bg-[#f4b400] hover:text-[#06111f]"
                >
                  <social.icon className="h-4 w-4" />
                </a>
              ))}
            </div>
          </div>

          {/* Quick Links */}

          <div>
            <h3 className="mb-4 font-semibold text-white">
              Quick Links
            </h3>

            <ul className="space-y-3">
              {quickLinks.map((link) => (
                <li key={link.name}>
                  <Link
                    href={link.href}
                    className="text-sm text-gray-400 transition-colors hover:text-[#f4b400]"
                  >
                    {link.name}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Resources */}

          <div>
            <h3 className="mb-4 font-semibold text-white">
              Resources
            </h3>

            <ul className="space-y-3">
              {resources.map((link) => (
                <li key={link.name}>
                  <Link
                    href={link.href}
                    className="text-sm text-gray-400 transition-colors hover:text-[#f4b400]"
                  >
                    {link.name}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Newsletter */}

          <div>
            <h3 className="mb-4 font-semibold text-white">
              Newsletter
            </h3>

            <p className="mb-4 text-sm text-gray-400">
              Get study tips and PilotVault updates.
            </p>

            <div className="relative mb-3">
              <Mail className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-500" />

              <input
                type="email"
                placeholder="Your email"
                className="w-full rounded-lg border border-[#1e3a5f] bg-[#1e3a5f] py-3 pl-10 pr-4 text-sm text-white placeholder:text-gray-500 focus:border-[#f4b400] focus:outline-none"
              />
            </div>

            <Button className="w-full bg-[#f4b400] font-semibold text-[#06111f] hover:bg-[#d9a000]">
              Subscribe
            </Button>
          </div>

        </div>

        {/* Bottom */}

        <div className="mt-10 border-t border-[#1e3a5f] pt-8">

          <div className="flex flex-col items-center justify-between gap-4 text-center md:flex-row">

            <p className="text-sm text-gray-500">
              © {new Date().getFullYear()} PilotVault SA. All rights reserved.
            </p>

            <div className="flex gap-6">
              <Link
                href="privacy"
                className="text-sm text-gray-500 transition-colors hover:text-gray-300"
              >
                Privacy Policy
              </Link>

              <Link
                href="terms"
                className="text-sm text-gray-500 transition-colors hover:text-gray-300"
              >
                Terms of Service
              </Link>
            </div>

          </div>
        </div>

      </div>
    </footer>
  )
}