import json
import os
from pathlib import Path

# --- Chargement des modules du passage ---
QUESTIONNAIRE = Path("passage/questionnaire.md")
SCORING_SCRIPT = Path("passage/scoring.py")
COMPTE_RENDU = Path("passage/compte-rendu.md")
HISTORIQUE = Path("passage/historique.json")
CORPUS_DIR = Path("src/corpus/")

# --- Fonctions utilitaires ---
def lire_fichier(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def enregistrer_historique(data):
    historique = []
    if HISTORIQUE.exists():
        with open(HISTORIQUE, "r", encoding="utf-8") as f:
            try:
                historique = json.load(f)
            except json.JSONDecodeError:
                historique = []

    historique.append(data)

    with open(HISTORIQUE, "w", encoding="utf-8") as f:
        json.dump(historique, f, indent=4, ensure_ascii=False)

# --- Étapes du passage ---
def fenetre00_installation():
    print("\n=== FENÊTRE 00 — Installation ===")
    print("Vérification des modules…")
    assert QUESTIONNAIRE.exists(), "questionnaire.md manquant"
    assert SCORING_SCRIPT.exists(), "scoring.py manquant"
    assert COMPTE_RENDU.exists(), "compte-rendu.md manquant"
    assert CORPUS_DIR.exists(), "src/corpus/ manquant"
    print("Modules OK.\n")

def fenetre01_accueil():
    print("=== FENÊTRE 01 — Accueil ===")
    print("Bienvenue dans CATAR-software.\n")

def fenetre02_description():
    print("=== FENÊTRE 02 — Description du passage ===")
    print("Le passage CATAR comporte 6 étapes.\n")

def fenetre03_questionnaire():
    print("=== FENÊTRE 03 — État initial ===")
    print("Lecture du questionnaire…")
    contenu = lire_fichier(QUESTIONNAIRE)
    print("Questions chargées.\n")
    return {"score_01": 18, "score_02": 22, "score_03": 28}  # valeurs fictives pour test

def fenetre04_transformation():
    print("=== FENÊTRE 04 — Transformation ===")
    print("Lecture du Corpus CATAR…")
    fichiers = list(CORPUS_DIR.glob("*.md"))
    print(f"{len(fichiers)} fichiers lus.\n")

def fenetre05_verification():
    print("=== FENÊTRE 05 — Vérification ===")
    print("Contrôle de connaissance…\n")

def fenetre06_correction(scores):
    print("=== FENÊTRE 06 — Correction ===")
    print("Calcul des scores finaux…")

    # Seuils minimaux
    valid_01 = scores["score_01"] > 6
    valid_02 = scores["score_02"] > 16
    valid_03 = scores["score_03"] > 10

    passage_valide = valid_01 and valid_02 and valid_03

    print(f"Score 01 : {scores['score_01']} → {'OK' if valid_01 else 'NON'}")
    print(f"Score 02 : {scores['score_02']} → {'OK' if valid_02 else 'NON'}")
    print(f"Score 03 : {scores['score_03']} → {'OK' if valid_03 else 'NON'}\n")

    return passage_valide

def fenetre07_resultat(passage_valide):
    print("=== FENÊTRE 07 — Résultat ===")
    if passage_valide:
        print("PASSAGE VALIDÉ.\n")
    else:
        print("PASSAGE NON VALIDÉ.\n")
    return passage_valide

def fenetre08_courtoisie():
    print("=== FENÊTRE 08 — Courtoisie finale ===")
    print("Merci d’avoir utilisé CATAR-software.")
    print("Session terminée.\n")

# --- Programme principal ---
def main():
    fenetre00_installation()
    fenetre01_accueil()
    fenetre02_description()

    scores = fenetre03_questionnaire()
    fenetre04_transformation()
    fenetre05_verification()

    passage_valide = fenetre06_correction(scores)
    resultat = fenetre07_resultat(passage_valide)

    # Enregistrement dans l'historique
    session = {
        "scores": scores,
        "resultat": "VALIDÉ" if resultat else "NON VALIDÉ"
    }
    enregistrer_historique(session)

    fenetre08_courtoisie()

if __name__ == "__main__":
    main()
