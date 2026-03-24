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

## Configuration des Backends LLM (Commutateur le workbench)

### Mode 1 : Local Ollama (Souverain et Gratuit — via Tailscale)
- **API Provider** : Ollama
- **Base URL** : `http://calypso:11434`
- **Model** : `uadf-agent`
- **Nom du profil Roo Code** : `ollama_local`
- **Statut** : `[x] Configuré et testé`
- **Prérequis** : Tailscale actif sur `pc` et `calypso`, Ollama en cours d'exécution sur `calypso`

### Mode 2 : Proxy Gemini Chrome (Cloud Gratuit + Copier-Coller)
- **API Provider** : OpenAI Compatible
- **Base URL** : `http://localhost:8000/v1`
- **API Key** : `sk-fake-key-uadf`
- **Model** : `gemini-manual`
- **Nom du profil Roo Code** : `gemini_proxy`
- **Statut** : `[x] Configuré et testé`
- **Prérequis** : proxy.py v2.8.0 démarré + Chrome ouvert sur Gem "Roo Code Agent"

### Mode 3 : Cloud Direct Claude Sonnet (Payant et Entièrement Automatique)
- **API Provider** : Anthropic
- **Model** : `claude-sonnet-4-6`
- **Nom du profil Roo Code** : `claude_api`
- **Statut** : `[~] Reporté à Phase 10`
- **API Key** : [stockée dans VS Code SecretStorage — ne jamais noter ici]
- **Prérequis** : Connexion Internet + crédit Anthropic disponible
