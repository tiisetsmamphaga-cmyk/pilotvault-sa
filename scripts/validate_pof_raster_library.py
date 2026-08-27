#!/usr/bin/env python3
"""Validate the bulk POF raster library and its promotion/lock state."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = Path("data/pof-raster-library-state.json")
REPORT_PATH = Path("data/pof-raster-qa-report.json")
RASTER_PREFIX = "public/explanation-images/principles-of-flight/raster-complete/"
PUBLIC_PREFIX = "/explanation-images/principles-of-flight/raster-complete/"

FORWARD = {
    "MAPPED": {"PRODUCTION_READY"},
    "PRODUCTION_READY": {"LIVE_VERIFIED"},
    "LIVE_VERIFIED": set(),
}
REPLACEMENT_REASONS = {"technical_error", "visual_error", "user_requested_change"}


def fail(message: str) -> None:
    print(f"POF raster library validation FAILED: {message}", file=sys.stderr)
    raise SystemExit(1)


def run_git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def read_json(path: Path) -> dict:
    try:
        return json.loads((ROOT / path).read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"cannot read {path}: {exc}")


def read_json_at(ref: str, path: Path) -> dict | None:
    result = run_git("show", f"{ref}:{path.as_posix()}")
    if result.returncode != 0:
        return None
    try:
        return json.loads(result.stdout)
    except Exception as exc:
        fail(f"{path} at {ref} is invalid JSON: {exc}")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_current(state: dict, report: dict) -> None:
    if state.get("schema_version") != 1 or report.get("schema_version") != 1:
        fail("unsupported schema version")
    if state.get("subject") != "principles-of-flight" or report.get("subject") != "principles-of-flight":
        fail("state/report subject must be principles-of-flight")

    status = state.get("status")
    if status not in FORWARD:
        fail(f"invalid library status: {status}")

    expected_counts = {
        "active_question_count": 360,
        "active_visual_count": 79,
        "library_asset_count": 83,
    }
    for field, expected in expected_counts.items():
        if state.get(field) != expected:
            fail(f"{field} must be {expected}, got {state.get(field)}")

    if state.get("no_baked_banner") is not True:
        fail("new POF raster assets must not contain a baked PilotVault banner")
    if state.get("website_branding") is not True:
        fail("PilotVault branding for the new POF raster library must live in the website UI")

    qa = state.get("qa") or {}
    for field in ("source_body_fidelity", "raster_integrity", "preview_build"):
        if qa.get(field) is not True:
            fail(f"qa.{field} must be true before the library can remain mapped")

    lock = state.get("lock") or {}
    if status == "LIVE_VERIFIED":
        if qa.get("live") is not True or lock.get("approved") is not True:
            fail("LIVE_VERIFIED requires qa.live=true and lock.approved=true")
    else:
        if qa.get("live") is not False or lock.get("approved") is not False:
            fail(f"{status} must remain unlocked with qa.live=false")

    assets = report.get("assets")
    if not isinstance(assets, list) or len(assets) != state["library_asset_count"]:
        fail("QA report asset count does not match library state")
    if report.get("asset_count") != len(assets):
        fail("QA report asset_count is stale")
    if report.get("max_batch_size") != 5:
        fail("POF QA batches must remain capped at five concepts")
    if report.get("legacy_banner_sources_cropped") != len(assets):
        fail("every migrated legacy source must have its baked banner cropped")

    seen_web: set[str] = set()
    seen_master: set[str] = set()
    for record in assets:
        master_rel = str(record.get("master_asset", ""))
        web_rel = str(record.get("web_asset", ""))
        public_url = str(record.get("public_web_url", ""))

        if not master_rel.startswith(RASTER_PREFIX) or not master_rel.lower().endswith(".png"):
            fail(f"invalid master asset path: {master_rel}")
        if not web_rel.startswith(RASTER_PREFIX) or not web_rel.lower().endswith(".webp"):
            fail(f"invalid web asset path: {web_rel}")
        if "/qa/" in master_rel or "/qa/" in web_rel:
            fail("QA contact sheets cannot be part of the locked production library")
        if not public_url.startswith(PUBLIC_PREFIX) or not public_url.lower().endswith(".webp"):
            fail(f"invalid public web path: {public_url}")
        if ".svg" in public_url.lower():
            fail("production raster library cannot expose SVG URLs")
        if master_rel in seen_master or web_rel in seen_web:
            fail("duplicate production asset path in QA report")
        seen_master.add(master_rel)
        seen_web.add(web_rel)

        master = ROOT / master_rel
        web = ROOT / web_rel
        if not master.is_file() or not web.is_file():
            fail(f"missing raster pair for {record.get('source_name')}")
        if sha256(master) != record.get("png_sha256"):
            fail(f"locked PNG hash mismatch: {master_rel}")
        if sha256(web) != record.get("webp_sha256"):
            fail(f"locked WebP hash mismatch: {web_rel}")

    print(f"Validated {len(assets)} hashed POF raster asset pairs at state {status}")


def validate_transition(base_sha: str, state: dict, report: dict) -> None:
    old_state = read_json_at(base_sha, STATE_PATH)
    old_report = read_json_at(base_sha, REPORT_PATH)

    if old_state is None:
        if state.get("status") != "MAPPED":
            fail("new raster library state must enter repository history at MAPPED")
        print("Validated initial POF raster library state at MAPPED")
        return

    old_status = old_state.get("status")
    new_status = state.get("status")

    if old_status == "LIVE_VERIFIED":
        changed = old_state != state or old_report != report
        if changed:
            reason = (state.get("lock") or {}).get("replacement_reason")
            if reason not in REPLACEMENT_REASONS:
                fail("LIVE_VERIFIED raster library changed without an approved replacement reason")
            if new_status != "MAPPED":
                fail("a locked raster library replacement must reopen at MAPPED")
            if (state.get("lock") or {}).get("approved") is not False:
                fail("a reopened raster library must be unlocked")
        return

    if old_status == new_status:
        return
    if new_status not in FORWARD.get(old_status, set()):
        fail(f"invalid raster library transition {old_status} -> {new_status}")

    print(f"Validated POF raster library transition {old_status} -> {new_status}")


def main() -> None:
    if len(sys.argv) != 2 or not sys.argv[1].strip():
        fail("usage: validate_pof_raster_library.py <base-sha>")

    state = read_json(STATE_PATH)
    report = read_json(REPORT_PATH)
    validate_current(state, report)
    validate_transition(sys.argv[1].strip(), state, report)
    print("POF raster library validation PASSED")


if __name__ == "__main__":
    main()
