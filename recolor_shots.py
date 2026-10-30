#!/usr/bin/env python3
"""Recolor the landing's REAL screenshots from the old palette to the Anastomosis palette.
Recovers the original captures from git history, maps every old-palette pixel to its
new counterpart (nearest-2 blend so anti-aliased edges stay smooth), passes everything
else through untouched (exam blues, whites, photos), and embeds them back into index.html
in place of the CSS mock shots."""
import base64, io, re, subprocess
import numpy as np
from PIL import Image

# old token -> new token (identity entries keep neutrals stable)
MAP = [
    ('F3EFE6', 'F7F3EB'), ('EAE5D8', 'EFE9DC'), ('FFFDF8', 'FFFDF8'), ('141311', '101418'),
    ('4A4741', '4A4741'), ('8A857A', '8A857A'), ('DDD6C6', 'E3DCCC'), ('E3DCCB', 'E9E2D2'),
    ('0E7C78', '1B4E5F'), ('0A5F5C', '143C4A'), ('D8ECE8', 'DDE8EC'),
    ('E4572E', 'B5342A'), ('C2441F', '8E2921'), ('FBE2D8', 'F2E1DD'),
    ('EFA21B', 'C9973C'), ('B87A0C', '9A742C'), ('FBEBC6', 'F4EAD4'),
    ('2A2825', '2A2E38'),
]
OLD = np.array([[int(h[i:i+2], 16) for i in (0, 2, 4)] for h, _ in MAP], dtype=np.float32)
NEW = np.array([[int(h[i:i+2], 16) for i in (0, 2, 4)] for _, h in MAP], dtype=np.float32)
T = 60.0  # pixels farther than this from every old token pass through unchanged

def recolor(img):
    if img.size[0] > 820:
        img = img.resize((820, int(img.size[1] * 820 / img.size[0])), Image.LANCZOS)
    arr = np.asarray(img.convert('RGB'), dtype=np.float32)
    h, w, _ = arr.shape
    flat = arr.reshape(-1, 3)
    # distances to every old token (chunked to bound memory)
    out = flat.copy()
    CH = 200_000
    for s in range(0, flat.shape[0], CH):
        p = flat[s:s+CH]                                    # (n,3)
        d = ((p[:, None, :] - OLD[None, :, :]) ** 2).sum(-1)  # (n,18)
        i1 = d.argmin(1)
        d1 = d.min(1)
        d2 = d.copy(); d2[np.arange(len(p)), i1] = 1e9
        i2 = d2.argmin(1)
        c1, c2 = OLD[i1], OLD[i2]
        n1, n2 = NEW[i1], NEW[i2]
        seg = c2 - c1
        denom = (seg ** 2).sum(1)
        denom[denom < 1e-6] = 1e-6
        wt = ((p - c1) * seg).sum(1) / denom
        wt = np.clip(wt, 0, 1)[:, None]
        blended = n1 * (1 - wt) + n2 * wt
        near = (d1 < T * T)[:, None]
        out[s:s+CH] = np.where(near, blended, p)
    return Image.fromarray(out.reshape(h, w, 3).astype(np.uint8))

def to_jpeg(img, max_kb=42):
    for q in (76, 74, 72, 70, 68, 66):
        b = io.BytesIO(); img.save(b, 'JPEG', quality=q, optimize=True, progressive=True)
        if b.tell() <= max_kb * 1024:
            return b.getvalue(), q
    return b.getvalue(), q

# ---- 1. recover originals from git (dfad85f = pre-retheme index with the real shots) ----
old_index = subprocess.run(['git', 'show', 'dfad85f:index.html'], capture_output=True, text=True).stdout
found = re.findall(r'<img src="data:image/jpeg;base64,([A-Za-z0-9+/=]+)" alt="([^"]*)"', old_index)
assert len(found) == 6, f'expected 6 originals, found {len(found)}'
imgs, alts = [f[0] for f in found], [f[1] for f in found]

# ---- 2. recolor + compress ----
payloads = []
for i, b64 in enumerate(imgs):
    im = Image.open(io.BytesIO(base64.b64decode(b64)))
    before = np.asarray(im.convert('RGB'), dtype=np.float32).reshape(-1, 3)
    rim = recolor(im)
    data, q = to_jpeg(rim)
    payloads.append(base64.b64encode(data).decode())
    print(f'shot-{i}: {im.size[0]}x{im.size[1]} -> {rim.size[0]}x{rim.size[1]} q{q} {len(data)//1024} KB')

# ---- 3. embed into index.html (replace the 6 mock lines, in document order) ----
src = open('index.html', encoding='utf-8').read()
lines = src.split('\n')
idxs = [n for n, l in enumerate(lines) if '<div class="shot"' in l or ('data:image/jpeg;base64' in l and 'product screenshot' in l and 'loading=' in l)]
assert len(idxs) == 6, f'expected 6 mock lines, found {len(idxs)}'
for n, alt in zip(idxs, alts):
    alt = alt.replace('Medchanic.MD', 'Anastomosis.MD')
    indent = re.match(r'\s*', lines[n]).group(0)
    lines[n] = f'{indent}<img src="data:image/jpeg;base64,{payloads.pop(0)}" alt="{alt}" loading="lazy">'
src = '\n'.join(lines)
# remove the now-unused mock CSS block
m = re.search(r'/\* ==== live product shots \(CSS-built, new palette\) ==== \*/.*?(?=\n</style>)', src, re.S)
if m:
    src = src[:m.start()] + src[m.end():]
    print('mock CSS removed')
open('index.html', 'w', encoding='utf-8').write(src)

# ---- 4. verify: decode an embedded shot, count old vs new palette pixels ----
print(f'index.html: {len(src)//1024} KB')
def near(arr, hexcolor, tol=28):
    c = np.array([int(hexcolor[i:i+2], 16) for i in (0, 2, 4)], dtype=np.float32)
    return (((arr - c) ** 2).sum(-1) < tol * tol).mean() * 100

emb = [p for p in re.findall(r'data:image/jpeg;base64,([A-Za-z0-9+/=]+)', src) if len(p) > 30000]
if emb:
    # the biggest payloads are the screenshots; test the first
    test = np.asarray(Image.open(io.BytesIO(base64.b64decode(emb[0]))).convert('RGB'), dtype=np.float32)
    print(f'verification on first embedded shot ({test.shape[1]}x{test.shape[0]}):')
    for old, new, name in [('0E7C78', '1B4E5F', 'teal->petrol'), ('E4572E', 'B5342A', 'coral->crimson'), ('EFA21B', 'C9973C', 'amber->gold')]:
        print(f'  {name}: {near(test, old):.2f}% old left | {near(test, new):.2f}% new present')
    print(f'  paper->bone: {near(test, "F3EFE6"):.2f}% old | {near(test, "F7F3EB"):.2f}% new')
else:
    print('WARNING: no embedded screenshots found!')
