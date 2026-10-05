"use client"

import { useMemo, useState } from "react"

// Chart colours: categorical slots 1 and 2 of the validated palette
// (blue / orange; passes lightness, chroma, CVD and contrast checks on white).
const SERIES_BLUE = "#2a78d6"
const SERIES_ORANGE = "#eb6834"
const GRID = "#e2e8f0"
const SA_OFFSET_MS = 2 * 60 * 60 * 1000 // South Africa is UTC+2 all year

export type FunnelCounts = { signedUp: number; tookMock: number; paid: number }

export type SeriesData = {
  signUps: string[]
  payments: { at: string; product: "ppl_pack" | "subject"; amountCents: number }[]
}

export type TrialUser = {
  id: string
  email: string | null
  fullName: string | null
  trialEndsAt: string | null
  lastSignInAt: string | null
  attemptCount: number
  lastAttemptAt: string | null
  subjectsTried: string[]
}

function percent(part: number, whole: number) {
  return whole ? `${Math.round((part / whole) * 100)}%` : "—"
}

function rand(cents: number) {
  return new Intl.NumberFormat("en-ZA", {
    style: "currency",
    currency: "ZAR",
    maximumFractionDigits: 0,
  }).format(cents / 100)
}

// ------------------------------------------------------------------ funnel

export function ConversionFunnel({ funnel }: { funnel: FunnelCounts }) {
  const steps = [
    { label: "Signed up", count: funnel.signedUp, note: "" },
    {
      label: "Took a mock exam",
      count: funnel.tookMock,
      note: `${percent(funnel.tookMock, funnel.signedUp)} of sign-ups`,
    },
    {
      label: "Paid",
      count: funnel.paid,
      note: `${percent(funnel.paid, funnel.signedUp)} of sign-ups · ${percent(
        funnel.paid,
        funnel.tookMock
      )} of mock takers`,
    },
  ]
  const max = Math.max(funnel.signedUp, 1)

  return (
    <section aria-labelledby="funnel-heading" className="rounded-xl border border-slate-200 bg-white p-4 sm:p-5">
      <h2 id="funnel-heading" className="text-base font-semibold text-slate-950">
        Conversion funnel
      </h2>
      <p className="mt-1 text-xs text-slate-500">Real students only (admin and test accounts excluded).</p>
      <ol className="mt-4 space-y-3">
        {steps.map((step) => (
          <li key={step.label}>
            <div className="flex items-baseline justify-between gap-3 text-sm">
              <span className="font-medium text-slate-800">{step.label}</span>
              <span className="tabular-nums">
                <span className="font-semibold text-slate-950">{step.count}</span>
                {step.note && <span className="ml-2 text-xs text-slate-500">{step.note}</span>}
              </span>
            </div>
            <div className="mt-1.5 h-2.5 w-full rounded-full bg-slate-100">
              <div
                className="h-2.5 rounded-full"
                style={{ width: `${(step.count / max) * 100}%`, background: SERIES_BLUE }}
              />
            </div>
          </li>
        ))}
      </ol>
    </section>
  )
}

// ------------------------------------------------------------------ over-time charts

type Granularity = "week" | "month"

type Bucket = { key: string; label: string; start: number; end: number }

function saDate(ms: number) {
  return new Date(ms + SA_OFFSET_MS)
}

function buildBuckets(granularity: Granularity, count: number): Bucket[] {
  const now = saDate(Date.now())
  const buckets: Bucket[] = []

  if (granularity === "month") {
    for (let i = count - 1; i >= 0; i -= 1) {
      const startLocal = Date.UTC(now.getUTCFullYear(), now.getUTCMonth() - i, 1)
      const endLocal = Date.UTC(now.getUTCFullYear(), now.getUTCMonth() - i + 1, 1)
      const label = new Intl.DateTimeFormat("en-ZA", { month: "short", timeZone: "UTC" }).format(
        new Date(startLocal)
      )
      buckets.push({ key: `m${startLocal}`, label, start: startLocal - SA_OFFSET_MS, end: endLocal - SA_OFFSET_MS })
    }
    return buckets
  }

  // Weeks start on Monday (SA time).
  const today = Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate())
  const mondayOffset = (now.getUTCDay() + 6) % 7
  const thisMonday = today - mondayOffset * 86400000

  for (let i = count - 1; i >= 0; i -= 1) {
    const startLocal = thisMonday - i * 7 * 86400000
    const label = new Intl.DateTimeFormat("en-ZA", { day: "numeric", month: "short", timeZone: "UTC" }).format(
      new Date(startLocal)
    )
    buckets.push({
      key: `w${startLocal}`,
      label,
      start: startLocal - SA_OFFSET_MS,
      end: startLocal + 7 * 86400000 - SA_OFFSET_MS,
    })
  }
  return buckets
}

