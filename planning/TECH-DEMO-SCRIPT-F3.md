# F3 — Technical Demo Script (~3:00 min, English)
# REVISED 2026-05-08 v4 — context-first, judge-without-crypto-background friendly

**Recording:** OBS Studio / Loom / Win+G. Screen only. Upload Loom (primary for Superteam UA) + YouTube Unlisted (backup, Arena A11).
**Target:** 2:55–3:05. Mostly browser + terminal. No slides.
**Rules note:** Colosseum requires a working product demo — not a slide deck. This script is 75% live product (browser + terminal + Discord), 25% explanation.
**Why this revision:** the previous version assumed the judge knows what a multisig and Squads are. Some judges don't. The first 30 seconds now build the foundation — DAO treasury, multisig, Squads — before the pitch lands.

---

## PRE-RECORDING SETUP (10 min)

**Accounts (fresh, devnet):**
- Multisig PDA: `Cn7XXry3SWbeqkBsH7uWXLViz4ffUqzyb3fi5Dkfr9Ao`
- Nonce pubkey: `BYCMzkaGMTsPLLxzoZE8qqLb56ov6V6hnoAacgnu2KBE`

**.env must have:**
```
CUSTOS_CLUSTER=devnet
CUSTOS_RPC_URL=https://api.devnet.solana.com
CUSTOS_WATCH=SQDS4ep65T869zMMBKyuUq6aD6EgTu8psMjkvj52pCf:Cn7XXry3SWbeqkBsH7uWXLViz4ffUqzyb3fi5Dkfr9Ao,11111111111111111111111111111111:BYCMzkaGMTsPLLxzoZE8qqLb56ov6V6hnoAacgnu2KBE
CUSTOS_DISCORD_WEBHOOK=<your webhook>
```

**Screen layout:**
- **Browser tab:** `https://custos-nox.up.railway.app` — open at top (hero), large dark font
- **Terminal LEFT:** `npm run dev` already running, 2 subscription lines visible
- **Terminal RIGHT:** empty prompt at `C:\Projects\custos`
- **Discord tab:** `#custos-alerts` — scrolled to bottom

Switch between browser → two-terminal layout → Discord at marked moments.

**Before recording:** run each smoke command once to verify all 4 fire. Then `npm run smoke:create` for a fresh multisig, update `.env`, restart daemon.

---

## SCRIPT

---

### [0:00–0:30] — What's a DAO treasury, and why this matters

*(Browser full screen — dashboard hero)*

"DAOs — decentralized organizations on Solana — manage their funds through multisig wallets. A multisig works like a company bank account that requires multiple signatures: three out of five people must approve before any money moves.

Squads is the most popular multisig tool on Solana. Many of Solana's largest DAOs, grant committees, and protocol treasuries use it. And right now, most of them have zero monitoring.

In April 2026, that cost one protocol $285 million."

*(Scroll down to Drift Timeline — 4 cards visible)*

"The Drift attack wasn't a sudden hack. The attacker spent nine days making config changes — in full public view, on-chain. No tool sent a single alert.

Custos Nox is that tool."

---

### [0:30–0:45] — The detectors, on the site

*(Scroll up to "What it catches" section — 5 detector cards with "Drift step 1/4" labels)*

"Five detectors running today. Four of them map to one step each in the Drift attack chain. The fifth covers an adjacent attack vector that has hit other Solana protocols.

Timelock removal. Multisig weakening. Privileged nonce. Stale nonce execution.

Any single one firing would have given the DAO days to respond."

---

### [0:45–0:55] — Architecture overlay (10 sec)

*(In CapCut: overlay `architecture.html` recording with fade in/out. No screen-cut from the host video — the diagram simply replaces the frame for 10 seconds.)*

"WebSocket subscription to Solana RPC. Five detectors run in parallel on every event. When one fires, fan-out to Discord, Slack, and console — none of them block the others. Sub-second alert latency end to end."

---

### [0:55–1:05] — Switch to terminals

*(Switch to two-terminal layout)*

