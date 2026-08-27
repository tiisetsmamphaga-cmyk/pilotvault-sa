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
ASSET_ROOT = "public/explanation-images/principles-of-flight"

ASSETS = {
    "pof-angle-of-attack-definition-001": (2, "pof-angle-of-attack-definition-v3"),
    "pof-chord-line-001": (2, "pof-chord-line-v2"),
    "pof-four-forces-equilibrium-001": (2, "pof-four-forces-level-flight-v2"),
    "pof-lift-relative-airflow-001": (2, "pof-lift-relative-airflow-v2"),
    "pof-venturi-bernoulli-001": (2, "pof-venturi-bernoulli-v2"),
    "pof-angle-of-incidence-001": (3, "pof-angle-of-incidence-v5"),
    "pof-centre-of-pressure-001": (3, "pof-centre-of-pressure-v1"),
    "pof-relative-airflow-001": (3, "pof-relative-airflow-v1"),
    "pof-speed-squared-lift-drag-001": (3, "pof-speed-squared-lift-drag-v1"),
    "pof-wing-area-lift-drag-001": (3, "pof-wing-area-lift-drag-v1"),
    "pof-aircraft-axes-controls-001": (4, "pof-aircraft-axes-controls-v1"),
    "pof-critical-aoa-stall-001": (4, "pof-critical-aoa-stall-v4"),
    "pof-stability-types-001": (4, "pof-stability-types-v1"),
    "pof-turn-lift-components-001": (4, "pof-turn-lift-components-v4"),
    "pof-washout-wing-twist-001": (4, "pof-washout-wing-twist-v1"),
}


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
    if set(ASSETS) != {v["visual_id"] for v in visuals}:
        raise SystemExit("Asset registry does not exactly match the 15 planned visuals")
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


def refining() -> None:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    visuals = {v["visual_id"]: v for v in data.get("visuals", [])}
    if len(data.get("visuals", [])) != 20:
        raise SystemExit(f"REFINING replay requires exactly 20 manifest visuals; got {len(data.get('visuals', []))}")
    for visual_id, (batch, stem) in ASSETS.items():
        v = visuals.get(visual_id)
        if not v or v.get("status") != "SOURCE_FOUND":
            raise SystemExit(f"{visual_id}: expected SOURCE_FOUND before REFINING; got {None if not v else v.get('status')}")
        master = f"{ASSET_ROOT}/refined-batch-{batch}/{stem}.png"
        web = f"{ASSET_ROOT}/refined-batch-{batch}/{stem}.webp"
        for path in (master, web):
            p = ROOT / path
            if not p.exists() or p.stat().st_size == 0:
                raise SystemExit(f"Missing raster asset: {path}")
        v["assets"] = {"master_asset": master, "web_asset": web}
        v["status"] = "REFINING"
        v["qa"] = {"technical": False, "teaching": False, "visual": False, "preview": False, "live": False}
        v["lock"] = {"approved": False, "replacement_reason": None}
    write(data)
    print("REFINING replay prepared: 15 visuals attached to reviewed raster pairs")


def qa_approved() -> None:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    visuals = {v["visual_id"]: v for v in data.get("visuals", [])}
    if len(data.get("visuals", [])) != 20:
        raise SystemExit(f"QA_APPROVED promotion requires exactly 20 manifest visuals; got {len(data.get('visuals', []))}")
    for visual_id, (batch, stem) in ASSETS.items():
        v = visuals.get(visual_id)
        if not v or v.get("status") != "REFINING":
            raise SystemExit(f"{visual_id}: expected REFINING before QA_APPROVED; got {None if not v else v.get('status')}")
        expected = {
            "master_asset": f"{ASSET_ROOT}/refined-batch-{batch}/{stem}.png",
            "web_asset": f"{ASSET_ROOT}/refined-batch-{batch}/{stem}.webp",
        }
        if v.get("assets") != expected:
            raise SystemExit(f"{visual_id}: asset drift: {v.get('assets')} != {expected}")
        for path in expected.values():
            p = ROOT / path
            if not p.exists() or p.stat().st_size == 0:
                raise SystemExit(f"Missing approved raster asset: {path}")
        v["status"] = "QA_APPROVED"
        v["qa"] = {"technical": True, "teaching": True, "visual": True, "preview": False, "live": False}
        v["lock"] = {"approved": False, "replacement_reason": None}
    write(data)
    print("QA_APPROVED promotion prepared: 15 rendered and technically reviewed visuals")


def main() -> None:
    allowed={"source-found","refining","qa-approved"}
    if len(sys.argv) != 2 or sys.argv[1] not in allowed:
        raise SystemExit("usage: replay_pof_batches_2_4.py source-found|refining|qa-approved")
    if sys.argv[1] == "source-found": source_found()
    elif sys.argv[1] == "refining": refining()
    else: qa_approved()


if __name__ == "__main__":
    main()
