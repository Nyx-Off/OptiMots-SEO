# SEO Audit Application

## Description

Cette application d'audit SEO est un outil de bureau conçu pour aider les utilisateurs à analyser des pages web pour le référencement (SEO). Elle permet d'extraire et d'analyser des données clés telles que les mots-clés, les liens entrants et sortants, et les balises alt manquantes dans les images.

## Fonctionnalités

- **Analyse de Page Web** : Permet d'entrer une URL et d'obtenir des données d'audit SEO détaillées.
- **Éditeur de Mots Clés Parasites** : Permet de personnaliser la liste des mots clés à exclure de l'analyse.
- **Exportation de Rapport** : Les résultats de l'audit peuvent être sauvegardés en format PDF.

## Installation

Pour exécuter cette application, vous aurez besoin de Python et de quelques bibliothèques. Suivez les étapes ci-dessous pour mettre en place l'environnement :

1. **Clonez le dépôt** : `git clone [URL_DU_REPO]`
2. **Installez les Dépendances** : Exécutez `pip install -r requirements.txt` dans le répertoire du projet pour installer les bibliothèques nécessaires.
3. **Assurez-vous que les Fichiers Requis sont dans le Bon Répertoire** :
   - Le dossier `assets` doit être dans le même répertoire que le fichier `main.py`.
   - Le fichier `parasite.csv` (liste de mots clés parasites) doit également se trouver dans le même répertoire que le fichier `main.py`.
4. **Lancez l'Application** : Exécutez `python main.py` (remplacez `main.py` par le nom de votre fichier principal).

## Utilisation

1. **Ouvrez l'Application** : Lancez l'application à partir de votre terminal ou IDE.
2. **Entrez l'URL** : Dans le champ 'Page Cible', entrez l'URL de la page que vous souhaitez analyser.
3. **Spécifiez les Mots-clés et le Nombre Top de Mots-clés** : Si nécessaire, ajoutez des mots-clés spécifiques et le nombre de mots-clés top à analyser.
4. **Exécutez l'Audit** : Cliquez sur le bouton 'Analyser' pour démarrer l'audit SEO.
5. **Consultez les Résultats** : Les résultats seront affichés dans une nouvelle fenêtre où vous pouvez les copier ou les sauvegarder en PDF.
6. **Édition du Fichier Parasite** : 
   - Vous pouvez éditer le fichier `parasite.csv` directement dans le programme. 
   - Le fichier doit contenir un mot clé par ligne.

## Contribution

Les contributions à ce projet sont les bienvenues. Si vous souhaitez contribuer, veuillez forker le dépôt et proposer une pull request avec vos modifications ou nouvelles fonctionnalités.
