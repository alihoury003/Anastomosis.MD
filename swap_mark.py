#!/usr/bin/env python3
"""
swap_mark.py — replace every embedded brand mark on every page.

Old marks (all replaced):
  - the legacy tw-9 jpeg (the const TW9 in loader-demos.html)
  - the previous kit embed mark (git HEAD:social-kit/mark-240.jpg, if it differs)
New mark: social-kit/mark-240.jpg (built by build_social_kit.py — currently tw-6,
machine-verified spelling).

Idempotent: once no old embeds remain, re-running is a no-op.
"""
import base64
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
PAGES = ['index.html', 'dashboard.html', 'pricing.html', 'login.html', 'signup.html',
         'forgot-password.html', 'reset-password.html', 'terms.html', 'privacy.html',
         'refund-policy.html', 'import.html']


def main():
    import re
    old_marks = []
    m = re.search(r'const TW9 = "([^"]+)"', open(os.path.join(HERE, 'loader-demos.html'), errors='replace').read())
    if m:
        old_marks.append(('legacy tw-9', m.group(1)))
    new_b = base64.b64encode(open(os.path.join(HERE, 'social-kit', 'mark-240.jpg'), 'rb').read()).decode()
    try:
        prev = subprocess.run(['git', 'show', 'HEAD:social-kit/mark-240.jpg'], capture_output=True, cwd=HERE).stdout
        if prev:
            prev_b = base64.b64encode(prev).decode()
            if prev_b != new_b:
                old_marks.append(('previous kit mark', prev_b))
    except Exception:
        pass
    total = 0
    for page in PAGES:
        p = os.path.join(HERE, page)
        src = open(p, errors='replace').read()
        n = 0
        for _, old in old_marks:
            n += src.count(old)
            src = src.replace(old, new_b)
        if n:
            open(p, 'w').write(src)
        total += n
        print(f'  {page}: {n} old embed(s) swapped')
    print(f'total swapped: {total} (new mark: {len(new_b)} b64 chars/embed)')


if __name__ == '__main__':
    main()
