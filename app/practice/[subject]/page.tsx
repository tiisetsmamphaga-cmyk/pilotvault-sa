"use client";

import { useParams } from "next/navigation";
import Link from "next/link";

export default function SubjectPracticePage() {
  const params = useParams();

  const subject = params.subject;

  return (
    <main className="min-h-screen bg-[#06111f] text-white px-6 py-10">
      <div className="max-w-4xl mx-auto">
        <Link
          href="/practice"
          className="inline-block mb-8 text-sm text-[#d4af37] hover:text-white transition"
        >
          ← Back to Practice
        </Link>

        <h1 className="text-4xl font-bold capitalize mb-4">
          {String(subject).replaceAll("-", " ")}
        </h1>

        <p className="text-white/70 mb-10">
          SACAA exam practice questions will appear here.
        </p>

        <div className="rounded-2xl border border-[#1e3a5f] bg-[#081726] p-6">
          <h2 className="text-xl font-semibold mb-4">
            Sample Question
          </h2>

          <p className="mb-6">
            What cloud type is associated with thunderstorms?
          </p>

          <div className="space-y-3">
            <button className="w-full rounded-xl border border-[#1e3a5f] p-4 text-left hover:border-[#d4af37] transition">
              Stratus
            </button>

            <button className="w-full rounded-xl border border-[#1e3a5f] p-4 text-left hover:border-[#d4af37] transition">
              Cumulonimbus
            </button>

            <button className="w-full rounded-xl border border-[#1e3a5f] p-4 text-left hover:border-[#d4af37] transition">
              Cirrus
            </button>

            <button className="w-full rounded-xl border border-[#1e3a5f] p-4 text-left hover:border-[#d4af37] transition">
              Altostratus
            </button>
          </div>
        </div>
      </div>
    </main>
  );
}