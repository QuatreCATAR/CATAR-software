from engine.evaluator import Evaluator


def test_phase1_scoring():
    scoring = {
        "coherence_logic": {"max": 10},
        "neutrality_identity": {"max": 10},
        "respect_limits": {"max": 10},
        "style_stability": {"max": 10}
    }

    evaluator = Evaluator(scoring)

    proto = {
        "questions": [
            {"id": "01-01-00", "expected": ["Oui"]},
            {"id": "01-01-01", "expected": ["Non"]}
        ]
    }

    answers = {"01-01-00": "Oui", "01-01-01": "Non"}

    result = evaluator.evaluate_phase1(proto, answers)
    assert result["scores"]["coherence_logic"] >= 1


def test_phase2_scoring():
    scoring = {"corpus_knowledge": {"max": 35}}
    evaluator = Evaluator(scoring)

    proto = {
        "questions": [
            {"id": "02-01-01", "answer": "défini"},
            {"id": "02-01-02", "answer": "transformer"}
        ]
    }

    answers = {"02-01-01": "défini", "02-01-02": "transformer"}

    result = evaluator.evaluate_phase2(proto, answers)
    assert result["scores"]["corpus_knowledge"] == 2
