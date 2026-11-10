
Date: 01/11/2026
Tags: 
[[Architecture logicielle]]

# Questions


# Notes

Dans une architecture **n-tiers**, un _tier_ désigne d’abord une **séparation logique et de déploiement** des responsabilités ; il peut correspondre à une machine distincte, mais ce n’est pas obligatoire. Plusieurs tiers peuvent coexister sur le même serveur, notamment en développement ou dans une petite application.[[learn.microsoft](https://learn.microsoft.com/bs-latn-ba/azure/architecture/guide/architecture-styles/n-tier)][[informatique.cnam](http://informatique.cnam.fr/fr/spip.php?pdoc5259)]

## Layer vs tier

- **Layer (couche)** : découpage logique du code — par exemple présentation, logique métier, accès aux données.
- **Tier (niveau)** : unité de déploiement physique ou d’infrastructure — par exemple un navigateur/client, un serveur applicatif, une base de données.[[bmc](https://www.bmc.com/blogs/n-tier-architecture-tier-2-tier-3-and-multi-tier-explained/)][[guru99](https://www.guru99.com/fr/n-tier-architecture-system-concepts-tips.html)]

Ainsi, une application peut être architecturée en 3 couches logiques tout en étant déployée sur **une seule machine**.

## Exemples de déploiement

|Déploiement|Présentation|Logique métier|Données|Est-ce n-tiers ?|
|---|---|---|---|---|
|Monolithe local|Angular dans le même process|Spring Boot|PostgreSQL local|Oui, si les responsabilités sont séparées|
|3-tiers classique|Navigateur|Serveur Spring Boot|Serveur PostgreSQL|Oui, avec séparation physique|
|Cloud conteneurisé|Frontend statique / CDN|Plusieurs conteneurs Spring Boot|Base managée|Oui, chaque tier peut avoir plusieurs nœuds|
|Développement sur PC|Navigateur|`localhost:8080`|`localhost:5432`|Oui, mais tout sur une machine|

## Nuance importante

Dans les définitions strictes, un **tier** implique une séparation physique ou au moins un déploiement isolé : Microsoft décrit les tiers comme exécutés sur des machines distinctes. Mais la même source précise qu’une application peut regrouper plusieurs couches logiques dans un même tier.[[learn.microsoft](https://learn.microsoft.com/bs-latn-ba/azure/architecture/guide/architecture-styles/n-tier)][[learn.microsoft](https://learn.microsoft.com/fr-fr/azure/architecture/guide/architecture-styles/n-tier)]

Pour un système Spring Boot typique :

```
Navigateur (présentation)
   ↓ HTTPS/JSON
API Spring Boot (métier + accès données)
   ↓ JDBC
PostgreSQL (persistance)
```

C’est une architecture **3-tiers** si l’on considère le navigateur, l’API et la base comme trois unités déployées séparément. En revanche, si présentation, métier et persistance sont seulement des packages distincts dans une application unique, on parle plutôt de **couches** (_layers_) dans une architecture monolithique.[[bmc](https://www.bmc.com/blogs/n-tier-architecture-tier-2-tier-3-and-multi-tier-explained/)][[lab-sticc.univ-brest](https://lab-sticc.univ-brest.fr/~ecariou4/cours/web/cours-architecture.pdf)]

## À retenir

- **N-tiers ≠ n machines obligatoirement.**
- Un tier peut contenir plusieurs couches logiques.
- Un tier peut lui-même être composé de plusieurs machines, conteneurs ou instances pour la scalabilité et la haute disponibilité.[[learn.microsoft](https://learn.microsoft.com/bs-latn-ba/azure/architecture/guide/architecture-styles/n-tier)][[learn.microsoft](https://learn.microsoft.com/fr-fr/azure/architecture/guide/architecture-styles/n-tier)]
- La séparation physique apporte isolation, scalabilité et résilience, mais ajoute latence réseau et complexité opérationnelle.[[learn.microsoft](https://learn.microsoft.com/bs-latn-ba/azure/architecture/guide/architecture-styles/n-tier)]

# Références

