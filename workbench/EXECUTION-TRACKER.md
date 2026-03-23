# EXECUTION TRACKER — Agentic Agile Workbench Assembly
## Suivi d'Exécution des Phases 0 à 12

**Référence :** [`DOC3-BUILD-Workbench-Assembly-Phases.md`](./DOC3-BUILD-Workbench-Assembly-Phases.md)
**Guide de reprise :** [`RESUME-GUIDE.md`](./RESUME-GUIDE.md)
**Version du tracker :** 1.0.0
**Créé le :** 2026-03-23

---

## 🔴 COMMENT UTILISER CE FICHIER

1. **Au démarrage de chaque session :** Lire la section [ÉTAT COURANT](#état-courant) en premier
2. **Pendant l'exécution :** Cocher chaque étape dès qu'elle est **validée** (critère de validation satisfait)
3. **À la fin de chaque session :** Mettre à jour la section [ÉTAT COURANT](#état-courant) avant de fermer
4. **En cas de blocage :** Documenter dans la section [BLOCAGES ET DÉCISIONS](#blocages-et-décisions)

### Légende des statuts
| Symbole | Signification |
| :---: | :--- |
| `[ ]` | À faire |
| `[-]` | En cours (session active) |
| `[x]` | Terminé et validé |
| `[!]` | Bloqué — voir section Blocages |
| `[~]` | Ignoré volontairement (avec justification) |

---

## ÉTAT COURANT

> **⚠️ METTRE À JOUR CETTE SECTION À CHAQUE FIN DE SESSION**

```
Dernière mise à jour  : 2026-03-23
Dernière session      : [À remplir]
Phase en cours        : Phase 0 — Pas encore commencé
Dernière étape faite  : Aucune
Prochaine action      : Commencer Phase 0, Étape 0.1
Blocages actifs       : Aucun
Dernier commit Git    : [Aucun — dépôt non encore initialisé]
Backend LLM actif     : [Non configuré]
Projet cible          : [Chemin du projet à remplir]
```

### Résumé de progression
| Phase | Nom | Statut | Étapes complètes |
| :---: | :--- | :---: | :---: |
| 0 | Base Saine VS Code + Roo Code | `[ ]` | 0/8 |
| 1 | Infrastructure Ollama + Modèles | `[ ]` | 0/6 |
| 2 | Dépôt Git du Projet | `[ ]` | 0/5 |
| 3 | Modelfile Ollama Personnalisé | `[ ]` | 0/4 |
| 4 | Personas Agile (.roomodes) | `[ ]` | 0/4 |
| 5 | Memory Bank (.clinerules + 7 fichiers) | `[ ]` | 0/11 |
| 6 | Proxy Gemini Chrome (proxy.py) | `[ ]` | 0/6 |
| 7 | Configuration Gem Gemini | `[ ]` | 0/3 |
| 8 | Roo Code Commutateur 3 Modes LLM | `[ ]` | 0/4 |
| 9 | Tests End-to-End | `[ ]` | 0/4 |
| 10 | API Anthropic Claude Sonnet | `[ ]` | 0/5 |
| 11 | Registre Central des Prompts | `[ ]` | 0/4 |
| 12 | Vérification Automatique Cohérence | `[ ]` | 0/5 |

**Progression globale : 0 / 73 étapes complètes**

---

## PHASE 0 — Base Saine : VS Code + Roo Code

**Objectif :** Partir d'un environnement VS Code et Roo Code propre.
**Exigences :** REQ-000
**Machine :** `pc` (laptop Windows)
**Statut phase :** `[ ]`

| # | Étape | Statut | Notes / Résultat |
| :---: | :--- | :---: | :--- |
| 0.1 | Sauvegarder les paramètres VS Code actuels (optionnel) | `[ ]` | Backup créé dans : |
| 0.2 | Désinstaller toutes les versions Roo Code / Cline | `[ ]` | |
| 0.3 | Nettoyer le cache et les données Roo Code | `[ ]` | |
| 0.4 | Nettoyer les paramètres VS Code résiduels dans settings.json | `[ ]` | |
| 0.5 | Réinstaller VS Code (si nécessaire) | `[~]` | Ignorer si VS Code stable |
| 0.6 | Installer la dernière version de Roo Code | `[ ]` | Version installée : |
| 0.7 | Vérifier l'état propre de Roo Code (pas de clé API pré-remplie) | `[ ]` | |
| 0.8 | Vérifier Git et Python (`git --version`, `python --version`) | `[ ]` | Git: / Python: |

**Critère de validation Phase 0 :**
- [ ] Icône Roo Code visible dans la barre latérale VS Code
- [ ] Aucune clé API pré-remplie dans les paramètres Roo Code
- [ ] `git --version` retourne un numéro de version
- [ ] `python --version` retourne un numéro de version

---

## PHASE 1 — Infrastructure Système : Ollama sur `calypso`

**Objectif :** Installer Ollama sur `calypso` et télécharger les modèles LLM.
**Exigences :** REQ-1.0, REQ-1.1, REQ-1.2
**Machine :** `calypso` (via SSH depuis `pc`)
**Prérequis :** Tailscale actif sur les deux machines
**Statut phase :** `[ ]`

| # | Étape | Statut | Notes / Résultat |
| :---: | :--- | :---: | :--- |
| 1.1 | Se connecter à `calypso` via SSH (`ssh calypso`) | `[ ]` | |
| 1.2 | Installer Ollama sur `calypso` (`curl -fsSL https://ollama.com/install.sh \| sh`) | `[ ]` | Version installée : |
| 1.3 | Configurer `OLLAMA_HOST=0.0.0.0:11434` dans systemd | `[ ]` | |
| 1.4 | Télécharger modèle principal `mychen76/qwen3_cline_roocode:32b` (~20 Go) | `[ ]` | Durée : |
| 1.5 | Télécharger modèle secondaire `qwen3:7b` | `[ ]` | |
| 1.6 | Vérifier API Ollama accessible depuis `pc` via Tailscale | `[ ]` | |

**Critère de validation Phase 1 :**
- [ ] `ollama --version` répond sur `calypso`
- [ ] `ollama list` affiche `mychen76/qwen3_cline_roocode:32b`
- [ ] `ollama list` affiche `qwen3:7b`
- [ ] `Invoke-WebRequest -Uri "http://calypso:11434/api/tags"` répond depuis `pc`

---

## PHASE 2 — Création du Dépôt Git du Projet

**Objectif :** Créer le dépôt Git qui versionnera tout le projet.
**Exigences :** REQ-000, REQ-4.1, REQ-4.5
**Machine :** `pc`
**Statut phase :** `[ ]`

| # | Étape | Statut | Notes / Résultat |
| :---: | :--- | :---: | :--- |
| 2.1 | Créer le dossier du projet | `[ ]` | Chemin : |
| 2.2 | Initialiser Git (`git init`, configurer user.name et user.email) | `[ ]` | |
| 2.3 | Créer le fichier `.gitignore` complet | `[ ]` | |
| 2.4 | Créer la structure de dossiers (`memory-bank/`, `docs/`, `scripts/`, `prompts/`) | `[ ]` | |
| 2.5 | Premier commit : squelette du projet | `[ ]` | Hash commit : |

**Critère de validation Phase 2 :**
- [ ] `git log --oneline` affiche le commit initial
- [ ] Les dossiers `memory-bank/`, `docs/`, `scripts/`, `prompts/` existent

---

## PHASE 3 — Modelfile et Modèle Personnalisé Ollama

**Objectif :** Créer le modèle `uadf-agent` avec paramètres de déterminisme et contexte 128K.
**Exigences :** REQ-1.2, REQ-1.3
**Machine :** `pc` (création fichier) + `calypso` (compilation)
**Statut phase :** `[ ]`

| # | Étape | Statut | Notes / Résultat |
| :---: | :--- | :---: | :--- |
| 3.1 | Créer le fichier `Modelfile` à la racine du projet | `[ ]` | |
| 3.2 | Compiler le modèle sur `calypso` (`ollama create uadf-agent -f Modelfile`) | `[ ]` | Durée : |
| 3.3 | Tester le modèle (`ollama run uadf-agent "Dis bonjour en une phrase."`) | `[ ]` | |
| 3.4 | Versionner le Modelfile (`git commit`) | `[ ]` | Hash commit : |

**Critère de validation Phase 3 :**
- [ ] `ollama show uadf-agent --modelfile` affiche `PARAMETER num_ctx 131072`
- [ ] `ollama show uadf-agent --modelfile` affiche `PARAMETER temperature 0.15`
- [ ] `ollama run uadf-agent "Dis bonjour"` répond correctement

---

## PHASE 4 — Personas Agile : Fichier `.roomodes`

**Objectif :** Créer les 4 personas Agile avec RBAC et obligation Git.
**Exigences :** REQ-3.1, REQ-3.2, REQ-3.3, REQ-3.4
**Machine :** `pc`
**Statut phase :** `[ ]`

| # | Étape | Statut | Notes / Résultat |
| :---: | :--- | :---: | :--- |
| 4.1 | Créer le fichier `.roomodes` | `[ ]` | |
| 4.2 | Insérer la configuration JSON des 4 personas | `[ ]` | |
| 4.3 | Vérifier le chargement des modes dans Roo Code (4 personas visibles) | `[ ]` | |
| 4.4 | Versionner `.roomodes` (`git commit`) | `[ ]` | Hash commit : |

**Critère de validation Phase 4 :**
- [ ] Mode "Product Owner" visible dans Roo Code
- [ ] Mode "Scrum Master" visible dans Roo Code
- [ ] Mode "Developer" visible dans Roo Code
- [ ] Mode "QA Engineer" visible dans Roo Code
- [ ] Product Owner refuse "Écris du code Python"
- [ ] Scrum Master refuse "Lance pytest"
- [ ] QA Engineer refuse "Modifie src/main.py"

---

## PHASE 5 — Memory Bank : `.clinerules` + 7 Fichiers Markdown

**Objectif :** Créer le système de mémoire persistante et les directives globales.
**Exigences :** REQ-4.1 à REQ-4.5, REQ-7.3
**Machine :** `pc`
**Statut phase :** `[ ]`

| # | Étape | Statut | Notes / Résultat |
| :---: | :--- | :---: | :--- |
| 5.1 | Créer le fichier `.clinerules` avec les 6 règles | `[ ]` | |
| 5.2 | Créer la structure `memory-bank/` avec les 7 fichiers | `[ ]` | |
| 5.3 | Remplir `memory-bank/projectBrief.md` | `[ ]` | |
| 5.4 | Remplir `memory-bank/productContext.md` | `[ ]` | |
| 5.5 | Remplir `memory-bank/systemPatterns.md` | `[ ]` | |
| 5.6 | Remplir `memory-bank/techContext.md` | `[ ]` | |
| 5.7 | Remplir `memory-bank/activeContext.md` | `[ ]` | |
| 5.8 | Remplir `memory-bank/progress.md` | `[ ]` | |
| 5.9 | Remplir `memory-bank/decisionLog.md` | `[ ]` | |
| 5.10 | Créer le dossier `docs/qa/` avec `.gitkeep` | `[ ]` | |
| 5.11 | Versionner Memory Bank et `.clinerules` (`git commit`) | `[ ]` | Hash commit : |

**Critère de validation Phase 5 :**
- [ ] `.clinerules` existe à la racine du projet
- [ ] Les 7 fichiers `memory-bank/*.md` existent et sont remplis
- [ ] En mode Developer, l'agent lit automatiquement `activeContext.md` et `progress.md`
- [ ] "Quel est l'état du projet ?" → réponse basée sur `progress.md`

---

## PHASE 6 — Proxy Gemini Chrome : `proxy.py` v2.1.0

**Objectif :** Créer le serveur proxy FastAPI relayant Roo Code vers Gemini Chrome.
**Exigences :** REQ-2.1.1 à REQ-2.4.4
**Machine :** `pc`
**Statut phase :** `[ ]`

| # | Étape | Statut | Notes / Résultat |
| :---: | :--- | :---: | :--- |
| 6.1 | Créer l'environnement virtuel Python (`python -m venv venv`) | `[ ]` | |
| 6.2 | Installer les dépendances (`pip install fastapi uvicorn pyperclip pydantic`) | `[ ]` | |
| 6.3 | Créer `proxy.py` v2.1.0 (copier depuis `template/proxy.py`) | `[ ]` | Version : v2.1.0 |
| 6.4 | Créer le script `scripts/start-proxy.ps1` | `[ ]` | |
| 6.5 | Tester le proxy (`/health` et `/v1/models`) | `[ ]` | |
| 6.6 | Versionner `proxy.py`, `requirements.txt`, `scripts/` | `[ ]` | Hash commit : |

**Critère de validation Phase 6 :**
- [ ] `python proxy.py` démarre sans erreur
- [ ] `http://localhost:8000/health` → `{"status": "ok"}`
- [ ] `http://localhost:8000/v1/models` → liste avec `"id": "gemini-manual"`

> **Note :** Utiliser `template/proxy.py` du dépôt workbench (version v2.1.0 avec 10 correctifs).
> Ne pas utiliser le code v2.0 de DOC3 qui est la version de référence originale.

---

## PHASE 7 — Configuration Gem Gemini Chrome

**Objectif :** Créer le Gem Gemini "Roo Code Agent" avec system prompt intégré.
**Exigences :** REQ-5.1, REQ-5.2, REQ-5.3
**Machine :** `pc` (Chrome)
**Statut phase :** `[ ]`

| # | Étape | Statut | Notes / Résultat |
| :---: | :--- | :---: | :--- |
| 7.1 | Créer le Gem "Roo Code Agent" sur gemini.google.com avec SP-007 | `[ ]` | URL Gem : |
| 7.2 | Vérifier que le Gem répond avec balises XML (test `<read_file>`) | `[ ]` | |
| 7.3 | Configurer Chrome (épingler onglet, workflow copier-coller documenté) | `[ ]` | |

**Critère de validation Phase 7 :**
- [ ] Gem "Roo Code Agent" créé et sauvegardé
- [ ] Test `"Lis le fichier memory-bank/activeContext.md"` → réponse avec `<read_file>` uniquement
- [ ] Workflow copier-coller compris et testé manuellement

> **⚠️ DÉPLOIEMENT MANUEL OBLIGATOIRE :** Le contenu du Gem provient de
> [`template/prompts/SP-007-gem-gemini-roo-agent.md`](../template/prompts/SP-007-gem-gemini-roo-agent.md).
> Ce prompt ne peut pas être déployé via Git — vérification manuelle requise.

---

## PHASE 8 — Roo Code : Commutateur 3 Modes LLM

**Objectif :** Configurer Roo Code pour basculer entre les 3 backends LLM.
**Exigences :** REQ-2.0, REQ-6.0
**Machine :** `pc`
**Statut phase :** `[ ]`

| # | Étape | Statut | Notes / Résultat |
| :---: | :--- | :---: | :--- |
| 8.1 | Configurer Mode 1 : Ollama Local (`http://calypso:11434`, `uadf-agent`) | `[ ]` | |
| 8.2 | Configurer Mode 2 : Proxy Gemini (`http://localhost:8000/v1`, `gemini-manual`) | `[ ]` | |
| 8.3 | Configurer Mode 3 : API Anthropic Claude (voir Phase 10) | `[~]` | Reporté à Phase 10 |
| 8.4 | Documenter le commutateur dans `memory-bank/techContext.md` + commit | `[ ]` | Hash commit : |

**Critère de validation Phase 8 :**
- [ ] Mode 1 : Roo Code répond via Ollama (`uadf-agent` visible dans logs Ollama)
- [ ] Mode 2 : Proxy affiche `PROMPT COPIE !` lors d'une requête Roo Code
- [ ] `memory-bank/techContext.md` mis à jour avec les URLs réelles

---

## PHASE 9 — Tests End-to-End : Validation Complète

**Objectif :** Valider les 3 modes LLM avec Memory Bank, personas RBAC et Git.
**Exigences :** REQ-000, REQ-4.2, REQ-4.3
**Machine :** `pc`
**Statut phase :** `[ ]`

| # | Étape | Statut | Notes / Résultat |
| :---: | :--- | :---: | :--- |
| 9.1 | Test E2E Mode 1 (Ollama) : créer `src/hello.py` + Memory Bank + Git | `[ ]` | |
| 9.2 | Test E2E Mode 2 (Proxy Gemini) : créer rapport QA + RBAC | `[ ]` | |
| 9.3 | Test RBAC complet (tableau 6 scénarios) | `[ ]` | |
| 9.4 | Versionner les résultats des tests | `[ ]` | Hash commit : |

**Critère de validation Phase 9 :**
- [ ] `src/hello.py` créé par l'agent en Mode 1
- [ ] `git log` affiche commit `feat(src): ajout hello.py`
- [ ] `memory-bank/activeContext.md` mis à jour après la session
- [ ] Rapport QA créé dans `docs/qa/` en Mode 2
- [ ] Les 6 scénarios RBAC du tableau 9.3 validés

**Tableau RBAC Phase 9.3 :**
| Mode | Demande | Attendu | Résultat |
| :--- | :--- | :--- | :--- |
| Product Owner | "Écris du code Python" | Refus | `[ ]` |
| Product Owner | "Crée une User Story" | Accepté | `[ ]` |
| Scrum Master | "Lance pytest" | Refus | `[ ]` |
| Scrum Master | "Quel est l'état des tests ?" | Accepté | `[ ]` |
| Developer | "Modifie src/hello.py" | Accepté | `[ ]` |
| QA Engineer | "Modifie src/hello.py" | Refus | `[ ]` |

---

## PHASE 10 — API Anthropic Claude : Mode Cloud Direct

**Objectif :** Configurer la connexion directe à l'API Anthropic (`claude-sonnet-4-6`).
**Exigences :** REQ-6.1, REQ-6.2, REQ-6.3, REQ-6.4
**Machine :** `pc`
**Statut phase :** `[ ]`

| # | Étape | Statut | Notes / Résultat |
| :---: | :--- | :---: | :--- |
| 10.1 | Obtenir une clé API Anthropic sur console.anthropic.com | `[ ]` | Clé créée (ne pas noter ici) |
| 10.2 | Configurer Roo Code avec la clé Anthropic et modèle `claude-sonnet-4-6` | `[ ]` | |
| 10.3 | Tester la connexion Anthropic (réponse sans intervention humaine) | `[ ]` | |
| 10.4 | Vérifier la sécurité : clé absente de tous les fichiers du projet | `[ ]` | `Select-String` → 0 résultat |
| 10.5 | Versionner la mise à jour de la Memory Bank | `[ ]` | Hash commit : |

**Critère de validation Phase 10 :**
- [ ] Roo Code répond via API Anthropic sans proxy
- [ ] `Select-String -Pattern "sk-ant-api" -Recurse` → aucun résultat
- [ ] Memory Bank mise à jour après la session de test

> **⚠️ SÉCURITÉ ABSOLUE :** La clé API (`sk-ant-api03-...`) ne doit JAMAIS apparaître
> dans un fichier du projet. VS Code SecretStorage uniquement.

---

## PHASE 11 — Registre Central des Prompts : `prompts/`

**Objectif :** Initialiser le registre centralisé des 7 system prompts canoniques.
**Exigences :** REQ-7.1 à REQ-7.5
**Machine :** `pc`
**Statut phase :** `[ ]`

| # | Étape | Statut | Notes / Résultat |
| :---: | :--- | :---: | :--- |
| 11.1 | Vérifier la structure `prompts/` (8 fichiers attendus) | `[ ]` | Fichiers présents : |
| 11.2 | Comprendre la structure d'un fichier SP canonique (en-tête YAML) | `[ ]` | |
| 11.3 | Vérifier la cohérence des prompts déployés vs SP canoniques | `[ ]` | |
| 11.4 | Versionner le registre des prompts (`git commit`) | `[ ]` | Hash commit : |

**Critère de validation Phase 11 :**
- [ ] `prompts/` contient 8 fichiers (README.md + SP-001 à SP-007)
- [ ] Chaque SP a un en-tête YAML valide (`id`, `version`, `target_file`, `target_field`)
- [ ] SP-007 est marqué `hors_git: true`
- [ ] Contenu de chaque SP correspond à l'artefact déployé

**Tableau de cohérence Phase 11.3 :**
| SP Canonique | Artefact Déployé | Vérifié |
| :--- | :--- | :---: |
| SP-001 | `Modelfile` bloc `SYSTEM """..."""` | `[ ]` |
| SP-002 | `.clinerules` (fichier entier) | `[ ]` |
| SP-003 | `.roomodes` > `product-owner` roleDefinition | `[ ]` |
| SP-004 | `.roomodes` > `scrum-master` roleDefinition | `[ ]` |
| SP-005 | `.roomodes` > `developer` roleDefinition | `[ ]` |
| SP-006 | `.roomodes` > `qa-engineer` roleDefinition | `[ ]` |
| SP-007 | Gem Gemini "Roo Code Agent" > Instructions | `[ ]` |

---

## PHASE 12 — Vérification Automatique : `check-prompts-sync.ps1` + Hook Git

**Objectif :** Script de vérification de cohérence des prompts + hook pre-commit.
**Exigences :** REQ-8.1 à REQ-8.4
**Machine :** `pc`
**Statut phase :** `[ ]`

| # | Étape | Statut | Notes / Résultat |
| :---: | :--- | :---: | :--- |
| 12.1 | Créer `scripts/check-prompts-sync.ps1` (copier depuis `template/scripts/`) | `[ ]` | |
| 12.2 | Créer le hook Git `.git/hooks/pre-commit` | `[ ]` | |
| 12.3 | Tester le script manuellement (sortie attendue : 6 PASS \| 0 FAIL) | `[ ]` | Résultat : PASS / FAIL |
| 12.4 | Tester le blocage du commit en cas de désynchronisation | `[ ]` | |
| 12.5 | Versionner `scripts/check-prompts-sync.ps1` | `[ ]` | Hash commit : |

**Critère de validation Phase 12 :**
- [ ] `scripts/check-prompts-sync.ps1` → `6 PASS | 0 FAIL | 1 WARN`
- [ ] Commit avec `.clinerules` modifié → bloqué par le hook
- [ ] Restauration de `.clinerules` → commit débloqué

> **Note :** Le hook `.git/hooks/pre-commit` n'est PAS versionné dans Git.
> Chaque développeur qui clone le dépôt doit recréer le hook (étape 12.2).

---

## CHECKLIST DE VALIDATION FINALE

> Cocher uniquement quand **tous** les critères de validation de la phase sont satisfaits.

- [ ] **Phase 0** : VS Code + Roo Code réinstallés proprement
- [ ] **Phase 1** : Ollama + `uadf-agent` (32B) + `qwen3:7b` installés sur `calypso`
- [ ] **Phase 2** : Dépôt Git initialisé avec `.gitignore` complet
- [ ] **Phase 3** : `Modelfile` compilé (`ollama create uadf-agent -f Modelfile`)
- [ ] **Phase 4** : `.roomodes` avec 4 personas RBAC validés
- [ ] **Phase 5** : Memory Bank (7 fichiers) + `.clinerules` (6 règles) — séquence VÉRIFIER→CRÉER→LIRE→AGIR validée
- [ ] **Phase 6** : `proxy.py` v2.1.0 démarre et répond sur `/health`
- [ ] **Phase 7** : Gem Gemini "Roo Code Agent" créé et répond avec balises XML
- [ ] **Phase 8** : Commutateur 3 modes configuré dans Roo Code
- [ ] **Phase 9** : Tests end-to-end validés (3 modes + RBAC + Memory Bank + Git)
- [ ] **Phase 10** : API Anthropic configurée, clé sécurisée dans VS Code SecretStorage
- [ ] **Phase 11** : Registre `prompts/` initialisé (7 SP canoniques)
- [ ] **Phase 12** : `check-prompts-sync.ps1` → 6 PASS | 0 FAIL, hook pre-commit actif

**🎯 Le système Agentic Agile Workbench est opérationnel quand toutes les cases sont cochées.**

---

## BLOCAGES ET DÉCISIONS

> Documenter ici tout blocage rencontré, décision prise, ou déviation par rapport à DOC3.

### Format d'entrée
```
### [DATE] — [PHASE X.Y] — [Titre court]
**Type :** Blocage | Décision | Déviation
**Description :** [Ce qui s'est passé]
**Résolution :** [Comment résolu, ou "En attente"]
**Impact :** [Phases affectées, si applicable]
```

*(Aucun blocage enregistré pour l'instant)*

---

## JOURNAL DES SESSIONS

> Une entrée par session de travail. Mettre à jour à chaque fin de session.

### Format d'entrée
```
### Session [N] — [DATE] — [Durée approximative]
**Phases travaillées :** Phase X à Phase Y
**Étapes complétées :** X.1, X.2, X.3, Y.1
**Dernier commit :** [hash] — [message]
**État en fin de session :** [Description de l'état exact]
**Prochaine action :** [Étape exacte à reprendre]
**Blocages :** [Aucun | Description]
```

*(Aucune session enregistrée — implémentation non encore commencée)*

---

## INFORMATIONS DE CONFIGURATION

> Remplir au fur et à mesure de l'implémentation. Ces informations sont nécessaires pour reprendre après une longue interruption.

| Paramètre | Valeur | Rempli en Phase |
| :--- | :--- | :---: |
| Chemin du projet cible | | 2.1 |
| Adresse IP Tailscale de `calypso` | | 1.1 |
| Version Ollama installée | | 1.2 |
| Version Roo Code installée | | 0.6 |
| Version Git installée | | 0.8 |
| Version Python installée | | 0.8 |
| Nom du modèle Ollama principal | `mychen76/qwen3_cline_roocode:32b` | 1.4 |
| Nom du modèle compilé | `uadf-agent` | 3.2 |
| URL Ollama (depuis `pc`) | `http://calypso:11434` | 1.6 |
| URL Proxy Gemini | `http://localhost:8000/v1` | 6.5 |
| Modèle Proxy Gemini | `gemini-manual` | 8.2 |
| Modèle Anthropic | `claude-sonnet-4-6` | 10.2 |
| URL Gem Gemini | | 7.1 |
| Hash du dernier commit | | En cours |

---

*Fin du fichier EXECUTION-TRACKER.md — Version 1.0.0*