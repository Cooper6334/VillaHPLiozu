// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// Astro 預設輸出純靜態網站，最適合部署到 Cloudflare Pages。
// ⚠️ 上線前必改：把 site 換成你的正式網址（自訂網域或 *.pages.dev）。
// sitemap、canonical、og:url、JSON-LD 全都依賴這個值，填錯會導致 SEO 失效。
export default defineConfig({
  site: 'https://liozu-stay.com',
  i18n: {
    defaultLocale: 'zh',
    locales: ['zh', 'en'],
    routing: {
      prefixDefaultLocale: false, // 中文在根路徑（/），英文在 /en/
    },
  },
  integrations: [
    // 自動產生 /sitemap-index.xml，並依 i18n 設定加上中英 hreflang 連結。
    sitemap({
      i18n: {
        defaultLocale: 'zh',
        locales: { zh: 'zh-Hant', en: 'en' },
      },
    }),
  ],
});
