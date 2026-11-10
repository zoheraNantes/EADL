
Date: 01/11/2026
Tags: 
[[Architecture logicielle]]

# Questions


# Notes

### 1. Principes généraux d’une API REST

- Une API REST est centrée sur des **ressources** (clients, commandes, produits…) identifiées par des URI et manipulées via HTTP.
- L’objectif est une interface **stateless**, faiblement couplée, indépendante de la plateforme et basée sur des formats standards (JSON principalement, parfois XML).
- On vise une API compréhensible, prévisible, performante, maintenable, documentée et sécurisée.

### 2. Conception des URI et des ressources

- Utiliser des URI clairs, lisibles et explicites, basés sur des **noms** (noms communs) représentant les ressources, pas des verbes : `/orders`, `/customers/5`, éviter `/create-order`.
- Utiliser le pluriel pour les collections (`/users`) et une hiérarchie simple collection/ressource : `/users/{id}`, `/users/{id}/orders`.
- Refléter les relations entre ressources dans les chemins, sans aller trop loin dans la profondeur (éviter des chaînes du type `/customers/1/orders/99/products/…`).
- Ne pas exposer directement la structure interne de la base (tables, schéma brut) : l’API doit modéliser le domaine métier, quitte à introduire une couche de mapping.

### 3. Méthodes HTTP et sémantique

- Respecter la sémantique standard des méthodes :
  - GET : lecture de ressource(s).
  - POST : création de ressource dans une collection ou envoi de données à traiter.
  - PUT : mise à jour complète (ou création si supporté) d’une ressource, idempotente.
  - PATCH : mise à jour partielle via document de patch (JSON Patch ou JSON Merge Patch).
  - DELETE : suppression d’une ressource.
- Adapter les comportements aux collections vs éléments (ex. POST sur `/customers` crée un client, GET sur `/customers/1` lit un client).
- Garantir l’idempotence de PUT et DELETE (même requête répétée → même résultat).

### 4. Représentations, formats et en-têtes

- Supporter des formats standardisés, principalement **JSON** (`application/json`), éventuellement XML (`application/xml`).
- Utiliser `Content-Type` pour annoncer le format envoyé, `Accept` pour le contenu souhaité par le client ; retourner 415 si le format n’est pas supporté, 406 si aucune représentation acceptable.
- Pour les grandes ressources binaires, envisager les réponses partielles avec `Accept-Ranges`, `Range` et le code 206 Partial Content, et éventuellement les requêtes HEAD.

### 5. Filtres, tri, pagination et projections

- Fournir des mécanismes de **filtrage** via des paramètres de requête (ex. `/orders?minCost=100&status=shipped`).
- Mettre en place **pagination** et éventuellement tri : paramètres `limit`/`offset` (ou `page`/`size`) et `sort=field[,asc|desc]` pour les collections importantes.
- Imposer un `limit` maximal pour éviter les abus et dérives de performance.
- Permettre des projections de champs (ex. `fields=id,name`) pour réduire la taille des réponses, tout en validant les champs exposés.

### 6. Codes de statut HTTP et gestion d’erreurs

- Utiliser des codes de statut **significatifs** :
  - 200, 201, 204 pour les succès (lecture, création, mise à jour/suppression sans contenu).
  - 400, 404, 409, 415, 422, etc. pour les erreurs côté client selon le cas ; 500+ pour erreurs serveur.
- En cas de longue opération, envisager un traitement **asynchrone** : retourner 202 Accepted, fournir une ressource de suivi `/status/{id}` qui indique l’état et, le cas échéant, redirige vers le résultat (303 See Other).
- Retourner des corps d’erreur structurés, explicites, avec un message clair et éventuellement un code d’erreur applicatif (ex. `{ "error": "Bad Request", "message": "The 'email' field is required." }`).

### 7. HATEOAS et navigation

- Enrichir les représentations de ressources avec des **liens hypermedia** vers les opérations et ressources liées (self, relations métier, actions possibles).
- Les liens décrivent la relation (`rel`), l’URL (`href`), la méthode HTTP et éventuellement les types supportés, ce qui permet au client de découvrir l’API dynamiquement.

### 8. Sécurité et robustesse

- Impératif d’utiliser HTTPS pour protéger les données en transit.
- Mettre en place des mécanismes d’authentification/autorisation adaptés : API keys, OAuth2/OIDC, JWT, etc.
- Limiter les abus et protéger contre les attaques (DoS, credential stuffing, bots) via **rate limiting**, quotas, éventuellement CAPTCHA et surveillance des anomalies.
- Ne pas exposer les détails internes sensibles dans les messages d’erreur.

### 9. Documentation et découverte

- Documenter l’API de manière exhaustive : description des endpoints, paramètres, schémas de requêtes/réponses, codes de statut, exemples.
- Utiliser des outils comme **Swagger/OpenAPI** pour produire une documentation interactive et maintenable, et éventuellement des SDK générés.

### 10. Versioning

- Anticiper l’évolution de l’API et éviter de casser les clients existants.
- Stratégies possibles :
  - URI versionnée (ex. `/v1/users`), simple et cache-friendly mais verbeuse.
  - Paramètre de query (ex. `/customers/3?version=2`).
  - En-têtes personnalisés (ex. `Custom-Header: api-version=2`).
  - Versionnement par media type (ex. `Accept: application/vnd.contoso.v1+json`).
- Si possible, éviter le versionnement pour les changements non cassants (ajout de champs ignorés par les anciens clients).

### 11. Aspects avancés : multitenant et découpage

- Pour une API **multi-tenant**, définir clairement comment le tenant est identifié (sous-domaine, segment d’URL, header, token) et garantir l’isolation des données.
- Éviter les API « bavardes » (trop de petites ressources nécessitant de nombreuses requêtes) ; regrouper les données quand c’est cohérent pour limiter la chattiness tout en évitant les réponses surdimensionnées.

### 12. Pour aller plus loin

[https://restfulapi.net/rest-api-n-1-problem/](https://restfulapi.net/rest-api-n-1-problem/)


# Références

