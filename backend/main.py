import json
import httpx
import sys
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from pydantic import BaseModel

sys.path.insert(0, str(Path(__file__).parent))
from prompts import DOCUMENT_PROMPTS, SYSTEM_PROMPT

app = FastAPI(title="PsicoDoc AI", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_URL = "https://aiapiv2.pekpik.com/v1"
KEYS_FILE = Path(__file__).parent.parent / "keys.json"


def load_keys() -> dict:
    if KEYS_FILE.exists():
        return json.loads(KEYS_FILE.read_text(encoding="utf-8"))
    return {"chat": [], "audio": []}


def save_keys(data: dict):
    KEYS_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


async def call_chat(messages: list, model: str = "deepseek-chat") -> str:
    keys = load_keys().get("chat", [])
    if not keys:
        raise HTTPException(503, "Nenhuma chave de API configurada. Adicione chaves em Configurações.")

    last_error = "Sem chaves disponíveis"
    for key in keys:
        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                r = await client.post(
                    f"{BASE_URL}/chat/completions",
                    headers={"Authorization": f"Bearer {key}"},
                    json={
                        "model": model,
                        "messages": messages,
                        "temperature": 0.3,
                        "max_tokens": 4096,
                    },
                )
            if r.status_code == 200:
                return r.json()["choices"][0]["message"]["content"]
            last_error = f"HTTP {r.status_code}: {r.text[:200]}"
            if r.status_code in (401, 403):
                continue  # try next key
        except Exception as exc:
            last_error = str(exc)
            continue

    raise HTTPException(503, f"Todas as chaves falharam. Último erro: {last_error}")


async def call_whisper(audio_bytes: bytes, filename: str) -> str:
    keys_data = load_keys()
    keys = keys_data.get("audio") or keys_data.get("chat", [])
    if not keys:
        raise HTTPException(503, "Nenhuma chave configurada para transcrição de áudio.")

    last_error = "Sem chaves"
    for key in keys:
        try:
            async with httpx.AsyncClient(timeout=300.0) as client:
                r = await client.post(
                    f"{BASE_URL}/audio/transcriptions",
                    headers={"Authorization": f"Bearer {key}"},
                    files={"file": (filename, audio_bytes, "audio/webm")},
                    data={"model": "whisper-1", "language": "pt"},
                )
            if r.status_code == 200:
                return r.json().get("text", "")
            last_error = f"HTTP {r.status_code}: {r.text[:200]}"
            if r.status_code in (401, 403):
                continue
        except Exception as exc:
            last_error = str(exc)
            continue

    raise HTTPException(503, f"Transcrição falhou. Último erro: {last_error}")


# ── Models ────────────────────────────────────────────────────────────────────

class GenerateRequest(BaseModel):
    transcript: str
    document_type: str
    patient_name: Optional[str] = ""
    session_date: Optional[str] = ""
    psychologist_name: Optional[str] = ""
    additional_context: Optional[str] = ""
    model: Optional[str] = "deepseek-chat"


class KeysUpdateRequest(BaseModel):
    chat: Optional[list] = None
    audio: Optional[list] = None


# ── Routes ────────────────────────────────────────────────────────────────────

@app.post("/api/transcribe")
async def transcribe(audio: UploadFile = File(...)):
    content = await audio.read()
    text = await call_whisper(content, audio.filename or "session.webm")
    return {"transcript": text}


@app.post("/api/generate")
async def generate(req: GenerateRequest):
    if not req.transcript.strip():
        raise HTTPException(400, "Transcrição está vazia.")
    if req.document_type not in DOCUMENT_PROMPTS:
        raise HTTPException(400, f"Tipo de documento inválido: {req.document_type}")

    user_prompt = DOCUMENT_PROMPTS[req.document_type].format(
        transcript=req.transcript,
        patient_name=req.patient_name or "Não informado",
        session_date=req.session_date or "Não informado",
        psychologist_name=req.psychologist_name or "Não informado",
        additional_context=f"\nContexto adicional: {req.additional_context}" if req.additional_context else "",
    )

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]

    result = await call_chat(messages, model=req.model or "deepseek-chat")
    return {"document": result, "type": req.document_type}


@app.get("/api/keys/status")
async def keys_status():
    data = load_keys()
    chat_keys = data.get("chat", [])
    audio_keys = data.get("audio", [])
    return {
        "chat_count": len(chat_keys),
        "audio_count": len(audio_keys),
        "has_chat": len(chat_keys) > 0,
        "has_audio": len(audio_keys) > 0 or len(chat_keys) > 0,
    }


@app.post("/api/keys/update")
async def update_keys(req: KeysUpdateRequest):
    data = load_keys()
    if req.chat is not None:
        data["chat"] = [k.strip() for k in req.chat if k.strip()]
    if req.audio is not None:
        data["audio"] = [k.strip() for k in req.audio if k.strip()]
    save_keys(data)
    return {
        "status": "ok",
        "chat_count": len(data.get("chat", [])),
        "audio_count": len(data.get("audio", [])),
    }


@app.get("/api/document-types")
async def document_types():
    return {
        "types": [
            {"id": "anamnese", "label": "Anamnese Psicológica"},
            {"id": "evolucao", "label": "Evolução de Sessão"},
            {"id": "soap", "label": "Nota SOAP"},
            {"id": "relatorio", "label": "Relatório Psicológico"},
            {"id": "declaracao", "label": "Declaração de Comparecimento"},
            {"id": "resumo", "label": "Resumo da Sessão"},
            {"id": "hipoteses", "label": "Hipóteses Clínicas e Temas Centrais"},
            {"id": "plano_terapeutico", "label": "Plano Terapêutico"},
        ]
    }


# Serve frontend (must be last)
_frontend = Path(__file__).parent.parent / "frontend"
if _frontend.exists():
    app.mount("/", StaticFiles(directory=str(_frontend), html=True), name="static")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
