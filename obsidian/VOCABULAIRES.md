## Shift Left
Le **Shift Left** est une approche de développement logiciel qui consiste à **effectuer les tests et les contrôles de qualité le plus tôt possible dans le cycle de développement**, plutôt que d'attendre la fin du projet.

## Hook
Un **hook** est un mécanisme qui permet de déclencher automatiquement une action lorsqu'un événement se produit.
Par exemple :
- **Git** : un hook `pre-commit` lance des vérifications avant un commit.
- **React** : les hooks comme `useState` permettent de gérer l'état d'un composant.
- **WordPress** : les hooks permettent d'exécuter du code lors de certains événements.
- **GitLab** : les webhooks permettent de notifier une application lorsqu'un événement se produit, par exemple un push.
```
git commit -n  "Modification API Identité"```



https://git-scm.com/docs/githooks?utm_source=chatgpt.com


**Forgejo** est une forge logicielle libre et open source qui sert à **héberger, gérer et partager des projets informatiques utilisant Git**.

Concrètement, Forgejo peut remplacer GitHub pour gérer tes projets de développement.

Avec Forgejo, tu peux :

- **Stocker ton code** dans des dépôts Git.
    
**Conserver l'historique** des modifications.
    
- **Travailler à plusieurs** sur un projet.
    
- **Gérer les tâches et les anomalies** avec les _issues_.
    
- **Automatiser les tests et les déploiements** avec Forgejo Actions (CI/CD).
    
- **Héberger ta propre forge** sur un serveur que tu contrôles.
    

### **Exemple avec ton projet API Identité**

Actuellement, tu utilises GitHub pour héberger ton code.

Avec Forgejo, tu pourrais héberger ce même projet sur ton propre serveur et utiliser Forgejo Actions pour automatiser les tests à chaque `push`.

**La différence principale :** GitHub est un service d'hébergement prêt à l'emploi, tandis que Forgejo est un logiciel que tu peux installer et administrer toi-même. Il existe également des services hébergés utilisant Forgejo, comme Codeberg.

Source : [Wikipédia – Forgejo](https://fr.wikipedia.org/wiki/Forgejo?utm_source=chatgpt.com), rubriques « Historique » et « Fonctionnalités ».

Wikipédia



## **Fork (fourche) dans GitHub**

Un **fork** est une copie d'un dépôt GitHub appartenant à une autre personne, créée sur ton propre compte GitHub.

Il permet de **travailler sur un projet existant sans modifier le dépôt original**.








