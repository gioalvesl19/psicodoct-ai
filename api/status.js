const { getKeys } = require('../lib/keys');

module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type,X-Keys');
  if (req.method === 'OPTIONS') return res.status(200).end();

  const keys = await getKeys(req);
  const source = process.env.PEKPIK_CHAT_KEYS
    ? 'env'
    : req.headers['x-keys']
    ? 'user'
    : 'auto';
  return res.status(200).json({ has_keys: keys.length > 0, count: keys.length, source });
};
