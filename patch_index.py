# -*- coding: utf-8 -*-
from pathlib import Path

B = Path(__file__).resolve().parent

html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="description" content="TOM XIE \u2014 \u54c1\u724c\u4e0e\u4ea7\u54c1\u89c6\u89c9\u8bbe\u8ba1\u5e08\u4e2a\u4eba\u4f5c\u54c1\u96c6" />
  <title>TOM XIE \u00b7 \u4e2a\u4eba\u4f5c\u54c1\u96c6</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;600&family=Syne:wght@600;700;800&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="css/styles.css" />
</head>
<body class="is-loading">
  <div class="cursor-glow" aria-hidden="true"></div>
  <nav class="site-nav">
    <div class="inner">
      <a class="brand" href="index.html">TOM XIE</a>
      <ul class="nav-links">
        <li><a href="#section-about" data-section="about">\u5173\u4e8e</a></li>
        <li><a href="#section-product" data-section="product">\u4ea7\u54c1\u6e32\u67d3</a></li>
        <li><a href="#section-ip" data-section="ip">IP\u8bbe\u8ba1</a></li>
        <li><a href="#section-scene" data-section="scene">\u573a\u666f\u6e32\u67d3</a></li>
        <li><a href="#section-poster" data-section="poster">\u54c1\u724c\u5e73\u9762</a></li>
        <li><a href="#section-other" data-section="other">\u5176\u4ed6</a></li>
        <li><a href="#section-contact" data-section="contact">\u8054\u7cfb</a></li>
      </ul>
    </div>
  </nav>
  <aside class="scroll-progress">
    <a href="#section-about" data-section="about"><span>01 \u5173\u4e8e</span></a>
    <a href="#section-product" data-section="product"><span>02 \u4ea7\u54c1</span></a>
    <a href="#section-ip" data-section="ip"><span>03 IP</span></a>
    <a href="#section-scene" data-section="scene"><span>04 \u573a\u666f</span></a>
    <a href="#section-poster" data-section="poster"><span>05 \u5e73\u9762</span></a>
    <a href="#section-other" data-section="other"><span>06 \u5176\u4ed6</span></a>
    <a href="#section-contact" data-section="contact"><span>07 \u8054\u7cfb</span></a>
  </aside>
  <header class="hero" id="top">
    <div class="hero-media"><img src="assets/hero/hero-bg.jpg" alt="" /></div>
    <div class="hero-overlay" aria-hidden="true"></div>
    <div class="hero-content">
      <p class="hero-eyebrow">Visual Design 2026</p>
      <h1>TOM XIE<br />\u4e2a\u4eba\u4f5c\u54c1\u96c6</h1>
      <p class="hero-desc">\u54c1\u724c\u8bbe\u8ba1\u5e08 \u00b7 IP \u8bbe\u8ba1\u5e08 \u00b7 3D\u89c6\u89c9\u8bbe\u8ba1\u5e08</p>
      <a class="hero-cta" href="#section-about">\u63a2\u7d22\u6211\u7684\u4f5c\u54c1 <span class="arrow">\u2193</span></a>
    </div>
  </header>
  <main class="works-index">
    <article class="panel" id="section-about" data-section="about">
      <div class="panel-bg"><img src="assets/product/001-01.png" alt="" loading="lazy" /></div>
      <div class="panel-scrim"></div>
      <div class="panel-inner">
        <div class="panel-copy">
          <div class="panel-num">01</div>
          <h2>\u5173\u4e8e TOM</h2>
          <p>\u62e5\u6709 5 \u5e74+ \u5168\u94fe\u8def\u54c1\u724c\u89c6\u89c9\u8bbe\u8ba1\u7ecf\u9a8c\uff0c\u64c5\u957f\u4ece 0 \u5230 1 \u6784\u5efa\u54c1\u724c\u89c6\u89c9\u8bc6\u522b\u7cfb\u7edf\uff08VI\uff09\u3001\u6253\u9020\u9ad8\u8fa8\u8bc6\u5ea6 IP \u5f62\u8c61\u53ca\u843d\u5730\u5546\u4e1a\u5316\u5e94\u7528\u3002\u7cbe\u901a 3D \u6e32\u67d3\u4e0e\u573a\u666f\u642d\u5efa\uff0c\u5177\u5907 MG/CG \u4e0e UI/UX \u80fd\u529b\u3002</p>
          <div class="panel-tags"><span>\u54c1\u724c\u89c6\u89c9</span><span>IP\u8bbe\u8ba1</span><span>3D\u89c6\u89c9</span></div>
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
    <article class="panel" id="section-other" data-section="other">
      <div class="panel-bg"><img src="assets/product/banner2.jpg" alt="" loading="lazy" /></div>
      <div class="panel-scrim"></div>
      <div class="panel-inner">
        <div class="panel-copy">
          <div class="panel-num">06</div>
          <h2>\u5176\u4ed6\u4f5c\u54c1</h2>
          <p>MG \u52a8\u6548\u3001UI \u754c\u9762\u3001\u793e\u5a92\u8fd0\u8425\u56fe\u3001\u6d3b\u52a8\u4e3b\u89c6\u89c9\u7b49\u8de8\u5a92\u4ecb\u8bbe\u8ba1\u3002</p>
          <div class="panel-tags"><span>\u52a8\u6548</span><span>UI</span><span>\u793e\u5a92</span></div>
          <a class="panel-link" href="works/other.html">\u8fdb\u5165\u4f5c\u54c1 \u2192</a>
        </div>
        <a class="panel-link-wrap" href="works/other.html">
          <div class="panel-preview"><img src="assets/product/004-01.png" alt="" loading="lazy" /></div>
        </a>
      </div>
    </article>
    <article class="panel panel-contact" id="section-contact" data-section="contact">
      <div class="panel-scrim panel-scrim--soft" aria-hidden="true"></div>
      <div class="panel-inner panel-inner--contact">
        <div class="panel-copy panel-copy--center">
          <div class="panel-num">07</div>
          <h2>\u8054\u7cfb\u6211</h2>
          <p>\u6b22\u8fce\u54c1\u724c\u5408\u4f5c\u3001\u5168\u804c\u673a\u4f1a\u6216\u9879\u76ee\u54a8\u8be2\uff0c\u901a\u5e38\u4f1a\u5728 24 \u5c0f\u65f6\u5185\u56de\u590d\u3002</p>
        </div>
        <div class="contact-cards">
          <a class="contact-card" href="tel:+8615899782952">
            <span class="contact-card__icon" aria-hidden="true">\u260e</span>
            <span class="contact-card__label">\u7535\u8bdd / \u5fae\u4fe1</span>
            <span class="contact-card__value">+86 158 9978 2952</span>
            <span class="contact-card__hint">\u5fae\u4fe1\u540c\u53f7\uff0c\u6dfb\u52a0\u8bf7\u6ce8\u660e\u6765\u610f</span>
          </a>
          <a class="contact-card" href="mailto:623797004@qq.com">
            <span class="contact-card__icon" aria-hidden="true">\u2709</span>
            <span class="contact-card__label">\u90ae\u7bb1</span>
            <span class="contact-card__value">623797004@qq.com</span>
            <span class="contact-card__hint">\u5982\u9700\u8fdb\u4e00\u6b65\u4e86\u89e3\uff0c\u6b22\u8fce\u90ae\u4ef6\u8054\u7cfb\uff0c\u6211\u53ef\u63d0\u4f9b\u5b8c\u6574\u7b80\u5386\u4e0e\u4f5c\u54c1\u96c6</span>
          </a>
        </div>
      </div>
    </article>
  </main>
  <footer class="site-footer">
    <p>&copy; 2026 TOM XIE \u00b7 \u4e2a\u4eba\u4f5c\u54c1\u96c6</p>
  </footer>
  <script src="js/app.js"></script>
</body>
</html>
"""

(B / "index.html").write_text(html, encoding="utf-8", newline="\n")
print("patched index.html OK")
