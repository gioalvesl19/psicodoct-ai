const { getKeys } = require('../lib/keys');

const BASE_URL = 'https://aiapiv2.pekpik.com/v1';

module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST,OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type,X-Keys');
  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).end();

  const { audio_b64, filename } = req.body || {};
  if (!audio_b64) return res.status(400).json({ error: 'Campo audio_b64 obrigatório.' });

  const keys = getKeys(req);
  if (!keys.length) return res.status(503).json({ error: 'Sem chaves de API. Configure na engrenagem ⚙️.' });

  const audioBuffer = Buffer.from(audio_b64, 'base64');
  let lastErr = 'Sem chaves';

  for (const key of keys) {
    try {
      const form = new FormData();
      form.append('file', new Blob([audioBuffer]), filename || 'session.webm');
      form.append('model', 'whisper-1');
      form.append('language', 'pt');

      const r = await fetch(`${BASE_URL}/audio/transcriptions`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${key}` },
        body: form,
      });

      if (r.ok) {
        const data = await r.json();
        return res.status(200).json({ transcript: data.text || '' });
      }
      lastErr = `HTTP ${r.status}: ${(await r.text()).slice(0, 120)}`;
    } catch (e) {
      lastErr = e.message;
    }
  }

  return res.status(503).json({ error: `Transcrição falhou: ${lastErr}` });
};
