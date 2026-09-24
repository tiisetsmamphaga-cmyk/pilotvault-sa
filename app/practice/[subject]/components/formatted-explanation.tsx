"use client"

type Section = {
  label: string
  suffix: string | null
  body: string
}

const SECTION_HEADERS = ["GIVEN", "CONCEPT", "FORMULA", "METHOD", "WORKING", "SOLVE", "REASONING", "ANSWER"]

// Matches a header line like "METHOD" or "METHOD (CRP-5 Flight Computer)" on its own line.
const HEADER_LINE = new RegExp(`^(${SECTION_HEADERS.join("|")})(\\s*\\(([^)]+)\\))?\\s*$`)

const SECTION_LABEL_COLOR: Record<string, string> = {
  GIVEN: "text-slate-500",
  CONCEPT: "text-indigo-600",
  FORMULA: "text-purple-600",
  METHOD: "text-[#1f4e79]",
  WORKING: "text-[#1f4e79]",
  SOLVE: "text-amber-700",
  REASONING: "text-teal-700",
  ANSWER: "text-green-700",
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
    <div className="mt-3 space-y-4">
      {sections.map((section, i) => {
        const labelColor = SECTION_LABEL_COLOR[section.label] ?? SECTION_LABEL_COLOR.GIVEN
        return (
          <div key={i}>
            <div className="flex flex-wrap items-baseline gap-2">
              <span className={`text-xs font-bold tracking-wide ${labelColor}`}>{section.label}</span>
              {section.suffix && <span className="text-xs font-medium text-slate-400">{section.suffix}</span>}
            </div>
            <p
              className={
                section.label === "ANSWER"
                  ? "mt-1 whitespace-pre-line text-lg font-bold leading-relaxed text-green-800"
                  : "mt-1 whitespace-pre-line leading-relaxed text-slate-700"
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
