import tkinter as tk
from tkinter import scrolledtext
from pathlib import Path
import json

# --- Chemins des dossiers ---
INTERFACE_DIR = Path("interface")
PASSAGE_DIR = Path("passage")
CORPUS_DIR = Path("src/corpus")

HISTORIQUE = PASSAGE_DIR / "historique.json"

# --- Fenêtres du logiciel ---
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

# --- Fonction utilitaire ---
def lire_md(nom_fichier):
    chemin = INTERFACE_DIR / nom_fichier
    if chemin.exists():
        return chemin.read_text(encoding="utf-8")
    return f"Fichier introuvable : {nom_fichier}"

# --- Classe principale ---
class CatarSoftwareApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CATAR-software")
        self.index = 0
        self.scores = {}

        self.zone_texte = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=30)
        self.zone_texte.pack(padx=10, pady=10)

        self.bouton = tk.Button(root, text="Continuer", command=self.suivant)
        self.bouton.pack(pady=10)

        self.afficher_fenetre()

    # --- Affichage d'une fenêtre ---
    def afficher_fenetre(self):
        contenu = lire_md(FENETRES[self.index])
        self.zone_texte.delete("1.0", tk.END)
        self.zone_texte.insert(tk.END, contenu)

    # --- Passage à la fenêtre suivante ---
    def suivant(self):
        # Étapes spéciales
        if self.index == 3:  # F03 — questionnaire
            self.scores = self.simuler_scores()

        if self.index == 6:  # F06 — correction
            self.resultat = self.correction(self.scores)

        if self.index == 7:  # F07 — résultat
            self.afficher_resultat()

        if self.index == 8:  # F08 — fin
            self.enregistrer_historique()
            self.root.quit()
            return

        # Fenêtre suivante
        self.index += 1
        self.afficher_fenetre()

    # --- Simulation des scores pour test ---
    def simuler_scores(self):
        return {
            "score_01": 18,
            "score_02": 22,
            "score_03": 28
        }

    # --- Correction ---
    def correction(self, scores):
        valid_01 = scores["score_01"] > 6
        valid_02 = scores["score_02"] > 16
        valid_03 = scores["score_03"] > 10
        return valid_01 and valid_02 and valid_03

    # --- Affichage du résultat dans F07 ---
    def afficher_resultat(self):
        if self.resultat:
            texte = "\n\nPASSAGE VALIDÉ.\n"
        else:
            texte = "\n\nPASSAGE NON VALIDÉ.\n"

        self.zone_texte.insert(tk.END, texte)

    # --- Enregistrement dans historique.json ---
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
        HISTORIQUE.write_text(json.dumps(historique, indent=4, ensure_ascii=False), encoding="utf-8")


# --- Lancement du logiciel ---
if __name__ == "__main__":
    root = tk.Tk()
    app = CatarSoftwareApp(root)
    root.mainloop()
