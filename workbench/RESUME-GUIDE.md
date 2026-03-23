# RESUME GUIDE — Protocole de Reprise de Session
## Agentic Agile Workbench — Assembly Phases 0 à 12

**Tracker d'exécution :** [`EXECUTION-TRACKER.md`](./EXECUTION-TRACKER.md)
**Plan d'implémentation :** [`DOC3-BUILD-Workbench-Assembly-Phases.md`](./DOC3-BUILD-Workbench-Assembly-Phases.md)
**Version :** 1.0.0
**Créé le :** 2026-03-23

---

## PROTOCOLE DE REPRISE EN 5 ÉTAPES

> À exécuter **au début de chaque session**, sans exception, quelle que soit la durée de l'interruption.

### ÉTAPE R1 — Lire l'État Courant (30 secondes)

Ouvrir [`EXECUTION-TRACKER.md`](./EXECUTION-TRACKER.md) et lire **uniquement** la section `ÉTAT COURANT` :

```
Dernière mise à jour  : [DATE]
Phase en cours        : [Phase X — Nom]
Dernière étape faite  : [X.Y — Description]
Prochaine action      : [Étape exacte à reprendre]
Blocages actifs       : [Aucun | Description]
Dernier commit Git    : [hash — message]
Backend LLM actif     : [Ollama | Proxy Gemini | Claude API]
Projet cible          : [Chemin]
```

**→ La "Prochaine action" indique exactement où reprendre.**

---

### ÉTAPE R2 — Vérifier l'État Réel du Système (2 minutes)

Exécuter les vérifications correspondant à la phase en cours :

#### Si Phase 0-1 (Infrastructure) :
```powershell
# Vérifier Tailscale
tailscale status

# Vérifier SSH vers calypso
ssh calypso "ollama list"
```

#### Si Phase 2-5 (Projet Git + Memory Bank) :
```powershell
# Vérifier le dépôt Git
cd [CHEMIN_PROJET]
git log --oneline -5
git status

# Vérifier la Memory Bank
Test-Path "memory-bank/activeContext.md"
Get-Content "memory-bank/activeContext.md"
```

#### Si Phase 6-8 (Proxy + Roo Code) :
```powershell
# Vérifier que le proxy peut démarrer
cd [CHEMIN_PROJET]
.\venv\Scripts\Activate.ps1
python -c "import fastapi, uvicorn, pyperclip; print('OK')"

# Vérifier Ollama depuis pc
Invoke-WebRequest -Uri "http://calypso:11434/api/tags" -Method GET | Select-Object -ExpandProperty Content
```

#### Si Phase 9-12 (Tests + Prompts) :
```powershell
# Vérifier l'état Git
cd [CHEMIN_PROJET]
git log --oneline -10

# Vérifier les fichiers clés
Test-Path ".clinerules"
Test-Path ".roomodes"
Test-Path "proxy.py"
Test-Path "prompts/README.md"
```

---

### ÉTAPE R3 — Réconcilier si Nécessaire (si écart détecté)

Si l'état réel du système **diffère** de ce qu'indique le tracker :

1. **Le tracker est en avance sur la réalité** (ex: étape marquée `[x]` mais fichier absent) :
   - Remettre l'étape à `[ ]` dans le tracker
   - Reprendre depuis cette étape

2. **La réalité est en avance sur le tracker** (ex: fichier existe mais étape non cochée) :
   - Vérifier le critère de validation de l'étape
   - Si validé → cocher `[x]` dans le tracker
   - Continuer à la prochaine étape non cochée

3. **Blocage non résolu depuis la dernière session** :
   - Lire la section `BLOCAGES ET DÉCISIONS` du tracker
   - Appliquer la résolution documentée, ou chercher une nouvelle solution
   - Mettre à jour le statut du blocage

---

### ÉTAPE R4 — Reprendre l'Implémentation

1. Naviguer dans [`EXECUTION-TRACKER.md`](./EXECUTION-TRACKER.md) jusqu'à la phase en cours
2. Trouver la première étape avec statut `[ ]` ou `[-]`
3. Ouvrir [`DOC3-BUILD-Workbench-Assembly-Phases.md`](./DOC3-BUILD-Workbench-Assembly-Phases.md) à la section correspondante pour les instructions détaillées
4. Exécuter l'étape
5. Vérifier le critère de validation
6. Cocher `[x]` dans le tracker dès que validé

---

### ÉTAPE R5 — Mettre à Jour le Tracker en Fin de Session

Avant de fermer, mettre à jour **obligatoirement** :

