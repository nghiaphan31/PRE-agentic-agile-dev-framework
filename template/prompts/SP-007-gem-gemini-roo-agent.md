---
id: SP-007
name: Gem Gemini Chrome "Roo Code Agent"
version: 1.3.0
last_updated: 2026-03-23
status: active

target_type: gemini_gem_instructions
target_file: EXTERNE
target_field: "Instructions du Gem (champ 'Instructions' dans l'interface de creation/edition du Gem)"
target_location: >
  DEPLOIEMENT MANUEL REQUIS — Ce prompt ne peut pas etre deploye automatiquement.
  Procedure :
  1. Aller sur https://gemini.google.com
  2. Cliquer sur "Gems" dans le menu lateral gauche
  3. Ouvrir le Gem nomme "Roo Code Agent" (ou le creer s'il n'existe pas)
  4. Cliquer sur l'icone d'edition (crayon)
  5. Dans le champ "Instructions", remplacer tout le contenu par le texte ci-dessous
  6. Cliquer sur "Save" pour sauvegarder le Gem
  7. Tester en envoyant un message de test dans le Gem

hors_git: true

depends_on:
  - proxy.py: "Le format des balises XML attendues par proxy.py doit correspondre exactement aux balises listees dans ce prompt"
  - SP-002: "Les balises XML listees dans REGLE 6 de .clinerules doivent etre identiques a celles listees dans ce prompt"

changelog:
  - version: 1.3.0
    date: 2026-03-23
    change: Ajout de browser_action et new_task (avec note limitation proxy mode) dans FORMAT DE REPONSE OBLIGATOIRE (FIX-012)
  - version: 1.2.0
    date: 2026-03-23
    change: Remplacement du contexte UADF hardcode par une instruction generique de lecture de la Memory Bank (FIX-010)
  - version: 1.1.0
    date: 2026-03-23
    change: Ajout de replace_in_file et list_files dans FORMAT DE REPONSE OBLIGATOIRE + regles 7 et 8
  - version: 1.0.0
    date: 2026-03-23
    change: Creation initiale — instructions Gem Gemini pour relai vers Roo Code via proxy clipboard
---

# SP-007 — Gem Gemini Chrome "Roo Code Agent"

## AVERTISSEMENT : DEPLOIEMENT MANUEL OBLIGATOIRE

> Ce prompt est le **seul** du registre UADF qui ne peut pas etre deploye automatiquement via Git.
> Il doit etre copie-colle manuellement dans l'interface web Gemini (gemini.google.com > Gems).
>
> **Consequence :** Toute modification de ce fichier DOIT etre accompagnee d'un commit Git avec la mention :
> `"DEPLOIEMENT MANUEL REQUIS : mettre a jour le Gem Gemini avec SP-007"`
>
> Voir REGLE 6.2 de `.clinerules` (SP-002) pour la procedure complete.

---

## Contenu du Prompt

> Copier exactement ce texte dans le champ "Instructions" du Gem Gemini "Roo Code Agent".

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

Pour modifier partiellement un fichier existant (PREFERER a write_to_file) :
<replace_in_file>
<path>chemin/vers/fichier</path>
<diff>
[bloc de recherche et remplacement]
</diff>
</replace_in_file>

Pour lister les fichiers d'un dossier :
<list_files>
<path>dossier/a/lister</path>
<recursive>false</recursive>
</list_files>

Pour terminer une tache :
<attempt_completion>
<result>
Description du resultat accompli
</result>
</attempt_completion>

Pour interagir avec un navigateur web :
<browser_action>
<action>launch|screenshot|click|type|scroll|close</action>
<url>https://url-a-ouvrir (pour action launch uniquement)</url>
<coordinate>x,y (pour actions click/scroll)</coordinate>
<text>texte a saisir (pour action type uniquement)</text>
</browser_action>

Pour deleguer une sous-tache a un nouvel agent (Boomerang Task) :
⚠️ NON SUPPORTE EN MODE PROXY GEMINI — utiliser uniquement en Mode Local (Ollama) ou Mode Cloud (Claude API)
<new_task>
<mode>code|architect|ask|debug</mode>
<message>Instructions completes pour le sous-agent</message>
</new_task>

