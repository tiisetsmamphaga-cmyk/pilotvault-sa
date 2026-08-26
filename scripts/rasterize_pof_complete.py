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
import xml.etree.ElementTree as ET
from pathlib import Path

import cairosvg
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "public" / "explanation-images" / "principles-of-flight" / "pdf-rebuild"
OUTPUT_DIR = ROOT / "public" / "explanation-images" / "principles-of-flight" / "raster-complete"
QA_DIR = OUTPUT_DIR / "qa"
MAP_PATH = ROOT / "data" / "pof-raster-conversion-map.json"

BANNER_MARKER = "PILOTVAULT PRINCIPLES OF FLIGHT"
BATCH_SIZE = 5


def _number(value: str | None, default: float = 0.0) -> float:
    if value is None:
        return default
    cleaned = value.strip().lower().replace("px", "")
    try:
        return float(cleaned)
    except ValueError:
        return default


def banner_crop_ratio(svg_text: str) -> float:
    """Return the exact top-banner height as a fraction of the SVG canvas."""
    if BANNER_MARKER not in svg_text:
        return 0.0

    root = ET.fromstring(svg_text)
    view_box = root.attrib.get("viewBox", "").split()
    if len(view_box) != 4:
        raise ValueError("POF source with banner must define a four-value viewBox")

    view_width = _number(view_box[2])
    view_height = _number(view_box[3])
    if view_width <= 0 or view_height <= 0:
        raise ValueError("POF source has invalid viewBox dimensions")

    candidates: list[float] = []
    for element in root.iter():
        if not element.tag.endswith("rect"):
            continue
        x = _number(element.attrib.get("x"), 0.0)
        y = _number(element.attrib.get("y"), 0.0)
        width = _number(element.attrib.get("width"), view_width)
        height = _number(element.attrib.get("height"), 0.0)
        fill = element.attrib.get("fill", "").strip().lower()

        is_top_full_width = abs(x) < 0.01 and abs(y) < 0.01 and abs(width - view_width) < 0.5
        is_banner_sized = 0 < height < view_height * 0.4
        is_non_background = fill not in {"", "#fff", "#ffffff", "white", "none"}
        if is_top_full_width and is_banner_sized and is_non_background:
            candidates.append(height)

    if not candidates:
        raise ValueError("PilotVault banner marker found but top banner rectangle could not be resolved")

    return max(candidates) / view_height


def render_source(svg_path: Path) -> Image.Image:
    svg_text = svg_path.read_text(encoding="utf-8")
    png_bytes = cairosvg.svg2png(bytestring=svg_text.encode("utf-8"), output_width=1600)
    image = Image.open(io.BytesIO(png_bytes)).convert("RGB")

    crop_ratio = banner_crop_ratio(svg_text)
    if crop_ratio:
        crop_y = int(round(image.height * crop_ratio))
        image = image.crop((0, crop_y, image.width, image.height))

    return image


def save_asset(svg_path: Path) -> dict[str, str | int | float]:
    svg_text = svg_path.read_text(encoding="utf-8")
    crop_ratio = banner_crop_ratio(svg_text)
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
        "banner_crop_ratio": round(crop_ratio, 6),
    }


def make_contact_sheet(batch_number: int, records: list[dict[str, str | int | float]]) -> str:
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
