#!/usr/bin/env python3
"""Fail closed if the production POF renderer admits an unapproved batch."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RENDERER = ROOT / "app" / "practice" / "[subject]" / "components" / "explanation-image.tsx"
EXPECTED_APPROVED = {"1", "2", "3", "4"}
EXPECTED_WEBSITE_TEMPLATE = {"2", "3", "4"}


def fail(message: str) -> None:
    raise SystemExit(f"POF renderer allow-list validation FAILED: {message}")


def extract_array_batches(text: str, constant_name: str) -> set[str]:
    match = re.search(
        rf"const\s+{re.escape(constant_name)}\s*=\s*\[(.*?)\]\s*as\s+const",
        text,
        flags=re.DOTALL,
    )
    if not match:
        fail(f"missing explicit {constant_name} array")
    return set(re.findall(r"refined-batch-(\d+)/", match.group(1)))


def main() -> None:
    if not RENDERER.exists():
        fail("renderer file is missing")
    text = RENDERER.read_text(encoding="utf-8")

    approved = extract_array_batches(text, "APPROVED_POF_BATCH_DIRECTORIES")
    website_template = extract_array_batches(text, "NEW_POF_WEBSITE_TEMPLATE_DIRECTORIES")

    if approved != EXPECTED_APPROVED:
        fail(f"approved renderer batches must be exactly {sorted(EXPECTED_APPROVED)}; got {sorted(approved)}")
    if website_template != EXPECTED_WEBSITE_TEMPLATE:
        fail(
            "website-owned POF template batches must be exactly "
            f"{sorted(EXPECTED_WEBSITE_TEMPLATE)}; got {sorted(website_template)}"
        )

    forbidden = ["raster-complete", "pdf-rebuild", "static-v4"]
    for token in forbidden:
        if token in text:
            fail(f"deprecated POF path is referenced: {token}")

    if re.search(r"refined-batch-\\d|refined-batch-\.\*|refined-batch-\[", text):
        fail("dynamic/regex POF batch admission is forbidden; use explicit batch directories")

    if "PILOTVAULT PRINCIPLES OF FLIGHT" not in text:
        fail("new POF batches must use the website-owned PilotVault POF header")

    print("POF renderer allow-list PASSED: Batch 1 grandfathered; Batches 2-4 explicitly admitted; no future wildcard")


if __name__ == "__main__":
    main()
