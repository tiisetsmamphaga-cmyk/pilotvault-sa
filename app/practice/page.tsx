import Link from "next/link"

const subjects = [
  { name: "Meteorology", slug: "meteorology" },
  { name: "Air Law", slug: "air-law" },
  { name: "Navigation", slug: "navigation" },
  { name: "Human Performance", slug: "human-performance" },
]

export default function PracticePage() {
  return (
    <main className="min-h-screen bg-[#06111f] text-white p-10">
      <h1 className="text-4xl font-bold">
        Choose Subject
      </h1>

      <div className="grid grid-cols-2 gap-6 mt-10">
        {subjects.map((subject) => (
          <Link
            key={subject.slug}
            href={`/practice/${subject.slug}`}
            className="rounded-xl border border-[#1e3a5f] bg-[#081726] p-6"
          >
            {subject.name}
          </Link>
        ))}
      </div>
    </main>
  )
}