
Date: 01/11/2026
Tags: 

[[Architecture logicielle]]
# Questions


# Notes

L’architecture **SOA** (*Service-Oriented Architecture*) est un style d’architecture logicielle dans lequel les fonctionnalités d’un système sont exposées sous forme de services réutilisables, accessibles via un réseau avec des interfaces bien définies.

## Idée principale

Chaque service réalise une fonction métier précise, par exemple “consulter un client”, “calculer une facture” ou “envoyer une notification”. Le service est conçu pour être autonome, réutilisable et faiblement couplé aux autres composants.

## Rôles typiques

On distingue généralement :

- le **fournisseur de service**, qui expose le service.
- le **consommateur de service**, qui l’utilise.
- parfois un **registre** ou broker, qui aide à découvrir les services disponibles.


## Caractéristiques

Une SOA vise surtout :

- la réutilisation.
- l’interopérabilité entre systèmes différents.
- le couplage faible.
- une intégration plus simple de logiciels hétérogènes.


## Différence avec les microservices

SOA et microservices se ressemblent, mais SOA est souvent pensée à l’échelle de l’entreprise, avec des services plus larges, tandis que les microservices découpent davantage les fonctionnalités en services plus petits et plus indépendants.

## Exemple simple

Imagine un système bancaire :

- un service pour gérer les comptes,
- un service pour faire les virements,
- un service pour vérifier l’identité.
Chaque service peut être appelé par d’autres applications sans connaître son implémentation interne.

En une phrase, SOA consiste à construire un système comme un ensemble de services métiers indépendants qui communiquent entre eux par contrat plutôt que par dépendances directes.



# Références

