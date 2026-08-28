import json
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

from engine.core import CatarEngine
from tools.export import Exporter


class CatarUI:
    def __init__(self):
        self.engine = CatarEngine("src/protocol", "src/protocol/scoring.json")
        self.exporter = Exporter()

        self.root = tk.Tk()
        self.root.title("CATAR-software — Interface Graphique")
        self.root.geometry("700x600")

        self.phase1_answers = {}
        self.phase2_answers = {}
        self.phase3_answers = {}

        self._build_ui()

    # ---------------------------------------------------------
    #  Interface
    # ---------------------------------------------------------
    def _build_ui(self):
        tk.Label(self.root, text="CATAR-software", font=("Arial", 18, "bold")).pack(pady=10)

        # Boutons de chargement
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        tk.Button(frame, text="Charger Phase 1", command=self.load_phase1).grid(row=0, column=0, padx=10)
        tk.Button(frame, text="Charger Phase 2", command=self.load_phase2).grid(row=0, column=1, padx=10)
        tk.Button(frame, text="Charger Phase 3", command=self.load_phase3).grid(row=0, column=2, padx=10)

        # Bouton d'évaluation
        tk.Button(self.root, text="Lancer l'évaluation", command=self.run_evaluation,
                  bg="#4CAF50", fg="white", font=("Arial", 12, "bold")).pack(pady=15)

        # Zone de résultats
        tk.Label(self.root, text="Résultats :", font=("Arial", 14)).pack()
        self.output = scrolledtext.ScrolledText(self.root, width=80, height=20)
        self.output.pack(pady=10)

        # Bouton d'export
        tk.Button(self.root, text="Exporter les résultats", command=self.export_results,
                  bg="#2196F3", fg="white", font=("Arial", 12, "bold")).pack(pady=10)

    # ---------------------------------------------------------
    #  Chargement des fichiers JSON
    # ---------------------------------------------------------
    def load_json_file(self):
        path = filedialog.askopenfilename(
            title="Sélectionner un fichier JSON",
            filetypes=[("JSON files", "*.json")]
        )
        if not path:
            return None

        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de charger le fichier : {e}")
            return None

    def load_phase1(self):
        data = self.load_json_file()
        if data:
            self.phase1_answers = data
            messagebox.showinfo("Phase 1", "Réponses Phase 1 chargées.")

    def load_phase2(self):
        data = self.load_json_file()
        if data:
            self.phase2_answers = data
            messagebox.showinfo("Phase 2", "Réponses Phase 2 chargées.")

    def load_phase3(self):
        data = self.load_json_file()
        if data:
            self.phase3_answers = data
            messagebox.showinfo("Phase 3", "Réponses Phase 3 chargées.")

    # ---------------------------------------------------------
    #  Évaluation
    # ---------------------------------------------------------
    def run_evaluation(self):
        if not self.phase1_answers or not self.phase2_answers or not self.phase3_answers:
            messagebox.showwarning("Attention", "Veuillez charger les trois phases.")
            return

        p1 = self.engine.evaluate_phase1(self.phase1_answers)
        p2 = self.engine.evaluate_phase2(self.phase2_answers)
        p3 = self.engine.evaluate_phase3(self.phase1_answers, self.phase3_answers)

        final = self.engine.aggregate_scores(p1, p2, p3)

        self.last_results = final  # stockés pour export

        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, json.dumps(final, indent=2, ensure_ascii=False))

    # ---------------------------------------------------------
    #  Export
    # ---------------------------------------------------------
    def export_results(self):
        if not hasattr(self, "last_results"):
            messagebox.showwarning("Attention", "Aucun résultat à exporter.")
            return

        paths = self.exporter.export_all(self.last_results)
        msg = "Exports générés :\n"
        for fmt, path in paths.items():
            msg += f" - {fmt} : {path}\n"

        messagebox.showinfo("Export", msg)

    # ---------------------------------------------------------
    #  Lancement
    # ---------------------------------------------------------
    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    ui = CatarUI()
    ui.run()
