# Chapitre 11 — Réponses aux révisions

## 1. Concepts

### 1. Qu'est-ce que le Shift Left ?

Le **Shift Left** consiste à effectuer les tests et les contrôles de qualité le plus tôt possible dans le développement, afin de détecter les erreurs avant leur intégration.

### 2. Quelle différence entre test manuel et automatisé ?

- **Manuel** : exécuté par une personne, adapté à l'exploration et à l'ergonomie.
    
- **Automatisé** : exécuté par un programme, adapté aux vérifications répétitives et aux régressions.
    

### 3. Quelle différence entre test unitaire et test d'intégration ?

- **Unitaire** : vérifie une fonction isolée.
    
- **Intégration** : vérifie le fonctionnement de plusieurs composants ensemble.
    

### 4. Que signifie E2E ?

**E2E (End-to-End)** signifie test de bout en bout. Il vérifie un parcours utilisateur complet.

### 5. Pourquoi la pyramide contient-elle davantage de tests unitaires ?

Parce que les tests unitaires sont **rapides, précis et moins coûteux à exécuter** que les tests E2E.

### 6. Que signifient AAA et FIRST ?

**AAA :**

- Arrange : préparer.
    
- Act : exécuter.
    
- Assert : vérifier.
    

**FIRST :**

- Fast : rapide.
    
- Isolated : indépendant.
    
- Repeatable : reproductible.
    
- Self-validating : résultat vérifiable automatiquement.
    
- Timely : écrit au bon moment.
    

### 7. Quelles sont les trois étapes du TDD ?

**TDD (Test-Driven Development)** :

1. Rouge : écrire un test qui échoue.
    
2. Vert : écrire le code nécessaire pour réussir.
    
3. Refactor : améliorer le code sans casser les tests.
    

### 8. Quelle différence entre CI, Continuous Delivery et Continuous Deployment ?

- **CI (Continuous Integration)** : intégrer régulièrement le code et exécuter les vérifications automatiques.
    
- **Continuous Delivery** : préparer automatiquement une version prête à être déployée, avec une décision humaine pour la production.
    
- **Continuous Deployment** : déployer automatiquement en production les versions validées.
    

### 9. Qu'est-ce qu'un pipeline ?

Un **pipeline** est un enchaînement automatisé de tâches : analyse du code, tests, construction, sécurité et déploiement.

### 10. Qu'est-ce qu'un Quality Gate ?

Un **Quality Gate** est un ensemble de critères de qualité obligatoires. Si un critère bloquant n'est pas respecté, le pipeline ne poursuit pas normalement son exécution.

### 11. Qu'est-ce qu'un workflow ?

Un **workflow** est un processus automatisé défini dans un fichier YAML. Dans GitHub Actions, il contient un ou plusieurs jobs.

### 12. Quelle différence entre job et step ?

- **Job** : ensemble d'étapes exécutées sur un runner.
    
- **Step** : commande ou action exécutée dans un job.
    

### 13. À quoi sert un runner ?

Un **runner** est une machine qui exécute les jobs d'un pipeline CI/CD.

### 14. À quoi sert `needs` ?

`needs` définit une **dépendance entre des jobs** dans GitHub Actions.

Exemple : le job `test` attend la réussite du job `lint`.

### 15. Quelle différence entre matrice, worker et sharding ?

- **Matrice** : exécute plusieurs configurations d'un job, par exemple différentes versions de Python.
    
- **Worker** : processus chargé d'exécuter des tests.
    
- **Sharding** : répartit une suite de tests entre plusieurs machines ou environnements.
    

### 16. Quelle différence entre artefact et cache ?

- **Artefact** : fichier produit par un job et conservé, comme un rapport de tests.
    
- **Cache** : données réutilisées pour accélérer les exécutions suivantes, comme des dépendances téléchargées.
    

### 17. Qu'est-ce qu'un flaky test ?

Un **flaky test** est un test instable qui réussit ou échoue selon les exécutions, sans modification du code testé.

### 18. À quoi sert un Health Check ?

Un **Health Check** vérifie qu'un service fonctionne ou qu'il est prêt à recevoir des requêtes.

---

## 2. Outils et frameworks

### 19. À quoi sert pytest ?

**pytest** est un framework Python permettant d'écrire et d'exécuter des tests automatisés : unitaires, d'intégration et API.

Il propose notamment des assertions, fixtures, tests paramétrés et plugins.

### 20. À quoi sert JUnit 5 ?

