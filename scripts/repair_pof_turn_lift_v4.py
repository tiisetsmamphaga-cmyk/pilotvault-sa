#!/usr/bin/env python3
"""Rebuild the reviewed balanced-level-turn visual and replace rejected v1 paths."""
from __future__ import annotations

import json
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "public/explanation-images/principles-of-flight/refined-batch-4"
MANIFEST = ROOT / "data/pof-visual-manifest.json"
W, H = 1600, 1050

NAVY = "#071426"
BLUE = "#204f7c"
GOLD = "#f4b400"
RED = "#c92b2b"
MUTED = "#415979"
PALE = "#f4f7fb"
LINE = "#9db3ce"
WHITE = "#ffffff"


def font(size: int, bold: bool = False):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    candidates = [
        Path("/usr/share/fonts/truetype/dejavu") / name,
        Path("/usr/share/fonts/dejavu") / name,
    ]
    for path in candidates:
        if path.exists():
            return ImageFont.truetype(str(path), size=size)
    return ImageFont.load_default()


def arrow(draw: ImageDraw.ImageDraw, a, b, fill, width=9, head=22):
    draw.line([a, b], fill=fill, width=width)
    ang = math.atan2(b[1]-a[1], b[0]-a[0])
    p1 = (b[0] - head*math.cos(ang-math.pi/6), b[1] - head*math.sin(ang-math.pi/6))
    p2 = (b[0] - head*math.cos(ang+math.pi/6), b[1] - head*math.sin(ang+math.pi/6))
    draw.polygon([b, p1, p2], fill=fill)


def center(draw, xy, text, fnt, fill):
    box = draw.textbbox((0,0), text, font=fnt)
    x = xy[0] - (box[2]-box[0])/2
    draw.text((x, xy[1]), text, font=fnt, fill=fill)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    im = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(im)

    center(d, (W/2, 48), "BALANCED LEVEL TURN", font(46, True), NAVY)
    center(d, (W/2, 105), "Resolve total lift into vertical and horizontal components.", font(28), MUTED)

    origin = (760, 472)
    bank_a, bank_b = (330, 748), (1192, 194)
    d.line([bank_a, bank_b], fill=NAVY, width=7)
    d.ellipse([origin[0]-13, origin[1]-13, origin[0]+13, origin[1]+13], outline=NAVY, width=4, fill=WHITE)

    arrow(d, origin, (760, 190), BLUE, width=9, head=25)
    arrow(d, origin, (760, 710), NAVY, width=9, head=25)
    arrow(d, origin, (385, 472), RED, width=9, head=25)
    total_end = (590, 222)
    arrow(d, origin, total_end, GOLD, width=10, head=25)

    d.line([(590, 222), (760, 222)], fill=LINE, width=3)
    d.line([(590, 222), (590, 472)], fill=LINE, width=3)

    d.text((360, 258), "TOTAL LIFT", font=font(31, True), fill="#a66a00")
    d.multiline_text((800, 245), "VERTICAL COMPONENT\nsupports weight", font=font(28, True), fill=BLUE, spacing=2)
    d.multiline_text((145, 520), "HORIZONTAL COMPONENT\nprovides centripetal force", font=font(28, True), fill=RED, spacing=2)
    center(d, (760, 748), "WEIGHT", font(30, True), NAVY)

    card = (170, 820, 1340, 915)
    d.rounded_rectangle(card, radius=20, fill=PALE, outline="#bfd0e4", width=2)
    center(d, (755, 845), "Vertical lift supports weight; horizontal lift provides centripetal force.", font(26, True), NAVY)
    center(d, (755, 890), "Source relationship: Principles of Flight — balanced-turn force resolution", font(18), "#8aa4c4")

    png = OUT / "pof-turn-lift-components-v4.png"
    webp = OUT / "pof-turn-lift-components-v4.webp"
    im.save(png, format="PNG", optimize=True)
    im.save(webp, format="WEBP", quality=94, method=6)

    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    visual = next(v for v in data["visuals"] if v["visual_id"] == "pof-turn-lift-components-001")
    visual["assets"] = {
        "master_asset": "public/explanation-images/principles-of-flight/refined-batch-4/pof-turn-lift-components-v4.png",
        "web_asset": "public/explanation-images/principles-of-flight/refined-batch-4/pof-turn-lift-components-v4.webp",
    }
    visual["status"] = "REFINING"
    visual["qa"] = {"technical": False, "teaching": False, "visual": False, "preview": False, "live": False}
    visual["lock"] = {"approved": False, "replacement_reason": None}
    MANIFEST.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {png.relative_to(ROOT)} and {webp.relative_to(ROOT)}; manifest now points to v4")


if __name__ == "__main__":
    main()
