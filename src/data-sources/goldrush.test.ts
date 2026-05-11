import { describe, expect, it, vi } from "vitest";
import { GoldRushClient, type GoldRushTransaction, GoldRushWatcher } from "./goldrush.js";

function buildResponse(items: unknown[]): Response {
  return new Response(JSON.stringify({ data: { items } }), {
    status: 200,
    headers: { "Content-Type": "application/json" },
  });
}

function buildErrorResponse(): Response {
  return new Response(JSON.stringify({ error: true, error_message: "bad key" }), {
    status: 200,
    headers: { "Content-Type": "application/json" },
  });
}

describe("GoldRushClient", () => {
  it("parses Covalent rows into GoldRushTransaction objects", async () => {
    const fetchImpl = vi.fn().mockResolvedValueOnce(
      buildResponse([
        {
          tx_hash: "sig1",
          block_signed_at: "2026-05-11T10:00:00Z",
          block_height: 333_000_000,
          successful: true,
          fee: 5000,
          from_address: "Alice",
          to_address: "MultisigPDA",
          log_events: [{ raw_log_data: "Program log: weakened" }],
        },
      ]),
    );

    const client = new GoldRushClient({
      apiKey: "test-key",
      fetchImpl: fetchImpl as unknown as typeof fetch,
    });

    const txs = await client.fetchRecentTransactions("MultisigPDA");

    expect(txs).toHaveLength(1);
    expect(txs[0]).toEqual<GoldRushTransaction>({
      signature: "sig1",
      blockSignedAt: "2026-05-11T10:00:00Z",
      blockHeight: 333_000_000,
      successful: true,
      fee: 5000,
      from: "Alice",
      to: "MultisigPDA",
      rawLogMessages: ["Program log: weakened"],
    });

    expect(fetchImpl).toHaveBeenCalledTimes(1);
    const calledUrl = (fetchImpl.mock.calls[0]?.[0] ?? "") as string;
    expect(calledUrl).toContain("/v1/solana-mainnet/address/MultisigPDA/transactions_v2/");
    expect(calledUrl).toContain("key=test-key");
  });

  it("throws on covalent-level error payloads", async () => {
    const fetchImpl = vi
      .fn()
      .mockResolvedValueOnce(buildErrorResponse()) as unknown as typeof fetch;
    const client = new GoldRushClient({ apiKey: "k", fetchImpl });
    await expect(client.fetchRecentTransactions("X")).rejects.toThrow(/bad key/);
  });

  it("throws on non-2xx HTTP", async () => {
    const fetchImpl = vi
      .fn()
      .mockResolvedValueOnce(new Response("nope", { status: 503 })) as unknown as typeof fetch;
    const client = new GoldRushClient({ apiKey: "k", fetchImpl });
    await expect(client.fetchRecentTransactions("X")).rejects.toThrow(/HTTP 503/);
  });

  it("rejects empty api key at construction", () => {
    expect(() => new GoldRushClient({ apiKey: "" })).toThrow(/apiKey/);
  });

  it("skips rows missing tx_hash", async () => {
    const fetchImpl = vi
      .fn()
      .mockResolvedValueOnce(
        buildResponse([{ tx_hash: "good" }, { block_signed_at: "no-hash-here" }]),
      ) as unknown as typeof fetch;
    const client = new GoldRushClient({ apiKey: "k", fetchImpl });
    const txs = await client.fetchRecentTransactions("X");
    expect(txs).toHaveLength(1);
    expect(txs[0]?.signature).toBe("good");
  });
});

describe("GoldRushWatcher", () => {
  it("delivers new transactions oldest-first", async () => {
    const fetchImpl = vi.fn().mockResolvedValue(
      buildResponse([
        { tx_hash: "newest", block_signed_at: "2026-05-11T10:02:00Z" },
        { tx_hash: "middle", block_signed_at: "2026-05-11T10:01:00Z" },
        { tx_hash: "oldest", block_signed_at: "2026-05-11T10:00:00Z" },
      ]),
    ) as unknown as typeof fetch;

    const seen: string[] = [];
    const watcher = new GoldRushWatcher({
      client: new GoldRushClient({ apiKey: "k", fetchImpl }),
      addresses: ["A"],
      onTransaction: (_addr, tx) => {
        seen.push(tx.signature);
      },
      logger: () => {},
    });

    await watcher.tick();
    expect(seen).toEqual(["oldest", "middle", "newest"]);
  });

  it("dedupes signatures across ticks", async () => {
    const fetchImpl = vi
      .fn()
      .mockResolvedValueOnce(buildResponse([{ tx_hash: "sig1" }]))
      .mockResolvedValueOnce(buildResponse([{ tx_hash: "sig1" }, { tx_hash: "sig2" }]))
      .mockResolvedValueOnce(buildResponse([{ tx_hash: "sig2" }])) as unknown as typeof fetch;

    const seen: string[] = [];
    const watcher = new GoldRushWatcher({
      client: new GoldRushClient({ apiKey: "k", fetchImpl }),
      addresses: ["A"],
      onTransaction: (_addr, tx) => {
        seen.push(tx.signature);
      },
      logger: () => {},
    });

    await watcher.tick();
    await watcher.tick();
    await watcher.tick();
    expect(seen).toEqual(["sig1", "sig2"]);
  });

  it("primeSeen suppresses initial backlog", async () => {
    const fetchImpl = vi
      .fn()
      .mockResolvedValueOnce(buildResponse([{ tx_hash: "old1" }, { tx_hash: "old2" }]))
      .mockResolvedValueOnce(
        buildResponse([{ tx_hash: "new1" }, { tx_hash: "old1" }, { tx_hash: "old2" }]),
      ) as unknown as typeof fetch;

    const seen: string[] = [];
    const watcher = new GoldRushWatcher({
      client: new GoldRushClient({ apiKey: "k", fetchImpl }),
      addresses: ["A"],
      onTransaction: (_addr, tx) => {
        seen.push(tx.signature);
      },
      logger: () => {},
    });

    await watcher.primeSeen();
    await watcher.tick();
    expect(seen).toEqual(["new1"]);
  });

  it("continues polling other addresses when one fails", async () => {
    const fetchImpl = vi
      .fn()
      .mockResolvedValueOnce(new Response("err", { status: 500 }) as unknown as Response)
      .mockResolvedValueOnce(buildResponse([{ tx_hash: "sigB" }])) as unknown as typeof fetch;

    const seen: Array<[string, string]> = [];
    const watcher = new GoldRushWatcher({
      client: new GoldRushClient({ apiKey: "k", fetchImpl }),
      addresses: ["A", "B"],
      onTransaction: (addr, tx) => {
        seen.push([addr, tx.signature]);
      },
      logger: () => {},
    });

    await watcher.tick();
    expect(seen).toEqual([["B", "sigB"]]);
  });

  it("rejects empty addresses list", () => {
    expect(
      () =>
        new GoldRushWatcher({
          client: new GoldRushClient({
            apiKey: "k",
            fetchImpl: vi.fn() as unknown as typeof fetch,
          }),
          addresses: [],
          onTransaction: () => {},
        }),
    ).toThrow(/non-empty/);
  });
});
