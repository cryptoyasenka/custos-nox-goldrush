# Pitch Deck Review — Judge's Eye Audit

**Date:** 2026-05-08
**Subject:** `assets/pitch-slides/deck-v2.html` (8 slides) + `assets/pitch-slides/architecture.html` (F3 overlay)
**Method:** Read deck slide-by-slide + cross-checked against `planning/PITCH-SCRIPT-F2.md`, `solana-frontier-hackathon/planning/SUBMISSION-RULES.md`, `TEN-K-WINNERS-DEEP-DIVE.md`, `PAST-WINNERS-ANALYSIS.md`, `SCORECARD.md`. Pretended to be Frontier judge watching silent slides.
**Status:** Analysis saved 2026-05-08 — improvements pending Yana's go-ahead.

---

## TL;DR Verdict

**Can submit as-is** — visual quality at Standout-level ($10K bar). Structure logical, matches past winners' decks (Attest Protocol, Reflect, Mercantill).

**Five fixes raise it to upper-half Standout + strengthen Public Goods Award lane.** Recommended before final F2 record.

---

## Visual Quality — Professional, ON PAR

- Dark theme (Vercel/Linear aesthetic) ✓
- Typography hierarchy clean ✓
- Color coding consistent: red=damage, green=solution, cyan=adjacent, orange=warning ✓
- Animations (count-up easeOutCubic, stagger fade-ins) ✓
- Custom SVG logo (lock+circle) ✓
- 1920×1080 fixed canvas with viewport scaling ✓

**Tier comparison:**
- Above: typical first-time hackathon decks
- On par: Reflect Protocol, Attest Protocol (Past Standout winners)
- Below: Stripe-corporate decks (not the bar for hackathons)

---

## Judge Test — Silent Watch (no voiceover yet)

Tracked when a judge understands WHAT the product is:

| Time | Slide | What judge sees | Product clarity |
|------|-------|-----------------|------------------|
| 0:00-0:16 | s1 (Incident) | $285M drained, 9 days prep, 0 alerts | **Hook strong, BUT product = ?** Footer "Open-source attack detection..." at 15px dimmed grey — invisible |
| 0:16-0:32 | s2 (Chain) | 4-step Drift timeline | "Is this a postmortem article? A service?" Still unclear |
| 0:32-0:46 | s3 (Gap) | 10K+ vs 50 STRIDE | Market gap clear, product still unknown |
| 0:46-0:59 | s4 (Detectors) | 5 detector cards | First HINT this is a tool. But CLI? Library? SaaS? |
| 0:59-1:13 | s5 (Proof) | "WebSocket → Discord alert" | **Finally clear: it's a daemon.** |
| 1:13+ | s6/s7/s8 | Setup, vision, CTA | All clear |

**Problem:** ~30% of viewing time elapses before judge knows what we're pitching. For 2-min pitch where judges may bail at 30s, this is risk.

---

## 6 Frontier Criteria (Section 8) — Coverage Audit

| # | Criterion | Coverage | Gap |
|---|-----------|----------|-----|
| 1 | **Functionality** | ⚠️ partial | "200+ tests, <1s, MIT" stated as text. **No screenshot of real alert.** F3 covers via live demo, but pitch shows zero visual proof of working product |
| 2 | **Potential Impact** | ✅ strong | 10K+ multisigs + $285M zero alerts — sized and quantified |
| 3 | **Novelty** | ⚠️ implicit | Nowhere does deck say **"0 open-source alternatives"** explicitly. Judge must infer. Should be loud: "First open-source Solana multisig monitor" |
| 4 | **UX** | ✅ ok | "5 min setup" + "<1s latency" + "no Rust, no credit card" — covered |
| 5 | **Open-source / Composes** | ⚠️ quiet | "MIT" mentioned but **Public Goods angle buried**. "No paid tiers ever" hidden in s7-note 24px grey. This is the primary $10K lane — must be loud |
| 6 | **Business Plan** | ⚠️ thin | v2/v3 named ("Hosted alert feed", "Mainnet watchlist") but **monetization model absent**. Public Goods angle compensates if amplified |

