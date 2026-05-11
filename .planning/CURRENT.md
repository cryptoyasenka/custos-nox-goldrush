# CURRENT — custos-nox-goldrush (sidetrack mirror)

**Last touched:** 2026-05-11 17:30 Kyiv
**Status:** Code complete. Submission BLOCKED — no live GoldRush bounty found.

## What this repo is

Independent mirror copy (not a GitHub fork — no "forked from" badge) of the main Frontier submission at `cryptoyasenka/custos-nox`, with a GoldRush-specific data-source addition. The main Frontier submission lives in `C:\Projects\custos\` and is LOCKED — never touch it.

Purpose: submit to the **Covalent GoldRush** sidetrack of the Solana Frontier Hackathon, if one ever materializes.

## Done

- [x] Cloned from main, origin repointed to `cryptoyasenka/custos-nox-goldrush`
- [x] Built `src/data-sources/goldrush.ts` — typed `GoldRushClient` hitting `api.covalenthq.com/v1/solana-mainnet/address/{addr}/transactions_v2/` + `GoldRushWatcher` polling each watched address, priming a seen-set on first tick to suppress restart backlog, fanning new signatures out in chronological order
- [x] 10 unit tests + full suite 244 green
- [x] Commit `81a2d36`, pushed to `origin/main`

## Status: blocked

Verified 2026-05-11 17:00 Kyiv via 3 sources:
- Colosseum announcement explicitly states tracks/bounties **removed** from Frontier (replaced with single $30K Grand Champion)
- Superteam Earn API: zero listings match GoldRush/Covalent
- WebSearch for current GoldRush bounty programs on Solana: no hits

The mirror repo stands as a portfolio artifact. If a GoldRush bounty surfaces (next hackathon cycle, Breakout, Eternal), submission values are ready at `C:\Users\Yana\.claude\snapshots\sidetrack-submit-values.md`.

## Next step

None autonomously. Yana decides in the morning whether to:
1. Wait for sponsor program to surface
2. Repurpose this code into the main repo as an alternative data source
3. Archive the mirror repo
