# Atelier 0 — Installation du poste (30 min, lundi 9h)

## Objectif
Avoir un poste prêt pour toute la semaine : dépôt forké, environnement Python, appli qui tourne.

## Prérequis
- Compte GitHub (gratuit)
- Git, Python 3.11+, VS Code (ou PyCharm), Docker Desktop / Docker Engine
- Navigateur Chrome ou Firefox

## Étapes

1. **Forker** le dépôt du formateur sur votre compte GitHub, puis le cloner :
   ```bash
   git clone git@github.com:<vous>/cicd-ia-labs.git && cd cicd-ia-labs
   git checkout -b <prenom>
   ```
2. **Environnement virtuel** :
   ```bash
   python -m venv .venv
   source .venv/bin/activate          # Windows : .venv\Scripts\activate
   pip install -r requirements-dev.txt
   python -m playwright install --with-deps chromium   # Windows/Mac : sans --with-deps
   ```
3. **Lancer l'application** : `make run` (ou `uvicorn minishop.api:app --reload`)
   - Boutique : http://localhost:8000
   - Documentation OpenAPI : http://localhost:8000/docs
4. **Lancer les tests** fournis : `pytest -m "not e2e and not visual"` → 5 tests verts.
5. **Activer les GitHub Actions** sur votre fork (onglet *Actions* → « I understand… enable »).
6. **Accès IA (pour le Module 2)** — au choix :
   - *Anthropic / Claude* (recommandé) : le formateur vous fournit une clé d'API à quota limité, puis
     `export LLM_PROVIDER=anthropic ANTHROPIC_API_KEY=<clé>` (ne la committez jamais, ne la partagez pas)
   - *Mistral* (API en ligne ; clé à créer sur https://console.mistral.ai) : `export LLM_PROVIDER=mistral MISTRAL_API_KEY=<clé>`
   - *Ollama* (100 % local, sans compte ni clé) : installez Ollama (https://ollama.com/download
     ou `docker run -d -p 11434:11434 --name ollama ollama/ollama`), puis
     `ollama pull qwen2.5-coder:1.5b` (~1 Go ; avec Docker : `docker exec ollama ollama pull qwen2.5-coder:1.5b`)
     et `export LLM_PROVIDER=ollama`. Machine puissante (16 Go de RAM ou GPU) : `ollama pull qwen2.5-coder:7b`
     puis `export LLM_MODEL=qwen2.5-coder:7b` pour de meilleurs résultats. Le modèle 1.5b sur CPU est lent
     (plusieurs minutes pour un fichier de tests) et se trompe souvent : c'est un bon sujet d'analyse.
   - Aucun accès : `LLM_PROVIDER=offline` (par défaut) — les outils utilisent un moteur simulé.
   Vérification : `python ai_tools/llm.py`
   (GitHub Models, l'accès gratuit des sessions précédentes, a été arrêté par GitHub le 30 juillet 2026.)

## Critères de réussite
- [ ] La boutique s'affiche, `/docs` aussi
- [ ] `pytest` passe
- [ ] Les Actions sont activées sur le fork

## Plan du dépôt
```
minishop/        application FastAPI (prix, catalogue, API, page web)
tests/           unit / api / e2e / visual / perf / generated
specs/           spécifications en langage naturel (entrée de l'IA)
ai_tools/        outils IA & ML (génération, revue, anomalies, risque, visuel, docs, métriques)
scripts/         simulation d'historique de CI pour les ateliers ML
monitoring/      Prometheus + Pushgateway + Grafana + Alertmanager (docker compose)
docs/            documentation MkDocs (docs-as-code)
security/        règles OWASP ZAP
ateliers/        les énoncés
```
