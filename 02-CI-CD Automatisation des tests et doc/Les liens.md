
Framework pre-commit : https://pre-commit.com/


# Trivy – Analyse de sécurité

**Trivy** est un outil d'analyse de sécurité qui permet de détecter des vulnérabilités connues dans une application.

Documentation : [https://github.com/aquasecurity/trivy-action](https://github.com/aquasecurity/trivy-action)

**À quoi sert Trivy ?**

- **Dépendances Python** : détecter les bibliothèques présentant des vulnérabilités connues.
    
- **Images Docker** : détecter les vulnérabilités dans les logiciels présents dans les images.
    
- **Configurations** : identifier certaines mauvaises configurations de sécurité.
    

**Exemple concret :** si MiniShop utilise une bibliothèque Python présentant une faille de sécurité connue, Trivy peut la signaler.

**Intégration dans GitHub Actions**

Trivy Action permet d'exécuter automatiquement Trivy dans un pipeline CI (intégration continue), sans installation manuelle sur le PC.

Dans notre pipeline :

- `scan-type: fs` : analyse les fichiers du projet.
    
- `scan-ref: .` : analyse le répertoire courant.
    
- `severity: HIGH,CRITICAL` : cible les vulnérabilités élevées et critiques.
    
- `exit-code: '0'` : ne fait pas échouer le job si des vulnérabilités sont détectées.
    

**Attention :** la configuration actuelle analyse les fichiers du projet, mais pas directement l'image Docker construite.

**À retenir :** Ruff vérifie la qualité du code, Pytest vérifie son fonctionnement et Trivy recherche des problèmes de sécurité connus.

https://www.zaproxy.org/


[Checkov](https://www.checkov.io/) est un ==outil open-source d'analyse statique du code (SAAC) et de vérification de la conformité pour l'**Infrastructure as Code (IaC)**==, créé par [Bridgecrew](https://github.com/bridgecrewio/checkov) (intégré à Prisma Cloud / Palo Alto Networks). [[1](https://www.checkov.io/), [2](https://github.com/bridgecrewio/checkov)]


**BrowserStack** est une plateforme de test qui permet aux développeurs de vérifier qu'un site web ou une application fonctionne correctement sur différents **navigateurs, systèmes d'exploitation et appareils**.

Par exemple, tu développes ton application sur Ubuntu avec Chrome. Elle fonctionne chez toi, mais est-ce qu'elle fonctionne aussi sur Safari avec un iPhone ou sur Edge avec Windows ?

BrowserStack permet de faire ces vérifications sans posséder physiquement tous ces appareils.

### **À quoi sert BrowserStack ?**

- **Tests de compatibilité** : Chrome, Firefox, Safari, Edge.
    
- **Tests sur mobiles** : iPhone, Android, tablettes.
    
- **Tests responsive** : vérifier l'affichage sur différentes tailles d'écran.
    
- **Tests automatisés** : exécuter des tests avec Selenium ou Playwright.
    
- **Intégration CI/CD** : lancer certains tests automatiquement dans un pipeline GitHub Actions.
https://www.browserstack.com/


**Création site web avec fichier .md**
 **Zensical**, un outil qui permet de créer un site web de documentation à partir de fichiers Markdown (`.md`).
Documentation officielle : [Zensical](https://zensical.org/?utm_source=chatgpt.com).


https://www.conventionalcommits.org/en/v1.0.0/


C EST QUOI commitizen-tools.gituhub.io/commitizen/config
**Commitizen** est un outil qui aide les développeurs à rédiger des messages de commit Git de manière standardisée.

[Documentation officielle de Commitizen — Configuration](https://commitizen-tools.github.io/commitizen/config/?utm_source=chatgpt.com)


**OpenSpec** est un outil open source qui permet de **définir ce qu'un logiciel doit faire avant de demander à une intelligence artificielle (IA) de le développer**.
https://github.com/Fission-AI/OpenSpec


**Cucumber**, utilise le langage **Gherkin** pour écrire des spécifications fonctionnelles sous forme de scénarios.

- **Gherkin** : langage pour écrire les spécifications avec _Given, When, Then_ (Étant donné, Quand, Alors).
    
- **Cucumber** : outil pour exécuter ces scénarios comme des tests.
    
- **OpenSpec** : outil pour organiser les spécifications et guider le développement avec l'IA.




