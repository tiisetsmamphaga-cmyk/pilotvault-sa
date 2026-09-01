"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { CreditCard, Gauge, GraduationCap, UserRound } from "lucide-react"

const items = [
  { label: "Dashboard", href: "/dashboard", icon: Gauge },
  { label: "Practice", href: "/practice", icon: GraduationCap },
  { label: "Plans", href: "/upgrade", icon: CreditCard },
  { label: "Profile", href: "/profile", icon: UserRound },
]

const supportedRoutes = new Set(["/dashboard", "/practice", "/upgrade", "/profile"])

export function AppMobileNavigation() {
  const pathname = usePathname()

  if (!supportedRoutes.has(pathname)) return null

  return (
    <>
      <div aria-hidden="true" className="h-[72px] md:hidden" />
      <nav
        aria-label="Student navigation"
        className="fixed inset-x-0 bottom-0 z-[70] border-t border-slate-200 bg-white/96 px-2 pb-[max(0.35rem,env(safe-area-inset-bottom))] pt-1.5 shadow-[0_-8px_24px_rgba(15,23,42,0.08)] backdrop-blur md:hidden"
      >
        <div className="mx-auto grid max-w-md grid-cols-4">
          {items.map((item) => {
            const Icon = item.icon
            const active = pathname === item.href

            return (
              <Link
                key={item.href}
                href={item.href}
                aria-current={active ? "page" : undefined}
                className={`flex min-h-[52px] flex-col items-center justify-center gap-1 rounded-lg px-1 text-[10px] font-semibold transition focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#1f4e79]/40 ${
                  active
                    ? "text-[#1f4e79]"
                    : "text-slate-500 hover:bg-slate-50 hover:text-slate-900"
                }`}
              >
                <span
                  className={`flex h-7 w-9 items-center justify-center rounded-lg transition ${
                    active ? "bg-[#d6e6f7]" : "bg-transparent"
                  }`}
                >
                  <Icon className="h-[18px] w-[18px]" aria-hidden="true" />
                </span>
                <span>{item.label}</span>
              </Link>
            )
          })}
        </div>
      </nav>
    </>
  )
}
