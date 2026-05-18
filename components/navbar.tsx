"use client"

import { useState } from "react"
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

  return (
    <motion.nav
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      transition={{ duration: 0.5 }}
      className="fixed top-0 left-0 right-0 z-50 bg-[#06111f]/95 backdrop-blur-md border-b border-[#1e3a5f]"
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16 lg:h-20">
          {/* Logo */}
          <Link href="#" className="flex items-center">
            <Image
              src="/images/logo.png"
              alt="PilotVault SA"
              width={200}
              height={50}
              className="h-[50px] w-auto"
              priority
            />
          </Link>

          {/* Desktop Navigation */}
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

          {/* Desktop CTA Buttons */}
          <div className="hidden lg:flex items-center gap-4">
            <Button
              variant="outline"
              className="border-[#1e3a5f] text-white hover:bg-[#1e3a5f] hover:text-white"
            >
              Login
            </Button>
            <Button className="bg-[#f4b400] text-[#06111f] hover:bg-[#d9a000] font-semibold">
              Sign Up
            </Button>
          </div>

          {/* Mobile Menu Button */}
          <button
            onClick={() => setIsOpen(!isOpen)}
            className="lg:hidden p-2 text-white"
          >
            {isOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
          </button>
        </div>

        {/* Mobile Menu */}
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
                  variant="outline"
                  className="border-[#1e3a5f] text-white hover:bg-[#1e3a5f] w-full"
                >
                  Login
                </Button>
                <Button className="bg-[#f4b400] text-[#06111f] hover:bg-[#d9a000] font-semibold w-full">
                  Sign Up
                </Button>
              </div>
            </div>
          </motion.div>
        )}
      </div>
    </motion.nav>
  )
}
