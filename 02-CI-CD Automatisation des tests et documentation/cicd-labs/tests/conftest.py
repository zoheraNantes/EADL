"""Fixtures partagées."""

import os

import pytest
from fastapi.testclient import TestClient

from minishop.api import app


@pytest.fixture
def client():
    """Client HTTP en mémoire (pas de serveur à lancer)."""
    return TestClient(app)


@pytest.fixture(scope="session")
def app_url():
    """URL de l'application réelle pour les tests e2e / perf / sécurité."""
    return os.getenv("BASE_URL", "http://localhost:8000")
