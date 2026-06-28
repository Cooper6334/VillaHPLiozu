# 圖片放這裡

把民宿照片放在這個資料夾，網站就能用 `/images/檔名` 引用。

建議檔名（對應目前程式碼，放進來後把對應的佔位 `<div>` 換成 `<img>`）：

- 首頁輪播：`hero-1.jpg`、`hero-2.jpg`、`hero-3.jpg`
- 房型照片：`room-double.jpg`、`room-family.jpg`、`room-glass.jpg`、`room-villa.jpg`

小提醒：
- 上傳前先壓縮（建議寬度 1600px 內、用 https://squoosh.app 轉成 .webp 或壓過的 .jpg），網站才會快。
- 房型照片檔名要和 `src/data/rooms.ts` 裡的 `image` 欄位一致。
