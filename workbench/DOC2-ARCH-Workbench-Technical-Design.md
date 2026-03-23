# Document 2 : Architecture, Solution et Stack Technique
## Agentic Agile Workbench

**Nom du Projet :** Agentic Agile Workbench
**Version :** 2.0 — Refactorisé (arbitrages intégrés, streaming SSE, RBAC précis)
**Date :** 2026-03-23
**Référence PRD :** DOC1-PRD-Workbench-Requirements.md v2.0

---

## 1. Principe Directeur

**Roo Code est le seul et unique moteur d'exécution agentique.** Tous les autres composants (moteur LLM local, proxy clipboard, API cloud, Memory Bank, personas Agile) sont des **fournisseurs de services** qui s'interfacent avec Roo Code via des protocoles standardisés.

Ce principe garantit que :
- Le comportement de Roo Code n'est jamais modifié, quelle que soit la source LLM utilisée.
- Le basculement entre les trois backends (Ollama local, Proxy Gemini Chrome, API Anthropic Claude) est transparent pour Roo Code — seul le paramètre "API Provider" change.
- La Memory Bank et les personas Agile fonctionnent identiquement dans les trois modes.

---

## 2. Diagramme d'Architecture Globale

```
+-----------------------------------------------------------------------------------+
|                           LAPTOP WINDOWS (VS Code)                                |
|                                                                                   |
|  +--------------------------------------------------------------------------+    |
|  |                      ROO CODE (Extension VS Code)                        |    |
|  |                                                                          |    |
|  |  +-------------+  +--------------+  +----------------------------+      |    |
|  |  |  .roomodes  |  | .clinerules  |  |   Memory Bank Reader       |      |    |
|  |  |  (4 Personas|  |  (6 Regles   |  |   (Lecture/Ecriture .md)   |      |    |
|  |  |   Agile)    |  |   imperatives|  |                            |      |    |
|  |  +-------------+  +--------------+  +----------------------------+      |    |
|  |                                                                          |    |
|  |    API OpenAI-Compatible (HTTP)         API Anthropic (HTTPS)            |    |
|  +------------------+-----------------------+----------------+--------------+    |
|                     |                                        |                   |
|         +-----------+------------+                           |                   |
|         |    COMMUTATEUR LLM     |  (Parametre Provider      |                   |
|         |    (3 modes)           |   dans Roo Code)          |                   |
|         +-----------+------------+                           |                   |
|                     |                                        |                   |
|       +-------------+-------------+                          |                   |
|       |                           |                          |                   |
|  +----+----------+   +------------+----------+   +-----------+-----------+       |
|  | MODE 1        |   | MODE 2                |   | MODE 3                |       |
|  | LOCAL         |   | PROXY GEMINI          |   | CLOUD DIRECT          |       |
|  |               |   |                       |   |                       |       |
|  | Ollama        |   | proxy.py              |   | API Anthropic         |       |
|  | localhost:    |   | localhost:8000        |   | api.anthropic.com     |       |
|  | 11434         |   | (FastAPI + SSE)       |   | (HTTPS natif)         |       |
|  |               |   |         |             |   |                       |       |
|  | uadf-agent    |   | Presse- |             |   | claude-sonnet-4-6     |       |
|  | (Qwen3-32B    |   | papiers |             |   | (Provider Anthropic   |       |
|  |  T=0.15)      |   | Windows |             |   |  integre Roo Code)    |       |
|  |               |   |         |             |   |                       |       |
|  | Gratuit       |   | Gratuit |             |   | Payant a l'usage      |       |
|  | 100% local    |   | Copier- |             |   | Entierement auto      |       |
|  | Hors ligne    |   | coller  |             |   | Connexion requise     |       |
|  +---------------+   +----+----+             +-----------------------+---+       |
|                           |                                                       |
|                  +--------+---------+                                             |
|                  |  INTERVENTION    |                                             |
|                  |  HUMAINE         |                                             |
|                  |  (Ctrl+V/Ctrl+C) |                                             |
|                  +--------+---------+                                             |
|                           |                                                       |
+---------------------------+-------------------+------+----------------------------+
                            |                   |      |
               +------------+------+    +-------+------+--------+
               |   GEMINI CHROME   |    |  ANTHROPIC CLOUD      |
               |   (Gem dedie      |    |  api.anthropic.com    |
               |    Roo Code)      |    |  claude-sonnet-4-6    |
               +-------------------+    +-----------------------+

+-----------------------------------------------------------------------------------+
|                       MEMORY BANK (Systeme de Fichiers)                           |
|   Fonctionne identiquement dans les 3 modes — Git versionne                       |
|                                                                                   |
|  memory-bank/                                                                     |
|  +-- projectBrief.md      (Vision & Non-Goals)                                    |
|  +-- productContext.md    (User Stories & Valeur Metier)                          |
|  +-- systemPatterns.md    (Architecture & Conventions)                            |
|  +-- techContext.md       (Stack & Commandes des 3 modes)                         |
|  +-- activeContext.md     (Tache en cours - Memoire Vive)                         |
|  +-- progress.md          (Checklist Phases & Features)                           |
|  +-- decisionLog.md       (ADR - Architecture Decision Records)                   |
+-----------------------------------------------------------------------------------+

+-----------------------------------------------------------------------------------+
|                       REGISTRE PROMPTS (prompts/)                                 |
|   Source de verite unique pour tous les system prompts — Git versionne            |
|                                                                                   |
|  prompts/                                                                         |
|  +-- README.md             (Index du registre)                                    |
|  +-- SP-001-ollama-modelfile-system.md   -> Modelfile[SYSTEM]                     |
|  +-- SP-002-clinerules-global.md         -> .clinerules (fichier entier)          |
|  +-- SP-003-persona-product-owner.md    -> .roomodes[product-owner]               |
|  +-- SP-004-persona-scrum-master.md     -> .roomodes[scrum-master]                |
|  +-- SP-005-persona-developer.md        -> .roomodes[developer]                   |
|  +-- SP-006-persona-qa-engineer.md      -> .roomodes[qa-engineer]                 |
|  +-- SP-007-gem-gemini-roo-agent.md     -> gemini.google.com (HORS GIT)           |
+-----------------------------------------------------------------------------------+
```

