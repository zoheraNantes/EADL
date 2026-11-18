"""Tests unitaires des règles de prix — POINT DE DÉPART (Atelier 1).

Complétez ce fichier : objectif >= 90 % de couverture sur minishop/pricing.py.
"""

from decimal import Decimal

import pytest

from minishop.pricing import line_total, money, quote

pytestmark = pytest.mark.unit


def test_money_arrondi_commercial():
    """0.125 s'arrondit à 0.13 (ROUND_HALF_UP), pas 0.12."""
    assert money("0.125") == Decimal("0.13")


def test_line_total_sans_remise():
    assert line_total(Decimal("12.50"), 2) == Decimal("25.00")


def test_quote_panier_vide():
    """Un panier vide coûte 0 € : pas de frais de livraison."""
    q = quote([])
    assert q.total == Decimal("0.00")
    assert q.shipping == Decimal("0.00")


# TODO Atelier 1 :
#  - remise volume à partir de 10 unités (et pas à 9 !)
def test_ligne_total_avec_remise_partir_de_10():
    """Une remise est appliqué à partir de 10 unités."""
    assert line_total(Decimal("10"), 9) == Decimal("90")
    assert line_total(Decimal("10"), 10) == Decimal("95")


#  - quantités invalides (0, 100, -1, "2", True) -> ValueError   (astuce : @pytest.mark.parametrize)
@pytest.mark.parametrize("qty", [0, -1, 100, "2", True])
def test_quantite_invalide(qty):
    with pytest.raises(ValueError):
        line_total(Decimal("10"), qty)


#  - coupons WELCOME10 / FIXED5 / FREESHIP (seuils inclus/exclus), coupon inconnu, casse
#  - livraison offerte à partir de 50 € APRÈS remise
#  - produit inconnu -> KeyError


# Test volontaire du linter Ruff
# Cette variable est déclarée mais jamais utilisée.
# Ruff doit détecter l'erreur F841.


# Test volontaire du linter Ruff pour vérifier que Ruff détecte une variable inutilisée (F841).
# À réactiver pour tester l'échec du pipeline CI l'erreur F841.

# def test_erreur_style():
#     prix = 10  # Variable inutilisée
#     assert True
