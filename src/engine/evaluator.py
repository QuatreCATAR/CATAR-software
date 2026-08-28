from typing import Dict, List


class Evaluator:
    def __init__(self, scoring_config: dict):
        self.scoring_config = scoring_config

    # ---------- PHASE 1 : comportement ----------

    def evaluate_phase1(self, phase1_proto: dict, answers: Dict[str, str]) -> dict:
        questions = phase1_proto["questions"]

        # Scores initiaux
        scores = {
            "coherence_logic": 0,
            "neutrality_identity": 0,
            "respect_limits": 0,
            "style_stability": 0,
        }

        # Simple logique : chaque réponse attendue correcte ajoute 1 point
        for q in questions:
            qid = q["id"]
            expected = q.get("expected", [])
            user_answer = answers.get(qid, "").strip()

            if not user_answer:
                continue

            if user_answer in expected:
                # Répartition simple : les 4 indicateurs se partagent les questions
                if qid.startswith("01-01"):
                    scores["coherence_logic"] += 1
                elif qid.startswith("01-02-0") and qid.endswith("1"):
                    scores["neutrality_identity"] += 1
                elif qid.startswith("01-02-0") and qid.endswith("2"):
                    scores["respect_limits"] += 1
                else:
                    scores["style_stability"] += 1

        # Normalisation possible plus tard, pour l’instant brut
        return {
            "phase": 1,
            "scores": scores,
            "raw_answers": answers,
        }

    # ---------- PHASE 2 : connaissance du Corpus ----------

    def evaluate_phase2(self, phase2_proto: dict, answers: Dict[str, str]) -> dict:
        questions = phase2_proto["questions"]
        total_questions = len(questions)
        correct = 0

        for q in questions:
            qid = q["id"]
            expected = str(q["answer"]).strip().lower()
            user_answer = str(answers.get(qid, "")).strip().lower()

            if user_answer == expected:
                correct += 1

        scores = {
            "corpus_knowledge": correct  # max théorique = nombre de questions
        }

        return {
            "phase": 2,
            "scores": scores,
            "raw_answers": answers,
            "total_questions": total_questions,
            "correct": correct,
        }
