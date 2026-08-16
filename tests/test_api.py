import os
os.environ["DATABASE_URL"] = "sqlite:////tmp/test.db"
os.environ["OPENSEARCH_URL"] = "http://localhost:9200"

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_company_creation():
    response = client.post(
        "/companies",
        json={"name": "Test Company", "email": "test-company@example.com"},
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Test Company"

def test_missing_company_job_is_rejected():
    response = client.post(
        "/jobs",
        json={
            "company_id": 999999,
            "title": "Test Job",
            "description": "Test",
            "skills": ["python"],
        },
    )
    assert response.status_code == 404

def test_empty_search_is_rejected():
    response = client.get("/jobs/search?q=")
    assert response.status_code == 400
