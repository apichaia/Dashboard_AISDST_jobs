"""
src/callbacks.py
Reactive cross-filtering Dash callbacks for all three tabs.
Ensures cross-filtering and synchronization between visual elements.
"""

from dash import Input, Output, State, html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

from src.data_loader import (
    DF_EDU, DF_JOBS, DF_COURSES,
    get_education_metrics,
    get_job_market_metrics,
    get_skills_mismatch_metrics,
    PROGRAM_TO_FIELD
)

BASE_DARK_TEMPLATE = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(17,24,39,0.3)",
    font=dict(family="Inter, -apple-system, sans-serif", color="#e5e7eb", size=11),
    margin=dict(l=45, r=20, t=35, b=40),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
        bgcolor="rgba(0,0,0,0)"
    )
)

def apply_dark_layout(fig, **kwargs):
    """Safely merge default dark styling with custom overrides."""
    layout_dict = dict(
        xaxis=dict(gridcolor="#1f2937", zerolinecolor="#374151"),
        yaxis=dict(gridcolor="#1f2937", zerolinecolor="#374151"),
        **BASE_DARK_TEMPLATE
    )
    for k, v in kwargs.items():
        if k in layout_dict and isinstance(layout_dict[k], dict) and isinstance(v, dict):
            merged = layout_dict[k].copy()
            merged.update(v)
            layout_dict[k] = merged
        else:
            layout_dict[k] = v
    fig.update_layout(**layout_dict)
    return fig

COLOR_PALETTE = {
    "Artificial Intelligence (AI)": "#38bdf8",     # Cyan / Sky
    "Data Science (DS)": "#a855f7",               # Purple
    "Statistics & Analytics (ST)": "#10b981",     # Emerald
    "AI": "#38bdf8",
    "Data Science": "#a855f7",
    "Statistics": "#10b981"
}


# =========================================================================
# TAB 1 LOGIC: EDUCATION & GRADUATES
# =========================================================================

def handle_edu_trend_click(click_data, current_val):
    if not click_data or "points" not in click_data:
        return current_val
    point = click_data["points"][0]
    clicked_prog = point.get("customdata") or point.get("data", {}).get("name")
    if clicked_prog and clicked_prog in COLOR_PALETTE:
        return "ALL" if current_val == clicked_prog else clicked_prog
    return current_val


