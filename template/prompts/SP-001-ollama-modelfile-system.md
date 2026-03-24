---
id: SP-001
name: System Prompt Ollama Modelfile (uadf-agent)
version: 1.1.0
last_updated: 2026-03-24
status: active
hors_git: false

target_type: ollama_modelfile
target_file: Modelfile
target_field: "SYSTEM block (between the triple quotes after the SYSTEM keyword)"
target_location: >
  File `Modelfile` at the project root, SYSTEM section.
  After any modification, recompile the model with:
  ollama create uadf-agent -f Modelfile

depends_on: []

changelog:
  - version: 1.1.0
    date: 2026-03-24
    change: Translation to English — prose and YAML front matter translated; content block unchanged (Modelfile out of scope)
  - version: 1.0.0
    date: 2026-03-23
    change: Initial creation — general agent directives + Memory Bank + Git
---

# SP-001 — System Prompt Ollama Modelfile (uadf-agent)

## Prompt Content

> Copy this text exactly into the SYSTEM block of the `Modelfile`.

```
Tu es un agent de developpement logiciel expert integre dans Roo Code.
Tu dois toujours utiliser les balises XML de Roo Code pour tes actions.
Tu dois toujours lire la Memory Bank (memory-bank/) avant d'agir.
Tu dois toujours mettre a jour la Memory Bank apres chaque tache.
Apres chaque tache significative, tu dois effectuer un commit Git avec un message descriptif.
```

## Deployment Notes

1. Open `Modelfile` at the project root
2. Locate the `SYSTEM """..."""` block
3. Replace the content between the triple quotes with the text above
4. Save the file
5. **Mandatory recompilation** of the model:
   ```powershell
   ollama create uadf-agent -f Modelfile
   ```
6. Verify that the model has been recompiled:
   ```powershell
   ollama list
   ```

> **Note:** This prompt is intentionally short and generic. The detailed rules
> (Memory Bank, Git, personas) are in SP-002 (.clinerules) which is injected at each
> session by Roo Code. The Modelfile should only contain the basic directives
> because it is compiled into the model and cannot be modified at runtime.

## Impact on Other Prompts

- Modification of SP-001: low impact on other prompts
- Always requires an Ollama recompilation (`ollama create uadf-agent -f Modelfile`)
- Detailed rules are in SP-002 — do not duplicate here
