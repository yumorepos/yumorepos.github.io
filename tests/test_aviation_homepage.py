"""Aviation case studies are immediately understandable and separated from archives."""
from pathlib import Path
from html.parser import HTMLParser
import unittest

ROOT=Path(__file__).resolve().parents[1]
HOME=(ROOT/"index.html").read_text(encoding="utf-8")
CSS=(ROOT/"style.css").read_text(encoding="utf-8")

class HeadingLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=="a" and a.get("href"):
            self.links.append(a["href"])

class AviationHomepage(unittest.TestCase):
    def test_hero_explains_actual_aviation_analytics_focus_without_javascript(self):
        hero=HOME.split('<!-- Hero -->',1)[1].split('<!-- About -->',1)[0]
        self.assertIn("I analyze airline",hero)
        self.assertIn("operations with evidence.",hero)
        self.assertIn("Python, SQL",hero)
        self.assertNotIn('class="gradient-text typewriter"',hero)

    def test_all_three_case_studies_have_genuine_findings_and_limits(self):
        a=HOME.split('<!-- Projects -->',1)[1].split('<!-- Skills -->',1)[0]
        for term in ("200","463","no detectable incremental ranking improvement",
                     "80.68%","75.16%","two distinct samples",
                     "12 better / 18 tied","no real airline savings"):
            self.assertIn(term,a)
        for i in ("01","02","03"):
            self.assertIn("CASE STUDY "+i+" / 03",a)

    def test_aviation_project_cards_are_separate_from_other_engineering(self):
        area=HOME.split('<!-- Aviation case studies continue in a dedicated two-column group -->',1)[1]
        flagship,additional=area.split('<div class="portfolio-secondary">',1)
        for p in ('airline-operations.html','disruption-recovery.html'):
            self.assertIn(p,flagship)
        self.assertNotIn('href="case-study.html"',flagship)
        self.assertIn("Autonomous Trading System",additional)
        self.assertIn('class="projects-grid aviation-portfolio-grid"',flagship)
        self.assertIn('class="projects-grid other-projects-grid"',additional)

    def test_homepage_html_div_nesting_is_balanced(self):
        # Prevent a successful text-only CI run with broken section wrappers.
        self.assertEqual(HOME.count("<div "),HOME.count("</div>"))

    def test_source_and_internal_navigation(self):
        parser=HeadingLinks()
        parser.feed(HOME)
        for link in ('network-lab.html','airline-operations.html','disruption-recovery.html'):
            self.assertIn(link,parser.links)
            self.assertTrue((ROOT/link).is_file())
        self.assertIn("@media(max-width:768px){.aviation-portfolio-grid",CSS)
        self.assertIn("grid-template-columns:1fr",CSS)

if __name__=="__main__":
    unittest.main()
