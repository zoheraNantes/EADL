# MiniShop — documentation qualité

Cette documentation est **versionnée avec le code** (docs-as-code) et **republiée à chaque pipeline**.

| Rapport | Où le trouver |
|---|---|
| Catalogue des tests (généré) | [Catalogue](tests/catalogue.md) |
| Rapport Allure | artefact `allure-report` du dernier run / GitHub Pages `/allure/` |
| Couverture | artefact `coverage-html` |
| Tableau de bord | Grafana « Qualité des tests — MiniShop » |

```mermaid
flowchart LR
  A[push / PR] --> B[lint + unit]
  B --> C[API + E2E]
  C --> D[perf + sécurité]
  D --> E[rapports Allure + doc]
  E --> F[(Pushgateway / Grafana)]
```
