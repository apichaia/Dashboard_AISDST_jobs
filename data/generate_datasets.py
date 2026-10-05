"""
generate_datasets.py
Generates realistic benchmark datasets for the AI & Data Science Job Market
and Education Dashboard (AISDST).
"""

import os
import random
import numpy as np
import pandas as pd

# Set reproducible seed
np.random.seed(42)
random.seed(42)

DATA_DIR = os.path.dirname(os.path.abspath(__file__))
os.makedirs(DATA_DIR, exist_ok=True)

# ---------------------------------------------------------
# 1. GENERATE EDUCATION DATA (education_data.csv)
# ---------------------------------------------------------

PROGRAMS = [
    {
        "program_name": "Artificial Intelligence (AI)",
        "field": "AI",
        "tuition_fee_thb": 72000,
        "tuition_fee_usd": 2050,
        "base_grads": 110,
        "growth": 1.15,
        "emp_rates": (86.5, 93.0, 97.2),
        "courses": [
            ("AI101", "Introduction to Artificial Intelligence", "Foundations", "Python, Logic, Search Algorithms"),
            ("AI201", "Deep Learning & Neural Networks", "Machine Learning", "PyTorch, TensorFlow, Computer Vision, CNN"),
            ("AI301", "Natural Language Processing", "NLP & GenAI", "NLP, Transformers, HuggingFace"),
            ("AI302", "Robotics & Computer Vision", "Applied AI", "OpenCV, Robotics, Sensor Fusion"),
            ("AI401", "AI Ethics, Governance & Safety", "Ethics & Policy", "AI Safety, Bias Mitigation, Governance"),
            ("CS102", "Data Structures and Algorithms", "Computer Science", "Algorithms, Python, C++, Data Structures"),
            ("MA201", "Linear Algebra & Optimization", "Mathematics", "Linear Algebra, Calculus, Optimization"),
            ("AI490", "Senior AI Capstone Project", "Project", "Git, Problem Solving, Prototyping")
        ]
    },
    {
        "program_name": "Data Science (DS)",
        "field": "Data Science",
        "tuition_fee_thb": 65000,
        "tuition_fee_usd": 1850,
        "base_grads": 140,
        "growth": 1.10,
        "emp_rates": (88.0, 94.5, 98.0),
        "courses": [
            ("DS101", "Foundations of Data Science", "Foundations", "Python, Exploratory Data Analysis, Pandas"),
            ("DS201", "Data Wrangling and Database Systems", "Data Engineering", "SQL, Relational Databases, ETL"),
            ("DS301", "Supervised and Unsupervised Learning", "Machine Learning", "Scikit-Learn, Regression, Classification"),
            ("DS302", "Big Data Analytics and Cloud Basics", "Big Data", "Spark, Hadoop, Cloud Infrastructure"),
            ("DS401", "Data Visualization & Storytelling", "Visualization", "Tableau, PowerBI, Plotly, Dashboarding"),
            ("ST202", "Applied Probability and Inference", "Statistics", "Hypothesis Testing, Bayesian Inference"),
            ("CS101", "Programming Fundamentals", "Computer Science", "Python, Git, OOP"),
            ("DS490", "Enterprise Data Science Practicum", "Project", "End-to-End Analytics, Communication")
        ]
    },
    {
        "program_name": "Statistics & Analytics (ST)",
        "field": "Statistics",
        "tuition_fee_thb": 48000,
        "tuition_fee_usd": 1370,
        "base_grads": 95,
        "growth": 1.04,
        "emp_rates": (82.0, 90.0, 95.5),
        "courses": [
            ("ST101", "Mathematical Statistics I", "Statistics", "Probability Theory, Distributions"),
            ("ST201", "Mathematical Statistics II", "Statistics", "Statistical Inference, Maximum Likelihood"),
            ("ST301", "Regression Analysis & ANOVA", "Applied Statistics", "Linear Models, R, Diagnostics"),
            ("ST302", "Time Series Analysis & Forecasting", "Applied Statistics", "ARIMA, Forecasting, Econometrics"),
            ("ST401", "Multivariate Statistical Analysis", "Advanced Stats", "PCA, Factor Analysis, Clustering"),
            ("ST402", "Biostatistics & Experimental Design", "Domain Applied", "Clinical Trials, A/B Testing, Survival Analysis"),
            ("CS105", "Statistical Computing with R & Python", "Computing", "R, Python, Simulation"),
            ("ST490", "Senior Statistics Thesis Project", "Project", "Statistical Modeling, Academic Writing")
        ]
    }
]

YEARS = [2021, 2022, 2023, 2024, 2025]

edu_records = []

