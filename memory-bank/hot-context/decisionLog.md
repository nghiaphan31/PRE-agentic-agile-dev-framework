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

---

## ADR-012 : Release-Specific DOC-3 and DOC-5
**Date :** 2026-04-02
**Statut :** Accepte

**Contexte :**
Tous les 5 documents canoniques etaient traites comme documents cumulatifs (RULE 12). Cependant, DOC-3 (Implementation Plan) et DOC-5 (Release Notes) ne sont pas adaptes au format cumulatif :
- DOC-3 doit documenter uniquement le scope de la release actuelle
- DOC-5 doit documenter uniquement les changements de la release actuelle

**Decision :**
- DOC-1 (PRD), DOC-2 (Architecture), DOC-4 (Operations) restent cumulatifs
- DOC-3 (Implementation Plan) devient release-specific — seul le scope de la release actuelle
- DOC-5 (Release Notes) devient release-specific — seul les changements de la release actuelle
- Seuils de lignes reduits pour DOC-3 (100 lignes min) et DOC-5 (50 lignes min)
- Les versions historiques sont preservees dans docs/releases/vX.Y/

**Coherence avec RULE 12 :**
- R-CANON-0 : Classification en deux types (cumulatif vs release-specific)
- R-CANON-A : Les documents release-specifiques sont conserves dans docs/releases/vX.Y/
- R-CANON-5 : Les 3 documents cumulatifs (DOC-1, DOC-2, DOC-4) doivent etre mis a jour ensemble
- R-CANON-6 : Les DOC-3 et DOC-5 sont mis a jour independamment par release
- R-CANON-7 : Les pointeurs CURRENT pour DOC-3 et DOC-5 pointent vers leurs dernieres versions release-specific

**Consequences :**
- Reduction de la taille des documents DOC-3 et DOC-5
- Focus sur le contenu de la release actuelle
- Historique preserve dans docs/releases/vX.Y/
- Meilleure lisibilite et maintenance

---

## ADR-013 : Ideation-to-Release Journey — Operational Reference Chapter in DOC-4
**Date :** 2026-04-08
**Statut :** Proposal

**Contexte :**
Suite a la completion de IDEA-012A/B/C qui implementent la gouvernance idee-to-release (regles, outillage, workflows), il manque une documentation operationnelle de reference. Le besoin est de creer un chapitre dedie dans DOC-4 qui decrit le parcours complet avec WHO/WHAT/WITH WHOM/WHERE/HOW pour chaque phase.

**Proposition :**
- Ajouter un nouveau chapitre dans DOC-4 (Operations Guide)
- Chapitre: "Ideation-to-Release Journey — Operational Reference"
- Documenter les 10 phases principales avec:
  - WHO: Role(s) implique(s)
  - WHAT: Livrable attendu
  - WITH WHOM: Collaboration avec autres roles
  - WHERE: Contexte branche Git
  - HOW: Outils utilises, entrees/dependances, regles appliquees
- Inclure les arbres de decision pour les chemins alternatifs
- Rendre le chapitre exhaustif et detaille

**Consequences :**
- Documentation operationnelle complete pour les nouveaux membres
- Reference unique pour comprendre le processus complet
- Complementaire a IDEA-012A/B/C (implementation vs documentation)

**Sync Analysis:**
- 🟢 NO_OVERLAP: IDEA-012A/B/C = implementation machinery, IDEA-022 = operational runbook
- 🟢 NO_DEPENDENCY: Pas de dependance sur des branches ou idees actives

---

## ADR-014 : IDEA-020 — Authoritative Orchestrator as Default Mode
**Date :** 2026-04-08
**Statut :** ACCEPTED

**Contexte :**
IDEA-020 a ete capture avec une hypothese incorrecte: que le mode orchestrator devait etre defini dans .roomodes. Analyse ulterieure a revele que orchestrator est un mode NATIF de Roo Code (built-in), pas un mode custom. Le fichier .roomodes ne definit que les modes persona custom (product-owner, scrum-master, developer, qa-engineer).

**Decision :**
- Hard blocker #1 RESOLVED: Orchestrator mode already exists as built-in
- Remaining blockers:
  - #2: No autonomous mode-switching mechanism (Roo Code limitation)
  - #3: No handoff state schema defined
- Focus on:
  1. Investigate Roo Code configuration for default mode
  2. Implement mandatory handoff protocol via .clinerules rules
  3. Define handoff state schema in memory-bank/hot-context/handoff-state.md

**Fichiers mis a jour :**
- docs/ideas/IDEA-020-orchestrator-authoritative-default.md — Status [ACCEPTED], corrected problem statement
- docs/ideas/IDEAS-BACKLOG.md — IDEA-020 status changed to [ACCEPTED]
- memory-bank/hot-context/handoff-state.md — NEW: handoff state schema defined

**Consequences :**
- Orchestrator is built-in and available immediately
- Need to investigate default mode configuration in Roo Code
- Handoff protocol requires .clinerules rules addition
- Target release: v2.10
