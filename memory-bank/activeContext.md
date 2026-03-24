# Contexte Actif

**Date de mise à jour :** 2026-03-24
**Mode actif :** debug
**Backend LLM actif :** Claude Sonnet API (claude-sonnet-4-6)

## Tâche en cours
Débogage proxy.py — chemin "downlink" Gemini → Roo Code : "Model Response Incomplete".

## Dernier résultat
FIX-028 appliqué : proxy.py v2.8.0

**Problème diagnostiqué :**
Roo Code affichait "Model Response Incomplete — The model failed to use any tools" même après que FIX-027 avait correctement désechappé la réponse Gemini.

**Cause racine :** L'ancien `_stream_response()` envoyait `role` ET `content` dans le même delta chunk SSE :
```json
{"delta": {"role": "assistant", "content": "<attempt_completion>..."}}
```
Le format OpenAI standard exige deux chunks séparés :
- Chunk 1 : `{"delta": {"role": "assistant"}}` (role seul)
- Chunk 2 : `{"delta": {"content": "..."}}` (content seul)
- Chunk 3 : `{"delta": {}, "finish_reason": "stop"}`

Roo Code ne parsait pas les balises XML quand role+content arrivaient ensemble.

**Correction FIX-028 :** `_stream_response()` envoie maintenant 3 chunks séparés conformes au format OpenAI.

**Historique des fixes de cette session :**
- FIX-026 (v2.6.0) : uplink — extraction du message utilisateur depuis `role='tool'` `<user_message>`
- FIX-027 (v2.7.0) : downlink — désechappement Markdown automatique `\<tag\>` → `<tag>`
- FIX-028 (v2.8.0) : downlink — format SSE streaming conforme OpenAI (role/content séparés)

## Prochain(s) pas
- [ ] Redémarrer le proxy (proxy.py v2.8.0)
- [ ] Tester : envoyer message → Gemini répond → proxy accepte → Roo Code exécute `<attempt_completion>` sans "Model Response Incomplete"
- [ ] Retirer les logs DIAG une fois le comportement validé (v2.8.1)
- [ ] Continuer Phase 8 : créer profils "ollama_local" et "gemini_proxy" dans Roo Code Settings > Providers

## Blocages / Questions ouvertes
Aucun blocage actif.

## Dernier commit Git
(à mettre à jour après commit)
