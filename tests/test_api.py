# tests/test_api.py

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200

def test_query_without_upload():
    response = client.post("/query/", json={"query": "Does it cover knee surgery?"})
    assert response.status_code == 404 or response.status_code == 400
