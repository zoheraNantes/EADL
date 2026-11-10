

Date: 01/11/2026
Tags: 

[[Architecture logicielle]]
# Questions


# Notes

**GraphQL** est un langage de requête pour les API qui répond à des problèmes spécifiques des architectures REST traditionnelles:

1. **Réduire le sur-fetching** — récupérer uniquement les données nécessaires, pas toutes les champs d'une ressource
2. **Éliminer le sous-fetching** — obtenir en une seule requête des données qui nécessiteraient plusieurs appels REST
3. **Offrir une API flexible et fortement typée** — le client définit exactement ce dont il a besoin
4. **Simplifier l'évolution des API** — ajouter de nouveaux champs sans casser les clients existants

---

## Services rendus

| Aspect | Bénéfice |
|--------|----------|
| **Flexibilité des requêtes** | Le client spécifie quels champs il veut, pas le serveur |
| **Une seule requête pour données complexes** | Évite les appels multiples et le problème N+1 |
| **Documentation automatique** | Le schéma GraphQL est auto-documenté et explorable |
| **Introspection** | Les outils peuvent découvrir la structure de l'API dynamiquement |
| **Versionning implicite** | Pas besoin de versioner l'API (v1, v2, v3...) |
| **Typage fort** | Validation des requêtes avant d'atteindre le serveur |

---

## Cas d'usage principaux

### 1. **Applications mobiles avec connexions lentes**
Récupérer uniquement les champs nécessaires minimise la bande passante. Une mobile n'a besoin que du titre et l'image, pas de tous les détails d'un produit.

```graphql
query {
  product(id: "123") {
    title
    image
  }
}
```

### 2. **Interfaces avec multiples écrans/contextes**
La même ressource (utilisateur, produit) a besoin de données différentes selon l'écran:
- Fiche produit détaillée → tous les champs
- Liste de produits → titre, prix, image
- Recommandations → titre, image

GraphQL satisfait tous ces cas sans créer des endpoints différents.

### 3. **Agrégation de plusieurs sources de données**
Un dashboard qui combine données utilisateur + commandes + recommandations + analytics → **une seule requête GraphQL**, au lieu de 4 appels REST.

```graphql
query {
  user { name, email }
  orders { total, date }
  recommendations { product { title } }
  stats { visits, revenue }
}
```

### 4. **APIs publiques avec nombreux clients**
Les applications web, mobile, desktop, tiers — chacun peut demander exactement ce qu'il lui faut. Le backend ne doit pas créer des endpoints spécialisés pour chaque client.

### 5. **Real-time et subscriptions**
GraphQL supporte les **WebSockets** pour les notifications en temps réel:

```graphql
subscription {
  orderUpdated {
    id
    status
  }
}
```

### 6. **Mutation et mutations complexes**
Modifier plusieurs ressources liées en une seule requête:

```graphql
mutation {
  createOrder(items: [...]) {
    order { id }
    invoice { url }
    notification { sent }
  }
}
```

---

## Comparaison REST vs GraphQL

| Problème REST | Solution GraphQL |
|---|---|
| GET `/users/123` retourne tous les champs, même inutiles | Requête: `{ user(id: 123) { name, email } }` |
| Afficher utilisateur + ses 10 dernières commandes = 11 appels | Une seule requête avec données imbriquées |
| Ajouter un champ → risque de casser les clients | Ajouter un champ optionnel, clients existants ignorent |
| API mal documentée, endpoints flous | Schéma auto-documenté, explorable en IDE |

---

## Limites de GraphQL

- **Courbe d'apprentissage** — plus complexe que REST
- **Caching plus difficile** — HTTP GET/POST ne suffisent pas toujours
- **Nécessite du travail serveur** — parser et valider les requêtes est plus coûteux que des endpoints statiques
- **Overkill pour APIs simples** — si vous avez 3 endpoints simples, REST suffit



# Références

