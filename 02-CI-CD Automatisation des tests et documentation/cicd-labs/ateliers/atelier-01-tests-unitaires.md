# Atelier 1 — Tests unitaires avec pytest (1 h 15)

**Module 1** · Compétences C8 (TDD), C19 (Clean Code)

## Objectif
Écrire une suite de tests unitaires solide pour les règles de prix de MiniShop et mesurer la couverture.

## Contexte
Lisez l'en-tête de `minishop/pricing.py` : il décrit les règles métier (remise volume, coupons, livraison,
arrondi). Le fichier `tests/unit/test_pricing.py` contient 3 tests d'exemple et une liste de TODO.

## Étapes

### 1. Échauffement (10 min)
```bash
pytest -m unit -v
pytest -m unit --cov --cov-report=term-missing
```
Notez la couverture de départ de `pricing.py`. Quelles lignes ne sont jamais exécutées ?

### 2. Tests paramétrés (25 min)
Complétez les TODO. Utilisez `@pytest.mark.parametrize` pour éviter le copier-coller :
```python
@pytest.mark.parametrize("qty", [0, -1, 100, "2", True])
def test_quantite_invalide(qty):
    with pytest.raises(ValueError):
        line_total(Decimal("10"), qty)
```
Pensez **valeurs limites** : 9 vs 10 unités, 19,99 € vs 20 € pour WELCOME10, 49,99 € vs 50 € pour la livraison.

### 3. Un petit cycle TDD (20 min)
Nouvelle règle demandée par le métier :
> Coupon `STUDENT15` : -15 % sur le sous-total, sans minimum, **non cumulable** avec la remise volume
> (si une ligne a la remise volume, le coupon ne s'applique pas à cette ligne).

1. **Rouge** : écrivez d'abord 3 tests qui échouent.
2. **Vert** : implémentez le minimum dans `pricing.py`.
3. **Refactor** : nettoyez sans casser les tests.

### 4. Couverture et qualité (15 min)
```bash
pytest -m unit --cov --cov-branch --cov-report=html
```
Ouvrez `htmlcov/index.html` dans le navigateur (`open` sous macOS, `xdg-open` sous Linux, `start` sous Windows).
Objectif : **≥ 90 % de couverture de branches** sur `pricing.py`.
Question : 100 % de couverture garantit-il l'absence de bug ? Testez :
```bash
MINISHOP_BUG=rounding pytest -m unit
```
Vos tests détectent-ils le bug d'arrondi injecté ?

## Critères de réussite
- [ ] ≥ 15 tests, dont au moins 3 paramétrés
- [ ] Couverture branches ≥ 90 % sur `pricing.py`
- [ ] La suite échoue avec `MINISHOP_BUG=rounding`
- [ ] STUDENT15 implémenté en TDD (historique Git : commit des tests AVANT le code)

## Pour aller plus loin
- Tests de propriétés avec **Hypothesis** : « le total n'est jamais négatif », « ajouter un article ne baisse jamais le sous-total ».
- Tests de mutation : `python ai_tools/mutation_score.py minishop/pricing.py tests/unit` (on y reviendra à l'Atelier 3).
