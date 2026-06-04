import Link from "next/link"

const faqs = [
  {
    question: "What is PilotVault SA?",
    answer:
      "PilotVault SA is a SACAA-focused aviation exam preparation platform designed to help South African student pilots prepare for their theory exams through mock exams, question banks, and explanations.",
  },
  {
    question: "Is PilotVault SA affiliated with SACAA?",
    answer:
      "No. PilotVault SA is an independent educational platform and is not affiliated with, endorsed by, or operated by the South African Civil Aviation Authority (SACAA).",
  },
  {
    question: "How does the free trial work?",
    answer:
      "New users receive a 3-day trial with access to all available subjects and a fixed 25-question mock exam for each subject.",
  },
  {
    question: "What happens when my trial expires?",
    answer:
      "When your trial expires, access to practice content will be restricted until you upgrade to a paid subscription.",
  },
  {
    question: "What do I get with a subscription?",
    answer:
      "Subscribers unlock topic-based practice, expanded mock exams, full question banks, detailed explanations, and future premium features.",
  },
  {
    question: "Can I practice specific topics?",
    answer:
      "Yes. Topic-based practice is available to active subscribers and helps you focus on weak areas within each subject.",
  },
  {
    question: "Do mock exams have a timer?",
    answer:
      "Yes. Mock exams simulate exam conditions with timed sessions, question navigation, scoring, and answer review.",
  },
  {
    question: "Will my progress be saved?",
    answer:
      "PilotVault SA is being developed with progress tracking features that will allow students to monitor performance and identify weak areas.",
  },
  {
    question: "What subjects are available?",
    answer:
      "Current subjects include Air Law, Meteorology, Navigation, Human Performance, Principles of Flight, Aircraft Technical and General, Radio Telephony, and Flight Planning.",
  },
  {
    question: "How do I contact support?",
    answer:
      "Support details can be found on the Contact page. We aim to respond to all enquiries as quickly as possible.",
  },
]

export default function FAQPage() {
  return (
    <main className="min-h-screen bg-[#06111f] text-white">
      <header className="border-b border-[#1e3a5f] bg-[#06111f]/95">
        <div className="mx-auto flex min-h-20 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
          <div>
            <p className="text-xs uppercase tracking-[0.25em] text-[#f4b400]">
              PilotVault SA
            </p>
            <h1 className="mt-1 text-lg font-bold">
              Frequently Asked Questions
            </h1>
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
        <div className="text-center">
          <p className="text-xs uppercase tracking-[0.3em] text-[#f4b400]">
            Help Center
          </p>

          <h2 className="mt-4 text-4xl font-bold sm:text-5xl">
            Frequently Asked Questions
          </h2>

          <p className="mx-auto mt-5 max-w-2xl text-lg leading-8 text-gray-400">
            Find answers to common questions about PilotVault SA,
            subscriptions, mock exams, and SACAA exam preparation.
          </p>
        </div>

        <div className="mt-12 space-y-5">
          {faqs.map((faq) => (
            <div
              key={faq.question}
              className="rounded-3xl border border-[#1e3a5f] bg-[#081726] p-6"
            >
              <h3 className="text-lg font-bold text-white">
                {faq.question}
              </h3>

              <p className="mt-3 leading-7 text-gray-400">
                {faq.answer}
              </p>
            </div>
          ))}
        </div>

        <div className="mt-12 rounded-3xl border border-[#f4b400]/30 bg-[#f4b400]/10 p-6 text-center sm:p-8">
          <h3 className="text-2xl font-bold">
            Still have questions?
          </h3>

          <p className="mx-auto mt-3 max-w-2xl text-gray-300">
            Visit our Contact page and we'll be happy to assist you.
          </p>

          <Link
            href="/contact"
            className="mt-6 inline-flex rounded-xl bg-[#f4b400] px-6 py-3 text-sm font-bold text-[#06111f] transition hover:bg-[#d9a000]"
          >
            Contact Support
          </Link>
        </div>
      </section>
    </main>
  )
}