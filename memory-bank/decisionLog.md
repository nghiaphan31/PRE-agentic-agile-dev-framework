# Decision Log — Architecture Decision Records (ADR)

---

## ADR-001 : Choix du moteur d'inférence local
**Date :** 2026-03-23
**Statut :** Accepté

**Contexte :**
Besoin d'un moteur d'inférence LLM local, gratuit et compatible avec l'API OpenAI pour Roo Code.

**Décision :**
Utilisation d'Ollama avec le modèle mychen76/qwen3_cline_roocode:14b compilé en uadf-agent.
(Déviation par rapport à DOC3 : 32b → 14b, RTX 5060 Ti 16 Go VRAM insuffisant pour 32b)

**Conséquences :**
- Avantage : Souveraineté totale, gratuit, compatible OpenAI
- Avantage : Modèle spécifiquement optimisé pour le Tool Calling Roo Code
- Inconvénient : Modèle 14b au lieu de 32b — capacités de raisonnement légèrement réduites

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

## ADR-003 : Versionnement Git intégral de tous les artefacts le workbench
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

---

## ADR-004 : Modèle secondaire qwen3:8b au lieu de qwen3:7b
**Date :** 2026-03-23
**Statut :** Accepté

**Contexte :**
Le modèle qwen3:7b spécifié dans DOC3 pour les Boomerang Tasks n'était pas disponible sur Ollama.

**Décision :**
Utilisation de qwen3:8b comme modèle secondaire pour les tâches légères (Boomerang Tasks).

**Conséquences :**
- Avantage : Performances équivalentes au 7b pour les tâches légères
- Aucun impact sur les autres phases (modèle non référencé dans Modelfile ni configurations Roo Code)
