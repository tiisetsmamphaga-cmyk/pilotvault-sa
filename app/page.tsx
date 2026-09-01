import { Navbar } from "@/components/navbar"
import { HeroSection } from "@/components/hero-section"
import { PricingSection } from "@/components/pricing-section"
import { CtaSection } from "@/components/cta-section"
import { Footer } from "@/components/footer"

export default function Home() {
  return (
    <main className="min-h-screen bg-[#eef3f8] text-slate-900">
      <Navbar />
      <HeroSection />
      <PricingSection />
      <CtaSection />
      <Footer />
    </main>
  )
}
