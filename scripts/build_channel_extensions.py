# -*- coding: utf-8 -*-
"""Generate WeChat header + 9:16 vertical covers from featured action KVs."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
KV_DIR = ROOT / "assets" / "poster" / "action-kv"
OUT_DIR = KV_DIR / "channels"

WECHAT_SIZE = (900, 383)  # 公众号图文封面 2.35:1
VERTICAL_SIZE = (1080, 1920)  # 9:16 竖版内容封面

SETS = [
    ("01-ce01-ultra-bright-clear", "ULTRA BRIGHT · 超亮超清"),
    ("02-kv03-motion-every-pixel", "MOTION IN EVERY PIXEL · 高刷性能"),
    ("03-ce09-your-display-story", "YOUR DISPLAY YOUR STORY · 创意无界"),
    ("04-kv25-vertical-display", "POST YOUR VISION · 竖屏数字海报"),
]


def cover_crop(
    img: Image.Image,
    target_w: int,
    target_h: int,
    *,
    anchor_y: str = "center",
) -> Image.Image:
    sw, sh = img.size
    target_ratio = target_w / target_h
    src_ratio = sw / sh

    if src_ratio > target_ratio:
        crop_h = sh
        crop_w = int(sh * target_ratio)
        x0 = (sw - crop_w) // 2
        y0 = 0
    else:
        crop_w = sw
        crop_h = int(sw / target_ratio)
        x0 = 0
        if anchor_y == "bottom":
            y0 = sh - crop_h
        elif anchor_y == "top":
            y0 = 0
        else:
            y0 = (sh - crop_h) // 2

    cropped = img.crop((x0, y0, x0 + crop_w, y0 + crop_h))
    return cropped.resize((target_w, target_h), Image.Resampling.LANCZOS)


def darken(img: Image.Image, factor: float = 0.72) -> Image.Image:
    arr = np.array(img.convert("RGB"), dtype=np.float32)
    arr *= factor
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))


def make_wechat_header(img: Image.Image) -> Image.Image:
    # Bottom-weighted crop keeps KV headline band visible.
    return cover_crop(img, *WECHAT_SIZE, anchor_y="bottom")


def make_vertical_cover(img: Image.Image) -> Image.Image:
    tw, th = VERTICAL_SIZE
    bg = cover_crop(img, tw, th, anchor_y="center")
    bg = bg.filter(ImageFilter.GaussianBlur(32))
    bg = darken(bg, 0.55)

    fg_w = int(tw * 0.9)
    ratio = fg_w / img.width
    fg_h = int(img.height * ratio)
    fg = img.resize((fg_w, fg_h), Image.Resampling.LANCZOS)

    canvas = bg.convert("RGBA")
    x = (tw - fg_w) // 2
    y = int(th * 0.06)
    shadow = Image.new("RGBA", (fg_w + 40, fg_h + 40), (0, 0, 0, 0))
    shadow.paste((0, 0, 0, 90), [18, 22, fg_w + 22, fg_h + 26])
    shadow = shadow.filter(ImageFilter.GaussianBlur(16))
    canvas.paste(shadow, (x - 20, y - 10), shadow)
    canvas.paste(fg.convert("RGBA"), (x, y))

    # Soft vignette toward bottom for safe text zone
    arr = np.array(canvas.convert("RGB"), dtype=np.float32)
    yy = np.linspace(0, 1, th)[:, np.newaxis]
    vignette = np.clip(1.0 - yy * 0.35, 0.65, 1.0)
    arr *= vignette[..., np.newaxis]
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))


def save_jpg(img: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if img.mode != "RGB":
        img = img.convert("RGB")
    img.save(path, "JPEG", quality=92, optimize=True)


def main() -> None:
    manifest: list[dict] = []

    for slug, title in SETS:
        src = KV_DIR / f"{slug}.jpg"
        if not src.exists():
            raise FileNotFoundError(src)

        img = Image.open(src).convert("RGB")
        wechat = make_wechat_header(img)
        vertical = make_vertical_cover(img)

        wechat_path = OUT_DIR / f"{slug}-wechat-900x383.jpg"
        vert_path = OUT_DIR / f"{slug}-vertical-9x16.jpg"
        save_jpg(wechat, wechat_path)
        save_jpg(vertical, vert_path)

        item = {
            "slug": slug,
            "title": title,
            "master": f"action-kv/{slug}.jpg",
            "wechat": f"action-kv/channels/{wechat_path.name}",
            "vertical": f"action-kv/channels/{vert_path.name}",
            "wechat_size": "900×383",
            "vertical_size": "1080×1920",
        }
        manifest.append(item)
        print("ok", slug)

    (OUT_DIR / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
