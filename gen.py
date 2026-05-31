# ASCII-only source; writes UTF-8 HTML
from pathlib import Path

B = Path(__file__).resolve().parent
W = B / "works"
W.mkdir(exist_ok=True)

# Unicode labels
T = {
    "name": "\u8c22\u610f",
    "portfolio": "\u4e2a\u4eba\u4f5c\u54c1\u96c6",
    "about": "\u5173\u4e8e",
    "product": "\u4ea7\u54c1",
    "scene": "\u573a\u666f",
    "poster": "\u5e73\u9762",
    "back_home": "\u2190 \u8fd4\u56de\u9996\u9875",
    "back_index": "\u2190 \u8fd4\u56de\u4f5c\u54c1\u96c6\u9996\u9875",
    "gallery": "\u4f5c\u54c1\u9009\u96c6",
    "explore": "\u63a2\u7d22\u4e94\u4e2a\u677f\u5757",
}

NAV_HOME = f"""
        <li><a href="#section-about" data-section="about">{T['about']}</a></li>
        <li><a href="#section-product" data-section="product">{T['product']}</a></li>
        <li><a href="#section-ip">IP</a></li>
        <li><a href="#section-scene" data-section="scene">{T['scene']}</a></li>
        <li><a href="#section-poster" data-section="poster">{T['poster']}</a></li>"""

NAV_WORK = """
      <li><a href="../index.html#section-about">\u5173\u4e8e</a></li>
      <li><a href="../index.html#section-product">\u4ea7\u54c1\u6e32\u67d3</a></li>
      <li><a href="../index.html#section-ip">IP\u8bbe\u8ba1</a></li>
      <li><a href="../index.html#section-scene">\u573a\u666f\u6e32\u67d3</a></li>
      <li><a href="../index.html#section-poster">\u54c1\u724c\u5e73\u9762</a></li>
      <li><a href="../index.html#section-other">\u5176\u4ed6\u4f5c\u54c1</a></li>
      <li><a href="../index.html#section-contact">\u8054\u7cfb</a></li>"""

HEAD = """  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;600&family=Syne:wght@600;700;800&display=swap" rel="stylesheet" />"""


def save(path, html):
    Path(path).write_text(html, encoding="utf-8", newline="\n")


def work_page(filename, page_title, label, h1, desc, anchor, strip, grid):
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{page_title} \u00b7 {T['name']}{T['portfolio']}</title>
{HEAD}
  <link rel="stylesheet" href="../css/styles.css" />
</head>
<body>
  <div class="cursor-glow" aria-hidden="true"></div>
  <nav class="site-nav scrolled"><div class="inner">
    <a class="brand" href="../index.html">XIE YI</a>
    <ul class="nav-links">{NAV_WORK}
    </ul>
  </div></nav>
  <header class="work-hero">
    <a class="back" href="../index.html#{anchor}">{T['back_home']}</a>
    <p class="label">{label}</p>
    <h1>{h1}</h1>
    <p>{desc}</p>
  </header>
  <section class="gallery-strip"><h2>{T['gallery']}</h2>
    <div class="horizontal-scroll">
{strip}
    </div>
  </section>
  <section class="masonry">
{grid}
  </section>
  <footer class="site-footer"><p><a href="../index.html">{T['back_index']}</a></p></footer>
  <script src="../js/app.js"></script>