---

## 3. Stack Technique Détaillée

### 3.1 Couche Interface & Orchestration

| Composant | Technologie | Version | Rôle |
| :--- | :--- | :--- | :--- |
| **IDE** | Visual Studio Code | Dernière stable | Environnement de développement principal |
| **Extension Agentique** | Roo Code | Dernière stable | Moteur d'exécution agentique, pont LLM ↔ système de fichiers |
| **Personas Agile** | JSON (`.roomodes`) | — | Définition des 4 personas et de leurs permissions RBAC |
| **Directives Session** | Markdown (`.clinerules`) | — | 6 règles impératives injectées dans chaque session |

### 3.2 Couche Moteur LLM Local (Mode Souverain)

| Composant | Technologie | Version | Rôle |
| :--- | :--- | :--- | :--- |
| **Moteur d'Inférence** | Ollama | Dernière stable | Gestion VRAM, chargement des poids, API REST locale |
| **Modèle Principal** | `mychen76/qwen3_cline_roocode:32b` | 32B quantifié | Cerveau principal, fine-tuné Tool Calling Roo Code |
| **Modèle Secondaire** | `qwen3:7b` | 7B | Agent délégué pour tâches légères (Boomerang Tasks) |
| **Configuration Modèle** | `Modelfile` Ollama | — | Verrouillage T=0.15, Min_P=0.03, num_ctx=131072 |
| **Port d'Écoute** | `localhost:11434` | — | API REST compatible OpenAI exposée par Ollama |

### 3.3 Couche Proxy Gemini Chrome (Mode Hybride)

| Composant | Technologie | Version | Rôle |
| :--- | :--- | :--- | :--- |
| **Langage** | Python | 3.10+ | Langage du serveur proxy |
| **Framework Web** | FastAPI | 0.110+ | Serveur ASGI léger, émulation API OpenAI + SSE |
| **Serveur ASGI** | Uvicorn | 0.29+ | Serveur de production pour FastAPI |
| **Gestion Presse-Papiers** | Pyperclip | 1.8+ | Lecture/écriture presse-papiers Windows |
| **Gestion Async** | asyncio (stdlib Python) | — | Boucle de polling non-bloquante |
| **Streaming** | StreamingResponse (FastAPI) | — | Réponse SSE en un seul chunk pour compatibilité Roo Code |
| **Port d'Écoute** | `localhost:8000` | — | Point d'entrée pour Roo Code en mode proxy |
| **Environnement Virtuel** | venv (stdlib Python) | — | Isolation des dépendances |

### 3.4 Couche Mémoire Persistante

| Composant | Technologie | Rôle |
| :--- | :--- | :--- |
| **Système de Fichiers** | NTFS Windows | Stockage physique des fichiers `.md` |
| **Format de Données** | Markdown (`.md`) | Lisibilité humaine, compatibilité Git |
| **Versionnement** | Git | Traçabilité des modifications de la Memory Bank |
| **Répertoire** | `memory-bank/` (racine projet) | Conteneur de toute la mémoire contextuelle |

### 3.5 Couche Interface Gemini Chrome

| Composant | Technologie | Rôle |
| :--- | :--- | :--- |
| **Interface Web** | Gemini Chrome (gemini.google.com) | LLM cloud gratuit, moteur de génération |
| **Profil Dédié** | Gem Gemini "Roo Code Agent" | Contient le system prompt Roo Code (SP-007) |
| **Navigateur** | Google Chrome | Accès à l'interface Gemini Web |

### 3.6 Couche Moteur LLM Cloud Direct (Mode Claude API)

| Composant | Technologie | Version | Rôle |
| :--- | :--- | :--- | :--- |
| **Fournisseur API** | Anthropic API | v1 (stable) | API cloud officielle, connexion directe sans proxy |
| **Modèle** | `claude-sonnet-4-6` | Dernière stable Sonnet | Modèle haute qualité, natif Roo Code, tool use intégré |
| **Endpoint** | `https://api.anthropic.com` | — | Point d'entrée HTTPS officiel Anthropic |
| **Authentification** | Clé API (`sk-ant-api03-...`) | — | Stockée dans VS Code SecretStorage via Roo Code |
| **Provider Roo Code** | "Anthropic" (natif) | — | Fournisseur intégré dans Roo Code, aucun middleware |

### 3.7 Couche Vérification de Cohérence des Prompts

| Composant | Technologie | Rôle |
| :--- | :--- | :--- |
| **Script de vérification** | PowerShell (`check-prompts-sync.ps1`) | Comparaison normalisée SP canoniques vs artefacts déployés |
| **Hook Git** | Shell script (`.git/hooks/pre-commit`) | Appel automatique du script avant chaque commit |
| **Registre** | Répertoire `prompts/` (Markdown + YAML) | Source de vérité unique pour tous les system prompts |

---

## 4. Décisions d'Architecture

### DA-001 — `.roomodes` comme registre central des personas Agile
**Décision :** Le fichier `.roomodes` est le registre central des personas Agile. Il définit pour chaque rôle : son identifiant unique (`slug`), son nom d'affichage, son `roleDefinition` (system prompt comportemental), et ses `groups` de permissions. Ce fichier est statique et versionné dans Git.
**Justification :** Séparation claire entre configuration (`.roomodes`) et comportement (`.clinerules`). Le `roleDefinition` est la source de vérité du comportement de chaque persona.
**Exigences adressées :** REQ-3.1, REQ-3.2, REQ-3.3, REQ-3.4

### DA-002 — `.clinerules` comme déclencheur de session universel
**Décision :** Le fichier `.clinerules` contient 6 règles impératives injectées au-dessus de chaque prompt utilisateur, forçant l'agent à suivre la séquence VÉRIFIER→CRÉER→LIRE→AGIR pour la Memory Bank, à versionner sous Git, et à maintenir la cohérence du registre de prompts. Ces directives sont inconditionnelles et s'appliquent à tous les modes.
**Justification :** Le `.clinerules` est le filet de sécurité universel. Même si un persona oublie sa propre règle, `.clinerules` la rappelle systématiquement à chaque session.
**Exigences adressées :** REQ-4.2, REQ-4.3, REQ-7.3

