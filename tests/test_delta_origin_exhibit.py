"""Scoped confidence checks for the new BTS origin and cause exhibit."""
from pathlib import Path
from html.parser import HTMLParser
import re
import unittest

ROOT=Path(__file__).resolve().parents[1]
PAGE=(ROOT/"airline-operations.html").read_text(encoding="utf-8")

class SegmentedEvidence(unittest.TestCase):
    def test_source_counts_reconcile_to_existing_page_population(self):
        self.assertIn('id="origin-comparison"',PAGE)
        self.assertIn("12,777 / 16,598",PAGE)
        self.assertIn("46,946 / 57,427",PAGE)
        self.assertIn("14,993 / 21,492",PAGE)
        self.assertIn("54,334 / 70,753",PAGE)
        self.assertEqual(12777+46946,59723)
        self.assertEqual(14993+54334,69327)
        self.assertEqual(16598+57427,74025)
        self.assertEqual(21492+70753,92245)

    def test_each_published_segment_rate_matches_its_own_denominator(self):
        records=[
            (12777,16598,"76.98%"),
            (46946,57427,"81.75%"),
            (14993,21492,"69.76%"),
            (54334,70753,"76.79%"),
            (1172,3821,"30.67%"),
            (4454,10481,"42.50%"),
            (2419,6499,"37.22%"),
            (8184,16419,"49.84%"),
        ]
        for n,d,pct in records:
            self.assertAlmostEqual(n/d*100,float(pct[:-1]),delta=.006)
            self.assertIn(pct,PAGE)
        self.assertIn("−4.77 pp",PAGE)
        self.assertIn("−7.03 pp",PAGE)

    def test_no_synthetic_cause_or_hub_causality_claims(self):
        for phrase in ("not an estimate of an ATL airport effect",
                       "cannot tell us whether a process at ATL caused the gap",
                       "carrier-reported attribution","Neither the raw gap nor",
                       "not an independently linked causal explanation"):
            self.assertIn(phrase,PAGE)
        self.assertIn('github.com/yumorepos/fleet-tracker/pull/12',PAGE)

    def test_chart_is_labeled_and_does_not_reuse_full_population_denominator(self):
        section=PAGE.split('id="origin-comparison"',1)[1].split('id="connections"',1)[0]
        values=re.findall(r'class="ops-bar-fill[^"]*"\s+style="width:([\d.]+)%"',section)
        self.assertEqual(values,["30.67","42.50","37.22","49.84"])
        self.assertIn("late-arriving flights with complete cause records",section)
        self.assertIn("not an independently linked causal explanation",section)

if __name__=="__main__":
    unittest.main()
