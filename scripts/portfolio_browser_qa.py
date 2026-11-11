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
                    # Final source-backed analysis sections added after the
                    # earlier screenshot QA run must also survive narrow
                    # viewports. Tables are intentionally horizontally scrollable
                    # inside their labeled region, not the full document.
                    if filename=="airline-operations.html":
                        if page.locator("#origin-comparison .case-results-table tbody tr").count()!=3:
                            issues.append(f"{tag}: missing origin KPI comparison rows")
                        if page.locator("#origin-comparison .ops-bar-row").count()!=4:
                            issues.append(f"{tag}: missing carrier-reported cause comparisons")
                    if filename=="disruption-recovery.html":
                        if page.locator("#sensitivity .case-results-table tbody tr").count()!=5:
                            issues.append(f"{tag}: missing five synthetic sensitivity variants")
                        if width<=390:
                            region=page.locator("#sensitivity .case-table-scroll")
                            if region.count()!=1:
                                issues.append(f"{tag}: missing scrollable sensitivity table")
                            else:
                                bounds=region.evaluate("""el=>({
                                  outer:el.clientWidth,inner:el.scrollWidth,
                                  region:el.getAttribute('role'),
                                  focus:el.getAttribute('tabindex')
                                })""")
                                if bounds["outer"]<=0 or bounds["inner"]<bounds["outer"] or bounds["region"]!="region" or bounds["focus"]!="0":
                                    issues.append(f"{tag}: sensitivity table keyboard/scroll region invalid: {bounds}")
                    if pageerrors:
                        issues.append(f"{tag}: uncaught JS errors: "+str(pageerrors[:3]))
                    # A full-page screenshot does NOT implicitly scroll the
                    # viewport: intersection-observer fade-ins would otherwise
                    # be invisible in below-the-fold screenshots. Walk through
                    # the complete page before asserting and capturing it.
                    page.wait_for_load_state("load")
                    await_reveal=page.evaluate("""async () => {
                      // The site's html {scroll-behavior:smooth} makes basic
                      // scrollTo calls animate and miss target positions during
                      // fast automated walkthroughs. Force instant test-only
                      // navigation while preserving actual site CSS.
                      const root=document.documentElement;
                      const prior=root.style.scrollBehavior;
                      root.style.scrollBehavior='auto';
                      try {
                        const height=root.scrollHeight;
                        const stride=Math.max(180,Math.floor(innerHeight*0.55));
                        for(let y=0;y<=height;y+=stride){
                          window.scrollTo({top:y,behavior:'instant'});
                          await new Promise(resolve=>setTimeout(resolve,100));
                        }
                        window.scrollTo({top:height,behavior:'instant'});
                        await new Promise(resolve=>setTimeout(resolve,250));
                        window.scrollTo({top:0,behavior:'instant'});
                        await new Promise(resolve=>setTimeout(resolve,700));
                        const remaining=[...document.querySelectorAll('.fade-in:not(.visible)')];
                        return remaining.map(el=>({
                          selector:el.className,
                          position:Math.round(el.getBoundingClientRect().top+scrollY)
                        }));
                      } finally {
                        root.style.scrollBehavior=prior;
                      }
                    }""")
                    if await_reveal:
                        issues.append(f"{tag}: {len(await_reveal)} scroll-triggered sections did not become visible: {await_reveal[:5]}")
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
