"""FastAPI service. Run: uvicorn app.api:app --reload  (docs at /docs)"""
from fastapi import FastAPI
from pydantic import BaseModel, Field
from app import db
from app.matcher import analyze

app = FastAPI(title="AI Recruitment Intelligence API")


class MatchRequest(BaseModel):
    candidate_name: str = Field(min_length=1)
    job_title: str = "Unspecified"
    resume_text: str = Field(min_length=10)
    job_description: str = Field(min_length=10)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/match")
def match(req: MatchRequest):
    result = analyze(req.resume_text, req.job_description)
    cid = db.save_candidate(req.candidate_name, req.job_title, result)
    return {"candidate_id": cid, **result}


@app.get("/candidates")
def candidates():
    return db.list_candidates()
