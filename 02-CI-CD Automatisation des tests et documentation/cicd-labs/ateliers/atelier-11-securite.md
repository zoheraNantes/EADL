# Atelier 11 — Tests de sécurité automatisés (2 h 30)

**Module 3** · Compétence C18 (DevSecOps) — OWASP ZAP, analyse des dépendances (Snyk, Dependabot)

## Objectif
Intégrer quatre familles de contrôles de sécurité dans la pipeline et savoir lesquels doivent bloquer.

| Famille | Question | Outil de l'atelier | Équivalents |
|---|---|---|---|
| SAST (code) | Mon code contient-il des motifs dangereux ? | Bandit, règles `S` de ruff | Semgrep, SonarQube, CodeQL |
| SCA (dépendances) | Mes bibliothèques ont-elles des CVE connues ? | pip-audit, Dependabot | Snyk, OWASP Dependency-Check, Renovate |
| Conteneur | Mon image embarque-t-elle des paquets vulnérables ? | Trivy (+ SBOM) | Grype, Docker Scout |
| DAST (appli qui tourne) | L'application exposée est-elle attaquable ? | OWASP ZAP | Burp Suite, Nuclei |

## Partie A — SAST (25 min)
1. `bandit -r minishop` puis `ruff check --select S .`
2. Ajoutez dans `minishop/api.py` une route de debug volontairement dangereuse :
   ```python
   @app.get("/debug/eval")
   def debug(expr: str):
       return {"result": eval(expr)}
   ```
   Les deux outils la détectent-ils ? Avec quelle sévérité ? (Retirez-la ensuite !)
3. Format **SARIF** + onglet *Security* de GitHub : `bandit -r minishop -f sarif -o bandit.sarif`
   puis `github/codeql-action/upload-sarif@v4` (permissions `security-events: write`, et `actions: read`
   si le dépôt est privé ; l'onglet n'existe sur un dépôt privé qu'avec GitHub Code Security).

## Partie B — Dépendances (30 min)
1. `pip-audit -r requirements.txt` → propre ? Ajoutez `jinja2==2.10` dans un fichier test, relancez.
2. **Dependabot** : le fichier `.github/dependabot.yml` est fourni. Activez *Dependabot alerts* et
   *security updates* sur votre fork (Settings → Code security). Observez les PR créées.
3. **Snyk** (compte gratuit) : `npx snyk test --file=requirements.txt` — comparez avec pip-audit.
4. Discussion : Dependabot vs Renovate ; bloquer sur **toute** CVE ou seulement HIGH/CRITICAL avec correctif ?

## Partie C — Image Docker (20 min)
```bash
docker build -t minishop .
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy image minishop
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock -v "$PWD":/out aquasec/trivy \
       image --format cyclonedx --output /out/sbom.cdx.json minishop
```
Changez `python:3.12-slim` en `python:3.12` (image complète) : combien de vulnérabilités en plus ?
Qu'est-ce qu'un **SBOM** et pourquoi les clients (et le Cyber Resilience Act) le demandent-ils ?

## Partie D — DAST avec OWASP ZAP (45 min)
1. Application lancée dans Docker, puis scan **baseline** (passif, quelques minutes) :
   ```bash
   mkdir -p zap && cp security/zap-rules.tsv zap/ && chmod 777 zap
   docker run --rm --network host -v "$PWD/zap":/zap/wrk ghcr.io/zaproxy/zaproxy:stable \
       zap-baseline.py -t http://localhost:8000 -c zap-rules.tsv -r zap-report.html
   ```
2. Lisez `zap/zap-report.html`. Corrigez au moins un avertissement : ajoutez un middleware qui pose
   `X-Content-Type-Options: nosniff` et une `Content-Security-Policy`. Passez la règle de `WARN` à `FAIL`
   dans `security/zap-rules.tsv` : elle protège désormais contre une régression.
3. Scan d'API guidé par le schéma : `zap-api-scan.py -t http://localhost:8000/openapi.json -f openapi`
4. **Burp Suite** (démo formateur) : proxy d'interception, Repeater sur `/cart/quote` — complémentaire
   du scan automatique pour les tests manuels d'intrusion.

## Partie E — Pipeline `security.yml` (10 min)
Assemblez les jobs (voir énoncé de l'Atelier 2 pour la structure). Décidez et justifiez ce qui bloque :

| Contrôle | Sur PR | Sur main | Nocturne |
|---|---|---|---|
| Bandit HIGH | | | |
| pip-audit | | | |
| Trivy HIGH/CRITICAL | | | |
| ZAP baseline | | | |
| ZAP API complet | | | |

## Critères de réussite
- [ ] La route `eval` est détectée par le SAST
- [ ] Dependabot actif et au moins une alerte comprise
- [ ] SBOM généré
- [ ] Un en-tête de sécurité corrigé et verrouillé en `FAIL` dans ZAP
- [ ] Tableau de politique de blocage rempli et justifié
