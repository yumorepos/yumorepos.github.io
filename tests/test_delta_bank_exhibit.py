"""Source-bound, denominator-safe contracts for the Delta departure-bank exhibit."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / "airline-operations.html").read_text(encoding="utf-8")
REPORT_URL = "https://github.com/yumorepos/fleet-tracker/blob/main/docs/BTS_DEPARTURE_BANK_DESTINATION_MIX_2025_RESULTS.md"

# Exact source-verified on-time and valid-arrival counts from the existing report.
BANKS = [
    ("Jan · 06–11", 4334, 5601, 20715, 24637, "-6.70"),
    ("Jan · 12–17", 4320, 5597, 16178, 20315, "-2.45"),
    ("Jan · 18–23", 4123, 5400, 8257, 10420, "-2.89"),
    ("Jul · 06–11", 6028, 6957, 25900, 29839, "-0.15"),
    ("Jul · 12–17", 5013, 7594, 16816, 23632, "-5.15"),
    ("Jul · 18–23", 3952, 6941, 9103, 14553, "-5.61"),
]


class DeltaDepartureBankExhibit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.section = HTML.split('id="departure-banks"', 1)[1].split('id="connections"', 1)[0]

    def test_original_origin_population_reconstructs_across_banks(self):
        # Overnight ATL = 0 / 0; other-origin overnight excludes direct comparison.
        jan = BANKS[:3]
        jul = BANKS[3:]
        self.assertEqual(sum(x[1] for x in jan), 12777)
        self.assertEqual(sum(x[2] for x in jan), 16598)
        self.assertEqual(sum(x[3] for x in jan) + 1796, 46946)
        self.assertEqual(sum(x[4] for x in jan) + 2055, 57427)
        self.assertEqual(sum(x[1] for x in jul), 14993)
        self.assertEqual(sum(x[2] for x in jul), 21492)
        self.assertEqual(sum(x[3] for x in jul) + 2515, 54334)
        self.assertEqual(sum(x[4] for x in jul) + 2729, 70753)

    def test_source_rates_and_difference_labels(self):
        self.assertEqual(self.section.count('<tr><th scope="row">'), 6)
        self.assertEqual(self.section.count('class="ops-bar-row"'), 6)
        for label, a_on, a_valid, b_on, b_valid, gap in BANKS:
            self.assertIn(label, self.section)
            self.assertIn(f"{a_on:,} / {a_valid:,}", self.section)
            self.assertIn(f"{b_on:,} / {b_valid:,}", self.section)
            self.assertAlmostEqual(round((a_on/a_valid - b_on/b_valid)*100,2),
                                   float(gap), places=2)
            self.assertIn(f"−{gap.lstrip('-')} pp", self.section)

    def test_selected_destination_coverage_and_boundaries(self):
        for term in ("60.77%", "66.17%", "63.01%", "65.39%",
                     "150 shared groups", "174 groups", "−5.28 pp", "−2.52 pp",
                     "no ATL-origin scheduled flights in the 00–05",
                     "not a causal adjustment", "not verified airline wave schedules"):
            self.assertIn(term.lower(), self.section.lower())
        self.assertIn(REPORT_URL, self.section)
        self.assertIn('role="region"', self.section)
        self.assertIn('tabindex="0"', self.section)

    def test_gap_bar_length_has_explicit_comparable_scale(self):
        widths = [float(x) for x in re.findall(
            r'class="ops-bar-fill[^"]*" style="width:([\d.]+)%"',
            self.section
        )]
        self.assertEqual(widths, [67, 24.5, 28.9, 1.5, 51.5, 56.1])
        self.assertIn("0–10 percentage-point scale", self.section)
        self.assertIn("labels retain the minus sign", self.section)


if __name__ == "__main__":
    unittest.main()
