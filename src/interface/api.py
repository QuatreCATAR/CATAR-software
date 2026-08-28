from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict

from engine.core import CatarEngine

# Initialisation du moteur CATAR
engine = CatarEngine(
    protocol_dir="src/protocol",
    scoring_file="src/protocol/scoring.json"
)

app = FastAPI(
    title="CATAR-software API",
    description="API REST pour l'évaluation cognitive CATAR",
    version="1.0"
)

# ---------- Modèles Pydantic ----------

class Phase1Input(BaseModel):
    answers: Dict[str, str]

class Phase2Input(BaseModel):
    answers: Dict[str, str]

class Phase3Input(BaseModel):
    before: Dict[str, str]
    after: Dict[str, str]

class AggregateInput(BaseModel):
    phase1: Dict[str, str]
    phase2: Dict[str, str]
    phase3_before: Dict[str, str]
    phase3_after: Dict[str, str]


# ---------- Endpoints ----------

@app.get("/health")
def health_check():
    return {"status": "OK", "message": "CATAR API opérationnelle"}


@app.post("/phase1")
def evaluate_phase1(data: Phase1Input):
    result = engine.evaluate_phase1(data.answers)
    return {"phase": 1, "result": result}


@app.post("/phase2")
def evaluate_phase2(data: Phase2Input):
    result = engine.evaluate_phase2(data.answers)
    return {"phase": 2, "result": result}


@app.post("/phase3")
def evaluate_phase3(data: Phase3Input):
    result = engine.evaluate_phase3(data.before, data.after)
    return {"phase": 3, "result": result}


@app.post("/aggregate")
def aggregate_scores(data: AggregateInput):
    phase1 = engine.evaluate_phase1(data.phase1)
    phase2 = engine.evaluate_phase2(data.phase2)
    phase3 = engine.evaluate_phase3(data.phase3_before, data.phase3_after)

    final = engine.aggregate_scores(phase1, phase2, phase3)
    return {"final_score": final}

