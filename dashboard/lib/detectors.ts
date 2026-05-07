export type DetectorStatus = "production" | "roadmap";

export interface DetectorMeta {
  id: string;
  name: string;
  subtitle: string;
  status: DetectorStatus;
  severity: "critical" | "high";
  attackStep: string;
  /** "Drift step 1/4", "Drift step 2/4", ... or "Adjacent vector" */
  chainLabel: string;
  description: string;
  /** One-line plain-english summary of what the attacker gains if this step goes undetected */
  impact: string;
}

export const DETECTORS: DetectorMeta[] = [
  {
    id: "spl-governance-timelock-removal",
    name: "Timelock Removal",
    subtitle: "Squads v4 + SPL Governance",
    status: "production",
    severity: "critical",
    chainLabel: "Drift step 1 / 4",
    attackStep: "Realm timelock 6 days → 0",
    description:
      "Fires when a governance timelock is removed or dropped below half. Matches the Drift step where the attacker collapsed the response window before draining funds.",
    impact: "DAO loses its window to pause withdrawals or cancel the attack.",
  },
  {
    id: "squads-multisig-weakening",
    name: "Multisig Weakening",
    subtitle: "Squads v4",
    status: "production",
    severity: "high",
    chainLabel: "Drift step 2 / 4",
    attackStep: "Squads threshold 5-of-9 → 1-of-9",
    description:
      "Fires when a Squads multisig signer threshold is reduced. Catches the moment a treasury becomes single-signer controlled — the irreversible pivot in most exploits.",
    impact: "Attacker needs only themselves to approve any treasury transaction.",
  },
  {
    id: "privileged-nonce",
    name: "Privileged Nonce",
    subtitle: "System Program",
    status: "production",
    severity: "critical",
    chainLabel: "Drift step 3 / 4",
    attackStep: "Durable nonce under attacker key",
    description:
      "Fires on initialization or authority rotation of a watched durable-nonce account. Flags the precondition for pre-signed, replay-at-will withdrawal transactions.",
    impact: "A pre-signed drain transaction is now armed and can execute at any time.",
  },
  {
    id: "stale-nonce-execution",
    name: "Stale Nonce Execution",
    subtitle: "System Program",
    status: "production",
    severity: "high",
    chainLabel: "Drift step 4 / 4",
    attackStep: "Pre-signed tx executed from stale nonce",
    description:
      "Fires when a durable nonce is advanced (a pre-signed transaction executes) more than 1 hour after the nonce was first initialized. Catches the final step in the Drift attack chain — the moment the attacker's pre-signed drain transaction lands.",
    impact: "This is the drain. Funds are already moving to the attacker's wallet.",
  },
  {
    id: "squads-signer-set-change",
    name: "Signer Set Change",
    subtitle: "Squads v4",
    status: "production",
    severity: "high",
    chainLabel: "Adjacent vector",
    attackStep: "Members rotated — honest signers evicted",
    description:
      "Fires when a Squads multisig's members vector is mutated. Removal of a legitimate signer or rotation fires high; pure additions fire medium. Catches the takeover vector where an attacker swaps honest co-signers for their own keys.",
    impact: "Quorum is compromised even if the threshold looks unchanged on paper.",
  },
];
