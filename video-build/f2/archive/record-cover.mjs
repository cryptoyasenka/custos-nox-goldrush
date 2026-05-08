import { chromium } from 'playwright-chromium';
import { fileURLToPath } from 'url';
import path from 'path';
import fs from 'fs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const browser = await chromium.launch({ args: ['--no-sandbox'] });
const ctx = await browser.newContext({
  viewport: { width: 1920, height: 1080 },
  recordVideo: { dir: __dirname, size: { width: 1920, height: 1080 } }
});
const page = await ctx.newPage();
const filePath = path.resolve(__dirname, 'cover.html');
await page.goto(`file:///${filePath.replace(/\\/g, '/')}`);

let done = false;
const deadline = Date.now() + 7000;
while (Date.now() < deadline && !done) {
  await page.waitForTimeout(500);
  if (await page.title() === 'COVER_DONE') done = true;
}
await page.waitForTimeout(500);

const vp = await page.video()?.path();
await ctx.close();
await browser.close();

if (vp && fs.existsSync(vp)) {
  fs.renameSync(vp, path.resolve(__dirname, 'cover.webm'));
  console.log('✓ cover.webm saved');
} else {
  console.error('✗ no video found');
}
