# Document 1 : Product Requirements Document (PRD)
## Agentic Agile Workbench

**Nom du Projet :** Agentic Agile Workbench
**Version :** 2.0 — Refactorisé (exigences atomiques, arbitrages intégrés)
**Date :** 2026-03-23
**Auteur :** Architecture Senior — Synthèse mychen76 LAAW + Proxy Gemini Chrome
**Statut :** Approuvé

---

## 1. Contexte et Vision Stratégique

Ce PRD synthétise deux sources d'inspiration complémentaires :

1. **Le Blueprint LAAW (mychen76)** : Un environnement de développement agentique local, souverain, orchestré par des agents IA spécialisés avec mémoire persistante et rituels Agile.
2. **Le Proxy Gemini Chrome** : Un mécanisme de pont réseau-presse-papiers permettant à Roo Code d'exploiter gratuitement la puissance de Gemini Web via une intervention humaine minimale (copier-coller).

L'objectif est de définir un système **unifié et enrichi** qui combine la souveraineté locale du LAAW avec la flexibilité du backend LLM hybride (local Ollama OU Gemini Chrome via proxy OU Claude Sonnet via API directe), tout en maintenant la rigueur Agile et la persistance de la mémoire contextuelle.

---

## 2. Exigence Fondamentale (REQ-000)

> **REQ-000 — Exigence Racine du Système Unifié**
>
> Le système global doit fournir un environnement de développement agentique opérationnel sur un laptop Windows avec VS Code, capable de :
> - Orchestrer des agents IA spécialisés selon les rôles Agile (Product Owner, Scrum Master, QA Engineer, Developer)
> - Maintenir une continuité de contexte absolue entre les sessions via une mémoire persistante en fichiers Markdown auditables
> - Exécuter des tâches de développement complexe en s'appuyant sur un backend LLM **commutable** : soit un modèle local (Ollama/Qwen3) pour la souveraineté totale, soit Gemini Chrome via un proxy API local pour la puissance gratuite du cloud, soit Claude Sonnet via API Anthropic directe pour l'automatisation complète
> - Garantir que Roo Code reste le moteur d'exécution agentique central dans les trois modes de fonctionnement, sans modification de son comportement natif

---

## 3. Décomposition Hiérarchique des Exigences

### 3.1 Domaine 1 — Moteur Agentique & Modèles de Fondation (REQ-1.x)

#### REQ-1.0 — Capacité d'Inférence LLM Locale
Le système doit être capable d'exécuter des inférences LLM entièrement en local, sans dépendance réseau externe, via Ollama.

| ID | Exigence | Description Détaillée | Critère d'Acceptation |
| :--- | :--- | :--- | :--- |
| **REQ-1.1** | **Modèle principal optimisé Tool Calling** | Le modèle Ollama utilisé comme agent principal doit être `mychen76/qwen3_cline_roocode:32b`, spécifiquement fine-tuné pour l'appel d'outils Roo Code. Aucun modèle de substitution n'est prévu — la disponibilité du modèle sur Ollama Hub est une précondition d'installation. | L'agent émet des requêtes JSON valides vers l'API Roo Code sans erreur de syntaxe ni de formatage sur 10 requêtes consécutives de test. |
| **REQ-1.2** | **Fenêtre de contexte minimale de 128K tokens** | Le paramètre `num_ctx` du Modelfile Ollama doit être configuré à exactement `131072` (128K tokens). Cette valeur est non-négociable : elle permet le chargement simultané du code source du projet ET des 7 fichiers de la Memory Bank dans le contexte de l'agent. | `ollama show uadf-agent --modelfile` affiche `PARAMETER num_ctx 131072`. |
| **REQ-1.3** | **Déterminisme de l'inférence** | Les paramètres de génération doivent être verrouillés dans le Modelfile pour éliminer les hallucinations lors de la génération de code : `temperature 0.15`, `min_p 0.03`, `top_p 0.95`, `repeat_penalty 1.1`. Ces valeurs sont fixes et non-modifiables par l'utilisateur à l'exécution. | `ollama show uadf-agent --modelfile` affiche les 4 paramètres avec les valeurs exactes ci-dessus. |
| **REQ-1.4** | **Délégation Boomerang Tasks** | Le système doit permettre à l'agent principal (32B) de déléguer des sous-tâches à un modèle secondaire léger (`qwen3:7b`) via le workflow "Boomerang Tasks" de Roo Code, puis d'intégrer la sortie dans sa propre boucle de décision. | L'agent 32B peut créer une sous-tâche Boomerang, le modèle 7B l'exécute, et le résultat est retourné à l'agent 32B sans intervention humaine. |

---

### 3.2 Domaine 2 — Backend LLM Hybride & Proxy Gemini Chrome (REQ-2.x)

#### REQ-2.0 — Commutabilité du Backend LLM
Le système doit permettre à l'utilisateur de basculer le backend LLM de Roo Code entre les trois modes (Ollama local, Proxy Gemini Chrome, API Anthropic Claude) en modifiant uniquement le paramètre "API Provider" dans les settings Roo Code, sans modifier le comportement de Roo Code ni la structure de la Memory Bank.

##### REQ-2.1 — Sous-domaine : Serveur Proxy Local (Interception)

| ID | Exigence | Description Détaillée | Critère d'Acceptation |
| :--- | :--- | :--- | :--- |
| **REQ-2.1.1** | **Serveur local FastAPI sur localhost:8000** | Un serveur web local Python (FastAPI + uvicorn) doit écouter sur `localhost:8000`. Il doit démarrer en moins de 3 secondes après exécution de `python proxy.py`. | `Invoke-WebRequest http://localhost:8000/health` retourne HTTP 200 avec `{"status":"ok"}` dans les 3 secondes suivant le démarrage. |
| **REQ-2.1.2** | **Émulation exacte du format OpenAI Chat Completions** | Le proxy doit exposer l'endpoint `POST /v1/chat/completions` et `GET /v1/models` au format OpenAI. Roo Code configuré en mode "OpenAI Compatible" avec `Base URL: http://localhost:8000/v1` doit se connecter sans erreur. | Roo Code envoie une requête au proxy et reçoit une réponse sans message d'erreur de connexion ni de format. |
| **REQ-2.1.3** | **Extraction séparée du system prompt et du user prompt** | Le proxy doit analyser le tableau `messages` de la requête JSON et extraire séparément : (a) le message de rôle `system`, (b) les messages de rôle `user`, (c) les messages de rôle `assistant` (historique). Cette extraction doit fonctionner même si le tableau contient un historique multi-tours de N messages. | Pour un tableau `messages` de 10 éléments (1 system + 4 user + 5 assistant), les 3 catégories sont correctement identifiées et séparées. |
| **REQ-2.1.4** | **Mode "Gem dédié" : filtrage du system prompt** | Lorsque la variable d'environnement `USE_GEM_MODE=true` (valeur par défaut), le proxy doit omettre le message de rôle `system` lors de la copie dans le presse-papiers. Seuls les messages `user` et `assistant` sont transmis. | Avec `USE_GEM_MODE=true`, le texte copié dans le presse-papiers ne contient aucun contenu du message `system`. La réduction de taille est mesurable (≥ 50% pour un system prompt Roo Code standard). |
| **REQ-2.1.5** | **Nettoyage des contenus base64 (images)** | Le proxy doit détecter tout élément `content` de type `array` contenant des objets `{"type": "image_url", ...}` et les remplacer par la chaîne littérale exacte : `[IMAGE OMISE - Non supportee par le proxy clipboard]`. | Une requête contenant une image base64 est traitée sans erreur. Le presse-papiers contient le message de remplacement à la place de l'image. |

