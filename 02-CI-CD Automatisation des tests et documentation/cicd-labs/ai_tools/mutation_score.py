"""Tests de mutation (version pédagogique, sans dépendance).

Principe : on introduit volontairement de petits bugs (« mutants ») dans le code,
un par un, et on relance les tests. Un mutant « tué » = les tests ont détecté le bug.
Score de mutation = mutants tués / mutants générés. C'est LE juge de la qualité
d'une suite de tests — en particulier des tests générés par IA (la couverture ne
dit pas si les tests vérifient vraiment quelque chose).

Mutations appliquées : opérateurs de comparaison (>= -> >, < -> <=, == -> !=),
opérateurs arithmétiques (+ <-> -, * <-> /), constantes numériques (+1),
chaînes Decimal("x") modifiées, booléens inversés.

Usage :
    python ai_tools/mutation_score.py minishop/pricing.py tests/unit
    python ai_tools/mutation_score.py minishop/pricing.py tests/generated --max 40
(Pour un outil complet : mutmut ou cosmic-ray en Python, PIT en Java, Stryker en JS.)
"""

from __future__ import annotations

import argparse
import ast
import copy
import subprocess
import sys
from pathlib import Path

CMP_SWAP = {ast.GtE: ast.Gt, ast.Gt: ast.GtE, ast.LtE: ast.Lt, ast.Lt: ast.LtE, ast.Eq: ast.NotEq, ast.NotEq: ast.Eq}
BIN_SWAP = {ast.Add: ast.Sub, ast.Sub: ast.Add, ast.Mult: ast.Div, ast.Div: ast.Mult}


def candidates(tree: ast.AST) -> list[tuple[int, str]]:
    """Liste (index du nœud, description) des mutations possibles, hors docstrings."""
    out = []
    docstrings = {
        id(n.body[0].value)
        for n in ast.walk(tree)
        if isinstance(n, (ast.Module, ast.FunctionDef))
        and n.body
        and isinstance(n.body[0], ast.Expr)
        and isinstance(n.body[0].value, ast.Constant)
    }
    for i, node in enumerate(ast.walk(tree)):
        if isinstance(node, ast.Compare) and type(node.ops[0]) in CMP_SWAP:
            out.append((i, f"l.{node.lineno} : {type(node.ops[0]).__name__} -> {CMP_SWAP[type(node.ops[0])].__name__}"))
        elif isinstance(node, ast.BinOp) and type(node.op) in BIN_SWAP:
            out.append((i, f"l.{node.lineno} : {type(node.op).__name__} -> {BIN_SWAP[type(node.op)].__name__}"))
        elif isinstance(node, ast.Constant) and id(node) not in docstrings:
            if isinstance(node.value, bool):
                out.append((i, f"l.{node.lineno} : {node.value} -> {not node.value}"))
            elif isinstance(node.value, int):
                out.append((i, f"l.{node.lineno} : {node.value} -> {node.value + 1}"))
            elif isinstance(node.value, str) and node.value.replace(".", "", 1).isdigit():
                out.append((i, f"l.{node.lineno} : '{node.value}' -> '{node.value}1'"))
    return out


def mutate(tree: ast.AST, index: int) -> ast.AST:
    t = copy.deepcopy(tree)
    node = list(ast.walk(t))[index]
    if isinstance(node, ast.Compare):
        node.ops[0] = CMP_SWAP[type(node.ops[0])]()
    elif isinstance(node, ast.BinOp):
        node.op = BIN_SWAP[type(node.op)]()
    elif isinstance(node.value, bool):
        node.value = not node.value
    elif isinstance(node.value, int):
        node.value += 1
    else:
        node.value = node.value + "1"
    return t


def run_tests(tests: str) -> bool:
    """True si les tests passent (=> mutant SURVIVANT)."""
    try:
        proc = subprocess.run(
            [sys.executable, "-m", "pytest", "-x", "-q", "-p", "no:cacheprovider", tests],
            capture_output=True,
            timeout=60,
        )
    except subprocess.TimeoutExpired:
        return False
    return proc.returncode == 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("source", type=Path)
    ap.add_argument("tests")
    ap.add_argument("--max", type=int, default=0, help="limiter le nombre de mutants (0 = tous)")
    args = ap.parse_args()

    original = args.source.read_text(encoding="utf-8")
    if not run_tests(args.tests):
        print("Les tests échouent déjà sur le code non muté : corrigez-les d'abord.")
        return 2
    tree = ast.parse(original)
    cands = candidates(tree)
    if args.max:
        cands = cands[:: max(1, len(cands) // args.max)][: args.max]
    killed, survivors = 0, []
    try:
        for n, (idx, desc) in enumerate(cands, 1):
            args.source.write_text(ast.unparse(mutate(tree, idx)), encoding="utf-8")
            survived = run_tests(args.tests)
            killed += not survived
            if survived:
                survivors.append(desc)
            print(f"[{n:>3}/{len(cands)}] {'SURVIT ' if survived else 'tué    '} {desc}")
    finally:
        args.source.write_text(original, encoding="utf-8")  # toujours restaurer le code
    score = killed / max(len(cands), 1)
    print(f"\nScore de mutation : {killed}/{len(cands)} = {score:.0%}")
    if survivors:
        print("Mutants survivants (= cas non vérifiés par vos tests) :")
        for s in survivors:
            print("  -", s)
    return 0


if __name__ == "__main__":
    sys.exit(main())
