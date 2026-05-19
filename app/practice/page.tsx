import Link from "next/link"

const subjects = [
  "Air Law",
  "Meteorology",
  "Navigation",
  "Human Performance",
  "Principles of Flight",
  "Aircraft Technical",
  "Radio Telephony",
  "Flight Planning",
]

export default function PracticePage() {
  return (
    <main className="min-h-screen bg-[#06111f] text-white px-6 py-10">
      <div className="max-w-6xl mx-auto">
        <Link
          href="/dashboard"
          className="inline-block mb-8 text-sm text-[#f4b400] hover:text-white transition"
        >
          ← Back to Dashboard
        </Link>

        <p className="text-[#f4b400] text-xs uppercase tracking-[0.18em]">
          Practice Mode
        </p>

        <h1 className="mt-3 text-4xl md:text-5xl font-bold">
          Choose a Subject
        </h1>

        <p className="mt-4 text-gray-400 max-w-2xl">
          Select a SACAA subject and start practicing exam-style questions with
          explanations.
        </p>

        <div className="mt-10 grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
          {subjects.map((subject) => {
            const slug = subject.toLowerCase().replaceAll(" ", "-")

            return (
              <Link
                key={subject}
                href={`/practice/${slug}`}
                className="rounded-2xl border border-[#1e3a5f] bg-[#081726] p-6 hover:border-[#f4b400] hover:bg-[#0b1f35] transition"
              >
                <h2 className="text-xl font-bold">{subject}</h2>

                <p className="mt-3 text-sm text-gray-400">
                  Practice realistic SACAA-style questions.
                </p>

                <div className="mt-6 flex items-center justify-between">
                  <span className="text-xs text-gray-500">0 questions</span>
                  <span className="text-sm font-bold text-[#f4b400]">
                    Start →
                  </span>
                </div>
              </Link>
            )
          })}
        </div>
      </div>
    </main>
  )
}