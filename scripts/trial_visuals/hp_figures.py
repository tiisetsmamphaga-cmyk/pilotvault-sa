"""Prepare the JAA Human Performance manual figures used as the base of the approach-illusion pictures.

usage: python3 scripts/trial_visuals/hp_figures.py
Extracts the embedded rasters of pages 145-149 (Figures 8.25, 8.28a, 8.29a, 8.30) from the manual in the repo
root, paints out the small legend box of 8.28a/8.29a with the sky colour of the same rows (the picture gets
phone-size labels instead), upscales 2x (Lanczos) with a light sharpen, and writes fig/hp/*.png.
"""
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageFilter

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
PDF = REPO / "484641488-335583371-DOC045-2-JAA-PPL-Human-Performance-pdf (1).pdf"
OUT = HERE / "fig" / "hp"

# extracted image -> (output name, legend box to paint out or None)
FIGURES = {
    "i-145-002.png": ("false-horizon-8-25.png", None),
    "i-147-008.png": ("upslope-8-28a.png", (400, 32, 742, 168)),
    "i-148-010.png": ("downslope-8-29a.png", (392, 30, 732, 167)),
    "i-149-012.png": ("black-hole-8-30.png", None),
}


def paint_out(im, box, sample_x=760):
    """Fill the box row by row with the colour at sample_x (the sky gradient runs top to bottom)."""
    px = im.load()
    x0, y0, x1, y1 = box
    for y in range(y0, y1):
        c = px[sample_x, y]
        for x in range(x0, x1):
            px[x, y] = c
    return im


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(["pdfimages", "-f", "145", "-l", "149", "-png", "-p", str(PDF), f"{tmp}/i"], check=True)
        for src, (name, box) in FIGURES.items():
            im = Image.open(Path(tmp) / src).convert("RGB")
            if box:
                im = paint_out(im, box)
            im = im.resize((im.width * 2, im.height * 2), Image.LANCZOS).filter(ImageFilter.UnsharpMask(1.2, 60, 2))
            im.save(OUT / name, optimize=True)
            print(name, im.size)


if __name__ == "__main__":
    main()
