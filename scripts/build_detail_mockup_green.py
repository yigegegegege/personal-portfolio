# -*- coding: utf-8 -*-
"""Build e-commerce detail mockup collage from green/ product renders."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[1]
GREEN = ROOT / "assets" / "product" / "ecom" / "green"
OUT_DETAIL = ROOT / "assets" / "product" / "ecom" / "detail" / "detail-mockup-long.png"
OUT_PREVIEW = ROOT / "assets" / "product" / "section-product-preview.png"

W, H = 2560, 1440
BG = (245, 246, 248)


def load_fit(path: Path, size: tuple[int, int], contain: bool = True) -> Image.Image:
    im = Image.open(path).convert("RGBA")
    im = remove_black(im)
    if contain:
        im.thumbnail(size, Image.Resampling.LANCZOS)
        canvas = Image.new("RGBA", size, (0, 0, 0, 0))
        ox = (size[0] - im.width) // 2
        oy = (size[1] - im.height) // 2
        canvas.paste(im, (ox, oy), im)
        return canvas
    return ImageOps.fit(im, size, Image.Resampling.LANCZOS)


def remove_black(im: Image.Image, t: int = 32) -> Image.Image:
    im = im.convert("RGBA")
    px = im.load()
    w, h = im.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if r <= t and g <= t and b <= t:
                px[x, y] = (0, 0, 0, 0)
    return im


def gradient(size: tuple[int, int], top: tuple[int, int, int], bottom: tuple[int, int, int]) -> Image.Image:
    w, h = size
    base = Image.new("RGB", size, top)
    draw = ImageDraw.Draw(base)
    for y in range(h):
        ratio = y / max(h - 1, 1)
        c = tuple(int(top[i] + (bottom[i] - top[i]) * ratio) for i in range(3))
        draw.line([(0, y), (w, y)], fill=c)
    return base


def paste_card(canvas: Image.Image, box: tuple[int, int, int, int], path: Path, bg: Image.Image | None = None) -> None:
    x0, y0, x1, y1 = box
    cw, ch = x1 - x0, y1 - y0
    layer = Image.new("RGBA", (cw, ch), (255, 255, 255, 255))
    if bg:
        bg_fit = ImageOps.fit(bg, (cw, ch), Image.Resampling.LANCZOS)
        layer = bg_fit.convert("RGBA")
    product = load_fit(path, (int(cw * 0.92), int(ch * 0.88)))
    px = (cw - product.width) // 2
    py = (ch - product.height) // 2
    layer.paste(product, (px, py), product)
    canvas.paste(layer, (x0, y0))


def draw_device(canvas: Image.Image) -> None:
    draw = ImageDraw.Draw(canvas)
    # laptop outer
    lx, ly, lw, lh = 120, 140, 1680, 980
    draw.rounded_rectangle([lx, ly, lx + lw, ly + lh], radius=28, fill=(30, 30, 30))
    draw.rounded_rectangle([lx + 14, ly + 14, lx + lw - 14, ly + lh - 70], radius=12, fill=(255, 255, 255))
    # phone
    px, py, pw, ph = 1880, 260, 420, 820
    draw.rounded_rectangle([px, py, px + pw, py + ph], radius=36, fill=(25, 25, 25))
    draw.rounded_rectangle([px + 12, py + 12, px + pw - 12, py + ph - 12], radius=28, fill=(255, 255, 255))


def try_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for name in ("msyh.ttc", "arial.ttf", "segoeui.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def main() -> None:
    slots = {
        "hero": GREEN / "01.jpg",
        "t1": GREEN / "023.jpg",
        "t2": GREEN / "030.jpg",
        "t3": GREEN / "32-1.jpg",
        "t4": GREEN / "40-1.jpg",
        "t5": GREEN / "13-2.jpg",
        "f1": GREEN / "42.jpg",
        "f2": GREEN / "41-1.jpg",
        "f3": GREEN / "01.jpg",
        "f4": GREEN / "023.jpg",
        "f5": GREEN / "030.jpg",
        "f6": GREEN / "40-1.jpg",
    }
    for k, p in slots.items():
        if not p.exists():
            raise SystemExit(f"missing {p}")

    canvas = Image.new("RGB", (W, H), BG)
    draw_device(canvas)

    # laptop inner screen
    sx, sy, sw, sh = 150, 170, 1620, 860
    screen = Image.new("RGB", (sw, sh), (255, 255, 255))

    outdoor = gradient((900, 520), (180, 210, 190), (90, 120, 100))
    night = gradient((520, 320), (20, 35, 55), (5, 10, 25))
    studio = gradient((520, 320), (240, 242, 245), (220, 224, 228))

    # thumbs
    for i, key in enumerate(["t1", "t2", "t3", "t4", "t5"]):
        paste_card(screen, (20, 20 + i * 158, 150, 20 + (i + 1) * 158 - 8), slots[key], studio)

    paste_card(screen, (170, 20, 920, 540), slots["hero"], outdoor)

    # product copy block (static)
    d = ImageDraw.Draw(screen)
    font_title = try_font(22)
    font_sub = try_font(16)
    d.text((950, 40), "Portable Camping Fan", fill=(20, 20, 20), font=font_title)
    d.text((950, 78), "20000mAh · LED Light · Tripod Stand", fill=(80, 80, 80), font=font_sub)
    d.text((950, 120), "$49.99", fill=(180, 20, 40), font=try_font(28))

    # feature row
    y0 = 560
    fw, fh = 250, 280
    gap = 12
    keys = ["f1", "f2", "f3", "f4", "f5", "f6"]
    labels = ["OUTDOORS", "LED RING", "AIRFLOW", "SIDE VIEW", "TRIPOD", "REAR IO"]
    bgs = [outdoor, night, studio, studio, studio, night]
    for i, (key, label, bg) in enumerate(zip(keys, labels, bgs)):
        x = 20 + i * (fw + gap)
        paste_card(screen, (x, y0, x + fw, y0 + fh), slots[key], bg)
        d.text((x + 12, y0 + fh - 28), label, fill=(30, 90, 60), font=font_sub)

    canvas.paste(screen, (sx, sy))

    # phone screen
    ps = Image.new("RGB", (380, 780), (255, 255, 255))
    paste_card(ps, (10, 20, 370, 360), slots["hero"], outdoor)
    paste_card(ps, (10, 380, 370, 560), slots["f6"], outdoor)
    d2 = ImageDraw.Draw(ps)
    d2.text((20, 580), "Portable Camping Fan", fill=(20, 20, 20), font=try_font(18))
    d2.text((20, 620), "$49.99", fill=(180, 20, 40), font=try_font(22))
    canvas.paste(ps, (1892, 282))

    title_font = try_font(36)
    ImageDraw.Draw(canvas).text((120, 40), "Amazon / 国际站 · 详情页视觉 mockup（橄榄绿款）", fill=(30, 30, 30), font=title_font)

    OUT_DETAIL.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(OUT_DETAIL, quality=92)
    preview = canvas.copy()
    preview.thumbnail((1280, 720), Image.Resampling.LANCZOS)
    preview.save(OUT_PREVIEW, quality=90)
    print("saved", OUT_DETAIL)
    print("saved", OUT_PREVIEW)


if __name__ == "__main__":
    main()
