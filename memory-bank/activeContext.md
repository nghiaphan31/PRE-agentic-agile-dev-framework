# Contexte Actif

**Date de mise à jour :** 2026-03-24
**Mode actif :** debug
**Backend LLM actif :** Claude Sonnet API (claude-sonnet-4-6)

## Tâche en cours
Débogage proxy.py — chemin "uplink" Roo → Gemini Chrome.

## Dernier résultat
FIX-026 appliqué : proxy.py v2.6.0

**Problème diagnostiqué (confirmé par logs DIAG) :**
FIX-025 était incorrect. La structure réelle des messages Roo Code est :
- `role='tool'` → contient `<user_message>\nDis bonjour en une seule phrase\n</user_message>` (le vrai message utilisateur)
- `role='user'` → contient uniquement `<environment_details>` (contexte VSCode, pas de texte utilisateur)

FIX-025 avait ajouté `<user_message>` dans `_ROO_INJECTION_START_TAGS`, ce qui faisait couper `_extract_user_text()` à `pos=0` → résultat `""` → prompt vide copié dans le presse-papiers.

**Correction FIX-026 :**
1. Retrait de `<user_message>` de `_ROO_INJECTION_START_TAGS`
2. Ajout de `_USER_MESSAGE_TAG_RE` (regex) pour extraire le contenu entre `<user_message>...</user_message>`
3. `_format_prompt()` GEM MODE cherche en priorité le dernier `role='tool'` contenant `<user_message>`, puis fallback sur `role='user'` non-vide

**Logs DIAG conservés** pour faciliter le débogage futur (peuvent être retirés une fois validé en production).

## Prochain(s) pas
- [ ] Redémarrer le proxy (proxy.py v2.6.0)
- [ ] Tester : envoyer "Dis bonjour en une seule phrase" → Gemini doit recevoir `[USER]\nDis bonjour en une seule phrase`
- [ ] Retirer les logs DIAG une fois le comportement validé (v2.6.1)
- [ ] Continuer Phase 8 : créer profils "ollama_local" et "gemini_proxy" dans Roo Code Settings > Providers

## Blocages / Questions ouvertes
Aucun blocage actif.

## Dernier commit Git
(à mettre à jour après commit)
