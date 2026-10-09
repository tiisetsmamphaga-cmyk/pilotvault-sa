"""Prepare the radio handbook figure used as the base of the Air Law VFR-minima pictures.

usage: python3 scripts/trial_visuals/al_figures.py
Extracts "VFR minima for aeroplanes" (The Pilot's Radio Handbook, page 53 of the book, PDF page 57), crops the
figure, paints out its small number labels with the colour beside them (the pictures add phone-size labels for
the band each question asks about), upscales 2x and writes fig/al/vfr-minima.png. Coordinates are in the
extracted image's pixels (699 x 713).
"""
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageFilter

HERE = Path(__file__).resolve().parent
PDF = HERE.parents[1] / "dd96a06ee49a6d1e.pdf"
OUT = HERE / "fig" / "al"
CROP = (0, 222, 699, 713)
# small labels painted out: (x0, y0, x1, y1)
SMALL = [(108, 265, 152, 283), (178, 316, 209, 334), (430, 312, 464, 331),       # above FL100
         (354, 398, 392, 414), (457, 434, 488, 451), (336, 487, 368, 505),       # below FL100
         (151, 491, 189, 509), (244, 528, 274, 545),                             # in the TMA
         (431, 579, 464, 597), (414, 606, 478, 624)]                             # low, uncontrolled


def paint_out(im, box):
    px = im.load()
    x0, y0, x1, y1 = box
    for y in range(y0, y1):
        c = px[max(x0 - 3, 0), y]
        for x in range(x0, x1):
            px[x, y] = c


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(["pdfimages", "-f", "57", "-l", "57", "-png", "-p", str(PDF), f"{tmp}/i"], check=True)
        im = Image.open(Path(tmp) / "i-057-000.png").convert("RGB")
    for box in SMALL:
        paint_out(im, box)
    im = im.crop(CROP)
    im = im.resize((im.width * 2, im.height * 2), Image.LANCZOS).filter(ImageFilter.UnsharpMask(1.2, 60, 2))
    im.save(OUT / "vfr-minima.png", optimize=True)
    print(im.size)


if __name__ == "__main__":
    main()
