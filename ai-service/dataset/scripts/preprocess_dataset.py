import os
import re
import pandas as pd
from validate_dataset import validate
from generate_statistics import generate_stats
from export_filtered_dataset import export

def clean_html(text):
    if not isinstance(text, str):
        return ""
    clean = re.compile(r"<[^>]+>")
    text = clean.sub("", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def limit_skills(skills_str):
    if not isinstance(skills_str, str):
        return ""
    parts = [p.strip() for p in skills_str.split(",") if p.strip()]
    selected = []
    current_len = 0
    for part in parts:
        if len(part) > 40:
            continue
        if current_len + len(part) + 2 > 180:
            break
        selected.append(part)
        current_len += len(part) + 2
        
    if not selected and parts:
        selected = [parts[0][:40]]
    return ", ".join(selected)

def load_and_filter(original_dir):
    # 1. Read original files
    print("\n[Preprocessing] Reading CSV files...")
    postings_df = pd.read_csv(os.path.join(original_dir, "job_postings.csv"))
    skills_df = pd.read_csv(os.path.join(original_dir, "job_skills.csv"))
    summary_df = pd.read_csv(os.path.join(original_dir, "job_summary.csv"))
    
    # 2. Merge dataframes on job_link
    print("[Preprocessing] Merging dataframes...")
    merged_df = pd.merge(postings_df, skills_df, on="job_link", how="inner")
    merged_df = pd.merge(merged_df, summary_df, on="job_link", how="inner")
    
    # 3. Filter technical internships and entry-level software roles
    print("[Preprocessing] Filtering tech roles...")
    tech_keywords = [
        "software", "developer", "engineer", "programmer", "data", "analyst", 
        "scientist", "ml", "ai", "intelligence", "devops", "cloud", 
        "cybersecurity", "security", "mobile", "ios", "android", "qa", 
        "testing", "ui", "ux", "design", "frontend", "backend", "full stack"
    ]
    tech_pattern = "|".join(tech_keywords)
    
    exclude_keywords = ["manager", "director", "head of", "lead", "principal", "staff", "senior", "sr."]
    exclude_pattern = "|".join(exclude_keywords)
    seniority_levels = ["Internship", "Entry level", "Associate"]
    
    is_tech = merged_df["job_title"].str.lower().str.contains(tech_pattern, na=False)
    is_not_senior = ~merged_df["job_title"].str.lower().str.contains(exclude_pattern, na=False)
    is_entry = merged_df["job_level"].isin(seniority_levels) | merged_df["job_title"].str.lower().str.contains("intern|trainee|associate", na=False)
    
    filtered_df = merged_df[is_tech & is_not_senior & is_entry].copy()
    
    # 4. Remove duplicates
    filtered_df.drop_duplicates(subset=["job_title", "company"], keep="first", inplace=True)
    
    # 5. Remove incomplete rows
    filtered_df.dropna(subset=["job_title", "company", "job_summary", "job_skills"], inplace=True)
    filtered_df = filtered_df[
        (filtered_df["job_title"].str.strip() != "") &
        (filtered_df["company"].str.strip() != "") &
        (filtered_df["job_summary"].str.strip() != "")
    ]
    
    # 6. Clean HTML and Limit Skills
    print("[Preprocessing] Cleaning HTML from summaries and limiting skills...")
    filtered_df["cleaned_summary"] = filtered_df["job_summary"].apply(clean_html)
    filtered_df["limited_skills"] = filtered_df["job_skills"].apply(limit_skills)
    
    return filtered_df

def preprocess():
    print("=== STARTING DATASET PREPROCESSING ===")
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    original_dir = os.path.join(base_dir, "original")
    processed_dir = os.path.join(base_dir, "processed")
    
    # Step 1: Load and filter the raw dataset
    df = load_and_filter(original_dir)
    
    # Step 2: Map schemas and export to CSV
    final_df = export(df, processed_dir)
    
    # Step 3: Validate the final exported format
    validate(final_df)
    
    # Step 4: Generate distribution statistics
    generate_stats(final_df)
    
    print("\n=== PREPROCESSING COMPLETE ===")

if __name__ == "__main__":
    preprocess()
