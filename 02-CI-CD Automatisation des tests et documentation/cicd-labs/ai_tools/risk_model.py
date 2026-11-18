"""Prédiction des zones à risque à partir de l'historique Git (apprentissage SUPERVISÉ).

Idée : chaque ligne de data/git-history.csv = (commit, fichier modifié, caractéristiques)
avec l'étiquette `broke_ci` (ce commit a-t-il cassé la CI ?). On entraîne un modèle qui,
pour un NOUVEAU changement, estime la probabilité de casse -> on priorise les tests
liés aux fichiers les plus risqués (test impact analysis / test prioritization).

Étapes :
  train   : entraîne + évalue (validation temporelle : on apprend sur le passé,
            on teste sur le futur), affiche l'importance des variables, sauve le modèle.
  predict : lit les fichiers modifiés (git diff ou --files) et propose l'ordre des tests.

Usage :
    python ai_tools/risk_model.py train data/git-history.csv
    python ai_tools/risk_model.py predict --files minishop/pricing.py README.md
    python ai_tools/risk_model.py predict --git-diff origin/main     # dans la CI
"""

from __future__ import annotations

import argparse
import csv
import json
import pickle  # noqa: S403 — modèle produit localement
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score

MODEL = Path("reports/risk_model.pkl")
FEATURES = [
    "lines_added",
    "lines_deleted",
    "files_in_commit",
    "is_fix_commit",
    "late_hour",
    "file_past_commits",
    "file_past_breaks_rate",
    "author_past_breaks_rate",
    "is_code",
]

# Correspondance fichier -> tests à lancer en priorité (à maintenir, ou à déduire de la couverture)
TEST_MAP = {
    "minishop/pricing.py": ["tests/unit/test_pricing.py", "tests/generated"],
    "minishop/catalog.py": ["tests/unit", "tests/api"],
    "minishop/api.py": ["tests/api", "tests/e2e"],
    "minishop/static/": ["tests/e2e", "tests/visual"],
}


