
Date: 01/11/2026
Tags: 
[[00 - Tags/Domain Driven Design|Domain Driven Design]]

# Questions


# Notes

En **Domain Driven Design (DDD)**, un **agrégat** est un concept central qui désigne un ensemble cohérent d’objets du domaine (entités et objets valeur) regroupés afin d’être manipulés comme une seule unité de cohérence métier[^1][^3][^9][^8].

L’agrégat possède plusieurs caractéristiques clés :

- **Racine d’agrégat** (aggregate root) : C’est l’entité principale par laquelle on accède à l’ensemble de l’agrégat. Seule cette racine est visible et accessible à l’extérieur de l’agrégat, assurant la cohérence et l’intégrité de toutes les règles métier internes.
- **Frontière de cohérence** : Les invariants métier (règles qui doivent toujours être vraies) sont garantis à l’intérieur de l’agrégat. Les modifications des entités ou objets valeur internes ne peuvent se faire que via la racine d’agrégat.
- **Manipulation unitaire** : Les opérations de création, modification ou suppression sont réalisées sur l’agrégat entier, garantissant l’intégrité des données du groupe.
- **Limite d’accès**: Les autres parties du système ne peuvent manipuler l’intérieur de l’agrégat que par l’intermédiaire de la racine, jamais directement.

**Exemple typique**: Une **facture** est un agrégat : elle contient des lignes, un client, un montant, etc. Les lignes de la facture ne peuvent être ajoutées, modifiées ou supprimées qu’à travers la facture elle-même, jamais indépendamment. La facture joue ici le rôle de racine d’agrégat.

Le pattern d’agrégat permet ainsi de :

- Structurer le modèle métier en unités cohérentes,
- Simplifier les accès et la gestion des règles métier complexes,
- Limiter les dépendances et interactions entre différentes parties du modèle, ce qui aide à maîtriser la complexité globale du système.

En résumé, **un agrégat, en DDD, est un groupe d’objets (entités, objets valeur) formant une unité métier cohérente, dont l’accès et la modification passent par une racine unique, garantissant ainsi l’intégrité et la cohérence métier**.


# Références

https://www.rebaze.fr/chapitre-formation/definition-et-role-des-agregats