"""Comparaison visuelle de captures d'écran (régression visuelle).

Deux mesures complémentaires :
  * diff pixel (avec tolérance par canal) : % de pixels différents — rapide mais
    sensible à l'anti-aliasing et aux polices ;
  * SSIM (similarité structurelle, proche de la perception humaine) : 1.0 = identique.
    C'est le principe de base des outils « Visual AI » (Applitools, Percy...), qui y
    ajoutent des modèles entraînés à ignorer le bruit (contenu dynamique, rendu).

Produit une image de diff (pixels changés en magenta sur fond atténué).

Usage :
    python ai_tools/visual_diff.py baseline.png current.png --diff diff.png
    # code retour 1 si la différence dépasse les seuils
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from PIL import Image


@dataclass
class VisualResult:
    diff_ratio: float
    ssim: float
    size_mismatch: bool

    def ok(self, max_diff: float, min_ssim: float) -> bool:
        return not self.size_mismatch and self.diff_ratio <= max_diff and self.ssim >= min_ssim


def _gray(a: np.ndarray) -> np.ndarray:
    return a[..., 0] * 0.299 + a[..., 1] * 0.587 + a[..., 2] * 0.114


def ssim(x: np.ndarray, y: np.ndarray, win: int = 8) -> float:
    """SSIM moyen sur fenêtres non chevauchantes (implémentation pédagogique)."""
    c1, c2 = (0.01 * 255) ** 2, (0.03 * 255) ** 2
    h, w = (x.shape[0] // win) * win, (x.shape[1] // win) * win
    xb = x[:h, :w].reshape(h // win, win, w // win, win).swapaxes(1, 2).reshape(-1, win * win)
    yb = y[:h, :w].reshape(h // win, win, w // win, win).swapaxes(1, 2).reshape(-1, win * win)
    mx, my = xb.mean(1), yb.mean(1)
    vx, vy = xb.var(1), yb.var(1)
    cov = ((xb - mx[:, None]) * (yb - my[:, None])).mean(1)
    s = ((2 * mx * my + c1) * (2 * cov + c2)) / ((mx**2 + my**2 + c1) * (vx + vy + c2))
    return float(s.mean())


def compare(baseline: Path, current: Path, diff_out: Path | None = None, tolerance: int = 16) -> VisualResult:
    a = np.asarray(Image.open(baseline).convert("RGB"), dtype=np.float64)
    b = np.asarray(Image.open(current).convert("RGB"), dtype=np.float64)
    if a.shape != b.shape:
        return VisualResult(1.0, 0.0, True)
    changed = (np.abs(a - b) > tolerance).any(axis=2)
    if diff_out:
        out = (a * 0.3 + 178).astype(np.uint8)
        out[changed] = [255, 0, 255]
        diff_out.parent.mkdir(parents=True, exist_ok=True)
        Image.fromarray(out).save(diff_out)
    return VisualResult(float(changed.mean()), ssim(_gray(a), _gray(b)), False)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("baseline", type=Path)
    ap.add_argument("current", type=Path)
    ap.add_argument("--diff", type=Path)
    ap.add_argument("--max-diff", type=float, default=0.001, help="part max de pixels différents")
    ap.add_argument("--min-ssim", type=float, default=0.995)
    args = ap.parse_args()
    r = compare(args.baseline, args.current, args.diff)
    print(f"pixels différents : {r.diff_ratio:.4%} | SSIM : {r.ssim:.4f} | tailles différentes : {r.size_mismatch}")
    return 0 if r.ok(args.max_diff, args.min_ssim) else 1


if __name__ == "__main__":
    sys.exit(main())
