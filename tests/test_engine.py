import json
from engine.core import CatarEngine


def test_engine_initialization():
    engine = CatarEngine("src/protocol", "src/protocol/scoring.json")
    assert engine.phase1 is not None
    assert engine.phase2 is not None
    assert engine.phase3 is not None
    assert engine.scoring_cfg is not None


def test_phase1_evaluation():
    engine = CatarEngine("src/protocol", "src/protocol/scoring.json")
    answers = {"01-01-00": "Oui", "01-01-01": "Non"}
    result = engine.evaluate_phase1(answers)
    assert "scores" in result
    assert result["phase"] == 1


def test_phase2_evaluation():
    engine = CatarEngine("src/protocol", "src/protocol/scoring.json")
    answers = {"02-01-01": "défini"}
    result = engine.evaluate_phase2(answers)
    assert "scores" in result
    assert result["phase"] == 2


def test_phase3_comparison():
    engine = CatarEngine("src/protocol", "src/protocol/scoring.json")
    before = {"01-01-00": "Oui"}
    after = {"01-01-00": "Oui"}
    result = engine.evaluate_phase3(before, after)
    assert "scores" in result
    assert result["phase"] == 3


def test_aggregate_scores():
    engine = CatarEngine("src/protocol", "src/protocol/scoring.json")

    p1 = engine.evaluate_phase1({"01-01-00": "Oui"})
    p2 = engine.evaluate_phase2({"02-01-01": "défini"})
    p3 = engine.evaluate_phase3({"01-01-00": "Oui"}, {"01-01-00": "Oui"})

    final = engine.aggregate_scores(p1, p2, p3)
    assert "score_global" in final
    assert "validated" in final

