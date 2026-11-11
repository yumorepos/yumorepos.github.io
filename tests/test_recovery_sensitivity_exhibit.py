"""Evidence and nonclaim contract for synthetic sensitivity case-study exhibit."""
from pathlib import Path
import unittest
from html.parser import HTMLParser

ROOT=Path(__file__).resolve().parents[1]
HTML=(ROOT/"disruption-recovery.html").read_text(encoding="utf-8")

class SensitivityExhibit(unittest.TestCase):
    def test_complete_five_scenario_comparisons(self):
        section=HTML.split('id="sensitivity"',1)[1].split('id="finding"',1)[0]
        for name in ("Original penalties and turn screen","Delay penalty ×0.5",
                     "Delay penalty ×2","Turn screen +20 minutes",
                     "Cancellation penalty ×2"):
            self.assertIn(name,section)
        self.assertIn("<td>11</td><td>19</td><td>2.23</td>",section)
        self.assertIn("<td>12</td><td>18</td><td>1.97</td>",section)
        self.assertEqual(section.count("<tr><th scope=\"row\">"),5)
        self.assertIn("11–13 of 30",section)

    def test_relevant_model_and_causality_limits_remain_visible(self):
        section=HTML.split('id="sensitivity"',1)[1].split('id="finding"',1)[0].lower()
        for claim in ("not evidence of airline-scale robustness",
                      "not test real-world airline operations",
                      "changing penalty values also changes the units",
                      "no losses are expected"):
            self.assertIn(claim,section)
        self.assertIn("network-lab/blob/main/experiments/disruption_recovery/SENSITIVITY_RESULTS.md",section)

if __name__=="__main__":
    unittest.main()
