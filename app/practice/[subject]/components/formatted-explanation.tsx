"use client"

type Section = {
  label: string
  suffix: string | null
  body: string
}

const SECTION_HEADERS = ["GIVEN", "CONCEPT", "FORMULA", "METHOD", "SOLVE", "ANSWER"]

// Matches a header line like "METHOD" or "METHOD (CRP-5 Flight Computer)" on its own line.
const HEADER_LINE = new RegExp(`^(${SECTION_HEADERS.join("|")})(\\s*\\(([^)]+)\\))?\\s*$`)

const SECTION_STYLES: Record<string, { chip: string; border: string; bg: string }> = {
  GIVEN: { chip: "bg-slate-600 text-white", border: "border-slate-300", bg: "bg-slate-50" },
  CONCEPT: { chip: "bg-indigo-600 text-white", border: "border-indigo-200", bg: "bg-indigo-50" },
  FORMULA: { chip: "bg-purple-600 text-white", border: "border-purple-200", bg: "bg-purple-50" },
  METHOD: { chip: "bg-[#1f4e79] text-white", border: "border-blue-200", bg: "bg-blue-50" },
  SOLVE: { chip: "bg-amber-600 text-white", border: "border-amber-200", bg: "bg-amber-50" },
  ANSWER: { chip: "bg-green-700 text-white", border: "border-green-300", bg: "bg-green-50" },
}

function parseSections(text: string): Section[] | null {
  const lines = text.split("\n")
  const sections: Section[] = []
  let current: Section | null = null

  for (const rawLine of lines) {
    const match = rawLine.trim().match(HEADER_LINE)
    if (match) {
      if (current) sections.push(current)
      current = { label: match[1], suffix: match[3] ?? null, body: "" }
    } else if (current) {
      current.body += (current.body ? "\n" : "") + rawLine
    } else if (rawLine.trim()) {
      // Content before any recognized header — not a structured explanation.
      return null
    }
  }
  if (current) sections.push(current)

  return sections.length > 0 ? sections : null
}

// Bolds inline annotations like "Exam tip:", "Rough check:", "Trap:" within a body of text.
function renderBody(body: string) {
  const trimmed = body.trim()
  const parts = trimmed.split(/(Exam tip:|Rough check:|Trap:)/g)
  return parts.map((part, i) =>
    part === "Exam tip:" || part === "Rough check:" || part === "Trap:" ? (
      <strong key={i} className="font-semibold text-slate-900">
        {part}
      </strong>
    ) : (
      part
    ),
  )
}

export function FormattedExplanation({ text }: { text: string }) {
  const sections = parseSections(text)

  if (!sections) {
    return <p className="mt-2 whitespace-pre-line leading-relaxed text-slate-700">{text}</p>
  }

  return (
    <div className="mt-3 space-y-3">
      {sections.map((section, i) => {
        const style = SECTION_STYLES[section.label] ?? SECTION_STYLES.GIVEN
        return (
          <div key={i} className={`rounded-md border ${style.border} ${style.bg} p-4`}>
            <div className="flex flex-wrap items-center gap-2">
              <span className={`rounded px-2 py-0.5 text-xs font-bold tracking-wide ${style.chip}`}>
                {section.label}
              </span>
              {section.suffix && <span className="text-xs font-medium text-slate-500">{section.suffix}</span>}
            </div>
            <p
              className={
                section.label === "ANSWER"
                  ? "mt-2 whitespace-pre-line text-lg font-bold leading-relaxed text-green-900"
                  : "mt-2 whitespace-pre-line leading-relaxed text-slate-700"
              }
            >
              {renderBody(section.body)}
            </p>
          </div>
        )
      })}
    </div>
  )
}
