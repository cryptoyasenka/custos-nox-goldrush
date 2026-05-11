// Standalone GoldRush watcher. Polls Covalent for transaction history on
// each address in CUSTOS_WATCH, prints new signatures to stdout, and
// optionally forwards them to a Discord webhook.
//
// This script is independent of the main daemon (src/daemon.ts) — it
// exists to demonstrate the GoldRush data-source adapter as a self-contained
// alt path. Run:
//
//   CUSTOS_GOLDRUSH_API_KEY=ck_... CUSTOS_WATCH=PROG:ADDR npm run watch:goldrush
//
// For the Frontier sidetrack judges this is the entry point that exercises
// src/data-sources/goldrush.ts end to end.

import { GoldRushClient, GoldRushWatcher } from "../src/data-sources/goldrush.js";

const apiKey = process.env.CUSTOS_GOLDRUSH_API_KEY;
if (!apiKey) {
  console.error("CUSTOS_GOLDRUSH_API_KEY is required");
  process.exit(1);
}

const watchRaw = process.env.CUSTOS_WATCH ?? "";
const addresses = watchRaw
  .split(",")
  .map((s: string) => s.trim())
  .filter(Boolean)
  .map((entry: string) => {
    const parts = entry.split(":");
    if (parts.length !== 2 || !parts[1]) {
      throw new Error(`CUSTOS_WATCH entry must be <programPubkey>:<accountPubkey>, got '${entry}'`);
    }
    return parts[1];
  });

if (addresses.length === 0) {
  console.error("CUSTOS_WATCH must contain at least one programPubkey:accountPubkey entry");
  process.exit(1);
}

const pollIntervalMs = Number(process.env.CUSTOS_GOLDRUSH_POLL_MS ?? "30000");
const discordWebhook = process.env.CUSTOS_DISCORD_WEBHOOK?.trim() || null;

const client = new GoldRushClient({ apiKey });
const watcher = new GoldRushWatcher({
  client,
  addresses,
  pollIntervalMs,
  onTransaction: async (address, tx) => {
    const line = JSON.stringify({
      source: "goldrush",
      address,
      signature: tx.signature,
      blockSignedAt: tx.blockSignedAt,
      successful: tx.successful,
      from: tx.from,
      to: tx.to,
    });
    process.stdout.write(`${line}\n`);
    if (discordWebhook) {
      try {
        await fetch(discordWebhook, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            content: `[goldrush] ${address} → ${tx.signature.slice(0, 16)}… at ${tx.blockSignedAt}`,
            allowed_mentions: { parse: [] },
          }),
        });
      } catch (err) {
        process.stderr.write(`discord post failed: ${String(err)}\n`);
      }
    }
  },
});

console.error(
  `[goldrush] watching ${addresses.length} address(es), poll every ${pollIntervalMs}ms`,
);
await watcher.primeSeen();
watcher.start();

const shutdown = (signal: string): never => {
  console.error(`[goldrush] received ${signal}, stopping`);
  watcher.stop();
  process.exit(0);
};
process.on("SIGINT", () => shutdown("SIGINT"));
process.on("SIGTERM", () => shutdown("SIGTERM"));
