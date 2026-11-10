# Aviation Operations & Analytics — Portfolio

[**View live portfolio**](https://yumorepos.github.io/) · [**Network Lab case study**](https://yumorepos.github.io/network-lab.html) · [**Interactive airline research dashboard**](https://network-lab-tweqoqjxhfrhj7imgmuftl.streamlit.app/)

This repository hosts a public, recruiter-facing technical portfolio focused on **airline operations analytics, network planning, geospatial data, data engineering and decision support**.

## Featured project: Network Lab

Network Lab screens potential routes across three fixed-aircraft, configured-schedule studies using public government aviation data. The project presents clear methods, source verification, a 200-market research snapshot, and a point-in-time replay of 463 historical candidate decisions.

**Evidence boundary:** Historical testing found **no detectable incremental ranking value** over a demand-only baseline at effects larger than the study's resolution. Smaller improvements remain unresolved. Network Lab is research-grade *fixed-gauge screening*, not a validated route-success predictor or live airline operations product.

- [Case study and visual summary](network-lab.html)
- [Source repository and reproducibility](https://github.com/yumorepos/network-lab)
- [Scope and assumptions](https://github.com/yumorepos/network-lab/blob/main/docs/FINAL_SCOPE_CONTRACT.md)
- [Limitations and historical audit](https://github.com/yumorepos/network-lab/blob/main/docs/LIMITATIONS.md)

## Site structure

| Path | Purpose |
|---|---|
| `index.html` | Homepage, skills, and project selection |
| `network-lab.html` | Primary aviation analytics case study |
| `case-study.html` | Clearly labeled archived engineering project |
| `style.css`, `main.js` | Shared presentation and interactions |
| `tests/` | Link, evidence and public-tree guard tests |
| `.github/workflows/ci.yml` | Checks run on push and pull requests |

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