def update_tab_education(selected_program, selected_years):
    programs_filter = None if (not selected_program or selected_program == "ALL") else [selected_program]
    years_filter = selected_years if (selected_years and len(selected_years) > 0) else None

    df_e, df_c = get_education_metrics(programs_filter, years_filter)

    # 1. Compute KPIs
    total_grads = f"{df_e['graduates_count'].sum():,}"
    avg_emp_y1 = f"{df_e['employment_rate_y1'].mean():.1f}%" if not df_e.empty else "N/A"
    avg_tuition = f"฿{int(df_e['tuition_fee_thb'].mean()):,}" if not df_e.empty else "N/A"
    total_courses_count = f"{len(df_c)}"

    # 2. Graduates Production Trend Chart
    fig_trend = go.Figure()
    all_unique_progs = df_e["program_name"].unique()
    for prog in all_unique_progs:
        sub = df_e[df_e["program_name"] == prog].sort_values("academic_year")
        color = COLOR_PALETTE.get(prog, "#38bdf8")
        fig_trend.add_trace(go.Bar(
            x=sub["academic_year"],
            y=sub["graduates_count"],
            name=prog,
            marker=dict(color=color, opacity=0.85, line=dict(color=color, width=1.5)),
            customdata=[prog] * len(sub),
            hovertemplate="<b>%{x}</b><br>Program: " + prog + "<br>Graduates: <b>%{y}</b><extra></extra>"
        ))
    apply_dark_layout(
        fig_trend,
        barmode="group",
        xaxis_title="Academic Year",
        yaxis_title="Graduates Count"
    )

    # 3. Post-Graduation Employment Velocity
    fig_emp = go.Figure()
    emp_summary = df_e.groupby("program_name")[["employment_rate_y1", "employment_rate_y2", "employment_rate_y3"]].mean().reset_index()
    stages = [
        ("Year 1", "employment_rate_y1", "#3b82f6"),
        ("Year 2", "employment_rate_y2", "#10b981"),
        ("Year 3", "employment_rate_y3", "#f59e0b")
    ]
    for stage_label, col, col_hex in stages:
        fig_emp.add_trace(go.Bar(
            x=emp_summary["program_name"].apply(lambda x: x.split(" (")[0]),
            y=emp_summary[col].round(1),
            name=stage_label,
            text=emp_summary[col].apply(lambda v: f"{v:.1f}%"),
            textposition="inside",
            marker=dict(color=col_hex, opacity=0.85),
            hovertemplate="<b>%{x}</b><br>" + stage_label + " Rate: <b>%{y}%</b><extra></extra>"
        ))
    apply_dark_layout(
        fig_emp,
        barmode="group",
        yaxis=dict(range=[70, 102], gridcolor="#1f2937", title="Employment Rate (%)")
    )

    # 4. Tuition Fees Benchmark
    fig_tuition = go.Figure()
    tuition_summary = df_e.groupby("program_name")["tuition_fee_thb"].mean().reset_index()
    for idx, row in tuition_summary.iterrows():
        p_name = row["program_name"]
        c = COLOR_PALETTE.get(p_name, "#06b6d4")
        fig_tuition.add_trace(go.Bar(
            x=[p_name.split(" (")[0]],
            y=[row["tuition_fee_thb"]],
            name=p_name,
            marker=dict(color=c, opacity=0.9),
            text=[f"฿{int(row['tuition_fee_thb']):,}"],
            textposition="outside",
            hovertemplate="<b>%{x}</b><br>Annual Fee: <b>฿%{y:,}</b><extra></extra>"
        ))
    max_fee = max(tuition_summary["tuition_fee_thb"] if not tuition_summary.empty else [100000]) * 1.25
    apply_dark_layout(
        fig_tuition,
        showlegend=False,
        yaxis_title="Annual Tuition (THB)",
        yaxis=dict(range=[0, max_fee], gridcolor="#1f2937")
    )

    # 5. Course Catalog & Skills Table
    table_rows = []
    for _, c_row in df_c.iterrows():
        skills_html = [
            html.Span(s.strip(), className="skill-badge") 
            for s in str(c_row["key_skills"]).split(",") if s.strip()
        ]
        table_rows.append(html.Tr([
            html.Td(c_row["course_code"], className="font-mono text-info fw-bold"),
            html.Td(c_row["course_name"]),
            html.Td(html.Span(c_row["skill_category"], className="badge bg-secondary")),
            html.Td(skills_html)
        ]))

    courses_table = html.Table([
        html.Thead(html.Tr([
            html.Th("Code", style={"width": "12%"}),
            html.Th("Course Title", style={"width": "33%"}),
            html.Th("Category", style={"width": "20%"}),
            html.Th("Mandatory Skills Acquired", style={"width": "35%"}),
        ])),
        html.Tbody(table_rows)
    ], className="table-dark-custom")

    return (
        total_grads, avg_emp_y1, avg_tuition, total_courses_count,
        fig_trend, fig_emp, fig_tuition, courses_table
    )


# =========================================================================
# TAB 2 LOGIC: JOB MARKET DEMAND
# =========================================================================

def handle_market_treemap_click(click_data, current_field):
    if not click_data or "points" not in click_data:
        return current_field
    point = click_data["points"][0]
    label = point.get("label") or point.get("id")
    if label in ["AI", "Data Science", "Statistics"]:
        return "ALL" if current_field == label else label
    return current_field


