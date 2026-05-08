# SUBMISSION ANALYSIS — 2026-05-08

**Status:** SOURCE OF TRUTH for F2 + F3 + project rework. If a future session reads this and CURRENT.md, it must NOT roll back to the old "75% terminal demo" plan or claim F2 mp3 are "ready" — they are deprecated, scheduled for full re-record.

**Sources verified this session:**
- https://ua.superteam.fun/guide/docs/submission/pitch-video (WebFetch)
- https://ua.superteam.fun/guide/docs/submission/tech-demo (WebFetch)
- C:/Projects/solana-frontier-hackathon/planning/SUBMISSION-RULES.md (Official Rules PDF extract)
- C:/Projects/solana-frontier-hackathon/planning/SUPERTEAM-GUIDE.md (community guide)

---

## DECISION (Yana 2026-05-08 evening)

> "Все надо улучшить — ну и что что есть что-то готовое, переделаем пока не будет идеально презентабельно и понятно судьям. Доработай и проект, и видео."

**Both videos and the dashboard are being reworked.** F2 was "done" but had structural gaps. F3 was being recorded as 75% terminal — pivoted to dashboard-first multi-DAO live monitor.

**No fallback to old plan.** Yana said context kept drifting back to the old "8 mp3 ready, terminal demo recording" plan after compactions. This document + CURRENT.md must be read FIRST on resume; old gen.sh / old TECH-DEMO-SCRIPT-F3 v4 / "Yana собирает в CapCut" lines are HISTORICAL.

---

## RULE 1 — Tech-demo terminal question (resolved)

**Dictionary text from official Superteam UA guide (`/guide/docs/submission/tech-demo`):**

> ❌ Не рекомендується: «Відео з IDE або GitHub з кодом та голосовим коментарем»

✅ Рекомендується:
> «Пояснення технічних рішень під час огляду. Якщо продукт не наочний — створи діаграми.»

**Interpretation:**
- Hard prohibition: IDE + GitHub + code + voiceover combo (i.e., code-walkthrough monologue).
- **Terminal is NOT named in the prohibition.** A CLI is not the same as IDE-with-code-on-screen.
- BUT spirit of the rule + "Custos Nox daemon = не наочний" → ✅ guide explicitly allows diagrams as substitute. Best path: dashboard-first + architecture diagram + Discord. Terminal usage = optional minimum (one-line "npm run dev" as proof, NOT 8 minutes of typing commands).

**Final F3 stance:** dashboard + architecture overlay + Discord = primary. Terminal optional (≤10s if at all).

---

## RULE 2 — Pitch-video required blocks (gap analysis vs current F2)

**Required blocks from `/guide/docs/submission/pitch-video`:**

| # | Block | Required? | Current F2 status |
|---|---|---|---|
| 1 | **Intro — one-sentence product description** ("Судді мають зрозуміти за 5 секунд") | ✅ MUST | ❌ Slide 1 = 18s incident narrative, no one-sentence intro at top |
| 2 | Problem (research-backed) | ✅ MUST | ✅ Slide 2 (Chainalysis) covers it |
| 3 | Solution (ONE main advantage) | ✅ MUST | ✅ Slide 4 |
| 4 | Vision (scaling potential) | ✅ MUST | ✅ Slide 7 |
| 5 | Go-to-Market | ✅ MUST | ⚠️ Slide 6 partially (Squads Discord + Superteam) — needs clearer audience-channel-step |
| 6 | **Monetization** (revenue model, costs, profit threshold) | ✅ MUST | ⚠️ Implicit "no paid tiers" — needs EXPLICIT line: "Public Goods. Free forever. Costs covered by SF grant + community." |
| 7 | Traction (numbers required, even small) | ✅ MUST | ✅ Slide 5 (200+ tests, sub-second, MIT) |
| 8 | **Team experience** | ✅ MUST | ❌ **NO TEAM SLIDE AT ALL** — biggest gap |
| 9 | Demo (screenshot at start; full demo separate) | ⚠️ recommended | ⚠️ No screenshot inside F2; F3 = the full demo (acceptable) |

