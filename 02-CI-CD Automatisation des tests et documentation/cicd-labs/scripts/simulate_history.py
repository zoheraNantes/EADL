"""Génère des données réalistes pour les ateliers IA/ML (Module 2) et monitoring (Module 4).

Produit dans data/ :
  junit-history/run-XXX.xml : 60 exécutions de CI au format JUnit, avec
        - un test « flaky » (échoue ~15 % du temps sans changement de code),
        - un test dont la durée se dégrade progressivement,
        - une vraie régression introduite au run 48 (corrigée au run 52),
        - des familles d'erreurs (timeout, assertion, connexion BDD).
  app-logs.jsonl : 5 000 lignes de logs HTTP dont ~1 % d'anomalies
        (pics de latence, rafales de 500, chemins inhabituels).
  git-history.csv : historique de modifications par fichier et par commit,
        avec l'étiquette « ce commit a cassé la CI » (pour le modèle de risque).

Les données sont déterministes (graine fixe) : tout le monde obtient les mêmes chiffres.
Usage : python scripts/simulate_history.py
"""

from __future__ import annotations

import csv
import json
import random
from pathlib import Path
from xml.sax.saxutils import escape

DATA = Path(__file__).resolve().parents[1] / "data"
rng = random.Random(42)

TESTS = {
    "tests.unit.test_pricing::test_money_arrondi_commercial": 0.004,
    "tests.unit.test_pricing::test_remise_volume_a_partir_de_10": 0.003,
    "tests.unit.test_pricing::test_coupon_discount[WELCOME10]": 0.003,
    "tests.unit.test_pricing::test_shipping_cost": 0.002,
    "tests.api.test_api::test_quote_ok": 0.05,
    "tests.api.test_api::test_commande_cycle_complet": 0.08,
    "tests.api.test_api::test_contrat_openapi": 0.04,
    "tests.e2e.test_parcours_achat::test_parcours_achat_avec_coupon": 2.4,  # flaky
    "tests.e2e.test_parcours_achat::test_page_accueil": 0.9,
    "tests.api.test_api::test_recherche_produits": 0.12,  # se dégrade
    "tests.integration.test_stock::test_reservation_stock": 0.6,
}
FLAKY = "tests.e2e.test_parcours_achat::test_parcours_achat_avec_coupon"
DEGRADING = "tests.api.test_api::test_recherche_produits"
REGRESSION = "tests.unit.test_pricing::test_remise_volume_a_partir_de_10"

ERRORS = {
    "timeout": "TimeoutError: Locator.click: Timeout 5000ms exceeded waiting for get_by_test_id('order-btn')",
    "assert": "AssertionError: assert Decimal('23.27') == Decimal('23.28')",
    "db": "OperationalError: could not connect to server: Connection refused (localhost:5432)",
    "net": "httpx.ConnectError: [Errno 111] Connection refused",
}

FILES = [
    "minishop/pricing.py",
    "minishop/api.py",
    "minishop/catalog.py",
    "minishop/static/index.html",
    "minishop/static/style.css",
    "minishop/stock.py",
    "minishop/search.py",
    "README.md",
    "docs/index.md",
]
FILE_RISK = {
    "minishop/pricing.py": 0.30,
    "minishop/api.py": 0.22,
    "minishop/stock.py": 0.28,
    "minishop/search.py": 0.18,
    "minishop/catalog.py": 0.08,
    "minishop/static/index.html": 0.12,
    "minishop/static/style.css": 0.05,
    "README.md": 0.01,
    "docs/index.md": 0.01,
}
AUTHORS = ["alice", "bob", "chloe", "driss", "emma"]


