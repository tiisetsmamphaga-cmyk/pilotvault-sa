#!/usr/bin/env python3
"""Replay Batches 2-4 on a clean branch with valid manifest state transitions."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data/pof-visual-manifest.json"
SCRATCH_REF = "origin/pof-batch-2-rebuild"
PLAN_PATH = "data/pof-batches-2-4-plan.json"


def git_show(ref_path: str) -> str:
    p = subprocess.run(["git", "show", ref_path], cwd=ROOT, text=True, capture_output=True)
    if p.returncode != 0:
        raise SystemExit(p.stderr)
    return p.stdout


def load_plan() -> list[dict]:
    raw = git_show(f"{SCRATCH_REF}:{PLAN_PATH}")
    data = json.loads(raw)
    visuals = [v for batch in data["batches"] for v in batch["visuals"]]
    if len(visuals) != 15:
        raise SystemExit(f"Expected 15 planned visuals, got {len(visuals)}")
    # Locked semantic correction: numerical critical-AoA questions are excluded.
    critical = next(v for v in visuals if v["visual_id"] == "pof-critical-aoa-stall-001")
    if critical["question_ids"] != [1212, 1236, 1324, 1329]:
        raise SystemExit(f"Critical-AoA mapping drifted: {critical['question_ids']}")
    turn = next(v for v in visuals if v["visual_id"] == "pof-turn-lift-components-001")
    if turn["source"].get("figure") != "1-40" or turn["source"].get("page") != 34:
        raise SystemExit("Balanced-turn source must remain handbook Figure 1-40 page 34")
    return visuals


def write(data: dict) -> None:
    MANIFEST.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def source_found() -> None:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if len(data.get("visuals", [])) != 5:
        raise SystemExit("Clean replay must start from the five locked Batch 1 visuals only")
    plan = load_plan()
    existing = {v["visual_id"] for v in data["visuals"]}
    if existing & {v["visual_id"] for v in plan}:
        raise SystemExit("Planned visual already exists in clean base manifest")
    for v in plan:
        v["assets"] = {"master_asset": None, "web_asset": None}
        v["status"] = "SOURCE_FOUND"
        v["qa"] = {"technical": False, "teaching": False, "visual": False, "preview": False, "live": False}
        v["lock"] = {"approved": False, "replacement_reason": None}
    data["visuals"].extend(plan)
    write(data)
    print("SOURCE_FOUND replay prepared: 15 visuals; total manifest visuals=20")


def main() -> None:
    if len(sys.argv) != 2 or sys.argv[1] != "source-found":
        raise SystemExit("usage: replay_pof_batches_2_4.py source-found")
    source_found()


if __name__ == "__main__":
    main()
