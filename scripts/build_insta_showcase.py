# -*- coding: utf-8 -*-
"""Insta360-style product showcase backgrounds for 11 LED cabinet assets."""
from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ASSETS = Path(r"C:\Users\62379\.cursor\projects\d-AI\assets")
OUT_DIR = Path(r"d:\AI\个人作品网页\sucai")
CANVAS = (1920, 1080)

MODE_OVERRIDE = {
    "04-white-showroom": "black",
    "06-xr-stage": "scene",
    "03-lineup-snow": "scene",
    "10-vertical-posters": "black",
    "11-square-array": "black",
}

SOURCES = [
    ("01-pedestal-modules.png", "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_001-01-1cd44f13-d59d-4682-b1de-3c8101340537.png"),
    ("02-pedestal-showcase.png", "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_003-01-e1f2b5fd-5de8-4ed0-a656-979adbdaffa1.png"),
    ("03-lineup-snow.png", "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_04-1-f079bd20-3199-4a4b-8bd3-e9909a54db81.png"),
    ("04-white-showroom.png", "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_004-01-716fd6dc-bf05-4b1c-8576-3590057bdc34.png"),
    ("05-four-panels.png", "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images____-1-0176c450-8ef9-45b5-a56f-6da0dbe90759.png"),
    ("06-xr-stage.png", "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_0acadbeac64f0c4a255c33cb05c1f34-47f795ce-f808-457d-85c7-23e8d604e53b.png"),
    ("07-dynamic-cluster.png", "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images______20230714181213-37d0a524-2c9f-47b2-93a3-d12414baaca9.png"),
    ("08-mountain-lineup.png", "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_03-2-9c9cde89-ecda-4704-9af0-9c1a0c1244a4.png"),
    ("09-five-panels.png", "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images___2-90bbed51-d12c-462a-a760-dea73c7d429e.png"),
    ("10-vertical-posters.png", "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_01-2-baa3975e-4713-4dd0-b38e-147034ad6bee.png"),
    ("11-square-array.png", "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_02-2-3623582b-7ede-429f-b6cd-8949a0447d4f.png"),
]


def corner_brightness(img: Image.Image) -> float:
    rgb = img.convert("RGB")
    w, h = rgb.size
    pts = [(4, 4), (w - 5, 4), (4, h - 5), (w - 5, h - 5)]
    vals = [sum(rgb.getpixel(p)) / 3 for p in pts]
    return sum(vals) / len(vals)


def detect_bg_mode(img: Image.Image) -> str:
    b = corner_brightness(img)
    if b > 210:
        return "white"
    if b < 45:
        return "black"
    return "scene"


def make_insta_background(w: int, h: int) -> Image.Image:
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    cx, cy = w * 0.5, h * 0.32
    dist = np.sqrt(((xx - cx) / w) ** 2 + ((yy - cy) / h) ** 2)
    base = 252 - dist * 42
    arr = np.stack(
        [
            np.clip(base * 0.99, 236, 255),
            np.clip(base * 0.99, 236, 255),
            np.clip(base * 1.01 + 4, 240, 255),
        ],
        axis=-1,
    ).astype(np.uint8)
    return Image.fromarray(arr, "RGB")


def alpha_from_bg(img: Image.Image, mode: str) -> Image.Image:
    rgba = img.convert("RGBA")
    arr = np.array(rgba, dtype=np.float32)
    r, g, b = arr[..., 0], arr[..., 1], arr[..., 2]

    if mode == "white":
        min_rgb = np.minimum(np.minimum(r, g), b)
        alpha = np.clip((245 - min_rgb) * (255 / 22), 0, 255)
        sat = np.maximum(np.maximum(r, g), b) - min_rgb
        alpha[(min_rgb > 228) & (sat < 35)] = np.minimum(alpha[(min_rgb > 228) & (sat < 35)], 20)
    elif mode == "black":
        max_rgb = np.maximum(np.maximum(r, g), b)
        alpha = np.clip((max_rgb - 18) * (255 / 28), 0, 255)
        # keep screen glow
        alpha[(r > 40) | (g > 40) | (b > 40)] = np.maximum(alpha[(r > 40) | (g > 40) | (b > 40)], alpha[(r > 40) | (g > 40) | (b > 40)])
    else:
        # scene: soft matte only at extreme corners
        min_rgb = np.minimum(np.minimum(r, g), b)
        edge = min_rgb.copy()
        alpha = np.full_like(min_rgb, 255.0)
        alpha[min_rgb > 248] = np.clip((min_rgb[min_rgb > 248] - 248) * -12 + 255, 80, 255)

    arr[..., 3] = alpha
    out = Image.fromarray(arr.astype(np.uint8))
    if out.getbbox():
        out = out.crop(out.getbbox())
    return out


