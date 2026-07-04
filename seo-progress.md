# SEO 優化進度

> 網站：留佇包棟民宿　https://liozu-stay.com
> 平台：Astro 靜態網站 + Cloudflare Pages（接 GitHub 自動部署）
> 最後更新：2026-07-04

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
| 圖片優化（2026-07-04，待上線） | 全站改 astro:assets `<Image>`：WebP＋srcset＋lazy，hero 首圖 fetchpriority=high，logo 513KB→4KB | `src/data/images.ts`、`index.astro`、`RoomGallery.astro`、`Header.astro`、`BaseLayout.astro` |

### 線上驗證結果（2026-06-30）
- `https://liozu-stay.com/sitemap-index.xml` → HTTP 200、`application/xml` ✅
- `https://liozu-stay.com/robots.txt` → HTTP 200、`text/plain` ✅
- 首頁含 canonical + hreflang + 新版 meta description ✅

### 修正 GSC「頁面會重新導向」（2026-07-04）
**問題**：GSC 通知「有新的原因導致網頁無法建立索引 → 頁面會重新導向」。

**根因**：sitemap／canonical／伺服器實際 200 的網址都用**結尾斜線**（`/rooms/`），但站內導覽連結（nav／Footer／按鈕）產生的是**無斜線**網址（`/rooms`），被伺服器 308 導向到有斜線版。Google 沿站內連結爬到無斜線網址 → 遇導向 → 報「頁面會重新導向」。

**線上導向行為（curl 驗證）**：
- `http://…/` → 301 → https（正常）
- `https://…/rooms`（無斜線）→ 308 → `/rooms/`
- `https://…/rooms/`（有斜線）→ 200 ✅
- `www.liozu-stay.com` → 連不上（未設定，暫無外部連結指向，先不處理）

**修正內容**：
| 項目 | 內容 | 檔案 |
|------|------|------|
| 內部連結補斜線 | `localePath()` 一律回傳結尾斜線網址，站內連結直接指向 200 頁面 | `src/data/content.ts` |
| 固定斜線策略 | 加 `trailingSlash: 'always'`，避免日後又寫出無斜線連結 | `astro.config.mjs` |

**驗證**：`npm run build` 後，10 頁站內連結全部為有斜線（`/rooms/`、`/en/rooms/`…）✅

**待辦**：
- ⬜ commit + push → 等 Cloudflare Pages 部署
- ⬜ GSC 該報告頁按「驗證修正」(Validate Fix)，等 Google 重新爬取轉綠
- ⬜（選配）Cloudflare 加 `www → 主網域` 301

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

### 1. 強化「留佇」品牌訊號 ✅ 已完成（2026-06-30）
- 首頁 h1 由「留佇 · 宜蘭冬山」改為「**留佇民宿** · 宜蘭冬山」，品牌全名更明確（英文同步改為 `Liozu Villa · Dongshan, Yilan`）
- JSON-LD 加入 `alternateName` 別名，告訴 Google 這些都是同一品牌：
  - 中文：`["留佇", "留佇民宿", "留佇包棟"]`
  - 英文：`["Liozu", "留佇", "留佇民宿", "Liozu B&B"]`
  - 對應檔案：`src/data/content.{zh,en}.json` 的 `site.alternateName`、`src/layouts/BaseLayout.astro`
- 目標關鍵字：**留佇民宿**、**留佇 宜蘭**、**留佇包棟**（單字「留佇」為通用詞，不列為主要目標）
- 狀態：本機建置驗證通過，**待 commit／push 上線**

### 2. 專屬 OG 預覽圖 ✅ 已完成
- `public/images/og-cover.jpg` 已建立並設定於 `content.*.json` 的 `site.ogImage`

### 3. 圖片優化 ✅ 已完成（2026-07-04，待 commit/push 上線）
- 19 張內容圖片搬到 `src/assets/images/`，新增 `src/data/images.ts` 解析器（`content.json` 路徑寫法 `/images/xxx.jpg` 不變）
- 全站 `<img>` 改用 astro:assets `<Image>`：自動轉 **WebP** + **srcset 多尺寸**（手機載小圖）+ **lazy load**
- 首頁 hero 首圖 `loading="eager"` + `fetchpriority="high"`（改善 LCP），其餘輪播圖與 about 圖 lazy
- Header logo：513KB PNG → 4KB WebP（@1x，另有 2x/3x 版本）；JSON-LD 的 logo 改指向縮小版
- 例外保留於 `public/images/`：`og-cover.jpg`（OG 網址須固定）、`line-qr.png`
- alt 文字：全站圖片皆有 alt（來自 content.json 的標題/說明；縮圖為裝飾性 alt=""）
- 驗證：build 10 頁 + 88 個 webp 變體；preview 全頁 200；hero 首圖含 fetchpriority=high
- 維護方式改變：新照片放 `src/assets/images/`（不用先手動壓縮），詳見 `readme.md`

### 4. 收錄追蹤
- 數日後用 `site:liozu-stay.com` 確認 Google 是否已收錄
- 觀察搜尋「留佇民宿」是否出現官網
- 用 [Rich Results Test](https://search.google.com/test/rich-results) 確認 JSON-LD 被 Google 認得

---

## 四、現況快照（2026-06-30）
- 官網收錄狀態：`site:liozu-stay.com` 尚無結果 → 等待 Google 索引（GSC 已要求收錄，通常數天內）
- 品牌字「留佇民宿」：Google 已知此品牌，但目前指向第三方訂房平台頁，官網收錄後可望取代／並列
