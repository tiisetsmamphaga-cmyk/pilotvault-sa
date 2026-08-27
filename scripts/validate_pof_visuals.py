#!/usr/bin/env python3
"""Validate the PilotVault Principles of Flight visual production manifest."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "pof-visual-manifest.json"

STATUSES = [
    "SOURCE_FOUND",
    "REFINING",
    "QA_FAILED",
    "QA_APPROVED",
    "PREVIEW_READY",
    "MAPPED",
    "PRODUCTION_READY",
    "LIVE_VERIFIED",
]
RASTER_EXTENSIONS = {".png", ".webp", ".jpg", ".jpeg"}
ASSET_ROOT = "public/explanation-images/principles-of-flight/"
BATCH1_GRANDFATHERED = {
    "pof-bank-load-factor-001",
    "pof-longitudinal-stability-001",
    "pof-parasite-drag-001",
    "pof-dihedral-001",
    "pof-glide-ratio-001",
}


def fail(message: str) -> None:
    print(f"POF visual validation FAILED: {message}", file=sys.stderr)
    raise SystemExit(1)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def validate_asset(path: str | None, visual_id: str, field: str, status: str) -> None:
    if path is None:
        require(status in {"SOURCE_FOUND", "REFINING", "QA_FAILED"}, f"{visual_id}: {field} cannot be null at status {status}")
        return

    lower = path.lower().split("?", 1)[0]
    suffix = Path(lower).suffix
    require(suffix in RASTER_EXTENSIONS, f"{visual_id}: {field} must be a raster asset; got {path}")
    require(".svg" not in lower, f"{visual_id}: SVG/vector assets are forbidden")
    require(lower.startswith(ASSET_ROOT), f"{visual_id}: {field} must live under {ASSET_ROOT}")


def main() -> None:
    require(MANIFEST.exists(), "data/pof-visual-manifest.json is missing")
    try:
        data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"manifest is not valid JSON: {exc}")

    require(data.get("schema_version") == 1, "schema_version must be 1")
    require(data.get("subject") == "principles-of-flight", "subject must be principles-of-flight")
    require(data.get("allowed_statuses") == STATUSES, "allowed_statuses must exactly match the locked workflow states")

    visuals = data.get("visuals")
    require(isinstance(visuals, list), "visuals must be an array")

    seen_visual_ids: set[str] = set()
    question_owner: dict[int, str] = {}

    for visual in visuals:
        require(isinstance(visual, dict), "each visual entry must be an object")
        visual_id = visual.get("visual_id")
        require(isinstance(visual_id, str) and re.fullmatch(r"pof-[a-z0-9-]+-[0-9]{3}", visual_id) is not None, "visual_id format is invalid")
        require(visual_id not in seen_visual_ids, f"duplicate visual_id {visual_id}")
        seen_visual_ids.add(visual_id)

        for text_field in ("topic", "concept", "mapping_reason"):
            value = visual.get(text_field)
            require(isinstance(value, str) and value.strip(), f"{visual_id}: {text_field} is required")

        status = visual.get("status")
        require(status in STATUSES, f"{visual_id}: invalid status {status}")

        question_ids = visual.get("question_ids")
        require(isinstance(question_ids, list) and question_ids, f"{visual_id}: question_ids must be a non-empty list")
        require(all(isinstance(q, int) for q in question_ids), f"{visual_id}: every question_id must be an integer")
        require(len(question_ids) == len(set(question_ids)), f"{visual_id}: duplicate question IDs within the entry")
        if len(question_ids) > 1:
            reuse = visual.get("reuse_justification")
            require(
                isinstance(reuse, str) and reuse.strip(),
                f"{visual_id}: reuse_justification is required when one visual maps to multiple questions",
            )
        for qid in question_ids:
            previous = question_owner.get(qid)
            require(previous is None or previous == visual_id, f"question {qid} is mapped to both {previous} and {visual_id}; explicit one-visual ownership is required")
            question_owner[qid] = visual_id

        source = visual.get("source")
        require(isinstance(source, dict), f"{visual_id}: source object is required")
        require(isinstance(source.get("document"), str) and source["document"].strip(), f"{visual_id}: source.document is required")
        require(isinstance(source.get("page"), int) and source["page"] > 0, f"{visual_id}: source.page must be a positive integer")
        require(isinstance(source.get("notes"), str) and source["notes"].strip(), f"{visual_id}: source.notes is required")

        brief = visual.get("brief")
        require(isinstance(brief, dict), f"{visual_id}: design brief is required")
        require(isinstance(brief.get("student_must_understand"), str) and brief["student_must_understand"].strip(), f"{visual_id}: brief.student_must_understand is required")
        for field in ("preserve", "refine", "add", "remove"):
            require(isinstance(brief.get(field), list), f"{visual_id}: brief.{field} must be a list")

        assets = visual.get("assets")
        require(isinstance(assets, dict), f"{visual_id}: assets object is required")
        validate_asset(assets.get("master_asset"), visual_id, "master_asset", status)
        validate_asset(assets.get("web_asset"), visual_id, "web_asset", status)

        qa = visual.get("qa")
        require(isinstance(qa, dict), f"{visual_id}: qa object is required")
        for gate in ("technical", "teaching", "visual", "preview", "live"):
            require(isinstance(qa.get(gate), bool), f"{visual_id}: qa.{gate} must be true or false")

        if status in {"QA_APPROVED", "PREVIEW_READY", "MAPPED", "PRODUCTION_READY", "LIVE_VERIFIED"}:
            require(qa["technical"] and qa["teaching"] and qa["visual"], f"{visual_id}: technical, teaching and visual QA must pass before {status}")
            if visual_id not in BATCH1_GRANDFATHERED:
                inspection = visual.get("visual_inspection")
                require(isinstance(inspection, dict), f"{visual_id}: visual_inspection is required before {status}")
                require(inspection.get("actual_image_reviewed") is True, f"{visual_id}: actual rendered image must be reviewed before {status}")
                require(inspection.get("batch1_quality_reference") is True, f"{visual_id}: image must explicitly pass the Batch 1 quality-reference check before {status}")
        if status in {"PREVIEW_READY", "MAPPED", "PRODUCTION_READY", "LIVE_VERIFIED"}:
            require(qa["preview"], f"{visual_id}: preview QA must pass before {status}")
        if status == "LIVE_VERIFIED":
            require(qa["live"], f"{visual_id}: live QA must pass before LIVE_VERIFIED")

        lock = visual.get("lock")
        require(isinstance(lock, dict), f"{visual_id}: lock object is required")
        require(isinstance(lock.get("approved"), bool), f"{visual_id}: lock.approved must be boolean")
        replacement_reason = lock.get("replacement_reason")
        require(replacement_reason in {None, "technical_error", "visual_error", "user_requested_change"}, f"{visual_id}: invalid replacement_reason")
        if status == "LIVE_VERIFIED":
            require(lock["approved"], f"{visual_id}: LIVE_VERIFIED assets must be locked")
        if lock["approved"]:
            require(status == "LIVE_VERIFIED", f"{visual_id}: only LIVE_VERIFIED assets may be locked as approved")

    print(f"POF visual validation PASSED: {len(visuals)} manifest visual(s), {len(question_owner)} question mapping(s)")


if __name__ == "__main__":
    main()