for prog in PROGRAMS:
    for idx, year in enumerate(YEARS):
        grads = int(prog["base_grads"] * (prog["growth"] ** idx) + random.randint(-4, 5))
        # Add slight natural variation to employment rates
        y1_rate = round(min(99.0, prog["emp_rates"][0] + idx * 0.8 + random.uniform(-1.0, 1.0)), 1)
        y2_rate = round(min(99.5, prog["emp_rates"][1] + idx * 0.5 + random.uniform(-0.8, 0.8)), 1)
        y3_rate = round(min(100.0, prog["emp_rates"][2] + idx * 0.3 + random.uniform(-0.5, 0.5)), 1)
        
        # Format courses as JSON string or delimited list
        course_list_str = "; ".join([f"{c[0]}: {c[1]} [{c[2]}]" for c in prog["courses"]])
        taught_skills_set = set()
        for c in prog["courses"]:
            for s in c[3].split(", "):
                taught_skills_set.add(s)
        skills_str = ", ".join(sorted(taught_skills_set))

        edu_records.append({
            "academic_year": year,
            "program_name": prog["program_name"],
            "field": prog["field"],
            "graduates_count": grads,
            "tuition_fee_thb": prog["tuition_fee_thb"] + (idx * 2000),
            "tuition_fee_usd": prog["tuition_fee_usd"] + (idx * 60),
            "employment_rate_y1": y1_rate,
            "employment_rate_y2": y2_rate,
            "employment_rate_y3": y3_rate,
            "mandatory_courses": course_list_str,
            "taught_skills": skills_str,
            "total_courses_count": len(prog["courses"])
        })

df_edu = pd.DataFrame(edu_records)
edu_path = os.path.join(DATA_DIR, "education_data.csv")
df_edu.to_csv(edu_path, index=False, encoding="utf-8")
print(f"Generated {len(df_edu)} education rows -> {edu_path}")

# Also generate a normalized courses catalog for easy tab rendering
course_records = []
for prog in PROGRAMS:
    for c in prog["courses"]:
        course_records.append({
            "program_name": prog["program_name"],
            "field": prog["field"],
            "course_code": c[0],
            "course_name": c[1],
            "skill_category": c[2],
            "key_skills": c[3]
        })
df_courses = pd.DataFrame(course_records)
courses_path = os.path.join(DATA_DIR, "curriculum_courses.csv")
df_courses.to_csv(courses_path, index=False, encoding="utf-8")
print(f"Generated {len(df_courses)} courses -> {courses_path}")


# ---------------------------------------------------------
# 2. GENERATE JOB MARKET DATA (job_market_data.csv)
# ---------------------------------------------------------

COMPANIES = [
    {"name": "SCB 10X", "industry": "FinTech / Web3", "size": "Medium (50-250)", "scale_factor": 1.25},
    {"name": "Agoda", "industry": "E-Commerce / Travel", "size": "Enterprise (>250)", "scale_factor": 1.35},
    {"name": "Kasikorn Business-Technology Group (KBTG)", "industry": "FinTech / Banking", "size": "Enterprise (>250)", "scale_factor": 1.20},
    {"name": "Line Man Wongnai", "industry": "On-Demand Platform", "size": "Enterprise (>250)", "scale_factor": 1.15},
    {"name": "True Digital Group", "industry": "Telecom & Media", "size": "Enterprise (>250)", "scale_factor": 1.10},
    {"name": "Sea Group / Shopee", "industry": "E-Commerce / Gaming", "size": "Enterprise (>250)", "scale_factor": 1.22},
    {"name": "PTT Digital Solutions", "industry": "Energy & Industrial", "size": "Enterprise (>250)", "scale_factor": 1.10},
    {"name": "AIS (Advanced Info Service)", "industry": "Telecom & Cloud", "size": "Enterprise (>250)", "scale_factor": 1.15},
    {"name": "Bitkub Capital Group", "industry": "FinTech / Crypto", "size": "Medium (50-250)", "scale_factor": 1.18},
    {"name": "Sertis AI", "industry": "AI Consultancy", "size": "Medium (50-250)", "scale_factor": 1.20},
    {"name": "Sunday Insurance", "industry": "InsurTech", "size": "Medium (50-250)", "scale_factor": 1.05},
    {"name": "Vulcan Coalition", "industry": "Social AI Enterprise", "size": "Startup (<50)", "scale_factor": 0.90},
    {"name": "Robinhood Delivery", "industry": "FoodTech / Logistics", "size": "Medium (50-250)", "scale_factor": 1.05},
    {"name": "BDMS Health Analytics", "industry": "HealthTech", "size": "Enterprise (>250)", "scale_factor": 1.12},
    {"name": "DataRockie Labs", "industry": "Analytics Consulting", "size": "Startup (<50)", "scale_factor": 0.95},
    {"name": "Muang Thai Life Tech", "industry": "InsurTech / Finance", "size": "Enterprise (>250)", "scale_factor": 1.08},
]

