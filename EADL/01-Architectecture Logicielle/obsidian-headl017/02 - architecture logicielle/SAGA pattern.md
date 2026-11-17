
Date: 01/11/2026
Tags: 
[[Architecture logicielle]]

# Questions


# Notes

L'architecture SAGA est un modèle de gestion des transactions distribuées qui permet de maintenir la cohérence des données dans des systèmes répartis, notamment les architectures de microservices. Plutôt que d'utiliser une unique transaction atomique répartie (comme le protocole Two-Phase Commit, 2PC, qui peut bloquer le système et constituer un point de défaillance), SAGA divise une grande transaction en plusieurs sous-transactions locales, exécutées séquentiellement. Chaque étape a sa propre transaction locale qui met à jour la base de données correspondante et déclenche la suivante.

Si une étape échoue, SAGA utilise une action compensatoire pour annuler les effets des étapes précédentes, assurant ainsi la cohérence globale sans bloquer le système. Ce modèle élimine les points de blocage et permet une meilleure tolérance aux pannes dans les systèmes distribués.

Il existe deux approches principales pour implémenter SAGA :

- **Chorégraphie (Event-Driven)** : Chaque service exécute sa tâche et publie un événement pour déclencher la suivante, sans coordonnateur central.
- **Orchestration (Centralisée)** : Un orchestrateur gère explicitement le déroulement des étapes et déclenche les actions ou compensations nécessaires.

Un exemple typique est le processus de commande e-commerce : création de commande, paiement, mise à jour du stock, livraison. Chaque étape est une transaction locale et, en cas d’échec, les compensations (annulation, remboursement, restitution) sont appliquées pour revenir à un état cohérent.

Ainsi, l’architecture SAGA est un modèle robuste pour gérer les transactions longues et distribuées dans des systèmes composés de plusieurs services autonomes.


# Références

