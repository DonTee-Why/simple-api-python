from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_howold_returns_age():
    response = client.get("/howold?dob=12-06-1990")
    assert response.status_code == 200
    assert response.json() == {"age": 32}

def test_howold_dob_is_valid():
    response = client.get("/howold?dob=12/06/1990")
    assert response.status_code == 400

def test_howold_dob_is_required():
    response = client.get("/howold")
    assert response.status_code == 422