##### REQ-2.2 — Sous-domaine : Transfert Presse-Papiers (Uplink)

| ID | Exigence | Description Détaillée | Critère d'Acceptation |
| :--- | :--- | :--- | :--- |
| **REQ-2.2.1** | **Injection dans le presse-papiers Windows en moins de 500ms** | Après réception et traitement de la requête de Roo Code, le proxy doit copier le texte formaté dans le presse-papiers système Windows via `pyperclip.copy()`. | Le délai entre la réception de la requête HTTP et la disponibilité du texte dans le presse-papiers est inférieur à 500ms (mesuré par `Get-Clipboard` immédiatement après). |
| **REQ-2.2.2** | **Format lisible avec séparateurs explicites** | Le texte copié dans le presse-papiers doit utiliser les séparateurs suivants : `[SYSTEM PROMPT]\n{contenu}` (si `USE_GEM_MODE=false`), `[USER]\n{contenu}`, `[ASSISTANT]\n{contenu}`. Les sections sont séparées par `\n\n---\n\n`. | Un humain peut identifier visuellement les sections system/user/assistant dans le presse-papiers en moins de 5 secondes. |
| **REQ-2.2.3** | **Notification console horodatée** | Le proxy doit afficher dans la console : (a) l'heure au format `HH:MM:SS`, (b) la taille du prompt en caractères, (c) les 5 instructions d'action numérotées pour l'utilisateur, (d) le délai de timeout restant. | La console affiche ces 4 éléments à chaque requête reçue. |

##### REQ-2.3 — Sous-domaine : Attente et Capture de la Réponse (Downlink)

| ID | Exigence | Description Détaillée | Critère d'Acceptation |
| :--- | :--- | :--- | :--- |
| **REQ-2.3.1** | **Polling asynchrone du presse-papiers toutes les secondes** | Le proxy doit surveiller le presse-papiers via une boucle `asyncio` avec `await asyncio.sleep(POLLING_INTERVAL)` (défaut : 1.0 seconde). La boucle ne doit pas bloquer le thread principal FastAPI. | Pendant le polling, le serveur FastAPI répond toujours à `GET /health` sans délai. |
| **REQ-2.3.2** | **Détection du changement par comparaison de hash MD5** | Le proxy doit calculer `MD5(contenu_initial_copié)` au moment de la copie, puis comparer avec `MD5(contenu_actuel_presse_papiers)` à chaque itération de polling. La détection est déclenchée dès que les deux hashes diffèrent. | La détection se produit dans les 2 secondes suivant le moment où l'utilisateur copie la réponse Gemini (1 cycle de polling maximum). |
| **REQ-2.3.3** | **Timeout configurable avec réponse HTTP 408** | Si aucun changement de presse-papiers n'est détecté dans le délai `TIMEOUT_SECONDS` (défaut : 300 secondes), le proxy doit retourner une réponse HTTP 408 (Request Timeout) à Roo Code avec le message : `"Timeout: Relancez votre requête dans Roo Code."` | Avec `TIMEOUT_SECONDS=5` (test), le proxy retourne HTTP 408 après 5 secondes sans action utilisateur. |
| **REQ-2.3.4** | **Validation de la présence de balises XML Roo Code** | Après détection d'un changement de presse-papiers, le proxy doit vérifier la présence d'au moins une des balises XML Roo Code suivantes dans le contenu capturé : `<write_to_file>`, `<read_file>`, `<execute_command>`, `<attempt_completion>`, `<ask_followup_question>`, `<replace_in_file>`, `<list_files>`, `<search_files>`, `<browser_action>`, `<new_task>`. Si aucune balise n'est présente, un avertissement est affiché en console (non-bloquant). | Avec une réponse Gemini valide, aucun avertissement. Avec un texte sans balises XML, l'avertissement s'affiche mais la réponse est quand même transmise à Roo Code. |

##### REQ-2.4 — Sous-domaine : Réinjection vers Roo Code

| ID | Exigence | Description Détaillée | Critère d'Acceptation |
| :--- | :--- | :--- | :--- |
| **REQ-2.4.1** | **Support du streaming SSE en un seul chunk** | Le proxy doit détecter si la requête contient `"stream": true` et retourner une réponse au format Server-Sent Events (SSE) avec : (1) un chunk de contenu, (2) un chunk de fin avec `"finish_reason": "stop"`, (3) la ligne `data: [DONE]`. Si `"stream": false`, retourner une réponse JSON complète non-streamée. | Roo Code configuré avec streaming activé reçoit la réponse sans erreur. Roo Code configuré sans streaming reçoit aussi la réponse sans erreur. |
| **REQ-2.4.2** | **Format JSON OpenAI complet pour la réponse non-streamée** | La réponse JSON non-streamée doit contenir exactement les champs : `id` (format `chatcmpl-proxy-{8 hex chars}`), `object` (`"chat.completion"`), `created` (timestamp Unix), `model` (valeur du champ `model` de la requête), `choices[0].index` (`0`), `choices[0].message.role` (`"assistant"`), `choices[0].message.content` (contenu brut Gemini), `choices[0].finish_reason` (`"stop"`), `usage.prompt_tokens` (`0`), `usage.completion_tokens` (`0`), `usage.total_tokens` (`0`). | La réponse JSON est parseable par Roo Code sans erreur de désérialisation. |
| **REQ-2.4.3** | **Réponse HTTP 200 avec Content-Type application/json** | La réponse HTTP doit avoir le statut 200 OK et le header `Content-Type: application/json` pour la réponse non-streamée, ou `Content-Type: text/event-stream` pour la réponse SSE. | Les headers de réponse sont corrects dans les deux modes. |
| **REQ-2.4.4** | **Préservation intégrale du contenu Gemini** | Le contenu de la réponse Gemini (incluant les balises XML Roo Code) doit être transmis tel quel dans `choices[0].message.content`, sans aucune modification, suppression, ajout ou transformation de caractères. | Le contenu dans `choices[0].message.content` est identique (byte-for-byte) au contenu copié depuis Gemini. |

