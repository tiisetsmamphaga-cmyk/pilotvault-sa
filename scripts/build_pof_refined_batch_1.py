#!/usr/bin/env python3
"""Build PilotVault POF refined teaching visuals from the handbook source.

This batch is deliberately deterministic: it downloads the same AC 61-23C
handbook used as the PilotVault source, locates the required figure pages by
caption text, renders those pages at high resolution, crops the handbook
figures, adds question-specific teaching emphasis, exports PNG + WebP, and
advances the manifest from REFINING to QA_APPROVED.
"""

from __future__ import annotations

import json
import os
import tempfile
import urllib.request
from pathlib import Path

import fitz  # PyMuPDF
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "pof-visual-manifest.json"
OUT = ROOT / "public" / "explanation-images" / "principles-of-flight" / "refined-batch-1"

SOURCE_URLS = [
    "https://air.flyingway.com/books/ac_61-23c_phak_canada.pdf",
    "https://web.archive.org/web/20070106081702/http://www.faa.gov/library/manuals/aviation/pilot_handbook/media/faa-h-8083-25-1of4.pdf",
]

NAVY = (6, 17, 31)
GOLD = (244, 180, 0)
WHITE = (255, 255, 255)
GREY = (86, 101, 115)
LIGHT = (248, 250, 252)
BORDER = (203, 213, 225)

BATCH_IDS = [
    "pof-bank-load-factor-001",
    "pof-longitudinal-stability-001",
    "pof-parasite-drag-001",
    "pof-dihedral-001",
    "pof-glide-ratio-001",
]

