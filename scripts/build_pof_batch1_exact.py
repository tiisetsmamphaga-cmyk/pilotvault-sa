from __future__ import annotations

import hashlib
import io
import sys
from pathlib import Path

import fitz
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps

EXPECTED_PDF_SHA256 = "89aca5abff3b3c14aca5d8865e8583994bff611bc0c4de94ec1c8a7ef7aaeed3"
EXPECTED_OUTPUT_SHA256 = {
    "pof-bank-load-factor-v1.webp": "deb7e9c6897b054bba317f51659fb6fc5c077829c509c3f793d3664b47388c0e",
    "pof-longitudinal-stability-v1.webp": "cfc95635e3c7a5da8d2210ca3311156c23af37c09e26ff9888239e05074a15cf",
    "pof-glide-ld-v1.webp": "5675024d01135fb090b868a84e17bbd6279890a593aa967d3d0365c714bf37da",
    "pof-drag-curves-v1.webp": "1716dfe6e1c28d2d7c6dd75a91f336e700eb67eee52a6969a41bfe73897870f2",
    "pof-dihedral-lateral-stability-v1.webp": "94341126148977941769e9f1c7f21e749cdd3b590b303aa13a50fd748f824aa9",
}

NAVY = "#06111f"
GOLD = "#f4b400"
TEXT = "#0b1726"
MUTED = "#5b6573"
LIGHT = "#f7f9fb"
WHITE = "#ffffff"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def F(size: int, bold: bool = False):
    try:
        return ImageFont.truetype(FONT_BOLD if bold else FONT, size)
    except OSError:
        return ImageFont.load_default()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def extract_embedded(pdf: fitz.Document, page_index: int, expected_size: tuple[int, int]):
    page = pdf[page_index]
    matches = []
    for info in page.get_images(full=True):
        xref = info[0]
        width, height = info[2], info[3]
        if (width, height) == expected_size:
            matches.append(xref)
    if len(matches) != 1:
        raise RuntimeError(
            f"Expected exactly one {expected_size} image on PDF page {page_index + 1}; found {len(matches)}"
        )
    data = pdf.extract_image(matches[0])["image"]
    return Image.open(io.BytesIO(data)).convert("RGB")


def enhance(image: Image.Image, target_width: int):
    scale = max(1, target_width / image.width)
    output = image.resize(
        (round(image.width * scale), round(image.height * scale)), Image.Resampling.LANCZOS
    )
    output = ImageOps.autocontrast(output, cutoff=0.15)
    output = ImageEnhance.Contrast(output).enhance(1.04)
    return output.filter(ImageFilter.UnsharpMask(radius=1.1, percent=135, threshold=3))


def header(canvas: Image.Image, draw: ImageDraw.ImageDraw, title: str):
    width, _ = canvas.size
    draw.rectangle((0, 0, width, 150), fill=NAVY)
    sub = "PILOTVAULT PRINCIPLES OF FLIGHT"
    sub_font = F(22, True)
    title_font = F(48, True)
    sub_box = draw.textbbox((0, 0), sub, font=sub_font)
    title_box = draw.textbbox((0, 0), title, font=title_font)
    draw.text(((width - (sub_box[2] - sub_box[0])) / 2, 26), sub, fill=GOLD, font=sub_font)
    draw.text(((width - (title_box[2] - title_box[0])) / 2, 61), title, fill=WHITE, font=title_font)
    draw.rectangle((0, 144, width, 150), fill=GOLD)


def paste_fit(canvas: Image.Image, image: Image.Image, box):
    x0, y0, x1, y1 = box
    resized = image.copy()
    resized.thumbnail((x1 - x0, y1 - y0), Image.Resampling.LANCZOS)
    x = x0 + ((x1 - x0) - resized.width) // 2
    y = y0 + ((y1 - y0) - resized.height) // 2
    canvas.paste(resized, (x, y))
    return x, y, resized.width, resized.height


def label(draw, x, y, text, font_size=28, fill="#fffaf0"):
    text_font = F(font_size, True)
    padding = 16
    box = draw.multiline_textbbox((0, 0), text, font=text_font, spacing=6)
    width = box[2] - box[0] + 2 * padding
    height = box[3] - box[1] + 2 * padding
    draw.rounded_rectangle((x, y, x + width, y + height), radius=18, fill=fill, outline=GOLD, width=4)
    draw.multiline_text((x + padding, y + padding - 2), text, font=text_font, fill=TEXT, spacing=6)


