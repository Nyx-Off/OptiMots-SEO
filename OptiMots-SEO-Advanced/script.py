import requests
from bs4 import BeautifulSoup
import re
import argparse
import logging
from colorama import init, Fore, Style
import reportlab.lib.pagesizes as ps
from reportlab.pdfgen import canvas
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch


# Initialisation de colorama
init()

# Configuration de la journalisation
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def print_colored(text, color):
    print(color + text + Style.RESET_ALL)

# Fonction pour créer un rapport PDF
def create_pdf_report(data, filename, num_keywords):
    doc = SimpleDocTemplate(filename, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    # Définir de nouveaux styles
    report_title_style = ParagraphStyle(
        'ReportTitle',
        parent=styles['Title'],
        fontSize=18,
        leading=22,
        textColor=colors.darkblue,
        spaceAfter=12,
        alignment=1  # Centre
    )

    report_heading_style = ParagraphStyle(
        'ReportHeading',
        parent=styles['Heading2'],
        fontSize=12,
        leading=14,
        textColor=colors.green,
        spaceAfter=6
    )

    report_body_style = styles['Normal']
    report_body_style.alignment = 1  # Justifié

    # Titre du rapport
    story.append(Paragraph('Rapport d\'Audit SEO', report_title_style))
    story.append(Spacer(1, 12))

    # URL
    story.append(Paragraph('URL analysée:', report_heading_style))
    story.append(Paragraph(data.get('url', ''), report_body_style))
    story.append(Spacer(1, 12))

    # Titre de la page
    story.append(Paragraph('Titre de la page:', report_heading_style))
    story.append(Paragraph(data.get('Title', 'Aucun titre'), report_body_style))
    story.append(Spacer(1, 12))

    # Description Meta
    story.append(Paragraph('Description Meta:', report_heading_style))
    story.append(Paragraph(data.get('Meta Description', 'Aucune description'), report_body_style))
    story.append(Spacer(1, 12))

    # En-têtes
    story.append(Paragraph('En-têtes:', report_heading_style))
    headers = data.get('Headers', {})
    for header, content in headers.items():
        story.append(Paragraph(f'{header.upper()}: {content}', report_body_style))
    story.append(Spacer(1, 12))

    # Mots clés
    story.append(Paragraph('Mots clés principaux:', report_heading_style))
    mots_cles = data.get('Mots clés', [])[:num_keywords]
    for mot, freq in mots_cles:
        story.append(Paragraph(f'{mot}: {freq}', report_body_style))
    story.append(Spacer(1, 12))

    # Liens
    story.append(Paragraph(f'Nombre de liens entrants: {data.get("Nombre de liens entrants", 0)}', report_body_style))
    story.append(Paragraph(f'Nombre de liens sortants: {data.get("Nombre de liens sortants", 0)}', report_body_style))
    story.append(Paragraph(f'Balises alt manquantes: {data.get("Balises alt manquantes", 0)}', report_body_style))
    
    doc.build(story)

def analyser_semantique(html):
    soupe = BeautifulSoup(html, 'html.parser')
    title = soupe.find('title').get_text() if soupe.find('title') else 'Aucun titre'
    meta_description = soupe.find('meta', attrs={'name': 'description'})
    meta_description_content = meta_description['content'] if meta_description and 'content' in meta_description.attrs else 'Aucune description'
    headers = {h.name: h.get_text() for h in soupe.find_all(re.compile('^h[1-6]$'))}
    return title, meta_description_content, headers

def recuperer_html(url):
    try:
        reponse = requests.get(url)
        reponse.raise_for_status()
        return reponse.text
    except requests.RequestException as e:
        logging.error(f'Erreur lors de la récupération de l\'URL {url}: {e}')
        return None

def enlever_balises_html(texte_html):
    soupe = BeautifulSoup(texte_html, 'html.parser')
    return soupe.get_text()

def extraire_valeurs_attribut(texte_html, balise, attribut):
    soupe = BeautifulSoup(texte_html, 'html.parser')
    return [element.get(attribut) for element in soupe.find_all(balise) if element.has_attr(attribut)]

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

def audit_seo(url, chemin_fichier_parasites,num_keywords):
    html = recuperer_html(url)
    if not html:
        return None
    
    texte_sans_html = enlever_balises_html(html)
    occurrences = compter_occurrences(texte_sans_html)
    parasites = charger_parasites(chemin_fichier_parasites)
    mots_cles = enlever_parasites(occurrences, parasites)
    
    title, meta_description, headers = analyser_semantique(html)
    alt_images = extraire_valeurs_attribut(html, 'img', 'alt')
    liens_href = extraire_valeurs_attribut(html, 'a', 'href')
    
    liens_entrants = [href for href in liens_href if href.startswith(url)]
    liens_sortants = [href for href in liens_href if not href.startswith(url)]
    
    logging.info('Audit SEO terminé avec succès')
    return {
        'url': url,
        'Title': title,
        'Meta Description': meta_description,
        'Headers': headers,
        'Mots clés': list(mots_cles.items()),
        'Nombre de liens entrants': len(liens_entrants),
        'Nombre de liens sortants': len(liens_sortants),
        'Balises alt manquantes': sum(1 for alt in alt_images if not alt)
    }

# Utilisation de la fonction audit_seo
# Utilisation de la fonction audit_seo
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Effectuer un audit SEO simple sur une page web.')
    parser.add_argument('url', help='L\'URL de la page à analyser')
    parser.add_argument('fichier_parasites', help='Chemin vers le fichier CSV des mots parasites', default='parasite.csv', nargs='?')
    parser.add_argument('--nmc', '--nombre_mots_cles', type=int, default=3, help='Nombre de mots clés à analyser', dest='nmc')
    parser.add_argument('--pdf', '--generer_pdf', action='store_true', help='Générer un rapport PDF', dest='pdf')
    args = parser.parse_args()

    resultats = audit_seo(args.url, args.fichier_parasites, args.nmc)
    resultats['Mots clés'] = resultats['Mots clés'][:args.nmc]
    
    # Affichage coloré dans la console
    print_colored('Résultats de l\'audit SEO :', Fore.GREEN)
    for key, value in resultats.items():
        if key == 'Mots clés':
            value = value[:args.nmc]  # Utilisez le nombre de mots clés spécifié par l'utilisateur
        print_colored(f'{key}: {value}', Fore.BLUE)
    
    # Générer un rapport PDF si demandé
    if args.pdf:
        sanitized_title = re.sub(r'[^\w]', '_', resultats['Title'])[:50]  # Sanitize pour nom de fichier
        date_str = datetime.now().strftime('%Y%m%d')
        pdf_filename = f'SEO_Audit_{date_str}_{sanitized_title}.pdf'
        create_pdf_report(resultats, pdf_filename, args.nmc)  # Utilisez le nombre de mots clés spécifié
        print_colored(f'Rapport d\'audit SEO créé : {pdf_filename}', Fore.GREEN)
