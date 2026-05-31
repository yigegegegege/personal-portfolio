# -*- coding: utf-8 -*-
"""Replace assets/product/cabinet with user-provided LED cabinet images."""
from pathlib import Path
import re
import shutil

from PIL import Image

ROOT = Path(__file__).resolve().parent
CABINET_DIR = ROOT / "assets" / "product" / "cabinet"
PRODUCT_HTML = ROOT / "works" / "product.html"
ASSETS = Path(r"C:\Users\62379\.cursor\projects\d-AI\assets")

SOURCES = [
    (ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_02-2-ab859e87-8c0a-426d-98ce-c81b37c870d6.png", "02-2"),
    (ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images______20230714181213-351525a3-cc4c-4157-814e-2d81e9ef9de1.png", "scene-01"),
    (ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images___3-4f42a69c-8145-4713-b898-b02ee6ec109c.png", "panel-01"),
    (ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_banner2-cbf10c9c-83c0-4ec2-9ef4-6a59efce5977.png", "banner-02"),
    (ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_02-1-0cc495c2-fb25-4476-a378-b9d39b4d07fe.png", "02-1"),
    (ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_01-1-fdf03c70-aa9e-406b-a79e-aa0a057107d5.png", "01-1"),
    (ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_012-807c2ec5-6d2d-43f1-826c-9567731e42bc.png", "012"),
    (ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_013-eca42413-8af9-4c25-b683-29dfe48c8397.png", "013"),
    (ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_010-fa348b7d-fa43-40ec-863f-8ee6e985955c.png", "010"),
    (ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_45G__008-9858ecc3-2e73-4613-a233-ce3c41543295.png", "45G-008"),
    (ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_45G__009-b9a534b6-2e9a-4b51-9196-3a0d7bede3c6.png", "45G-009"),
    (ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_45G__010-f9ab575a-218c-41d2-a87d-61f633001603.png", "45G-010"),
    (ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_45G__007-cbbe8c59-02b4-4f59-8244-c10158a48f07.png", "45G-007"),
    (ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_45G__012-9be9d554-e363-46ed-8cf4-6fb8902ff8d0.png", "45G-012"),
    (ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_45G__010-8eabe7b1-230b-460c-a0d4-131246ba1b35.png", "45G-010-alt"),
    (ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_007-3-67a077db-9e01-42f2-8fc3-9ff48523d3f3.png", "007-3"),
    (ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_007-2-ea7ca7d7-8fa9-47ae-be17-3d9898e5528c.png", "007-2"),
    (ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_008-1-c80f9e35-ee0f-407a-994d-26be0bd2e368.png", "008-1"),
    (ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_008-2-6aecef41-03d1-4f2a-985c-caa37d80309c.png", "008-2"),
    (ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images___-59771548-331c-4f09-a821-cae7bce78974.png", "cabinet-20"),
    (ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_03png-bff778c0-3229-4646-ac92-67d31980a51c.png", "03"),
    (ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_04-7619279c-ef35-4d93-b21a-24316f16a6bc.png", "04"),
    (ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images___9-b11c183e-d53c-4776-8421-3a8415c738dd.png", "scene-09"),
    (ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images___8-591a0461-7642-4b10-aa84-7431e778a6d9.png", "scene-08"),
    (ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_014-1-0e1eabce-8b8f-46bd-9242-fc334b77b6f8.png", "014-1"),
    (ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_013-1-b5d97b3f-50a4-4f5a-ae6e-12dfedc12120.png", "013-1"),
    (ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_012-2-1030c293-5f8e-48f7-bf44-37f89b900e1b.png", "012-2"),
    (ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_011-2-70bfafeb-40e2-46b5-8c38-209ae39f5e96.png", "011-2"),
    (ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_024-abc511cf-05a6-4f9e-9c6d-bdf83de36d9a.png", "024"),
    (ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_027-b51c0184-0aa5-43b3-bf29-005b9615f39d.png", "027"),
    (ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_023-bf3196c0-c5d7-44f4-8058-a60754e34762.png", "023"),
    (ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_025-ab01b3c6-ab14-4dca-aad2-adf684e4940c.png", "025"),
    (ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_026-bd246ba5-4766-4fd8-a63b-fd04467ab21c.png", "026"),
    (ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_011-f88d4d59-1360-4b5d-89be-437f29754bda.png", "011"),
    (ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_017-d5b6ddaf-6eff-44be-b9f0-c192d92ff303.png", "017"),
    (ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_015-1af0f628-577c-4431-ac07-2c9321279b53.png", "015"),
    (ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_008-f1a74f9c-d7f8-4915-a949-81950b3aced2.png", "008"),
    (ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_007-60777368-2da5-4a82-9267-cfbd122cb2cb.png", "007"),
    (ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_009-5acd1c23-271c-4704-bef9-9d0882e2e4e7.png", "009"),
    (ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_63L_00012-c163fe1b-3b27-4d31-ad62-6c70655bdee0.png", "63L-012"),
    (ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_63L_00013-8eccc3b1-1a5d-4834-84d9-7c124b6a86af.png", "63L-013"),
    (ASSETS / "c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images____6-41ef8139-e56d-4a7a-affc-3adcd671e7ca.png", "scene-06"),
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
    if CABINET_DIR.exists():
        shutil.rmtree(CABINET_DIR)
    CABINET_DIR.mkdir(parents=True)
    for src, stem in SOURCES:
        if not src.exists():
            raise FileNotFoundError(src)
        export(src, CABINET_DIR / f"{stem}.jpg")


def gallery_lines() -> str:
    lines = []
    for _, stem in SOURCES:
        src = f"../assets/product/cabinet/{stem}.jpg"
        lines.append(
            f'          <figure class="gallery-card"><img src="{src}" alt="{stem}" loading="lazy" />'
            f"<figcaption>{stem}</figcaption></figure>"
        )
    return "\n".join(lines)


def patch_html() -> None:
    text = PRODUCT_HTML.read_text(encoding="utf-8")
    gallery = gallery_lines()
    pattern = (
        r'(<section class="gallery-collection" id="col-cob">.*?<div class="horizontal-scroll">)\s*'
        r".*?"
        r"(</div>\s*</section>\s*</section>\s*<section class=\"gallery-collection\" id=\"col-module\">)"
    )
    new_text, n = re.subn(
        pattern,
        r"\1\n" + gallery + r"\n        \2",
        text,
        count=1,
        flags=re.DOTALL,
    )
    if not n:
        raise SystemExit("col-cob gallery block not found")
    new_text = new_text.replace(
        "?? COB ????????????????????????????????????",
        "??????????????????????????????????????",
        1,
    )
    PRODUCT_HTML.write_text(new_text, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    sync_assets()
    patch_html()
    print(f"synced {len(SOURCES)} LED cabinet images")
