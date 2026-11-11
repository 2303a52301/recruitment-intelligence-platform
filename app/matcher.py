"""NLP core: TF-IDF + cosine similarity matching and skill extraction."""
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

SKILLS = [
    "python", "java", "sql", "c++", "javascript", "react", "node.js", "fastapi", "flask", "django",
    "rest api", "docker", "kubernetes", "git", "aws", "azure", "linux", "pandas", "numpy",
    "scikit-learn", "tensorflow", "pytorch", "machine learning", "deep learning", "nlp",
    "etl", "postgresql", "mysql", "mongodb", "sqlite", "power bi", "tableau", "spark", "airflow",
    "data cleaning", "data structures", "algorithms", "oop", "streamlit", "ci/cd", "github actions",
]


def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9+#./\s-]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def extract_skills(text: str) -> set:
    """Whole-word/phrase match against the skill vocabulary."""
    t = clean_text(text)
    found = set()
    for skill in SKILLS:
        if re.search(rf"(?<![a-z0-9]){re.escape(skill)}(?![a-z0-9])", t):
            found.add(skill)
    return found


def similarity_score(resume: str, job_description: str) -> float:
    """TF-IDF vectors for both texts, then cosine similarity -> 0-100."""
    docs = [clean_text(resume), clean_text(job_description)]
    if not all(docs):
        return 0.0
    tfidf = TfidfVectorizer(stop_words="english", ngram_range=(1, 2)).fit_transform(docs)
    return round(float(cosine_similarity(tfidf[0], tfidf[1])[0][0]) * 100, 2)


def analyze(resume: str, job_description: str) -> dict:
    r, j = extract_skills(resume), extract_skills(job_description)
    skill_cov = len(r & j) / len(j) * 100 if j else 0.0
    sim = similarity_score(resume, job_description)
    return {
        "similarity_score": sim,
        "skill_coverage": round(skill_cov, 2),
        "final_score": round(0.6 * sim + 0.4 * skill_cov, 2),  # weighted blend
        "matched_skills": sorted(r & j),
        "missing_skills": sorted(j - r),
    }