1. **Section `ÉTAT COURANT`** — mettre à jour tous les champs
2. **Tableau `Résumé de progression`** — mettre à jour les compteurs d'étapes
3. **Section `JOURNAL DES SESSIONS`** — ajouter une entrée pour la session
4. **Section `BLOCAGES ET DÉCISIONS`** — documenter tout nouveau blocage

---

## RÉFÉRENCE RAPIDE — DÉPENDANCES ENTRE PHASES

```
Phase 0 (VS Code propre)
    └─→ Phase 4 (Roo Code doit être installé pour charger .roomodes)
    └─→ Phase 8 (Roo Code doit être configuré)

Phase 1 (Ollama sur calypso)
    └─→ Phase 3 (ollama create uadf-agent nécessite Ollama installé)
    └─→ Phase 8 Mode 1 (Roo Code → Ollama nécessite Ollama actif)

Phase 2 (Dépôt Git)
    └─→ TOUTES les phases suivantes (tout est versionné dans ce dépôt)

Phase 3 (Modelfile)
    └─→ Phase 8 Mode 1 (uadf-agent doit exister)
    └─→ Phase 11 SP-001 (cohérence Modelfile ↔ SP-001)

Phase 4 (.roomodes)
    └─→ Phase 9 Tests RBAC
    └─→ Phase 11 SP-003 à SP-006

Phase 5 (Memory Bank + .clinerules)
    └─→ Phase 9 (tests Memory Bank)
    └─→ Phase 11 SP-002

Phase 6 (proxy.py)
    └─→ Phase 7 (Gem Gemini utilise le proxy)
    └─→ Phase 8 Mode 2
    └─→ Phase 11 SP-007

Phase 7 (Gem Gemini)
    └─→ Phase 8 Mode 2 (test complet)
    └─→ Phase 9 Test E2E Mode 2

Phase 8 (Commutateur 3 modes)
    └─→ Phase 9 (tests des 3 modes)

Phase 9 (Tests E2E)
    └─→ Phase 10 (Mode 3 Claude testé ici)

Phase 10 (API Anthropic)
    └─→ Phase 9 Test E2E Mode 3 (si non fait)

Phase 11 (Registre prompts)
    └─→ Phase 12 (check-prompts-sync.ps1 vérifie les SP)

Phase 12 (Hook pre-commit)
    └─→ Fin — système complet
```

---

## RÉFÉRENCE RAPIDE — FICHIERS SOURCES À UTILISER

> Pour chaque phase, utiliser les fichiers du dépôt `agentic-agile-workbench` comme source canonique.
> **Ne pas recopier manuellement depuis DOC3** — les fichiers `template/` sont la version de référence à jour.

| Phase | Fichier à créer dans le projet | Source canonique dans le workbench |
| :---: | :--- | :--- |
| 3 | `Modelfile` | [`template/Modelfile`](../template/Modelfile) |
| 4 | `.roomodes` | [`template/.roomodes`](../template/.roomodes) |
| 5 | `.clinerules` | [`template/.clinerules`](../template/.clinerules) |
| 6 | `proxy.py` | [`template/proxy.py`](../template/proxy.py) ← **v2.1.0** |
| 6 | `requirements.txt` | [`template/requirements.txt`](../template/requirements.txt) |
| 6 | `scripts/start-proxy.ps1` | [`template/scripts/start-proxy.ps1`](../template/scripts/start-proxy.ps1) |
| 7 | Gem Gemini Instructions | [`template/prompts/SP-007-gem-gemini-roo-agent.md`](../template/prompts/SP-007-gem-gemini-roo-agent.md) |
| 11 | `prompts/` (dossier entier) | [`template/prompts/`](../template/prompts/) |
| 12 | `scripts/check-prompts-sync.ps1` | [`template/scripts/check-prompts-sync.ps1`](../template/scripts/check-prompts-sync.ps1) |

> **⚠️ Différence DOC3 vs template/ :** DOC3 contient le code `proxy.py` v2.0 (version de référence originale).
> Le fichier `template/proxy.py` est à la version **v2.1.0** avec 10 correctifs de robustesse.
> Toujours utiliser `template/proxy.py` pour le déploiement.

---

## RÉFÉRENCE RAPIDE — COMMANDES DE VÉRIFICATION PAR PHASE

### Phase 0
```powershell
git --version
python --version
pip --version
```

### Phase 1
```bash
# Sur calypso (SSH)
ollama --version
ollama list
sudo systemctl show ollama | grep Environment
```
```powershell
# Sur pc
Invoke-WebRequest -Uri "http://calypso:11434/api/tags" -Method GET | Select-Object -ExpandProperty Content
```

