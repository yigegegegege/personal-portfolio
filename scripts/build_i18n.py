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
    "common.backToTop": {"zh": "回到顶部", "en": "Back to top"},
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
        "zh": "5 年品牌视觉 · 跨部门落地 · 求职意向与项目经历",
        "en": "5 yrs brand visual · Cross-functional delivery · Target roles & projects",
    },
    "home.footer": {
        "zh": "© 2026 谢意 TOM XIE · Visual Designer · 深圳",
        "en": "© 2026 Xie Yi TOM XIE · Visual Designer · Shenzhen",
    },
    # About page
    "about.subtitle": {
        "zh": "谢意 · 视觉设计师 · 品牌视觉 / 独立站与官网 / 平面设计 / IP / 3D / AIGC",
        "en": "Xie Yi · Visual Designer · Brand / Web / Print / IP / 3D / AIGC",
    },
    "about.introTitle": {"zh": "个人简介", "en": "Profile"},
    "about.intro1": {
        "zh": "5 年品牌视觉设计经验（深圳蓝普视讯 2021.06 至今），主导 VIS 升级、品牌 IP「小蓝猫」体系及全触点视觉落地。",
        "en": "5 years in brand visual design (LPDISPLAY, since Jun 2021), leading VIS refresh, XIAOLANMAO IP system, and full-touchpoint rollout.",
    },
    "about.intro2": {
        "zh": "独立完成活动主 KV、画册/折页/海报等平面设计完稿，以及亚马逊/阿里国际站主图与详情、公众号/视频号模板；负责品牌官网/独立站视觉与 CMS 运维，约 80% 版块配图由我产出。",
        "en": "Deliver event KV, brochures, print-ready pages, Amazon/Alibaba Intl. listings, and WeChat/video templates; own web visual & CMS ops — ~80% of section visuals.",
    },
    "about.intro3": {
        "zh": "C4D/Blender 完成产品渲染与指挥大厅、会议、演播室、商显、交通、xR 等六大类方案场景图，服务销售提案与官网案例库。",
        "en": "C4D/Blender product renders and six solution-scene categories for sales proposals and web case library.",
    },
    "about.intro4": {
        "zh": "2025.05 起搭建「参考图 + Prompt 模板 + PS 审稿」AIGC 流程，缩短营销场景草图与提案物料周期。",
        "en": "Since May 2025: reference images + prompt templates + PS review workflow to speed marketing drafts.",
    },
    "about.intro5": {
        "zh": "与市场、运营、开发协作推动 2022 全站重构上线、2025 视觉更新上线及 INFOCOMM/ISE 等国际展会主题视觉。",
        "en": "With marketing, ops, and dev: 2022/2025 site relaunches and INFOCOMM/ISE trade-show visual systems.",
    },
    "about.infoTitle": {"zh": "基本信息", "en": "Info"},
    "about.jobIntent": {"zh": "求职意向", "en": "Target Role"},
    "about.jobIntentVal": {
        "zh": "品牌视觉设计师 / 视觉设计师 / 高级视觉设计师",
        "en": "Brand Visual Designer / Visual Designer / Senior Visual Designer",
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
    "about.projectsTitle": {"zh": "项目经历", "en": "Projects"},
    "about.photoTitle": {"zh": "摄影与审美", "en": "Photography & Taste"},
    "about.photoDesc": {
        "zh": "个人兴趣摄影，关注户外光线与构图，用于保持对消费电子与生活方式品牌画面的敏感度。",
        "en": "Personal photography focused on outdoor light and composition — keeps sensitivity for consumer tech and lifestyle brand imagery.",
    },
    "about.photoCommercialCap": {
        "zh": "商业视觉 · 立式数字海报屏场景渲染（海滨黄金时刻）",
        "en": "Commercial visual · Vertical digital poster scene render (coastal golden hour)",
    },
    "about.motionTitle": {"zh": "Motion 精选", "en": "Motion Highlights"},
    "about.motionDesc": {
        "zh": "水晶石实习期间两部代表性项目：三维产品宣传《MIX FOLD》与 MG 动效《About Korean》。",
        "en": "Two standout projects from Crystal Stone internship: MIX FOLD product CG and About Korean MG motion.",
    },
    "about.motionMixTitle": {"zh": "《MIX FOLD》", "en": "MIX FOLD"},
    "about.motionMixDesc": {
        "zh": "深圳水晶石教育 · 2021.04—2021.05。产品宣传短片：场景建模、材质灯光与渲染；AE/PR 参与剪辑校色。",
        "en": "Shenzhen Crystal Stone · Apr–May 2021. Product promo: scene modeling, materials, lighting, rendering; AE/PR edit & grade.",
    },
    "about.motionKoreanTitle": {"zh": "《About Korean》· MG 动效", "en": "About Korean · MG Motion"},
    "about.motionKoreanDesc": {
        "zh": "AE 完成镜头动画、图形节奏与字幕包装，输出 MG 宣传短片。",
        "en": "AE-driven camera animation, graphic rhythm, and typography — MG promo piece.",
    },
    "about.viewWork": {"zh": "查看作品", "en": "View Work"},
    "about.heroTitle": {"zh": "关于我", "en": "About Me"},
    "about.expLpTitle": {
        "zh": "深圳蓝普视讯科技有限公司 · 品牌视觉设计",
        "en": "Shenzhen LPDISPLAY · Brand Visual Design",
    },
    "about.expBlock1": {"zh": "品牌 VIS、IP 与创意视觉", "en": "Brand VIS, IP & Creative Visual"},
    "about.expBlock2": {"zh": "数字阵地与电商视觉", "en": "Digital Touchpoints & E-commerce Visual"},
    "about.expBlock3": {"zh": "3D 渲染与方案场景", "en": "3D Rendering & Solution Scenes"},
    "about.expBlock4": {"zh": "整合营销、展会与 AIGC", "en": "Integrated Marketing, Trade Shows & AIGC"},
    "about.expLp1": {
        "zh": "作为品牌创意视觉主责，主导公司及子公司 VIS（Logo、主色 #0066FF、标准字、组合规范）规划与迭代。",
        "en": "Lead brand creative visual; drove group VIS (logo, #0066FF, typography, lockups) planning and iteration.",
    },
    "about.expLp2": {
        "zh": "参与 IP「小蓝猫 / XIAOLANMAO」多方案比选，以年轻化、潮流感形象定稿并编写应用规范；落地画册、展会 KV、自媒体模板、3D 屏显与周边。",
        "en": "Co-led XIAOLANMAO IP selection and guidelines; rolled out across brochures, show KV, social templates, 3D displays, merch.",
    },
    "about.expLp3": {
        "zh": "改版产品画册、案例画册、彩页等核心平面设计物料，保证多触点视觉一致。",
        "en": "Refreshed product/case brochures and core print assets for consistent multi-touchpoint visual.",
    },
    "about.expLp4": {
        "zh": "负责品牌官网/独立站视觉策略与 CMS 内容运维（产品中心、解决方案、案例库）；2022 全站重构 + 2025 视觉更新上线，约 80% Banner/配图由我独立完成并交付。",
        "en": "Owned web/standalone visual strategy and CMS ops; 2022/2025 relaunches — ~80% banners/visuals delivered solo.",
    },
    "about.expLp5": {
        "zh": "制定亚马逊、阿里国际站主图规范与详情页信息架构/版式，配合运营上新节点交付与改稿。",
        "en": "Defined Amazon/Alibaba Intl. listing specs and detail-page IA/layout for go-live cycles.",
    },
    "about.expLp6": {
        "zh": "独立完成折页、海报、主图/详情等平面设计完稿（PS/AI），按印刷与屏幕双渠道规范输出，协同开发完成页面上线。",
        "en": "Delivered print and screen-ready flyers, posters, listing visuals (PS/AI) with dev for page launch.",
    },
    "about.expLp7": {
        "zh": "C4D/Blender 完成室内外 LED 产品高精度渲染，用于画册、官网与销售提案。",
        "en": "High-precision indoor/outdoor LED product renders (C4D/Blender) for brochures, web, and sales.",
    },
    "about.expLp8": {
        "zh": "搭建指挥大厅、演播室、会议、商业零售、交通显示、xR 虚拟拍摄等场景图库，与官网解决方案栏目对齐。",
        "en": "Built solution-scene libraries (command center, studio, meeting, retail, transport, xR) aligned with web.",
    },
    "about.expLp9": {
        "zh": "探索户外裸眼 3D 大屏创意构图，在官方 IP 规范内融入屏显内容创意。",
        "en": "Explored outdoor naked-eye 3D compositions within official IP guidelines.",
    },
    "about.expLp10": {
        "zh": "主导 INFOCOMM、ISE、中东 SLS、LDI 等大型展会主题 KV、展位效果图及主屏/吊屏版式，搭建前与结构图对稿。",
        "en": "Led INFOCOMM, ISE, SLS, LDI booth KV, renders, and screen layouts — aligned pre-build.",
    },
    "about.expLp11": {
        "zh": "活动 KV 与自媒体模板结合潮流版式与品牌色做年轻化升级，适配公众号/视频号传播节奏；AE/PR 完成短片包装与校色。",
        "en": "Refreshed event KV and social templates with trend layouts and brand color; AE/PR motion packaging.",
    },
    "about.expLp12": {
        "zh": "2025.05 起建立中英文 Prompt 模板（含负向词、命名规范），即梦/ChatGPT 出图 + PS 终稿审稿，用于场景营销草图与自媒体配图。",
        "en": "Since May 2025: bilingual prompt templates, Jimeng/ChatGPT output + PS review for marketing/social drafts.",
    },
    "about.expCrystal": {
        "zh": "深圳水晶石教育 · 影视后期与三维设计",
        "en": "Shenzhen Crystal Stone · Post-production & 3D",
    },
    "about.expCrystalDesc": {
        "zh": "MG/宣传片剪辑特效（AE/PR）；《MIX FOLD》指定场景镜头、材质灯光与渲染。",
        "en": "MG/commercial editing, FX (AE/PR); MIX FOLD assigned scene shots — materials, lighting, rendering.",
    },
    "about.expEarly": {
        "zh": "富甲一方 / 贝百教育 / 神农牡丹 · 平面与电商视觉",
        "en": "Fujia / Beibai / Shennong · Graphic & E-commerce Visual",
    },
    "about.expEarlyDesc": {
        "zh": "官网/活动 Banner、印刷物料；抖音、微信公众号视觉与短视频剪辑。",
        "en": "Web/event banners, print assets; Douyin, WeChat visual and short-video editing.",
    },
    "about.expShifang": {
        "zh": "十方心理有限公司 · UI/UX 设计师（实习）",
        "en": "Shifang Psychology · UI/UX Designer (Intern)",
    },
    "about.expShifangDesc": {
        "zh": "《有爱心理》APP 全平台界面与官网营销物料。",
        "en": "Youai Psychology app UI across platforms and web marketing assets.",
    },
    "about.proj1Title": {
        "zh": "LPDISPLAY 品牌 VI 升级与 IP「小蓝猫」体系",
        "en": "LPDISPLAY VI Upgrade & XIAOLANMAO IP System",
    },
    "about.proj1Meta": {
        "zh": "2022.04 — 至今 · 项目角色：创意视觉设计师 · VIS 主导 · <a href=\"poster.html#col-vi\">查看作品</a>",
        "en": "Apr 2022 — Present · Role: Creative Visual · VIS Lead · <a href=\"poster.html#col-vi\">View work</a>",
    },
    "about.proj1Bg": {
        "zh": "<strong>背景：</strong>配合品牌国际化，启动 Logo、VIS 及 IP 全面升级。",
        "en": "<strong>Context:</strong> Brand internationalization drove full Logo, VIS, and IP refresh.",
    },
    "about.proj1Duty": {
        "zh": "<strong>职责：</strong>Logo 多方案比选；输出 VI 基础/应用系统及画册、彩页、名片等平面设计规范；IP「小蓝猫」年轻化方案获采纳为核心资产。",
        "en": "<strong>Role:</strong> Logo options; VI base/application systems; XIAOLANMAO youth scheme adopted as core asset.",
    },
    "about.proj1Result": {
        "zh": "<strong>成果：</strong>建立可复用品牌手册与 IP 应用规范，统一画册、展会、电商、自媒体输出，提升品牌潮流感与记忆点。",
        "en": "<strong>Outcome:</strong> Reusable brand manual and IP guidelines unified brochures, shows, e-com, and social.",
    },
    "about.proj2Title": {
        "zh": "品牌官网/独立站视觉升级与 CMS 内容体系重构",
        "en": "Website/Standalone Visual Refresh & CMS Rebuild",
    },
    "about.proj2Meta": {
        "zh": "2022.04 — 2026.04 · 项目角色：视觉设计 · 主责 · <a href=\"poster.html#col-banner\">品牌 KV</a> · <a href=\"product.html#col-ecom\">跨境电商</a>",
        "en": "Apr 2022 — Apr 2026 · Role: Visual Design · Lead · <a href=\"poster.html#col-banner\">Brand KV</a> · <a href=\"product.html#col-ecom\">E-commerce</a>",
    },
    "about.proj2Bg": {
        "zh": "<strong>背景：</strong>原官网/独立站信息架构陈旧，需对齐 B2B 专业调性并支撑业务展示。",
        "en": "<strong>Context:</strong> Legacy site IA needed B2B tone and stronger business showcase.",
    },
    "about.proj2Duty": {
        "zh": "<strong>职责：</strong>2022.07 定稿全站风格；独立完成 Banner、图标、版块配图等平面设计交付（约 80%），协同开发完成页面上线；2024.10—2025.03 重构产品中心、解决方案、案例库栏目。",
        "en": "<strong>Role:</strong> Site style sign-off Jul 2022; ~80% banners/visuals solo; rebuilt product, solution, case sections 2024–2025.",
    },
    "about.proj2Result": {
        "zh": "<strong>成果：</strong>新版官网/独立站成功上线，核心栏目内容完整度显著提升，成为销售与客户了解品牌的首要入口。",
        "en": "<strong>Outcome:</strong> New site live with fuller core sections — primary entry for sales and clients.",
    },
    "about.proj3Title": {
        "zh": "国际行业展会主题视觉与展位设计",
        "en": "International Trade Show Visual & Booth Design",
    },
    "about.proj3Meta": {
        "zh": "2022.06 — 2026.01 · 项目角色：主视觉设计师 · 创意视觉 · <a href=\"poster.html#col-case-study\">查看作品</a>",
        "en": "Jun 2022 — Jan 2026 · Role: Key Visual Designer · <a href=\"poster.html#col-case-study\">View work</a>",
    },
    "about.proj3Bg": {
        "zh": "<strong>背景：</strong>海外市场拓展需统一、高辨识度的展台视觉体系。",
        "en": "<strong>Context:</strong> Overseas expansion needed a unified, recognizable booth visual system.",
    },
    "about.proj3Duty": {
        "zh": "<strong>职责：</strong>ISE（2024—2026）、INFOCOMM（2023—2025）、中东 SLS（2025—2026）等方案视觉；展位结构、主屏/吊屏版式、产品墙与中英文参数排版。",
        "en": "<strong>Role:</strong> ISE, INFOCOMM, SLS visuals; booth structure, screen layouts, bilingual product walls.",
    },
    "about.proj3Result": {
        "zh": "<strong>成果：</strong>多套方案投入现场搭建，保障海内外展会品牌露出一致性，支撑海外市场拓展。",
        "en": "<strong>Outcome:</strong> Multiple schemes built on-site with consistent global brand presence.",
    },
    "about.proj4Title": {
        "zh": "LED 产品 3D 渲染与解决方案场景可视化",
        "en": "LED Product 3D Rendering & Solution Scene Visualization",
    },
    "about.proj4Meta": {
        "zh": "2022 — 2026 · 项目角色：3D 视觉设计 · 独立负责 · <a href=\"scene.html\">查看作品</a>",
        "en": "2022 — 2026 · Role: 3D Visual Design · Solo · <a href=\"scene.html\">View work</a>",
    },
    "about.proj4Bg": {
        "zh": "<strong>背景：</strong>销售与市场需高质量场景图支撑提案，纯摄影成本高、迭代慢。",
        "en": "<strong>Context:</strong> Sales needed quality scene visuals; photography was costly and slow.",
    },
    "about.proj4Duty": {
        "zh": "<strong>职责：</strong>产品线高精度材质灯光渲染；搭建六大类应用场景 3D 图库并与官网案例库对齐。",
        "en": "<strong>Role:</strong> High-precision product renders; six-category 3D scene library aligned with web cases.",
    },
    "about.proj4Result": {
        "zh": "<strong>成果：</strong>形成可复用场景图库，缩短销售与市场部门物料制作周期，支撑多产品线提案。",
        "en": "<strong>Outcome:</strong> Reusable scene library shortened sales/marketing production cycles.",
    },
    "about.proj5Title": {
        "zh": "品牌 IP · AIGC 视觉资产工作流",
        "en": "Brand IP · AIGC Visual Asset Workflow",
    },
    "about.proj5Meta": {
        "zh": "2025.05 — 2026.04 · 项目角色：品牌视觉设计 · 流程搭建与执行 · <a href=\"aigc.html\">查看作品</a>",
        "en": "May 2025 — Apr 2026 · Role: Brand Visual · Workflow build & run · <a href=\"aigc.html\">View work</a>",
    },
    "about.proj5Bg": {
        "zh": "<strong>背景：</strong>营销提案与自媒体配图需求增长，需在 IP 合规前提下提效。",
        "en": "<strong>Context:</strong> Growing proposal/social needs required faster output within IP compliance.",
    },
    "about.proj5Duty": {
        "zh": "<strong>职责：</strong>建立 Prompt 模板、负向词库与试生成归档；即梦/ChatGPT 出图 + PS 终稿审稿。",
        "en": "<strong>Role:</strong> Prompt templates, negative-word library, archives; Jimeng/ChatGPT + PS final review.",
    },
    "about.proj5Result": {
        "zh": "<strong>成果：</strong>形成「设计规范 → Prompt → 生成 → 审稿」闭环，降低纯 3D 试错成本，为提案与自媒体提供快速视觉草案。",
        "en": "<strong>Outcome:</strong> Guidelines → Prompt → Generate → Review loop cut 3D trial cost for fast drafts.",
    },
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
        "zh": "「小蓝猫 / XIAOLANMAO」从定稿、规范到展会与社媒落地；含应用场景融合、周边示意与 AIGC 辅助场景草图（保持 IP 合规）。",
        "en": "XIAOLANMAO IP from finalization and guidelines to trade shows and social rollout — scene fusion, merch mockups, and compliant AIGC sketches.",
    },
    "aigc.heroDesc": {
        "zh": "2025.05 起建立「<strong style=\"color: var(--text); font-weight: 600;\">PS 终稿审稿中枢</strong>」汇聚 IP / 电商 / KV / 详情等素材，再按品牌 IP 与电商视觉分线执行；含双引擎并行、三泳道闭环与上线质检驳回回流。",
        "en": "Since May 2025, built a <strong style=\"color: var(--text); font-weight: 600;\">PS final-review hub</strong> for IP, e-commerce, KV, and detail assets — dual-engine lanes, three-lane loops, and QC rejection flow.",
    },
    "scene.heroDesc": {
        "zh": "六大类解决方案场景、国际展会展台可视化与项目案例渲染，服务新品叙事、官网案例与销售提案。",
        "en": "Six solution-scene categories, trade-show booth visualization, and case renders for launch narratives, web cases, and sales proposals.",
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

SITE_URL = "https://personal-portfolio-two-pi-54.vercel.app"

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
    "poster": {
        "zh": {
            "description": "谢意作品集 — 品牌视觉：新品上市主 KV、企业 VIS、产品画册与国际展会跨境社媒物料",
            "ogTitle": "品牌视觉 · 谢意 TOM XIE",
            "ogDescription": "运动户外主 KV · VI 手册 · INFOCOMM / ISE / 中东 SLS 展会物料",
        },
        "en": {
            "description": "Brand visual portfolio — launch KV, corporate VIS, brochures, and international trade-show social assets",
            "ogTitle": "Brand Visual · Xie Yi TOM XIE",
            "ogDescription": "Action sports KV · VI manual · INFOCOMM / ISE / SLS trade-show assets",
        },
    },
    "product": {
        "zh": {
            "description": "谢意作品集 — 产品视觉：跨境电商主图与详情页、LED 产品渲染与 XR 方案场景",
            "ogTitle": "产品视觉 · 谢意 TOM XIE",
            "ogDescription": "亚马逊 / 国际站主图与详情 · 产品渲染 · XR 可视化",
        },
        "en": {
            "description": "Product visual portfolio — cross-border listing creatives, LED renders, and XR solution scenes",
            "ogTitle": "Product Visual · Xie Yi TOM XIE",
            "ogDescription": "Amazon / international listings · product renders · XR visualization",
        },
    },
    "ip": {
        "zh": {
            "description": "谢意作品集 — IP 设计：小蓝猫 XIAOLANMAO 定稿、规范与展会社媒周边落地",
            "ogTitle": "IP 设计 · 谢意 TOM XIE",
            "ogDescription": "小蓝猫 IP · 应用规范 · 展会与社媒落地",
        },
        "en": {
            "description": "IP design portfolio — XIAOLANMAO finalization, guidelines, and rollout across shows and social",
            "ogTitle": "IP Design · Xie Yi TOM XIE",
            "ogDescription": "XIAOLANMAO IP · brand guidelines · show & social rollout",
        },
    },
    "aigc": {
        "zh": {
            "description": "谢意作品集 — AIGC 视觉工作流：星型 PS 审稿中枢、IP 双引擎、电商三泳道、上线质检与 Prompt 外形锁定",
            "ogTitle": "AIGC 工作流 · 谢意 TOM XIE",
            "ogDescription": "PS 终稿审稿中枢 · 双引擎并行 · 三泳道闭环 · 上线质检",
        },
        "en": {
            "description": "AIGC visual workflow — PS review hub, dual IP engines, e-commerce lanes, and QC rejection flow",
            "ogTitle": "AIGC Workflow · Xie Yi TOM XIE",
            "ogDescription": "PS final-review hub · dual engines · three-lane loops · launch QC",
        },
    },
    "scene": {
        "zh": {
            "description": "谢意作品集 — 场景 3D：六大类解决方案场景、国际展会展台可视化与项目案例渲染",
            "ogTitle": "场景 3D · 谢意 TOM XIE",
            "ogDescription": "解决方案场景 · 展会展台 · 官网案例与销售提案渲染",
        },
        "en": {
            "description": "Scene 3D portfolio — solution environments, trade-show booth visualization, and case-study renders",
            "ogTitle": "Scene 3D · Xie Yi TOM XIE",
            "ogDescription": "Solution scenes · exhibition booths · web cases and sales proposals",
        },
    },
    "about": {
        "zh": {
            "description": "谢意 TOM XIE — 视觉设计师 · 深圳 · 5 年品牌视觉经验，专注新品上市、VIS 与 AIGC 审稿工作流",
            "ogTitle": "关于我 · 谢意 TOM XIE",
            "ogDescription": "视觉设计师 · 品牌视觉 / 新品上市 · 深圳",
        },
        "en": {
            "description": "About Xie Yi TOM XIE — visual designer in Shenzhen with 5 years in brand visual, launch KV, VIS, and AIGC workflow",
            "ogTitle": "About · Xie Yi TOM XIE",
            "ogDescription": "Visual designer · brand / launch visual · Shenzhen",
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
