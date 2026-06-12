import { Hono } from "hono";

type Bindings = {
  SAVES: R2Bucket;
};

interface VersionEntry {
  sha256: string;
  timestamp: string;
  size: number;
}

const MAX_VERSIONS = 20;
const MAX_AGE_MS = 30 * 24 * 60 * 60 * 1000;
const MAX_BODY_BYTES = 2 * 1024 * 1024;
const HASH_RE = /^[0-9a-f]+$/;

const app = new Hono<{ Bindings: Bindings }>();

function indexKey(userHash: string): string {
  return `user-${userHash}-index`;
}

function persistentKey(userHash: string, sha256: string): string {
  return `user-${userHash}-persistent-${sha256}`;
}

async function sha256hex(data: ArrayBuffer): Promise<string> {
  const digest = await crypto.subtle.digest("SHA-256", data);
  return Array.from(new Uint8Array(digest))
    .map((b) => b.toString(16).padStart(2, "0"))
    .join("");
}

async function readIndex(bucket: R2Bucket, userHash: string): Promise<VersionEntry[]> {
  const obj = await bucket.get(indexKey(userHash));
  if (!obj) return [];
  return (await obj.json()) as VersionEntry[];
}

async function writeIndex(bucket: R2Bucket, userHash: string, index: VersionEntry[]): Promise<void> {
  await bucket.put(indexKey(userHash), JSON.stringify(index), {
    httpMetadata: { contentType: "application/json" },
  });
}

app.post("/saves/:hash/upload", async (c) => {
  const userHash = c.req.param("hash");
  if (!HASH_RE.test(userHash)) {
    return c.json({ error: "invalid hash" }, 400);
  }

  const body = await c.req.arrayBuffer();
  if (body.byteLength === 0) {
    return c.json({ error: "empty body" }, 400);
  }
  if (body.byteLength > MAX_BODY_BYTES) {
    return c.json({ error: "payload too large" }, 413);
  }

  const sha256 = await sha256hex(body);

  await c.env.SAVES.put(persistentKey(userHash, sha256), body, {
    httpMetadata: { contentType: "application/octet-stream" },
  });

  const now = new Date().toISOString();
  let index = await readIndex(c.env.SAVES, userHash);
  const cutoff = Date.now() - MAX_AGE_MS;

  // Prune expired entries and delete their objects
  const expired = index.filter((e) => new Date(e.timestamp).getTime() < cutoff);
  await Promise.all(expired.map((e) => c.env.SAVES.delete(persistentKey(userHash, e.sha256))));
  index = index.filter((e) => new Date(e.timestamp).getTime() >= cutoff);

  // Deduplicate: re-upload of the same content moves it to the top
  index = index.filter((e) => e.sha256 !== sha256);
  index.unshift({ sha256, timestamp: now, size: body.byteLength });

  // Cap at MAX_VERSIONS and delete overflow
  const overflow = index.splice(MAX_VERSIONS);
  await Promise.all(overflow.map((e) => c.env.SAVES.delete(persistentKey(userHash, e.sha256))));

  await writeIndex(c.env.SAVES, userHash, index);

  return c.json({ sha256 }, 201);
});

app.get("/saves/:hash/versions", async (c) => {
  const userHash = c.req.param("hash");
  if (!HASH_RE.test(userHash)) {
    return c.json({ error: "invalid hash" }, 400);
  }

  const index = await readIndex(c.env.SAVES, userHash);
  return c.json(index);
});

app.get("/saves/:hash/:uploadHash", async (c) => {
  const userHash = c.req.param("hash");
  const uploadHash = c.req.param("uploadHash");
  if (!HASH_RE.test(userHash) || !HASH_RE.test(uploadHash)) {
    return c.json({ error: "invalid hash" }, 400);
  }

  const obj = await c.env.SAVES.get(persistentKey(userHash, uploadHash));
  if (!obj) {
    return c.json({ error: "not found" }, 404);
  }

  return new Response(await obj.arrayBuffer(), {
    headers: { "Content-Type": "application/octet-stream" },
  });
});

export default app;
