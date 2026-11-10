
Date: 01/11/2026
Tags: 
[[Design pattern]]

# Questions


# Notes

Le **design pattern Façade** est un patron de conception structurel qui consiste à fournir une **interface simple et unifiée** vers un **sous-système complexe** (plusieurs classes, modules, bibliothèques). Il agit comme une « façade » qui masque la complexité interne et offre aux clients quelques méthodes claires et faciles à utiliser.

## Intention du pattern

- **Simplifier l’utilisation** d’un ensemble de classes ou d’API compliqué (librairie, framework, sous-système métier).
- **Réduire le couplage** entre le code client et les détails internes du sous-système : le client ne connaît que la façade, pas les classes internes.
- **Centraliser certains scénarios d’usage** fréquents (séquences d’appels répétitives) dans des méthodes de haut niveau.


## Idée en pratique

Sans façade :

- Le client doit instancier plusieurs classes, connaître leur ordre d’appel, gérer les dépendances (ex. `SubsystemA`, `SubsystemB`, `SubsystemC`).

Avec façade :

- Une classe `SystemFacade` expose quelques méthodes comme `initialiser()`, `executerTraitementComplet()`.
- À l’intérieur, `SystemFacade` orchestre les appels vers `SubsystemA`, `SubsystemB`, etc.
- Le client n’a plus à gérer cette complexité.

```java
public class VideoConverterFacade {
    private final VideoReader reader = new VideoReader();
    private final VideoEncoder encoder = new VideoEncoder();
    private final VideoWriter writer = new VideoWriter();

    public void convert(String input, String outputFormat) {
        var video = reader.read(input);
        var encoded = encoder.encode(video, outputFormat);
        writer.write(encoded);
    }
}
```


## Différence avec d’autres patterns

- **Adaptateur (Adapter)** : transforme une interface en une autre interface attendue par le client. La façade, elle, **simplifie** l’accès à un ensemble de classes, sans forcément changer de contrat existant.[^6][^7]
- **Décorateur (Decorator)** : ajoute des comportements à un objet existant sans changer son interface. La façade **masque/agrège** des interfaces multiples derrière une seule.


## Quand l’utiliser

- Quand un module ou une bibliothèque devient **trop complexe à manipuler directement** (nombreux objets, configuration verbeuse).
- Quand on veut **isoler** le reste de l’application d’un framework externe (ORM, moteur de paiement, API tierce) pour faciliter la maintenance ou un futur remplacement.
- Pour **organiser un gros système en sous-systèmes** bien délimités, chacun exposant une façade vers l’extérieur.

# Références

