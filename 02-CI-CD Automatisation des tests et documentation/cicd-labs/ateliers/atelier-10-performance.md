# Atelier 10 — Tests de performance et de charge (2 h 30)

**Module 3** · Simulation de charge avec JMeter ; monitoring des temps de réponse

## Objectif
Mesurer le comportement de MiniShop sous charge, définir des seuils (SLO) qui font échouer la
pipeline, et surveiller les temps de réponse pendant le test.

## Vocabulaire
- **Test de charge** : charge attendue (ex. 50 utilisateurs) — tient-on les SLO ?
- **Test de stress** : on monte jusqu'à la rupture — où et comment ça casse ?
- **Test d'endurance** : charge moyenne pendant longtemps — fuites mémoire ?
- **p95** : 95 % des requêtes sont plus rapides que cette valeur. On ne pilote **jamais** à la moyenne.

## Partie A — Locust (50 min)
1. Lisez `tests/perf/locustfile.py` (scénario pondéré + SLO : p95 < 300 ms, erreurs < 1 %).
2. Mode interactif : `locust -f tests/perf/locustfile.py --host http://localhost:8000` → http://localhost:8089.
   Montez de 10 à 200 utilisateurs. Où le p95 décroche-t-il ?
3. Injectez une régression : relancez l'appli avec `MINISHOP_BUG=slow`. Le SLO échoue-t-il ?
4. Mode CI :
   ```bash
   locust -f tests/perf/locustfile.py --host http://localhost:8000 --headless -u 50 -r 10 -t 1m \
          --csv reports/perf --html reports/perf.html ; echo "code retour : $?"
   ```

## Partie B — JMeter (50 min)
1. Ouvrez `tests/perf/minishop.jmx` dans l'interface JMeter **pour le lire uniquement**.
   Repérez : Thread Group, valeurs par défaut HTTP, échantillonneurs, assertion de durée.
2. Lancez en **mode non-GUI** (seul mode acceptable en CI) :
   ```bash
   jmeter -n -t tests/perf/minishop.jmx -Jhost=localhost -Jport=8000 -Jusers=20 -Jduration=60 \
          -f -l reports/jmeter.jtl -e -o reports/jmeter-html
   # ou sans installation :
   docker run --rm --network host -v "$PWD":/w -w /w justb4/jmeter:5.5 -n -t tests/perf/minishop.jmx \
          -Jhost=localhost -Jport=8000 -f -l reports/jmeter.jtl -e -o reports/jmeter-html
   ```
   (`-f` écrase les résultats du lancement précédent ; sans lui, JMeter refuse de démarrer au 2e essai.
   Sur Docker Desktop, si `--network host` n'est pas activé dans les réglages, retirez-le et passez
   `-Jhost=host.docker.internal`.)
3. Ajoutez une requête `GET /products/${productId}` alimentée par un **CSV Data Set Config**.
4. Ouvrez le rapport HTML : *Response Times Over Time*, *Percentiles*. Comparez avec Locust.
   Gatling (Scala/Java) et k6 (JS) : mêmes concepts, scénarios en code.

## Partie C — Monitoring pendant le test (30 min)
1. Démarrez la stack : `docker compose -f monitoring/docker-compose.yml up -d`
2. Prometheus scrape `/metrics` de l'appli sur `host.docker.internal:8000`. **Sous Linux (Docker Engine)**,
   l'appli doit écouter sur toutes les interfaces, sinon la cible reste *down* dans
   http://localhost:9090/targets : lancez-la avec `uvicorn minishop.api:app --host 0.0.0.0`
   (ou `docker compose up -d --build`). Dans Grafana (http://localhost:3000, admin/admin),
   tableau « Qualité des tests — MiniShop » : panneaux **latence p95 par route** et **requêtes/s**.
3. Relancez Locust et observez en direct. Requête PromQL du p95 :
   `histogram_quantile(0.95, sum by (le, path) (rate(minishop_http_request_duration_seconds_bucket[1m])))`

## Partie D — Dans la CI (20 min)
Workflow `perf.yml` : déclenché la **nuit** (`schedule`) et à la demande (`workflow_dispatch` avec le
nombre d'utilisateurs en paramètre), pas sur chaque PR (pourquoi ?). Rapports en artefacts.

## Critères de réussite
- [ ] Le point de rupture de MiniShop est mesuré et expliqué
- [ ] Le SLO fait échouer le run avec `MINISHOP_BUG=slow`
- [ ] JMeter exécuté en non-GUI avec rapport HTML
- [ ] Latences visibles dans Grafana pendant un test de charge
