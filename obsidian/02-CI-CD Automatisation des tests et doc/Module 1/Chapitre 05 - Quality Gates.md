# Chapitre 05 — Quality Gates

## 1. Définition

Un **Quality Gate (porte de qualité)** est un ensemble de critères qui doivent être respectés pour autoriser la poursuite d'un pipeline.

Si un critère obligatoire échoue, le pipeline peut être bloqué.

## 2. Exemples de critères

### Qualité du code

- Aucune erreur de lint.
    
- Outils : Ruff, ESLint.
    

### Tests automatisés

- Tous les tests obligatoires réussissent.
    
- Outils : pytest, JUnit.
    

### Couverture de tests

- Respect d'un seuil minimal.
    
- Exemple du cours : 80 à 85 %.
    
- Outils : coverage.py, JaCoCo.
    

### Sécurité

- Absence de vulnérabilités critiques corrigibles.
    
- Outils : pip-audit, Trivy, Snyk.
    

### Performance

- Respect d'un temps de réponse maximal.
    
- Taux d'erreur inférieur au seuil fixé.
    
- Outils : Locust, JMeter.
    

### Revue humaine

- Validation du code par une autre personne.
    
- Exemple : une approbation obligatoire.
    

## 3. Couverture de tests

La couverture mesure la proportion du code exécutée pendant les tests.

Une couverture élevée ne garantit pas l'absence de bugs.

## À retenir

**Quality Gate = condition de qualité à respecter avant de poursuivre le pipeline.**

Les seuils sont configurables selon le projet.