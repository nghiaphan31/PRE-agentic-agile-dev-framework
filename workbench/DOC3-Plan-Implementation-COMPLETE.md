# Document 3 : Plan d'Implémentation Séquentiel COMPLET
## Unified Agentic Development Framework (UADF) — Phases 0 à 12

**Nom du Projet :** Unified Agentic Development Framework (UADF)
**Version :** 3.0 — Document unique fusionné (phases 0-12 en continu)
**Date :** 2026-03-23
**Plateforme cible :** Windows 10/11 + Visual Studio Code
**Références :** DOC1-PRD-Unified-Agentic-Framework.md v2.0, DOC2-Architecture-Solution-Stack.md v2.0

---

## Prérequis Système

Avant de commencer, vérifiez que votre machine dispose de :
- Windows 10/11 (64-bit)
- Google Chrome installé avec un compte Google actif
- Au moins 16 Go de RAM (32 Go recommandés pour le modèle 32B)
- Au moins 30 Go d'espace disque libre (modèles + projet)
- Carte graphique NVIDIA avec 8+ Go de VRAM (recommandé) OU CPU suffisant
- Connexion Internet pour les téléchargements initiaux
- Git installé (`git --version` doit répondre dans PowerShell)
- Python 3.10+ installé (`python --version` doit répondre dans PowerShell)

---

## Vue d'Ensemble des Phases

```
PHASE 0  : Base Saine — Nettoyage et Réinstallation VS Code + Roo Code
    |
    v
PHASE 1  : Infrastructure Système (Ollama + Modèles LLM)
    |
    v
PHASE 2  : Création du Dépôt Git du Projet UADF
    |
    v
PHASE 3  : Modelfile et Modèle Personnalisé Ollama
    |
    v
PHASE 4  : Personas Agile (.roomodes) avec Règles Git
    |
    v
PHASE 5  : Memory Bank (.clinerules avec 6 Règles + 7 fichiers .md)
    |
    v
PHASE 6  : Proxy Gemini Chrome (proxy.py v2.0 avec SSE)
    |
    v
PHASE 7  : Configuration Gemini Chrome (Gem dédié)
    |
    v
PHASE 8  : Configuration Roo Code (Commutateur 3 modes LLM)
    |
    v
PHASE 9  : Tests de Validation End-to-End
    |
    v
PHASE 10 : Mode Cloud Direct — API Anthropic Claude Sonnet
    |
    v
PHASE 11 : Registre Central des System Prompts (prompts/)
    |
    v
PHASE 12 : Vérification Automatique de Cohérence des Prompts
```

### Tableau de Correspondance Phases / Exigences PRD

| Phase | Description | Exigences PRD |
| :--- | :--- | :--- |
| Phase 0 | Base saine VS Code + Roo Code | REQ-000 |
| Phase 1 | Installation Ollama + modèles | REQ-1.0, REQ-1.1, REQ-1.2 |
| Phase 2 | Dépôt Git + .gitignore complet | REQ-000, REQ-4.1, REQ-4.5 |
| Phase 3 | Modelfile personnalisé + commit | REQ-1.2, REQ-1.3 |
| Phase 4 | .roomodes personas Agile + règles Git | REQ-3.1, REQ-3.2, REQ-3.3, REQ-3.4 |
| Phase 5 | .clinerules (6 règles) + 7 fichiers Memory Bank | REQ-4.1 à REQ-4.5 |
| Phase 6 | proxy.py v2.0 (SSE + JSON) + scripts/ | REQ-2.1.1 à REQ-2.4.4 |
| Phase 7 | Gem Gemini Chrome + doc Memory Bank | REQ-5.1, REQ-5.2, REQ-5.3 |
| Phase 8 | Roo Code commutateur 3 modes LLM | REQ-2.0, REQ-6.0 |
| Phase 9 | Tests end-to-end (dont test Git auto-portant) | REQ-000 |
| Phase 10 | API Anthropic Claude Sonnet (claude-sonnet-4-6) | REQ-6.1, REQ-6.2, REQ-6.3, REQ-6.4 |
| Phase 11 | Registre central des prompts (prompts/) | REQ-7.1, REQ-7.2, REQ-7.3, REQ-7.4, REQ-7.5 |
| Phase 12 | Vérification automatique cohérence prompts (script + hook pre-commit) | REQ-8.1, REQ-8.2, REQ-8.3, REQ-8.4 |

---

## PHASE 0 : Base Saine — Nettoyage et Réinstallation VS Code + Roo Code

**Objectif :** Partir d'un environnement VS Code et Roo Code propre, sans pollution de configurations précédentes.
**Exigences adressées :** REQ-000

> **Pourquoi cette phase est critique :** Un environnement VS Code "pollué" peut causer des comportements imprévisibles de Roo Code : paramètres API résiduels, extensions conflictuelles, cache corrompu, ou anciennes versions de Roo Code (Cline) coexistant avec la nouvelle. Cette phase garantit une ardoise vierge.

### Étape 0.1 — Sauvegarder les Paramètres VS Code Actuels (Optionnel)

```powershell
$vscodeSettings = "$env:APPDATA\Code\User"
$backup = "$env:USERPROFILE\Desktop\vscode-backup-$(Get-Date -Format 'yyyyMMdd')"
Copy-Item -Path $vscodeSettings -Destination $backup -Recurse
Write-Host "Sauvegarde créée : $backup"
```

### Étape 0.2 — Désinstaller Toutes les Versions de Roo Code / Cline

1. Dans VS Code, ouvrez le panneau Extensions (`Ctrl+Shift+X`)
2. Recherchez **"Roo"** dans la barre de recherche
3. Pour chaque extension trouvée (Roo Code, Roo Cline, Cline, etc.) : cliquez sur l'engrenage → **"Uninstall"**
4. Recherchez **"Cline"** et répétez l'opération
5. Rechargez VS Code (`Ctrl+Shift+P` > "Developer: Reload Window")

### Étape 0.3 — Nettoyer le Cache et les Données de Roo Code

Fermez VS Code complètement, puis dans PowerShell :

```powershell
$extensionsPath = "$env:USERPROFILE\.vscode\extensions"
$globalStoragePath = "$env:APPDATA\Code\User\globalStorage"

Write-Host "=== Extensions Roo/Cline trouvées ==="
Get-ChildItem $extensionsPath | Where-Object { $_.Name -match "roo|cline|saoud" } | Select-Object Name

Write-Host "=== Données globales Roo/Cline trouvées ==="
Get-ChildItem $globalStoragePath | Where-Object { $_.Name -match "roo|cline|saoud" } | Select-Object Name
```

Supprimez les dossiers identifiés :

```powershell
Get-ChildItem $extensionsPath | Where-Object { $_.Name -match "roo|cline|saoud" } | Remove-Item -Recurse -Force
Get-ChildItem $globalStoragePath | Where-Object { $_.Name -match "roo|cline|saoud" } | Remove-Item -Recurse -Force
Write-Host "Nettoyage terminé."
```

### Étape 0.4 — Nettoyer les Paramètres VS Code Résiduels

```powershell
$settingsFile = "$env:APPDATA\Code\User\settings.json"
if (Test-Path $settingsFile) {
    Write-Host "=== Entrées Roo/Cline dans settings.json ==="
    Get-Content $settingsFile | Select-String -Pattern "roo|cline|ollama|anthropic" -CaseSensitive:$false
}
```

Si des entrées résiduelles sont trouvées, ouvrez `settings.json` dans un éditeur de texte et supprimez les sections concernées.

### Étape 0.5 — Réinstaller VS Code (Si Nécessaire)

Si VS Code lui-même est instable :
1. **Paramètres Windows > Applications** → recherchez "Visual Studio Code" → **Désinstaller**
2. Supprimez les dossiers résiduels :
   ```powershell
   Remove-Item "$env:APPDATA\Code" -Recurse -Force -ErrorAction SilentlyContinue
   Remove-Item "$env:USERPROFILE\.vscode" -Recurse -Force -ErrorAction SilentlyContinue
   ```
3. Téléchargez la dernière version stable sur **https://code.visualstudio.com**
4. Installez avec les options par défaut

### Étape 0.6 — Installer la Dernière Version de Roo Code

1. Ouvrez VS Code
2. Ouvrez le panneau Extensions (`Ctrl+Shift+X`)
3. Recherchez **"Roo Code"**
4. Vérifiez que l'éditeur est **"Roo Coder"** (l'éditeur officiel)
5. Cliquez sur **"Install"**

**Critère de validation :** L'icône Roo Code apparaît dans la barre latérale gauche de VS Code.

### Étape 0.7 — Vérifier l'État Propre de Roo Code

1. Cliquez sur l'icône Roo Code dans la barre latérale
2. Le panneau s'ouvre sans erreur
3. Dans les paramètres Roo Code (engrenage) : aucune clé API ne doit être pré-remplie
4. La liste des modes contient uniquement les modes par défaut (Code, Architect, Ask, Debug, Orchestrator)

> **Si des modes personnalisés ou des clés API apparaissent déjà :** Répétez les étapes 0.3 et 0.4.

### Étape 0.8 — Vérifier Git et Python

```powershell
git --version
python --version
pip --version
```

Chaque commande doit retourner un numéro de version. Si l'une échoue :
- **Git :** https://git-scm.com/download/win
- **Python :** https://python.org/downloads (cochez "Add to PATH" lors de l'installation)

---

## PHASE 1 : Infrastructure Système — Installation d'Ollama et des Modèles

**Objectif :** Installer le moteur d'inférence local et télécharger les modèles LLM.
**Exigences adressées :** REQ-1.0, REQ-1.1, REQ-1.2

### Étape 1.1 — Installer Ollama pour Windows

1. Allez sur **https://ollama.com/download**
2. Cliquez sur **"Download for Windows"** et téléchargez l'installateur `.exe`
3. Exécutez l'installateur (installation standard)
4. Après installation, Ollama démarre automatiquement en tâche de fond
5. Vérifiez que l'icône Ollama apparaît dans la zone de notification Windows (coin bas-droit)

**Critère de validation :**
```powershell
ollama --version
```
Résultat attendu : `ollama version 0.x.x`

### Étape 1.2 — Télécharger le Modèle Principal (Qwen3 32B optimisé Roo Code)

```powershell
ollama pull mychen76/qwen3_cline_roocode:32b
```

> **Note :** Ce téléchargement peut prendre 15 à 45 minutes. Le modèle pèse environ 20 Go.

**Critère de validation :**
```powershell
ollama list
```
Vous devez voir `mychen76/qwen3_cline_roocode:32b` dans la liste.

### Étape 1.3 — Télécharger le Modèle Secondaire (Qwen3 7B pour Boomerang Tasks)

```powershell
ollama pull qwen3:7b
```

**Critère de validation :** `ollama list` affiche `qwen3:7b`.

### Étape 1.4 — Vérifier que l'API Ollama est Accessible

```powershell
Invoke-WebRequest -Uri "http://localhost:11434/api/tags" -Method GET | Select-Object -ExpandProperty Content
```

Vous devez voir une réponse JSON listant vos modèles. Si erreur de connexion, relancez Ollama depuis le menu Démarrer.

---

## PHASE 2 : Création du Dépôt Git du Projet UADF

**Objectif :** Créer le dépôt Git qui versionnera TOUT : code, scripts, prompts, configurations, Memory Bank.
**Exigences adressées :** REQ-000, REQ-4.1, REQ-4.5

> **Principe fondamental :** Dans UADF, Git ne versionne pas seulement le code applicatif. Il versionne l'intégralité de l'intelligence du projet : les prompts système (`.clinerules`, `.roomodes`), les scripts (`proxy.py`), la configuration (`Modelfile`), et la mémoire persistante (`memory-bank/`). Chaque modification significative de l'un de ces éléments doit faire l'objet d'un commit Git avec un message descriptif.

### Étape 2.1 — Créer le Dossier du Projet

```powershell
mkdir C:\Users\$env:USERNAME\Projects\mon-projet-uadf
cd C:\Users\$env:USERNAME\Projects\mon-projet-uadf
code .
```

### Étape 2.2 — Initialiser Git

Dans le terminal VS Code (`Ctrl+`` `) :
```powershell
git init
git config user.name "Votre Nom"
git config user.email "votre@email.com"
```

