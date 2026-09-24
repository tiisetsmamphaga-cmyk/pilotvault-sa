"""Strip the baked-in PilotVault frame from ATG explanation images so the site's card supplies it.

The card on the practice page already shows the title and the KEY FACT panel, so the image itself should be
only the diagram: no navy banner, no caption line, no outer frame and no text-only fact boxes.

    python3 clean.py <list.txt>   list lines: <folder>/<stem>.<ext> as used in explanation_image_url
    python3 clean.py --phak       the PHAK-refined set in phak-question-specific-v2

Drawn images are re-rendered from their SVG source by render_clean.js, which removes those parts; textbook extracts (webp only) are cropped to
the area inside the frame. Output: public/explanation-images/aircraft-technical-and-general/clean-v1/<stem>.webp
"""
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

REPO = Path(__file__).resolve().parents[2]
ATG = REPO / "public/explanation-images/aircraft-technical-and-general"
OUT = ATG / "clean-v1"
HERE = Path(__file__).parent

def trim(img, pad=24):
    a = np.asarray(img.convert("RGB")).astype(int)
    ink = (np.abs(a - 255).sum(axis=2) > 24)
    ys, xs = np.where(ink)
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    x0, y0 = max(0, x0 - pad), max(0, y0 - pad)
    x1, y1 = min(img.width, x1 + pad), min(img.height, y1 + pad)
    return img.crop((x0, y0, x1, y1))


def main(listfile):
    OUT.mkdir(parents=True, exist_ok=True)
    work = Path("/tmp/atg-clean")
    work.mkdir(exist_ok=True)
    svgs = []
    for rel in Path(listfile).read_text().split():
        folder, name = rel.split("/")
        stem = name.rsplit(".", 1)[0]
        src_svg = ATG / folder / f"{stem}.svg"
        if src_svg.exists():
            (work / f"{stem}.svg").write_text(src_svg.read_text())
            svgs.append(stem)
        else:
            # textbook extract: keep only what sits inside the frame (x 32-1168, y 134-566 at 1.5x)
            im = Image.open(ATG / folder / name).convert("RGB")
            k = im.width / 1200
            im = trim(im.crop((int(32 * k), int(134 * k), int(1168 * k), int(566 * k))))
            im.save(OUT / f"{stem}.webp", quality=90, method=6)
            print("cropped", stem, im.size)
    if svgs:
        subprocess.run(["node", str(HERE / "render_clean.js"), str(work), str(work / "png"), *[f"{s}.svg" for s in svgs]],
                       check=True, stdout=subprocess.DEVNULL)
        for stem in svgs:
            im = trim(Image.open(work / "png" / f"{stem}.png"))
            im.save(OUT / f"{stem}.webp", quality=90, method=6)
            print("cleaned", stem, im.size)


def phak():
    """PHAK-refined images: keep the left diagram panel, dropping their header, text column and footer."""
    k = 1920 / 1400
    for p in sorted((ATG / "phak-question-specific-v2").glob("*.webp")):
        a = np.asarray(Image.open(p).convert("RGB")).copy()
        band = a[:, 1184:1198].astype(int)  # the panel's right border; text that crosses it is darker and kept
        grey = (np.abs(band - band.mean(axis=2, keepdims=True)).sum(axis=2) < 30) & (band.mean(axis=2) > 170) & (band.mean(axis=2) < 245)
        a[:, 1184:1198][grey] = 255
        im = Image.fromarray(a).crop((int(48 * k) + 6, int(114 * k) + 6, 1215, int(784 * k) - 6))
        trim(im).save(OUT / p.name, quality=90, method=6)
        print("cropped", p.stem, im.size)
    # q-2632's "RESULTING MOTION" label runs under the text column in the source; the cleaned copy was
    # patched by hand to drop the cut-off label (see data/atg-explanations/image-review-2026-09-24.md).


if __name__ == "__main__":
    phak() if sys.argv[1:] == ["--phak"] else main(sys.argv[1])
