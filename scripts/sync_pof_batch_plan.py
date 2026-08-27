#!/usr/bin/env python3
"""Append SOURCE_FOUND visuals from the staged POF batch plan to the production manifest.

This helper is intentionally append-only for new visual IDs. Existing manifest entries,
especially locked Batch 1 records, are preserved exactly as parsed objects and are never
rewritten from the plan.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "pof-visual-manifest.json"
PLAN = ROOT / "data" / "pof-batches-2-4-plan.json"


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    plan = json.loads(PLAN.read_text(encoding="utf-8"))

    if manifest.get("subject") != "principles-of-flight":
        raise SystemExit("Unexpected manifest subject")
    if plan.get("subject") != "principles-of-flight":
        raise SystemExit("Unexpected plan subject")

    visuals = manifest.get("visuals")
    if not isinstance(visuals, list):
        raise SystemExit("Manifest visuals must be a list")

    existing = {item.get("visual_id") for item in visuals if isinstance(item, dict)}
    added = 0
    for batch in plan.get("batches", []):
        if not isinstance(batch, dict):
            raise SystemExit("Invalid batch entry")
        batch_no = batch.get("batch")
        if batch_no not in {2, 3, 4}:
            raise SystemExit(f"Unexpected batch number: {batch_no}")
        batch_visuals = batch.get("visuals")
        if not isinstance(batch_visuals, list) or len(batch_visuals) > 5:
            raise SystemExit(f"Batch {batch_no} must contain 1-5 visuals")
        for visual in batch_visuals:
            visual_id = visual.get("visual_id") if isinstance(visual, dict) else None
            if not isinstance(visual_id, str):
                raise SystemExit(f"Batch {batch_no} has invalid visual_id")
            if visual_id in existing:
                continue
            if visual.get("status") != "SOURCE_FOUND":
                raise SystemExit(f"{visual_id} must enter manifest at SOURCE_FOUND")
            visuals.append(visual)
            existing.add(visual_id)
            added += 1

    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Added {added} SOURCE_FOUND visual(s); manifest now has {len(visuals)} visual(s)")


if __name__ == "__main__":
    main()
