
Date: 01/11/2026
Tags: 
[[Architecture logicielle]]

# Questions


# Notes


L’**Event-Driven Architecture** (**EDA**), ou **architecture orientée événements**, est un style d’architecture dans lequel les microservices communiquent principalement en publiant et en consommant des **événements**. Un événement représente quelque chose qui s’est produit, par exemple `CommandeCréée`, `PaiementValidé` ou `ColisExpédié`.[[cloud.google](https://cloud.google.com/eventarc/advanced/docs/event-driven-architectures?hl=fr)][[aws.amazon](https://aws.amazon.com/event-driven-architecture/)]

## Fonctionnement

```
Service Commande
      │
      │ publie CommandeCréée
      ▼
Message broker / Event bus
      ├──> Service Facturation
      ├──> Service Stock
      └──> Service Notification
```

Le service Commande ne connaît pas nécessairement les consommateurs. Il publie l’événement sur un broker, qui le distribue aux services abonnés. Les producteurs, le routeur et les consommateurs peuvent ainsi être déployés et mis à l’échelle indépendamment.[[cloud.google](https://cloud.google.com/eventarc/docs/event-driven-architectures?hl=fr)][[docs.cloud.google](https://docs.cloud.google.com/eventarc/standard/docs/event-driven-architectures)]

## Exemple

Lorsqu’une commande est créée :

```
1. Le service Commande enregistre la commande.
2. Il publie l’événement CommandeCréée.
3. Le service Stock réserve les articles.
4. Le service Facturation prépare la facture.
5. Le service Notification envoie un e-mail.
```

Ces traitements peuvent être réalisés de manière asynchrone. Le service Commande n’a pas besoin d’attendre la fin de chaque traitement pour répondre au client.[[learn.microsoft](https://learn.microsoft.com/en-us/dotnet/architecture/microservices/multi-container-microservice-net-applications/integration-event-based-microservice-communications)]

## Éléments principaux

Une EDA comporte généralement :

- un **producteur d’événements** : publie un événement ;
- un **canal ou broker** : transporte, conserve et éventuellement route les événements ;
- un **consommateur** : réagit à un événement ;
- un **contrat d’événement** : définit sa structure et sa signification.[[learn.microsoft](https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/event-driven)]

Des technologies comme Kafka, RabbitMQ, Pulsar, AWS EventBridge ou Azure Service Bus peuvent jouer différents rôles dans ce type d’architecture, selon leurs capacités de transport, de routage et de conservation.

## Avantages

- faible couplage entre les microservices ;
- communication asynchrone ;
- traitement parallèle ;
- ajout de nouveaux consommateurs sans modifier le producteur ;
- meilleure absorption des pics de charge ;
- possibilité de rejouer certains événements selon la technologie utilisée ;
- déploiement et mise à l’échelle indépendants.[[learn.microsoft](https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/)][[aws.amazon](https://aws.amazon.com/what-is/eda/)]

## Points de vigilance

L’EDA introduit aussi des contraintes :

- cohérence souvent éventuelle entre les services ;
- débogage plus complexe ;
- gestion des doublons et de l’idempotence ;
- gestion des événements en erreur ;
- évolution des contrats d’événements ;
- traçabilité des traitements distribués ;
- nécessité de surveiller les files ou flux.

Un consommateur doit donc pouvoir traiter deux fois le même événement sans produire un résultat incorrect :

```
CommandeCréée reçue
CommandeCréée reçue à nouveau
```

Le traitement doit rester idempotent.

## À ne pas confondre

L’EDA n’est pas synonyme d’**Event Sourcing** :

- l’EDA décrit une manière de faire communiquer les composants au moyen d’événements ;
- l’Event Sourcing décrit une stratégie de persistance où les changements d’état sont conservés comme une suite d’événements.

On peut donc utiliser une architecture orientée événements sans faire d’Event Sourcing. De même, un système Event Sourcing peut utiliser des événements sans que tous ses échanges interservices soient nécessairement conçus comme une EDA.

En résumé :

> **Dans une architecture orientée événements, un microservice publie ce qui s’est produit et d’autres microservices réagissent à cet événement de manière découplée, souvent asynchrone.**


# Références

