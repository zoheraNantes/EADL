"""Tests d'API — POINT DE DÉPART (Atelier 1, puis Atelier 9)."""

import pytest

pytestmark = pytest.mark.api


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_liste_produits(client):
    r = client.get("/products")
    assert r.status_code == 200
    assert {"mug", "tshirt"} <= {p["id"] for p in r.json()}


# TODO Atelier 9 : /products/{id} (200, 404), /cart/quote (200, 404, 422), /orders (201, 422), GET /orders/{id}
