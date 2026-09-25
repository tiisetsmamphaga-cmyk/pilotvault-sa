import Link from "next/link"
import { notFound } from "next/navigation"
import { Check } from "lucide-react"

import { Footer } from "@/components/footer"
import { Navbar } from "@/components/navbar"

import { SITE_NAME, SITE_URL, pageMetadata } from "@/lib/seo"
import { PPL_SUBJECTS, getPplSubject } from "@/lib/subjects"

export const dynamicParams = false

export function generateStaticParams() {
  return PPL_SUBJECTS.map((subject) => ({ subject: subject.slug }))
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ subject: string }>
}) {
  const subject = getPplSubject((await params).subject)
  if (!subject) return {}

  return pageMetadata({
    title: `SACAA PPL ${subject.name} Practice Questions`,
    description: `Prepare for the SACAA PPL ${subject.name} exam with practice questions on ${subject.searchFocus}. Timed mock exams and detailed explanations. Try it free for 3 days.`,
    path: `/subjects/${subject.slug}`,
  })
}

const PREPARATION = [
  {
    title: "Timed mock exams",
    text: "Practise under exam conditions with a timer, question navigation and a full answer review.",
  },
  {
    title: "Topic-based practice",
    text: "Drill one topic at a time to strengthen your weak areas before exam day.",
  },
  {
    title: "Detailed explanations",
    text: "Understand why each answer is right, not just which option to pick.",
  },
  {
    title: "Track your scores",
    text: "See your mock exam results over time on your dashboard.",
  },
]

export default async function SubjectPage({
  params,
}: {
  params: Promise<{ subject: string }>
}) {
  const subject = getPplSubject((await params).subject)
  if (!subject) notFound()

  const otherSubjects = PPL_SUBJECTS.filter((s) => s.slug !== subject.slug)
  const breadcrumbs = {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    itemListElement: [
      { "@type": "ListItem", position: 1, name: SITE_NAME, item: SITE_URL },
      { "@type": "ListItem", position: 2, name: "Subjects", item: `${SITE_URL}/subjects` },
      {
        "@type": "ListItem",
        position: 3,
        name: subject.name,
        item: `${SITE_URL}/subjects/${subject.slug}`,
      },
    ],
  }

  return (
    <main className="min-h-screen bg-[#eef3f8] text-slate-900">
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify(breadcrumbs).replace(/</g, "\\u003c"),
        }}
      />
      <Navbar />

      <section className="mx-auto max-w-5xl px-4 pb-12 pt-32 sm:px-6 sm:pb-16 lg:px-8">
        <nav aria-label="Breadcrumb" className="text-sm text-slate-500">
          <Link href="/subjects" className="hover:text-[#1f4e79]">
            Subjects
          </Link>
          <span className="mx-2">/</span>
          <span className="text-slate-700">{subject.name}</span>
        </nav>

        <div className="mt-6 flex items-center gap-4">
          <div className="flex h-14 w-14 shrink-0 items-center justify-center rounded-xl bg-[#d6e6f7]">
            <subject.icon className="h-7 w-7 text-[#1f4e79]" />
          </div>
          <p className="text-xs font-semibold uppercase tracking-[0.3em] text-[#1f4e79]">
            SACAA PPL Theory Subject
          </p>
        </div>

        <h1 className="mt-5 text-4xl font-bold tracking-tight text-slate-900 sm:text-5xl">
          SACAA PPL {subject.name} practice questions
        </h1>
        <p className="mt-5 max-w-3xl text-lg leading-8 text-slate-600">
          {subject.intro}
        </p>

        <div className="mt-8 flex flex-col gap-3 sm:flex-row">
          <Link
            href="/#pricing"
            className="inline-flex min-h-11 items-center justify-center rounded-lg bg-[#1f4e79] px-6 py-3 text-sm font-bold text-white transition hover:bg-[#183d60]"
          >
            Start your 3-day free trial
          </Link>
          <Link
            href="/subjects"
            className="inline-flex min-h-11 items-center justify-center rounded-lg border border-[#1f4e79] bg-white px-6 py-3 text-sm font-bold text-[#1f4e79] transition hover:bg-[#f1f5f9]"
          >
            All subjects
          </Link>
        </div>

        <div className="mt-12 rounded-2xl border border-slate-200 bg-[#f8fafc] p-6 sm:p-8">
          <h2 className="text-2xl font-bold text-slate-900">
            {subject.name} topics covered
          </h2>
          <ul className="mt-6 grid gap-3 sm:grid-cols-2">
            {subject.topics.map((topic) => (
              <li key={topic} className="flex items-start gap-3 text-slate-700">
                <Check className="mt-0.5 h-5 w-5 shrink-0 text-[#1f4e79]" aria-hidden="true" />
                <span>{topic}</span>
              </li>
            ))}
          </ul>
        </div>

        <div className="mt-8">
          <h2 className="text-2xl font-bold text-slate-900">
            How you&apos;ll prepare for {subject.name}
          </h2>
          <div className="mt-6 grid gap-4 sm:grid-cols-2">
            {PREPARATION.map((item) => (
              <div
                key={item.title}
                className="rounded-2xl border border-slate-200 bg-white p-6"
              >
                <h3 className="font-bold text-slate-900">{item.title}</h3>
                <p className="mt-2 text-sm leading-6 text-slate-600">{item.text}</p>
              </div>
            ))}
          </div>
        </div>

        <div className="mt-12">
          <h2 className="text-xl font-bold text-slate-900">Other PPL subjects</h2>
          <div className="mt-4 flex flex-wrap gap-2">
            {otherSubjects.map((other) => (
              <Link
                key={other.slug}
                href={`/subjects/${other.slug}`}
                className="rounded-full border border-slate-200 bg-white px-4 py-2 text-sm font-medium text-slate-700 transition hover:border-[#1f4e79]/40 hover:text-[#1f4e79]"
              >
                {other.name}
              </Link>
            ))}
          </div>
        </div>
      </section>

      <Footer />
    </main>
  )
}
