// Best-effort, in-memory request limiter for the contact form. Nothing is persisted:
// counters live in the memory of the running server instance and expire on their own.
// Each server instance counts separately, so this dampens bursts; it is not a hard quota.

const WINDOW_MS = 10 * 60 * 1000;
const MAX_PER_CLIENT = 5;
const GLOBAL_WINDOW_MS = 60 * 60 * 1000;
const MAX_GLOBAL = 40;
const MAX_TRACKED = 2000;

const perClient = new Map<string, number[]>();
let globalHits: number[] = [];
const delivered = new Map<string, number>();

function prune(now: number) {
  globalHits = globalHits.filter((t) => now - t < GLOBAL_WINDOW_MS);
  for (const [key, hits] of perClient) {
    const fresh = hits.filter((t) => now - t < WINDOW_MS);
    if (fresh.length) perClient.set(key, fresh);
    else perClient.delete(key);
  }
  for (const [id, at] of delivered) if (now - at > 24 * 60 * 60 * 1000) delivered.delete(id);
  while (perClient.size > MAX_TRACKED) {
    const first = perClient.keys().next().value;
    if (first === undefined) break;
    perClient.delete(first);
  }
}

/** Returns false when the client or the whole site exceeded its window. */
export function allowRequest(clientKey: string, now = Date.now()): boolean {
  prune(now);
  const hits = perClient.get(clientKey) ?? [];
  if (hits.length >= MAX_PER_CLIENT || globalHits.length >= MAX_GLOBAL) return false;
  hits.push(now);
  perClient.set(clientKey, hits);
  globalHits.push(now);
  return true;
}

export function wasDelivered(requestId: string): boolean {
  return delivered.has(requestId);
}

export function markDelivered(requestId: string, now = Date.now()) {
  delivered.set(requestId, now);
}

/** Test helper. */
export function resetRateLimit() {
  perClient.clear();
  globalHits = [];
  delivered.clear();
}