def load(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def featurize(rows: list[dict]) -> tuple[np.ndarray, np.ndarray, dict]:
    """Variables calculées UNIQUEMENT avec le passé de chaque ligne (pas de fuite de données)."""
    file_commits, file_breaks = defaultdict(int), defaultdict(int)
    author_commits, author_breaks = defaultdict(int), defaultdict(int)
    X, y = [], []
    for r in rows:
        f, a = r["file"], r["author"]
        X.append(
            [
                int(r["lines_added"]),
                int(r["lines_deleted"]),
                int(r["files_in_commit"]),
                int(r["is_fix_commit"]),
                int(int(r["hour"]) >= 20),
                file_commits[f],
                file_breaks[f] / file_commits[f] if file_commits[f] else 0.0,
                author_breaks[a] / author_commits[a] if author_commits[a] else 0.0,
                int(f.endswith((".py", ".html", ".js"))),
            ]
        )
        y.append(int(r["broke_ci"]))
        file_commits[f] += 1
        file_breaks[f] += int(r["broke_ci"])
        author_commits[a] += 1
        author_breaks[a] += int(r["broke_ci"])
    state = {
        "file_commits": dict(file_commits),
        "file_breaks": dict(file_breaks),
        "author_commits": dict(author_commits),
        "author_breaks": dict(author_breaks),
    }
    return np.array(X, dtype=float), np.array(y), state


def train(csv_path: Path) -> int:
    rows = load(csv_path)
    X, y, state = featurize(rows)
    cut = int(len(X) * 0.75)  # validation TEMPORELLE
    models = {
        "Régression logistique": LogisticRegression(max_iter=1000),
        "Gradient boosting": GradientBoostingClassifier(random_state=0),
    }
    best, best_auc = None, -1.0
    print(f"{len(X)} lignes — apprentissage sur {cut}, test sur {len(X) - cut} (les plus récentes)\n")
    for name, m in models.items():
        m.fit(X[:cut], y[:cut])
        proba = m.predict_proba(X[cut:])[:, 1]
        auc = roc_auc_score(y[cut:], proba)
        print(f"== {name} : AUC = {auc:.3f}")
        print(classification_report(y[cut:], (proba >= 0.5).astype(int), target_names=["ok", "casse"], zero_division=0))
        if auc > best_auc:
            best, best_auc = m, auc
    base = max(y[cut:].mean(), 1 - y[cut:].mean())
    print(f"Référence naïve (toujours la classe majoritaire) : exactitude {base:.0%}")
    if hasattr(best, "feature_importances_"):
        imp = sorted(zip(FEATURES, best.feature_importances_, strict=True), key=lambda t: -t[1])
        print("\nImportance des variables :")
        for f, v in imp:
            print(f"  {f:<26} {'█' * int(v * 50)} {v:.2f}")
    elif hasattr(best, "coef_"):
        print("\nCoefficients (signe = sens de l'effet ; variables non normalisées) :")
        for f, v in sorted(zip(FEATURES, best.coef_[0], strict=True), key=lambda t: -abs(t[1])):
            print(f"  {f:<26} {v:+.3f}")
    print(
        "\nAstuce atelier : essayez class_weight='balanced' et un seuil de décision < 0.5 "
        "(le rappel sur « casse » compte plus que l'exactitude)."
    )
    best.fit(X, y)  # ré-entraînement sur tout l'historique
    MODEL.parent.mkdir(parents=True, exist_ok=True)
    MODEL.write_bytes(pickle.dumps({"model": best, "state": state}))
    print(f"\nModèle sauvegardé : {MODEL}")
    return 0


def changed_files(ref: str) -> list[tuple[str, int, int]]:
    out = subprocess.run(["git", "diff", "--numstat", ref], capture_output=True, text=True, check=True).stdout
    res = []
    for line in out.splitlines():
        a, d, f = line.split("\t")
        res.append((f, int(a) if a.isdigit() else 0, int(d) if d.isdigit() else 0))
    return res


def predict(files: list[tuple[str, int, int]], author: str, hour: int) -> int:
    bundle = pickle.loads(MODEL.read_bytes())  # noqa: S301
    m, st = bundle["model"], bundle["state"]
    scored = []
    for f, a, d in files:
        fc, fb = st["file_commits"].get(f, 0), st["file_breaks"].get(f, 0)
        ac, ab = st["author_commits"].get(author, 0), st["author_breaks"].get(author, 0)
        x = [
            [
                a,
                d,
                len(files),
                0,
                int(hour >= 20),
                fc,
                fb / fc if fc else 0.0,
                ab / ac if ac else 0.0,
                int(f.endswith((".py", ".html", ".js"))),
            ]
        ]
        scored.append((f, float(m.predict_proba(np.array(x, dtype=float))[0, 1])))
    scored.sort(key=lambda t: -t[1])
    order: list[str] = []
    for f, _ in scored:
        for prefix, tests in TEST_MAP.items():
            if f.startswith(prefix):
                order += [t for t in tests if t not in order]
    print("Risque estimé par fichier modifié :")
    for f, p in scored:
        print(f"  {p:6.1%}  {f}")
    print("\nOrdre de test proposé :", " ".join(order) or "(aucun test ciblé : suite complète)")
    Path("reports").mkdir(exist_ok=True)
    Path("reports/tests_to_run.txt").write_text(" ".join(order) + "\n", encoding="utf-8")
    Path("reports/risk.json").write_text(json.dumps(dict(scored), indent=2), encoding="utf-8")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    t = sub.add_parser("train")
    t.add_argument("csv", type=Path)
    p = sub.add_parser("predict")
    p.add_argument("--files", nargs="*", default=[])
    p.add_argument("--git-diff", help="référence git à comparer (ex. origin/main)")
    p.add_argument("--author", default="alice")
    p.add_argument("--hour", type=int, default=15)
    args = ap.parse_args()
    if args.cmd == "train":
        return train(args.csv)
    files = changed_files(args.git_diff) if args.git_diff else [(f, 30, 10) for f in args.files]
    return predict(files, args.author, args.hour)


if __name__ == "__main__":
    sys.exit(main())
