# Atelier 7 — Tests visuels et outils « AI-powered » (2 h)

**Module 2** · Automatisation du testing visuel avec l'IA ; Testim, Applitools, Mabl

## Objectif
Détecter automatiquement les régressions d'interface par comparaison d'images, comprendre ce
qu'apporte la « Visual AI » par rapport au diff de pixels, et évaluer les outils du marché.

## Partie A — Régression visuelle maison (60 min)

1. Application lancée (`make run`), puis :
   ```bash
   pytest -m visual -rs          # 1er passage : crée les baselines (skipped)
   pytest -m visual              # 2e passage : compare -> vert
   ```
2. Provoquez des régressions et observez `tests/visual/diff/*.png` :
   | Changement dans `minishop/static/style.css` | Détecté ? | % pixels | SSIM |
   |---|---|---|---|
   | `--accent: #2563eb` (bleu au lieu de vert) | | | |
   | `padding: 12px` → `padding: 14px` sur `#products li` | | | |
   | Police : `font-family: Georgia, serif` | | | |
   | Bouton « Ajouter » masqué (`display:none`) | | | |
3. Lisez `ai_tools/visual_diff.py`. Pourquoi le **SSIM** (calculé ici en niveaux de gris) rate-t-il
   le changement de couleur ? Proposez une correction (SSIM par canal, ou ΔE dans l'espace Lab).
4. **Le problème des baselines** : générez-les sur votre poste, poussez, lancez en CI → échec. Pourquoi ?
   (polices, anti-aliasing, OS). Solution : générer les baselines **dans l'image CI** (job dédié,
   `UPDATE_BASELINES=1`, artefact téléchargé puis commité).
5. Contenu dynamique : ajoutez l'heure dans l'en-tête de la page. Comment éviter les faux positifs ?
   (masquer une zone : `page.screenshot(mask=[page.locator(...)])`)

## Partie B — Outils IA du marché (45 min, par groupes)

Chaque groupe prend un outil, crée un compte d'essai gratuit si possible, et présente en 5 min :
principe, ce que l'IA apporte vraiment, intégration CI, prix, limites, dépendance au fournisseur.

| Outil | Ce que fait l'IA | Piste de démo |
|---|---|---|
| **Applitools Eyes** | Visual AI : ignore le bruit de rendu, compare la mise en page, regroupe les diffs similaires | SDK `eyes-playwright` sur la page d'accueil |
| **Testim** (Tricentis) | Localisateurs « intelligents » auto-réparants, enregistrement de parcours | Enregistrer le parcours d'achat, changer un `id`, rejouer |
| **Mabl** | Tests low-code, auto-healing, détection d'anomalies de performance et visuelles | Parcours d'achat, insights après plusieurs runs |
| Alternatives ouvertes | Playwright `toHaveScreenshot`, BackstopJS, Percy (BrowserStack), Lost Pixel | Comparer à notre outil maison |

Grille de comparaison commune : *détection de vraies régressions*, *taux de faux positifs*,
*effort de maintenance*, *coût*, *données envoyées chez le fournisseur*.

## Partie C — Auto-healing : le principe (15 min)
Changez `data-testid="quote-btn"` en `data-testid="compute-btn"`. Le test E2E casse.
Un outil auto-réparant aurait retrouvé le bouton par son texte, sa position, ses attributs voisins.
Discussion : pourquoi `get_by_role("button", name="Calculer le total")` est-il déjà plus robuste ?
Quel risque si l'outil « répare » un test qui aurait dû échouer ?

## Critères de réussite
- [ ] Baselines en place, au moins 3 régressions provoquées et analysées
- [ ] Le défaut du SSIM en niveaux de gris expliqué
- [ ] Stratégie de baselines en CI décrite
- [ ] Présentation d'un outil du marché avec la grille commune
