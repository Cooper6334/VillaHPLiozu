# Progress Log

## Session: 2026-06-28

### Phase 1: 需求與規劃確認
- **Status:** in_progress
- **Started:** 2026-06-28
- Actions taken:
  - 透過 brainstorming 釐清需求：靜態民宿網站、自己改程式碼、只要詢問表單
  - 看過參考站結構（5 頁：關於/房型/訂房/位置/詢問）
  - 確定技術選型：Astro + Cloudflare Pages
  - 確定表單策略：先不用 Formspree，需要時改 Google 表單
  - 說明 Astro 概念與成本（唯一必要花費為網域年費）
  - 建立規劃檔案
- 待確認：內容資料來源（真實 / 範例 / 參考站改寫）
- Files created/modified:
  - task_plan.md (created)
  - findings.md (created)
  - progress.md (created)

### Phase 2-6: 建置框架與頁面
- **Status:** complete（內容佔位，待真實資料）
- Actions taken:
  - 安裝 Astro 7.0.3
  - 建立設定：astro.config.mjs、tsconfig.json、.gitignore
  - 資料層：src/data/site.ts、src/data/rooms.ts
  - 共用：BaseLayout、Header（手機選單）、Footer
  - 樣式：src/styles/global.css（原生 CSS、CSS 變數）
  - 五頁：index / rooms / booking / location / contact
  - 首頁原生 JS 輪播、contact 頁 Google 表單嵌入機制
  - npm run build 成功；preview 三頁 HTTP 200
- Files created/modified: 見 src/ 與 public/

### 排版改版（依參考站 hxybnb）
- **Status:** complete
- Actions taken:
  - 抓參考站 HTML + style.css + pages.css 分析排版（記於 findings.md）
  - global.css 改極簡黑白灰：#000/#fff/灰、Cormorant Unicase + Noto Sans TC、寬字距、白底黑框按鈕
  - Header 改細緻極簡（左 logo + 細線 nav + 詢問鈕 + 漢堡）
  - Footer 改細線置中極簡
  - 新增 SideSocial（固定側邊社群 + 回頂端）
  - 首頁：滿版 hero 輪播 + topInfo 白塊上移 + about 圖文重疊 + 房型預覽
  - 房型頁：左圖右文 + 上下細線框 detail
  - 訂房頁：regu 細線標題框
  - 位置頁：地圖 + 細線雙欄
  - 詢問頁：表格式聯絡資訊（Google 表單未設定時的樣式）
  - npm run build 成功（5 頁）
- Files: global.css, BaseLayout, Header, Footer, SideSocial(新), 5 個 pages

### 內容集中化（單一 content.json）
- **Status:** complete
- Actions taken:
  - 建立 src/data/content.json：全站文字 + 圖片連結集中於此（site/nav/home/rooms/booking/location/contact）
  - 建立 src/data/content.ts 載入器（型別 + 具名匯出）
  - 刪除舊的 site.ts、rooms.ts
  - 五頁 + 4 元件全改從 content 讀取，移除所有寫死文字
  - 新增「如何修改網站內容.md」編輯說明
  - build 成功；grep 驗證 JSON 內容（房內泡湯/玻璃屋景觀房/訂房步驟）有渲染進 dist
- Files: content.json(新), content.ts(新), 如何修改網站內容.md(新), 刪 site.ts/rooms.ts, 改全部 pages+components

### 首頁調整：移除房型預覽、加入地圖+資訊
- **Status:** complete
- Actions taken:
  - index.astro 移除「精選房型」區段（含 CSS）
  - 比照參考站，新增「交通位置」區：Google Map iframe + 民宿資訊（地址/電話/LINE/登記編號）+ 更多交通資訊按鈕
  - content.json：移除未使用的 home.roomsPreview，新增 home.map（eyebrow/heading/note/buttonText）
  - build 成功；grep 驗證首頁無「精選房型」、含地圖 iframe 與資訊
- Files: index.astro, content.json

### 移除 phone、新增 instagram
- **Status:** complete
- Actions taken:
  - content.json site：刪 phone / phoneHref，新增 instagram；booking.steps[0] 電話→Instagram；contact.infoLabels phone→instagram，新增 instagramText
  - 所有原顯示電話處改為 Instagram：Header、Footer、SideSocial(TEL→IG)、booking、location、index map-info、contact
  - grep 確認 src 無 phone 殘留；build 成功；dist 無 tel: 連結、含 instagram 連結
