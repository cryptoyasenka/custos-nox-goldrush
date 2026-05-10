import { NONCE_ACCOUNT_LENGTH, SYSTEM_PROGRAM_ID, parseNonceAccount } from "../parsers/nonce.js";
import type { Alert, Detector, SolanaEvent } from "../types/events.js";
import { buildAlert } from "./_shared.js";

export const PRIVILEGED_NONCE_DETECTOR_NAME = "privileged-nonce";

export const PrivilegedNonceDetector: Detector = {
  name: PRIVILEGED_NONCE_DETECTOR_NAME,
  description:
    "Alerts when a watched System Program nonce account is initialized or has its authority rotated. " +
    "Durable nonces let a single key pre-sign transactions that bypass multisig approval — " +
    "Drift-class attack chains weaponize this after taking over governance.",

  async inspect(event: SolanaEvent): Promise<Alert | null> {
    if (event.kind !== "account_change") return null;
    if (!event.program.equals(SYSTEM_PROGRAM_ID)) return null;
    if (event.data.length !== NONCE_ACCOUNT_LENGTH) return null;
    if (event.previousData && event.data.equals(event.previousData)) return null;

    const curr = parseNonceAccount(event.data);
    if (!curr) return null;

    const prev = event.previousData ? parseNonceAccount(event.previousData) : null;
    const accountBase58 = event.account.toBase58();

    // Case 1: brand-new initialization (was uninitialized or absent).
    if (
      curr.state === "initialized" &&
      curr.authority &&
      (!prev || prev.state === "uninitialized")
    ) {
      return buildAlert({
        detectorName: PRIVILEGED_NONCE_DETECTOR_NAME,
        event,
        severity: "critical",
        subject: `Nonce account ${accountBase58} initialized with authority ${curr.authority.toBase58()}`,
        context: {
          reason: "nonce_initialized",
          account: accountBase58,
          authority: curr.authority.toBase58(),
        },
      });
    }

    // Case 2: authority rotated on an already-initialized nonce.
    if (
      curr.state === "initialized" &&
      curr.authority &&
      prev &&
      prev.state === "initialized" &&
      prev.authority &&
      !prev.authority.equals(curr.authority)
    ) {
      return buildAlert({
        detectorName: PRIVILEGED_NONCE_DETECTOR_NAME,
        event,
        severity: "high",
        subject: `Nonce authority rotated ${prev.authority.toBase58()} → ${curr.authority.toBase58()} on ${accountBase58}`,
        context: {
          reason: "nonce_authority_rotated",
          account: accountBase58,
          previousAuthority: prev.authority.toBase58(),
          currentAuthority: curr.authority.toBase58(),
        },
      });
    }

    return null;
  },
};
