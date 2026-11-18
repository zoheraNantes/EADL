# Atelier 8 — Tests fonctionnels UI de bout en bout (2 h 30)

**Module 3** · Tests UI avec Selenium, Cypress (et Playwright)

## Objectif
Automatiser les parcours utilisateur de MiniShop, les rendre fiables, et les exécuter dans la CI
sur plusieurs navigateurs avec des traces exploitables en cas d'échec.

## Partie A — Playwright (75 min)

1. Lancer le test fourni : `pytest -m e2e --headed --slowmo 300`
2. Enregistrer un parcours pour démarrer vite :
   ```bash
   playwright codegen http://localhost:8000
   ```
   Le code généré est un **brouillon** : réécrivez-le proprement.
3. Écrire dans `tests/e2e/test_parcours_achat.py` :
   - parcours d'achat : 2 mugs + WELCOME10 → total `27.40` → commande confirmée ;
   - coupon invalide → message d'erreur (`get_by_role("alert")`) ;
   - bouton « Commander » désactivé tant que le panier est vide.
4. Bonnes pratiques à appliquer :
   - localisateurs par **rôle / texte / data-testid**, jamais par XPath ou classe CSS ;
   - assertions **web-first** (`expect(...).to_have_text`) : pas de `time.sleep` ;
   - une fixture `shop` qui ouvre la page ; tests **indépendants** entre eux.
5. Page Object (15 min) : extrayez une classe `ShopPage` (`add(product)`, `apply_coupon(code)`,
   `total()`, `order()`). Les tests deviennent lisibles par le métier.

## Partie B — Selenium, pour comparer (35 min)
```bash
pip install selenium
```
Écrivez `tests/e2e/test_selenium_accueil.py` qui vérifie le titre et ajoute un produit au panier
(Selenium Manager télécharge le driver tout seul). Notez ce qui vous a manqué par rapport à Playwright
(attentes explicites `WebDriverWait`, pas de traces…). Optionnel : la même chose en **Cypress** (JS).

## Partie C — Dans la CI (40 min)
Créez `.github/workflows/e2e.yml` :
- matrice `browser: [chromium, firefox]`, `python -m playwright install --with-deps ${{ matrix.browser }}` ;
- démarrer l'appli en arrière-plan et **attendre** qu'elle réponde :
  `timeout 30 bash -c 'until curl -sf localhost:8000/health; do sleep 1; done'` ;
- `pytest -m e2e --browser ${{ matrix.browser }} --tracing retain-on-failure --video retain-on-failure --output test-results`
- artefact `test-results/` **en cas d'échec** ; ouvrez une trace avec `playwright show-trace trace.zip`
  (ou https://trace.playwright.dev).
- Parallélisation : `pytest -n 2` — attention aux tests qui partagent des données (commandes).

Cassez volontairement l'interface (renommez un `data-testid`) et diagnostiquez **uniquement** avec la trace.

## Critères de réussite
- [ ] 3 parcours E2E verts, sans aucun `sleep`
- [ ] Page Object en place
- [ ] Exécution CI sur 2 navigateurs, traces récupérables en cas d'échec
- [ ] Comparatif Selenium / Playwright (/ Cypress) en 5 lignes

## Pour aller plus loin
- Grilles cloud **BrowserStack / Sauce Labs** : mêmes tests, navigateurs et mobiles réels (essais gratuits).
- Tests d'accessibilité : `pip install axe-playwright-python`.
