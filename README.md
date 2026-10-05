# AI & Data Science Job Market and Education Dashboard (AISDST)

> **Interactive Analytical Dashboard & Skills Gap Intelligence System**  
> Developed for Academic Executives, Students, and Labor Policy Makers  
> Powered by Python Dash (Plotly), Pandas, and Modern Web Standards

---

## 📌 Executive Summary (ภาพรวมโครงการ)

The **AI & Data Science Job Market and Education Dashboard (AISDST)** is an end-to-end analytical platform designed to bridge the critical gap between higher education curricula and labor market dynamics across **Artificial Intelligence (AI)**, **Data Science (DS)**, and **Statistics (ST)**.

### Core Analytical Objectives:
1. **Curriculum & Talent Pipeline Analysis (ศักยภาพการผลิตและทักษะในหลักสูตร):** Quantify graduate output across degree programs, track 1-to-3-year post-graduation employment velocity, and benchmark program tuition fees against curriculum skill offerings.
2. **Labor Market Demand Intelligence (ความต้องการของตลาดแรงงานจริง):** Monitor active job openings, rank high-demand skills, analyze industry and employer distributions, and examine salary structures stratified by experience levels.
3. **Skills Mismatch & Gap Analysis (การวิเคราะห์ช่องว่างทักษะ):** Correlate skills taught in university mandatory courses with market expectations to highlight talent shortages, over-supplies, and unaddressed competencies for curriculum modernizations.

---

## 🛠️ Architecture & Technical Stack

```
┌────────────────────────────────────────────────────────────────────────┐
│                        Dashboard_AISDST_jobs                           │
├───────────────────────────────────┬────────────────────────────────────┤
│   Plotly Dash Full Web Platform   │   Standalone Executive Preview     │
│   (Python / Dash / Pandas)        │   (Single-file HTML / Tailwind)    │
├───────────────────────────────────┼────────────────────────────────────┤
│ • Interactive Multi-Tab Layout    │ • Single-File HTML Dashboard       │
│ • Reactive Cross-filtering Callbacks│ • ContentEditable Dynamic KPIs    │
│ • Deep Drill-down & Analytics     │ • Chart.js Interactive Visuals     │
│ • Rich Plotly Graph Engine        │ • Zero Build Step Needed           │
└───────────────────────────────────┴────────────────────────────────────┘
```

### Technology Highlights:
- **Core Backend & Data Layer:** Python 3.14+, Pandas for data manipulation, NumPy for statistical aggregations.
- **Frontend / Dashboard Framework:** Plotly Dash (`dash`, `dash-bootstrap-components`, `plotly.graph_objects`, `plotly.express`).
- **Reactive Engine:** Real-time `@app.callback` cross-filtering allowing selections on one visual (e.g., academic year, program, experience level) to immediately propagate to all components within that tab.
- **Lightweight Portable Dashboard:** Standalone responsive HTML (`index.html`) featuring Tailwind CSS (via CDN) and Chart.js for executive presentations and open data distribution.

---

## 📊 Dashboard Modules & Features

The platform provides 3 dedicated analytical tabs in the Dash application, supplemented by a standalone open data summary:

### 🎓 Tab 1: Education & Graduates (ปริมาณคนที่จบ และ Skills ที่เรียนมา)
- **Graduates Output Trend:** Multi-line & bar timeline tracking graduate output across AI, Data Science, and Statistics programs.
- **Curriculum & Skills Tag Cloud / Table:** Detailed breakdown of mandatory coursework categorized into core skill domains (e.g., Machine Learning, Agentic AI, Cloud & MLOps, Statistical Inference).
- **Post-Graduation Employment Rate:** Stacked progression tracking employment ratios achieved at Year 1, Year 2, and Year 3 post-graduation.
- **Tuition Fee & ROI Benchmark:** Comparative cost analysis across academic programs with interactive KPI summaries.

