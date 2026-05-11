// Covalent GoldRush data-source adapter.
//
// Why this exists: Custos Nox's primary data path is a Helius mainnet
// WebSocket subscription (see supervisor.ts). For operators who already
// have a Covalent GoldRush key — or who prefer poll-based monitoring over
// holding a live WS connection — this adapter polls
// /v1/solana-mainnet/address/{addr}/transactions_v2/ and emits a slim
// transaction stream that downstream detectors can consume the same way
// they consume a Solana RPC subscription.
//
// The adapter is intentionally independent of supervisor.ts. It owns its
// own polling loop and emits a typed event per newly-observed signature.
// Wiring into the existing alert dispatch happens in scripts/run-goldrush.mjs
// so the main daemon path stays unchanged for the Frontier submission.

const GOLDRUSH_BASE_URL = "https://api.covalenthq.com/v1";
const SOLANA_CHAIN_NAME = "solana-mainnet";
const DEFAULT_POLL_INTERVAL_MS = 30_000;
const DEFAULT_PAGE_SIZE = 25;

export interface GoldRushTransaction {
  signature: string;
  blockSignedAt: string;
  blockHeight: number;
  successful: boolean;
  fee: number;
  from: string | null;
  to: string | null;
  rawLogMessages: string[];
}

export interface GoldRushClientOptions {
  apiKey: string;
  fetchImpl?: typeof fetch;
  baseUrl?: string;
  pageSize?: number;
}

// Minimal shape of /transactions_v2 we depend on. Covalent returns many
// extra fields; we ignore them so this adapter doesn't break if the
// schema gains optional keys.
interface CovalentTxRow {
  tx_hash?: string;
  block_signed_at?: string;
  block_height?: number;
  successful?: boolean;
  fee?: number;
  from_address?: string | null;
  to_address?: string | null;
  log_events?: Array<{ raw_log_topics?: unknown; raw_log_data?: string | null }>;
}

interface CovalentTxResponse {
  data?: { items?: CovalentTxRow[] };
  error?: boolean;
  error_message?: string | null;
}

export class GoldRushClient {
  private readonly apiKey: string;
  private readonly fetchImpl: typeof fetch;
  private readonly baseUrl: string;
  private readonly pageSize: number;

  constructor(opts: GoldRushClientOptions) {
    if (!opts.apiKey) throw new Error("GoldRushClient: apiKey is required");
    this.apiKey = opts.apiKey;
    this.fetchImpl = opts.fetchImpl ?? globalThis.fetch;
    this.baseUrl = opts.baseUrl ?? GOLDRUSH_BASE_URL;
    this.pageSize = opts.pageSize ?? DEFAULT_PAGE_SIZE;
  }

  async fetchRecentTransactions(address: string): Promise<GoldRushTransaction[]> {
    const url = new URL(`${this.baseUrl}/${SOLANA_CHAIN_NAME}/address/${address}/transactions_v2/`);
    url.searchParams.set("page-size", String(this.pageSize));
    url.searchParams.set("no-logs", "false");
    // Covalent accepts the key either via Basic auth or ?key=. We use the
    // query param because Basic auth needs a non-empty password too on
    // some HTTP stacks and trips Node 24's strict header parser.
    url.searchParams.set("key", this.apiKey);

    const res = await this.fetchImpl(url.toString());
    if (!res.ok) {
      throw new Error(`GoldRush HTTP ${res.status} for ${address}`);
    }
    const body = (await res.json()) as CovalentTxResponse;
    if (body.error) {
      throw new Error(`GoldRush error for ${address}: ${body.error_message ?? "unknown"}`);
    }
    const items = body.data?.items ?? [];
    return items
      .filter(
        (row): row is Required<Pick<CovalentTxRow, "tx_hash">> & CovalentTxRow =>
          typeof row.tx_hash === "string" && row.tx_hash.length > 0,
      )
      .map((row) => ({
        signature: row.tx_hash as string,
        blockSignedAt: row.block_signed_at ?? "",
        blockHeight: row.block_height ?? 0,
        successful: row.successful ?? true,
        fee: row.fee ?? 0,
        from: row.from_address ?? null,
        to: row.to_address ?? null,
        rawLogMessages: (row.log_events ?? [])
          .map((e) => e.raw_log_data ?? "")
          .filter((s): s is string => Boolean(s)),
      }));
  }
}

export type GoldRushTxHandler = (address: string, tx: GoldRushTransaction) => Promise<void> | void;

