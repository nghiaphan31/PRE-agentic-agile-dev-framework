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

## ADR-015 : Co-Acceptance of IDEA-014 and IDEA-015
**Date :** 2026-04-08
**Statut :** Accepted

**Contexte :**
IDEA-014 (Canonical Docs Status Governance) et IDEA-015 (Mandatory Release Coherence Audit) ont été affinés ensemble lors de la session REFINEMENT-2026-04-08-003. L'affinage a révélé que ces idées sont **complémentaires et interdépendantes** :

| Aspect | IDEA-014 | IDEA-015 |
|--------|----------|----------|
| **Rôle** | Politique/Spécification | Application/Mise en œuvre |
| **Livrable** | Amélioration de la RÈGLE 8, définition du cycle de vie des statuts | Passerelle de version GitHub Actions |
| **Validation** | Règles de transition de statut documentées | Règles de transition de statut suivies |

**Insight clé :** IDEA-014 fournit la **SPÉCIFICATION** (ce que doit être le cycle de vie des statuts), tandis que IDEA-015 fournit l'**APPLICATION** (comment s'assurer que le cycle de vie est respecté). Aucune idée n'est complète sans l'autre.

**Décision :**
**Co-accepter IDEA-014 et IDEA-015 ensemble comme [ACCEPTED] pour la v2.7.**

Cette décision est basée sur :
1. **Atomicité** : Les idées ont été affinées ensemble et dépendent l'une de l'autre pour une mise en œuvre complète
2. **Complétude** : Le critère d'acceptation AC-4 de IDEA-014 ne peut être vérifié sans la passerelle de version de IDEA-015
3. **Intégrité de la gouvernance** : Une politique sans application est inefficace ; une application sans politique est sans direction

**Mises à jour des statuts :**

| Idée | Statut précédent | Nouveau statut | Notes |
|------|------------------|----------------|-------|
| IDEA-014 | [REFINED] | [ACCEPTED] | Co-acceptée avec IDEA-015 |
| IDEA-015 | [REFINED] | [ACCEPTED] | Co-acceptée avec IDEA-014 |

**Fichiers mis à jour :**
- docs/ideas/IDEAS-BACKLOG.md — Status IDEA-014 et IDEA-015 changés vers [ACCEPTED]
- docs/ideas/IDEA-014-canonical-docs-status-governance.md — Status changé vers [ACCEPTED], historique mis à jour
- docs/ideas/IDEA-015-mandatory-release-coherence-audit.md — Status changé vers [ACCEPTED], historique mis à jour
- docs/ideas/ADR-013-co-accept-idea-014-015.md — NOUVEAU: Document d'ADR pour la co-acceptation

**Conséquences :**

### Positives
- **Complétude de la gouvernance** : La politique et l'application sont désormais formellement acceptées
- **Intégrité des versions** : La version v2.7 inclura à la fois la définition du cycle de vie des statuts et son mécanisme d'application
- **Clarté de la documentation** : Les documents canoniques auront des transitions de statut explicites et des vérifications automatisées

### Négatives
- **Complexité de mise en œuvre** : Les deux idées doivent être mises en œuvre ensemble, nécessitant une coordination
- **Charge de test** : La passerelle de version (IDEA-015) doit être testée avec le cycle de vie des statuts (IDEA-014) pour s'assurer qu'ils fonctionnent ensemble

### Atténuations
- **Mise en œuvre par phases** : IDEA-014 (mises à jour des RÈGLES) peut être mise en œuvre en premier, suivie de IDEA-015 (passerelle de version)
- **Documentation partagée** : DOC-4 sera mis à jour pour documenter à la fois le cycle de vie des statuts et la procédure de la passerelle de version

**Prochaines étapes :**
1. **Mettre à jour la RÈGLE 8** : Ajouter la définition explicite du cycle de vie des statuts (Brouillon → En revue → Gelé)
2. **Implémenter la passerelle de version** : Créer `.github/workflows/release-gate.yml` pour appliquer le statut Gelé lors du marquage de la version
3. **Mettre à jour la documentation** : DOC-4 doit documenter à la fois le cycle de vie des statuts et la procédure de la passerelle de version
4. **Coordonner la mise en œuvre** : S'assurer que IDEA-014 et IDEA-015 sont mises en œuvre de manière synchronisée

**Dépendances :**

