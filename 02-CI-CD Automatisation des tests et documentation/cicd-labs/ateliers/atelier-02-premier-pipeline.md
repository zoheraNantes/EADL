# Atelier 2 — Premier pipeline CI avec GitHub Actions (1 h 30)

**Module 1** · Compétence C17

## Objectif
Construire un pipeline qui, à chaque push et Pull Request : lint, teste en parallèle sur plusieurs
versions de Python, mesure la couverture, publie les rapports et construit l'image Docker.

## Étapes

### 1. Le pipeline minimal (15 min)
Créez `.github/workflows/ci.yml` :
```yaml
name: CI
on:
  push:
    branches: [main]
  pull_request:
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.12" }
      - run: pip install -r requirements-dev.txt
      - run: pytest -m "unit or api"
```
Poussez sur votre branche, ouvrez une PR vers `main` **de votre fork** et observez l'onglet *Actions*.

### 2. Qualité de code (10 min)
Ajoutez un job `lint` (ruff) **avant** les tests (`needs: lint`). Utilisez
`ruff check . --output-format=github` : les erreurs s'affichent directement dans la PR.
Cassez volontairement le style pour voir l'annotation.

### 3. Matrice et parallélisme (20 min)
- Matrice Python `3.11`, `3.12`, `3.13` (`strategy.matrix`), `fail-fast: false`.
- Tests en parallèle dans chaque job : `pytest -n auto` (pytest-xdist).
- Cache pip (`cache: pip` de `setup-python`). Comparez la durée avant / après.

### 4. Rapports et quality gate (20 min)
- `--cov --cov-report=xml --cov-report=html --cov-fail-under=85 --junitxml=reports/junit.xml`
- Publiez `reports/` et `htmlcov/` avec `actions/upload-artifact@v4` **même en cas d'échec** (`if: always()`).
- Écrivez la couverture dans `$GITHUB_STEP_SUMMARY` (`coverage report --format=markdown`).

### 5. Conteneurs (15 min)
- Un job qui exécute les tests **dans** `python:3.12-slim` (`container:`).
- Un job `docker` qui construit l'image puis fait un *smoke test* (`curl /health`).

### 6. Protéger `main` (10 min)
Settings → Branches → règle sur `main` : PR obligatoire + checks `lint` et `unit` requis.

### 7. Équivalent GitLab CI (bonus, 10 min)
Traduisez votre pipeline en `.gitlab-ci.yml` (stages, `parallel: matrix`, `artifacts: reports: junit`).
Quelles notions sont identiques ? Lesquelles diffèrent ?

## Critères de réussite
- [ ] Pipeline vert sur la PR, 3 versions de Python
- [ ] Un test cassé fait échouer la PR et le rapport reste téléchargeable
- [ ] La couverture apparaît dans le résumé du run
- [ ] Image Docker construite et testée

## Pièges fréquents
- Indentation YAML (2 espaces, jamais de tabulation)
- Oublier `needs:` → tout part en parallèle
- `if: always()` manquant → pas de rapport quand on en a le plus besoin
