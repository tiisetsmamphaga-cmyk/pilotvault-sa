"use client"

import { isEquationLine, MathLine } from "./math-text"

type Section = {
  label: string
  suffix: string | null
  body: string
}

const SECTION_HEADERS = ["GIVEN", "CONCEPT", "RULE", "FORMULA", "METHOD", "WORKING", "SOLVE", "REASONING", "ANSWER"]

// Matches a header line like "METHOD" or "METHOD (CRP-5 Flight Computer)" on its own line.
const HEADER_LINE = new RegExp(`^(${SECTION_HEADERS.join("|")})(\\s*\\(([^)]+)\\))?\\s*$`)

const SECTION_LABEL_COLOR: Record<string, string> = {
  GIVEN: "text-slate-500",
  CONCEPT: "text-indigo-600",
  RULE: "text-indigo-600",
  FORMULA: "text-purple-600",
  METHOD: "text-[#1f4e79]",
  WORKING: "text-[#1f4e79]",
  SOLVE: "text-amber-700",
  REASONING: "text-teal-700",
  ANSWER: "text-green-700",
}

const SECTION_CARD_STYLES: Record<string, { chip: string; border: string; bg: string }> = {
  GIVEN: { chip: "bg-slate-600 text-white", border: "border-slate-300", bg: "bg-slate-50" },
  CONCEPT: { chip: "bg-indigo-600 text-white", border: "border-indigo-200", bg: "bg-indigo-50" },
  RULE: { chip: "bg-indigo-600 text-white", border: "border-indigo-200", bg: "bg-indigo-50" },
  FORMULA: { chip: "bg-purple-600 text-white", border: "border-purple-200", bg: "bg-purple-50" },
  METHOD: { chip: "bg-[#1f4e79] text-white", border: "border-blue-200", bg: "bg-blue-50" },
  WORKING: { chip: "bg-[#1f4e79] text-white", border: "border-blue-200", bg: "bg-blue-50" },
  SOLVE: { chip: "bg-amber-600 text-white", border: "border-amber-200", bg: "bg-amber-50" },
  REASONING: { chip: "bg-teal-600 text-white", border: "border-teal-200", bg: "bg-teal-50" },
  ANSWER: { chip: "bg-green-700 text-white", border: "border-green-300", bg: "bg-green-50" },
}

// Whiz-wheel (CRP-5 flight computer) explanations keep the older card layout; everything else flows as plain labeled text.
function isWhizWheel(sections: Section[]) {
  return sections.some((s) => s.suffix && /crp-5|flight computer/i.test(s.suffix))
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

// Sections that hold worked sums: their equation lines are set as school-style maths.
const MATH_SECTIONS = new Set(["FORMULA", "METHOD", "WORKING", "SOLVE"])

// Bolds inline annotations like "Exam tip:", "Rough check:", "Trap:" within a body of text.
function renderText(text: string, key: string) {
  const parts = text.split(/(Exam tip:|Rough check:|Trap:)/g)
  return parts.map((part, i) =>
    part === "Exam tip:" || part === "Rough check:" || part === "Trap:" ? (
      <strong key={`${key}-${i}`} className="font-semibold text-slate-900">
        {part}
      </strong>
    ) : (
      part
    ),
  )
}

// In maths sections each line is its own row, so a sum set as a fraction gets its own height and a blank line
// between steps is a small, even gap rather than a whole empty line.
function renderBody(body: string, label?: string) {
  const trimmed = body.trim()
  if (!label || !MATH_SECTIONS.has(label)) return renderText(trimmed, "t")
  return trimmed.split("\n").map((line, i) =>
    line.trim() === "" ? (
      <span key={i} className="block h-3" aria-hidden />
    ) : (
      <span key={i} className="block">
        {isEquationLine(line) && !/Exam tip:|Rough check:|Trap:/.test(line) ? <MathLine line={line} /> : renderText(line, `l${i}`)}
      </span>
    ),
  )
}

// The ANSWER section's first line is the answer; anything after it (an exam tip) is ordinary text.
function splitAnswer(body: string) {
  const lines = body.trim().split("\n")
  return { answer: lines[0], rest: lines.slice(1).join("\n").trim() }
}

function AnswerBody({ body, className }: { body: string; className: string }) {
  const { answer, rest } = splitAnswer(body)
  return (
    <>
      <p className={className}>{answer}</p>
      {rest && <p className="mt-2 whitespace-pre-line leading-relaxed text-slate-700">{renderText(rest, "a")}</p>}
    </>
  )
}

// children (e.g. a KEY FACT section) render inside the same box, under the text.
export function FormattedExplanation({ text, children }: { text: string; children?: React.ReactNode }) {
  const sections = parseSections(text)

  if (!sections) {
    return (
      <div className="mt-3 rounded-lg border border-slate-200 bg-slate-50 p-5">
        <p className="whitespace-pre-line leading-relaxed text-slate-700">{text}</p>
        {children}
      </div>
    )
  }

  if (isWhizWheel(sections)) {
    return (
      <div className="mt-3 space-y-3">
        {sections.map((section, i) => {
          const style = SECTION_CARD_STYLES[section.label] ?? SECTION_CARD_STYLES.GIVEN
          return (
            <div key={i} className={`rounded-md border ${style.border} ${style.bg} p-4`}>
              <div className="flex flex-wrap items-center gap-2">
                <span className={`rounded px-2 py-0.5 text-xs font-bold tracking-wide ${style.chip}`}>
                  {section.label}
                </span>
                {section.suffix && <span className="text-xs font-medium text-slate-500">{section.suffix}</span>}
              </div>
              {section.label === "ANSWER" ? (
                <AnswerBody body={section.body} className="mt-2 text-lg font-bold leading-relaxed text-green-900" />
              ) : (
                <p className="mt-2 whitespace-pre-line leading-relaxed text-slate-700">
                  {renderBody(section.body, section.label)}
                </p>
              )}
            </div>
          )
        })}
        {children}
      </div>
    )
  }

  return (
    <div className="mt-3 space-y-4 rounded-lg border border-slate-200 bg-slate-50 p-5">
      {sections.map((section, i) => {
        const labelColor = SECTION_LABEL_COLOR[section.label] ?? SECTION_LABEL_COLOR.GIVEN
        return (
          <div key={i}>
            <div className="flex flex-wrap items-baseline gap-2">
              <span className={`text-xs font-bold tracking-wide ${labelColor}`}>{section.label}</span>
              {section.suffix && <span className="text-xs font-medium text-slate-400">{section.suffix}</span>}
            </div>
            {section.label === "ANSWER" ? (
              <AnswerBody body={section.body} className="mt-1 text-lg font-bold leading-relaxed text-green-800" />
            ) : (
              <p className="mt-1 whitespace-pre-line leading-relaxed text-slate-700">
                {renderBody(section.body, section.label)}
              </p>
            )}
          </div>
        )
      })}
      {children}
    </div>
  )
}
