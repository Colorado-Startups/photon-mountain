import { describe, expect, it } from "vitest";
import { readRpc } from "./rpc";

describe("readRpc", () => {
  it("reads a JSON answer and a server-sent event answer alike", async () => {
    const msg = { jsonrpc: "2.0", id: 1, result: { ok: true } };
    expect(await readRpc(Response.json(msg))).toEqual(msg);
    expect(await readRpc(new Response(`event: message\ndata: ${JSON.stringify(msg)}\n\n`))).toEqual(msg);
  });
});
