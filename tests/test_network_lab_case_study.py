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
                     "Smaller effects remain unresolved","LAUNCH","MONITOR","PASS"]:
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

    def test_exact_study_counts(self):
        import re
        s=(ROOT/"network-lab.html").read_text()
        expected={
            "WestJet · YYC":(76,0,0,76),
            "Alaska · SEA":(45,0,0,45),
            "Porter · YYZ":(79,1,1,77),
            "Total":(200,1,1,198),
        }
        for study,nums in expected.items():
            escaped=re.escape(study)
            matches=re.findall(r'<tr><th scope="row">'+escaped+r'</th>(.*?)</tr>',s)
            self.assertEqual(len(matches),1,study)
            vals=tuple(map(int,re.findall(r'<td>([0-9]+)</td>',matches[0])))
            self.assertEqual(vals,nums,study)
        self.assertEqual(sum(x[0] for k,x in expected.items() if k!="Total"),200)
    def test_public_project_links_do_not_point_to_private_repos(self):
        private_destinations = (
            "github.com/yumorepos/autonomous-trading-system",
            "github.com/yumorepos/polymarket-autopilot",
        )
        for path in ("index.html", "network-lab.html", "case-study.html"):
            text = (ROOT / path).read_text(encoding="utf-8").lower()
            for destination in private_destinations:
                self.assertNotIn(destination, text, path)

    def test_all_public_page_local_links_resolve(self):
        for path in ("index.html", "network-lab.html", "case-study.html"):
            s = (ROOT / path).read_text(encoding="utf-8")
            links = Scan()
            links.feed(s)
            for href in links.urls:
                if href.startswith(("http:", "https:", "mailto:")):
                    continue
                target, _, anchor = href.partition("#")
                if not target:
                    self.assertIn(anchor, links.ids, f"{path}: {href}")
                else:
                    linked = ROOT / target
                    self.assertTrue(linked.is_file(), f"{path}: {href}")
                    if anchor and target.endswith(".html"):
                        dest = Scan()
                        dest.feed(linked.read_text(encoding="utf-8"))
                        self.assertIn(anchor, dest.ids, f"{path}: {href}")

    def test_no_outdated_public_resume_or_pdf_links(self):
        # Resume content is application-specific, not permanent GitHub Pages collateral.
        self.assertFalse((ROOT / "Yumo-Xu-Resume.pdf").exists())
        for path in ("index.html", "network-lab.html", "case-study.html", "README.md"):
            text = (ROOT / path).read_text(encoding="utf-8").lower()
            self.assertNotIn("yumo-xu-resume.pdf", text, path)
        for path in ROOT.glob("*.pdf"):
            self.fail(f"Unexpected publicly hosted PDF: {path.name}")

if __name__=="__main__": unittest.main()
