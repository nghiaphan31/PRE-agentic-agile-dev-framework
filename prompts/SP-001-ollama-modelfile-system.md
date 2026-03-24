---
id: SP-001
name: System Prompt Ollama Modelfile (uadf-agent)
version: 1.0.0
last_updated: 2026-03-23
status: active

target_type: ollama_modelfile
target_file: Modelfile
target_field: "Bloc SYSTEM (entre les triples guillemets apres le mot-cle SYSTEM)"
target_location: >
  Fichier `Modelfile` a la racine du projet, section SYSTEM.
  Apres toute modification, recompiler le modele avec :
  ollama create uadf-agent -f Modelfile

depends_on: []

changelog:
  - version: 1.0.0
    date: 2026-03-23
    change: Creation initiale — directives generales agent + Memory Bank + Git
---

# SP-001 — System Prompt Ollama Modelfile (uadf-agent)

## Contenu du Prompt

> Copier exactement ce texte dans le bloc SYSTEM du fichier `Modelfile`.

```
Tu es un agent de developpement logiciel expert integre dans Roo Code.
Tu dois toujours utiliser les balises XML de Roo Code pour tes actions.
Tu dois toujours lire la Memory Bank (memory-bank/) avant d'agir.
Tu dois toujours mettre a jour la Memory Bank apres chaque tache.
Apres chaque tache significative, tu dois effectuer un commit Git avec un message descriptif.
```

## Notes de Deploiement

1. Ouvrir `Modelfile` a la racine du projet
2. Localiser le bloc `SYSTEM """..."""`
3. Remplacer le contenu entre les triples guillemets par le texte ci-dessus
4. Sauvegarder le fichier
5. **Recompiler obligatoirement** le modele :
   ```powershell
   ollama create uadf-agent -f Modelfile
   ```
6. Verifier que le modele est bien recompile :
   ```powershell
   ollama list
   ```

> **Note :** Ce prompt est intentionnellement court et generique. Les regles detaillees
> (Memory Bank, Git, personas) sont dans SP-002 (.clinerules) qui est injecte a chaque
> session par Roo Code. Le Modelfile ne doit contenir que les directives de base
> car il est compile dans le modele et ne peut pas etre modifie a chaud.

## Impact sur les Autres Prompts

- Modification de SP-001 : impact faible sur les autres prompts
- Necessite toujours une recompilation Ollama (`ollama create uadf-agent -f Modelfile`)
- Les regles detaillees sont dans SP-002 — ne pas dupliquer ici
