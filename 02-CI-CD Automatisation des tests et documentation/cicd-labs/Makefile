.PHONY: install run test unit api e2e visual cov lint perf security docs monitoring
install:      ## Installer les dépendances
	pip install -r requirements-dev.txt && playwright install --with-deps chromium
run:          ## Lancer l'application
	uvicorn minishop.api:app --reload
test:         ## Tous les tests sauf e2e/visual
	pytest -m "not e2e and not visual"
unit:
	pytest -m unit
api:
	pytest -m api
e2e:          ## Nécessite l'appli lancée (make run)
	pytest -m e2e
visual:
	pytest -m visual
cov:
	pytest -m "not e2e and not visual" --cov --cov-report=term-missing --cov-report=html
lint:
	ruff check . && ruff format --check .
perf:         ## Nécessite l'appli lancée
	locust -f tests/perf/locustfile.py --headless -u 20 -r 5 -t 30s --host http://localhost:8000
security:
	bandit -r minishop -q -ll && pip-audit -r requirements.txt   # -ll : bloque à partir de la sévérité moyenne
docs:
	python ai_tools/gen_test_docs.py && mkdocs serve
monitoring:
	docker compose -f monitoring/docker-compose.yml up -d