export interface GoldRushWatcherOptions {
  client: GoldRushClient;
  addresses: string[];
  onTransaction: GoldRushTxHandler;
  pollIntervalMs?: number;
  // Setter for the wall-clock used in tests. Defaults to setTimeout/clearTimeout.
  scheduler?: {
    setTimeout: typeof setTimeout;
    clearTimeout: typeof clearTimeout;
  };
  logger?: (msg: string) => void;
}

// Per-address ring of seen signatures. We cap at ~1000 to keep memory
// bounded — that's >30 minutes of activity for a busy multisig.
const SEEN_RING_CAP = 1024;

export class GoldRushWatcher {
  private readonly opts: Required<Omit<GoldRushWatcherOptions, "scheduler" | "logger">> & {
    scheduler: NonNullable<GoldRushWatcherOptions["scheduler"]>;
    logger: NonNullable<GoldRushWatcherOptions["logger"]>;
  };
  private readonly seen = new Map<string, Set<string>>();
  private readonly seenOrder = new Map<string, string[]>();
  private timer: ReturnType<typeof setTimeout> | null = null;
  private running = false;

  constructor(opts: GoldRushWatcherOptions) {
    if (opts.addresses.length === 0) {
      throw new Error("GoldRushWatcher: addresses must be non-empty");
    }
    this.opts = {
      client: opts.client,
      addresses: opts.addresses,
      onTransaction: opts.onTransaction,
      pollIntervalMs: opts.pollIntervalMs ?? DEFAULT_POLL_INTERVAL_MS,
      scheduler: opts.scheduler ?? { setTimeout, clearTimeout },
      logger: opts.logger ?? ((msg: string) => process.stdout.write(`[goldrush] ${msg}\n`)),
    };
    for (const a of this.opts.addresses) {
      this.seen.set(a, new Set());
      this.seenOrder.set(a, []);
    }
  }

  // Prime the seen-set with the current state before delivering events.
  // Without this, the first poll would deliver the entire 25-tx page as
  // "new" alerts on every restart. Tradeoff: a signature that lands
  // between primeSeen and the first tick is lost. For monitoring the
  // tradeoff is right — we'd rather miss one tx than alert-storm.
  async primeSeen(): Promise<void> {
    for (const address of this.opts.addresses) {
      try {
        const txs = await this.opts.client.fetchRecentTransactions(address);
        for (const tx of txs) this.recordSeen(address, tx.signature);
        this.opts.logger(`primed ${address} with ${txs.length} known signatures`);
      } catch (err) {
        this.opts.logger(`prime failed for ${address}: ${errMsg(err)}`);
      }
    }
  }

  async tick(): Promise<void> {
    for (const address of this.opts.addresses) {
      let txs: GoldRushTransaction[];
      try {
        txs = await this.opts.client.fetchRecentTransactions(address);
      } catch (err) {
        this.opts.logger(`fetch failed for ${address}: ${errMsg(err)}`);
        continue;
      }
      // Covalent returns newest-first. Iterate oldest-first so handlers
      // see events in chronological order.
      for (let i = txs.length - 1; i >= 0; i--) {
        const tx = txs[i];
        if (!tx) continue;
        if (this.hasSeen(address, tx.signature)) continue;
        this.recordSeen(address, tx.signature);
        try {
          await this.opts.onTransaction(address, tx);
        } catch (err) {
          this.opts.logger(`handler threw on ${tx.signature}: ${errMsg(err)}`);
        }
      }
    }
  }

  start(): void {
    if (this.running) return;
    this.running = true;
    const loop = async (): Promise<void> => {
      if (!this.running) return;
      await this.tick();
      if (!this.running) return;
      this.timer = this.opts.scheduler.setTimeout(loop, this.opts.pollIntervalMs);
    };
    void loop();
  }

  stop(): void {
    this.running = false;
    if (this.timer) {
      this.opts.scheduler.clearTimeout(this.timer);
      this.timer = null;
    }
  }

  private hasSeen(address: string, signature: string): boolean {
    return this.seen.get(address)?.has(signature) ?? false;
  }

  private recordSeen(address: string, signature: string): void {
    const set = this.seen.get(address);
    const order = this.seenOrder.get(address);
    if (!set || !order) return;
    if (set.has(signature)) return;
    set.add(signature);
    order.push(signature);
    if (order.length > SEEN_RING_CAP) {
      const evicted = order.shift();
      if (evicted) set.delete(evicted);
    }
  }
}

function errMsg(err: unknown): string {
  return err instanceof Error ? err.message : String(err);
}
