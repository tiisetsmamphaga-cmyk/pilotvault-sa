// Usage: node render.js <dir-with-svgs> <png-out-dir> [file.svg ...]
let chromium
try {
  ;({ chromium } = require("playwright"))
} catch {
  ;({ chromium } = require("/opt/node22/lib/node_modules/playwright"))
}
const fs = require("fs")
const path = require("path")

;(async () => {
  const [dir, outDir, ...only] = process.argv.slice(2)
  fs.mkdirSync(outDir, { recursive: true })
  const files = (only.length ? only : fs.readdirSync(dir).filter((f) => f.endsWith(".svg"))).sort()
  const browser = await chromium.launch()
  const page = await browser.newPage({ viewport: { width: 1200, height: 680 }, deviceScaleFactor: 1.5 })
  let problems = 0
  for (const f of files) {
    const svg = fs.readFileSync(path.join(dir, f), "utf8")
    await page.setContent(`<html><body style="margin:0">${svg}</body></html>`)
    const report = await page.evaluate(() => {
      const svg = document.querySelector("svg")
      const texts = [...svg.querySelectorAll("text")].map((el) => {
        const r = el.getBoundingClientRect()
        return { s: el.textContent, x0: r.left, y0: r.top, x1: r.right, y1: r.bottom }
      })
      const issues = []
      for (let i = 0; i < texts.length; i++) {
        const a = texts[i]
        if (a.x0 < 30 || a.x1 > 1170) issues.push(`OUT OF CARD X: "${a.s}" [${a.x0.toFixed(0)}..${a.x1.toFixed(0)}]`)
        for (let j = i + 1; j < texts.length; j++) {
          const b = texts[j]
          const ox = Math.min(a.x1, b.x1) - Math.max(a.x0, b.x0)
          const oy = Math.min(a.y1, b.y1) - Math.max(a.y0, b.y0)
          if (ox > 1 && oy > 1) issues.push(`TEXT OVERLAP: "${a.s}" <> "${b.s}"`)
        }
      }
      return issues
    })
    report.forEach((r) => console.log(`${f}: ${r}`))
    problems += report.length
    const png = path.join(outDir, f.replace(/\.svg$/, ".png"))
    await page.locator("svg").screenshot({ path: png })
    console.log(`rendered ${png}`)
  }
  await browser.close()
  console.log(problems ? `${problems} issue(s)` : "no text overlaps")
})()
