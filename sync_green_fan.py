# -*- coding: utf-8 -*-
"""Replace ecom/green with user-provided green fan images only."""
from pathlib import Path
import shutil

from PIL import Image

ROOT = Path(__file__).resolve().parent
GREEN_DIR = ROOT / "assets" / "product" / "ecom" / "green"

SOURCES = [
    (
        r"C:\Users\62379\.cursor\projects\d-AI\assets\c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_023-25284115-7d81-4123-affc-8a09f5000e70.png",
        "023",
    ),
    (
        r"C:\Users\62379\.cursor\projects\d-AI\assets\c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_021-cff01526-02d3-46a1-9d4d-89a91f24c075.png",
        "021",
    ),
    (
        r"C:\Users\62379\.cursor\projects\d-AI\assets\c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_31-7db7f4d9-4317-4768-9ed6-e607deac09b5.png",
        "31",
    ),
    (
        r"C:\Users\62379\.cursor\projects\d-AI\assets\c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_030-fb1a2f1f-9da1-4857-806e-44a5e7173b3d.png",
        "030",
    ),
    (
        r"C:\Users\62379\.cursor\projects\d-AI\assets\c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_022-23bee539-da69-4c79-bb85-653b778ea882.png",
        "022",
    ),
    (
        r"C:\Users\62379\.cursor\projects\d-AI\assets\c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_40-1-83e06200-7a45-43ac-96b6-be5dc97b2c54.png",
        "40-1",
    ),
    (
        r"C:\Users\62379\.cursor\projects\d-AI\assets\c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_06-dea1baca-e1f8-4aee-9e05-7ef28fcac1c1.png",
        "06",
    ),
    (
        r"C:\Users\62379\.cursor\projects\d-AI\assets\c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_01-1dbef90e-2c86-47e2-8773-4962fda6a7fd.png",
        "01",
    ),
    (
        r"C:\Users\62379\.cursor\projects\d-AI\assets\c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_13-2-e9eac399-e05f-4a28-8c5b-6185231c677b.png",
        "13-2",
    ),
    (
        r"C:\Users\62379\.cursor\projects\d-AI\assets\c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_024-5ec926cb-cbe0-4c25-b428-1d552ae08057.png",
        "024",
    ),
    (
        r"C:\Users\62379\.cursor\projects\d-AI\assets\c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_001-2-7fb8df20-0e9f-40ee-8eba-65a5e358624e.png",
        "001-2",
    ),
    (
        r"C:\Users\62379\.cursor\projects\d-AI\assets\c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_14-2-b1cdd74b-d535-40a0-bcc5-6e8325f50396.png",
        "14-2",
    ),
    (
        r"C:\Users\62379\.cursor\projects\d-AI\assets\c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_38-1-45c1a110-0509-4818-80cc-917ef257aece.png",
        "38-1",
    ),
    (
        r"C:\Users\62379\.cursor\projects\d-AI\assets\c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_42-38706734-6602-485f-8362-436658d73904.png",
        "42",
    ),
    (
        r"C:\Users\62379\.cursor\projects\d-AI\assets\c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_32-1-797bafab-e794-49c5-a63c-0978781063ce.png",
        "32-1",
    ),
    (
        r"C:\Users\62379\.cursor\projects\d-AI\assets\c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_41-1-fec48645-a006-4819-9315-93556b9c5e39.png",
        "41-1",
    ),
]


def export(src: Path, dest: Path, max_w: int = 1400) -> None:
    im = Image.open(src)
    if im.mode in ("RGBA", "LA"):
        bg = Image.new("RGB", im.size, (8, 9, 12))
        bg.paste(im, mask=im.split()[-1])
        im = bg
    elif im.mode != "RGB":
        im = im.convert("RGB")
    w, h = im.size
    if w > max_w:
        h = int(h * max_w / w)
        im = im.resize((max_w, h), Image.Resampling.LANCZOS)
    im.save(dest, "JPEG", quality=88, optimize=True)


def sync_assets() -> None:
    if GREEN_DIR.exists():
        shutil.rmtree(GREEN_DIR)
    GREEN_DIR.mkdir(parents=True)
    for src_str, stem in SOURCES:
        src = Path(src_str)
        if not src.exists():
            raise FileNotFoundError(src)
        export(src, GREEN_DIR / f"{stem}.jpg")


if __name__ == "__main__":
    sync_assets()
    print(f"synced {len(SOURCES)} green fan images")
