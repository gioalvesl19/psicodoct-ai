function getKeys(req) {
  const envKeys = process.env.PEKPIK_CHAT_KEYS || '';
  if (envKeys.trim()) {
    return envKeys.split(/[,\n]/).map(k => k.trim()).filter(Boolean);
  }
  const headerKeys = req.headers['x-keys'] || '';
  return headerKeys.split(',').map(k => k.trim()).filter(Boolean);
}

module.exports = { getKeys };
