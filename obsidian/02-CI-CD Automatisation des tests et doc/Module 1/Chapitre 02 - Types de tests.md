# Chapitre 02 — Types de tests

## 1. Test unitaire

Vérifie une fonction ou une unité de code isolée.

**Exemple :** vérifier qu'une fonction calcule correctement une réduction.

- Très rapide.
    
- Permet de localiser précisément les erreurs.
    

## 2. Test d'intégration

Vérifie que plusieurs composants fonctionnent correctement ensemble.

**Exemple :** vérifier que le calcul du panier fonctionne avec le catalogue de produits.

## 3. Test fonctionnel / API

Vérifie le comportement attendu d'une fonctionnalité.

**Exemple :** envoyer une requête POST à `/cart/quote` et vérifier le montant retourné.

API = Application Programming Interface (interface de programmation d'application).

## 4. Test E2E — End-to-End

Test de bout en bout.

Vérifie un parcours utilisateur complet.

**Exemple :** ajouter des produits au panier, appliquer un coupon et créer une commande.

Ces tests sont généralement plus longs à exécuter.

## 5. Tests non fonctionnels

Vérifient les caractéristiques de qualité de l'application.

Exemples :

- Performance.
    
- Sécurité.
    
- Accessibilité.
    
- Aspect visuel.
    

## 6. Pyramide des tests

**Base : tests unitaires**

- Très nombreux.
    
- Rapides et précis.
    

**Milieu : tests d'intégration et API**

- Moins nombreux.
    
- Vérifient les interactions.
    

**Sommet : tests E2E**

- Peu nombreux.
    
- Réservés aux parcours critiques.
    

## À retenir

- **Unitaire** = une fonction isolée.
    
- **Intégration** = plusieurs composants ensemble.
    
- **API** = comportement d'une fonctionnalité à travers une interface.
    
- **E2E** = parcours complet.
    
- **Non fonctionnel** = qualité, performance, sécurité, accessibilité.
    

La pyramide contient principalement des tests unitaires.