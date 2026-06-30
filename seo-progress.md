# SEO 優化進度

> 網站：留佇包棟民宿　https://liozu-stay.com
> 平台：Astro 靜態網站 + Cloudflare Pages（接 GitHub 自動部署）
> 最後更新：2026-06-30

---

## 一、技術／程式面（已上線 ✅）

這些都已寫進程式碼並部署上線，搜尋引擎可正常讀取。

| 項目 | 內容 | 檔案 |
|------|------|------|
| Sitemap | 自動產生 `/sitemap-index.xml` → `/sitemap-0.xml`，含中英 hreflang | `astro.config.mjs`（`@astrojs/sitemap`） |
| robots.txt | 允許全站索引，指向 sitemap | `public/robots.txt` |
| 正式網址 | `site` 設為 `https://liozu-stay.com`（canonical/OG/sitemap 皆依賴） | `astro.config.mjs` |
| canonical | 每頁自動輸出標準網址 | `src/layouts/BaseLayout.astro` |
| hreflang | zh-Hant／en／x-default 中英互指 | `src/layouts/BaseLayout.astro` |
| Open Graph | 補完 og:url／og:site_name／og:image／og:locale 等 | `src/layouts/BaseLayout.astro` |
| Twitter Card | summary_large_image 大圖卡片 | `src/layouts/BaseLayout.astro` |
| JSON-LD 結構化資料 | `BedAndBreakfast`：名稱、地址、經緯度、地圖、社群、寵物友善、設施 | `src/layouts/BaseLayout.astro` |
| 每頁獨立 description | 5 頁中英各一段含關鍵字描述，集中於 `seo` 區塊管理 | `src/data/content.{zh,en}.json` |
| og:image / 經緯度 | site 區塊新增 `ogImage`、`geo`、`addressLocality/Region/postalCode` | `src/data/content.{zh,en}.json` |
| Cloudflare build 修復 | 重新產生 `package-lock.json`，補回缺漏的 `@emnapi` 套件定義（解決 `npm ci` Missing 錯誤） | `package-lock.json` |

### 線上驗證結果（2026-06-30）
- `https://liozu-stay.com/sitemap-index.xml` → HTTP 200、`application/xml` ✅
- `https://liozu-stay.com/robots.txt` → HTTP 200、`text/plain` ✅
- 首頁含 canonical + hreflang + 新版 meta description ✅

---

## 二、外部設定面

| 項目 | 狀態 | 備註 |
|------|------|------|
| **Google Search Console — 主動要求收錄** | ✅ 已完成（2026-06-30） | 已驗證擁有權、提交 sitemap、要求建立索引 |
| **Google 商家檔案（商家資訊卡）** | ✅ 已完成（2026-06-30） | 強化「留佇民宿」在地搜尋 |
| FB／IG 個人檔案網站欄填官網 | ⬜ 待辦 | 累積指向官網的連結 |
| 第三方平台（booking.com／twstay 等）加官網連結 | ⬜ 待辦 | JSON-LD `sameAs` 已連向 FB/IG/LINE/Booking |

---

## 三、待辦項目（依優先序）

### 1. 強化「留佇」品牌訊號（程式面，可立即做）
- 首頁明確、多次出現「留佇民宿／留佇包棟民宿」全名
- JSON-LD 加 `alternateName`（「留佇」「留佇民宿」），告訴 Google 這些別名都是同一品牌
- 目標關鍵字：**留佇民宿**、**留佇 宜蘭**、**留佇包棟**（單字「留佇」為通用詞，不列為主要目標）

### 2. 專屬 OG 預覽圖
- 目前用 `house.jpg`（堪用）。建議做一張 **1200×630** 含民宿名稱的分享圖 → 放 `public/images/` → 改 `content.*.json` 的 `site.ogImage`

### 3. 圖片優化
- 改用 Astro `<Image>` 元件自動轉 WebP + lazy load，並補齊 `alt` 文字
- 改善 Core Web Vitals（載入速度，排名因素）與圖片搜尋曝光

### 4. 收錄追蹤
- 數日後用 `site:liozu-stay.com` 確認 Google 是否已收錄
- 觀察搜尋「留佇民宿」是否出現官網
- 用 [Rich Results Test](https://search.google.com/test/rich-results) 確認 JSON-LD 被 Google 認得

---

## 四、現況快照（2026-06-30）
- 官網收錄狀態：`site:liozu-stay.com` 尚無結果 → 等待 Google 索引（GSC 已要求收錄，通常數天內）
- 品牌字「留佇民宿」：Google 已知此品牌，但目前指向第三方訂房平台頁，官網收錄後可望取代／並列
