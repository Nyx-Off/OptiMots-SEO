import re

def compter_occurrences(texte):
    # Suppression de la ponctuation et conversion en minuscules
    texte = texte.lower()
    texte = re.sub(r'[^\w\s]','',texte)  # Utilisation d'une expression régulière pour supprimer la ponctuation
    mots = texte.split()
    
    # Comptage des occurrences des mots
    occurrences = {}
    for mot in mots:
        occurrences[mot] = occurrences.get(mot, 0) + 1
    
    # Tri des mots par occurrence
    occurrences_triees = dict(sorted(occurrences.items(), key=lambda item: item[1], reverse=True))
    
    return occurrences_triees

def enlever_parasites(occurrences, parasites):
    # Nettoyage des mots parasites (conversion en minuscules et suppression des caractères spéciaux)
    parasites = set(mot.lower() for mot in parasites)
    return {mot: occurrences[mot] for mot in occurrences if mot not in parasites}

def charger_parasites(fichier):
    with open(fichier, 'r') as file:
        parasites = file.read().splitlines()
    return parasites

# Remplacez 'chemin_vers_votre_fichier_parasite' par le chemin réel de votre fichier 'parasite.csv'
liste_parasites = charger_parasites('parasite.csv')

# Utilisez un texte de votre choix ici
texte_a_analyser = """
Geralt de Riv est une créature mi-humaine mi-magique. 
A la fois mage et guerrier, c'est un mercenaire redoutable, 
un chasseur de monstres dont la réputation n'est plus à faire : c'est le meilleur sorceleur jamais connu. 
Son étrange apparence - de longs cheveux blancs et des yeux nyctalopes - fait de lui un héros solitaire. 
Tueur à gages parfait, il va de ville en ville pour gagner sa vie. 
Il croise sur sa route nombre de personnages pittoresques, qui lui offrent parfois l'amitié ou l'amour. 
Mais Geralt de Riv, armé de sa dague et de son humour caustique, ne cherche qu'une seule chose : retrouver sa part d'humanité perdue.
"""

# Obtenez les occurrences des mots
occurrences_mots = compter_occurrences(texte_a_analyser)

# Filtrez les mots clés
mots_cles = enlever_parasites(occurrences_mots, liste_parasites)

# Imprimez les mots clés pour les voir
print(mots_cles)