### Phase 2
```powershell
git log --oneline
git status
Get-ChildItem -Name
```

### Phase 3
```bash
# Sur calypso
ollama show uadf-agent --modelfile | grep -E "num_ctx|temperature"
```

### Phase 4
```powershell
# Vérifier que .roomodes est valide JSON
Get-Content ".roomodes" | ConvertFrom-Json | Select-Object -ExpandProperty customModes | Select-Object slug, name
```

### Phase 5
```powershell
Get-ChildItem "memory-bank/" -Name
Get-Content "memory-bank/activeContext.md"
Get-Content "memory-bank/progress.md"
```

### Phase 6
```powershell
.\venv\Scripts\Activate.ps1
python proxy.py &
Start-Sleep 2
Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get
Invoke-RestMethod -Uri "http://localhost:8000/v1/models" -Method Get
```

### Phase 7
```
# Vérification manuelle dans Chrome :
# 1. Ouvrir https://gemini.google.com > Gems > "Roo Code Agent"
# 2. Envoyer : "Lis le fichier memory-bank/activeContext.md"
# 3. Vérifier que la réponse contient UNIQUEMENT <read_file>...</read_file>
```

### Phase 8
```powershell
# Mode 1 — Vérifier Ollama accessible
Invoke-WebRequest -Uri "http://calypso:11434/api/tags" -Method GET

# Mode 2 — Vérifier proxy actif
Invoke-RestMethod -Uri "http://localhost:8000/health"
```

### Phase 9
```powershell
Test-Path "src/hello.py"
git log --oneline -5
Get-Content "memory-bank/activeContext.md"
Get-ChildItem "docs/qa/" -Name
```

### Phase 10
```powershell
# Vérifier absence de la clé API dans les fichiers
Select-String -Path "*.py", "*.md", "*.json", "*.txt", "*.env" -Pattern "sk-ant-api" -Recurse
# Doit retourner AUCUN résultat
```

### Phase 11
```powershell
Get-ChildItem "prompts/" -Name
# Doit afficher 8 fichiers : README.md + SP-001 à SP-007
```

### Phase 12
```powershell
powershell.exe -ExecutionPolicy Bypass -File "scripts/check-prompts-sync.ps1"
# Doit afficher : 6 PASS | 0 FAIL | 1 WARN
```

---

## SCÉNARIOS DE REPRISE COURANTS

### Scénario A — Reprise après interruption courte (< 1 jour)

1. Lire `ÉTAT COURANT` dans le tracker
2. Exécuter les vérifications de la phase en cours (section ci-dessus)
3. Reprendre à la "Prochaine action"

### Scénario B — Reprise après longue interruption (> 1 semaine)

1. Lire `ÉTAT COURANT` dans le tracker
2. Lire le `JOURNAL DES SESSIONS` (dernière entrée)
3. Exécuter **toutes** les vérifications des phases complétées pour confirmer l'état
4. Vérifier que Tailscale est actif et `calypso` accessible
5. Vérifier que le dépôt Git est propre (`git status`)
6. Reprendre à la "Prochaine action"

### Scénario C — Reprise sur une nouvelle machine

1. Cloner le dépôt `agentic-agile-workbench`
2. Lire `ÉTAT COURANT` dans le tracker
3. Identifier le projet cible (section `INFORMATIONS DE CONFIGURATION`)
4. Cloner ou accéder au dépôt du projet cible
5. Recréer le hook pre-commit si Phase 12 est complète (étape 12.2)
6. Recréer l'environnement Python (`python -m venv venv && pip install -r requirements.txt`)
7. Reprendre à la "Prochaine action"

### Scénario D — Blocage sur une étape

1. Documenter le blocage dans la section `BLOCAGES ET DÉCISIONS` du tracker
2. Marquer l'étape avec `[!]` dans le tracker
3. Mettre à jour `ÉTAT COURANT` avec le blocage
4. Consulter [`DOC3-BUILD-Workbench-Assembly-Phases.md`](./DOC3-BUILD-Workbench-Assembly-Phases.md) pour les notes de dépannage de la phase
5. Si le blocage est sur `calypso` : vérifier `sudo systemctl status ollama` et les logs
6. Si le blocage est sur le proxy : vérifier les logs Python et `pip list`
7. Une fois résolu : mettre à jour le statut du blocage, remettre l'étape à `[ ]`, reprendre

### Scénario E — Régression (une étape validée ne fonctionne plus)

1. Identifier la phase affectée
2. Remettre les étapes concernées à `[ ]` dans le tracker
3. Documenter dans `BLOCAGES ET DÉCISIONS`
4. Exécuter les vérifications de la phase (section ci-dessus)
5. Reprendre depuis la première étape défaillante

