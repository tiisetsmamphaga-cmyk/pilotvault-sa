import Link from "next/link"

export default function PrivacyPolicyPage() {
  return (
    <main className="min-h-screen bg-[#06111f] text-white">
      <header className="border-b border-[#1e3a5f] bg-[#06111f]/95">
        <div className="mx-auto flex min-h-20 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
          <div>
            <p className="text-xs uppercase tracking-[0.25em] text-[#f4b400]">
              PilotVault SA
            </p>
            <h1 className="mt-1 text-lg font-bold">Privacy Policy</h1>
          </div>

          <Link
            href="/"
            className="rounded-xl border border-[#1e3a5f] px-4 py-3 text-sm text-gray-300 transition hover:border-[#f4b400] hover:text-[#f4b400]"
          >
            Back Home
          </Link>
        </div>
      </header>

      <section className="mx-auto max-w-5xl px-4 py-12 sm:px-6 lg:px-8">
        <div className="rounded-3xl border border-[#1e3a5f] bg-[#081726] p-6 sm:p-10">
          <p className="text-xs uppercase tracking-[0.3em] text-[#f4b400]">
            Last Updated
          </p>

          <p className="mt-2 text-gray-400">
            June 2026
          </p>

          <h2 className="mt-6 text-4xl font-bold">
            Privacy Policy
          </h2>

          <p className="mt-6 text-gray-400 leading-8">
            PilotVault SA respects your privacy and is committed to protecting
            your personal information. This Privacy Policy explains how we
            collect, use, store, and protect information when you use the
            PilotVault SA platform.
          </p>
        </div>

        <div className="mt-8 space-y-6">
          <div className="rounded-3xl border border-[#1e3a5f] bg-[#081726] p-6">
            <h3 className="text-xl font-bold">
              Information We Collect
            </h3>

            <p className="mt-4 text-gray-400 leading-7">
              We may collect information including:
            </p>

            <ul className="mt-4 space-y-2 text-gray-400">
              <li>• Full name</li>
              <li>• Email address</li>
              <li>• Account information</li>
              <li>• Subscription information</li>
              <li>• Exam performance and progress data</li>
              <li>• Device and usage information</li>
            </ul>
          </div>

          <div className="rounded-3xl border border-[#1e3a5f] bg-[#081726] p-6">
            <h3 className="text-xl font-bold">
              How We Use Your Information
            </h3>

            <ul className="mt-4 space-y-2 text-gray-400">
              <li>• Create and manage your account</li>
              <li>• Deliver exam preparation services</li>
              <li>• Track learning progress and analytics</li>
              <li>• Improve platform performance</li>
              <li>• Process subscriptions and payments</li>
              <li>• Provide customer support</li>
              <li>• Communicate service updates</li>
            </ul>
          </div>

          <div className="rounded-3xl border border-[#1e3a5f] bg-[#081726] p-6">
            <h3 className="text-xl font-bold">
              Payment Processing
            </h3>

            <p className="mt-4 text-gray-400 leading-7">
              Payments are processed securely through trusted third-party
              payment providers. PilotVault SA does not store or have direct
              access to your card details.
            </p>
          </div>

          <div className="rounded-3xl border border-[#1e3a5f] bg-[#081726] p-6">
            <h3 className="text-xl font-bold">
              Data Security
            </h3>

            <p className="mt-4 text-gray-400 leading-7">
              We take reasonable technical and organizational measures to
              protect your personal information from unauthorized access,
              disclosure, loss, or misuse.
            </p>
          </div>

          <div className="rounded-3xl border border-[#1e3a5f] bg-[#081726] p-6">
            <h3 className="text-xl font-bold">
              Data Sharing
            </h3>

            <p className="mt-4 text-gray-400 leading-7">
              PilotVault SA does not sell your personal information. Information
              may only be shared with service providers required to operate the
              platform, process payments, or comply with legal obligations.
            </p>
          </div>

          <div className="rounded-3xl border border-[#1e3a5f] bg-[#081726] p-6">
            <h3 className="text-xl font-bold">
              Your Rights
            </h3>

            <p className="mt-4 text-gray-400 leading-7">
              You may request access to your personal information, correction of
              inaccurate information, or deletion of your account where legally
              permitted.
            </p>
          </div>

          <div className="rounded-3xl border border-[#1e3a5f] bg-[#081726] p-6">
            <h3 className="text-xl font-bold">
              Contact
            </h3>

            <p className="mt-4 text-gray-400 leading-7">
              If you have questions regarding this Privacy Policy, please
              contact PilotVault SA support.
            </p>
          </div>
        </div>
      </section>
    </main>
  )
}