### 💼 Tab 2: Job Market Demand (ปริมาณงานที่จ้าง และ Skills ที่ต้องการ)
- **Job Market Openings & Growth Velocity:** Real-time KPI counters and time-series tracking active postings across AI, Data Science, and Statistics.
- **Top Demanded Skills Ranking:** Horizontal bar chart and word frequency representation of required competencies extracted from employer job requisitions.
- **Industry & Employer Treemap:** Hierarchical visualization of top hiring sectors (FinTech, HealthTech, E-Commerce, Consulting, etc.) and company tiers.
- **Salary Band Distributions:** Interactive box-plots and salary range spreads across seniority levels (Entry-level, Mid-level, Senior, Expert).

### 🔍 Tab 3: Skills Mismatch Analysis (วิเคราะห์ช่องว่างทักษะ)
- **Curriculum vs. Market Radar / Diverging Chart:** Direct side-by-side contrast of academic skill coverage versus industry demand frequency, pinpointing **Shortage** and **Over-supply** areas.
- **Critical Gap Matrix (Gap Analysis Table):** Filterable discrepancy table isolating high-demand skills that currently lack mandatory academic course coverage.

### 🌐 Standalone Executive HTML Dashboard (`index.html`)
- Standalone HTML5 dashboard with dark-mode UI.
- Editable KPI metrics using HTML5 `contenteditable="true"`.
- Chart.js interactive visualizations for salary ranges, global hiring geography, and skill growth trajectories.
- Curated reference catalog of Open Data sources.

---

## 📁 Repository Structure

```
Dashboard_AISDST_jobs/
├── README.md                      # Comprehensive project documentation
├── PROJECT_STATUS.md              # Real-time implementation progress tracker
├── requirements.txt               # Python package dependencies
├── app.py                         # Plotly Dash primary application entry point
├── index.html                     # Standalone executive HTML dashboard
├── data/
│   ├── education_data.csv         # University curriculum & graduate outcomes dataset
│   ├── job_market_data.csv        # Labor market demand & salary dataset
│   └── generate_datasets.py       # Reproducible data generation & curation script
├── src/
│   ├── __init__.py
│   ├── components/                # Layout components for Tabs 1, 2, 3
│   │   ├── tab_education.py
│   │   ├── tab_market.py
│   │   └── tab_mismatch.py
│   ├── callbacks.py               # Reactive Dash cross-filtering logic
│   └── data_loader.py             # Data ingestion, schema validation & helpers
└── assets/
    └── custom.css                 # Dark-mode dashboard theme & polish
```

---

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.10+ (tested on Python 3.14)
- Modern web browser (Chrome, Edge, Firefox, Safari)

### 1. Installation
Clone the repository and install required Python packages:

```bash
git clone https://github.com/apichaia/Dashboard_AISDST_jobs.git
cd Dashboard_AISDST_jobs
pip install -r requirements.txt
```

### 2. Generate Synthetic Datasets (Optional / Included)
To regenerate or inspect the baseline datasets:
```bash
python data/generate_datasets.py
```

### 3. Launch the Interactive Dash Platform
Start the local Dash analytical server:
```bash
python app.py
```
Open your browser and navigate to:  
👉 **http://127.0.0.1:8050**

### 4. Open the Standalone Executive HTML Dashboard
Simply open `index.html` in any web browser without needing any server:
```bash
# Windows
start index.html
```

---

## 🔄 Cross-Filtering Interaction Guide
1. **In Tab 1 (Education):** Selecting a specific curriculum or academic year filter automatically adjusts graduate trends, updates the course table, and recalculates employment statistics.
2. **In Tab 2 (Job Market):** Filtering by job category (AI, Data Science, Statistics) or experience level instantly recalibrates salary box-plots and skills demand charts.
3. **In Tab 3 (Skills Mismatch):** Selecting an academic track immediately recomputes the radar overlap and refreshes the curriculum deficit recommendations table.

---

## 📄 Documentation Sources
- `gemini-code-1791194961259.md`: Business Requirements Document (BRD) - AI & Data Science Job Market and Education Dashboard.
- `gemini-code-1791193677901.md`: Interactive HTML Agent Handoff Specification for Open Data Job Market Metrics.

---

## 📜 License
This project is licensed under the MIT License - open for educational and policy research.