// Rounds the axis top up to a clean, evenly halvable number (2, 4, 10, 20, 50 ...).
function niceMax(value: number) {
  if (value <= 2) return 2
  if (value <= 4) return 4
  const magnitude = 10 ** Math.floor(Math.log10(value))
  const steps = [1, 2, 4, 10]
  for (const step of steps) {
    if (step * magnitude >= value) return step * magnitude
  }
  return 10 * magnitude
}

type ColumnDatum = { label: string; parts: { value: number; color: string; name: string }[] }

function ColumnChart({
  title,
  data,
  formatValue,
  legend,
  minAxisMax = 0,
}: {
  title: string
  data: ColumnDatum[]
  formatValue: (value: number) => string
  legend?: { name: string; color: string }[]
  // Keeps the axis readable when every value is zero or tiny.
  minAxisMax?: number
}) {
  const [hover, setHover] = useState<number | null>(null)
  const width = 640
  const height = 200
  const left = 48
  const right = 8
  const top = 12
  const bottom = 28
  const plotW = width - left - right
  const plotH = height - top - bottom
  const totals = data.map((d) => d.parts.reduce((sum, p) => sum + p.value, 0))
  const yMax = niceMax(Math.max(...totals, minAxisMax))
  const ticks = [0, yMax / 2, yMax]
  const band = plotW / data.length
  const barW = Math.min(24, band * 0.6)
  const y = (value: number) => top + plotH - (value / yMax) * plotH
  const labelEvery = data.length > 8 ? 2 : 1

  return (
    <figure className="min-w-0">
      <figcaption className="flex flex-wrap items-center justify-between gap-2">
        <span className="text-sm font-semibold text-slate-900">{title}</span>
        {legend && (
          <span className="flex flex-wrap gap-3 text-xs text-slate-600">
            {legend.map((item) => (
              <span key={item.name} className="flex items-center gap-1.5">
                <span className="h-2.5 w-2.5 rounded-sm" style={{ background: item.color }} />
                {item.name}
              </span>
            ))}
          </span>
        )}
      </figcaption>
      <div className="relative mt-2">
        <svg viewBox={`0 0 ${width} ${height}`} className="h-auto w-full" role="img" aria-label={title}>
          {ticks.map((tick) => (
            <g key={tick}>
              <line x1={left} x2={width - right} y1={y(tick)} y2={y(tick)} stroke={GRID} strokeWidth={1} />
              <text x={left - 8} y={y(tick) + 4} textAnchor="end" fontSize={11} fill="#64748b">
                {formatValue(tick)}
              </text>
            </g>
          ))}
          {data.map((datum, index) => {
            const cx = left + band * index + band / 2
            let base = top + plotH
            const visible = datum.parts.filter((part) => part.value > 0)

            return (
              <g key={datum.label + index}>
                {visible.map((part, partIndex) => {
                  const h = (part.value / yMax) * plotH
                  const isTop = partIndex === visible.length - 1
                  const gap = partIndex > 0 ? 2 : 0
                  // Upper segments give up 2px at their base: the surface gap.
                  const segTop = base - h
                  const yTop = segTop
                  const segH = Math.max(h - gap, 1)
                  base = segTop
                  const r = isTop ? Math.min(4, segH, barW / 2) : 0

                  return (
                    <path
                      key={part.name}
                      d={`M ${cx - barW / 2} ${yTop + segH} V ${yTop + r} Q ${cx - barW / 2} ${yTop} ${
                        cx - barW / 2 + r
                      } ${yTop} H ${cx + barW / 2 - r} Q ${cx + barW / 2} ${yTop} ${cx + barW / 2} ${yTop + r} V ${
                        yTop + segH
                      } Z`}
                      fill={part.color}
                      opacity={hover === null || hover === index ? 1 : 0.45}
                    />
                  )
                })}
                {index % labelEvery === 0 && (
                  <text x={cx} y={height - 8} textAnchor="middle" fontSize={11} fill="#64748b">
                    {datum.label}
                  </text>
                )}
                <rect
                  x={left + band * index}
                  y={top}
                  width={band}
                  height={plotH}
                  fill="transparent"
                  onMouseEnter={() => setHover(index)}
                  onMouseLeave={() => setHover(null)}
                />
              </g>
            )
          })}
        </svg>
        {hover !== null && (
          <div
            className="pointer-events-none absolute top-0 z-10 whitespace-nowrap rounded-lg border border-slate-200 bg-white px-3 py-2 text-xs shadow-md"
            style={{
              left: `${((left + band * hover + band / 2) / width) * 100}%`,
              // Keep the tooltip inside the chart near either edge.
              transform:
                hover >= data.length - 3 ? "translateX(-100%)" : hover <= 1 ? "translateX(0)" : "translateX(-50%)",
            }}
          >
            <p className="font-semibold text-slate-900">{data[hover].label}</p>
            {data[hover].parts.map((part) => (
              <p key={part.name} className="flex items-center gap-1.5 text-slate-600">
                <span className="h-2 w-2 rounded-sm" style={{ background: part.color }} />
                {part.name}: <span className="font-semibold text-slate-900">{formatValue(part.value)}</span>
              </p>
            ))}
            {data[hover].parts.length > 1 && (
              <p className="mt-0.5 text-slate-600">
                Total:{" "}
                <span className="font-semibold text-slate-900">
                  {formatValue(data[hover].parts.reduce((sum, p) => sum + p.value, 0))}
                </span>
              </p>
            )}
          </div>
        )}
      </div>
    </figure>
  )
}

