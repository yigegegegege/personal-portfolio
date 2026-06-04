# -*- coding: utf-8 -*-
"""Inject data-i18n tags and generate js/i18n-data.js."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORKS = ROOT / "works"

# slug -> {zh, en}
STRINGS: dict[str, dict[str, str]] = {
    # Shared nav & contact
    "nav.brandVisual": {"zh": "品牌视觉", "en": "Brand Visual"},
    "nav.productVisual": {"zh": "产品视觉", "en": "Product Visual"},
    "nav.ipDesign": {"zh": "IP 设计", "en": "IP Design"},
    "nav.aigc": {"zh": "AIGC", "en": "AIGC"},
    "nav.scene3d": {"zh": "场景 3D", "en": "Scene 3D"},
    "nav.about": {"zh": "关于", "en": "About"},
    "nav.contact": {"zh": "联系", "en": "Contact"},
    "nav.contactLead": {
        "zh": "欢迎视觉设计相关合作，通常 24 小时内回复。",
        "en": "Open to visual design collaborations — I usually reply within 24 hours.",
    },
    "nav.phoneWechat": {"zh": "电话 / 微信", "en": "Phone / WeChat"},
    "nav.email": {"zh": "邮箱", "en": "Email"},
    "common.backHome": {"zh": "← 返回首页", "en": "← Back to Home"},
    "common.backPortfolio": {"zh": "← 返回作品集首页", "en": "← Back to Portfolio"},
    "common.viewWork": {"zh": "进入作品", "en": "View Work"},
    "common.learnMore": {"zh": "了解更多", "en": "Learn More"},
    "common.viewLarge": {"zh": "查看大图", "en": "View Full Size"},
    "common.collection": {"zh": "选集", "en": "Collection"},
    "common.featured": {"zh": "精选素材", "en": "Featured"},
    # Home
    "home.heroEyebrow": {
        "zh": "视觉设计师 · 品牌视觉 / 新品上市 · 深圳",
        "en": "Visual Designer · Brand / Product Launch · Shenzhen",
    },
    "home.heroTitle": {
        "zh": "品牌与产品<em>视觉</em>",
        "en": "Brand & Product <em>Visual</em>",
    },
    "home.heroDesc": {
        "zh": "主 KV · 跨境电商详情 · VIS 与 IP · AIGC 审稿工作流",
        "en": "Key Visuals · Cross-border E-commerce · VIS & IP · AIGC Review Workflow",
    },
    "home.heroBrowse": {"zh": "浏览作品", "en": "Browse Work"},
    "home.heroAbout": {"zh": "关于我", "en": "About Me"},
    "home.panelBrandTitle": {"zh": "品牌视觉", "en": "Brand Visual"},
    "home.panelBrandLead": {
        "zh": "新品主 KV · VI 手册 · 国际展会与跨境社媒",
        "en": "Launch KV · VI Manual · Trade Shows & Cross-border Social",
    },
    "home.panelProductTitle": {"zh": "产品视觉", "en": "Product Visual"},
    "home.panelProductLead": {
        "zh": "亚马逊 / 国际站主图与详情 · 产品渲染与 XR 方案",
        "en": "Amazon / Intl. listings · Product renders & XR solutions",
    },
    "home.panelIpTitle": {"zh": "IP 设计", "en": "IP Design"},
    "home.panelIpLead": {
        "zh": "小蓝猫 XIAOLANMAO · 规范 · 社媒与周边落地",
        "en": "XIAOLANMAO · Guidelines · Social & Merch Rollout",
    },
    "home.panelAigcTitle": {"zh": "AIGC 工作流", "en": "AIGC Workflow"},
    "home.panelAigcLead": {
        "zh": "星型审稿中枢 · IP 双引擎 · 电商三泳道 · 上线质检",
        "en": "PS review hub · Dual IP engines · E-com lanes · QC gate",
    },
    "home.panelSceneTitle": {"zh": "场景 3D", "en": "Scene 3D"},
    "home.panelSceneLead": {
        "zh": "解决方案场景 · 展会展台 · 项目案例渲染",
        "en": "Solution scenes · Exhibition booths · Project renders",
    },
    "home.panelAboutTitle": {"zh": "关于我", "en": "About Me"},
    "home.panelAboutLead": {
        "zh": "5 年品牌视觉 · 跨部门落地 · 求职意向与代表项目",
        "en": "5 yrs brand visual · Cross-functional delivery · Selected projects",
    },
    "home.footer": {
        "zh": "© 2026 谢意 TOM XIE · Visual Designer · 深圳",
        "en": "© 2026 Xie Yi TOM XIE · Visual Designer · Shenzhen",
    },
    # About page
    "about.subtitle": {
        "zh": "谢意 · 视觉设计师 · 品牌视觉 / 新品上市视觉",
        "en": "Xie Yi · Visual Designer · Brand & Product Launch Visual",
    },
    "about.introTitle": {"zh": "个人简介", "en": "Profile"},
    "about.intro1": {
        "zh": "5 年品牌视觉（蓝普视讯 2021.06 至今），专注<strong style=\"color: var(--text); font-weight: 600;\">新品与产品线上市视觉</strong>、品牌 VIS 与 IP 规范落地。作品集建议浏览顺序：<a href=\"../index.html#section-poster\">品牌</a> → <a href=\"../index.html#section-product\">产品</a> → <a href=\"../index.html#section-ip\">IP</a> → <a href=\"../index.html#section-aigc\">AIGC</a>。",
        "en": "5 years in brand visual (LPDISPLAY, since Jun 2021), focused on <strong style=\"color: var(--text); font-weight: 600;\">product launch visuals</strong>, VIS & IP guidelines. Suggested order: <a href=\"../index.html#section-poster\">Brand</a> → <a href=\"../index.html#section-product\">Product</a> → <a href=\"../index.html#section-ip\">IP</a> → <a href=\"../index.html#section-aigc\">AIGC</a>.",
    },
    "about.intro2": {
        "zh": "独立交付主 KV、电商主图与详情、画册/单页及 INFOCOMM、ISE 等国际展会展位视觉；与市场、销售、运营、开发协作完成官网上线与现场搭建对稿。",
        "en": "Deliver key visuals, e-commerce assets, brochures, and INFOCOMM/ISE booth graphics; collaborate with marketing, sales, ops, and dev on web launch and on-site build alignment.",
    },
    "about.intro3": {
        "zh": "熟练 PS、AI；AE/PR 做短片与活动包装；C4D/Blender 出产品渲染与方案场景图。",
        "en": "Proficient in PS & AI; AE/PR for motion; C4D/Blender for product and scene renders.",
    },
    "about.intro4": {
        "zh": "2025 年起在品牌色与 IP 规范不变前提下，用「参考图 + Prompt 模板 + PS 审稿」做营销场景草图，加快提案迭代。",
        "en": "Since May 2025: reference images + prompt templates + PS review for marketing scene drafts, faster iteration.",
    },
    "about.intro5": {"zh": "2021 年度优秀员工。", "en": "2021 Outstanding Employee Award."},
    "about.infoTitle": {"zh": "基本信息", "en": "Info"},
    "about.jobIntent": {"zh": "求职意向", "en": "Target Role"},
    "about.jobIntentVal": {
        "zh": "视觉设计师 · 智能硬件 / 消费电子品牌视觉",
        "en": "Visual Designer · Smart hardware / Consumer electronics brand visual",
    },
    "about.education": {"zh": "教育经历", "en": "Education"},
    "about.educationVal": {
        "zh": "武汉理工大学 · 计算机科学与技术 · 本科（2021.03 — 2023.06）<br />中原工学院 · 软件技术 · 大专（2017.09 — 2019.06）",
        "en": "Wuhan University of Technology · Computer Science · Bachelor (Mar 2021 — Jun 2023)<br />Zhongyuan University of Technology · Software Technology · Associate (Sep 2017 — Jun 2019)",
    },
    "about.location": {"zh": "现住址", "en": "Location"},
    "about.locationVal": {"zh": "深圳市宝安区", "en": "Bao'an, Shenzhen"},
    "about.contactInfo": {"zh": "联系方式", "en": "Contact"},
    "about.wechatNote": {"zh": "（微信同号）", "en": "(WeChat same number)"},
    "about.skillsTitle": {"zh": "技能", "en": "Skills"},
    "about.skillVisual": {"zh": "视觉", "en": "Visual"},
    "about.skillMotion": {"zh": "动态", "en": "Motion"},
    "about.skill3d": {"zh": "三维", "en": "3D"},
    "about.skillNote": {
        "zh": "另熟悉 Figma、官网 CMS 内容运维；AIGC 终稿均经 Photoshop 审稿。",
        "en": "Also Figma and website CMS ops; all AIGC finals reviewed in Photoshop.",
    },
    "about.expTitle": {"zh": "工作经历", "en": "Experience"},
    "about.projectsTitle": {"zh": "代表项目", "en": "Selected Projects"},
    "about.photoTitle": {"zh": "摄影与审美", "en": "Photography & Taste"},
    "about.photoDesc": {
        "zh": "个人兴趣摄影，关注户外光线与构图，用于保持对消费电子与生活方式品牌画面的敏感度。",
        "en": "Personal photography focused on outdoor light and composition — keeps sensitivity for consumer tech and lifestyle brand imagery.",
    },
    "about.viewWork": {"zh": "查看作品", "en": "View Work"},
    "about.heroTitle": {"zh": "关于我", "en": "About Me"},
    "about.expLpTitle": {
        "zh": "深圳蓝普视讯科技有限公司 · 品牌视觉设计",
        "en": "Shenzhen LPDISPLAY · Brand Visual Design",
    },
    "about.expBlock1": {"zh": "新品上市与产品视觉", "en": "Product Launch & Visual"},
    "about.expBlock2": {"zh": "品牌调性与视觉规范", "en": "Brand Tone & Visual Guidelines"},
    "about.expBlock3": {"zh": "跨部门协作与项目落地", "en": "Cross-functional Delivery"},
    "about.expBlock4": {"zh": "AIGC 创新应用", "en": "AIGC Innovation"},
    "about.expLp1": {
        "zh": "按产品线定位整理版式与主色方向，独立完成主视觉、活动 KV、画册与单页完稿。",
        "en": "Defined layout and color direction per product line; delivered KV, brochures, and print-ready pages.",
    },
    "about.expLp2": {
        "zh": "负责亚马逊、阿里国际站主图规范与详情页信息架构/版式，配合运营上新。",
        "en": "Owned Amazon & Alibaba Intl. listing specs and detail-page IA/layout for go-live.",
    },
    "about.expLp3": {
        "zh": "C4D/Blender 输出产品渲染及指挥大厅、会议、演播室、商显、交通、xR 等方案场景图，用于销售提案与官网案例。",
        "en": "C4D/Blender renders for command centers, meetings, studios, retail, transport, xR — for sales and web cases.",
    },
    "about.expLp4": {
        "zh": "主导公司及子公司 VIS（Logo、主色 #0066FF、标准字、组合规范）及应用稿。",
        "en": "Led VIS (logo, #0066FF, typography, lockups) and application assets for group brands.",
    },
    "about.expLp5": {
        "zh": "参与 IP「小蓝猫 / XIAOLANMAO」比选定稿，编写应用规范；落地画册、展会主 KV、自媒体模板、3D 屏显与周边。",
        "en": "Co-led XIAOLANMAO IP finalization and guidelines; rolled out across brochures, shows, social, 3D displays, merch.",
    },
    "about.expLp6": {
        "zh": "2022 全站视觉重构、2025 视觉更新；2024.10—2025.03 独立运维 CMS（产品中心、解决方案、案例库），约 80% 版块配图由我交付，协同开发上线。",
        "en": "2022 full-site redesign, 2025 refresh; CMS ops (products, solutions, cases) — ~80% visuals delivered with dev.",
    },
    "about.expLp7": {
        "zh": "INFOCOMM、ISE、中东 SLS、LDI 等展会：主题 KV、展位效果图、主屏/吊屏版式与中英文产品墙排版，搭建前与结构图对稿。",
        "en": "INFOCOMM, ISE, SLS, LDI: booth KV, renders, screen layouts, bilingual product walls — aligned pre-build.",
    },
    "about.expLp8": {
        "zh": "2025.05 起建立中英文 Prompt 模板（含负向词、命名规范），即梦/ChatGPT 出图 + PS 终稿审稿。",
        "en": "Since May 2025: bilingual prompt templates (incl. negatives), Jimeng/ChatGPT output + PS final review.",
    },
    "about.expLp9": {
        "zh": "用于 LED 场景营销草图、自媒体配图与周边示意，在合规前提下减少纯 3D 白模反复渲染。",
        "en": "For LED marketing scenes, social assets, merch mockups — reducing pure 3D white-model iterations.",
    },
    "about.expCrystal": {
        "zh": "深圳水晶石教育 · 影视后期与三维设计",
        "en": "Shenzhen Crystal Stone · Post-production & 3D",
    },
    "about.expCrystalDesc": {
        "zh": "MG/宣传片剪辑特效与校色（AE/PR）；《MIX FOLD》指定场景镜头、材质灯光与渲染。",
        "en": "MG/commercial editing, FX, grading (AE/PR); MIX FOLD scene lighting and rendering.",
    },
    "about.expEarly": {
        "zh": "富甲一方 / 贝百教育 / 神农牡丹 · 平面与电商视觉",
        "en": "Fujia / Beibai / Shennong · Graphic & E-commerce Visual",
    },
    "about.expEarlyDesc": {
        "zh": "官网与电商 Banner/详情/画册；抖音、微信公众号视觉。",
        "en": "Web & e-commerce banners, details, brochures; Douyin and WeChat visual.",
    },
    "about.expShifang": {
        "zh": "十方心理有限公司 · UI/UX 设计师（实习）",
        "en": "Shifang Psychology · UI/UX Designer (Intern)",
    },
    "about.expShifangDesc": {
        "zh": "《有爱心理》APP 界面与官网营销物料。",
        "en": "Youai Psychology app UI and marketing assets.",
    },
    "about.proj1Title": {
        "zh": "LPDISPLAY 品牌 VI 升级与 IP「小蓝猫」",
        "en": "LPDISPLAY VI Upgrade & XIAOLANMAO IP",
    },
    "about.proj2Title": {"zh": "官网视觉升级与 CMS 重构", "en": "Website Visual Refresh & CMS Rebuild"},
    "about.proj3Title": {"zh": "国际展会主题视觉与展位", "en": "International Trade Show Visual & Booth"},
    "about.proj4Title": {"zh": "品牌 IP · AIGC 视觉工作流", "en": "Brand IP · AIGC Visual Workflow"},
    "poster.heroTitle": {"zh": "品牌视觉", "en": "Brand Visual"},
    "product.heroTitle": {"zh": "产品视觉", "en": "Product Visual"},
    "ip.heroTitle": {"zh": "IP 设计", "en": "IP Design"},
    "aigc.heroTitle": {"zh": "AIGC 视觉工作流", "en": "AIGC Visual Workflow"},
    "scene.heroTitle": {"zh": "场景 3D", "en": "Scene 3D"},
    "poster.heroDesc": {
        "zh": "新品上市主 KV、企业 VIS 与产品画册；INFOCOMM / ISE / 中东 SLS 等国际展会与跨境社媒物料，突出品牌调性统一与营销落地。",
        "en": "Launch KV, corporate VIS, brochures; INFOCOMM/ISE/SLS trade show and cross-border social assets with unified brand tone.",
    },
    "product.heroDesc": {
        "zh": "跨境电商主图与详情页优先展示；并含 LED 产品渲染、方案场景与 XR 可视化，服务新品上市与销售提案。",
        "en": "Cross-border listing visuals first; LED renders, solution scenes, and XR visualization for launch and sales proposals.",
    },
    "ip.heroDesc": {
        "zh": "主导「小蓝猫 / XIAOLANMAO」IP 定稿与应用规范，落地画册、展会、3D 屏显与营销周边；含 AIGC 场景与周边示意工作流。",
        "en": "Led XIAOLANMAO IP finalization and guidelines; rolled out across brochures, shows, 3D displays, merch, and AIGC workflows.",
    },
    "aigc.heroDesc": {
        "zh": "2025.05 起建立「PS 终稿审稿中枢」汇聚 IP / 电商 / KV / 详情等素材，再按品牌 IP 与电商视觉分线执行；含双引擎并行、三泳道闭环与上线质检驳回回流。",
        "en": "Since May 2025: PS final-review hub for IP, e-com, KV, and detail assets — dual engines, three-lane loops, and QC rejection flow.",
    },
    "scene.heroDesc": {
        "zh": "C4D / Blender 搭建指挥中心、演播室、会议、商显、交通、xR 等应用场景写实渲染，服务官网案例、展会效果图与销售物料。",
        "en": "C4D/Blender photoreal scenes — command centers, studios, retail, transport, xR — for web cases, booth renders, and sales kits.",
    },
}

TITLES = {
    "home": {
        "zh": "谢意 TOM XIE · 视觉设计师作品集",
        "en": "Xie Yi TOM XIE · Visual Designer Portfolio",
    },
    "poster": {"zh": "品牌视觉 · 谢意 TOM XIE", "en": "Brand Visual · Xie Yi TOM XIE"},
    "product": {"zh": "产品视觉 · 谢意 TOM XIE", "en": "Product Visual · Xie Yi TOM XIE"},
    "ip": {"zh": "IP 设计 · 谢意 TOM XIE", "en": "IP Design · Xie Yi TOM XIE"},
    "aigc": {"zh": "AIGC 工作流 · 谢意 TOM XIE", "en": "AIGC Workflow · Xie Yi TOM XIE"},
    "scene": {"zh": "场景 3D · 谢意 TOM XIE", "en": "Scene 3D · Xie Yi TOM XIE"},
    "about": {"zh": "关于我 · 谢意 TOM XIE", "en": "About · Xie Yi TOM XIE"},
}

META = {
    "home": {
        "zh": {
            "description": "谢意 TOM XIE — 视觉设计师作品集：新品上市主 KV、跨境电商详情、品牌 VIS、IP 规范与 AIGC 工作流",
            "ogTitle": "谢意 · 视觉设计师作品集",
            "ogDescription": "品牌与产品视觉 · 跨境电商 · AIGC 审稿工作流 · 深圳",
        },
        "en": {
            "description": "Xie Yi TOM XIE — Visual designer portfolio: launch KV, cross-border e-commerce, brand VIS, IP guidelines & AIGC workflow",
            "ogTitle": "Xie Yi · Visual Designer Portfolio",
            "ogDescription": "Brand & product visual · Cross-border e-commerce · AIGC review workflow · Shenzhen",
        },
    },
}

NAV_ACTIONS = """      <div class="nav-actions">
        <button type="button" class="lang-toggle" id="lang-toggle" aria-label="Switch to English">EN</button>
        <button type="button" class="nav-contact-btn" id="nav-contact-toggle" aria-expanded="false" aria-haspopup="true" aria-controls="nav-contact-menu" data-i18n="nav.contact">联系</button>
        <div class="nav-contact-menu" id="nav-contact-menu" role="menu" hidden>
          <p class="nav-contact-menu__lead" data-i18n="nav.contactLead">欢迎视觉设计相关合作，通常 24 小时内回复。</p>
          <a class="nav-contact-menu__item" href="tel:+8615899782952" role="menuitem">
            <span class="nav-contact-menu__label" data-i18n="nav.phoneWechat">电话 / 微信</span>
            <span class="nav-contact-menu__value">+86 158 9978 2952</span>
          </a>
          <a class="nav-contact-menu__item" href="mailto:623797004@qq.com" role="menuitem">
            <span class="nav-contact-menu__label" data-i18n="nav.email">邮箱</span>
            <span class="nav-contact-menu__value">623797004@qq.com</span>
          </a>
        </div>
      </div>"""

NAV_ACTIONS_WORK = NAV_ACTIONS.replace('href="tel:', 'href="tel:').replace(
    'class="nav-actions"',
    'class="nav-actions"',
)

NAV_INDEX = """      <ul class="nav-links">
        <li><a href="#section-poster" data-section="poster" data-i18n="nav.brandVisual">品牌视觉</a></li>
        <li><a href="#section-product" data-section="product" data-i18n="nav.productVisual">产品视觉</a></li>
        <li><a href="#section-ip" data-section="ip" data-i18n="nav.ipDesign">IP 设计</a></li>
        <li><a href="#section-aigc" data-section="aigc" data-i18n="nav.aigc">AIGC</a></li>
        <li><a href="#section-scene" data-section="scene" data-i18n="nav.scene3d">场景 3D</a></li>
        <li><a href="#section-about" data-section="about" data-i18n="nav.about">关于</a></li>
      </ul>"""

NAV_WORK = """      <ul class="nav-links">
        <li><a href="../index.html#section-poster" data-i18n="nav.brandVisual">品牌视觉</a></li>
        <li><a href="../index.html#section-product" data-i18n="nav.productVisual">产品视觉</a></li>
        <li><a href="../index.html#section-ip" data-i18n="nav.ipDesign">IP 设计</a></li>
        <li><a href="../index.html#section-aigc" data-i18n="nav.aigc">AIGC</a></li>
        <li><a href="../index.html#section-scene" data-i18n="nav.scene3d">场景 3D</a></li>
        <li><a href="../index.html#section-about" data-i18n="nav.about">关于</a></li>
      </ul>"""


def write_i18n_data() -> None:
    out = ROOT / "js" / "i18n-data.js"
    payload = {"strings": STRINGS, "titles": TITLES, "meta": META}
    out.write_text(
        "window.I18N_DATA = " + json.dumps(payload, ensure_ascii=False, indent=2) + ";\n",
        encoding="utf-8",
    )
    print("wrote", out.name, f"({len(STRINGS)} strings)")


def patch_index() -> None:
    path = ROOT / "index.html"
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"<ul class=\"nav-links\">.*?</ul>", NAV_INDEX.strip(), text, count=1, flags=re.DOTALL)
    text = re.sub(
        r"<div class=\"nav-actions\">.*?</div>\s*</div>\s*</nav>",
        NAV_ACTIONS + "\n    </div>\n  </nav>",
        text,
        count=1,
        flags=re.DOTALL,
    )
    if 'data-i18n-page="home"' not in text:
        text = text.replace("<body class=\"is-loading page-home\">", '<body class="is-loading page-home" data-i18n-page="home">')
    replacements = [
        ('<p class="hero-eyebrow">视觉设计师 · 品牌视觉 / 新品上市 · 深圳</p>',
         '<p class="hero-eyebrow" data-i18n="home.heroEyebrow">视觉设计师 · 品牌视觉 / 新品上市 · 深圳</p>'),
        ('<h1>品牌与产品<em>视觉</em></h1>',
         '<h1 data-i18n="home.heroTitle" data-i18n-html>品牌与产品<em>视觉</em></h1>'),
        ('<p class="hero-desc">主 KV · 跨境电商详情 · VIS 与 IP · AIGC 审稿工作流</p>',
         '<p class="hero-desc" data-i18n="home.heroDesc">主 KV · 跨境电商详情 · VIS 与 IP · AIGC 审稿工作流</p>'),
        ('<a class="hero-btn" href="#section-poster">浏览作品</a>',
         '<a class="hero-btn" href="#section-poster" data-i18n="home.heroBrowse">浏览作品</a>'),
        ('<a class="hero-link" href="works/about.html">关于我</a>',
         '<a class="hero-link" href="works/about.html" data-i18n="home.heroAbout">关于我</a>'),
        ('<h2>品牌视觉</h2>\n          <p class="panel-lead">新品主 KV · VI 手册 · 国际展会与跨境社媒</p>\n          <span class="panel-more">进入作品</span>',
         '<h2 data-i18n="home.panelBrandTitle">品牌视觉</h2>\n          <p class="panel-lead" data-i18n="home.panelBrandLead">新品主 KV · VI 手册 · 国际展会与跨境社媒</p>\n          <span class="panel-more" data-i18n="common.viewWork">进入作品</span>'),
        ('<h2>产品视觉</h2>\n          <p class="panel-lead">亚马逊 / 国际站主图与详情 · 产品渲染与 XR 方案</p>\n          <span class="panel-more">进入作品</span>',
         '<h2 data-i18n="home.panelProductTitle">产品视觉</h2>\n          <p class="panel-lead" data-i18n="home.panelProductLead">亚马逊 / 国际站主图与详情 · 产品渲染与 XR 方案</p>\n          <span class="panel-more" data-i18n="common.viewWork">进入作品</span>'),
        ('<h2>IP 设计</h2>\n          <p class="panel-lead">小蓝猫 XIAOLANMAO · 规范 · 社媒与周边落地</p>\n          <span class="panel-more">进入作品</span>',
         '<h2 data-i18n="home.panelIpTitle">IP 设计</h2>\n          <p class="panel-lead" data-i18n="home.panelIpLead">小蓝猫 XIAOLANMAO · 规范 · 社媒与周边落地</p>\n          <span class="panel-more" data-i18n="common.viewWork">进入作品</span>'),
        ('<h2>AIGC 工作流</h2>\n          <p class="panel-lead">星型审稿中枢 · IP 双引擎 · 电商三泳道 · 上线质检</p>\n          <span class="panel-more">进入作品</span>',
         '<h2 data-i18n="home.panelAigcTitle">AIGC 工作流</h2>\n          <p class="panel-lead" data-i18n="home.panelAigcLead">星型审稿中枢 · IP 双引擎 · 电商三泳道 · 上线质检</p>\n          <span class="panel-more" data-i18n="common.viewWork">进入作品</span>'),
        ('<h2>场景 3D</h2>\n          <p class="panel-lead">解决方案场景 · 展会展台 · 项目案例渲染</p>\n          <span class="panel-more">进入作品</span>',
         '<h2 data-i18n="home.panelSceneTitle">场景 3D</h2>\n          <p class="panel-lead" data-i18n="home.panelSceneLead">解决方案场景 · 展会展台 · 项目案例渲染</p>\n          <span class="panel-more" data-i18n="common.viewWork">进入作品</span>'),
        ('<h2>关于我</h2>\n          <p class="panel-lead">5 年品牌视觉 · 跨部门落地 · 求职意向与代表项目</p>\n          <span class="panel-more">了解更多</span>',
         '<h2 data-i18n="home.panelAboutTitle">关于我</h2>\n          <p class="panel-lead" data-i18n="home.panelAboutLead">5 年品牌视觉 · 跨部门落地 · 求职意向与代表项目</p>\n          <span class="panel-more" data-i18n="common.learnMore">了解更多</span>'),
        ('<p>&copy; 2026 谢意 TOM XIE · Visual Designer · 深圳</p>',
         '<p data-i18n="home.footer">&copy; 2026 谢意 TOM XIE · Visual Designer · 深圳</p>'),
        ('<script src="js/app.js"></script>',
         '<script src="js/i18n-data.js"></script>\n  <script src="js/i18n.js"></script>\n  <script src="js/app.js"></script>'),
    ]
    for old, new in replacements:
        text = text.replace(old, new)
    path.write_text(text, encoding="utf-8")
    print("patched index.html")


def patch_work(path: Path, page_key: str, hero_key: str | None = None) -> None:
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"<ul class=\"nav-links\">.*?</ul>", NAV_WORK.strip(), text, count=1, flags=re.DOTALL)
    text = re.sub(
        r"<div class=\"nav-actions\">.*?</div>\s*</div>\s*</nav>",
        NAV_ACTIONS + "\n    </div>\n  </nav>",
        text,
        count=1,
        flags=re.DOTALL,
    )
    if f'data-i18n-page="{page_key}"' not in text:
        text = re.sub(r"<body([^>]*)>", f'<body\\1 data-i18n-page="{page_key}">', text, count=1)
    text = re.sub(
        r'<a class="back" href="([^"]+)">← 返回首页</a>',
        r'<a class="back" href="\1" data-i18n="common.backHome">← 返回首页</a>',
        text,
    )
    text = re.sub(
        r'<a href="\.\./index\.html">← 返回作品集首页</a>',
        r'<a href="../index.html" data-i18n="common.backPortfolio">← 返回作品集首页</a>',
        text,
    )
    if hero_key and f'data-i18n="{hero_key}"' not in text:
        text = re.sub(
            r"(<header class=\"work-hero\">.*?<p>)(.+?)(</p>\s*</header>)",
            rf'\1<span data-i18n="{hero_key}">\2</span>\3',
            text,
            count=1,
            flags=re.DOTALL,
        )
    title_key = f"{page_key}.heroTitle"
    if title_key in STRINGS:
        text = re.sub(
            r"(<header class=\"work-hero\">.*?<h1>)(.+?)(</h1>)",
            rf'\1<span data-i18n="{title_key}">\2</span>\3',
            text,
            count=1,
            flags=re.DOTALL,
        )
    if "../js/app.js" in text and "i18n-data.js" not in text:
        text = text.replace(
            '<script src="../js/app.js"></script>',
            '<script src="../js/i18n-data.js"></script>\n  <script src="../js/i18n.js"></script>\n  <script src="../js/app.js"></script>',
        )
    path.write_text(text, encoding="utf-8")
    print("patched", path.name)


def patch_about() -> None:
    path = WORKS / "about.html"
    text = path.read_text(encoding="utf-8")
    pairs = [
        ('<p>谢意 · 视觉设计师 · 品牌视觉 / 新品上市视觉</p>', '<p data-i18n="about.subtitle">谢意 · 视觉设计师 · 品牌视觉 / 新品上市视觉</p>'),
        ('<h1>关于我</h1>', '<h1 data-i18n="about.heroTitle">关于我</h1>'),
        ('<h2>个人简介</h2>', '<h2 data-i18n="about.introTitle">个人简介</h2>'),
        ('<h2>基本信息</h2>', '<h2 data-i18n="about.infoTitle">基本信息</h2>'),
        ('<strong>求职意向</strong>', '<strong data-i18n="about.jobIntent">求职意向</strong>'),
        ('<p>视觉设计师 · 智能硬件 / 消费电子品牌视觉</p>', '<p data-i18n="about.jobIntentVal">视觉设计师 · 智能硬件 / 消费电子品牌视觉</p>'),
        ('<strong>教育经历</strong>', '<strong data-i18n="about.education">教育经历</strong>'),
        ('<strong>现住址</strong>', '<strong data-i18n="about.location">现住址</strong>'),
        ('<p>深圳市宝安区</p>', '<p data-i18n="about.locationVal">深圳市宝安区</p>'),
        ('<strong>联系方式</strong>', '<strong data-i18n="about.contactInfo">联系方式</strong>'),
        ('（微信同号）', '<span data-i18n="about.wechatNote">（微信同号）</span>'),
        ('<h2>技能</h2>', '<h2 data-i18n="about.skillsTitle">技能</h2>'),
        ('<span class="skill-group__title">视觉</span>', '<span class="skill-group__title" data-i18n="about.skillVisual">视觉</span>'),
        ('<span class="skill-group__title">动态</span>', '<span class="skill-group__title" data-i18n="about.skillMotion">动态</span>'),
        ('<span class="skill-group__title">三维</span>', '<span class="skill-group__title" data-i18n="about.skill3d">三维</span>'),
        ('<p class="skill-note">另熟悉 Figma、官网 CMS 内容运维；AIGC 终稿均经 Photoshop 审稿。</p>',
         '<p class="skill-note" data-i18n="about.skillNote">另熟悉 Figma、官网 CMS 内容运维；AIGC 终稿均经 Photoshop 审稿。</p>'),
        ('<h2>工作经历</h2>', '<h2 data-i18n="about.expTitle">工作经历</h2>'),
        ('<h3>深圳蓝普视讯科技有限公司 · 品牌视觉设计</h3>', '<h3 data-i18n="about.expLpTitle">深圳蓝普视讯科技有限公司 · 品牌视觉设计</h3>'),
        ('<h4>新品上市与产品视觉</h4>', '<h4 data-i18n="about.expBlock1">新品上市与产品视觉</h4>'),
        ('<h4>品牌调性与视觉规范</h4>', '<h4 data-i18n="about.expBlock2">品牌调性与视觉规范</h4>'),
        ('<h4>跨部门协作与项目落地</h4>', '<h4 data-i18n="about.expBlock3">跨部门协作与项目落地</h4>'),
        ('<h4>AIGC 创新应用</h4>', '<h4 data-i18n="about.expBlock4">AIGC 创新应用</h4>'),
        ('<li>按产品线定位整理版式与主色方向，独立完成主视觉、活动 KV、画册与单页完稿。</li>', '<li data-i18n="about.expLp1">按产品线定位整理版式与主色方向，独立完成主视觉、活动 KV、画册与单页完稿。</li>'),
        ('<li>负责亚马逊、阿里国际站主图规范与详情页信息架构/版式，配合运营上新。</li>', '<li data-i18n="about.expLp2">负责亚马逊、阿里国际站主图规范与详情页信息架构/版式，配合运营上新。</li>'),
        ('<li>C4D/Blender 输出产品渲染及指挥大厅、会议、演播室、商显、交通、xR 等方案场景图，用于销售提案与官网案例。</li>', '<li data-i18n="about.expLp3">C4D/Blender 输出产品渲染及指挥大厅、会议、演播室、商显、交通、xR 等方案场景图，用于销售提案与官网案例。</li>'),
        ('<li>主导公司及子公司 VIS（Logo、主色 #0066FF、标准字、组合规范）及应用稿。</li>', '<li data-i18n="about.expLp4">主导公司及子公司 VIS（Logo、主色 #0066FF、标准字、组合规范）及应用稿。</li>'),
        ('<li>参与 IP「小蓝猫 / XIAOLANMAO」比选定稿，编写应用规范；落地画册、展会主 KV、自媒体模板、3D 屏显与周边。</li>', '<li data-i18n="about.expLp5">参与 IP「小蓝猫 / XIAOLANMAO」比选定稿，编写应用规范；落地画册、展会主 KV、自媒体模板、3D 屏显与周边。</li>'),
        ('<li>2022 全站视觉重构、2025 视觉更新；2024.10—2025.03 独立运维 CMS（产品中心、解决方案、案例库），约 80% 版块配图由我交付，协同开发上线。</li>', '<li data-i18n="about.expLp6">2022 全站视觉重构、2025 视觉更新；2024.10—2025.03 独立运维 CMS（产品中心、解决方案、案例库），约 80% 版块配图由我交付，协同开发上线。</li>'),
        ('<li>INFOCOMM、ISE、中东 SLS、LDI 等展会：主题 KV、展位效果图、主屏/吊屏版式与中英文产品墙排版，搭建前与结构图对稿。</li>', '<li data-i18n="about.expLp7">INFOCOMM、ISE、中东 SLS、LDI 等展会：主题 KV、展位效果图、主屏/吊屏版式与中英文产品墙排版，搭建前与结构图对稿。</li>'),
        ('<li>2025.05 起建立中英文 Prompt 模板（含负向词、命名规范），即梦/ChatGPT 出图 + PS 终稿审稿。</li>', '<li data-i18n="about.expLp8">2025.05 起建立中英文 Prompt 模板（含负向词、命名规范），即梦/ChatGPT 出图 + PS 终稿审稿。</li>'),
        ('<li>用于 LED 场景营销草图、自媒体配图与周边示意，在合规前提下减少纯 3D 白模反复渲染。</li>', '<li data-i18n="about.expLp9">用于 LED 场景营销草图、自媒体配图与周边示意，在合规前提下减少纯 3D 白模反复渲染。</li>'),
        ('<h3>深圳水晶石教育 · 影视后期与三维设计</h3>', '<h3 data-i18n="about.expCrystal">深圳水晶石教育 · 影视后期与三维设计</h3>'),
        ('<p>MG/宣传片剪辑特效与校色（AE/PR）；《MIX FOLD》指定场景镜头、材质灯光与渲染。</p>', '<p data-i18n="about.expCrystalDesc">MG/宣传片剪辑特效与校色（AE/PR）；《MIX FOLD》指定场景镜头、材质灯光与渲染。</p>'),
        ('<h3>富甲一方 / 贝百教育 / 神农牡丹 · 平面与电商视觉</h3>', '<h3 data-i18n="about.expEarly">富甲一方 / 贝百教育 / 神农牡丹 · 平面与电商视觉</h3>'),
        ('<p>官网与电商 Banner/详情/画册；抖音、微信公众号视觉。</p>', '<p data-i18n="about.expEarlyDesc">官网与电商 Banner/详情/画册；抖音、微信公众号视觉。</p>'),
        ('<h3>十方心理有限公司 · UI/UX 设计师（实习）</h3>', '<h3 data-i18n="about.expShifang">十方心理有限公司 · UI/UX 设计师（实习）</h3>'),
        ('<p>《有爱心理》APP 界面与官网营销物料。</p>', '<p data-i18n="about.expShifangDesc">《有爱心理》APP 界面与官网营销物料。</p>'),
        ('<h2>摄影与审美</h2>', '<h2 data-i18n="about.photoTitle">摄影与审美</h2>'),
        ('<h2>代表项目</h2>', '<h2 data-i18n="about.projectsTitle">代表项目</h2>'),
        ('<h3>LPDISPLAY 品牌 VI 升级与 IP「小蓝猫」</h3>', '<h3 data-i18n="about.proj1Title">LPDISPLAY 品牌 VI 升级与 IP「小蓝猫」</h3>'),
        ('<h3>官网视觉升级与 CMS 重构</h3>', '<h3 data-i18n="about.proj2Title">官网视觉升级与 CMS 重构</h3>'),
        ('<h3>国际展会主题视觉与展位</h3>', '<h3 data-i18n="about.proj3Title">国际展会主题视觉与展位</h3>'),
        ('<h3>品牌 IP · AIGC 视觉工作流</h3>', '<h3 data-i18n="about.proj4Title">品牌 IP · AIGC 视觉工作流</h3>'),
        ('<p>2021 年度优秀员工。</p>', '<p data-i18n="about.intro5">2021 年度优秀员工。</p>'),
        ('<p>熟练 PS、AI；AE/PR 做短片与活动包装；C4D/Blender 出产品渲染与方案场景图。</p>', '<p data-i18n="about.intro3">熟练 PS、AI；AE/PR 做短片与活动包装；C4D/Blender 出产品渲染与方案场景图。</p>'),
        ('<p>2025 年起在品牌色与 IP 规范不变前提下，用「参考图 + Prompt 模板 + PS 审稿」做营销场景草图，加快提案迭代。</p>', '<p data-i18n="about.intro4">2025 年起在品牌色与 IP 规范不变前提下，用「参考图 + Prompt 模板 + PS 审稿」做营销场景草图，加快提案迭代。</p>'),
        ('<p>独立交付主 KV、电商主图与详情、画册/单页及 INFOCOMM、ISE 等国际展会展位视觉；与市场、销售、运营、开发协作完成官网上线与现场搭建对稿。</p>', '<p data-i18n="about.intro2">独立交付主 KV、电商主图与详情、画册/单页及 INFOCOMM、ISE 等国际展会展位视觉；与市场、销售、运营、开发协作完成官网上线与现场搭建对稿。</p>'),
    ]
    for old, new in pairs:
        text = text.replace(old, new)
    edu_old = '<p>武汉理工大学 · 计算机科学与技术 · 本科（2021.03 — 2023.06）<br />中原工学院 · 软件技术 · 大专（2017.09 — 2019.06）</p>'
    edu_new = '<p data-i18n="about.educationVal" data-i18n-html>武汉理工大学 · 计算机科学与技术 · 本科（2021.03 — 2023.06）<br />中原工学院 · 软件技术 · 大专（2017.09 — 2019.06）</p>'
    text = text.replace(edu_old, edu_new)
    intro1_old = '<p>5 年品牌视觉（蓝普视讯 2021.06 至今），专注<strong style="color: var(--text); font-weight: 600;">新品与产品线上市视觉</strong>、品牌 VIS 与 IP 规范落地。作品集建议浏览顺序：<a href="../index.html#section-poster">品牌</a> → <a href="../index.html#section-product">产品</a> → <a href="../index.html#section-ip">IP</a> → <a href="../index.html#section-aigc">AIGC</a>。</p>'
    intro1_new = '<p data-i18n="about.intro1" data-i18n-html>5 年品牌视觉（蓝普视讯 2021.06 至今），专注<strong style="color: var(--text); font-weight: 600;">新品与产品线上市视觉</strong>、品牌 VIS 与 IP 规范落地。作品集建议浏览顺序：<a href="../index.html#section-poster">品牌</a> → <a href="../index.html#section-product">产品</a> → <a href="../index.html#section-ip">IP</a> → <a href="../index.html#section-aigc">AIGC</a>。</p>'
    text = text.replace(intro1_old, intro1_new)
    photo_old = '<p style="font-size: 15px; color: var(--text-muted); margin-bottom: 20px; line-height: 1.7;">个人兴趣摄影，关注户外光线与构图，用于保持对消费电子与生活方式品牌画面的敏感度。</p>'
    photo_new = '<p style="font-size: 15px; color: var(--text-muted); margin-bottom: 20px; line-height: 1.7;" data-i18n="about.photoDesc">个人兴趣摄影，关注户外光线与构图，用于保持对消费电子与生活方式品牌画面的敏感度。</p>'
    text = text.replace(photo_old, photo_new)
    path.write_text(text, encoding="utf-8")
    print("patched about.html details")


def main() -> None:
    patch_index()
    patch_work(WORKS / "poster.html", "poster", "poster.heroDesc")
    patch_work(WORKS / "product.html", "product", "product.heroDesc")
    patch_work(WORKS / "ip.html", "ip", "ip.heroDesc")
    patch_work(WORKS / "aigc.html", "aigc", "aigc.heroDesc")
    patch_work(WORKS / "scene.html", "scene", "scene.heroDesc")
    patch_work(WORKS / "about.html", "about", None)
    patch_about()
    write_i18n_data()


if __name__ == "__main__":
    main()
