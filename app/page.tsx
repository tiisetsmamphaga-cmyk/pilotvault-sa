import { Navbar } from "@/components/navbar"
import { HeroSection } from "@/components/hero-section"
import { ExamPreviewSection } from "@/components/exam-preview-section"
import { SubjectsSection } from "@/components/subjects-section"
import { PricingSection } from "@/components/pricing-section"
import { CtaSection } from "@/components/cta-section"
import { Footer } from "@/components/footer"

export default function Home() {
  return (
    <main className="min-h-screen bg-[#06111f]">
      <Navbar />
      <HeroSection />
      <ExamPreviewSection />
      <SubjectsSection />
      <PricingSection />
      <CtaSection />
      <Footer />
    </main>
  )
}