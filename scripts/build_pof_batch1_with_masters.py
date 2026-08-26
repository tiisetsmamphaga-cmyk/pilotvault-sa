from __future__ import annotations

import hashlib
import sys
from pathlib import Path

import build_pof_batch1_exact as exact

EXPECTED_PNG_SHA256 = {
    "pof-bank-load-factor-v1.png": "8fd90eda56ddaeef7a83a73e0208e3c7d9a4a426e461b450e63c399ee9aae6d3",
    "pof-longitudinal-stability-v1.png": "25d09a12c9df3f43f533899e511b8b5579562b5e9d2dc9ca9d1e56db555c5775",
    "pof-glide-ld-v1.png": "74b2a2c9447019ee838650113de402a32fce85141ffb7e702378668a80e3ee76",
    "pof-drag-curves-v1.png": "e086422dfd3b36a0cbd967bbc97451fa6e5f532cba99b1630da5a53d2c50bada",
    "pof-dihedral-lateral-stability-v1.png": "c3949751b561017d426a57a6565689d8df158f0fad20ad7cf5294f8bae92f91a",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("usage: build_pof_batch1_with_masters.py INPUT_PDF OUTPUT_DIR")

    source = Path(sys.argv[1])
    output = Path(sys.argv[2])
    original_save = exact.save

    def save_master_and_web(canvas, out, name, quality=88):
        out.mkdir(parents=True, exist_ok=True)
        png_name = Path(name).with_suffix(".png").name
        png_path = out / png_name
        canvas.save(png_path, "PNG", optimize=True)
        actual_png = sha256(png_path)
        expected_png = EXPECTED_PNG_SHA256[png_name]
        if actual_png != expected_png:
            raise RuntimeError(
                f"{png_name}: deterministic PNG hash mismatch: {actual_png} != {expected_png}"
            )
        print(f"VERIFIED {png_name}: {png_path.stat().st_size} bytes, sha256={actual_png}")
        original_save(canvas, out, name, quality)

    exact.save = save_master_and_web
    exact.build(source, output)

    files = sorted(output.iterdir())
    if len(files) != 10:
        raise RuntimeError(f"Expected 10 final assets (5 PNG + 5 WebP); found {len(files)}")


if __name__ == "__main__":
    main()
