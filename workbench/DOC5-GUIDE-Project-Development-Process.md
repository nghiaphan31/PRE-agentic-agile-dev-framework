# Document 5 : Manuel du Processus Agile Applicatif
## Comment développer un projet applicatif avec l'Agentic Agile Workbench

**Nom du Projet :** Agentic Agile Workbench
**Version :** 2.0
**Date :** 2026-03-23
**Références :** DOC1-PRD v2.0, DOC2-Architecture v2.0, DOC3-Plan v3.0, DOC4-Guide-Deploiement v1.0

---

## Préambule : Pourquoi ce Document ?

Les documents DOC1 à DOC4 décrivent **l'atelier lui-même** : ses exigences, son architecture, son installation, son déploiement. Ils ne décrivent pas **comment travailler avec l'atelier** pour produire un logiciel applicatif ou métier.

Ce document répond à la question : **"J'ai l'atelier opérationnel. Comment je développe mon projet ?"**

Il couvre :
1. Le **processus Agile** adapté au développement agentique
2. La **nomenclature et les templates** de tous les artifacts d'un projet applicatif
3. Les **mécanismes anti-risques** spécifiques au développement agentique (perte de mémoire, hallucination, multi-sessions sur plusieurs mois)
4. La **phase amont ouverte** : comment transformer des idées narratives non-structurées en artifacts structurés
5. La **traçabilité et le versionnement** de tout le processus

### Convention : Prompts Prêts à Copier-Coller

Ce document utilise une convention visuelle pour distinguer les explications des actions opérationnelles.

Les blocs `📋 PROMPT` sont des **prompts prêts à copier-coller dans Roo Code**. Chaque bloc est **auto-portant** : vous pouvez le copier-coller sans avoir lu le reste du document, et l'agent exécutera l'étape complète de manière autonome.

**Format d'un bloc PROMPT :**

> 📋 **PROMPT [X.Y] — [Titre]**
> **Mode Roo Code requis :** `[slug-du-mode]`
> **Complexité :** 🟢 Simple (1 envoi, agent autonome) | 🔄 Itératif (dialogue humain/agent) | 🔵 Séquentiel (plusieurs prompts à enchaîner)
> **Copier-coller le bloc ci-dessous tel quel :**

```markdown
[Texte du prompt — auto-portant, prêt à coller dans Roo Code]
```

*→ Artifact produit : `chemin/fichier.md`*

### Distinction : User Prompts (ce document) vs System Prompts (`template/prompts/`)

