"""Revue de Pull Request assistée par IA : risques + tests manquants.

Lit un diff (git diff BASE...HEAD), demande au LLM une analyse orientée TEST,
et écrit un commentaire Markdown (posté sur la PR par la CI).

L'IA CONSEILLE, elle ne bloque pas : le job ne fait jamais échouer la pipeline
(décision humaine), sauf option --fail-on-high.

Usage :
    python ai_tools/review_pr.py --base origin/main --out reports/ai-review.md
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ai_tools.llm import LLMError, chat, is_offline  # noqa: E402

SYSTEM = """Tu es un relecteur de code expert en qualité logicielle et en tests automatisés.
On te donne le diff d'une Pull Request d'une application Python (FastAPI).
Réponds en français, en Markdown, avec EXACTEMENT ces sections :
### Résumé (2 lignes)
### Risques détectés  (liste ; préfixe chaque risque par [ÉLEVÉ], [MOYEN] ou [FAIBLE])
### Tests manquants   (liste de tests concrets à écrire : nom de test + ce qu'il vérifie)
### Proposition de test (UN test pytest complet dans un bloc ```python)
Ne commente pas le style. N'invente rien qui n'est pas dans le diff."""

MAX_CHARS = 24_000


def get_diff(base: str) -> str:
    return subprocess.run(
        ["git", "diff", f"{base}...HEAD", "--", ".", ":(exclude)data/*"], capture_output=True, text=True, check=True
    ).stdout


def offline_review(diff: str) -> str:
    """Heuristiques simples : utile sans LLM et pour comparer avec la sortie du modèle."""
    added = [ln[1:] for ln in diff.splitlines() if ln.startswith("+") and not ln.startswith("+++")]
    files = sorted({ln[6:] for ln in diff.splitlines() if ln.startswith("+++ b/")})
    code_files = [f for f in files if f.startswith("minishop/")]
    test_files = [f for f in files if f.startswith("tests/")]
    risks = []
    if code_files and not test_files:
        risks.append("[ÉLEVÉ] Du code applicatif change sans aucun test ajouté ou modifié.")
    if any("float(" in ln for ln in added):
        risks.append("[MOYEN] Usage de float pour des montants : préférer Decimal.")
    if any(k in ln for ln in added for k in ("print(", "breakpoint(", "pdb")):
        risks.append("[FAIBLE] Code de débogage laissé dans le diff.")
    if any("except:" in ln or "except Exception:" in ln for ln in added):
        risks.append("[MOYEN] Exception attrapée trop largement.")
    return "\n".join(
        [
            "### Résumé",
            f"{len(files)} fichier(s) modifié(s), {len(added)} ligne(s) ajoutée(s).",
            "### Risques détectés",
            *(f"- {r}" for r in risks or ["- Aucun risque détecté par les règles."]),
            "### Tests manquants",
            *(f"- Tests pour `{f}`" for f in code_files if not test_files),
            "",
            "_Revue heuristique (mode offline). Configurez LLM_PROVIDER pour une revue IA._",
        ]
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="origin/main")
    ap.add_argument("--diff-file", type=Path, help="utiliser un fichier diff plutôt que git")
    ap.add_argument("--out", type=Path, default=Path("reports/ai-review.md"))
    ap.add_argument("--fail-on-high", action="store_true")
    args = ap.parse_args()

    diff = args.diff_file.read_text(encoding="utf-8") if args.diff_file else get_diff(args.base)
    if not diff.strip():
        body = "Aucun changement à analyser."
    elif is_offline():
        body = offline_review(diff)
    else:
        truncated = diff[:MAX_CHARS] + ("\n[... diff tronqué ...]" if len(diff) > MAX_CHARS else "")
        try:
            body = chat(SYSTEM, f"```diff\n{truncated}\n```")
        except LLMError as exc:
            body = offline_review(diff) + f"\n\n> LLM indisponible : {exc}"
    header = "## 🤖 Revue IA orientée tests\n\n> Suggestions générées automatiquement : à valider par un humain.\n\n"
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(header + body + "\n", encoding="utf-8")
    print(header + body)
    return 1 if (args.fail_on_high and "[ÉLEVÉ]" in body) else 0


if __name__ == "__main__":
    sys.exit(main())
