# Aviation Operations & Analytics — Portfolio

[**View live portfolio**](https://yumorepos.github.io/) · [**Network Lab case study**](https://yumorepos.github.io/network-lab.html) · [**Interactive airline research dashboard**](https://network-lab-tweqoqjxhfrhj7imgmuftl.streamlit.app/)

This repository hosts a public, recruiter-facing technical portfolio focused on **airline operations analytics, network planning, geospatial data, data engineering and decision support**.

## Three flagship aviation case studies

| Case study | What it demonstrates | Evidence boundary |
| --- | --- | --- |
| [01 · Airline Network Planning & Model Validation](network-lab.html) | Python/DuckDB route screening, source reconciliation and historical replay against a demand-only baseline | No detectable incremental ranking lift at the study's resolution; not a validated route-success predictor |
| [02 · Airline Operational Performance & Reliability](airline-operations.html) | Verified BTS Delta Jan/Jul 2025 domestic reporting-carrier KPIs, local-time reconstruction and independently checked SQL aircraft-connection candidates | Two descriptive snapshots; candidate aircraft connections are not complete rotations, and delay associations are not causal |
| [03 · Disruption Recovery Optimization](disruption-recovery.html) | [Synthetic MILP experiment](https://github.com/yumorepos/network-lab/tree/main/experiments/disruption_recovery), finite reference verification and cost-aware greedy comparison | Fictional inputs; no measured airline operating savings or production deployment |

**Source repositories:** [Network Lab](https://github.com/yumorepos/network-lab) · [Fleet Tracker (Delta reliability study)](https://github.com/yumorepos/fleet-tracker) · [Avgeek Intelligence Lab (selectively reusable, some demo modules)](https://github.com/yumorepos/avgeek-intelligence-lab).

The three case studies are the primary portfolio. Other projects on the site are labeled separately and should not be interpreted as operational airline products. Each study documents its question, methods, verification, decision implications, and limitations.

## Website structure

| Path | Purpose |
| --- | --- |
| `index.html` | Homepage and three-study portfolio overview |
| `network-lab.html` | Network planning and validation case study |
| `airline-operations.html` | Historical Delta operational reliability study |
| `disruption-recovery.html` | Synthetic operations research and optimization study |
| `case-study.html` | Archived, separately labeled engineering work |
| `style.css`, `main.js` | Shared presentation and interactions |
| `tests/`, `scripts/` | Link, research-claim, public-tree, browser and accessibility checks |
| `.github/workflows/` | Automated source and browser-related checks |

The website is static HTML/CSS/JavaScript, hosted on GitHub Pages. The separate Streamlit dashboard is deployed from the Network Lab repository.

## Local checks

Run from the repository root:

```bash
python -m unittest discover -s tests -p 'test_*.py' -v
```

Open `index.html` locally to inspect the layout. For final review, confirm the public links, mobile navigation, accessibility and current Streamlit views manually; automated HTML checks cannot verify the rendered deployment.

## Publication and privacy

This is an intentionally **public portfolio**. It should contain project evidence and contact links that the owner has approved—not transcripts, personal background documents, private credentials, stale résumé PDFs or employers' internal files.

An outdated résumé PDF was removed from the current public branch in November 2026. **Deletion from `main` does not erase public Git history, cached copies or forks.** A current, tailored résumé should be supplied directly with job applications rather than treated as a permanent public download.

Use `main` as the published GitHub Pages source. Before updating live pages, review the diff, run CI and inspect the deployed result.
