# Findings & Decisions

## Requirements
<!-- Captured from user request -->
- 靜態民宿網站，風格參考 https://tw-bnb.com/web/hxybnb/index.php?page=about.php
- 技術：Astro + Cloudflare Pages
- 內容由使用者自己改程式碼維護（不需要 CMS / 後台）
- 只需要詢問表單，不需要線上付款 / 即時空房系統
- 先不用 Formspree；需要表單時改用 Google 表單功能
- 使用者技能背景：JavaScript、jQuery、HTML5 DOM（建議改用原生 JS）

## 參考站結構（懷鄉園泡湯民宿）
五個主要頁面：
- 關於我們（about）
- 客房介紹（rooms）
- 訂房資訊（booking-info）
- 民宿位置（location）
- 線上詢問（contact，表單）

主要元素：
- 特色文案（泡湯浴缸、獨棟庭園別墅、玻璃屋、戶外烤肉）
- 線上詢問表單
- 訂房系統連結
- 聯絡方式：電話、LINE、Facebook
- 頁尾資訊：營業地址、合法民宿編號

## 參考站排版分析（hxybnb，2026-06-28 抓 HTML+CSS 分析）
風格：極簡黑白灰精品民宿風
- 配色：#000 / #fff / 灰階 #333 #8d8d8d #d0d0d0；無彩色
- 字型：英文標題 'Cormorant Unicase' serif；中文 微軟正黑體
- 寬字距 letter-spacing 2–8px、寬行高、大量留白
- 容器寬 1000–1170px 置中
版面結構（由上到下）：
1. 固定側邊社群按鈕（sideSocial）+ 回頂端（goTop）
2. Header：置中大 logo + phoneBox + bookingBox + bars(漢堡)
3. Hero jumbo2：滿版大圖 820px（手機 400px）
4. topInfo：白色區塊 margin-top:-100px 蓋住 hero、置中、h2 斜體大標 + Cormorant 英文小標 + 左對齊介紹文
5. aboutBox：大圖 750x500 + 白底文字框 absolute 疊在圖右下角（圖文重疊）
6. stay 房型：stayLeft 圖 61.5% + stayRight 文字 30%，roomInfo 上下 1px 黑線框
7. roomPic：大圖 1000x600 + 下方縮圖列（每張 15.6% 橫排）
8. regu 須知：reguTitle 小框（上下框線）
9. bookingForm：table 式，input 只有 border-bottom 底線，submit hover 變黑
10. footer shopInfo + 社群 + copyRight
設計語彙：1px 細線分隔/裝飾、按鈕白底黑框→hover 黑底白字、圖文重疊、滿版大圖

## Technical Decisions
| Decision | Rationale |
|----------|-----------|
| Astro 框架 | 內容導向網站主流、元件化、預設零 JS、SEO 佳 |
| Cloudflare Pages 部署 | 免費、台灣節點快、自動 HTTPS + 自動部署 |
| Google 表單收詢問 | 免費、零維護、可嵌入 iframe 或外連 |
| 原生 JS 取代 jQuery | 減少相依、現代 API 已足夠 |

## Issues Encountered
| Issue | Resolution |
|-------|------------|
|       |            |

## Resources
- 參考站：https://tw-bnb.com/web/hxybnb/index.php?page=about.php
- Astro 官方文件：https://docs.astro.build
- Cloudflare Pages + Astro 指南：https://developers.cloudflare.com/pages/framework-guides/deploy-an-astro-site/
- 專案目錄：C:\code\villawp

## 成本概要
- 必要：網域年費約 NT$300–600（.com）/ NT$800–1000（.com.tw），可選
- 其餘（開發工具、主機、HTTPS、Google 表單）全免費
- 最省：用 *.pages.dev 免費網址 → 0 元上線

---
*Update this file after every 2 view/browser/search operations*