---

### 3.3 Domaine 3 — Agilité & Ségrégation des Rôles (REQ-3.x)

#### REQ-3.0 — Équipe Agile Virtuelle
Le système doit simuler une équipe Scrum complète via des Custom Modes Roo Code, chacun avec des responsabilités, des comportements et des permissions d'accès distincts et non-chevauchants.

| ID | Exigence | Description Détaillée | Critère d'Acceptation |
| :--- | :--- | :--- | :--- |
| **REQ-3.1** | **4 personas Agile dans `.roomodes`** | Le fichier `.roomodes` doit définir exactement 4 Custom Modes avec les slugs : `product-owner`, `scrum-master`, `developer`, `qa-engineer`. Chaque mode doit avoir un `roleDefinition` (system prompt comportemental) et des `groups` de permissions. | Les 4 modes apparaissent dans le sélecteur de mode Roo Code après chargement de `.roomodes`. |
| **REQ-3.2** | **Ségrégation stricte des permissions (RBAC)** | Les permissions de chaque persona sont définies par la matrice suivante (voir section 4.1). Aucun persona ne peut accéder à des ressources hors de sa matrice. | Test RBAC : le Product Owner ne peut pas créer de fichier `.py`. Le QA Engineer ne peut pas modifier `src/`. Le Scrum Master ne peut pas exécuter de commandes de test. |
| **REQ-3.3** | **Refus comportemental des actions hors périmètre** | Chaque persona doit refuser explicitement les demandes hors de son rôle et suggérer le persona approprié. Ce refus est inscrit dans le `roleDefinition` de chaque mode. | Si le mode `product-owner` reçoit "Écris du code Python", il répond en refusant et en suggérant de basculer vers le mode `developer`. |
| **REQ-3.4** | **Scrum Master : facilitateur pur sans exécution de tests** | Le Scrum Master peut lire tous les fichiers (y compris `docs/qa/`), écrire dans `memory-bank/` et `docs/`, et exécuter uniquement les commandes Git (`git add`, `git commit`, `git status`, `git log`). Il ne peut pas exécuter de commandes de test ni modifier le code source. | Le Scrum Master peut lire un rapport QA dans `docs/qa/` mais ne peut pas exécuter `pytest` ou `npm test`. |

---

### 3.4 Domaine 4 — Persistance & Banque de Mémoire (REQ-4.x)

#### REQ-4.0 — Mémoire Contextuelle Persistante
Le système doit maintenir une continuité de contexte absolue entre les sessions de développement via un système de fichiers Markdown structuré, versionnable et lisible par un humain.

