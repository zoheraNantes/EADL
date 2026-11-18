"""Génération de tests pytest à partir d'une spécification en langage naturel.

Deux moteurs :
  * LLM (LLM_PROVIDER=anthropic|mistral|ollama|openai) : le modèle lit la spec ET le
    code source, puis propose des tests (scénarios de la spec + cas limites).
  * offline (par défaut) : un analyseur déterministe de la grammaire Gherkin
    (voir l'en-tête de specs/pricing.feature) — utile sans réseau et comme
    « vérité terrain » pour comparer avec la sortie du LLM.

Dans tous les cas, les tests générés sont EXÉCUTÉS immédiatement (garde-fou) :
un test généré qui échoue est soit un bug de l'application, soit une
hallucination du modèle -> revue humaine obligatoire.

Usage :
    python ai_tools/generate_tests.py specs/pricing.feature \
        --source minishop/pricing.py --out tests/generated/test_pricing_generated.py
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ai_tools.llm import LLMError, chat, extract_code, is_offline, provider  # noqa: E402

PROMPT_FILE = Path(__file__).parent / "prompts" / "generate_tests.md"

FIELDS = {"sous-total": "subtotal", "remise": "discount", "livraison": "shipping", "total": "total"}


# --------------------------------------------------------------------------- offline
def slug(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")


def parse_feature(text: str) -> list[dict]:
    scenarios, current = [], None
    for raw in text.splitlines():
        line = raw.strip()
        if line.startswith("Scénario:") or line.startswith("Scenario:"):
            current = {"name": line.split(":", 1)[1].strip(), "items": [], "coupon": None, "asserts": [], "error": None}
            scenarios.append(current)
            continue
        if current is None or not line or line.startswith("#"):
            continue
        if "panier avec" in line:
            current["items"] = [{"product_id": p, "qty": int(q)} for q, p in re.findall(r'(\d+)\s+"([^"]+)"', line)]
        elif m := re.search(r'coupon "([^"]+)"', line):
            current["coupon"] = m.group(1)
        elif m := re.search(r"(sous-total|remise|livraison|total) vaut ([\d.]+)", line):
            current["asserts"].append((FIELDS[m.group(1)], m.group(2)))
        elif m := re.search(r'erreur "([^"]+)"', line):
            current["error"] = m.group(1)
    return scenarios


def render_offline(scenarios: list[dict], spec_name: str) -> str:
    out = [
        f'"""Tests générés automatiquement depuis {spec_name} (moteur : offline).',
        "",
        "NE PAS MODIFIER À LA MAIN : régénérer avec ai_tools/generate_tests.py",
        '"""',
        "from decimal import Decimal",
        "",
        "import pytest",
        "",
        "from minishop.pricing import quote",
        "",
        "pytestmark = [pytest.mark.generated, pytest.mark.unit]",
        "",
    ]
    for sc in scenarios:
        out += ["", "", f"def test_{slug(sc['name'])}():", f'    """{sc["name"]}"""']
        call = f"quote({sc['items']!r}, {sc['coupon']!r})"
        if sc["error"]:
            exc = "KeyError" if "Produit" in sc["error"] else "ValueError"
            out += [f"    with pytest.raises({exc}, match={sc['error']!r}):", f"        {call}"]
        else:
            out.append(f"    q = {call}")
            out += [f'    assert q.{f} == Decimal("{v}")' for f, v in sc["asserts"]]
    return "\n".join(out) + "\n"


# --------------------------------------------------------------------------- LLM
def render_llm(spec: str, source: str, spec_name: str) -> str:
    system = PROMPT_FILE.read_text(encoding="utf-8")
    user = (
        f"## Spécification ({spec_name})\n\n{spec}\n\n"
        f"## Code source sous test\n\n```python\n{source}\n```\n\n"
        "Génère le fichier de tests complet."
    )
    return extract_code(chat(system, user))


# --------------------------------------------------------------------------- garde-fou
def run_pytest(path: Path) -> tuple[bool, str]:
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", str(path)], capture_output=True, text=True
    )
    return proc.returncode == 0, proc.stdout[-3000:]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("spec", type=Path)
    ap.add_argument("--source", type=Path, default=Path("minishop/pricing.py"))
    ap.add_argument("--out", type=Path, default=Path("tests/generated/test_pricing_generated.py"))
    ap.add_argument("--no-run", action="store_true", help="ne pas exécuter les tests générés")
    args = ap.parse_args()

    spec = args.spec.read_text(encoding="utf-8")
    if is_offline():
        engine, code = "offline", render_offline(parse_feature(spec), args.spec.name)
    else:
        try:
            engine, code = provider(), render_llm(spec, args.source.read_text(encoding="utf-8"), args.spec.name)
        except LLMError as exc:
            print(f"[!] LLM indisponible ({exc}) -> repli sur le moteur offline", file=sys.stderr)
            engine, code = "offline", render_offline(parse_feature(spec), args.spec.name)

    try:
        compile(code, str(args.out), "exec")
    except SyntaxError as exc:
        print(f"[x] Le code généré ne compile pas : {exc}", file=sys.stderr)
        args.out.with_suffix(".rejected.txt").write_text(code, encoding="utf-8")
        return 2

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(code, encoding="utf-8")
    subprocess.run([sys.executable, "-m", "ruff", "format", "-q", str(args.out)], capture_output=True)
    n = len(re.findall(r"^def test_", code, flags=re.M))
    print(f"[+] {n} tests écrits dans {args.out} (moteur : {engine})")
    if args.no_run:
        return 0
    ok, output = run_pytest(args.out)
    print(output)
    print(
        "[+] Tous les tests générés passent"
        if ok
        else "[!] Des tests générés échouent : à analyser (bug ou hallucination ?)"
    )
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
