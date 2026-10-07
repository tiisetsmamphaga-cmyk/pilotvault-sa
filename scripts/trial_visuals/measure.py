"""Zoomed, gridded crop of a reference picture, for measuring an object before redrawing it as clean SVG.

usage: python3 scripts/trial_visuals/measure.py <image> <x0> <y0> <x1> <y1> <out.png> [zoom] [step]
Red vertical lines every `step` px (labelled), green horizontal lines every step/2 px, in source coordinates.
Read the outline points off the grid, then write them as paths in a component module (see aircraft.py).
"""
import sys

from PIL import Image, ImageDraw


def grid(src, box, out, zoom=4, step=20):
    x0, y0, x1, y1 = box
    im = Image.open(src).convert("RGB").crop(box)
    im = im.resize(((x1 - x0) * zoom, (y1 - y0) * zoom), Image.NEAREST)
    d = ImageDraw.Draw(im)
    for x in range(x0 - x0 % step + step, x1, step):
        X = (x - x0) * zoom
        d.line([(X, 0), (X, im.height)], fill=(255, 0, 0))
        d.text((X + 2, 2), str(x), fill=(255, 0, 0))
    half = max(step // 2, 1)
    for y in range(y0 - y0 % half + half, y1, half):
        Y = (y - y0) * zoom
        d.line([(0, Y), (im.width, Y)], fill=(0, 160, 0))
        d.text((2, Y + 2), str(y), fill=(0, 120, 0))
    im.save(out)


if __name__ == "__main__":
    a = sys.argv[1:]
    grid(a[0], tuple(int(v) for v in a[1:5]), a[5], int(a[6]) if len(a) > 6 else 4, int(a[7]) if len(a) > 7 else 20)