| Dépendance | Type | Raison |
|------------|------|--------|
| IDEA-015 | Prérequis | Le critère AC-4 de IDEA-014 nécessite la passerelle de version de IDEA-015 |
| RÈGLE 8 | Gouvernance | Doit être mis à jour pour inclure la définition du cycle de vie des statuts |
| DOC-4 | Documentation | Doit documenter à la fois le cycle de vie des statuts et la passerelle de version |

**Contexte historique :**
La version v2.6 présentait une lacune critique de gouvernance : DOC-1 était toujours marqué comme "Brouillon" alors qu'il aurait dû être "Gelé". Cela était symptomatique d'un manque d'application, et non d'un manque de politique. La RÈGLE 8.1 stipulait déjà que les documents Gelés sont en lecture seule — elle n'était tout simplement pas appliquée. Cet ADR comble cette lacune en acceptant à la fois la politique (IDEA-014) et son application (IDEA-015) ensemble.

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

---

## ADR-014 Update (2026-04-08) : IDEA-020 IMPLEMENTED

**Statut :** IMPLEMENTED

**Implementation completed:**
- RULE 16 (Mandatory Handoff Protocol) added to .clinerules
- RULE 16 synced to template/.clinerules
- SP-002 rebuilt via scripts/rebuild_sp002.py (byte-for-byte match verified)
- handoff-state.md schema already existed on develop-v2.11 (added in commit 9d3f7a8)
- IDEA-020 status updated to [IMPLEMENTED] in IDEAS-BACKLOG.md

**Target release:** v2.11 (updated from v2.10)

---

## ADR-015 : IDEA-021 Release-Specific DOC-3 and DOC-5

**Date:** 2026-04-08
**Statut:** IMPLEMENTED

**Contexte:**
DOC-3 (Implementation Plan) et DOC-5 (Release Notes) etaient trait comme documents cumulatifs contenant l'historique complet. Cependant, par definition:
- DOC-3 devrait documenter uniquement le scope de cette release
- DOC-5 devrait documenter uniquement les changements de cette release

**Decision:**
- DOC-1 (PRD), DOC-2 (Architecture), DOC-4 (Operations) restent cumulatifs
- DOC-3 (Implementation Plan) devient release-specific
- DOC-5 (Release Notes) devient release-specific
- Les versions historiques sont preservees dans docs/releases/vX.Y/

**Implementation:**
- RULE 12 updated in .clinerules (R-CANON-0 through R-CANON-7)
- template/.clinerules synced
- SP-002 rebuilt via scripts/rebuild_sp002.py
- .githooks/pre-receive updated for release-specific validation
- .github/workflows/canonical-docs-check.yml updated
- v2.10: Created DOC-3-v2.10 and DOC-5-v2.10 (release-specific)
- v2.11: Created DOC-3-v2.11 and DOC-5-v2.11 (release-specific)
- DOC-3-CURRENT.md and DOC-5-CURRENT.md point to latest release

**Consequences:**
- DOC-3 et DOC-5 ne contiennent que le contenu de la release courante
- Historique preserve dans docs/releases/vX.Y/
- Line count minimums: DOC-3 >= 100 lines, DOC-5 >= 50 lines

---

## ADR-016 : Skip Pre-v2.10 Releases in Audit Validation

**Date:** 2026-04-08
**Statut:** ACCEPTED

**Contexte:**
L'audit de coherence cumulative (scripts/audit_cumulative_docs.py) validait TOUTES les releases. Cependant, les releases pre-v2.10 ont ete creees avec des criteres de gouvernance differents (line counts beaucoup plus bas). Les appliquer aux releases v1.0-v2.9 cause des echecs de validation qui ne reflettent pas des vrais problemes de gouvernance.

**Decision:**
- Modifier scripts/audit_cumulative_docs.py pour ne valider que les releases v2.10 et superieures
- Les releases pre-v2.10 (v1.0 a v2.9) sont exemptees de la validation cumulative
- Les seuils de lignes (DOC-1: 500, DOC-2: 500, DOC-3: 100, DOC-4: 300, DOC-5: 50) s'appliquent prospectivement a partir de v2.10

**Rationale:**
- Les regles de gouvernance (RULE 12) ont ete formalisees en v2.10
- Les releases historiques pre-v2.10 ont ete creees sans ces exigences explicites
- Appliquer les nouvelles exigences retrospectivement n'est pas equitable
- La gouvernance s'applique prospectivement

