import { chromium } from 'playwright-chromium';
import { fileURLToPath } from 'url';
import path from 'path';
import fs from 'fs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const DECK_PATH = path.resolve(__dirname, '../../assets/pitch-slides/deck-v2.html');

const SLIDE_DURATIONS_MS = [
  16000, // s1: $285M count-up + voice ~14s
  16000, // s2: stagger + Chainalysis facts
  14000, // s3: 10000+ count-up + gap claim
  13000, // s4: detector cards stagger
  14000, // s5: 200+ count-up + stakes line
  14000, // s6: setup steps + GTM mention
  12000, // s7: vision rows
  10000, // s8: CTA close
];
// Total = 109 sec silent video (~1:49)

if (!fs.existsSync(DECK_PATH)) {
  console.error('✗ deck not found at', DECK_PATH);
  process.exit(1);
}

const browser = await chromium.launch({ args: ['--no-sandbox'] });
const ctx = await browser.newContext({
  viewport: { width: 1920, height: 1080 },
  recordVideo: { dir: __dirname, size: { width: 1920, height: 1080 } }
});
const page = await ctx.newPage();
await page.goto(`file:///${DECK_PATH.replace(/\\/g, '/')}`);

await page.waitForTimeout(500);

for (let i = 0; i < SLIDE_DURATIONS_MS.length; i++) {
  console.log(`slide ${i + 1}/${SLIDE_DURATIONS_MS.length} — holding ${SLIDE_DURATIONS_MS[i]}ms`);
  await page.waitForTimeout(SLIDE_DURATIONS_MS[i]);
  if (i < SLIDE_DURATIONS_MS.length - 1) {
    await page.keyboard.press('ArrowRight');
  }
}
await page.waitForTimeout(1000);

const vp = await page.video()?.path();
await ctx.close();
await browser.close();

if (vp && fs.existsSync(vp)) {
  const out = path.resolve(__dirname, 'slides.webm');
  fs.renameSync(vp, out);
  const totalSec = SLIDE_DURATIONS_MS.reduce((a, b) => a + b, 0) / 1000;
  console.log(`✓ slides.webm saved (~${totalSec}s, ${SLIDE_DURATIONS_MS.length} slides, silent)`);
  console.log(`  path: ${out}`);
} else {
  console.error('✗ no video found');
  process.exit(1);
}
