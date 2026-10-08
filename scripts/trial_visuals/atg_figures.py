"""Prepare the Aircraft General Knowledge manual figures used as the base of the ATG trial pictures, in HD.

usage: python3 scripts/trial_visuals/atg_figures.py [name ...]     (needs realesrgan_ncnn_py and pdfimages)

The manual (091e41264c1bdb10.pdf) is a scan at about 87 ppi, too soft for a phone. Each figure is cropped from
the page scan at its native resolution, upscaled 4x with Real-ESRGAN (the anime/line-art model for drawings, the
photo model for photographs), its small printed text is painted out with the colour beside it (the pictures add
phone-size labels instead) and it is written to fig/atg/<name>.png. Crop boxes are in 200-dpi page pixels (the
page render is 2084 px wide); paint-out boxes are in the upscaled figure's pixels.
"""
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
PDF = HERE.parents[1] / "091e41264c1bdb10.pdf"
PUBLIC = HERE.parents[1] / "public"
OUT = HERE / "fig" / "atg"
PAGE_W = 2084            # 200-dpi render width of a page
LINE, PHOTO = 3, 4       # Real-ESRGAN models: x4plus-anime (drawings), x4plus (photographs)

# name: ([(page, (x0, y0, x1, y1)), ...] stacked top to bottom, model)
FIGS = {
    "braced-monoplane": ([(14, (530, 753, 1663, 1449))], PHOTO),
    "valve-timing": ([(55, (739, 1365, 1451, 2088))], LINE),
    "gear-pump": ([(94, (656, 2053, 1544, 2670)), (95, (656, 24, 1544, 311))], LINE),
    "cylinder-fins": ([(82, (706, 1862, 1484, 2597))], PHOTO),
    "oil-pressure-zero": ([(103, (679, 447, 1493, 1083))], LINE),
    "cowl-flap": ([(83, (481, 1826, 1716, 2631))], LINE),
    "hydraulic-brake": ([(48, (686, 796, 1508, 1549))], LINE),
    "oil-cooler": ([(88, (684, 524, 1511, 1345))], PHOTO),
    "main-bearings": ([(91, (695, 1525, 1461, 2250))], PHOTO),
}
# figures already in public/ that are too small: name: (path, model)
SMALL = {
    "compass-deviation": ("explanation-images/navigation/refined-batch-1/nav-compass-deviation-v1.webp", LINE),
}
# small printed text painted out after upscaling: name: [(x0, y0, x1, y1), ...]
PAINT = {}


def page_scan(page, tmp):
    subprocess.run(["pdfimages", "-f", str(page), "-l", str(page), "-png", str(PDF), f"{tmp}/p{page}"], check=True)
    return Image.open(sorted(Path(tmp).glob(f"p{page}-*.png"))[0]).convert("RGB")


def crop(parts):
    with tempfile.TemporaryDirectory() as tmp:
        pieces = []
        for page, box in parts:
            scan = page_scan(page, tmp)
            k = scan.width / PAGE_W
            pieces.append(scan.crop(tuple(round(v * k) for v in box)))
    out = Image.new("RGB", (max(p.width for p in pieces), sum(p.height for p in pieces)), "white")
    y = 0
    for p in pieces:
        out.paste(p, (0, y))
        y += p.height
    return out


def paint_out(im, box):
    px = im.load()
    x0, y0, x1, y1 = box
    for y in range(y0, y1):
        c = px[max(x0 - 4, 0), y]
        for x in range(x0, x1):
            px[x, y] = c


def upscale(im, model):
    from realesrgan_ncnn_py import Realesrgan
    return Realesrgan(gpuid=0, model=model).process_pil(im)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    names = sys.argv[1:] or list(FIGS) + list(SMALL)
    for name in names:
        if name in FIGS:
            parts, model = FIGS[name]
            im = crop(parts)
        else:
            path, model = SMALL[name]
            im = Image.open(PUBLIC / path).convert("RGB")
        hd = upscale(im, model)
        for box in PAINT.get(name, ()):
            paint_out(hd, box)
        hd.save(OUT / f"{name}.png", optimize=True)
        print(name, im.size, "->", hd.size)


if __name__ == "__main__":
    main()
