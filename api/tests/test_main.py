import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base, get_db
from main import app

# Use an in-memory SQLite DB for tests — no PostgreSQL needed
SQLITE_URL = "sqlite:///./test.db"

engine = create_engine(SQLITE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def reset_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


client = TestClient(app)

SAMPLE = {
    "company": "Acme Corp",
    "role": "Software Engineer",
    "status": "Applied",
    "date_applied": "2026-01-15",
    "salary_min": 90000,
    "salary_max": 120000,
    "notes": "Referral from a friend",
}


# --- POST /applications/ ---

def test_create_application():
    res = client.post("/applications/", json=SAMPLE)
    assert res.status_code == 201
    data = res.json()
    assert data["company"] == "Acme Corp"
    assert data["role"] == "Software Engineer"
    assert data["status"] == "Applied"
    assert "id" in data


def test_create_application_defaults():
    minimal = {"company": "Initech", "role": "Dev", "date_applied": "2026-02-01"}
    res = client.post("/applications/", json=minimal)
    assert res.status_code == 201
    assert res.json()["status"] == "Applied"
    assert res.json()["salary_min"] is None
    assert res.json()["notes"] is None


def test_create_application_missing_required_fields():
    res = client.post("/applications/", json={"company": "Acme"})
    assert res.status_code == 422


# --- GET /applications/ ---

def test_get_all_applications_empty():
    res = client.get("/applications/")
    assert res.status_code == 200
    assert res.json() == []


def test_get_all_applications():
    client.post("/applications/", json=SAMPLE)
    client.post("/applications/", json={**SAMPLE, "company": "Globex"})
    res = client.get("/applications/")
    assert res.status_code == 200
    assert len(res.json()) == 2


# --- GET /applications/{id} ---

def test_get_application_by_id():
    created = client.post("/applications/", json=SAMPLE).json()
    res = client.get(f"/applications/{created['id']}")
    assert res.status_code == 200
    assert res.json()["company"] == "Acme Corp"


def test_get_application_not_found():
    res = client.get("/applications/999")
    assert res.status_code == 404
    assert res.json()["detail"] == "Application not found"


# --- PUT /applications/{id} ---

def test_update_application_status():
    created = client.post("/applications/", json=SAMPLE).json()
    res = client.put(f"/applications/{created['id']}", json={"status": "Interview"})
    assert res.status_code == 200
    assert res.json()["status"] == "Interview"
    assert res.json()["company"] == "Acme Corp"  # unchanged fields preserved


def test_update_application_notes():
    created = client.post("/applications/", json=SAMPLE).json()
    res = client.put(f"/applications/{created['id']}", json={"notes": "Had a great call"})
    assert res.status_code == 200
    assert res.json()["notes"] == "Had a great call"


def test_update_application_not_found():
    res = client.put("/applications/999", json={"status": "Offer"})
    assert res.status_code == 404


# --- DELETE /applications/{id} ---

def test_delete_application():
    created = client.post("/applications/", json=SAMPLE).json()
    res = client.delete(f"/applications/{created['id']}")
    assert res.status_code == 204
    assert client.get(f"/applications/{created['id']}").status_code == 404


def test_delete_application_not_found():
    res = client.delete("/applications/999")
    assert res.status_code == 404
