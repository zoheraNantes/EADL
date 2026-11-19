# CI/CD : automatisation des tests avec l'IA et documentation — dépôt des ateliers

Application fil rouge **MiniShop** (FastAPI) et 12 ateliers pour apprendre à intégrer des tests
automatisés — unitaires, API, E2E, visuels, performance, sécurité — dans une pipeline CI/CD,
à les **augmenter avec l'IA** et à les **documenter / surveiller**.

## Démarrage rapide
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
python -m playwright install --with-deps chromium
make run          # http://localhost:8000  —  API : http://localhost:8000/docs
make test         # tests rapides
```
Détails : [ateliers/atelier-00-installation.md](ateliers/atelier-00-installation.md)

## Programme des ateliers
| # | Atelier | Module | Durée |
|---|---|---|---|
| 0 | [Installation du poste](ateliers/atelier-00-installation.md) | — | 0 h 30 |
| 1 | [Tests unitaires avec pytest (TDD, couverture)](ateliers/atelier-01-tests-unitaires.md) | M1 | 1 h 15 |
| 2 | [Premier pipeline GitHub Actions (+ GitLab CI)](ateliers/atelier-02-premier-pipeline.md) | M1 | 1 h 30 |
| 3 | [Générer des tests avec un LLM](ateliers/atelier-03-generation-tests-ia.md) | M2 | 2 h 30 |
| 4 | [L'IA dans la pipeline : génération et revue de PR](ateliers/atelier-04-ia-dans-la-ci.md) | M2 | 1 h 30 |
| 5 | [Anomalies dans les logs et les exécutions de tests](ateliers/atelier-05-anomalies-logs-tests.md) | M2 | 2 h |
| 6 | [ML : zones à risque et priorisation des tests](ateliers/atelier-06-ml-zones-a-risque.md) | M2 | 2 h 30 |
| 7 | [Tests visuels et outils AI-powered](ateliers/atelier-07-tests-visuels-ia.md) | M2 | 2 h |
| 8 | [Tests UI de bout en bout (Playwright, Selenium)](ateliers/atelier-08-tests-ui-e2e.md) | M3 | 2 h 30 |
| 9 | [Tests d'API (pytest, Postman/Newman, OpenAPI)](ateliers/atelier-09-tests-api.md) | M3 | 2 h |
| 10 | [Performance et charge (Locust, JMeter)](ateliers/atelier-10-performance.md) | M3 | 2 h 30 |
| 11 | [Sécurité automatisée (Bandit, pip-audit, Trivy, ZAP)](ateliers/atelier-11-securite.md) | M3 | 2 h 30 |
| 12 | [Reporting Allure, doc vivante, Prometheus/Grafana](ateliers/atelier-12-reporting-doc-monitoring.md) | M4 | 3 h |

## Outils IA fournis (`ai_tools/`)
| Script | Rôle | Atelier |
|---|---|---|
| `llm.py` | Client LLM (Anthropic, Mistral, Ollama, OpenAI, offline) | 3-5 |
| `generate_tests.py` | Spécification → tests pytest, exécutés immédiatement | 3, 4 |
| `mutation_score.py` | Score de mutation (qualité réelle des tests) | 3 |
| `review_pr.py` | Revue de PR orientée tests | 4 |
| `log_anomalies.py` | IsolationForest + z-score robuste sur logs JSON | 5 |
| `test_history.py` | Flaky, ralentissements, familles d'échecs (clustering) | 5 |
| `risk_model.py` | Modèle de risque Git → priorisation des tests | 6 |
| `visual_diff.py` | Diff pixel + SSIM, image de diff | 7 |
| `gen_test_docs.py` | Catalogue des tests généré (doc vivante) | 12 |
| `push_metrics.py` | Résultats JUnit → Prometheus Pushgateway | 12 |

## Bugs injectables (pour les démos de régression)
| Variable | Effet |
|---|---|
| `MINISHOP_BUG=rounding` | arrondi bancaire au lieu de commercial (0,125 → 0,12) |
| `MINISHOP_BUG=slow` | 300-800 ms de latence sur `/cart/*` |
