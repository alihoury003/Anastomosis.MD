#!/usr/bin/env python3
"""
swap_mark.py — replace the embedded brand mark on every page.

The pages carried the old tw-9 jpeg (with the gold .md, on its original
paper tone) inline — often several times per page (multi-screen headers,
loader finale). This swaps every occurrence for the active kit mark
(social-kit/mark-240.jpg — currently the no-.md version on exact bone),
built by build_social_kit.py.

Idempotent: once no old embeds remain, re-running is a no-op.
"""
import base64
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
PAGES = ['index.html', 'dashboard.html', 'pricing.html', 'login.html', 'signup.html',
         'forgot-password.html', 'reset-password.html', 'terms.html', 'privacy.html',
         'refund-policy.html', 'import.html']


def main():
    m = re.search(r'const TW9 = "([^"]+)"', open(os.path.join(HERE, 'loader-demos.html'), errors='replace').read())
    old = m.group(1)
    new = base64.b64encode(open(os.path.join(HERE, 'social-kit', 'mark-240.jpg'), 'rb').read()).decode()
    total = 0
    for page in PAGES:
        p = os.path.join(HERE, page)
        src = open(p, errors='replace').read()
        n = src.count(old)
        if n:
            open(p, 'w').write(src.replace(old, new))
        already = src.count(new) - n  # embeds already on the new mark before this run
        total += n
        print(f'  {page}: {n} old embed(s) swapped' + (f' ({already} already current)' if already else ''))
    print(f'total swapped: {total}')


if __name__ == '__main__':
    main()
