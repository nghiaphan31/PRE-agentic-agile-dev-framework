# -*- coding: utf-8 -*-
"""
le workbench Proxy v2.2.0 — Pont Roo Code <-> Gemini Chrome
Supporte stream=true (SSE) et stream=false (JSON complet).
Exigences: REQ-2.1.1 a REQ-2.4.4

Changelog:
  v2.0.0 - 2026-03-23 : Creation initiale (DA-006, DA-007, DA-008, DA-009, DA-014)
  v2.0.1 - 2026-03-23 : FIX-001 — Console multi-ligne avec avertissement NOUVELLE conversation (GAP-006)
  v2.0.2 - 2026-03-23 : FIX-004 — try/except autour de pyperclip.paste() pour eviter crash si presse-papiers verrouille (P-003)
  v2.0.3 - 2026-03-23 : FIX-005 — Compteur de requetes dans la console pour distinguer les requetes concurrentes (P-002)
  v2.0.4 - 2026-03-23 : FIX-006 — Verification longueur minimale du contenu colle (GAP-005)
  v2.0.5 - 2026-03-23 : FIX-008 — Troncature automatique de l'historique via MAX_HISTORY_CHARS (GAP-001)
  v2.0.6 - 2026-03-23 : FIX-014 — Verification longueur minimale BLOQUANTE (seuil 100 chars) pour eviter injection de contenu parasite (REG-001)
  v2.0.7 - 2026-03-23 : FIX-015 — Garde runtime <new_task> dans _wait_clipboard() pour eviter deadlock (GAP R1-003)
  v2.0.8 - 2026-03-23 : FIX-016 — Fallback troncature dans _format_prompt() quand un seul message depasse MAX_HISTORY_CHARS (REG-002)
  v2.0.9 - 2026-03-23 : FIX-017 — asyncio.Lock() pour serialisation du presse-papiers (GAP R1-004)
  v2.1.0 - 2026-03-23 : FIX-018 — Suppression "ou effacer l'historique existant" — TOUJOURS NOUVELLE conversation (GAP R1-001)
  v2.1.1 - 2026-03-23 : FIX-019 — Force UTF-8 stdout sur Windows pour eviter UnicodeEncodeError cp1252
  v2.2.0 - 2026-03-23 : FIX-020 — Validation XML bloquante (Gemini texte libre bloque comme <new_task>) (GAP R2-001)
                         FIX-021 — Detection balises XML echappees markdown (\<read_file\>) avec message specifique (GAP R2-002)
"""
import asyncio, hashlib, json, os, sys, time, uuid
from datetime import datetime
from typing import AsyncGenerator, List, Optional, Union

# FIX-019: Force UTF-8 stdout sur Windows (cp1252 ne supporte pas les caracteres Unicode etendus)
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import pyperclip, uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel

USE_GEM_MODE = os.getenv("USE_GEM_MODE", "true").lower() == "true"
POLLING_INTERVAL = float(os.getenv("POLLING_INTERVAL", "1.0"))
TIMEOUT_SECONDS = int(os.getenv("TIMEOUT_SECONDS", "300"))
PORT = int(os.getenv("PROXY_PORT", "8000"))
# FIX-008: Limite de taille de l'historique pour eviter l'explosion du presse-papiers (GAP-001)
MAX_HISTORY_CHARS = int(os.getenv("MAX_HISTORY_CHARS", "40000"))

# FIX-005: Compteur de requetes pour distinguer les requetes concurrentes dans la console (P-002)
_request_counter = 0

# FIX-017: Verrou asyncio pour serialiser l'acces au presse-papiers (GAP R1-004)
# Deux requetes concurrentes partagent le meme presse-papiers — sans verrou, les deux polleraient
# simultanement et retourneraient la meme reponse. Le verrou force la mise en file d'attente.
_clipboard_lock = asyncio.Lock()

ROO_XML_TAGS = [
    "<write_to_file>", "<read_file>", "<execute_command>",
    "<attempt_completion>", "<ask_followup_question>", "<replace_in_file>",
    "<list_files>", "<search_files>", "<browser_action>", "<new_task>"
]

