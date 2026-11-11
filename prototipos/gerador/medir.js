// Mede a altura de cada artboard (para o quadro do canvas) e verifica rolagem horizontal da página em 390 px (CO02).
// Uso: node medir.js <lista.json> <saida.json>
const fs = require('fs');
const { chromium } = require('playwright');

(async () => {
  const [lista, saida] = process.argv.slice(2);
  const itens = JSON.parse(fs.readFileSync(lista, 'utf8'));
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1 });
  await page.route('**/*', r => (r.request().url().startsWith('data:') ? r.continue() : r.abort()));
  const out = {};
  for (const it of itens) {
    const html = fs.readFileSync(it.path, 'utf8').replace('__H__', '900');
    await page.setViewportSize({ width: it.w, height: 900 });
    await page.setContent(html, { waitUntil: 'domcontentloaded' });
    const h = await page.evaluate(() => Math.ceil(document.documentElement.scrollHeight));
    let overflow390 = null;
    if (it.w > 400) {
      await page.setViewportSize({ width: 390, height: 844 });
      overflow390 = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
      if (overflow390 > 0) {
        out[it.file + '#culpado'] = await page.evaluate(() => {
          const r = [];
          for (const el of document.querySelectorAll('body *')) {
            const b = el.getBoundingClientRect();
            if (b.right > window.innerWidth + 1 && b.width > 0 && (!el.checkVisibility || el.checkVisibility()) && !el.closest('[style*="overflow-x:auto"]')) r.push([b.right|0, el.tagName, (el.getAttribute('style')||'').slice(0,80), (el.textContent||'').trim().slice(0,60)]);
          }
          r.sort((a,b)=>a[0]-b[0]);
          return r.slice(0,4);
        });
      }
    } else {
      overflow390 = await page.evaluate(() => document.documentElement.scrollWidth - 390);
    }
    out[it.file] = { h, overflow390 };
  }
  await browser.close();
  fs.writeFileSync(saida, JSON.stringify(out, null, 1));
})();
