# Chapitre 01 — Automatisation des tests

## 1. Définition

L'automatisation des tests consiste à utiliser des programmes pour vérifier automatiquement qu'une application fonctionne conformément aux résultats attendus.

**Objectif :** détecter les régressions rapidement et éviter de répéter manuellement les mêmes vérifications.

## 2. Tests manuels et automatisés

**Tests manuels :**

- Réalisés par une personne.
    
- Adaptés à l'exploration et à l'ergonomie.
    
- Demandent du temps à chaque exécution.
    

**Tests automatisés :**

- Exécutés par des outils.
    
- Rapides et reproductibles.
    
- Nécessitent un travail initial d'écriture et de maintenance.
    
- Adaptés aux tests de régression.
    

Les deux approches sont complémentaires.

## 3. Shift Left

**Shift Left :** déplacer les vérifications le plus tôt possible dans le développement.

L'objectif est de détecter les erreurs avant la fusion du code (_merge_).

Un bug découvert tardivement coûte généralement davantage à corriger.

## 4. Quand automatiser ?

Automatiser en priorité les tests :

- Répétitifs.
    
- Critiques pour le fonctionnement de l'application.
    
- Exécutés avec plusieurs jeux de données.
    
- Dont le résultat attendu est stable.
    

Privilégier les tests manuels pour :

- L'exploration.
    
- L'évaluation de l'ergonomie.
    
- Les fonctionnalités provisoires qui changent fréquemment.
    

## À retenir

**Automatiser le répétitif et conserver l'humain pour l'exploration.**

**Shift Left = tester le plus tôt possible.**