class MessageContent(BaseModel):
    role: str
    content: Union[str, list]

class ChatRequest(BaseModel):
    model: str
    messages: List[MessageContent]
    temperature: Optional[float] = 0.0
    max_tokens: Optional[int] = None
    stream: Optional[bool] = False

app = FastAPI(title="le workbench Proxy", version="2.2.0")

def _hash(text: str) -> str:
    return hashlib.md5(text.encode("utf-8")).hexdigest()

def _clean_content(content) -> str:
    """Nettoie le contenu : supprime les images base64. REQ-2.1.5"""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, dict):
                if item.get("type") == "text":
                    parts.append(item.get("text", ""))
                elif item.get("type") == "image_url":
                    parts.append("[IMAGE OMISE - Non supportee par le proxy clipboard]")
                else:
                    parts.append(str(item))
        return "\n".join(parts)
    return str(content)

def _format_prompt(messages: List[MessageContent]) -> str:
    """Formate les messages en texte lisible. REQ-2.1.3, REQ-2.1.4, REQ-2.2.2"""
    parts = []
    for msg in messages:
        content = _clean_content(msg.content)
        if not content.strip():
            continue
        if msg.role == "system":
            if USE_GEM_MODE:
                continue
            parts.append("[SYSTEM PROMPT]\n" + content)
        elif msg.role == "user":
            parts.append("[USER]\n" + content)
        elif msg.role == "assistant":
            parts.append("[ASSISTANT]\n" + content)

    full = "\n\n---\n\n".join(parts)
    # FIX-008: Troncature de l'historique si depassement de MAX_HISTORY_CHARS (GAP-001)
    if len(full) > MAX_HISTORY_CHARS:
        truncated = full[-MAX_HISTORY_CHARS:]
        # Trouver la premiere frontiere de section complete pour eviter un decoupe au milieu d'un message
        boundary = truncated.find("[USER]")
        if boundary > 0:
            truncated = "[...HISTORIQUE TRONQUE...]\n\n---\n\n" + truncated[boundary:]
        else:
            # FIX-016: Fallback quand un seul message depasse MAX_HISTORY_CHARS (REG-002)
            # boundary == -1 signifie qu'aucun [USER] n'existe dans les derniers MAX_HISTORY_CHARS chars
            # => un seul message depasse la limite. On cherche le dernier [USER] dans le texte complet
            # pour garantir que Gemini recoit toujours un message complet avec en-tete de contexte.
            last_user = full.rfind("[USER]")
            if last_user >= 0:
                truncated = "[...HISTORIQUE TRONQUE...]\n\n---\n\n" + full[last_user:]
            else:
                # Aucun [USER] dans tout le texte (ex: uniquement des messages [ASSISTANT])
                # On retourne le texte brut tronque avec l'en-tete de contexte
                truncated = "[...HISTORIQUE TRONQUE...]\n\n---\n\n" + truncated
        print(f"  AVERTISSEMENT: Historique tronque ({len(full)} -> {len(truncated)} chars)")
        return truncated
    return full

# FIX-021: Balises XML echappees markdown — Gemini echappe parfois les < > en \< \> (GAP R2-002)
ROO_XML_TAGS_ESCAPED = [tag.replace("<", r"\<").replace(">", r"\>") for tag in ROO_XML_TAGS]

def _validate_response(text: str) -> bool:
    """Verifie la presence de balises XML Roo Code. REQ-2.3.4"""
    return any(tag in text for tag in ROO_XML_TAGS)

def _has_escaped_xml(text: str) -> bool:
    """Detecte les balises XML echappees markdown (ex: \<read_file\>). FIX-021"""
    return any(tag in text for tag in ROO_XML_TAGS_ESCAPED)

def _build_json_response(content: str, model: str) -> dict:
    """Construit une reponse JSON OpenAI. REQ-2.4.2"""
    return {
        "id": "chatcmpl-proxy-" + uuid.uuid4().hex[:8],
        "object": "chat.completion",
        "created": int(time.time()),
        "model": model,
        "choices": [{"index": 0, "message": {"role": "assistant", "content": content}, "finish_reason": "stop"}],
        "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
    }