def update_tab_market(selected_field, selected_exp, currency):
    fields_filter = None if (not selected_field or selected_field == "ALL") else [selected_field]
    exp_filter = None if (not selected_exp or selected_exp == "ALL") else [selected_exp]

    df_j, df_skills = get_job_market_metrics(fields_filter, exp_filter)

    sal_col = "avg_salary_thb" if currency == "THB" else "avg_salary_usd"
    curr_symbol = "฿" if currency == "THB" else "$"

    # 1. Compute KPIs
    total_openings = f"{len(df_j):,}"
    median_sal = f"{curr_symbol}{int(df_j[sal_col].median()):,}" if not df_j.empty else "N/A"
    top_skill = df_skills.iloc[0]["skill"] if not df_skills.empty else "N/A"
    top_ind = df_j["industry"].mode()[0] if not df_j.empty else "N/A"

    # 2. Top Demanded Skills Horizontal Bar Chart
    fig_skills = go.Figure()
    if not df_skills.empty:
        df_s_top12 = df_skills.head(12).iloc[::-1]
        fig_skills.add_trace(go.Bar(
            x=df_s_top12["count"],
            y=df_s_top12["skill"],
            orientation="h",
            marker=dict(
                color=df_s_top12["demand_share_pct"],
                colorscale="Viridis",
                showscale=True,
                colorbar=dict(title="Share %", thickness=10, len=0.7)
            ),
            text=df_s_top12["demand_share_pct"].apply(lambda v: f"{v}%"),
            textposition="outside",
            hovertemplate="Skill: <b>%{y}</b><br>Postings: <b>%{x}</b> (%{text})<extra></extra>"
        ))
    apply_dark_layout(
        fig_skills,
        xaxis_title="Requisition Frequency (Count)",
        yaxis_title=""
    )

    # 3. Salary Range Distribution by Experience Level (Box Plot)
    fig_box = px.box(
        df_j,
        x="experience_level",
        y=sal_col,
        color="field",
        category_orders={"experience_level": ["Entry-level", "Mid-level", "Senior", "Expert"]},
        color_discrete_map=COLOR_PALETTE
    )
    apply_dark_layout(
        fig_box,
        boxmode="group",
        xaxis_title="",
        yaxis_title=f"Monthly Salary ({currency})"
    )

    # 4. Industry & Company Treemap
    if not df_j.empty:
        fig_treemap = px.treemap(
            df_j,
            path=["field", "industry", "company_name"],
            color="field",
            color_discrete_map=COLOR_PALETTE
        )
        fig_treemap.update_traces(
            textinfo="label+value",
            hoverinfo="label+value+percent parent"
        )
        fig_treemap.update_layout(
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter, sans-serif", color="#ffffff")
        )
    else:
        fig_treemap = go.Figure()

    # 5. Featured Vacancies Table
    table_rows = []
    recent_jobs = df_j.head(25)
    for _, j in recent_jobs.iterrows():
        table_rows.append(html.Tr([
            html.Td(j["job_title"], className="fw-semibold text-white"),
            html.Td(j["company_name"], className="text-info"),
            html.Td(html.Span(j["experience_level"], className="badge bg-dark border border-secondary")),
            html.Td(f"{curr_symbol}{int(j[sal_col]):,}", className="font-mono text-success"),
            html.Td(html.Span(j["field"], className="badge", style={"backgroundColor": COLOR_PALETTE.get(j["field"], "#3b82f6")}))
        ]))

    jobs_table = html.Table([
        html.Thead(html.Tr([
            html.Th("Role"),
            html.Th("Company"),
            html.Th("Level"),
            html.Th("Avg Salary"),
            html.Th("Field")
        ])),
        html.Tbody(table_rows)
    ], className="table-dark-custom")

    return (
        total_openings, median_sal, top_skill, top_ind,
        fig_skills, fig_box, fig_treemap, jobs_table
    )


# =========================================================================
# TAB 3 LOGIC: SKILLS MISMATCH ANALYSIS
# =========================================================================

