"""
src/data_loader.py
Data loading, preprocessing, filtering, and cross-tab metrics computation.
"""

import os
from collections import Counter
import pandas as pd
import numpy as np

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")

def load_data():
    """Load education, job market, and curriculum courses datasets."""
    edu_path = os.path.join(DATA_DIR, "education_data.csv")
    jobs_path = os.path.join(DATA_DIR, "job_market_data.csv")
    courses_path = os.path.join(DATA_DIR, "curriculum_courses.csv")
    
    if not os.path.exists(edu_path) or not os.path.exists(jobs_path):
        from data.generate_datasets import main as gen_main
        gen_main()
        
    df_edu = pd.read_csv(edu_path)
    df_jobs = pd.read_csv(jobs_path)
    df_courses = pd.read_csv(courses_path) if os.path.exists(courses_path) else pd.DataFrame()
    
    return df_edu, df_jobs, df_courses

# Preload static datasets into memory
DF_EDU, DF_JOBS, DF_COURSES = load_data()

PROGRAM_TO_FIELD = {
    "Artificial Intelligence (AI)": "AI",
    "Data Science (DS)": "Data Science",
    "Statistics & Analytics (ST)": "Statistics"
}

FIELD_TO_PROGRAM = {v: k for k, v in PROGRAM_TO_FIELD.items()}


def get_education_metrics(selected_programs=None, selected_years=None):
    """
    Filter and compute analytics for Tab 1 (Education & Graduates).
    """
    df = DF_EDU.copy()
    
    if selected_programs:
        if isinstance(selected_programs, str):
            selected_programs = [selected_programs]
        df = df[df["program_name"].isin(selected_programs)]
        
    if selected_years:
        if isinstance(selected_years, int):
            selected_years = [selected_years]
        df = df[df["academic_year"].isin(selected_years)]
        
    # Filter courses
    df_c = DF_COURSES.copy()
    if selected_programs:
        df_c = df_c[df_c["program_name"].isin(selected_programs)]
        
    return df, df_c


def get_job_market_metrics(selected_fields=None, selected_levels=None, selected_years=None):
    """
    Filter and compute analytics for Tab 2 (Job Market Demand).
    """
    df = DF_JOBS.copy()
    
    if selected_fields:
        if isinstance(selected_fields, str):
            selected_fields = [selected_fields]
        df = df[df["field"].isin(selected_fields)]
        
    if selected_levels:
        if isinstance(selected_levels, str):
            selected_levels = [selected_levels]
        df = df[df["experience_level"].isin(selected_levels)]
        
    if selected_years:
        if isinstance(selected_years, int):
            selected_years = [selected_years]
        df = df[df["posting_year"].isin(selected_years)]
        
    # Compute Top Skills Frequency
    all_skills = []
    for skills_str in df["required_skills"].dropna():
        for s in skills_str.split(", "):
            if s.strip():
                all_skills.append(s.strip())
                
    skill_counts = Counter(all_skills)
    df_skills = pd.DataFrame(skill_counts.most_common(20), columns=["skill", "count"])
    if not df_skills.empty:
        total_postings = len(df)
        df_skills["demand_share_pct"] = (df_skills["count"] / max(total_postings, 1) * 100).round(1)
        
    return df, df_skills


def get_skills_mismatch_metrics(selected_program=None):
    """
    Tab 3: Compare skills taught in university coursework vs demanded in market.
    """
    if not selected_program or selected_program == "All Programs":
        target_field = None
        df_c = DF_COURSES.copy()
        df_j = DF_JOBS.copy()
    else:
        target_field = PROGRAM_TO_FIELD.get(selected_program, "Data Science")
        df_c = DF_COURSES[DF_COURSES["program_name"] == selected_program].copy()
        df_j = DF_JOBS[DF_JOBS["field"] == target_field].copy()
        
    # 1. Count taught skills frequency in curriculum
    taught_counter = Counter()
    for skills_str in df_c["key_skills"].dropna():
        for s in skills_str.split(", "):
            taught_counter[s.strip()] += 1
            
    # 2. Count required skills frequency in job market postings
    market_counter = Counter()
    for skills_str in df_j["required_skills"].dropna():
        for s in skills_str.split(", "):
            market_counter[s.strip()] += 1
            
    # Union of key skills found in market (top 20) + top taught skills
    top_market_skills = [s for s, _ in market_counter.most_common(16)]
    all_tracked_skills = list(dict.fromkeys(top_market_skills + list(taught_counter.keys())))[:20]
    
    total_market_jobs = max(len(df_j), 1)
    total_courses = max(len(df_c), 1)
    
    comparison_rows = []
    for skill in all_tracked_skills:
        m_count = market_counter.get(skill, 0)
        c_count = taught_counter.get(skill, 0)
        
        market_pct = round((m_count / total_market_jobs) * 100, 1)
        # Normalized course coverage score (out of 100)
        curriculum_score = min(100.0, round((c_count / max(total_courses * 0.35, 1)) * 100, 1))
        
        # Determine gap status
        if market_pct >= 20.0 and c_count == 0:
            status = "🚨 Critical Market Shortage"
            action = "Urgent: Add mandatory course / lab"
        elif market_pct >= 35.0 and c_count <= 1:
            status = "⚠️ Moderate Deficit"
            action = "Expand curriculum depth & projects"
        elif market_pct >= 20.0 and c_count >= 1:
            status = "✅ Strong Market Alignment"
            action = "Maintain curriculum excellence"
        elif market_pct < 15.0 and c_count >= 2:
            status = "📚 Academic Foundational"
            action = "Ensure practical industry context"
        else:
            status = "⚖️ Balanced"
            action = "Monitor market movement"
            
        gap_diff = round(market_pct - curriculum_score, 1)
        
        comparison_rows.append({
            "skill": skill,
            "market_demand_pct": market_pct,
            "market_openings_count": m_count,
            "curriculum_score": curriculum_score,
            "curriculum_courses_count": c_count,
            "gap_difference": gap_diff,
            "status": status,
            "action_recommendation": action
        })
        
    df_gap = pd.DataFrame(comparison_rows).sort_values(by="gap_difference", ascending=False)
    
    # Critical Missing Skills table: market demand > 15% but 0 courses taught
    df_critical_missing = df_gap[
        (df_gap["market_demand_pct"] >= 15.0) & (df_gap["curriculum_courses_count"] == 0)
    ].copy()
    
    return df_gap, df_critical_missing
