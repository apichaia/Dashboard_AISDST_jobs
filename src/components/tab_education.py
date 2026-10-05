"""
src/components/tab_education.py
Tab 1: Education & Graduates (ปริมาณคนที่จบ และ Skills ที่เรียนมา)
"""

from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

from src.data_loader import DF_EDU, DF_COURSES

PROGRAM_OPTIONS = [
    {"label": "All Curricula (ทั้งหมด)", "value": "ALL"},
    {"label": "Artificial Intelligence (AI)", "value": "Artificial Intelligence (AI)"},
    {"label": "Data Science (DS)", "value": "Data Science (DS)"},
    {"label": "Statistics & Analytics (ST)", "value": "Statistics & Analytics (ST)"},
]

YEAR_OPTIONS = sorted(DF_EDU["academic_year"].unique().tolist())

# Dark Plotly Template configuration
DARK_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#e5e7eb", size=12),
    margin=dict(l=40, r=20, t=40, b=40),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    xaxis=dict(gridcolor="#283344", zerolinecolor="#283344"),
    yaxis=dict(gridcolor="#283344", zerolinecolor="#283344")
)

def render_tab_education_layout():
    """Generates layout for Tab 1: Education & Graduates."""
    return html.Div([
        # Filter & Control Header
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Label("Filter by Academic Program (เลือกหลักสูตร):", className="fw-bold text-muted small mb-1"),
                    dcc.Dropdown(
                        id="edu-program-filter",
                        options=PROGRAM_OPTIONS,
                        value="ALL",
                        clearable=False,
                        className="text-dark"
                    )
                ])
            ], md=6, sm=12, className="mb-3"),
            dbc.Col([
                html.Div([
                    html.Label("Filter by Academic Year (ปีการศึกษา):", className="fw-bold text-muted small mb-1"),
                    dcc.Dropdown(
                        id="edu-year-filter",
                        options=[{"label": f"Year {y}", "value": y} for y in YEAR_OPTIONS],
                        value=YEAR_OPTIONS,
                        multi=True,
                        placeholder="Select Academic Years...",
                        className="text-dark"
                    )
                ])
            ], md=6, sm=12, className="mb-3")
        ], className="align-items-center mb-2"),

        # Top KPI Metric Cards Row
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Div("Total Graduates (2021-2025)", className="kpi-title"),
                    html.Div(id="edu-kpi-total-grads", className="kpi-value", children="--"),
                    html.Div("Cumulative talent pipeline", className="kpi-subtitle")
                ], className="kpi-card")
            ], md=3, sm=6, className="mb-3"),
            dbc.Col([
                html.Div([
                    html.Div("Avg. Employment Rate (Year 1)", className="kpi-title"),
                    html.Div(id="edu-kpi-emp-y1", className="kpi-value", children="--"),
                    html.Div("Within 12 months of graduation", className="kpi-subtitle")
                ], className="kpi-card")
            ], md=3, sm=6, className="mb-3"),
            dbc.Col([
                html.Div([
                    html.Div("Avg. Tuition Fee / Year", className="kpi-title"),
                    html.Div(id="edu-kpi-avg-tuition", className="kpi-value", children="--"),
                    html.Div("Estimated investment", className="kpi-subtitle")
                ], className="kpi-card")
            ], md=3, sm=6, className="mb-3"),
            dbc.Col([
                html.Div([
                    html.Div("Mandatory Core Courses", className="kpi-title"),
                    html.Div(id="edu-kpi-total-courses", className="kpi-value", children="--"),
                    html.Div("Industry-aligned coursework", className="kpi-subtitle")
                ], className="kpi-card")
            ], md=3, sm=6, className="mb-3"),
        ], className="mb-2"),

        # Row 1 of Charts: Trend of Graduates + Stacked Employment Rate
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Div([
                        html.Span("📈", className="me-2"),
                        html.Span("Graduates Production Trend (จำนวนบัณฑิตที่ผลิตได้ในแต่ละปี)"),
                        html.Small(" [Click bar/line to cross-filter]", className="text-muted ms-auto font-monospace small")
                    ], className="card-title-custom"),
                    dcc.Graph(id="edu-trend-chart", config={"displayModeBar": False}, style={"height": "340px"})
                ], className="dash-card")
            ], md=7, sm=12, className="mb-3"),

            dbc.Col([
                html.Div([
                    html.Div([
                        html.Span("💼", className="me-2"),
                        html.Span("Post-Graduation Employment Velocity (อัตราการได้งานทำ Y1/Y2/Y3)")
                    ], className="card-title-custom"),
                    dcc.Graph(id="edu-employment-chart", config={"displayModeBar": False}, style={"height": "340px"})
                ], className="dash-card")
            ], md=5, sm=12, className="mb-3"),
        ]),

        # Row 2 of Visualizations: Tuition Comparison & Curriculum Courses / Skill Tag Cloud
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Div([
                        html.Span("💰", className="me-2"),
                        html.Span("Tuition Fees Benchmark (ค่าเทอมและผลตอบแทนตามหลักสูตร)")
                    ], className="card-title-custom"),
                    dcc.Graph(id="edu-tuition-chart", config={"displayModeBar": False}, style={"height": "340px"})
                ], className="dash-card")
            ], md=5, sm=12, className="mb-3"),

            dbc.Col([
                html.Div([
                    html.Div([
                        html.Span("📚", className="me-2"),
                        html.Span("Mandatory Courses & Curriculum Skill Categories (รายวิชาบังคับและทักษะที่สอน)")
                    ], className="card-title-custom"),
                    html.Div(id="edu-courses-table-container", style={"height": "340px", "overflowY": "auto"})
                ], className="dash-card")
            ], md=7, sm=12, className="mb-3"),
        ])
    ])
