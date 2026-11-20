# Chapitre 03 — Bonnes pratiques et TDD

## 1. Méthode AAA

AAA = Arrange, Act, Assert.

Cette méthode organise un test en trois étapes.

- **Arrange (Préparer)** : préparer les données et les conditions du test.
    
- **Act (Agir)** : exécuter l'action à tester.
    
- **Assert (Vérifier)** : comparer le résultat obtenu au résultat attendu.
    

## 2. Principes FIRST

FIRST définit cinq qualités d'un bon test.

- **F — Fast** : rapide.
    
- **I — Isolated** : indépendant des autres tests.
    
- **R — Repeatable** : reproductible.
    
- **S — Self-validating** : indique clairement réussite ou échec.
    
- **T — Timely** : écrit au bon moment, idéalement avec le code.
    

## 3. TDD — Test-Driven Development

Développement piloté par les tests.

Le TDD consiste à écrire un test avant d'implémenter la fonctionnalité correspondante.

### Cycle TDD

**1. Rouge**

- Écrire un test qui échoue.
    

**2. Vert**

- Écrire le minimum de code nécessaire pour réussir le test.
    

**3. Refactor**

- Améliorer le code sans modifier son comportement.
    
- Vérifier que les tests réussissent toujours.
    

**4. Recommencer**

- Passer à la règle suivante.
    

## À retenir

- **AAA** = structure d'un test.
    
- **FIRST** = qualités d'un bon test.
    
- **TDD** = méthode de développement.
    
- **Rouge → Vert → Refactor** = cycle TDD.