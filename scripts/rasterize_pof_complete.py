#!/usr/bin/env python3
"""Rasterise the legacy POF teaching diagrams for the production image system.

The SVG files in pdf-rebuild are treated as source artwork only. Production POF
explanations use the generated PNG/WebP assets. The baked PilotVault header is
removed from the raster export because branding belongs in the website UI.
"""

from __future__ import annotations

import io
import json
import math
from pathlib import Path

import cairosvg
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "public" / "explanation-images" / "principles-of-flight" / "pdf-rebuild"
OUTPUT_DIR = ROOT / "public" / "explanation-images" / "principles-of-flight" / "raster-complete"
QA_DIR = OUTPUT_DIR / "qa"
MAP_PATH = ROOT / "data" / "pof-raster-conversion-map.json"

BANNER_MARKER = "PILOTVAULT PRINCIPLES OF FLIGHT"
BANNER_RATIO = 112 / 680
BATCH_SIZE = 5


def render_source(svg_path: Path) -> Image.Image:
    svg_text = svg_path.read_text(encoding="utf-8")
    png_bytes = cairosvg.svg2png(bytestring=svg_text.encode("utf-8"), output_width=1600)
    image = Image.open(io.BytesIO(png_bytes)).convert("RGB")

    # Legacy diagrams used a 112px banner in a 680px-high 1200px canvas.
    # Scale the crop proportionally after high-resolution rasterisation.
    if BANNER_MARKER in svg_text:
        crop_y = int(round(image.height * BANNER_RATIO))
        image = image.crop((0, crop_y, image.width, image.height))

    return image


def save_asset(svg_path: Path) -> dict[str, str | int]:
    image = render_source(svg_path)
    stem = svg_path.stem
    png_path = OUTPUT_DIR / f"{stem}.png"
    webp_path = OUTPUT_DIR / f"{stem}.webp"

    image.save(png_path, format="PNG", optimize=True)
    image.save(webp_path, format="WEBP", quality=92, method=6)

    return {
        "source_name": svg_path.name,
        "source_path": str(svg_path.relative_to(ROOT)).replace("\\", "/"),
        "master_asset": str(png_path.relative_to(ROOT)).replace("\\", "/"),
        "web_asset": str(webp_path.relative_to(ROOT)).replace("\\", "/"),
        "public_web_url": "/" + str(webp_path.relative_to(ROOT / "public")).replace("\\", "/"),
        "width": image.width,
        "height": image.height,
    }


def make_contact_sheet(batch_number: int, records: list[dict[str, str | int]]) -> str:
    thumbs: list[tuple[Image.Image, str]] = []
    cell_w, cell_h = 620, 430
    for record in records:
        path = ROOT / str(record["web_asset"])
        img = Image.open(path).convert("RGB")
        img.thumbnail((cell_w - 40, cell_h - 70), Image.Resampling.LANCZOS)
        thumbs.append((img, str(record["source_name"])))

    cols = 2
    rows = math.ceil(len(thumbs) / cols)
    sheet = Image.new("RGB", (cols * cell_w, rows * cell_h), "white")
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()

    for index, (img, label) in enumerate(thumbs):
        col = index % cols
        row = index // cols
        x0 = col * cell_w
        y0 = row * cell_h
        x = x0 + (cell_w - img.width) // 2
        y = y0 + 30
        sheet.paste(img, (x, y))
        draw.text((x0 + 20, y0 + cell_h - 28), label, fill="black", font=font)

    out = QA_DIR / f"batch-{batch_number:02d}.webp"
    sheet.save(out, format="WEBP", quality=88, method=6)
    return str(out.relative_to(ROOT)).replace("\\", "/")


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    QA_DIR.mkdir(parents=True, exist_ok=True)

    svg_paths = sorted(SOURCE_DIR.glob("*.svg"))
    if not svg_paths:
        raise SystemExit("No legacy POF source diagrams found")

    records = [save_asset(path) for path in svg_paths]
    batches = []
    for start in range(0, len(records), BATCH_SIZE):
        batch_records = records[start : start + BATCH_SIZE]
        batch_number = start // BATCH_SIZE + 1
        sheet = make_contact_sheet(batch_number, batch_records)
        batches.append({
            "batch": batch_number,
            "contact_sheet": sheet,
            "assets": [r["source_name"] for r in batch_records],
        })

    payload = {
        "source_directory": str(SOURCE_DIR.relative_to(ROOT)).replace("\\", "/"),
        "output_directory": str(OUTPUT_DIR.relative_to(ROOT)).replace("\\", "/"),
        "banner_removed": True,
        "raster_only_for_production": True,
        "batch_size": BATCH_SIZE,
        "asset_count": len(records),
        "assets": records,
        "batches": batches,
    }
    MAP_PATH.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"Generated {len(records)} POF raster asset pairs in {len(batches)} QA batches")


if __name__ == "__main__":
    main()
