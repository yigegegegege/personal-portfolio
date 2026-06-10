# -*- coding: utf-8 -*-
"""Copy action-sports product KV assets into portfolio poster/action-kv."""
from __future__ import annotations

import json
import shutil
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = Path(r"C:\Users\62379\.cursor\projects\d-AI\assets")
OUT_DIR = ROOT / "assets" / "poster" / "action-kv"
HERO_DIR = ROOT / "assets" / "hero"

# Source filename key -> (slug, caption zh, caption en, featured, hero_order).
# Keys are matched against Cursor asset filenames; visual content verified against on-image copy.
ENTRIES: list[tuple[str, str, str, str, bool, int | None]] = [
    ("KV28____________", "01-ce01-ultra-bright-clear", "ULTRA BRIGHT · 超亮超清", "ULTRA BRIGHT · ULTRA CLEAR", True, 1),
    ("KV26____________", "02-kv03-motion-every-pixel", "MOTION IN EVERY PIXEL · 高刷性能", "MOTION IN EVERY PIXEL · High Refresh", True, 2),
    ("CE10____________", "03-ce09-your-display-story", "YOUR DISPLAY YOUR STORY · 创意无界", "YOUR DISPLAY · YOUR STORY", True, 3),
    ("CE03____________", "04-kv25-vertical-display", "POST YOUR VISION · 竖屏数字海报", "POST YOUR VISION · Vertical Display", True, 4),
    ("CE04____________", "05-ce03-bright-as-daylight", "BRIGHT AS DAYLIGHT · 超高亮度", "BRIGHT AS DAYLIGHT · Ultra-High Brightness", False, None),
    ("KV09____________", "06-kv11-mountain-bike", "山地骑行 · 泥泞越野", "Mountain Bike · Mud Action", False, None),
    ("KV11___________", "07-kv14-kayak-rapids", "皮划艇 · 激流勇进", "Kayak · Whitewater Rapids", False, None),
    ("CE07____________", "08-ce04-cool-under-pressure", "COOL UNDER PRESSURE · 散热设计", "COOL UNDER PRESSURE · Thermal Design", False, None),
    ("KV03____________", "09-kv09-waterproof-splash", "防水溅射 · 户外防护", "Waterproof · Splash Resistance", False, None),
    ("CE02____________", "10-ce02-engineered-endure", "ENGINEERED TO ENDURE · 户外耐用", "ENGINEERED TO ENDURE · Outdoor Hardware", False, None),
    ("CE09____________", "11-kv01-rugged-reliability", "RUGGED RELIABILITY · 户外箱体", "RUGGED RELIABILITY · Outdoor Cabinet", False, None),
    ("KV01____LED_____", "12-ce07-rugged-climbing", "RUGGED RELIABILITY · 攀岩场景", "RUGGED RELIABILITY · Rock Climbing", False, None),
    ("KV25____________", "13-kv16-think-bold", "THINK BOLD · 户外大屏", "THINK BOLD · Outdoor Display", False, None),
    ("CE01____________", "14-kv19-seamless-clarity", "SEAMLESS OUTDOOR CLARITY · 模组清晰", "SEAMLESS OUTDOOR CLARITY · Modular LED", False, None),
    ("KV20______COB___", "15-kv20-flip-chip-cob", "FLIP CHIP COB · 高端显示", "FLIP CHIP COB · Fine Pitch Display", False, None),
    ("KV14____________", "16-kv26-night-city-action", "都市夜景 · 动感跳跃", "Night City · Dynamic Action", False, None),
    ("KV05___________", "17-kv28-snowboard-sunset", "滑雪场景 · 日落高光", "Snowboard · Golden Hour Action", False, None),
    ("KV16____________", "18-kv05-mountain-hero", "雪山峰顶 · 产品特写", "Mountain Peaks · Product Hero", False, None),
    ("KV19____________", "19-ce10-alpine-product", "高山日出 · 工业质感", "Alpine Sunrise · Pro Hardware", False, None),
]


def find_src(key: str) -> Path:
    """Match e.g. KV03 or CE01 inside the Cursor asset filename."""
    matches = [
        p
        for p in sorted(SRC_DIR.glob("*20260608*.png"))
        if f"images_{key}" in p.name or f"images_{key}_" in p.name
    ]
    if not matches:
        raise FileNotFoundError(f"Missing source for key: {key}")
    return matches[0]


def save_jpg(src: Path, dst: Path) -> None:
    img = Image.open(src)
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    dst.parent.mkdir(parents=True, exist_ok=True)
    img.save(dst, "JPEG", quality=92, optimize=True)


def main() -> None:
    manifest: list[dict] = []
    hero_jobs: list[tuple[int, Path]] = []

    for key, slug, cap_zh, cap_en, featured, hero_order in ENTRIES:
        src = find_src(key)
        dst = OUT_DIR / f"{slug}.jpg"
        save_jpg(src, dst)
        item = {
            "file": f"action-kv/{slug}.jpg",
            "caption_zh": cap_zh,
            "caption_en": cap_en,
            "featured": featured,
        }
        manifest.append(item)
        if hero_order:
            hero_jobs.append((hero_order, dst))
        print("ok", dst.name)

    (OUT_DIR / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    HERO_DIR.mkdir(parents=True, exist_ok=True)
    for order, src in sorted(hero_jobs, key=lambda x: x[0]):
        hero_dst = HERO_DIR / f"hero-slide-{order:02d}.jpg"
        shutil.copy2(src, hero_dst)
        print("hero", hero_dst.name)

    preview = ROOT / "assets" / "poster" / "section-poster-preview.jpg"
    shutil.copy2(OUT_DIR / "01-ce01-ultra-bright-clear.jpg", preview)
    print("preview", preview)


if __name__ == "__main__":
    main()