### Étape 2.3 — Créer le Fichier `.gitignore` Complet

```powershell
New-Item -Name ".gitignore" -ItemType File
```

Ouvrez `.gitignore` et collez :
```gitignore
# Environnement Python (jamais versionné)
venv/
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.egg-info/
dist/
build/

# Variables d'environnement (contient des clés API — JAMAIS versionné)
.env
.env.local
.env.*.local

# Logs
*.log
logs/

# Fichiers temporaires Windows
Thumbs.db
Desktop.ini
*.tmp

# Fichiers VS Code locaux (paramètres personnels, pas de projet)
.vscode/settings.json
.vscode/launch.json
.vscode/tasks.json

# IMPORTANT : Les fichiers suivants DOIVENT être versionnés (ne pas les ajouter ici)
# .roomodes        -> Versionné (personas Agile)
# .clinerules      -> Versionné (règles Memory Bank + Git)
# Modelfile        -> Versionné (config modèle Ollama)
# proxy.py         -> Versionné (serveur proxy Gemini)
# memory-bank/     -> Versionné (mémoire persistante)
# requirements.txt -> Versionné (dépendances Python)
# prompts/         -> Versionné (registre central des prompts)
# scripts/         -> Versionné (scripts PowerShell)
```

Sauvegardez (`Ctrl+S`).

### Étape 2.4 — Créer la Structure de Dossiers du Projet

```powershell
mkdir memory-bank
mkdir docs
mkdir docs\qa
mkdir scripts
mkdir prompts
```

### Étape 2.5 — Premier Commit : Squelette du Projet

```powershell
git add .gitignore
git commit -m "chore: initialisation dépôt UADF - squelette projet et .gitignore"
```

**Critère de validation :** `git log --oneline` affiche le commit initial.

---

## PHASE 3 : Modelfile et Modèle Personnalisé Ollama

**Objectif :** Créer un modèle Ollama personnalisé avec les paramètres de déterminisme et la fenêtre de contexte étendue.
**Exigences adressées :** REQ-1.2, REQ-1.3

### Étape 3.1 — Créer le Fichier `Modelfile`

```powershell
New-Item -Name "Modelfile" -ItemType File
```

Ouvrez `Modelfile` dans VS Code et collez exactement :
```dockerfile
FROM mychen76/qwen3_cline_roocode:32b

# Parametres de determinisme (anti-hallucination) — REQ-1.3
PARAMETER temperature 0.15
PARAMETER min_p 0.03
PARAMETER top_p 0.95
PARAMETER repeat_penalty 1.1

# Fenetre de contexte maximale (128K tokens) — REQ-1.2
PARAMETER num_ctx 131072

# Parametres de performance GPU
PARAMETER num_gpu 99
PARAMETER num_thread 8

SYSTEM """
Tu es un agent de developpement logiciel expert integre dans Roo Code.
Tu dois toujours utiliser les balises XML de Roo Code pour tes actions.
Tu dois toujours lire la Memory Bank (memory-bank/) avant d'agir.
Tu dois toujours mettre a jour la Memory Bank apres chaque tache.
Apres chaque tache significative, tu dois effectuer un commit Git avec un message descriptif.
"""
```

Sauvegardez (`Ctrl+S`).

### Étape 3.2 — Compiler le Modèle Personnalisé

```powershell
ollama create uadf-agent -f Modelfile
```

**Critère de validation :**
```powershell
ollama show uadf-agent --modelfile
```
Doit afficher `PARAMETER num_ctx 131072` et `PARAMETER temperature 0.15`.

### Étape 3.3 — Tester le Modèle

```powershell
ollama run uadf-agent "Dis bonjour en une phrase."
```

Tapez `/bye` pour quitter.

### Étape 3.4 — Versionner le Modelfile

```powershell
git add Modelfile
git commit -m "feat: ajout Modelfile Ollama (uadf-agent, T=0.15, ctx=131072)"
```

---

## PHASE 4 : Personas Agile — Fichier `.roomodes` avec Règles Git

**Objectif :** Créer les 4 personas Agile avec leurs permissions RBAC et l'obligation de versionnement Git.
**Exigences adressées :** REQ-3.1, REQ-3.2, REQ-3.3, REQ-3.4

> **Pourquoi inscrire Git dans les roleDefinitions ?** Le Developer et le Scrum Master ont accès au terminal. En inscrivant l'obligation de commit Git dans leur `roleDefinition`, on garantit que ce comportement est auto-portant : même si `.clinerules` n'est pas lu, le persona lui-même sait qu'il doit versionner. C'est une défense en profondeur.

> **Scrum Master — facilitateur pur (REQ-3.4) :** Le Scrum Master peut lire tous les fichiers (y compris `docs/qa/`), écrire dans `memory-bank/` et `docs/`, et exécuter uniquement les commandes Git. Il ne peut pas exécuter de commandes de test ni modifier le code source. Pour connaître l'état des tests, il lit les rapports QA dans `docs/qa/` produits par le QA Engineer.

### Étape 4.1 — Créer le Fichier `.roomodes`

```powershell
New-Item -Name ".roomodes" -ItemType File
```

### Étape 4.2 — Insérer la Configuration des Personas

Ouvrez `.roomodes` dans VS Code et collez le contenu JSON suivant :

```json
{
  "customModes": [
    {
      "slug": "product-owner",
      "name": "Product Owner",
      "roleDefinition": "Tu es le Product Owner de l'équipe Scrum. Ton rôle est de définir et prioriser le backlog produit. Tu rédiges les User Stories au format 'En tant que [persona], je veux [action] afin de [bénéfice]'. Tu maintiens le fichier memory-bank/productContext.md à jour. Tu ne touches JAMAIS au code source ni aux scripts. Si on te demande d'écrire du code, tu refuses poliment et suggères de basculer vers le mode Developer.",
      "groups": [
        "read",
        ["edit", { "fileRegex": "memory-bank/productContext\\.md|docs/.*\\.md|user-stories.*\\.md", "description": "Documentation produit uniquement" }]
      ],
      "source": "project"
    },
    {
      "slug": "scrum-master",
      "name": "Scrum Master",
      "roleDefinition": "Tu es le Scrum Master de l'équipe Scrum. Tu facilites les cérémonies Agile (Sprint Planning, Daily, Review, Rétrospective). Tu identifies et supprimes les impediments. Tu maintiens memory-bank/progress.md et memory-bank/activeContext.md à jour. Tu ne touches pas au code source applicatif. Tu peux lire tous les fichiers du projet, y compris les rapports QA dans docs/qa/. Pour connaître l'état des tests, tu lis les rapports produits par le QA Engineer dans docs/qa/ — tu n'exécutes pas de commandes de test toi-même. RÈGLE GIT OBLIGATOIRE : Après chaque mise à jour de la Memory Bank, tu DOIS exécuter un commit Git avec le message format 'docs(memory): [description de la mise à jour]'.",
      "groups": [
        "read",
        ["edit", { "fileRegex": "memory-bank/.*\\.md|docs/.*\\.md", "description": "Memory Bank et documentation" }],
        ["command", { "allowedCommands": ["git add", "git commit", "git status", "git log"], "description": "Commandes Git pour versionner la Memory Bank" }]
      ],
      "source": "project"
    },
    {
      "slug": "developer",
      "name": "Developer",
      "roleDefinition": "Tu es le Developer senior de l'équipe Scrum. Tu implémentes les User Stories du backlog. Tu écris du code propre, testé et documenté. PROTOCOLE OBLIGATOIRE EN 3 ÉTAPES : (1) AVANT de coder : lire memory-bank/activeContext.md, memory-bank/systemPatterns.md et memory-bank/techContext.md. (2) APRÈS avoir codé : mettre à jour memory-bank/activeContext.md et memory-bank/progress.md. (3) AVANT de clôturer la tâche : exécuter 'git add .' puis 'git commit -m [message descriptif au format conventionnel]'. Le versionnement Git est NON NÉGOCIABLE : tout fichier créé ou modifié doit être commité avant attempt_completion.",
      "groups": [
        "read",
        "edit",
        "browser",
        "command",
        "mcp"
      ],
      "source": "project"
    },
    {
      "slug": "qa-engineer",
      "name": "QA Engineer",
      "roleDefinition": "Tu es le QA Engineer de l'équipe Scrum. Tu conçois et exécutes les plans de test. Tu analyses les logs et rapports de test. Tu rédiges les rapports de bugs avec reproduction steps clairs dans docs/qa/. Tu ne modifies JAMAIS le code source applicatif. Tu peux exécuter des commandes de test (npm test, pytest, etc.) et lire tous les fichiers.",
      "groups": [
        "read",
        ["edit", { "fileRegex": "docs/qa/.*\\.md|memory-bank/progress\\.md", "description": "Rapports QA et suivi progression" }],
        ["command", { "allowedCommands": ["npm test", "npm run test", "pytest", "python -m pytest", "dotnet test", "go test", "git status", "git log"], "description": "Commandes de test et consultation Git" }]
      ],
      "source": "project"
    }
  ]
}
```

Sauvegardez (`Ctrl+S`).

### Étape 4.3 — Vérifier le Chargement des Modes dans Roo Code

1. Cliquez sur l'icône Roo Code dans la barre latérale
2. Cliquez sur le sélecteur de mode en haut du panneau
3. Vous devez voir : "Product Owner", "Scrum Master", "Developer", "QA Engineer"

> **Si les modes n'apparaissent pas :** Rechargez VS Code (`Ctrl+Shift+P` > "Developer: Reload Window").

### Étape 4.4 — Versionner `.roomodes`

```powershell
git add .roomodes
git commit -m "feat(agile): ajout personas Agile RBAC avec règles Git intégrées (.roomodes)"
```

**Critère de validation RBAC :**
- Mode Product Owner → demandez "Écris du code Python" → doit refuser
- Mode Scrum Master → demandez "Lance pytest" → doit refuser
- Mode QA Engineer → demandez "Modifie src/main.py" → doit refuser

---

## PHASE 5 : Memory Bank — `.clinerules` avec 6 Règles + 7 Fichiers Markdown

**Objectif :** Créer le système de mémoire persistante (7 fichiers Markdown) et les directives globales (`.clinerules`) qui forcent l'agent à suivre la séquence VÉRIFIER→CRÉER→LIRE→AGIR à chaque session.
**Exigences adressées :** REQ-4.1, REQ-4.2, REQ-4.3, REQ-4.4, REQ-4.5, REQ-7.3
**Décisions d'architecture :** DA-002, DA-003

---

### Étape 5.1 — Créer le Fichier `.clinerules`

Créez le fichier `.clinerules` à la racine du projet :

```powershell
New-Item -Path "." -Name ".clinerules" -ItemType File
```

Ouvrez `.clinerules` et collez **exactement** ce contenu (source canonique : [`SP-002-clinerules-global.md`](../prompts/SP-002-clinerules-global.md)) :