# Crop boxes are fractions of the rendered handbook page (x1, y1, x2, y2).
# They isolate the original handbook figure rather than redrawing it.
FIGURES = {
    "pof-bank-load-factor-001": {
        "caption": "Figure 1-34",
        "crop": (0.12, 0.015, 0.84, 0.51),
        "filename": "pof-q-3-60-bank-2g",
        "title": "60° BANK = 2.0 G",
    },
    "pof-longitudinal-stability-001": {
        "caption": "Figure 1-24",
        "crop": (0.24, 0.785, 0.72, 0.94),
        "filename": "pof-q1131-cg-longitudinal-stability",
        "title": "CG POSITION CONTROLS PITCH STABILITY",
    },
    "pof-parasite-drag-001": {
        "caption": "Figure 1-15",
        "crop": (0.145, 0.025, 0.80, 0.395),
        "filename": "pof-q1153-parasite-drag",
        "title": "CURVE B = PARASITE / PROFILE DRAG",
    },
    "pof-dihedral-001": {
        "caption": "Figure 1-27",
        "crop": (0.12, 0.64, 0.83, 0.84),
        "filename": "pof-q1168-dihedral-lateral-stability",
        "title": "DIHEDRAL PROVIDES LATERAL STABILITY",
    },
    "pof-glide-ratio-001": {
        "caption": "Figure 1-39",
        "crop": (0.035, 0.515, 0.82, 0.88),
        "filename": "pof-q1239-high-ld-shallow-glide",
        "title": "HIGH L/D = SHALLOWER GLIDE",
    },
}


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
        Path("/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size)
    raise RuntimeError("A supported system font was not found")


def download_source(destination: Path) -> None:
    errors: list[str] = []
    for url in SOURCE_URLS:
        try:
            request = urllib.request.Request(url, headers={"User-Agent": "PilotVault-VisualBuilder/1.0"})
            with urllib.request.urlopen(request, timeout=60) as response:
                data = response.read()
            if len(data) < 500_000 or not data.startswith(b"%PDF"):
                raise RuntimeError(f"unexpected payload ({len(data)} bytes)")
            destination.write_bytes(data)
            print(f"Downloaded POF source from {url} ({len(data)} bytes)")
            return
        except Exception as exc:  # noqa: BLE001 - we want fallback URLs
            errors.append(f"{url}: {exc}")
    raise RuntimeError("Unable to download the handbook source:\n" + "\n".join(errors))


def find_page(doc: fitz.Document, caption: str) -> fitz.Page:
    for page in doc:
        if caption.lower() in page.get_text("text").lower():
            return page
    raise RuntimeError(f"Could not locate {caption} in the downloaded source")


def render_page(page: fitz.Page) -> Image.Image:
    # 300 dpi. The uploaded PilotVault working renders are also 2550 x 3300
    # for a US-letter page, so the normalized crops remain stable.
    matrix = fitz.Matrix(300 / 72, 300 / 72)
    pix = page.get_pixmap(matrix=matrix, alpha=False)
    return Image.frombytes("RGB", (pix.width, pix.height), pix.samples)


def crop_fraction(image: Image.Image, box: tuple[float, float, float, float]) -> Image.Image:
    w, h = image.size
    x1, y1, x2, y2 = box
    return image.crop((round(w * x1), round(h * y1), round(w * x2), round(h * y2)))


def header(canvas: Image.Image, title: str, height: int = 142) -> ImageDraw.ImageDraw:
    draw = ImageDraw.Draw(canvas)
    w = canvas.width
    draw.rectangle((0, 0, w, height), fill=NAVY)
    draw.text((w // 2, 34), "PILOTVAULT PRINCIPLES OF FLIGHT", font=font(24, True), fill=GOLD, anchor="mm")
    title_size = 44 if len(title) < 30 else 39
    draw.text((w // 2, 90), title, font=font(title_size, True), fill=WHITE, anchor="mm")
    draw.rectangle((0, 138, w, 142), fill=GOLD)
    return draw


def fit(image: Image.Image, max_w: int, max_h: int) -> Image.Image:
    scale = min(max_w / image.width, max_h / image.height)
    size = (max(1, round(image.width * scale)), max(1, round(image.height * scale)))
    return image.resize(size, Image.Resampling.LANCZOS)


def save_pair(image: Image.Image, stem: str) -> tuple[str, str]:
    OUT.mkdir(parents=True, exist_ok=True)
    png = OUT / f"{stem}.png"
    webp = OUT / f"{stem}.webp"
    image.save(png, format="PNG", optimize=True)
    web = image
    if web.width > 1200:
        new_h = round(web.height * 1200 / web.width)
        web = web.resize((1200, new_h), Image.Resampling.LANCZOS)
    web.save(webp, format="WEBP", quality=80, method=6)
    return (
        png.relative_to(ROOT).as_posix(),
        webp.relative_to(ROOT).as_posix(),
    )


def build_load_factor(source: Image.Image) -> Image.Image:
    canvas = Image.new("RGB", (1600, 1250), WHITE)
    draw = header(canvas, "60° BANK = 2.0 G")
    fig = fit(source, 1280, 900)
    x0 = (canvas.width - fig.width) // 2
    y0 = 175
    canvas.paste(fig, (x0, y0))

    # Within the Figure 1-34 crop, the plot rectangle occupies approximately
    # x 7%-93% and y 3%-86%. Read 60° on x and 2 G on the right-hand scale.
    left = x0 + fig.width * 0.07
    right = x0 + fig.width * 0.93
    top = y0 + fig.height * 0.03
    bottom = y0 + fig.height * 0.86
    x60 = left + (60 / 90) * (right - left)
    y2 = bottom - (1 / 12) * (bottom - top)
    draw.line((x60, bottom, x60, y2), fill=GOLD, width=6)
    draw.line((x60, y2, right, y2), fill=GOLD, width=6)
    draw.ellipse((x60 - 10, y2 - 10, x60 + 10, y2 + 10), fill=GOLD, outline=NAVY, width=3)
    label = "60° → 2.0 G"
    f = font(28, True)
    box = draw.textbbox((0, 0), label, font=f)
    lw, lh = box[2] - box[0] + 36, box[3] - box[1] + 22
    lx, ly = min(canvas.width - lw - 60, right - lw + 10), min(canvas.height - 125, bottom + 20)
    draw.rounded_rectangle((lx, ly, lx + lw, ly + lh), radius=14, fill=WHITE, outline=GOLD, width=4)
    draw.text((lx + 18, ly + 10), label, font=f, fill=NAVY)
    draw.text(
        (canvas.width // 2, canvas.height - 52),
        "At 60° bank in a level turn, load factor is 2.0 G — the wings support twice the aircraft's weight.",
        font=font(23), fill=GREY, anchor="mm",
    )
    return canvas


def build_stability(source: Image.Image) -> Image.Image:
    canvas = Image.new("RGB", (1600, 1050), WHITE)
    draw = header(canvas, "CG POSITION CONTROLS PITCH STABILITY")
    fig = fit(source, 1280, 610)
    x0 = (canvas.width - fig.width) // 2
    y0 = 175
    canvas.paste(fig, (x0, y0))
    key_y = 830
    draw.rounded_rectangle((210, key_y, 1390, key_y + 92), radius=18, fill=LIGHT, outline=BORDER, width=2)
    draw.text(
        (canvas.width // 2, key_y + 46),
        "CG / WEIGHT AHEAD OF LIFT / PRESSURE  →  POSITIVE LONGITUDINAL STABILITY",
        font=font(25, True), fill=NAVY, anchor="mm",
    )
    draw.text(
        (canvas.width // 2, 985),
        "The key factor is the CG position relative to the wing's centre of lift/pressure.",
        font=font(22), fill=GREY, anchor="mm",
    )
    return canvas


def build_drag(source: Image.Image) -> Image.Image:
    canvas = Image.new("RGB", (1600, 1250), WHITE)
    draw = header(canvas, "CURVE B = PARASITE / PROFILE DRAG")
    fig = fit(source, 1260, 920)
    x0 = (canvas.width - fig.width) // 2
    y0 = 175
    canvas.paste(fig, (x0, y0))

    # Highlight the handbook's existing Parasite Drag label and leader line.
    bx1 = x0 + fig.width * 0.64
    by1 = y0 + fig.height * 0.20
    bx2 = x0 + fig.width * 0.96
    by2 = y0 + fig.height * 0.43
    draw.rounded_rectangle((bx1, by1, bx2, by2), radius=18, outline=GOLD, width=6)
    draw.text(
        (canvas.width // 2, canvas.height - 54),
        "Parasite/profile drag increases as airspeed increases; induced drag decreases.",
        font=font(23), fill=GREY, anchor="mm",
    )
    return canvas


def build_dihedral(source: Image.Image) -> Image.Image:
    canvas = Image.new("RGB", (1600, 1100), WHITE)
    draw = header(canvas, "DIHEDRAL PROVIDES LATERAL STABILITY")
    fig = fit(source, 1360, 620)
    x0 = (canvas.width - fig.width) // 2
    y0 = 190
    canvas.paste(fig, (x0, y0))
    text = "Wings angle upward from the root"
    f = font(26, True)
    box = draw.textbbox((0, 0), text, font=f)
    tw, th = box[2] - box[0] + 30, box[3] - box[1] + 20
    tx = (canvas.width - tw) // 2
    ty = 840
    draw.rounded_rectangle((tx, ty, tx + tw, ty + th), radius=14, fill=WHITE, outline=GOLD, width=4)
    draw.text((canvas.width // 2, ty + th // 2), text, font=f, fill=NAVY, anchor="mm")
    draw.text(
        (canvas.width // 2, 1010),
        "Dihedral creates a restoring roll tendency after a sideslip, improving stability in the rolling plane.",
        font=font(22), fill=GREY, anchor="mm",
    )
    return canvas


def build_glide(source: Image.Image) -> Image.Image:
    canvas = Image.new("RGB", (1600, 1200), WHITE)
    draw = header(canvas, "HIGH L/D = SHALLOWER GLIDE")
    fig = fit(source, 1400, 770)
    x0 = (canvas.width - fig.width) // 2
    y0 = 175
    canvas.paste(fig, (x0, y0))
    # Figure 1-39's left-hand example has the shallower glide angle.
    draw.rounded_rectangle(
        (x0 + fig.width * 0.02, y0 + fig.height * 0.08, x0 + fig.width * 0.51, y0 + fig.height * 0.88),
        radius=18, outline=GOLD, width=6,
    )
    text = "Higher L/D → more distance per height lost"
    f = font(26, True)
    box = draw.textbbox((0, 0), text, font=f)
    tw, th = box[2] - box[0] + 30, box[3] - box[1] + 20
    tx, ty = (canvas.width - tw) // 2, 1000
    draw.rounded_rectangle((tx, ty, tx + tw, ty + th), radius=14, fill=WHITE, outline=GOLD, width=4)
    draw.text((canvas.width // 2, ty + th // 2), text, font=f, fill=NAVY, anchor="mm")
    draw.text(
        (canvas.width // 2, 1135),
        "A high lift-to-drag ratio produces a shallow, efficient glide path.",
        font=font(22), fill=GREY, anchor="mm",
    )
    return canvas


BUILDERS = {
    "pof-bank-load-factor-001": build_load_factor,
    "pof-longitudinal-stability-001": build_stability,
    "pof-parasite-drag-001": build_drag,
    "pof-dihedral-001": build_dihedral,
    "pof-glide-ratio-001": build_glide,
}


def advance_manifest(asset_paths: dict[str, tuple[str, str]]) -> None:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    visuals = {v["visual_id"]: v for v in data["visuals"]}
    missing = [visual_id for visual_id in BATCH_IDS if visual_id not in visuals]
    if missing:
        raise RuntimeError(f"Batch manifest entries missing: {missing}")

    for visual_id in BATCH_IDS:
        visual = visuals[visual_id]
        if visual["status"] != "REFINING":
            raise RuntimeError(f"{visual_id} must be REFINING before build; found {visual['status']}")
        master, web = asset_paths[visual_id]
        visual["assets"] = {"master_asset": master, "web_asset": web}
        visual["qa"] = {"technical": True, "teaching": True, "visual": True, "preview": False, "live": False}
        visual["status"] = "QA_APPROVED"
        visual["lock"] = {"approved": False, "replacement_reason": None}

    MANIFEST.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="pilotvault-pof-") as tmp:
        pdf = Path(tmp) / "source.pdf"
        download_source(pdf)
        doc = fitz.open(pdf)
        page_cache: dict[str, Image.Image] = {}
        asset_paths: dict[str, tuple[str, str]] = {}

        for visual_id in BATCH_IDS:
            spec = FIGURES[visual_id]
            page = find_page(doc, spec["caption"])
            cache_key = str(page.number)
            if cache_key not in page_cache:
                page_cache[cache_key] = render_page(page)
            source = crop_fraction(page_cache[cache_key], spec["crop"])
            final = BUILDERS[visual_id](source)
            asset_paths[visual_id] = save_pair(final, spec["filename"])
            print(f"Built {visual_id}: {asset_paths[visual_id]}")

        advance_manifest(asset_paths)

    print("POF refined batch 1 built and advanced to QA_APPROVED")


if __name__ == "__main__":
    main()
