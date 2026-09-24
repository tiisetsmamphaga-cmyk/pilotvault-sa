// Usage: node render_clean.js <svg-dir> <png-out-dir> file.svg ...
// Removes the baked-in banner, outer frame, caption line and text-only fact boxes by their rendered
// position, then screenshots what is left. Works for every ATG generator's SVG layout.
let chromium
try {
  ;({ chromium } = require("playwright"))
} catch {
  ;({ chromium } = require("/opt/node22/lib/node_modules/playwright"))
}
const fs = require("fs")
const path = require("path")

;(async () => {
  const [dir, outDir, ...files] = process.argv.slice(2)
  fs.mkdirSync(outDir, { recursive: true })
  const browser = await chromium.launch()
  const page = await browser.newPage({ viewport: { width: 1200, height: 1000 }, deviceScaleFactor: 1.5 })
  for (const f of files) {
    const svg = fs.readFileSync(path.join(dir, f), "utf8")
    await page.setContent(`<html><body style="margin:0;background:#fff">${svg}</body></html>`)
    const removed = await page.evaluate(() => {
      const svg = document.querySelector("svg")
      const vb = svg.viewBox.baseVal
      const box = svg.getBoundingClientRect()
      const k = vb.width / box.width
      const bb = (el) => {
        const r = el.getBoundingClientRect()
        return { x0: (r.left - box.left) * k, y0: (r.top - box.top) * k, x1: (r.right - box.left) * k, y1: (r.bottom - box.top) * k }
      }
      const W = vb.width, H = vb.height
      const dark = (c) => /^#0[0-9a-f]1[0-9a-f]{3}$/i.test(c || "") || /^#07152/i.test(c || "") || /^#06111f$/i.test(c || "")
      const shapes = [...svg.querySelectorAll("rect,text,circle,line,path,polygon,polyline,ellipse,image")]
      const kill = new Set()

      // banner: dark full-width band at the top, plus anything drawn inside it
      let bannerBottom = 0
      for (const r of svg.querySelectorAll("rect")) {
        const b = bb(r)
        if (b.y0 <= 1 && b.x1 - b.x0 >= W * 0.95 && b.y1 < H * 0.3 && dark(r.getAttribute("fill"))) bannerBottom = Math.max(bannerBottom, b.y1)
      }
      if (bannerBottom) for (const el of shapes) if (bb(el).y1 <= bannerBottom + 6) kill.add(el)

      // outer frame: the big stroked card below the banner; the caption sits beneath it
      let frameBottom = H
      for (const r of svg.querySelectorAll("rect")) {
        const b = bb(r)
        const w = b.x1 - b.x0, h = b.y1 - b.y0
        if (w >= W * 0.85 && w < W * 0.99 && h >= H * 0.5 && b.y0 >= bannerBottom - 1) {
          kill.add(r)
          frameBottom = Math.min(frameBottom, b.y1)
        }
      }
      for (const el of svg.querySelectorAll("text")) if (bb(el).y0 >= frameBottom - 2) kill.add(el)

      // text-only fact boxes: the right-hand fact column and the three answer boxes along the bottom
      const regions = []
      for (const r of svg.querySelectorAll("rect")) {
        const w = +r.getAttribute("width"), h = +r.getAttribute("height"), x = +r.getAttribute("x")
        if ((w === 378 && h === 138) || (w === 340 && (h === 136 || h === 145)) || (w === 380 && x >= 760)) regions.push(bb(r))
      }
      // any other card that holds only text (and its own accent bars or ANSWER pill) is a fact box too
      const inside = (g, el) => {
        const b = bb(el)
        const cx = (b.x0 + b.x1) / 2, cy = (b.y0 + b.y1) / 2
        return cx >= g.x0 - 1 && cx <= g.x1 + 1 && cy >= g.y0 - 1 && cy <= g.y1 + 1
      }
      const fixedRegions = regions.length
      for (const r of svg.querySelectorAll("rect")) {
        if (kill.has(r) || !+r.getAttribute("rx")) continue
        const g = bb(r)
        const w = g.x1 - g.x0, h = g.y1 - g.y0
        if (w < 150 || h < 30 || h >= H * 0.5) continue
        if (h < 60 && w < W * 0.5) continue // short boxes are table rows; only wide ones are caption bars
        const content = shapes.filter((el) => el !== r && !kill.has(el) && inside(g, el))
        // accent bars and ANSWER pills are small; a larger rectangle inside a card is part of a drawing (e.g. a tank)
        const isDrawing = (el) => {
          if (el.tagName === "text") return false
          if (el.tagName !== "rect") return true
          const b = bb(el)
          return b.x1 - b.x0 >= 40 && b.y1 - b.y0 >= 40
        }
        const drawing = content.filter(isDrawing)
        const texts = content.filter((el) => el.tagName === "text")
        if (texts.length && !drawing.length) regions.push(g)
      }
      // ...unless that would leave no drawing at all (e.g. the compass deviation card, which is the subject)
      const drawingLeft = shapes.some((el) => !kill.has(el) && el.tagName !== "text" && el.tagName !== "rect" && !regions.some((g) => inside(g, el)))
      if (!drawingLeft) regions.length = fixedRegions
      for (const el of shapes) if (regions.some((g) => inside(g, el))) kill.add(el)
      kill.forEach((el) => el.remove())
      return kill.size
    })
    const png = path.join(outDir, f.replace(/\.svg$/, ".png"))
    await page.locator("svg").screenshot({ path: png })
    console.log(`${f}: removed ${removed}`)
  }
  await browser.close()
})()
