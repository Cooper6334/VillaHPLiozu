// Cloudflare Pages Function：讀取 Google 日曆的 iCal（.ics）feed，
// 解析出「已訂日期」回傳 JSON 給前端月曆。只回傳日期、不含事件標題（保護隱私）。
//
// 設定：在 Cloudflare Pages → Settings → Environment variables 新增
//   ICAL_URL = 你的 Google 日曆「iCal 格式的私密網址」或公開 iCal 網址
// （Google 日曆 → 設定 → 該日曆 → 整合日曆 → 私密網址（iCal 格式））

export async function onRequest(context) {
  const { env } = context;
  const headers = {
    'content-type': 'application/json; charset=utf-8',
    'access-control-allow-origin': '*',
    // 邊緣快取 5 分鐘，兼顧即時與流量
    'cache-control': 'public, max-age=300',
  };

  const icalUrl = env && env.ICAL_URL;
  if (!icalUrl) {
    return new Response(JSON.stringify({ configured: false, booked: [] }), { headers });
  }

  try {
    const res = await fetch(icalUrl, { cf: { cacheTtl: 300, cacheEverything: true } });
    if (!res.ok) throw new Error('ical fetch failed: ' + res.status);
    const text = await res.text();
    const booked = parseBookedDates(text);
    return new Response(
      JSON.stringify({ configured: true, booked, updated: new Date().toISOString() }),
      { headers }
    );
  } catch (err) {
    return new Response(
      JSON.stringify({ configured: true, booked: [], error: String(err) }),
      { status: 200, headers }
    );
  }
}

// 解析 iCal 文字 → 已訂日期陣列（YYYY-MM-DD）
function parseBookedDates(ics) {
  // 處理折行（以空白/Tab 開頭的續行）
  const unfolded = ics.replace(/\r?\n[ \t]/g, '');
  const lines = unfolded.split(/\r\n|\n|\r/);

  const booked = new Set();
  let cur = null;
  for (const line of lines) {
    if (line === 'BEGIN:VEVENT') {
      cur = {};
    } else if (line === 'END:VEVENT') {
      // 過濾掉標題包含「小幫手」的事件（例如工作人員排班，非實際訂房）
      if (cur && cur.start && !(cur.summary && cur.summary.includes('小幫手'))) {
        addRange(booked, cur);
      }
      cur = null;
    } else if (cur) {
      if (line.startsWith('DTSTART')) {
        const p = parseDt(line);
        cur.start = p.date;
        cur.allDay = p.allDay;
      } else if (line.startsWith('DTEND')) {
        cur.end = parseDt(line).date;
      } else if (line.startsWith('SUMMARY')) {
        cur.summary = line.slice(line.indexOf(':') + 1);
      }
    }
  }
  return Array.from(booked).sort();
}

function parseDt(line) {
  const value = line.slice(line.indexOf(':') + 1).trim();
  const allDay = /VALUE=DATE(?!-TIME)/.test(line) || /^\d{8}$/.test(value);
  const y = value.slice(0, 4);
  const m = value.slice(4, 6);
  const d = value.slice(6, 8);
  return { date: `${y}-${m}-${d}`, allDay };
}

function addRange(set, ev) {
  const DAY = 24 * 3600 * 1000;
  const s = Date.parse(ev.start + 'T00:00:00Z');
  let e = ev.end ? Date.parse(ev.end + 'T00:00:00Z') : s;
  // 全天事件的 DTEND 為「不含」當天（住宿：start..end-1 為入住的夜晚）
  if (ev.allDay && ev.end) e -= DAY;
  if (isNaN(s)) return;
  for (let t = s; t <= e; t += DAY) {
    set.add(new Date(t).toISOString().slice(0, 10));
  }
}