async def _stream_response(content: str, model: str) -> AsyncGenerator[str, None]:
    """Genere une reponse SSE en un seul chunk. REQ-2.4.1, DA-014"""
    rid = "chatcmpl-proxy-" + uuid.uuid4().hex[:8]
    ts = int(time.time())
    chunk = {"id": rid, "object": "chat.completion.chunk", "created": ts, "model": model,
             "choices": [{"index": 0, "delta": {"role": "assistant", "content": content}, "finish_reason": None}]}
    yield f"data: {json.dumps(chunk)}\n\n"
    done = {"id": rid, "object": "chat.completion.chunk", "created": ts, "model": model,
            "choices": [{"index": 0, "delta": {}, "finish_reason": "stop"}]}
    yield f"data: {json.dumps(done)}\n\n"
    yield "data: [DONE]\n\n"

async def _wait_clipboard(initial_hash: str, ts: str) -> str:
    """Attend la reponse Gemini dans le presse-papiers. REQ-2.3.1, REQ-2.3.2, REQ-2.3.3"""
    start = time.time()
    while True:
        await asyncio.sleep(POLLING_INTERVAL)
        # FIX-004: try/except pour eviter crash si presse-papiers verrouille ou contenu non-texte (P-003)
        try:
            current = pyperclip.paste()
        except Exception as e:
            print(f"[{ts}] AVERTISSEMENT: Erreur acces presse-papiers: {e}")
            continue
        if _hash(current) != initial_hash:
            elapsed = time.time() - start
            print(f"[{ts}] REPONSE DETECTEE ! {len(current)} chars en {elapsed:.1f}s")
            # FIX-014: Verification longueur minimale BLOQUANTE — seuil 100 chars (REG-001)
            # Remplace FIX-006 (seuil 20, non-bloquant) : le contenu trop court est ignore
            # et le proxy continue de poller pour eviter d'injecter du contenu parasite dans Roo Code.
            if len(current) < 100:
                print(f"[{ts}] ⚠️  CONTENU TROP COURT ({len(current)} chars) — IGNORE : {repr(current[:50])}")
                print(f"[{ts}]    Verifiez que vous avez copie la reponse Gemini COMPLETE (Ctrl+A puis Ctrl+C)")
                initial_hash = _hash(current)
                continue
            # FIX-015: Garde runtime <new_task> — bloque l'injection si Gemini ignore la Regle 9 de SP-007 (GAP R1-003)
            # <new_task> en mode proxy cause un deadlock (deux instances Roo Code partagent le meme presse-papiers).
            if "<new_task>" in current:
                print(f"[{ts}] 🚫 ERREUR CRITIQUE : La reponse Gemini contient <new_task> !")
                print(f"[{ts}]    Les Boomerang Tasks ne sont PAS supportees en Mode Proxy (deadlock presse-papiers).")
                print(f"[{ts}]    ACTION REQUISE : Demandez a Gemini de reformuler sans <new_task>.")
                print(f"[{ts}]    Copiez la reponse corrigee (sans <new_task>) pour continuer.")
                initial_hash = _hash(current)
                continue
            # FIX-020: Validation XML BLOQUANTE — Gemini en texte libre est bloque comme <new_task> (GAP R2-001)
            # Avant: avertissement non-bloquant => Roo Code recevait du texte libre => boucle infinie de requetes
            # Apres: le proxy continue de poller et demande a l'utilisateur de reformuler
            if not _validate_response(current):
                # FIX-021: Detection specifique des balises echappees markdown \<tag\> (GAP R2-002)
                if _has_escaped_xml(current):
                    print(f"[{ts}] 🚫 ERREUR : Balises XML echappees detectees (ex: \\<read_file\\> au lieu de <read_file>)")
                    print(f"[{ts}]    Gemini a echappe les balises XML avec des backslashes (rendu Markdown).")
                    print(f"[{ts}]    ACTION REQUISE : Dans Gemini, demandez : 'Reformule ta reponse en texte brut")
                    print(f"[{ts}]    sans echapper les balises XML (pas de backslash devant < et >)'")
                    print(f"[{ts}]    Puis Ctrl+A Ctrl+C pour copier la reponse corrigee.")
                else:
                    print(f"[{ts}] 🚫 ERREUR : Aucune balise XML Roo Code detectee — reponse en texte libre.")
                    print(f"[{ts}]    Gemini a repondu en langage naturel au lieu d'utiliser les balises XML.")
                    print(f"[{ts}]    ACTION REQUISE : Dans Gemini, demandez : 'Reformule ta reponse en utilisant")
                    print(f"[{ts}]    les balises XML Roo Code (ex: <read_file>, <attempt_completion>, etc.)'")
                    print(f"[{ts}]    Puis Ctrl+A Ctrl+C pour copier la reponse corrigee.")
                initial_hash = _hash(current)
                continue
            return current
        if time.time() - start > TIMEOUT_SECONDS:
            raise HTTPException(status_code=408, detail="Timeout: Relancez votre requete dans Roo Code.")

