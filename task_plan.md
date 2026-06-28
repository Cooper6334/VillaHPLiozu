# Task Plan: 民宿靜態網站（Astro + Cloudflare Pages）

## Goal
用 Astro 建置一個民宿型錄式靜態網站，部署到 Cloudflare Pages；先不接 Formspree，需要表單時改用 Google 表單（嵌入或連結）。

## Current Phase
Phase 7（等待真實資料 + 部署）

## Phases

### Phase 1: 需求與規劃確認
- [x] 確認技術選型（Astro + Cloudflare Pages）
- [x] 確認內容由使用者自己改程式碼維護（不需 CMS）
- [x] 確認表單策略（先不用 Formspree，需要時用 Google 表單）
- [x] 確認內容資料來源：使用者將提供真實資料（先建框架、佔位，再替換）
- [x] 在 findings.md 記錄需求
- **Status:** complete

### Phase 2: 專案初始化
- [x] 確認本機已安裝 Node.js（v24.13.0 / npm 11.6.2 / git 2.44）
- [x] 安裝 Astro 7.0.3、建立 package.json
- [x] 設定 `.gitignore`、astro.config.mjs、tsconfig.json
- **Status:** complete

### Phase 3: 共用版型與樣式系統
- [x] 建立 BaseLayout（共用 `<head>`、SEO meta、Google Fonts）
- [x] 建立 Header（含手機漢堡選單）與 Footer（地址、電話、LINE、FB、合法編號）
- [x] 樣式方案：原生 CSS（global.css，CSS 變數配色：森林綠 + 暖金）
- [x] 建立全站共用導覽資料（src/data/site.ts）
- **Status:** complete

### Phase 4: 頁面實作（佔位資料，待換真實內容）
- [x] 首頁 / 關於我們（index.astro，含特色、關於、房型預覽）
- [x] 客房介紹（rooms.astro，資料來自 src/data/rooms.ts）
- [x] 訂房資訊（booking.astro）
- [x] 民宿位置（location.astro，含 Google Map 嵌入）
- [x] 線上詢問（contact.astro，可嵌入 Google 表單，未設定時顯示聯絡方式）
- **Status:** complete（內容為佔位，待替換真實資料）

### Phase 5: 互動與表單
- [x] 首頁圖片輪播（原生 JS：自動播放 + 箭頭 + 圓點）
- [x] 手機選單開合（原生 JS）
- [x] 詢問頁：Google 表單嵌入機制 + LINE 詢問按鈕
- **Status:** complete

### Phase 6: 測試與本地預覽
- [x] `npm run build` 成功（5 頁）
- [x] `npm run preview`：首頁/房型/詢問頁皆 HTTP 200，title 正確
- [ ] 待真實內容與圖片後再做 RWD / 連結 / alt 最終檢查
- **Status:** in_progress

### Phase 7: 部署與網域
- [ ] 推到 GitHub
- [ ] 連接 Cloudflare Pages 自動部署
- [ ] 取得 *.pages.dev 預覽網址
- [ ] （後續）綁定自訂網域 + DNS
- **Status:** pending（需使用者的 GitHub / Cloudflare 帳號）

## Key Questions
1. 內容用真實資料、範例資料、還是參考站改寫？（待確認）
2. 樣式用原生 CSS 還是 Tailwind？（Phase 3 決定）
3. 網域要不要現在買、買哪個（.com / .com.tw）？（Phase 7）

## Decisions Made
| Decision | Rationale |
|----------|-----------|
| Astro | 內容型網站主流、元件化好維護、預設零 JS、SEO 佳；使用者有 HTML/JS/DOM 基礎上手快 |
| Cloudflare Pages | 免費、台灣連線快、自動 HTTPS、自動部署 |
| 不用 Formspree，改 Google 表單 | 使用者要求；Google 表單免費、零維護、可嵌入或連結 |
| 不用 CMS | 使用者會自己改程式碼，內容不常變動 |
| 建議用原生 JS 取代 jQuery | 現代瀏覽器原生 API 已足夠，少載一個函式庫 |

## Errors Encountered
| Error | Attempt | Resolution |
|-------|---------|------------|
|       | 1       |            |

## Notes
- 內容資料來源尚未確定，Phase 2-4 可先用範例資料 + 佔位圖建立框架，之後替換。
- 決策前重讀本計畫；所有錯誤記錄於此。