def update_tab_mismatch(selected_program, severity_filter):
    df_gap, df_crit = get_skills_mismatch_metrics(selected_program)

    if severity_filter == "CRITICAL":
        display_df = df_gap[df_gap["status"].str.contains("Critical", case=False)]
    elif severity_filter == "DEFICIT":
        display_df = df_gap[df_gap["status"].str.contains("Deficit", case=False)]
    elif severity_filter == "ALIGNED":
        display_df = df_gap[df_gap["status"].str.contains("Alignment|Academic", case=False)]
    else:
        display_df = df_gap

    # 1. Executive Alert Banner
    crit_count = len(df_crit)
    top_missing_skills = ", ".join(df_crit["skill"].head(3).tolist()) if crit_count > 0 else "None"
    banner = dbc.Alert([
        html.Div([
            html.H5(f"⚡ Skills Gap Diagnostic for {selected_program}", className="alert-heading fw-bold mb-1"),
            html.P(
                f"Identified {crit_count} high-priority industry competencies with ZERO mandatory course coverage. "
                f"Top market blindspots: {top_missing_skills}.",
                className="mb-0 small"
            )
        ])
    ], color="danger" if crit_count > 0 else "success", className="border-0 shadow-sm")

    # 2. Radar Chart (Curriculum Score vs Market Demand %)
    fig_radar = go.Figure()
    top_radar_df = df_gap.head(10)
    skills_labels = top_radar_df["skill"].tolist()
    market_vals = top_radar_df["market_demand_pct"].tolist()
    curriculum_vals = top_radar_df["curriculum_score"].tolist()

    if skills_labels:
        skills_labels.append(skills_labels[0])
        market_vals.append(market_vals[0])
        curriculum_vals.append(curriculum_vals[0])

    fig_radar.add_trace(go.Scatterpolar(
        r=market_vals,
        theta=skills_labels,
        fill='toself',
        name='Market Requisition Rate (%)',
        line=dict(color='#f43f5e', width=2),
        fillcolor='rgba(244, 63, 94, 0.25)'
    ))
    fig_radar.add_trace(go.Scatterpolar(
        r=curriculum_vals,
        theta=skills_labels,
        fill='toself',
        name='Curriculum Course Score (0-100)',
        line=dict(color='#38bdf8', width=2),
        fillcolor='rgba(56, 189, 248, 0.25)'
    ))
    apply_dark_layout(
        fig_radar,
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], color="#9ca3af", gridcolor="#1f2937"),
            angularaxis=dict(color="#e5e7eb", gridcolor="#1f2937"),
            bgcolor="rgba(0,0,0,0)"
        )
    )

    # 3. Diverging Bar Chart (Shortage vs Over-Supply)
    fig_diverging = go.Figure()
    div_df = df_gap.copy().sort_values("gap_difference")
    colors = [
        '#f43f5e' if val > 20 else ('#f59e0b' if val > 0 else '#10b981')
        for val in div_df["gap_difference"]
    ]
    fig_diverging.add_trace(go.Bar(
        y=div_df["skill"],
        x=div_df["gap_difference"],
        orientation="h",
        marker=dict(color=colors),
        hovertemplate="Skill: <b>%{y}</b><br>Net Gap Index: <b>%{x}</b><extra></extra>"
    ))
    apply_dark_layout(
        fig_diverging,
        xaxis=dict(
            title="◄ Academic Foundation Focus | Industry Shortage / Market Deficit ►",
            zeroline=True,
            zerolinecolor="#ffffff",
            zerolinewidth=2
        )
    )

    # 4. Critical Gap Analysis Table
    table_rows = []
    for _, r in display_df.iterrows():
        badge_class = "skill-badge"
        if "Critical" in r["status"]:
            badge_class += " critical"
        elif "Deficit" in r["status"]:
            badge_class += " warning"
        else:
            badge_class += " success"

        table_rows.append(html.Tr([
            html.Td(r["skill"], className="fw-bold text-white"),
            html.Td(f"{r['market_demand_pct']}% ({r['market_openings_count']} jobs)", className="font-mono text-danger"),
            html.Td(f"{r['curriculum_courses_count']} Course(s)", className="font-mono text-info"),
            html.Td(html.Span(r["status"], className=badge_class)),
            html.Td(r["action_recommendation"], className="small text-light")
        ]))

    gap_table = html.Table([
        html.Thead(html.Tr([
            html.Th("Skill / Competency", style={"width": "18%"}),
            html.Th("Industry Demand", style={"width": "18%"}),
            html.Th("Curriculum Taught", style={"width": "16%"}),
            html.Th("Diagnostic Status", style={"width": "22%"}),
            html.Th("Recommended Academic Action", style={"width": "26%"})
        ])),
        html.Tbody(table_rows)
    ], className="table-dark-custom")

    return banner, fig_radar, fig_diverging, gap_table


# =========================================================================
# CALLBACK REGISTRATION
# =========================================================================

def register_callbacks(app):
    """Register callbacks to the Dash app instance."""
    app.callback(
        Output("edu-program-filter", "value"),
        Input("edu-trend-chart", "clickData"),
        State("edu-program-filter", "value"),
        prevent_initial_call=True
    )(handle_edu_trend_click)

    app.callback(
        [
            Output("edu-kpi-total-grads", "children"),
            Output("edu-kpi-emp-y1", "children"),
            Output("edu-kpi-avg-tuition", "children"),
            Output("edu-kpi-total-courses", "children"),
            Output("edu-trend-chart", "figure"),
            Output("edu-employment-chart", "figure"),
            Output("edu-tuition-chart", "figure"),
            Output("edu-courses-table-container", "children"),
        ],
        [
            Input("edu-program-filter", "value"),
            Input("edu-year-filter", "value")
        ]
    )(update_tab_education)

    app.callback(
        Output("market-field-filter", "value"),
        Input("market-treemap-chart", "clickData"),
        State("market-field-filter", "value"),
        prevent_initial_call=True
    )(handle_market_treemap_click)

    app.callback(
        [
            Output("market-kpi-total-jobs", "children"),
            Output("market-kpi-median-salary", "children"),
            Output("market-kpi-top-skill", "children"),
            Output("market-kpi-top-industry", "children"),
            Output("market-skills-chart", "figure"),
            Output("market-salary-boxplot", "figure"),
            Output("market-treemap-chart", "figure"),
            Output("market-jobs-table-container", "children"),
        ],
        [
            Input("market-field-filter", "value"),
            Input("market-exp-filter", "value"),
            Input("market-currency-toggle", "value"),
        ]
    )(update_tab_market)

    app.callback(
        [
            Output("mismatch-alert-banner", "children"),
            Output("mismatch-radar-chart", "figure"),
            Output("mismatch-diverging-chart", "figure"),
            Output("mismatch-table-container", "children"),
        ],
        [
            Input("mismatch-program-filter", "value"),
            Input("mismatch-severity-filter", "value")
        ]
    )(update_tab_mismatch)
