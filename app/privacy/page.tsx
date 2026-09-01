import { Footer } from "@/components/footer"
import { Navbar } from "@/components/navbar"

const sections = [
  {
    title: "Information We Collect",
    body: "We may collect information including:",
    items: [
      "Full name",
      "Email address",
      "Account information",
      "Subscription information",
      "Exam performance and progress data",
      "Device and usage information",
    ],
  },
  {
    title: "How We Use Your Information",
    items: [
      "Create and manage your account",
      "Deliver exam preparation services",
      "Track learning progress and analytics",
      "Improve platform performance",
      "Process subscriptions and payments",
      "Provide customer support",
      "Communicate service updates",
    ],
  },
  {
    title: "Payment Processing",
    body: "Payments are processed securely through trusted third-party payment providers. PilotVault SA does not store or have direct access to your card details.",
  },
  {
    title: "Data Security",
    body: "We take reasonable technical and organizational measures to protect your personal information from unauthorized access, disclosure, loss, or misuse.",
  },
  {
    title: "Data Sharing",
    body: "PilotVault SA does not sell your personal information. Information may only be shared with service providers required to operate the platform, process payments, or comply with legal obligations.",
  },
  {
    title: "Your Rights",
    body: "You may request access to your personal information, correction of inaccurate information, or deletion of your account where legally permitted.",
  },
  {
    title: "Contact",
    body: "If you have questions regarding this Privacy Policy, please contact PilotVault SA support.",
  },
]

export default function PrivacyPolicyPage() {
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
            Privacy Policy
          </h1>
          <p className="mt-6 leading-8 text-slate-600">
            PilotVault SA respects your privacy and is committed to protecting
            your personal information. This Privacy Policy explains how we
            collect, use, store, and protect information when you use the
            PilotVault SA platform.
          </p>
        </div>

        <div className="mt-8 space-y-6">
          {sections.map((section) => (
            <article
              key={section.title}
              className="rounded-2xl border border-slate-200 bg-[#f8fafc] p-6"
            >
              <h2 className="text-xl font-bold text-slate-900">{section.title}</h2>
              {section.body && (
                <p className="mt-4 leading-7 text-slate-600">{section.body}</p>
              )}
              {section.items && (
                <ul className="mt-4 space-y-2 text-slate-600">
                  {section.items.map((item) => (
                    <li key={item}>• {item}</li>
                  ))}
                </ul>
              )}
            </article>
          ))}
        </div>
      </section>

      <Footer />
    </main>
  )
}
