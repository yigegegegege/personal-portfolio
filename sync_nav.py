# -*- coding: utf-8 -*-
import re
from pathlib import Path

WORKS = Path(__file__).resolve().parent / "works"

NAV = """  <nav class="site-nav scrolled">
    <div class="inner">
      <a class="brand" href="../index.html">TOM XIE</a>
      <ul class="nav-links">
        <li><a href="../index.html#section-about">\u5173\u4e8e</a></li>
        <li><a href="../index.html#section-product">\u4ea7\u54c1\u6e32\u67d3</a></li>
        <li><a href="../index.html#section-ip">IP\u8bbe\u8ba1</a></li>
        <li><a href="../index.html#section-scene">\u573a\u666f\u6e32\u67d3</a></li>
        <li><a href="../index.html#section-poster">\u54c1\u724c\u5e73\u9762</a></li>
        <li><a href="../index.html#section-other">\u5176\u4ed6\u4f5c\u54c1</a></li>
        <li><a href="../index.html#section-contact">\u8054\u7cfb</a></li>
      </ul>
    </div>
  </nav>"""

pattern = re.compile(
    r"<nav class=\"site-nav[^\"]*\">.*?</nav>",
    re.DOTALL,
)

for path in WORKS.glob("*.html"):
    text = path.read_text(encoding="utf-8", errors="replace")
    new_text, n = pattern.subn(NAV, text, count=1)
    if n:
        path.write_text(new_text, encoding="utf-8", newline="\n")
        print("updated", path.name)
    else:
        print("skip", path.name)
