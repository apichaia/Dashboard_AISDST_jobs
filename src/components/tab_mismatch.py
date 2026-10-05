"""
src/components/tab_mismatch.py
Tab 3: Skills Mismatch Analysis (วิเคราะห์ช่องว่างทักษะ)
"""

from dash import dcc, html
import dash_bootstrap_components as dbc

PROGRAM_OPTIONS_MISMATCH = [
    {"label": "Artificial Intelligence (AI) Curriculum vs Market", "value": "Artificial Intelligence (AI)"},
    {"label": "Data Science (DS) Curriculum vs Market", "value": "Data Science (DS)"},
    {"label": "Statistics & Analytics (ST) Curriculum vs Market", "value": "Statistics & Analytics (ST)"},
]

SEVERITY_OPTIONS = [
    {"label": "All Monitored Skills (ทักษะทั้งหมด)", "value": "ALL"},
    {"label": "Critical Shortages Only (ขาดแคลนวิกฤต - ไม่มีการเปิดสอน)", "value": "CRITICAL"},
    {"label": "Moderate Deficits (ต้องเพิ่มความเข้มข้น)", "value": "DEFICIT"},
    {"label": "Well-Aligned / Core Foundation (สอดคล้องดี)", "value": "ALIGNED"}
]

def render_tab_mismatch_layout():
    """Generates layout for Tab 3: Skills Mismatch Analysis."""
    return html.Div([
        # Filter & Control Row
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Label("Select Academic Track for Gap Comparison (เลือกหลักสูตรที่ต้องการเทียบเคียง):", 
                               className="fw-bold text-muted small mb-1"),
                    dcc.Dropdown(
                        id="mismatch-program-filter",
                        options=PROGRAM_OPTIONS_MISMATCH,
                        value="Artificial Intelligence (AI)",
                        clearable=False,
                        className="text-dark"
                    )
                ])
            ], md=6, sm=12, className="mb-3"),

            dbc.Col([
                html.Div([
                    html.Label("Filter by Gap Severity (ระดับความรุนแรงของช่องว่าง):", 
                               className="fw-bold text-muted small mb-1"),
                    dcc.Dropdown(
                        id="mismatch-severity-filter",
                        options=SEVERITY_OPTIONS,
                        value="ALL",
                        clearable=False,
                        className="text-dark"
                    )
                ])
            ], md=6, sm=12, className="mb-3"),
        ], className="align-items-center mb-2"),

        # Executive Gap Alert Banner
        dbc.Row([
            dbc.Col([
                html.Div(id="mismatch-alert-banner", className="mb-3")
            ], width=12)
        ]),

        # Row 1: Radar Chart (Curriculum vs Market) + Diverging Bar Chart (Shortage vs Over-supply)
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Div([
                        html.Span("🎯", className="me-2"),
                        html.Span("Curriculum Coverage vs. Market Demand (Radar Chart เปรียบเทียบทักษะ)")
                    ], className="card-title-custom"),
                    dcc.Graph(id="mismatch-radar-chart", config={"displayModeBar": False}, style={"height": "380px"})
                ], className="dash-card")
            ], md=6, sm=12, className="mb-3"),

            dbc.Col([
                html.Div([
                    html.Div([
                        html.Span("⚖️", className="me-2"),
                        html.Span("Skills Gap Spectrum: Shortage vs Over-Supply (Diverging Bar Chart)")
                    ], className="card-title-custom"),
                    dcc.Graph(id="mismatch-diverging-chart", config={"displayModeBar": False}, style={"height": "380px"})
                ], className="dash-card")
            ], md=6, sm=12, className="mb-3"),
        ]),

        # Row 2: Comprehensive Gap Analysis Table & Curriculum Recommendations
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Div([
                        html.Span("🚨", className="me-2"),
                        html.Span("Critical Curriculum Deficits (รายการทักษะที่ตลาดต้องการสูงแต่ยังไม่มีในวิชาบังคับ)"),
                        html.Small(" [Actionable Policy Recommendations]", className="text-muted ms-auto font-monospace small")
                    ], className="card-title-custom"),
                    html.Div(id="mismatch-table-container", style={"height": "360px", "overflowY": "auto"})
                ], className="dash-card")
            ], width=12, className="mb-3"),
        ])
    ])
