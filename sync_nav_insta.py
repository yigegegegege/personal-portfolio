# -*- coding: utf-8 -*-
"""Sync unified nav across portfolio HTML files."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WORKS = ROOT / "works"

NAV_INDEX = """      <ul class="nav-links">
        <li><a href="#section-poster" data-section="poster">品牌视觉</a></li>
        <li><a href="#section-product" data-section="product">产品视觉</a></li>
        <li><a href="#section-ip" data-section="ip">IP 设计</a></li>
        <li><a href="#section-aigc" data-section="aigc">AIGC</a></li>
        <li><a href="#section-scene" data-section="scene">场景 3D</a></li>
        <li><a href="#section-about" data-section="about">关于</a></li>
      </ul>"""

NAV_WORK = """      <ul class="nav-links">
        <li><a href="../index.html#section-poster">品牌视觉</a></li>
        <li><a href="../index.html#section-product">产品视觉</a></li>
        <li><a href="../index.html#section-ip">IP 设计</a></li>
        <li><a href="../index.html#section-aigc">AIGC</a></li>
        <li><a href="../index.html#section-scene">场景 3D</a></li>
        <li><a href="../index.html#section-about">关于</a></li>
      </ul>"""

NAV_RE = re.compile(r"<ul class=\"nav-links\">.*?</ul>", re.DOTALL)


def main() -> None:
    index = ROOT / "index.html"
    t = index.read_text(encoding="utf-8")
    t = NAV_RE.sub(NAV_INDEX.strip(), t, count=1)
    index.write_text(t, encoding="utf-8", newline="\n")
    print("index.html")

    for path in sorted(WORKS.glob("*.html")):
        text = path.read_text(encoding="utf-8")
        text = NAV_RE.sub(NAV_WORK.strip(), text, count=1)
        path.write_text(text, encoding="utf-8", newline="\n")
        print(path.name)


if __name__ == "__main__":
    main()