REGLES IMPORTANTES :
1. Toujours utiliser les balises XML ci-dessus pour les actions — jamais de texte libre pour les actions
2. Toujours lire la Memory Bank (memory-bank/) avant d'agir sur le code
3. Toujours mettre a jour memory-bank/activeContext.md apres chaque action significative
4. Toujours effectuer un commit Git apres chaque modification de fichier
5. Etre concis et precis dans les descriptions — eviter les explications superflues
6. Si une tache est ambigue, demander une clarification avant d'agir
7. Toujours utiliser replace_in_file plutot que write_to_file pour les modifications partielles
8. Toujours utiliser list_files pour decouvrir la structure du projet avant de coder
9. Ne JAMAIS utiliser new_task en Mode Proxy Gemini — cela cree un conflit de presse-papiers (deadlock)

CONTEXTE DU PROJET :
Ne suppose rien sur le projet en cours. Avant toute action, lis les fichiers de la Memory Bank pour comprendre le contexte :
- memory-bank/projectbrief.md — objectifs et perimetre du projet
- memory-bank/activeContext.md — tache en cours, decisions recentes, prochaines etapes
- memory-bank/techContext.md — stack technique, outils, contraintes
Si le dossier memory-bank/ n'existe pas, demande a l'utilisateur de te fournir le contexte du projet avant d'agir.
```

## Notes de Deploiement

### Procedure de Creation du Gem (premiere fois)

1. Aller sur **https://gemini.google.com**
2. Dans le menu lateral gauche, cliquer sur **"Gems"**
3. Cliquer sur **"New Gem"** (ou "Nouveau Gem")
4. Donner le nom : **"Roo Code Agent"**
5. Dans le champ **"Instructions"**, coller le texte de la section "Contenu du Prompt"
6. Optionnel : ajouter une description "Agent de developpement pour Roo Code via proxy clipboard"
7. Cliquer sur **"Save"**

### Procedure de Mise a Jour du Gem (modifications ulterieures)

1. Aller sur **https://gemini.google.com > Gems**
2. Trouver le Gem **"Roo Code Agent"** et cliquer sur l'icone d'edition (crayon)
3. Dans le champ **"Instructions"**, remplacer tout le contenu par la nouvelle version
4. Cliquer sur **"Save"**
5. **Commiter dans Git** avec le message :
   ```
   chore(prompts): mise a jour SP-007 v[X.Y.Z] - DEPLOIEMENT MANUEL EFFECTUE
   ```

### Verification du Bon Fonctionnement

Apres deploiement, tester le Gem en envoyant ce message :
```
Lis le fichier memory-bank/activeContext.md
```

Le Gem doit repondre avec la balise XML :
```xml
<read_file>
<path>memory-bank/activeContext.md</path>
</read_file>
```

Si le Gem repond en texte libre sans balises XML, les instructions n'ont pas ete correctement sauvegardees.

## Dependance Critique avec proxy.py

Ce prompt est etroitement couple avec `proxy.py` :

- `proxy.py` envoie les requetes de Roo Code vers le clipboard (que Gemini lit)
- `proxy.py` lit les reponses de Gemini depuis le clipboard
- `proxy.py` valide que les reponses contiennent des balises XML valides

**Si `proxy.py` change le format des balises XML attendues :**
1. Mettre a jour ce fichier SP-007 (section "FORMAT DE REPONSE OBLIGATOIRE")
2. Incrementer la version
3. Commiter avec `"DEPLOIEMENT MANUEL REQUIS"`
4. Mettre a jour manuellement le Gem Gemini

## Impact sur les Autres Prompts

- Modification de SP-007 : verifier la coherence avec SP-002 (REGLE 6 — balises XML)
- Si les balises XML changent : verifier `proxy.py` pour s'assurer que le parsing est compatible
- SP-007 est le seul prompt "Hors Git" — toute modification necessite une action manuelle supplementaire
