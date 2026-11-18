# Atelier 4 — L'IA dans la pipeline : génération et revue de PR (1 h 30)

**Module 2** · Intégration CI/CD de l'IA

## Objectif
Faire tourner les outils IA **dans** GitHub Actions en appelant une API de LLM (Claude, d'Anthropic) avec une clé
stockée en **secret** de dépôt :
génération de tests sur chaque PR et commentaire de revue automatique orienté tests.

## Étapes

### 1. Appeler un LLM depuis un workflow (15 min)
Créez `.github/workflows/ai-tests.yml` avec :
```yaml
permissions:
  contents: read
  pull-requests: write  # pour commenter la PR
```
Enregistrez votre clé dans Settings → Secrets and variables → Actions → *New repository secret*,
sous le nom `ANTHROPIC_API_KEY` (jamais dans le dépôt, jamais dans un `echo`).
Premier job : un simple `python ai_tools/llm.py` avec ces variables d'environnement :
```yaml
    env:
      LLM_PROVIDER: anthropic
      LLM_MODEL: claude-haiku-5-5       # modèle économique du cours
      ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
```
Sans secret, `llm.py` échoue avec « Variable ANTHROPIC_API_KEY manquante » ; les autres outils, eux, se
replient sur le moteur offline (le job reste vert : lisez le log pour savoir quel moteur a répondu).
Le job doit installer le SDK : `pip install -r requirements-dev.txt` (ou au minimum `pip install anthropic`).

Variante sans clé ni compte — Ollama sur le runner, avec `LLM_PROVIDER: ollama` (le code ne quitte pas
le runner, mais sur CPU un petit modèle est lent et se trompe souvent) :
```yaml
      - name: Démarrer Ollama et charger le modèle
        run: |
          docker run -d --name ollama -p 11434:11434 ollama/ollama
          timeout 60 bash -c 'until curl -sf localhost:11434/api/tags; do sleep 1; done'
          docker exec ollama ollama pull qwen2.5-coder:1.5b
```
(GitHub Models, qui permettait d'appeler un LLM avec le jeton automatique, a été arrêté le 30 juillet 2026.)

### 2. Génération de tests sur chaque PR (25 min)
- Lancer `ai_tools/generate_tests.py` ; `continue-on-error: true` (un test généré qui échoue est
  un **signal**, pas un blocage).
- Mesurer la couverture **avant / après** ajout des tests générés et l'écrire dans `$GITHUB_STEP_SUMMARY`.
- Publier `tests/generated/` en artefact (l'humain décide de les intégrer ou non).

### 3. Revue de PR par IA (30 min)
- Job `ai-review` avec `fetch-depth: 0` (pour avoir le diff complet).
- `python ai_tools/review_pr.py --base origin/${{ github.base_ref }}`
- Poster le résultat : `gh pr comment <num> --body-file reports/ai-review.md --edit-last`
  (`GH_TOKEN` requis).
- Testez avec une PR piège : ajoutez une fonction qui utilise `float` pour un montant, sans test.

### 4. Discussion : jusqu'où faire confiance ? (20 min)
Par groupe, répondez :
- La revue IA doit-elle pouvoir **bloquer** une PR ? (cf. option `--fail-on-high`)
- Que se passe-t-il si le diff contient un secret ? (avec une API en ligne, le diff part chez le
  fournisseur du modèle ; avec un modèle sur le runner, non — au prix de la qualité et de la durée)
- Coût, quota, latence : que faire si le modèle ne répond pas ou si le quota de la clé est atteint ? (regardez le repli offline du code)
- Comment éviter qu'un contributeur externe déclenche des appels IA sur votre quota ?
  (indice : `pull_request` vs `pull_request_target`, environnements protégés)

## Critères de réussite
- [ ] Le workflow appelle un LLM (log : `moteur : anthropic`, et non `repli sur le moteur offline`)
- [ ] Une PR reçoit un commentaire de revue IA, mis à jour à chaque push
- [ ] Le résumé du run montre la couverture avant/après les tests générés

## Pour aller plus loin
- Comparer Claude, l'API Mistral (`LLM_PROVIDER: mistral`) et un modèle local (`qwen2.5-coder:1.5b` via Ollama) : qualité, durée, coût.
- Équivalent GitLab : job `ia:review-mr` dans `.gitlab-ci.yml` (note de MR via l'API).
