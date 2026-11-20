# Chapitre 13 — Réponses sur les outils et frameworks

## 1. Outils CI/CD

1. **GitHub Actions** : automatise les workflows CI/CD dans GitHub.
    
2. **GitLab CI/CD** : automatise les pipelines dans GitLab.
    
3. **Jenkins** : serveur d'automatisation extensible grâce à ses plugins.
    
4. **Azure DevOps** : plateforme Microsoft pour le développement et les pipelines.
    
5. **GitHub Actions** : fichiers YAML dans `.github/workflows/`.
    
6. **GitLab CI/CD** : fichier `.gitlab-ci.yml`.
    
7. **Jenkins** : fichier `Jenkinsfile`, généralement écrit avec la syntaxe de pipeline Groovy.
    
8. **actions/checkout** : récupère le code du dépôt sur le runner.
    
9. **actions/setup-python** : installe ou sélectionne une version de Python pour le job.
    
10. **actions/upload-artifact** : conserve les fichiers produits par un job.
    

## 2. Frameworks de tests

11. **pytest** : framework Python pour les tests automatisés.
    
12. **JUnit 5** : framework de tests pour Java et Kotlin.
    
13. **Selenium** : automatise les navigateurs avec WebDriver.
    
14. **Cypress** : framework de tests Web en JavaScript et TypeScript.
    
15. **Playwright** : framework d'automatisation de navigateurs, avec attentes automatiques et traces.
    
16. **Selenium** : utilise le standard W3C WebDriver.
    
17. **Selenium, Cypress et Playwright** : permettent les tests E2E de navigateur.
    

## 3. Outils et plugins pytest

18. **pytest-cov** : mesure la couverture du code pendant les tests pytest.
    
19. **pytest-xdist** : répartit les tests sur plusieurs workers.
    
20. **pytest-html** : génère des rapports de tests HTML.
    
21. **Fixture** : prépare les ressources nécessaires aux tests.
    
22. **pytest.mark.parametrize** : exécute un même test avec plusieurs jeux de données.
    
23. **pytest -m** : sélectionne les tests selon leurs marqueurs.
    
24. **--strict-markers** : signale comme erreur les marqueurs non déclarés.
    

## 4. Qualité et couverture

25. **Ruff** : analyse et formate le code Python.
    
26. **ESLint** : analyse le code JavaScript et TypeScript.
    
27. **coverage.py** : mesure la couverture du code Python.
    
28. **JaCoCo** : mesure la couverture du code Java.
    
29. **Différence** : Ruff vérifie la qualité du code ; coverage.py mesure le code exécuté par les tests.
    

## 5. Sécurité

30. **pip-audit** : détecte les vulnérabilités connues dans les dépendances Python.
    
31. **Trivy** : analyse notamment les images de conteneurs et les vulnérabilités.
    
32. **Snyk** : détecte des vulnérabilités dans les dépendances et d'autres composants logiciels.
    
33. **Différence** : l'analyse du code recherche des problèmes dans le code écrit ; l'analyse des dépendances recherche des vulnérabilités dans les bibliothèques utilisées.
    

## 6. Performance

34. **Locust** : outil de tests de charge utilisant des scénarios Python.
    
35. **JMeter** : outil de tests de charge et de performance.
    
36. **p95** : 95e percentile ; 95 % des mesures sont inférieures ou égales à cette valeur.
    

## 7. Conteneurs et environnements

37. **Docker** : construit et exécute des applications dans des conteneurs.
    
38. **Docker Compose** : définit et exécute plusieurs services conteneurisés.
    
39. **Kubernetes** : orchestre le déploiement et la gestion des conteneurs.
    
40. **Health Check** : vérifie qu'un service fonctionne ou est prêt.
    
41. **Conteneur en CI/CD** : permet d'utiliser un environnement isolé et reproductible.
    

## 8. Rapports et automatisation

42. **JUnit XML** : format de rapport des résultats de tests.
    
43. **Allure** : outil de génération et de consultation de rapports de tests.
    
44. **if: always()** : permet de publier les rapports même si les tests ont échoué, sous réserve des conditions d'exécution du job.
    
45. **$GITHUB_STEP_SUMMARY** : permet d'afficher un résumé Markdown dans GitHub Actions.
    
46. **Artefact** : fichier conservé après un job. **Cache** : données réutilisées pour accélérer les jobs suivants.
    
47. **Branch Protection** : impose des conditions avant de modifier ou fusionner du code dans une branche protégée.
    

## 9. Outils et technologies complémentaires

48. **Git** : système de gestion de versions du code source.
    
49. **YAML** : format de données utilisé pour configurer les pipelines.
    
50. **FastAPI** : framework Python utilisé pour développer l'API MiniShop.
    
51. **Ollama** : permet d'exécuter des modèles d'intelligence artificielle localement.
    
52. **API Claude** : interface permettant à une application d'utiliser les modèles Claude d'Anthropic.
    
53. **pip** : gestionnaire de paquets Python.
    
54. **venv** : crée un environnement Python isolé pour les dépendances d'un projet.
    
55. **Make** : outil qui exécute des tâches définies dans un `Makefile`, par exemple lancer l'application ou les tests.
    

---

## Mémo — Reconnaître rapidement les outils

- **CI/CD** : GitHub Actions, GitLab CI/CD, Jenkins, Azure DevOps.
    
- **Tests Python** : pytest.
    
- **Tests Java** : JUnit 5.
    
- **Tests navigateur** : Selenium, Cypress, Playwright.
    
- **Plugins pytest** : pytest-cov, pytest-xdist, pytest-html.
    
- **Qualité du code** : Ruff, ESLint.
    
- **Couverture** : coverage.py, JaCoCo.
    
- **Sécurité** : pip-audit, Trivy, Snyk.
    
- **Performance** : Locust, JMeter.
    
- **Conteneurs** : Docker, Docker Compose, Kubernetes.
    
- **Rapports** : JUnit XML, Allure.
    
- **Automatisation GitHub** : checkout, setup-python, upload-artifact.
    
- **IA** : Ollama, API Claude.
    
- **Application du TP** : FastAPI.
    
- **Gestion des versions** : Git.
    
- **Configuration** : YAML.
    
- **Environnement Python** : pip, venv.
    
- **Exécution des tâches** : Make.