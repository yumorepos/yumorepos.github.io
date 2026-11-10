# Aviation Operations Analytics Portfolio — Program Charter
**Planning baseline:** 2026-11-09  
**Status:** Proposal / planning, not a declaration that the three case studies are published  
**Program owner:** Portfolio maintainer  
**Source of truth for published site:** `main` on `yumorepos/yumorepos.github.io`

## North star

Build **one recruiter-facing aviation operations analytics portfolio** containing exactly **three differentiated, evidence-backed case studies**. Reuse current code, data and validated research. The aim is to earn interviews for airline operations analytics, network planning, reliability/performance analysis, operations research or closely adjacent analyst roles—not to operate an airline-grade production system or build a broad consumer app.

Five hours per week is the *planning capacity*, not a deadline guarantee. Avoid unnecessary paid data, APIs and hosting. Keep job applications active throughout.

## Projects, boundaries, and asset reuse

| Portfolio case study | Primary question | Current assets | Skills signaled | Status and limits |
| --- | --- | --- | --- | --- |
| **1. Network Planning & Model Validation** | Can public demand/network evidence reliably screen route scenarios, and what survives historical testing? | [network-lab](https://github.com/yumorepos/network-lab) and its existing [public case study](https://yumorepos.github.io/network-lab.html) | Python, SQL/DuckDB, geospatial joins, data lineage, economics, baseline comparison, research integrity | Fixed-gauge research; historical replay found **no detectable incremental ranking lift above a demand-only baseline at the study's resolution**. Preserve negative finding; no route success claims. Geography audit/presentation validation remain explicit checks. |
| **2. Airline Operational Performance & Fleet Evidence** | Which historical schedule-variance, turnaround, delay-propagation, weather-exposure and aircraft-activity measures can public records actually support? | [fleet-tracker](https://github.com/yumorepos/fleet-tracker) collectors, DuckDB/Parquet and audits; reuse BTS ingest/statistical components from [avgeek-intelligence-lab](https://github.com/yumorepos/avgeek-intelligence-lab) | Operational KPI definitions, ETL/SQL, QA, event linking, longitudinal analysis, visualization and uncertainty | **Conditional pivot, not yet validated by a BTS pilot.** Start with Delta U.S. domestic reportable flights; retain aircraft activity as observed *proxy*, not true utilization. Do not assert actual maintenance events. |
| **3. Disruption Recovery & Optimization** | On clearly synthetic disruptions, how do constrained aircraft reassignment/cancellation choices compare with transparent baselines? | [network-lab disruption recovery](https://github.com/yumorepos/network-lab/blob/main/experiments/disruption_recovery/README.md) | MILP, operations research, constraints, independent oracle, reproducible evaluation, decision trade-offs | Existing educational optimizer has documented path-order correction and 30 synthetic scenario baseline comparison. It is **not** validated airline software, actual costs, or commercial savings. |

**Avgeek Intelligence Lab is a component source, not a fourth flagship app.** The static [portfolio website](https://yumorepos.github.io/) is the *only* public presentation home. Existing projects stay in their repositories unless a bounded, tested extraction is justified. Trading/housing/job automation projects remain secondary or archived—not deleted.

## Data feasibility policy

Candidate sources, subject to fresh documentation/access/licensing checks at implementation time:

- **BTS On-Time Performance**: U.S. reporting-carrier, primarily domestic historical reported flight segments with tail numbers where present; scheduled/actual times, elapsed/block times, cancellations and delay fields. Validate missing tail values, diversions, joins, day boundaries and carrier coverage before aggregating.
- **BTS T-100**: segment/market aggregates useful for aircraft-type/market context—not per-tail histories.
- **NOAA / Iowa Environmental Mesonet / federal historical weather**: time-aligned airport observations; document station coverage, timezone handling and absence of causal identification.
- **FAA NAS status / airport metadata**: airport operational context and reference mapping where archived coverage supports analysis; do not confuse live status with historical event data.
- **Statistics Canada airport movements and Canadian weather**: useful for airport-level context, not complete Canadian tail-level utilization.
- **OpenSky**: sample or supplementary aircraft activity with coverage, identity and access constraints; never represent it as all flights.
- **BTS DB1C / DB1B as applicable**: network/economic context only after survey vintages, sampling, and comparability have been checked.

**Evidence boundaries:** Observed aircraft block hours are not total aircraft utilization without availability/complete flight coverage; a long ground interval is not proof of maintenance; "air carrier delay" does not equal maintenance; weather association is not weather causation; tail-number joins must preserve uncertainty and tail swaps. No fabricated schedules, savings, live-feed claims, source licenses, or model results.

## Operating workflow and gates

1. **Verify before changing.** Read current repo `main`, README, tests, open PRs/issues and dashboard URLs. Check for later work before executing an old plan.
2. **Specify the decision.** Record business question, audience, precise metric definitions, dates, grain, source and known limitations.
3. **Run a narrow data pilot.** Measure actual source availability, coverage, missingness, key uniqueness, join reliability and unit/timezone correctness. Define go / revise / stop thresholds *before* scaling ingestion.
4. **Reproduce and compare.** Provide reproducible scripts, unit/integration tests, a simple baseline and (when relevant) sensitivity or holdout analysis.
5. **Publish a truthful case study.** Present the question, dataset, method, verified finding, validation, uncertainty, actionable implication and accessible chart; label demos/synthetic cases.
6. **Keep changes reviewable.** Prefer one small PR per deliverable, with tests and evidence. No rewriting history, publishing contact details, storing credentials or uploading employer-internal material. Never merge/deploy until checks pass.

### Definition of done (each case study)
- Public summary readable in 2–3 minutes: **problem → data → analysis → finding → limitation → business implication**.
- Working source/method links; version or date on data; claims traced to inspectable artifacts.
- Correct metric units and timezones; independently validated computations and regression tests where appropriate.
- One polished recruiter-friendly visualization, accessible/mobile layout and working links.
- Honest result whether positive, negative, or inconclusive. No unresolved P0 accuracy or privacy issue.
- README, GitHub profile links and resume talking points agree with published evidence.

## Roadmap (provisional 10–12 week envelope, ~5 hours/week)

| Phase | Focus | Exit gate |
| --- | --- | --- |
| **0. Inventory & program setup** (week 1) | Verify repo HEADs, open PRs, current site, evidence and issue ledger; agree strict 3-study structure | Current inventory, risks and acceptance criteria recorded |
| **1. Network Lab closeout** (weeks 1–3) | Finish geographic audit reconciliation and freeze scope; verify CI, dashboard, source citations, responsive case study | Flagship published with verified claims and recorded limitations |
| **2. Fleet/BTS pilot** (weeks 4–5) | Use two bounded Delta months (proposed Jan/Jul 2025); inspect tails, elapsed time, cancellations, sequencing, coverage and data rights | Written go / revise / stop decision and quality report. **Do not build a UI before passing.** |
| **3. Operational performance study** (weeks 6–8) | Only after pilot: publish schedule adherence, reliable turnarounds/delay chains, weather exposure; use aircraft activity as qualified extension | Reproducible metrics and second case study |
| **4. Recovery optimization study** (weeks 9–10) | Reuse existing MILP; reproduce tests and compare to stronger baseline; one bounded interactive/static scenario | Educational synthetic third case study with baseline and limitations |
| **5. Recruiter-facing polish** (weeks 11–12) | Update homepage, project cards, GitHub profile, resume bullets; test mobile links and chart accessibility | Cohesive three-story portfolio and concise interview walkthrough |

This is a **gated sequence**, not permission to spend all 12 weeks building. If evidence or employment priorities change, shorten scope. If the BTS pilot fails, publish a transparent data-quality study or pivot the second case study to airport-level reliability rather than claiming unavailable tail-level metrics.

## Weekly working agreement

Every session starts with:
1. **Current state:** which milestone, what was actually merged/published, and what remains unknown.
2. **One highest-value next action:** smallest testable artifact moving toward interview readiness.
3. **Execution/verification:** show commands, source links, tests and findings, clearly marking not-run or provisional assertions.
4. **Stop point:** update blockers, decisions, next action and estimated *effort budget* (not a delivery promise).

**Decision filter for new work:** Would this add a demonstrably distinct employer skill? Is relevant data usable and licensable? Can it be validated with available time? Does an existing repo already do it? If not compelling on all four, defer or reject.

## Initial backlog

- [ ] Verify current Network Lab audit/replay, dashboard and project claims against latest actual artifacts.
- [ ] Capture current open PR and issue inventory for all four aviation-facing repos plus portfolio site.
- [ ] Create case-study template and recruiter-readability checklist.
- [ ] Define the BTS Delta Jan/Jul 2025 pilot specification, inclusion/exclusion criteria and metric QA checks.
- [ ] Reproduce optimizer regression and 30-scenario baseline before any feature expansion.
- [ ] Verify website/mobile accessibility, broken links and GitHub-profile positioning.
- [ ] Create a lightweight decision log for GO / PIVOT / STOP outcomes.

## Out of scope without new evidence and explicit reprioritization

A new all-in-one app, full Astro Fleet Tracker dashboard, 24/7 fleet feed, maintenance-event inference, complete Canadian per-tail histories, airline production optimizer, paid datasets, speculative route performance claims, and fourth/fifth flagship case studies.
