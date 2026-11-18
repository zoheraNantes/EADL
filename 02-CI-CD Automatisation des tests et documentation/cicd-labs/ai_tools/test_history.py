"""Analyse de l'historique des exécutions de tests (fichiers JUnit XML).

Ce que fait le script :
  * Taux de réussite par test, nombre de « bascules » succès/échec -> score de FLAKINESS.
  * Tendance de durée (pente d'une régression linéaire) -> tests qui RALENTISSENT.
  * Durées anormales (z-score) sur le dernier run.
  * Regroupement des messages d'échec (TF-IDF + clustering) -> familles de pannes
    (timeout UI, assertion métier, infra BDD, réseau...).
  * Option --explain : un LLM résume chaque famille et propose une piste (si LLM configuré).

Usage :
    python ai_tools/test_history.py data/junit-history
    python ai_tools/test_history.py reports/history --explain --report reports/test-insights.md
"""

from __future__ import annotations

import argparse
import sys
import xml.etree.ElementTree as ET  # noqa: S405 — fichiers produits par notre propre CI
from collections import defaultdict
from pathlib import Path

import numpy as np
from sklearn.cluster import AgglomerativeClustering
from sklearn.feature_extraction.text import TfidfVectorizer

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ai_tools.llm import LLMError, chat, is_offline  # noqa: E402


def load_runs(folder: Path) -> list[dict]:
    runs = []
    for f in sorted(folder.glob("*.xml")):
        root = ET.parse(f).getroot()  # noqa: S314
        cases = {}
        for tc in root.iter("testcase"):
            name = f"{tc.get('classname')}::{tc.get('name')}"
            fail = tc.find("failure")
            if fail is None:
                fail = tc.find("error")
            cases[name] = {
                "time": float(tc.get("time", 0)),
                "failed": fail is not None,
                "message": (fail.get("message") or fail.text or "") if fail is not None else "",
            }
        runs.append({"file": f.name, "cases": cases})
    return runs


def per_test_stats(runs: list[dict]) -> list[dict]:
    series: dict[str, list[dict]] = defaultdict(list)
    for r in runs:
        for name, c in r["cases"].items():
            series[name].append(c)
    stats = []
    for name, s in series.items():
        fails = [c["failed"] for c in s]
        flips = sum(a != b for a, b in zip(fails, fails[1:], strict=False))
        times = np.array([c["time"] for c in s])
        slope = float(np.polyfit(np.arange(len(times)), times, 1)[0]) if len(times) > 2 else 0.0
        z_last = float((times[-1] - times[:-1].mean()) / (times[:-1].std() or 1)) if len(times) > 2 else 0.0
        # flakiness : beaucoup de bascules isolées (échec entouré de succès)
        isolated = sum(1 for i in range(1, len(fails) - 1) if fails[i] and not fails[i - 1] and not fails[i + 1])
        stats.append(
            {
                "test": name,
                "runs": len(s),
                "pass_rate": 1 - sum(fails) / len(fails),
                "flips": flips,
                "isolated_failures": isolated,
                "flaky_score": round(isolated / max(sum(fails), 1), 2) if sum(fails) >= 3 else 0.0,
                "mean_time": float(times.mean()),
                "slope_per_run": slope,
                "z_last": z_last,
            }
        )
    return stats


def cluster_failures(runs: list[dict], distance: float = 1.2) -> dict[int, list[tuple[str, str, str]]]:
    msgs = [(r["file"], n, c["message"]) for r in runs for n, c in r["cases"].items() if c["failed"]]
    if len(msgs) < 2:
        return {0: msgs} if msgs else {}
    X = TfidfVectorizer(token_pattern=r"[A-Za-z_]{3,}").fit_transform([m[2] for m in msgs]).toarray()
    labels = AgglomerativeClustering(n_clusters=None, distance_threshold=distance).fit_predict(X)
    groups: dict[int, list] = defaultdict(list)
    for lab, m in zip(labels, msgs, strict=True):
        groups[int(lab)].append(m)
    return dict(sorted(groups.items(), key=lambda kv: -len(kv[1])))


def explain(cluster_msgs: list[tuple[str, str, str]]) -> str:
    sample = "\n".join(f"- {t}: {m}" for _, t, m in cluster_msgs[:8])
    return chat(
        "Tu es un ingénieur SRE/QA. Réponds en français, en 3 lignes maximum.",
        "Voici des échecs de tests d'une même famille :\n"
        + sample
        + "\n\nDonne : 1) la cause probable, 2) bug applicatif, test fragile ou infra ?, 3) l'action à mener.",
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("folder", type=Path)
    ap.add_argument("--report", type=Path, default=Path("reports/test-insights.md"))
    ap.add_argument("--explain", action="store_true", help="résumé des familles d'échecs par LLM")
    args = ap.parse_args()

    runs = load_runs(args.folder)
    if not runs:
        print(f"Aucun fichier JUnit dans {args.folder}")
        return 1
    stats = per_test_stats(runs)
    flaky = sorted([s for s in stats if s["flaky_score"] >= 0.6], key=lambda s: -s["isolated_failures"])
    slowing = sorted(
        [s for s in stats if s["slope_per_run"] > 0.01 * max(s["mean_time"], 0.01)], key=lambda s: -s["slope_per_run"]
    )
    groups = cluster_failures(runs)

    L = [
        "# Analyse de l'historique des tests",
        "",
        f"{len(runs)} exécutions analysées, {len(stats)} tests.",
        "",
        "## Tests instables (flaky)",
        "",
        "| Test | Taux de réussite | Échecs isolés | Score |",
        "|---|---|---|---|",
    ]
    L += [f"| `{s['test']}` | {s['pass_rate']:.0%} | {s['isolated_failures']} | {s['flaky_score']} |" for s in flaky]
    L += [
        "",
        "## Tests qui ralentissent",
        "",
        "| Test | Durée moyenne | Pente (s/run) | Dernier run (z) |",
        "|---|---|---|---|",
    ]
    L += [f"| `{s['test']}` | {s['mean_time']:.2f}s | +{s['slope_per_run']:.4f} | {s['z_last']:.1f} |" for s in slowing]
    L += ["", "## Familles d'échecs (clustering des messages)", ""]
    for i, (lab, msgs) in enumerate(groups.items(), 1):
        tests = sorted({t.split("::")[1] for _, t, _ in msgs})
        runs_ = sorted({r for r, _, _ in msgs})
        L += [
            f"### Famille {i} — {len(msgs)} échecs, {len(runs_)} runs",
            "",
            f"- Exemple : `{msgs[0][2][:140]}`",
            f"- Tests touchés : {', '.join(tests)}",
            f"- Runs : {runs_[0]} … {runs_[-1]}",
        ]
        if args.explain and not is_offline():
            try:
                L += ["- **Analyse IA** : " + explain(msgs).replace("\n", " ")]
            except LLMError as exc:
                L += [f"- Analyse IA indisponible : {exc}"]
        L.append("")
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text("\n".join(L), encoding="utf-8")
    print("\n".join(L))
    return 0


if __name__ == "__main__":
    sys.exit(main())
