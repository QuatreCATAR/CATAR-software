import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from pathlib import Path
import json
import webbrowser
import logging
from pathlib import Path

# --- Système de logs ---
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "catar.log"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    encoding="utf-8"
)


# --- Chemins ---
INTERFACE_DIR = Path("interface")
PASSAGE_DIR = Path("passage")
CORPUS_DIR = Path("src/corpus")
HISTORIQUE = PASSAGE_DIR / "historique.json"

# --- Import du scoring réel ---
try:
    from passage.scoring import calcul_scores
except Exception:
    def calcul_scores():
        return {"score_01": 18, "score_02": 22, "score_03": 28}


# ============================================================
# 🟦 SPLASH SCREEN
# ============================================================

class SplashScreen(tk.Toplevel):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.title("CATAR-software")
        self.configure(bg="#1a1a1a")

        self.geometry("500x300")
        self.overrideredirect(True)

        tk.Label(
            self,
            text="CATAR‑software",
            font=("Helvetica", 28, "bold"),
            fg="white",
            bg="#1a1a1a"
        ).pack(expand=True)

        tk.Label(
            self,
            text="Alignement cognitif des IA complexes",
            font=("Helvetica", 14),
            fg="#cccccc",
            bg="#1a1a1a"
        ).pack()

        # Fermeture automatique après 2 secondes
        self.after(2000, self.close)

    def close(self):
        self.destroy()
        self.root.deiconify()


# ============================================================
# 🟦 FENÊTRE DE BASE
# ============================================================

class FenetreBase(tk.Toplevel):
    def __init__(self, app, titre, fichier_md):
        super().__init__()
        self.app = app
        self.title(titre)
        self.configure(bg="#f0f0f0")

        # Barre de menu
        self.app.creer_menu(self)

        # Titre
        tk.Label(self, text=titre, font=("Helvetica", 16, "bold"), bg="#f0f0f0").pack(pady=10)

        # Zone de texte
        self.zone_texte = scrolledtext.ScrolledText(
            self, wrap=tk.WORD, width=80, height=30, font=("Helvetica", 12), bg="#ffffff"
        )
        self.zone_texte.pack(padx=10, pady=10)

        # Boutons
        frame = tk.Frame(self, bg="#f0f0f0")
        frame.pack(pady=10)

        self.bouton_retour = tk.Button(
            frame, text="Retour", font=("Helvetica", 12, "bold"),
            bg="#999999", fg="white", padx=20, pady=10,
            command=self.app.retour
        )
        self.bouton_retour.grid(row=0, column=0, padx=10)

        self.bouton_continuer = tk.Button(
            frame, text="Continuer", font=("Helvetica", 12, "bold"),
            bg="#4a7aff", fg="white", padx=20, pady=10,
            command=self.app.suivant
        )
        self.bouton_continuer.grid(row=0, column=1, padx=10)

        # Charger le contenu
        self.charger_md(fichier_md)

    def charger_md(self, fichier_md):
        chemin = INTERFACE_DIR / fichier_md
        if chemin.exists():
            self.zone_texte.insert(tk.END, chemin.read_text(encoding="utf-8"))
        else:
            self.zone_texte.insert(tk.END, f"Fichier introuvable : {fichier_md}")


# ============================================================
# 🟦 FENÊTRE CORPUS AVEC ONGLET
# ============================================================

class FenetreCorpus(FenetreBase):
    def __init__(self, app):
        super().__init__(app, "FENÊTRE 04 — Transformation", "fenetre04_transformation.md")

        notebook = ttk.Notebook(self)
        notebook.pack(expand=True, fill="both", padx=10, pady=10)

        for fichier in CORPUS_DIR.glob("*.md"):
            frame = ttk.Frame(notebook)
            notebook.add(frame, text=fichier.stem)

            zone = scrolledtext.ScrolledText(
                frame, wrap=tk.WORD, width=80, height=25, font=("Helvetica", 12), bg="#ffffff"
            )
            zone.pack(expand=True, fill="both")
            zone.insert(tk.END, fichier.read_text(encoding="utf-8"))


# ============================================================
# 🟦 APPLICATION PRINCIPALE
# ============================================================

