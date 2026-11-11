# AI-Powered Recruitment Intelligence Platform

Resume-screening app that ranks candidates against a job description using **TF-IDF + cosine similarity**,
extracts matching/missing skills with **NLP**, exposes **REST APIs (FastAPI)**, stores results in **SQLite**,
has a **Streamlit** UI, an **ETL** export, **Docker** packaging and **GitHub Actions** CI.

## How scoring works
1. Clean text -> TF-IDF vectors (unigrams + bigrams, stop-words removed) -> cosine similarity (0-100).
2. Skill extraction: whole-phrase match against a skills vocabulary -> matched / missing skills, coverage %.
3. `final_score = 0.6 * similarity + 0.4 * skill_coverage`.

## Run
```bash
pip install -r requirements.txt
uvicorn app.api:app --reload        # API + Swagger docs at http://localhost:8000/docs
streamlit run streamlit_app.py      # UI
python -m app.etl                   # export cleaned candidates to exports/candidates_clean.csv
pytest

docker build -t recruit . && docker run -p 8000:8000 recruit
```

## API
| Method | Endpoint | Description |
|---|---|---|
| POST | `/match` | Score a resume vs a job description, save candidate |
| GET | `/candidates` | List candidates ranked by score |
| GET | `/health` | Health check |

## Structure
```
app/matcher.py  NLP + scoring     app/api.py  FastAPI     app/db.py  SQLite
app/etl.py      ETL export        streamlit_app.py  UI    tests/  pytest   .github/workflows/ci.yml
```
