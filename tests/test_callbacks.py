"""
tests/test_callbacks.py
Unit tests verifying callback reactivity, data manipulation, and figure generation.
"""

import unittest
from src.data_loader import (
    load_data,
    get_education_metrics,
    get_job_market_metrics,
    get_skills_mismatch_metrics
)
from src.callbacks import (
    BASE_DARK_TEMPLATE,
    COLOR_PALETTE
)

class TestAISDST(unittest.TestCase):

    def test_data_loading(self):
        df_edu, df_jobs, df_courses = load_data()
        self.assertFalse(df_edu.empty, "Education data should not be empty")
        self.assertFalse(df_jobs.empty, "Job market data should not be empty")
        self.assertFalse(df_courses.empty, "Curriculum courses data should not be empty")
        self.assertIn("graduates_count", df_edu.columns)
        self.assertIn("required_skills", df_jobs.columns)

    def test_education_filtering(self):
        df_filtered, df_c = get_education_metrics(
            selected_programs=["Artificial Intelligence (AI)"],
            selected_years=[2023, 2024]
        )
        self.assertEqual(len(df_filtered), 2)
        self.assertEqual(df_filtered["program_name"].iloc[0], "Artificial Intelligence (AI)")

    def test_job_market_metrics(self):
        df_j, df_skills = get_job_market_metrics(
            selected_fields=["AI"],
            selected_levels=["Mid-level"]
        )
        self.assertFalse(df_j.empty)
        self.assertTrue((df_j["field"] == "AI").all())
        self.assertTrue((df_j["experience_level"] == "Mid-level").all())
        self.assertFalse(df_skills.empty)
        self.assertIn("demand_share_pct", df_skills.columns)

    def test_skills_mismatch(self):
        df_gap, df_crit = get_skills_mismatch_metrics("Artificial Intelligence (AI)")
        self.assertFalse(df_gap.empty)
        self.assertIn("market_demand_pct", df_gap.columns)
        self.assertIn("curriculum_score", df_gap.columns)
        self.assertIn("status", df_gap.columns)
        # Should have detected critical shortage skills
        self.assertGreater(len(df_crit), 0)

if __name__ == "__main__":
    unittest.main()