```markdown
# PROTOCOLE UADF — DIRECTIVES IMPERATIVES (TOUTES SESSIONS, TOUS MODES)

## REGLE 1 : LECTURE OBLIGATOIRE AU DEMARRAGE DE CHAQUE SESSION
Avant toute action, tu DOIS exécuter la séquence suivante dans cet ordre exact :

1. VÉRIFIER : Est-ce que memory-bank/activeContext.md existe ?
   - Si NON → passer à l'étape CRÉER
   - Si OUI → passer à l'étape LIRE
2. CRÉER (si absent) : Créer immédiatement memory-bank/activeContext.md ET memory-bank/progress.md
   en utilisant les templates définis en bas de ce fichier.
3. LIRE : Lire memory-bank/activeContext.md puis memory-bank/progress.md
4. AGIR : Traiter la demande de l'utilisateur

Cette séquence VÉRIFIER→CRÉER→LIRE→AGIR est NON NÉGOCIABLE et s'applique à TOUTES les sessions.

## REGLE 2 : ECRITURE OBLIGATOIRE A LA CLOTURE DE CHAQUE TACHE
Avant de cloturer toute tache (avant attempt_completion), tu DOIS mettre a jour :
1. memory-bank/activeContext.md  (nouvel etat, prochaine action)
2. memory-bank/progress.md       (cocher les features terminees)

Si une decision d'architecture a ete prise durant la session :
3. memory-bank/decisionLog.md    (ADR avec date, contexte, decision, consequences)

## REGLE 3 : LECTURE CONTEXTUELLE SELON LA TACHE
- Avant de modifier l'architecture : lire memory-bank/systemPatterns.md
- Avant d'executer des commandes build/test : lire memory-bank/techContext.md
- En debut de sprint ou de nouvelle feature : lire memory-bank/productContext.md

## REGLE 4 : AUCUNE EXCEPTION AUX REGLES 1-3
Ces regles s'appliquent a TOUS les modes et a TOUTES les sessions, sans exception.

## REGLE 5 : VERSIONNEMENT GIT OBLIGATOIRE ET AUTO-PORTANT
Cette regle s'applique a tous les modes ayant acces au terminal (developer, scrum-master).

### 5.1 — Ce qui DOIT etre versionne
TOUT doit etre versionne sous Git, sans exception :
- Le code source applicatif (src/, app/, etc.)
- Les scripts systeme (proxy.py, scripts/start-proxy.ps1, etc.)
- Les fichiers de configuration (Modelfile, .roomodes, .clinerules, requirements.txt)
- La Memory Bank (memory-bank/*.md)
- Les prompts systeme (prompts/SP-*.md et prompts/README.md)
- Les documents de plans et d'architecture (plans/*.md)
- Les rapports QA (docs/qa/*.md)

### 5.2 — Quand commiter
Tu DOIS executer un commit Git dans les situations suivantes :
- Apres avoir cree ou modifie un fichier de code
- Apres avoir mis a jour la Memory Bank
- Apres avoir modifie .roomodes, .clinerules, Modelfile ou tout fichier de prompts/
- Apres avoir modifie proxy.py ou tout autre script
- Avant de cloturer une tache (avant attempt_completion)

### 5.3 — Format des messages de commit (Conventional Commits)
Tu DOIS utiliser le format Conventional Commits :
- feat(scope): description     -> Nouvelle fonctionnalite
- fix(scope): description      -> Correction de bug
- docs(memory): description    -> Mise a jour Memory Bank
- docs(plans): description     -> Mise a jour documentation
- chore(config): description   -> Modification de configuration
- chore(prompts): description  -> Modification d'un system prompt
- refactor(scope): description -> Refactorisation sans changement fonctionnel
- test(scope): description     -> Ajout ou modification de tests

### 5.4 — Commandes Git a utiliser
  git add .
  git commit -m "type(scope): description concise"

### 5.5 — Ce qui NE doit PAS etre versionne
- Le dossier venv/ (environnement Python local)
- Les fichiers .env (cles API — JAMAIS dans Git)
- Les fichiers __pycache__/ et *.pyc
- Les logs (*.log)

## REGLE 6 : COHERENCE DU REGISTRE DES PROMPTS
Cette regle s'applique au mode developer et scrum-master.

### 6.1 — Avant tout commit touchant un artefact lie a un prompt
Si tu modifies l'un des fichiers suivants : proxy.py, .roomodes, .clinerules, Modelfile
tu DOIS verifier si le changement impacte un system prompt dans prompts/.

### 6.2 — Procedure de verification
1. Lire prompts/README.md pour identifier le prompt concerne
2. Ouvrir le fichier SP-XXX correspondant dans prompts/
3. Si le contenu du prompt doit changer : modifier SP-XXX, incrementer sa version
4. Si SP-007 (Gem Gemini) est impacte : ajouter un avertissement dans le commit :
   "DEPLOIEMENT MANUEL REQUIS : mettre a jour le Gem Gemini avec SP-007"
5. Inclure les fichiers prompts/ modifies dans le meme commit que les fichiers cibles

### 6.3 — Exemple de commit avec mise a jour de prompt
  git add proxy.py prompts/SP-007-gem-gemini-roo-agent.md
  git commit -m "chore(prompts): mise a jour SP-007 suite modification proxy.py - DEPLOIEMENT MANUEL REQUIS"

## TEMPLATES DE FICHIERS MEMORY BANK

### Template activeContext.md
---
# Contexte Actif
**Date de mise a jour :** [DATE]
**Mode actif :** [MODE]
**Backend LLM actif :** [Ollama uadf-agent | Proxy Gemini | Claude Sonnet API]

## Tache en cours
[Description de la tache en cours]

## Dernier resultat
[Resultat de la derniere action]

## Prochain(s) pas
- [ ] [Prochaine action immediate]

## Blocages / Questions ouvertes
[Aucun | Description du blocage]

## Dernier commit Git
[Hash court et message du dernier commit]
---

### Template progress.md
---
# Progression du Projet
**Derniere mise a jour :** [DATE]

## Infrastructure UADF
- [ ] Phase 0 : Base saine VS Code + Roo Code
- [ ] Phase 1 : Ollama + modeles
- [ ] Phase 2 : Depot Git initialise
- [ ] Phase 3 : Modelfile personnalise
- [ ] Phase 4 : .roomodes (personas Agile)
- [ ] Phase 5 : Memory Bank + .clinerules
- [ ] Phase 6 : proxy.py (Gemini Chrome)
- [ ] Phase 7 : Gem Gemini configure
- [ ] Phase 8 : Roo Code commutateur 3 modes
- [ ] Phase 9 : Tests end-to-end valides
- [ ] Phase 10 : API Anthropic Claude configure
- [ ] Phase 11 : Registre prompts/ initialise
- [ ] Phase 12 : check-prompts-sync.ps1 + hook pre-commit

## Features Produit

### Epic 1 : [A definir]
- [ ] [Feature a definir]

## Legende
- [ ] A faire  |  [-] En cours  |  [x] Termine
---
```

Sauvegardez (Ctrl+S).

> **Pourquoi VÉRIFIER→CRÉER→LIRE→AGIR ?** Sans la vérification préalable, l'agent tenterait de lire un fichier inexistant et échouerait silencieusement. La séquence garantit que la Memory Bank est toujours initialisée avant d'être lue.

---

### Étape 5.2 — Créer la Structure de la Memory Bank

```powershell
# Créer le dossier memory-bank et les 7 fichiers
New-Item -Path "." -Name "memory-bank" -ItemType Directory
New-Item -Path "memory-bank" -Name "projectBrief.md" -ItemType File
New-Item -Path "memory-bank" -Name "productContext.md" -ItemType File
New-Item -Path "memory-bank" -Name "systemPatterns.md" -ItemType File
New-Item -Path "memory-bank" -Name "techContext.md" -ItemType File
New-Item -Path "memory-bank" -Name "activeContext.md" -ItemType File
New-Item -Path "memory-bank" -Name "progress.md" -ItemType File
New-Item -Path "memory-bank" -Name "decisionLog.md" -ItemType File
```

---

### Étape 5.3 — Remplir `memory-bank/projectBrief.md`

Ouvrez `memory-bank/projectBrief.md` et collez :

```markdown
# Project Brief

## Vision du Projet
[Décrivez ici la vision globale de votre projet en 2-3 phrases]

## Objectifs Principaux
1. [Objectif 1]
2. [Objectif 2]
3. [Objectif 3]

## Non-Goals (Ce que ce projet NE fait PAS)
- [Non-goal 1]
- [Non-goal 2]

## Contraintes
- [Contrainte technique ou métier]

## Parties Prenantes
- Product Owner : [Nom]
- Utilisateurs cibles : [Description]
```

> **Note :** Ce fichier est rempli une seule fois en début de projet. Il ne change que si la vision du projet change fondamentalement.

---

### Étape 5.4 — Remplir `memory-bank/productContext.md`

Ouvrez `memory-bank/productContext.md` et collez :

```markdown
# Product Context

## User Stories du Sprint Courant

### Sprint [N] — [Dates]

#### US-001 : [Titre]
**En tant que** [persona]
**Je veux** [action]
**Afin de** [bénéfice]
**Critères d'acceptation :**
- [ ] [Critère 1]
- [ ] [Critère 2]

## Backlog (Prochains Sprints)
- [ ] [Feature à venir 1]
- [ ] [Feature à venir 2]
```

---

### Étape 5.5 — Remplir `memory-bank/systemPatterns.md`

Ouvrez `memory-bank/systemPatterns.md` et collez :

```markdown
# System Patterns

## Architecture des Dossiers
[Collez ici l'arborescence de votre projet]

## Conventions de Nommage
- Fichiers : [convention, ex: kebab-case]
- Variables : [convention, ex: camelCase]
- Classes : [convention, ex: PascalCase]
- Constantes : [convention, ex: UPPER_SNAKE_CASE]

## Patterns Techniques Adoptés
- [Pattern 1 : ex: Repository Pattern pour l'accès aux données]
- [Pattern 2 : ex: Service Layer pour la logique métier]

## Anti-Patterns à Éviter
- [Anti-pattern 1]
```

---

### Étape 5.6 — Remplir `memory-bank/techContext.md`

Ouvrez `memory-bank/techContext.md` et collez :

```markdown
# Tech Context

## Stack Technique
- Langage principal : [ex: Python 3.11]
- Framework : [ex: FastAPI 0.110]
- Base de données : [ex: SQLite / PostgreSQL]
- Tests : [ex: pytest]

## Commandes Essentielles
```bash
pip install -r requirements.txt
python main.py
pytest tests/
```

## Variables d'Environnement Requises
- `[VAR_NAME]` : [Description et valeur par défaut]

## Dépendances Critiques et Versions
| Package | Version | Raison |
| :--- | :--- | :--- |
| [package] | [version] | [raison] |

## Configuration des Backends LLM (Commutateur UADF)

### Mode 1 : Local Ollama (Souverain et Gratuit)
- API Provider : Ollama
- Base URL : http://localhost:11434
- Model : uadf-agent
- Prérequis : Ollama en cours d'exécution (icône zone de notification)

### Mode 2 : Proxy Gemini Chrome (Cloud Gratuit + Copier-Coller)
- API Provider : OpenAI Compatible
- Base URL : http://localhost:8000/v1
- API Key : sk-fake-key-uadf
- Model : gemini-manual
- Prérequis : proxy.py démarré + Chrome ouvert sur Gem "Roo Code Agent"

### Mode 3 : Cloud Direct Claude Sonnet (Payant et Entièrement Automatique)
- API Provider : Anthropic
- Model : claude-sonnet-4-6
- API Key : [stockée dans VS Code SecretStorage — ne jamais noter ici]
- Prérequis : Connexion Internet + crédit Anthropic disponible
```

---

### Étape 5.7 — Remplir `memory-bank/activeContext.md`

Ouvrez `memory-bank/activeContext.md` et collez :

```markdown
# Contexte Actif

**Date de mise à jour :** 2026-03-23
**Mode actif :** developer
**Backend LLM actif :** Ollama uadf-agent

## Tâche en cours
Initialisation du projet UADF — Configuration de l'environnement de développement.

## Dernier résultat
Structure initiale du projet créée. Memory Bank initialisée. Dépôt Git initialisé.

## Prochain(s) pas
- [ ] Compléter les informations dans projectBrief.md
- [ ] Définir les premières User Stories dans productContext.md
- [ ] Configurer le proxy Gemini Chrome (proxy.py)
- [ ] Configurer le Gem Gemini Chrome

## Blocages / Questions ouvertes
Aucun blocage identifié pour le moment.

## Dernier commit Git
[À remplir après le premier commit de la Memory Bank]
```

---

### Étape 5.8 — Remplir `memory-bank/progress.md`

Ouvrez `memory-bank/progress.md` et collez :