- Files: content.json, Header, Footer, SideSocial, booking, location, index, contact

### 佔位字修正 + 全文字集中化（零寫死文字）
- **Status:** complete
- Actions taken:
  - content.json：home.intro.subheading ○○→「留佇包棟民宿」
  - 新增 ui 區塊：按鈕/版權/aria 標籤/輪播標籤/地圖標題/社群文字(IG/FB/LINE)/分隔符號/箭頭圖示
  - 新增 home.about.imageLabel、home.map.labels、rooms.itemEyebrow、contact.formTitle/loadingText/formHint
  - content.ts 匯出 ui
  - 全部 .astro（Header/Footer/SideSocial/BaseLayout/5 pages）改吃 content，移除所有寫死文字與符號
  - grep 最終掃描：.astro 內已無任何寫死中文/符號（©/｜/·/：/、/↑/‹/› 皆來自 ui）
  - build 成功；dist 驗證副標無 ○○、版權含真實名稱
- Files: content.json, content.ts, 全部 components + pages

### 頁尾社群列改 icon
- **Status:** complete
- Actions taken:
  - 新增 SocialIcons.astro（內嵌 LINE/FB/IG 品牌 SVG，圓形外框 hover 反白，aria-label 取自 ui）
  - Footer 以 <SocialIcons /> 取代原文字社群列（LINE id · Facebook · Instagram）
  - build 成功；dist 驗證頁尾 3 個 svg、無文字 Facebook 殘留、保留 aria-label
- Files: SocialIcons.astro(新), Footer.astro

### 移除 header 與首頁交通位置的 IG
- **Status:** complete
- Actions taken:
  - Header 移除 Instagram 連結（保留線上詢問按鈕）
  - index 首頁「交通位置」info 區移除 IG 列（保留地址/LINE/編號）
  - build 成功；驗證 header 無 instagram、首頁 IG 連結剩 2（頁尾 icon + 左側固定鈕，屬保留）
  - 備註：content.json 的 home.map.labels.instagram 已不再使用但保留（資料無害）
- Files: Header.astro, index.astro

### 側邊固定按鈕改 icon + 移到右側
- **Status:** complete
- Actions taken:
  - 新增共用 Icon.astro（line/facebook/instagram SVG），SocialIcons 改用它（消除重複 SVG）
  - SideSocial 文字(LINE/FB/IG)→Icon SVG；定位 left:0→right:0
  - build 成功；驗證 dist CSS .side-social 為 right:0、無 left:0；側邊按鈕無文字
- Files: Icon.astro(新), SocialIcons.astro, SideSocial.astro

### 置頂列 logo 取代文字
- **Status:** complete
- Actions taken:
  - 從 images/Logo 橫式 JPG 用 PIL 將白底轉透明 + 去邊，輸出 public/images/logo.png（藍字橫式，1345×839）
  - content.json 新增 site.logo = /images/logo.png
  - Header brand 改用 <img class="brand-logo">（height 48px，手機 38px），移除文字品牌
  - build 成功；dist 含 logo.png、brand 用圖片、無文字品牌殘留
  - 備註：真實照片在專案根目錄 images/（LINE 相簿 20 張），日後可放入 public/images/ 作 hero/房型/about
- Files: public/images/logo.png(新), content.json, Header.astro

### 客房介紹改為包棟民宿
- **Status:** complete
- Actions taken:
  - content.json rooms：新增 summary（包棟說明：僅整棟出租不單租 / 7 間雙人房 / 3 間可加沙發床 / 可住 14 人）
  - labels price→count（房間數）；list 改 2 房型（雙人房×4、雙人房可加沙發床×3），移除單間房價
  - content.ts Room 介面 price→count
  - rooms.astro 新增「包棟說明」細線區塊；detail 列 price→count；buttonText「包棟詢問」
  - build 成功；驗證含包棟說明/7 間/3 間沙發床/不單租、無 NT$ 殘留
- Files: content.json, content.ts, rooms.astro

### 客房頁列出 7 間房 + 加床每間+2人
- **Status:** complete
- Actions taken:
  - summary 可住人數：基本 14 人，3 間各加沙發床(+2)最多 20 人
  - rooms.list 改為 7 間獨立房（雙人房 01-04 標準、05-07 可加沙發床 2–4 人）
  - labels count→bed（床型/加床）；content.ts Room 介面 count→bed；rooms.astro detail 列改 bed
  - 圖片路徑 room-1.jpg … room-7.jpg
  - build 成功；驗證 7 張房卡、ROOM 07、3 間可加沙發床
