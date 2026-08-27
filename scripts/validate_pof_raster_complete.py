#!/usr/bin/env python3
"""One-time fidelity QA for the complete POF raster migration.

The production PNG/WebP files are derived from the existing handbook-grounded
POF source artwork. This validator proves that the teaching body was preserved,
the legacy baked website banner was removed before export, and every web asset
is a valid raster image.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageStat

from rasterize_pof_complete import BANNER_MARKER, ROOT, banner_crop_ratio, render_source

MAP_PATH = ROOT / "data" / "pof-raster-conversion-map.json"
REPORT_PATH = ROOT / "data" / "pof-raster-qa-report.json"
MAX_BATCH_SIZE = 5
MAX_WEBP_MEAN_ABS_ERROR = 12.0


def fail(message: str) -> None:
    print(f"POF raster QA FAILED: {message}", file=sys.stderr)
    raise SystemExit(1)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    if not MAP_PATH.exists():
        fail("conversion map is missing")

    data = json.loads(MAP_PATH.read_text(encoding="utf-8"))
    assets = data.get("assets")
    batches = data.get("batches")
    if not isinstance(assets, list) or not assets:
        fail("conversion map has no assets")
    if data.get("asset_count") != len(assets):
        fail("asset_count does not match conversion map")
    if not data.get("banner_removed"):
        fail("conversion map does not record banner removal")
    if not data.get("raster_only_for_production"):
        fail("conversion map does not enforce raster production output")
    if data.get("batch_size") != MAX_BATCH_SIZE:
        fail("QA batch size must remain five")
    if not isinstance(batches, list) or not batches:
        fail("QA batches are missing")

    batch_members: list[str] = []
    for batch in batches:
        names = batch.get("assets")
        if not isinstance(names, list) or not 1 <= len(names) <= MAX_BATCH_SIZE:
            fail(f"batch {batch.get('batch')} exceeds the five-concept QA limit")
        batch_members.extend(names)
    source_names = [str(record.get("source_name")) for record in assets]
    if batch_members != source_names:
        fail("batch membership does not exactly cover the raster asset list in order")

    report_assets = []
    banner_count = 0
    for index, record in enumerate(assets, start=1):
        source = ROOT / str(record["source_path"])
        png = ROOT / str(record["master_asset"])
        webp = ROOT / str(record["web_asset"])
        public_web_url = str(record["public_web_url"])

        for path in (source, png, webp):
            if not path.exists():
                fail(f"missing file: {path.relative_to(ROOT)}")

        if not public_web_url.startswith("/explanation-images/principles-of-flight/raster-complete/"):
            fail(f"{record['source_name']}: unexpected public raster path")
        if public_web_url.lower().endswith(".svg") or not public_web_url.lower().endswith(".webp"):
            fail(f"{record['source_name']}: production URL must be WebP, never SVG")

        source_text = source.read_text(encoding="utf-8")
        expected_ratio = banner_crop_ratio(source_text)
        recorded_ratio = float(record.get("banner_crop_ratio", 0.0))
        if abs(expected_ratio - recorded_ratio) > 0.0000015:
            fail(f"{record['source_name']}: recorded crop ratio does not match source geometry")
        if BANNER_MARKER in source_text:
            banner_count += 1
            if expected_ratio <= 0:
                fail(f"{record['source_name']}: legacy banner exists but no crop was applied")

        expected = render_source(source).convert("RGB")
        with Image.open(png) as master_image:
            master = master_image.convert("RGB")
        with Image.open(webp) as web_image:
            web = web_image.convert("RGB")

        if master.size != expected.size:
            fail(f"{record['source_name']}: PNG dimensions do not match cropped source")
        if web.size != expected.size:
            fail(f"{record['source_name']}: WebP dimensions do not match cropped source")
        if master.width < 1200 or master.height < 500:
            fail(f"{record['source_name']}: raster output is below the production readability floor")

        # PNG must be pixel-identical to the source teaching body after the exact
        # banner crop. This protects arrows, axes, labels and geometry.
        if ImageChops.difference(expected, master).getbbox() is not None:
            fail(f"{record['source_name']}: PNG teaching body is not pixel-faithful to source")

        web_diff = ImageChops.difference(master, web)
        mean_error = sum(ImageStat.Stat(web_diff).mean) / 3.0
        if mean_error > MAX_WEBP_MEAN_ABS_ERROR:
            fail(
                f"{record['source_name']}: WebP compression error {mean_error:.2f} exceeds "
                f"{MAX_WEBP_MEAN_ABS_ERROR:.2f}"
            )

        if (master.width, master.height) != (int(record["width"]), int(record["height"])):
            fail(f"{record['source_name']}: conversion map dimensions are stale")

        report_assets.append(
            {
                "source_name": record["source_name"],
                "master_asset": record["master_asset"],
                "web_asset": record["web_asset"],
                "public_web_url": public_web_url,
                "width": master.width,
                "height": master.height,
                "banner_crop_ratio": recorded_ratio,
                "png_sha256": sha256(png),
                "webp_sha256": sha256(webp),
                "webp_mean_abs_error": round(mean_error, 4),
            }
        )

        batch_number = (index - 1) // MAX_BATCH_SIZE + 1
        print(f"QA PASS batch {batch_number:02d}: {record['source_name']}")

    report = {
        "schema_version": 1,
        "subject": "principles-of-flight",
        "asset_count": len(report_assets),
        "batch_count": len(batches),
        "max_batch_size": MAX_BATCH_SIZE,
        "legacy_banner_sources_cropped": banner_count,
        "technical_body_fidelity": "pixel-identical PNG after geometry-aware banner crop",
        "web_delivery": "WebP quality checked against PNG master",
        "assets": report_assets,
    }
    REPORT_PATH.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(
        f"POF raster QA PASSED: {len(report_assets)} assets, {len(batches)} batches, "
        f"{banner_count} legacy banners removed"
    )


if __name__ == "__main__":
    main()