```markdown
# Progression du Projet

**Dernière mise à jour :** 2026-03-23

## Infrastructure UADF

### Phase de Setup
- [x] Phase 0 : Base saine VS Code + Roo Code (réinstallation propre)
- [x] Phase 1 : Installation Ollama + modèles Qwen3-32B et 7B
- [x] Phase 2 : Dépôt Git initialisé avec .gitignore complet
- [x] Phase 3 : Modelfile personnalisé (uadf-agent, T=0.15, ctx=131072)
- [x] Phase 4 : .roomodes (4 personas Agile avec règles Git)
- [x] Phase 5 : Memory Bank (7 fichiers) + .clinerules (6 règles)
- [ ] Phase 6 : proxy.py (serveur Gemini Chrome, SSE)
- [ ] Phase 7 : Gem Gemini Chrome configuré
- [ ] Phase 8 : Roo Code commutateur 3 modes LLM
- [ ] Phase 9 : Tests end-to-end validés
- [ ] Phase 10 : API Anthropic Claude Sonnet configuré
- [ ] Phase 11 : Registre prompts/ initialisé
- [ ] Phase 12 : check-prompts-sync.ps1 + hook pre-commit

## Features Produit

### Epic 1 : [À définir]
- [ ] [Feature à définir]

## Légende
- [ ] À faire  |  [-] En cours  |  [x] Terminé
```

---

### Étape 5.9 — Remplir `memory-bank/decisionLog.md`

Ouvrez `memory-bank/decisionLog.md` et collez :

```markdown
# Decision Log — Architecture Decision Records (ADR)

---

## ADR-001 : Choix du moteur d'inférence local
**Date :** 2026-03-23
**Statut :** Accepté

**Contexte :**
Besoin d'un moteur d'inférence LLM local, gratuit et compatible avec l'API OpenAI pour Roo Code.

**Décision :**
Utilisation d'Ollama avec le modèle mychen76/qwen3_cline_roocode:32b compilé en uadf-agent.

**Conséquences :**
- Avantage : Souveraineté totale, gratuit, compatible OpenAI
- Avantage : Modèle spécifiquement optimisé pour le Tool Calling Roo Code
- Inconvénient : Nécessite 20+ Go de stockage et 16+ Go de RAM

---

## ADR-002 : Architecture du Proxy Gemini Chrome
**Date :** 2026-03-23
**Statut :** Accepté

**Contexte :**
Besoin d'exploiter Gemini Chrome gratuitement depuis Roo Code sans modifier son comportement.

**Décision :**
Serveur FastAPI local émulant l'API OpenAI, avec relay presse-papiers pour l'intervention humaine.
Streaming SSE en un seul chunk pour compatibilité totale avec Roo Code (DA-014).

**Conséquences :**
- Avantage : Roo Code non modifié, compatibilité native
- Avantage : Gratuité totale de Gemini Chrome
- Inconvénient : Nécessite une intervention humaine (copier-coller) à chaque requête

---

## ADR-003 : Versionnement Git intégral de tous les artefacts UADF
**Date :** 2026-03-23
**Statut :** Accepté

**Contexte :**
Besoin de tracer l'évolution de tous les artefacts du système : code, prompts, scripts, Memory Bank.

**Décision :**
Git versionne TOUT (code, .clinerules, .roomodes, Modelfile, proxy.py, memory-bank/).
La règle de commit est inscrite dans .clinerules (REGLE 5) ET dans les roleDefinitions
du Developer et du Scrum Master pour une défense en profondeur auto-portante.

**Conséquences :**
- Avantage : Traçabilité complète de l'évolution du système
- Avantage : Possibilité de rollback sur n'importe quel artefact
- Avantage : Comportement auto-portant : l'IA elle-même maintient le versionnement
- Inconvénient : Nécessite une discipline de commit cohérente
```

---

### Étape 5.10 — Créer le Dossier `docs/qa/`

```powershell
New-Item -Path "." -Name "docs" -ItemType Directory
New-Item -Path "docs" -Name "qa" -ItemType Directory
New-Item -Path "docs/qa" -Name ".gitkeep" -ItemType File
```

> **Pourquoi `docs/qa/` maintenant ?** Le Scrum Master lit les rapports QA dans `docs/qa/`. Ce dossier doit exister avant la première session Scrum Master pour éviter une erreur de lecture.

---

### Étape 5.11 — Versionner la Memory Bank et `.clinerules`

```powershell
git add .clinerules memory-bank/ docs/
git commit -m "feat(uadf): Memory Bank (7 fichiers) + .clinerules (6 règles VÉRIFIER→CRÉER→LIRE→AGIR)"
```

**Critère de validation Phase 5 :**
1. Ouvrez Roo Code et démarrez une nouvelle session en mode Developer
2. L'agent doit automatiquement lire `memory-bank/activeContext.md` et `memory-bank/progress.md` avant de répondre
3. Si vous demandez "Quel est l'état du projet ?", l'agent doit répondre en se basant sur le contenu de `progress.md`

> **Si l'agent n'utilise pas la Memory Bank :** Vérifiez que `.clinerules` est bien à la racine du projet (pas dans un sous-dossier). Rechargez VS Code (`Ctrl+Shift+P` > "Developer: Reload Window").

---

## PHASE 6 : Proxy Gemini Chrome — `proxy.py` v2.0 avec SSE

**Objectif :** Créer le serveur proxy Python FastAPI qui relaie les requêtes Roo Code vers Gemini Chrome via le presse-papiers Windows, avec support SSE transparent.
**Exigences adressées :** REQ-2.1.1 à REQ-2.4.4
**Décisions d'architecture :** DA-006, DA-007, DA-008, DA-009, DA-014

---

### Étape 6.1 — Créer l'Environnement Virtuel Python

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

> **Si erreur de politique d'exécution PowerShell :**
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```
> Puis relancez `.\venv\Scripts\Activate.ps1`. Vous devez voir `(venv)` au début de l'invite.

---

### Étape 6.2 — Installer les Dépendances Python

```powershell
pip install fastapi uvicorn pyperclip pydantic
pip freeze > requirements.txt
```

> **Versions minimales requises :** `fastapi>=0.110.0`, `uvicorn>=0.27.0`, `pyperclip>=1.8.2`, `pydantic>=2.0.0`

---

### Étape 6.3 — Créer `proxy.py` v2.0

Créez `proxy.py` à la racine du projet. Source canonique : [`SP-007-gem-gemini-roo-agent.md`](../prompts/SP-007-gem-gemini-roo-agent.md) pour le system prompt du Gem associé.

```python
"""
UADF Proxy v2.0 — Pont Roo Code <-> Gemini Chrome
Supporte stream=true (SSE) et stream=false (JSON complet).
Exigences: REQ-2.1.1 a REQ-2.4.4
"""
import asyncio, hashlib, json, os, time, uuid
from datetime import datetime
from typing import AsyncGenerator, List, Optional, Union

import pyperclip, uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel

USE_GEM_MODE = os.getenv("USE_GEM_MODE", "true").lower() == "true"
POLLING_INTERVAL = float(os.getenv("POLLING_INTERVAL", "1.0"))
TIMEOUT_SECONDS = int(os.getenv("TIMEOUT_SECONDS", "300"))
PORT = int(os.getenv("PROXY_PORT", "8000"))

ROO_XML_TAGS = [
    "<write_to_file>", "<read_file>", "<execute_command>",
    "<attempt_completion>", "<ask_followup_question>", "<replace_in_file>",
    "<list_files>", "<search_files>", "<browser_action>", "<new_task>"
]

class MessageContent(BaseModel):
    role: str
    content: Union[str, list]

class ChatRequest(BaseModel):
    model: str
    messages: List[MessageContent]
    temperature: Optional[float] = 0.0
    max_tokens: Optional[int] = None
    stream: Optional[bool] = False

app = FastAPI(title="UADF Proxy", version="2.0.0")

def _hash(text: str) -> str:
    return hashlib.md5(text.encode("utf-8")).hexdigest()

def _clean_content(content) -> str:
    """Nettoie le contenu : supprime les images base64. REQ-2.1.5"""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, dict):
                if item.get("type") == "text":
                    parts.append(item.get("text", ""))
                elif item.get("type") == "image_url":
                    parts.append("[IMAGE OMISE - Non supportee par le proxy clipboard]")
                else:
                    parts.append(str(item))
        return "\n".join(parts)
    return str(content)

def _format_prompt(messages: List[MessageContent]) -> str:
    """Formate les messages en texte lisible. REQ-2.1.3, REQ-2.1.4, REQ-2.2.2"""
    parts = []
    for msg in messages:
        content = _clean_content(msg.content)
        if not content.strip():
            continue
        if msg.role == "system":
            if USE_GEM_MODE:
                continue  # Filtrage system prompt en mode Gem (DA-008)
            parts.append("[SYSTEM PROMPT]\n" + content)
        elif msg.role == "user":
            parts.append("[USER]\n" + content)
        elif msg.role == "assistant":
            parts.append("[ASSISTANT]\n" + content)
    return "\n\n---\n\n".join(parts)

def _validate_response(text: str) -> bool:
    """Verifie la presence de balises XML Roo Code. REQ-2.3.4"""
    return any(tag in text for tag in ROO_XML_TAGS)

def _build_json_response(content: str, model: str) -> dict:
    """Construit une reponse JSON OpenAI. REQ-2.4.2"""
    return {
        "id": "chatcmpl-proxy-" + uuid.uuid4().hex[:8],
        "object": "chat.completion",
        "created": int(time.time()),
        "model": model,
        "choices": [{"index": 0, "message": {"role": "assistant", "content": content}, "finish_reason": "stop"}],
        "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
    }

async def _stream_response(content: str, model: str) -> AsyncGenerator[str, None]:
    """Genere une reponse SSE en un seul chunk. REQ-2.4.1, DA-014"""
    rid = "chatcmpl-proxy-" + uuid.uuid4().hex[:8]
    ts = int(time.time())
    chunk = {"id": rid, "object": "chat.completion.chunk", "created": ts, "model": model,
             "choices": [{"index": 0, "delta": {"role": "assistant", "content": content}, "finish_reason": None}]}
    yield f"data: {json.dumps(chunk)}\n\n"
    done = {"id": rid, "object": "chat.completion.chunk", "created": ts, "model": model,
            "choices": [{"index": 0, "delta": {}, "finish_reason": "stop"}]}
    yield f"data: {json.dumps(done)}\n\n"
    yield "data: [DONE]\n\n"

async def _wait_clipboard(initial_hash: str, ts: str) -> str:
    """Attend la reponse Gemini dans le presse-papiers. REQ-2.3.1, REQ-2.3.2, REQ-2.3.3"""
    start = time.time()
    while True:
        await asyncio.sleep(POLLING_INTERVAL)
        current = pyperclip.paste()
        if _hash(current) != initial_hash:
            elapsed = time.time() - start
            print(f"[{ts}] REPONSE DETECTEE ! {len(current)} chars en {elapsed:.1f}s")
            if not _validate_response(current):
                print(f"[{ts}] AVERTISSEMENT : Aucune balise XML Roo Code detectee.")
            return current
        if time.time() - start > TIMEOUT_SECONDS:
            raise HTTPException(status_code=408, detail="Timeout: Relancez votre requete dans Roo Code.")

@app.post("/v1/chat/completions")
async def chat_completions(request: ChatRequest):
    """Point d'entree principal. REQ-2.1.1, REQ-2.1.2"""
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"\n{'='*60}\n[{ts}] REQUETE | modele: {request.model} | stream: {request.stream}")
    formatted = _format_prompt(request.messages)
    pyperclip.copy(formatted)
    initial_hash = _hash(formatted)
    print(f"[{ts}] {'GEM MODE' if USE_GEM_MODE else 'MODE COMPLET'} | {len(formatted)} chars")
    print(f"[{ts}] PROMPT COPIE ! ACTION : 1.Chrome 2.Gem 3.Ctrl+V 4.Attendre 5.Ctrl+A+C")
    print(f"         Timeout dans {TIMEOUT_SECONDS}s...")
    response_text = await _wait_clipboard(initial_hash, ts)
    if request.stream:
        return StreamingResponse(_stream_response(response_text, request.model), media_type="text/event-stream")
    return JSONResponse(content=_build_json_response(response_text, request.model), status_code=200)

@app.get("/v1/models")
async def list_models():
    return JSONResponse({"object": "list", "data": [{"id": "gemini-manual", "object": "model", "created": int(time.time()), "owned_by": "uadf-proxy"}]})

@app.get("/health")
async def health_check():
    return {"status": "ok", "proxy": "UADF", "version": "2.0.0", "gem_mode": USE_GEM_MODE}

if __name__ == "__main__":
    print(f"{'='*60}\n  UADF PROXY v2.0 | http://localhost:{PORT}/v1\n  Mode: {'GEM' if USE_GEM_MODE else 'COMPLET'} | Timeout: {TIMEOUT_SECONDS}s\n{'='*60}")
    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="warning")
