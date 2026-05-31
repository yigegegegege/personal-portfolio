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

- `index.html` - Home: 5 full-screen sections with links to detail pages
- `works/*.html` - Detail pages per section
- `assets/` - Images copied from chanpinshengtu and IP AI folders
- `css/styles.css` / `js/app.js` - Styles and interactions
- `gen.py` - Regenerate HTML (UTF-8) after asset changes

## Sections

1. About - `works/about.html`
2. Product visuals - `works/product.html`
3. IP character - `works/ip.html`
4. Scenes and exhibitions - `works/scene.html`
5. Brand graphics - `works/poster.html`
