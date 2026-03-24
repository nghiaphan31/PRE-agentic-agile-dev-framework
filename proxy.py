# -*- coding: utf-8 -*-
"""
le workbench Proxy v2.6.0 — Pont Roo Code <-> Gemini Chrome
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
                         FIX-021 — Detection balises XML echappees markdown (\\<read_file\\>) avec message specifique (GAP R2-002)
  v2.3.0 - 2026-03-23 : FIX-022 — GEM MODE n'envoie que le dernier message [USER] (pas l'historique) pour eviter contamination de contexte (GAP R2-003)
  v2.4.0 - 2026-03-23 : FIX-023 — Suppression des blocs <environment_details>, <SYSTEM>, <task>, <feedback> injectes par Roo Code (GAP R2-004)
  v2.5.0 - 2026-03-23 : FIX-024 — Extraction du texte utilisateur pur avant le premier bloc injecte par Roo Code (GAP R2-005)
                         Remplace l'approche regex strip par une extraction "avant le premier tag injecte"
  v2.5.1 - 2026-03-24 : FIX-025 — Ajout <user_message> dans _ROO_INJECTION_START_TAGS (REVERTED par FIX-026) (GAP R2-006)
  v2.6.0 - 2026-03-24 : FIX-026 — Correction structure reelle messages Roo Code (GAP R2-007)
                         Roo Code envoie le message utilisateur dans un message role='tool' encapsule dans <user_message>...</user_message>.
                         FIX-025 etait incorrect : <user_message> n'est PAS un tag d'injection, c'est le wrapper du vrai message utilisateur.
                         Correction : (1) Retrait de <user_message> de _ROO_INJECTION_START_TAGS,
                                      (2) _format_prompt() GEM MODE extrait le contenu de <user_message> dans les messages role='tool'.
"""
import asyncio, hashlib, json, os, re, sys, time, uuid
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

app = FastAPI(title="le workbench Proxy", version="2.6.0")

# FIX-024: Balises d'injection Roo Code — tout ce qui suit le premier de ces tags est du contexte interne (GAP R2-005)
# FIX-026: Structure reelle confirmee par logs DIAG (GAP R2-007) :
#   - Les messages role='user' contiennent uniquement <environment_details> (pas de texte utilisateur)
#   - Le vrai message utilisateur arrive dans un message role='tool' encapsule dans <user_message>...</user_message>
#   - <user_message> N'EST PAS un tag d'injection — c'est le wrapper du vrai message utilisateur
#   - FIX-025 etait incorrect : il coupait a pos=0 et retournait "" pour le vrai message utilisateur
_ROO_INJECTION_START_TAGS = [
    "<environment_details",  # Contexte VSCode (fichiers, onglets, heure, cout, mode)
    "<SYSTEM>",              # System prompt injecte dans les messages user
    "<task>",                # Description de tache injectee
    "<feedback>",            # Feedback utilisateur injecte
]

# FIX-026: Regex pour extraire le contenu d'un message role='tool' encapsule dans <user_message>...</user_message>
_USER_MESSAGE_TAG_RE = re.compile(r"<user_message>\s*(.*?)\s*</user_message>", re.DOTALL)

def _extract_user_text(text: str) -> str:
    """Extrait uniquement le texte utilisateur reel, avant tout bloc injecte par Roo Code. FIX-024

    Roo Code injecte des blocs XML apres le texte utilisateur :
      "Dis bonjour\\n<environment_details>...\\n====\\n\\nREMINDERS..."
    On coupe au premier tag d'injection rencontre et on retourne uniquement ce qui precede.
    Si aucun tag d'injection n'est trouve, on retourne le texte complet.
    """
    cut_pos = len(text)
    first_tag_found = None
    for tag in _ROO_INJECTION_START_TAGS:
        pos = text.find(tag)
        if pos != -1 and pos < cut_pos:
            cut_pos = pos
            first_tag_found = tag
    result = text[:cut_pos].strip()
    # DIAG-LOG: affiche le tag de coupure et le resultat extrait
    print(f"  [DIAG _extract_user_text] input[:80]={repr(text[:80])}")
    print(f"  [DIAG _extract_user_text] first_tag_found={first_tag_found!r} at pos={cut_pos if first_tag_found else 'N/A'}")
    print(f"  [DIAG _extract_user_text] result={repr(result[:120])}")
    return result

def _hash(text: str) -> str:
    return hashlib.md5(text.encode("utf-8")).hexdigest()

