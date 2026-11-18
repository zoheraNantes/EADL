"""Test E2E Playwright — POINT DE DÉPART (Atelier 8).

Prérequis : application lancée (make run) ; BASE_URL=http://localhost:8000 par défaut.
Lancer :   pytest -m e2e --headed        (pour voir le navigateur)
"""

import re

import pytest
from playwright.sync_api import Page, expect

pytestmark = pytest.mark.e2e


def test_page_accueil(page: Page, app_url):
    page.goto(app_url)
    expect(page).to_have_title(re.compile("MiniShop"))
    expect(page.get_by_test_id("products").locator("li")).to_have_count(5)


# TODO Atelier 8 : ajouter 2 mugs, appliquer WELCOME10, vérifier le total, commander.
