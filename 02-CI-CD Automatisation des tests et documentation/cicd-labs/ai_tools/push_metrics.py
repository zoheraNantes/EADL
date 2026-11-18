"""Pousse les résultats d'un run de tests (JUnit XML) vers un Prometheus Pushgateway.

Métriques exposées (labels : job, branch) :
  ci_tests_total, ci_tests_failed, ci_tests_skipped, ci_tests_duration_seconds,
  ci_tests_pass_ratio, ci_test_case_duration_seconds{test=...}, ci_last_run_timestamp

Usage :
    python ai_tools/push_metrics.py reports/junit.xml --gateway localhost:9091 --branch main
    # rejouer l'historique simulé pour remplir Grafana :
    python ai_tools/push_metrics.py data/junit-history/*.xml --gateway localhost:9091 --replay
"""

from __future__ import annotations

import argparse
import time
import xml.etree.ElementTree as ET  # noqa: S405
from pathlib import Path

from prometheus_client import CollectorRegistry, Gauge, push_to_gateway


def parse(path: Path) -> dict:
    root = ET.parse(path).getroot()  # noqa: S314
    cases = list(root.iter("testcase"))
    failed = sum(tc.find("failure") is not None or tc.find("error") is not None for tc in cases)
    skipped = sum(tc.find("skipped") is not None for tc in cases)
    return {
        "total": len(cases),
        "failed": failed,
        "skipped": skipped,
        "duration": sum(float(tc.get("time", 0)) for tc in cases),
        "cases": {f"{tc.get('classname')}::{tc.get('name')}": float(tc.get("time", 0)) for tc in cases},
    }


def push(res: dict, gateway: str, job: str, branch: str) -> None:
    reg = CollectorRegistry()
    labels = ["branch"]
    Gauge("ci_tests_total", "Nombre de tests", labels, registry=reg).labels(branch).set(res["total"])
    Gauge("ci_tests_failed", "Tests en échec", labels, registry=reg).labels(branch).set(res["failed"])
    Gauge("ci_tests_skipped", "Tests ignorés", labels, registry=reg).labels(branch).set(res["skipped"])
    Gauge("ci_tests_duration_seconds", "Durée cumulée", labels, registry=reg).labels(branch).set(res["duration"])
    ran = max(res["total"] - res["skipped"], 1)
    Gauge("ci_tests_pass_ratio", "Taux de réussite", labels, registry=reg).labels(branch).set(
        (ran - res["failed"]) / ran
    )
    g = Gauge("ci_test_case_duration_seconds", "Durée par test", ["branch", "test"], registry=reg)
    for name, t in res["cases"].items():
        g.labels(branch, name).set(t)
    Gauge("ci_last_run_timestamp", "Horodatage du run", labels, registry=reg).labels(branch).set_to_current_time()
    push_to_gateway(gateway, job=job, registry=reg)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("junit", nargs="+", type=Path)
    ap.add_argument("--gateway", default="localhost:9091")
    ap.add_argument("--job", default="minishop-ci")
    ap.add_argument("--branch", default="main")
    ap.add_argument("--replay", action="store_true", help="pause entre fichiers (scrape Prometheus)")
    ap.add_argument("--interval", type=float, default=6.0)
    args = ap.parse_args()
    for f in args.junit:
        res = parse(f)
        push(res, args.gateway, args.job, args.branch)
        print(f"{f.name}: {res['total']} tests, {res['failed']} échecs, {res['duration']:.1f}s -> {args.gateway}")
        if args.replay:
            time.sleep(args.interval)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