---

## Colosseum Pitch Template Requirements (blog "Perfecting Your Submission")

Required 5 elements in ≤3 min pitch video:

1. ✅ **Problem statement** — Drift exploit timeline (s1+s2)
2. ✅ **Target audience** — 10K+ Solana DAOs / multisigs (s3)
3. ✅ **Broader vision** — v1/v2/v3 (s7)
4. ❌ **Team background** — only on s8 (last) at 26px small text. Frontier judges (Lily Liu / Anatoly / Garrett Harper Squads) often shortlist by personality. Solo founder credibility should appear earlier
5. ❌ **User feedback / early traction** — deck has ZERO mention of Superteam UA traction, Squads Discord interest, GitHub stars, X engagement. Any validation = strong signal for shortlist

---

## Five Concrete Improvements (Recommended Before Final Record)

### Fix #1 — Slide 1 product reveal (HIGH PRIORITY)

**Why:** Judge doesn't know what we're pitching for first 30 seconds.

**What:** Between `$285M` amount and `s1-tag` ("9 days of on-chain prep · Zero alerts fired"), add new line:
```html
<div class="s1-product">Custos Nox — the alerts they didn't have</div>
```
With CSS: cyan or green color, ~38px font, weight 600, letter-spacing 0.04em.

**Effect:** Judge gets incident + product name + value prop in 5 seconds.

---

### Fix #2 — Slide 4 product type in headline (MEDIUM PRIORITY)

**Why:** Slide 4 is where judge first hints it's a tool, but doesn't know what kind.

**What:** Change `s4-sub` from:
> "Any single alert would have bought hours of response time"

To:
> "Open-source TypeScript daemon. Any single alert would have bought hours of response time"

OR change `s4-headline`:
> "One detector per step — open-source TypeScript daemon"

**Effect:** Product type ("daemon") lands at slide 4 instead of slide 5.

---

### Fix #3 — Slide 5 (Proof) add real alert screenshot (HIGH PRIORITY)

**Why:** Functionality criterion currently text-only. One real screenshot = sealed deal for judge.

**What:** Add a 4th element to `proof-row` OR replace one of the 3 cards with a Discord/Slack embed mockup or real screenshot. Could be:
- `assets/pitch-slides/discord-alert-screenshot.png` (320×200)
- Render in card as `<img>` with caption "Real alert from devnet"

**If can't get real screenshot in time:** create HTML/CSS mockup of Discord embed with red CRITICAL bar + alert text + timestamp + Solscan link. Looks like real Discord, judges read as proof.

**Effect:** Functionality criterion goes from text claim → visual evidence.

---

### Fix #4 — Public Goods Award louder signal (HIGH PRIORITY for $10K lane)

**Why:** "No paid tiers ever — public good" is buried in s7-note (24px grey). This is THE positioning for $10K Public Goods Award (separate from Standout).

**What options:**
- **Option A:** On slide 7 (vision), add green badge "🏛 PUBLIC GOOD · MIT · Free forever" above v1 row.
- **Option B:** On v1 vision-row, change `vision-status` from "Live today" to "Live · Public Good · Free forever" — louder green pill.
- **Option C:** Add separate small text on slide 1 or footer "Built as Public Good · MIT · No paid tier ever".

**Recommended:** Option B — minimal change, high signal.

**Effect:** Judges scoring Public Goods Award have unambiguous lane signal.

---

### Fix #5 — Solo founder credibility footer on slide 1 (LOW PRIORITY)

**Why:** Personality-driven shortlist signal. Currently solo founder appears only on last slide, may be missed by skim-judges.

**What:** Add to slide 1 footer (currently empty `<span></span>`):
```html
<span>Solo · Yasya · Superteam Ukraine</span>
```

Right side already has "Frontier 2026 · Superteam Ukraine". Could put left side as `Built solo by Yasya`.

**Effect:** Seeds founder credibility from slide 1.

---

## What NOT to Change

