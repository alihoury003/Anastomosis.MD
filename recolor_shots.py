#!/usr/bin/env python3
"""Recolor the landing's REAL screenshots old->new palette, at FULL original resolution.
Quality-first pipeline: no resizing (zero resampling blur), WebP q84+ — WebP beats
JPEG on UI screenshots at the same byte budget. Idempotent: recovers the originals
from git, recolors, embeds; replaces mocks or previously embedded shots."""
import base64, io, re, subprocess
import numpy as np
from PIL import Image, features

assert features.check('webp'), 'PIL built without WebP support'

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
T = 60.0

def recolor(img):
    """Map every old-palette pixel to its new counterpart. NO resize — full resolution in and out."""
    arr = np.asarray(img.convert('RGB'), dtype=np.float32)
    h, w, _ = arr.shape
    flat = arr.reshape(-1, 3)
    out = flat.copy()
    CH = 200_000
    for s in range(0, flat.shape[0], CH):
        p = flat[s:s+CH]
        d = ((p[:, None, :] - OLD[None, :, :]) ** 2).sum(-1)
        i1 = d.argmin(1); d1 = d.min(1)
        d2 = d.copy(); d2[np.arange(len(p)), i1] = 1e9
        i2 = d2.argmin(1)
        c1, c2 = OLD[i1], OLD[i2]
        n1, n2 = NEW[i1], NEW[i2]
        seg = c2 - c1
        denom = (seg ** 2).sum(1); denom[denom < 1e-6] = 1e-6
        wt = np.clip(((p - c1) * seg).sum(1) / denom, 0, 1)[:, None]
        blended = n1 * (1 - wt) + n2 * wt
        near = (d1 < T * T)[:, None]
        out[s:s+CH] = np.where(near, blended, p)
    return Image.fromarray(out.reshape(h, w, 3).astype(np.uint8))

def to_webp(img, max_kb=68):
    for q in (86, 84, 82, 80, 78):
        b = io.BytesIO()
        img.save(b, 'WEBP', quality=q, method=6)
        if b.tell() <= max_kb * 1024:
            return b.getvalue(), q
    return b.getvalue(), q

# ---- 1. originals from git (full 1100px, pre-retheme) ----
old_index = subprocess.run(['git', 'show', 'dfad85f:index.html'], capture_output=True, text=True).stdout
found = re.findall(r'<img src="data:image/jpeg;base64,([A-Za-z0-9+/=]+)" alt="([^"]*)"', old_index)
assert len(found) == 6, f'expected 6 originals, found {len(found)}'

# ---- 2. recolor at full resolution + WebP ----
payloads = []
for i, (b64, alt) in enumerate(found):
    im = Image.open(io.BytesIO(base64.b64decode(b64)))
    rim = recolor(im)
    data, q = to_webp(rim)
    payloads.append(base64.b64encode(data).decode())
    print(f'shot-{i}: {im.size[0]}x{im.size[1]} FULL-RES webp q{q} {len(data)//1024} KB')

# ---- 3. embed (idempotent: replaces mocks OR previously embedded shots) ----
src = open('index.html', encoding='utf-8').read()
lines = src.split('\n')
idxs = [n for n, l in enumerate(lines)
        if '<div class="shot"' in l
        or ('data:image/jpeg;base64' in l and 'product screenshot' in l and 'loading=' in l)
        or ('data:image/webp;base64' in l and 'product screenshot' in l and 'loading=' in l)]
assert len(idxs) == 6, f'expected 6 shot lines, found {len(idxs)}'
for n, (b64, alt) in zip(idxs, found):
    alt = alt.replace('Medchanic.MD', 'Anastomosis.MD')
    indent = re.match(r'\s*', lines[n]).group(0)
    lines[n] = f'{indent}<img src="data:image/webp;base64,{payloads.pop(0)}" alt="{alt}" loading="lazy">'
src = '\n'.join(lines)
m = re.search(r'/\* ==== live product shots \(CSS-built, new palette\) ==== \*/.*?(?=\n</style>)', src, re.S)
if m:
    src = src[:m.start()] + src[m.end():]
open('index.html', 'w', encoding='utf-8').write(src)
print(f'index.html: {len(src)//1024} KB')

# ---- 4. verify: decode embedded shots, old vs new palette presence ----
def near(arr, hexcolor, tol=28):
    c = np.array([int(hexcolor[i:i+2], 16) for i in (0, 2, 4)], dtype=np.float32)
    return (((arr - c) ** 2).sum(-1) < tol * tol).mean() * 100
emb = [p for p in re.findall(r'data:image/webp;base64,([A-Za-z0-9+/=]+)', src) if len(p) > 30000]
names = ['block', 'report', 'analyst', 'explanations', 'flashcards', 'dashboard']
for i, p in enumerate(emb):
    a = np.asarray(Image.open(io.BytesIO(base64.b64decode(p))).convert('RGB'), dtype=np.float32)
    print(f"{names[i]:13s} {a.shape[1]}x{a.shape[0]} | old teal {near(a,'0E7C78'):5.2f}% | petrol {near(a,'1B4E5F'):5.2f}% | old coral {near(a,'E4572E'):5.2f}% | old amber {near(a,'EFA21B'):5.2f}%")
