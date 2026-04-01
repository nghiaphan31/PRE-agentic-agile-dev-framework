# Decision Log — Architecture Decision Records (ADR)

> ⚠️ **APPEND ONLY** — RULE MB-3: This file is APPEND ONLY. Never overwrite, delete, or edit existing ADRs. Only append new decisions at the bottom. To update status, append a new entry with the new status.

> 📋 **RULE G-0**: Every plan creates a branch. Every branch implements a plan.

---

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

---

## ADR-011 : Anthropic Batch API pour Coherence Audits
**Date :** 2026-04-01
**Statut :** Accepte

**Contexte :**
Les audits de coherence v2.6 (14 P0, 17 P1, 14 P2) ont ete realises via l'API Batch Claude Sonnet. L'API Batch permet un traitement asynchrone de 11 requetes en ~2 minutes pour $1.20 USD, contre plusieurs heures de traitement interactif.

**Decision :**
- L'Anthropic Batch API est adoptee comme outil standard pour les audits de coherence
- Les scripts `scripts/batch/submit.py`, `scripts/batch/retrieve.py`, `scripts/batch/poll.py` constituent le toolkit canonical
- Les resultats sont stockes dans `batch_artifacts/BATCH-YYYY-MM-DD-NNNN.txt` (schema BATCH-date-seq)
- Un ADR est obligatoire pour documenter l'adoption de nouvelles technologies impactant l'architecture

**Consequences :**
- Audit de coherence complet en ~2 minutes vs heures interactives
- Cout reduit ($1.20 vs $20+ pour 11 requetes interactives)
- Traitement parallele natif pour les audits multi-dimensionnels
- Necessite une etape de retrieval distincte (model async)
