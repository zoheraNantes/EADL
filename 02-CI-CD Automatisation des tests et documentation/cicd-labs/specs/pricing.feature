# language: fr
# Spécification fonctionnelle du calcul de panier MiniShop.
# Source d'entrée de l'Atelier 3 : génération de tests par IA.
#
# Grammaire reconnue par le générateur hors-ligne :
#   Étant donné un panier avec <qty> "<produit>" [et <qty> "<produit>" ...]
#   Étant donné un panier vide
#   Quand j'applique le coupon "<CODE>"          (facultatif)
#   Quand je calcule le total
#   Alors le <champ> vaut <montant>               (champ : sous-total | remise | livraison | total)
#   Alors une erreur "<message partiel>" est levée

Fonctionnalité: Calcul du total d'un panier

  Scénario: Panier vide
    Étant donné un panier vide
    Quand je calcule le total
    Alors le total vaut 0.00
    Et la livraison vaut 0.00

  Scénario: Achat simple avec frais de livraison
    Étant donné un panier avec 2 "mug"
    Quand je calcule le total
    Alors le sous-total vaut 25.00
    Et la livraison vaut 4.90
    Et le total vaut 29.90

  Scénario: Livraison offerte à partir de 50 euros
    Étant donné un panier avec 1 "hoodie" et 1 "mug"
    Quand je calcule le total
    Alors la livraison vaut 0.00
    Et le total vaut 56.50

  Scénario: Remise volume dès 10 unités
    Étant donné un panier avec 10 "sticker"
    Quand je calcule le total
    Alors le sous-total vaut 23.28

  Scénario: Coupon de bienvenue
    Étant donné un panier avec 2 "mug"
    Quand j'applique le coupon "WELCOME10"
    Et je calcule le total
    Alors la remise vaut 2.50
    Et le total vaut 27.40

  Scénario: Coupon de bienvenue sous le seuil
    Étant donné un panier avec 1 "mug"
    Quand j'applique le coupon "WELCOME10"
    Et je calcule le total
    Alors la remise vaut 0.00

  Scénario: Coupon de livraison offerte
    Étant donné un panier avec 1 "sticker"
    Quand j'applique le coupon "FREESHIP"
    Et je calcule le total
    Alors la livraison vaut 0.00
    Et le total vaut 2.45

  Scénario: Coupon inconnu
    Étant donné un panier avec 1 "mug"
    Quand j'applique le coupon "NOEL2026"
    Et je calcule le total
    Alors une erreur "Coupon inconnu" est levée

  Scénario: Produit inconnu
    Étant donné un panier avec 1 "licorne"
    Quand je calcule le total
    Alors une erreur "Produit inconnu" est levée

  Scénario: Coupon FIXED5 sur un panier d'au moins 30 euros
    Étant donné un panier avec 3 "mug"
    Quand j'applique le coupon "FIXED5"
    Et je calcule le total
    Alors la livraison vaut 4.90
    Et le total vaut 37.40

  Scénario: Remise volume et coupon WELCOME10
    Étant donné un panier avec 10 "sticker"
    Quand j'applique le coupon "WELCOME10"
    Et je calcule le total
    Alors le sous-total vaut 23.28
    Et la remise vaut 2.33
    Et la livraison vaut 4.90
    Et le total vaut 25.85

  Scénario: Quantité égale à zéro
    Étant donné un panier avec 0 "mug"
    Quand je calcule le total
    Alors une erreur "Quantité hors limites" est levée