def save(canvas: Image.Image, output: Path, name: str, quality=88):
    output.mkdir(parents=True, exist_ok=True)
    path = output / name
    canvas.save(path, "WEBP", quality=quality, method=6)
    actual = sha256(path)
    expected = EXPECTED_OUTPUT_SHA256[name]
    if actual != expected:
        raise RuntimeError(f"{name}: deterministic output hash mismatch: {actual} != {expected}")
    print(f"VERIFIED {name}: {path.stat().st_size} bytes, sha256={actual}")


def build(pdf_path: Path, output: Path):
    if sha256(pdf_path) != EXPECTED_PDF_SHA256:
        raise RuntimeError("Handbook SHA-256 mismatch; refusing to generate visuals from an unverified source")

    pdf = fitz.open(pdf_path)

    bank = enhance(extract_embedded(pdf, 26, (472, 327)), 1500)
    c = Image.new("RGB", (1800, 1280), WHITE)
    d = ImageDraw.Draw(c)
    header(c, d, "BANK ANGLE, LOAD FACTOR & STALL SPEED")
    x, y, w, h = paste_fit(c, bank, (110, 205, 1690, 1060))
    label(d, 105, 190, "BANK ↑  →  LOAD FACTOR ↑", 30)
    label(d, 1210, 190, "60° BANK  =  2.0 G", 30)
    sx, sy = w / 472, h / 327
    x60 = x + int((62 + (427 - 62) * 60 / 90) * sx)
    y2 = y + int(261 * sy)
    ybase = y + int(284 * sy)
    d.line((x60, ybase, x60, y2), fill=GOLD, width=6)
    d.line((x60, y2, x + int(427 * sx), y2), fill=GOLD, width=6)
    d.ellipse((x60 - 14, y2 - 14, x60 + 14, y2 + 14), fill=GOLD, outline=NAVY, width=3)
    d.rounded_rectangle((180, 1120, 1620, 1230), radius=22, fill=LIGHT, outline="#d6dde6", width=3)
    message = "STALL SPEED rises with √load factor — increasing bank in a level turn raises both G-load and stall speed."
    message_font = F(26, True)
    message_width = d.textbbox((0, 0), message, font=message_font)[2]
    d.text(((1800 - message_width) / 2, 1157), message, fill=TEXT, font=message_font)
    save(c, output, "pof-bank-load-factor-v1.webp", 85)

    s1 = enhance(extract_embedded(pdf, 18, (202, 103)), 760)
    s2 = enhance(extract_embedded(pdf, 18, (203, 114)), 760)
    s3 = enhance(extract_embedded(pdf, 18, (248, 100)), 820)
    c = Image.new("RGB", (1800, 1280), WHITE)
    d = ImageDraw.Draw(c)
    header(c, d, "LONGITUDINAL STABILITY & CG POSITION")
    panels = [
        (90, 205, 570, 790, s1, "NEUTRAL", "Lift acts through CG\n→ no restoring pitch moment"),
        (660, 205, 1140, 790, s2, "UNSTABLE / AFT CG", "Lift acts ahead of CG\n→ pitch-up tendency increases"),
        (1230, 205, 1710, 790, s3, "POSITIVE STABILITY", "CG ahead of lift\n+ tail downforce restores pitch"),
    ]
    for x0, y0, x1, y1, image, title, body in panels:
        d.rounded_rectangle((x0, y0, x1, y1), radius=20, fill=WHITE, outline="#d8dee8", width=3)
        paste_fit(c, image, (x0 + 25, y0 + 35, x1 - 25, y0 + 330))
        d.text((x0 + 22, y0 + 355), title, font=F(27, True), fill=GOLD if "POSITIVE" in title else NAVY)
        d.multiline_text((x0 + 22, y0 + 410), body, font=F(22), fill=TEXT, spacing=8)
    d.rounded_rectangle((170, 860, 1630, 1120), radius=24, fill=LIGHT, outline="#d6dde6", width=3)
    d.text((215, 900), "KEY IDEA", font=F(28, True), fill=NAVY)
    d.multiline_text(
        (215, 950),
        "Moving the CG aft reduces longitudinal stability.\nA forward CG requires more tail/elevator force to pitch the nose up.",
        font=F(27),
        fill=TEXT,
        spacing=14,
    )
    save(c, output, "pof-longitudinal-stability-v1.webp", 88)

    glide = enhance(extract_embedded(pdf, 31, (458, 224)), 1500)
    c = Image.new("RGB", (1800, 1180), WHITE)
    d = ImageDraw.Draw(c)
    header(c, d, "LIFT-TO-DRAG RATIO & GLIDE ANGLE")
    paste_fit(c, glide, (80, 205, 1720, 900))
    label(d, 120, 200, "HIGHER L/D\n→ SHALLOWER GLIDE", 27)
    label(d, 1240, 200, "MORE DRAG / LOWER L/D\n→ STEEPER GLIDE", 27)
    d.rounded_rectangle((180, 930, 1620, 1090), radius=22, fill=LIGHT, outline="#d6dde6", width=3)
    line1 = "The resultant of LIFT + DRAG balances WEIGHT in a steady glide."
    line2 = "Extending flaps adds drag, reduces L/D and shortens the glide."
    line1_font, line2_font = F(27, True), F(25)
    line1_width = d.textbbox((0, 0), line1, font=line1_font)[2]
    line2_width = d.textbbox((0, 0), line2, font=line2_font)[2]
    d.text(((1800 - line1_width) / 2, 965), line1, fill=TEXT, font=line1_font)
    d.text(((1800 - line2_width) / 2, 1017), line2, fill=MUTED, font=line2_font)
    save(c, output, "pof-glide-ld-v1.webp", 88)

    drag = enhance(extract_embedded(pdf, 8, (303, 246)), 1320)
    c = Image.new("RGB", (1800, 1260), WHITE)
    d = ImageDraw.Draw(c)
    header(c, d, "INDUCED, PARASITE & TOTAL DRAG")
    x, y, w, h = paste_fit(c, drag, (250, 205, 1550, 1040))
    label(d, 110, 190, "LOW SPEED\nINDUCED DRAG HIGH", 27)
    label(d, 1280, 190, "HIGH SPEED\nPARASITE DRAG HIGH", 27)
    px = x + int(95 * w / 303)
    py = y + int(141 * h / 246)
    d.ellipse((px - 18, py - 18, px + 18, py + 18), fill=GOLD, outline=NAVY, width=4)
    label(d, px + 35, py - 35, "MINIMUM TOTAL DRAG\n= VMD = MAX L/D", 24, WHITE)
    d.rounded_rectangle((250, 1080, 1550, 1190), radius=20, fill=LIGHT, outline="#d6dde6", width=3)
    message = "Total drag is lowest at VMD, the same speed at which maximum lift-to-drag ratio occurs."
    message_font = F(25, True)
    message_width = d.textbbox((0, 0), message, font=message_font)[2]
    d.text(((1800 - message_width) / 2, 1117), message, fill=TEXT, font=message_font)
    save(c, output, "pof-drag-curves-v1.webp", 88)

    dihedral = enhance(extract_embedded(pdf, 20, (320, 98)), 1450)
    c = Image.new("RGB", (1800, 1100), WHITE)
    d = ImageDraw.Draw(c)
    header(c, d, "DIHEDRAL & LATERAL STABILITY")
    paste_fit(c, dihedral, (120, 215, 1680, 690))
    label(d, 100, 200, "DIHEDRAL\n= UPWARD WING ANGLE", 27)
    label(d, 1210, 200, "IMPROVES\nLATERAL (ROLL) STABILITY", 27)
    d.rounded_rectangle((150, 745, 1650, 1005), radius=24, fill=LIGHT, outline="#d6dde6", width=3)
    d.text((205, 785), "AFTER A ROLL DISTURBANCE:", font=F(27, True), fill=NAVY)
    lines = [
        "1. The aircraft sideslips.",
        "2. Dihedral gives the lower wing a greater effective angle of attack and more lift.",
        "3. The lift difference creates a restoring roll toward wings-level.",
    ]
    y_pos = 835
    for line in lines:
        d.text((225, y_pos), line, font=F(24), fill=TEXT)
        y_pos += 44
    save(c, output, "pof-dihedral-lateral-stability-v1.webp", 88)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("usage: build_pof_batch1_exact.py INPUT_PDF OUTPUT_DIR")
    build(Path(sys.argv[1]), Path(sys.argv[2]))
