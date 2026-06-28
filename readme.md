# 如何修改網站內容

全站的**文字**與**圖片連結**都集中在語言對應的檔案：

```
src/data/content.zh.json   ← 中文（預設，網址 / ）
src/data/content.en.json   ← 英文（網址 /en/ ）
```

兩個檔的**結構完全一樣**，只是文字不同。改中文就動 `content.zh.json`，改英文就動 `content.en.json`。
圖片路徑與連結兩邊共用同樣的值即可。平常維護只要改這些檔，**不用碰其他程式碼**。

> 多語：右上角有語言下拉選單（中文／English），預設中文。新增語言請告知。

---

## 改文字
直接修改對應語言檔（如 `content.zh.json`）裡的字串，例如把民宿名稱換掉：

```json
"site": {
  "name": "你的民宿名稱",
  "phone": "0912-345-678",
  ...
}
```

存檔後重新整理瀏覽器（開發模式）或重新建置即可看到變化。

## 換圖片
1. 把照片放進 `public/images/` 資料夾。
2. 在 `content.json` 把對應的 `image` 路徑改成 `/images/你的檔名.jpg`。

對應的圖片欄位：
- 首頁輪播：`home.hero[].image`
- 關於我們：`home.about.image`
- 各房型：`rooms.list[].image`

> 小提醒：上傳前先壓縮（建議寬度 1600px 內），網站才會快。

## 增 / 減房型、特色、須知
這些是「陣列」，可以自由增加或刪除整段 `{ ... }`：
- 房型：`rooms.list`
- 首頁特色：`home.features`
- 入住須知：`booking.notes`

## 介面文字（按鈕、標籤、符號）
全站共用的介面文字都在 `ui` 區塊，例如：
- `bookingButton`：Header 的「線上詢問」按鈕
- `copyright`：頁尾版權字（`{year}` 會自動帶入年份、`{name}` 帶入民宿名稱）
- `prevLabel`/`nextLabel`/`slideLabel`：輪播的無障礙標籤（`{n}` 為第幾張）
- `instagramText`/`facebookText`/`lineShort`：社群連結顯示文字
- `separator`/`titleSeparator`/`labelSeparator`/`featureSeparator`：分隔符號

> 全站已無任何寫死文字，畫面上看得到的字都能在 `content.json` 找到並修改。

## 啟用線上表單
把 Google 表單的嵌入網址貼到 `site.googleFormUrl`，線上詢問頁就會自動顯示表單；留空則顯示電話／LINE 聯絡方式。

---

## 改完怎麼看 / 上線
- 本機預覽：在專案資料夾執行 `npm run dev`，開 http://localhost:4321
- 正式建置：`npm run build`（產出在 `dist/`）

⚠️ JSON 格式注意：每個項目用逗號 `,` 分隔，最後一個項目後面**不要**加逗號；字串要用雙引號 `"`。改完若網站壞掉，多半是這裡少了引號或多了逗號。
