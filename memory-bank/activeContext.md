# Contexte Actif

**Date de mise à jour :** 2026-03-23
**Mode actif :** developer
**Backend LLM actif :** Claude Sonnet API (claude-sonnet-4-6)

## Tâche en cours
Phase 8 — Configuration du commutateur 3 modes LLM dans Roo Code.

## Dernier résultat
FIX-024 appliqué : proxy.py v2.5.0

**Problème diagnostiqué :** FIX-023 (regex strip) ne fonctionnait pas correctement — le bloc `<environment_details>` était partiellement supprimé mais le contenu après `</environment_details>` (bloc `====\n\nREMINDERS...`) restait. De plus, le texte utilisateur réel ("Dis bonjour en une seule phrase.") apparaît **avant** le premier tag injecté, pas après.

**Structure réelle d'un message Roo Code :**
```
Dis bonjour en une seule phrase.
<environment_details>
...
</environment_details>
====

REMINDERS
...
```

**Correction FIX-024 :** Remplacement de l'approche "strip regex" par une approche "extraction avant le premier tag injecté" :
- `_extract_user_text()` trouve la position du premier tag d'injection (`<environment_details`, `<SYSTEM>`, `<task>`, `<feedback>`) et retourne uniquement le texte qui précède.
- Résultat : Gemini reçoit uniquement `[USER]\nDis bonjour en une seule phrase.`

## Prochain(s) pas
- [ ] Redémarrer le proxy (proxy.py v2.5.0)
- [ ] Tester : envoyer "Dis bonjour en une seule phrase." → Gemini doit recevoir `[USER]\nDis bonjour en une seule phrase.`
- [ ] Créer profil "ollama_local" dans Roo Code Settings > Providers
- [ ] Créer profil "gemini_proxy" dans Roo Code Settings > Providers
- [ ] Tester Mode 1 Ollama
- [ ] Tester Mode 2 Proxy Gemini
- [ ] Mettre à jour memory-bank/techContext.md avec URLs réelles (étape 8.4)

## Blocages / Questions ouvertes
Aucun blocage actif.

## Dernier commit Git
[à mettre à jour après commit]
