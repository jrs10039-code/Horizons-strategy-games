// Horizons AI War Room: private relay to the Claude API.
// Runs as a Vercel serverless function. The API key lives only in Vercel's
// environment variables, never in the web page.
//
// Environment variables (set in Vercel → Project → Settings → Environment Variables):
//   ANTHROPIC_API_KEY  your key from console.anthropic.com
//   PASSCODE           a word you share with the people you invite
//   ALLOWED_ORIGINS    optional, comma-separated; defaults to the GitHub Pages site

const MODELS = {
  player: 'claude-haiku-5-5',   // rival players: matches the Claude-hosted version that was tested
  disney: 'claude-sonnet-5-5',  // Disney's player: the game centers on its choices
  referee: 'claude-sonnet-5-5', // judges moves and keeps the numbers honest
  analyst: 'claude-opus-5-5',   // one call per click: the cross-game insights
};
const MAX_OUTPUT = { player: 6000, disney: 2500, referee: 10000, analyst: 8000 };
const MAX_INPUT_CHARS = 250000;
const DEFAULT_ORIGINS = ['https://jrs10039-code.github.io'];

module.exports = async (req, res) => {
  const allowed = (process.env.ALLOWED_ORIGINS || DEFAULT_ORIGINS.join(',')).split(',').map(s => s.trim());
  const origin = req.headers.origin || '';
  if (allowed.includes(origin) || origin.startsWith('http://localhost')) {
    res.setHeader('Access-Control-Allow-Origin', origin);
    res.setHeader('Vary', 'Origin');
  }
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(204).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Use POST.' });

  const body = typeof req.body === 'string' ? safeJson(req.body) : (req.body || {});
  const { passcode, role, system, prompt } = body;

  if (!process.env.ANTHROPIC_API_KEY) return res.status(500).json({ error: 'The server has no API key yet.' });
  if (!process.env.PASSCODE || passcode !== process.env.PASSCODE) return res.status(401).json({ error: 'Wrong passcode.' });
  if (!MODELS[role]) return res.status(400).json({ error: 'Unknown role.' });
  if (typeof prompt !== 'string' || !prompt || prompt.length + String(system || '').length > MAX_INPUT_CHARS) {
    return res.status(400).json({ error: 'Prompt missing or too long.' });
  }

  // Retry politely if the API is busy (rate limits on a new account are low).
  for (let attempt = 0; attempt < 4; attempt++) {
    const r = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'content-type': 'application/json',
        'x-api-key': process.env.ANTHROPIC_API_KEY,
        'anthropic-version': '2023-06-01',
      },
      body: JSON.stringify({
        model: MODELS[role],
        max_tokens: MAX_OUTPUT[role],
        system: String(system || ''),
        messages: [{ role: 'user', content: prompt }],
      }),
    });
    if (r.status === 429 || r.status === 529) {
      await new Promise(ok => setTimeout(ok, 2000 * (attempt + 1) + Math.random() * 1000));
      continue;
    }
    const data = await r.json().catch(() => ({}));
    if (!r.ok) return res.status(r.status).json({ error: data?.error?.message || 'Claude API error.' });
    const text = (data.content || []).filter(b => b.type === 'text').map(b => b.text).join('');
    return res.status(200).json({ text, model: data.model, usage: data.usage });
  }
  return res.status(429).json({ error: 'Claude is busy. Try again in a minute.' });
};

function safeJson(s) { try { return JSON.parse(s); } catch { return {}; } }
