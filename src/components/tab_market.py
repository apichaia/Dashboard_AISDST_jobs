"""
src/components/tab_market.py
Tab 2: Job Market Demand (ปริมาณงานที่จ้าง และ Skills ที่ต้องการ)
"""

from dash import dcc, html
import dash_bootstrap_components as dbc

FIELD_OPTIONS = [
    {"label": "All Fields (AI / DS / ST)", "value": "ALL"},
    {"label": "Artificial Intelligence (AI)", "value": "AI"},
    {"label": "Data Science", "value": "Data Science"},
    {"label": "Statistics", "value": "Statistics"}
]

EXPERIENCE_OPTIONS = [
    {"label": "All Experience Levels", "value": "ALL"},
    {"label": "Entry-level (0-2 Yrs)", "value": "Entry-level"},
    {"label": "Mid-level (3-5 Yrs)", "value": "Mid-level"},
    {"label": "Senior (6-9 Yrs)", "value": "Senior"},
    {"label": "Expert (10+ Yrs)", "value": "Expert"}
]

def render_tab_market_layout():
    """Generates layout for Tab 2: Job Market Demand."""
    return html.Div([
        # Filter & Control Row
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Label("Filter by Technical Field (สายงาน):", className="fw-bold text-muted small mb-1"),
                    dcc.Dropdown(
                        id="market-field-filter",
                        options=FIELD_OPTIONS,
                        value="ALL",
                        clearable=False,
                        className="text-dark"
                    )
                ])
            ], md=4, sm=12, className="mb-3"),

            dbc.Col([
                html.Div([
                    html.Label("Filter by Experience Level (ระดับประสบการณ์):", className="fw-bold text-muted small mb-1"),
                    dcc.Dropdown(
                        id="market-exp-filter",
                        options=EXPERIENCE_OPTIONS,
                        value="ALL",
                        clearable=False,
                        className="text-dark"
                    )
                ])
            ], md=4, sm=12, className="mb-3"),

            dbc.Col([
                html.Div([
                    html.Label("Currency Display (สกุลเงิน):", className="fw-bold text-muted small mb-1"),
                    dcc.RadioItems(
                        id="market-currency-toggle",
                        options=[
                            {"label": " THB (฿) ", "value": "THB"},
                            {"label": " USD ($) ", "value": "USD"}
                        ],
                        value="THB",
                        inline=True,
                        className="mt-2 text-light"
                    )
                ])
            ], md=4, sm=12, className="mb-3")
        ], className="align-items-center mb-2"),

        # Top KPI Metric Cards Row
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Div("Active Job Openings", className="kpi-title"),
                    html.Div(id="market-kpi-total-jobs", className="kpi-value", children="--"),
                    html.Div("Tracked across top employer listings", className="kpi-subtitle")
                ], className="kpi-card")
            ], md=3, sm=6, className="mb-3"),

            dbc.Col([
                html.Div([
                    html.Div("Median Base Salary", className="kpi-title"),
                    html.Div(id="market-kpi-median-salary", className="kpi-value", children="--"),
                    html.Div("Across selected filters", className="kpi-subtitle")
                ], className="kpi-card")
            ], md=3, sm=6, className="mb-3"),

            dbc.Col([
                html.Div([
                    html.Div("Top Required Skill", className="kpi-title"),
                    html.Div(id="market-kpi-top-skill", className="kpi-value", children="--"),
                    html.Div("Highest requisition mention rate", className="kpi-subtitle")
                ], className="kpi-card")
            ], md=3, sm=6, className="mb-3"),

            dbc.Col([
                html.Div([
                    html.Div("Leading Hiring Sector", className="kpi-title"),
                    html.Div(id="market-kpi-top-industry", className="kpi-value", children="--"),
                    html.Div("Highest active job postings", className="kpi-subtitle")
                ], className="kpi-card")
            ], md=3, sm=6, className="mb-3"),
        ], className="mb-2"),

        # Row 1 of Charts: Top In-Demand Skills + Salary Distribution Box Plot
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Div([
                        html.Span("🔥", className="me-2"),
                        html.Span("Top Demanded Skills (ทักษะที่ตลาดต้องการสูงสุดตามลำดับ)"),
                        html.Small(" [Click bar to cross-filter]", className="text-muted ms-auto font-monospace small")
                    ], className="card-title-custom"),
                    dcc.Graph(id="market-skills-chart", config={"displayModeBar": False}, style={"height": "350px"})
                ], className="dash-card")
            ], md=6, sm=12, className="mb-3"),

            dbc.Col([
                html.Div([
                    html.Div([
                        html.Span("💵", className="me-2"),
                        html.Span("Salary Range Distribution by Seniority (โครงสร้างเงินเดือนตามระดับประสบการณ์)")
                    ], className="card-title-custom"),
                    dcc.Graph(id="market-salary-boxplot", config={"displayModeBar": False}, style={"height": "350px"})
                ], className="dash-card")
            ], md=6, sm=12, className="mb-3"),
        ]),

        # Row 2 of Visualizations: Industry / Company Treemap + Job Postings Table
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Div([
                        html.Span("🏢", className="me-2"),
                        html.Span("Industry & Company Hiring Landscape (สัดส่วนการจ้างงานตามอุตสาหกรรมและบริษัท)")
                    ], className="card-title-custom"),
                    dcc.Graph(id="market-treemap-chart", config={"displayModeBar": False}, style={"height": "350px"})
                ], className="dash-card")
            ], md=7, sm=12, className="mb-3"),

            dbc.Col([
                html.Div([
                    html.Div([
                        html.Span("📋", className="me-2"),
                        html.Span("Featured Vacancies (ประกาศงานล่าสุด)")
                    ], className="card-title-custom"),
                    html.Div(id="market-jobs-table-container", style={"height": "350px", "overflowY": "auto"})
                ], className="dash-card")
            ], md=5, sm=12, className="mb-3"),
        ])
    ])