def add_ground_shadow(canvas: Image.Image, box: tuple[int, int, int, int]) -> None:
    x0, y0, x1, y1 = box
    sw, sh = x1 - x0, max(24, (y1 - y0) // 10)
    shadow = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    draw = ImageDraw.Draw(shadow)
    draw.ellipse([0, 0, sw, sh], fill=(0, 0, 0, 55))
    shadow = shadow.filter(ImageFilter.GaussianBlur(18))
    canvas.paste(
        shadow,
        (x0 + sw // 8, y1 - sh // 3),
        shadow,
    )


def fit_on_canvas(subject: Image.Image, canvas_size: tuple[int, int], margin: float = 0.08) -> Image.Image:
    cw, ch = canvas_size
    bg = make_insta_background(cw, ch).convert("RGBA")
    max_w = int(cw * (1 - margin * 2))
    max_h = int(ch * (1 - margin * 2))
    ratio = min(max_w / subject.width, max_h / subject.height)
    nw, nh = int(subject.width * ratio), int(subject.height * ratio)
    subject = subject.resize((nw, nh), Image.Resampling.LANCZOS)
    x = (cw - nw) // 2
    y = (ch - nh) // 2 + int(ch * 0.02)
    add_ground_shadow(bg, (x, y, x + nw, y + nh))
    bg.paste(subject, (x, y), subject)
    return bg.convert("RGB")


def process_one(src: Path, dst: Path, mode: str) -> None:
    img = Image.open(src)
    if mode == "scene":
        # full-frame card on Insta background — preserves complex scenes
        cw, ch = CANVAS
        bg = make_insta_background(cw, ch).convert("RGBA")
        ratio = min((cw * 0.92) / img.width, (ch * 0.88) / img.height)
        nw, nh = int(img.width * ratio), int(img.height * ratio)
        framed = img.convert("RGBA").resize((nw, nh), Image.Resampling.LANCZOS)
        x, y = (cw - nw) // 2, (ch - nh) // 2
        card = Image.new("RGBA", (nw + 48, nh + 48), (0, 0, 0, 0))
        mask = Image.new("L", (nw + 48, nh + 48), 0)
        ImageDraw.Draw(mask).rounded_rectangle(
            [0, 0, nw + 47, nh + 47], radius=28, fill=255
        )
        shadow = Image.new("RGBA", (nw + 48, nh + 48), (0, 0, 0, 0))
        ImageDraw.Draw(shadow).rounded_rectangle(
            [8, 12, nw + 39, nh + 43], radius=28, fill=(0, 0, 0, 70)
        )
        shadow = shadow.filter(ImageFilter.GaussianBlur(14))
        bg.paste(shadow, (x - 24 + 6, y - 24 + 10), shadow)
        white_card = Image.new("RGBA", (nw, nh), (255, 255, 255, 255))
        white_card = Image.composite(framed, white_card, framed.split()[3])
        card.paste(white_card, (24, 24))
        card.putalpha(mask)
        bg.paste(card, (x - 24, y - 24), card)
        result = bg.convert("RGB")
    else:
        subject = alpha_from_bg(img, mode)
        result = fit_on_canvas(subject, CANVAS)

    result = result.filter(ImageFilter.UnsharpMask(radius=0.8, percent=60, threshold=2))
    dst.parent.mkdir(parents=True, exist_ok=True)
    result.save(dst, "JPEG", quality=92, optimize=True)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    manifest = []
    for out_name, src_name in SOURCES:
        src = ASSETS / src_name
        dst = OUT_DIR / out_name.replace(".png", ".jpg")
        if not src.exists():
            raise FileNotFoundError(src)
        mode = MODE_OVERRIDE.get(Path(out_name).stem, detect_bg_mode(Image.open(src)))
        process_one(src, dst, mode)
        manifest.append(f"{dst.name}\t{mode}\t{src_name}")
        print("ok", dst.name, mode)

    (OUT_DIR / "insta-showcase-manifest.txt").write_text(
        "Insta360-style product showcase (1920x1080)\n\n" + "\n".join(manifest),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
