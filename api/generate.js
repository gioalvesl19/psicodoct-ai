const { getKeys } = require('../lib/keys');
const { callChat } = require('../lib/pekpik');
const { SYSTEM_PROMPT, buildPrompt } = require('../lib/prompts');

module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST,OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type,X-Keys');
  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  const { transcript, document_type, patient_name, session_date, psychologist_name, additional_context } = req.body || {};
  if (!transcript?.trim()) return res.status(400).json({ error: 'Transcrição vazia.' });

  const validTypes = ['anamnese','evolucao','soap','relatorio','declaracao','resumo','hipoteses','plano_terapeutico'];
  if (!validTypes.includes(document_type)) return res.status(400).json({ error: `Tipo inválido: ${document_type}` });

  const keys = await getKeys(req);
  if (!keys.length) return res.status(503).json({ error: 'Não foi possível obter chaves de API. Tente novamente em instantes.' });

  try {
    const userPrompt = buildPrompt(document_type, { transcript, patient_name, session_date, psychologist_name, additional_context });
    const messages = [
      { role: 'system', content: SYSTEM_PROMPT },
      { role: 'user', content: userPrompt },
    ];
    const document = await callChat(keys, messages);
    return res.status(200).json({ document, type: document_type });
  } catch (err) {
    return res.status(503).json({ error: err.message });
  }
};