---

## POINTS D'ATTENTION CRITIQUES

> Ces points sont les causes les plus fréquentes d'échec ou de confusion lors d'une reprise.

### 1. Tailscale doit être actif AVANT toute opération sur `calypso`
```powershell
tailscale status
# calypso doit apparaître comme pair actif
```
Si Tailscale est inactif, toutes les opérations Ollama (Phases 1, 3, 8 Mode 1) échoueront.

### 2. L'environnement virtuel Python doit être activé AVANT de lancer proxy.py
```powershell
.\venv\Scripts\Activate.ps1
# Le prompt doit afficher (venv)
python proxy.py
```
Sans activation, `import fastapi` échouera.

### 3. Le hook pre-commit n'est PAS versionné dans Git
Après un `git clone` du projet cible, recréer le hook manuellement (étape 12.2 de DOC3).
Le hook est dans `.git/hooks/pre-commit` — ce dossier est exclu de Git.

### 4. La clé API Anthropic ne doit JAMAIS être dans un fichier
Elle est stockée uniquement dans VS Code SecretStorage.
Vérification : `Select-String -Pattern "sk-ant-api" -Recurse` → doit retourner vide.

### 5. Utiliser template/proxy.py (v2.1.0), pas le code de DOC3 (v2.0)
DOC3 contient la version de référence originale v2.0 à titre documentaire.
Le fichier déployable est [`template/proxy.py`](../template/proxy.py) (v2.1.0 avec 10 correctifs).

### 6. Le Gem Gemini doit être recréé manuellement si le compte Google change
SP-007 est le seul prompt non versionnable dans Git.
Source : [`template/prompts/SP-007-gem-gemini-roo-agent.md`](../template/prompts/SP-007-gem-gemini-roo-agent.md).

### 7. Après chaque étape significative : commit Git
Le tracker note les hash de commit pour chaque phase.
Si un hash est manquant, exécuter `git log --oneline -5` pour le retrouver.

---

## STRUCTURE DES FICHIERS DE SUIVI

```
workbench/
├── EXECUTION-TRACKER.md   ← CE FICHIER EST LA SOURCE DE VÉRITÉ DE L'ÉTAT
│                             Mettre à jour à chaque fin de session
├── RESUME-GUIDE.md        ← CE FICHIER (protocole de reprise)
│                             Ne pas modifier sauf pour corriger des erreurs
└── DOC3-BUILD-Workbench-Assembly-Phases.md
                           ← Instructions détaillées de chaque étape
                             Référence en lecture seule pendant l'implémentation
```

---

## MISE À JOUR DU TRACKER — TEMPLATE COPIER-COLLER

### Mise à jour de la section ÉTAT COURANT

```markdown
## ÉTAT COURANT

> **⚠️ METTRE À JOUR CETTE SECTION À CHAQUE FIN DE SESSION**

```
Dernière mise à jour  : YYYY-MM-DD
Dernière session      : Session N — YYYY-MM-DD
Phase en cours        : Phase X — [Nom de la phase]
Dernière étape faite  : X.Y — [Description courte]
Prochaine action      : Phase X, Étape X.Z — [Description]
Blocages actifs       : [Aucun | Description du blocage]
Dernier commit Git    : [abc1234] — [message du commit]
Backend LLM actif     : [Ollama uadf-agent | Proxy Gemini | Claude API | Non configuré]
Projet cible          : C:\Users\[user]\AGENTIC_DEVELOPMENT_PROJECTS\PROJECTS\[nom-projet]
```
```

### Ajout d'une entrée dans JOURNAL DES SESSIONS

```markdown
### Session N — YYYY-MM-DD — [~Xh]
**Phases travaillées :** Phase X à Phase Y
**Étapes complétées :** X.1, X.2, X.3, Y.1, Y.2
**Dernier commit :** abc1234 — feat(scope): description
**État en fin de session :** [Description précise de l'état du système]
**Prochaine action :** Phase Y, Étape Y.3 — [Description]
**Blocages :** [Aucun | Description et statut]
```

### Ajout d'un blocage dans BLOCAGES ET DÉCISIONS

```markdown
### YYYY-MM-DD — Phase X.Y — [Titre court du blocage]
**Type :** Blocage
**Description :** [Ce qui s'est passé exactement]
**Résolution :** [Comment résolu, ou "En attente — [prochaine tentative]"]
**Impact :** [Phases X, Y affectées]
```

---

*Fin du fichier RESUME-GUIDE.md — Version 1.0.0*
