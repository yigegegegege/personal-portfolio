# -*- coding: utf-8 -*-
"""Copy yanzhan/shuban channel KV sets into portfolio and patch poster.html."""
from __future__ import annotations

import json
import re
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SRC = Path(r"D:\AI\chanpinshengtu\生成产出\草稿\yanzhan\shuban")
LABELS = Path(r"D:\AI\chanpinshengtu\生成产出\草稿\yanzhan\manifest.json")
POSTER = ROOT / "works" / "poster.html"
OUT = ROOT / "assets" / "poster" / "yanzhan-channels"
MANIFEST = OUT / "manifest.json"
FEATURED = {"01-stadium", "06-waterproof", "08-seamless", "11-mtb"}

SCENE_RE = re.compile(r"LPDISPLAYD_KV_(\d+)_(.+?)_horizontal_v3_20260610\.jpg$")


def save_jpg(src: Path, dst: Path) -> tuple[int, int]:
    img = Image.open(src)
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    dst.parent.mkdir(parents=True, exist_ok=True)
    img.save(dst, "JPEG", quality=92, optimize=True)
    return img.size


def headline_title(path: Path) -> str:
    data = json.loads((SRC / "manifest.json").read_text(encoding="utf-8"))
    key = path.name
    for item in data:
        if Path(item["file"]).name == key or item["file"].endswith(path.name):
            words = item.get("headline", [])
            return " ".join(words)
    return path.stem


def zh_label(num: str, scene: str) -> str:
    needle = f"LPDISPLAYD_KV_{num}_{scene}_horizontal"
    for item in json.loads(LABELS.read_text(encoding="utf-8")):
        if needle in item["slug"]:
            return item["label"]
    return scene.replace("_", " ")


def build_sets() -> list[dict]:
    masters = sorted(SRC.glob("LPDISPLAYD_KV_*_horizontal_v3_20260610.jpg"))
    manifest: list[dict] = []

    for master_src in masters:
        m = SCENE_RE.match(master_src.name)
        if not m:
            continue
        num, scene = m.group(1), m.group(2)
        slug = f"{int(num):02d}-{scene.replace('_', '-')}"

        wechat_src = SRC / "gongzhonghao" / f"LPDISPLAYD_KV_{num}_{scene}_gongzhonghao_v3_20260610.jpg"
        square_src = SRC / "gongzhonghao" / f"LPDISPLAYD_KV_{num}_{scene}_gongzhonghao_square_v3_20260610.jpg"
        if not wechat_src.exists() or not square_src.exists():
            raise FileNotFoundError(f"Missing channel files for {master_src.name}")

        master_dst = OUT / f"{slug}-master.jpg"
        wechat_dst = OUT / f"{slug}-wechat-900x383.jpg"
        square_dst = OUT / f"{slug}-square-900x900.jpg"

        master_size = save_jpg(master_src, master_dst)
        wechat_size = save_jpg(wechat_src, wechat_dst)
        square_size = save_jpg(square_src, square_dst)

        en = headline_title(master_src)
        zh = zh_label(num, scene)
        title = f"{int(num):02d} · {en} · {zh}"

        manifest.append({
            "slug": slug,
            "title": title,
            "master": f"yanzhan-channels/{master_dst.name}",
            "wechat": f"yanzhan-channels/{wechat_dst.name}",
            "square": f"yanzhan-channels/{square_dst.name}",
            "master_size": f"{master_size[0]}×{master_size[1]}",
            "wechat_size": f"{wechat_size[0]}×{wechat_size[1]}",
            "square_size": f"{square_size[0]}×{square_size[1]}",
        })
        print("ok", slug)

    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return manifest


def render_html(manifest: list[dict]) -> str:
    parts = [
        '      <div class="channel-extend-block" id="col-action-kv-channels">',
        '        <header class="collection-head collection-head--inline">',
        '          <h3>渠道尺寸延展</h3>',
        '          <p>同一套主 KV 延展公众号头图（900×383）与方形社媒封面（900×900），核心卖点与构图逻辑保持一致。</p>',
        '        </header>',
        '',
    ]
    for item in manifest:
        slug = item["slug"]
        if slug in FEATURED:
            article_class = 'channel-extend-set'
            article_attrs = ""
        else:
            article_class = "channel-extend-set channel-extend-set--more"
            article_attrs = " hidden"
        parts.extend([
            f'        <article class="{article_class}"{article_attrs}>',
            f'          <p class="channel-extend-set__title">{item["title"]}</p>',
            '          <figure class="channel-extend-set__master">',
            f'            <img src="../assets/poster/{item["master"]}" alt="主 KV · {item["title"]}" loading="lazy" width="1920" height="1080" />',
            '            <figcaption>主 KV · 横版投放</figcaption>',
            '          </figure>',
            '          <div class="channel-extend-set__channels">',
            '            <figure class="channel-extend-set__wechat">',
            f'              <img src="../assets/poster/{item["wechat"]}" alt="公众号头图 900×383" loading="lazy" width="900" height="383" />',
            '              <figcaption>公众号头图 · 900×383</figcaption>',
            '            </figure>',
            '            <figure class="channel-extend-set__vertical">',
            f'              <img src="../assets/poster/{item["square"]}" alt="方形社媒封面 900×900" loading="lazy" width="900" height="900" />',
            '              <figcaption>方形社媒封面 · 900×900</figcaption>',
            '            </figure>',
            '          </div>',
            '        </article>',
            '',
        ])
    parts.extend([
        '',
        '        <div class="channel-extend-actions">',
        '          <button type="button" class="channel-extend-toggle" id="channel-extend-toggle" aria-expanded="false" data-label-expand="展开全部 21 套渠道延展" data-label-collapse="收起渠道延展">展开全部 21 套渠道延展</button>',
        '        </div>',
        '      </div>',
    ])
    return "\n".join(parts)


def patch_poster(html_block: str) -> None:
    text = POSTER.read_text(encoding="utf-8")
    text, n = re.subn(
        r'      <div class="channel-extend-block" id="col-action-kv-channels">.*?</div>\n\n      <dl class="case-study-meta">',
        html_block + '\n\n      <dl class="case-study-meta">',
        text,
        count=1,
        flags=re.S,
    )
    if n != 1:
        raise SystemExit(f"poster patch failed: {n}")
    text = text.replace(
        "社媒投放 KV · 公众号头图 · 9:16 竖版封面 · 新品上市主视觉",
        "社媒投放 KV · 公众号头图 · 方形社媒封面 · 新品上市主视觉",
    )
    POSTER.write_text(text, encoding="utf-8")


def main() -> None:
    manifest = build_sets()
    patch_poster(render_html(manifest))
    print("patched poster.html with", len(manifest), "channel sets")


if __name__ == "__main__":
    main()
