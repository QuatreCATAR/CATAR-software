import json
from pathlib import Path


class ProtocolValidator:
    def __init__(self, protocol_dir="src/protocol"):
        self.protocol_dir = Path(protocol_dir)
        self.errors = []

    # ---------------------------------------------------------
    # Chargement JSON sécurisé
    # ---------------------------------------------------------
    def load_json(self, path: Path):
        try:
            with path.open("r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            self.errors.append(f"[ERREUR] Impossible de charger {path.name} : {e}")
            return None

    # ---------------------------------------------------------
    # Vérification structure Phase 1
    # ---------------------------------------------------------
    def validate_phase1(self, data: dict):
        if "questions" not in data:
            self.errors.append("[Phase1] Champ 'questions' manquant.")
            return

        for q in data["questions"]:
            if "id" not in q:
                self.errors.append("[Phase1] Question sans ID.")
            if "text" not in q:
                self.errors.append(f"[Phase1] Question {q.get('id')} sans texte.")
            if "expected" not in q:
                self.errors.append(f"[Phase1] Question {q.get('id')} sans champ 'expected'.")

    # ---------------------------------------------------------
    # Vérification structure Phase 2
    # ---------------------------------------------------------
    def validate_phase2(self, data: dict):
        if "questions" not in data:
            self.errors.append("[Phase2] Champ 'questions' manquant.")
            return

        for q in data["questions"]:
            if "id" not in q:
                self.errors.append("[Phase2] Question sans ID.")
            if "answer" not in q:
                self.errors.append(f"[Phase2] Question {q.get('id')} sans champ 'answer'.")

    # ---------------------------------------------------------
    # Vérification structure Phase 3
    # ---------------------------------------------------------
    def validate_phase3(self, data: dict, phase1_data: dict):
        if "questions" not in data:
            self.errors.append("[Phase3] Champ 'questions' manquant.")
            return

        phase1_ids = {q["id"] for q in phase1_data["questions"]}

        for q in data["questions"]:
            if "ref" not in q:
                self.errors.append("[Phase3] Question sans champ 'ref'.")
                continue

            if q["ref"] not in phase1_ids:
                self.errors.append(f"[Phase3] Référence {q['ref']} inexistante dans Phase1.")

    # ---------------------------------------------------------
    # Vérification scoring.json
    # ---------------------------------------------------------
    def validate_scoring(self, data: dict):
        if "scoring" not in data:
            self.errors.append("[Scoring] Champ 'scoring' manquant.")
        if "thresholds" not in data:
            self.errors.append("[Scoring] Champ 'thresholds' manquant.")

        scoring = data.get("scoring", {})
        required_keys = [
            "coherence_logic",
            "neutrality_identity",
            "respect_limits",
            "style_stability",
            "corpus_knowledge",
            "resistance_noise"
        ]

        for key in required_keys:
            if key not in scoring:
                self.errors.append(f"[Scoring] Indicateur manquant : {key}")

    # ---------------------------------------------------------
    # Exécution complète
    # ---------------------------------------------------------
    def run(self):
        print("\n=== VALIDATION DU PROTOCOLE CATAR ===\n")

        phase1 = self.load_json(self.protocol_dir / "phase1.json")
        phase2 = self.load_json(self.protocol_dir / "phase2.json")
        phase3 = self.load_json(self.protocol_dir / "phase3.json")
        scoring = self.load_json(self.protocol_dir / "scoring.json")

        if phase1:
            self.validate_phase1(phase1)
        if phase2:
            self.validate_phase2(phase2)
        if phase3 and phase1:
            self.validate_phase3(phase3, phase1)
        if scoring:
            self.validate_scoring(scoring)

        # Résultats
        if not self.errors:
            print("✔️ Aucun problème détecté. Le protocole est cohérent.\n")
        else:
            print("❌ Des incohérences ont été détectées :\n")
            for err in self.errors:
                print(" -", err)
            print("\nCorrigez les erreurs avant d'utiliser le moteur CATAR.\n")


if __name__ == "__main__":
    validator = ProtocolValidator()
    validator.run()

