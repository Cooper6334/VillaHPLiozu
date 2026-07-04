// 圖片解析器：把 content.json 裡的 "/images/xxx.jpg" 路徑
// 對應到 src/assets/images/ 的實體檔案，交給 astro:assets 做壓縮／WebP／srcset。
// content.json 的寫法維持不變，新增圖片時把檔案放進 src/assets/images/ 即可。
import type { ImageMetadata } from 'astro';

const modules = import.meta.glob<{ default: ImageMetadata }>(
  '../assets/images/*.{jpg,jpeg,png,webp,avif}',
  { eager: true }
);

export function resolveImage(path: string): ImageMetadata {
  const key = path.replace(/^\/images\//, '../assets/images/');
  const mod = modules[key];
  if (!mod) {
    throw new Error(
      `找不到圖片：${path}（請確認 src/assets/images/ 內有對應檔案）`
    );
  }
  return mod.default;
}