```

> **Points clés du code :**
> - `USE_GEM_MODE=true` (défaut) : filtre le message `system` — le system prompt est dans le Gem (DA-008)
> - `_stream_response()` : retourne la réponse en un seul chunk SSE suivi de `[DONE]` — transparent pour Roo Code (DA-014)
> - `_wait_clipboard()` : polling asynchrone non-bloquant toutes les secondes (DA-006)
> - `_validate_response()` : avertissement non-bloquant si pas de balises XML (REQ-2.3.4)

---

### Étape 6.4 — Créer le Script de Démarrage `scripts/start-proxy.ps1`

```powershell
New-Item -Path "." -Name "scripts" -ItemType Directory
```

Créez `scripts/start-proxy.ps1` :

```powershell
# UADF Proxy — Script de démarrage
$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot
& ".\venv\Scripts\Activate.ps1"
Write-Host "Démarrage UADF Proxy v2.0..." -ForegroundColor Green
Write-Host "URL : http://localhost:8000/v1" -ForegroundColor Cyan
python proxy.py
```

---

### Étape 6.5 — Tester le Proxy

**Terminal 1 — Démarrer le proxy :**
```powershell
.\venv\Scripts\Activate.ps1
python proxy.py
```

Sortie attendue :
```
============================================================
  UADF PROXY v2.0 | http://localhost:8000/v1
  Mode: GEM | Timeout: 300s
============================================================
```

**Terminal 2 — Tester `/health` :**
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get
```
Réponse attendue : `{"status": "ok", "proxy": "UADF", "version": "2.0.0", "gem_mode": true}`

**Terminal 2 — Tester `/v1/models` :**
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/v1/models" -Method Get
```
Réponse attendue : liste contenant `"id": "gemini-manual"`.

---

### Étape 6.6 — Versionner `proxy.py` et les Scripts

```powershell
git add proxy.py requirements.txt scripts/
git commit -m "feat(proxy): proxy.py v2.0 FastAPI SSE — pont Roo Code <-> Gemini Chrome"
```

**Critère de validation Phase 6 :**
- `python proxy.py` démarre sans erreur
- `http://localhost:8000/health` répond `{"status": "ok"}`
- `http://localhost:8000/v1/models` répond avec `gemini-manual`

---

## PHASE 7 : Configuration Gemini Chrome — Gem "Roo Code Agent"

**Objectif :** Créer un Gem Gemini dédié avec le system prompt Roo Code intégré, pour éviter de retransmettre le system prompt à chaque requête via le presse-papiers.
**Exigences adressées :** REQ-5.1, REQ-5.2, REQ-5.3
**Décisions d'architecture :** DA-010

---

### Étape 7.1 — Créer le Gem Gemini "Roo Code Agent"

1. Ouvrez **Google Chrome** (pas un autre navigateur)
2. Allez sur **https://gemini.google.com**
3. Connectez-vous avec votre compte Google
4. Dans le menu latéral gauche, cliquez sur **"Gems"**
5. Cliquez sur **"New Gem"** (ou "Nouveau Gem")
6. Donnez le nom : **`Roo Code Agent`**
7. Dans le champ **"Instructions"**, collez **exactement** ce texte (source canonique : [`SP-007-gem-gemini-roo-agent.md`](../prompts/SP-007-gem-gemini-roo-agent.md)) :

```
Tu es un agent de developpement logiciel expert qui travaille en collaboration avec Roo Code (extension VS Code).

TON ROLE :
Tu recois des demandes de Roo Code via un systeme de relai clipboard (proxy). Tu dois analyser ces demandes et fournir des reponses structurees que Roo Code pourra interpreter et executer.

FORMAT DE REPONSE OBLIGATOIRE :
Tu DOIS toujours structurer tes reponses avec les balises XML suivantes selon le type d'action :

Pour lire un fichier :
<read_file>
<path>chemin/vers/fichier</path>
</read_file>

Pour ecrire dans un fichier :
<write_to_file>
<path>chemin/vers/fichier</path>
<content>
contenu complet du fichier
</content>
</write_to_file>

Pour executer une commande terminal :
<execute_command>
<command>commande a executer</command>
</execute_command>

Pour rechercher dans les fichiers :
<search_files>
<path>dossier/de/recherche</path>
<regex>pattern de recherche</regex>
</search_files>

Pour terminer une tache :
<attempt_completion>
<result>
Description du resultat accompli
</result>
</attempt_completion>

REGLES IMPORTANTES :
1. Toujours utiliser les balises XML ci-dessus pour les actions — jamais de texte libre pour les actions
2. Toujours lire la Memory Bank (memory-bank/) avant d'agir sur le code
3. Toujours mettre a jour memory-bank/activeContext.md apres chaque action significative
4. Toujours effectuer un commit Git apres chaque modification de fichier
5. Etre concis et precis dans les descriptions — eviter les explications superflues
6. Si une tache est ambigue, demander une clarification avant d'agir

CONTEXTE DU PROJET :
Tu travailles sur un projet utilisant le framework UADF (Unified Agentic Development Framework).
Le projet utilise une equipe Agile virtuelle avec 4 personas : Product Owner, Scrum Master, Developer, QA Engineer.
La memoire persistante est stockee dans le dossier memory-bank/ (7 fichiers Markdown).
```

8. Cliquez sur **"Save"**

> **IMPORTANT — Déploiement manuel obligatoire :** Ce prompt est le seul du registre UADF qui ne peut pas être déployé automatiquement via Git. Toute modification future de ce Gem doit être accompagnée d'un commit Git avec la mention : `"DEPLOIEMENT MANUEL REQUIS : mettre a jour le Gem Gemini avec SP-007"` (voir REGLE 6.2 de `.clinerules`).

---

### Étape 7.2 — Vérifier le Bon Fonctionnement du Gem

1. Ouvrez le Gem "Roo Code Agent" dans Gemini
2. Envoyez ce message de test :
   ```
   Lis le fichier memory-bank/activeContext.md
   ```
3. Le Gem doit répondre **uniquement** avec :
   ```xml
   <read_file>
   <path>memory-bank/activeContext.md</path>
   </read_file>
   ```

> **Si le Gem répond en texte libre sans balises XML :** Les instructions n'ont pas été correctement sauvegardées. Recommencez l'étape 7.1 en vous assurant de coller le texte dans le champ "Instructions" (pas dans la zone de chat).

---

### Étape 7.3 — Configurer Chrome pour le Workflow Proxy

Pour utiliser le proxy efficacement :

1. **Épinglez l'onglet Gemini** dans Chrome (clic droit sur l'onglet > "Épingler")
2. **Gardez le Gem "Roo Code Agent" ouvert** en permanence pendant les sessions de développement
3. **Workflow à chaque requête proxy :**
   - Le proxy affiche dans le terminal : `PROMPT COPIE ! ACTION : 1.Chrome 2.Gem 3.Ctrl+V 4.Attendre 5.Ctrl+A+C`
   - Basculez sur Chrome (`Alt+Tab`)
   - Cliquez dans la zone de saisie du Gem
   - Collez (`Ctrl+V`) — le prompt de Roo Code apparaît
   - Attendez la réponse de Gemini
   - Sélectionnez tout (`Ctrl+A`) et copiez (`Ctrl+C`)
   - Le proxy détecte automatiquement le changement dans le presse-papiers et retourne la réponse à Roo Code

---

## PHASE 8 : Roo Code — Commutateur 3 Modes LLM

**Objectif :** Configurer Roo Code pour basculer entre les 3 backends LLM (Ollama local, Proxy Gemini Chrome, API Anthropic Claude) via le paramètre "API Provider".
**Exigences adressées :** REQ-2.0, REQ-000
**Décisions d'architecture :** DA-007, DA-011

---

### Étape 8.1 — Configurer le Mode 1 : Ollama Local

1. Dans VS Code, cliquez sur l'icône **Roo Code** dans la barre latérale
2. Cliquez sur l'icône **⚙️ Paramètres** (engrenage) en haut du panneau Roo Code
3. Dans la section **"API Provider"**, sélectionnez **"Ollama"**
4. Dans **"Base URL"**, entrez : `http://localhost:11434`
5. Dans **"Model"**, entrez : `uadf-agent`
6. Sauvegardez

**Test de validation Mode 1 :**
```powershell
ollama list
# Doit afficher uadf-agent dans la liste
```
Puis dans Roo Code (mode Developer), envoyez : `Dis bonjour en une phrase.`
L'agent doit répondre via Ollama (vérifiable dans les logs Ollama).

---

### Étape 8.2 — Configurer le Mode 2 : Proxy Gemini Chrome

1. Dans Roo Code Paramètres > **"API Provider"**, sélectionnez **"OpenAI Compatible"**
2. Dans **"Base URL"**, entrez : `http://localhost:8000/v1`
3. Dans **"API Key"**, entrez : `sk-fake-key-uadf` (valeur fictive requise par Roo Code)
4. Dans **"Model"**, entrez : `gemini-manual`
5. Sauvegardez

**Test de validation Mode 2 :**
1. Démarrez le proxy : `python proxy.py`
2. Ouvrez Chrome sur le Gem "Roo Code Agent"
3. Dans Roo Code (mode Developer), envoyez : `Dis bonjour en une phrase.`
4. Le proxy doit afficher : `PROMPT COPIE ! ACTION : 1.Chrome 2.Gem 3.Ctrl+V 4.Attendre 5.Ctrl+A+C`
5. Suivez les instructions du proxy (copier-coller dans Chrome)
6. Roo Code doit recevoir la réponse de Gemini

---

### Étape 8.3 — Configurer le Mode 3 : API Anthropic Claude

> **Note :** Cette configuration est détaillée en Phase 10. Vous pouvez la sauter pour l'instant et revenir après avoir validé les Modes 1 et 2.

1. Dans Roo Code Paramètres > **"API Provider"**, sélectionnez **"Anthropic"**
2. Dans **"API Key"**, entrez votre clé Anthropic (`sk-ant-api03-...`)
3. Dans **"Model"**, entrez : `claude-sonnet-4-6`
4. Sauvegardez

---

### Étape 8.4 — Documenter le Commutateur dans `memory-bank/techContext.md`

Ouvrez `memory-bank/techContext.md` et complétez la section "Configuration des Backends LLM" avec les valeurs réelles de votre configuration (URLs, modèles confirmés).

```powershell
git add memory-bank/techContext.md
git commit -m "docs(memory): techContext.md mis à jour avec configuration commutateur 3 modes LLM"
```

---

## PHASE 9 : Tests End-to-End — Validation Complète du Système

**Objectif :** Valider que les 3 modes LLM fonctionnent correctement avec la Memory Bank, les personas Agile et le versionnement Git.
**Exigences adressées :** REQ-000, REQ-4.2, REQ-4.3

---

### Étape 9.1 — Test End-to-End Mode 1 (Ollama)

**Prérequis :** Ollama en cours d'exécution, `uadf-agent` disponible, Roo Code configuré en Mode 1.

**Scénario de test :**
1. Sélectionnez le mode **"Developer"** dans Roo Code
2. Envoyez : `Crée un fichier src/hello.py avec une fonction hello() qui retourne "Hello UADF"`
3. **Comportement attendu :**
   - L'agent lit `memory-bank/activeContext.md` et `memory-bank/progress.md` (REGLE 1 — séquence VÉRIFIER→CRÉER→LIRE→AGIR)
   - L'agent crée `src/hello.py`
   - L'agent met à jour `memory-bank/activeContext.md` (REGLE 2)
   - L'agent exécute `git add . && git commit -m "feat(src): ajout hello.py"` (REGLE 5)

**Vérification :**
```powershell
Test-Path "src/hello.py"          # Doit retourner True
git log --oneline -3              # Doit afficher un commit récent avec "feat(src)"
Get-Content "memory-bank/activeContext.md"  # Doit mentionner la création de hello.py
```

---

### Étape 9.2 — Test End-to-End Mode 2 (Proxy Gemini)

**Prérequis :** `python proxy.py` en cours d'exécution, Chrome ouvert sur Gem "Roo Code Agent", Roo Code configuré en Mode 2.

