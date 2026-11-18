
## **MÉMO – Démarrer une application avec Docker et Nginx**

### **1. Principe : ne conserver que le nécessaire**

Lorsqu'on déploie une application, on cherche à utiliser une **image Docker minimale**, contenant uniquement ce qui est nécessaire à son exécution.

- **Pendant le développement** : on utilise les outils de compilation, les dépendances de développement et les outils de test.
    
- **En production** : on conserve uniquement les fichiers et les dépendances nécessaires au fonctionnement de l'application.
    

**Objectif :** réduire la taille de l'image Docker, limiter les vulnérabilités potentielles et faciliter le déploiement.

### **2. Utiliser Nginx**

**Nginx** est un serveur web qui permet notamment de distribuer des fichiers statiques (HTML, CSS, JavaScript).

Pour une application front-end, deux possibilités :

- **Nginx installé sur un serveur** : copier les fichiers de l'application dans le répertoire servi par Nginx.
    
- **Nginx dans un conteneur Docker** : créer une image contenant Nginx et les fichiers de l'application.
    

Dans l'image Docker officielle Nginx, les fichiers statiques sont généralement placés dans :

```
/usr/share/nginx/html
```

### **3. Construire et démarrer l'application**

Pour une application front-end nécessitant une compilation :

1. **Construire l'application** : générer les fichiers HTML, CSS et JavaScript destinés à la production.
    
2. **Préparer l'image Docker** : utiliser une image Nginx légère.
    
3. **Copier les fichiers générés** dans le répertoire de Nginx.
    
4. **Démarrer le conteneur** : Docker lance Nginx, qui sert les fichiers au navigateur.
    
5. **Vérifier le fonctionnement** : accéder à l'application et effectuer un Smoke Test.
    

### **4. Utiliser un build multi-stage**

Un **build multi-stage (construction en plusieurs étapes)** permet de séparer la construction de l'application de son exécution.

- **Étape 1 – Build** : installer les outils et dépendances nécessaires pour construire l'application.
    
- **Étape 2 – Runtime** : conserver uniquement les fichiers générés et le serveur nécessaire pour les exécuter.
    

Ainsi, les outils de compilation ne sont pas présents dans l'image finale.

### **À retenir**

**Développement → Build → Image minimale → Conteneur → Application accessible**

Permet de  **ne pas embarquer inutilement les outils de développement dans l'image de production**.

Attention : Nginx peut servir directement une application front-end statique, mais une application Python, Java ou Node.js avec une logique côté serveur nécessite également un environnement d'exécution adapté.
