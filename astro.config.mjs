// @ts-check
import { defineConfig } from 'astro/config';

// Astro 預設輸出純靜態網站，最適合部署到 Cloudflare Pages。
// 部署後請把 site 換成你的正式網址（或 *.pages.dev 預覽網址）。
export default defineConfig({
  site: 'https://villawp.pages.dev',
  i18n: {
    defaultLocale: 'zh',
    locales: ['zh', 'en'],
    routing: {
      prefixDefaultLocale: false, // 中文在根路徑（/），英文在 /en/
    },
  },
});