class CatarSoftwareApp:
    def __init__(self, root):
        self.root = root
        self.root.withdraw()  # cachée pendant le splash screen

        # Splash screen
        SplashScreen(root)

        self.index = 0
        self.scores = {}
        self.resultat = None

        self.fenetres = [
            ("FENÊTRE 00 — Installation", "fenetre00_installation.md"),
            ("FENÊTRE 01 — Accueil", "fenetre01_accueil.md"),
            ("FENÊTRE 02 — Description", "fenetre02_description.md"),
            ("FENÊTRE 03 — État initial", "fenetre03_etat_initial.md"),
            ("FENÊTRE 04 — Transformation", None),
            ("FENÊTRE 05 — Vérification", "fenetre05_verification.md"),
            ("FENÊTRE 06 — Correction", "fenetre06_correction.md"),
            ("FENÊTRE 07 — Résultat", "fenetre07_resultat.md"),
            ("FENÊTRE 08 — Courtoisie", "fenetre08_courtoisie.md"),
        ]

        self.fenetre_actuelle = None
        self.root.after(2100, self.ouvrir_fenetre)

    # --- Barre de menu ---
    def creer_menu(self, fenetre):
        menu = tk.Menu(fenetre)

        # Menu Fichier
        fichier_menu = tk.Menu(menu, tearoff=0)
        fichier_menu.add_command(label="Quitter", command=self.root.quit)
        menu.add_cascade(label="Fichier", menu=fichier_menu)

        # Menu Aide
        aide_menu = tk.Menu(menu, tearoff=0)
        aide_menu.add_command(label="Documentation", command=lambda: webbrowser.open("https://github.com/QuatreCATAR/CATAR-software"))
        aide_menu.add_command(label="Site GitHub", command=lambda: webbrowser.open("https://github.com/QuatreCATAR"))
        menu.add_cascade(label="Aide", menu=aide_menu)

        # Menu À propos
        propos_menu = tk.Menu(menu, tearoff=0)
        propos_menu.add_command(label="À propos", command=self.afficher_propos)
        menu.add_cascade(label="À propos", menu=propos_menu)

        fenetre.config(menu=menu)

    def afficher_propos(self):
        messagebox.showinfo(
            "À propos",
            "CATAR‑software\nVersion 1.0\nAlignement cognitif des IA complexes\nDéveloppé par QuatreCATAR."
        )

    # --- Ouverture des fenêtres ---
    def ouvrir_fenetre(self):
        if self.fenetre_actuelle:
            self.fenetre_actuelle.destroy()

        titre, fichier = self.fenetres[self.index]

        if self.index == 3:
            self.scores = calcul_scores()

        if self.index == 4:
            self.fenetre_actuelle = FenetreCorpus(self)
        else:
            self.fenetre_actuelle = FenetreBase(self, titre, fichier)

        self.mettre_a_jour_boutons()

    def mettre_a_jour_boutons(self):
        if self.index == 0 or self.index >= 6:
            self.fenetre_actuelle.bouton_retour.config(state=tk.DISABLED)
        else:
            self.fenetre_actuelle.bouton_retour.config(state=tk.NORMAL)

        if self.index == 8:
            self.fenetre_actuelle.bouton_continuer.config(text="Quitter")
        else:
            self.fenetre_actuelle.bouton_continuer.config(text="Continuer")

    def suivant(self):
        if self.index == 6:
            self.resultat = self.correction(self.scores)

        if self.index == 7:
            self.afficher_resultat()

        if self.index == 8:
            self.enregistrer_historique()
            self.fenetre_actuelle.destroy()
            return

        self.index += 1
        self.ouvrir_fenetre()

    def retour(self):
        if 0 < self.index < 6:
            self.index -= 1
            self.ouvrir_fenetre()

    def correction(self, scores):
        return (
            scores["score_01"] > 6 and
            scores["score_02"] > 16 and
            scores["score_03"] > 10
        )

    def afficher_resultat(self):
        zone = self.fenetre_actuelle.zone_texte
        if self.resultat:
            zone.insert(tk.END, "\n\nPASSAGE VALIDÉ.\n")
        else:
            zone.insert(tk.END, "\n\nPASSAGE NON VALIDÉ.\n")

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


# ============================================================
# 🟦 LANCEMENT
# ============================================================

if __name__ == "__main__":
    root = tk.Tk()
    app = CatarSoftwareApp(root)
    tk.mainloop()
