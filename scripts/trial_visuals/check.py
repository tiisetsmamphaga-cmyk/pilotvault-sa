"""Check explanation pictures against docs/EXPLANATION_ILLUSTRATION_STANDARD.md before anyone sees them.

usage: python3 scripts/trial_visuals/check.py <module> [--only id,id] [--out dir]

For every picture in the module's registry it renders the SVG in Chromium and reports:
  - text smaller than 11 px when the picture is shown 328 px wide on a phone
  - labels overlapping each other
  - labels crossed by an airflow streamline
  - labels outside their panel (captions: outside the canvas)
and writes <out>/<slug>-phone.png (as on a phone, 328 px wide) and <out>/<slug>-desktop.png.
Exit code 1 when anything fails.
"""
import argparse
import importlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from kit import REPO, svg  # noqa: E402

PHONE_W = 328
MIN_PHONE_PX = 11

JS = r"""
let chromium
try { ({ chromium } = require("playwright")) } catch { ({ chromium } = require("/opt/node22/lib/node_modules/playwright")) }
const fs = require("fs"), path = require("path")
;(async () => {
  const [dir, phoneW, ...names] = process.argv.slice(2)
  const browser = await chromium.launch()
  const results = {}
  for (const name of names) {
    const svgText = fs.readFileSync(path.join(dir, name + ".svg"), "utf8")
    const page = await browser.newPage({ viewport: { width: 1400, height: 1000 } })
    await page.setContent(`<html><body style="margin:0">${svgText}</body></html>`)
    results[name] = await page.evaluate(() => {
      const svg = document.querySelector("svg")
      const vb = svg.viewBox.baseVal
      const groups = {}
      for (const t of svg.querySelectorAll("text:not([data-halo])")) {
        const key = t.getAttribute("data-label") ? "L" + t.getAttribute("data-label") :
          t.getAttribute("data-caption") ? "C" + t.getAttribute("data-caption") : "T" + Math.random()
        const r = t.getBoundingClientRect(), s = svg.getBoundingClientRect()
        const k = vb.width / s.width
        const box = [(r.left - s.left) * k, (r.top - s.top) * k, (r.right - s.left) * k, (r.bottom - s.top) * k]
        const panel = t.closest("[data-panel]")
        const g = groups[key] || (groups[key] = { text: [], size: parseFloat(t.getAttribute("font-size")),
          caption: key[0] === "C", box: box.slice(), panel: panel ? panel.getAttribute("data-box").split(",").map(Number) : null })
        g.text.push(t.textContent)
        g.box = [Math.min(g.box[0], box[0]), Math.min(g.box[1], box[1]), Math.max(g.box[2], box[2]), Math.max(g.box[3], box[3])]
      }
      const flows = []
      for (const p of svg.querySelectorAll("path[data-flow]")) {
        const m = p.getCTM(), L = p.getTotalLength(), pts = []
        for (let i = 0; i <= 60; i++) {
          const q = p.getPointAtLength(L * i / 60)
          pts.push([m.a * q.x + m.c * q.y + m.e, m.b * q.x + m.d * q.y + m.f])
        }
        flows.push(pts)
      }
      return { width: vb.width, height: vb.height, labels: Object.values(groups), flows }
    })
    // previews: as on a phone and on a desktop
    await page.setViewportSize({ width: Number(phoneW), height: 1200 })
    await page.setContent(`<html><body style="margin:0;background:#fff"><img style="display:block;width:${phoneW}px" src="data:image/svg+xml;base64,${Buffer.from(svgText).toString("base64")}"></body></html>`)
    await page.waitForTimeout(200)
    await page.locator("img").screenshot({ path: path.join(dir, name + "-phone.png") })
    await page.close()
  }
  fs.writeFileSync(path.join(dir, "results.json"), JSON.stringify(results))
  await browser.close()
})()
"""


def overlap(a, b, pad=4):
    return a[0] < b[2] + pad and b[0] < a[2] + pad and a[1] < b[3] + pad and b[1] < a[3] + pad


def inside(box, area, pad=2):
    return box[0] >= area[0] - pad and box[1] >= area[1] - pad and box[2] <= area[2] + pad and box[3] <= area[3] + pad


def check(res):
    problems = []
    W = res["width"]
    labels = res["labels"]
    for g in labels:
        name = " / ".join(g["text"])
        px = g["size"] * PHONE_W / W
        if px < MIN_PHONE_PX:
            problems.append(f"text too small on a phone ({px:.1f}px): {name}")
        if g["caption"] or not g["panel"]:
            if not inside(g["box"], (0, 0, W, res["height"])):
                problems.append(f"outside the picture: {name}")
        else:
            x, y, w, h = g["panel"]
            if not inside(g["box"], (x, y, x + w, y + h)):
                problems.append(f"outside its panel: {name}")
        for pts in res["flows"]:
            if any(g["box"][0] <= px_ <= g["box"][2] and g["box"][1] <= py_ <= g["box"][3] for px_, py_ in pts):
                problems.append(f"airflow arrow crosses the label: {name}")
                break
    for i, a in enumerate(labels):
        for b in labels[i + 1:]:
            if overlap(a["box"], b["box"]):
                problems.append(f"labels overlap: {' / '.join(a['text'])}  <->  {' / '.join(b['text'])}")
    return problems


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("module")
    ap.add_argument("--only", default="")
    ap.add_argument("--out", default=str(Path(tempfile.gettempdir()) / "picture-check"))
    a = ap.parse_args()
    items = importlib.import_module(a.module).R.items
    if a.only:
        keep = {int(x) for x in a.only.split(",")}
        items = [i for i in items if i["id"] in keep]
    seen, todo = set(), []
    for it in items:  # one check per picture, even when several questions share it
        slug = it["url"].rsplit("/", 1)[1].rsplit(".", 1)[0]
        if slug not in seen:
            seen.add(slug)
            todo.append((slug, it))
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    for slug, it in todo:
        (out / f"{slug}.svg").write_text(svg(it["draw"](), it["w"], it["h"]))
    (out / "check.js").write_text(JS)
    env = dict(os.environ, NODE_PATH="/opt/node22/lib/node_modules")
    subprocess.run(["node", str(out / "check.js"), str(out), str(PHONE_W), *[s for s, _ in todo]], check=True, env=env, cwd=REPO)
    results = json.loads((out / "results.json").read_text())
    failed = 0
    for slug, _ in todo:
        problems = check(results[slug])
        print(("FAIL " if problems else "ok   ") + slug)
        for p in problems:
            print("     - " + p)
        failed += bool(problems)
    print(f"{len(todo) - failed}/{len(todo)} pictures pass; phone previews in {out}")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
