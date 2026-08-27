#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "pof-visual-manifest.json"
PATCH = ROOT / "data" / "pof-batch-2-4-working-patch.json"

manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
patch = json.loads(PATCH.read_text(encoding="utf-8"))
existing = {v["visual_id"]: v for v in manifest["visuals"]}

for incoming in patch["visuals"]:
    vid = incoming["visual_id"]
    if vid in existing:
        existing[vid].update(incoming)
    else:
        manifest["visuals"].append(incoming)
        existing[vid] = incoming

MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"Applied {len(patch['visuals'])} POF working visual entries")
