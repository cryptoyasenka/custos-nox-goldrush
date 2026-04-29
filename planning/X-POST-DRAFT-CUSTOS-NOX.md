# X Post Drafts — @yasenka244 (Custos Nox)

Post from @yasenka244 (personal). Tag @CustosNox project account once it exists.

---

## POST 1 — Announcement (post after @CustosNox created)

Built a real-time Solana security monitor for the @colosseum Frontier Hackathon.

Custos Nox watches multisigs and DAOs for the exact on-chain moves that set up the Drift $285M drain — before the exploit executes.

5 detectors. TypeScript. Self-host in 5 min. MIT.

github.com/cryptoyasenka/custos-nox

[attach: dashboard screenshot or demo video clip]

---

## POST 2 — Technical thread (after F3 demo recorded)

The Drift attack didn't start with a drain tx. It started 9 days earlier, on-chain:

Day 1: Realm timelock → 0
Day 3: Squads multisig migrated to 2-of-5, zero timelock
Day 6: Durable nonce seeded under attacker key
Day 9: Pre-signed drain tx executes

Custos Nox fires on all 4. Here's the live devnet demo 🧵

[attach: F3 demo video]

---

## POST 3 — After Week 4 video / close to submission

Week 4 on Custos Nox.

5 detectors live. 205 tests green. Full Drift attack chain covered.

Recording the pitch and tech demo this week, then submitting to @colosseum Frontier.

Built with @SuperteamUKR 🇺🇦

github.com/cryptoyasenka/custos-nox

---

## POST 4 — After submission

Submitted Custos Nox to @colosseum Frontier Hackathon.

Open-source Solana multisig attack monitor. 5 detectors. MIT licensed.

If you run a DAO or treasury on Squads, try it:
github.com/cryptoyasenka/custos-nox

Feedback welcome 🙏

#Solana #SolanaHackathon #Colosseum

---

## SUPERTEAM UA TG ANNOUNCEMENT (post in @KumekaGroup)

Привіт! Yana (@yasenka244) з Superteam Ukraine.

Будую **Custos Nox** — open-source демон для Solana, який моніторить мультисіги і DAO в реальному часі на предмет атак типу Drift.

5 детекторів. TypeScript, нуль Rust. Самостійний хостинг за 5 хвилин. MIT ліцензія.

🔗 Dashboard: https://custos-nox.up.railway.app
📦 GitHub: https://github.com/cryptoyasenka/custos-nox

Буду вдячна за фідбек і зірочку на GitHub! 🙏

---

## POST 5 — Detector spotlight: TimelockRemoval

A timelock-to-zero on a Solana governance program isn't a config tweak. It's the fuse.

Custos Nox fires within seconds of the on-chain change — for both Squads v4 and SPL Governance Realms.

If your DAO's timelock just dropped to 0 and nobody scheduled it, somebody is moving.

[attach: alert screenshot — "[CRITICAL] squads-timelock-removal" card]

→ github.com/cryptoyasenka/custos-nox

---

## POST 6 — Detector spotlight: PrivilegedNonce

Durable nonces let you pre-sign a Solana tx that executes weeks later.

That's a feature for a payroll wallet. It's a weapon when an admin signer creates one without an audit trail.

Custos Nox watches every nonce init and authority rotation on accounts you care about.

[attach: alert screenshot — "[CRITICAL] privileged-nonce" card]

→ github.com/cryptoyasenka/custos-nox

---

## POST 7 — Self-host in 5 minutes

Custos Nox runs anywhere Node runs. No paid tier, no SaaS.

```
git clone github.com/cryptoyasenka/custos-nox
cd custos-nox && npm install
cp .env.example .env  # add Helius WS + Discord webhook
npm run dev
```

Watching your first multisig in 5 minutes. MIT.

[attach: terminal recording or 4-line gif of `npm run dev` showing 2 subscriptions live]

---

## POST 8 — Drift forensics: the 9-day fuse

The Drift $285M drain wasn't one transaction. It was 4 moves spread over 9 days, every one of them on chain in public:

Day 1 — Realm timelock → 0
Day 3 — Squads multisig migrated to 2-of-5, zero timelock
Day 6 — Durable nonce seeded under attacker key
Day 9 — Pre-signed drain tx executes

Custos Nox fires on all 4. Sub-second.

[attach: timeline graphic — 4 horizontal blocks with detector names mapped to each day]

→ github.com/cryptoyasenka/custos-nox

---

## POST 9 — Long tail positioning (gentle, no shade)

@solana Foundation's STRIDE program watches the top ~100 protocols.

The other ~10,000 multisigs and DAO treasuries on Solana — grant committees, small-team treasuries, NFT mint authorities — have nothing.

Custos Nox is for them. Self-host, free, MIT.

[attach: dashboard screenshot showing 5 live alert cards]

→ custos-nox.up.railway.app

---

## POST 10 — Community ask: what to detect next

5 detectors live. Working on v0.4 candidates:

• Squads permission-byte escalation (signer privilege bumps)
• Initial-connect retry handler (no missed alerts on cold start)
• Multi-cluster watch (mainnet + devnet side-by-side)

What attack pattern should we catch that we don't yet? Reply with the vector.

[attach: simple text card or 5 detector icons grid]

---

## POST 11 — Submission week (post 2026-05-08 morning Київ)

Submitting Custos Nox to @colosseum Frontier Hackathon this week.

Where we landed:
• 5 detectors covering the full Drift chain + 1 adjacent
• 205 tests, GitHub Actions green
• Live dashboard, MIT licensed
• ~3,200 lines of TypeScript, zero Rust, zero paid tiers

Built solo from Kyiv 🇺🇦 with @SuperteamUKR.

[attach: collage — alert card + dashboard + GitHub stars/tests badge]

→ github.com/cryptoyasenka/custos-nox

---

## SQUADS DISCORD OUTREACH (DM to Squads team or post in their server)

Hey — building Custos Nox, an open-source real-time monitor for Squads multisigs.

It detects threshold weakening, timelock removal, and privileged nonce seeding — the exact setup steps used in the April 2026 Drift exploit — and fires alerts to Discord/Slack within seconds of the on-chain event.

5 detectors live, TypeScript daemon, self-hostable in 5 min. MIT licensed.

Would love feedback from the Squads team, and happy to add a Squads-specific integration if there's interest.

Repo: https://github.com/cryptoyasenka/custos-nox