@app.post("/v1/chat/completions")
async def chat_completions(request: ChatRequest):
    """Point d'entree principal. REQ-2.1.1, REQ-2.1.2"""
    # FIX-005: Increment global request counter to distinguish concurrent requests (P-002)
    global _request_counter
    _request_counter += 1
    req_num = _request_counter
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"\n{'='*60}\n[{ts}] REQUETE #{req_num} | modele: {request.model} | stream: {request.stream}")
    # FIX-017: Serialisation du presse-papiers via asyncio.Lock() (GAP R1-004)
    # Si le verrou est deja pris par une autre requete, on attend et on avertit l'utilisateur.
    if _clipboard_lock.locked():
        print(f"[{ts}] ⏳ REQUETE #{req_num} EN ATTENTE — Le presse-papiers est occupe par une autre requete.")
        print(f"[{ts}]    Cette requete sera traitee automatiquement des que la precedente sera terminee.")
    async with _clipboard_lock:
        ts = datetime.now().strftime("%H:%M:%S")
        formatted = _format_prompt(request.messages)
        pyperclip.copy(formatted)
        initial_hash = _hash(formatted)
        print(f"[{ts}] {'GEM MODE' if USE_GEM_MODE else 'MODE COMPLET'} | {len(formatted)} chars")
        # FIX-001: Multi-line console with explicit NOUVELLE conversation warning (GAP-006)
        print(f"[{ts}] ══════════════════════════════════════════════════")
        print(f"[{ts}] PROMPT COPIE ({len(formatted)} chars) — ACTIONS REQUISES :")
        print(f"         1. Chrome → gemini.google.com → Gem 'Roo Code Agent'")
        print(f"         2. ⚠️  TOUJOURS ouvrir une NOUVELLE conversation Gemini")
        print(f"         3. Ctrl+V pour coller le prompt")
        print(f"         4. Attendre la fin de la reponse Gemini")
        print(f"         5. Ctrl+A puis Ctrl+C pour copier TOUTE la reponse")
        print(f"         ⚠️  Ne pas utiliser le presse-papiers pour autre chose !")
        print(f"         Timeout dans {TIMEOUT_SECONDS}s...")
        response_text = await _wait_clipboard(initial_hash, ts)
    if request.stream:
        return StreamingResponse(_stream_response(response_text, request.model), media_type="text/event-stream")
    return JSONResponse(content=_build_json_response(response_text, request.model), status_code=200)

@app.get("/v1/models")
async def list_models():
    return JSONResponse({"object": "list", "data": [{"id": "gemini-manual", "object": "model", "created": int(time.time()), "owned_by": "uadf-proxy"}]})

@app.get("/health")
async def health_check():
    return {"status": "ok", "proxy": "le workbench", "version": "2.2.0", "gem_mode": USE_GEM_MODE}

if __name__ == "__main__":
    print(f"{'='*60}\n  le workbench PROXY v2.2.0 | http://localhost:{PORT}/v1\n  Mode: {'GEM' if USE_GEM_MODE else 'COMPLET'} | Timeout: {TIMEOUT_SECONDS}s\n{'='*60}")
    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="warning")