**Scénario de test :**
1. Sélectionnez le mode **"QA Engineer"** dans Roo Code
2. Envoyez : `Crée un rapport de test dans docs/qa/test-hello-2026-03-23.md`
3. **Comportement attendu :**
   - Le proxy affiche les instructions copier-coller dans le terminal
   - Vous effectuez le copier-coller dans Chrome/Gemini
   - Gemini répond avec des balises XML
   - Le proxy retourne la réponse à Roo Code (via SSE ou JSON selon `stream`)
   - L'agent crée le rapport dans `docs/qa/`
   - L'agent ne peut PAS modifier `src/hello.py` (RBAC QA Engineer)

**Vérification :**
```powershell
Test-Path "docs/qa/test-hello-2026-03-23.md"  # Doit retourner True
git log --oneline -3                           # Doit afficher un commit récent
```

---

### Étape 9.3 — Test RBAC Complet

| Mode | Demande | Comportement Attendu |
| :--- | :--- | :--- |
| Product Owner | "Écris du code Python" | Refus — hors périmètre |
| Product Owner | "Crée une User Story" | Accepté — rédige dans `memory-bank/productContext.md` |
| Scrum Master | "Lance pytest" | Refus — pas d'exécution de tests |
| Scrum Master | "Quel est l'état des tests ?" | Accepté — lit `docs/qa/` et répond |
| Developer | "Modifie src/hello.py" | Accepté — modifie le fichier et commite |
| QA Engineer | "Modifie src/hello.py" | Refus — hors périmètre |
| QA Engineer | "Lance pytest" | Accepté — exécute les tests |

---

### Étape 9.4 — Versionner les Résultats des Tests

```powershell
git add src/ docs/ memory-bank/
git commit -m "test(e2e): validation complète 3 modes LLM + RBAC + Memory Bank"
```

**Critère de validation Phase 9 :**
- Les 3 modes LLM répondent correctement
- La Memory Bank est lue et mise à jour à chaque session
- Le RBAC bloque les actions hors périmètre pour chaque persona
- Chaque action est versionnée dans Git avec un message Conventional Commits

---

## PHASE 10 : API Anthropic Claude — Mode Cloud Direct

**Objectif :** Configurer la connexion directe à l'API Anthropic avec le modèle `claude-sonnet-4-6`, sans proxy intermédiaire.
**Exigences adressées :** REQ-6.1, REQ-6.2, REQ-6.3, REQ-6.4
**Décisions d'architecture :** DA-011

---

### Étape 10.1 — Obtenir une Clé API Anthropic

1. Allez sur **https://console.anthropic.com**
2. Créez un compte ou connectez-vous
3. Dans **"API Keys"**, cliquez sur **"Create Key"**
4. Donnez un nom : `uadf-roo-code`
5. Copiez la clé (`sk-ant-api03-...`) — **elle ne sera affichée qu'une seule fois**

> **SÉCURITÉ ABSOLUE :** Ne jamais stocker cette clé dans un fichier du projet. Ne jamais la commiter dans Git. VS Code SecretStorage est le seul endroit autorisé (DA-011, REQ-6.4).

---

### Étape 10.2 — Configurer Roo Code avec la Clé Anthropic

1. Dans VS Code, ouvrez Roo Code Paramètres
2. Dans **"API Provider"**, sélectionnez **"Anthropic"**
3. Dans **"API Key"**, collez votre clé `sk-ant-api03-...`
4. Dans **"Model"**, entrez : `claude-sonnet-4-6`
5. Sauvegardez

> **Note de maintenance (REQ-6.2) :** Le modèle `claude-sonnet-4-6` est la version de référence au 2026-03-23. Anthropic publie régulièrement de nouvelles versions. Pour vérifier la dernière version disponible : https://docs.anthropic.com/en/docs/about-claude/models. Mettez à jour ce champ, REQ-6.2 dans DOC1, et DA-011 dans DOC2 lors de chaque mise à jour majeure.

---

### Étape 10.3 — Tester la Connexion Anthropic

Dans Roo Code (mode Developer), envoyez :
```
Dis bonjour et indique quel modèle tu es.
```

**Comportement attendu :**
- La réponse arrive sans intervention humaine (contrairement au Mode 2)
- La réponse utilise les balises XML Roo Code
- La Memory Bank est lue et mise à jour automatiquement
- Un commit Git est effectué automatiquement

---

### Étape 10.4 — Vérifier la Sécurité de la Clé API

```powershell
# Vérifier que la clé n'est PAS dans les fichiers du projet
Select-String -Path "*.py", "*.md", "*.json", "*.txt", "*.env" -Pattern "sk-ant-api" -Recurse
# Doit retourner AUCUN résultat
```

> **Si la clé apparaît dans les résultats :** Supprimez-la immédiatement du fichier, invalidez la clé sur console.anthropic.com, et créez-en une nouvelle. Vérifiez que `.gitignore` contient bien `*.env`.

---

### Étape 10.5 — Versionner la Mise à Jour de la Memory Bank

```powershell
git add memory-bank/
git commit -m "docs(memory): activeContext.md mis à jour — Mode 3 Claude API validé"
```

**Critère de validation Phase 10 :**
- Roo Code répond via l'API Anthropic sans proxy
- La clé API n'est dans aucun fichier du projet (`Select-String` retourne vide)
- La Memory Bank est mise à jour après la session de test

---

## PHASE 11 : Registre des Prompts — Initialisation de `prompts/`

**Objectif :** Initialiser le registre centralisé des system prompts dans `prompts/` avec les 7 fichiers SP canoniques et le `README.md` d'index.
**Exigences adressées :** REQ-7.1, REQ-7.2, REQ-7.3, REQ-7.4, REQ-7.5
**Décisions d'architecture :** DA-012

---

### Étape 11.1 — Vérifier la Structure du Registre

Le dossier `prompts/` doit déjà exister si vous avez cloné ce dépôt. Vérifiez :

```powershell
Get-ChildItem -Path "prompts/" -Name
```

Sortie attendue :
```
README.md
SP-001-ollama-modelfile-system.md
SP-002-clinerules-global.md
SP-003-persona-product-owner.md
SP-004-persona-scrum-master.md
SP-005-persona-developer.md
SP-006-persona-qa-engineer.md
SP-007-gem-gemini-roo-agent.md
```

> **Si le dossier `prompts/` est absent :** Créez-le et les fichiers SP manuellement en suivant les étapes 11.2 à 11.4.

---

### Étape 11.2 — Comprendre la Structure d'un Fichier SP Canonique

Chaque fichier `SP-XXX-*.md` dans `prompts/` suit cette structure :

```markdown
---
id: SP-XXX
name: [Nom descriptif]
version: 1.0.0
last_updated: [DATE]
status: active

target_type: [ollama_modelfile | roo_clinerules | roo_roomodes | gemini_gem_instructions]
target_file: [Fichier cible ou EXTERNE]
target_field: "[Champ exact à modifier dans le fichier cible]"
target_location: >
  [Instructions de déploiement détaillées]

hors_git: [true | false]  # true uniquement pour SP-007

depends_on:
  - [SP-XXX]: "[Raison de la dépendance]"

changelog:
  - version: 1.0.0
    date: [DATE]
    change: [Description du changement]
---

# SP-XXX — [Nom]

## Contenu du Prompt

> Copier exactement ce texte dans [cible].

[CONTENU DU PROMPT]

## Notes de Déploiement

[Instructions étape par étape]

## Impact sur les Autres Prompts

[Dépendances et impacts]
```

> **Pourquoi cette structure ?** L'en-tête YAML permet au script `check-prompts-sync.ps1` (Phase 12) d'identifier automatiquement la cible de déploiement et d'extraire le contenu à comparer.

---

### Étape 11.3 — Vérifier la Cohérence des Prompts Déployés

Vérifiez manuellement que chaque artefact déployé correspond à son SP canonique :

| SP Canonique | Artefact Déployé | Vérification |
| :--- | :--- | :--- |
| `SP-001` | `Modelfile` bloc `SYSTEM """..."""` | Comparer le contenu |
| `SP-002` | `.clinerules` (fichier entier) | Comparer le contenu |
| `SP-003` | `.roomodes` > `customModes[0].roleDefinition` | Comparer la chaîne JSON |
| `SP-004` | `.roomodes` > `customModes[1].roleDefinition` | Comparer la chaîne JSON |
| `SP-005` | `.roomodes` > `customModes[2].roleDefinition` | Comparer la chaîne JSON |
| `SP-006` | `.roomodes` > `customModes[3].roleDefinition` | Comparer la chaîne JSON |
| `SP-007` | Gem Gemini "Roo Code Agent" > Instructions | Vérification manuelle |

---

### Étape 11.4 — Versionner le Registre des Prompts

```powershell
git add prompts/
git commit -m "feat(prompts): initialisation registre SP canoniques (SP-001 à SP-007)"
```

**Critère de validation Phase 11 :**
- `prompts/` contient 8 fichiers (README.md + 7 SP)
- Chaque SP a un en-tête YAML valide avec `id`, `version`, `target_file`, `target_field`
- SP-007 est marqué `hors_git: true`
- Le contenu de chaque SP correspond à l'artefact déployé

---

## PHASE 12 : Vérification Automatique — `check-prompts-sync.ps1` + Hook Git

**Objectif :** Créer le script PowerShell de vérification de cohérence des prompts et le hook Git pre-commit qui l'appelle automatiquement avant chaque commit.
**Exigences adressées :** REQ-8.1, REQ-8.2, REQ-8.3, REQ-8.4
**Décisions d'architecture :** DA-013

---

### Étape 12.1 — Créer `scripts/check-prompts-sync.ps1`

Créez `scripts/check-prompts-sync.ps1` et collez **exactement** ce code :

```powershell
<#
.SYNOPSIS
    UADF — Vérification de cohérence des system prompts canoniques vs artefacts déployés.
    REQ-8.1, REQ-8.3, REQ-8.4 | DA-013

.DESCRIPTION
    Compare le contenu de chaque SP canonique (prompts/SP-XXX-*.md) avec l'artefact
    déployé correspondant. Utilise une comparaison normalisée (CRLF->LF, trim).
    SP-007 (Gem Gemini) est exclu de la vérification automatique avec avertissement.
    Retourne exit code 0 si tout est synchronisé, 1 si désynchronisation détectée.
#>

param(
    [switch]$Verbose = $false
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot
$PromptsDir = Join-Path $ProjectRoot "prompts"
$PassCount = 0
$FailCount = 0
$WarnCount = 0

function Normalize-Text {
    param([string]$Text)
    # Normalisation : CRLF -> LF, trim espaces/sauts de ligne en début/fin
    return $Text.Replace("`r`n", "`n").Replace("`r", "`n").Trim()
}

function Extract-PromptContent {
    param([string]$SpFile)
    # Extraire le contenu entre les balises ```markdown ou ``` (premier bloc de code)
    $content = Get-Content $SpFile -Raw -Encoding UTF8
    if ($content -match "(?s)```(?:markdown|python|)?\r?\n(.*?)\r?\n```") {
        return Normalize-Text $Matches[1]
    }
    return $null
}

function Show-Diff {
    param([string]$Expected, [string]$Actual, [string]$Label)
    $expLines = $Expected -split "`n"
    $actLines = $Actual -split "`n"
    $maxLines = [Math]::Max($expLines.Count, $actLines.Count)
    $diffLines = @()
    for ($i = 0; $i -lt [Math]::Min($maxLines, 20); $i++) {
        $e = if ($i -lt $expLines.Count) { $expLines[$i] } else { "" }
        $a = if ($i -lt $actLines.Count) { $actLines[$i] } else { "" }
        if ($e -ne $a) {
            $diffLines += "  Ligne $($i+1):"
            $diffLines += "    SP (attendu) : $e"
            $diffLines += "    Déployé      : $a"
        }
    }
    if ($diffLines.Count -gt 0) {
        Write-Host "  Premières différences :" -ForegroundColor Yellow
        $diffLines | ForEach-Object { Write-Host $_ -ForegroundColor Yellow }
    }
}

Write-Host ""
Write-Host "=" * 60
Write-Host "  UADF — Vérification Cohérence Prompts" -ForegroundColor Cyan
Write-Host "=" * 60

