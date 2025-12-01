#  Bot Discord : Le Choixpeau Magique

Projet de rattrapage - Bot Discord B2

## Description

Ce bot est un assistant Poudlard interactif. Sa fonctionnalité principale est le **Choixpeau Magique**, un système de questionnaire basé sur un **Arbre Binaire** parcouru par l'utilisateur pour déterminer sa Maison (Gryffondor, Serpentard, Serdaigle, Poufsouffle) et lui attribuer le grade correspondant sur le serveur.

Le bot respecte toutes les contraintes techniques imposées :
* Les structures de données (**Piles**, **Arbres**) sont codées à la main (pas de `import queue` ou `import tree`).
* Persistance des données via JSON.

## ⚙️ Installation et Lancement

1. **Prérequis**
   * Python 3.8 ou supérieur.
   * La librairie `discord.py`.
   ```bash
   pip install discord.py

2. **lancement**
    ```bash
    python main.py