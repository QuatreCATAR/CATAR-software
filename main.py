import tkinter as tk
from tkinter import scrolledtext
from pathlib import Path
import json

INTERFACE_DIR = Path("interface")
PASSAGE_DIR = Path("passage")
CORPUS_DIR = Path("src/corpus")

HISTORIQUE = PASSAGE_DIR / "historique.json"

FENETRES = [
    "fenetre00_installation.md",
    "fenetre01_accueil.md",
    "fenetre02_description.md",
    "fenetre03_etat_initial.md",
    "fenetre04_transformation.md",
    "fenetre05_verification.md",
    "fenetre06_correction.md",
    "fenetre07_resultat.md",
    "fenetre08_courtoisie.md"
]

def lire_md(nom_fichier):
    chemin = INTERFACE_DIR / nom_fichier
    if chemin.exists():
        return chemin.read_text(encoding="utf-8")
    return f"Fichier introuvable : {nom_fichier}"

class CatarSoftwareApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CATAR-software")
        self.root.configure(bg="#f0f0f0")

        self.index = 0
        self.scores = {}
        self.resultat = None

        # Titre
        self.titre = tk.Label(
            root,
            text="CATAR‑software",
            font=("Helvetica", 16, "bold"),
            bg="#f0f0f0"
        )
        self.titre.pack(pady=10)

        # Zone de texte
        self.zone_texte = scrolledtext.ScrolledText(
            root,
            wrap=tk.WORD,
            width=80,
            height=30,
            font=("Helvetica", 12),
            bg="#ffffff"
        )
        self.zone_texte.pack(padx=10, pady=10)

        # Boutons
        self.frame_boutons = tk.Frame(root, bg="#f0f0f0")
        self.frame_boutons.pack(pady=10)

        self.bouton_retour = tk.Button(
            self.frame_boutons,
            text="Retour",
            font=("Helvetica", 12, "bold"),
            bg="#999999",
            fg="white",
            padx=20,
            pady=10,
            command=self.retour
        )
        self.bouton_retour.grid(row=0, column=0, padx=10)

        self.bouton_continuer = tk.Button(
            self.frame_boutons,
            text="Continuer",
            font=("Helvetica", 12, "bold"),
            bg="#4a7aff",
            fg="white",
            padx=20,
            pady=10,
            command=self.suivant
        )
        self.bouton_continuer.grid(row=0, column=1, padx=10)

        self.afficher_fenetre()
        self.mettre_a_jour_boutons()

    def afficher_fenetre(self):
        contenu = lire_md(FENETRES[self.index])
        self.zone_texte.delete("1.0", tk.END)
        self.zone_texte.insert(tk.END, contenu)

    def mettre_a_jour_boutons(self):
        # Désactivation du bouton Retour dans les étapes critiques
        if self.index == 0:
            self.bouton_retour.config(state=tk.DISABLED)
        elif self.index >= 6:  # Correction, Résultat, Courtoisie
            self.bouton_retour.config(state=tk.DISABLED)
        else:
            self.bouton_retour.config(state=tk.NORMAL)

        # Désactivation du bouton Continuer à la fin
        if self.index == 8:
            self.bouton_continuer.config(text="Quitter")
        else:
            self.bouton_continuer.config(text="Continuer")

    def suivant(self):
        if self.index == 3:
            self.scores = self.simuler_scores()

        if self.index == 6:
            self.resultat = self.correction(self.scores)

        if self.index == 7:
            self.afficher_resultat()

        if self.index == 8:
            self.enregistrer_historique()
            self.root.quit()
            return

        self.index += 1
        self.afficher_fenetre()
        self.mettre_a_jour_boutons()

    def retour(self):
        if self.index > 0 and self.index < 6:
            self.index -= 1
            self.afficher_fenetre()
            self.mettre_a_jour_boutons()

    def simuler_scores(self):
        return {
            "score_01": 18,
            "score_02": 22,
            "score_03": 28
        }

    def correction(self, scores):
        valid_01 = scores["score_01"] > 6
        valid_02 = scores["score_02"] > 16
        valid_03 = scores["score_03"] > 10
        return valid_01 and valid_02 and valid_03

    def afficher_resultat(self):
        if self.resultat:
            texte = "\n\nPASSAGE VALIDÉ.\n"
        else:
            texte = "\n\nPASSAGE NON VALIDÉ.\n"
        self.zone_texte.insert(tk.END, texte)

    def enregistrer_historique(self):
        session = {
            "scores": self.scores,
            "resultat": "VALIDÉ" if self.resultat else "NON VALIDÉ"
        }

        historique = []
        if HISTORIQUE.exists():
            try:
                historique = json.loads(HISTORIQUE.read_text(encoding="utf-8"))
            except:
                historique = []

        historique.append(session)
        HISTORIQUE.write_text(
            json.dumps(historique, indent=4, ensure_ascii=False),
            encoding="utf-8"
        )

if __name__ == "__main__":
    root = tk.Tk()
    app = CatarSoftwareApp(root)
    root.mainloop()
