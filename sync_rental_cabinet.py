# -*- coding: utf-8 -*-
"""Replace assets/product/rental with user-provided LED rental cabinet images."""
from pathlib import Path
import re
import shutil

from PIL import Image

ROOT = Path(__file__).resolve().parent
RENTAL_DIR = ROOT / "assets" / "product" / "rental"
PRODUCT_HTML = ROOT / "works" / "product.html"
ASSETS = Path(r"C:\Users\62379\.cursor\projects\d-AI\assets")

SOURCES = [
    (ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_03-2-73065b28-c6e4-47c8-bff0-96fe0a146b93.png", "03-2"),
    (ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images____-1-b9cf010a-cdd5-4667-8246-9a8752845af2.png", "corner-01"),
    (ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images___2-b805aad2-08bf-4a1b-b70d-ae3ee0bc06a1.png", "rear-02"),
    (ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_008-a63e28ce-658f-41da-b115-7a6603511077.png", "008"),
    (ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_007-47740f34-c2ab-4def-8902-c50385b74859.png", "007"),
    (ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_002-c959c2bd-2e1a-422a-a644-fbe7945dd646.png", "002"),
    (ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_005-6f612527-a246-45cd-acd0-5f935254fbda.png", "005"),
    (ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images____2-e9936df9-60d9-4392-955c-c1380d5ab060.png", "lock-02"),
    (ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images________-459beec2-bf15-4743-b625-701b14fa7b17.png", "press-detail"),
    (ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images____-c54bb626-a955-4c11-839d-ab0090b17c05.png", "front-back"),
    (ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_d8841c3084df4d36ee02e9d94678e90-ea431c12-c823-4e71-b14d-8e17349324e3.png", "panel-01"),
    (ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_d51b856bffd859ea5d45fc595df5ac9-4d8bf8e9-94de-41f0-b962-b34adb2e1c89.png", "panel-02"),
    (ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images____4x4-2efa9da6-eeb0-4883-bce1-188022116e69.png", "wall-4x4"),
    (ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_____-0a372bb4-0f69-4906-ba2c-b2ef45102395.png", "rear-red"),
    (ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images___-9f83162a-7333-4172-82c5-90d985adb136.png", "module-tilt"),
    (ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images______-56a333da-1e00-48ac-b96a-20f5464b8358.png", "exploded"),
    (ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images____-c9737e89-8eb0-4bbb-af70-7b603802221d.png", "rear-open"),
    (ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_____-612a44e2-a6d3-40f5-85e9-8a6c44e6f906.png", "corner-lock"),
    (ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_019_1_-1bfa370d-dd4a-4808-9a9e-56a4a5694f9d.png", "019-1"),
    (ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_020-d0f146a2-20ac-4a1e-bdfd-0f8b502147b6.png", "020"),
    (ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_043-91b24dbf-447c-41a0-b37d-7599ce125410.png", "043"),
    (ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_042-c94c97ff-9b78-4cca-8df5-ec0c89aee084.png", "042"),
    (ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_012-e901fc3a-b93c-4761-bfec-162bf26eda45.png", "012"),
    (ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_038-33e4d5b3-6726-4a35-94a8-5c11ef58e8e0.png", "038"),
    (ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_021-afb2c432-da91-4f38-866b-5a5e94686062.png", "021"),
    (ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_022-7ace2ee4-7f9b-407d-ac4c-f686223d7297.png", "022"),
    (ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_011-faf00ae3-a314-4ca6-af73-b7531569848e.png", "011"),
    (ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_34-d62bd9d7-4846-45f7-ba4f-c757b2c8c2fb.png", "34"),
    (ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_024-14d3dd83-42d6-453b-866b-7795962e9148.png", "024"),
    (ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_006-b6094ac7-220d-494a-acd4-c9e96988f58f.png", "006"),
    (ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_005-48903175-3d1e-4a8f-a134-756a6b5f99ca.png", "005-alt"),
    (ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_023-b1e50a7f-5457-4b30-9b70-3e86188cdb31.png", "023"),
    (ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_011-7b6c2ada-7bd6-4e7f-a37b-e7793cef7e5f.png", "011-alt"),
    (ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_014-a7f99bf2-0658-4342-8217-d4df90ff0b3f.png", "014"),
    (ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_015-a0ec2d80-356f-4fad-b3d4-47be0a45eb73.png", "015"),
    (ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_007-9f3f5ec6-f385-4e8c-b58b-35905d1a1566.png", "007-alt"),
    (ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_016-82bfc404-6224-4560-a07e-4a2671727266.png", "016"),
    (ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_019-478349bf-f804-49e0-847e-6e73fa3e64ed.png", "019"),
    (ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_018-ad42c7b6-c445-40a7-8791-75265ce2ff0f.png", "018"),
    (ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_009-5de8891d-7f1c-455f-bcff-f0fe0f12d94a.png", "009"),
    (ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_027-e1c344fb-ff45-4c7c-91f7-48a6857b532c.png", "027"),
    (ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_026-b0a44d9f-03bb-4799-8455-c4bb1e142a07.png", "026"),
]


def export(src: Path, dest: Path, max_w: int = 1600) -> None:
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
    if RENTAL_DIR.exists():
        shutil.rmtree(RENTAL_DIR)
    RENTAL_DIR.mkdir(parents=True)
    for src, stem in SOURCES:
        if not src.exists():
            raise FileNotFoundError(src)
        export(src, RENTAL_DIR / f"{stem}.jpg")


def gallery_lines() -> str:
    lines = []
    for _, stem in SOURCES:
        src = f"../assets/product/rental/{stem}.jpg"
        lines.append(
            f'          <figure class="gallery-card"><img src="{src}" alt="{stem}" loading="lazy" />'
            f"<figcaption>{stem}</figcaption></figure>"
        )
    return "\n".join(lines)


def patch_html() -> None:
    text = PRODUCT_HTML.read_text(encoding="utf-8")
    gallery = gallery_lines()
    pattern = (
        r'(<section class="gallery-collection" id="col-signage">.*?<div class="horizontal-scroll">)\s*'
        r".*?"
        r'(</div>\s*</section>\s*</section>\s*<section class="gallery-collection" id="col-ecom">)'
    )
    new_text, n = re.subn(
        pattern,
        r"\1\n" + gallery + r"\n        \2",
        text,
        count=1,
        flags=re.DOTALL,
    )
    if not n:
        raise SystemExit("col-signage gallery block not found")
    PRODUCT_HTML.write_text(new_text, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    sync_assets()
    patch_html()
    print(f"synced {len(SOURCES)} LED rental cabinet images")
