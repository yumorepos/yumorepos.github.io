"""Evidence-driven, local-link and terminology tests for Case Study 2."""
from html.parser import HTMLParser
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]

class LinkScan(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links=[]
        self.ids=set()
    def handle_starttag(self, tag, attrs):
        data=dict(attrs)
        if data.get("id"):
            self.ids.add(data["id"])
        if tag=="a" and data.get("href"):
            self.links.append(data["href"])

class AirlineOperationsCaseStudy(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.page=(ROOT/"airline-operations.html").read_text(encoding="utf-8")
        cls.home=(ROOT/"index.html").read_text(encoding="utf-8")

    def test_page_linked_from_portfolio(self):
        self.assertIn('href="airline-operations.html"',self.home)
        self.assertTrue((ROOT/"airline-operations.html").is_file())
        self.assertIn("Airline Operational Performance",self.page)

    def test_exact_source_counts_and_kpi_results(self):
        for x in ("76,306","94,066","74,025","92,245","80.68%","75.16%",
                  "2.80%","1.40%","0.19%","0.53%",
                  "53,047","71,881","77 / 74 min",
                  "66.63%","10.43%","68.54%","14.70%",
                  "28.90%","40.39%","27 offline tests"):
            self.assertIn(x,self.page,x)

    def test_no_unverified_operational_claims(self):
        lower=self.page.lower()
        for term in ("does not prove", "not certified","not delta's complete global network",
                     "two july observed same-tail pairs overlapped",
                     "three january flight records","candidate","sqlite window functions",
                     "no weather or seasonal cause","not verified complete aircraft rotations"):
            self.assertIn(term,lower,term)
        self.assertNotIn("actual maintenance events occurred",lower)
        self.assertNotIn("caused the next departure delay.",lower)

    def test_all_internal_page_links_resolve(self):
        scanner=LinkScan()
        scanner.feed(self.page)
        for url in scanner.links:
            if url.startswith(("https:","http:","mailto:")): continue
            dest,_,anchor=url.partition("#")
            if dest:
                file=ROOT/dest
                self.assertTrue(file.is_file(),url)
                if anchor:
                    linked=LinkScan()
                    linked.feed(file.read_text(encoding="utf-8"))
                    self.assertIn(anchor,linked.ids,url)
            elif anchor:
                self.assertIn(anchor,scanner.ids,url)

    def test_comparison_chart_is_data_labeled_and_mobile_styled(self):
        widths=re.findall(r'class="ops-bar-fill[^"]*"\s+style="width:(\d+\.\d+)%"',self.page)
        self.assertEqual(widths,["66.63","10.43","68.54","14.70"])
        style=(ROOT/"style.css").read_text()
        self.assertIn("@media(max-width:600px){.ops-bar-row",style)

if __name__=="__main__":
    unittest.main()