**Implementation:**
- Commit 109903a: `fix(audit): skip validation of historical releases pre-v2.10`
- Variable MIN_VERSION = "v2.10" dans audit_cumulative_docs.py

**Fichiers mis a jour:**
- scripts/audit_cumulative_docs.py — ajout du filtrage par version

**Consequences:**
- Les releases pre-v2.10 ne sont plus marquees comme echouees dans l'audit
- L'audit se concentre sur les releases actuelles et futures
- Cohérence avec laportée prospective de la gouvernance v2.10+

---

## ADR-017 : TECH-002 — Auto-Detect Merged Features for Release Scope

**Date:** 2026-04-08
**Statut:** [IDEA]

**Contexte:**
TECH-002 a ete capture suite a l'observation que IDEA-019 (conversation-logging-mechanism) a ete implementee et fusionnee dans `develop` mais n'a pas ete automatiquement ajoutee au scope de la release v2.11. Le processus de release scoping est actuellement manuel.

**Decision:**
- Capture de TECH-002 comme technical suggestion
- Fichier cree: `docs/ideas/TECH-002-auto-detect-merged-features-for-release-scope.md`
- Entrees ajoutees dans `docs/ideas/TECH-SUGGESTIONS-BACKLOG.md`

**Options proposees:**
1. Option A: Git Hook + Script (Pre-merge) — hook sur `develop` qui extrait l'IDEA ID
2. Option B: Scheduled Scan (CI/CD) — GitHub Actions nocturne
3. Option C: On-Demand Orchestrator Command — commande "sync release scope"

**Prochaines etapes:**
- Architect doit evaluer la complexite (7/10) et choisir l'approche
- Decision [ACCEPTED]/[REJECTED]/[DEFERRED] a venir

**Fichiers mis a jour:**
- `docs/ideas/TECH-002-auto-detect-merged-features-for-release-scope.md` — NOUVEAU
- `docs/ideas/TECH-SUGGESTIONS-BACKLOG.md` — entree TECH-002 ajoutee

**Related Ideas:**
- IDEA-003: Release Governance
- IDEA-019: Conversation Logging Mechanism (catalyseur)
- IDEA-022: Ideation-to-Release Journey

---

## ADR-018 : Single Source of Truth for Release Tracking

**Date:** 2026-04-08
**Statut:** ACCEPTED

**Contexte:**
No authoritative location for release version existed. CHANGELOG.md was stale (v1.0, v2.0 only). DOC-5-CURRENT.md showed v2.11 but v2.12 was the actual released version. Agents could not reliably determine the current release state.

**Decision:**
- Create `memory-bank/hot-context/RELEASE.md` as the sole authoritative source for:
  - Current released version: v2.12.0
  - Current draft version: v2.13
- All agents MUST consult RELEASE.md for release state before any action
- RULE 2 (Mandatory Write at Close of Task) updated to require RELEASE.md update at release close

**Fichiers mis a jour:**
- memory-bank/hot-context/RELEASE.md — NOUVEAU: Single source of truth
- .clinerules — RULE 2 updated to require RELEASE.md updates
- docs/ideas/TECH-003-release-tracking-single-source-of-truth.md — Capture TECH-003

**Consequences:**
- All agents must consult RELEASE.md for release state
- CHANGELOG.md and DOC-5-CURRENT.md are no longer authoritative
- Release state tracked in one canonical location

---

## ADR-018 Update: TECH-003 Refined

**Date:** 2026-04-08
**Statut:** TECH-003 [REFINED]

**Update:** TECH-003 has been refined with precise schema definition:

1. **Schema Specification:** Defined exact table structures (Released Versions, Draft Version, Scope Section)
2. **Update Protocol:** Established when and how to update RELEASE.md (on release events, commits, scope changes)
3. **Consistency Enforcement:** Defined GitHub Actions workflow requirements for release-consistency-check.yml
4. **Artifact Relationships:** Clarified how RELEASE.md interacts with EXECUTION-TRACKER, DOC-5-CURRENT, Git tags

**Implementation remaining:**
- Create `.github/workflows/release-consistency-check.yml`
- Update `.clinerules` RULE 2 to include RELEASE.md update protocol
