import Link from "next/link"

import { Footer } from "@/components/footer"
import { Navbar } from "@/components/navbar"

import { pageMetadata } from "@/lib/seo"
import { PPL_SUBJECTS } from "@/lib/subjects"

export const metadata = pageMetadata({
  title: "SACAA PPL Exam Question Database: All 8 Subjects",
  description:
    "Practise all 8 SACAA PPL subjects: Air Law, Meteorology, Navigation, Human Performance, Principles of Flight, Aircraft General, Radio Telephony and Flight Planning.",
  path: "/subjects",
})

export default function SubjectsPage() {
  return (
    <main className="min-h-screen bg-[#eef3f8] text-slate-900">
      <Navbar />

      <section className="mx-auto max-w-7xl px-4 pb-12 pt-32 sm:px-6 sm:pb-16 lg:px-8">
        <div className="mx-auto max-w-3xl text-center">
          <p className="text-xs font-semibold uppercase tracking-[0.3em] text-[#1f4e79]">
            SACAA Theory Subjects
          </p>
          <h1 className="mt-4 text-4xl font-bold tracking-tight text-slate-900 sm:text-5xl">
            Everything you need to pass your exams.
          </h1>
          <p className="mt-5 text-lg leading-8 text-slate-600">
            PilotVault SA provides preparation material across the core SACAA
            Private Pilot Licence subjects. CPL content is being expanded, with
            the full CPL Pack launching on 1 January 2027.
          </p>
        </div>

        <div className="mt-12 grid gap-6 md:grid-cols-2 lg:grid-cols-4">
          {PPL_SUBJECTS.map((subject) => (
            <Link
              key={subject.slug}
              href={`/subjects/${subject.slug}`}
              className="rounded-2xl border border-slate-200 bg-[#f8fafc] p-6 transition hover:border-[#1f4e79]/40 hover:bg-white"
            >
              <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-[#d6e6f7]">
                <subject.icon className="h-6 w-6 text-[#1f4e79]" />
              </div>
              <h2 className="mt-5 text-lg font-bold text-slate-900">
                {subject.name}
              </h2>
              <p className="mt-3 text-sm leading-6 text-slate-600">
                {subject.summary}
              </p>
              <p className="mt-4 text-sm font-semibold text-[#1f4e79]">
                View topics &rarr;
              </p>
            </Link>
          ))}
        </div>

        <div className="mt-12 rounded-2xl border border-[#1f4e79]/20 bg-[#d6e6f7]/55 p-6 text-center sm:p-8">
          <h2 className="text-2xl font-bold text-slate-900">
            Ready to start preparing?
          </h2>
          <p className="mx-auto mt-3 max-w-2xl text-slate-600">
            Access SACAA-focused mock exams, explanations, and structured
            practice designed for South African student pilots.
          </p>
          <Link
            href="/#pricing"
            className="mt-6 inline-flex min-h-11 items-center justify-center rounded-lg bg-[#1f4e79] px-6 py-3 text-sm font-bold text-white transition hover:bg-[#183d60]"
          >
            View access options
          </Link>
        </div>
      </section>

      <Footer />
    </main>
  )
}
