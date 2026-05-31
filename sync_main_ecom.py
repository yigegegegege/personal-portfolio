# -*- coding: utf-8 -*-
"""Replace ecom/main with user-provided product main images only."""
from pathlib import Path
import shutil

from PIL import Image

MAIN_DIR = Path(__file__).resolve().parent / "assets" / "product" / "ecom" / "main"

SOURCES = [
    (
        r"C:\Users\62379\.cursor\projects\d-AI\assets\c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_A__960x600_1-06ca023b-8ee9-4bf9-8b9a-33bee080f1ac.png",
        "a-960x600-01",
    ),
    (
        r"C:\Users\62379\.cursor\projects\d-AI\assets\c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_A_1_960x600_-f08dcc40-3f8b-4076-98c1-e183612e7db5.png",
        "a-plus-1-960x600",
    ),
    (
        r"C:\Users\62379\.cursor\projects\d-AI\assets\c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_A__960x600_2-8ec37f88-5234-4abe-9e0b-e5b8936d7c09.png",
        "a-960x600-02",
    ),
    (
        r"C:\Users\62379\.cursor\projects\d-AI\assets\c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_A__960x600_3-2e4d377d-0939-46f7-9ab0-99cf96d8c0be.png",
        "a-960x600-03",
    ),
    (
        r"C:\Users\62379\.cursor\projects\d-AI\assets\c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_A__960x600_4-555fa86e-3bbd-45b4-8cad-38c3b1861b98.png",
        "a-960x600-04",
    ),
    (
        r"C:\Users\62379\.cursor\projects\d-AI\assets\c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_A_3_960x600_-1b73b5a7-873a-4726-a4fe-69597d3485b4.png",
        "a-plus-3-960x600",
    ),
    (
        r"C:\Users\62379\.cursor\projects\d-AI\assets\c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_A_2_960x600_-4e8ca99a-edd3-464a-b6f6-5548f08c6c29.png",
        "a-plus-2-960x600",
    ),
    (
        r"C:\Users\62379\.cursor\projects\d-AI\assets\c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_A_4_960x600_-17e3dd93-b45b-4222-ba85-8dbe7f2d02d5.png",
        "a-plus-4-960x600",
    ),
    (
        r"C:\Users\62379\.cursor\projects\d-AI\assets\c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_A_5_960x600_-58a0da11-bd5c-4d18-a4de-f3672a3ea7ab.png",
        "a-plus-5-960x600",
    ),
    (
        r"C:\Users\62379\.cursor\projects\d-AI\assets\c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_A_6_960x600_-d92fbf0e-3b27-4478-9638-584fc5ab606f.png",
        "a-plus-6-960x600",
    ),
    (
        r"C:\Users\62379\.cursor\projects\d-AI\assets\c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images___02-1-b2cf4f5d-9d60-4df0-89cc-c3d9a6c6017f.png",
        "\u4e3b\u56fe02-1",
    ),
    (
        r"C:\Users\62379\.cursor\projects\d-AI\assets\c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images___01-1-faf8ba9c-fd47-40f9-b010-9d367b24342b.png",
        "\u4e3b\u56fe01-1",
    ),
    (
        r"C:\Users\62379\.cursor\projects\d-AI\assets\c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images___01-2-652d5629-4daf-4bdb-adcf-7da4df58a7df.png",
        "\u4e3b\u56fe01-2",
    ),
    (
        r"C:\Users\62379\.cursor\projects\d-AI\assets\c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images___02-2-65e278ab-f134-41d7-8bc2-74cba02678d3.png",
        "\u4e3b\u56fe02-2",
    ),
    (
        r"C:\Users\62379\.cursor\projects\d-AI\assets\c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images___03-f0cace35-b6f0-4756-8412-e8f0c00258dd.png",
        "\u4e3b\u56fe03",
    ),
    (
        r"C:\Users\62379\.cursor\projects\d-AI\assets\c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images___04-f5928c38-d321-4365-a6f8-ee88c39d25fa.png",
        "\u4e3b\u56fe04",
    ),
    (
        r"C:\Users\62379\.cursor\projects\d-AI\assets\c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images___05-88e16a9b-9151-43e3-887c-aacaaf72c6c8.png",
        "\u4e3b\u56fe05",
    ),
    (
        r"C:\Users\62379\.cursor\projects\d-AI\assets\c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images___06-30a50581-7c8c-4529-9700-25551f16c703.png",
        "\u4e3b\u56fe06",
    ),
    (
        r"C:\Users\62379\.cursor\projects\d-AI\assets\c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images___07-830bf45e-291e-43c3-ba0a-de8250cc4fe0.png",
        "\u4e3b\u56fe07",
    ),
    (
        r"C:\Users\62379\.cursor\projects\d-AI\assets\c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images___11-2e8b9fa4-babd-481f-aaf4-f6762d9543c7.png",
        "\u4e3b\u56fe11",
    ),
    (
        r"C:\Users\62379\.cursor\projects\d-AI\assets\c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images___12-3206e086-6ff5-4689-83e0-ca7d84fa4b4c.png",
        "\u4e3b\u56fe12",
    ),
    (
        r"C:\Users\62379\.cursor\projects\d-AI\assets\c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images___13-5db024fe-b41e-44d9-84de-11f2fbee03c9.png",
        "\u4e3b\u56fe13",
    ),
    (
        r"C:\Users\62379\.cursor\projects\d-AI\assets\c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images___14-36cdb956-e89a-441b-a1d7-d950a42c4ad5.png",
        "\u4e3b\u56fe14",
    ),
    (
        r"C:\Users\62379\.cursor\projects\d-AI\assets\c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images___15-d8cb44fd-1467-4379-aefc-790e5ab797c0.png",
        "\u4e3b\u56fe15",
    ),
    (
        r"C:\Users\62379\.cursor\projects\d-AI\assets\c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images___17-d3a307c1-48c4-4b31-91a3-0cbe3567681a.png",
        "\u4e3b\u56fe17",
    ),
    (
        r"C:\Users\62379\.cursor\projects\d-AI\assets\c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images___16-c8cb37cb-d1d6-4a87-a5c2-e3a0d66e2e55.png",
        "\u4e3b\u56fe16",
    ),
]


