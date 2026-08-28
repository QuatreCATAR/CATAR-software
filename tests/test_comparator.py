from engine.comparator import Comparator


def test_comparator_stability():
    comparator = Comparator()

    proto = {
        "questions": [
            {"id": "01-01-00"},
            {"id": "01-01-01"}
        ]
    }

    before = {"01-01-00": "Oui", "01-01-01": "Non"}
    after = {"01-01-00": "Oui", "01-01-01": "Non"}

    result = comparator.compare(proto, before, after)
    assert result["scores"]["resistance_noise"] == 2