**Anti-patterns avoided:** ✅ no buzzwords, no "build for everyone", no inflated competitor matrix. Current F2 is clean on negative checks. Failure is on **missing required positive blocks** (team, monetization, one-sentence intro).

### F2 fix plan

1. **New one-sentence intro at slide-1 start** — ≤5s, must be parsable in isolation:
   > "Custos Nox is a real-time security monitor for Solana DAO multisigs — open-source, sub-second alerts, MIT licensed."
   Then continue with the Drift hook.
2. **New team slide (insert before close, ~18-20s) — FINAL TEXT (Yana confirmed 2026-05-08):**
   > "Built solo by Yana — Solana developer based in Kyiv. Background in Web3 security tooling: open-source ML models published on OpenGradient TEE hub, covering MEV detection, account abstraction, and EigenLayer monitoring. Custos Nox follows the same line — built as a public good, free forever."

   Visual: minimal — name, Kyiv, OpenGradient mention, one-line tagline. No photo unless Yana wants one. The credibility fact = "ML models on OpenGradient TEE for security domain", which directly anchors why a security-monitoring daemon makes sense from her hands.
3. **Explicit monetization line on slide 6 close:**
   > "No paid tiers ever. Public Goods Award sustainability — covered by Solana Foundation grant + Superteam Ukraine."

Implementation: deck-v2.html gets new slide-7.5 (team) and minor edits to slide-1 + slide-6. PITCH-SCRIPT-F2.md + VIDEO-2-PITCH.txt sync. gen.sh becomes 9 chunks (was 8). Total target ≤ 2:00 with Veo3 intro.

---

## RULE 3 — Tech-demo content requirements

**Required from `/guide/docs/submission/tech-demo`:**
- Повний огляд додатка — увесь юзер флоу
- Основні технічні рішення — і чому саме такі
- Пріоритизація функцій
- Як реалізована інтеграція з Solana

**Current F3 v4 status:**
- ✅ Solana integration: explicit (Squads + SPL Governance + Helius RPC)
- ⚠️ User flow: 70% terminal commands → not "user flow", that's "operator flow on devnet". DAO operator's actual flow = open dashboard, see alert, react.
- ✅ Technical decisions explained (5 detectors, fan-out webhooks)
- ⚠️ Prioritization: implicit (4 Drift-chain detectors + 1 adjacent), not stated as a decision
- ❌ "Не наочний → use diagrams" — we have architecture overlay (10s), but the rest is terminal-heavy = anti-pattern adjacency

### F3 rewrite plan (v5 — dashboard-first multi-DAO)

**Key narrative shift:**
> "Right now, Custos Nox is monitoring N publicly-known Solana DAO multisigs holding $XXX in TVL — including the same Drift Security Council that lost $285M last month. If any of them changes a threshold or signer, alert in under a second."

**v5 timing target ~3:00:**

| Time | Screen | Content |
|---|---|---|
| 0:00–0:25 | Browser hero | Context: DAOs, multisigs, Squads, $285M Drift |
| 0:25–0:50 | Browser **#live** section | **LIVE multi-DAO monitor**: "Watching Drift Security Council, Jito DAO, MarginFi, Marinade, Mango on Solana mainnet right now. N events captured today. Last alert Y minutes ago." |
| 0:50–1:30 | Browser detector cards | 5 detectors explained with Drift-chain mapping |
| 1:30–1:40 | Architecture overlay | WS → 5 detectors parallel → fan-out (10s with fade) |
| 1:40–2:30 | Browser alert replay | Devnet attack replay shown in dashboard alert feed (NOT terminal). Click → expanded alert detail with severity / what changed / Solscan link. |
| 2:30–2:45 | Discord screen | 4 Discord embeds, fan-out story |
| 2:45–3:00 | Browser footer | Setup (3 lines: PDA, env, npm run dev) + GitHub URL |

**Terminal usage in v5:** zero, OR a 5s "npm run dev" inside dashboard's own embedded log viewer (if we add one). NOT a full-screen terminal session.