def export(src: Path, dest: Path, max_w: int = 1400) -> None:
    im = Image.open(src)
    if im.mode in ("RGBA", "LA"):
        bg = Image.new("RGB", im.size, (255, 255, 255))
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
    if MAIN_DIR.exists():
        shutil.rmtree(MAIN_DIR)
    MAIN_DIR.mkdir(parents=True)
    for src_str, stem in SOURCES:
        src = Path(src_str)
        if not src.exists():
            raise FileNotFoundError(src)
        export(src, MAIN_DIR / f"{stem}.jpg")


def gallery_lines() -> str:
    lines = []
    for _, stem in SOURCES:
        fname = f"{stem}.jpg"
        src = f"../assets/product/ecom/main/{fname}"
        lines.append(
            f'          <figure class="gallery-card"><img src="{src}" alt="{stem}" loading="lazy" />'
            f"<figcaption>{stem}</figcaption></figure>"
        )
    return "\n".join(lines)


def patch_html() -> None:
    import re

    page = Path(__file__).resolve().parent / "works" / "product.html"
    text = page.read_text(encoding="utf-8")
    gallery = gallery_lines()
    pattern = (
        r'(<div class="ecom-group" id="ecom-main">.*?<div class="horizontal-scroll">)\s*'
        r".*?"
        r'(</div>\s*</section>\s*</div>\s*</section>\s*\n\n  </div>)'
    )
    new_text, n = re.subn(
        pattern,
        r"\1\n" + gallery + r"\n        \2",
        text,
        count=1,
        flags=re.DOTALL,
    )
    if not n:
        raise SystemExit("ecom-main gallery block not found")
    page.write_text(new_text, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    sync_assets()
    patch_html()
    print(f"synced {len(SOURCES)} main images and patched product.html")
