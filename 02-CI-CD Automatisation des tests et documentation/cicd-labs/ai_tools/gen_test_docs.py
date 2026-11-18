"""Documentation vivante : génère le catalogue des tests à partir du code des tests.

Pour chaque fichier tests/**/test_*.py : docstring du module, puis chaque test
(nom, marqueurs, docstring, paramètres). Si un rapport JUnit est fourni, ajoute le
dernier statut (✅/❌/⏭) et la durée -> la doc est mise à jour À CHAQUE PIPELINE.

Usage :
    python ai_tools/gen_test_docs.py --junit reports/junit.xml --out docs/tests/catalogue.md
"""

from __future__ import annotations

import argparse
import ast
import datetime as dt
import re
import xml.etree.ElementTree as ET  # noqa: S405
from pathlib import Path


def marks_of(node: ast.FunctionDef, module_marks: list[str]) -> list[str]:
    marks = list(module_marks)
    for d in node.decorator_list:
        src = ast.unparse(d)
        if src.startswith("pytest.mark."):
            marks.append(src.removeprefix("pytest.mark.").split("(")[0])
    return marks


def module_marks(tree: ast.Module) -> list[str]:
    for n in tree.body:
        if isinstance(n, ast.Assign) and any(getattr(t, "id", "") == "pytestmark" for t in n.targets):
            return re.findall(r"pytest\.mark\.(\w+)", ast.unparse(n.value))
    return []


def junit_status(path: Path | None) -> dict[str, tuple[str, float]]:
    if not path or not path.exists():
        return {}
    res = {}
    for tc in ET.parse(path).getroot().iter("testcase"):  # noqa: S314
        name = tc.get("name", "").split("[")[0]
        st = (
            "❌"
            if tc.find("failure") is not None or tc.find("error") is not None
            else ("⏭" if tc.find("skipped") is not None else "✅")
        )
        prev = res.get(name)
        res[name] = ("❌" if (prev and prev[0] == "❌") else st, float(tc.get("time", 0)) + (prev[1] if prev else 0))
    return res


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tests", type=Path, default=Path("tests"))
    ap.add_argument("--junit", type=Path)
    ap.add_argument("--out", type=Path, default=Path("docs/tests/catalogue.md"))
    args = ap.parse_args()
    status = junit_status(args.junit)
    total, documented = 0, 0
    L = [
        "# Catalogue des tests",
        "",
        f"_Généré automatiquement le {dt.datetime.now():%d/%m/%Y %H:%M} — ne pas éditer à la main._",
        "",
    ]
    for f in sorted(args.tests.rglob("test_*.py")):
        tree = ast.parse(f.read_text(encoding="utf-8"))
        mm = module_marks(tree)
        tests = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name.startswith("test_")]
        if not tests:
            continue
        L += [
            f"## `{f.as_posix()}`",
            "",
            (ast.get_docstring(tree) or "_Pas de description._").split("\n")[0],
            "",
            "| Statut | Test | Marqueurs | Description | Durée |",
            "|---|---|---|---|---|",
        ]
        for t in tests:
            total += 1
            doc = (ast.get_docstring(t) or "").split("\n")[0]
            documented += bool(doc)
            st, dur = status.get(t.name, ("·", 0.0))
            params = " (paramétré)" if any("parametrize" in ast.unparse(d) for d in t.decorator_list) else ""
            L.append(
                f"| {st} | `{t.name}`{params} | {', '.join(marks_of(t, mm))} | "
                f"{doc or '⚠️ _non documenté_'} | {dur:.2f}s |"
            )
        L.append("")
    L[3:3] = [f"**{total} tests** — {documented} documentés ({documented / max(total, 1):.0%}).", ""]
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text("\n".join(L), encoding="utf-8")
    print(f"Catalogue écrit : {args.out} ({total} tests, {documented} documentés)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
