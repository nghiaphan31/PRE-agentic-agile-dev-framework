# Document 4 : Guide de Déploiement de l'Atelier UADF
## Comment utiliser ce template sur un nouveau projet ou une base de code existante

**Nom du Projet :** Unified Agentic Development Framework (UADF)
**Version :** 1.0
**Date :** 2026-03-23
**Références :** DOC1-PRD-Unified-Agentic-Framework.md v2.0, DOC2-Architecture-Solution-Stack.md v2.0, DOC3-Plan-Implementation-COMPLETE.md v3.0

---

## 1. Comprendre ce que ce Dépôt Est (et n'est pas)

### 1.1 Ce Dépôt = L'Atelier, pas le Produit

La distinction la plus importante à comprendre avant tout déploiement :

```
PRE-agentic-agile-dev-framework/   ← VOUS ÊTES ICI
│                                     C'est l'ATELIER
│
│  plans/          ← Les plans de l'atelier (DOC1, DOC2, DOC3, DOC4)
│  prompts/        ← Les outils de l'atelier (system prompts SP-001 à SP-007)
│  proxy.py        ← Une machine de l'atelier (pont Roo Code <-> Gemini Chrome)
│  .roomodes       ← Les rôles des ouvriers de l'atelier (4 personas Agile)
│  .clinerules     ← Le règlement de l'atelier (6 règles impératives)
│  scripts/        ← Les scripts utilitaires de l'atelier
│
└── Il produit des PROJETS (dépôts séparés, dans d'autres dossiers)
```

**Ce dépôt ne contient pas de code applicatif.** Il contient les règles, outils, processus et system prompts qui permettent de développer n'importe quel projet de manière agentique, agile et versionnée.

**Analogie :** C'est comme un atelier de menuiserie. L'atelier contient les outils (scies, rabots, marteaux), les plans de travail, les règles de sécurité. Les meubles fabriqués (les projets) sont des entités séparées qui quittent l'atelier une fois terminés.

### 1.2 Ce que ce Dépôt Contient

| Fichier / Dossier | Rôle dans l'Atelier | Analogie |
| :--- | :--- | :--- |
| `plans/DOC1-PRD-*.md` | Exigences de l'atelier lui-même | Manuel de l'atelier |
| `plans/DOC2-Architecture-*.md` | Architecture technique de l'atelier | Plans des machines |
| `plans/DOC3-Plan-Implementation-*.md` | Guide d'installation de l'atelier | Notice de montage |
| `plans/DOC4-Guide-Deploiement-*.md` | Ce document — comment utiliser l'atelier | Mode d'emploi |
| `prompts/SP-001 à SP-007` | System prompts canoniques | Fiches de poste des ouvriers |
| `.roomodes` | Définition des 4 personas Agile | Organigramme de l'atelier |
| `.clinerules` | 6 règles impératives pour tous les modes | Règlement intérieur |
| `proxy.py` | Pont Roo Code ↔ Gemini Chrome | Machine de relais |
| `scripts/` | Scripts utilitaires | Outils automatisés |

### 1.3 Ce que ce Dépôt NE Contient PAS

