# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# 專案規則

## Git
- **禁止執行 `git push`**，一律由使用者手動 push。可以 commit，但推送由使用者自行處理。

## 民宿資訊
- 衛浴：每間房皆附獨立衛浴，另有共用廁所一間（英文：Every room has its own private bathroom, plus one shared toilet.）。

# 指令

```bash
npm run dev      # 本機開發伺服器 → http://localhost:4321
npm run build    # 正式建置，產出靜態檔到 dist/
npm run preview  # 預覽 dist/ 的建置結果
```

沒有測試、lint 或 type-check 腳本。型別檢查靠 Astro 在 `astro build` 時自動執行。

# 架構

這是一個 **Astro 7 純靜態網站**（民宿官網），輸出到 `dist/`，預期部署到 Cloudflare Pages。沒有後端、沒有資料庫、沒有 framework UI（無 React/Vue）。所有頁面都是 `.astro` 元件。

## 內容與程式碼分離（核心設計）

全站的**文字與圖片連結**都集中在語言對應的 JSON 檔，**與版面程式碼完全分離**：

```
src/data/content.zh.json   ← 中文（預設，網址 /）
src/data/content.en.json   ← 英文（網址 /en/）
```

- **兩檔結構必須完全一致**，只是語言不同；改一邊的欄位結構，另一邊也要同步，否則型別會對不上。`src/data/content.ts` 以 `content.zh.json` 的型別為基準，把英文版斷言為相同結構。
- 平常維護內容（文字、圖片路徑、增刪房型/特色/須知）**只動 `content.*.json`，不碰其他程式碼**。畫面上所有可見文字（含按鈕、標籤、分隔符號）都來自 `content.*.json` 的 `ui`、`seo` 等區塊，**沒有任何寫死字串**。
- ⚠️ JSON 格式：項目間用逗號分隔、最後一項後**不要**加逗號、字串用雙引號。網站壞掉多半是這裡的引號或逗號問題。

## 多語機制

- i18n 設定在 `astro.config.mjs`：`defaultLocale: 'zh'`、`prefixDefaultLocale: false`，所以中文在根路徑、英文在 `/en/`。
- 頁面以資料夾分流：`src/pages/*.astro`（中文）與 `src/pages/en/*.astro`（英文），兩組頁面結構相同。
- `src/data/content.ts` 提供統一存取函式：
  - `getContent(Astro.currentLocale)` 取得當前語言的全部內容物件。
  - `localePath(locale, href)` 產生帶語言前綴的內部連結（中文無前綴、英文加 `/en`）—— **站內連結一律用它**，不要手寫路徑。
  - `getLang(locale)` 正規化語言碼。

## 頁面與版型

- 所有頁面包在 `src/layouts/BaseLayout.astro` 內。此 layout 集中處理 **SEO**：`<title>`、canonical、中英 `hreflang`、Open Graph、Twitter Card，以及 `BedAndBreakfast` 的 JSON-LD 結構化資料——這些全部由 `content.*.json` 的 `site`/`seo` 欄位驅動。
- 頁面典型開頭：`const c = getContent(Astro.currentLocale)`，再解構出 `home`/`rooms`/`site`/`ui`/`seo` 等區塊渲染。
- 元件在 `src/components/`（Header、Footer、RoomGallery、LanguageSwitcher 等），互動（如首頁輪播）用頁面內 `<script>` 的原生 JS，**不依賴任何前端框架或 jQuery**。

## SEO 注意事項

- `astro.config.mjs` 的 `site` 值（正式網址）是 sitemap、canonical、og:url、JSON-LD 的基準，**上線前務必改成正式網域**，填錯會導致 SEO 失效。
- `@astrojs/sitemap` 會自動產生 `/sitemap-index.xml` 並加上中英 hreflang。

## 線上表單

把 Google 表單嵌入網址填入 `content.*.json` 的 `site.googleFormUrl`，詢問頁會自動顯示表單；留空則顯示電話／LINE 聯絡方式。
