# Personal Portfolio Web

Output folder for the portfolio site.

## Open

Double-click `index.html`, or run:

```bash
cd web
python -m http.server 8080
```

Then open http://localhost:8080

## Structure

- `index.html` - Home: 6 full-screen sections (no「更多探索」)
- `works/*.html` - Detail pages per section (JD-curated galleries)
- `assets/` - Images copied from chanpinshengtu and IP AI folders
- `css/styles.css` / `js/app.js` - Styles and interactions
- `gen.py` - Regenerate HTML (UTF-8) after asset changes
- `apply_jd_curate.py` - Re-apply Insta360 JD gallery curation after manual HTML edits
- `sync_nav_insta.py` - Sync unified navigation across all HTML pages
- `scripts/find_unused_assets.py` / `scripts/cleanup_unused.py` - Audit and remove unreferenced assets

## Sections (Insta360 视觉设计师导向)

1. Brand visual - `works/poster.html`（ISE 案例 / VI / KV / 展会社媒）
2. Product visual - `works/product.html`（跨境电商优先 + LED / XR）
3. IP - `works/ip.html`（小蓝猫规范 / 场景 / 周边）
4. AIGC - `works/aigc.html`（中枢 ×1 + IP ×5 + 电商 ×5 + 质检 ×1 / 前后对比 / 合规）
5. Scene 3D - `works/scene.html`（解决方案 / 展会 / 项目）
6. About - `works/about.html`
7. Contact - on `index.html`

Generated assets live under `assets/aigc/`, `assets/poster/case-study/`, `assets/product/ecom/main/`, `assets/photo/`.

Removed: `works/other.html` and `assets/other/`（动效 / 插画 / 字体练习等与 JD 弱相关）