# --- SP-001 : Modelfile ---
Write-Host ""
Write-Host "[SP-001] Modelfile bloc SYSTEM..." -NoNewline
$ModelfilePath = Join-Path $ProjectRoot "Modelfile"
$Sp001Path = Join-Path $PromptsDir "SP-001-ollama-modelfile-system.md"
if (-not (Test-Path $ModelfilePath)) {
    Write-Host " SKIP (Modelfile absent)" -ForegroundColor Yellow
    $WarnCount++
} else {
    $spContent = Extract-PromptContent $Sp001Path
    $modelfileRaw = Get-Content $ModelfilePath -Raw -Encoding UTF8
    if ($modelfileRaw -match '(?s)SYSTEM\s+"""(.*?)"""') {
        $deployedContent = Normalize-Text $Matches[1]
        if ($spContent -eq $deployedContent) {
            Write-Host " PASS" -ForegroundColor Green
            $PassCount++
        } else {
            Write-Host " FAIL" -ForegroundColor Red
            Show-Diff $spContent $deployedContent "SP-001"
            $FailCount++
        }
    } else {
        Write-Host " FAIL (bloc SYSTEM introuvable dans Modelfile)" -ForegroundColor Red
        $FailCount++
    }
}

# --- SP-002 : .clinerules ---
Write-Host "[SP-002] .clinerules (fichier entier)..." -NoNewline
$ClinerPath = Join-Path $ProjectRoot ".clinerules"
$Sp002Path = Join-Path $PromptsDir "SP-002-clinerules-global.md"
if (-not (Test-Path $ClinerPath)) {
    Write-Host " SKIP (.clinerules absent)" -ForegroundColor Yellow
    $WarnCount++
} else {
    $spContent = Extract-PromptContent $Sp002Path
    $deployedContent = Normalize-Text (Get-Content $ClinerPath -Raw -Encoding UTF8)
    if ($spContent -eq $deployedContent) {
        Write-Host " PASS" -ForegroundColor Green
        $PassCount++
    } else {
        Write-Host " FAIL" -ForegroundColor Red
        Show-Diff $spContent $deployedContent "SP-002"
        $FailCount++
    }
}

# --- SP-003 à SP-006 : .roomodes ---
$RoomodesPath = Join-Path $ProjectRoot ".roomodes"
$SpPersonas = @(
    @{ Id = "SP-003"; File = "SP-003-persona-product-owner.md"; Slug = "product-owner"; Index = 0 },
    @{ Id = "SP-004"; File = "SP-004-persona-scrum-master.md"; Slug = "scrum-master"; Index = 1 },
    @{ Id = "SP-005"; File = "SP-005-persona-developer.md"; Slug = "developer"; Index = 2 },
    @{ Id = "SP-006"; File = "SP-006-persona-qa-engineer.md"; Slug = "qa-engineer"; Index = 3 }
)

if (-not (Test-Path $RoomodesPath)) {
    Write-Host "[SP-003..006] .roomodes absent — SKIP" -ForegroundColor Yellow
    $WarnCount += 4
} else {
    $roomodesJson = Get-Content $RoomodesPath -Raw -Encoding UTF8 | ConvertFrom-Json
    foreach ($persona in $SpPersonas) {
        Write-Host "[$($persona.Id)] .roomodes > $($persona.Slug) roleDefinition..." -NoNewline
        $spFile = Join-Path $PromptsDir $persona.File
        $spContent = Extract-PromptContent $spFile
        $mode = $roomodesJson.customModes | Where-Object { $_.slug -eq $persona.Slug }
        if ($null -eq $mode) {
            Write-Host " FAIL (slug '$($persona.Slug)' introuvable dans .roomodes)" -ForegroundColor Red
            $FailCount++
        } else {
            $deployedContent = Normalize-Text $mode.roleDefinition
            if ($spContent -eq $deployedContent) {
                Write-Host " PASS" -ForegroundColor Green
                $PassCount++
            } else {
                Write-Host " FAIL" -ForegroundColor Red
                Show-Diff $spContent $deployedContent $persona.Id
                $FailCount++
            }
        }
    }
}

# --- SP-007 : Gem Gemini (hors Git — vérification manuelle) ---
Write-Host ""
Write-Host "[SP-007] Gem Gemini 'Roo Code Agent'..." -NoNewline
Write-Host " AVERTISSEMENT (déploiement manuel requis)" -ForegroundColor Yellow
Write-Host "  -> Vérifier manuellement sur https://gemini.google.com > Gems > 'Roo Code Agent'"
Write-Host "  -> Comparer avec : prompts/SP-007-gem-gemini-roo-agent.md"
$WarnCount++

# --- Résumé ---
Write-Host ""
Write-Host "=" * 60
Write-Host "  RÉSUMÉ : $PassCount PASS | $FailCount FAIL | $WarnCount WARN" -ForegroundColor $(if ($FailCount -gt 0) { "Red" } elseif ($WarnCount -gt 0) { "Yellow" } else { "Green" })
Write-Host "=" * 60
Write-Host ""

if ($FailCount -gt 0) {
    Write-Host "ÉCHEC : $FailCount prompt(s) désynchronisé(s). Commit bloqué." -ForegroundColor Red
    Write-Host "Action requise : mettre à jour les artefacts déployés pour correspondre aux SP canoniques." -ForegroundColor Red
    exit 1
} else {
    Write-Host "SUCCÈS : Tous les prompts vérifiables sont synchronisés." -ForegroundColor Green
    exit 0
}
```

---

### Étape 12.2 — Créer le Hook Git `pre-commit`

```powershell
# Créer le fichier hook pre-commit
$hookContent = @'
#!/bin/sh
# UADF — Hook pre-commit : vérification cohérence prompts (REQ-8.2, DA-013)
echo "UADF pre-commit : vérification cohérence prompts..."
powershell.exe -ExecutionPolicy Bypass -File "scripts/check-prompts-sync.ps1"
if [ $? -ne 0 ]; then
    echo "COMMIT BLOQUÉ : Désynchronisation détectée dans les prompts."
    echo "Corrigez les désynchronisations avant de commiter."
    exit 1
fi
exit 0
'@

$hookPath = Join-Path $ProjectRoot ".git/hooks/pre-commit"
Set-Content -Path $hookPath -Value $hookContent -Encoding UTF8 -NoNewline
```

> **Note Windows :** Le hook Git est un script shell (`#!/bin/sh`). Git for Windows exécute les hooks via son shell intégré (Git Bash). La commande `powershell.exe` est disponible dans Git Bash sur Windows.

---

### Étape 12.3 — Tester le Script de Vérification

```powershell
# Tester manuellement le script
.\venv\Scripts\Activate.ps1  # Si nécessaire pour l'environnement
powershell.exe -ExecutionPolicy Bypass -File "scripts/check-prompts-sync.ps1"
```

**Sortie attendue (tout synchronisé) :**
```
============================================================
  UADF — Vérification Cohérence Prompts
============================================================

[SP-001] Modelfile bloc SYSTEM... PASS
[SP-002] .clinerules (fichier entier)... PASS
[SP-003] .roomodes > product-owner roleDefinition... PASS
[SP-004] .roomodes > scrum-master roleDefinition... PASS
[SP-005] .roomodes > developer roleDefinition... PASS
[SP-006] .roomodes > qa-engineer roleDefinition... PASS

[SP-007] Gem Gemini 'Roo Code Agent'... AVERTISSEMENT (déploiement manuel requis)
  -> Vérifier manuellement sur https://gemini.google.com > Gems > 'Roo Code Agent'
  -> Comparer avec : prompts/SP-007-gem-gemini-roo-agent.md

============================================================
  RÉSUMÉ : 6 PASS | 0 FAIL | 1 WARN
============================================================

SUCCÈS : Tous les prompts vérifiables sont synchronisés.
```

---

### Étape 12.4 — Tester le Blocage du Commit en Cas de Désynchronisation

Pour tester que le hook bloque bien un commit en cas de désynchronisation :

```powershell
# 1. Modifier temporairement .clinerules pour créer une désynchronisation
Add-Content -Path ".clinerules" -Value "`n# TEST DESYNC"

# 2. Tenter un commit — doit être bloqué
git add .clinerules
git commit -m "test: vérification blocage hook pre-commit"
# Attendu : "COMMIT BLOQUÉ : Désynchronisation détectée dans les prompts."

# 3. Restaurer .clinerules
git checkout .clinerules
```

---

### Étape 12.5 — Versionner les Scripts et le Hook

```powershell
git add scripts/check-prompts-sync.ps1
git commit -m "feat(prompts): check-prompts-sync.ps1 + hook pre-commit — vérification cohérence automatique"
```

> **Note :** Le hook `.git/hooks/pre-commit` n'est PAS versionné dans Git (le dossier `.git/` est exclu). Chaque développeur qui clone le dépôt doit recréer le hook en exécutant l'étape 12.2.

---

**Critère de validation Phase 12 :**
- `scripts/check-prompts-sync.ps1` s'exécute sans erreur et affiche `6 PASS | 0 FAIL`
- Un commit avec `.clinerules` modifié est bloqué par le hook pre-commit
- La restauration de `.clinerules` débloque le commit

---

## Récapitulatif Final — Système UADF Complet

### Arborescence du Projet après les 13 Phases

```
[RACINE DU PROJET]
├── .clinerules              # 6 règles impératives (SP-002) — VÉRIFIER→CRÉER→LIRE→AGIR
├── .gitignore               # venv/, .env, __pycache__, *.log
├── .roomodes                # 4 personas Agile RBAC (SP-003 à SP-006)
├── Modelfile                # Modèle uadf-agent (SP-001) — T=0.15, ctx=131072
├── proxy.py                 # Proxy Gemini Chrome v2.0 (FastAPI + SSE)
├── requirements.txt         # Dépendances Python (fastapi, uvicorn, pyperclip, pydantic)
├── docs/
│   └── qa/                  # Rapports QA (écrits par QA Engineer uniquement)
│       └── .gitkeep
├── memory-bank/             # Memory Bank — 7 fichiers Markdown
│   ├── activeContext.md     # Tâche en cours, dernier résultat, prochaine action
│   ├── decisionLog.md       # ADR horodatés
│   ├── productContext.md    # User Stories, backlog
│   ├── progress.md          # Checklist phases UADF + features
│   ├── projectBrief.md      # Vision, objectifs, Non-Goals
│   ├── systemPatterns.md    # Architecture, conventions, patterns
│   └── techContext.md       # Stack, commandes, config backends LLM
├── plans/                   # Documents de planification (DOC1, DOC2, DOC3)
│   ├── DOC1-PRD-Unified-Agentic-Framework.md
│   ├── DOC2-Architecture-Solution-Stack.md
│   └── DOC3-Plan-Implementation-COMPLETE.md
├── prompts/                 # Registre SP canoniques (SP-001 à SP-007)
│   ├── README.md
│   ├── SP-001-ollama-modelfile-system.md
│   ├── SP-002-clinerules-global.md
│   ├── SP-003-persona-product-owner.md
│   ├── SP-004-persona-scrum-master.md
│   ├── SP-005-persona-developer.md
│   ├── SP-006-persona-qa-engineer.md
│   └── SP-007-gem-gemini-roo-agent.md
├── scripts/
│   ├── check-prompts-sync.ps1  # Vérification cohérence prompts
│   └── start-proxy.ps1         # Démarrage proxy Gemini Chrome
└── src/                     # Code source applicatif (créé par Developer)
```

---

### Tableau de Bord des 3 Modes LLM

| Mode | Provider Roo Code | URL / Modèle | Coût | Automatique | Prérequis |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1 — Local** | Ollama | `http://localhost:11434` / `uadf-agent` | Gratuit | ✅ Oui | Ollama en cours |
| **2 — Proxy** | OpenAI Compatible | `http://localhost:8000/v1` / `gemini-manual` | Gratuit | ❌ Copier-coller | proxy.py + Chrome |
| **3 — Cloud** | Anthropic | `api.anthropic.com` / `claude-sonnet-4-6` | Payant | ✅ Oui | Clé API + Internet |

---

### Checklist de Validation Finale