Ce document contient des **User Prompts** — des instructions opérationnelles que **l'humain envoie à l'agent** pour déclencher une étape précise du workflow Agile (Sprint Planning, développement d'une User Story, etc.).

Ils sont distincts des **System Prompts** stockés dans `template/prompts/` (fichiers SP-001 à SP-007), qui configurent l'identité et les règles de comportement des agents IA. Ces derniers sont déployés dans des fichiers techniques (`.clinerules`, `.roomodes`, `Modelfile`) et s'appliquent en permanence, en arrière-plan, pour toutes les sessions.

| | User Prompts (ce document) | System Prompts (`template/prompts/`) |
| :--- | :--- | :--- |
| **Rôle** | Déclencher une action workflow | Configurer l'identité et les règles de l'agent |
| **Utilisé par** | L'humain (copier-coller dans Roo Code) | L'agent IA (automatiquement, en arrière-plan) |
| **Portée** | Une tâche précise, une session | Toutes les sessions, tous les modes |
| **Cible** | Interface chat de Roo Code | `.clinerules`, `.roomodes`, `Modelfile`, Gemini Gem |
| **Fréquence** | À chaque étape du workflow | Une fois déployés, puis maintenance |

---

## Table des Matières

1. Vue d'Ensemble du Processus
2. Phase 0 - Amont Ouvert : De l'Idée aux Artifacts
3. Phase 1 - Cadrage : Initialisation du Projet
4. Phase 2 - Sprints de Développement
5. Phase 3 - Livraison et Maintenance
6. Nomenclature des Artifacts
7. Templates des Artifacts
8. Mécanismes Anti-Risques Agentiques
9. Protocoles de Session
10. Tableau de Bord du Projet

---

## 1. Vue d'Ensemble du Processus

### 1.1 Principes Fondamentaux

Le processus repose sur **quatre principes non-négociables** :

| Principe | Description | Mécanisme de l'Atelier |
| :--- | :--- | :--- |
| **Mémoire Persistante** | Tout contexte est écrit, jamais supposé mémorisé | Memory Bank (7 fichiers `.md`) |
| **Traçabilité Totale** | Tout artifact est versionné avec son historique | Git + Conventional Commits |
| **Convergence Progressive** | Les entrées narratives mûrissent vers des artifacts structurés | Phase 0 → Phase 1 → Phase 2 |
| **Défense en Profondeur** | Chaque règle est redondante (`.clinerules` + `roleDefinition` + protocoles) | `.clinerules` + `.roomodes` |

### 1.2 Carte du Processus

```
+-------------------------------------------------------------------------+
|                    PHASE 0 - AMONT OUVERT                               |
|                                                                          |
|  Entrées narratives, non-structurées, désordonnées                      |
|  (emails, notes, conversations, code existant, idées vagues)            |
|                                                                          |
|  -> Artifact : BRIEF-001 (Vision Narrative Brute)                       |
|  -> Artifact : BRIEF-002 (Synthèse Structurée)                          |
|  -> Artifact : BRIEF-003 (Décision de Lancement)                        |
+----------------------------------+--------------------------------------+
                                   | Convergence
                                   v
+-------------------------------------------------------------------------+
|                    PHASE 1 - CADRAGE                                     |
|                                                                          |
|  Initialisation du projet, Memory Bank, backlog initial                 |
|                                                                          |
|  -> Artifact : PRJ-001 (Project Brief)                                  |
|  -> Artifact : PRJ-002 (Architecture Initiale)                          |
|  -> Artifact : PRJ-003 (Backlog Initial)                                |
|  -> Artifact : PRJ-004 (Tech Context)                                   |
+----------------------------------+--------------------------------------+
                                   | Itération
                                   v
+-------------------------------------------------------------------------+
|                    PHASE 2 - SPRINTS (répétée N fois)                   |
|                                                                          |
|  Sprint Planning -> Développement -> Tests -> Review -> Rétrospective   |
|                                                                          |
|  -> Artifact : SPR-XXX-001 (Sprint Backlog)                             |
|  -> Artifact : SPR-XXX-002 (User Stories)                               |
|  -> Artifact : SPR-XXX-003 (Code Source)                                |
|  -> Artifact : SPR-XXX-004 (Rapport de Tests)                           |
|  -> Artifact : SPR-XXX-005 (Sprint Review)                              |
|  -> Artifact : SPR-XXX-006 (Rétrospective)                              |
+----------------------------------+--------------------------------------+
                                   | Livraison
                                   v
+-------------------------------------------------------------------------+
|                    PHASE 3 - LIVRAISON & MAINTENANCE                    |
|                                                                          |
|  -> Artifact : REL-XXX-001 (Release Notes)                              |
|  -> Artifact : REL-XXX-002 (Documentation Utilisateur)                  |
|  -> Artifact : REL-XXX-003 (Runbook de Déploiement)                     |
+-------------------------------------------------------------------------+
```

### 1.3 Rôles et Responsabilités par Phase

| Phase | Persona Principal | Personas Secondaires | Livrables |
| :--- | :--- | :--- | :--- |
| Phase 0 - Amont | Product Owner | Developer | BRIEF-001, BRIEF-002, BRIEF-003 |
| Phase 1 - Cadrage | Product Owner | Developer, Scrum Master | PRJ-001 à PRJ-004 |
| Phase 2 - Sprint Planning | Product Owner | Scrum Master | SPR-XXX-001, SPR-XXX-002 |
| Phase 2 - Développement | Developer | — | SPR-XXX-003 |
| Phase 2 - Tests | QA Engineer | Developer | SPR-XXX-004 |
| Phase 2 - Review | Product Owner | Scrum Master | SPR-XXX-005 |
| Phase 2 - Rétrospective | Scrum Master | Tous | SPR-XXX-006 |
| Phase 3 - Livraison | Developer | QA Engineer | REL-XXX-001 à REL-XXX-003 |

---

## 2. Phase 0 - Amont Ouvert : De l'Idée aux Artifacts

### 2.1 Pourquoi une Phase Amont Ouverte ?

Le développement logiciel commence rarement par un cahier des charges structuré. Il commence par :
- Un email de 3 lignes : "Il faudrait un outil pour gérer nos commandes clients"
- Une conversation : "Le problème c'est que les commerciaux saisissent les données deux fois"
- Un code existant sans documentation : "Voilà ce qu'on a, il faut le refaire proprement"
- Des notes désordonnées sur plusieurs documents
- Une idée vague qui évolue au fil des discussions

**L'atelier doit accepter ces entrées telles quelles** et les transformer progressivement en artifacts structurés. C'est le rôle de la Phase 0.

> **Règle d'or de la Phase 0 :** Ne jamais forcer une structure prématurée. Laisser la compréhension mûrir avant de structurer.

### 2.2 Entrées Acceptées en Phase 0

| Type d'Entrée | Exemple | Traitement |
| :--- | :--- | :--- |
| **Texte narratif libre** | Email, note, compte-rendu de réunion | Copier tel quel dans BRIEF-001 |
| **Code existant** | Dépôt legacy, scripts, prototypes | Audit Developer → BRIEF-002 |
| **Conversation orale** | Retranscription, notes de réunion | Copier tel quel dans BRIEF-001 |
| **Document Word/PDF** | Cahier des charges partiel, spec fonctionnelle | Extraire le texte → BRIEF-001 |
| **Maquettes/Wireframes** | Images, captures d'écran | Décrire en texte → BRIEF-001 |
| **Idée vague** | "Je veux quelque chose comme Trello mais pour..." | Dialogue Product Owner → BRIEF-001 |

### 2.3 Processus de Maturation Phase 0

---

#### Étape 0.1 — Collecte des entrées brutes

> 📋 **PROMPT 0.1 — Collecte des entrées brutes**
> **Mode Roo Code requis :** `product-owner`
> **Complexité :** 🟢 Simple — 1 envoi, remplacer [ENTREES BRUTES] par vos données avant d'envoyer
> **Copier-coller le bloc ci-dessous tel quel, puis remplacer [ENTREES BRUTES] :**

```markdown
Crée le fichier docs/brief/BRIEF-001-vision-narrative.md avec le contenu suivant,
copié exactement tel quel sans reformuler :

---
# BRIEF-001 - Vision Narrative Brute
**Date de création :** [DATE]
**Créé par :** Product Owner
**Statut :** Brouillon

## Entrées Brutes

### Entrée 1 - [Source : email / réunion / note / code existant]
**Date :** [DATE]
**Auteur :** [NOM]

[ENTREES BRUTES — coller ici emails, notes, conversations, descriptions telles quelles]

## Historique des Ajouts
| Date | Source | Résumé |
| :--- | :--- | :--- |
| [DATE] | [SOURCE] | [RESUME EN 1 LIGNE] |
---

Commite avec : 'docs(brief): vision narrative initiale - phase amont'
```

*→ Artifact produit : `docs/brief/BRIEF-001-vision-narrative.md`*

---

#### Étape 0.2 — Analyse structurée

> 📋 **PROMPT 0.2 — Analyse structurée des entrées brutes**
> **Mode Roo Code requis :** `developer`
> **Complexité :** 🟢 Simple — 1 envoi, l'agent produit BRIEF-002 en autonomie
> **Copier-coller le bloc ci-dessous tel quel :**

```markdown
Lis docs/brief/BRIEF-001-vision-narrative.md.
Identifie et liste dans docs/brief/BRIEF-002-synthese-structuree.md :
- Les fonctionnalités mentionnées (même implicitement)
- Les utilisateurs cibles identifiables
- Les contraintes techniques ou métier
- Les ambiguïtés et questions ouvertes
- Ce qui est hors périmètre apparent
Ne prends aucune décision. Documente seulement ce que tu comprends.
Commite avec : 'docs(brief): synthèse structurée phase amont'
```

*→ Artifact produit : `docs/brief/BRIEF-002-synthese-structuree.md`*

---

#### Étape 0.3 — Clarification des ambiguïtés

> 📋 **PROMPT 0.3 — Clarification des ambiguïtés**
> **Mode Roo Code requis :** `product-owner`
> **Complexité :** 🔄 Itératif — dialogue question/réponse jusqu'à résolution de toutes les ambiguïtés critiques
> **Copier-coller le bloc ci-dessous tel quel :**

```markdown
Lis docs/brief/BRIEF-002-synthese-structuree.md.
Pour chaque ambiguïté listée dans la section "Ambiguïtés et Questions Ouvertes",
pose-moi une question précise.
Attends ma réponse avant de passer à la suivante.
Mets à jour BRIEF-002 avec chaque réponse obtenue en marquant la question comme "Résolue".
```

*→ Dialogue itératif jusqu'à résolution des ambiguïtés critiques. BRIEF-002 mis à jour.*

---

#### Étape 0.4 — Décision de lancement GO/NO-GO

> 📋 **PROMPT 0.4 — Décision de lancement GO/NO-GO**
> **Mode Roo Code requis :** `product-owner`
> **Complexité :** 🟢 Simple — 1 envoi, l'agent crée BRIEF-003 et commite les 3 artifacts
> **Copier-coller le bloc ci-dessous tel quel :**

```markdown
Sur la base de docs/brief/BRIEF-001-vision-narrative.md et
docs/brief/BRIEF-002-synthese-structuree.md,
crée docs/brief/BRIEF-003-decision-lancement.md avec :
- La décision GO / NO-GO / ATTENTE
- Les conditions de lancement si ATTENTE
- La date de décision
- Les risques identifiés et leur mitigation
- Le périmètre validé pour le lancement

Commite les 3 fichiers BRIEF avec le message :
'docs(brief): phase amont complète - décision [GO/NO-GO]'
```

*→ Artifact produit : `docs/brief/BRIEF-003-decision-lancement.md`*
*→ Commit Git des 3 artifacts BRIEF*

---

### 2.4 Critère de Sortie de Phase 0

La Phase 0 est terminée quand :
- [ ] BRIEF-001 existe et contient toutes les entrées brutes
- [ ] BRIEF-002 existe et liste fonctionnalités, utilisateurs, contraintes, ambiguïtés
- [ ] Toutes les ambiguïtés critiques sont résolues (ou documentées comme acceptées)
- [ ] BRIEF-003 contient une décision GO
- [ ] Les 3 fichiers sont commités dans Git

> **Si la décision est NO-GO ou ATTENTE :** Archiver les fichiers BRIEF dans `docs/brief/archive/` et commiter. Le projet peut reprendre plus tard en repartant de ces artifacts.

---

## 3. Phase 1 - Cadrage : Initialisation du Projet

### 3.1 Objectif

Transformer la décision GO de la Phase 0 en une base de projet structurée et opérationnelle : Memory Bank remplie, architecture initiale définie, backlog initial créé.

### 3.2 Séquence de Cadrage

---

#### Étape 1.1 — Initialisation de la Memory Bank

> 📋 **PROMPT 1.1 — Initialisation de la Memory Bank**
> **Mode Roo Code requis :** `product-owner`
> **Complexité :** 🟢 Simple — 1 envoi, l'agent remplit projectBrief.md et productContext.md
> **Copier-coller le bloc ci-dessous tel quel :**

```markdown
Lis docs/brief/BRIEF-002-synthese-structuree.md et
docs/brief/BRIEF-003-decision-lancement.md.

Remplis les fichiers Memory Bank suivants :

1. memory-bank/projectBrief.md :
   - Vision du projet (2-3 phrases synthétiques)
   - Objectifs principaux (mesurables)
   - Non-Goals explicites
   - Contraintes identifiées
   - Parties prenantes

2. memory-bank/productContext.md :
   - Personas utilisateurs identifiés
   - Premières User Stories (format standard)
   - Backlog initial priorisé

Commite avec : 'feat(memory): initialisation Memory Bank depuis phase amont'
```

*→ Artifacts mis à jour : `memory-bank/projectBrief.md`, `memory-bank/productContext.md`*

---

#### Étape 1.2 — Architecture Initiale

> 📋 **PROMPT 1.2 — Architecture initiale du projet**
> **Mode Roo Code requis :** `developer`
> **Complexité :** 🟢 Simple — 1 envoi, l'agent propose l'architecture et met à jour la Memory Bank
> **Copier-coller le bloc ci-dessous tel quel :**

```markdown
Lis memory-bank/projectBrief.md et memory-bank/productContext.md.

Propose une architecture initiale dans docs/architecture/PRJ-002-architecture-initiale.md :
- Stack technique recommandée (avec justification)
- Structure des dossiers du projet
- Patterns architecturaux retenus
- Décisions d'architecture (ADR format)
- Dépendances externes identifiées

Mets à jour memory-bank/systemPatterns.md et memory-bank/techContext.md.
Mets à jour memory-bank/decisionLog.md avec les ADR.
Commite avec : 'feat(architecture): architecture initiale + Memory Bank mise à jour'
```

*→ Artifact produit : `docs/architecture/PRJ-002-architecture-initiale.md`*
*→ Artifacts mis à jour : `memory-bank/systemPatterns.md`, `memory-bank/techContext.md`, `memory-bank/decisionLog.md`*

---

#### Étape 1.3 — Validation de l'Architecture

> 📋 **PROMPT 1.3 — Validation de l'architecture par le Product Owner**
> **Mode Roo Code requis :** `product-owner`
> **Complexité :** 🔄 Itératif — l'agent liste les incohérences éventuelles, dialogue si corrections nécessaires
> **Copier-coller le bloc ci-dessous tel quel :**

```markdown
Lis docs/architecture/PRJ-002-architecture-initiale.md.
Vérifie que l'architecture proposée est cohérente avec :
- La vision dans memory-bank/projectBrief.md
- Les contraintes identifiées
- Les Non-Goals

Si des incohérences existent, liste-les.
Si l'architecture est validée, mets à jour docs/brief/BRIEF-003-decision-lancement.md
avec la mention 'Architecture validée le [DATE]' et commite.
```

*→ Artifact mis à jour : `docs/brief/BRIEF-003-decision-lancement.md` (mention de validation)*

---

#### Étape 1.4 — Backlog Initial Structuré

> 📋 **PROMPT 1.4 — Création du backlog initial MoSCoW**
> **Mode Roo Code requis :** `product-owner`
> **Complexité :** 🟢 Simple — 1 envoi, l'agent crée le backlog structuré avec priorisation MoSCoW
> **Copier-coller le bloc ci-dessous tel quel :**

```markdown
Sur la base de memory-bank/productContext.md et de l'architecture validée,
crée docs/backlog/PRJ-003-backlog-initial.md avec :

- Les Epics identifiées (regroupements fonctionnels)
- Les User Stories de chaque Epic (format standard)
- La priorisation MoSCoW (Must/Should/Could/Won't)
- Les dépendances entre User Stories
- L'estimation de complexité (T-shirt sizing : XS/S/M/L/XL)

Mets à jour memory-bank/productContext.md avec le backlog structuré.
Commite avec : 'feat(backlog): backlog initial structuré avec priorisation MoSCoW'
```

*→ Artifact produit : `docs/backlog/PRJ-003-backlog-initial.md`*
*→ Artifact mis à jour : `memory-bank/productContext.md`*

---

### 3.3 Critère de Sortie de Phase 1

- [ ] `memory-bank/projectBrief.md` rempli et validé
- [ ] `memory-bank/productContext.md` contient le backlog initial
- [ ] `memory-bank/systemPatterns.md` contient l'architecture initiale
- [ ] `memory-bank/techContext.md` contient la stack et les commandes
- [ ] `docs/architecture/PRJ-002-architecture-initiale.md` existe
- [ ] `docs/backlog/PRJ-003-backlog-initial.md` existe avec priorisation MoSCoW
- [ ] Tous les fichiers commités dans Git

---

## 4. Phase 2 - Sprints de Développement

### 4.1 Structure d'un Sprint

Un sprint dure **1 à 2 semaines**. Il suit le cycle Scrum standard adapté au développement agentique :

```
SPRINT PLANNING (Début de sprint)
  Durée : 1-2 heures
  Personas : Product Owner + Scrum Master
  Artifact : SPR-XXX-001 (Sprint Backlog)

DÉVELOPPEMENT (Corps du sprint)
  Durée : 80% du sprint
  Persona : Developer
  Artifact : SPR-XXX-003 (Code Source + commits)
  Règle : 1 User Story = N commits = 1 livraison

TESTS (Fin de développement)
  Durée : 15% du sprint
  Persona : QA Engineer
  Artifact : SPR-XXX-004 (Rapport de Tests)

SPRINT REVIEW (Fin de sprint)
  Durée : 1 heure
  Personas : Product Owner + Scrum Master
  Artifact : SPR-XXX-005 (Sprint Review)

RÉTROSPECTIVE (Après la review)
  Durée : 30 minutes
  Persona : Scrum Master
  Artifact : SPR-XXX-006 (Rétrospective)

MISE À JOUR MEMORY BANK (Obligatoire avant clôture)
  Persona : Scrum Master
  Fichiers : activeContext.md, progress.md
  Commit : 'docs(memory): clôture sprint XXX'
```

### 4.2 Sprint Planning

> 📋 **PROMPT 4.2 — Sprint Planning**
> **Mode Roo Code requis :** `product-owner`
> **Complexité :** 🟢 Simple — 1 envoi, remplacer [NNN] par le numéro du sprint (ex: 001)
> **Copier-coller le bloc ci-dessous tel quel, puis remplacer [NNN] :**

```markdown
Lis memory-bank/productContext.md et memory-bank/progress.md.

Crée docs/sprints/sprint-[NNN]/SPR-[NNN]-001-sprint-backlog.md avec :
- L'objectif du sprint (Sprint Goal - 1 phrase)
- Les User Stories sélectionnées du backlog (avec leur ID)
- La capacité estimée (en points ou en jours)
- Les critères d'acceptation de chaque US
- Les dépendances techniques identifiées

Mets à jour memory-bank/activeContext.md avec le Sprint Goal.
Commite avec : 'feat(sprint-[NNN]): sprint planning - [Sprint Goal]'
```

*→ Artifact produit : `docs/sprints/sprint-[NNN]/SPR-[NNN]-001-sprint-backlog.md`*
*→ Artifact mis à jour : `memory-bank/activeContext.md`*

---

### 4.3 Développement d'une User Story

**Protocole obligatoire en 5 étapes :**

```
ÉTAPE D.1 - LECTURE MEMORY BANK (obligatoire)
  Lire : activeContext.md, systemPatterns.md, techContext.md

ÉTAPE D.2 - COMPRÉHENSION DE LA USER STORY
  Lire : docs/sprints/sprint-[NNN]/SPR-[NNN]-001-sprint-backlog.md
  Identifier : critères d'acceptation, dépendances

ÉTAPE D.3 - IMPLÉMENTATION
  Coder la User Story
  Commiter après chaque sous-tâche significative
  Format commit : 'feat(US-XXX): [description]'

ÉTAPE D.4 - MISE À JOUR MEMORY BANK
  Mettre à jour : activeContext.md (état courant)
  Si décision d'architecture : mettre à jour decisionLog.md

ÉTAPE D.5 - COMMIT FINAL
  git add .
  git commit -m 'feat(US-XXX): implémentation complète - [description]'
```

> 📋 **PROMPT 4.3 — Développement d'une User Story**
> **Mode Roo Code requis :** `developer`
> **Complexité :** 🟢 Simple — 1 envoi, remplacer [NNN] et [XXX] avant d'envoyer
> **Copier-coller le bloc ci-dessous tel quel, puis remplacer [NNN] et [XXX] :**

```markdown
Lis memory-bank/activeContext.md, memory-bank/systemPatterns.md
et memory-bank/techContext.md.

Implémente la User Story US-[XXX] définie dans
docs/sprints/sprint-[NNN]/SPR-[NNN]-001-sprint-backlog.md.

Respecte les conventions de memory-bank/systemPatterns.md.
Commite après chaque sous-tâche avec le format 'feat(US-XXX): [description]'.
Mets à jour memory-bank/activeContext.md après chaque sous-tâche.
Avant de clôturer, commite memory-bank/ avec 'docs(memory): US-XXX implémentée'.
```

*→ Artifact produit : code source dans `src/` (commits successifs)*
*→ Artifact mis à jour : `memory-bank/activeContext.md`*

---

### 4.4 Tests

> 📋 **PROMPT 4.4 — Rapport de Tests du Sprint**
> **Mode Roo Code requis :** `qa-engineer`
> **Complexité :** 🔵 Séquentiel — l'agent teste chaque US du sprint et documente les résultats
> **Copier-coller le bloc ci-dessous tel quel, puis remplacer [NNN] :**

```markdown
Lis docs/sprints/sprint-[NNN]/SPR-[NNN]-001-sprint-backlog.md
pour connaître les critères d'acceptation de chaque US.

Pour chaque User Story du sprint :
1. Exécute les tests automatisés existants
2. Vérifie chaque critère d'acceptation
3. Documente les résultats dans
   docs/sprints/sprint-[NNN]/SPR-[NNN]-004-rapport-tests.md

Commite avec : 'test(sprint-[NNN]): rapport de tests - [NNN] US testées'
```

*→ Artifact produit : `docs/sprints/sprint-[NNN]/SPR-[NNN]-004-rapport-tests.md`*

---

### 4.5 Sprint Review

> 📋 **PROMPT 4.5 — Sprint Review**
> **Mode Roo Code requis :** `product-owner`
> **Complexité :** 🟢 Simple — 1 envoi, l'agent crée la review et met à jour le backlog
> **Copier-coller le bloc ci-dessous tel quel, puis remplacer [NNN] :**

```markdown
Lis docs/sprints/sprint-[NNN]/SPR-[NNN]-004-rapport-tests.md.

Crée docs/sprints/sprint-[NNN]/SPR-[NNN]-005-sprint-review.md avec :
- Les US livrées (validées par les tests)
- Les US non livrées (avec raison)
- La vélocité du sprint (points livrés / points planifiés)
- Les feedbacks sur les fonctionnalités livrées
- Les ajustements du backlog (nouvelles US, repriorisation)

Mets à jour memory-bank/productContext.md avec les ajustements backlog.
Commite avec : 'docs(sprint-[NNN]): sprint review - vélocité [X]%'
```

*→ Artifact produit : `docs/sprints/sprint-[NNN]/SPR-[NNN]-005-sprint-review.md`*
*→ Artifact mis à jour : `memory-bank/productContext.md`*

---

### 4.6 Rétrospective

> 📋 **PROMPT 4.6 — Rétrospective du Sprint**
> **Mode Roo Code requis :** `scrum-master`
> **Complexité :** 🟢 Simple — 1 envoi, l'agent crée la rétro et clôture le sprint dans la Memory Bank
> **Copier-coller le bloc ci-dessous tel quel, puis remplacer [NNN] :**

```markdown
Lis docs/sprints/sprint-[NNN]/SPR-[NNN]-005-sprint-review.md
et memory-bank/activeContext.md.

Crée docs/sprints/sprint-[NNN]/SPR-[NNN]-006-retrospective.md avec :
- Ce qui a bien fonctionné (Keep)
- Ce qui doit être amélioré (Improve)
- Ce qui doit être arrêté (Stop)
- Les actions concrètes pour le prochain sprint
- Les impediments identifiés et leur résolution

Mets à jour memory-bank/progress.md (cocher les US terminées).
Mets à jour memory-bank/activeContext.md (état fin de sprint).


Commite avec : 'docs(memory): clôture sprint [NNN] - [X] US livrées'
```

*→ Artifact produit : `docs/sprints/sprint-[NNN]/SPR-[NNN]-006-retrospective.md`*
*→ Artifacts mis à jour : `memory-bank/progress.md`, `memory-bank/activeContext.md`*

---

## 5. Phase 3 - Livraison et Maintenance

### 5.1 Préparation d'une Release

> 📋 **PROMPT 5.1 — Release Notes**
> **Mode Roo Code requis :** `developer`
> **Complexité :** 🟢 Simple — 1 envoi, remplacer [VERSION] par le numéro SemVer (ex: 1.0.0)
> **Copier-coller le bloc ci-dessous tel quel, puis remplacer [VERSION] :**

```markdown
Lis memory-bank/progress.md pour identifier les features livrées
depuis la dernière release.

Crée docs/releases/REL-[VERSION]-001-release-notes.md avec :
- La version (format SemVer : MAJOR.MINOR.PATCH)
- La date de release
- Les nouvelles fonctionnalités (avec référence aux US)
- Les corrections de bugs
- Les changements breaking (si MAJOR)
- Les instructions de migration (si applicable)

Commite avec : 'docs(release): release notes v[VERSION]'
```

*→ Artifact produit : `docs/releases/REL-[VERSION]-001-release-notes.md`*

---

### 5.2 Documentation Utilisateur

> 📋 **PROMPT 5.2 — Documentation Utilisateur**
> **Mode Roo Code requis :** `developer`
> **Complexité :** 🟢 Simple — 1 envoi, remplacer [VERSION] avant d'envoyer
> **Copier-coller le bloc ci-dessous tel quel, puis remplacer [VERSION] :**

```markdown
Sur la base des features livrées dans docs/releases/REL-[VERSION]-001-release-notes.md,
crée ou mets à jour docs/releases/REL-[VERSION]-002-documentation-utilisateur.md.

La documentation doit couvrir :
- Guide de démarrage rapide
- Description de chaque fonctionnalité
- Exemples d'utilisation
- FAQ

Commite avec : 'docs(release): documentation utilisateur v[VERSION]'
```

*→ Artifact produit : `docs/releases/REL-[VERSION]-002-documentation-utilisateur.md`*

---

### 5.3 Runbook de Déploiement

> 📋 **PROMPT 5.3 — Runbook de Déploiement**
> **Mode Roo Code requis :** `developer`
> **Complexité :** 🟢 Simple — 1 envoi, remplacer [VERSION] avant d'envoyer
> **Copier-coller le bloc ci-dessous tel quel, puis remplacer [VERSION] :**

```markdown
Crée docs/releases/REL-[VERSION]-003-runbook-deploiement.md avec :
- Les prérequis système
- Les étapes de déploiement (numérotées, précises)
- Les variables d'environnement requises
- Les commandes de vérification post-déploiement
- La procédure de rollback

Commite avec : 'docs(release): runbook déploiement v[VERSION]'
```

*→ Artifact produit : `docs/releases/REL-[VERSION]-003-runbook-deploiement.md`*

---

## 6. Nomenclature des Artifacts

### 6.1 Convention de Nommage

**Format général :** `[CATEGORIE]-[NUMERO]-[DESCRIPTION-COURTE].[ext]`

**Catégories :**

| Préfixe | Catégorie | Phase | Emplacement |
| :--- | :--- | :--- | :--- |
| `BRIEF` | Artifacts de phase amont | Phase 0 | `docs/brief/` |
| `PRJ` | Artifacts de cadrage projet | Phase 1 | `docs/architecture/`, `docs/backlog/` |
| `SPR` | Artifacts de sprint | Phase 2 | `docs/sprints/sprint-[NNN]/` |
| `QA` | Rapports de tests | Phase 2 | `docs/sprints/sprint-[NNN]/` ou `docs/qa/` |
| `REL` | Artifacts de release | Phase 3 | `docs/releases/` |
| `ADR` | Architecture Decision Records | Toutes | `memory-bank/decisionLog.md` |
| `US` | User Stories | Phase 1-2 | `memory-bank/productContext.md` |

### 6.2 Nomenclature Complète des Artifacts

#### Artifacts Phase 0 - Amont

| ID Artifact | Nom du Fichier | Description | Persona Responsable |
| :--- | :--- | :--- | :--- |
| `BRIEF-001` | `BRIEF-001-vision-narrative.md` | Entrées brutes non-structurées | Product Owner |
| `BRIEF-002` | `BRIEF-002-synthese-structuree.md` | Analyse structurée des entrées | Developer |
| `BRIEF-003` | `BRIEF-003-decision-lancement.md` | Décision GO/NO-GO avec conditions | Product Owner |

#### Artifacts Phase 1 - Cadrage

| ID Artifact | Nom du Fichier | Description | Persona Responsable |
| :--- | :--- | :--- | :--- |
| `PRJ-001` | `memory-bank/projectBrief.md` | Vision, objectifs, Non-Goals | Product Owner |
| `PRJ-002` | `PRJ-002-architecture-initiale.md` | Architecture, stack, ADR initiaux | Developer |
| `PRJ-003` | `PRJ-003-backlog-initial.md` | Epics, US, priorisation MoSCoW | Product Owner |
| `PRJ-004` | `memory-bank/techContext.md` | Stack, commandes, variables d'env | Developer |

#### Artifacts Phase 2 - Sprint

| ID Artifact | Nom du Fichier | Description | Persona Responsable |
| :--- | :--- | :--- | :--- |
| `SPR-[NNN]-001` | `SPR-[NNN]-001-sprint-backlog.md` | US sélectionnées, Sprint Goal | Product Owner |
| `SPR-[NNN]-002` | `SPR-[NNN]-002-user-stories.md` | Détail des US (si non dans backlog) | Product Owner |
| `SPR-[NNN]-003` | Code source dans `src/` | Implémentation des US | Developer |
| `SPR-[NNN]-004` | `SPR-[NNN]-004-rapport-tests.md` | Résultats des tests, bugs | QA Engineer |
| `SPR-[NNN]-005` | `SPR-[NNN]-005-sprint-review.md` | Vélocité, US livrées, feedbacks | Product Owner |
| `SPR-[NNN]-006` | `SPR-[NNN]-006-retrospective.md` | Keep/Improve/Stop, actions | Scrum Master |

#### Artifacts Phase 3 - Release

| ID Artifact | Nom du Fichier | Description | Persona Responsable |
| :--- | :--- | :--- | :--- |
| `REL-[VER]-001` | `REL-[VER]-001-release-notes.md` | Changelog, nouvelles features | Developer |
| `REL-[VER]-002` | `REL-[VER]-002-documentation-utilisateur.md` | Guide utilisateur | Developer |
| `REL-[VER]-003` | `REL-[VER]-003-runbook-deploiement.md` | Procédure de déploiement | Developer |

#### Artifacts Memory Bank (Persistants)

| Fichier | Fréquence de Mise à Jour | Persona Responsable |
| :--- | :--- | :--- |
| `memory-bank/projectBrief.md` | Rare (changement de vision) | Product Owner |
| `memory-bank/productContext.md` | Chaque sprint (backlog) | Product Owner |
| `memory-bank/systemPatterns.md` | Après décision d'architecture | Developer |
| `memory-bank/techContext.md` | Après changement de stack | Developer |
| `memory-bank/activeContext.md` | **À chaque session** | Tous |
| `memory-bank/progress.md` | **À chaque fin de sprint** | Scrum Master |
| `memory-bank/decisionLog.md` | Après chaque ADR | Developer |

### 6.3 Structure des Dossiers d'un Projet Applicatif

```
[RACINE DU PROJET]
|-- .clinerules                    # Règles atelier (copie depuis workbench)
|-- .gitignore                     # Exclusions Git
|-- .roomodes                      # Personas Agile (copie depuis workbench)
|-- .workbench-version             # Version de l'atelier déployée
|-- Modelfile                      # Config Ollama (si Mode Local)
|-- proxy.py                       # Proxy Gemini (si Mode Proxy)
|-- requirements.txt               # Dépendances Python proxy
|
|-- docs/                          # Tous les artifacts documentaires
|   |-- brief/                     # Phase 0 - Amont
|   |   |-- BRIEF-001-vision-narrative.md
|   |   |-- BRIEF-002-synthese-structuree.md
|   |   |-- BRIEF-003-decision-lancement.md
|   |   +-- archive/               # Projets NO-GO archivés
|   |
|   |-- architecture/              # Phase 1 - Cadrage
|   |   +-- PRJ-002-architecture-initiale.md
|   |
|   |-- backlog/                   # Phase 1 - Backlog
|   |   +-- PRJ-003-backlog-initial.md
|   |
|   |-- sprints/                   # Phase 2 - Sprints
|   |   |-- sprint-001/
|   |   |   |-- SPR-001-001-sprint-backlog.md
|   |   |   |-- SPR-001-004-rapport-tests.md
|   |   |   |-- SPR-001-005-sprint-review.md
|   |   |   +-- SPR-001-006-retrospective.md
|   |   +-- sprint-002/
|   |       +-- ...
|   |
|   |-- qa/                        # Rapports QA (écrits par QA Engineer)
|   |   +-- .gitkeep
|   |
|   +-- releases/                  # Phase 3 - Releases
|       |-- REL-1.0.0-001-release-notes.md
|       |-- REL-1.0.0-002-documentation-utilisateur.md
|       +-- REL-1.0.0-003-runbook-deploiement.md
|
|-- memory-bank/                   # Memory Bank - 7 fichiers persistants
|   |-- activeContext.md
|   |-- decisionLog.md
|   |-- productContext.md
|   |-- progress.md
|   |-- projectBrief.md
|   |-- systemPatterns.md
|   +-- techContext.md
|
|-- prompts/                       # Registre prompts (copie depuis workbench)
|   |-- README.md
|   +-- SP-001 à SP-007
|
|-- scripts/                       # Scripts utilitaires (copie depuis workbench)
|   |-- check-prompts-sync.ps1
|   +-- start-proxy.ps1
|
+-- src/                           # Code source applicatif
    +-- [structure spécifique au projet]
```

---

## 7. Templates des Artifacts

### 7.1 Template BRIEF-001 - Vision Narrative

```markdown
# BRIEF-001 - Vision Narrative Brute
**Date de création :** [DATE]
**Créé par :** Product Owner
**Statut :** Brouillon

---

## Entrées Brutes

> Ce fichier contient les entrées TELLES QUELLES, sans reformulation.
> Ne pas modifier le contenu original. Ajouter de nouvelles entrées à la suite.

### Entrée 1 - [Source : email / réunion / note / code existant]
**Date :** [DATE]
**Auteur :** [NOM]

[COLLER ICI LE TEXTE BRUT SANS MODIFICATION]

---

### Entrée 2 - [Source]
**Date :** [DATE]

[COLLER ICI]

---

## Historique des Ajouts
| Date | Source | Résumé |
| :--- | :--- | :--- |
| [DATE] | [SOURCE] | [RESUME EN 1 LIGNE] |
```

### 7.2 Template BRIEF-002 - Synthèse Structurée

```markdown
# BRIEF-002 - Synthèse Structurée
**Date de création :** [DATE]
**Basé sur :** BRIEF-001-vision-narrative.md
**Statut :** En cours d'analyse

---

## Fonctionnalités Identifiées

### Fonctionnalités Explicites (mentionnées clairement)
- [F-001] [Description]
- [F-002] [Description]

### Fonctionnalités Implicites (déduites du contexte)
- [F-I-001] [Description] - *Déduit de : "[citation de BRIEF-001]"*

---

## Utilisateurs Cibles Identifiés

| Persona | Description | Besoins Principaux |
| :--- | :--- | :--- |
| [Nom] | [Description] | [Besoins] |

---

## Contraintes Identifiées

### Contraintes Techniques
- [CT-001] [Description]

### Contraintes Métier / Légales
- [CM-001] [Description]

---

## Périmètre Apparent

### Dans le Périmètre
- [Description]

### Hors Périmètre (apparent)
- [Description]

---

## Ambiguïtés et Questions Ouvertes

| ID | Question | Criticité | Statut |
| :--- | :--- | :--- | :--- |
| [Q-001] | [Question précise] | CRITIQUE / HAUTE / BASSE | Ouverte / Résolue |

### Réponses aux Questions
**Q-001 :** [Réponse obtenue le DATE]

---

## Risques Identifiés
- [R-001] [Description du risque] - Probabilité : [H/M/B] - Impact : [H/M/B]
```

### 7.3 Template BRIEF-003 - Décision de Lancement

```markdown
# BRIEF-003 - Décision de Lancement
**Date de décision :** [DATE]
**Décideur :** [NOM]

---

## Décision

**[ ] GO** - Le projet est lancé
**[ ] NO-GO** - Le projet est abandonné
**[ ] ATTENTE** - Le projet est suspendu jusqu'à [CONDITION]

---

## Justification
[Pourquoi cette décision ?]

---

## Conditions de Lancement (si ATTENTE)
- [ ] [Condition 1]
- [ ] [Condition 2]

---

## Risques Acceptés
- [R-001] [Description] - Mitigation : [Plan]

---

## Périmètre Validé pour le Lancement
[Description du périmètre initial validé]

---

## Historique
| Date | Décision | Raison |
| :--- | :--- | :--- |
| [DATE] | [GO/NO-GO/ATTENTE] | [Raison] |
```

### 7.4 Template SPR-[NNN]-001 - Sprint Backlog

```markdown
# SPR-[NNN]-001 - Sprint [NNN] Backlog
**Sprint :** [NNN]
**Dates :** [DATE DEBUT] -> [DATE FIN]
**Sprint Goal :** [UNE PHRASE DÉCRIVANT L'OBJECTIF DU SPRINT]
**Capacité :** [X] points / [Y] jours

---

## User Stories Sélectionnées

### US-[XXX] - [Titre]
**Epic :** [Nom de l'Epic]
**Priorité :** Must / Should / Could
**Complexité :** XS / S / M / L / XL ([X] points)
**Assigné à :** Developer

**En tant que** [persona]
**Je veux** [action]
**Afin de** [bénéfice]

**Critères d'Acceptation :**
- [ ] [CA-001] [Critère mesurable]
- [ ] [CA-002] [Critère mesurable]

**Dépendances :** [US-XXX ou Aucune]
**Notes techniques :** [Contraintes d'implémentation]

---

## Récapitulatif

| US | Titre | Points | Statut |
| :--- | :--- | :--- | :--- |
| US-[XXX] | [Titre] | [X] | À faire / En cours / Terminé |

**Total points planifiés :** [X]
**Total points livrés :** [Y] *(mis à jour en fin de sprint)*
**Vélocité :** [Y/X * 100]% *(mis à jour en fin de sprint)*
```

### 7.5 Template SPR-[NNN]-004 - Rapport de Tests

```markdown
# SPR-[NNN]-004 - Rapport de Tests Sprint [NNN]
**Sprint :** [NNN]
**Date de test :** [DATE]
**QA Engineer :** [Mode QA Engineer - Roo Code]
**Backend LLM utilisé :** [Ollama / Proxy Gemini / Claude API]

---

## Résumé Exécutif

| Métrique | Valeur |
| :--- | :--- |
| US testées | [X] / [Y] planifiées |
| Tests passés | [X] |
| Tests échoués | [X] |
| Bugs critiques | [X] |
| Bugs mineurs | [X] |
| Couverture de code | [X]% |

---

## Résultats par User Story

### US-[XXX] - [Titre]
**Statut global :** VALIDÉE / REJETÉE / PARTIELLE

| Critère d'Acceptation | Résultat | Notes |
| :--- | :--- | :--- |
| CA-001 : [Description] | PASS / FAIL | [Notes] |
| CA-002 : [Description] | PASS / FAIL | [Notes] |

**Commande de test exécutée :** `[commande]`

**Sortie :** `[sortie de la commande]`

---

## Bugs Identifiés

### BUG-[NNN]-001 - [Titre]
**Sévérité :** CRITIQUE / HAUTE / MOYENNE / BASSE
**US concernée :** US-[XXX]
**Steps de reproduction :**
1. [Étape 1]
2. [Étape 2]
**Comportement attendu :** [Description]
**Comportement observé :** [Description]
**Statut :** Ouvert / Corrigé / Accepté

---

## Recommandation QA
**[ ] Sprint validé** - Toutes les US critiques passent les tests
**[ ] Sprint rejeté** - Des bugs critiques bloquent la livraison
**[ ] Livraison partielle** - [X] US validées sur [Y]
```

### 7.6 Template SPR-[NNN]-005 - Sprint Review

```markdown
# SPR-[NNN]-005 - Sprint Review Sprint [NNN]
**Sprint :** [NNN]
**Date :** [DATE]
**Participants :** Product Owner, Scrum Master

---

## Sprint Goal
[Rappel du Sprint Goal]
**Atteint :** OUI / NON / PARTIELLEMENT

---

## User Stories Livrées

| US | Titre | Points | Validée par QA |
| :--- | :--- | :--- | :--- |
| US-[XXX] | [Titre] | [X] | OUI / NON |

**Vélocité :** [X] points livrés / [Y] points planifiés = [Z]%

---

## User Stories Non Livrées

| US | Titre | Raison | Action |
| :--- | :--- | :--- | :--- |
| US-[XXX] | [Titre] | [Raison] | Reporter sprint suivant / Abandonner |

---

## Feedbacks sur les Fonctionnalités
[Observations sur les fonctionnalités livrées]

---

## Ajustements du Backlog
- [US-XXX] : Repriorisée de Should -> Must (raison : [])
- [US-YYY] : Nouvelle US ajoutée (raison : [])
- [US-ZZZ] : Abandonnée (raison : [])

---

## Décision de Release
**[ ] Release planifiée** pour la version [X.Y.Z]
**[ ] Pas de release** - Continuer les sprints
```

### 7.7 Template SPR-[NNN]-006 - Rétrospective

```markdown
# SPR-[NNN]-006 - Rétrospective Sprint [NNN]
**Sprint :** [NNN]
**Date :** [DATE]
**Facilité par :** Scrum Master

---

## Keep - Ce qui a bien fonctionné
- [Description]
- [Description]

## Improve - Ce qui doit être amélioré
- [Description] -> Action : [Action concrète]
- [Description] -> Action : [Action concrète]

## Stop - Ce qui doit être arrêté
- [Description]

---

## Actions pour le Prochain Sprint

| Action | Responsable | Échéance |
| :--- | :--- | :--- |
| [Description] | [Persona] | Sprint [NNN+1] |

---

## Impediments Identifiés

| Impediment | Impact | Résolution |
| :--- | :--- | :--- |
| [Description] | [Impact] | [Plan de résolution] |

---

## Métriques du Sprint
- Vélocité : [X] points
- Vélocité moyenne (3 derniers sprints) : [Y] points
- Tendance : En hausse / Stable / En baisse
```

---

## 8. Mécanismes Anti-Risques Agentiques

### 8.1 Catalogue des Risques Agentiques

Le développement agentique présente des risques spécifiques absents du développement humain classique. Ce catalogue les identifie et décrit les contre-mesures intégrées dans l'atelier.

| ID Risque | Risque | Probabilité | Impact | Contre-mesure Principale |
| :--- | :--- | :--- | :--- | :--- |
| **RA-001** | Perte de contexte entre sessions | TRÈS HAUTE | CRITIQUE | Memory Bank + Séquence VÉRIFIER→CRÉER→LIRE→AGIR |
| **RA-002** | Hallucination de code | HAUTE | CRITIQUE | Temperature 0.15 + Modelfile déterministe |
| **RA-003** | Dérive de l'architecture sur plusieurs mois | HAUTE | HAUTE | `systemPatterns.md` + ADR dans `decisionLog.md` |
| **RA-004** | Incohérence entre sessions longues | HAUTE | HAUTE | `activeContext.md` mis à jour à chaque session |
| **RA-005** | Régression silencieuse | MOYENNE | CRITIQUE | Tests QA obligatoires + rapports versionnés |
| **RA-006** | Perte de la vision produit | MOYENNE | HAUTE | `projectBrief.md` immuable sauf décision explicite |
| **RA-007** | Duplication de code non détectée | MOYENNE | MOYENNE | `systemPatterns.md` + revue Developer |
| **RA-008** | Décisions d'architecture non tracées | HAUTE | HAUTE | `decisionLog.md` + REGLE 2 `.clinerules` |
| **RA-009** | Prompt injection / dérive comportementale | BASSE | CRITIQUE | `.clinerules` + RBAC `.roomodes` |
| **RA-010** | Travail sur mauvaise version du code | MOYENNE | HAUTE | Git obligatoire + commits fréquents |

---

### 8.2 RA-001 - Perte de Contexte entre Sessions

**Description du risque :** Un LLM n'a aucune mémoire entre deux sessions. Sans mécanisme explicite, chaque session repart de zéro. Sur un projet de plusieurs mois, cela conduit à des incohérences, des réimplémentations, des contradictions.

**Contre-mesures intégrées :**

```
NIVEAU 1 - Séquence obligatoire au démarrage (REGLE 1 .clinerules)
  L'agent DOIT lire activeContext.md et progress.md avant toute action
  Si les fichiers n'existent pas, il les crée depuis les templates

NIVEAU 2 - Mise à jour obligatoire à la clôture (REGLE 2 .clinerules)
  L'agent DOIT mettre à jour activeContext.md avant attempt_completion
  activeContext.md contient : tâche en cours, dernier résultat, prochaine action

NIVEAU 3 - Contexte thématique selon la tâche (REGLE 3 .clinerules)
  Avant modification architecture : lire systemPatterns.md
  Avant commandes build/test : lire techContext.md
  En début de sprint : lire productContext.md

NIVEAU 4 - Redondance dans les roleDefinitions (.roomodes)
  Le Developer a le protocole LIRE->CODER->METTRE A JOUR->COMMITER inscrit
  dans son roleDefinition - même si .clinerules n'est pas lu
```

**Protocole de reprise après longue interruption (> 1 semaine) :**

> 📋 **PROMPT RA-001 — Reprise après interruption**
> **Mode Roo Code requis :** `scrum-master`
> **Complexité :** 🟢 Simple — 1 envoi, remplacer [X] par le nombre de jours d'interruption
> **Copier-coller le bloc ci-dessous tel quel, puis remplacer [X] :**

```markdown
Je reprends le projet après [X] jours d'interruption.
Lis dans cet ordre :
1. memory-bank/activeContext.md
2. memory-bank/progress.md
3. memory-bank/projectBrief.md
4. memory-bank/productContext.md

Puis génère un résumé de l'état du projet :
- Où en est-on ?
- Quelle était la dernière tâche en cours ?
- Quelles sont les prochaines actions ?
- Y a-t-il des blocages identifiés ?

Mets à jour activeContext.md avec la date de reprise.
Commite avec : 'docs(memory): reprise projet après [X] jours - [DATE]'
```

---

### 8.3 RA-002 - Hallucination de Code

**Description du risque :** Un LLM peut générer du code syntaxiquement correct mais fonctionnellement faux, inventer des APIs inexistantes, ou produire des implémentations qui semblent plausibles mais ne fonctionnent pas.

**Contre-mesures intégrées :**

```
NIVEAU 1 - Paramètres de déterminisme (Modelfile Ollama)
  temperature 0.15 (quasi-déterministe)
  min_p 0.03, top_p 0.95, repeat_penalty 1.1
  Réduit drastiquement les réponses "créatives" non fondées

NIVEAU 2 - Tests QA obligatoires après chaque US
  Le QA Engineer exécute les tests réels (pas simulés)
  Les critères d'acceptation sont vérifiés un par un
  Les bugs sont documentés dans SPR-[NNN]-004

NIVEAU 3 - Commits fréquents avec messages descriptifs
  Chaque sous-tâche est commitée séparément
  En cas d'hallucination détectée : git revert vers le dernier commit sain

NIVEAU 4 - Lecture de la Memory Bank avant de coder
  systemPatterns.md contient les patterns RÉELS du projet
  techContext.md contient les commandes RÉELLES testées
  L'agent code en cohérence avec ce qui existe, pas ce qu'il imagine
```

**Détection d'une hallucination :**

```
Signes d'alerte :
- L'agent importe une bibliothèque qui n'est pas dans requirements.txt
- L'agent appelle une fonction qui n'existe pas dans le code
- L'agent décrit une architecture différente de systemPatterns.md
- Les tests QA échouent systématiquement sur une US

Action corrective :
1. git log --oneline -10  (identifier le dernier commit sain)
2. git diff HEAD~1        (voir ce qui a changé)
3. git revert [hash]      (revenir en arrière si nécessaire)
4. Mettre à jour activeContext.md avec la description du problème
5. Relancer le Developer avec un contexte plus précis
```

---

### 8.4 RA-003 - Dérive Architecturale sur Plusieurs Mois

**Description du risque :** Sur un projet long, les décisions d'architecture prises en Phase 1 peuvent être oubliées ou contredites par des décisions ultérieures. Sans traçabilité, le code devient incohérent.

**Contre-mesures intégrées :**

```
NIVEAU 1 - decisionLog.md comme registre des ADR
  Chaque décision d'architecture est documentée avec :
  Date, contexte, décision prise, conséquences
  Format : ADR-[NNN] avec numérotation séquentielle

NIVEAU 2 - systemPatterns.md comme référence vivante
  Mis à jour après chaque décision d'architecture
  Contient les patterns ACTUELS (pas les patterns initiaux)
  L'agent lit ce fichier avant toute modification architecturale

NIVEAU 3 - REGLE 2 .clinerules
  Si une décision d'architecture est prise durant la session :
  obligatoirement mettre à jour decisionLog.md

NIVEAU 4 - Revue architecturale en Sprint Review
  Le Product Owner vérifie la cohérence avec la vision initiale
  Les dérives sont ident
iifiées et documentées
```

**Protocole de revue architecturale (tous les 3 sprints) :**

> 📋 **PROMPT RA-003 — Revue architecturale**
> **Mode Roo Code requis :** `developer`
> **Complexité :** 🟢 Simple — 1 envoi, remplacer [NNN] par le numéro du sprint courant
> **Copier-coller le bloc ci-dessous tel quel, puis remplacer [NNN] :**

```markdown
Lis memory-bank/systemPatterns.md, memory-bank/decisionLog.md
et docs/architecture/PRJ-002-architecture-initiale.md.

Compare l'architecture initiale avec l'architecture actuelle.
Identifie :
- Les dérives par rapport à l'architecture initiale
- Les décisions implicites non documentées dans decisionLog.md
- Les patterns incohérents entre modules

Documente tes conclusions dans docs/architecture/ARCH-REVIEW-[DATE].md.
Mets à jour decisionLog.md avec les ADR manquants.
Commite avec : 'docs(architecture): revue architecturale sprint [NNN]'
```

---

### 8.5 RA-004 - Incohérence sur Sessions Longues (Multi-Mois)

**Description du risque :** Sur un projet de plusieurs mois avec des dizaines de sessions, les informations dans la Memory Bank peuvent devenir obsolètes, contradictoires ou incomplètes.

**Contre-mesures intégrées :**

```
NIVEAU 1 - activeContext.md comme "mémoire vive"
  Mis à jour à CHAQUE session (début et fin)
  Contient toujours l'état le plus récent
  Inclut le hash du dernier commit Git

NIVEAU 2 - progress.md comme "tableau de bord"
  Checklist des phases et features
  Mis à jour à chaque fin de sprint
  Permet de voir d'un coup d'oeil où en est le projet

NIVEAU 3 - Versionnement Git de la Memory Bank
  git log --oneline -- memory-bank/ montre l'historique complet
  En cas de doute : git show [hash]:memory-bank/activeContext.md

NIVEAU 4 - Audit de cohérence périodique (mensuel)
```

**Protocole d'audit de cohérence Memory Bank (mensuel) :**

> 📋 **PROMPT RA-004 — Audit de cohérence Memory Bank**
> **Mode Roo Code requis :** `scrum-master`
> **Complexité :** 🔵 Séquentiel — l'agent vérifie chaque fichier et corrige les incohérences
> **Copier-coller le bloc ci-dessous tel quel :**

```markdown
Effectue un audit de cohérence de la Memory Bank.

Pour chaque fichier, vérifie :
1. projectBrief.md : La vision est-elle toujours valide ?
2. productContext.md : Le backlog est-il à jour avec les sprints livrés ?
3. systemPatterns.md : Les patterns correspondent-ils au code actuel ?
4. techContext.md : Les commandes et versions sont-elles à jour ?
5. activeContext.md : L'état décrit correspond-il à la réalité Git ?
6. progress.md : Les cases cochées correspondent-elles aux commits ?
7. decisionLog.md : Toutes les décisions récentes sont-elles documentées ?

Pour chaque incohérence trouvée, corrige le fichier concerné.
Commite avec : 'docs(memory): audit cohérence mensuel [DATE]'
```

---

### 8.6 RA-005 - Régression Silencieuse

**Description du risque :** Une modification du Developer peut casser une fonctionnalité existante sans que personne ne le détecte, surtout si les tests ne couvrent pas toutes les fonctionnalités.

**Contre-mesures intégrées :**

```
NIVEAU 1 - Tests QA obligatoires après chaque US
  Le QA Engineer teste non seulement la nouvelle US
  Mais aussi les US précédentes potentiellement impactées

NIVEAU 2 - Commits atomiques
  Chaque US = série de commits liés
  git bisect permet d'identifier le commit qui a introduit la régression

NIVEAU 3 - Rapport de tests versionné
  SPR-[NNN]-004 documente l'état des tests à chaque sprint
  Comparaison possible entre sprints pour détecter les régressions

NIVEAU 4 - Critères d'acceptation dans le Sprint Backlog
  Chaque US a des critères d'acceptation précis et testables
  Le QA Engineer vérifie chaque critère individuellement
```

---

### 8.7 RA-008 - Décisions d'Architecture Non Tracées

**Description du risque :** L'agent prend des décisions d'architecture implicites (choix d'une bibliothèque, pattern d'implémentation) sans les documenter. Ces décisions sont perdues entre les sessions.

**Contre-mesures intégrées :**

```
NIVEAU 1 - REGLE 2 .clinerules (obligatoire)
  Si une décision d'architecture a été prise durant la session :
  OBLIGATOIREMENT mettre à jour memory-bank/decisionLog.md

NIVEAU 2 - Format ADR standardisé
  Chaque ADR contient : Date, Contexte, Décision, Conséquences
  Numérotation séquentielle : ADR-001, ADR-002, ...

NIVEAU 3 - Détection proactive par le Developer
  Avant de choisir une bibliothèque : vérifier decisionLog.md
  Si une décision similaire existe : la respecter ou la réviser explicitement
```

**Format ADR standard :**

```markdown
## ADR-[NNN] : [Titre de la décision]
**Date :** [DATE]
**Statut :** Proposé / Accepté / Déprécié / Remplacé par ADR-[YYY]

**Contexte :**
[Pourquoi cette décision était nécessaire]

**Décision :**
[Ce qui a été décidé]

**Conséquences :**
- Avantage : [Description]
- Inconvénient : [Description]
- Impact sur : [Fichiers/modules concernés]
```

---

### 8.8 Tableau de Synthèse Anti-Risques

| Risque | Mécanisme Préventif | Mécanisme Détectif | Mécanisme Correctif |
| :--- | :--- | :--- | :--- |
| RA-001 Perte contexte | Memory Bank + REGLE 1 | Séquence VÉRIFIER→CRÉER→LIRE | Protocole reprise longue interruption |
| RA-002 Hallucination | T=0.15 + Modelfile | Tests QA + git diff | git revert + relance avec contexte précis |
| RA-003 Dérive archi | decisionLog.md + REGLE 2 | Revue archi tous les 3 sprints | ARCH-REVIEW + mise à jour ADR |
| RA-004 Incohérence multi-mois | activeContext.md à chaque session | Audit mensuel Memory Bank | Correction + commit docs(memory) |
| RA-005 Régression | Tests QA obligatoires | SPR-[NNN]-004 compare aux précédents | git bisect + fix + re-test |
| RA-008 ADR non tracés | REGLE 2 .clinerules | Audit decisionLog.md | Rétro-documentation des décisions |

---

## 9. Protocoles de Session

### 9.1 Protocole de Démarrage de Session

**Applicable à toutes les sessions, tous modes, tous personas.**

```
ÉTAPE 1 - VÉRIFICATION (automatique via .clinerules REGLE 1)
  L'agent vérifie l'existence de :
  - memory-bank/activeContext.md
  - memory-bank/progress.md

ÉTAPE 2 - CRÉATION si absents
  Si l'un des fichiers est absent :
  L'agent le crée depuis le template défini dans .clinerules
  Puis passe à l'étape 3

ÉTAPE 3 - LECTURE
  L'agent lit dans cet ordre :
  1. memory-bank/activeContext.md  (état courant)
  2. memory-bank/progress.md       (avancement global)

ÉTAPE 4 - LECTURE CONTEXTUELLE (selon la tâche)
  Si modification d'architecture prévue : lire systemPatterns.md
  Si commandes build/test prévues : lire techContext.md
  Si début de sprint : lire productContext.md

ÉTAPE 5 - ACTION
  L'agent traite la demande de l'utilisateur
```

> 📋 **PROMPT 9.1 — Démarrage de session (instruction de contexte)**
> **Mode Roo Code requis :** `[le mode approprié à la tâche]`
> **Complexité :** 🟢 Simple — à ajouter en tête de n'importe quel prompt pour forcer la lecture du contexte
> **Copier-coller ce préfixe avant votre demande :**

```markdown
Avant d'agir, lis memory-bank/activeContext.md et
memory-bank/progress.md pour te remettre dans le contexte du projet.

[Décrire ici la tâche à accomplir]
```

---

### 9.2 Protocole de Clôture de Session

**Applicable avant tout `attempt_completion`, tous modes, tous personas.**

```
ÉTAPE 1 - MISE À JOUR activeContext.md (obligatoire)
  Contenu à mettre à jour :
  - Date de mise à jour
  - Tâche accomplie durant cette session
  - État actuel du projet
  - Prochaine(s) action(s) recommandée(s)
  - Blocages éventuels
  - Hash du dernier commit Git

ÉTAPE 2 - MISE À JOUR progress.md (si features terminées)
  Cocher les US ou phases terminées durant la session

ÉTAPE 3 - MISE À JOUR decisionLog.md (si décision d'architecture)
  Documenter toute décision d'architecture prise durant la session
  Format ADR standard (voir section 8.7)

ÉTAPE 4 - COMMIT GIT (obligatoire)
  git add .
  git commit -m "docs(memory): [description de la session]"
  Le hash de ce commit doit être noté dans activeContext.md
```

---

### 9.3 Protocole de Reprise après Interruption

**Utiliser ce protocole après toute interruption > 1 semaine.**

> 📋 **PROMPT 9.3 — Reprise après interruption longue**
> **Mode Roo Code requis :** `scrum-master`
> **Complexité :** 🟢 Simple — 1 envoi, remplacer [X] et [DATE]
> **Copier-coller le bloc ci-dessous tel quel, puis remplacer [X] et [DATE] :**

```markdown
Je reprends le projet après [X] jours/semaines d'interruption.

Effectue un bilan de reprise :

1. Lis memory-bank/activeContext.md
   -> Quelle était la dernière tâche en cours ?
   -> Quel était l'état du projet ?

2. Lis memory-bank/progress.md
   -> Quelles phases/features sont terminées ?
   -> Quelles sont en cours ?

3. Exécute : git log --oneline -10
   -> Quels sont les derniers commits ?
   -> Y a-t-il des commits non documentés dans la Memory Bank ?

4. Lis memory-bank/projectBrief.md
   -> La vision du projet est-elle toujours valide ?

5. Génère un rapport de reprise dans docs/sprints/REPRISE-[DATE].md :
   - État du projet au moment de la reprise
   - Prochaines actions recommandées
   - Risques identifiés après l'interruption

6. Mets à jour memory-bank/activeContext.md avec la date de reprise.
7. Commite avec : 'docs(memory): reprise projet après [X] jours - [DATE]'
```

---

### 9.4 Protocole de Changement de Backend LLM

**Utiliser ce protocole lors du basculement entre les 3 modes LLM.**

```
AVANT LE BASCULEMENT :
  1. Commiter l'état actuel de la Memory Bank
     git add memory-bank/
     git commit -m "docs(memory): sauvegarde avant changement backend LLM"

  2. Noter dans activeContext.md le nouveau backend utilisé
     "Backend LLM actif : [Ollama uadf-agent | Proxy Gemini | Claude Sonnet API]"

APRÈS LE BASCULEMENT :
  3. Tester le nouveau backend avec une requête simple
     "Lis memory-bank/activeContext.md et résume l'état du projet."

  4. Vérifier que la Memory Bank est correctement lue
     Le résumé doit correspondre au contenu réel des fichiers

POURQUOI CE PROTOCOLE :
  Chaque backend LLM a des caractéristiques différentes :
  - Ollama (local) : déterministe, peut être plus lent sur tâches complexes
  - Proxy Gemini : haute qualité, nécessite copier-coller humain
  - Claude API : haute qualité, entièrement automatique, payant
  La Memory Bank garantit la continuité du contexte quel que soit le backend.
```

> ⚠️ **LIMITATIONS CONNUES DU MODE PROXY GEMINI** (à documenter dans `activeContext.md` lors du basculement) :
>
> | Limitation | Détail | Alternative |
> | :--- | :--- | :--- |
> | **Boomerang Tasks (`new_task`) : NON SUPPORTÉ** | Deux instances Roo Code concurrentes partagent le même presse-papiers → deadlock immédiat | Utiliser Mode Local (Ollama) ou Mode Cloud (Claude API) |
> | **Tâches longues (> 10 tours LLM) : DÉCONSEILLÉ** | Taille du presse-papiers explose, fatigue cognitive humaine | Découper en sous-tâches de < 10 tours, ou utiliser Claude API |
> | **Utilisation parallèle du presse-papiers : IMPOSSIBLE** | Tout Ctrl+C pendant une session proxy écrase la réponse Gemini en attente | Ne pas utiliser le presse-papiers pour autre chose pendant une session |
> | **Exécution sans surveillance : IMPOSSIBLE** | Présence humaine continue requise à chaque tour LLM | Utiliser Mode Local (Ollama) ou Mode Cloud (Claude API) |
> | **Conversation Gemini : TOUJOURS nouvelle conversation** | Le proxy envoie déjà l'historique complet dans le presse-papiers — continuer une conversation existante duplique l'historique | Ouvrir une nouvelle conversation Gemini à chaque session proxy |

> 📋 **PROMPT 9.4 — Test de basculement backend LLM**
> **Mode Roo Code requis :** `scrum-master`
> **Complexité :** 🟢 Simple — 1 envoi pour vérifier que le nouveau backend lit bien la Memory Bank
> **Copier-coller le bloc ci-dessous tel quel :**

```markdown
Lis memory-bank/activeContext.md et résume en 5 points :
1. Le projet en cours
2. La dernière tâche accomplie
3. L'état actuel
4. Les prochaines actions
5. Les blocages éventuels
```

---

### 9.5 Protocole de Gestion des Conflits Git

**Utiliser ce protocole si des conflits Git apparaissent (rare mais possible).**

> 📋 **PROMPT 9.5 — Résolution de conflits Git**
> **Mode Roo Code requis :** `developer`
> **Complexité :** 🔄 Itératif — l'agent identifie les conflits et propose des résolutions
> **Copier-coller le bloc ci-dessous tel quel :**

```markdown
Un conflit Git a été détecté.

1. Exécute : git status
   -> Identifier les fichiers en conflit

2. Pour chaque fichier en conflit :
   - Si conflit dans memory-bank/ : privilégier la version la plus récente
   - Si conflit dans src/ : analyser les deux versions et choisir la meilleure
   - Si conflit dans docs/ : fusionner les deux versions si possible

3. Après résolution :
   git add [fichiers résolus]
   git commit -m 'fix(git): résolution conflit [description]'

4. Mettre à jour memory-bank/activeContext.md avec la description du conflit
   et sa résolution.
```

---

### 9.6 Protocole de Gestion des Erreurs d'Agent

**Utiliser ce protocole si l'agent produit des résultats incorrects ou incohérents.**

```
DIAGNOSTIC :
  1. Identifier le type d'erreur :
     - Hallucination (code inventé, API inexistante)
     - Incohérence avec la Memory Bank (ignore les conventions)
     - Dépassement de contexte (oublie le début de la conversation)
     - Erreur de permission RBAC (tente une action hors périmètre)

CORRECTION SELON LE TYPE :

  Hallucination :
  -> git revert [dernier commit problématique]
  -> Relancer avec un contexte plus précis et des exemples concrets
  -> Vérifier que systemPatterns.md et techContext.md sont à jour

  Incohérence avec Memory Bank :
  -> Vérifier que .clinerules est à la racine du projet
  -> Recharger VS Code (Ctrl+Shift+P > "Developer: Reload Window")
  -> Relancer en rappelant explicitement de lire la Memory Bank

  Dépassement de contexte :
  -> Commencer une nouvelle session Roo Code
  -> La nouvelle session relira la Memory Bank depuis le début
  -> C'est pour cela que la Memory Bank doit être à jour avant chaque clôture

  Erreur RBAC :
  -> Vérifier que le bon persona est sélectionné dans Roo Code
  -> Vérifier que .roomodes est à la racine du projet
  -> Si le persona tente une action hors périmètre, il doit refuser
     et suggérer le persona approprié
```

---

## 10. Tableau de Bord du Projet

### 10.1 Indicateurs de Santé du Projet

Le tableau de bord est maintenu dans `memory-bank/progress.md`. Il doit refléter en permanence l'état réel du projet.

**Indicateurs à surveiller :**

| Indicateur | Source | Fréquence de Mise à Jour | Seuil d'Alerte |
| :--- | :--- | :--- | :--- |
| Vélocité du sprint | SPR-[NNN]-005 | Fin de sprint | < 50% de la vélocité cible |
| Couverture de tests | SPR-[NNN]-004 | Fin de sprint | < 70% |
| Bugs critiques ouverts | SPR-[NNN]-004 | Continu | > 0 |
| ADR non documentés | decisionLog.md | Continu | > 0 |
| Memory Bank à jour | activeContext.md | Chaque session | > 48h sans mise à jour |
| Commits sans message | git log | Continu | > 0 commits "WIP" ou vides |

---

### 10.2 Template progress.md Étendu pour Projet Applicatif

```markdown
# Progression du Projet [NOM DU PROJET]
**Dernière mise à jour :** [DATE]
**Sprint courant :** [NNN]
**Backend LLM actif :** [Ollama / Proxy Gemini / Claude API]

---

## Infrastructure Atelier
- [x] Phase 0 : Amont ouvert - Décision GO
- [x] Phase 1 : Cadrage - Memory Bank initialisée
- [x] Phase 1 : Architecture initiale validée
- [x] Phase 1 : Backlog initial créé
- [ ] Phase 2 : Sprint 001 en cours
- [ ] Phase 3 : Première release

---

## Backlog par Epic

### Epic 1 : [Nom de l'Epic]
- [x] US-001 : [Titre] - Sprint 001 - LIVRÉE
- [-] US-002 : [Titre] - Sprint 001 - EN COURS
- [ ] US-003 : [Titre] - Sprint 002 - PLANIFIÉE
- [ ] US-004 : [Titre] - Backlog - NON PLANIFIÉE

### Epic 2 : [Nom de l'Epic]
- [ ] US-010 : [Titre] - Backlog - NON PLANIFIÉE

---

## Historique des Sprints

| Sprint | Dates | Goal | US Planifiées | US Livrées | Vélocité |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Sprint 001 | [DATE]->[DATE] | [Goal] | [X] | [Y] | [Z]% |

---

## Bugs Ouverts

| ID | Sévérité | US | Description | Sprint Cible |
| :--- | :--- | :--- | :--- | :--- |
| BUG-001-001 | HAUTE | US-002 | [Description] | Sprint 002 |

---

## Décisions d'Architecture Récentes
- ADR-001 : [Titre] - [DATE] - Accepté
- ADR-002 : [Titre] - [DATE] - Accepté

---

## Légende
- [ ] À faire  |  [-] En cours  |  [x] Terminé
```

---

### 10.3 Checklist de Qualité par Sprint

À vérifier en fin de chaque sprint avant de commencer le suivant :

**Qualité du Code :**
- [ ] Toutes les US du sprint ont des tests QA documentés
- [ ] Aucun bug critique ouvert
- [ ] Le code respecte les conventions de `systemPatterns.md`
- [ ] Toutes les dépendances sont dans `requirements.txt` / `package.json`

**Qualité de la Memory Bank :**
- [ ] `activeContext.md` mis à jour avec l'état fin de sprint
- [ ] `progress.md` mis à jour (US cochées)
- [ ] `decisionLog.md` contient tous les ADR du sprint
- [ ] `productContext.md` reflète les ajustements backlog de la Sprint Review

**Qualité du Versionnement :**
- [ ] Tous les fichiers modifiés sont commités
- [ ] Les messages de commit suivent le format Conventional Commits
- [ ] Aucun fichier `.env` ou `venv/` dans Git
- [ ] `git log --oneline -10` montre des commits descriptifs

**Qualité des Artifacts :**
- [ ] `SPR-[NNN]-001` (Sprint Backlog) existe et est complet
- [ ] `SPR-[NNN]-004` (Rapport de Tests) existe et est signé par QA Engineer
- [ ] `SPR-[NNN]-005` (Sprint Review) existe avec la vélocité calculée
- [ ] `SPR-[NNN]-006` (Rétrospective) existe avec les actions du prochain sprint

---

### 10.4 Commandes de Diagnostic Rapide

Ces commandes permettent de vérifier rapidement l'état du projet :

```powershell
# État Git du projet
git log --oneline -10
git status

# Vérifier que la Memory Bank est à jour
Get-Content memory-bank/activeContext.md | Select-Object -First 10

# Lister tous les artifacts du projet
Get-ChildItem docs/ -Recurse -Filter "*.md" | Select-Object Name, LastWriteTime

# Vérifier les bugs ouverts dans les rapports QA
Select-String -Path "docs/sprints/**/*.md" -Pattern "Statut : Ouvert"

# Vérifier la cohérence des prompts (atelier)
powershell -ExecutionPolicy Bypass -File "scripts/check-prompts-sync.ps1"

# Historique de la Memory Bank
git log --oneline -- memory-bank/

# Dernière mise à jour de activeContext.md
git log --oneline -3 -- memory-bank/activeContext.md
```

---

### 10.5 Signaux d'Alerte et Actions Correctives

| Signal d'Alerte | Cause Probable | Action Corrective |
| :--- | :--- | :--- |
| L'agent ignore la Memory Bank | `.clinerules` absent ou mal placé | Vérifier que `.clinerules` est à la racine, recharger VS Code |
| L'agent hallucine du code | Contexte insuffisant, temperature trop haute | Lire `systemPatterns.md` + `techContext.md` avant de coder |
| Les tests échouent systématiquement | Régression introduite, hallucination | `git bisect` pour identifier le commit fautif, `git revert` |
| La vélocité chute de > 30% | Complexité sous-estimée, impediments | Rétrospective immédiate, revoir les estimations |
| `activeContext.md` date de > 48h | Sessions sans mise à jour Memory Bank | Audit Memory Bank (protocole 9.3) |
| Conflits Git fréquents | Plusieurs sessions parallèles | Toujours commiter avant de changer de session |
| Bugs critiques s'accumulent | Tests insuffisants, US trop larges | Découper les US, renforcer les critères d'acceptation |
| L'architecture dérive | ADR non documentés, Memory Bank obsolète | Revue architecturale (protocole RA-003) |

---

## Annexe A - Correspondance Artifacts / Memory Bank / Git

| Artifact | Fichier | Commit Format | Persona |
| :--- | :--- | :--- | :--- |
| BRIEF-001 | `docs/brief/BRIEF-001-*.md` | `docs(brief): vision narrative initiale` | Product Owner |
| BRIEF-002 | `docs/brief/BRIEF-002-*.md` | `docs(brief): synthèse structurée` | Developer |
| BRIEF-003 | `docs/brief/BRIEF-003-*.md` | `docs(brief): décision lancement [GO/NO-GO]` | Product Owner |
| PRJ-001 | `memory-bank/projectBrief.md` | `feat(memory): initialisation projectBrief` | Product Owner |
| PRJ-002 | `docs/architecture/PRJ-002-*.md` | `feat(architecture): architecture initiale` | Developer |
| PRJ-003 | `docs/backlog/PRJ-003-*.md` | `feat(backlog): backlog initial MoSCoW` | Product Owner |
| SPR-NNN-001 | `docs/sprints/sprint-NNN/SPR-NNN-001-*.md` | `feat(sprint-NNN): sprint planning` | Product Owner |
| SPR-NNN-004 | `docs/sprints/sprint-NNN/SPR-NNN-004-*.md` | `test(sprint-NNN): rapport de tests` | QA Engineer |
| SPR-NNN-005 | `docs/sprints/sprint-NNN/SPR-NNN-005-*.md` | `docs(sprint-NNN): sprint review` | Product Owner |
| SPR-NNN-006 | `docs/sprints/sprint-NNN/SPR-NNN-006-*.md` | `docs(sprint-NNN): rétrospective` | Scrum Master |
| REL-VER-001 | `docs/releases/REL-VER-001-*.md` | `docs(release): release notes vVER` | Developer |
| ADR-NNN | `memory-bank/decisionLog.md` | `docs(memory): ADR-NNN [titre]` | Developer |

---

## Annexe B - Glossaire du Processus

| Terme | Définition |
| :--- | :--- |
| **Artifact** | Document produit par le processus Agile. Chaque artifact a un ID unique, un template, un persona responsable et un emplacement défini dans la structure du projet. |
| **Amont Ouvert** | Phase 0 du processus. Accepte des entrées non-structurées (emails, notes, code existant) et les transforme progressivement en artifacts structurés via BRIEF-001, BRIEF-002, BRIEF-003. |
| **Convergence Progressive** | Principe selon lequel les entrées narratives brutes (Phase 0) mûrissent vers des artifacts de plus en plus structurés (Phase 1, Phase 2) sans forcer une structure prématurée. |
| **Défense en Profondeur** | Principe de sécurité agentique : chaque règle critique est inscrite à plusieurs niveaux (`.clinerules`, `roleDefinition`, protocoles de session) pour qu'elle soit respectée même si un niveau est ignoré. |
| **Epic** | Regroupement fonctionnel de User Stories partageant un objectif métier commun. Une Epic peut s'étendre sur plusieurs sprints. |
| **Hallucination** | Comportement d'un LLM qui génère du contenu plausible mais incorrect (code inventé, API inexistante, architecture fictive). Contre-mesure principale : temperature 0.15 + tests QA obligatoires. |
| **Impediment** | Obstacle qui empêche l'équipe de progresser. Identifié par le Scrum Master dans la Rétrospective. Doit avoir un plan de résolution documenté. |
| **MoSCoW** | Méthode de priorisation : Must (obligatoire), Should (important), Could (souhaitable), Won't (hors périmètre). Utilisée pour le backlog initial (PRJ-003). |
| **Perte de Contexte** | Risque agentique RA-001. Un LLM n'a aucune mémoire entre deux sessions. La Memory Bank est le mécanisme principal de contre-mesure. |
| **Protocole de Session** | Séquence d'actions obligatoires au démarrage et à la clôture de chaque session Roo Code. Garantit la continuité du contexte entre les sessions. |
| **Régression Silencieuse** | Bug introduit par une modification qui casse une fonctionnalité existante sans être détecté immédiatement. Contre-mesure : tests QA après chaque US. |
| **Sprint Goal** | Objectif en une phrase du sprint. Définit ce que l'équipe s'engage à livrer. Inscrit dans SPR-NNN-001 et dans `activeContext.md`. |
| **T-shirt Sizing** | Méthode d'estimation de complexité : XS (< 1h), S (1-4h), M (4-8h), L (1-3j), XL (> 3j). Utilisée pour le backlog initial. |
| **User Story** | Description d'une fonctionnalité du point de vue de l'utilisateur. Format : "En tant que [persona], je veux [action] afin de [bénéfice]". Identifiée par US-NNN. |
| **Vélocité** | Nombre de points livrés par sprint. Indicateur de la capacité de l'équipe. Calculée dans SPR-NNN-005. |

---

## Annexe C - Table des Références

| Réf. | Type | Titre / Identifiant | Description |
| :--- | :--- | :--- | :--- |
| [DOC1] | Document interne | `workbench/DOC1-PRD-Workbench-Requirements.md` | Exigences de l'atelier - REQ-xxx référencées dans ce document |
| [DOC2] | Document interne | `workbench/DOC2-ARCH-Workbench-Technical-Design.md` | Architecture technique de l'atelier - DA-xxx référencées |
| [DOC3] | Document interne | `workbench/DOC3-BUILD-Workbench-Assembly-Phases.md` | Plan
 d'installation de l'atelier (Phases 0-12) |
| [DOC4] | Document interne | `workbench/DOC4-GUIDE-Workbench-Deployment-Howto.md` | Guide de déploiement de l'atelier sur projets |
| [DOC5] | Document interne | `workbench/DOC5-GUIDE-Project-Development-Process.md` | Ce document - Manuel du processus Agile applicatif |
| [SCRUM] | Standard | Scrum Guide (scrumguides.org) | Guide officiel Scrum - référence pour les cérémonies et rôles |
| [MOSCOW] | Méthode | MoSCoW Prioritization | Méthode de priorisation Must/Should/Could/Won't |
| [ADR] | Pattern | Architecture Decision Records (adr.github.io) | Format standard pour documenter les décisions d'architecture |
| [SEMVER] | Standard | Semantic Versioning (semver.org) | Convention MAJOR.MINOR.PATCH pour les releases |
| [CONVCOMMITS] | Standard | Conventional Commits (conventionalcommits.org) | Convention de messages de commit : type(scope): description |
| [MEMORY-BANK] | Composant Atelier | `memory-bank/` (7 fichiers .md) | Système de mémoire persistante - contre-mesure principale RA-001 |
| [CLINERULES] | Composant Atelier | `.clinerules` (6 règles impératives) | Directives de session - REGLE 1 à REGLE 6 |
| [ROOMODES] | Composant Atelier | `.roomodes` (4 personas Agile) | Personas Product Owner, Scrum Master, Developer, QA Engineer |
