"""Tests de régression visuelle (Atelier 7).

Premier lancement : les baselines n'existent pas -> elles sont créées et le test est
« skipped ». Committez tests/visual/baselines/*.png ; les lancements suivants comparent.
Pour accepter un changement volontaire : UPDATE_BASELINES=1 pytest -m visual

Prérequis : application lancée (make run).
"""

import os
import shutil
import sys
from pathlib import Path

import pytest
from playwright.sync_api import Page

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from ai_tools.visual_diff import compare  # noqa: E402

pytestmark = pytest.mark.visual

HERE = Path(__file__).parent
BASE, CURRENT, DIFF = HERE / "baselines", HERE / "current", HERE / "diff"


def check(page: Page, name: str, **kwargs):
    CURRENT.mkdir(exist_ok=True)
    current = CURRENT / f"{name}.png"
    page.screenshot(path=str(current), **kwargs)
    baseline = BASE / f"{name}.png"
    if not baseline.exists() or os.getenv("UPDATE_BASELINES") == "1":
        BASE.mkdir(exist_ok=True)
        shutil.copy(current, baseline)
        pytest.skip(f"Baseline créée : {baseline}")
    r = compare(baseline, current, DIFF / f"{name}.png")
    assert r.ok(max_diff=0.002, min_ssim=0.99), (
        f"Régression visuelle sur '{name}' : {r.diff_ratio:.3%} pixels, SSIM={r.ssim:.4f} -> voir {DIFF / name}.png"
    )


@pytest.fixture
def shop(page: Page, app_url):
    page.set_viewport_size({"width": 1280, "height": 800})
    page.goto(app_url)
    page.get_by_test_id("add-mug").wait_for()
    return page


def test_accueil(shop: Page):
    check(shop, "accueil", full_page=True)


def test_panier_avec_total(shop: Page):
    shop.get_by_test_id("add-mug").click()
    shop.get_by_test_id("add-tshirt").click()
    shop.get_by_test_id("quote-btn").click()
    shop.get_by_test_id("summary").wait_for()
    check(shop, "panier", clip={"x": 853, "y": 0, "width": 427, "height": 800})