- [ ] Phase 0 : VS Code + Roo Code réinstallés proprement
- [ ] Phase 1 : Ollama + `uadf-agent` (32B) + `qwen3:7b` installés
- [ ] Phase 2 : Dépôt Git initialisé avec `.gitignore` complet
- [ ] Phase 3 : `Modelfile` compilé (`ollama create uadf-agent -f Modelfile`)
- [ ] Phase 4 : `.roomodes` avec 4 personas RBAC validés
- [ ] Phase 5 : Memory Bank (7 fichiers) + `.clinerules` (6 règles) — séquence VÉRIFIER→CRÉER→LIRE→AGIR validée
- [ ] Phase 6 : `proxy.py` v2.0 démarre et répond sur `/health`
- [ ] Phase 7 : Gem Gemini "Roo Code Agent" créé et répond avec balises XML
- [ ] Phase 8 : Commutateur 3 modes configuré dans Roo Code
- [ ] Phase 9 : Tests end-to-end validés (3 modes + RBAC + Memory Bank + Git)
- [ ] Phase 10 : API Anthropic configurée, clé sécurisée dans VS Code SecretStorage
- [ ] Phase 11 : Registre `prompts/` initialisé (7 SP canoniques)
- [ ] Phase 12 : `check-prompts-sync.ps1` → 6 PASS | 0 FAIL, hook pre-commit actif

**Le système UADF est opérationnel quand toutes les cases sont cochées.**

---

## Annexe A — Table des Références

| Réf. | Type | Titre / Identifiant | Description |
| :--- | :--- | :--- | :--- |
| [DOC1] | Document interne | `workbench/DOC1-PRD-Unified-Agentic-Framework.md` | Product Requirements Document v2.0 — source de toutes les exigences REQ-xxx implémentées dans ce plan |
| [DOC2] | Document interne | `workbench/DOC2-Architecture-Solution-Stack.md` | Architecture, Solution et Stack Technique v2.0 — justifie les choix techniques de chaque phase |
| [DOC3] | Document interne | `workbench/DOC3-Plan-Implementation-COMPLETE.md` | Ce document — Plan d'Implémentation Séquentiel Complet v3.0 (Phases 0–12) |
| [DOC4] | Document interne | `workbench/DOC4-Guide-Deploiement-Atelier.md` | Guide de Déploiement de l'Atelier sur projets nouveaux et existants |
| [SP-001] | System Prompt | `template/prompts/SP-001-ollama-modelfile-system.md` | System prompt du Modelfile Ollama — déployé en Phase 3 |
| [SP-002] | System Prompt | `template/prompts/SP-002-clinerules-global.md` | Contenu canonique du fichier `.clinerules` — déployé en Phase 5 |
| [SP-003] | System Prompt | `template/prompts/SP-003-persona-product-owner.md` | `roleDefinition` Product Owner — déployé en Phase 4 |
| [SP-004] | System Prompt | `template/prompts/SP-004-persona-scrum-master.md` | `roleDefinition` Scrum Master — déployé en Phase 4 |
| [SP-005] | System Prompt | `template/prompts/SP-005-persona-developer.md` | `roleDefinition` Developer — déployé en Phase 4 |
| [SP-006] | System Prompt | `template/prompts/SP-006-persona-qa-engineer.md` | `roleDefinition` QA Engineer — déployé en Phase 4 |
| [SP-007] | System Prompt | `template/prompts/SP-007-gem-gemini-roo-agent.md` | Instructions du Gem Gemini "Roo Code Agent" — déployé manuellement en Phase 7 |
| [OLLAMA-DL] | Téléchargement | https://ollama.com/download/windows | Installateur Ollama pour Windows — utilisé en Phase 1 |
| [QWEN3-32B] | Modèle LLM | `mychen76/qwen3_cline_roocode:32b` sur Ollama Hub | Modèle principal fine-tuné Tool Calling Roo Code — téléchargé en Phase 1 |
| [QWEN3-7B] | Modèle LLM | `qwen3:7b` sur Ollama Hub | Modèle secondaire pour Boomerang Tasks — téléchargé en Phase 1 |
| [ROOCODE-EXT] | Extension VS Code | Roo Code (marketplace VS Code) | Extension agentique — installée en Phase 0 |
| [FASTAPI] | Bibliothèque Python | `pip install fastapi uvicorn pyperclip` | Dépendances du proxy — installées en Phase 6 |
| [ANTHROPIC-KEY] | Documentation | https://console.anthropic.com | Console Anthropic pour générer la clé API — utilisée en Phase 10 |
| [ANTHROPIC-MODELS] | Documentation | https://docs.anthropic.com/en/docs/about-claude/models | Liste des modèles Claude disponibles — à consulter pour mettre à jour `claude-sonnet-4-6` |
| [GEMINI-GEMS] | Interface | https://gemini.google.com > Gems | Interface de création des Gems Gemini — utilisée en Phase 7 |
| [GIT-HOOKS] | Documentation | https://git-scm.com/docs/githooks | Documentation des hooks Git — utilisée en Phase 12 |
| [SEMVER] | Standard | Semantic Versioning (semver.org) | Convention MAJOR.MINOR.PATCH pour les fichiers SP et le workbench |

---

## Annexe B — Table des Abréviations

| Abréviation | Forme complète | Explication |
| :--- | :--- | :--- |
| **ADR** | Architecture Decision Record | Enregistrement horodaté d'une décision d'architecture. Stocké dans `memory-bank/decisionLog.md`. |
| **API** | Application Programming Interface | Interface de programmation. Trois APIs dans l'UADF : Ollama REST (locale), OpenAI-compatible (proxy), Anthropic HTTPS (cloud). |
| **ASGI** | Asynchronous Server Gateway Interface | Standard Python pour serveurs web asynchrones. FastAPI + Uvicorn = pile ASGI du proxy (Phase 6). |
| **DA** | Décision d'Architecture | Identifiant des décisions dans DOC2 (DA-001 à DA-014). Référencé dans les phases pour justifier les choix. |
| **GEM** | Gem Gemini | Profil personnalisé Gemini Web avec system prompt permanent. Créé en Phase 7 avec SP-007. |
| **GPU** | Graphics Processing Unit | Processeur graphique. `num_gpu 99` dans le Modelfile délègue l'inférence au GPU (Phase 3). |
| **HTTP** | HyperText Transfer Protocol | Protocole de communication. Le proxy écoute sur HTTP `localhost:8000` (Phase 6). |
| **JSON** | JavaScript Object Notation | Format de données structuré. Utilisé pour `.roomodes` (Phase 4) et les réponses API. |
| **LAAW** | Local Agentic Agile Workflow | Blueprint mychen76 — source d'inspiration pour la Memory Bank et les personas Agile. |
| **LLM** | Large Language Model | Grand modèle de langage. Trois modes dans l'UADF : Qwen3-32B, Gemini Pro, Claude Sonnet. |
| **MCP** | Model Context Protocol | Protocole d'extension Roo Code. Accessible uniquement au persona Developer. |
| **MD5** | Message Digest 5 | Algorithme de hachage. Utilisé par le proxy pour détecter les changements de presse-papiers (Phase 6). |
| **PO** | Product Owner | Persona Agile — vision produit, User Stories, backlog. Mode `product-owner` dans `.roomodes`. |
| **PRD** | Product Requirements Document | Document d'exigences produit. DOC1 est le PRD de l'UADF. |
| **RBAC** | Role-Based Access Control | Contrôle d'accès par rôles. Matrice définie en Phase 4 et dans DOC1 section 4.1. |
| **REQ** | Requirement (Exigence) | Identifiant des exigences dans DOC1. Chaque phase de ce document référence les REQ qu'elle implémente. |
| **SM** | Scrum Master | Persona Agile facilitateur pur — Memory Bank + Git uniquement, sans code ni tests. |
| **SP** | System Prompt | Fichier canonique du registre `template/prompts/` avec métadonnées YAML. |
| **SSE** | Server-Sent Events | Protocole de streaming HTTP serveur→client. Implémenté dans `proxy.py` v2.0 (Phase 6). |
| **UADF** | Unified Agentic Development Framework | Nom du système décrit dans ce document. |
| **VRAM** | Video Random Access Memory | Mémoire GPU. Qwen3-32B nécessite 8+ Go de VRAM (Phase 1, prérequis). |
| **YAML** | YAML Ain't Markup Language | Format de sérialisation lisible. Utilisé pour les en-têtes des fichiers SP (Phase 11). |

---

## Annexe C — Glossaire

| Terme | Définition |
| :--- | :--- |
| **Atelier (Workbench)** | Ce dépôt (`agentic-agile-workbench`). Contient les outils, règles et processus réutilisables. Ce plan d'implémentation décrit comment installer l'atelier sur une machine. |
| **Balises XML Roo Code** | Syntaxe d'action de Roo Code : `<write_to_file>`, `<read_file>`, `<execute_command>`, `<attempt_completion>`, etc. Validées en Phase 9 (tests end-to-end). |
| **Boomerang Tasks** | Mécanisme Roo Code de délégation de sous-tâches au modèle 7B. Configuré en Phase 8, testé en Phase 9. |
| **Commit Git** | Instantané versionné du dépôt. Chaque phase se termine par un commit avec message au format Conventional Commits. |
| **Conventional Commits** | Convention de messages de commit : `type(scope): description`. Types : `feat`, `fix`, `docs`, `chore`, `refactor`, `test`. |
| **Déterminisme** | Stabilité des réponses LLM. Obtenu via `temperature 0.15`, `min_p 0.03`, `top_p 0.95`, `repeat_penalty 1.1` dans le Modelfile (Phase 3). |
| **Fenêtre de contexte** | Capacité maximale de traitement simultané d'un LLM. Fixée à 128K tokens (`num_ctx 131072`) dans le Modelfile (Phase 3). |
| **Fine-tuning** | Entraînement spécialisé d'un LLM. `mychen76/qwen3_cline_roocode:32b` est fine-tuné pour le Tool Calling Roo Code (Phase 1). |
| **Gem Gemini** | Profil Gemini Web avec system prompt permanent (SP-007). Créé manuellement en Phase 7 — non versionné dans Git. |
| **Hook pre-commit** | Script Git exécuté avant chaque commit. Créé en Phase 12 — appelle `check-prompts-sync.ps1` et bloque si désynchronisation. |
| **Memory Bank** | 7 fichiers Markdown dans `memory-bank/` persistant le contexte entre sessions. Créés en Phase 5, utilisés dès Phase 9. |
| **Modelfile** | Fichier de configuration Ollama. Créé en Phase 3, compilé avec `ollama create uadf-agent -f Modelfile`. |
| **Mode Cloud** | Roo Code → API Anthropic directe (`claude-sonnet-4-6`). Configuré en Phase 10. |
| **Mode Local** | Roo Code → Ollama `localhost:11434` → Qwen3-32B. Configuré en Phase 8. |
| **Mode Proxy** | Roo Code → proxy FastAPI `localhost:8000` → presse-papiers → Gemini Web. Configuré en Phase 8. |
| **Persona Agile** | Mode Roo Code simulant un rôle Scrum. Défini dans `.roomodes` en Phase 4. |
| **Polling** | Vérification périodique du presse-papiers toutes les secondes dans `proxy.py` (Phase 6). |
| **Proxy** | Serveur FastAPI local (`proxy.py`) créé en Phase 6. Intercepte les requêtes Roo Code et les relaie vers Gemini Web. |
| **Registre de prompts** | Répertoire `template/prompts/` créé en Phase 11. Source de vérité unique pour tous les system prompts. |
| **Séquence VÉRIFIER→CRÉER→LIRE→AGIR** | Protocole obligatoire au démarrage de session. Défini dans REGLE 1 de `.clinerules` (Phase 5), validé en Phase 9. |
| **Token** | Unité de traitement LLM ≈ 0,75 mot. La fenêtre 128K tokens ≈ 96 000 mots. |
| **Tool Calling** | Capacité LLM à appeler des outils via balises XML. Qwen3-32B est fine-tuné pour le Tool Calling Roo Code. |
| **VS Code SecretStorage** | Stockage chiffré VS Code pour la clé API Anthropic. Configuré en Phase 10 — jamais dans Git. |
