"""ETL: extract candidates from SQLite -> clean/transform -> export structured CSV."""
import json
import os
import pandas as pd
from app import db


def run(out_dir="exports"):
    df = pd.DataFrame(db.list_candidates())                              # Extract
    if df.empty:
        print("No candidates to export."); return None
    df["name"] = df["name"].str.strip().str.title()                      # Clean
    df = df.drop_duplicates(subset=["name", "job_title"], keep="last")
    for col in ("matched_skills", "missing_skills"):                     # Transform
        df[col] = df[col].apply(lambda s: ", ".join(json.loads(s)))
    df["shortlisted"] = df["final_score"] >= 50
    os.makedirs(out_dir, exist_ok=True)                                  # Load
    path = f"{out_dir}/candidates_clean.csv"
    df.to_csv(path, index=False)
    print(f"Exported {len(df)} candidates -> {path}")
    return path


if __name__ == "__main__":
    run()
