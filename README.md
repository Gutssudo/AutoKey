# Autokey

**Autokey** est un logiciel Python, compatible avec Python 3.12, conçu pour créer des **macros** et automatiser des actions répétitives sur votre clavier. Il est particulièrement utile pour éviter la détection AFK (Away From Keyboard) dans les jeux vidéo, tout en restant flexible et personnalisable pour d'autres usages.

## Fonctionnalités

- **Création de macros personnalisées** : Configurez des séquences de touches à exécuter automatiquement.
- **Simule des frappes clavier** : Simule des pressions et des relâchements de touches.
- **Support de la temporisation** : Ajoutez des délais personnalisés entre chaque action pour un comportement plus réaliste.
- **Exécutable ou script Python** : Le logiciel peut être utilisé en tant qu'exécutable `.exe` ou via le script `main.py` pour les utilisateurs de Python 3.12.
- **Multithreading et Multiprocessing** : Permet l'exécution de plusieurs processus simultanément pour une expérience fluide.
- **Détection de touches** : Démarrez ou arrêtez une macro en fonction d'une touche prédéfinie.
- **Evite la détection AFK** : Idéal pour automatiser des actions simples en jeu et éviter de se faire expulser pour inactivité.



### Prérequis

- **Python 3.12** doit être installé sur votre machine si vous exécutez le fichier `main.py`.
- Installez les dépendances nécessaires avec `pip` :

```bash
pip install -r requirements.txt
```

## Exécution 

### Fichier python
Après avoir installé les prérequis, Vous pouvez exécuter main.py

```bash
python main.py
```

### Fichier executable
Pour l'exécution via le fichier `.exe`, il est inutile d'installer Python ou les dépendances


