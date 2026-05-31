# -*- coding: utf-8 -*-
"""Replace ecom/white with user-provided white fan images only."""
from pathlib import Path
import re
import shutil

from PIL import Image

ROOT = Path(__file__).resolve().parent
WHITE_DIR = ROOT / "assets" / "product" / "ecom" / "white"
PRODUCT_HTML = ROOT / "works" / "product.html"

SOURCES = [
    (
        r"C:\Users\62379\.cursor\projects\d-AI\assets\c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_009-38174fb2-0e8d-499f-9367-99e4d2428c51.png",
        "009",
    ),
    (
        r"C:\Users\62379\.cursor\projects\d-AI\assets\c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_14-1-c2132d6e-fcd3-42e0-b122-be9cc3ee2494.png",
        "14-1",
    ),
    (
        r"C:\Users\62379\.cursor\projects\d-AI\assets\c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_010-8eca8c0d-4041-4b66-89e3-b39fd97e7dfc.png",
        "010",
    ),
    (
        r"C:\Users\62379\.cursor\projects\d-AI\assets\c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_12-1-6cc44d68-2a1b-4416-902f-ee459de35713.png",
        "12-1",
    ),
    (
        r"C:\Users\62379\.cursor\projects\d-AI\assets\c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_16-1-3f934177-2310-4da2-9bd1-28b6531cc8d6.png",
        "16-1",
    ),
    (
        r"C:\Users\62379\.cursor\projects\d-AI\assets\c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_002-1-c80270ce-6309-4100-b1bd-a0137ac44344.png",
        "002-1",
    ),
    (
        r"C:\Users\62379\.cursor\projects\d-AI\assets\c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_27-0bf5a9c8-5c2b-4bdf-992a-2ed099596592.png",
        "27",
    ),
    (
        r"C:\Users\62379\.cursor\projects\d-AI\assets\c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_33-2-3bfb417e-59c9-4dec-81ff-f6176d067f69.png",
        "33-2",
    ),
    (
        r"C:\Users\62379\.cursor\projects\d-AI\assets\c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_25-904b6215-f508-429a-b48c-1d4c08e5b034.png",
        "25",
    ),
    (
        r"C:\Users\62379\.cursor\projects\d-AI\assets\c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_37-2-c40734b0-bd39-4c53-a166-cd0a42ce2514.png",
        "37-2",
    ),
    (
        r"C:\Users\62379\.cursor\projects\d-AI\assets\c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_17-30e9b646-08a4-4f58-8832-e7d0dfefd75d.png",
        "17",
    ),
    (
        r"C:\Users\62379\.cursor\projects\d-AI\assets\c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_34-2-7a81d5d4-d155-4924-a93d-52869a9afff6.png",
        "34-2",
    ),
    (
        r"C:\Users\62379\.cursor\projects\d-AI\assets\c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_20-d21f5975-1b10-415c-8cd2-2ddd476a87a5.png",
        "20",
    ),
    (
        r"C:\Users\62379\.cursor\projects\d-AI\assets\c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_38-2-031203e6-a012-4d72-995f-9eb8b6c1d3a7.png",
        "38-2",
    ),
    (
        r"C:\Users\62379\.cursor\projects\d-AI\assets\c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_002-2-3dd03904-6666-48db-ba56-ec2f920fc51c.png",
        "002-2",
    ),
    (
        r"C:\Users\62379\.cursor\projects\d-AI\assets\c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_004-8be7f44d-d091-4fe9-b295-d4a23f6f2cff.png",
        "004",
    ),
    (
        r"C:\Users\62379\.cursor\projects\d-AI\assets\c__Users_62379_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_23-5769dcd4-3254-48a8-8225-3c5baae02f17.png",
        "23",
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


def sync_assets() -> list[str]:
    if WHITE_DIR.exists():
        shutil.rmtree(WHITE_DIR)
    WHITE_DIR.mkdir(parents=True)
    names = []
    for src_str, stem in SOURCES:
        src = Path(src_str)
        if not src.exists():
            raise FileNotFoundError(src)
        out = WHITE_DIR / f"{stem}.jpg"
        export(src, out)
        names.append(out.name)
    return names


def gallery_html() -> str:
    lines = []
    for _, stem in SOURCES:
        fname = f"{stem}.jpg"
        src = f"../assets/product/ecom/white/{fname}"
        lines.append(
            f'          <figure class="gallery-card"><img src="{src}" alt="{stem}" loading="lazy" />'
            f"<figcaption>{stem}</figcaption></figure>"
        )
    return "\n".join(lines)


def patch_html() -> None:
    text = PRODUCT_HTML.read_text(encoding="utf-8")
    new_scroll = (
        '      <section class="gallery-strip" aria-label="\u767d\u8272\u98ce\u6247">\n'
        "        <div class=\"horizontal-scroll\">\n"
        f"{gallery_html()}\n"
        "        </div>\n"
        "      </section>"
    )
    pattern = (
        r'      <section class="gallery-strip" aria-label="????">'
        r".*?</section>\n    </div>\n    <div class=\"ecom-group\" id=\"ecom-green\">"
    )
    new_text, n = re.subn(
        pattern,
        new_scroll + '\n    </div>\n    <div class="ecom-group" id="ecom-green">',
        text,
        count=1,
        flags=re.DOTALL,
    )
    if not n:
        raise SystemExit("ecom-white gallery block not found")
    PRODUCT_HTML.write_text(new_text, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    files = sync_assets()
    patch_html()
    print(f"synced {len(files)} white fan images")
