"""
Atualiza o keys.json com as chaves mais recentes do arquivo txt.
Uso: python update_keys.py "C:/Users/alves/Downloads/FREE AI API Keys 2026.txt"
"""
import sys
import re
import json
from pathlib import Path

TXT_FILE = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("C:/Users/alves/Downloads/FREE AI API Keys 2026.txt")
KEYS_FILE = Path(__file__).parent / "keys.json"

def extract_keys(text: str, model_filter: str = "deepseek-chat") -> list[str]:
    pattern = re.compile(
        r'\|\s*`(sk-[A-Za-z0-9]+)`\s*\|\s*' + re.escape(model_filter)
    )
    return pattern.findall(text)

def main():
    if not TXT_FILE.exists():
        print(f"Arquivo não encontrado: {TXT_FILE}")
        sys.exit(1)

    content = TXT_FILE.read_text(encoding="utf-8", errors="ignore")

    chat_keys = extract_keys(content, "deepseek-chat")
    # Also try gpt-5.4 keys
    gpt_keys = extract_keys(content, "gpt-5.4")
    all_chat = list(dict.fromkeys(chat_keys + gpt_keys))  # dedupe preserving order

    # Audio keys (same endpoint, reuse chat keys if no dedicated ones found)
    audio_keys = []

    existing = json.loads(KEYS_FILE.read_text(encoding="utf-8")) if KEYS_FILE.exists() else {}
    data = {
        "chat": all_chat or existing.get("chat", []),
        "audio": audio_keys or existing.get("audio", []),
    }
    KEYS_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"✅ keys.json atualizado!")
    print(f"   Chat keys:  {len(data['chat'])}")
    print(f"   Audio keys: {len(data['audio'])}")
    if not all_chat:
        print("⚠️  Nenhuma chave deepseek-chat encontrada. O arquivo pode ter expirado.")

if __name__ == "__main__":
    main()
