#!/usr/bin/env bash
# F3 Tech Demo — voiceover generation (TECH-DEMO-SCRIPT-F3.md v5, 2026-05-08).
# 9 chunks: 7 main sections + architecture overlay + 1 alert-detail beat.
# v5 is dashboard-first (terminal-zero). Old 17-chunk v4 set is deprecated.
# Run: cd video-build/f3/voice && bash gen.sh
set -e

VOICE="en-US-AriaNeural"
RATE="+0%"

mkdir -p "$(dirname "$0")"
cd "$(dirname "$0")"

# v4 leftovers — different filenames, would silently linger. Wipe before regen.
rm -f *.mp3

echo "→ Generating F3 voiceover v5 (9 chunks, voice=$VOICE)..."

edge-tts --voice "$VOICE" --rate "$RATE" --write-media 01-hero.mp3 \
  --text "DAOs on Solana hold their treasuries through multisig wallets — three-of-five signatures, like a corporate bank account. Squads is the most popular multisig tool on Solana. Major protocol treasuries, grant committees, and security councils run on it. And until now, almost none of them had any monitoring. Last April, that cost one protocol two hundred eighty-five million dollars. Nine days of on-chain preparation. Zero alerts."

edge-tts --voice "$VOICE" --rate "$RATE" --write-media 02-live-watchlist.mp3 \
  --text "Custos Nox is watching twelve Solana DAOs on mainnet right now — Mango, Marinade, Pyth, Solend, Jupiter, Raydium, Orca, BonkDAO, plus Helius, Squads, Superteam, and MonkeDAO. Each card links straight to its Realms page. The status dot on each card stays green while no anomalies fire — turns yellow on a single high-severity event, red on critical. If any of these twelve changes a threshold, swaps a signer, or removes a timelock, Custos Nox catches it on the next slot."

edge-tts --voice "$VOICE" --rate "$RATE" --write-media 03-detectors.mp3 \
  --text "Five detectors run on every event. Four map directly onto steps from the Drift attack chain — and the fifth covers an adjacent attack vector that has hit other Solana protocols. Timelock removal — Drift step one. The reaction window for the DAO is gone. Multisig weakening — Drift step two. Three-of-five drops to one-of-five. Single-signer control. Privileged nonce — Drift step three. The drain transaction is pre-signed and armed. Stale nonce execution — Drift step four. The drain itself. Signer rotation — adjacent vector. A legitimate signer is silently swapped for an attacker key. The threshold looks the same. The quorum is not. Any one of these firing on Drift would have given hours of response time. Nine days, in the real attack."

edge-tts --voice "$VOICE" --rate "$RATE" --write-media 04-architecture.mp3 \
  --text "WebSocket subscription per DAO. Five detectors run in parallel on every event. When one fires, fan-out to Discord, Slack, and the dashboard alert feed — none of them block the others. Sub-second end-to-end."

edge-tts --voice "$VOICE" --rate "$RATE" --write-media 05a-replay-rows.mp3 \
  --text "Here's what those four detectors look like firing back-to-back. This is a devnet replay of the Drift chain — same dashboard the operator would see on mainnet. First row — Timelock removal. Severity CRITICAL. Subject: the multisig P D A. Solscan link to the exact transaction. Second row — Multisig weakening. Severity HIGH. The context shows old threshold three, new threshold one. Third row — Privileged nonce. CRITICAL. The drain transaction is now pre-signed and waiting. Fourth row — Stale nonce execution. CRITICAL. The drain executes."

edge-tts --voice "$VOICE" --rate "$RATE" --write-media 05b-replay-detail.mp3 \
  --text "Each alert has the severity, the exact field that changed, the signer who did it, and a Solscan link. No log files. No grep. The team sees the chain unfolding in real time."

edge-tts --voice "$VOICE" --rate "$RATE" --write-media 06-discord.mp3 \
  --text "Same four alerts, simultaneously, in Discord. Slack and the dashboard fired at the same instant. If Drift had this running on March twenty-third, the first CRITICAL alert would have landed nine days before the drain."

edge-tts --voice "$VOICE" --rate "$RATE" --write-media 07a-setup.mp3 \
  --text "Three lines to set up. Open app dot squads dot so, copy your multisig P D A. Paste it into CUSTOS WATCH. Add a Discord webhook. N P M run dev. M I T licensed. No paid tiers. Free Helius R P C tier is enough for a single DAO."

edge-tts --voice "$VOICE" --rate "$RATE" --write-media 07b-close.mp3 \
  --text "Solana Foundation's STRIDE program covers fifty protocols. The other ten thousand DAOs have nothing. Custos Nox is for them. github dot com slash cryptoyasenka slash custos hyphen nox."

echo "✓ Done. 9 mp3 files in $(pwd)"
ls -la *.mp3
