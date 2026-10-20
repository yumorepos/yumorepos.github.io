# Yumo — portfolio, Network Lab update

**Status:** GitHub Pages website source, updated 2026-10-20.

## Changes

- Updated the featured **Network Lab** project card to the user-approved short description.
- Added `network-lab.html`, a dedicated, factual long-form case study with methodology and independent-review links.
- Replaced outdated live-trading claims at the existing legacy `case-study.html` URL with a historical-project notice.
- Kept the established dark layout, typography, navbar, animations, and project cards.
- Updated the main page title and share metadata; removed nonexistent `og-image.png` references.
- Fixed the navigation-logo `href="#"` handler so it no longer attempts to `querySelector('#')`.

## Preview

Open `index.html` locally. Select **Read the case study** in the featured Network Lab card. Review desktop and mobile layouts before publishing.

## How to deploy safely

These **five website files** are maintained on the `main` branch of `yumorepos/yumorepos.github.io`:

- Replace `index.html`, `main.js`, and `style.css`.
- Add `network-lab.html`.
- Replace the old `case-study.html` with the included historical-project notice.

Review the old `Yumo-Xu-Resume.pdf` separately: the site no longer links it, but the old file may still remain accessible by direct URL on GitHub Pages. Check whether its contents are still current before leaving it publicly hosted.

## Evidence

- https://github.com/yumorepos/network-lab/blob/main/docs/FINAL_SCOPE_CONTRACT.md
- https://github.com/yumorepos/network-lab/blob/main/docs/FINAL_INDEPENDENT_REVIEW.md
- https://github.com/yumorepos/network-lab/blob/main/docs/LIMITATIONS.md

The independent review's numeric test counts are **reported historical results**, not re-run in this website edit. The live Streamlit demo link is intentionally omitted until availability is manually confirmed. The GitHub links were checked against accessible repository documents. LinkedIn and email addresses were preserved from the existing site but should be verified by the user.
