# Contexte Actif

**Date de mise à jour :** 2026-03-23
**Mode actif :** developer
**Backend LLM actif :** Claude Sonnet API (claude-sonnet-4-6)

## Tâche en cours
Phase 8 — Configuration du commutateur 3 modes LLM dans Roo Code.

## Dernier résultat
FIX-020 + FIX-021 appliqués : proxy.py v2.2.0

**Problème diagnostiqué :** Gemini répondait en texte libre (sans balises XML) ou avec des balises XML échappées markdown (`\<read_file\>`), causant une boucle infinie de requêtes dans Roo Code.

**Corrections apportées :**
- **FIX-020** : Validation XML maintenant BLOQUANTE — si Gemini répond sans balises XML, le proxy continue de poller et affiche un message d'action clair pour l'utilisateur (comme le garde `<new_task>`)
- **FIX-021** : Détection spécifique des balises XML échappées markdown (`\<read_file\>`) avec message d'erreur dédié
- **SP-007 v1.6.0** : Règles 11 et 12 ajoutées — interdiction explicite d'échapper les balises XML et d'utiliser du texte libre sans balise XML

## Prochain(s) pas
- [ ] Redémarrer le proxy (proxy.py v2.2.0)
- [ ] Mettre à jour le Gem Gemini manuellement avec SP-007 v1.6.0 (DEPLOIEMENT MANUEL REQUIS)
- [ ] Tester : envoyer "Dis bonjour en une phrase." → Gemini doit répondre avec `<attempt_completion>`
- [ ] Créer profil "ollama_local" dans Roo Code Settings > Providers
- [ ] Créer profil "gemini_proxy" dans Roo Code Settings > Providers
- [ ] Tester Mode 1 Ollama (envoyer message depuis Roo Code, vérifier logs Ollama sur calypso)
- [ ] Tester Mode 2 Proxy Gemini (proxy affiche PROMPT COPIE !)
- [ ] Mettre à jour memory-bank/techContext.md avec URLs réelles (étape 8.4)

## Blocages / Questions ouvertes
⚠️ DEPLOIEMENT MANUEL REQUIS : Mettre à jour le Gem Gemini avec SP-007 v1.6.0 (template/prompts/SP-007-gem-gemini-roo-agent.md)

## Dernier commit Git
248f2a3 — fix(proxy): v2.2.0 FIX-020+FIX-021 — validation XML bloquante + detection balises echappees markdown - DEPLOIEMENT MANUEL REQUIS : mettre a jour le Gem Gemini avec SP-007 v1.6.0
