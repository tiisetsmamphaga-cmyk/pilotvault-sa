from pathlib import Path

path = Path(__file__).resolve().parents[1] / "app" / "practice" / "[subject]" / "components" / "principles-of-flight-visual.tsx"
text = path.read_text(encoding="utf-8")

replacements = {
    "angle-of-attack-v5.png": "angle-of-attack-v8.png",
    "boundary-layer-transition-v4.png": "boundary-layer-transition-v5.png",
    "centre-pressure-shift-v4.png": "centre-pressure-shift-v5.png",
    "lift-pressure-distribution-v4.png": "lift-pressure-distribution-v5.png",
    "lift-drag-directions-v4.png": "lift-drag-directions-v5.png",
    "vx-vy-v4.png": "vx-vy-v7.png",
    "v-speeds-v4.png": "v-speeds-v5.png",
    "steady-climb-forces-v4.png": "steady-climb-forces-v6.png",
    "drag-curves-v4.png": "drag-curves-v6.png",
    "wingtip-vortices-induced-drag-v4.png": "wingtip-vortices-induced-drag-v6.png",
    "wind-glide-groundpath-v4.png": "wind-glide-groundpath-v7.png",
    "static-pressure-v4.png": "static-pressure-v7.png",
    "spin-autorotation-v4.png": "spin-autorotation-v5.png",
    "stall-speed-load-factor-v4.png": "stall-speed-load-factor-v6.png",
    "trim-tab-v4.png": "trim-tab-v5.png",
}

updated = text
for old, new in replacements.items():
    updated = updated.replace(old, new)

if updated != text:
    path.write_text(updated, encoding="utf-8")
    print("Updated POF mapper to QA-approved versioned assets")
else:
    print("POF mapper already uses QA-approved versioned assets")
