# -*- coding: utf-8 -*-
"""Curate portfolio galleries for Insta360 Visual Designer JD."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WORKS = ROOT / "works"

# Remove whole collections (not aligned with JD)
REMOVE_SECTIONS: dict[str, list[str]] = {
    "product.html": [],
    "ip.html": ["col-other-ip"],
    "poster.html": ["col-logo"],
}

# Per section: keep figures whose src contains any of these substrings.
# Missing section id -> keep all figures in that section.
FIGURE_KEEP: dict[str, dict[str, list[str]]] = {
    "poster.html": {
        "col-vi": [
            "lp-corp",
            "lpdisplay-vis",
            "lp-uniform",
        ],
        "col-social": [
            "/lpdisplay/01-sls",
            "/lpdisplay/02-sls",
            "/lpdisplay/03-sls",
            "/lpdisplay/04-sls",
            "ise-2026",
            "ise-2025",
            "ise-2024",
            "infocomm",
            "/lpdisplay/24-",
            "/lpdisplay/25-",
            "/lpdisplay/26-",
            "/lpdisplay/27-",
            "/lpdisplay/28-",
            "/lpdisplay/29-",
            "/lpdisplay/30-flip",
            "/lpdisplay/31-",
            "/lpdisplay/32-",
            "/lpdisplay/33-",
            "/lpdisplay/34-",
            "/lpdisplay/35-",
            "/lpdisplay/36-",
            "/vod/28-infocomm",
            "/vod/29-infocomm",
            "/vod/30-infocomm",
            "/vod/31-ise",
            "/vod/32-ise",
            "/vod/33-ise",
            "/vod/34-infocomm",
            "/vod/35-infocomm",
            "/vod/20-vivid",
            "/vod/25-premium",
            "/vod/17-our-factory",
            "/vod/01.png",
            "/vod/23-cineled",
        ],
    },
    "ip.html": {
        "col-stickers": [
            "sticker-01",
            "sticker-03",
            "sticker-05",
            "sticker-07",
            "sticker-10",
            "sticker-12",
        ],
        "col-social": [
            "social-02-en",
            "social-03-en",
            "social-05-infocomm",
            "social-06-infocomm",
            "social-07-ise",
            "social-10-new-year",
            "social-18-thanksgiving-en",
            "social-20-derivative",
            "social-21-emoji",
            "social-17-cny",
        ],
    },
    "scene.html": {
        "col-exhibition": [
            "exhi-02-ise2025",
            "exhi-01-sls",
            "exhi-09-sls",
            "exhi-04-lpdisplay",
            "exhi-08-lp",
            "exhi-17-archemy",
            "exhi-18-lpdisplay",
            "exhi-19-lp",
            "exhi-03-demos",
            "exhi-20-lpdisplay",
        ],
    },
}

FIGURE_RE = re.compile(
    r"<figure\s+class=\"gallery-card[^\"]*\"[^>]*>.*?</figure>",
    re.DOTALL | re.IGNORECASE,
)
SECTION_RE = re.compile(
    r'<section\s+class="gallery-collection"\s+id="([^"]+)"[^>]*>.*?</section>',
    re.DOTALL,
)
SRC_RE = re.compile(r'src="([^"]+)"', re.IGNORECASE)


def figure_src(fig_html: str) -> str | None:
    m = SRC_RE.search(fig_html)
    return m.group(1) if m else None


def should_keep(fig_src: str, patterns: list[str] | None) -> bool:
    if patterns is None:
        return True
    return any(p in fig_src for p in patterns)


def filter_section(section_html: str, section_id: str, file_key: str) -> str:
    rules = FIGURE_KEEP.get(file_key, {})
    patterns = rules.get(section_id)

    def repl(fig_match: re.Match) -> str:
        fig = fig_match.group(0)
        src = figure_src(fig)
        if not src:
            return fig
        return fig if should_keep(src, patterns) else ""

    inner = FIGURE_RE.sub(repl, section_html)
    if FIGURE_RE.search(inner):
        return inner
    return ""


def curate_file(path: Path) -> None:
    key = path.name
    text = path.read_text(encoding="utf-8")

    for sid in REMOVE_SECTIONS.get(key, []):
        text = re.sub(
            rf'<section\s+class="gallery-collection"\s+id="{re.escape(sid)}"[^>]*>.*?</section>\s*',
            "",
            text,
            flags=re.DOTALL,
        )
        text = re.sub(
            rf'\s*<a\s+href="#{re.escape(sid)}"[^>]*>.*?</a>\s*',
            "\n",
            text,
        )

    if key in FIGURE_KEEP:

        def section_repl(m: re.Match) -> str:
            sid = m.group(1)
            body = m.group(0)
            if sid in REMOVE_SECTIONS.get(key, []):
                return ""
            return filter_section(body, sid, key)

        text = SECTION_RE.sub(section_repl, text)

    text = re.sub(r"\n{3,}", "\n\n", text)
    path.write_text(text, encoding="utf-8", newline="\n")
    print("curated", key)


NAV_WORK = """  <nav class="site-nav scrolled">
    <div class="inner">
      <a class="brand" href="../index.html">谢意 · TOM XIE</a>
      <ul class="nav-links">
        <li><a href="../index.html#section-poster">品牌视觉</a></li>
        <li><a href="../index.html#section-product">产品视觉</a></li>
        <li><a href="../index.html#section-ip">IP 设计</a></li>
        <li><a href="../index.html#section-aigc">AIGC</a></li>
        <li><a href="../index.html#section-scene">场景 3D</a></li>
        <li><a href="../index.html#section-about">关于</a></li>
      </ul>
      <div class="nav-actions">
        <button type="button" class="nav-contact-btn" id="nav-contact-toggle" aria-expanded="false" aria-haspopup="true" aria-controls="nav-contact-menu">联系</button>
        <div class="nav-contact-menu" id="nav-contact-menu" role="menu" hidden>
          <p class="nav-contact-menu__lead">欢迎视觉设计相关合作，通常 24 小时内回复。</p>
          <a class="nav-contact-menu__item" href="tel:+8615899782952" role="menuitem">
            <span class="nav-contact-menu__label">电话 / 微信</span>
            <span class="nav-contact-menu__value">+86 158 9978 2952</span>
          </a>
          <a class="nav-contact-menu__item" href="mailto:623797004@qq.com" role="menuitem">
            <span class="nav-contact-menu__label">邮箱</span>
            <span class="nav-contact-menu__value">623797004@qq.com</span>
          </a>
        </div>
      </div>
    </div>
  </nav>"""

NAV_PATTERN = re.compile(
    r'<nav class="site-nav[^"]*">.*?</nav>',
    re.DOTALL,
)


def sync_nav() -> None:
    for path in WORKS.glob("*.html"):
        if path.name == "other.html":
            continue
        text = path.read_text(encoding="utf-8")
        new_text, n = NAV_PATTERN.subn(NAV_WORK, text, count=1)
        if n:
            path.write_text(new_text, encoding="utf-8", newline="\n")
            print("nav", path.name)


def renumber_collections(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    n = 0
    for m in list(re.finditer(r'(<span class="collection-num">)选集 \d+', text)):
        n += 1
        pass
    parts = text.split('<span class="collection-num">')
    if len(parts) < 2:
        return
    out = [parts[0]]
    for i, chunk in enumerate(parts[1:], start=1):
        chunk = re.sub(r"^选集 \d+", f"选集 {i:02d}", chunk, count=1)
        out.append('<span class="collection-num">' + chunk)
    path.write_text("".join(out), encoding="utf-8", newline="\n")


def main() -> None:
    other = WORKS / "other.html"
    if other.exists():
        other.unlink()
        print("deleted other.html")

    for path in sorted(WORKS.glob("*.html")):
        if path.name == "other.html":
            continue
        curate_file(path)
        renumber_collections(path)

    sync_nav()
    print("done")


if __name__ == "__main__":
    main()
