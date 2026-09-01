import { Footer } from "@/components/footer"
import { Navbar } from "@/components/navbar"

const sections = [
  {
    title: "Acceptance of Terms",
    body: "By using PilotVault SA, you agree to comply with these Terms and Conditions and all applicable laws and regulations.",
  },
  {
    title: "Educational Purpose",
    body: "PilotVault SA is an independent aviation exam preparation platform designed to assist students in preparing for SACAA examinations. PilotVault SA is not affiliated with, endorsed by, or operated by the South African Civil Aviation Authority (SACAA).",
  },
  {
    title: "Account Responsibility",
    body: "Users are responsible for maintaining the confidentiality of their login credentials and all activity occurring under their account.",
  },
  {
    title: "Free Trial",
    body: "PilotVault SA may provide a limited free trial. Trial access includes restricted content and features. Trial access may expire automatically after the designated trial period.",
  },
  {
    title: "Subscriptions",
    body: "Access to premium content and features requires an active paid subscription. Subscription plans, pricing, and available features may change from time to time.",
  },
  {
    title: "Payments",
    body: "Payments are processed securely through approved payment providers. Access to premium services may be suspended if payment is unsuccessful or reversed.",
  },
  {
    title: "Refund Policy",
    body: "Refund requests may be reviewed on a case-by-case basis. PilotVault SA reserves the right to determine eligibility for refunds in accordance with applicable laws and payment provider requirements.",
  },
  {
    title: "Intellectual Property",
    body: "All platform content, branding, software, graphics, explanations, and study materials remain the property of PilotVault SA unless otherwise stated. Unauthorized copying, redistribution, or commercial use is prohibited.",
  },
  {
    title: "Limitation of Liability",
    body: "PilotVault SA provides educational resources only and does not guarantee examination results. Users remain responsible for their own preparation, decisions, and performance.",
  },
  {
    title: "Termination",
    body: "PilotVault SA reserves the right to suspend or terminate accounts that violate these terms, misuse the platform, or engage in fraudulent activity.",
  },
  {
    title: "Changes to These Terms",
    body: "PilotVault SA may update these Terms and Conditions from time to time. Continued use of the platform constitutes acceptance of the updated terms.",
  },
  {
    title: "Contact",
    body: "Questions regarding these Terms and Conditions may be directed to PilotVault SA support.",
  },
]

export default function TermsPage() {
  return (
    <main className="min-h-screen bg-[#eef3f8] text-slate-900">
      <Navbar />

      <section className="mx-auto max-w-5xl px-4 pb-12 pt-32 sm:px-6 sm:pb-16 lg:px-8">
        <div className="rounded-2xl border border-slate-200 bg-[#f8fafc] p-6 sm:p-10">
          <p className="text-xs font-semibold uppercase tracking-[0.3em] text-[#1f4e79]">
            Last Updated
          </p>
          <p className="mt-2 text-slate-500">June 2026</p>
          <h1 className="mt-6 text-4xl font-bold tracking-tight text-slate-900">
            Terms &amp; Conditions
          </h1>
          <p className="mt-6 leading-8 text-slate-600">
            These Terms and Conditions govern your access to and use of
            PilotVault SA. By creating an account, accessing the platform, or
            subscribing to a paid plan, you agree to these terms.
          </p>
        </div>

        <div className="mt-8 space-y-6">
          {sections.map((section) => (
            <article
              key={section.title}
              className="rounded-2xl border border-slate-200 bg-[#f8fafc] p-6"
            >
              <h2 className="text-xl font-bold text-slate-900">{section.title}</h2>
              <p className="mt-4 leading-7 text-slate-600">{section.body}</p>
            </article>
          ))}
        </div>
      </section>

      <Footer />
    </main>
  )
}
