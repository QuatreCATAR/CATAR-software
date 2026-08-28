from fastapi.testclient import TestClient
from interface.api import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "OK"


def test_phase1_endpoint():
    response = client.post("/phase1", json={"answers": {"01-01-00": "Oui"}})
    assert response.status_code == 200
    assert "result" in response.json()


def test_phase2_endpoint():
    response = client.post("/phase2", json={"answers": {"02-01-01": "défini"}})
    assert response.status_code == 200
    assert "result" in response.json()


def test_phase3_endpoint():
    response = client.post("/phase3", json={
        "before": {"01-01-00": "Oui"},
        "after": {"01-01-00": "Oui"}
    })
    assert response.status_code == 200
    assert "result" in response.json()
