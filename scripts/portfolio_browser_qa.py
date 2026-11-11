"""Manual browser verification of existing static portfolio pages.

Offline file:// fixture. Checks responsive content bounds and mobile menu
behavior; screenshots are review artifacts, not automatic visual approval.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
PAGES=("index.html","network-lab.html","airline-operations.html","disruption-recovery.html")
VIEWPORTS={"desktop":(1365,900),"mobile":(390,844),"small-mobile":(320,740)}
KEY_ELEMENTS={
  "index.html":(".hero-title",".nav-inner",".project-featured",".aviation-portfolio-grid",".portfolio-secondary"),
  "network-lab.html":(".case-hero h1",".nav-inner",".case-snapshot",".case-article"),
  "airline-operations.html":(".case-hero h1",".nav-inner",".case-snapshot",".case-article",".ops-figure"),
  "disruption-recovery.html":(".case-hero h1",".nav-inner",".case-snapshot",".case-article",".ops-figure"),
}

def run(output:Path):
    output.mkdir(parents=True,exist_ok=True)
    issues=[]
    audit=[]
    with sync_playwright() as pw:
        browser=pw.chromium.launch(headless=True)
        try:
            for label,(width,height) in VIEWPORTS.items():
                context=browser.new_context(viewport={"width":width,"height":height},device_scale_factor=1)
                # The portfolio's analytical content is self-contained. Offline
                # rendering should not depend on external font CDNs.
                context.route("https://fonts.googleapis.com/**",lambda route:route.abort())
                context.route("https://fonts.gstatic.com/**",lambda route:route.abort())
                for filename in PAGES:
                    page=context.new_page()
                    pageerrors=[]
                    page.on("pageerror",lambda error:pageerrors.append(str(error)))
                    page.goto((ROOT/filename).as_uri(),wait_until="domcontentloaded")
                    page.wait_for_timeout(220)
                    metrics=page.evaluate("""() => ({
                      viewport:window.innerWidth,
                      document:document.documentElement.scrollWidth,
                      headingCount:document.querySelectorAll('h1').length
                    })""")
                    tag=f"{filename} @ {label} ({width}px)"
                    if metrics["headingCount"]!=1:
                        issues.append(f"{tag}: expected exactly one H1, found {metrics['headingCount']}")
                    if metrics["document"]>width+2:
                        issues.append(f"{tag}: horizontal document overflow {metrics['document']} > {width}")
                    for selector in KEY_ELEMENTS[filename]:
                        locator=page.locator(selector).first
                        if locator.count()==0:
                            issues.append(f"{tag}: missing {selector}")
                            continue
                        box=locator.bounding_box()
                        if box is None:
                            issues.append(f"{tag}: {selector} lacks a visible layout box")
                        elif box["x"] < -3 or box["x"]+box["width"]>width+3:
                            issues.append(f"{tag}: {selector} extends beyond viewport, x={box['x']:.1f} width={box['width']:.1f}")
                    if filename=="index.html" and width<=390:
                        btn=page.locator("#mobile-menu-btn")
                        menu=page.locator("#mobile-menu")
                        if not btn.is_visible():
                            issues.append(f"{tag}: mobile menu control not visible")
                        else:
                            if btn.get_attribute("aria-expanded")!="false":
                                issues.append(f"{tag}: initial aria-expanded is not false")
                            btn.click()
                            if btn.get_attribute("aria-expanded")!="true" or not menu.is_visible():
                                issues.append(f"{tag}: mobile menu failed to open with accessible state")
                            page.locator('#mobile-menu a[href="#projects"]').click()
                            if btn.get_attribute("aria-expanded")!="false" or menu.is_visible():
                                issues.append(f"{tag}: mobile menu failed to close after navigation")
                    if pageerrors:
                        issues.append(f"{tag}: uncaught JS errors: "+str(pageerrors[:3]))
                    # A full-page screenshot does NOT implicitly scroll the
                    # viewport: intersection-observer fade-ins would otherwise
                    # be invisible in below-the-fold screenshots. Walk through
                    # the complete page before asserting and capturing it.
                    await_reveal=page.evaluate("""async () => {
                      const height=document.documentElement.scrollHeight;
                      const stride=Math.max(240,Math.floor(innerHeight*0.65));
                      for(let y=0;y<=height;y+=stride){
                        window.scrollTo(0,y);
                        await new Promise(resolve=>setTimeout(resolve,65));
                      }
                      window.scrollTo(0,height);
                      await new Promise(resolve=>setTimeout(resolve,200));
                      window.scrollTo(0,0);
                      await new Promise(resolve=>setTimeout(resolve,350));
                      return document.querySelectorAll('.fade-in:not(.visible)').length;
                    }""")
                    if await_reveal:
                        issues.append(f"{tag}: {await_reveal} scroll-triggered sections did not become visible")
                    snap=output/f"{Path(filename).stem}-{label}.png"
                    page.screenshot(path=str(snap),full_page=True,animations="disabled")
                    audit.append({"page":filename,"viewport":label,"width":width,
                                  "document_width":metrics["document"],
                                  "heading_count":metrics["headingCount"],
                                  "js_errors":pageerrors,"unrevealed_after_scroll":await_reveal,
                                  "screenshot":snap.name})
                    page.close()
                context.close()
        finally:
            browser.close()
    summary={"checked":len(audit),"issues":issues,"screenshots":audit,
             "note":"Bounding-box and interaction checks, not manual screenshot visual acceptance."}
    (output/"browser_qa.json").write_text(json.dumps(summary,indent=2)+"\n")
    print(json.dumps({"checked":len(audit),"issues":issues},indent=2))
    return len(issues)

if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output",type=Path,default=Path("browser_qa_artifacts"))
    args=p.parse_args()
    raise SystemExit(1 if run(args.output) else 0)
