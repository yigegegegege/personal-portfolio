# -*- coding: utf-8 -*-
"""Compose AIGC compare-scene using official 011-1 3D IP + layout reference."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets" / "aigc"
REFS = ASSETS / "refs"

CHAR_3D = Path(
    r"C:\Users\62379\.cursor\projects\d-AI\assets"
    r"\c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_011-1-f52d17ad-d260-421d-bc1d-02f708a2f0cb.png"
)
LAYOUT = Path(
    r"C:\Users\62379\.cursor\projects\d-AI\assets"
    r"\c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_image-c9b82f9f-9324-40d5-a5bc-11232c2190fa.png"
)
OUT = ASSETS / "compare-scene.png"


def remove_black_bg(im: Image.Image, thresh: int = 28) -> Image.Image:
    im = im.convert("RGBA")
    px = im.load()
    w, h = im.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if r <= thresh and g <= thresh and b <= thresh:
                px[x, y] = (0, 0, 0, 0)
    return im


def sketch_layer(im: Image.Image) -> Image.Image:
    """Blue pencil-sketch look for left panel."""
    gray = ImageOps.grayscale(im.convert("RGB"))
    edges = gray.filter(ImageFilter.FIND_EDGES)
    edges = ImageEnhance.Contrast(edges).enhance(2.2)
    base = ImageEnhance.Color(im.convert("RGB")).enhance(0.15)
    blue = Image.new("RGB", im.size, (30, 80, 160))
    mixed = ImageChops.multiply(base, blue)
    sketch = Image.blend(mixed, edges.convert("RGB"), 0.45)
    sketch = ImageEnhance.Brightness(sketch).enhance(1.05)
    return sketch.convert("RGBA")


def draw_label(draw: ImageDraw.ImageDraw, text: str, box: tuple[int, int, int, int]) -> None:
    try:
        font = ImageFont.truetype("msyh.ttc", 28)
    except OSError:
        font = ImageFont.load_default()
    draw.text((box[0] + 16, box[1] + 12), text, fill=(255, 238, 0, 255), font=font)


def main() -> None:
    layout = Image.open(LAYOUT).convert("RGBA")
    w, h = layout.size
    mid = w // 2

    char = remove_black_bg(Image.open(CHAR_3D))
    target_h = int(h * 0.58)
    scale = target_h / char.height
    char = char.resize((max(1, int(char.width * scale)), target_h), Image.Resampling.LANCZOS)

    right_bg = layout.crop((mid, 0, w, h))
    left_bg = layout.crop((0, 0, mid, h))

    # Slightly shift character left on each panel
    cx_right = mid + int((w - mid) * 0.08)
    cy = int(h * 0.22)
    cx_left = int(mid * 0.08)

    right = right_bg.copy()
    right.paste(char, (cx_right, cy), char)

    char_sk = sketch_layer(char)
    left = left_bg.copy()
    left.paste(char_sk, (cx_left, cy), char_sk)

    canvas = Image.new("RGBA", (w, h))
    canvas.paste(left, (0, 0))
    canvas.paste(right, (mid, 0))

    draw = ImageDraw.Draw(canvas)
    draw_label(draw, "AI 草图", (0, 0, mid, 56))
    draw_label(draw, "PS 终稿", (mid, 0, w, 56))

    # Center divider
    draw.line([(mid, 0), (mid, h)], fill=(255, 255, 255, 40), width=2)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(OUT, quality=92)
    print("saved", OUT)


if __name__ == "__main__":
    main()
