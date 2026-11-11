"""Static evidence, link, scope and illustration checks for recovery case study."""
from html.parser import HTMLParser
from pathlib import Path
import re
import unittest

ROOT=Path(__file__).resolve().parents[1]
class LinkScan(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links=[]
        self.ids=set()
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if a.get("id"):
            self.ids.add(a["id"])
        if tag=="a" and a.get("href"):
            self.links.append(a["href"])

class DisruptionRecoveryCaseStudy(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html=(ROOT/"disruption-recovery.html").read_text()
        cls.home=(ROOT/"index.html").read_text()

    def test_three_aviation_stories_on_homepage(self):
        self.assertIn('href="network-lab.html"',self.home)
        self.assertIn('href="airline-operations.html"',self.home)
        self.assertIn('href="disruption-recovery.html"',self.home)
        self.assertLess(self.home.index('href="airline-operations.html"'),
                        self.home.index('href="disruption-recovery.html"'))
        self.assertLess(self.home.index('href="disruption-recovery.html"'),
                        self.home.index('href="case-study.html"'))

    def test_exact_verified_benchmark_values(self):
        for v in ("413.62","503.67","1,269.00","2,109.03","90.05",
                  "12 cases","18","30 fictional","11 focused tests",
                  "byte-for-byte identical output"):
            self.assertIn(v,self.html)

    def test_honest_model_limits(self):
        for text in ("not real airline savings","crew legality","maintenance",
                     "only within enumerated paths","synthetic",
                     "does not include real airline schedules",
                     "not directly comparable"):
            self.assertIn(text,self.html.lower())
        self.assertNotIn("saved airlines millions",self.html.lower())

    def test_static_internal_links_resolve(self):
        scan=LinkScan()
        scan.feed(self.html)
        for href in scan.links:
            if href.startswith(("http:","https:","mailto:")):
                continue
            target,_,fragment=href.partition("#")
            if not target:
                self.assertIn(fragment,scan.ids)
                continue
            link=ROOT/target
            self.assertTrue(link.is_file(),href)
            if fragment:
                other=LinkScan()
                other.feed(link.read_text())
                self.assertIn(fragment,other.ids)

    def test_static_chart_values_and_no_js_dependency(self):
        nums=re.findall(r'class="ops-bar-fill[^"]*"\s+style="width:([\d.]+)%"',self.html)
        self.assertEqual(nums,["19.61","23.88","60.17","100"])
        self.assertIn('href="style.css"',self.html)
        self.assertNotIn("<script",self.html)

if __name__=="__main__":
    unittest.main()
