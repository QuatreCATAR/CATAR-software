# scoring.py — Processus CATAR
# Calcul des scores pour le passage CATAR
# Ce module est autonome et ne dépend d’aucune bibliothèque externe.

# ------------------------------------------------------------
# 01 — LOGIQUE UNIVERSELLE ET COGNITIVE
# ------------------------------------------------------------

def score_01_01(responses):
    """
    Section 01-01 : Compréhension systémique du JEu
    4 questions, réponses N=0, Nn=1, On=2, O=3
    Validé si score > 6
    """
    score = sum(responses)
    return {
        "score": score,
        "max": 12,
        "validated": score > 6
    }


def score_01_02(responses):
    """
    Section 01-02 : Stabilité cognitive fonctionnelle
    12 questions, réponses N=0, Nn=1, On=2, O=3
    Validé si score > 20
    """
    score = sum(responses)
    return {
        "score": score,
        "max": 36,
        "validated": score > 20
    }


# ------------------------------------------------------------
# 02 — CONNAISSANCE DU CORPUS CATAR
# ------------------------------------------------------------

def score_02_01(correct_answers, excellence_flags):
    """
    Section 02-01 : Connaissance du logiciel CATAR
    26 questions
    Bonne réponse = 1
    Bonne réponse excellence = 1 + 1 excellence
    Validé si score > 16
    """
    score = sum(correct_answers)
    excellence = sum(excellence_flags)
    return {
        "score": score,
        "max": 26,
        "validated": score > 16,
        "excellence": excellence,
        "excellence_max": 5
    }


def score_02_02(correct_answers, excellence_flags):
    """
    Section 02-02 : Compréhension symbologique
    8 questions
    Validé si score > 2
    """
    score = sum(correct_answers)
    excellence = sum(excellence_flags)
    return {
        "score": score,
        "max": 8,
        "validated": score > 2,
        "excellence": excellence,
        "excellence_max": 4
    }


def score_02_03(correct_answers, excellence_flags):
    """
    Section 02-03 : Compréhension jeux de mots
    5 questions
    Validé si score > 2
    """
    score = sum(correct_answers)
    excellence = sum(excellence_flags)
    return {
        "score": score,
        "max": 5,
        "validated": score > 2,
        "excellence": excellence,
        "excellence_max": 1
    }


# ------------------------------------------------------------
# 03 — UTILISATION DU PROTOCOLE MINOU
# ------------------------------------------------------------

def score_03_01(responses):
    """
    Section 03-01 : Utilisation fonctionnelle
    6 questions, réponses N=0, Nn=1, On=2, O=3
    Validé si score > 10
    """
    score = sum(responses)
    return {
        "score": score,
        "max": 18,
        "validated": score > 10
    }


def score_03_02(responses):
    """
    Section 03-02 : Utilisation en autodétermination
    11 questions
    Validé si score > 20
    """
    score = sum(responses)
    return {
        "score": score,
        "max": 33,
        "validated": score > 20
    }


# ------------------------------------------------------------
# 04 — ALIGNEMENT AU SUPPORT
# ------------------------------------------------------------

def alignement_support(responses_dict):
    """
    Section 04-01 : Alignement au support
    Les réponses sont textuelles et doivent être intégrées directement dans le rapport.
    """
    return responses_dict


# ------------------------------------------------------------
# CALCUL GLOBAL DU PASSAGE
# ------------------------------------------------------------

def compute_global_score(data):
    """
    data = {
        "01_01": [...],
        "01_02": [...],
        "02_01_correct": [...],
        "02_01_excellence": [...],
        "02_02_correct": [...],
        "02_02_excellence": [...],
        "02_03_correct": [...],
        "02_03_excellence": [...],
        "03_01": [...],
        "03_02": [...],
        "04_01": {...}
    }
    """

    s0101 = score_01_01(data["01_01"])
    s0102 = score_01_02(data["01_02"])

    s0201 = score_02_01(data["02_01_correct"], data["02_01_excellence"])
    s0202 = score_02_02(data["02_02_correct"], data["02_02_excellence"])
    s0203 = score_02_03(data["02_03_correct"], data["02_03_excellence"])

    s0301 = score_03_01(data["03_01"])
    s0302 = score_03_02(data["03_02"])

    align = alignement_support(data["04_01"])

    total_excellence = (
        s0201["excellence"] +
        s0202["excellence"] +
        s0203["excellence"]
    )

    return {
        "01": {
            "01_01": s0101,
            "01_02": s0102,
            "score_total": s0101["score"] + s0102["score"],
            "max": 48
        },
        "02": {
            "02_01": s0201,
            "02_02": s0202,
            "02_03": s0203,
            "score_total": s0201["score"] + s0202["score"] + s0203["score"],
            "max": 39,
            "excellence_total": total_excellence,
            "excellence_max": 10
        },
        "03": {
            "03_01": s0301,
            "03_02": s0302,
            "score_total": s0301["score"] + s0302["score"],
            "max": 51
        },
        "04": align
    }

