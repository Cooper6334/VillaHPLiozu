# 這個資料夾只放「原樣輸出」的圖片

一般民宿照片請放 **`src/assets/images/`**（建置時會自動壓縮、轉 WebP、產生多尺寸），
`content.json` 內的路徑仍寫 `/images/檔名.jpg`，不用改寫法。

只有「網址必須固定、不能被壓縮改名」的檔案才放這裡：

- `og-cover.jpg`：社群分享（FB／LINE）預覽圖，網址固定為 `/images/og-cover.jpg`
- `line-qr.png`：LINE QR code

詳細說明見專案根目錄的 `readme.md`。