"Left terminal — Custos Nox, watching a Squads multisig on devnet. That's the DAO's security monitor.

Right terminal — me, playing the attacker. Same steps, same order as Drift.

Watch the left terminal."

---

### [1:05–1:22] — Detector 1: Timelock

"The attacker's first move: remove the governance timelock. The timelock is the DAO's reaction window — the time the community has to notice something is wrong and respond."

*(Type and Enter:)*
```
npm run smoke:timelock -- Cn7XXry3SWbeqkBsH7uWXLViz4ffUqzyb3fi5Dkfr9Ao
```
*(wait 4 sec for confirmation)*

"CRITICAL. Timelock gone. No buffer left for the DAO."

---

### [1:22–1:37] — Detector 2: Multisig Weakening

"Next: weaken the multisig. Change the rule from 'three people must approve' to 'one person must approve'. The treasury is now under single-signer control."

*(Type and Enter:)*
```
npm run smoke:weaken -- Cn7XXry3SWbeqkBsH7uWXLViz4ffUqzyb3fi5Dkfr9Ao
```
*(wait 4 sec)*

"HIGH. Three-of-five dropped to one-of-five. The attacker can now approve any transaction alone."

---

### [1:37–1:52] — Detector 3: Privileged Nonce

"Third: create a durable nonce under an attacker-controlled key. This lets you pre-sign a transaction that stays valid forever — and execute it whenever you want. This is the moment the drain was armed."

*(Type and Enter:)*
```
npm run smoke:nonce-init
```
*(wait 4 sec)*

"CRITICAL. Pre-signed drain transaction is now live and waiting."

---

### [1:52–2:05] — Detector 5: Signer Rotation

"And one more — not from the Drift attack specifically, but from similar exploits: the attacker silently swaps out a legitimate co-signer for their own key. The threshold looks the same. The quorum is not."

*(Type and Enter:)*
```
npm run smoke:rotate-signers -- Cn7XXry3SWbeqkBsH7uWXLViz4ffUqzyb3fi5Dkfr9Ao
```
*(wait 4 sec)*

"HIGH. Legitimate signer evicted, attacker key added."

---

### [2:05–2:21] — Discord — full screen

*(Switch to Discord, maximized)*

"This is what the DAO team would see in Discord.

Not a log file — a clear alert with severity level, exactly what changed, and a direct link to the transaction on Solscan.

If Drift had this running on March 23rd, that first CRITICAL alert would have landed nine days before the drain.

Discord, Slack, and terminal all fire simultaneously. One failing webhook never blocks the others."

*(Slowly scroll through 4 embeds — 4 sec)*

---

### [2:21–2:29] — Detector 4: Stale Nonce Execution (tests)

*(Switch back to right terminal)*

"The fourth Drift-chain detector catches the drain itself — when the pre-signed transaction executes from a stale nonce. Fourteen unit tests cover the exact Drift pattern, all green."

*(Type and Enter:)*
```
npm test src/detectors/stale-nonce-execution
```
*(wait for "14 passing")*

---

### [2:29–2:45] — How to set this up (compressed to fit architecture overlay budget)

*(Switch to browser — "Self-host in 5 minutes" section)*

"How does a DAO actually set this up?

Step one: open app.squads.so — your multisig address, the PDA, is visible right there. Copy it.

Step two: paste it into one line in the config: CUSTOS_WATCH equals your PDA.

Step three: add a Discord or Slack webhook URL. Run npm run dev.

That's it. From that moment, any config change on your multisig — threshold, signers, timelock, nonce — fires an alert to your team within a second.

Free Helius RPC. MIT licensed. No paid tiers. No vendor lock-in."

---

### [2:45–3:00] — Close

*(Scroll to footer — GitHub URL visible)*

"Solana Foundation's STRIDE program covers protocols above ten million in TVL — about fifty protocols.

The other ten thousand DAO treasuries, grant multisigs, and community funds on Solana have nothing.

Custos Nox is for them.

github.com/cryptoyasenka/custos-nox"

*(Hold on GitHub URL 3 sec. End.)*

