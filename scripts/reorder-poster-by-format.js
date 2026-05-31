const fs = require("fs");
const path = require("path");

const webRoot = path.join(__dirname, "..");
const posterHtml = path.join(webRoot, "works", "poster.html");

function pngSize(buf) {
  return { w: buf.readUInt32BE(16), h: buf.readUInt32BE(20) };
}

function jpegSize(buf) {
  let i = 2;
  while (i < buf.length) {
    if (buf[i] !== 0xff) {
      i++;
      continue;
    }
    const m = buf[i + 1];
    if (m === 0xc0 || m === 0xc2) {
      return { w: buf.readUInt16BE(i + 7), h: buf.readUInt16BE(i + 5) };
    }
    i += 2 + buf.readUInt16BE(i + 2);
  }
  return { w: 0, h: 0 };
}

function dims(absPath) {
  const buf = fs.readFileSync(absPath);
  if (buf[0] === 0x89) return pngSize(buf);
  if (buf[0] === 0xff && buf[1] === 0xd8) return jpegSize(buf);
  return { w: 0, h: 0 };
}

function orientIndex(ratio) {
  if (ratio > 1.05) return 0;
  if (ratio < 0.95) return 2;
  return 1;
}

function lpSocialPriority(base) {
  const n = parseInt(base, 10) || 99;
  if (/sls-2025/.test(base)) return [1, n];
  if (/ise-2026-countdown/.test(base)) return [2, n];
  if (/ise-2024-countdown|ise-2024-thin/.test(base)) return [3, n];
  if (/ise-2025-countdown/.test(base)) return [4, n];
  if (/ise-2026-promo|ise-2026-invitation/.test(base)) return [5, n];
  if (/european-office|lp-social-extra/.test(base)) return [6, n];
  if (/lampsi|airport-expo|follow-us|lp-support/.test(base)) return [7, n];
  return [8, n];
}

function productPagePriority(base) {
  if (base.includes("la-series-rental")) return [2, base];
  if (base.includes("firefly")) return [1, base];
  if (base.includes("la-series-special")) return [4, base];
  return [3, base];
}

function sortKey(file, collectionId) {
  const rel = file.replace(/^\.\.\//, "");
  const abs = path.join(webRoot, rel);
  const d = dims(abs);
  const ratio = d.w / d.h;
  const base = path.basename(rel).toLowerCase();

  if (collectionId === "col-vi") {
    if (/brochure|corp-brochure/.test(base)) return [0, ratio, file];
    if (/lpdisplay-vis|vis-/.test(base)) return [1, ratio, file];
    if (/business-card/.test(base)) return [2, ratio, file];
    if (/uniform/.test(base)) return [3, ratio, file];
    return [9, ratio, file];
  }
  if (collectionId === "col-product-page") {
    return productPagePriority(base).concat([file]);
  }
  if (collectionId === "social-lpdisplay") {
    const o = orientIndex(ratio);
    if (o === 2) return [2, lpSocialPriority(base)[0], lpSocialPriority(base)[1], file];
    return [1, lpSocialPriority(base)[0], lpSocialPriority(base)[1], file];
  }
  if (collectionId === "social-vod") {
    const o = orientIndex(ratio);
    if (o === 2) return [2, ratio, file];
    if (o === 0) return [0, ratio, file];
    const n = parseInt(base, 10) || 99;
    return [1, n, file];
  }
  if (collectionId === "col-banner") {
    const isVod = base.startsWith("vod-");
    return [isVod ? 1 : 0, ratio, file];
  }

  return [orientIndex(ratio), ratio, file];
}

function cardHtml(src, alt) {
  const a = alt ? ` alt="${alt.replace(/"/g, "&quot;")}"` : ' alt=""';
  const cap = alt
    ? `<figcaption>${alt.replace(/</g, "&lt;")}</figcaption>`
    : "";
  return `          <figure class="gallery-card"><img src="${src}"${a} loading="lazy" />${cap}</figure>`;
}

let html = fs.readFileSync(posterHtml, "utf8");

const stripRe =
  /(<section class="gallery-strip"[^>]*>\s*<div class="horizontal-scroll">)([\s\S]*?)(<\/div>\s*<\/section>)/g;

let stripIndex = 0;
const collectionOrder = [
  "col-vi",
  "col-product-page",
  "col-banner",
  "social-lpdisplay",
  "social-vod",
  "col-logo",
  "col-icon",
];

html = html.replace(stripRe, (match, open, inner, close) => {
  const collectionId = collectionOrder[stripIndex] || "other";
  stripIndex++;

  const cardRe =
    /<figure class="gallery-card"><img src="([^"]+)"([^>]*)>(?:<\/img>)?(?:<figcaption>[^<]*<\/figcaption>)?<\/figure>/g;
  const cards = [];
  let m;
  while ((m = cardRe.exec(inner)) !== null) {
    const src = m[1];
    const attrs = m[2];
    const altM = attrs.match(/alt="([^"]*)"/);
    cards.push({ src, alt: altM ? altM[1] : "" });
  }

  if (!cards.length) return match;

  cards.sort((a, b) => {
    const ka = sortKey(a.src, collectionId);
    const kb = sortKey(b.src, collectionId);
    for (let i = 0; i < Math.max(ka.length, kb.length); i++) {
      if (ka[i] < kb[i]) return -1;
      if (ka[i] > kb[i]) return 1;
    }
    return 0;
  });

  const body = cards.map((c) => cardHtml(c.src, c.alt)).join("\n");
  return `${open}\n${body}\n        ${close}`;
});

fs.writeFileSync(posterHtml, html, "utf8");
console.log("Reordered", stripIndex, "gallery strips in poster.html");
