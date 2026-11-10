
Date: 01/11/2026
Tags: 
[[Microservices]]

# Questions


# Notes

Le **polyglotisme** dans les microservices désigne le fait d’utiliser plusieurs langages de programmation, frameworks, et parfois plusieurs technologies de base de données, selon les besoins de chaque service.

## Idée principale

Dans une architecture microservices, chaque service est autonome et peut être développé avec l’outil le plus adapté à sa fonction métier.
Par exemple, un service de traitement temps réel peut être écrit en Go ou Rust, tandis qu’un service orienté data peut être en Java ou Python.

## Ce que ça apporte

- Meilleur **choix technologique** pour chaque besoin métier.
- Possibilité d’optimiser performance, productivité et maintenabilité selon le service.
- En base de données, on parle aussi de **polyglot persistence** quand différents services utilisent différents types de stockage, comme SQL pour des données structurées et NoSQL pour des données plus flexibles.


## Limites

Le polyglotisme augmente aussi la complexité : il faut gérer plus de compétences, plus d’outils, des pipelines de déploiement plus variés et des tests plus difficiles.
Il est donc utile surtout quand les besoins des services sont vraiment différents, pas juste pour “multiplier les langages”.

## Exemple simple

Une application e-commerce peut avoir :

- un service catalogue en Java,
- un service recommandation en Python,
- un service paiement en Go,
- une base relationnelle pour les commandes,
- une base document pour les fiches produit.

En résumé, le polyglotisme en microservices, c’est **choisir la bonne technologie pour chaque service**, plutôt que forcer toute l’application à utiliser la même pile technique.

# Références

[https://memeagora.blogspot.com/2006/12/polyglot-programming.html](https://memeagora.blogspot.com/2006/12/polyglot-programming.html)

[https://martinfowler.com/bliki/PolyglotPersistence.html](https://martinfowler.com/bliki/PolyglotPersistence.html)
