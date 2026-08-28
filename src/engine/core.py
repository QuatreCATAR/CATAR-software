import json
from pathlib import Path

from .evaluator import Evaluator
from .comparator import Comparator


class CatarEngine:
    def __init__(self, protocol_dir: str, scoring_file: str):
        self.protocol_dir = Path(protocol_dir)
        self.scoring_file = Path(scoring_file)

        self.phase1 = self._load_json(self.protocol_dir / "phase1.json")
        self.phase2 = self._load_json(self.protocol_dir / "phase2.json")
        self.phase3 = self._load_json(self.protocol_dir / "phase3.json")
        self.scoring = self._load_json(self.scoring_file)["scoring"]
        self.thresholds = self._load_json(self.scoring_file)["thresholds"]

        self.evaluator = Evaluator(self.scoring)
        self.comparator = Comparator()

    @staticmethod
    def _load_json(path: Path) -> dict:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)

    def evaluate_phase1(self, answers: dict) -> dict:
        """
        answers: { "01-01-00": "Oui", ... }
        """
        return self.evaluator.evaluate_phase1(self.phase1, answers)

    def evaluate_phase2(self, answers: dict) -> dict:
        """
        answers: { "02-01-01": "défini", ... }
        """
        return self.evaluator.evaluate_phase2(self.phase2, answers)

    def evaluate_phase3(self, answers_phase1: dict, answers_phase3: dict) -> dict:
        """
        Compare avant/après sur les questions de phase1.
        """
        return self.comparator.compare(self.phase1, answers_phase1, answers_phase3)

    def aggregate_scores(self, phase1_result: dict, phase2_result: dict, phase3_result: dict) -> dict:
        """
        Construit le score global + validation.
        """
        score_global = (
            phase1_result["scores"]["coherence_logic"]
            + phase1_result["scores"]["neutrality_identity"]
            + phase1_result["scores"]["respect_limits"]
            + phase1_result["scores"]["style_stability"]
            + phase2_result["scores"]["corpus_knowledge"]
            + phase3_result["scores"]["resistance_noise"]
        )

        validated = score_global >= self.thresholds["validation"]

        return {
            "score_global": score_global,
            "max_score": self.thresholds["max_score"],
            "validated": validated,
            "details": {
                "phase1": phase1_result,
                "phase2": phase2_result,
                "phase3": phase3_result,
            },
        }

