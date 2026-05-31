(function () {
  "use strict";

  const nav = document.querySelector(".site-nav");
  const panels = document.querySelectorAll(".panel[data-section]");
  const progressLinks = document.querySelectorAll(".scroll-progress a");
  const revealItems = document.querySelectorAll(
    ".panel, .gallery-card, .masonry-item, .collection-head"
  );

  /* Nav background on scroll */
  function onScroll() {
    if (nav) {
      nav.classList.toggle("scrolled", window.scrollY > 40);
    }
    updateActiveSection();
  }

  /* Section spy for side dots + nav */
  function updateActiveSection() {
    let current = "";
    panels.forEach((panel) => {
      const rect = panel.getBoundingClientRect();
      if (rect.top <= window.innerHeight * 0.45 && rect.bottom >= window.innerHeight * 0.25) {
        current = panel.dataset.section || "";
      }
    });

    document.querySelectorAll(".nav-links a[data-section]").forEach((a) => {
      a.classList.toggle("active", a.dataset.section === current);
    });
    progressLinks.forEach((a) => {
      a.classList.toggle("active", a.dataset.section === current);
    });
  }

  /* Intersection reveal */
  const io = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("in-view", "visible");
        }
      });
    },
    { threshold: 0.15, rootMargin: "0px 0px -8% 0px" }
  );

  revealItems.forEach((el) => io.observe(el));

  /* Parallax on panel backgrounds */
  let ticking = false;
  function parallax() {
    panels.forEach((panel) => {
      const bg = panel.querySelector(".panel-bg");
      if (!bg) return;
      const rect = panel.getBoundingClientRect();
      const center = rect.top + rect.height / 2 - window.innerHeight / 2;
      const offset = center * 0.06;
      bg.style.transform = `translateY(${offset}px) scale(1.05)`;
    });
    ticking = false;
  }

  window.addEventListener(
    "scroll",
    () => {
      onScroll();
      if (!ticking) {
        requestAnimationFrame(parallax);
        ticking = true;
      }
    },
    { passive: true }
  );

  onScroll();
  parallax();

  /* Cursor ambient glow */
  const glow = document.querySelector(".cursor-glow");
  if (glow && window.matchMedia("(pointer: fine)").matches) {
    document.body.classList.add("has-pointer");
    window.addEventListener(
      "mousemove",
      (e) => {
        glow.style.left = e.clientX + "px";
        glow.style.top = e.clientY + "px";
      },
      { passive: true }
    );
  }

  /* Horizontal gallery drag-scroll hint */
  document.querySelectorAll(".horizontal-scroll").forEach((strip) => {
    let isDown = false;
    let startX;
    let scrollLeft;

    strip.addEventListener("mousedown", (e) => {
      isDown = true;
      startX = e.pageX - strip.offsetLeft;
      scrollLeft = strip.scrollLeft;
      strip.style.cursor = "grabbing";
    });
    strip.addEventListener("mouseleave", () => {
      isDown = false;
      strip.style.cursor = "";
    });
    strip.addEventListener("mouseup", () => {
      isDown = false;
      strip.style.cursor = "";
    });
    strip.addEventListener("mousemove", (e) => {
      if (!isDown) return;
      e.preventDefault();
      const x = e.pageX - strip.offsetLeft;
      strip.scrollLeft = scrollLeft - (x - startX) * 1.2;
    });
  });

  /* Gallery card — hover to preview full image (work subpages) */
  function initGalleryHoverPreview() {
    const cards = document.querySelectorAll(
      ".gallery-card:not(.gallery-card--sticker):not(.gallery-card--motion)"
    );
    if (!cards.length || !window.matchMedia("(pointer: fine)").matches) return;

    const preview = document.createElement("div");
    preview.className = "img-hover-preview";
    preview.setAttribute("role", "tooltip");
    preview.setAttribute("aria-hidden", "true");
    preview.innerHTML =
      '<img alt="" decoding="async" />' +
      '<p class="img-hover-preview__caption"></p>';
    document.body.appendChild(preview);

    const previewImg = preview.querySelector("img");
    const previewCaption = preview.querySelector(".img-hover-preview__caption");
    let activeCard = null;
    let hideTimer = null;

    function positionPreview(clientX, clientY) {
      const pad = 16;
      const gap = 20;
      const rect = preview.getBoundingClientRect();
      let x = clientX + gap;
      let y = clientY + gap;

      if (x + rect.width > window.innerWidth - pad) {
        x = clientX - rect.width - gap;
      }
      if (y + rect.height > window.innerHeight - pad) {
        y = clientY - rect.height - gap;
      }

      preview.style.left = Math.max(pad, x) + "px";
      preview.style.top = Math.max(pad, y) + "px";
    }

    function show(card, e) {
      const img = card.querySelector("img");
      if (!img) return;

      clearTimeout(hideTimer);
      if (activeCard && activeCard !== card) {
        activeCard.classList.remove("is-preview-active");
      }

      activeCard = card;
      card.classList.add("is-preview-active");

      const caption = card.querySelector("figcaption");
      previewCaption.textContent = caption ? caption.textContent.trim() : "";
      previewImg.alt = img.alt || "";

      const src = img.currentSrc || img.src;
      if (previewImg.getAttribute("data-src") !== src) {
        previewImg.setAttribute("data-src", src);
        previewImg.src = src;
        previewImg.onload = () => {
          if (activeCard === card) positionPreview(e.clientX, e.clientY);
        };
      }

      preview.classList.add("is-visible");
      preview.setAttribute("aria-hidden", "false");
      requestAnimationFrame(() => positionPreview(e.clientX, e.clientY));
    }

    function hide() {
      hideTimer = setTimeout(() => {
        preview.classList.remove("is-visible");
        preview.setAttribute("aria-hidden", "true");
        if (activeCard) {
          activeCard.classList.remove("is-preview-active");
          activeCard = null;
        }
      }, 40);
    }

    cards.forEach((card) => {
      card.addEventListener("mouseenter", (e) => show(card, e));
      card.addEventListener("mousemove", (e) => {
        if (activeCard === card) positionPreview(e.clientX, e.clientY);
      });
      card.addEventListener("mouseleave", hide);
    });
  }

  initGalleryHoverPreview();

  document.body.classList.remove("is-loading");
})();
