# -*- coding: utf-8 -*-
"""Optimize hero carousel + key poster/home assets (WebP + recompressed JPEG)."""
from __future__ import annotations

import json
import re
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
HERO = ROOT / "assets" / "hero"
INDEX = ROOT / "index.html"

# Curated hero sources (current hero-slide numbering after yanzhan import)
HERO_PICKS = [1, 2, 3, 4, 5, 6, 14, 20]

MAX_HERO_W = 1280
JPG_QUALITY = 82
WEBP_QUALITY = 82


def optimize_image(src: Path, *, max_w: int | None = None) -> tuple[Path, Path]:
    img = Image.open(src)
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    if max_w and img.width > max_w:
        h = int(img.height * max_w / img.width)
        img = img.resize((max_w, h), Image.Resampling.LANCZOS)

    jpg = src.with_suffix(".jpg")
    webp = src.with_suffix(".webp")
    img.save(jpg, "JPEG", quality=JPG_QUALITY, optimize=True, progressive=True)
    img.save(webp, "WEBP", quality=WEBP_QUALITY, method=6)
    return jpg, webp


def rebuild_hero() -> list[dict]:
    slides: list[dict] = []
    staging = HERO / "_staging"
    staging.mkdir(exist_ok=True)

    for i, src_num in enumerate(HERO_PICKS, 1):
        src = HERO / f"hero-slide-{src_num:02d}.jpg"
        if not src.exists():
            raise FileNotFoundError(src)
        staged = staging / f"slide-{i:02d}.jpg"
        if src.resolve() != staged.resolve():
            staged.write_bytes(src.read_bytes())

    for f in HERO.glob("hero-slide-*"):
        if f.suffix.lower() in {".jpg", ".jpeg", ".webp"}:
            f.unlink()

    for i in range(1, len(HERO_PICKS) + 1):
        staged = staging / f"slide-{i:02d}.jpg"
        dst_base = HERO / f"hero-slide-{i:02d}"
        optimize_image(staged, max_w=MAX_HERO_W)
        staged.with_suffix(".jpg").replace(dst_base.with_suffix(".jpg"))
        staged.with_suffix(".webp").replace(dst_base.with_suffix(".webp"))
        with Image.open(dst_base.with_suffix(".jpg")) as im:
            w, h = im.size
        slides.append({"index": i, "width": w, "height": h})
        print("hero", dst_base.name, f"{w}x{h}")

    for f in staging.iterdir():
        f.unlink()
    staging.rmdir()

    optimize_image(HERO / "hero-bg.jpg", max_w=MAX_HERO_W)
    print("hero-bg optimized")
    return slides


def compress_jpegs(folder: Path, *, max_w: int | None = None) -> None:
    for path in sorted(folder.rglob("*.jpg")):
        before = path.stat().st_size
        optimize_image(path, max_w=max_w)
        after = path.stat().st_size
        if before > after:
            print(f"jpg {path.relative_to(ROOT)} {before // 1024}KB -> {after // 1024}KB")


def compress_key_poster_assets() -> None:
    targets = [
        ROOT / "assets" / "poster" / "section-poster-preview.jpg",
    ]
    for path in targets:
        if path.exists():
            before = path.stat().st_size
            optimize_image(path, max_w=1280)
            webp = path.with_suffix(".webp")
            after = path.stat().st_size
            print(f"preview {path.name} {before // 1024}KB -> {after // 1024}KB (+ webp)")

    channels = ROOT / "assets" / "poster" / "yanzhan-channels"
    if channels.exists():
        compress_jpegs(channels, max_w=1920)

    action_kv = ROOT / "assets" / "poster" / "action-kv"
    if action_kv.exists():
        compress_jpegs(action_kv, max_w=1280)


def patch_index_carousel(slides: list[dict]) -> None:
    lines = ['      <div class="hero-carousel" data-interval="5000">']
    for slide in slides:
        i = slide["index"]
        active = " is-active" if i == 1 else ""
        attrs = 'decoding="async" fetchpriority="high"' if i == 1 else 'loading="lazy" decoding="async"'
        w, h = slide["width"], slide["height"]
        lines.extend([
            f'        <div class="hero-carousel__slide{active}">',
            "          <picture>",
            f'            <source srcset="assets/hero/hero-slide-{i:02d}.webp" type="image/webp" />',
            f'            <img src="assets/hero/hero-slide-{i:02d}.jpg" alt="" width="{w}" height="{h}" {attrs} />',
            "          </picture>",
            "        </div>",
        ])
    lines.append("      </div>")
    block = "\n".join(lines)

    text = INDEX.read_text(encoding="utf-8")
    text, n = re.subn(
        r'      <div class="hero-carousel" data-interval="5000">.*?</div>\n    </div>\n    <div class="hero-overlay"',
        block + '\n    </div>\n    <div class="hero-overlay"',
        text,
        count=1,
        flags=re.S,
    )
    if n != 1:
        raise SystemExit(f"carousel patch failed: {n}")
    INDEX.write_text(text, encoding="utf-8")
    print("patched index.html carousel:", len(slides), "slides")


def main() -> None:
    slides = rebuild_hero()
    compress_key_poster_assets()
    patch_index_carousel(slides)
    summary = {
        "hero_slides": len(slides),
        "hero_picks": HERO_PICKS,
        "max_hero_width": MAX_HERO_W,
    }
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