**Why this is stronger than v4:**
- Matches "повний user flow" — DAO operator never opens a terminal in real life
- Eliminates anti-pattern adjacency (terminal+voiceover)
- Multi-DAO monitor = traction signal ("we already cover the ecosystem")
- Drift Security Council in the watchlist = best possible narrative anchor

---

## RULE 4 — Multi-DAO mainnet monitor (the "stronger" variant)

Yana wanted "сильнее" version. Single DAO is weak; multi-DAO is the upgrade.

**Target watchlist (research pending — Task #32):**
- Drift Security Council multisig (post-attack — the same one that lost $285M)
- Jito DAO multisig
- MarginFi multisig
- Marinade multisig
- Mango DAO multisig
- (optional) Bonk DAO, Solana Foundation grant multisig, Squads team multisig

Constraints:
- Each PDA must be **publicly known and verifiable on Solscan/Squads**
- Mix of Squads v4 (programId `SQDS4ep65T869zMMBKyuUq6aD6EgTu8psMjkvj52pCf`) and SPL Governance is OK — daemon supports both
- Helius free tier 1M req/mo accommodates 5–7 WS subscriptions easily

Deployment:
- Mainnet daemon as separate Railway service (Yana confirmed: no credit limits)
- Daemon writes JSONL events file or pushes via SSE
- Dashboard `#live` section reads real stream, replaces hardcoded SAMPLE_ALERTS

---

## What is being thrown away (so future sessions don't restore it)

- ❌ The old 8-mp3 F2 set in `video-build/f2/voice/` — slide-1 needs new intro, new slide-7.5 needs to exist, slide-6 needs monetization line. Re-generate ALL.
- ❌ The old 17-mp3 F3 set in `video-build/f3/voice/` — entire script changes. Re-generate ALL.
- ❌ TECH-DEMO-SCRIPT-F3.md v4 with terminal-heavy timing. Replaced by v5 (dashboard-first).
- ❌ VIDEO-3-DEMO.txt with "two terminals layout" instructions. Replaced.
- ❌ `#live` section's SAMPLE_ALERTS in `dashboard/app/page.tsx` lines ~265-299. Replaced with real mainnet stream.

What stays:
- ✅ Veo3 intro `assets/Blockchain_transactions_flow_red…_202605081236.mp4`
- ✅ deck-v2.html structure (slides 2-5, 7-8 mostly intact, slide 1 + slide 6 patched, new slide 7.5 added)
- ✅ architecture.html overlay
- ✅ All 5 detectors + daemon code + 200+ tests (no code change in detectors)
- ✅ Dashboard layout, components — only `#live` data source changes
- ✅ 03b-architecture.mp3 (architecture overlay narration) — text might need a 1-line tweak if rewritten

---

## Next-action priority (synced to TaskList #29-38)

1. ✅ Save this analysis (Task #29)
2. → Update CURRENT.md to point here (Task #30)
3. → Commit (Task #31) — locks the rework decision
4. → Research mainnet PDAs (Task #32)
5. → Build live mainnet monitor on dashboard (Task #33)
6. → Deploy mainnet daemon to Railway (Task #34)
7. → Patch F2 deck (Task #35)
8. → Regenerate F2 voice (Task #36)
9. → Rewrite F3 v5 (Task #37)
10. → Regenerate F3 voice (Task #38)

---

## Time budget reality check

- Deadline: **2026-05-10 23:59 PDT** = ~46h from this snapshot (2026-05-08 evening)
- Hours of work needed (estimate):
  - Research PDAs: 1h
  - Live monitor (dashboard + daemon glue): 4–6h
  - Railway deploy: 1h
  - F2 deck patches + regen: 2h
  - F3 v5 script + regen: 2h
  - CapCut assembly + Loom upload: 3h (Yana's hands)
- Total: ~13–15h of build + 3h Yana CapCut = feasible in 2 evenings. No slack — but no blockers either.

If time pressure forces cuts: **multi-DAO live monitor is the must-keep** (it's the "сильнее" upgrade Yana asked for). F2 team slide is must-add. Everything else can degrade to "good enough".
