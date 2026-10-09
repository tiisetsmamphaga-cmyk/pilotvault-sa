// School-style maths for worked calculations: "a ÷ b" becomes a stacked fraction, and equation lines are set in a
// serif maths face, so "ROC = 7500 ÷ 16 = 469 fpm" reads like it would on paper. The explanation text stays plain
// (÷, ×, −), so anything this cannot parse still reads correctly as typed.

type MathNode = string | { num: MathNode[]; den: MathNode[] }

const MINUS = /^(−| - )/

// Matching ")" for the "(" at i, or -1.
function closing(s: string, i: number) {
  let depth = 0
  for (let j = i; j < s.length; j++) {
    if (s[j] === "(") depth++
    else if (s[j] === ")" && --depth === 0) return j
  }
  return -1
}

function stripParens(s: string) {
  const t = s.trim()
  return t.startsWith("(") && closing(t, 0) === t.length - 1 ? t.slice(1, -1).trim() : t
}

// Where the numerator of a "÷" at the end of `left` starts: back to the nearest + or − (a × b ÷ c is (a × b) / c),
// an unmatched "(", or the start of the expression.
function numeratorStart(left: string) {
  let depth = 0
  for (let j = left.length - 1; j >= 0; j--) {
    const c = left[j]
    if (c === ")") depth++
    else if (c === "(") {
      if (depth === 0) return j + 1
      depth--
    } else if (depth === 0 && (c === "+" || c === "−" || (c === "-" && left[j - 1] === " " && left[j + 1] === " "))) {
      return j + 1
    }
  }
  return 0
}

// Where the denominator of a "÷" at the start of `right` ends: the next ×, +, −, an unmatched ")", or a clause
// break (", " or ";") — a ÷ b × c is (a / b) × c.
function denominatorEnd(right: string) {
  let depth = 0
  for (let j = 0; j < right.length; j++) {
    const c = right[j]
    if (c === "(") depth++
    else if (c === ")") {
      if (depth === 0) return j
      depth--
    } else if (depth === 0) {
      if (c === "×" || c === "+" || c === "−" || c === ";") return j
      if (c === "," && right[j + 1] === " ") return j
      if (MINUS.test(right.slice(j)) && c === " " && j > 0) return j
    }
  }
  return right.length
}

function topLevelDivide(s: string) {
  let depth = 0
  for (let j = 0; j < s.length; j++) {
    if (s[j] === "(") depth++
    else if (s[j] === ")") depth--
    else if (s[j] === "÷" && depth === 0) return j
  }
  return -1
}

export function parseMath(s: string): MathNode[] {
  const i = topLevelDivide(s)
  if (i >= 0) {
    const left = s.slice(0, i)
    const right = s.slice(i + 1)
    const a = numeratorStart(left)
    const b = denominatorEnd(right)
    const num = stripParens(left.slice(a))
    const den = stripParens(right.slice(0, b))
    if (num && den) {
      const before = left.slice(0, a)
      const after = right.slice(b)
      return [...(before ? parseMath(before) : []), { num: parseMath(num), den: parseMath(den) }, " ",
        ...(after ? parseMath(after) : [])]
    }
  }
  // no top-level ÷: look inside brackets; a bracket holding only a fraction loses its brackets
  const out: MathNode[] = []
  let text = ""
  for (let j = 0; j < s.length; j++) {
    if (s[j] === "(") {
      const k = closing(s, j)
      const inner = k > 0 ? s.slice(j + 1, k) : ""
      if (k > 0 && inner.includes("÷")) {
        if (text) out.push(text)
        text = ""
        const parsed = parseMath(inner)
        const onlyFraction = parsed.filter((n) => typeof n !== "string" || n.trim()).length === 1 &&
          parsed.some((n) => typeof n !== "string")
        out.push(...(onlyFraction ? parsed : ["(", ...parsed, ")"]))
        j = k
        continue
      }
    }
    text += s[j]
  }
  if (text) out.push(text)
  return out
}

// A working line is a short sum: it has "=", "≈" or "÷" and is not a sentence (long, or broken up with ";").
export function isEquationLine(line: string) {
  const t = line.trim()
  return (/\s[=≈]\s/.test(t) || t.includes("÷")) && t.length <= 80 && !t.includes(";")
}

// Older text types "x" for times and a spaced hyphen for minus; show the proper signs.
function signs(line: string) {
  return line.replace(/(\d|\))\s?x\s?(?=[\d(])/g, "$1 × ").replace(/\s-\s/g, " − ")
}

// Splits a line at = and ≈. The part before the first sign is a label ("Time", "Step 2: Groundspeed") and is left
// alone unless it is itself a sum (starts with a number or a bracket).
export function parseEquationLine(line: string): MathNode[] {
  const parts = signs(line).split(/(\s[=≈]\s)/)
  const out: MathNode[] = []
  parts.forEach((part, i) => {
    if (i % 2 === 1) out.push(part)
    else if (i === 0 && !/^\s*[\d(]/.test(part)) out.push(part)
    else out.push(...parseMath(part))
  })
  return out
}

function renderNodes(nodes: MathNode[], key = ""): React.ReactNode[] {
  return nodes.map((n, i) =>
    typeof n === "string" ? (
      n
    ) : (
      <span key={`${key}${i}`} className="mx-0.5 inline-flex flex-col items-center align-middle leading-tight">
        <span className="border-b border-current px-1 pb-px">{renderNodes(n.num, `${key}${i}n`)}</span>
        <span className="px-1 pt-px">{renderNodes(n.den, `${key}${i}d`)}</span>
      </span>
    ),
  )
}

export function MathLine({ line }: { line: string }) {
  return (
    <span className="inline-block py-1 font-serif text-[1.08em] text-slate-800 [font-family:'Cambria_Math',Cambria,'STIX_Two_Text','Times_New_Roman',serif]">
      {renderNodes(parseEquationLine(line))}
    </span>
  )
}
