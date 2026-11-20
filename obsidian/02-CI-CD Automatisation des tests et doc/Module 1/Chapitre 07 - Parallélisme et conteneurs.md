# Chapitre 07 — Parallélisme et conteneurs

## 1. Parallélisme

Le parallélisme permet d'exécuter plusieurs tâches simultanément pour réduire la durée totale du pipeline.

## 2. Matrice

Une matrice permet de lancer plusieurs variantes d'un job.

Exemple : tester une application avec Python 3.11, 3.12 et 3.13.

## 3. Worker

Un worker est un processus chargé d'exécuter une partie du travail.

Exemple : pytest-xdist répartit les tests entre plusieurs workers.

`pytest -n auto`

Cette commande utilise plusieurs workers selon les ressources disponibles.

## 4. Sharding

Le sharding consiste à répartir une suite de tests en plusieurs groupes exécutés sur différentes machines ou environnements.

## 5. Tests en conteneurs

Un conteneur fournit un environnement d'exécution isolé et reproductible.

### container

Permet d'exécuter un job dans un conteneur.

### services

Permet de démarrer des services nécessaires aux tests.

Exemples :

- PostgreSQL.
    
- Redis.
    

### Docker Compose

Permet de démarrer plusieurs services conteneurisés ensemble.

### Kubernetes

Permet d'orchestrer des conteneurs et leurs environnements d'exécution.

## 6. Health Check

Vérification permettant de déterminer si un service est prêt ou fonctionne correctement.

Exemple : attendre que PostgreSQL soit prêt avant d'exécuter les tests d'intégration.

## À retenir

- **Matrice** = plusieurs configurations.
    
- **Worker** = processus d'exécution.
    
- **Sharding** = répartition des tests.
    
- **Conteneur** = environnement isolé.
    
- **Health Check** = vérification de disponibilité.