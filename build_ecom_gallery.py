# -*- coding: utf-8 -*-
from pathlib import Path

DST = Path(__file__).resolve().parent / "assets" / "product" / "ecom"

GROUPS = [
    ("white", "\u767d\u8272\u98ce\u6247", "\u9732\u8425\u98ce\u6247\u767d\u8272\u6b3e\u5355\u54c1\u4e0e\u7ec4\u5408\u6e32\u67d3\uff0c\u9ed1\u5e95\u68da\u62cd\u7a81\u51fa\u7ed3\u6784\u4e0e\u8d28\u611f\u3002"),
    ("green", "\u7eff\u8272\u98ce\u6247", "\u6a44\u6984\u7eff\u6b3e\u98ce\u6247\u5355\u54c1\u3001\u573a\u666f\u4e0e\u529f\u80fd\u5356\u70b9\u56fe\uff0c\u542b\u78c1\u5438\u9065\u63a7\u7b49\u7535\u5546\u8be6\u60c5\u89c6\u89c9\u3002"),
    ("main", "\u4ea7\u54c1\u4e3b\u56fe", "\u4e9a\u9a6c\u900a / \u963f\u91cc\u56fd\u9645\u7ad9\u4e3b\u56fe\u3001\u573a\u666f\u6d77\u62a5\u4e0e\u8be6\u60c5\u9875\u957f\u56fe\uff0c\u8986\u76d6\u5356\u70b9\u4e0e\u4f7f\u7528\u573a\u666f\u3002"),
]


def cards(cat: str) -> str:
    lines = []
    for p in sorted((DST / cat).glob("*.jpg")):
        src = f"../assets/product/ecom/{cat}/{p.name}"
        cap = p.stem
        lines.append(
            f'          <figure class="gallery-card"><img src="{src}" alt="{cap}" loading="lazy" />'
            f"<figcaption>{cap}</figcaption></figure>"
        )
    return "\n".join(lines)


def build() -> str:
    parts = []
    for cat, title, desc in GROUPS:
        parts.append(
            f"""    <div class="ecom-group" id="ecom-{cat}">
      <header class="ecom-group__head">
        <h3 class="ecom-group__title">{title}</h3>
        <p class="ecom-group__desc">{desc}</p>
      </header>
      <section class="gallery-strip" aria-label="{title}">
        <div class="horizontal-scroll">
{cards(cat)}
        </div>
      </section>
    </div>"""
        )
    return "\n".join(parts)


def patch_product_page() -> None:
    page = Path(__file__).resolve().parent / "works" / "product.html"
    text = page.read_text(encoding="utf-8")
    inner = build()
    block = f"""    <section class="gallery-collection" id="col-ecom">
      <header class="collection-head">
        <span class="collection-num">\u9009\u96c6 05</span>
        <h2>\u7535\u5546\u4ea7\u54c1</h2>
        <p>\u4e9a\u9a6c\u900a\u3001\u963f\u91cc\u5df4\u5df4\u56fd\u9645\u7ad9\u4ea7\u54c1\u4e3b\u56fe\u89c4\u8303\u4e0e\u8be6\u60c5\u9875\u89c6\u89c9\uff0c\u652f\u6491\u98ce\u6247\u7b49\u54c1\u7c7b\u51fa\u6d77\u5c55\u793a\u4e0e\u8f6c\u5316\u3002</p>
      </header>
{inner}
    </section>"""
    import re

    new_text, n = re.subn(
        r'    <section class="gallery-collection" id="col-ecom">.*?</section>\s*\n\n  </div>',
        block + "\n\n  </div>",
        text,
        count=1,
        flags=re.DOTALL,
    )
    if not n:
        raise SystemExit("col-ecom block not found")
    page.write_text(new_text, encoding="utf-8", newline="\n")
    print("patched product.html OK")


if __name__ == "__main__":
    patch_product_page()
