(function () {
  "use strict";

  const STORAGE_KEY = "portfolio-lang";
  const DEFAULT_LANG = "zh";

  function getDict() {
    return window.I18N_DATA || { strings: {}, titles: {}, meta: {} };
  }

  function getLang() {
    const saved = localStorage.getItem(STORAGE_KEY);
    return saved === "en" ? "en" : DEFAULT_LANG;
  }

  function setLang(lang) {
    localStorage.setItem(STORAGE_KEY, lang === "en" ? "en" : "zh");
  }

  function applyToElement(el, lang) {
    const dict = getDict();
    const key = el.getAttribute("data-i18n");
    if (!key) return;

    const entry = dict.strings[key];
    if (!entry) return;

    const value = entry[lang] || entry.zh || "";
    if (el.hasAttribute("data-i18n-html")) {
      el.innerHTML = value;
    } else {
      el.textContent = value;
    }
  }

  function applyAltAttributes(lang) {
    const dict = getDict();
    document.querySelectorAll("[data-i18n-alt]").forEach((el) => {
      const key = el.getAttribute("data-i18n-alt");
      const entry = dict.strings[key];
      if (entry) el.setAttribute("alt", entry[lang] || entry.zh || "");
    });
  }

  function applyTitle(lang) {
    const dict = getDict();
    const page = document.body.dataset.i18nPage;
    if (!page || !dict.titles[page]) return;
    document.title = dict.titles[page][lang] || dict.titles[page].zh;
  }

  function applyMeta(lang) {
    const dict = getDict();
    const page = document.body.dataset.i18nPage;
    if (!page || !dict.meta[page]) return;
    const meta = dict.meta[page][lang] || dict.meta[page].zh;
    if (!meta) return;
    const desc = document.querySelector('meta[name="description"]');
    if (desc && meta.description) desc.setAttribute("content", meta.description);
    const ogTitle = document.querySelector('meta[property="og:title"]');
    if (ogTitle && meta.ogTitle) ogTitle.setAttribute("content", meta.ogTitle);
    const ogDesc = document.querySelector('meta[property="og:description"]');
    if (ogDesc && meta.ogDescription) ogDesc.setAttribute("content", meta.ogDescription);
  }

  function applyLanguage(lang) {
    document.documentElement.lang = lang === "en" ? "en" : "zh-CN";
    document.body.classList.toggle("lang-en", lang === "en");
    document.body.classList.toggle("lang-zh", lang !== "en");

    document.querySelectorAll("[data-i18n]").forEach((el) => applyToElement(el, lang));
    applyAltAttributes(lang);
    applyTitle(lang);
    applyMeta(lang);

    const toggle = document.getElementById("lang-toggle");
    if (toggle) {
      toggle.textContent = lang === "en" ? "中文" : "EN";
      toggle.setAttribute("aria-label", lang === "en" ? "Switch to Chinese" : "Switch to English");
      toggle.setAttribute("title", lang === "en" ? "切换中文" : "Switch to English");
    }
  }

  function initToggle() {
    const toggle = document.getElementById("lang-toggle");
    if (!toggle) return;
    toggle.addEventListener("click", () => {
      const next = getLang() === "en" ? "zh" : "en";
      setLang(next);
      applyLanguage(next);
    });
  }

  window.PortfolioI18n = {
    applyLanguage,
    getLang,
    setLang,
  };

  document.addEventListener("DOMContentLoaded", () => {
    initToggle();
    applyLanguage(getLang());
  });
})();