</body>
</html>"""
    save(W / filename, html)


def fig(src, cap):
    return f'      <figure class="gallery-card"><img src="{src}" alt="{cap}" loading="lazy" /><figcaption>{cap}</figcaption></figure>'


def mimg(src):
    return f'    <div class="masonry-item"><img src="{src}" alt="" loading="lazy" /></div>'


# --- index ---
save(
    B / "index.html",
    f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="description" content="{T['name']} \u2014 \u54c1\u724c\u4e0e\u4ea7\u54c1\u89c6\u89c9\u8bbe\u8ba1\u5e08\u4e2a\u4eba\u4f5c\u54c1\u96c6" />
  <title>{T['name']} \u00b7 {T['portfolio']}</title>
{HEAD}
  <link rel="stylesheet" href="css/styles.css" />
</head>
<body class="is-loading">
  <div class="cursor-glow" aria-hidden="true"></div>
  <nav class="site-nav">
    <div class="inner">
      <a class="brand" href="index.html">XIE YI</a>
      <ul class="nav-links">{NAV_HOME}
      </ul>
    </div>
  </nav>
  <aside class="scroll-progress">
    <a href="#section-about" data-section="about" title="{T['about']}"><span>01 {T['about']}</span></a>
    <a href="#section-product" data-section="product" title="{T['product']}"><span>02 {T['product']}</span></a>
    <a href="#section-ip" data-section="ip" title="IP"><span>03 IP</span></a>
    <a href="#section-scene" data-section="scene" title="{T['scene']}"><span>04 {T['scene']}</span></a>
    <a href="#section-poster" data-section="poster" title="{T['poster']}"><span>05 {T['poster']}</span></a>
  </aside>
  <header class="hero" id="top">
    <div class="hero-media"><img src="assets/hero/hero-bg.jpg" alt="" /></div>
    <div class="hero-overlay" aria-hidden="true"></div>
    <div class="hero-content">
      <p class="hero-eyebrow">Visual Design 2025-2026</p>
      <h1>{T['name']}<br />{T['portfolio']}</h1>
      <p class="hero-desc">\u54c1\u724c\u8bbe\u8ba1\u5e08 \u00b7 IP \u8bbe\u8ba1\u5e08 \u00b7 \u4ea7\u54c1\u573a\u666f\u89c6\u89c9<br />\u4e13\u6ce8 LED \u663e\u793a\u884c\u4e1a\u54c1\u724c\u4f53\u7cfb\u4e0e\u6c89\u6d78\u5f0f\u8425\u9500\u753b\u9762</p>
      <a class="hero-cta" href="#section-about">{T['explore']} <span class="arrow">\u2193</span></a>
    </div>
  </header>
  <main class="works-index">
    <article class="panel" id="section-about" data-section="about">
      <div class="panel-bg"><img src="assets/product/001-01.png" alt="" loading="lazy" /></div>
      <div class="panel-scrim"></div>
      <div class="panel-inner">
        <div class="panel-copy">
          <div class="panel-num">01</div>
          <h2>\u5173\u4e8e\u6211</h2>
          <p>\u6b66\u6c49\u7406\u5de5\u5927\u5b66\u672c\u79d1\uff0c\u73b0\u5c45\u6df1\u5733\u3002\u84dd\u666e\u89c6\u8baf\u54c1\u724c\u89c6\u89c9 / IP \u8bbe\u8ba1\u3002</p>
          <div class="panel-tags"><span>\u54c1\u724c</span><span>IP</span><span>3D</span></div>
          <a class="panel-link" href="works/about.html">\u67e5\u770b\u8be6\u7ec6 \u2192</a>
        </div>
        <a class="panel-link-wrap" href="works/about.html"><div class="panel-preview"><img src="assets/product/banner1.jpg" alt="" loading="lazy" /></div></a>
      </div>
    </article>
    <article class="panel" id="section-product" data-section="product">
      <div class="panel-bg"><img src="assets/product/003-01.png" alt="" loading="lazy" /></div>
      <div class="panel-scrim"></div>
      <div class="panel-inner">
        <div class="panel-copy">
          <div class="panel-num">02</div>
          <h2>\u4ea7\u54c1\u89c6\u89c9</h2>
          <p>LED \u6a21\u7ec4\u3001\u4e00\u4f53\u673a\u3001\u5e7f\u544a\u673a\u4ea7\u54c1\u4e3b\u56fe\u4e0e\u7cfb\u5217\u5316\u6e32\u67d3\u3002</p>
          <div class="panel-tags"><span>\u6e32\u67d3</span><span>KV</span><span>COB</span></div>
          <a class="panel-link" href="works/product.html">\u8fdb\u5165\u4f5c\u54c1 \u2192</a>
        </div>
        <a class="panel-link-wrap" href="works/product.html"><div class="panel-preview"><img src="assets/product/COB3.png" alt="" loading="lazy" /></div></a>
      </div>
    </article>
    <article class="panel" id="section-ip" data-section="ip">
      <div class="panel-bg"><img src="assets/ip/ip-scenario-command-center-led-1.png" alt="" loading="lazy" /></div>
      <div class="panel-scrim"></div>
      <div class="panel-inner">
        <div class="panel-copy">
          <div class="panel-num">03</div>
          <h2>IP \u5f62\u8c61</h2>
          <p>\u5c0f\u84dd\u732b\u89d2\u8272\u573a\u666f\u5ef6\u5c55\u4e0e\u5c55\u4f1a\u5468\u8fb9\u3002</p>
          <div class="panel-tags"><span>IP</span><span>AI</span><span>\u5468\u8fb9</span></div>
          <a class="panel-link" href="works/ip.html">\u8fdb\u5165\u4f5c\u54c1 \u2192</a>
        </div>
        <a class="panel-link-wrap" href="works/ip.html"><div class="panel-preview"><img src="assets/ip/ip-scenario-airport-led-1.png" alt="" loading="lazy" /></div></a>
      </div>
    </article>
    <article class="panel" id="section-scene" data-section="scene">
      <div class="panel-bg"><img src="assets/scene/001-1.png" alt="" loading="lazy" /></div>
      <div class="panel-scrim"></div>
      <div class="panel-inner">
        <div class="panel-copy">
          <div class="panel-num">04</div>
          <h2>\u573a\u666f\u4e0e\u5c55\u89c8</h2>
          <p>\u6307\u6325\u4e2d\u5fc3\u3001\u64ad\u63a7\u3001\u5546\u4e1a\u7a7a\u95f4\u6c99\u76d8\u4e0e\u5c55\u4f1a\u573a\u666f\u3002</p>
          <div class="panel-tags"><span>3D</span><span>\u5c55\u4f1a</span></div>
          <a class="panel-link" href="works/scene.html">\u8fdb\u5165\u4f5c\u54c1 \u2192</a>
        </div>
        <a class="panel-link-wrap" href="works/scene.html"><div class="panel-preview"><img src="assets/scene/002-1.png" alt="" loading="lazy" /></div></a>
      </div>
    </article>
    <article class="panel" id="section-poster" data-section="poster">
      <div class="panel-bg"><img src="assets/poster/Banner(1920x1080).jpg" alt="" loading="lazy" /></div>
      <div class="panel-scrim"></div>
      <div class="panel-inner">
        <div class="panel-copy">
          <div class="panel-num">05</div>
          <h2>\u54c1\u724c\u5e73\u9762</h2>
          <p>Banner\u3001\u9080\u8bf7\u51fd\u3001\u793e\u5a92\u4e0e\u5c55\u4f1a\u9884\u544a\u7269\u6599\u3002</p>
          <div class="panel-tags"><span>KV</span><span>\u793e\u5a92</span></div>
          <a class="panel-link" href="works/poster.html">\u8fdb\u5165\u4f5c\u54c1 \u2192</a>
        </div>
        <a class="panel-link-wrap" href="works/poster.html"><div class="panel-preview"><img src="assets/poster/Banner(1080x1440).jpg" alt="" loading="lazy" /></div></a>
      </div>
    </article>
  </main>
  <footer class="site-footer">
    <p>&copy; 2026 {T['name']}<br /><a href="mailto:623797004@qq.com">623797004@qq.com</a></p>
  </footer>
  <script src="js/app.js"></script>
</body>
</html>""",
)