**JUnit 5** est un framework de tests utilisé principalement pour les applications Java et Kotlin.

Il permet notamment de réaliser des tests unitaires et d'intégration.

### 21. Quelle différence entre Selenium, Cypress et Playwright ?

Ce sont des outils d'automatisation des tests de navigateur.

- **Selenium** : utilise WebDriver et prend en charge plusieurs langages.
    
- **Cypress** : principalement destiné aux tests Web en JavaScript et TypeScript.
    
- **Playwright** : prend en charge plusieurs navigateurs et langages, avec des attentes automatiques et des traces.
    

### 22. À quoi sert Ruff ?

**Ruff** est un outil Python qui analyse le code pour détecter des erreurs et des problèmes de style. Il peut également formater le code.

### 23. À quoi sert coverage.py ?

**coverage.py** mesure la couverture du code Python par les tests, c'est-à-dire les parties du code exécutées pendant les tests.

### 24. À quoi sert GitHub Actions ?

**GitHub Actions** permet d'automatiser des workflows, notamment les pipelines CI/CD, directement depuis un dépôt GitHub.

### 25. Quelle différence entre GitHub Actions et GitLab CI/CD ?

Les deux permettent d'automatiser des pipelines.

- **GitHub Actions** : utilise des workflows YAML dans `.github/workflows/`.
    
- **GitLab CI/CD** : utilise principalement le fichier `.gitlab-ci.yml`.
    

### 26. À quoi sert Docker ?

**Docker** permet de créer et d'exécuter des applications dans des conteneurs isolés et reproductibles.

### 27. À quoi sert Kubernetes ?

**Kubernetes** est un outil d'orchestration permettant de déployer, gérer et mettre à l'échelle des applications conteneurisées.

### 28. À quoi servent Locust et JMeter ?

**Locust et JMeter** sont des outils de tests de charge et de performance.

Ils permettent notamment de mesurer le comportement d'une application lorsqu'elle reçoit de nombreuses requêtes.

### 29. À quoi servent pip-audit et Trivy ?

- **pip-audit** : recherche les vulnérabilités connues dans les dépendances Python.
    
- **Trivy** : analyse notamment les images de conteneurs pour détecter des vulnérabilités et des problèmes de configuration.
    

### 30. À quoi sert le format JUnit XML ?

**JUnit XML** est un format de rapport de tests permettant aux outils CI/CD d'afficher les résultats : tests réussis, échoués ou ignorés.

---

## 3. Questions essentielles

### Pourquoi automatiser les tests ?

Pour détecter rapidement les erreurs, éviter les régressions et réduire le temps consacré aux vérifications répétitives.

### Quels tests exécuter en premier dans un pipeline ?

Les tests les plus rapides et les moins coûteux, généralement les contrôles de lint et les tests unitaires.

C'est le principe **Fail Fast**.

### Pourquoi utiliser des Quality Gates ?

Pour empêcher qu'une version ne respectant pas les critères de qualité définis poursuive le processus de livraison.

### Pourquoi les tests doivent-ils être indépendants ?

Pour pouvoir les exécuter dans n'importe quel ordre, y compris en parallèle, sans influencer leurs résultats.

### Pourquoi une couverture de 100 % ne garantit-elle pas l'absence de bugs ?

Parce que la couverture mesure le code exécuté par les tests, **pas la qualité des vérifications**.

Un test peut exécuter du code sans contrôler correctement son comportement.

---

## Mémo final — Les notions indispensables

- **Shift Left** : tester tôt.
    
- **AAA** : préparer, exécuter, vérifier.
    
- **FIRST** : cinq qualités d'un bon test.
    
- **TDD** : rouge, vert, refactor.
    
- **CI** : intégrer et tester automatiquement.
    
- **Continuous Delivery** : prêt à déployer.
    
- **Continuous Deployment** : déploiement automatique.
    
- **Pipeline** : enchaînement de tâches.
    
- **Quality Gate** : seuil de qualité bloquant.
    
- **Workflow** : processus automatisé.
    
- **Job** : ensemble d'étapes.
    
- **Step** : commande ou action.
    
- **Runner** : machine d'exécution.
    
- **Worker** : processus d'exécution.
    
- **Matrice** : plusieurs configurations.
    
- **Sharding** : répartition des tests.
    
- **Artefact** : résultat conservé.
    
- **Cache** : accélération des exécutions.
    
- **Flaky Test** : test instable.
    
- **Health Check** : vérification de l'état d'un service.