| ID | Exigence | Description Détaillée | Critère d'Acceptation |
| :--- | :--- | :--- | :--- |
| **REQ-4.1** | **Stockage dans `memory-bank/` versionné sous Git** | La totalité de la mémoire contextuelle doit résider dans le répertoire `memory-bank/` à la racine du projet. Ce répertoire doit être inclus dans le suivi Git (non exclu par `.gitignore`). | `git ls-files memory-bank/` liste les 7 fichiers Memory Bank. |
| **REQ-4.2** | **Séquence obligatoire VÉRIFIER → CRÉER → LIRE → AGIR** | À chaque démarrage de session, l'agent doit suivre cette séquence exacte et non-négociable : (1) VÉRIFIER l'existence de `activeContext.md` et `progress.md`. (2) Si absents : CRÉER immédiatement depuis les templates définis dans `.clinerules`, puis passer à l'étape 3. (3) LIRE `activeContext.md` puis `progress.md`. (4) AGIR sur la demande de l'utilisateur. Cette séquence s'applique à tous les modes et toutes les sessions sans exception. | Après fermeture et réouverture de VS Code, l'agent lit `activeContext.md` avant toute action. Si les fichiers sont supprimés manuellement, l'agent les recrée depuis les templates avant d'agir. |
| **REQ-4.3** | **Mise à jour obligatoire avant clôture de tâche** | Avant d'exécuter `attempt_completion`, l'agent doit obligatoirement mettre à jour : (a) `activeContext.md` avec l'état courant et la prochaine action, (b) `progress.md` avec les features validées. Si une décision d'architecture a été prise : (c) `decisionLog.md` avec un ADR horodaté. | L'historique Git montre un commit de mise à jour Memory Bank avant chaque commit de code. |
| **REQ-4.4** | **7 fichiers thématiques distincts et non-chevauchants** | La Memory Bank doit être composée exactement de ces 7 fichiers, chacun avec une responsabilité unique : `projectBrief.md` (vision, non-goals, contraintes), `productContext.md` (user stories, backlog), `systemPatterns.md` (architecture, conventions), `techContext.md` (stack, commandes, variables d'env), `activeContext.md` (tâche en cours, état actuel), `progress.md` (checklist phases et features), `decisionLog.md` (ADR horodatés). | Les 7 fichiers existent dans `memory-bank/` avec des contenus non-redondants. |
| **REQ-4.5** | **Versionnement Git de toute modification Memory Bank** | Toute modification d'un fichier `memory-bank/*.md` doit être incluse dans un commit Git avec un message au format `docs(memory): {description}`. | `git log --oneline -- memory-bank/` montre des commits avec le préfixe `docs(memory):`. |

---

### 3.5 Domaine 5 — Configuration Gemini Chrome (REQ-5.x)

#### REQ-5.0 — Préparation de l'Interface Gemini Web
Pour que le proxy fonctionne de bout en bout, l'interface Gemini Chrome doit être configurée pour répondre dans le format attendu par Roo Code.

| ID | Exigence | Description Détaillée | Critère d'Acceptation |
| :--- | :--- | :--- | :--- |
| **REQ-5.1** | **Gem dédié "Roo Code Agent" avec system prompt complet** | Un profil "Gem" doit être créé dans Gemini Web (gemini.google.com > Gems) avec le nom exact "Roo Code Agent". Les instructions du Gem doivent contenir l'intégralité du system prompt Roo Code défini dans `template/prompts/SP-007-gem-gemini-roo-agent.md`. | Le Gem "Roo Code Agent" existe dans l'interface Gemini. Ses instructions correspondent exactement au contenu de `template/prompts/SP-007-gem-gemini-roo-agent.md`. |
| **REQ-5.2** | **Réponses Gemini exclusivement en balises XML Roo Code** | Le Gem doit être configuré pour répondre uniquement avec des balises XML Roo Code, sans texte de courtoisie avant la première balise ni après la dernière. | Sur 5 requêtes de test, Gemini répond avec des balises XML valides sans texte parasite. |
| **REQ-5.3** | **Maintien de l'historique de conversation multi-tours** | Le Gem doit prendre en compte l'historique de conversation transmis par le proxy dans le presse-papiers pour assurer la cohérence des réponses sur plusieurs échanges consécutifs. | Une séquence de 3 requêtes liées (créer fichier → modifier fichier → tester fichier) produit des réponses cohérentes sans répétition ni contradiction. |

---

### 3.6 Domaine 6 — Mode Cloud Direct via API Anthropic (REQ-6.x)

#### REQ-6.0 — Connexion Directe à l'API Anthropic Claude
Le système doit permettre à Roo Code de se connecter directement à l'API officielle Anthropic pour utiliser Claude Sonnet comme backend LLM, sans proxy intermédiaire ni intervention humaine.

| ID | Exigence | Description Détaillée | Critère d'Acceptation |
| :--- | :--- | :--- | :--- |
| **REQ-6.1** | **Clé API Anthropic valide et stockée de manière sécurisée** | L'utilisateur doit disposer d'une clé API Anthropic valide au format `sk-ant-api03-...`. Cette clé doit être stockée exclusivement dans les paramètres chiffrés de l'extension Roo Code (VS Code SecretStorage). | La clé API est fonctionnelle (test de connexion réussi). Elle n'apparaît dans aucun fichier du projet (`.env`, `.clinerules`, `.roomodes`, `memory-bank/`, etc.). |
| **REQ-6.2** | **Modèle `claude-sonnet-4-6` comme référence** | Roo Code doit être configuré pour utiliser le modèle `claude-sonnet-4-6`. Ce modèle répond nativement aux balises XML Roo Code sans configuration supplémentaire du format de réponse. **Note de maintenance :** Vérifier périodiquement la liste des modèles disponibles sur https://docs.anthropic.com/en/docs/about-claude/models et mettre à jour ce document avec la dernière version stable de la gamme Sonnet. | Roo Code envoie une requête à `claude-sonnet-4-6` et reçoit une réponse avec des balises XML valides. |
| **REQ-6.3** | **Connexion via le provider natif "Anthropic" de Roo Code** | La connexion à l'API Anthropic doit utiliser le fournisseur natif "Anthropic" intégré dans Roo Code, sans aucun proxy ou middleware. L'endpoint est `https://api.anthropic.com`. | Roo Code se connecte directement à `api.anthropic.com`. Aucun processus proxy local n'est nécessaire. |
| **REQ-6.4** | **Interdiction absolue de versionnement de la clé API** | La clé API Anthropic ne doit jamais apparaître dans aucun fichier du projet, versionné ou non. Elle est stockée exclusivement dans VS Code SecretStorage (chiffré, non accessible depuis le système de fichiers). | `git grep "sk-ant"` dans le dépôt retourne zéro résultat. |

---

### 3.7 Domaine 7 — Registre Central des Prompts Système (REQ-7.x)

#### REQ-7.0 — Registre Centralisé des System Prompts
Le système doit maintenir un répertoire `prompts/` contenant une version canonique et à jour de chaque system prompt utilisé dans le workbench, avec identification précise de sa cible de déploiement.

| ID | Exigence | Description Détaillée | Critère d'Acceptation |
| :--- | :--- | :--- | :--- |
| **REQ-7.1** | **7 fichiers SP canoniques dans `prompts/`** | Le répertoire `prompts/` doit contenir exactement 7 fichiers canoniques nommés `SP-001-ollama-modelfile-system.md` à `SP-007-gem-gemini-roo-agent.md`, plus un fichier `README.md` d'index. Chaque fichier SP doit avoir un en-tête YAML avec les champs : `id`, `name`, `version` (format MAJOR.MINOR.PATCH), `last_updated`, `status`, `target_type`, `target_file`, `target_field`, `target_location`, `depends_on`, `changelog`. | `Get-ChildItem prompts/` liste 8 fichiers (7 SP + README). Chaque SP a un en-tête YAML valide avec tous les champs requis. |
| **REQ-7.2** | **Identification sans ambiguïté de la cible de déploiement** | Chaque fichier SP doit spécifier : (a) `target_file` : chemin exact du fichier cible (ex: `Modelfile`, `.clinerules`, `.roomodes`), (b) `target_field` : champ exact dans le fichier cible (ex: `Bloc SYSTEM`, `fichier entier`, `customModes[2].roleDefinition`), (c) `target_location` : procédure de déploiement en langage naturel. Pour SP-007 (Gem Gemini, externe Git) : `hors_git: true` et procédure manuelle documentée. | Un développeur peut déployer n'importe quel SP sans ambiguïté en lisant uniquement son fichier canonique. |
| **REQ-7.3** | **Cohérence obligatoire avant commit (REGLE 6)** | Toute modification d'un artefact lié à un prompt (`template/proxy.py`, `.roomodes`, `.clinerules`, `Modelfile`) doit déclencher une vérification et mise à jour du fichier SP correspondant dans `prompts/`. Cette obligation est inscrite dans REGLE 6 de `.clinerules`. | Un commit modifiant `.clinerules` sans mettre à jour `template/prompts/SP-002-clinerules-global.md` est bloqué par le hook pre-commit (REQ-8.2). |
| **REQ-7.4** | **Versionnement sémantique des prompts** | Chaque fichier SP doit maintenir un `changelog` avec numéro de version sémantique (MAJOR.MINOR.PATCH) et description des modifications. La version est incrémentée à chaque modification : PATCH pour correction mineure, MINOR pour ajout de règle, MAJOR pour refonte complète. | Le champ `changelog` de chaque SP contient au moins une entrée. La version dans l'en-tête YAML correspond à la dernière entrée du changelog. |
| **REQ-7.5** | **Déploiement manuel documenté pour SP-007** | SP-007 (Gem Gemini) étant externe à Git, sa procédure de déploiement manuel doit être documentée dans le fichier SP-007 lui-même. Tout commit modifiant SP-007 doit inclure la mention `DEPLOIEMENT MANUEL REQUIS` dans le message de commit. | SP-007 contient `hors_git: true` dans son en-tête YAML. REGLE 6.2 de `.clinerules` impose la mention dans le message de commit. |

---

### 3.8 Domaine 8 — Vérification Automatique de Cohérence des Prompts (REQ-8.x)

#### REQ-8.0 — Détection Automatique de Désynchronisation Prompt/Artefact
Le système doit fournir un mécanisme automatique de détection des désynchronisations entre les fichiers SP canoniques du registre `prompts/` et leurs artefacts cibles déployés (`.clinerules`, `.roomodes`, `Modelfile`).

| ID | Exigence | Description Détaillée | Critère d'Acceptation |
| :--- | :--- | :--- | :--- |
| **REQ-8.1** | **Script PowerShell `template/template/scripts/check-prompts-sync.ps1`** | Un script PowerShell doit comparer le contenu de chaque fichier SP canonique avec son artefact cible déployé. La comparaison doit être normalisée : (a) normalisation des retours à la ligne (`\r\n` → `\n` via guillemets doubles PowerShell), (b) désérialisation JSON pour `.roomodes` avant extraction du `roleDefinition`, (c) extraction du contenu entre les balises de code markdown du fichier SP via regex robuste. Le script retourne exit code 0 si tout est synchronisé, exit code 1 si désynchronisation détectée. | `.\scripts\check-prompts-sync.ps1` retourne exit code 0 après une installation propre. Retourne exit code 1 si `.clinerules` est modifié sans mettre à jour SP-002. |
| **REQ-8.2** | **Hook Git pre-commit bloquant** | Un hook Git `.git/hooks/pre-commit` doit appeler automatiquement `check-prompts-sync.ps1` avant chaque commit et bloquer le commit (exit code 1) si une désynchronisation est détectée. Le message de blocage doit indiquer quel SP est désynchronisé. | Un commit avec `.clinerules` modifié mais SP-002 non mis à jour est bloqué avec un message explicatif. Un commit avec les deux fichiers mis à jour passe sans blocage. |
| **REQ-8.3** | **Rapport de vérification avec diff lisible** | Le script doit produire un rapport structuré avec : (a) statut par SP (`[SYNC]` en vert ou `[DESYNC]` en rouge), (b) nom du fichier SP et nom de l'artefact cible, (c) en cas de désynchronisation : affichage des 200 premiers caractères du contenu SP canonique ET du contenu déployé pour permettre l'identification visuelle de la différence. | Un utilisateur peut identifier en moins de 10 secondes quel prompt est désynchronisé et quelle est la différence approximative. |
| **REQ-8.4** | **Exclusion de SP-007 de la vérification automatique** | SP-007 (Gem Gemini, externe Git) doit être exclu de la vérification automatique. Le script doit afficher `[MANUEL] SP-007 : VÉRIFICATION MANUELLE REQUISE` en magenta sans bloquer le commit. Ce message compte comme un avertissement, pas comme une erreur. | Le script affiche le message `[MANUEL]` pour SP-007 mais retourne exit code 0 si les autres SP sont synchronisés. |

---

## 4. Matrices de Traçabilité

### 4.1 Matrice RBAC des Permissions par Persona

| Permission | Product Owner | Scrum Master | Developer | QA Engineer |
| :--- | :---: | :---: | :---: | :---: |
| Lecture de tous les fichiers (`read`) | ✅ | ✅ | ✅ | ✅ |
| Écriture `memory-bank/productContext.md` | ✅ | ✅ | ✅ | ❌ |
| Écriture `memory-bank/*.md` (tous) | ❌ | ✅ | ✅ | ❌ |
| Écriture `docs/*.md` (documentation) | ✅ | ✅ | ✅ | ❌ |
| Écriture `docs/qa/*.md` (rapports QA) | ❌ | ❌ | ❌ | ✅ |
| Écriture code source (`src/`, `*.py`, etc.) | ❌ | ❌ | ✅ | ❌ |
| Exécution terminal général (`command`) | ❌ | ❌ | ✅ | ❌ |
| Exécution commandes Git uniquement | ❌ | ✅ | ✅ | ❌ |
| Exécution commandes de test | ❌ | ❌ | ✅ | ✅ |
| Accès navigateur (`browser`) | ❌ | ❌ | ✅ | ✅ |
| Accès MCP (`mcp`) | ❌ | ❌ | ✅ | ❌ |

**Commandes Git autorisées pour le Scrum Master :** `git add`, `git commit`, `git status`, `git log` uniquement.
**Commandes de test autorisées pour le QA Engineer :** `npm test`, `npm run test`, `pytest`, `python -m pytest`, `dotnet test`, `go test`, `git status`, `git log`.

### 4.2 Matrice de Traçabilité des Exigences

| ID Exigence | Domaine | Priorité | Dépendances |
| :--- | :--- | :--- | :--- |
| REQ-000 | Fondamental | CRITIQUE | — |
| REQ-1.0 | Moteur Local | HAUTE | REQ-000 |
| REQ-1.1 | Moteur Local — Modèle | HAUTE | REQ-1.0 |
| REQ-1.2 | Moteur Local — Contexte | HAUTE | REQ-1.0 |
| REQ-1.3 | Moteur Local — Déterminisme | HAUTE | REQ-1.0 |
| REQ-1.4 | Moteur Local — Boomerang | MOYENNE | REQ-1.1 |
| REQ-2.0 | Proxy Hybride | HAUTE | REQ-000 |
| REQ-2.1.1 | Proxy — Serveur | CRITIQUE | REQ-2.0 |
| REQ-2.1.2 | Proxy — Format OpenAI | CRITIQUE | REQ-2.1.1 |
| REQ-2.1.3 | Proxy — Extraction messages | HAUTE | REQ-2.1.1 |
| REQ-2.1.4 | Proxy — Filtrage system prompt | MOYENNE | REQ-2.1.3 |
| REQ-2.1.5 | Proxy — Nettoyage images | MOYENNE | REQ-2.1.3 |
| REQ-2.2.1 | Proxy — Uplink presse-papiers | CRITIQUE | REQ-2.1.3 |
| REQ-2.2.2 | Proxy — Format lisible | HAUTE | REQ-2.2.1 |
| REQ-2.2.3 | Proxy — Notification console | HAUTE | REQ-2.2.1 |
| REQ-2.3.1 | Proxy — Polling async | CRITIQUE | REQ-2.2.1 |
| REQ-2.3.2 | Proxy — Détection hash MD5 | CRITIQUE | REQ-2.3.1 |
| REQ-2.3.3 | Proxy — Timeout HTTP 408 | HAUTE | REQ-2.3.1 |
| REQ-2.3.4 | Proxy — Validation balises XML | MOYENNE | REQ-2.3.2 |
| REQ-2.4.1 | Proxy — Streaming SSE | CRITIQUE | REQ-2.3.2 |
| REQ-2.4.2 | Proxy — Format JSON OpenAI | CRITIQUE | REQ-2.4.1 |
| REQ-2.4.3 | Proxy — Headers HTTP | CRITIQUE | REQ-2.4.1 |
| REQ-2.4.4 | Proxy — Préservation contenu | HAUTE | REQ-2.4.1 |
| REQ-3.0 | Agilité | HAUTE | REQ-000 |
| REQ-3.1 | Agilité — 4 personas | HAUTE | REQ-3.0 |
| REQ-3.2 | Agilité — RBAC | HAUTE | REQ-3.1 |
| REQ-3.3 | Agilité — Refus comportemental | MOYENNE | REQ-3.2 |
| REQ-3.4 | Agilité — SM facilitateur pur | HAUTE | REQ-3.2 |
| REQ-4.0 | Mémoire | HAUTE | REQ-000 |
| REQ-4.1 | Mémoire — Stockage Git | CRITIQUE | REQ-4.0 |
| REQ-4.2 | Mémoire — Séquence VÉRIFIER→CRÉER→LIRE→AGIR | CRITIQUE | REQ-4.1 |
| REQ-4.3 | Mémoire — Écriture avant clôture | CRITIQUE | REQ-4.1 |
| REQ-4.4 | Mémoire — 7 fichiers thématiques | HAUTE | REQ-4.1 |
| REQ-4.5 | Mémoire — Versionnement Git | MOYENNE | REQ-4.1 |
| REQ-5.0 | Gemini Config | HAUTE | REQ-2.0 |
| REQ-5.1 | Gemini — Gem dédié | CRITIQUE | REQ-5.0 |
| REQ-5.2 | Gemini — Format XML | CRITIQUE | REQ-5.1 |
| REQ-5.3 | Gemini — Historique multi-tours | HAUTE | REQ-5.1 |
| REQ-6.0 | Cloud API Directe | HAUTE | REQ-000 |
| REQ-6.1 | Cloud — Clé API sécurisée | CRITIQUE | REQ-6.0 |
| REQ-6.2 | Cloud — Modèle claude-sonnet-4-6 | CRITIQUE | REQ-6.0 |
| REQ-6.3 | Cloud — Provider natif Roo Code | CRITIQUE | REQ-6.0 |
| REQ-6.4 | Cloud — Interdiction versionnement clé | CRITIQUE | REQ-6.1 |
| REQ-7.0 | Registre Prompts | HAUTE | REQ-000 |
| REQ-7.1 | Registre — 7 fichiers SP canoniques | HAUTE | REQ-7.0 |
| REQ-7.2 | Registre — Cibles sans ambiguïté | CRITIQUE | REQ-7.1 |
| REQ-7.3 | Registre — Cohérence avant commit | CRITIQUE | REQ-7.1, REQ-5.x |
| REQ-7.4 | Registre — Versionnement sémantique | HAUTE | REQ-7.1 |
| REQ-7.5 | Registre — Déploiement manuel SP-007 | HAUTE | REQ-7.2, REQ-5.x |
| REQ-8.0 | Vérification Cohérence | HAUTE | REQ-7.0 |
| REQ-8.1 | Vérification — Script PowerShell normalisé | HAUTE | REQ-7.1, REQ-7.2 |
| REQ-8.2 | Vérification — Hook pre-commit bloquant | HAUTE | REQ-8.1 |
| REQ-8.3 | Vérification — Rapport avec diff lisible | MOYENNE | REQ-8.1 |
| REQ-8.4 | Vérification — Exclusion SP-007 | HAUTE | REQ-7.5, REQ-8.1 |

---

## 5. Contraintes et Non-Goals

### 5.1 Contraintes

- Le système doit fonctionner sur un laptop Windows 10/11 avec VS Code sans serveur dédié ni infrastructure cloud payante (sauf Mode Cloud qui implique des coûts API Anthropic à l'usage).
- Le proxy Gemini Chrome repose sur une intervention humaine minimale (copier-coller) : ce n'est pas un système entièrement automatisé.
- La qualité des réponses en mode Gemini Chrome dépend de la disponibilité et du comportement de l'interface web Gemini (hors contrôle du système).
- Le Mode Cloud (Claude API) implique des coûts à l'usage selon la tarification Anthropic en vigueur.
- Le modèle Ollama `mychen76/qwen3_cline_roocode:32b` est une dépendance externe sans fallback documenté — sa disponibilité sur Ollama Hub est une précondition d'installation.

### 5.2 Non-Goals

- Ce système ne vise PAS à automatiser le copier-coller vers Gemini Chrome (pas d'automatisation de navigateur type Selenium).
- Ce système ne vise PAS à gérer des projets multi-utilisateurs ou des environnements distribués.
- Ce système ne vise PAS à supporter des modèles LLM autres que les trois modes documentés dans cette version 1.0.
- Ce système ne vise PAS à remplacer un vrai outil de gestion de projet Agile (Jira, Linear, etc.) — il simule les rôles Agile pour le développement assisté par IA.
- Le Mode Proxy Gemini ne supporte PAS les Boomerang Tasks (`new_task`) — deux instances Roo Code concurrentes partagent le même presse-papiers, créant un deadlock. Utiliser le Mode Local (Ollama) ou le Mode Cloud (Claude API) pour les tâches nécessitant des sous-agents.

### 5.3 Tableau Comparatif des 3 Modes LLM

| Critère | Mode Local (Ollama) | Mode Proxy (Gemini Chrome) | Mode Cloud (Claude API) |
| :--- | :--- | :--- | :--- |
| **Coût** | Gratuit | Gratuit | Payant (à l'usage) |
| **Intervention humaine** | Aucune | Copier-coller à chaque requête | Aucune |
| **Qualité du raisonnement** | Haute (32B local) | Très haute (Gemini Pro) | Très haute (Claude Sonnet) |
| **Vitesse** | Dépend du hardware | Dépend de l'humain | Rapide (API directe) |
| **Souveraineté des données** | Totale (100% local) | Partielle (données envoyées à Google) | Partielle (données envoyées à Anthropic) |
| **Disponibilité** | Toujours (hors ligne) | Nécessite Chrome + compte Google | Nécessite Internet + clé API |
| **Streaming** | Natif Ollama | SSE en un seul chunk (proxy) | Natif Anthropic |
| **Configuration Roo Code** | Provider: Ollama | Provider: OpenAI Compatible | Provider: Anthropic |
| **Exigences PRD** | REQ-1.x | REQ-2.x, REQ-5.x | REQ-6.x |

---

## Annexe A — Table des Références

| Réf. | Type | Titre / Identifiant | Description |
| :--- | :--- | :--- | :--- |
| [DOC1] | Document interne | `workbench/DOC1-PRD-Workbench-Requirements.md` | Ce document — Product Requirements Document v2.0 |
| [DOC2] | Document interne | `workbench/DOC2-ARCH-Workbench-Technical-Design.md` | Architecture, Solution et Stack Technique v2.0 |
| [DOC3] | Document interne | `workbench/DOC3-BUILD-Workbench-Assembly-Phases.md` | Plan d'Implémentation Séquentiel Complet v3.0 (Phases 0–12) |
| [DOC4] | Document interne | `workbench/DOC4-GUIDE-Workbench-Deployment-Howto.md` | Guide de Déploiement de l'Atelier sur projets nouveaux et existants |
| [DOC5] | Document interne | `workbench/DOC5-GUIDE-Project-Development-Process.md` | Manuel du Processus Agile Applicatif v1.0 — processus, nomenclature artifacts, anti-risques agentiques, protocoles de session |
| [SP-001] | System Prompt | `template/prompts/SP-001-ollama-modelfile-system.md` | System prompt du Modelfile Ollama (bloc SYSTEM) |
| [SP-002] | System Prompt | `template/prompts/SP-002-clinerules-global.md` | Contenu canonique du fichier `.clinerules` (6 règles impératives) |
| [SP-003] | System Prompt | `template/prompts/SP-003-persona-product-owner.md` | `roleDefinition` du persona Product Owner dans `.roomodes` |
| [SP-004] | System Prompt | `template/prompts/SP-004-persona-scrum-master.md` | `roleDefinition` du persona Scrum Master dans `.roomodes` |
| [SP-005] | System Prompt | `template/prompts/SP-005-persona-developer.md` | `roleDefinition` du persona Developer dans `.roomodes` |
| [SP-006] | System Prompt | `template/prompts/SP-006-persona-qa-engineer.md` | `roleDefinition` du persona QA Engineer dans `.roomodes` |
| [SP-007] | System Prompt | `template/prompts/SP-007-gem-gemini-roo-agent.md` | Instructions du Gem Gemini "Roo Code Agent" (déploiement manuel, hors Git) |
| [LAAW] | Source externe | Blueprint LAAW — mychen76 | Blueprint "Local Agentic Agile Workflow" — source d'inspiration principale pour la Memory Bank et les personas Agile |
| [PROXY] | Source externe | Proxy API Gemini Chrome | Mécanisme de pont réseau-presse-papiers permettant à Roo Code d'utiliser Gemini Web gratuitement |
| [OLLAMA] | Outil externe | https://ollama.com | Moteur d'inférence LLM local, gère les modèles Qwen3 |
| [ANTHROPIC] | API externe | https://api.anthropic.com | API officielle Anthropic pour Claude Sonnet |
| [GEMINI] | Interface externe | https://gemini.google.com | Interface web Gemini de Google, utilisée en mode Proxy Chrome |
| [ROOCODE] | Extension VS Code | Roo Code (extension VS Code) | Moteur d'exécution agentique central — orchestre tous les composants |
| [OPENAI-FMT] | Standard | Format OpenAI Chat Completions | Standard d'API `/v1/chat/completions` émulé par le proxy pour compatibilité Roo Code |
| [SEMVER] | Standard | Semantic Versioning (semver.org) | Convention de versionnement MAJOR.MINOR.PATCH utilisée pour les fichiers SP et le workbench |

---

## Annexe B — Table des Abréviations

| Abréviation | Forme complète | Explication |
| :--- | :--- | :--- |
| **ADR** | Architecture Decision Record | Enregistrement horodaté d'une décision d'architecture avec contexte, décision prise et conséquences. Stocké dans `memory-bank/decisionLog.md`. |
| **API** | Application Programming Interface | Interface de programmation permettant à deux logiciels de communiquer. Ici : API Ollama (locale), API Anthropic (cloud), API OpenAI (format émulé). |
| **ASGI** | Asynchronous Server Gateway Interface | Standard Python pour les serveurs web asynchrones. Uvicorn est un serveur ASGI utilisé par FastAPI. |
| **DA** | Décision d'Architecture | Identifiant des décisions d'architecture dans DOC2 (ex: DA-001, DA-014). Chaque DA justifie un choix technique et référence les exigences PRD adressées. |
| **GEM** | Gem Gemini | Profil personnalisé dans l'interface Gemini Web (gemini.google.com > Gems) contenant un system prompt dédié. Ici : "Roo Code Agent" avec SP-007. |
| **Git** | — (nom propre) | Système de contrôle de version distribué. Utilisé pour versionner le code source, la Memory Bank et les fichiers de configuration. |
| **GPU** | Graphics Processing Unit | Processeur graphique utilisé pour accélérer l'inférence des modèles LLM locaux via Ollama. |
| **HTTP** | HyperText Transfer Protocol | Protocole de communication web. Le proxy écoute sur HTTP (localhost:8000). L'API Anthropic utilise HTTPS. |
| **HTTPS** | HTTP Secure | Version chiffrée de HTTP. Utilisée pour les connexions à l'API Anthropic et à Gemini Web. |
| **JSON** | JavaScript Object Notation | Format de données texte structuré. Utilisé pour `.roomodes`, les réponses API OpenAI, et les requêtes du proxy. |
| **LAAW** | Local Agentic Agile Workflow | Blueprint de développement agentique local créé par mychen76, source d'inspiration principale pour la Memory Bank et les personas Agile du workbench. |
| **LLM** | Large Language Model | Grand modèle de langage. Exemples : Qwen3-32B (local via Ollama), Gemini Pro (cloud Google), Claude Sonnet (cloud Anthropic). |
| **MD5** | Message Digest 5 | Algorithme de hachage utilisé par le proxy pour détecter les changements dans le presse-papiers (comparaison de hash avant/après). |
| **MCP** | Model Context Protocol | Protocole d'extension de Roo Code permettant d'intégrer des outils externes. Accessible uniquement au persona Developer. |
| **NTFS** | New Technology File System | Système de fichiers Windows utilisé pour stocker la Memory Bank et les fichiers de configuration. |
| **PO** | Product Owner | Persona Agile responsable de la vision produit, des User Stories et du backlog. Correspond au mode `product-owner` dans `.roomodes`. |
| **PRD** | Product Requirements Document | Document d'exigences produit. Ce document (DOC1) définit toutes les exigences atomiques du système le workbench. |
| **RBAC** | Role-Based Access Control | Contrôle d'accès basé sur les rôles. Chaque persona Agile a une matrice de permissions précise définissant ce qu'il peut lire, écrire et exécuter. |
| **REQ** | Requirement (Exigence) | Identifiant des exigences dans ce PRD (ex: REQ-000, REQ-2.1.4). Format : REQ-{domaine}.{sous-domaine}. |
| **REST** | Representational State Transfer | Style d'architecture pour les API web. Ollama expose une API REST sur localhost:11434. |
| **SM** | Scrum Master | Persona Agile facilitateur pur : gère la Memory Bank et les commits Git, mais ne code pas et n'exécute pas de tests. |
| **SP** | System Prompt | Fichier canonique du registre `template/prompts/` contenant un prompt système avec métadonnées YAML (id, version, cible, changelog). |
| **SSE** | Server-Sent Events | Protocole de streaming HTTP unidirectionnel (serveur → client). Le proxy retourne les réponses Gemini en SSE quand `stream: true`. |
| **le workbench** | Agentic Agile Workbench | Nom du système décrit dans ce document. Combine Roo Code, Ollama, le proxy Gemini Chrome et l'API Anthropic dans un environnement de développement agentique unifié. |
| **VRAM** | Video Random Access Memory | Mémoire de la carte graphique. Le modèle Qwen3-32B nécessite 8+ Go de VRAM pour une inférence GPU optimale. |
| **VS Code** | Visual Studio Code | Éditeur de code Microsoft, environnement de développement principal du workbench. |
| **YAML** | YAML Ain't Markup Language | Format de sérialisation de données lisible par l'humain. Utilisé pour les en-têtes des fichiers SP canoniques. |

---

## Annexe C — Glossaire

| Terme | Définition |
| :--- | :--- |
| **Agent agentique** | Programme IA capable d'exécuter des actions autonomes (lire/écrire des fichiers, exécuter des commandes, appeler des APIs) en réponse à des instructions en langage naturel, sans intervention humaine à chaque étape. |
| **Atelier (Workbench)** | Ce dépôt (`agentic-agile-workbench`). Contient les outils, règles et processus réutilisables pour développer des projets applicatifs. S'oppose au "projet" qui contient le code métier. |
| **Balises XML Roo Code** | Syntaxe spéciale utilisée par Roo Code pour déclencher des actions : `<write_to_file>`, `<read_file>`, `<execute_command>`, `<attempt_completion>`, etc. Tout LLM connecté à Roo Code doit répondre avec ces balises. |
| **Boomerang Tasks** | Mécanisme de Roo Code permettant à l'agent principal (32B) de déléguer une sous-tâche à un modèle secondaire (7B), puis de récupérer le résultat dans sa propre boucle de décision. |
| **Clipboard / Presse-papiers** | Zone mémoire temporaire de Windows (Ctrl+C / Ctrl+V). Le proxy utilise le presse-papiers comme canal de communication entre Roo Code et Gemini Web. |
| **Commit Git** | Instantané versionné de l'état du dépôt. Chaque modification significative (code, Memory Bank, configuration) doit faire l'objet d'un commit avec un message descriptif au format Conventional Commits. |
| **Conventional Commits** | Convention de messages de commit : `type(scope): description`. Types utilisés : `feat`, `fix`, `docs`, `chore`, `refactor`, `test`. |
| **Déterminisme** | Propriété d'un modèle LLM à produire des réponses stables et reproductibles. Obtenu en fixant `temperature 0.15`, `min_p 0.03`, `top_p 0.95`, `repeat_penalty 1.1` dans le Modelfile. |
| **Fenêtre de contexte** | Nombre maximum de tokens qu'un LLM peut traiter simultanément. Fixée à 128K tokens (`num_ctx 131072`) pour permettre le chargement du code source ET de la Memory Bank. |
| **Fine-tuning** | Entraînement supplémentaire d'un modèle LLM sur des données spécifiques. `mychen76/qwen3_cline_roocode:32b` est fine-tuné pour le Tool Calling de Roo Code. |
| **Gem Gemini** | Profil personnalisé dans l'interface Gemini Web contenant un system prompt permanent. Le Gem "Roo Code Agent" contient SP-007 et répond exclusivement avec des balises XML Roo Code. |
| **Hook Git pre-commit** | Script exécuté automatiquement par Git avant chaque commit. Utilisé pour vérifier la cohérence des prompts (REQ-8.2) et bloquer le commit si désynchronisation détectée. |
| **Memory Bank** | Système de 7 fichiers Markdown dans `memory-bank/` qui persistent le contexte entre les sessions Roo Code. Remplace la mémoire volatile du LLM par une mémoire durable et auditable. |
| **Modelfile** | Fichier de configuration Ollama définissant le modèle de base, les paramètres d'inférence et le system prompt. Compilé avec `ollama create uadf-agent -f Modelfile`. |
| **Mode Cloud** | Configuration Roo Code utilisant l'API Anthropic directe (`claude-sonnet-4-6`). Entièrement automatisé, payant à l'usage, nécessite une clé API. |
| **Mode Local** | Configuration Roo Code utilisant Ollama en local (`mychen76/qwen3_cline_roocode:32b`). Gratuit, souverain, fonctionne hors ligne. |
| **Mode Proxy** | Configuration Roo Code utilisant le proxy FastAPI local qui relaie les requêtes vers Gemini Web via le presse-papiers. Gratuit, nécessite une intervention humaine (copier-coller). |
| **Persona Agile** | Mode Roo Code simulant un rôle Scrum : Product Owner, Scrum Master, Developer, QA Engineer. Chaque persona a un `roleDefinition` (comportement) et des `groups` (permissions RBAC). |
| **Polling** | Technique de vérification périodique d'un état. Le proxy vérifie le presse-papiers toutes les secondes (`asyncio.sleep(1.0)`) pour détecter la réponse Gemini. |
| **Proxy** | Intermédiaire réseau. Ici : serveur FastAPI local (`template/proxy.py`) qui intercepte les requêtes Roo Code, les relaie vers Gemini Web via le presse-papiers, et retourne la réponse à Roo Code. |
| **Registre de prompts** | Répertoire `template/prompts/` contenant les versions canoniques et versionnées de tous les system prompts du workbench. Source de vérité unique. |
| **Séquence VÉRIFIER→CRÉER→LIRE→AGIR** | Protocole obligatoire au démarrage de chaque session Roo Code : (1) vérifier l'existence des fichiers Memory Bank, (2) les créer si absents, (3) les lire, (4) agir sur la demande. Défini dans REGLE 1 de `.clinerules`. |
| **SemVer** | Semantic Versioning. Format MAJOR.MINOR.PATCH : MAJOR = rupture de compatibilité, MINOR = nouvelle fonctionnalité rétrocompatible, PATCH = correction de bug. |
| **System Prompt** | Instructions permanentes données à un LLM avant toute interaction utilisateur. Définit le comportement, les règles et les contraintes de l'agent. |
| **Token** | Unité de traitement d'un LLM. Environ 0,75 mot en français. La fenêtre de 128K tokens ≈ 96 000 mots ≈ un roman de taille moyenne. |
| **Tool Calling** | Capacité d'un LLM à appeler des fonctions/outils externes en générant des requêtes structurées (JSON ou XML). `mychen76/qwen3_cline_roocode:32b` est fine-tuné pour le Tool Calling de Roo Code. |
| **VS Code SecretStorage** | Mécanisme de stockage chiffré intégré à VS Code. Utilisé pour stocker la clé API Anthropic de manière sécurisée, sans jamais l'écrire dans un fichier. |
