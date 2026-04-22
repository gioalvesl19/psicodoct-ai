// In-memory cache per warm function instance
const cache = { keys: [], ts: 0 };
const CACHE_TTL_MS = 20 * 60 * 1000; // 20 minutes

const GITHUB_RAW =
  'https://raw.githubusercontent.com/alistaitsacle/free-llm-api-keys/main/README.md';

async function fetchPublicKeys() {
  const now = Date.now();
  if (cache.keys.length && now - cache.ts < CACHE_TTL_MS) {
    return cache.keys;
  }
  try {
    const r = await fetch(GITHUB_RAW, { signal: AbortSignal.timeout(8000) });
    if (!r.ok) return cache.keys;
    const text = await r.text();
    const keys = [];
    for (const line of text.split('\n')) {
      if (line.includes('deepseek-chat')) {
        const m = line.match(/`(sk-[A-Za-z0-9]{30,})`/);
        if (m) keys.push(m[1]);
      }
    }
    if (keys.length) {
      cache.keys = keys;
      cache.ts = now;
    }
    return keys.length ? keys : cache.keys;
  } catch {
    return cache.keys;
  }
}

async function getKeys(req) {
  // 1. Vercel env var (optional, for production overrides)
  const env = process.env.PEKPIK_CHAT_KEYS || '';
  if (env.trim()) return env.split(/[,\n]/).map(k => k.trim()).filter(Boolean);

  // 2. User-provided header override (from localStorage in browser)
  const header = (req.headers['x-keys'] || '').trim();
  if (header) return header.split(',').map(k => k.trim()).filter(Boolean);

  // 3. Auto-fetch from public GitHub repo
  return fetchPublicKeys();
}

module.exports = { getKeys, fetchPublicKeys };
