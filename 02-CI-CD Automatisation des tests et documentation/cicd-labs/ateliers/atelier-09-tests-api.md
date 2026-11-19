# Atelier 9 — Tests d'API (2 h)

**Module 3** · Tests API avec Postman, RestAssured (et pytest)

## Objectif
Tester l'API MiniShop à trois niveaux : tests en code (pytest), collection Postman exécutée en CI
(Newman), et tests de contrat / propriétés générés depuis le schéma OpenAPI.

## Partie A — pytest + TestClient (50 min)
Complétez `tests/api/test_api_smoke.py` (ou créez `tests/api/test_api.py`) :
- `/products/{id}` : 200 et 404 ;
- `/cart/quote` : 200 (vérifier le total), 404 produit inconnu, 422 quantité 0 / 100 / coupon inconnu / corps invalide ;
- `/orders` : 201 puis `GET /orders/{id}` renvoie la même commande ; 422 panier vide ;
- `/metrics` expose `minishop_http_requests_total`.
Le `TestClient` appelle l'application **en mémoire** : rapide, pas de serveur à lancer.
Variante « serveur réel » : même tests avec `httpx.Client(base_url=app_url)` contre l'appli Docker.

## Partie B — Test de contrat (20 min)
Écrivez un test qui échoue si une route publique disparaît ou si un champ de réponse change de type
(lisez `/openapi.json`). Discussion : contrat **côté fournisseur** vs **côté consommateur** (Pact).

## Partie C — Postman / Newman (30 min)
1. Importez `tests/api/minishop.postman_collection.json` dans Postman, lancez-la.
2. Ajoutez 2 requêtes avec scripts de test (`pm.test(...)`), dont une qui enchaîne
   « créer une commande » → « la relire » (variable `pm.collectionVariables.set("orderId", ...)`).
3. En ligne de commande / CI :
   ```bash
   npx newman run tests/api/minishop.postman_collection.json --env-var baseUrl=http://localhost:8000 \
       -r cli,junit --reporter-junit-export reports/newman.xml
   ```

## Partie D — Tests générés depuis OpenAPI (20 min)
```bash
pip install schemathesis
schemathesis run http://localhost:8000/openapi.json --checks all
```
Schemathesis génère des centaines de requêtes (propriétés, cas limites). Trouve-t-il des réponses 500 ?
Lien avec le Module 2 : c'est de la génération de tests **à partir d'une spécification**, sans LLM.

## RestAssured (Java) — pour information
Si votre équipe est en Java, l'équivalent de la partie A :
```java
given().contentType(JSON).body("{\"items\":[{\"product_id\":\"mug\",\"qty\":2}],\"coupon\":\"WELCOME10\"}")
.when().post("/cart/quote")
.then().statusCode(200).body("total", equalTo("27.40"));
```

## Critères de réussite
- [ ] ≥ 12 tests d'API, codes d'erreur compris
- [ ] Test de contrat en place
- [ ] Collection Postman exécutée par Newman avec rapport JUnit
- [ ] Schemathesis lancé, résultats analysés
