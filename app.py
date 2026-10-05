"""
app.py
Main entry point for AI & Data Science Job Market and Education Dashboard (AISDST).
Built with Plotly Dash, Dash Bootstrap Components, and Pandas.
"""

import os
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc

from src.components.tab_education import render_tab_education_layout
from src.components.tab_market import render_tab_market_layout
from src.components.tab_mismatch import render_tab_mismatch_layout
from src.callbacks import register_callbacks

# Initialize Dash application with Darkly theme & custom font assets
app = Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.DARKLY,
        "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css"
    ],
    suppress_callback_exceptions=True,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1, shrink-to-fit=no"}
    ],
    title="AISDST | AI & Data Science Job Market & Education Dashboard"
)

server = app.server

# ---------------------------------------------------------------------------
# Navigation Bar & Brand Header
# ---------------------------------------------------------------------------
navbar = html.Header(
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Span("AISDST", className="aisdst-logo-badge me-2"),
                    html.Span(
                        "AI & Data Science Job Market and Education Dashboard",
                        className="fs-5 fw-bold text-white align-middle"
                    ),
                    html.Div(
                        "ระบบวิเคราะห์ศักยภาพการผลิตบัณฑิต ความต้องการของตลาดแรงงาน และช่องว่างทางทักษะ",
                        className="text-muted small mt-1"
                    )
                ])
            ], md=8, sm=12),
            dbc.Col([
                html.Div([
                    dbc.Badge("Interactive Reactive Analytics", color="primary", className="me-2 p-2"),
                    dbc.Button(
                        [html.I(className="bi bi-box-arrow-up-right me-1"), "Executive HTML"],
                        href="/assets/index.html" if os.path.exists("assets/index.html") else "#",
                        target="_blank",
                        color="outline-info",
                        size="sm",
                        className="rounded-pill"
                    )
                ], className="text-md-end text-sm-start mt-2 mt-md-0")
            ], md=4, sm=12)
        ], className="align-items-center")
    ], fluid=True),
    className="aisdst-navbar"
)

# ---------------------------------------------------------------------------
# App Main Layout Container with 3 Analytical Tabs
# ---------------------------------------------------------------------------
app.layout = html.Div([
    navbar,
    dbc.Container([
        dbc.Tabs(
            id="dashboard-tabs",
            active_tab="tab-1",
            children=[
                dbc.Tab(
                    label="🎓 Tab 1: Education & Graduates (บัณฑิตและหลักสูตร)",
                    tab_id="tab-1",
                    children=[
                        html.Div(render_tab_education_layout(), className="pt-3")
                    ]
                ),
                dbc.Tab(
                    label="💼 Tab 2: Job Market Demand (ตลาดแรงงานและการจ้างงาน)",
                    tab_id="tab-2",
                    children=[
                        html.Div(render_tab_market_layout(), className="pt-3")
                    ]
                ),
                dbc.Tab(
                    label="🔍 Tab 3: Skills Mismatch Analysis (วิเคราะห์ช่องว่างทักษะ)",
                    tab_id="tab-3",
                    children=[
                        html.Div(render_tab_mismatch_layout(), className="pt-3")
                    ]
                ),
            ],
            className="mt-3"
        ),
        
        # Footer
        html.Footer([
            html.Hr(className="border-secondary my-4"),
            dbc.Row([
                dbc.Col([
                    html.P([
                        "AISDST Platform © 2026. Built according to Business Requirements Document (BRD). ",
                        "Designed for Academic Deans, Curriculum Committees, and Workforce Analysts."
                    ], className="text-muted small mb-0")
                ], md=8),
                dbc.Col([
                    html.P([
                        html.Span("Open Data Ready • Cross-filtering Reactive Engine", className="text-info small")
                    ], className="text-md-end text-muted small mb-0")
                ], md=4)
            ], className="pb-4")
        ])
    ], fluid=True, className="px-4")
])

# Register reactive cross-filtering callbacks
register_callbacks(app)

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=8050)