### DA-003 — Memory Bank segmentée en 7 fichiers thématiques
**Décision :** La Memory Bank est segmentée en 7 fichiers thématiques pour éviter la pollution contextuelle et optimiser l'attention du LLM. Chaque fichier a une responsabilité unique et non-chevauchante.
**Justification :** Un fichier monolithique forcerait le LLM à charger toute la mémoire à chaque session. La segmentation permet de charger uniquement les fichiers pertinents selon la tâche.
**Exigences adressées :** REQ-4.4

### DA-004 — Modelfile avec paramètres de déterminisme verrouillés
**Décision :** Le modèle `mychen76/qwen3_cline_roocode:32b` est compilé avec un `Modelfile` personnalise verrouillant : `temperature 0.15`, `min_p 0.03`, `top_p 0.95`, `repeat_penalty 1.1`, `num_ctx 131072`, `num_gpu 99`, `num_thread 8`. Ces valeurs sont non-modifiables à l'exécution.
**Justification :** Le déterminisme maximal élimine les hallucinations lors de la génération de code. La fenêtre de 128K tokens permet de charger simultanément le projet et la Memory Bank.
**Exigences adressées :** REQ-1.2, REQ-1.3

### DA-005 — Boomerang Tasks pour délégation aux modèles légers
**Décision :** Le workflow "Boomerang Tasks" de Roo Code est utilisé pour déléguer les tâches répétitives ou volumineuses (analyse de logs, génération de tests unitaires) au modèle secondaire `qwen3:7b`.
**Justification :** Optimisation VRAM et accélération des cycles répétitifs. Le modèle 32B reste disponible pour les décisions complexes.
**Exigences adressées :** REQ-1.4

> ⚠️ **LIMITATION MODE PROXY :** Les Boomerang Tasks ne sont pas supportées en Mode Proxy Gemini.
> Le proxy est un endpoint unique partagé par toutes les instances Roo Code — les requêtes
> concurrentes de l'agent principal et du sous-agent créent un conflit de presse-papiers (deadlock).
> **Utiliser le Mode Local (Ollama) ou le Mode Cloud (Claude API) pour les tâches nécessitant des sous-agents.**

### DA-006 — FastAPI + asyncio pour le proxy
**Décision :** FastAPI est choisi plutôt que Flask pour sa gestion native de l'asynchronisme (asyncio), indispensable pour maintenir la connexion HTTP ouverte pendant l'attente de l'intervention humaine (polling du presse-papiers) sans bloquer le serveur.
**Justification :** Flask est synchrone par défaut — il bloquerait le serveur pendant le polling. FastAPI avec asyncio maintient le serveur réactif (endpoint `/health` répond pendant le polling).
**Exigences adressées :** REQ-2.3.1, REQ-2.1.1

### DA-007 — Émulation format OpenAI Chat Completions
**Décision :** Le proxy émule exactement le format de l'API OpenAI Chat Completions (`/v1/chat/completions`). Cette décision garantit une compatibilité native avec Roo Code configuré en mode "OpenAI Compatible", sans aucune modification du code source de Roo Code.
**Justification :** Roo Code supporte nativement le format OpenAI. En émulant ce format, le proxy est transparent pour Roo Code.
**Exigences adressées :** REQ-2.1.2, REQ-2.4.2

### DA-008 — Mode "Gem dédié" avec filtrage du system prompt
**Décision :** Le proxy implémente un mode `USE_GEM_MODE=true` (défaut) qui filtre le message `system` lors de la copie dans le presse-papiers. Lorsque ce mode est actif, seuls les messages `user` et `assistant` sont transmis.
**Justification :** Le system prompt de Roo Code représente plusieurs milliers de tokens. En le stockant dans le Gem Gemini (SP-007), on évite de le retransmettre à chaque requête, réduisant la taille du transfert de 50%+.
**Exigences adressées :** REQ-2.1.4

### DA-009 — Nettoyage des contenus base64
**Décision :** Le proxy détecte et remplace les éléments `{"type": "image_url", ...}` par le message `[IMAGE OMISE - Non supportee par le proxy clipboard]`.
**Justification :** Les images base64 peuvent représenter des centaines de Ko. Leur présence dans le presse-papiers rendrait le transfert impossible. Le remplacement par un message textuel préserve le contexte sans bloquer le flux.
**Exigences adressées :** REQ-2.1.5

### DA-010 — Gem Gemini avec system prompt Roo Code intégré
**Décision :** Un "Gem" dédié est créé dans Gemini Web avec l'intégralité du system prompt de Roo Code (SP-007). Cette approche évite de retransmettre le system prompt à chaque requête via le presse-papiers.
**Justification :** Le system prompt Roo Code est statique et ne change pas entre les requêtes. Le stocker dans le Gem une seule fois est plus efficace que de le retransmettre à chaque échange.
**Exigences adressées :** REQ-5.1, REQ-5.2

### DA-011 — Fournisseur Anthropic natif Roo Code pour le Mode Cloud
**Décision :** La connexion à l'API Anthropic utilise le provider natif "Anthropic" intégré dans Roo Code. Le modèle de référence est `claude-sonnet-4-6`. La clé API est stockée dans VS Code SecretStorage, jamais dans les fichiers du projet.
**Justification :** Le provider natif garantit la compatibilité totale avec le streaming, la vision et le tool use natif de Claude. VS Code SecretStorage est chiffré et non accessible depuis le système de fichiers, garantissant la sécurité de la clé API.
**Exigences adressées :** REQ-6.1, REQ-6.2, REQ-6.3, REQ-6.4

### DA-012 — Registre centralisé des system prompts dans `prompts/`
**Décision :** Un répertoire `prompts/` versionné contient une copie canonique de chaque system prompt avec métadonnées YAML (cible, version, dépendances, changelog). REGLE 6 dans `.clinerules` impose la cohérence avant chaque commit. SP-007 (Gem Gemini) est marqué `hors_git: true` avec procédure de déploiement manuel documentée.
**Justification :** Les system prompts sont dispersés dans plusieurs artefacts (.roomodes JSON, .clinerules texte, Modelfile compilé, Gemini Web externe). Sans registre centralisé, une modification de `.clinerules` peut rendre le Gem Gemini incohérent sans que personne ne le remarque.
**Exigences adressées :** REQ-7.1, REQ-7.2, REQ-7.3, REQ-7.4, REQ-7.5

