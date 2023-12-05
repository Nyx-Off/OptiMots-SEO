import requests
from bs4 import BeautifulSoup
import re
import argparse

def recuperer_html(url):
    reponse = requests.get(url)
    reponse.raise_for_status()
    return reponse.text

def enlever_balises_html(texte_html):
    soupe = BeautifulSoup(texte_html, 'html.parser')
    return soupe.get_text()

def compter_alt_manquants(texte_html):
    soupe = BeautifulSoup(texte_html, 'html.parser')
    images = soupe.find_all('img')
    return sum(1 for image in images if not image.has_attr('alt') or not image['alt'])

def compter_occurrences(texte):
    texte = texte.lower()
    texte = re.sub(r'[^\w\s]','', texte)
    mots = texte.split()
    occurrences = {}
    for mot in mots:
        occurrences[mot] = occurrences.get(mot, 0) + 1
    return dict(sorted(occurrences.items(), key=lambda item: item[1], reverse=True))

def enlever_parasites(occurrences, parasites):
    return {mot: occurrences[mot] for mot in occurrences if mot not in parasites}

def charger_parasites(chemin_fichier):
    with open(chemin_fichier, 'r', encoding='utf-8') as fichier:
        parasites = fichier.read().splitlines()
    return parasites

def extraire_valeurs_attribut(texte_html, balise, attribut):
    soupe = BeautifulSoup(texte_html, 'html.parser')
    return [element.get(attribut) for element in soupe.find_all(balise) if element.has_attr(attribut)]

def audit_seo(url, chemin_fichier_parasites):
    html = recuperer_html(url)
    texte_sans_html = enlever_balises_html(html)
    occurrences = compter_occurrences(texte_sans_html)
    parasites = charger_parasites(chemin_fichier_parasites)
    mots_cles = enlever_parasites(occurrences, parasites)

    liens_href = extraire_valeurs_attribut(html, 'a', 'href')
    liens_entrants = [href for href in liens_href if href.startswith(url)]
    liens_sortants = [href for href in liens_href if not href.startswith(url)]

    return {
        'Mots clés': list(mots_cles.items())[:3],  # Affiche les 3 premiers mots clés
        'Nombre de liens entrants': len(liens_entrants),
        'Nombre de liens sortants': len(liens_sortants),
        'Balises alt manquantes': compter_alt_manquants(html)
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Effectuer un audit SEO simple sur une page web.')
    parser.add_argument('url', help='L\'URL de la page à analyser')
    parser.add_argument('fichier_parasites', help='Chemin vers le fichier CSV des mots parasites', default='parasite.csv', nargs='?')
    args = parser.parse_args()

    resultats = audit_seo(args.url, args.fichier_parasites)
    print(resultats)
