# Chapitre 04 — CI/CD et pipelines

## 1. CI — Continuous Integration

Intégration continue.

Consiste à intégrer régulièrement les modifications du code et à lancer automatiquement des vérifications.

Exemples :

- Compilation ou build.
    
- Analyse du code.
    
- Tests automatisés.
    

**Objectif :** détecter rapidement les problèmes d'intégration.

## 2. Continuous Delivery

Livraison continue.

Le logiciel est automatiquement préparé et validé pour pouvoir être mis en production.

**La mise en production nécessite encore une décision humaine.**

## 3. Continuous Deployment

Déploiement continu.

Chaque version qui réussit les vérifications prévues peut être déployée automatiquement en production.

**La mise en production est automatisée.**

## 4. Pipeline CI/CD

Un pipeline est un enchaînement automatisé de tâches permettant de vérifier, construire et livrer une application.

### Étapes d'un pipeline type

1. **Commit / Push / PR** : modification du code.
    
2. **Lint** : contrôle de la qualité et du style du code.
    
3. **Tests unitaires** : vérification des fonctions.
    
4. **Build** : construction de l'application ou de son image.
    
5. **Tests API / E2E** : vérification du comportement.
    
6. **Sécurité** : analyse des vulnérabilités.
    
7. **Déploiement** : mise à disposition de l'application.
    

## 5. Fail Fast

Principe consistant à détecter et signaler les erreurs le plus tôt possible.

On place généralement les vérifications rapides avant les vérifications longues et coûteuses.

## À retenir

- **CI** = intégrer et vérifier automatiquement.
    
- **Continuous Delivery** = application prête à être déployée.
    
- **Continuous Deployment** = déploiement automatique.
    
- **Pipeline** = suite de tâches automatisées.
    
- **Fail Fast** = échouer rapidement pour éviter du travail inutile.