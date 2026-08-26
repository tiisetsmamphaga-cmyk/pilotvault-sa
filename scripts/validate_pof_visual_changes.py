#!/usr/bin/env python3
"""Validate POF visual changes and the full promotion history.

This protects the production workflow from state skipping, silent modification of
approved assets, and reintroduction of SVG/vector explanation visuals.

For long-lived visual branches, promotion may move `main` across several already-
validated workflow states in one ref update. In that case we validate every
manifest snapshot in the commit range instead of incorrectly treating the final
state as a direct jump from the production manifest.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = Path("data/pof-visual-manifest.json")
POF_RENDERER = ROOT / "app" / "practice" / "[subject]" / "components" / "principles-of-flight-visual.tsx"

FORWARD = {
    "SOURCE_FOUND": {"REFINING"},
    "REFINING": {"QA_FAILED", "QA_APPROVED"},
    "QA_FAILED": {"REFINING"},
    "QA_APPROVED": {"PREVIEW_READY"},
    "PREVIEW_READY": {"MAPPED"},
    "MAPPED": {"PRODUCTION_READY"},
    "PRODUCTION_READY": {"LIVE_VERIFIED"},
    "LIVE_VERIFIED": set(),
}
REOPEN_STATES = {"REFINING", "QA_FAILED"}
REPLACEMENT_REASONS = {"technical_error", "visual_error", "user_requested_change"}


def fail(message: str) -> None:
    print(f"POF visual change validation FAILED: {message}", file=sys.stderr)
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


def load_manifest_at(ref: str) -> dict:
    result = run_git("show", f"{ref}:{MANIFEST_PATH.as_posix()}")
    if result.returncode != 0:
        return {"visuals": []}
    try:
        return json.loads(result.stdout)
    except Exception as exc:
        fail(f"manifest at {ref} is invalid JSON: {exc}")


def load_current_manifest() -> dict:
    path = ROOT / MANIFEST_PATH
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"cannot read current manifest: {exc}")


def reject_new_svg_assets(base_sha: str) -> None:
    result = run_git(
        "diff",
        "--diff-filter=AM",
        "--name-only",
        base_sha,
        "HEAD",
        "--",
        "public/explanation-images/principles-of-flight",
    )
    if result.returncode != 0:
        fail(f"git diff failed while checking POF assets: {result.stderr.strip()}")

    svg_paths = [line.strip() for line in result.stdout.splitlines() if line.strip().lower().endswith(".svg")]
    if svg_paths:
        fail(
            "new or modified POF SVG/vector explanation assets are forbidden: "
            + ", ".join(svg_paths)
        )


def reject_svg_references() -> None:
    manifest_text = (ROOT / MANIFEST_PATH).read_text(encoding="utf-8").lower()
    if ".svg" in manifest_text:
        fail("the POF manifest contains an SVG reference")

    if POF_RENDERER.exists() and ".svg" in POF_RENDERER.read_text(encoding="utf-8").lower():
        fail("principles-of-flight-visual.tsx contains an SVG reference")


def index_visuals(manifest: dict) -> dict[str, dict]:
    visuals = manifest.get("visuals", [])
    if not isinstance(visuals, list):
        fail("manifest.visuals must be an array")
    result: dict[str, dict] = {}
    for visual in visuals:
        if not isinstance(visual, dict) or not isinstance(visual.get("visual_id"), str):
            fail("every manifest visual must have a string visual_id")
        result[visual["visual_id"]] = visual
    return result


def validate_pair(old_manifest: dict, new_manifest: dict, context: str) -> None:
    old = index_visuals(old_manifest)
    new = index_visuals(new_manifest)

    for visual_id, visual in new.items():
        if visual_id not in old and visual.get("status") != "SOURCE_FOUND":
            fail(f"{context}: {visual_id}: new visuals must enter the workflow at SOURCE_FOUND")

    for visual_id, old_visual in old.items():
        if visual_id not in new:
            if old_visual.get("status") == "LIVE_VERIFIED":
                fail(f"{context}: {visual_id}: LIVE_VERIFIED visuals cannot be deleted")
            continue

        new_visual = new[visual_id]
        old_status = old_visual.get("status")
        new_status = new_visual.get("status")

        if old_status == "LIVE_VERIFIED" and old_visual != new_visual:
            reason = new_visual.get("lock", {}).get("replacement_reason")
            if reason not in REPLACEMENT_REASONS:
                fail(
                    f"{context}: {visual_id}: approved LIVE_VERIFIED visual changed without an explicit "
                    "technical_error, visual_error, or user_requested_change replacement reason"
                )
            if new_status not in REOPEN_STATES:
                fail(
                    f"{context}: {visual_id}: an approved visual must be reopened to "
                    "REFINING or QA_FAILED before replacement"
                )
            continue

        if old_status == new_status:
            continue

        allowed = FORWARD.get(old_status, set())
        if new_status in allowed:
            continue

        if old_status != "LIVE_VERIFIED" and new_status in REOPEN_STATES:
            continue

        fail(
            f"{context}: {visual_id}: invalid state transition "
            f"{old_status} -> {new_status}; stages may not be skipped"
        )


def manifest_history(base_sha: str) -> list[tuple[str, dict]]:
    result = run_git(
        "rev-list",
        "--reverse",
        "--ancestry-path",
        f"{base_sha}..HEAD",
        "--",
        MANIFEST_PATH.as_posix(),
    )
    if result.returncode != 0:
        fail(f"cannot enumerate manifest history: {result.stderr.strip()}")

    snapshots: list[tuple[str, dict]] = [(base_sha, load_manifest_at(base_sha))]
    for sha in [line.strip() for line in result.stdout.splitlines() if line.strip()]:
        snapshots.append((sha, load_manifest_at(sha)))

    current = load_current_manifest()
    if snapshots[-1][1] != current:
        snapshots.append(("HEAD", current))
    return snapshots


def validate_transitions(base_sha: str) -> None:
    snapshots = manifest_history(base_sha)
    for index in range(1, len(snapshots)):
        old_ref, old_manifest = snapshots[index - 1]
        new_ref, new_manifest = snapshots[index]
        validate_pair(old_manifest, new_manifest, f"{old_ref[:8]} -> {new_ref[:8]}")
    print(f"Validated {max(0, len(snapshots) - 1)} manifest transition(s) across promotion history")


def main() -> None:
    if len(sys.argv) != 2 or not sys.argv[1].strip():
        fail("usage: validate_pof_visual_changes.py <base-sha>")

    base_sha = sys.argv[1].strip()
    reject_new_svg_assets(base_sha)
    reject_svg_references()
    validate_transitions(base_sha)
    print("POF visual change validation PASSED")


if __name__ == "__main__":
    main()
