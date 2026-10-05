"""
src/callbacks.py
Reactive cross-filtering Dash callbacks for all three tabs.
Styled according to the Deep Navy Command Center design tokens.
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

# Deep Navy Command Center Design Tokens
DARK_TEMPLATE = {
    "paper_bgcolor": "rgba(0,0,0,0)",
    "plot_bgcolor": "rgba(0,0,0,0)",
    "font": {"color": "#8E9AAF", "family": "Segoe UI, sans-serif", "size": 11},
    "margin": {"l": 30, "r": 20, "t": 30, "b": 30},
    "xaxis": {
        "gridcolor": "#1E3A63",
        "zerolinecolor": "#1E3A63",
        "tickfont": {"color": "#8E9AAF", "size": 11},
    },
    "yaxis": {
        "gridcolor": "#1E3A63",
        "zerolinecolor": "#1E3A63",
        "tickfont": {"color": "#8E9AAF", "size": 11},
    },
    "legend": {
        "font": {"color": "#FFFFFF", "size": 11},
        "orientation": "h",
        "yanchor": "bottom",
        "y": 1.02,
        "xanchor": "right",
        "x": 1,
        "bgcolor": "rgba(0,0,0,0)"
    },
}

BASE_DARK_TEMPLATE = DARK_TEMPLATE  # Compatibility alias

def apply_dark_layout(fig, **kwargs):
    """Safely apply plotly_dark template and merge Deep Navy design tokens."""
    fig.layout.template = "plotly_dark"
    layout_dict = {
        "paper_bgcolor": DARK_TEMPLATE["paper_bgcolor"],
        "plot_bgcolor": DARK_TEMPLATE["plot_bgcolor"],
        "font": DARK_TEMPLATE["font"].copy(),
        "margin": DARK_TEMPLATE["margin"].copy(),
        "xaxis": DARK_TEMPLATE["xaxis"].copy(),
        "yaxis": DARK_TEMPLATE["yaxis"].copy(),
        "legend": DARK_TEMPLATE["legend"].copy(),
    }
    for k, v in kwargs.items():
        if k in layout_dict and isinstance(layout_dict[k], dict) and isinstance(v, dict):
            merged = layout_dict[k].copy()
            merged.update(v)
            layout_dict[k] = merged
        else:
            layout_dict[k] = v
    fig.update_layout(**layout_dict)
    return fig

# Command Center Accent Color Palette
COLOR_PALETTE = {
    "Artificial Intelligence (AI)": "#0091FF",     # Electric Blue
    "Data Science (DS)": "#00E5A3",               # Mint Green
    "Statistics & Analytics (ST)": "#FACC15",     # Warm Gold
    "AI": "#0091FF",
    "Data Science": "#00E5A3",
    "Statistics": "#FACC15"
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

    # 1. Compute KPIs with Command Center Pill Badges
    tot_val = df_e['graduates_count'].sum()
    total_grads = html.Div([
        html.Span(f"{tot_val:,}", className="align-middle"),
        html.Span("12.4% ↑", className="badge-pill-positive ms-2 align-middle")
    ])

    avg_emp_val = df_e['employment_rate_y1'].mean() if not df_e.empty else 0
    avg_emp_y1 = html.Div([
        html.Span(f"{avg_emp_val:.1f}%", className="align-middle"),
        html.Span("Velocity ↑", className="badge-pill-positive ms-2 align-middle")
    ]) if not df_e.empty else "N/A"

    avg_tuit_val = int(df_e['tuition_fee_thb'].mean()) if not df_e.empty else 0
    avg_tuition = html.Div([
        html.Span(f"฿{avg_tuit_val:,}", className="align-middle"),
        html.Span("ROI Benchmark", className="badge-pill-neutral ms-2 align-middle")
    ]) if not df_e.empty else "N/A"

    total_courses_count = html.Div([
        html.Span(f"{len(df_c)}", className="align-middle"),
        html.Span("Core Required", className="badge-pill-neutral ms-2 align-middle")
    ])

    # 2. Graduates Production Trend Chart
    fig_trend = go.Figure()
    all_unique_progs = df_e["program_name"].unique()
    for prog in all_unique_progs:
        sub = df_e[df_e["program_name"] == prog].sort_values("academic_year")
        color = COLOR_PALETTE.get(prog, "#0091FF")
        fig_trend.add_trace(go.Bar(
            x=sub["academic_year"],
            y=sub["graduates_count"],
            name=prog,
            marker=dict(color=color, opacity=0.9, line=dict(color=color, width=1)),
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
        ("Year 1", "employment_rate_y1", "#0091FF"),  # Electric Blue
        ("Year 2", "employment_rate_y2", "#00E5A3"),  # Mint Green
        ("Year 3", "employment_rate_y3", "#FACC15")   # Warm Yellow
    ]
    for stage_label, col, col_hex in stages:
        fig_emp.add_trace(go.Bar(
            x=emp_summary["program_name"].apply(lambda x: x.split(" (")[0]),
            y=emp_summary[col].round(1),
            name=stage_label,
            text=emp_summary[col].apply(lambda v: f"{v:.1f}%"),
            textposition="inside",
            marker=dict(color=col_hex, opacity=0.9),
            hovertemplate="<b>%{x}</b><br>" + stage_label + " Rate: <b>%{y}%</b><extra></extra>"
        ))
    apply_dark_layout(
        fig_emp,
        barmode="group",
        yaxis=dict(range=[70, 102], gridcolor="#1E3A63", title="Employment Rate (%)")
    )

    # 4. Tuition Fees Benchmark
    fig_tuition = go.Figure()
    tuition_summary = df_e.groupby("program_name")["tuition_fee_thb"].mean().reset_index()
    for idx, row in tuition_summary.iterrows():
        p_name = row["program_name"]
        c = COLOR_PALETTE.get(p_name, "#0091FF")
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
        yaxis=dict(range=[0, max_fee], gridcolor="#1E3A63")
    )

    # 5. Course Catalog & Skills Table
    table_rows = []
    for _, c_row in df_c.iterrows():
        skills_html = [
            html.Span(s.strip(), className="skill-badge") 
            for s in str(c_row["key_skills"]).split(",") if s.strip()
        ]
        table_rows.append(html.Tr([
            html.Td(c_row["course_code"], className="font-mono text-accent fw-bold", style={"color": "#38BDF8"}),
            html.Td(c_row["course_name"], className="text-white"),
            html.Td(html.Span(c_row["skill_category"], className="badge-pill-neutral")),
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

    # 1. Compute KPIs with Command Center Pill Badges
    tot_jobs = len(df_j)
    total_openings = html.Div([
        html.Span(f"{tot_jobs:,}", className="align-middle"),
        html.Span("18.5% ↑", className="badge-pill-positive ms-2 align-middle")
    ])

    med_sal_val = int(df_j[sal_col].median()) if not df_j.empty else 0
    median_sal = html.Div([
        html.Span(f"{curr_symbol}{med_sal_val:,}", className="align-middle"),
        html.Span("Benchmark", className="badge-pill-neutral ms-2 align-middle")
    ]) if not df_j.empty else "N/A"

    top_skill_name = df_skills.iloc[0]["skill"] if not df_skills.empty else "N/A"
    top_skill = html.Div([
        html.Span(top_skill_name, className="align-middle"),
        html.Span("Dominant", className="badge-pill-warning ms-2 align-middle")
    ]) if not df_skills.empty else "N/A"

    top_ind_name = df_j["industry"].mode()[0] if not df_j.empty else "N/A"
    top_industry = html.Div([
        html.Span(top_ind_name.split(" /")[0], className="align-middle"),
        html.Span("Leading Hub", className="badge-pill-neutral ms-2 align-middle")
    ]) if not df_j.empty else "N/A"

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
                colorscale=[[0, "#10223E"], [0.5, "#0091FF"], [1, "#00E5A3"]],
                showscale=True,
                colorbar=dict(
                    title=dict(text="Share %", font=dict(color="#8E9AAF", size=10)),
                    tickfont=dict(color="#8E9AAF", size=9),
                    thickness=10,
                    len=0.7
                )
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
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Segoe UI, sans-serif", color="#FFFFFF")
        )
    else:
        fig_treemap = go.Figure()

    # 5. Featured Vacancies Table
    table_rows = []
    recent_jobs = df_j.head(25)
    for _, j in recent_jobs.iterrows():
        field_color = COLOR_PALETTE.get(j["field"], "#0091FF")
        table_rows.append(html.Tr([
            html.Td(j["job_title"], className="fw-semibold text-white"),
            html.Td(j["company_name"], style={"color": "#38BDF8"}),
            html.Td(html.Span(j["experience_level"], className="badge-pill-neutral")),
            html.Td(f"{curr_symbol}{int(j[sal_col]):,}", className="font-mono", style={"color": "#00E5A3", "fontWeight": "600"}),
            html.Td(html.Span(j["field"], style={
                "backgroundColor": f"{field_color}33",
                "color": field_color,
                "padding": "2px 8px",
                "borderRadius": "4px",
                "fontSize": "11px",
                "fontWeight": "600"
            }))
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
        total_openings, median_sal, top_skill, top_industry,
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

    # 1. Executive Alert Banner with Command Center Styling
    crit_count = len(df_crit)
    top_missing_skills = ", ".join(df_crit["skill"].head(3).tolist()) if crit_count > 0 else "None"
    alert_class = "alert-command-danger" if crit_count > 0 else "alert-command-success"
    
    banner = html.Div([
        html.Div([
            html.Span("⚠️", className="me-2 fs-5") if crit_count > 0 else html.Span("✅", className="me-2 fs-5"),
            html.Strong(f"Skills Gap Command Diagnostic: {selected_program}", className="fs-6 me-3"),
            html.Span(f"{crit_count} Critical Shortage(s) Detected", className="badge-pill-negative me-2" if crit_count > 0 else "badge-pill-positive me-2"),
        ], className="d-flex align-items-center mb-1"),
        html.Div(
            f"Curriculum blindspots lacking mandatory coursework: {top_missing_skills}. Immediate academic review recommended.",
            className="small",
            style={"color": "#D1D5DB"}
        )
    ], className=f"p-3 {alert_class} mb-3 shadow-sm")

    # 2. Radar Chart (Electric Blue for Curriculum vs Coral Orange for Market)
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
        line=dict(color='#FF6B4A', width=2),  # Coral Orange
        fillcolor='rgba(255, 107, 74, 0.25)'
    ))
    fig_radar.add_trace(go.Scatterpolar(
        r=curriculum_vals,
        theta=skills_labels,
        fill='toself',
        name='Curriculum Course Score (0-100)',
        line=dict(color='#0091FF', width=2),  # Electric Blue
        fillcolor='rgba(0, 145, 255, 0.25)'
    ))
    apply_dark_layout(
        fig_radar,
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], color="#8E9AAF", gridcolor="#1E3A63"),
            angularaxis=dict(color="#FFFFFF", gridcolor="#1E3A63"),
            bgcolor="rgba(0,0,0,0)"
        )
    )

    # 3. Diverging Bar Chart (Shortage vs Over-Supply with Command Center Tokens)
    fig_diverging = go.Figure()
    div_df = df_gap.copy().sort_values("gap_difference")
    colors = [
        '#FF6B4A' if val > 20 else ('#FACC15' if val > 0 else '#00E5A3')
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
            zerolinecolor="#FFFFFF",
            zerolinewidth=1.5
        )
    )

    # 4. Critical Gap Analysis Table with Status Badges
    table_rows = []
    for _, r in display_df.iterrows():
        if "Critical" in r["status"]:
            badge = html.Span("Critical Shortage", className="badge-pill-negative")
        elif "Deficit" in r["status"]:
            badge = html.Span("Moderate Deficit", className="badge-pill-warning")
        else:
            badge = html.Span("Well Aligned", className="badge-pill-positive")

        table_rows.append(html.Tr([
            html.Td(r["skill"], className="fw-bold text-white"),
            html.Td(f"{r['market_demand_pct']}% ({r['market_openings_count']} jobs)", className="font-mono", style={"color": "#FF6B4A", "fontWeight": "600"}),
            html.Td(f"{r['curriculum_courses_count']} Course(s)", className="font-mono", style={"color": "#38BDF8"}),
            html.Td(badge),
            html.Td(r["action_recommendation"], className="small", style={"color": "#D1D5DB"})
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
