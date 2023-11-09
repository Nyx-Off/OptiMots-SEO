# Outil d'Audit SEO Simple

Ce dépôt contient un script Python conçu pour effectuer un audit SEO de base sur une page web. Cet outil est utile pour les webmasters et les spécialistes du SEO qui souhaitent obtenir un aperçu rapide des éléments SEO fondamentaux d'une page.

## Fonctionnalités

L'outil d'audit SEO analyse une page web et fournit les informations suivantes :

- **Mots clés** : Liste les trois mots les plus fréquents trouvés sur la page.
- **Liens entrants** : Compte le nombre de liens internes pointant vers d'autres pages du même domaine.
- **Liens sortants** : Compte le nombre de liens qui pointent vers des domaines externes.
- **Balises alt manquantes** : Dénombre les images qui manquent d'une description `alt`, ce qui est essentiel pour l'accessibilité et le référencement.

## Prérequis

Pour exécuter ce script, vous aurez besoin de Python 3 ainsi que des bibliothèques `requests` et `beautifulsoup4`.

Installez les dépendances avec `pip` :
`pip install requests beautifulsoup4`

## Utilisation
Le script peut être exécuté avec une URL et un chemin vers un fichier CSV contenant les mots parasites. Par exemple :
`python script.py https://www.example.com/path parasite.csv`


Le fichier CSV des mots parasites doit contenir un mot par ligne, comme suit :

`le
la
et
en
à
il`

## Résultats
L'exécution du script affichera dans la console un dictionnaire contenant les résultats de l'audit :


`
{
  "Mots clés": [("exemple", 10), ("audit", 8), ("seo", 6)],
  "Nombre de liens entrants": 5,
  "Nombre de liens sortants": 15,
  "Balises alt manquantes": 2
}
`

## Licence

Ce projet est ouvert sous licence MIT.
