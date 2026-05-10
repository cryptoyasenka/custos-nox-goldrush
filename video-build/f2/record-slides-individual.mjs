import { execSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { chromium } from "playwright-chromium";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const DECK_PATH = path.resolve(__dirname, "../../assets/pitch-slides/deck-v2.html");
const OUT_DIR = path.resolve(__dirname, "slides-individual");

const SLIDE_DURATIONS_MS = [
  16000, // s1 — incident + product reveal + 9-days punch
  16000, // s2 — Drift attack chain timeline
  14000, // s3 — STRIDE vs 10,000+ gap
  14000, // s4 — 5 detector cards (now with daemon type label)
  14000, // s5 — 4 proof cards (200+/<1s/MIT/Discord mockup)
  14000, // s6 — setup in 5 min
  13000, // s7 — vision (now with Public Good badge)
  12000, // s8 — Team (Yasya + OpenGradient models)
  10000, // s9 — CTA + final
];
// Per-slide lead-in: ~500ms (browser settle + slide reveal). Trim in CapCut if needed.

if (!fs.existsSync(DECK_PATH)) {
  console.error("✗ deck not found at", DECK_PATH);
  process.exit(1);
}

if (!fs.existsSync(OUT_DIR)) fs.mkdirSync(OUT_DIR, { recursive: true });

const browser = await chromium.launch({ args: ["--no-sandbox"] });

for (let idx = 0; idx < SLIDE_DURATIONS_MS.length; idx++) {
  const slideNum = idx + 1;
  const tmpDir = path.join(OUT_DIR, `tmp-${slideNum}`);
  if (!fs.existsSync(tmpDir)) fs.mkdirSync(tmpDir, { recursive: true });

  console.log(
    `▶ recording slide ${slideNum}/${SLIDE_DURATIONS_MS.length} — ${SLIDE_DURATIONS_MS[idx]}ms`,
  );

  const ctx = await browser.newContext({
    viewport: { width: 1920, height: 1080 },
    recordVideo: { dir: tmpDir, size: { width: 1920, height: 1080 } },
  });
  const page = await ctx.newPage();
  await page.goto(`file:///${DECK_PATH.replace(/\\/g, "/")}`);

  // Hide HUD so it doesn't appear in recording
  await page.addStyleTag({ content: ".hud { display: none !important; }" });

  // Settle: let initial paint + onSlideEnter(0) finish
  await page.waitForTimeout(300);

  // Jump straight to target slide WITHOUT fade transition, then re-fire animations
  if (idx > 0) {
    await page.evaluate((targetIdx) => {
      const all = document.querySelectorAll(".slide");
      all.forEach((s, i) => {
        s.style.transition = "none";
        s.classList.remove("active");
        s.style.display = "none";
        s.style.opacity = "0";
      });
      const target = all[targetIdx];
      target.style.display = "flex";
      // Force reflow so opacity transition is consistent
      target.getBoundingClientRect();
      target.classList.add("active");
      target.style.opacity = "1";
      // Re-fire entrance animations
      if (typeof onSlideEnter === "function") onSlideEnter(targetIdx);
    }, idx);
  }

  // Hold for slide duration
  await page.waitForTimeout(SLIDE_DURATIONS_MS[idx]);

  const videoPath = await page.video()?.path();
  await ctx.close();

  if (videoPath && fs.existsSync(videoPath)) {
    const webmOut = path.join(OUT_DIR, `slide-${slideNum}.webm`);
    if (fs.existsSync(webmOut)) fs.unlinkSync(webmOut);
    fs.renameSync(videoPath, webmOut);
    console.log(`  ✓ saved ${webmOut}`);

    // CapCut on Windows rejects .webm — transcode to H.264 .mp4 (yuv420p, faststart).
    const mp4Out = path.join(OUT_DIR, `slide-${slideNum}.mp4`);
    if (fs.existsSync(mp4Out)) fs.unlinkSync(mp4Out);
    try {
      execSync(
        `ffmpeg -y -loglevel error -i "${webmOut}" -c:v libx264 -pix_fmt yuv420p -preset slow -crf 18 -movflags +faststart -an "${mp4Out}"`,
        { stdio: "inherit" },
      );
      console.log(`  ✓ transcoded ${mp4Out}`);
    } catch (e) {
      console.error(`  ✗ ffmpeg failed for slide ${slideNum}:`, e.message);
    }

    // Clean tmp dir
    try {
      fs.rmSync(tmpDir, { recursive: true, force: true });
    } catch (e) {
      /* ignore */
    }
  } else {
    console.error(`  ✗ no video for slide ${slideNum}`);
  }
}

await browser.close();

const lastIdx = SLIDE_DURATIONS_MS.length;
console.log(`\n✓ all ${lastIdx} slides saved to ${OUT_DIR}`);
console.log(`  WebM (lossless source): slide-1.webm ... slide-${lastIdx}.webm`);
console.log(`  MP4 (CapCut-ready):     slide-1.mp4  ... slide-${lastIdx}.mp4`);
console.log("  Sequence in CapCut by filename order. Import the .mp4 set.");
