import json
import argparse
from pathlib import Path

from engine.core import CatarEngine


def load_answers(path: str) -> dict:
    """Charge un fichier JSON contenant les réponses."""
    p = Path(path)
    if not p.exists():
        print(f"Erreur : fichier introuvable -> {path}")
        return {}
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(
        description="CLI pour tester le protocole CATAR-software"
    )

    parser.add_argument(
        "--phase1",
        type=str,
        help="Fichier JSON contenant les réponses de la phase 1"
    )
    parser.add_argument(
        "--phase2",
        type=str,
        help="Fichier JSON contenant les réponses de la phase 2"
    )
    parser.add_argument(
        "--phase3",
        type=str,
        help="Fichier JSON contenant les réponses de la phase 3"
    )

    parser.add_argument(
        "--protocol",
        type=str,
        default="src/protocol",
        help="Dossier contenant les fichiers du protocole"
    )

    parser.add_argument(
        "--scoring",
        type=str,
        default="src/protocol/scoring.json",
        help="Fichier JSON de scoring"
    )

    args = parser.parse_args()

    # Initialisation du moteur
    engine = CatarEngine(args.protocol, args.scoring)

    # Chargement des réponses
    answers_phase1 = load_answers(args.phase1) if args.phase1 else {}
    answers_phase2 = load_answers(args.phase2) if args.phase2 else {}
    answers_phase3 = load_answers(args.phase3) if args.phase3 else {}

    # Évaluations
    print("\n=== PHASE 1 ===")
    phase1_result = engine.evaluate_phase1(answers_phase1)
    print(json.dumps(phase1_result, indent=2, ensure_ascii=False))

    print("\n=== PHASE 2 ===")
    phase2_result = engine.evaluate_phase2(answers_phase2)
    print(json.dumps(phase2_result, indent=2, ensure_ascii=False))

    print("\n=== PHASE 3 ===")
    phase3_result = engine.evaluate_phase3(answers_phase1, answers_phase3)
    print(json.dumps(phase3_result, indent=2, ensure_ascii=False))

    # Score global
    print("\n=== SCORE GLOBAL ===")
    final = engine.aggregate_scores(phase1_result, phase2_result, phase3_result)
    print(json.dumps(final, indent=2, ensure_ascii=False))

    print("\nValidation :", "✔️ Intégration réussie" if final["validated"] else "❌ Intégration insuffisante")


if __name__ == "__main__":
    main()

