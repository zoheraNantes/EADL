
Date: 01/11/2026
Tags: 
[[02 - architecture logicielle/Domain Driven Design/Domain Driven Design|Domain Driven Design]]

# Questions


# Notes

Un **Value Object** (objet valeur) en Domain Driven Design (DDD) est un objet *immuable* qui représente un concept du domaine métier défini uniquement par ses **attributs** et qui n’a **pas d’identité propre**. Contrairement aux entités, un Value Object est comparé par l’égalité de ses valeurs et non par une identité unique. Par exemple, une adresse, une couleur, ou un montant d’argent peuvent être modélisés comme des Value Objects.

Les principales caractéristiques d’un Value Object sont :

- **Immutabilité** : Une fois créé, ses attributs ne peuvent plus être modifiés, ce qui garantit la cohérence et la prévisibilité.
- **Absence d’identité** : Deux Value Objects avec les mêmes attributs sont considérés identiques, sans distinction basée sur un ID.
- **Encapsulation de concepts métier** : Ils représentent des notions composées, souvent complexes, qui ont un sens métier précis.
- **Égalité basée sur la valeur** : L’égalité est déterminée par la comparaison de leurs propriétés, pas par référence d’objet.

Ils facilitent une modélisation claire et robuste, protègent la cohérence des données et simplifient le code métier en encapsulant des règles de validation et de gestion des données dans l’objet lui-même.

Par exemple, deux objets `Adresse` avec le même numéro de rue, code postal et ville sont considérés comme identiques, et il ne sert à rien d’identifier une adresse par un ID unique.

Ainsi, un Value Object sert à représenter des concepts métiers significatifs sans gestion d’identité, en garantissant la stabilité et la cohérence des données dans le domaine applicatif.

# Références