- ❌ Le code source de votre application (c'est dans le dépôt du projet)
- ❌ La Memory Bank de votre projet (c'est dans le dépôt du projet)
- ❌ Les rapports QA de votre projet (c'est dans le dépôt du projet)
- ❌ Les User Stories de votre projet (c'est dans la Memory Bank du projet)

### 1.4 Pourquoi Versionner ce Dépôt ?

Ce dépôt évoluera au fil du temps. Vous le mettrez à jour quand :
- Une règle `.clinerules` s'avère insuffisante ou ambiguë → vous la corrigez ici
- Vous ajoutez un nouveau persona (ex: DevOps Engineer, Architect) → vous l'ajoutez dans `.roomodes` et `prompts/`
- Vous améliorez `proxy.py` (nouveau timeout, meilleure gestion des erreurs) → vous le mettez à jour ici
- Vous découvrez un pattern de Memory Bank plus efficace → vous mettez à jour les templates dans `.clinerules`

**Chaque amélioration de l'atelier bénéficie à tous les futurs projets.** C'est l'intérêt de séparer l'atelier des projets.

---

## 2. Vue d'Ensemble : Atelier vs Projets

```
┌─────────────────────────────────────────────────────────────────┐
│                    ATELIER UADF (ce dépôt)                      │
│                                                                  │
│  .roomodes  .clinerules  prompts/  proxy.py  scripts/  plans/   │
│                                                                  │
│  Versionné, enrichi, partagé entre tous les projets             │
└──────────────────────────┬──────────────────────────────────────┘
                           │ Déploiement (copie des fichiers)
              ┌────────────┴────────────┐
              │                         │
              ▼                         ▼
┌─────────────────────┐   ┌─────────────────────────────────────┐
│   NOUVEAU PROJET    │   │   PROJET EXISTANT (code spaghetti)  │
│                     │   │                                     │
│  mon-nouveau-projet/│   │  mon-projet-legacy/                 │
│  ├── .roomodes      │   │  ├── src/  (code existant)          │
│  ├── .clinerules    │   │  ├── .roomodes  (ajouté)            │
│  ├── proxy.py       │   │  ├── .clinerules  (ajouté)          │
│  ├── prompts/       │   │  ├── proxy.py  (ajouté)             │
│  ├── memory-bank/   │   │  ├── prompts/  (ajouté)             │
│  │   (vide → rempli)│   │  ├── memory-bank/  (audit d'abord)  │
│  └── src/  (à créer)│   │  └── docs/qa/  (ajouté)            │
└─────────────────────┘   └─────────────────────────────────────┘
```

---

## 3. Déploiement sur un Nouveau Projet

### 3.1 Prérequis

Avant de commencer, l'atelier UADF doit être installé et fonctionnel sur votre machine (phases 0-12 de DOC3). En particulier :
- Ollama avec `uadf-agent` disponible (Mode 1) OU proxy.py démarré (Mode 2) OU clé Anthropic configurée (Mode 3)
- VS Code avec l'extension Roo Code installée

### 3.2 Étape 1 — Créer le Dépôt du Nouveau Projet

```powershell
# Créer le dossier du nouveau projet (EN DEHORS du dossier de l'atelier)
New-Item -Path "C:\Projets" -Name "mon-nouveau-projet" -ItemType Directory
cd "C:\Projets\mon-nouveau-projet"

# Initialiser Git
git init
git branch -M main
```

> **Important :** Le nouveau projet est un dépôt Git **séparé** de l'atelier. Ne créez pas le projet à l'intérieur du dossier `PRE-agentic-agile-dev-framework/`.

### 3.3 Étape 2 — Copier les Fichiers de l'Atelier

```powershell
# Définir le chemin de l'atelier (adaptez selon votre installation)
$Atelier = "C:\Users\[VOTRE_NOM]\AGENTIC_DEVELOPMENT_PROJECTS\projects\PRE-agentic-agile-dev-framework"
$Projet = "C:\Projets\mon-nouveau-projet"

# Copier les fichiers de configuration
Copy-Item "$Atelier\.roomodes" "$Projet\"
Copy-Item "$Atelier\.clinerules" "$Projet\"
Copy-Item "$Atelier\Modelfile" "$Projet\"          # Si Mode Ollama
Copy-Item "$Atelier\proxy.py" "$Projet\"           # Si Mode Gemini
Copy-Item "$Atelier\requirements.txt" "$Projet\"   # Si Mode Gemini

# Copier les dossiers
Copy-Item "$Atelier\scripts" "$Projet\" -Recurse
Copy-Item "$Atelier\prompts" "$Projet\" -Recurse
```

### 3.4 Étape 3 — Créer le `.gitignore`

Créez `.gitignore` à la racine du projet :

```
# Environnement Python
venv/
__pycache__/
*.pyc
*.pyo

# Clés API — JAMAIS dans Git
.env
*.env

# Logs
*.log

# OS
.DS_Store
Thumbs.db
```

### 3.5 Étape 4 — Initialiser la Memory Bank

```powershell
# Créer la structure Memory Bank
New-Item -Path "$Projet" -Name "memory-bank" -ItemType Directory
New-Item -Path "$Projet\memory-bank" -Name "projectBrief.md" -ItemType File
New-Item -Path "$Projet\memory-bank" -Name "productContext.md" -ItemType File
New-Item -Path "$Projet\memory-bank" -Name "systemPatterns.md" -ItemType File
New-Item -Path "$Projet\memory-bank" -Name "techContext.md" -ItemType File
New-Item -Path "$Projet\memory-bank" -Name "activeContext.md" -ItemType File
New-Item -Path "$Projet\memory-bank" -Name "progress.md" -ItemType File
New-Item -Path "$Projet\memory-bank" -Name "decisionLog.md" -ItemType File

# Créer le dossier des rapports QA
New-Item -Path "$Projet" -Name "docs" -ItemType Directory
New-Item -Path "$Projet\docs" -Name "qa" -ItemType Directory
New-Item -Path "$Projet\docs\qa" -Name ".gitkeep" -ItemType File
```

### 3.6 Étape 5 — Remplir `memory-bank/projectBrief.md`

C'est **la seule étape manuelle obligatoire** avant d'ouvrir Roo Code. Ouvrez `memory-bank/projectBrief.md` et remplissez :

```markdown
# Project Brief

## Vision du Projet
[2-3 phrases décrivant ce que ce projet fait et pour qui]

## Objectifs Principaux
1. [Objectif 1 — mesurable]
2. [Objectif 2 — mesurable]
3. [Objectif 3 — mesurable]

## Non-Goals (Ce que ce projet NE fait PAS)
- [Non-goal 1 — important pour éviter le scope creep]
- [Non-goal 2]

## Contraintes
- [Contrainte technique : ex: doit tourner sur Python 3.11+]
- [Contrainte métier : ex: doit respecter RGPD]

## Parties Prenantes
- Product Owner : [Votre nom]
- Utilisateurs cibles : [Description des utilisateurs finaux]
```

> **Pourquoi remplir cela manuellement ?** Roo Code ne peut pas inventer la vision de votre projet. C'est la seule information que vous devez fournir. Tout le reste (architecture, code, tests, documentation) sera généré par l'agent.

### 3.7 Étape 6 — Premier Commit

```powershell
cd "$Projet"
git add .
git commit -m "chore(init): initialisation projet avec atelier UADF v2.0"
```

### 3.8 Étape 7 — Ouvrir dans VS Code et Démarrer

```powershell
code "$Projet"
```

Dans VS Code :
1. Sélectionnez le mode **"Product Owner"** dans Roo Code
2. Envoyez : `Lis le projectBrief.md et crée les premières User Stories dans memory-bank/productContext.md`
3. L'agent lit la vision, crée les User Stories, commite automatiquement

**L'atelier est opérationnel sur votre nouveau projet.**

---

## 4. Déploiement sur une Base de Code Existante (Code Spaghetti)

### 4.1 Pourquoi c'est Différent

Avec un nouveau projet, la Memory Bank est vide et se remplit progressivement. Avec un projet existant, la Memory Bank doit être remplie **en premier** — avant tout refactoring — pour que l'agent comprenne ce qu'il va modifier.

**Risque sans cette étape :** L'agent refactorise sans comprendre les dépendances cachées du code spaghetti → il casse des fonctionnalités existantes.

### 4.2 Étape 1 — Ouvrir le Projet Existant

```powershell
cd "C:\Projets\mon-projet-legacy"

# Si Git n'est pas encore initialisé
git init
git add .
git commit -m "chore(init): état initial du code avant refactoring UADF"
```

> **Commiter l'état initial est critique.** Cela crée un point de retour sûr si le refactoring part dans une mauvaise direction.

### 4.3 Étape 2 — Copier les Fichiers de l'Atelier

Identique au cas "Nouveau Projet" (section 3.3) :

```powershell
$Atelier = "C:\Users\[VOTRE_NOM]\AGENTIC_DEVELOPMENT_PROJECTS\projects\PRE-agentic-agile-dev-framework"
$Projet = "C:\Projets\mon-projet-legacy"

Copy-Item "$Atelier\.roomodes" "$Projet\"
Copy-Item "$Atelier\.clinerules" "$Projet\"
Copy-Item "$Atelier\proxy.py" "$Projet\"
Copy-Item "$Atelier\requirements.txt" "$Projet\"
Copy-Item "$Atelier\scripts" "$Projet\" -Recurse
Copy-Item "$Atelier\prompts" "$Projet\" -Recurse
```

### 4.4 Étape 3 — Créer la Memory Bank (avec contexte existant)

```powershell
New-Item -Path "$Projet" -Name "memory-bank" -ItemType Directory
# Créer les 7 fichiers (identique à la section 3.5)
```

### 4.5 Étape 4 — Audit du Code Existant (CRITIQUE)

C'est **l'étape la plus importante** pour un projet existant. Elle n'existe pas pour un nouveau projet.

Ouvrez VS Code sur le projet, sélectionnez le mode **"Developer"** dans Roo Code, et envoyez :

```
Effectue un audit complet du code source dans ce projet.
Pour chaque point ci-dessous, documente tes découvertes dans le fichier indiqué :

1. Dans memory-bank/projectBrief.md :
   - Quelle est la fonction principale de ce projet ?
   - Quels sont les utilisateurs cibles apparents ?
   - Quelles sont les contraintes techniques visibles ?

2. Dans memory-bank/systemPatterns.md :
   - Quelle est l'architecture des dossiers ?
   - Quelles conventions de nommage sont utilisées (même si incohérentes) ?
   - Quels patterns techniques sont utilisés (même si mal implémentés) ?
   - Quels anti-patterns identifies-tu ? (couplage fort, duplication, etc.)
   - Quelles sont les dépendances critiques entre modules ?

3. Dans memory-bank/techContext.md :
   - Quel est le langage et la version ?
   - Quelles sont les dépendances (requirements.txt, package.json, etc.) ?
   - Quelles sont les commandes pour lancer et tester le projet ?
   - Y a-t-il des variables d'environnement requises ?

4. Dans memory-bank/decisionLog.md :
   - Documente les décisions d'architecture apparentes (même implicites)
   - Note les dettes techniques identifiées

Commite chaque fichier Memory Bank au fur et à mesure.
```

> **Pourquoi laisser l'agent faire l'audit ?** L'agent lit le code sans préjugés. Il identifie les patterns réels (pas ceux que vous pensez avoir implémentés). Il documente de manière structurée et versionnée. Vous pouvez corriger ses conclusions si nécessaire.

### 4.6 Étape 5 — Définir la Stratégie de Refactoring

Après l'audit, sélectionnez le mode **"Product Owner"** et envoyez :

```
Lis memory-bank/systemPatterns.md et memory-bank/projectBrief.md.
Sur la base des anti-patterns identifiés et de la vision du projet,
crée les User Stories de refactoring dans memory-bank/productContext.md.

Chaque User Story doit :
- Adresser un anti-pattern spécifique identifié dans l'audit
- Avoir des critères d'acceptation mesurables
- Être indépendante des autres (pour pouvoir être livrée séparément)
- Être ordonnée par priorité (les dépendances d'abord)
```

### 4.7 Étape 6 — Refactoring Guidé par les User Stories

Le refactoring se fait User Story par User Story, dans l'ordre défini par le Product Owner :

```
Pour chaque User Story :

1. Mode Developer :
   "Implémente la User Story US-XXX définie dans memory-bank/productContext.md.
    Lis d'abord systemPatterns.md pour respecter les conventions cibles.
    Commite après chaque modification significative."

2. Mode QA Engineer :
   "Teste les changements de la User Story US-XXX.
    Rédige le rapport dans docs/qa/test-US-XXX-[DATE].md."

3. Mode Scrum Master :
   "Mets à jour memory-bank/progress.md pour marquer US-XXX comme terminée.
    Identifie les impediments éventuels."
```

> **Pourquoi User Story par User Story ?** Le code spaghetti a des dépendances cachées. Refactoriser en petits incréments versionnés permet de détecter les régressions immédiatement et de revenir en arrière si nécessaire (`git revert`).

---

## 5. Ce qui Reste dans l'Atelier vs ce qui va dans le Projet

Cette table est la référence pour savoir où chaque fichier doit vivre :

| Fichier / Dossier | Reste dans l'Atelier | Va dans chaque Projet | Notes |
| :--- | :---: | :---: | :--- |
| `plans/DOC1/DOC2/DOC3/DOC4` | ✅ | ❌ | Documentation de l'atelier — pas du projet |
| `.roomodes` | ✅ (template) | ✅ (copie) | Copié, peut être adapté par projet |
| `.clinerules` | ✅ (template) | ✅ (copie) | Copié, peut être adapté par projet |
| `Modelfile` | ✅ (template) | ✅ (copie) | Copié si Mode Ollama utilisé |
| `proxy.py` | ✅ (template) | ✅ (copie) | Copié si Mode Gemini utilisé |
| `requirements.txt` | ✅ (template) | ✅ (copie) | Copié si Mode Gemini utilisé |
| `scripts/` | ✅ (template) | ✅ (copie) | Copié dans chaque projet |
| `prompts/SP-*.md` | ✅ (source de vérité) | ✅ (copie) | Copié — le projet a sa propre copie versionnée |
| `prompts/README.md` | ✅ (template) | ✅ (copie) | Copié |
| `memory-bank/` | ❌ | ✅ (spécifique) | Unique par projet — ne jamais copier d'un projet à l'autre |
| `src/` (code applicatif) | ❌ | ✅ (spécifique) | Unique par projet |
| `docs/qa/` | ❌ | ✅ (spécifique) | Rapports QA spécifiques au projet |

### 5.1 Pourquoi Copier les Fichiers plutôt que de les Référencer ?

Vous pourriez penser à utiliser des sous-modules Git ou des liens symboliques pour éviter la duplication. **Ne faites pas cela.** Voici pourquoi :

- **Indépendance :** Chaque projet doit pouvoir évoluer indépendamment. Si vous améliorez `.clinerules` dans l'atelier, vous choisissez quand et si vous mettez à jour chaque projet.
- **Traçabilité :** La version de `.clinerules` utilisée dans un projet est versionnée dans ce projet. Vous savez exactement quelle version de l'atelier était active quand un bug a été introduit.
- **Simplicité :** Pas de dépendances entre dépôts à gérer. Chaque projet est autonome.

---

## 6. Tableau de Bord des 3 Modes LLM par Cas d'Usage

| Mode | Cas d'Usage Recommandé | Avantage | Inconvénient |
| :--- | :--- | :--- | :--- |
| **Mode 1 — Ollama local** | Développement quotidien, tâches répétitives, code simple | Gratuit, hors ligne, 100% automatique | Plus lent que Claude, qualité variable sur tâches complexes |
| **Mode 2 — Proxy Gemini** | Tâches complexes quand Ollama est insuffisant, sans budget API | Gratuit, haute qualité | Copier-coller manuel à chaque requête |
| **Mode 3 — Claude API** | Refactoring complexe, architecture, décisions critiques | Meilleure qualité, 100% automatique | Payant à l'usage |

**Recommandation pratique :**
- Commencez en Mode 1 (Ollama) pour les tâches simples
- Basculez en Mode 3 (Claude) pour les décisions d'architecture et le refactoring complexe
- Utilisez le Mode 2 (Gemini) comme alternative gratuite au Mode 3 si le budget est une contrainte

---

## 7. Cycle de Vie d'un Projet avec l'Atelier UADF

```
PHASE SETUP (une seule fois par projet)
│
├── Copier les fichiers de l'atelier
├── Initialiser la Memory Bank
├── [Si existant] Audit du code
└── Premier commit

PHASE DÉVELOPPEMENT (itérative — un sprint = 1-2 semaines)
│
├── Mode Product Owner
│   └── Définir / affiner les User Stories du sprint
│
├── Mode Developer (répété pour chaque User Story)
│   ├── Lire Memory Bank (VÉRIFIER→CRÉER→LIRE→AGIR)
│   ├── Implémenter la User Story
│   ├── Mettre à jour Memory Bank
│   └── Commiter
│
├── Mode QA Engineer
│   ├── Tester les implémentations
│   ├── Rédiger les rapports dans docs/qa/
│   └── Commiter les rapports
│
└── Mode Scrum Master
    ├── Lire docs/qa/ pour l'état des tests
    ├── Mettre à jour memory-bank/progress.md
    └── Identifier les impediments

PHASE MAINTENANCE (continue)
│
├── Bugs → Mode QA Engineer (rapport) + Mode Developer (fix)
├── Nouvelles features → Mode Product Owner (US) + Mode Developer (impl)
└── Améliorations atelier → Mettre à jour PRE-agentic-agile-dev-framework/
```

---

## 8. Questions Fréquentes

### Q : Dois-je recréer le Gem Gemini pour chaque projet ?

**Non.** Le Gem Gemini "Roo Code Agent" est configuré une seule fois dans votre compte Google. Il est générique — il répond aux requêtes Roo Code quelle que soit la nature du projet. Vous n'avez pas à le recréer.

### Q : Dois-je réinstaller Ollama pour chaque projet ?

**Non.** Ollama est un daemon Windows qui tourne en arrière-plan. Le modèle `uadf-agent` est compilé une seule fois. Vous n'avez qu'à vous assurer qu'Ollama tourne (icône dans la zone de notification) avant d'ouvrir Roo Code.

### Q : Puis-je adapter `.roomodes` pour un projet spécifique ?

**Oui.** Par exemple, si un projet nécessite un persona "DevOps Engineer", vous pouvez l'ajouter dans la copie de `.roomodes` du projet. L'atelier n'est pas modifié. Si l'adaptation est utile pour tous les projets futurs, vous pouvez ensuite la reporter dans l'atelier.

### Q : Que faire si l'agent ne suit pas les règles `.clinerules` ?

1. Vérifiez que `.clinerules` est bien à la racine du projet (pas dans un sous-dossier)
2. Rechargez VS Code (`Ctrl+Shift+P` > "Developer: Reload Window")
3. Si le problème persiste, vérifiez que la règle est formulée de manière impérative et non suggestive

### Q : Comment mettre à jour un projet quand l'atelier évolue ?

1. Identifiez ce qui a changé dans l'atelier (consultez le `git log` de l'atelier)
2. Copiez manuellement les fichiers modifiés vers le projet
3. Commitez dans le projet avec un message explicite : `chore(uadf): mise à jour atelier v[X.Y] — [description du changement]`

### Q : Puis-je avoir plusieurs projets ouverts simultanément dans VS Code ?

**Oui**, via les workspaces VS Code. Chaque projet a ses propres `.roomodes` et `.clinerules`. Roo Code lit les fichiers du projet actuellement ouvert dans VS Code.

---

## 9. Checklist de Déploiement

### Pour un Nouveau Projet

- [ ] Dépôt Git créé en dehors du dossier de l'atelier
- [ ] Fichiers de l'atelier copiés (`.roomodes`, `.clinerules`, `proxy.py`, `scripts/`, `prompts/`)
- [ ] `.gitignore` créé (venv/, .env, __pycache__, *.log)
- [ ] Memory Bank initialisée (7 fichiers créés)
- [ ] `memory-bank/projectBrief.md` rempli avec la vision du projet
- [ ] `docs/qa/` créé avec `.gitkeep`
- [ ] Premier commit effectué
- [ ] VS Code ouvert sur le nouveau projet
- [ ] Mode Product Owner → premières User Stories créées

### Pour une Base de Code Existante

- [ ] État initial commité (`git commit -m "chore(init): état initial avant refactoring UADF"`)
- [ ] Fichiers de l'atelier copiés (identique au cas précédent)
- [ ] Memory Bank initialisée (7 fichiers créés)
- [ ] `docs/qa/` créé avec `.gitkeep`
- [ ] **Audit du code effectué par le Developer** → Memory Bank remplie
- [ ] `memory-bank/projectBrief.md` vérifié et corrigé si nécessaire
- [ ] `memory-bank/systemPatterns.md` contient les anti-patterns identifiés
- [ ] User Stories de refactoring créées par le Product Owner
- [ ] Refactoring démarré User Story par User Story

---

## Annexe A — Table des Références

| Réf. | Type | Titre / Identifiant | Description |
| :--- | :--- | :--- | :--- |
| [DOC1] | Document interne | `workbench/DOC1-PRD-Unified-Agentic-Framework.md` | Product Requirements Document v2.0 — définit les exigences REQ-xxx du système UADF |
| [DOC2] | Document interne | `workbench/DOC2-Architecture-Solution-Stack.md` | Architecture, Solution et Stack Technique v2.0 — justifie les choix techniques |
| [DOC3] | Document interne | `workbench/DOC3-Plan-Implementation-COMPLETE.md` | Plan d'Implémentation Séquentiel Complet v3.0 — guide d'installation de l'atelier (Phases 0–12) |
| [DOC4] | Document interne | `workbench/DOC4-Guide-Deploiement-Atelier.md` | Ce document — Guide de Déploiement de l'Atelier sur projets nouveaux et existants |
| [SP-001] | System Prompt | `template/prompts/SP-001-ollama-modelfile-system.md` | System prompt du Modelfile Ollama — copié dans le projet lors du déploiement |
| [SP-002] | System Prompt | `template/prompts/SP-002-clinerules-global.md` | Contenu canonique du fichier `.clinerules` — copié à la racine du projet |
| [SP-003] | System Prompt | `template/prompts/SP-003-persona-product-owner.md` | `roleDefinition` Product Owner — intégré dans `.roomodes` du projet |
| [SP-004] | System Prompt | `template/prompts/SP-004-persona-scrum-master.md` | `roleDefinition` Scrum Master — intégré dans `.roomodes` du projet |
| [SP-005] | System Prompt | `template/prompts/SP-005-persona-developer.md` | `roleDefinition` Developer — intégré dans `.roomodes` du projet |
| [SP-006] | System Prompt | `template/prompts/SP-006-persona-qa-engineer.md` | `roleDefinition` QA Engineer — intégré dans `.roomodes` du projet |
| [SP-007] | System Prompt | `template/prompts/SP-007-gem-gemini-roo-agent.md` | Instructions du Gem Gemini "Roo Code Agent" — déploiement manuel hors Git |
| [DEPLOY-SCRIPT] | Script PowerShell | `template/scripts/deploy-to-project.ps1` | Script de déploiement automatisé de l'atelier sur un projet (paramètres : `-ProjectPath`, `-Update`, `-DryRun`) |
| [WORKBENCH-VERSION] | Fichier de version | `template/.workbench-version` | Fichier copié dans chaque projet pour tracer la version de l'atelier déployée |
| [VERSION] | Fichier de version | `VERSION` (racine du workbench) | Version courante du workbench (format SemVer MAJOR.MINOR.PATCH) |
| [CHANGELOG] | Journal des modifications | `CHANGELOG.md` (racine du workbench) | Historique des versions du workbench avec procédure de mise à jour des projets |
| [GITHUB-WORKBENCH] | Dépôt GitHub | https://github.com/nghiaphan31/agentic-agile-workbench | Dépôt GitHub du workbench — source pour cloner et mettre à jour l'atelier |
| [SEMVER] | Standard | Semantic Versioning (semver.org) | Convention MAJOR.MINOR.PATCH utilisée pour versionner le workbench et les fichiers SP |

---

## Annexe B — Table des Abréviations

| Abréviation | Forme complète | Explication |
| :--- | :--- | :--- |
| **ADR** | Architecture Decision Record | Enregistrement horodaté d'une décision d'architecture. Stocké dans `memory-bank/decisionLog.md` du projet. |
| **API** | Application Programming Interface | Interface de programmation. Trois APIs dans l'UADF : Ollama REST (locale), OpenAI-compatible (proxy), Anthropic HTTPS (cloud). |
| **DA** | Décision d'Architecture | Identifiant des décisions dans DOC2 (DA-001 à DA-014). Référencé dans DOC3 pour justifier les choix. |
| **GEM** | Gem Gemini | Profil personnalisé Gemini Web avec system prompt permanent. "Roo Code Agent" contient SP-007. |
| **Git** | — (nom propre) | Système de contrôle de version distribué. Chaque projet déployé doit être un dépôt Git. |
| **JSON** | JavaScript Object Notation | Format de données structuré. Utilisé pour `.roomodes` (personas Agile). |
| **LAAW** | Local Agentic Agile Workflow | Blueprint mychen76 — source d'inspiration pour la Memory Bank et les personas Agile de l'UADF. |
| **LLM** | Large Language Model | Grand modèle de langage. Trois modes dans l'UADF : Qwen3-32B (local), Gemini Pro (cloud Google), Claude Sonnet (cloud Anthropic). |
| **PO** | Product Owner | Persona Agile — vision produit, User Stories, backlog. Mode `product-owner` dans `.roomodes`. |
| **PRD** | Product Requirements Document | Document d'exigences produit. DOC1 est le PRD de l'UADF. |
| **RBAC** | Role-Based Access Control | Contrôle d'accès par rôles. Chaque persona Agile a une matrice de permissions précise. |
| **REQ** | Requirement (Exigence) | Identifiant des exigences dans DOC1. |
| **SM** | Scrum Master | Persona Agile facilitateur pur — Memory Bank + Git uniquement, sans code ni tests. |
| **SP** | System Prompt | Fichier canonique du registre `template/prompts/` avec métadonnées YAML. |
| **SSE** | Server-Sent Events | Protocole de streaming HTTP serveur→client. Utilisé par le proxy pour retourner les réponses Gemini. |
| **UADF** | Unified Agentic Development Framework | Nom du système décrit dans les documents de ce workbench. |
| **VS Code** | Visual Studio Code | Éditeur de code Microsoft — environnement de développement principal de l'UADF. |
| **YAML** | YAML Ain't Markup Language | Format de sérialisation lisible. Utilisé pour les en-têtes des fichiers SP canoniques. |

---

## Annexe C — Glossaire

| Terme | Définition |
| :--- | :--- |
| **Atelier (Workbench)** | Ce dépôt (`agentic-agile-workbench`). Contient les outils, règles et processus réutilisables pour développer des projets applicatifs. S'oppose au "projet" qui contient le code métier. Analogie : atelier de menuiserie vs meubles fabriqués. |
| **Audit de code** | Étape obligatoire lors du déploiement sur une base de code existante. Le Developer lit le code source et remplit la Memory Bank (`systemPatterns.md`, `techContext.md`) avec les patterns, anti-patterns et dettes techniques identifiés. |
| **Balises XML Roo Code** | Syntaxe d'action de Roo Code : `<write_to_file>`, `<read_file>`, `<execute_command>`, `<attempt_completion>`, etc. Tout LLM connecté doit répondre avec ces balises. |
| **Code spaghetti** | Code source mal structuré, sans architecture claire, difficile à maintenir. Le déploiement de l'atelier sur un code spaghetti nécessite une étape d'audit préalable avant toute modification. |
| **Commit initial** | Premier commit Git d'un projet, effectué avant tout déploiement de l'atelier. Pour un projet existant : `git commit -m "chore(init): état initial avant refactoring UADF"`. Crée un point de retour sûr. |
| **Déploiement** | Copie des fichiers de l'atelier (`template/`) dans un projet applicatif. Peut être fait manuellement ou via `deploy-to-project.ps1`. |
| **deploy-to-project.ps1** | Script PowerShell dans `template/scripts/` qui automatise le déploiement. Paramètres : `-ProjectPath` (obligatoire), `-Update` (mise à jour), `-DryRun` (simulation sans écriture). |
| **Gem Gemini** | Profil Gemini Web avec system prompt permanent (SP-007). Créé une seule fois dans l'interface Gemini — partagé entre tous les projets utilisant le Mode Proxy. |
| **Memory Bank** | 7 fichiers Markdown dans `memory-bank/` du projet persistant le contexte entre sessions. Créés lors du déploiement, remplis progressivement par les personas Agile. |
| **Mise à jour de l'atelier** | Processus de propagation d'une nouvelle version du workbench vers les projets existants. Déclenché par `deploy-to-project.ps1 -Update` ou manuellement. Décrit dans `CHANGELOG.md`. |
| **Mode Cloud** | Roo Code → API Anthropic directe (`claude-sonnet-4-6`). Entièrement automatisé, payant à l'usage. |
| **Mode Local** | Roo Code → Ollama `localhost:11434` → Qwen3-32B. Gratuit, souverain, fonctionne hors ligne. |
| **Mode Proxy** | Roo Code → proxy FastAPI `localhost:8000` → presse-papiers → Gemini Web. Gratuit, nécessite copier-coller humain. |
| **Persona Agile** | Mode Roo Code simulant un rôle Scrum : Product Owner, Scrum Master, Developer, QA Engineer. Chaque persona a des permissions RBAC précises. |
| **Projet applicatif** | Dépôt Git contenant le code métier d'une application. Distinct de l'atelier. Reçoit les fichiers de l'atelier lors du déploiement. |
| **Séquence VÉRIFIER→CRÉER→LIRE→AGIR** | Protocole obligatoire au démarrage de chaque session Roo Code dans un projet déployé. Défini dans REGLE 1 de `.clinerules`. |
| **SemVer** | Semantic Versioning. Format MAJOR.MINOR.PATCH : MAJOR = rupture de compatibilité, MINOR = nouvelle fonctionnalité, PATCH = correction. Utilisé pour versionner le workbench (`VERSION`) et les fichiers SP. |
| **Template** | Répertoire `template/` du workbench contenant tous les fichiers à copier dans les projets applicatifs. Distinct de `workbench/` qui contient la documentation. |
| **`.workbench-version`** | Fichier créé à la racine de chaque projet déployé, contenant la version du workbench utilisée (ex: `2.0.0`). Permet de savoir quelle version de l'atelier est déployée dans chaque projet. |
