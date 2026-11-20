# Chapitre 09 — Organisation des tests

## 1. Structurer les tests

Organiser les tests selon leur catégorie.

Exemples :

- Tests unitaires.
    
- Tests API.
    
- Tests E2E.
    
- Tests visuels.
    
- Tests de performance.
    

Cette organisation permet au pipeline de sélectionner les tests adaptés à chaque étape.

## 2. Marqueurs pytest

Les marqueurs permettent de classer et de sélectionner les tests.

Exemples :

- `unit`
    
- `api`
    
- `e2e`
    
- `visual`
    
- `slow`
    

## 3. Fixtures

Une fixture pytest prépare des ressources ou des données réutilisables par les tests.

Exemples :

- Client de test.
    
- Base de données de test.
    
- Données initiales.
    

## 4. Tests déterministes

Un test déterministe produit le même résultat dans les mêmes conditions.

Éviter les dépendances non maîtrisées :

- Heure réelle.
    
- Hasard.
    
- Ordre d'exécution.
    
- Réseau externe.
    

## 5. Flaky Tests

Un _flaky test_ est un test instable qui réussit ou échoue selon les exécutions, sans modification du code testé.

Il faut rechercher et corriger la cause de son instabilité.

## 6. Clean Code dans les tests

Les tests doivent être :

- Lisibles.
    
- Simples.
    
- Indépendants.
    
- Faciles à maintenir.
    
- Nommés selon le comportement vérifié.
    

## 7. Anti-modèles

### Trop de tests E2E

Pipeline lent et fragile.

### Tests sans assertions pertinentes

Bonne couverture apparente, mais vérifications insuffisantes.

### Environnements différents

Tests réussis en local mais échouant dans la CI.

### Tests instables tolérés

Perte de confiance dans les résultats.

## À retenir

Une bonne suite de tests doit être **rapide, fiable, indépendante, lisible et reproductible**.