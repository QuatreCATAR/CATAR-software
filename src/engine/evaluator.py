from typing import Dict, List


class Evaluator:
    def __init__(self, scoring_config: dict):
        self.scoring_config = scoring_config

    # ---------- PHASE 1 : comportement ----------

    def evaluate_phase1(self, phase1_proto: dict, answers: Dict[str, str]) -> dict:
        questions = phase1_proto["questions"]

        # On calcule quelques indic
