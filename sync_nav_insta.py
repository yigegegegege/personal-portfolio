# -*- coding: utf-8 -*-
"""Sync unified nav across portfolio HTML files."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WORKS = ROOT / "works"

NAV_ACTIONS = """      <div class="nav-actions">
        <button type="button" class="lang-toggle" id="lang-toggle" aria-label="Switch to English">EN</button>
        <button type="button" class="nav-contact-btn" id="nav-contact-toggle" aria-expanded="false" aria-haspopup="true" aria-controls="nav-contact-menu" data-i18n="nav.contact">联系</button>
        <div class="nav-contact-menu" id="nav-contact-menu" role="menu" hidden>
          <p class="nav-contact-menu__lead" data-i18n="nav.contactLead">欢迎视觉设计相关合作，通常 24 小时内回复。</p>
          <a class="nav-contact-menu__item" href="tel:+8615899782952" role="menuitem">
            <span class="nav-contact-menu__label" data-i18n="nav.phoneWechat">电话 / 微信</span>
            <span class="nav-contact-menu__value">+86 158 9978 2952</span>
          </a>
          <a class="nav-contact-menu__item" href="mailto:623797004@qq.com" role="menuitem">
            <span class="nav-contact-menu__label" data-i18n="nav.email">邮箱</span>
            <span class="nav-contact-menu__value">623797004@qq.com</span>
          </a>
        </div>
      </div>"""

NAV_INDEX = """      <ul class="nav-links">
        <li><a href="#section-poster" data-section="poster" data-i18n="nav.brandVisual">品牌视觉</a></li>
        <li><a href="#section-product" data-section="product" data-i18n="nav.productVisual">产品视觉</a></li>
        <li><a href="#section-ip" data-section="ip" data-i18n="nav.ipDesign">IP 设计</a></li>
        <li><a href="#section-aigc" data-section="aigc" data-i18n="nav.aigc">AIGC</a></li>
        <li><a href="#section-scene" data-section="scene" data-i18n="nav.scene3d">场景 3D</a></li>
        <li><a href="#section-about" data-section="about" data-i18n="nav.about">关于</a></li>
      </ul>"""

NAV_WORK = """      <ul class="nav-links">
        <li><a href="../index.html#section-poster" data-i18n="nav.brandVisual">品牌视觉</a></li>
        <li><a href="../index.html#section-product" data-i18n="nav.productVisual">产品视觉</a></li>
        <li><a href="../index.html#section-ip" data-i18n="nav.ipDesign">IP 设计</a></li>
        <li><a href="../index.html#section-aigc" data-i18n="nav.aigc">AIGC</a></li>
        <li><a href="../index.html#section-scene" data-i18n="nav.scene3d">场景 3D</a></li>
        <li><a href="../index.html#section-about" data-i18n="nav.about">关于</a></li>
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
