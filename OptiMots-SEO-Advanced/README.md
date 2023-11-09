# Outil d'Audit SEO Pro

Ce script Python est un outil d'audit SEO qui fournit un rapport rapide sur les aspects essentiels du référencement d'une page web donnée.

## Fonctionnalités

L'outil analyse les éléments suivants :

- Les occurrences des mots clés dans le texte de la page.
- La présence de balises `alt` sur les images.
- Le nombre de liens internes (entrants) et externes (sortants).
- Le titre de la page, la description meta, et les en-têtes (h1 à h6).

## Installation

Assurez-vous d'avoir Python 3 installé sur votre système. Les dépendances suivantes sont nécessaires :
`pip install requests beautifulsoup4 colorama reportlab`

## Usage

L'outil doit être utilisé directement depuis la ligne de commande :
`python script.py <URL> <chemin_vers_fichier_des_mots_parasites> --nmc <nombre_de_mots_clés> --pdf`

Où :

- `<URL>` est l'URL de la page à analyser.
- `<chemin_vers_fichier_des_mots_parasites>` est le chemin du fichier CSV contenant les mots parasites à exclure.
- `<nombre_de_mots_clés>` est le nombre de mots clés à afficher dans le rapport.
- `--pdf` est une option pour générer un rapport PDF de l'audit.

## Exemple

`python script.py https://www.example.com/path/to/page parasite.csv --nmc 10 --pdf`

Ceci analysera la page spécifiée, exclura les mots du fichier parasite.csv, affichera les 10 mots clés les plus fréquents, et générera un rapport PDF.

## Rapport PDF

Le rapport PDF contiendra une analyse détaillée et est nommé selon le schéma `SEO_Audit_<YYYYMMDD>_<TitreDeLaPage>.pdf`.

## Contributions
Les contributions sont les bienvenues. Si vous souhaitez améliorer le script ou signaler un bug, n'hésitez pas à ouvrir une issue ou une pull request.


## Licence
Ce projet est sous licence MIT.
