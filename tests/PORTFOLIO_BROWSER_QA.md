# Static portfolio browser QA — November 11, 2026

**Purpose:** Maintain the existing three-case-study portfolio without adding a
new site, dashboard or automatic data pipeline. Verify real headless browser
behavior (not just HTML string assertions).

[Successful original browser QA run](https://github.com/yumorepos/yumorepos.github.io/actions/runs/43104159435):
- Chromium / Playwright 1.57.0, checked four static pages at **1365, 390,
  and 320 px** viewports = **12 successful renders**.
- Checked major heading and container bounding boxes, document horizontal
  overflow, uncaught JavaScript errors and mobile menu open/close actions.
- All tests passed: **zero automated layout/interaction issues detected**.
- Screenshots and \`browser_qa.json\` retained as an Actions artifact for
  14 days. The artifact is for **manual** visual acceptance, not proof that
  someone has inspected every image.

To reproduce from repo root with compatible Python:

    python -m pip install playwright==1.57.0
    python -m playwright install chromium
    python scripts/portfolio_browser_qa.py --output browser_qa_artifacts

The workflow is deliberately **manual-only** (\`workflow_dispatch\`): no
scheduled screenshots or downloads. The offline browser renderer opens local
static files; remote Google font loading is disabled for deterministic checks.
Core analytical pages and graphs must still be manually inspected for chart
meaning, typographic hierarchy, and mobile readability before a claim of
complete visual quality assurance. The browser QA adds confidence but does not
verify external link freshness or domain-specific analysis correctness.
