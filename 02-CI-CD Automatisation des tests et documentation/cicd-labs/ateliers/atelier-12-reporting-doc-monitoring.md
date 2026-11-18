# Atelier 12 — Reporting, documentation vivante et monitoring des tests (3 h)

**Module 4** · Compétences C20 (documentation), C33 (surveillance des systèmes automatisés)

## Objectif
À chaque pipeline : un rapport de tests interactif, une documentation des tests à jour publiée
automatiquement, des métriques historisées dans Grafana et des alertes en cas de régression.

## Partie A — Rapports interactifs avec Allure (45 min)
1. ```bash
   pytest -m "not e2e and not visual" --alluredir=allure-results
   npm install -g allure-commandline        # nécessite Java ; sinon : docker run frankescobar/allure-docker-service
   allure serve allure-results
   ```
2. Enrichissez 3 tests avec les décorateurs Allure et observez le rapport :
   ```python
   import allure
   @allure.feature("Panier")
   @allure.story("Coupons")
   @allure.severity(allure.severity_level.CRITICAL)
   def test_coupon_welcome10(): ...
       with allure.step("Calculer le devis"): ...
       allure.attach(json.dumps(q.as_dict()), "devis", allure.attachment_type.JSON)
   ```
3. Les **tendances** : Allure garde un historique si l'on recopie `allure-report/history/` dans
   `allure-results/history/` avant de générer. Lancez 3 fois (dont une avec `MINISHOP_BUG=rounding`) et
   observez *Trend* et *Categories*. (Pour info : **Extent Reports** est l'équivalent côté Java/.NET.)

## Partie B — Documentation des tests versionnée et automatique (50 min)
1. **Structurer** : la doc vit dans `docs/` (MkDocs), versionnée avec le code. Complétez
   `docs/strategie-de-test.md` (risques, quality gates, règles IA, flaky, indicateurs).
2. **Une décision = un ADR** : rédigez `docs/adr/0002-...md` pour une décision prise cette semaine
   (ex. Locust plutôt que JMeter en PR, politique de blocage sécurité).
3. **Documentation générée depuis les tests** :
   ```bash
   pytest -m "not e2e and not visual" --junitxml=reports/junit.xml
   python ai_tools/gen_test_docs.py --junit reports/junit.xml
   mkdocs serve        # http://localhost:8000 -> arrêtez d'abord l'appli, ou : mkdocs serve -a localhost:8001
   ```
   Le catalogue liste chaque test, ses marqueurs, sa docstring et son dernier statut.
   Objectif : **100 % des tests documentés** (une docstring = la règle métier vérifiée).
4. **IA pour la documentation** (bonus) : demandez à un LLM de produire une docstring pour chaque test
   non documenté, à partir de son code. Relisez avant de committer.
5. Confluence / Notion : la même page peut y être poussée par API depuis la CI (script `requests`),
   mais la **source de vérité reste le dépôt**.

## Partie C — Monitoring des tests avec Prometheus et Grafana (55 min)
1. `docker compose -f monitoring/docker-compose.yml up -d`
2. Rejouez l'historique simulé pour remplir les graphiques :
   ```bash
   python scripts/simulate_history.py
   python ai_tools/push_metrics.py data/junit-history/run-0[4-6]*.xml --replay --interval 6
   ```
3. Grafana (http://localhost:3000, admin/admin) → dossier *Formation CI/CD* → « Qualité des tests ».
   Repérez la régression des runs 48-51 et le test qui ralentit.
4. Ajoutez un panneau : **nombre de tests en échec par run sur 24 h** et un panneau *Table* des tests
   les plus lents.
5. **Alertes** : lisez `monitoring/alerts.yml`. Vérifiez dans Prometheus (onglet *Alerts*) que
   `TauxDeReussiteEnBaisse` passe en *firing* pendant les runs 48-51 (rejouez l'étape 2 au besoin).
   Pour voir la notification partir, lancez `python scripts/alert_receiver.py` dans un autre terminal :
   Alertmanager y envoie ses webhooks (sans ce récepteur, ses logs affichent « connection refused »,
   c'est attendu). Ajoutez une alerte
   « plus de 2 runs consécutifs en échec ». Routez-la vers un canal (Slack/Teams/mail) dans
   `alertmanager.yml`, ou créez la règle directement dans Grafana Alerting.
6. ELK (pour info) : les logs JSON de l'appli (`MINISHOP_LOG_FILE`) s'ingèrent tels quels dans
   Elasticsearch/Loki ; l'Atelier 5 en fait l'analyse automatique.

## Partie D — Tout assembler dans la pipeline (30 min)
Workflow `quality-report.yml` sur `main` : tests → Allure (avec historique) → catalogue → `mkdocs build`
→ publication **GitHub Pages** (site + `/allure/`) → `push_metrics.py` vers le Pushgateway si le secret
`PUSHGATEWAY_URL` existe. Activez Pages (Settings → Pages → Source : GitHub Actions).

## Critères de réussite
- [ ] Rapport Allure avec features/stories, étapes, pièce jointe et tendance
- [ ] Stratégie de test + 1 ADR rédigés
- [ ] Catalogue des tests généré et publié sur GitHub Pages
- [ ] Tableau de bord Grafana enrichi d'un panneau, une alerte personnalisée qui se déclenche
