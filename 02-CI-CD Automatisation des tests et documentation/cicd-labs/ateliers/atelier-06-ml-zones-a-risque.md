# Atelier 6 — Machine learning : prédire les zones à risque et prioriser les tests (2 h 30)

**Module 2** · Apprentissage à partir des erreurs, prédiction des zones à risque, analyse des métriques

## Objectif
Entraîner un modèle qui estime, pour un changement de code, la probabilité de casser la CI,
puis s'en servir pour **lancer d'abord les tests les plus susceptibles d'échouer** (*fail fast*).

## Données
`data/git-history.csv` (généré par `scripts/simulate_history.py`) : une ligne = un fichier modifié
dans un commit, avec `broke_ci` = 1 si ce commit a cassé la pipeline.

## Étapes

### 1. Explorer les données (25 min)
Dans un notebook ou un script :
```python
import pandas as pd            # pip install pandas
df = pd.read_csv("data/git-history.csv")
df.broke_ci.mean()                                   # taux de casse global
df.groupby("file").broke_ci.mean().sort_values()    # par fichier
df.groupby("author").broke_ci.mean()                # par auteur (attention à l'usage RH !)
```
Formulez 3 hypothèses (ex. « les gros commits cassent plus »). Vérifiez-les.

### 2. Entraîner et évaluer (30 min)
```bash
python ai_tools/risk_model.py train data/git-history.csv
```
- Pourquoi une **validation temporelle** (passé → futur) et pas un découpage aléatoire ?
- L'exactitude est de 83 %… comme la référence naïve « ça ne casse jamais ». Que vaut vraiment le modèle ?
  Regardez **l'AUC** et le **rappel** sur la classe « casse ».
- Lisez `featurize()` : pourquoi les variables historiques sont-elles calculées *avant* chaque ligne ?
  (notion de **fuite de données**)

### 3. Améliorer le modèle (35 min)
Essayez, et notez AUC + rappel « casse » :
| Variante | AUC | Rappel casse | Précision casse |
|---|---|---|---|
| Défaut | | | |
| `class_weight="balanced"` | | | |
| Seuil de décision 0.3 au lieu de 0.5 | | | |
| `RandomForestClassifier` | | | |
| Nouvelle variable (ex. `lines_added + lines_deleted`, jour de la semaine…) | | | |
Quelle variante choisir si un faux positif coûte 2 min de tests et un faux négatif 1 h de débogage ?

### 4. Prioriser les tests (25 min)
```bash
python ai_tools/risk_model.py predict --files minishop/pricing.py minishop/static/style.css
cat reports/tests_to_run.txt
```
Dans la CI (voir `TEST_MAP` dans le script) :
```yaml
- run: python ai_tools/risk_model.py predict --git-diff origin/${{ github.base_ref }}
- run: pytest -x -m "not e2e and not visual" $(cat reports/tests_to_run.txt)   # d'abord les tests ciblés, échec rapide
- run: pytest -m "not e2e and not visual"                                      # puis la suite complète
```
(Le filtre `-m` évite de lancer les tests navigateur sans application démarrée. Attention : si tous les
tests ciblés sont désélectionnés — PR purement CSS —, pytest renvoie le code 5 « aucun test » : à tolérer.)
Remplacer `TEST_MAP` (manuelle) par une table déduite de la **couverture** : quels tests exécutent quel
fichier ? (indice : `pytest --cov --cov-context=test` puis `coverage json --show-contexts`)

### 5. Analyser les métriques de test (25 min)
Construisez un tableau de bord texte (ou un notebook) qui croise pour chaque module :
couverture, score de mutation (Atelier 3), nombre d'échecs dans l'historique, risque prédit.
Où investir en priorité l'effort de test la semaine prochaine ? Justifiez.

## Critères de réussite
- [ ] Le modèle est entraîné, évalué correctement (AUC, rappel), et le piège de l'exactitude expliqué
- [ ] Au moins 2 variantes comparées, choix argumenté par le coût des erreurs
- [ ] La sélection de tests par risque tourne dans un workflow de PR
- [ ] Recommandation écrite d'investissement de test

## Éthique & limites (à discuter)
- Un modèle « par auteur » peut devenir un outil de surveillance : à proscrire en évaluation individuelle.
- Le modèle apprend le passé : un nouveau module n'a pas d'historique (démarrage à froid).
- Ne jamais **supprimer** des tests sur la seule foi du modèle : on réordonne, on ne retire pas.
