# Villawp

留佇包棟民宿官網 `https://liozu-stay.com`。**Astro 7 靜態站**（名字有 wp 但不是 WordPress），
中英雙語，部署在 Cloudflare Pages（接 GitHub 自動部署）。

---

## 文件正本＝Obsidian vault

**架構、SEO、內容結構一律以 vault 為準：`../memo/Villa/`**

動工前先讀 `../memo/Villa/Villawp/Villawp.md`。

> ⚠️ **不要把知識抄回這個檔案。** CLAUDE.md 只放工作規則與導航。

### 改動前必讀

| 你要改什麼 | 先讀 |
|-----------|------|
| 網站文字／圖片 | `../memo/Villa/Villawp/元件/content JSON 內容層.md` |
| SEO／canonical／hreflang／JSON-LD | `../memo/Villa/Villawp/元件/BaseLayout 與 SEO.md` |
| 訂房表單 | `../memo/Villa/Villawp/元件/BookingForm.md`（換表單要同時改兩處） |
| 中英雙語 | `../memo/Villa/Villawp/概念/i18n 中英雙語.md` |
| AI 曝光度測試 | `../memo/Villa/Villawp/概念/AI 曝光度測試.md`（改題目要升版號） |
| 某一頁 | `../memo/Villa/Villawp/頁面/*.astro.md` |

---

## Git

- **禁止執行 `git push`**，一律由使用者手動 push。
- **commit 基本上由使用者操作**，除非使用者直接下令，否則不要主動 `git commit`。

---

## 常用命令

```bash
npm run dev      # astro dev
npm run build    # astro build
npm run preview  # astro preview
```

---

## 改內容不用碰程式碼

全站文字與圖片路徑集中在 `src/data/content.zh.json` 與 `content.en.json`。
兩檔**結構完全一樣**，只是文字不同。平常維護只改這兩個檔。

- 改版面才要動 `.astro` —— 中英是**實體兩份檔**（`src/pages/xxx.astro` 與 `src/pages/en/xxx.astro`），要改兩邊。
- 換圖：照片丟進 `src/assets/images/`，content 裡路徑寫 `/images/檔名.jpg`。
  **不需要先壓縮**，建置時自動轉 WebP 並產生多種尺寸。

---

## 兩個不能填錯的設定

都在 `astro.config.mjs`：

| 設定 | 值 | 填錯會怎樣 |
|------|-----|-----------|
| `site` | `https://liozu-stay.com` | sitemap／canonical／og:url／JSON-LD **全部依賴它**，錯了 SEO 整組失效 |
| `trailingSlash` | `'always'` | 站內連結被 308 導向，GSC 報「頁面會重新導向」而不索引 |

---

## 進度與待辦

- `todo.md` — 零散待辦
- `seo-progress.md` — SEO 工程進度與線上驗證結果
- `task_plan.md` / `findings.md` / `progress.md` — planning-with-files 規劃檔
- `readme.md` — 寫給**非工程師**看的「如何修改網站內容」，改動網站結構時記得同步
