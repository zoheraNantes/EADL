

Date: 01/11/2026
Tags: [[Architecture logicielle]]

[[Architecture logicielle]]
# Questions


# Notes

L’**eventual consistency** (cohérence à terme) signifie qu’après une modification, les différents microservices ne voient pas tous immédiatement la même donnée, mais finiront par converger vers le même état — à condition qu’aucune nouvelle écriture ne survienne. C’est un compromis fréquent en microservices : on accepte une divergence temporaire pour gagner en disponibilité, autonomie et scalabilité.[[algomaster](https://algomaster.io/learn/microservices/eventual-consistency)][[stackandsystem](https://stackandsystem.com/series/microservices/consistency-in-microservices-explained)]

## Pourquoi c’est courant

Dans une architecture microservices, chaque service possède généralement sa propre base de données et son propre domaine métier. Il n’y a donc pas une seule base partagée dans laquelle une transaction ACID pourrait mettre à jour toutes les informations d’un coup.[[ltts](https://www.ltts.com/blog/eventual-consistency-microservices)][[geeksforgeeks](https://www.geeksforgeeks.org/system-design/what-is-eventual-consistency-between-microservices/)]

Quand le service **Commandes** crée une commande, il ne peut pas toujours mettre à jour instantanément le **stock**, la **facturation** et le **service de livraison** dans une transaction globale. Il publie plutôt un événement, par exemple `CommandeCreee`, que les autres services consomment quand ils le peuvent.[[ltts](https://www.ltts.com/blog/eventual-consistency-microservices)][[netmentor](https://www.netmentor.es/entrada/en/consistencia-eventual-microservicios)]

## Exemple simple

1. Le service Commandes enregistre la commande et publie `CommandeCreee`.
2. Le service Stock reçoit l’événement et décrémente le stock.
3. Le service Facturation reçoit l’événement et génère la facture.
4. Pendant quelques millisecondes, secondes, voire plus longtemps en cas d’incident, les données des services peuvent être divergentes.[[stackandsystem](https://stackandsystem.com/series/microservices/consistency-in-microservices-explained)][[netmentor](https://www.netmentor.es/entrada/en/consistencia-eventual-microservicios)]

Le système est donc **incohérent pendant un intervalle**, mais pas « cassé » : il converge vers un état cohérent.

## Eventual vs strong consistency

|Aspect|Strong consistency|Eventual consistency|
|---|---|---|
|Lecture après écriture|Reflète immédiatement la dernière écriture validée|Peut refléter une donnée obsolète pendant un temps|
|Coordination|Forte entre services ou bases|Faible, souvent asynchrone|
|Disponibilité en cas de panne|Plus difficile à maintenir|Meilleure tolérance aux pannes partielles|
|Cas d’usage|Solde bancaire, réservation d’une dernière place, paiement critique|Catalogue produits, profil utilisateur, notifications, vues de lecture|

La cohérence forte garantit que chaque lecture voit la dernière écriture validée, tandis que la cohérence à terme accepte des écarts temporaires puis une convergence.[[nhimg](https://nhimg.org/faq/what-is-the-difference-between-eventual-consistency-and-strong-consistency-in-mi/)]

## Comment l’implémenter

- **Événements asynchrones** : un service publie un événement sur Kafka, RabbitMQ, etc., et les services concernés s’abonnent.[[netmentor](https://www.netmentor.es/entrada/en/consistencia-eventual-microservicios)][[dev](https://dev.to/evanhameed99/microservice-architecture-eventual-consistency-3ckp)]
- **Outbox pattern** : la modification métier et l’événement à publier sont écrits dans la même transaction locale, puis un processus publie l’événement. Cela évite qu’une donnée change sans que l’événement soit émis.
- **Saga** : une opération métier répartie devient une chaîne de transactions locales ; en cas d’échec, des actions compensatoires annulent ou ajustent les étapes déjà réalisées.[[ltts](https://www.ltts.com/blog/eventual-consistency-microservices)]
- **Idempotence** : un consommateur doit pouvoir traiter deux fois le même événement sans dupliquer un effet, car les files peuvent livrer un message plus d’une fois.[[softwareengineering.stackexchange](https://softwareengineering.stackexchange.com/questions/354911/microservices-handling-eventual-consistency)]
- **Retry et dead-letter queue** : si un service est indisponible, l’événement est conservé, retenté, puis envoyé dans une file d’erreurs si le problème persiste.[[leyaa](https://leyaa.ai/codefly/learn/microservices/part-2/microservices-eventual-consistency-handling/visualize)]

## Les pièges à anticiper

- L’utilisateur peut voir une donnée pas encore à jour, par exemple une commande créée mais dont le stock ne semble pas encore décrémenté.[[algomaster](https://algomaster.io/learn/microservices/eventual-consistency)][[stackandsystem](https://stackandsystem.com/series/microservices/consistency-in-microservices-explained)]
- Il faut distinguer les données critiques, qui exigent parfois une cohérence forte, des données dérivées ou consultables, qui tolèrent mieux l’eventual consistency.[[nhimg](https://nhimg.org/faq/what-is-the-difference-between-eventual-consistency-and-strong-consistency-in-mi/)]
- « Eventually » n’a pas de délai garanti par défaut : sans conception et supervision explicites, la convergence peut prendre plus de temps que prévu.[[stackandsystem](https://stackandsystem.com/series/microservices/consistency-in-microservices-explained)]
- Les conflits d’écriture concurrents doivent être gérés, par exemple avec des versions, horodatages ou règles métier de résolution.[[geeksforgeeks](https://www.geeksforgeeks.org/system-design/what-is-eventual-consistency-between-microservices/)]

En pratique, on utilise souvent l’eventual consistency pour les flux asynchrones et non critiques, tout en conservant une cohérence forte sur les opérations où une divergence immédiate serait inacceptable, comme un paiement ou une réservation.[[nhimg](https://nhimg.org/faq/what-is-the-difference-between-eventual-consistency-and-strong-consistency-in-mi/)]



# Références

