"""Détection d'anomalies dans des logs applicatifs JSON (une ligne = une requête).

Approche (apprentissage NON supervisé) :
  1. Fenêtrage : on agrège les logs par fenêtres de N secondes
     (nb requêtes, taux d'erreurs 5xx/4xx, latence p50/p95/max, chemins inconnus).
  2. IsolationForest isole les fenêtres « atypiques » sans avoir besoin d'exemples étiquetés.
  3. En complément, une règle simple par requête (z-score robuste de la latence
     par route) pour pointer les requêtes précises.

Usage :
    python ai_tools/log_anomalies.py data/app-logs.jsonl --window 30 --contamination 0.02
    python ai_tools/log_anomalies.py logs/app.jsonl --fail-on-anomaly   # mode « quality gate » CI
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
from sklearn.ensemble import IsolationForest

KNOWN_PATHS = {
    "/products",
    "/products/{product_id}",
    "/cart/quote",
    "/orders",
    "/orders/{order_id}",
    "/health",
    "/metrics",
    "/",
    "/openapi.json",
    "/docs",
}


def load(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def windows(logs: list[dict], size: int) -> tuple[list[int], np.ndarray]:
    buckets: dict[int, list[dict]] = defaultdict(list)
    for e in logs:
        buckets[int(e["ts"] // size)].append(e)
    keys = sorted(buckets)
    feats = []
    for k in keys:
        b = buckets[k]
        lat = sorted(e["latency_ms"] for e in b)
        feats.append(
            [
                len(b),
                sum(e["status"] >= 500 for e in b) / len(b),
                sum(400 <= e["status"] < 500 for e in b) / len(b),
                lat[len(lat) // 2],
                lat[int(len(lat) * 0.95) - 1 if len(lat) > 1 else 0],
                lat[-1],
                sum(e["path"] not in KNOWN_PATHS for e in b),
            ]
        )
    return keys, np.array(feats)


def per_request_outliers(logs: list[dict], threshold: float = 6.0) -> list[dict]:
    by_path: dict[str, list[float]] = defaultdict(list)
    for e in logs:
        by_path[e["path"]].append(e["latency_ms"])
    stats = {}
    for p, v in by_path.items():
        med = statistics.median(v)
        mad = statistics.median(abs(x - med) for x in v) or 1.0
        stats[p] = (med, mad)
    out = []
    for e in logs:
        med, mad = stats[e["path"]]
        z = 0.6745 * (e["latency_ms"] - med) / mad
        if z > threshold or e["path"] not in KNOWN_PATHS:
            out.append({**e, "robust_z": round(z, 1)})
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("logfile", type=Path)
    ap.add_argument("--window", type=int, default=30, help="taille des fenêtres en secondes")
    ap.add_argument("--contamination", type=float, default=0.02, help="part d'anomalies attendue")
    ap.add_argument("--report", type=Path, default=Path("reports/anomalies.md"))
    ap.add_argument("--fail-on-anomaly", action="store_true", help="code retour 1 si anomalie (quality gate)")
    args = ap.parse_args()

    logs = load(args.logfile)
    keys, X = windows(logs, args.window)
    if len(keys) < 10:
        print("Pas assez de données pour un modèle (min. 10 fenêtres).")
        return 0
    model = IsolationForest(contamination=args.contamination, random_state=0).fit(X)
    scores = model.decision_function(X)
    flagged = [(keys[i], scores[i], X[i]) for i in np.where(model.predict(X) == -1)[0]]
    flagged.sort(key=lambda t: t[1])
    outliers = per_request_outliers(logs)

    lines = [
        "# Rapport d'anomalies",
        "",
        f"- Fichier : `{args.logfile}` — {len(logs)} requêtes, {len(keys)} fenêtres de {args.window}s",
        f"- Fenêtres anormales (IsolationForest) : **{len(flagged)}**",
        f"- Requêtes atypiques (z-score robuste / chemin inconnu) : **{len(outliers)}**",
        "",
        "## Fenêtres les plus atypiques",
        "",
        "| Début (ts) | Score | Req. | 5xx | 4xx | p50 ms | p95 ms | max ms | chemins inconnus |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for k, s, f in flagged[:15]:
        lines.append(
            f"| {k * args.window} | {s:.3f} | {int(f[0])} | {f[1]:.0%} | {f[2]:.0%} | "
            f"{f[3]:.0f} | {f[4]:.0f} | {f[5]:.0f} | {int(f[6])} |"
        )
    lines += [
        "",
        "## Exemples de requêtes atypiques",
        "",
        "| ts | méthode | chemin | statut | latence ms | z |",
        "|---|---|---|---|---|---|",
    ]
    for e in outliers[:20]:
        lines.append(
            f"| {e['ts']} | {e['method']} | `{e['path']}` | {e['status']} | {e['latency_ms']} | {e['robust_z']} |"
        )

    # Évaluation si les données contiennent la vérité terrain (données simulées)
    if any("_truth" in e for e in logs):
        truth = {i for i, e in enumerate(logs) if e.get("_truth")}
        found = {
            i for i, e in enumerate(logs) if e.get("_truth") is not None and any(o["ts"] == e["ts"] for o in outliers)
        }
        lines += [
            "",
            "## Évaluation (données simulées)",
            "",
            f"- Rappel sur les requêtes anormales connues : {len(found)}/{len(truth)} "
            f"({len(found) / max(len(truth), 1):.0%})",
            f"- Précision : {len(found)}/{len(outliers)} signalements sont de vraies anomalies "
            f"({len(found) / max(len(outliers), 1):.0%})",
        ]

    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines[:6]))
    print(f"\nRapport complet : {args.report}")
    return 1 if (args.fail_on_anomaly and flagged) else 0


if __name__ == "__main__":
    sys.exit(main())
