"""Source-bound evidence and accessibility checks for the day-resampling exhibit."""

from html.parser import HTMLParser
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PAGE = (ROOT / "airline-operations.html").read_text(encoding="utf-8")
RESULTS_URL = (
    "https://github.com/yumorepos/fleet-tracker/blob/main/"
    "docs/BTS_DAY_RESAMPLING_2025_RESULTS.md"
)


class ExhibitParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.table_count = 0
        self.regions = []
        self.rows = 0

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "a" and "href" in attributes:
            self.links.append(attributes["href"])
        if tag == "table":
            self.table_count += 1
        if tag == "div" and attributes.get("role") == "region":
            self.regions.append(attributes)
        if tag == "tr":
            self.rows += 1


class DeltaDayResamplingExhibit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.assertion_page = PAGE
        cls.section = PAGE.split('id="day-resampling"', 1)[1].split(
            'id="connections"', 1
        )[0]

    def test_single_bounded_section(self):
        self.assertEqual(PAGE.count('id="day-resampling"'), 1)
        self.assertIn("Does the matched July gap", self.section)
        self.assertIn('id="departure-banks"', PAGE)
        self.assertIn('id="connections"', PAGE)

    def test_exact_verified_july_resampling_metrics(self):
        for text in (
            "July 2025",
            "−2.518 percentage points",
            "−5.226 to +0.644 pp",
            "−5.347 to +0.263 pp",
            "32 / 300",
            "26 / 300",
            "1,200",
            "zero disagreements",
        ):
            with self.subTest(text=text):
                self.assertIn(text, self.section)

    def test_correct_denominators_and_uncertainty(self):
        lower = self.section.lower()
        for text in (
            "matched, standardized",
            "unadjusted, full-population",
            "not statistical confidence intervals",
            "excludes substantial portions",
            "cannot establish a causal atl airport effect",
            "31 observed operating days per month",
            "not make an operational change",
        ):
            with self.subTest(text=text):
                self.assertIn(text, lower)
        self.assertNotIn("confidence interval of", lower)
        self.assertNotIn("airport caused the gap", lower)
        self.assertNotIn("preventable savings", lower)

    def test_source_link_and_mobile_table_semantics(self):
        parser = ExhibitParser()
        parser.feed(self.section)
        self.assertIn(RESULTS_URL, parser.links)
        self.assertEqual(parser.table_count, 1)
        self.assertEqual(parser.rows, 3)
        self.assertEqual(len(parser.regions), 1)
        self.assertEqual(parser.regions[0].get("tabindex"), "0")
        self.assertIn("<caption>", self.section)
        self.assertEqual(self.section.count('scope="col"'), 3)
        self.assertEqual(self.section.count('scope="row"'), 2)

    def test_preexisting_population_values_unchanged(self):
        for text in (
            "76,306",
            "94,066",
            "74,025",
            "92,245",
            "−5.28 pp",
            "−2.52 pp",
            "53,047",
            "71,881",
        ):
            with self.subTest(text=text):
                self.assertIn(text, PAGE)


if __name__ == "__main__":
    unittest.main()
