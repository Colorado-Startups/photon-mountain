// Read one JSON-RPC answer from /mcp. Clients on the 2025 protocol get it as a server-sent event, even with
// JSON responses on, because the SDK serves them through its stateless legacy path; newer clients get JSON.
export async function readRpc(res: Response): Promise<{ result?: Record<string, any>; error?: { message: string } }> {
  const text = await res.text();
  if (text.trimStart().startsWith("{")) return JSON.parse(text);
  const data = text.split("\n").filter((l) => l.startsWith("data:")).map((l) => l.slice(5).trim()).join("");
  return JSON.parse(data);
}