- Files: content.json, content.ts, rooms.astro

### 客房改回 2 種房型
- **Status:** complete
- Actions taken:
  - rooms.list 改 2 筆：房型1 大房間(沙發床,3–4人,3間,roomlarge1)、房型2 一般房(2人,4間,room1)
  - labels bed→count(房間數)；content.ts Room bed→count；rooms.astro detail 用 count
  - summary 對齊：房型1×3+房型2×4=7 間、最多 20 人；itemEyebrow→ROOM TYPE
  - 移除獨立衛浴（前次）；build 成功，驗證 2 張房型卡、無舊 7 房殘留
- Files: content.json, content.ts, rooms.astro

### 房型照片輪播 + 縮圖
- **Status:** complete
- Actions taken:
  - content.json 房型 image(字串)→images(陣列)：房型1 roomlarge1-3、房型2 room1-4
  - content.ts Room image→images:string[]
  - 新增 RoomGallery.astro：主圖輪播(箭頭) + 下方縮圖取代點點，縮圖高亮目前照片、可點切換；每個 gallery 獨立 JS
  - rooms.astro 用 <RoomGallery>，room-photo→room-media（含 reverse 排序與 RWD）
  - build 成功；驗證主圖 7 張、縮圖 7 個
- Files: content.json, content.ts, RoomGallery.astro(新), rooms.astro

### 客房介紹→設施介紹 + 公共設施
- **Status:** complete
- Actions taken:
  - nav 與頁面標題「客房介紹」→「設施介紹」(eyebrow FACILITIES)
  - 房型上方加「房型」小標(sectionTitle/sectionEyebrow)
  - content.json 新增 facilities：客廳(含卡拉OK,livingroom1-2)、兒童遊戲區(childplace)、戶外泳池(pool/pool_2/pool_3)
  - content.ts 加 Facility 型別 + facilities/facilitiesContent 匯出
  - rooms.astro 在房型下方加「公共設施」區，沿用 .room 排版 + RoomGallery（只有 名稱+描述）
  - build 成功；驗證標題/選單/三設施/泳池圖
- Files: content.json, content.ts, rooms.astro

### 多語功能（中/英）
- **Status:** complete
- Actions taken:
  - astro.config i18n：defaultLocale zh、locales [zh,en]、prefixDefaultLocale false（中文 /，英文 /en/）
  - content.json→content.zh.json；新增 content.en.json（全文翻譯，結構一致）
  - content.ts 改 getContent(locale)/getLang/localePath/languages，保留 Room/Facility 型別
  - 新增 LanguageSwitcher.astro（右上 <details> 下拉，連到對應語言同頁；點外面收合）
  - Header/Footer/BaseLayout/SideSocial/SocialIcons/RoomGallery 改 getContent(Astro.currentLocale)；內部連結用 localePath 加 /en 前綴；html lang 動態
  - 新增 src/pages/en/*.astro 五個薄包裝（import 中文頁，依 /en/ 自動切英文）
  - build 成功 10 頁；驗證 /en 出英文、/ 出中文無洩漏、nav 與語言切換連結正確、html lang=en
- Files: astro.config.mjs, content.zh.json(改名), content.en.json(新), content.ts, LanguageSwitcher.astro(新), 全部 components+pages, en/*.astro(新5)

## Test Results
| Test | Input | Expected | Actual | Status |
|------|-------|----------|--------|--------|
| 建置 | npm run build | 成功產生 5 頁 | 5 page(s) built | ✓ |
| 首頁 | GET / | 200 | 200，title 正確 | ✓ |
| 房型頁 | GET /rooms/ | 200 | 200 | ✓ |
| 詢問頁 | GET /contact/ | 200 | 200 | ✓ |

## Error Log
| Timestamp | Error | Attempt | Resolution |
|-----------|-------|---------|------------|
|           |       | 1       |            |

## 5-Question Reboot Check
| Question | Answer |
|----------|--------|
| Where am I? | Phase 1（需求與規劃確認） |
| Where am I going? | Phase 2 專案初始化 → 版型 → 頁面 → 部署 |
| What's the goal? | Astro 民宿靜態網站，部署 Cloudflare Pages |
| What have I learned? | 見 findings.md |
| What have I done? | 見上方 Phase 1 紀錄 |

---
*Update after completing each phase or encountering errors*