work_page(
    "product.html",
    "\u4ea7\u54c1\u89c6\u89c9",
    "02 \u00b7 Product",
    "\u4ea7\u54c1\u89c6\u89c9",
    "LED \u4ea7\u54c1\u4e3b\u56fe\u4e0e\u6e32\u67d3\u3002",
    "section-product",
    "\n".join(
        [
            fig("../assets/product/banner1.jpg", "Banner"),
            fig("../assets/product/001-01.png", "KV 001"),
            fig("../assets/product/003-01.png", "KV 003"),
            fig("../assets/product/COB3.png", "COB"),
            fig("../assets/product/01-1.png", "Render"),
        ]
    ),
    "\n".join(
        [
            mimg("../assets/product/banner1.jpg"),
            mimg("../assets/product/001-01.png"),
            mimg("../assets/product/COB3.png"),
            mimg("../assets/product/02-1.png"),
        ]
    ),
)

work_page(
    "ip.html",
    "IP \u5f62\u8c61",
    "03 \u00b7 IP",
    "IP \u5f62\u8c61",
    "\u5c0f\u84dd\u732b\u573a\u666f\u4e0e\u5468\u8fb9\u5ef6\u5c55\u3002",
    "section-ip",
    "\n".join(
        [
            fig("../assets/ip/ip-scenario-airport-led-1.png", "\u673a\u573a"),
            fig("../assets/ip/ip-scenario-command-center-led-1.png", "\u6307\u6325\u4e2d\u5fc3"),
            fig("../assets/ip/ip-scenario-classroom-led-1.png", "\u6559\u5ba4"),
            fig("../assets/ip/ip-scenario-broadcast-studio-led-1.png", "\u64ad\u63a7"),
            fig("../assets/ip/ip-merch-mascot-exhibition-booth-5.png", "\u5c55\u4f1a"),
        ]
    ),
    "\n".join(
        [
            mimg("../assets/ip/ip-scenario-airport-led-1.png"),
            mimg("../assets/ip/ip-scenario-command-center-led-1.png"),
            mimg("../assets/ip/ip-merch-tote-exhibition-swag-1.png"),
            mimg("../assets/ip/ip-merch-figurine-office-desk-1.png"),
        ]
    ),
)

