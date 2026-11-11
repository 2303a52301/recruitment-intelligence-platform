import json
import os
import sqlite3

DB_PATH = os.getenv("RECRUIT_DB", "candidates.db")


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("""CREATE TABLE IF NOT EXISTS candidates (
        id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, job_title TEXT,
        final_score REAL, similarity_score REAL, skill_coverage REAL,
        matched_skills TEXT, missing_skills TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")
    return conn


def save_candidate(name, job_title, result):
    with get_conn() as c:
        cur = c.execute(
            "INSERT INTO candidates (name, job_title, final_score, similarity_score, skill_coverage,"
            " matched_skills, missing_skills) VALUES (?,?,?,?,?,?,?)",
            (name, job_title, result["final_score"], result["similarity_score"], result["skill_coverage"],
             json.dumps(result["matched_skills"]), json.dumps(result["missing_skills"])))
        return cur.lastrowid


def list_candidates():
    with get_conn() as c:
        return [dict(r) for r in c.execute("SELECT * FROM candidates ORDER BY final_score DESC")]
