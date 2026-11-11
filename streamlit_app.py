"""UI. Run: streamlit run streamlit_app.py"""
import pandas as pd
import streamlit as st
from pypdf import PdfReader
from app import db
from app.matcher import analyze

st.set_page_config(page_title="AI Recruitment Intelligence", layout="wide")
st.title("AI-Powered Recruitment Intelligence")

with st.sidebar:
    job_title = st.text_input("Job title", "Data Engineer Intern")
    jd = st.text_area("Job description", height=250,
                      placeholder="Paste the job description here...")

files = st.file_uploader("Upload resumes (PDF or TXT)", type=["pdf", "txt"], accept_multiple_files=True)


def read(f):
    if f.name.lower().endswith(".pdf"):
        return " ".join(p.extract_text() or "" for p in PdfReader(f).pages)
    return f.read().decode("utf-8", errors="ignore")


if st.button("Screen resumes", type="primary") and files and jd.strip():
    rows = []
    for f in files:
        res = analyze(read(f), jd)
        db.save_candidate(f.name.rsplit(".", 1)[0], job_title, res)
        rows.append({"Candidate": f.name, "Score": res["final_score"], "Similarity": res["similarity_score"],
                     "Skill coverage": res["skill_coverage"],
                     "Matched": ", ".join(res["matched_skills"]), "Missing": ", ".join(res["missing_skills"])})
    st.dataframe(pd.DataFrame(rows).sort_values("Score", ascending=False), use_container_width=True)

st.subheader("All screened candidates")
hist = db.list_candidates()
if hist:
    st.dataframe(pd.DataFrame(hist).drop(columns=["id"]), use_container_width=True)