work_page(
    "scene.html",
    "\u573a\u666f\u4e0e\u5c55\u89c8",
    "04 \u00b7 Scene",
    "\u573a\u666f\u4e0e\u5c55\u89c8",
    "\u7a7a\u95f4\u6c99\u76d8\u4e0e\u5c55\u4f1a\u573a\u666f\u3002",
    "section-scene",
    "\n".join(
        [
            fig("../assets/scene/001-1.png", "001"),
            fig("../assets/scene/002-1.png", "002"),
            fig("../assets/scene/003.png", "003"),
            fig("../assets/scene/004.png", "004"),
        ]
    ),
    "\n".join(
        [
            mimg("../assets/scene/001-1.png"),
            mimg("../assets/scene/002-1.png"),
            mimg("../assets/scene/003.png"),
            mimg("../assets/scene/004.png"),
        ]
    ),
)

work_page(
    "poster.html",
    "\u54c1\u724c\u5e73\u9762",
    "05 \u00b7 Poster",
    "\u54c1\u724c\u5e73\u9762",
    "Banner \u4e0e\u6e20\u9053\u7269\u6599\u3002",
    "section-poster",
    "\n".join(
        [
            fig("../assets/poster/Banner(1920x1080).jpg", "1920x1080"),
            fig("../assets/poster/Banner(1080x1440).jpg", "1080x1440"),
            fig("../assets/poster/Banner(1080x1440)2.jpg", "1080x1440-2"),
            fig("../assets/poster/banner en.jpg", "EN"),
        ]
    ),
    "\n".join(
        [
            mimg("../assets/poster/Banner(1920x1080).jpg"),
            mimg("../assets/poster/Banner(1080x1440).jpg"),
        ]
    ),
)

about_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>\u5173\u4e8e\u6211 \u00b7 {T['name']}</title>
{HEAD}
  <link rel="stylesheet" href="../css/styles.css" />
  <style>
    .about-grid {{ max-width: var(--max); margin: 0 auto; padding: 0 24px 80px; display: grid; gap: 24px; }}
    @media (min-width: 800px) {{ .about-grid {{ grid-template-columns: 1fr 1fr; }} }}
    .about-card {{ background: var(--bg-elevated); border: 1px solid rgba(255,255,255,0.08); border-radius: var(--radius); padding: 28px 32px; }}
    .about-card h2 {{ font-family: Syne, sans-serif; font-size: 18px; color: var(--accent-a); margin-bottom: 12px; }}
    .about-card p, .about-card li {{ font-size: 15px; color: var(--text-muted); line-height: 1.7; }}
    .about-card ul {{ padding-left: 18px; }}
    .about-card a {{ color: var(--accent-b); }}
  </style>
</head>
<body>
  <div class="cursor-glow" aria-hidden="true"></div>
  <nav class="site-nav scrolled"><div class="inner">
    <a class="brand" href="../index.html">XIE YI</a>
    <ul class="nav-links">{NAV_WORK}</ul>
  </div></nav>
  <header class="work-hero">
    <a class="back" href="../index.html#section-about">{T['back_home']}</a>
    <p class="label">01 \u00b7 About</p>
    <h1>\u5173\u4e8e\u6211</h1>
    <p>{T['name']} \u2014 \u54c1\u724c / IP \u8bbe\u8ba1\u5e08</p>
  </header>
  <div class="about-grid">
    <article class="about-card"><h2>\u7ecf\u5386</h2><p>\u6b66\u6c49\u7406\u5de5\u5927\u5b66 \u00b7 \u8ba1\u7b97\u673a\u79d1\u5b66\u4e0e\u6280\u672f</p><p style="margin-top:12px">LPDISPLAY \u54c1\u724c\u89c6\u89c9 / IP</p></article>
    <article class="about-card"><h2>\u80fd\u529b</h2><ul><li>\u54c1\u724c\u89c6\u89c9</li><li>IP \u89d2\u8272</li><li>\u4ea7\u54c1\u6e32\u67d3</li><li>3D \u573a\u666f</li></ul></article>
    <article class="about-card"><h2>\u8054\u7cfb</h2><p><a href="tel:+8615899782952">+86 158 9978 2952</a><br /><a href="mailto:623797004@qq.com">623797004@qq.com</a></p></article>
    <article class="about-card"><h2>\u4f5c\u54c1</h2><ul>
      <li><a href="product.html">\u4ea7\u54c1\u89c6\u89c9</a></li>
      <li><a href="ip.html">IP</a></li>
      <li><a href="scene.html">\u573a\u666f</a></li>
      <li><a href="poster.html">\u5e73\u9762</a></li>
    </ul></article>
  </div>
  <footer class="site-footer"><p><a href="../index.html">{T['back_index']}</a></p></footer>
  <script src="../js/app.js"></script>
</body>
</html>"""
save(W / "about.html", about_html)

print("generated OK")
