# -*- coding: utf-8 -*-
"""Generate hero-bg.jpg: LED cabinets on dark bg with blue-purple light streaks."""
from __future__ import annotations

import random
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
CABINET = ROOT / "assets" / "product" / "cabinet"
OUT = ROOT / "assets" / "hero" / "hero-bg.jpg"

W, H = 1920, 1080
RNG = random.Random(20260603)

PRODUCTS = [
    "45G-010.jpg",
    "02-2.jpg",
    "panel-01.jpg",
    "01-1.jpg",
    "007-2.jpg",
    "45G-008.jpg",
    "cabinet-20.jpg",
    "scene-01.jpg",
]


def remove_light_bg(img: Image.Image, threshold: float = 235.0, soften: float = 18.0) -> Image.Image:
    rgba = img.convert("RGBA")
    arr = np.array(rgba, dtype=np.float32)
    r, g, b = arr[..., 0], arr[..., 1], arr[..., 2]
    min_rgb = np.minimum(np.minimum(r, g), b)
    alpha = np.clip((threshold - min_rgb) * (255.0 / soften), 0, 255)
    sat = np.maximum(np.maximum(r, g), b) - min_rgb
    near_white = (min_rgb > threshold - 30) & (sat < 40)
    alpha[near_white] = np.minimum(alpha[near_white], 25)
    arr[..., 3] = alpha
    out = Image.fromarray(arr.astype(np.uint8))
    if out.getbbox():
        out = out.crop(out.getbbox())
    return out


def make_base() -> Image.Image:
    arr = np.zeros((H, W, 3), dtype=np.float32)
    yy, xx = np.mgrid[0:H, 0:W]
    # deep blue-purple base gradient
    arr[..., 0] = 6 + (xx / W) * 18 + (yy / H) * 8
    arr[..., 1] = 4 + (xx / W) * 10
    arr[..., 2] = 22 + (xx / W) * 45 + (1 - yy / H) * 20
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))


def add_glow_layers(base: Image.Image) -> Image.Image:
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(glow)

    blobs = [
        ((180, H - 120), 520, (90, 60, 255, 110)),
        ((W // 2, H // 2), 680, (160, 80, 255, 85)),
        ((W - 280, 200), 420, (60, 140, 255, 75)),
        ((W * 0.65, H * 0.72), 380, (200, 50, 220, 70)),
    ]
    for center, radius, color in blobs:
        x0, y0 = center[0] - radius, center[1] - radius
        x1, y1 = center[0] + radius, center[1] + radius
        draw.ellipse([x0, y0, x1, y1], fill=color)

    glow = glow.filter(ImageFilter.GaussianBlur(55))
    streak = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(streak)
    # light streaks (blue-purple, like reference composition)
    streak_paths = [
        [(0, H), (W * 0.45, H * 0.55), (W * 0.85, H * 0.15)],
        [(W * 0.1, H * 0.9), (W * 0.55, H * 0.4), (W, H * 0.05)],
        [(0, H * 0.55), (W * 0.35, H * 0.35), (W * 0.7, 0)],
    ]
    colors = [
        (120, 90, 255, 140),
        (80, 160, 255, 120),
        (180, 70, 240, 100),
    ]
    for pts, col in zip(streak_paths, colors):
        for i in range(len(pts) - 1):
            sdraw.line([pts[i], pts[i + 1]], fill=col, width=RNG.randint(28, 42))
    streak = streak.filter(ImageFilter.GaussianBlur(28))

    out = base.convert("RGBA")
    out = Image.alpha_composite(out, glow)
    out = Image.alpha_composite(out, streak)
    return out.convert("RGB")


def paste_product(canvas: Image.Image, path: Path, cx: float, cy: float, scale: float, angle: float) -> None:
    prod = remove_light_bg(Image.open(path))
    target_w = int(W * scale)
    ratio = target_w / prod.width
    target_h = int(prod.height * ratio)
    prod = prod.resize((target_w, target_h), Image.Resampling.LANCZOS)
    prod = prod.rotate(angle, resample=Image.Resampling.BICUBIC, expand=True)
    x = int(cx - prod.width / 2)
    y = int(cy - prod.height / 2)
    canvas.paste(prod, (x, y), prod)


def add_vignette(img: Image.Image) -> Image.Image:
    arr = np.array(img, dtype=np.float32)
    yy, xx = np.mgrid[0:H, 0:W]
    cx, cy = W * 0.42, H * 0.55
    dist = np.sqrt(((xx - cx) / W) ** 2 + ((yy - cy) / H) ** 2)
    vignette = np.clip(1.0 - dist * 0.85, 0.35, 1.0)
    arr *= vignette[..., np.newaxis]
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    canvas = add_glow_layers(make_base()).convert("RGBA")

    placements = [
        (0.78, 0.38, 0.36, -14),
        (0.58, 0.52, 0.30, 11),
        (0.38, 0.42, 0.28, -8),
        (0.22, 0.58, 0.32, 16),
        (0.68, 0.68, 0.26, 6),
        (0.48, 0.22, 0.24, -22),
        (0.88, 0.55, 0.22, 18),
    ]
    files = [CABINET / name for name in PRODUCTS if (CABINET / name).exists()]
    RNG.shuffle(files)

    for i, (px, py, sc, ang) in enumerate(placements):
        if i >= len(files):
            break
        paste_product(canvas, files[i], W * px, H * py, sc, ang + RNG.uniform(-6, 6))

    # soft foreground blur accent (depth)
    accent = canvas.copy()
    accent = accent.filter(ImageFilter.GaussianBlur(6))
    canvas = Image.blend(canvas, accent, 0.12)

    result = add_vignette(canvas.convert("RGB"))
    result = result.filter(ImageFilter.UnsharpMask(radius=1.2, percent=80, threshold=3))
    result.save(OUT, "JPEG", quality=90, optimize=True)
    print("saved", OUT, result.size)


if __name__ == "__main__":
    main()
