# Approved Aviation Portfolio Program — November 9, 2026 Handoff

**State:** Approved plan and names; documentation-only draft on [PR #2](https://github.com/yumorepos/yumorepos.github.io/pull/2). This document does **not** imply any build, merge, public deployment, or GitHub code migration.

## Final approved public case-study names

1. **Network Lab — Airline Network Planning & Model Validation** — [network-lab](https://github.com/yumorepos/network-lab).
2. **Airline Operational Performance & Reliability** — selectively reuse [fleet-tracker](https://github.com/yumorepos/fleet-tracker) and [avgeek-intelligence-lab](https://github.com/yumorepos/avgeek-intelligence-lab).
3. **Airline Disruption Recovery Optimization** — reuse the [existing synthetic MILP](https://github.com/yumorepos/network-lab/blob/main/experiments/disruption_recovery/README.md).

Keep repository names and live URLs unchanged for now. The only public portfolio home is https://yumorepos.github.io/.

## Verified/documented research decisions

**Network Lab:** 200 research screens, 463 replay decisions documented. Its full route ranking showed **no detectable incremental ranking value over demand-only at the study's resolution**. Preserve the bounded negative conclusion and freeze model scope; current geography/CBSA audits, CI, live dashboard, and mobile QA need rechecking. Do not imply all issues fixed because a PR was closed.

**Operational Performance:** Fleet Tracker already includes Python, DuckDB/Parquet, OpenSky capture and data-quality audits. Avgeek has BTS on-time ingest and route marts, some demo-only UI. No need for another large frontend. Start with a **small Delta BTS on-time pilot, proposed January and July 2025**, and verify source field definitions, tail coverage, aircraft/day/time keys, canceled/diverted flights, overnight rollover, valid gate times, join continuity and licensing before computing any KPI. If per-tail data fail, pivot to airline/airport reliability. Do not infer actual maintenance or airline-wide utilization.

**Recovery Optimization:** Existing research MILP is based on synthetic flights, illustrates a documented path-ordering fix and includes a reported 30-scenario test against a weak greedy baseline. Reproduce tests and improve benchmark. Do not claim real airline savings, complete dispatch constraints or actual airline operations.

**Public-source candidates:**
- [BTS on-time](https://transtats.bts.gov/DL_SelectFields.aspx?QO_fu146_anzr=b0-gvzr&gnoyr_VQ=FGJ) for reported U.S. flight-level operational analysis;
- [BTS T-100](https://transtats.bts.gov/TableInfo.asp?QO_fu146_anzr=Nv4+Pn44vr45&gnoyr_VQ=FMG) for aggregate traffic, never complete per-tail histories;
- [NOAA Integrated Surface Database](https://www.ncei.noaa.gov/products/land-based-station/integrated-surface-database) for historical weather exposure, not proof of cause;
- [Statistics Canada aviation](https://www150.statcan.gc.ca/n1/en/subjects/transportation/air_transportation) for airport-level Canadian aggregates;
- [OpenSky](https://openskynetwork.github.io/opensky-api/rest.html) for supplementary observed movements, with coverage and access limitations;
- [DB1C/DB1B](https://www.bts.gov/topics/airlines-and-airports) for future O&D context only after survey-vintage comparability checks.

No BTS pilot, new full CI run, or exhaustive live-site/mobile verification was performed in the feasibility research. Preserve this distinction.

## Roadmap (~5 hours/week)

| Gate | Deliverable | Exit |
| --- | --- | --- |
| 0/1. Network Lab closeout | Current PR/CI/geography issue ledger; truthful site and dashboard | verified claims, resolved/documented caveats, no unvalidated modeling |
| 2. Delta data pilot | Jan/Jul 2025 BTS quality profile and GO/PIVOT/STOP | measured denominators, timing/join QA, source provenance |
| 3. Operations case study | delays, adherence, reliable turns/weather analysis | reproducible reported outcomes, no false utilization |
| 4. Recovery optimizer | existing MILP replay, stronger baseline, scenario story | tested synthetic results with constraints and limitations |
| 5. Portfolio polish | one public site, GitHub profile, case study links, interview summary | three 2–3 minute defensible case studies |

Keep targeted applications active. Don't make another all-in-one app, parallel dashboards or paid ingestion pipeline.

## Next conversation: copy/paste

> Resume the approved Aviation Operations Analytics Portfolio program from the November 9 handoff and GitHub draft PR #2. Use the three approved case-study names. First, perform a **read-only status review** of Network Lab and the public portfolio: check latest commits and PRs #33–#37, geographic/CBSA audit findings, frozen scope, actual metrics, CI and dashboard/mobile presentation. Distinguish resolved issues, documented limitations, open blockers and unverified claims. Choose the smallest verifiable next step; do not merge, deploy or modify frozen modeling without verified need. Report links, tests, blockers and next action. Only then scope the Delta BTS pilot, reusing Avgeek and Fleet Tracker.

**Additional chat-project attachments created separately:** `AVIATION_PORTFOLIO_START_HERE.md`, `AVIATION_PUBLIC_DATA_RESEARCH_NOTES.md`, `AVIATION_NEXT_SESSION_HANDOFF.md` and prior `aviation_portfolio_feasibility_audit_2026-11-09.md`. These must be uploaded to ChatGPT Project manually; a GitHub draft does not attach them to ChatGPT.
