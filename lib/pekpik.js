const BASE_URL = 'https://aiapiv2.pekpik.com/v1';

async function callChat(keys, messages) {
  let lastErr = 'Sem chaves configuradas. Adicione chaves na engrenagem ⚙️ do topo.';
  for (const key of keys) {
    try {
      const r = await fetch(`${BASE_URL}/chat/completions`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${key}`, 'Content-Type': 'application/json' },
        body: JSON.stringify({ model: 'deepseek-chat', messages, temperature: 0.3, max_tokens: 4096 }),
      });
      if (r.ok) return (await r.json()).choices[0].message.content;
      lastErr = `HTTP ${r.status}`;
    } catch (e) {
      lastErr = e.message;
    }
  }
  throw new Error(lastErr);
}

async function callWhisper(keys, audioBuffer, filename) {
  let lastErr = 'Sem chaves';
  for (const key of keys) {
    try {
      const { FormData, Blob } = await import('node:buffer').then(() => globalThis);
      const form = new FormData();
      form.append('file', new Blob([audioBuffer]), filename);
      form.append('model', 'whisper-1');
      form.append('language', 'pt');
      const r = await fetch(`${BASE_URL}/audio/transcriptions`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${key}` },
        body: form,
      });
      if (r.ok) return (await r.json()).text || '';
      lastErr = `HTTP ${r.status}: ${(await r.text()).slice(0, 120)}`;
    } catch (e) {
      lastErr = e.message;
    }
  }
  throw new Error(`Transcrição Whisper falhou: ${lastErr}`);
}

module.exports = { callChat, callWhisper };
