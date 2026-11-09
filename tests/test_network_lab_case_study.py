from html.parser import HTMLParser
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]

class Scan(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls=[]
        self.ids=set()
        self.n_details=0
        self.n_summary=0
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if a.get("id"): self.ids.add(a["id"])
        if tag=="a" and a.get("href"): self.urls.append(a["href"])
        if tag=="details": self.n_details+=1
        if tag=="summary": self.n_summary+=1

class EvidenceChecks(unittest.TestCase):
    def test_case_study_and_local_links(self):
        s=(ROOT/"network-lab.html").read_text()
        scan=Scan()
        scan.feed(s)
        for term in ["200","463","demand-only","WestJet","Alaska","Porter",
                     "Smaller improvements remain unresolved","LAUNCH","MONITOR","PASS"]:
            self.assertIn(term.lower(),s.lower())
        self.assertNotIn("right-sized",s.lower())
        self.assertEqual(scan.n_details,scan.n_summary)
        self.assertEqual(scan.n_details,1)
        for url in scan.urls:
            if url.startswith(("http:","https:","mailto:")): continue
            path,_,frag=url.partition("#")
            if path:
                self.assertTrue((ROOT/path).is_file(),url)
                if frag and path.endswith(".html"):
                    target=Scan()
                    target.feed((ROOT/path).read_text())
                    self.assertIn(frag,target.ids)
            elif frag: self.assertIn(frag,scan.ids)
        for legacy in ["dashboard_route_screen.png","dashboard_scenario_grid.png"]:
            self.assertNotIn(legacy,s)
if __name__=="__main__": unittest.main()
