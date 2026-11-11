import os
os.environ["RECRUIT_DB"] = "test_candidates.db"
from fastapi.testclient import TestClient
from app.api import app
from app.matcher import analyze, extract_skills

RESUME = "Python developer with SQL, Pandas, Docker and FastAPI experience. Built ETL pipelines."
JD = "Looking for an intern skilled in Python, SQL, Docker, Kubernetes and ETL pipelines."


def test_extract_skills():
    assert {"python", "sql", "docker", "fastapi"} <= extract_skills(RESUME)


def test_analyze_matches_and_missing():
    r = analyze(RESUME, JD)
    assert "kubernetes" in r["missing_skills"] and "python" in r["matched_skills"]
    assert 0 < r["final_score"] <= 100


def test_api_roundtrip():
    c = TestClient(app)
    assert c.get("/health").json() == {"status": "ok"}
    r = c.post("/match", json={"candidate_name": "Test", "resume_text": RESUME, "job_description": JD})
    assert r.status_code == 200 and r.json()["final_score"] > 0
    assert any(x["name"] == "Test" for x in c.get("/candidates").json())


def teardown_module():
    if os.path.exists("test_candidates.db"):
        os.remove("test_candidates.db")
