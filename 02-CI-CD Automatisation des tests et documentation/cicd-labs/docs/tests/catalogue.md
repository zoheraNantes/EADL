# Catalogue des tests

_Généré automatiquement le 16/11/2026 03:24 — ne pas éditer à la main._
**8 tests** — 2 documentés (25%).


## `tests/api/test_api_smoke.py`

Tests d'API — POINT DE DÉPART (Atelier 1, puis Atelier 9).

| Statut | Test | Marqueurs | Description | Durée |
|---|---|---|---|---|
| ✅ | `test_health` | api | ⚠️ _non documenté_ | 0.01s |
| ✅ | `test_liste_produits` | api | ⚠️ _non documenté_ | 0.00s |

## `tests/e2e/test_parcours_achat.py`

Test E2E Playwright — POINT DE DÉPART (Atelier 8).

| Statut | Test | Marqueurs | Description | Durée |
|---|---|---|---|---|
| · | `test_page_accueil` | e2e | ⚠️ _non documenté_ | 0.00s |

## `tests/unit/test_pricing.py`

Tests unitaires des règles de prix — POINT DE DÉPART (Atelier 1).

| Statut | Test | Marqueurs | Description | Durée |
|---|---|---|---|---|
| ✅ | `test_money_arrondi_commercial` | unit | 0.125 s'arrondit à 0.13 (ROUND_HALF_UP), pas 0.12. | 0.00s |
| ✅ | `test_line_total_sans_remise` | unit | ⚠️ _non documenté_ | 0.00s |
| ✅ | `test_quote_panier_vide` | unit | Un panier vide coûte 0 € : pas de frais de livraison. | 0.00s |

## `tests/visual/test_visual.py`

Tests de régression visuelle (Atelier 7).

| Statut | Test | Marqueurs | Description | Durée |
|---|---|---|---|---|
| · | `test_accueil` | visual | ⚠️ _non documenté_ | 0.00s |
| · | `test_panier_avec_total` | visual | ⚠️ _non documenté_ | 0.00s |