---

## TIMING

| Section | ~Sec | On screen |
|---------|------|-----------|
| 0:00–0:30 What's a DAO treasury | 0:30 | Browser hero + Drift Timeline |
| 0:30–0:45 The detectors on the site | 0:15 | Browser detector cards |
| 0:45–0:55 Architecture overlay | 0:10 | architecture.html (CapCut overlay) |
| 0:55–1:05 Switch to terminals | 0:10 | Two-terminal layout |
| 1:05–1:22 Detector 1 Timelock | 0:17 | Terminal |
| 1:22–1:37 Detector 2 Weakening | 0:15 | Terminal |
| 1:37–1:52 Detector 3 Nonce | 0:15 | Terminal |
| 1:52–2:05 Detector 5 Signer Rotation | 0:13 | Terminal |
| 2:05–2:21 Discord — 4 embeds | 0:16 | Discord |
| 2:21–2:29 Detector 4 stale-nonce tests | 0:08 | Terminal |
| 2:29–2:45 Setup walkthrough (compressed) | 0:16 | Browser |
| 2:45–3:00 Close | 0:15 | Browser |
| **Total** | **~3:00** | |

70% live product (browser + terminal + Discord). 25% explanation. 5% architecture overlay (covers the "if not visual — diagrams" guide requirement).

---

## COMMANDS — copy to a notepad before recording

```
npm run smoke:timelock -- Cn7XXry3SWbeqkBsH7uWXLViz4ffUqzyb3fi5Dkfr9Ao
npm run smoke:weaken -- Cn7XXry3SWbeqkBsH7uWXLViz4ffUqzyb3fi5Dkfr9Ao
npm run smoke:nonce-init
npm run smoke:rotate-signers -- Cn7XXry3SWbeqkBsH7uWXLViz4ffUqzyb3fi5Dkfr9Ao
npm test src/detectors/stale-nonce-execution
```

---

## KEY SENTENCES TO MEMORIZE

These are the lines that make the demo land — practice them until natural:

1. **"A multisig works like a company bank account that requires multiple signatures."** — opens with an analogy any judge understands
2. **"Squads is the most popular multisig tool on Solana."** — establishes scale and relevance
3. **"In April 2026, that cost one protocol $285 million."** — the hook
4. **"The Drift attack wasn't a sudden hack."** — sets up the 9-day window
5. **"Custos Nox is that tool."** — the positioning, said quietly and with confidence
6. **"This is the moment the drain was armed."** — on nonce-init, the most technically sharp moment
7. **"If Drift had this running on March 23rd, that first CRITICAL alert would have landed nine days before the drain."** — the Discord section's emotional payoff
8. **"The other ten thousand DAO treasuries on Solana have nothing."** — closes with the gap

---

## WHAT JUDGES WILL REMEMBER

- The first 30 seconds explained DAO/multisig/Squads in one paragraph — even a non-Solana judge can follow from here on
- They watched a live attack chain trigger four detectors back-to-back on devnet — not a mockup
- They saw Discord alerts landing in real time with severity and Solscan links — the distribution story is concrete
- The setup story was three steps — copy PDA, set one env var, run npm — friction is zero
- The closing quantified the gap: STRIDE covers fifty, ten thousand have nothing

---

## RECORDING TIPS

- One smooth take, natural pace. The first 30 seconds are calm and explanatory — don't rush to the terminal yet.
- Pause 4 sec after each smoke command so the alert text lands and is readable
- Don't edit out tx confirmation waits — they prove the chain is real, not a mockup
- Switch to Discord in one smooth motion (already maximized in another tab)
- For the setup section: scroll the website slowly, read the three steps clearly
- Upload to **Loom** (required by Superteam UA guide for tech demo). Also upload YouTube Unlisted as backup.
- Title: `Custos Nox — F3 Tech Demo (Solana Frontier 2026)`
- In **Arena A11**: paste YouTube URL. For **Superteam Earn** Ukrainian track submission: paste Loom URL.
- Verify both URLs work in incognito before pasting