export function OverTimeCharts({ series }: { series: SeriesData }) {
  const [granularity, setGranularity] = useState<Granularity>("week")
  const [showTable, setShowTable] = useState(false)

  const rows = useMemo(() => {
    const buckets = buildBuckets(granularity, 12)
    const inBucket = (iso: string, bucket: Bucket) => {
      const ms = new Date(iso).getTime()
      return ms >= bucket.start && ms < bucket.end
    }

    return buckets.map((bucket) => {
      const payments = series.payments.filter((payment) => inBucket(payment.at, bucket))
      return {
        label: bucket.label,
        signUps: series.signUps.filter((at) => inBucket(at, bucket)).length,
        ppl: payments.filter((p) => p.product === "ppl_pack").reduce((sum, p) => sum + p.amountCents, 0),
        subject: payments.filter((p) => p.product === "subject").reduce((sum, p) => sum + p.amountCents, 0),
      }
    })
  }, [granularity, series])

  return (
    <section aria-labelledby="trends-heading" className="rounded-xl border border-slate-200 bg-white p-4 sm:p-5">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h2 id="trends-heading" className="text-base font-semibold text-slate-950">
            Sign-ups and revenue over time
          </h2>
          <p className="mt-1 text-xs text-slate-500">
            Last 12 {granularity === "week" ? "weeks" : "months"}, real students only. Revenue is paid (fulfilled)
            payments.
          </p>
        </div>
        <div className="flex rounded-lg border border-slate-300 p-0.5 text-xs font-semibold" role="group" aria-label="Group by">
          {(["week", "month"] as Granularity[]).map((option) => (
            <button
              key={option}
              type="button"
              onClick={() => setGranularity(option)}
              aria-pressed={granularity === option}
              className={`min-h-8 rounded-md px-3 ${
                granularity === option ? "bg-[#1f4e79] text-white" : "text-slate-600 hover:bg-slate-50"
              }`}
            >
              {option === "week" ? "Weekly" : "Monthly"}
            </button>
          ))}
        </div>
      </div>

      <div className="mt-4 grid gap-6 lg:grid-cols-2">
        <ColumnChart
          title="Sign-ups"
          data={rows.map((row) => ({
            label: row.label,
            parts: [{ name: "Sign-ups", value: row.signUps, color: SERIES_BLUE }],
          }))}
          formatValue={(value) => String(Math.round(value))}
          minAxisMax={4}
        />
        <ColumnChart
          title="Revenue"
          legend={[
            { name: "PPL Pack", color: SERIES_BLUE },
            { name: "Single subjects", color: SERIES_ORANGE },
          ]}
          data={rows.map((row) => ({
            label: row.label,
            parts: [
              { name: "PPL Pack", value: row.ppl, color: SERIES_BLUE },
              { name: "Single subjects", value: row.subject, color: SERIES_ORANGE },
            ],
          }))}
          formatValue={rand}
          minAxisMax={100000}
        />
      </div>

      <button
        type="button"
        onClick={() => setShowTable((value) => !value)}
        className="mt-3 text-xs font-semibold text-[#1f4e79] underline"
      >
        {showTable ? "Hide table" : "Show as table"}
      </button>
      {showTable && (
        <div className="mt-2 overflow-x-auto">
          <table className="w-full min-w-[480px] text-left text-xs">
            <thead className="text-slate-500">
              <tr>
                <th className="py-1.5 pr-3 font-semibold">{granularity === "week" ? "Week of" : "Month"}</th>
                <th className="py-1.5 pr-3 font-semibold">Sign-ups</th>
                <th className="py-1.5 pr-3 font-semibold">PPL Pack</th>
                <th className="py-1.5 pr-3 font-semibold">Single subjects</th>
                <th className="py-1.5 font-semibold">Total revenue</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 tabular-nums text-slate-700">
              {rows.map((row) => (
                <tr key={row.label}>
                  <td className="py-1.5 pr-3">{row.label}</td>
                  <td className="py-1.5 pr-3">{row.signUps}</td>
                  <td className="py-1.5 pr-3">{rand(row.ppl)}</td>
                  <td className="py-1.5 pr-3">{rand(row.subject)}</td>
                  <td className="py-1.5">{rand(row.ppl + row.subject)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  )
}

// ------------------------------------------------------------------ trials ending soon

function formatWhen(value: string | null) {
  if (!value) return "—"
  return new Intl.DateTimeFormat("en-ZA", {
    weekday: "short",
    day: "2-digit",
    month: "short",
    hour: "2-digit",
    minute: "2-digit",
    timeZone: "Africa/Johannesburg",
  }).format(new Date(value))
}

export function TrialsEndingSoon({
  users,
  subjectName,
}: {
  users: TrialUser[]
  subjectName: (slug: string) => string
}) {
  const now = Date.now()
  const hour = 60 * 60 * 1000
  const groups = [
    { title: "Ending in the next 24 hours", from: now, to: now + 24 * hour },
    { title: "Ending in 24 to 48 hours", from: now + 24 * hour, to: now + 48 * hour },
    { title: "Ended in the last 24 hours (discount still open)", from: now - 24 * hour, to: now },
  ].map((group) => ({
    ...group,
    users: users
      .filter((user) => {
        if (!user.trialEndsAt) return false
        const ends = new Date(user.trialEndsAt).getTime()
        return ends >= group.from && ends < group.to
      })
      .sort((a, b) => (a.trialEndsAt ?? "").localeCompare(b.trialEndsAt ?? "")),
  }))
  const total = groups.reduce((sum, group) => sum + group.users.length, 0)

  return (
    <section aria-labelledby="trials-heading" className="rounded-xl border border-slate-200 bg-white p-4 sm:p-5">
      <h2 id="trials-heading" className="text-base font-semibold text-slate-950">
        Trials ending soon <span className="font-normal text-slate-500">({total})</span>
      </h2>
      <p className="mt-1 text-xs text-slate-500">
        The 15% discount runs until 24 hours after a trial ends, so this is the best window to follow up.
      </p>

      {total === 0 ? (
        <p className="mt-3 text-sm text-slate-500">No trials end in this window.</p>
      ) : (
        <div className="mt-3 space-y-4">
          {groups
            .filter((group) => group.users.length)
            .map((group) => (
              <div key={group.title}>
                <h3 className="text-xs font-semibold uppercase tracking-[0.1em] text-slate-500">{group.title}</h3>
                <ul className="mt-2 divide-y divide-slate-100 border-y border-slate-100">
                  {group.users.map((user) => (
                    <li key={user.id} className="flex flex-col gap-1 py-2.5 text-sm sm:flex-row sm:items-center sm:justify-between">
                      <div className="min-w-0">
                        <p className="truncate font-medium text-slate-900">
                          {user.fullName?.trim() || "—"}{" "}
                          <span className="font-normal text-slate-600">{user.email}</span>
                        </p>
                        <p className="text-xs text-slate-500">
                          {user.attemptCount
                            ? `${user.attemptCount} mock${user.attemptCount === 1 ? "" : "s"} · ${user.subjectsTried
                                .map(subjectName)
                                .join(", ")}`
                            : "No mock exams yet"}
                          {" · last login "}
                          {formatWhen(user.lastSignInAt)}
                        </p>
                      </div>
                      <p className="shrink-0 text-xs font-semibold text-slate-700">
                        {new Date(user.trialEndsAt ?? 0).getTime() > now ? "Trial ends" : "Trial ended"}{" "}
                        {formatWhen(user.trialEndsAt)}
                      </p>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
        </div>
      )}
    </section>
  )
}
