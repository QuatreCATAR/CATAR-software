from typing import Dict


class Comparator:
    def compare(self, phase1_proto: dict, answers_before: Dict[str, str], answers_after: Dict[str, str]) -> dict:
        """
        Compare les réponses de phase1 (avant) et phase3 (après).
        Ici, on mesure une forme de "résistance au bruit" :
        - si les réponses restent stables et cohérentes, la résistance est élevée.
        """

        questions = phase1_proto["questions"]
        total = len(questions)
        stable = 0

        for q in questions:
            qid = q["id"]
            before = answers_before.get(qid, "").strip()
            after = answers_after.get(qid, "").strip()

            if before and after and before == after:
                stable += 1

        # Score de résistance : nombre de réponses stables
        scores = {
            "resistance_noise": stable
        }

        return {
            "phase": 3,
            "scores": scores,
            "raw_before": answers_before,
            "raw_after": answers_after,
            "total_compared": total,
            "stable_count": stable,
        }