def _clean_content(content) -> str:
    """Nettoie le contenu : supprime les images base64, extrait le texte utilisateur pur. REQ-2.1.5, FIX-024"""
    # DIAG-LOG: affiche le type et debut du contenu brut recu
    if isinstance(content, str):
        print(f"  [DIAG _clean_content] type=str, raw[:80]={repr(content[:80])}")
        return _extract_user_text(content)
    if isinstance(content, list):
        print(f"  [DIAG _clean_content] type=list, len={len(content)}, items[0]={repr(str(content[0])[:80]) if content else 'EMPTY'}")
        parts = []
        for item in content:
            if isinstance(item, dict):
                if item.get("type") == "text":
                    parts.append(_extract_user_text(item.get("text", "")))
                elif item.get("type") == "image_url":
                    parts.append("[IMAGE OMISE - Non supportee par le proxy clipboard]")
                else:
                    parts.append(str(item))
        return "\n".join(parts)
    print(f"  [DIAG _clean_content] type=other({type(content).__name__}), raw[:80]={repr(str(content)[:80])}")
    return _extract_user_text(str(content))

def _format_prompt(messages: List[MessageContent]) -> str:
    """Formate les messages en texte lisible. REQ-2.1.3, REQ-2.1.4, REQ-2.2.2

    FIX-022: En GEM MODE, n'envoie que le dernier message [USER] pour eviter la contamination
    de contexte. Le Gem Gemini a ses propres instructions et chaque conversation est nouvelle —
    envoyer l'historique complet fait que Gemini continue le contexte precedent au lieu de
    traiter la nouvelle demande independamment. (GAP R2-003)
    """
    # FIX-022: GEM MODE — extraire uniquement le dernier message utilisateur
    # FIX-026: Structure reelle Roo Code — le vrai message utilisateur arrive dans role='tool'
    #   encapsule dans <user_message>...</user_message>. Les messages role='user' ne contiennent
    #   que <environment_details> (contexte VSCode), pas le texte saisi par l'utilisateur.
    #   Priorite de recherche : (1) dernier role='tool' avec <user_message>, (2) dernier role='user' non-vide
    if USE_GEM_MODE:
        last_user_content = None

        # Priorite 1 : chercher le dernier message role='tool' contenant <user_message>...</user_message>
        for msg in reversed(messages):
            if msg.role == "tool":
                raw = msg.content if isinstance(msg.content, str) else str(msg.content)
                match = _USER_MESSAGE_TAG_RE.search(raw)
                if match:
                    extracted = match.group(1).strip()
                    if extracted:
                        last_user_content = extracted
                        print(f"  [DIAG _format_prompt] FIX-026: extrait de role='tool' <user_message>: {repr(extracted[:80])}")
                        break

        # Priorite 2 : fallback sur le dernier role='user' non-vide (cas sans <user_message>)
        if not last_user_content:
            for msg in reversed(messages):
                if msg.role == "user":
                    content = _clean_content(msg.content)
                    if content.strip():
                        last_user_content = content
                        break

        if last_user_content:
            return "[USER]\n" + last_user_content
        # Fallback final: aucun message utilisateur trouve, envoyer le dernier message quel que soit le role
        for msg in reversed(messages):
            content = _clean_content(msg.content)
            if content.strip():
                return content
        return ""

    # MODE COMPLET (non-GEM): envoyer l'historique complet avec troncature
    parts = []
    for msg in messages:
        content = _clean_content(msg.content)
        if not content.strip():
            continue
        if msg.role == "system":
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
            last_user = full.rfind("[USER]")
            if last_user >= 0:
                truncated = "[...HISTORIQUE TRONQUE...]\n\n---\n\n" + full[last_user:]
            else:
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
    """Detecte les balises XML echappees markdown (ex: \\<read_file\\>). FIX-021"""
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
        # DIAG-LOG: dump structure brute des messages recus de Roo Code
        print(f"  [DIAG chat_completions] {len(request.messages)} messages recus:")
        for i, msg in enumerate(request.messages):
            raw_content = msg.content if isinstance(msg.content, str) else str(msg.content)
            print(f"  [DIAG msg[{i}]] role={msg.role!r}, content[:120]={repr(raw_content[:120])}")
        formatted = _format_prompt(request.messages)
        # DIAG-LOG: dump du prompt final formate
        print(f"  [DIAG _format_prompt] result[:200]={repr(formatted[:200])}")
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
    return {"status": "ok", "proxy": "le workbench", "version": "2.6.0", "gem_mode": USE_GEM_MODE}

if __name__ == "__main__":
    print(f"{'='*60}\n  le workbench PROXY v2.6.0 | http://localhost:{PORT}/v1\n  Mode: {'GEM' if USE_GEM_MODE else 'COMPLET'} | Timeout: {TIMEOUT_SECONDS}s\n{'='*60}")
    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="warning")
