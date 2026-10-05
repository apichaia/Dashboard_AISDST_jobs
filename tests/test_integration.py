"""
tests/test_integration.py
Integration tests executing Dash callbacks directly and verifying chart output structures.
"""

import unittest
from app import app
from src.callbacks import update_tab_education, update_tab_market, update_tab_mismatch
import plotly.graph_objects as go

class TestIntegrationCallbacks(unittest.TestCase):

    def test_tab1_callbacks(self):
        # Test Tab 1 with ALL curricula and all years
        res = update_tab_education("ALL", [2021, 2022, 2023, 2024, 2025])
        self.assertEqual(len(res), 8)
        tot_grads, emp_y1, tuition, n_courses, fig_trend, fig_emp, fig_tuition, table = res
        self.assertNotEqual(tot_grads, "--")
        self.assertIn("%", emp_y1)
        self.assertIn("฿", tuition)
        self.assertIsInstance(fig_trend, go.Figure)
        self.assertIsInstance(fig_emp, go.Figure)
        self.assertIsInstance(fig_tuition, go.Figure)

    def test_tab1_crossfilter_program(self):
        # Test Tab 1 filtered to AI only
        res = update_tab_education("Artificial Intelligence (AI)", [2024])
        self.assertEqual(len(res), 8)
        tot_grads, emp_y1, tuition, n_courses, fig_trend, fig_emp, fig_tuition, table = res
        self.assertNotEqual(tot_grads, "--")
        self.assertEqual(len(fig_trend.data), 1)

    def test_tab2_callbacks(self):
        # Test Tab 2 with ALL fields, ALL experience levels, THB
        res = update_tab_market("ALL", "ALL", "THB")
        self.assertEqual(len(res), 8)
        tot_jobs, median_sal, top_skill, top_ind, fig_skills, fig_box, fig_tree, jobs_tbl = res
        self.assertNotEqual(tot_jobs, "--")
        self.assertIn("฿", median_sal)
        self.assertIsInstance(fig_skills, go.Figure)
        self.assertIsInstance(fig_box, go.Figure)
        self.assertIsInstance(fig_tree, go.Figure)

    def test_tab2_callbacks_usd_and_filter(self):
        # Test Tab 2 with Data Science, Senior, USD
        res = update_tab_market("Data Science", "Senior", "USD")
        self.assertEqual(len(res), 8)
        tot_jobs, median_sal, top_skill, top_ind, fig_skills, fig_box, fig_tree, jobs_tbl = res
        self.assertIn("$", median_sal)

    def test_tab3_callbacks(self):
        # Test Tab 3 with AI program and ALL severity
        banner, fig_radar, fig_div, gap_tbl = update_tab_mismatch("Artificial Intelligence (AI)", "ALL")
        self.assertIsNotNone(banner)
        self.assertIsInstance(fig_radar, go.Figure)
        self.assertIsInstance(fig_div, go.Figure)
        self.assertIsNotNone(gap_tbl)

    def test_tab3_callbacks_critical_filter(self):
        # Test Tab 3 with Critical Shortages Only
        banner, fig_radar, fig_div, gap_tbl = update_tab_mismatch("Data Science (DS)", "CRITICAL")
        self.assertIsNotNone(banner)
        self.assertIsInstance(fig_radar, go.Figure)
        self.assertIsInstance(fig_div, go.Figure)
        self.assertIsNotNone(gap_tbl)

if __name__ == "__main__":
    unittest.main()
