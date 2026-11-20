# Chapitre 06 — GitHub Actions et GitLab CI

## 1. GitHub Actions

GitHub Actions permet d'automatiser des workflows, notamment les pipelines CI/CD.

Les workflows sont décrits dans des fichiers YAML placés dans :

`.github/workflows/`

## 2. Vocabulaire GitHub Actions

### Workflow

Ensemble de jobs automatisés définis dans un fichier YAML.

### Événement

Déclencheur du workflow.

Exemples :

- `push` : envoi de modifications.
    
- `pull_request` : demande de fusion.
    
- `schedule` : planification.
    
- `workflow_dispatch` : lancement manuel.
    

### Job

Ensemble d'étapes exécutées sur un runner.

### Step

Étape d'un job.

Elle peut exécuter une commande ou utiliser une action.

### Runner

Machine qui exécute les jobs.

Exemples : Linux, Windows, macOS.

### Action

Composant réutilisable permettant d'effectuer une tâche.

Exemples :

- `actions/checkout` : récupérer le dépôt.
    
- `actions/setup-python` : préparer Python.
    

### needs

Définit une dépendance entre jobs.

Exemple : les tests démarrent seulement après la réussite du job de lint.

## 3. GitLab CI/CD

GitLab CI/CD permet également de créer des pipelines automatisés.

Le pipeline est défini dans :

`.gitlab-ci.yml`

Concepts importants :

- **Stage** : phase du pipeline.
    
- **Job** : tâche automatisée.
    
- **Script** : commandes exécutées.
    
- **Image** : environnement conteneurisé du job.
    
- **Artifacts** : fichiers produits et conservés après un job.
    

## 4. Artefacts, cache et rapports

### Artefacts

Fichiers produits par un job.

Exemples :

- Rapports de tests.
    
- Captures d'écran.
    
- Fichiers compilés.
    

### Cache

Conserve temporairement des éléments réutilisables pour accélérer les exécutions suivantes.

Exemple : dépendances Python déjà téléchargées.

### JUnit XML

Format de rapport de résultats de tests, compris par plusieurs plateformes CI/CD.

### if: always()

Permet d'exécuter une étape même si une étape précédente a échoué, sous réserve des autres conditions applicables.

Exemple : publier un rapport de tests après un échec.

## À retenir

- **Workflow** = automatisation complète.
    
- **Job** = ensemble d'étapes.
    
- **Step** = action élémentaire.
    
- **Runner** = machine d'exécution.
    
- **Action** = composant réutilisable.
    
- **needs** = dépendance entre jobs.
    
- **Artefact** = résultat conservé.
    
- **Cache** = accélération des exécutions suivantes.