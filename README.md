# APEX-07 loader and transparent favicon refresh

Based on repository `main` commit `8f1197f`.

## Changes
- `index.html` and `dashboard.html` use the same full-screen Anastomosis.MD loader markup, SVG animation, colors, sizing, and status sequence. The dashboard's overlay waits for authentication, user/question data, and initial rendering before dismissal (and also waits for the sequence to complete).
- `brand-loader.css` and `brand-loader.js` contain the shared presentation and lifecycle code.
- `favicon.svg`, `favicon.ico`, `icon-192.png`, and `icon-512.png` now have transparent canvases, using the existing official red/teal mark. This removes the cream tile from browser-tab icons and the Google-facing PNG favicon. The existing 192×192 favicon link in `index.html` is retained. The Apple touch icon is unchanged.

## Google Search favicon
The homepage already linked a square PNG favicon and the favicon endpoints were reachable. The blue globe can remain in Search until Google refreshes its cached favicon. Verify the domain in Search Console using its DNS TXT record; keep that TXT record in DNS. Then use URL Inspection on `https://anastomosismd.com/`, run the live test, and request indexing. Google controls the refresh timing; this may take days or longer, with no instant guarantee.

## Files and application
Includes the updated HTML, shared loader files, favicon assets, this README, and `APEX-07-loader-refresh.patch`. Apply the patch from the repository root at the matching base:

```sh
git apply APEX-07-loader-refresh.patch
```

These changes are local only; they have not been committed, pushed, or deployed. No payment/Paddle files or features are changed.

## Checks
- `node --check brand-loader.js`
- `git diff --check`
- HTML parsing, duplicate-ID and local asset checks.
- Normalized comparison confirmed homepage/dashboard loader markup and SVG match except page-specific integration attributes.
- PNG/ICO alpha channels and ICO sizes (16, 32, 48 px) verified.
