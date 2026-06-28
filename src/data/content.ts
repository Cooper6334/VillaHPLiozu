// 多語資料載入器：中文在 content.zh.json、英文在 content.en.json。
// 一般維護「不用」改這個檔，改對應語言的 content.*.json 即可。
import zh from './content.zh.json';
import enRaw from './content.en.json';

export type Lang = 'zh' | 'en';

// 以中文版的結構為型別基準，確保英文版欄位一致。
const en = enRaw as unknown as typeof zh;
const all = { zh, en };

export interface Room {
  name: string;
  capacity: string;
  count: string;
  description: string;
  features: string[];
  images: string[];
}

export interface Facility {
  name: string;
  description: string;
  images: string[];
}

// 由 Astro.currentLocale 取得語言（預設中文）。
export function getLang(locale?: string | null): Lang {
  return locale === 'en' ? 'en' : 'zh';
}

// 取得對應語言的全部內容。
export function getContent(locale?: string | null) {
  return all[getLang(locale)];
}

// 將內部連結加上語言前綴（中文無前綴，英文加 /en）。
export function localePath(locale: string | null | undefined, href: string): string {
  if (getLang(locale) === 'zh') return href;
  if (href === '/') return '/en/';
  return '/en' + href;
}

// 語言選單清單（給語言切換器用）。
export const languages = [
  { code: 'zh', label: '中文' },
  { code: 'en', label: 'English' },
] as const;
