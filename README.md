# APEX-07 Anastomosis.MD brand loader refresh

This package updates the real site files based on repository `main` commit `8f1197f` (2026-11-10 inspection), replacing the EKG overlays on the public homepage and dashboard with the Anastomosis.MD align → anastomose → perfuse loader.

## Included
- `index.html` — homepage loader markup and stylesheet/script references.
- `dashboard.html` — dashboard loader and data-ready dismissal.
- `brand-loader.css` and `brand-loader.js` — shared visuals, animation, reduced-motion handling, and safe timeouts.
- `APEX-07-loader-refresh.patch` — unified patch for the four changed files.

The homepage still contains the existing user-added PNG favicon link to `/icon-192.png`; no icon-line edit was removed or replaced. Existing payment/Paddle functionality and files are not modified by this package.

The dashboard overlay now stays visible through authentication, user-data and question-bank loading, and the initial screen renders. The homepage overlay starts directly after its markup, waits for both the animation and page `load` event, and includes click-to-skip and a 12-second safety fallback.

## Apply
From the repository root at the matching base commit, run:

```sh
git apply APEX-07-loader-refresh.patch
```

The patch is local-only: it has not been committed, pushed, or deployed.

## Checks performed
- `node --check brand-loader.js`
- `git diff --check`
- HTML parser checks for both pages, duplicate IDs, and local CSS/JS/image/icon references.

## Search-result favicon note
The live homepage already declares `/icon-192.png`, `/favicon.svg`, and `/favicon.ico`. The 192×192 PNG, SVG, and ICO URLs were checked; their artwork is the site's anatomical-heart mark, not a generic globe. The screenshot's generic globe is therefore consistent with Google's currently cached search-result favicon rather than a missing or incorrect site icon. Google controls when its Search favicon is refreshed; after deployment, inspect/request reindexing of the homepage in Search Console, but the display may take days or longer and cannot be guaranteed immediately.
