# -*- coding: utf-8 -*-
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POSTER = ROOT / "works" / "poster.html"
FEATURED = {"01-stadium", "06-waterproof", "08-seamless", "11-mtb"}


def patch() -> None:
    text = POSTER.read_text(encoding="utf-8")

    def repl(match: re.Match[str]) -> str:
        block = match.group(0)
        slug_m = re.search(r"yanzhan-channels/([\w-]+)-master", block)
        if not slug_m:
            return block
        slug = slug_m.group(1)
        if slug in FEATURED:
            return block
        return block.replace(
            '<article class="channel-extend-set">',
            '<article class="channel-extend-set channel-extend-set--more" hidden>',
            1,
        )

    text = re.sub(
        r'<article class="channel-extend-set">.*?</article>\s*',
        repl,
        text,
        flags=re.S,
    )

    more_count = len(FEATURED)
    total = len(re.findall(r"channel-extend-set", text)) - 1  # rough
    toggle = """
        <div class="channel-extend-actions">
          <button type="button" class="channel-extend-toggle" id="channel-extend-toggle" aria-expanded="false" data-label-expand="展开全部 21 套渠道延展" data-label-collapse="收起渠道延展">展开全部 21 套渠道延展</button>
        </div>
"""
    marker = "      </div>\n\n      <dl class=\"case-study-meta\">"
    if "channel-extend-toggle" not in text:
        text = text.replace(marker, toggle + marker, 1)

    text = text.replace(
        "社媒投放 KV · 公众号头图 · 9:16 竖版封面 · 新品上市主视觉",
        "社媒投放 KV · 公众号头图 · 方形社媒封面 · 新品上市主视觉",
    )

    POSTER.write_text(text, encoding="utf-8")
    print("patched poster.html")


if __name__ == "__main__":
    patch()
