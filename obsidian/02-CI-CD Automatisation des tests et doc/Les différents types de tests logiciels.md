
Date: 16/11/2026
Tags: 
[[Les différents types de tests logiciels]]

# Questions
# Notes

En développement logiciel, les tests permettent de vérifier le fonctionnement, la qualité, la sécurité et la fiabilité d'une application.

Ils sont classés selon leur niveau, leur objectif et leur méthode d'exécution.

## 1. Tests par niveau

- **Test unitaire** : vérifie une fonction, une méthode ou un composant isolé.
- **Test d'intégration** : vérifie que plusieurs composants fonctionnent ensemble.
- **Test système** : vérifie le fonctionnement de l'application complète.
- **Test d'acceptation (recette)** : vérifie que l'application répond aux besoins du client.
- **Test de bout en bout (E2E – End-to-End)** : vérifie un parcours utilisateur complet.

## 2. Tests fonctionnels

- **Test fonctionnel** : vérifie qu'une fonctionnalité respecte les exigences.
- **Test de non-régression** : vérifie qu'une modification n'a pas cassé une fonctionnalité existante.
- **Smoke test (test de fumée)** : vérifie rapidement les fonctionnalités essentielles.
- **Sanity test (test de cohérence)** : vérifie rapidement une fonctionnalité après une modification.
- **Test exploratoire** : recherche des anomalies sans suivre uniquement des scénarios prédéfinis.
- **Test d'interface utilisateur (UI – User Interface)** : vérifie les interactions avec l'interface.
- **Test d'API (Application Programming Interface)** : vérifie les réponses et comportements d'une API.

## 3. Tests non fonctionnels

- **Test de performance** : mesure les performances de l'application.
- **Test de charge** : vérifie le comportement avec un nombre attendu d'utilisateurs ou de requêtes.
- **Test de stress** : vérifie le comportement au-delà des limites normales.
- **Test d'endurance (Soak test)** : vérifie la stabilité sur une longue durée.
- **Test de montée en charge (Scalability test)** : vérifie la capacité à supporter une augmentation de charge.
- **Test de sécurité** : recherche les vulnérabilités.
- **Test de pénétration (Pentest)** : simule des attaques autorisées pour identifier des failles.
- **Test d'accessibilité** : vérifie l'utilisation de l'application par des personnes en situation de handicap.
- **Test de compatibilité** : vérifie le fonctionnement sur différents navigateurs, systèmes et appareils.
- **Test de fiabilité** : vérifie que l'application fonctionne correctement dans la durée.
- **Test de récupération** : vérifie la capacité à reprendre après une panne.
- **Test de résilience** : vérifie le comportement face aux défaillances.

## 4. Tests selon la méthode

- **Test boîte noire (Black-box)** : teste le comportement sans examiner le code interne.
- **Test boîte blanche (White-box)** : teste en tenant compte de la structure du code.
- **Test boîte grise (Grey-box)** : combine une connaissance partielle du fonctionnement interne avec des tests externes.
- **Test manuel** : exécuté par une personne.
- **Test automatisé** : exécuté par un outil ou un script.
- **Test basé sur les risques** : priorise les tests selon les risques identifiés.
- **Test de mutation** : modifie volontairement le code pour vérifier que les tests détectent les erreurs.

## 5. Tests spécifiques à la CI/CD

**CI/CD = Continuous Integration / Continuous Delivery ou Continuous Deployment**

En français : intégration continue / livraison continue ou déploiement continu.

Les tests suivants peuvent être intégrés dans un pipeline CI/CD :

- **Tests unitaires automatisés**
- **Tests d'intégration automatisés**
- **Tests d'API automatisés**
- **Tests de non-régression automatisés**
- **Tests E2E automatisés**
- **Tests de sécurité automatisés**
- **Tests de performance automatisés**

Ces tests permettent de vérifier automatiquement le logiciel lors des modifications du code.

## À retenir

Les catégories de tests peuvent se recouper.

Par exemple, un test d'API peut être à la fois :
- Un test d'intégration.
- Un test fonctionnel.
- Un test automatisé.
- Un test de non-régression.

Il n'existe pas de liste universelle exhaustive : d'autres tests spécialisés existent selon les applications et les technologies.

## Sources

- [ISTQB – Certified Tester Foundation Level 4.0](https://istqb.org/certifications/certified-tester-foundation-level-ctfl-v4-0/) — Référentiel international des tests logiciels.
