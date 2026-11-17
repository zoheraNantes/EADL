
Date: 01/11/2026
Tags: 
[[Architecture logicielle]]

# Questions


# Notes


Pattern utilisé dans les applications microservices modernes qui définit un point d'entrée unique au backend depuis les différents frontends.

1. Gestion de la sécurité centralisée
2. Gestion du trafic optimisée ( routage avec équilibrage de charge, limitation de débit)
3. Aggrégation des réponses : le client fait une seule requête, l'api gateway gère les requêtes internes et fait une seule réponse
4. L'api gateway fait office de facade masquant la compléxité et l'emplacement réel des traitements

Inconvénient : peut générer de l'over fetching ou de l'under fetching (problème de chatty client)

### Avantage 1 : Sécurité centralisée

Elle gère l'authentification (OAuth, JWT), l'autorisation et la protection contre les attaques (DDoS, rate limiting) en un seul endroit, évitant de dupliquer ces contrôles sur chaque service.

### Avantage 2 : Gestion du trafic optimisée

Routage intelligent, équilibrage de charge, mise en cache et limitation de débit améliorent les performances et la disponibilité, en masquant la complexité des backends.

### Avantage 3 : Simplification client

Les clients font une seule requête ; la gateway agrège les réponses de multiples services, traduit les protocoles et génère une API cohérente, facilitant le développement frontend.

# Références