def junit_history(n_runs: int = 60) -> None:
    out = DATA / "junit-history"
    out.mkdir(parents=True, exist_ok=True)
    for run in range(1, n_runs + 1):
        cases, failures, total_time = [], 0, 0.0
        for name, base in TESTS.items():
            dur = base * rng.uniform(0.8, 1.25)
            if name == DEGRADING:
                dur = base * (1 + run * 0.06) * rng.uniform(0.9, 1.1)
            err = None
            if name == FLAKY and rng.random() < 0.15:
                err = ("timeout", ERRORS["timeout"])
                dur = 5.2
            if name == REGRESSION and 48 <= run < 52:
                err = ("assert", ERRORS["assert"])
            if name.startswith("tests.integration") and run in (23, 24):
                err = ("db", ERRORS["db"])
            if name.startswith("tests.api") and run == 37:
                err = ("net", ERRORS["net"])
            classname, test = name.split("::")
            total_time += dur
            body = ""
            if err:
                failures += 1
                body = f'<failure message="{escape(err[1], {chr(34): "&quot;"})}" type="{err[0]}">{escape(err[1])}</failure>'
            cases.append(
                f'    <testcase classname="{classname}" name="{escape(test)}" time="{dur:.3f}">{body}</testcase>'
            )
        ts = f"2026-10-{1 + (run - 1) // 2:02d}T{9 + (run % 2) * 5:02d}:00:00"
        xml = [
            '<?xml version="1.0" encoding="utf-8"?>',
            "<testsuites>",
            f'  <testsuite name="pytest" tests="{len(cases)}" failures="{failures}" errors="0" '
            f'time="{total_time:.3f}" timestamp="{ts}" hostname="ci-run-{run:03d}">',
            *cases,
            "  </testsuite>",
            "</testsuites>",
        ]
        (out / f"run-{run:03d}.xml").write_text("\n".join(xml), encoding="utf-8")


def app_logs(n: int = 5000) -> None:
    paths = ["/products", "/products/{product_id}", "/cart/quote", "/orders", "/health"]
    weights = [30, 25, 25, 8, 12]
    t = 1_790_000_000.0
    lines = []
    for i in range(n):
        t += rng.expovariate(2.0)
        path = rng.choices(paths, weights)[0]
        latency = max(1.0, rng.gauss({"/cart/quote": 18, "/orders": 35}.get(path, 8), 3))
        status = 200 if path != "/orders" else 201
        if rng.random() < 0.01:
            status = rng.choice([404, 422])
        kind = None
        if 3000 <= i < 3040:  # rafale d'erreurs 500 sur /orders
            path, status, latency, kind = "/orders", 500, rng.gauss(900, 120), "burst_500"
        elif rng.random() < 0.004:  # pics de latence isolés
            latency, kind = rng.uniform(1500, 4000), "latency_spike"
        elif rng.random() < 0.002:  # scan / chemin inhabituel
            path, status, latency, kind = rng.choice(["/.env", "/wp-admin", "/admin/config"]), 404, 2.0, "scan"
        lines.append(
            json.dumps(
                {
                    "ts": round(t, 3),
                    "method": "GET" if "products" in path or path == "/health" else "POST",
                    "path": path,
                    "status": status,
                    "latency_ms": round(latency, 2),
                    "_truth": kind,
                }
            )
        )
    (DATA / "app-logs.jsonl").write_text("\n".join(lines) + "\n", encoding="utf-8")


def git_history(n_commits: int = 600) -> None:
    rows = []
    for c in range(1, n_commits + 1):
        files = rng.sample(FILES, k=rng.choice([1, 1, 2, 2, 3, 4]))
        author = rng.choice(AUTHORS)
        is_fix = rng.random() < 0.2
        for f in files:
            added = int(rng.expovariate(1 / 25)) + 1
            deleted = int(rng.expovariate(1 / 12))
            p = FILE_RISK[f] * (1 + min(added + deleted, 300) / 150)
            if author == "emma":  # nouvelle arrivée : plus de casse au début
                p *= 1.6 if c < 300 else 1.0
            if f.endswith((".md", ".css")):
                p *= 0.5
            broke = rng.random() < min(p, 0.95)
            rows.append(
                {
                    "commit": f"c{c:04d}",
                    "file": f,
                    "author": author,
                    "lines_added": added,
                    "lines_deleted": deleted,
                    "is_fix_commit": int(is_fix),
                    "files_in_commit": len(files),
                    "hour": rng.choice([9, 10, 11, 14, 15, 16, 17, 18, 22, 23]),
                    "broke_ci": int(broke),
                }
            )
    with (DATA / "git-history.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    DATA.mkdir(exist_ok=True)
    junit_history()
    app_logs()
    git_history()
    print(f"Données générées dans {DATA}/ : junit-history/ (60 runs), app-logs.jsonl, git-history.csv")
