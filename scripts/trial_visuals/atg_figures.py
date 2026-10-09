"""Prepare the Aircraft General Knowledge manual figures used as the base of the ATG trial pictures, in HD.

usage: python3 scripts/trial_visuals/atg_figures.py [name ...]     (needs realesrgan_ncnn_py and pdfimages)

The manual (091e41264c1bdb10.pdf) is a scan at about 87 ppi, too soft for a phone. Each figure is cropped from
the page scan at its native resolution, upscaled 4x with Real-ESRGAN (the anime/line-art model for drawings, the
photo model for photographs) and written to fig/atg/<name>.png. Crop boxes are in 200-dpi page pixels (the page
render is 2084 px wide). Print too small for a phone is covered in atg_phone.py, which adds phone-size labels.
Photos too poor to sharpen (the oil cooler and crankcase photos) are not used.
"""
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageFilter

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
}
# figures already in public/ that are too small: name: (path, model)
SMALL = {
    "compass-deviation": ("explanation-images/navigation/refined-batch-1/nav-compass-deviation-v1.webp", LINE),
}
# photos whose scan screening shows as streaks after upscaling: name: median filter size applied first
DESCREEN = {"cylinder-fins": 3}


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
    if len(pieces) > 1:            # a figure split over two pages: drop the blank margin rows at the join
        pieces = [trim_blank(p, bottom=i == 0) for i, p in enumerate(pieces)]
    out = Image.new("RGB", (max(p.width for p in pieces), sum(p.height for p in pieces)), "white")
    y = 0
    for p in pieces:
        out.paste(p, (0, y))
        y += p.height
    return out


def trim_blank(im, bottom):
    """Remove near-white rows from the bottom (or top) edge of one half of a split figure."""
    g = im.convert("L")
    rows = range(im.height - 1, -1, -1) if bottom else range(im.height)
    cut = 0
    for y in rows:
        dark = sum(1 for x in range(im.width) if g.getpixel((x, y)) < 225)
        if dark > im.width * 0.01:
            break
        cut += 1
    return im.crop((0, 0, im.width, im.height - cut)) if bottom else im.crop((0, cut, im.width, im.height))



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
        if name in DESCREEN:
            im = im.filter(ImageFilter.MedianFilter(DESCREEN[name]))
        hd = upscale(im, model)
        hd.save(OUT / f"{name}.png", optimize=True)
        print(name, im.size, "->", hd.size)


if __name__ == "__main__":
    main()
