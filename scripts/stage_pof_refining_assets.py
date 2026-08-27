#!/usr/bin/env python3
"""Attach reviewed Batch 2-4 raster paths and move SOURCE_FOUND -> REFINING."""
from __future__ import annotations

import json
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "pof-visual-manifest.json"

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
    "pof-critical-aoa-stall-001": (4, "pof-critical-aoa-stall-v3"),
    "pof-stability-types-001": (4, "pof-stability-types-v1"),
    "pof-turn-lift-components-001": (4, "pof-turn-lift-components-v1"),
    "pof-washout-wing-twist-001": (4, "pof-washout-wing-twist-v1"),
}


def main() -> None:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    index = {v["visual_id"]: v for v in data["visuals"]}

    for visual_id, (batch, stem) in ASSETS.items():
        visual = index.get(visual_id)
        if visual is None:
            raise SystemExit(f"Missing manifest visual: {visual_id}")
        if visual.get("status") not in {"SOURCE_FOUND", "REFINING"}:
            raise SystemExit(f"{visual_id}: expected SOURCE_FOUND/REFINING, got {visual.get('status')}")

        rel_dir = f"public/explanation-images/principles-of-flight/refined-batch-{batch}"
        png = f"{rel_dir}/{stem}.png"
        webp = f"{rel_dir}/{stem}.webp"
        for rel, expected_format in ((png, "PNG"), (webp, "WEBP")):
            path = ROOT / rel
            if not path.exists() or path.stat().st_size <= 0:
                raise SystemExit(f"Missing/empty asset: {rel}")
            with Image.open(path) as im:
                im.verify()
                if im.format != expected_format:
                    raise SystemExit(f"{rel}: expected {expected_format}, got {im.format}")
            with Image.open(path) as im:
                if im.width < 1000 or im.height < 600:
                    raise SystemExit(f"{rel}: image is too small ({im.width}x{im.height})")

        visual["assets"] = {"master_asset": png, "web_asset": webp}
        visual["status"] = "REFINING"
        visual["qa"] = {"technical": False, "teaching": False, "visual": False, "preview": False, "live": False}
        visual["lock"] = {"approved": False, "replacement_reason": None}

    MANIFEST.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Staged {len(ASSETS)} visuals at REFINING with decoded PNG/WebP pairs")


if __name__ == "__main__":
    main()
