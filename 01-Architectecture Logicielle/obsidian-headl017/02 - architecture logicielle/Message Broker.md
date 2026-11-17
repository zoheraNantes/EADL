
Date: 01/11/2026
Tags: 
[[Microservices]]

# Questions


# Notes


Un **message broker** (ou *agent de messages*) est un **logiciel intermédiaire** qui permet à différentes applications, services ou systèmes de **communiquer entre eux en envoyant et recevant des messages**, sans qu’ils aient besoin de connaître directement l’autre.

### Rôle principal

- Il **reçoit** les messages d’un émetteur (producteur / publisher).
- Il **stocke**, **route** et **achemine** ces messages vers un ou plusieurs destinataires (consommateurs / subscribers).
- Il gère la **délivrance fiable** des messages, souvent avec des files d’attente ou un modèle pub‑sub (*publish/subscribe*).


### Pourquoi on l’utilise

- Permet des communications **asynchrones** : l’émetteur ne bloque pas en attendant la réponse.
- Permet le **découplage** entre services (microservices, front / back, apps legacy, etc.).
- Facilite la **scalabilité** et la **résilience** (messages persistés, retries, gestion de charge).





# Références

