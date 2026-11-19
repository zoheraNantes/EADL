# ADR 0001 — Playwright pour les tests E2E

- **Statut** : accepté
- **Date** : AAAA-MM-JJ

## Contexte
Il faut automatiser les parcours utilisateur de MiniShop dans la CI, sur Chromium au minimum.

## Options étudiées
| Critère | Selenium | Cypress | Playwright |
|---|---|---|---|
| Langages | Java, Python, JS, C#… | JS/TS | Python, JS/TS, Java, .NET |
| Attente automatique | Non (attentes explicites) | Oui | Oui |
| Multi-navigateurs | Oui (WebDriver) | Chromium, Firefox, WebKit (partiel) | Chromium, Firefox, WebKit |
| Parallélisation | Selenium Grid | Payant (Cloud) / plugins | Natif (workers, xdist) |
| Traces / vidéo | Outils tiers | Oui | Oui (trace viewer) |

## Décision
Playwright (Python), même langage que l'application et les autres tests.

## Conséquences
- Image CI `mcr.microsoft.com/playwright/python` pour des navigateurs identiques partout.
- Les baselines visuelles sont générées dans cette image, jamais sur un poste local.
