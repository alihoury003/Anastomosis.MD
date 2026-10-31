#!/usr/bin/env python3
"""
unify_favicons.py — one favicon set, every page.

The site's pages each carried a single inline icon, and they disagreed
(index = the mark at 48px, dashboard = an old dark 64px variant, pricing =
a legacy .ico payload...). This replaces every icon link on every page with
the social-kit set:
    16 + 32 + 48 PNG data URIs (16/32 = small-size cut, 48 = native)
    + apple-touch-icon 180 data URI
and adds the og / twitter card block to index.html and pricing.html
(og:image = the raw-GitHub URL of og-1200x630.png once it is on main).

Idempotent: strips ALL icon links (including a previous run's) and any
previous og-card block, then inserts the current set exactly once.

Deploy note: root PNG/ICO files are not served by the static host (they
fall back to index.html), which is exactly why the favicons ride inline.
"""
import base64
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PAGES = ['index.html', 'dashboard.html', 'pricing.html', 'login.html', 'signup.html',
         'forgot-password.html', 'reset-password.html', 'terms.html', 'privacy.html',
         'refund-policy.html', 'import.html']
OG_PAGES = {'index.html', 'pricing.html'}
RAW_OG = 'https://raw.githubusercontent.com/alihoury003/Anastomosis.MD/main/og-1200x630.png'

ICON_RE = re.compile(
    r'[ \t]*<link[^>]*rel=["\']?(?:shortcut icon|icon|apple-touch-icon[^"\']*)["\']?[^>]*>[ \t]*\n?',
    re.I)
FAV_BLOCK_RE = re.compile(r'[ \t]*<!-- favicon: anastomosis social kit -->.*?<!-- /favicon -->[ \t]*\n?', re.S)
OG_BLOCK_RE = re.compile(r'[ \t]*<!-- og-card -->.*?<!-- /og-card -->[ \t]*\n?', re.S)


def b64(path):
    with open(os.path.join(HERE, path), 'rb') as f:
        return base64.b64encode(f.read()).decode()


def build_snippet():
    fv = 'social-kit/favicon'
    return ('<!-- favicon: anastomosis social kit -->\n'
            '<link rel="icon" type="image/png" sizes="16x16" href="data:image/png;base64,' + b64(fv + '/favicon-16.png') + '">\n'
            '<link rel="icon" type="image/png" sizes="32x32" href="data:image/png;base64,' + b64(fv + '/favicon-32.png') + '">\n'
            '<link rel="icon" type="image/png" sizes="48x48" href="data:image/png;base64,' + b64(fv + '/favicon-48.png') + '">\n'
            '<link rel="apple-touch-icon" href="data:image/png;base64,' + b64(fv + '/apple-touch-icon.png') + '">\n'
            '<!-- /favicon -->')


def build_og(title, desc):
    return ('<!-- og-card -->\n'
            f'<meta property="og:type" content="website">\n'
            f'<meta property="og:title" content="{title}">\n'
            f'<meta property="og:description" content="{desc}">\n'
            f'<meta property="og:image" content="{RAW_OG}">\n'
            f'<meta property="og:image:width" content="1200">\n'
            f'<meta property="og:image:height" content="630">\n'
            f'<meta property="og:image:alt" content="Anastomosis.MD — two vessels, one mind">\n'
            f'<meta name="twitter:card" content="summary_large_image">\n'
            '<!-- /og-card -->')


def main():
    snip = build_snippet()
    for page in PAGES:
        p = os.path.join(HERE, page)
        src = open(p, errors='replace').read()
        removed = len(ICON_RE.findall(src)) + len(FAV_BLOCK_RE.findall(src))
        og_removed = len(OG_BLOCK_RE.findall(src))
        out = ICON_RE.sub('', src)
        out = FAV_BLOCK_RE.sub('', out)
        out = OG_BLOCK_RE.sub('', out)
        block = snip + '\n'
        if page in OG_PAGES:
            t = re.search(r'<title>([^<]*)</title>', out)
            d = re.search(r'<meta name="description" content="([^"]*)"', out)
            if not t or not d:
                print(f'  {page}: WARNING — title/description not found, og card skipped')
            else:
                block += build_og(t.group(1).strip(), d.group(1).strip()) + '\n'
        assert '</head>' in out, page
        out = out.replace('</head>', block + '</head>', 1)
        with open(p, 'w') as f:
            f.write(out)
        grew = len(out) - len(src)
        print(f'  {page}: removed {removed} old icon link(s)'
              + (f' + {og_removed} old og block(s)' if og_removed else '')
              + f', inserted unified set{" + og card" if page in OG_PAGES else ""} ({grew:+,} bytes)')
    # the og image itself goes to repo root for a flat upload to main
    import shutil
    shutil.copy(os.path.join(HERE, 'social-kit/og-1200x630.png'), os.path.join(HERE, 'og-1200x630.png'))
    print('  og-1200x630.png copied to repo root (for the flat upload + raw-GitHub og:image URL)')


if __name__ == '__main__':
    main()
