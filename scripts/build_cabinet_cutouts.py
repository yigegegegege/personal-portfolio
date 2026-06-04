# -*- coding: utf-8 -*-
"""Build LED cabinet showcase cutouts: white bg -> #F7F7F8, preserve product pixels."""
from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image

ASSETS = Path(r"C:\Users\62379\.cursor\projects\d-AI\assets")
OUT_DIR = Path(__file__).resolve().parent.parent / "assets" / "product" / "cabinet"
BG = (247, 247, 248)
MAX_W = 1400

SOURCES = [
    ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_____-f7d2f6e9-e69d-4828-a44f-b9cbdee59b4a.png",
    ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_____2-26e4504f-5cd2-401c-b509-056cc0e34696.png",
    ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_____3-7176175d-c95c-4c8a-909d-186c1c828cf7.png",
    ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_____4-25bd61fe-2bc7-4df0-9c13-1b446f19b6b1.png",
    ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_____5-d79dc18e-adcc-42ef-b272-c85ee85dd965.png",
    ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_____6-50b6b9f6-c3da-4046-8131-397c2cd886c8.png",
    ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_____7-c0c133a5-f2dc-4f86-a0cc-abcab8817674.png",
    ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_____8-2c1c201c-0c41-441b-bfbb-02a436bcfce9.png",
    ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_____9-8714b5b3-09c6-45f5-a0e5-55b84a06505b.png",
]


def replace_white_bg(img: Image.Image, bg: tuple[int, int, int] = BG) -> Image.Image:
    rgb = img.convert("RGB")
    arr = np.array(rgb, dtype=np.float32)
    r, g, b = arr[..., 0], arr[..., 1], arr[..., 2]
    min_rgb = np.minimum(np.minimum(r, g), b)
    max_rgb = np.maximum(np.maximum(r, g), b)
    sat = max_rgb - min_rgb

    # Soft matte: only swap near-white, low-saturation pixels (keeps product edges).
    bg_weight = np.clip((min_rgb - 218) / 32, 0, 1) * np.clip(1 - sat / 42, 0, 1)
    bg_weight[(min_rgb > 238) & (sat < 28)] = 1.0

    target = np.array(bg, dtype=np.float32)
    out = arr * (1 - bg_weight[..., None]) + target * bg_weight[..., None]
    return Image.fromarray(out.astype(np.uint8), "RGB")


def export(src: Path, dest: Path) -> None:
    im = Image.open(src)
    im = replace_white_bg(im)
    w, h = im.size
    if w > MAX_W:
        h = int(h * MAX_W / w)
        im = im.resize((MAX_W, h), Image.Resampling.LANCZOS)
    dest.parent.mkdir(parents=True, exist_ok=True)
    im.save(dest, "PNG", optimize=True)


def main() -> None:
    for i, src in enumerate(SOURCES, start=1):
        if not src.exists():
            raise FileNotFoundError(src)
        dest = OUT_DIR / f"cutout-{i:02d}.png"
        export(src, dest)
        print(dest.name, dest.stat().st_size)


if __name__ == "__main__":
    main()
