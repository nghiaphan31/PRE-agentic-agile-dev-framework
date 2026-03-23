# Contexte Actif

**Date de mise à jour :** 2026-03-23
**Mode actif :** developer
**Backend LLM actif :** Claude Sonnet API (claude-sonnet-4-6)

## Tâche en cours
Phase 8 — Configuration du commutateur 3 modes LLM dans Roo Code.

## Dernier résultat
FIX-023 appliqué : proxy.py v2.4.0

**Problème diagnostiqué :** Le proxy envoyait les blocs `<environment_details>` injectés par Roo Code dans le contenu des messages. Ces blocs (fichiers ouverts, onglets VSCode, heure, coût, mode actif, liste des reminders) noyaient le vrai message utilisateur. Exemple : "Dis bonjour en une seule phrase." → Gemini ne recevait que `[USER]\n<environment_details>...</environment_details>` sans le texte réel.

**Corrections apportées :**
- **FIX-023** : `_strip_roo_injected_blocks()` supprime via regex les blocs `<environment_details>`, `<SYSTEM>`, `<task>`, `<feedback>` du contenu de chaque message avant envoi à Gemini.
- Appliqué dans `_clean_content()` pour les messages string ET list.
- Import `re` ajouté.

## Prochain(s) pas
- [ ] Redémarrer le proxy (proxy.py v2.4.0)
- [ ] Tester : envoyer "Dis bonjour en une seule phrase." → Gemini doit recevoir uniquement `[USER]\nDis bonjour en une seule phrase.` et répondre avec `<attempt_completion><result>Bonjour !</result></attempt_completion>`
- [ ] Créer profil "ollama_local" dans Roo Code Settings > Providers
- [ ] Créer profil "gemini_proxy" dans Roo Code Settings > Providers
- [ ] Tester Mode 1 Ollama
- [ ] Tester Mode 2 Proxy Gemini
- [ ] Mettre à jour memory-bank/techContext.md avec URLs réelles (étape 8.4)

## Blocages / Questions ouvertes
Aucun blocage actif.

## Dernier commit Git
[à mettre à jour après commit]
