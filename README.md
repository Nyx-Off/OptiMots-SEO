## OptiMots-SEO

Ce projet contient un script Python qui effectue un audit SEO de base sur une page web donnée. L'audit inclut le comptage des mots-clés (en excluant les mots parasites), l'identification des liens entrants et sortants, ainsi que la vérification de la présence des attributs alt dans les images.

## Fonctionnalités

- Comptage des occurrences de mots-clés dans le texte d'une page web.
- Filtrage des mots parasites à l'aide d'une liste personnalisable.
- Extraction des attributs `alt` des balises `img` et `href` des balises `a`.
- Distinction entre les liens internes (entrants) et externes (sortants).
- Compte des balises `alt` manquantes pour améliorer l'accessibilité.

## Prérequis

Pour exécuter ce script, vous aurez besoin de Python 3.x et des bibliothèques suivantes :

- `requests`
- `beautifulsoup4`

Vous pouvez les installer en utilisant `pip` :
pip install requests beautifulsoup4


## Utilisation
Pour utiliser le script, clonez ce dépôt et exécutez le fichier script.py en passant l'URL de la page à analyser et le chemin vers le fichier CSV contenant les mots parasites.
Assurez-vous de mettre à jour le chemin du fichier parasite.csv dans le script pour qu'il corresponde à votre configuration.

## Exemple de résultat
Un exemple de sortie du script pourrait ressembler à ceci :

{'Mots clés': [('campus', 27), ('date', 22), ('lire', 22)], 'Nombre de liens entrants': 42, 'Nombre de liens sortants': 176, 'Balises alt manquantes': 17}

Cela indiquerait les principaux mots-clés identifiés, le nombre de liens internes et externes, ainsi que les balises d'image alt manquantes.

## Licence
Ce projet est distribué sous la licence MIT.