### DA-013 — Vérification automatique via script PowerShell + hook Git pre-commit
**Décision :** Un script `template/template/scripts/check-prompts-sync.ps1` compare le contenu déployé avec les SP canoniques via comparaison normalisée (correction encodage `\r\n`/`\n`, désérialisation JSON pour `.roomodes`, regex robuste d'extraction). Un hook Git `.git/hooks/pre-commit` appelle ce script automatiquement et bloque le commit si désynchronisation détectée. SP-007 est exclu de la vérification automatique avec avertissement de vérification manuelle.
**Justification :** REGLE 6 étant une directive comportementale, elle peut être ignorée par un agent LLM. Le hook pre-commit transforme la vérification en contrainte technique non-contournable.
**Exigences adressées :** REQ-8.1, REQ-8.2, REQ-8.3, REQ-8.4

### DA-014 — Streaming SSE en un seul chunk pour le proxy
**Décision :** Le proxy implémente le streaming SSE (Server-Sent Events) en retournant la réponse Gemini en un seul chunk SSE suivi de `data: [DONE]`. Si la requête contient `"stream": false`, une réponse JSON complète non-streamée est retournée. Le proxy détecte automatiquement le mode via le champ `stream` de la requête.
**Justification :** Roo Code peut envoyer des requêtes avec `stream: true` (comportement par défaut dans certaines versions). Sans support SSE, le proxy retournerait une réponse JSON non-streamée que Roo Code pourrait rejeter en attendant le format SSE. L'implémentation SSE en un seul chunk est transparente pour Roo Code quelle que soit sa configuration.
**Exigences adressées :** REQ-2.4.1, REQ-2.4.3

---

## 5. Architecture des Couches Fonctionnelles

### Couche A — Orchestration Comportementale (`.roomodes` & `.clinerules`)

**Matrice RBAC des Permissions (DA-001) :**

| Permission | Product Owner | Scrum Master | Developer | QA Engineer |
| :--- | :---: | :---: | :---: | :---: |
| `read` (lecture tous fichiers) | ✅ | ✅ | ✅ | ✅ |
| `edit` `memory-bank/productContext.md` | ✅ | ✅ | ✅ | ❌ |
| `edit` `memory-bank/*.md` (tous) | ❌ | ✅ | ✅ | ❌ |
| `edit` `docs/*.md` (documentation) | ✅ | ✅ | ✅ | ❌ |
| `edit` `docs/qa/*.md` (rapports QA) | ❌ | ❌ | ❌ | ✅ |
| `edit` code source (tous fichiers) | ❌ | ❌ | ✅ | ❌ |
| `command` terminal général | ❌ | ❌ | ✅ | ❌ |
| `command` Git uniquement | ❌ | ✅ | ✅ | ❌ |
| `command` tests uniquement | ❌ | ❌ | ✅ | ✅ |
| `browser` accès navigateur | ❌ | ❌ | ✅ | ✅ |
| `mcp` accès MCP | ❌ | ❌ | ✅ | ❌ |

**Commandes Git autorisées Scrum Master :** `git add`, `git commit`, `git status`, `git log`
**Commandes test autorisées QA Engineer :** `npm test`, `npm run test`, `pytest`, `python -m pytest`, `dotnet test`, `go test`, `git status`, `git log`

---

### Couche B — Memory Bank (Fichiers Markdown)

**Structure et Responsabilités des 7 Fichiers (DA-003) :**

| Fichier | Fréquence de Lecture | Fréquence d'Écriture | Contenu |
| :--- | :--- | :--- | :--- |
| `projectBrief.md` | Début de projet | Rare | Vision, objectifs, Non-Goals, contraintes |
| `productContext.md` | Début de sprint | Par sprint | User Stories, valeur métier, backlog |
| `systemPatterns.md` | Avant modification architecture | Après décision architecture | Structure dossiers, conventions, patterns |
| `techContext.md` | Avant commande build/test | Après changement dépendance | Stack, versions, commandes, variables d'env |
| `activeContext.md` | **À chaque démarrage session** | **À chaque fin de tâche** | Tâche en cours, dernier résultat, prochaine action |
| `progress.md` | **À chaque démarrage session** | **À chaque validation feature** | Checklist phases le workbench, features terminées/en cours |
| `decisionLog.md` | Avant décision architecture | Après décision architecture | ADR horodatés avec contexte, décision, conséquences |

**Séquence obligatoire au démarrage de session (DA-002, REQ-4.2) :**
```
1. VÉRIFIER existence de activeContext.md et progress.md
2. Si absents → CRÉER depuis templates .clinerules (immédiatement)
3. LIRE activeContext.md puis progress.md
4. AGIR sur la demande utilisateur
```

---

### Couche C — Moteur LLM Local (Ollama + Qwen3)

**Contenu du `Modelfile` (DA-004) :**
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

---

### Couche D — Proxy Gemini Chrome (FastAPI + Pyperclip + SSE)

**Flux de Données Détaillé :**
```
ETAPE 1 — RECEPTION (Roo Code -> Proxy)
POST http://localhost:8000/v1/chat/completions
{ "model": "gemini-manual", "messages": [...], "stream": true|false }

ETAPE 2 — EXTRACTION & FORMATAGE
Si USE_GEM_MODE=true : ignorer role:system
Nettoyer images base64 → [IMAGE OMISE...]
Formater : [USER]\n{contenu}\n\n---\n\n[ASSISTANT]\n{contenu}

ETAPE 3 — UPLINK
pyperclip.copy(formatted_prompt)
hash_initial = md5(formatted_prompt)
Console: instructions numérotées pour l'utilisateur

ETAPE 4 — POLLING ASYNCHRONE
while True:
  await asyncio.sleep(1.0)
  if md5(pyperclip.paste()) != hash_initial: break
  if elapsed > 300s: raise HTTP 408

ETAPE 5 — VALIDATION
Vérifier présence balises XML Roo Code (warning si absent, non-bloquant)

ETAPE 6 — REINJECTION
Si stream=true  → SSE : data:{chunk}\n\ndata:{done}\n\ndata:[DONE]\n\n
Si stream=false → JSON : {"id":..., "choices":[{"message":{"content":"..."}}]}
```

**Code complet `template/proxy.py` v2.0 (DA-006, DA-007, DA-008, DA-009, DA-014) :**

```python
"""
le workbench Proxy v2.0 — Pont Roo Code <-> Gemini Chrome
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

app = FastAPI(title="le workbench Proxy", version="2.0.0")

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
                continue
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
    return {"status": "ok", "proxy": "le workbench", "version": "2.0.0", "gem_mode": USE_GEM_MODE}

if __name__ == "__main__":
    print(f"{'='*60}\n  le workbench PROXY v2.0 | http://localhost:{PORT}/v1\n  Mode: {'GEM' if USE_GEM_MODE else 'COMPLET'} | Timeout: {TIMEOUT_SECONDS}s\n{'='*60}")
    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="warning")
```

---

### Couche E — Configuration Gemini Chrome (Gem Dédié)

**Contenu du System Prompt du Gem "Roo Code Agent" (SP-007) :**
```
Tu es l'agent de codage integre dans Roo Code, un assistant IA expert en developpement logiciel.

REGLES ABSOLUES ET NON-NEGOCIABLES :
1. Tu dois TOUJOURS repondre en utilisant les balises XML de Roo Code.
2. Tu ne dois JAMAIS generer de texte de courtoisie, d'introduction ou de conclusion.
3. Tu ne dois JAMAIS expliquer ce que tu vas faire : tu le fais directement avec les balises XML.
4. Tu dois traiter chaque message comme une instruction directe a executer.
5. Si tu as besoin d'informations supplementaires, utilise ask_followup_question.

BALISES XML DISPONIBLES :
- write_to_file (path + content) : creer ou ecrire un fichier complet
- read_file (path) : lire un fichier
- execute_command (command) : executer une commande terminal
- replace_in_file (path + diff) : modifier une partie d'un fichier
- list_files (path) : lister les fichiers d'un dossier
- search_files (path + regex) : rechercher dans les fichiers
- attempt_completion (result) : signaler la completion d'une tache
- ask_followup_question (question) : poser une question a l'utilisateur

RAPPEL : Aucun texte avant la premiere balise XML. Aucun texte apres la derniere balise XML.
```

---

### Couche F — Registre des Prompts (`prompts/`)

| Fichier SP | Cible de Déploiement | Champ Cible | Hors Git |
| :--- | :--- | :--- | :---: |
| `SP-001-ollama-modelfile-system.md` | `Modelfile` | Bloc `SYSTEM """..."""` | Non |
| `SP-002-clinerules-global.md` | `.clinerules` | Fichier entier | Non |
| `SP-003-persona-product-owner.md` | `.roomodes` | `customModes[0].roleDefinition` | Non |
| `SP-004-persona-scrum-master.md` | `.roomodes` | `customModes[1].roleDefinition` | Non |
| `SP-005-persona-developer.md` | `.roomodes` | `customModes[2].roleDefinition` | Non |
| `SP-006-persona-qa-engineer.md` | `.roomodes` | `customModes[3].roleDefinition` | Non |
| `SP-007-gem-gemini-roo-agent.md` | `gemini.google.com > Gems > Instructions` | Instructions du Gem | **Oui** |

---

## 6. Matrice de Traçabilité Architecture / Fonctionnalité / Exigence

| Composant Architectural | Couche | Fonctionnalité | Décisions | Exigences PRD |
| :--- | :--- | :--- | :--- | :--- |
| **VS Code + Roo Code** | Interface | Moteur d'exécution agentique central | — | REQ-000 |
| **`.roomodes`** | Orchestration | Registre JSON des 4 personas Agile avec RBAC | DA-001 | REQ-3.1, REQ-3.2, REQ-3.3, REQ-3.4 |
| **`.clinerules`** | Orchestration | 6 règles impératives : Memory Bank, Git, Cohérence Prompts | DA-002 | REQ-4.2, REQ-4.3, REQ-7.3 |
| **Persona `product-owner`** | Orchestration | Rédaction User Stories, lecture docs, refus code | DA-001 | REQ-3.1, REQ-3.2, REQ-3.3 |
| **Persona `scrum-master`** | Orchestration | Facilitation Agile, Memory Bank, Git uniquement, pas de tests | DA-001 | REQ-3.1, REQ-3.2, REQ-3.4 |
| **Persona `developer`** | Orchestration | Implémentation complète, code + terminal + Git | DA-001 | REQ-3.1, REQ-3.2 |
| **Persona `qa-engineer`** | Orchestration | Tests + rapports QA, pas de modification code source | DA-001 | REQ-3.1, REQ-3.2 |
| **Ollama (daemon Windows)** | Moteur LLM Local | Inférence locale, API REST OpenAI sur localhost:11434 | — | REQ-1.0, REQ-000 |
| **`mychen76/qwen3_cline_roocode:32b`** | Moteur LLM Local | Modèle principal fine-tuné Tool Calling Roo Code | DA-004 | REQ-1.1 |
| **`Modelfile` (T=0.15, num_ctx=131072)** | Moteur LLM Local | Déterminisme + fenêtre contexte 128K tokens | DA-004 | REQ-1.2, REQ-1.3 |
| **`qwen3:7b` + Boomerang Tasks** | Moteur LLM Local | Délégation tâches légères au modèle secondaire | DA-005 | REQ-1.4 |
| **`template/proxy.py` — POST `/v1/chat/completions`** | Proxy Hybride | Point d'entrée unique, interception requêtes Roo Code | DA-006, DA-007 | REQ-2.1.1, REQ-2.1.2 |
| **`template/proxy.py` — `_format_prompt()`** | Proxy Hybride | Extraction payload, filtrage system prompt (GEM MODE) | DA-008 | REQ-2.1.3, REQ-2.1.4 |
| **`template/proxy.py` — `_clean_content()`** | Proxy Hybride | Nettoyage images base64, remplacement par message textuel | DA-009 | REQ-2.1.5 |
| **`template/proxy.py` — `pyperclip.copy()`** | Proxy Hybride | Injection prompt formaté dans presse-papiers Windows | — | REQ-2.2.1 |
| **`template/proxy.py` — Séparateurs `[USER]`, `[ASSISTANT]`** | Proxy Hybride | Format lisible avec séparateurs explicites | DA-008 | REQ-2.2.2 |
| **`template/proxy.py` — Messages console horodatés** | Proxy Hybride | Notification utilisateur avec timestamp et 5 instructions | — | REQ-2.2.3 |
| **`template/proxy.py` — Boucle `asyncio` + `pyperclip.paste()`** | Proxy Hybride | Polling asynchrone non-bloquant toutes les secondes | DA-006 | REQ-2.3.1 |
| **`template/proxy.py` — Comparaison hash MD5** | Proxy Hybride | Détection changement presse-papiers | — | REQ-2.3.2 |
| **`template/proxy.py` — Timeout 300s + HTTP 408** | Proxy Hybride | Gestion non-réponse utilisateur | — | REQ-2.3.3 |
| **`template/proxy.py` — `_validate_response()`** | Proxy Hybride | Vérification présence balises XML Roo Code (warning non-bloquant) | — | REQ-2.3.4 |
| **`template/proxy.py` — `_stream_response()` (SSE)** | Proxy Hybride | Réponse SSE en un seul chunk si `stream=true` | DA-014 | REQ-2.4.1, REQ-2.4.3 |
| **`template/proxy.py` — `_build_json_response()`** | Proxy Hybride | Réponse JSON OpenAI complète si `stream=false` | DA-007 | REQ-2.4.2, REQ-2.4.3 |
| **`template/proxy.py` — Transmission contenu brut** | Proxy Hybride | Contenu Gemini transmis tel quel sans modification | — | REQ-2.4.4 |
| **`memory-bank/`** | Mémoire | Conteneur mémoire contextuelle, intégré Git | DA-003 | REQ-4.1, REQ-4.5 |
| **`memory-bank/activeContext.md`** | Mémoire | Mémoire vive de session, lu et écrit à chaque session | DA-002, DA-003 | REQ-4.2, REQ-4.3, REQ-4.4 |
| **`memory-bank/progress.md`** | Mémoire | Checklist phases le workbench et features produit | DA-002, DA-003 | REQ-4.2, REQ-4.3, REQ-4.4 |
| **`memory-bank/projectBrief.md`** | Mémoire | Vision, objectifs, Non-Goals, contraintes | DA-003 | REQ-4.4 |
| **`memory-bank/productContext.md`** | Mémoire | User Stories, valeur métier, backlog | DA-003 | REQ-4.4 |
| **`memory-bank/systemPatterns.md`** | Mémoire | Architecture, conventions, patterns techniques | DA-003 | REQ-4.4 |
| **`memory-bank/techContext.md`** | Mémoire | Stack, versions, commandes, variables d'env | DA-003 | REQ-4.4 |
| **`memory-bank/decisionLog.md`** | Mémoire | ADR horodatés après chaque décision d'architecture | DA-003 | REQ-4.4, REQ-4.5 |
| **Gem Gemini "Roo Code Agent"** | Gemini Config | Profil dédié avec system prompt Roo Code complet (SP-007) | DA-010 | REQ-5.1, REQ-5.2 |
| **Instructions du Gem (balises XML)** | Gemini Config | Règles strictes imposant réponses XML uniquement, sans texte parasite | DA-010 | REQ-5.2 |
| **Historique conversation dans presse-papiers** | Gemini Config | Transmission historique multi-tours pour cohérence des réponses | DA-008 | REQ-5.3 |
| **Provider "Anthropic" dans Roo Code** | Cloud Direct | Connexion directe à api.anthropic.com sans proxy | DA-011 | REQ-6.3 |
| **Clé API Anthropic (VS Code SecretStorage)** | Cloud Direct | Authentification Anthropic, stockée chiffrée, jamais dans Git | DA-011 | REQ-6.1, REQ-6.4 |
| **Modèle `claude-sonnet-4-6`** | Cloud Direct | Modèle Claude Sonnet haute qualité, natif Roo Code | DA-011 | REQ-6.2 |
| **Commutateur Provider Roo Code** | Commutateur LLM | Bascule entre Ollama/Proxy/Anthropic sans modifier Roo Code | DA-007, DA-011 | REQ-2.0 |
| **Variable `USE_GEM_MODE`** | Proxy Hybride | Active le filtrage du system prompt quand Gem configuré | DA-008 | REQ-2.1.4 |
| **Répertoire `prompts/`** | Registre Prompts | Source de vérité unique pour tous les system prompts | DA-012 | REQ-7.1 |
| **Fichiers `template/prompts/SP-XXX-*.md`** | Registre Prompts | Fichiers canoniques avec en-tête YAML (id, version, target, changelog) | DA-012 | REQ-7.1, REQ-7.2, REQ-7.4 |
| **`template/prompts/README.md`** | Registre Prompts | Index du registre avec tableau ID/fichier/cible/Hors Git | DA-012 | REQ-7.2 |
| **REGLE 6 dans `.clinerules`** | Registre Prompts | Directive impérative : vérifier cohérence prompts avant commit | DA-012 | REQ-7.3 |
| **Flag `hors_git: true` dans SP-007** | Registre Prompts | Marqueur déploiement manuel, déclenche mention commit obligatoire | DA-012 | REQ-7.5 |
| **`template/template/scripts/check-prompts-sync.ps1`** | Vérification Prompts | Comparaison normalisée SP canoniques vs artefacts, rapport PASS/FAIL avec diff | DA-013 | REQ-8.1, REQ-8.3, REQ-8.4 |
| **`.git/hooks/pre-commit`** | Vérification Prompts | Hook Git appelant check-prompts-sync.ps1, bloque commit si désync | DA-013 | REQ-8.2 |

---

## Annexe A — Table des Références

| Réf. | Type | Titre / Identifiant | Description |
| :--- | :--- | :--- | :--- |
| [DOC1] | Document interne | `workbench/DOC1-PRD-Workbench-Requirements.md` | Product Requirements Document v2.0 — source de toutes les exigences REQ-xxx référencées dans ce document |
| [DOC2] | Document interne | `workbench/DOC2-ARCH-Workbench-Technical-Design.md` | Ce document — Architecture, Solution et Stack Technique v2.0 |
| [DOC3] | Document interne | `workbench/DOC3-BUILD-Workbench-Assembly-Phases.md` | Plan d'Implémentation Séquentiel Complet v3.0 (Phases 0–12) |
| [DOC4] | Document interne | `workbench/DOC4-GUIDE-Workbench-Deployment-Howto.md` | Guide de Déploiement de l'Atelier sur projets nouveaux et existants |
| [SP-001] | System Prompt | `template/prompts/SP-001-ollama-modelfile-system.md` | System prompt du Modelfile Ollama — contenu du bloc `SYSTEM """..."""` |
| [SP-002] | System Prompt | `template/prompts/SP-002-clinerules-global.md` | Contenu canonique du fichier `.clinerules` (6 règles impératives) |
| [SP-003] | System Prompt | `template/prompts/SP-003-persona-product-owner.md` | `roleDefinition` du persona Product Owner dans `.roomodes` |
| [SP-004] | System Prompt | `template/prompts/SP-004-persona-scrum-master.md` | `roleDefinition` du persona Scrum Master dans `.roomodes` |
| [SP-005] | System Prompt | `template/prompts/SP-005-persona-developer.md` | `roleDefinition` du persona Developer dans `.roomodes` |
| [SP-006] | System Prompt | `template/prompts/SP-006-persona-qa-engineer.md` | `roleDefinition` du persona QA Engineer dans `.roomodes` |
| [SP-007] | System Prompt | `template/prompts/SP-007-gem-gemini-roo-agent.md` | Instructions du Gem Gemini "Roo Code Agent" — déploiement manuel hors Git (`hors_git: true`) |
| [OLLAMA] | Outil externe | https://ollama.com | Moteur d'inférence LLM local — expose une API REST OpenAI-compatible sur `localhost:11434` |
| [FASTAPI] | Bibliothèque Python | https://fastapi.tiangolo.com | Framework web ASGI Python utilisé pour le serveur proxy (`template/proxy.py`) |
| [UVICORN] | Bibliothèque Python | https://www.uvicorn.org | Serveur ASGI de production pour FastAPI |
| [PYPERCLIP] | Bibliothèque Python | https://pypi.org/project/pyperclip | Gestion du presse-papiers Windows depuis Python |
| [ANTHROPIC] | API externe | https://api.anthropic.com | API officielle Anthropic — endpoint de connexion directe pour le Mode Cloud |
| [ANTHROPIC-MODELS] | Documentation | https://docs.anthropic.com/en/docs/about-claude/models | Liste des modèles Claude disponibles — à consulter pour mettre à jour `claude-sonnet-4-6` |
| [GEMINI] | Interface externe | https://gemini.google.com | Interface web Gemini de Google — utilisée en Mode Proxy Chrome |
| [ROOCODE] | Extension VS Code | Roo Code (extension VS Code) | Moteur d'exécution agentique central — orchestre tous les composants via balises XML |
| [OPENAI-FMT] | Standard | Format OpenAI Chat Completions v1 | Standard d'API `/v1/chat/completions` émulé par le proxy pour compatibilité native avec Roo Code |
| [SEMVER] | Standard | Semantic Versioning (semver.org) | Convention MAJOR.MINOR.PATCH utilisée pour les fichiers SP et le workbench |

---

## Annexe B — Table des Abréviations

| Abréviation | Forme complète | Explication |
| :--- | :--- | :--- |
| **ADR** | Architecture Decision Record | Enregistrement horodaté d'une décision d'architecture. Stocké dans `memory-bank/decisionLog.md`. Format : contexte, décision, conséquences. |
| **API** | Application Programming Interface | Interface de programmation. Ici : API Ollama REST (locale), API Anthropic HTTPS (cloud), format API OpenAI (émulé par le proxy). |
| **ASGI** | Asynchronous Server Gateway Interface | Standard Python pour serveurs web asynchrones. FastAPI + Uvicorn forment la pile ASGI du proxy. |
| **DA** | Décision d'Architecture | Identifiant des décisions dans ce document (DA-001 à DA-014). Chaque DA justifie un choix technique et référence les REQ adressées. |
| **GEM** | Gem Gemini | Profil personnalisé dans Gemini Web contenant un system prompt permanent. "Roo Code Agent" contient SP-007. |
| **GPU** | Graphics Processing Unit | Processeur graphique. `num_gpu 99` dans le Modelfile délègue l'inférence au GPU pour accélérer Qwen3-32B. |
| **HTTP** | HyperText Transfer Protocol | Protocole de communication. Le proxy écoute sur HTTP `localhost:8000`. L'API Anthropic utilise HTTPS. |
| **JSON** | JavaScript Object Notation | Format de données structuré. Utilisé pour `.roomodes`, les réponses API OpenAI et les requêtes du proxy. |
| **LAAW** | Local Agentic Agile Workflow | Blueprint mychen76 — source d'inspiration pour la Memory Bank segmentée et les personas Agile. |
| **LLM** | Large Language Model | Grand modèle de langage. Trois instances dans le workbench : Qwen3-32B (local), Gemini Pro (cloud Google), Claude Sonnet (cloud Anthropic). |
| **MCP** | Model Context Protocol | Protocole d'extension Roo Code pour outils externes. Accessible uniquement au persona Developer. |
| **MD5** | Message Digest 5 | Algorithme de hachage. Utilisé par le proxy pour détecter les changements de presse-papiers (`_hash()` dans `template/proxy.py`). |
| **NTFS** | New Technology File System | Système de fichiers Windows. Stocke physiquement la Memory Bank et les fichiers de configuration. |
| **PO** | Product Owner | Persona Agile — vision produit, User Stories, backlog. Mode `product-owner` dans `.roomodes`. |
| **PRD** | Product Requirements Document | Document d'exigences produit. DOC1 est le PRD du workbench. |
| **RBAC** | Role-Based Access Control | Contrôle d'accès par rôles. Matrice définie en section 5 (Couche A) et dans DOC1 section 4.1. |
| **REQ** | Requirement (Exigence) | Identifiant des exigences dans DOC1 (ex: REQ-2.1.4). Chaque DA de ce document référence les REQ qu'il adresse. |
| **REST** | Representational State Transfer | Style d'architecture API web. Ollama expose une API REST sur `localhost:11434`. |
| **SM** | Scrum Master | Persona Agile facilitateur pur — Memory Bank + Git uniquement, sans code ni tests. |
| **SP** | System Prompt | Fichier canonique du registre `template/prompts/` avec métadonnées YAML. |
| **SSE** | Server-Sent Events | Protocole de streaming HTTP serveur→client. Le proxy retourne les réponses Gemini en SSE quand `stream: true` (DA-014). |
| **le workbench** | Agentic Agile Workbench | Nom du système décrit dans ce document. |
| **VRAM** | Video Random Access Memory | Mémoire GPU. Qwen3-32B nécessite 8+ Go de VRAM pour une inférence GPU optimale. |
| **YAML** | YAML Ain't Markup Language | Format de sérialisation lisible. Utilisé pour les en-têtes des fichiers SP canoniques. |

---

## Annexe C — Glossaire

| Terme | Définition |
| :--- | :--- |
| **Atelier (Workbench)** | Ce dépôt (`agentic-agile-workbench`). Contient les outils, règles et processus réutilisables. S'oppose au "projet applicatif" qui contient le code métier. |
| **Balises XML Roo Code** | Syntaxe d'action de Roo Code : `<write_to_file>`, `<read_file>`, `<execute_command>`, `<attempt_completion>`, etc. Tout LLM connecté doit répondre avec ces balises. |
| **Boomerang Tasks** | Mécanisme Roo Code de délégation : l'agent 32B crée une sous-tâche pour le modèle 7B, récupère le résultat et l'intègre dans sa boucle (DA-005, REQ-1.4). |
| **Commutateur LLM** | Paramètre "API Provider" dans les settings Roo Code. Bascule entre Ollama (Mode Local), proxy FastAPI (Mode Proxy) et Anthropic (Mode Cloud) sans modifier Roo Code (DA-007, DA-011). |
| **Couche** | Niveau d'abstraction dans l'architecture le workbench. Six couches : A (Orchestration), B (Memory Bank), C (LLM Local), D (Proxy Gemini), E (Gemini Chrome), F (Registre Prompts). |
| **Déterminisme** | Stabilité des réponses LLM. Obtenu via `temperature 0.15`, `min_p 0.03`, `top_p 0.95`, `repeat_penalty 1.1` dans le Modelfile (DA-004, REQ-1.3). |
| **Fenêtre de contexte** | Capacité maximale de traitement simultané d'un LLM. Fixée à 128K tokens (`num_ctx 131072`) pour charger code + Memory Bank (DA-004, REQ-1.2). |
| **Fine-tuning** | Entraînement spécialisé d'un LLM. `mychen76/qwen3_cline_roocode:32b` est fine-tuné pour le Tool Calling Roo Code (REQ-1.1). |
| **Gem Gemini** | Profil Gemini Web avec system prompt permanent (SP-007). Évite de retransmettre le system prompt à chaque requête — réduction de 50%+ de la taille des transferts (DA-010). |
| **Hook pre-commit** | Script Git exécuté avant chaque commit. Appelle `check-prompts-sync.ps1` et bloque le commit si désynchronisation SP/artefact détectée (DA-013, REQ-8.2). |
| **Memory Bank** | 7 fichiers Markdown dans `memory-bank/` persistant le contexte entre sessions. Segmentés par thème pour optimiser l'attention du LLM (DA-003, REQ-4.4). |
| **Modelfile** | Fichier de configuration Ollama. Définit le modèle de base, les paramètres d'inférence et le system prompt. Compilé avec `ollama create uadf-agent -f Modelfile` (DA-004). |
| **Mode Cloud** | Roo Code → API Anthropic directe (`claude-sonnet-4-6`). Automatisé, payant, nécessite clé API dans VS Code SecretStorage (DA-011, REQ-6.x). |
| **Mode Local** | Roo Code → Ollama `localhost:11434` → Qwen3-32B. Gratuit, souverain, hors ligne (REQ-1.x). |
| **Mode Proxy** | Roo Code → proxy FastAPI `localhost:8000` → presse-papiers → Gemini Web. Gratuit, nécessite copier-coller humain (DA-006 à DA-014, REQ-2.x). |
| **Persona Agile** | Mode Roo Code simulant un rôle Scrum. Défini dans `.roomodes` avec `roleDefinition` (comportement) et `groups` (permissions RBAC). |
| **Polling** | Vérification périodique d'un état. Le proxy vérifie le presse-papiers toutes les secondes via `asyncio.sleep(1.0)` (DA-006, REQ-2.3.1). |
| **Proxy** | Serveur FastAPI local (`template/proxy.py`) interceptant les requêtes Roo Code, les relayant vers Gemini Web via presse-papiers, et retournant la réponse (DA-006, DA-007). |
| **Registre de prompts** | Répertoire `template/prompts/` — source de vérité unique pour tous les system prompts, versionnés avec métadonnées YAML (DA-012, REQ-7.x). |
| **Séquence VÉRIFIER→CRÉER→LIRE→AGIR** | Protocole obligatoire au démarrage de session : vérifier Memory Bank → créer si absente → lire → agir. Défini dans REGLE 1 de `.clinerules` (DA-002, REQ-4.2). |
| **SSE (Server-Sent Events)** | Streaming HTTP unidirectionnel. Le proxy retourne la réponse Gemini en un seul chunk SSE pour compatibilité avec Roo Code en mode `stream: true` (DA-014, REQ-2.4.1). |
| **Token** | Unité de traitement LLM ≈ 0,75 mot. La fenêtre 128K tokens ≈ 96 000 mots. |
| **Tool Calling** | Capacité LLM à appeler des outils via requêtes structurées. Qwen3-32B est fine-tuné pour le Tool Calling Roo Code (balises XML). |
| **VS Code SecretStorage** | Stockage chiffré VS Code pour la clé API Anthropic. Non accessible depuis le système de fichiers — garantit REQ-6.4 (jamais dans Git). |