- **Slide structure** (incident → chain → gap → solution → proof → setup → vision → CTA) — matches past winners' arc, do not touch
- **Visual style** — dark theme + typography are at Standout-level
- **Solo-founder positioning** — all 3 past Grand Prize winners were solo, this is a feature not a bug
- **F2/F3 split** — pitch (why) vs tech demo (how) is required by Colosseum rules, our split is correct
- **Slide 4 5-card layout** (just fixed) — keep
- **No periods in taglines** (just fixed) — keep

---

## Optional Polish (Nice-to-Have, Not Critical)

1. **Slide 3 (gap):** Could add small "STRIDE = Solana Treasury · Risk · Investigations · Defense · Engineering" tooltip/footnote since acronym is unknown to most judges.
2. **Slide 6 (setup):** `CUSTOS_WATCH=<PROGRAM>:<YOUR_PDA>` — could add example value: `CUSTOS_WATCH=squads:7Hd8...XYZ` so judge sees concrete syntax.
3. **Slide 7 (vision):** "Up next" status on v2 — could add concrete date/quarter ("Q3 2026") to show roadmap reality.
4. **Slide 4 readability:** Detector cards now at 26px name / 21px step (down from 30/25 to fit 5 cards). Check after re-record — if too small at viewing distance, may need to reduce to 4-row layout (3+2 wide).

---

## Track Positioning (External, Not Visual)

For Arena project page submission text, explicitly mention:
- **Primary track:** Privacy + Confidential Compute (web3 security infrastructure category)
- **Secondary track:** Public Goods Award candidate (MIT + free forever)
- **Tertiary fit:** AI/Agent track NOT a fit — don't position there

This is the Arena form text, not the deck — keep deck universal.

---

## Implementation Order (If Yana Says "Apply All")

1. Fix #1 (slide 1 product reveal) — CSS + HTML add
2. Fix #2 (slide 4 product type) — single line text change
3. Fix #4 (Public Goods badge) — single line CSS change
4. Fix #5 (solo founder footer) — single span change
5. Fix #3 (alert screenshot) — most work; mockup in HTML/CSS or real screenshot generation
6. Re-run `node record-slides.mjs` → slides.webm v3
7. Open in player for Yana review
8. Commit: `fix(deck): product reveal s1, type label s4, public goods badge, alert screenshot proof`
9. Push to origin

---

## Past Winners Cross-Check (relevance)

| Past winner | Pattern they used | We have? |
|-------------|-------------------|----------|
| **Attest Protocol** ($10K Public Goods) | EAS-for-Solana, "MIT + composability" loud | ⚠️ ours is implicit |
| **IDL Space** ($10K Public Goods) | "Postman for Solana" — clear product analogy in slide 1 | ❌ ours has no analogy |
| **Mercantill** ($10K AI track) | "Banking for AI agents" — single-line product on slide 1 | ❌ ours product appears slide 5 |
| **Reflect Protocol** ($50K Grand) | Single primitive, evidence-first deck | ✅ ours matches |
| **Ore** ($50K Grand) | Solo, minimal frontend, evidence | ✅ ours matches |

**Pattern from winners:** the strongest decks land **product analogy or one-line value prop in slide 1**. Ours doesn't yet. Fix #1 closes this gap.

---

## Sources Used

- `C:\Projects\custos\planning\PITCH-SCRIPT-F2.md` (narration source)
- `C:\Projects\solana-frontier-hackathon\planning\SUBMISSION-RULES.md` (Colosseum rules + pitch template requirements)
- `C:\Projects\solana-frontier-hackathon\planning\SCORECARD.md` (6 judge criteria)
- `C:\Projects\solana-frontier-hackathon\planning\TEN-K-WINNERS-DEEP-DIVE.md` (11 solo $10K winners patterns)
- `C:\Projects\solana-frontier-hackathon\planning\PAST-WINNERS-ANALYSIS.md` (262 winners across 4 hackathons)
- `C:\Projects\custos\assets\pitch-slides\deck-v2.html` (current deck, 1029 lines after 2026-05-08 fixes)
- `C:\Projects\custos\assets\pitch-slides\architecture.html` (F3 overlay)
- `C:\Projects\custos\src\alerts\webhook.ts` (sinks: Discord, Slack, Telegram, Console)
