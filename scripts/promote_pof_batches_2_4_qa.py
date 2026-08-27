#!/usr/bin/env python3
"""Promote reviewed POF Batch 2-4 visuals from REFINING to QA_APPROVED.

Promotion is fail-closed: every PNG/WebP must exactly match the reviewed Git-blob
hash lock, decode successfully, remain banner-free, and already be owned by the
manifest before status or QA flags are changed.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "pof-visual-manifest.json"
HASHES = ROOT / "data" / "pof-batches-2-4-reviewed-hashes.json"
TARGET_IDS = {
    "pof-angle-of-attack-definition-001",
    "pof-chord-line-001",
    "pof-four-forces-equilibrium-001",
    "pof-lift-relative-airflow-001",
    "pof-venturi-bernoulli-001",
    "pof-angle-of-incidence-001",
    "pof-centre-of-pressure-001",
    "pof-relative-airflow-001",
    "pof-speed-squared-lift-drag-001",
    "pof-wing-area-lift-drag-001",
    "pof-aircraft-axes-controls-001",
    "pof-critical-aoa-stall-001",
    "pof-stability-types-001",
    "pof-turn-lift-components-001",
    "pof-washout-wing-twist-001",
}


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    header = f"blob {len(data)}\0".encode()
    return hashlib.sha1(header + data).hexdigest()


def assert_no_baked_banner(path: Path) -> None:
    with Image.open(path).convert("RGB") as im:
        width, height = im.size
        top = im.crop((0, 0, width, max(1, int(height * 0.12))))
        pixels = list(top.getdata())
        dark = sum(1 for r, g, b in pixels if r < 45 and g < 55 and b < 75)
        # A few dark labels/aircraft lines are fine. A full-width navy branding bar is not.
        if pixels and dark / len(pixels) > 0.55:
            raise SystemExit(f"Baked dark branding/banner suspected in {path}")


def main() -> None:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    lock = json.loads(HASHES.read_text(encoding="utf-8"))
    expected = lock.get("files", {})
    if len(expected) != 30:
        raise SystemExit(f"Expected exactly 30 reviewed raster files, found {len(expected)}")

    for rel, sha in expected.items():
        path = ROOT / rel
        if not path.exists():
            raise SystemExit(f"Reviewed file missing: {rel}")
        actual = git_blob_sha(path)
        if actual != sha:
            raise SystemExit(f"Reviewed hash mismatch for {rel}: {actual} != {sha}")
        with Image.open(path) as im:
            im.verify()
        assert_no_baked_banner(path)

    index = {v["visual_id"]: v for v in data["visuals"]}
    missing = TARGET_IDS - set(index)
    if missing:
        raise SystemExit(f"Manifest is missing target IDs: {sorted(missing)}")

    owned_paths: set[str] = set()
    for visual_id in TARGET_IDS:
        visual = index[visual_id]
        if visual.get("status") not in {"REFINING", "QA_APPROVED"}:
            raise SystemExit(f"{visual_id}: expected REFINING/QA_APPROVED, got {visual.get('status')}")
        assets = visual.get("assets", {})
        for field in ("master_asset", "web_asset"):
            rel = assets.get(field)
            if rel not in expected:
                raise SystemExit(f"{visual_id}: {field} is not in reviewed hash lock: {rel}")
            if rel in owned_paths:
                raise SystemExit(f"Asset path is owned by more than one visual: {rel}")
            owned_paths.add(rel)

        visual["status"] = "QA_APPROVED"
        visual["qa"] = {
            "technical": True,
            "teaching": True,
            "visual": True,
            "preview": False,
            "live": False,
        }
        visual["visual_inspection"] = {
            "actual_image_reviewed": True,
            "batch1_quality_reference": True,
            "question_specific": True,
            "source_grounded": True,
            "no_baked_pilotvault_banner": True,
            "review_notes": "Actual rendered master/delivery pair reviewed against the locked Batch 1 quality standard; weaker revisions were rejected before this promotion.",
        }
        visual["lock"] = {"approved": False, "replacement_reason": None}

    if owned_paths != set(expected):
        extra = set(expected) - owned_paths
        raise SystemExit(f"Reviewed raster lock contains unowned assets: {sorted(extra)}")

    MANIFEST.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"QA-approved {len(TARGET_IDS)} POF visuals with 30 exact reviewed raster hashes")


if __name__ == "__main__":
    main()
