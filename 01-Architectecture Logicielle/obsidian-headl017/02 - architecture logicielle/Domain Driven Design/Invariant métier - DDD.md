

Date: 01/11/2026
Tags: 
[[02 - architecture logicielle/Domain Driven Design/Domain Driven Design|Domain Driven Design]]

# Questions


# Notes


En Domain Driven Design (DDD), une **business invariance** (invariant métier) est une **règle ou contrainte fondamentale** du domaine métier qui doit toujours être respectée, quel que soit l’état ou l’évolution du système. Ces invariants définissent ce qui doit rester vrai pour garantir la cohérence et la validité du modèle du domaine.[^1]

Par exemple :

- Pour un compte bancaire, un invariant typique serait que **le solde ne peut jamais devenir négatif**, quelle que soit la suite des opérations effectuées sur ce compte. 
- Dans une réservation, un invariant pourrait imposer qu’**une réservation ne peut exister sans référence à un client valide**.

Les invariants métiers sont :

- **Enforcés par le modèle du domaine** (via entités, agrégats, racines d’agrégats) et la logique métier dans le code.
- **Essentiels pour garantir la stabilité, la prévisibilité et la qualité du système**, car ils empêchent l’apparition d’états incohérents ou irréalistes dans l’application.  

Ils sont considérés comme une partie critique du design lors du développement d’un système complexe orienté métier, car ils traduisent les règles incontournables du métier dans la logique applicative, et l’ensemble des membres de l’équipe (métier et technique) doit les comprendre de façon claire et partagée. 


# Références

