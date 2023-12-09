import os
import re
import requests
import tkinter as tk
from bs4 import BeautifulSoup
from tkinter import PhotoImage, Canvas
from tkinter import filedialog, messagebox, scrolledtext,ttk
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

class SEOAuditApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Audit SEO")
        self.geometry("802x346")  # Taille spécifiée dans le design
        self.configure(bg="#EBF3FF")
        self.main_interface()
        self.current_window = None
        self.iconbitmap("assets/frame0/icone.ico")

    def hide_main_window(self):
        self.withdraw()

    def main_interface(self):
        #chemin d'accès aux assets
        assets_path = "assets/frame0"

        # Création d'un canvas pour l'arrière-plan
        self.canvas = Canvas(
            self,
            bg="#EBF3FF",
            height=346,
            width=802,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.pack()

        url_label = self.canvas.create_text(95, 85, anchor="nw", text="Page Cible", fill="#000000", font=("Helvetica", 10))
        keywords_label = self.canvas.create_text(485, 85, anchor="nw", text="Mots-clés (séparés par une virgule)", fill="#000000", font=("Helvetica", 10))

        # Création des champs d'entrée avec des images d'arrière-plan
        self.entry_image_1 = PhotoImage(file=os.path.join(assets_path, "entry_1.png"))
        self.entry_bg_1 = self.canvas.create_image(215.5, 125.0, image=self.entry_image_1)
        self.url_entry = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
        self.url_entry.place(x=93.0, y=107.0, width=245.0, height=36.0)
        self.url_entry.bind("<Return>", lambda event: self.run_audit())

        self.entry_image_2 = PhotoImage(file=os.path.join(assets_path, "entry_2.png"))
        self.entry_bg_2 = self.canvas.create_image(605.5, 125.0, image=self.entry_image_2)
        self.keywords_entry = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
        self.keywords_entry.place(x=483.0, y=107.0, width=245.0, height=36.0)
            
        self.top_keywords_label = self.canvas.create_text(93, 150, anchor="nw", text="Nombre de mots-clés dans le top", fill="#000000", font=("Helvetica", 10))
        self.entry_bg_3 = self.canvas.create_image(215.5, 190.0, image=self.entry_image_1)
        self.top_keywords_entry = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
        self.top_keywords_entry.place(x=93.0, y=180.0, width=245.0, height=20.0)

        # Création des boutons avec des images d'arrière-plan
        self.button_image_1 = PhotoImage(file=os.path.join(assets_path, "run_btn.png"))
        self.analyze_button = tk.Button(self, image=self.button_image_1, borderwidth=0, command=self.run_audit, relief="flat")
        self.analyze_button.place(x=336.0, y=240.0, width=130.0, height=35.0)

        self.button_image_2 = PhotoImage(file=os.path.join(assets_path, "edit_btn.png"))
        self.edit_parasites_button = tk.Button(self, image=self.button_image_2, borderwidth=0, command=self.edit_parasites, relief="flat")
        self.edit_parasites_button.place(x=279.0, y=290.0, width=243.0, height=35.0)

    def result_interface(self, resultats):
        assets_path = "assets/frame0"

        self.hide_main_window()
        if self.current_window:
            self.current_window.destroy()

        # Créer une nouvelle fenêtre secondaire et la définir comme la fenêtre actuelle
        self.current_window = tk.Toplevel(self,bg="#EBF3FF")
        self.current_window.iconbitmap("assets/frame0/icone.ico")
        self.current_window.title("Résultats de l'Audit SEO")
        self.current_window.geometry("800x400")
        
        def format_results(resultats):
            if not resultats:  # Vérifie si la liste est vide
                return "N/A"
            return ' | '.join([f"{mot}: {occurrence}" for mot, occurrence in resultats])
 
         # Formattez la sortie des mots clés pour l'insertion dans le Treeview
        mots_cles_utilisateur_formatte = format_results(resultats['Mots clés utilisateur'].items())
        top_mots_cles_formatte = format_results(resultats['Top mots clés'])

        # Utilisation de Treeview pour afficher les résultats
        tree = ttk.Treeview(self.current_window)
        tree["columns"] = ("one", "two")
        tree.column("#0", width=270, minwidth=270, stretch=tk.NO)
        tree.column("one", width=270, minwidth=270, stretch=tk.NO)

        tree.heading("#0",text="Paramètre",anchor=tk.W)
        tree.heading("one", text="Valeur", anchor=tk.W)

        # Insertion des données
        tree.insert("", 1, text="Mots clés utilisateur", values=(mots_cles_utilisateur_formatte, ""))
        tree.insert("", 2, text="Top mots clés", values=(top_mots_cles_formatte, ""))
        tree.insert("", 3, text="Nombre de liens entrants", values=(resultats['Nombre de liens entrants'], ""))
        tree.insert("", 4, text="Nombre de liens sortants", values=(resultats['Nombre de liens sortants'], ""))
        tree.insert("", 5, text="Balises alt manquantes", values=(resultats['Balises alt manquantes'], ""))

        tree.pack(side=tk.TOP, fill=tk.X)

        # Ajouter la possibilité de copier le contenu des cellules
        tree.bind("<Double-1>", lambda event: self.on_double_click(tree, event))
        tree.bind("<Button-3>", lambda event: self.on_right_click(tree, event))

        # Bouton pour sauvegarder le rapport
        self.save_button_image = PhotoImage(file=os.path.join(assets_path, "save2_btn.png"))
        save_button = tk.Button(self.current_window, image=self.save_button_image, command=lambda: self.save_results_to_pdf(resultats), borderwidth=0, relief="flat")
        save_button.pack(padx=50, pady=30)
        
        self.retour_button_image = PhotoImage(file=os.path.join(assets_path, "back_btn.png"))
        retour_button = tk.Button(self.current_window, image=self.retour_button_image, command=self.back_menu, borderwidth=0, relief="flat")
        retour_button.pack(padx=50, pady=0)
        
        self.current_window.protocol("WM_DELETE_WINDOW", self.quit_app)

    def parasites_interface(self):
        assets_path = "assets/frame0"

        self.hide_main_window()  # Cache la fenêtre principale
        if self.current_window:  # Ferme la fenêtre actuelle si elle est ouverte
            self.current_window.destroy()

        self.current_window = tk.Toplevel(self,bg="#EBF3FF")
        self.current_window.iconbitmap("assets/frame0/icone.ico")
        self.current_window.title("Éditeur de mots clés parasites")
        self.current_window.geometry("600x550")

        # Champ de texte pour l'édition
        self.parasites_text = scrolledtext.ScrolledText(self.current_window, undo=True)
        self.parasites_text.pack(expand=True, fill='both')

        # Charger et afficher le contenu actuel du fichier
        current_content = load_stopwords('parasite.csv')
        self.parasites_text.insert(tk.INSERT, "\n".join(current_content))

        # Bouton pour sauvegarder
        self.save_parasites_button_image = PhotoImage(file=os.path.join(assets_path, "save_btn.png"))
        save_button = tk.Button(self.current_window, image=self.save_parasites_button_image, command=lambda: self.save_parasites(self.current_window), borderwidth=0, relief="flat")
        save_button.pack(side=tk.LEFT, padx=10, pady=10)

        # Bouton pour fermer sans sauvegarder
        self.close_button_image = PhotoImage(file=os.path.join(assets_path, "back_btn.png"))
        close_button = tk.Button(self.current_window, image=self.close_button_image, command=self.back_action, borderwidth=0, relief="flat")
        close_button.pack(side=tk.RIGHT, padx=10, pady=10)
        
        self.current_window.protocol("WM_DELETE_WINDOW", self.quit_app)

    def run_audit(self):
        url = self.url_entry.get().strip().replace(" ", "")
        if not self.validate_url(url):
            messagebox.showerror("Erreur d'URL", "Le format de l'URL n'est pas correct.\nVeuillez entrer une URL valide comme 'http://exemple.com'.")
            return
        try:
            top_count = int(self.top_keywords_entry.get().strip())
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer un nombre valide pour le nombre de mots-clés dans le top.")
            return
        user_keywords = self.keywords_entry.get().split(",")
        resultats = audit_seo(url, 'parasite.csv', user_keywords, top_count)
        self.result_interface(resultats)
        if self.current_window:
            return

    def validate_url(self, url):
        pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        return re.match(pattern, url) is not None

    def format_results(resultats):
        return ' | '.join([f"{mot}: {occurrence}" for mot, occurrence in resultats])

    def on_double_click(self, tree, event):
        # Permet de rendre la cellule éditable
        item = tree.identify('item', event.x, event.y)
        column = tree.identify_column(event.x)
        if column == '#1':
            tree.item(item, open=True)  # Ou tout autre logique pour éditer l'item

    def on_right_click(self, tree, event):
            # Menu contextuel pour copier le contenu
            iid = tree.identify_row(event.y)
            if iid:
                # Sélectionner la ligne sur laquelle le clic droit a été effectué
                tree.selection_set(iid)
                menu = tk.Menu(tree, tearoff=0)
                menu.add_command(label="Copier", command=lambda: self.copier_valeur(tree, iid))
                menu.add_command(label="tu foue quoi ici ? ",)
                menu.post(event.x_root, event.y_root)

    def copier_valeur(self, tree, iid):
        # Fonction pour copier le contenu de l'item sélectionné
        selected_item = tree.selection()[0]
        clipboard_content = tree.item(selected_item, 'values')
        self.clipboard_clear()
        self.clipboard_append(clipboard_content)
            
    def save_results_to_pdf(self, resultats):
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if not file_path:
            return

        doc = SimpleDocTemplate(file_path, pagesize=LETTER)
        story = []
        styles = getSampleStyleSheet()

        # Titre
        story.append(Paragraph("Rapport d'Audit SEO", styles['Title']))

        # URL analysée
        story.append(Spacer(1, 12))
        story.append(Paragraph(f"URL analysée: {resultats.get('url', 'Non spécifiée')}", styles['Normal']))

        # Mots clés utilisateur
        story.append(Spacer(1, 12))
        story.append(Paragraph("Mots clés utilisateur:", styles['Heading2']))
        if resultats['Mots clés utilisateur']:
            for mot, occurrence in resultats['Mots clés utilisateur'].items():
                story.append(Paragraph(f"{mot}: {occurrence}", styles['Normal']))
        else:
            story.append(Paragraph("N/A", styles['Normal']))

        # Top mots clés
        story.append(Spacer(1, 12))
        story.append(Paragraph("Top mots clés:", styles['Heading2']))
        for mot, occurrence in resultats['Top mots clés']:
            story.append(Paragraph(f"{mot}: {occurrence}", styles['Normal']))

        # Liens entrants
        story.append(Spacer(1, 12))
        story.append(Paragraph("Liens entrants:", styles['Heading2']))
        for lien in resultats['liens_entrants']:
            story.append(Paragraph(lien, styles['Normal']))

        # Liens sortants
        story.append(Spacer(1, 12))
        story.append(Paragraph("Liens sortants:", styles['Heading2']))
        for lien in resultats['liens_sortants']:
            story.append(Paragraph(lien, styles['Normal']))
            
        # Balises alt manquantes
        story.append(Paragraph("Balises alt manquantes:", styles['Heading2']))
        if resultats['Details Balises alt manquantes']:
            for image_src in resultats['Details Balises alt manquantes']:
                story.append(Paragraph(image_src, styles['Normal']))
        else:
            story.append(Paragraph("Aucune", styles['Normal']))

        doc.build(story)
        messagebox.showinfo("Sauvegarde Réussie", "Le rapport a été sauvegardé avec succès en format PDF.")

    def edit_parasites(self):
        self.parasites_interface()

    def save_parasites(self, edit_window):
        updated_content = self.parasites_text.get("1.0", tk.END).strip()
        with open('parasite.csv', 'w', encoding='utf-8') as file:
            file.write(updated_content)
        messagebox.showinfo("Sauvegarde réussie", "Les modifications ont été sauvegardées.")
        self.back_action()  # Rouvre le menu principal

    def update_keywords(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                new_keywords = file.read().splitlines()
            # Vous pouvez ici intégrer la logique pour mettre à jour les mots clés parasites
            messagebox.showinfo("Mise à Jour Réussie", "La liste des mots clés parasites a été mise à jour.")
    
    def back_action(self):
        if self.current_window:  # Ferme la fenêtre actuelle si elle est ouverte
            self.current_window.destroy()
        self.current_window = None
        self.deiconify()  # Réaffiche le menu principal si c'était caché
        
    def back_menu(self):
        # Code pour gérer le retour au menu principal
        if self.current_window is not None:
            self.current_window.destroy()
            self.current_window = None
        self.deiconify()  # Réaffiche la fenêtre principale
        
    def quit_app(self):
        self.destroy()  # Ferme la fenêtre principale
        self.quit()     # Arrête l'exécution de Tkinter

def fetch_html(url):
    reponse = requests.get(url)
    reponse.raise_for_status()
    return reponse.text

def strip_html(texte_html):
    soupe = BeautifulSoup(texte_html, 'html.parser')
    return soupe.get_text()

def count_missing_alt_tags(texte_html):
    soupe = BeautifulSoup(texte_html, 'html.parser')
    images = soupe.find_all('img')
    return sum(1 for image in images if not image.has_attr('alt') or not image['alt'])

def count_occurrences(texte):
    texte = texte.lower()
    texte = re.sub(r'[^\w\s]','', texte)
    mots = texte.split()
    occurrences = {}
    for mot in mots:
        occurrences[mot] = occurrences.get(mot, 0) + 1
    return dict(sorted(occurrences.items(), key=lambda item: item[1], reverse=True))

def remove_stopwords(occurrences, parasites):
    return {mot: occurrences[mot] for mot in occurrences if mot not in parasites}

def load_stopwords(chemin_fichier):
    with open(chemin_fichier, 'r', encoding='utf-8') as fichier:
        parasites = fichier.read().splitlines()
    return parasites

def extract_attribute_values(texte_html, balise, attribut):
    soupe = BeautifulSoup(texte_html, 'html.parser')
    return [element.get(attribut) for element in soupe.find_all(balise) if element.has_attr(attribut)]

def normalize_url(url):
    """ Supprime les parties http://, https:// et www. d'une URL et extrait la racine de l'URL. """
    url_sans_schema = re.sub(r'^(http://|https://)?(www\.)?', '', url)
    return re.match(r'[^/]+', url_sans_schema).group()

def find_empty_alt_balise(texte_html):
    soupe = BeautifulSoup(texte_html, 'html.parser')
    images_sans_alt = [img['src'] for img in soupe.find_all('img') if not img.get('alt')]
    return images_sans_alt

def audit_seo(url, chemin_fichier_parasites, user_keywords, top_count=3): 
    resultats = {}
    html = fetch_html(url)
    texte_sans_html = strip_html(html)
    occurrences = count_occurrences(texte_sans_html)
    parasites = load_stopwords(chemin_fichier_parasites)
    mots_cles = remove_stopwords(occurrences, parasites)
    url_base = normalize_url(url)

    liens_href = extract_attribute_values(html, 'a', 'href')
    liens_entrants = []
    liens_sortants = []
    for href in liens_href:
        if href and normalize_url(href) == url_base:
            liens_entrants.append(href)
        else:
            liens_sortants.append(href)

    top_mots_cles = dict(sorted(mots_cles.items(), key=lambda item: item[1], reverse=True)[:top_count])
    mots_cles_utilisateur = {mot: occurrences.get(mot, 0) for mot in user_keywords if mot in occurrences}

    resultats['url'] = url
    resultats['Mots clés utilisateur'] = mots_cles_utilisateur
    resultats['Top mots clés'] = list(top_mots_cles.items())[:top_count]
    resultats['Nombre de liens entrants'] = len(liens_entrants)
    resultats['Nombre de liens sortants'] = len(liens_sortants)
    resultats['Balises alt manquantes'] = count_missing_alt_tags(html)  # Pour l'interface graphique
    resultats['Details Balises alt manquantes'] = find_empty_alt_balise(html)  # Pour le rapport PDF
    resultats['liens_entrants'] = liens_entrants
    resultats['liens_sortants'] = liens_sortants
        
    return resultats

if __name__ == "__main__":
    app = SEOAuditApplication()
    app.mainloop()