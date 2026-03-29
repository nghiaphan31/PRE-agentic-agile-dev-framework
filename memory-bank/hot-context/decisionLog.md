# Decision Log — Architecture Decision Records (ADR)

---

## ADR-010 : Ad-Hoc Idea Governance — From Discovery to Release
**Date :** 2026-03-29
**Statut :** Accepte

**Contexte :**
IDEA-009 (Generic Anthropic Batch API Toolkit) a emerge de maniere reactive pendant l'audit de coherence v2.3. Le processus standard (DOC-1 → DOC-2 → DOC-3 → pipeline Calypso → release) n'etait pas adapte. Cependant, GitFlow et les 5 documents canoniques restent non negociables.

**Decision :**
Deux chemins de gouvernance :
- Path 1 [STRUCTURED] : processus complet pour ideas planifiees via PRD
- Path 2 [AD-HOC] : processus leger pour ideas reactives, avec triage de release tier (Minor/Medium/Major)
  - Minor : bug fixes, dev-tooling, pas de pipeline Calypso, tests unitaires + integration
  - Medium : nouvelles features, peut utiliser pipeline Calypso partiellement
  - Major : changements architecturaux, processus complet obligatoire
- Tous les 5 documents canoniques (DOC-1 a DOC-5) doivent etre mis a jour quel que soit le chemin
- ADR obligatoire pour chaque idea ad-hoc
- Tests obligatoires et complets quel que soit le tier

**Coherence DOC-1 / DOC-2 — Non-Negotiable :**
- DOC-1 (PRD) et DOC-2 (Architecture) doivent etre coherents, auto-contenus et complets a tout moment
- Aucune lacune de documentation (requirements ou architecture) n'est acceptable
- Quand DOC-1 change, DOC-2 doit etre revu pour coherence
- Quand DOC-2 change, DOC-1 doit etre verifie pour complétude

**Consequences :**
- Fast path pour improvements a bas risque
- Cadre de decision clair pour le tier de release
- GitFlow et 5 docs toujours maintenu
- Aucune idea ne tombe entre les gouttes

---

## ADR-006 : Adoption du modele GitFlow develop / develop-vX.Y / main
**Date :** 2026-03-28
**Statut :** Accepte

(Contenu complet dans docs/ideas/IDEA-003-release-governance.md)