ROLES_DEFINITION = {
    "AI": {
        "titles": [
            "AI Engineer", "Machine Learning Engineer", "LLM Application Developer",
            "Agentic AI Engineer", "Computer Vision Specialist", "NLP Research Scientist",
            "MLOps Infrastructure Engineer"
        ],
        "core_skills": [
            "Python", "PyTorch", "TensorFlow", "Docker", "Kubernetes", "MLOps",
            "Agentic AI", "Transformers", "LangChain", "Vector Databases", "Git", "Cloud Infrastructure (AWS/GCP)"
        ],
        "salary_base": {"Entry-level": (45000, 70000), "Mid-level": (75000, 130000), "Senior": (135000, 220000), "Expert": (220000, 380000)}
    },
    "Data Science": {
        "titles": [
            "Data Scientist", "Senior Data Scientist", "Analytics Engineer",
            "Machine Learning Analyst", "Quantitative Researcher", "Lead Decision Scientist",
            "Customer Insights Data Scientist"
        ],
        "core_skills": [
            "Python", "SQL", "Pandas", "Scikit-Learn", "A/B Testing", "Spark",
            "Tableau", "PowerBI", "Cloud Infrastructure (AWS/GCP)", "Data Modeling", "Feature Engineering", "Git"
        ],
        "salary_base": {"Entry-level": (40000, 65000), "Mid-level": (70000, 120000), "Senior": (125000, 200000), "Expert": (200000, 340000)}
    },
    "Statistics": {
        "titles": [
            "Statistician", "Biostatistician", "Risk & Credit Model Specialist",
            "Econometrician", "Statistical Data Analyst", "Actuarial Data Modeler",
            "Experimental Design Specialist"
        ],
        "core_skills": [
            "R", "Python", "SQL", "Statistical Modeling", "Hypothesis Testing",
            "Time Series Analysis", "SAS", "SPSS", "Survival Analysis", "Monte Carlo Simulation", "Tableau"
        ],
        "salary_base": {"Entry-level": (35000, 55000), "Mid-level": (58000, 95000), "Senior": (100000, 165000), "Expert": (170000, 280000)}
    }
}

EXPERIENCE_LEVELS = ["Entry-level", "Mid-level", "Senior", "Expert"]
EXP_WEIGHTS = [0.35, 0.38, 0.20, 0.07]  # Real market weight: more entry/mid openings

job_records = []
job_id_counter = 1001

for company in COMPANIES:
    # Each company posts 20-45 positions across AI, DS, and ST
    num_jobs = random.randint(22, 45)
    for _ in range(num_jobs):
        field = random.choices(["AI", "Data Science", "Statistics"], weights=[0.45, 0.38, 0.17])[0]
        field_cfg = ROLES_DEFINITION[field]
        
        title = random.choice(field_cfg["titles"])
        exp_level = random.choices(EXPERIENCE_LEVELS, weights=EXP_WEIGHTS)[0]
        
        # Skill assignment: 3 to 6 required skills from the pool + occasional cross-domain skills
        num_skills = random.randint(3, 6)
        selected_skills = random.sample(field_cfg["core_skills"], min(num_skills, len(field_cfg["core_skills"])))
        
        # Calculate salary with company scale factor
        min_base, max_base = field_cfg["salary_base"][exp_level]
        scale = company["scale_factor"] * random.uniform(0.92, 1.08)
        
        min_sal = int(round((min_base * scale) / 1000) * 1000)
        max_sal = int(round((max_base * scale) / 1000) * 1000)
        avg_sal = int((min_sal + max_sal) / 2)
        
        # Posting year/date simulation (2023-2025)
        posting_year = random.choices([2023, 2024, 2025], weights=[0.20, 0.40, 0.40])[0]
        posting_month = random.randint(1, 12)
        posting_day = random.randint(1, 28)
        posting_date = f"{posting_year}-{posting_month:02d}-{posting_day:02d}"
        
        job_records.append({
            "job_id": f"JOB-{job_id_counter}",
            "job_title": title,
            "field": field,
            "company_name": company["name"],
            "industry": company["industry"],
            "company_size": company["size"],
            "experience_level": exp_level,
            "min_salary_thb": min_sal,
            "max_salary_thb": max_sal,
            "avg_salary_thb": avg_sal,
            "min_salary_usd": int(min_sal / 35),
            "max_salary_usd": int(max_sal / 35),
            "avg_salary_usd": int(avg_sal / 35),
            "required_skills": ", ".join(selected_skills),
            "primary_skill": selected_skills[0],
            "posting_date": posting_date,
            "posting_year": posting_year,
            "is_remote_friendly": random.choice([True, False, True]) # 66% remote friendly
        })
        job_id_counter += 1

df_jobs = pd.DataFrame(job_records)
jobs_path = os.path.join(DATA_DIR, "job_market_data.csv")
df_jobs.to_csv(jobs_path, index=False, encoding="utf-8")
print(f"Generated {len(df_jobs)} job postings -> {jobs_path}")

print("Dataset generation completed successfully!")
