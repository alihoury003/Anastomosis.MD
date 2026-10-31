#!/usr/bin/env python3
"""
build_social_kit.py — production social-media + favicon assets for Anastomosis.MD

From a single source mark (default: the live provisional mark, logo-lab/tw-9.png):
  1. master      — native resolution, paper background unified to brand bone (soft key)
  2. avatars     — 1024 master + 512/400/300/200 + 2048 (labelled upscale) + circle-transparent
  3. favicons    — tight square crop: favicon.ico (16+32+48) + PNG 16/32/48/180/192/512 + webmanifest
  4. og card     — 1200x630: mark + Instrument Serif gradient wordmark + mono tagline
  5. preview     — social-kit/preview.html (self-contained, base64-embedded, size ladders + tab mock)
  6. root favicon.ico is refreshed with the new multi-size icon

Re-run with any source mark (e.g. after the logo crown):
    python3 build_social_kit.py --source logo-lab/<mark>.png
"""
import argparse, base64, io, json, os, shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFont

BONE = (247, 243, 235)
INK, CRIMSON, PETROL, GOLD = (16, 20, 24), (181, 52, 42), (27, 78, 95), (201, 151, 60)
INK3 = (138, 133, 122)
HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.join(HERE, 'social-kit')

def b64(img, fmt='PNG'):
    buf = io.BytesIO(); img.save(buf, fmt); return base64.b64encode(buf.getvalue()).decode()

def load_master(src):
    """Native-resolution master with the paper background unified to brand bone."""
    im = Image.open(src).convert('RGB')
    a = np.asarray(im).astype(np.float32)
    h, w = a.shape[:2]
    # background tone from clean corners
    pads = [a[:12, :12], a[:12, -12:], a[-12:, :12], a[-12:, -12:]]
    bg = np.concatenate([p.reshape(-1, 3) for p in pads]).mean(axis=0)
    d = np.abs(a - bg).sum(axis=2)
    t = 36.0
    wt = np.clip((t - d) / t, 0, 1)[..., None]          # 1 = background, 0 = mark
    bone = np.array(BONE, np.float32)
    out = a * (1 - wt) + bone * wt
    master = Image.fromarray(out.clip(0, 255).astype(np.uint8))
    info = bg_tone=tuple(bg.round().astype(int))
    return master, bg_tone

def content_bbox(master):
    a = np.asarray(master).astype(np.int16)
    d = np.abs(a - np.array(BONE)).sum(axis=2)
    mask = d > 60
    ys, xs = np.where(mask)
    return int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())

def circle_metric(master):
    """share of content pixels outside the inscribed circle (must be ~0 for avatars)"""
    a = np.asarray(master).astype(np.int16)
    d = np.abs(a - np.array(BONE)).sum(axis=2)
    ys, xs = np.where(d > 60)
    h, w = d.shape
    r = np.hypot(xs - w/2, ys - h/2)
    outside = int((r > w/2).sum())
    return outside, float(r.max()) if len(r) else 0.0, int(len(r))

def square_crop(master, bbox, pad_frac):
    x0, y0, x1, y1 = bbox
    bw, bh = x1 - x0, y1 - y0
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    side = int(max(bw, bh) * (1 + 2 * pad_frac))
    side = min(side, master.size[0])
    left = max(0, min(master.size[0] - side, cx - side // 2))
    top = max(0, min(master.size[1] - side, cy - side // 2))
    return master.crop((left, top, left + side, top + side))


def small_cut(crop512, dil=5, ink=(86, 58, 60)):
    """small-size cut: dilate the ink so 16/32px keep their presence (pro favicon practice)"""
    import numpy as np
    from PIL import ImageFilter
    a = np.asarray(crop512).astype(np.int16)
    content = np.abs(a - np.array(BONE)).sum(axis=2) > 60
    mask = Image.fromarray((content * 255).astype(np.uint8))
    dilated = np.asarray(mask.filter(ImageFilter.MaxFilter(dil))) > 0
    grow = dilated & ~content
    out = np.asarray(crop512).copy()
    out[grow] = ink
    return Image.fromarray(out)

def write_ico(path, images):
    """multi-size .ico with PNG-embedded frames (per-size control)"""
    import struct
    blobs = []
    for im in images:
        buf = io.BytesIO(); im.save(buf, 'PNG'); blobs.append(buf.getvalue())
    n = len(blobs)
    out = struct.pack('<HHH', 0, 1, n)
    offset = 6 + 16 * n
    for im, b in zip(images, blobs):
        out += struct.pack('<BBBBHHII', im.size[0] % 256, im.size[1] % 256, 0, 0, 1, 32, len(b), offset)
        offset += len(b)
    with open(path, 'wb') as f:
        f.write(out + b''.join(blobs))

def gradient_wordmark(text, font_path, size, stops):
    """serif wordmask with the arteriovenous gradient, returned as RGBA on transparent"""
    font = ImageFont.truetype(font_path, size)
    tmp = Image.new('L', (10, 10)); dr = ImageDraw.Draw(tmp)
    box = dr.textbbox((0, 0), text, font=font)
    tw, th = box[2] - box[0], box[3] - box[1]
    mask = Image.new('L', (tw + 8, th + 12), 0)
    ImageDraw.Draw(mask).text((4 - box[0], 4 - box[1]), text, font=font, fill=255)
    W = mask.size[0]
    grad = np.zeros((mask.size[1], W, 3), np.uint8)
    xs = np.linspace(0, 1, W)
    for ch in range(3):
        pieces, last = [], 0.0
        for (p0, c0), (p1, c1) in zip(stops, stops[1:]):
            seg = np.clip((xs - p0) / (p1 - p0), 0, 1)
            pieces.append(c0[ch] + (c1[ch] - c0[ch]) * seg)
        grad[:, :, ch] = np.maximum.reduce(pieces).astype(np.uint8)
    out = Image.fromarray(grad, 'RGB').convert('RGBA')
    out.putalpha(mask)
    return out

def tracked_text(draw, xy, text, font, fill, tracking):
    x, y = xy
    for chx in text:
        draw.text((x, y), chx, font=font, fill=fill)
        x += draw.textlength(chx, font=font) + tracking

def build(source, no_md=False):
    os.makedirs(KIT, exist_ok=True)
    for sub in ('avatar', 'favicon', 'fonts'):
        os.makedirs(os.path.join(KIT, sub), exist_ok=True)
    report = []

    master, bg_tone = load_master(source)
    native = master.size[0]
    # the active brand mark: with or without the gold .md (--no-md)
    MD_BOX = (571, 719, 700, 781)
    no_md_img = master.copy()
    ImageDraw.Draw(no_md_img).rectangle(MD_BOX, fill=BONE)
    mark = no_md_img if no_md else master
    mark.save(os.path.join(KIT, 'avatar', f'avatar-{native}.png'))
    # upscaled master (labelled) + platform sizes
    mark.resize((2048, 2048), Image.LANCZOS).save(os.path.join(KIT, 'avatar', 'avatar-2048.png'))
    for s in (512, 400, 300, 200):
        mark.resize((s, s), Image.LANCZOS).save(os.path.join(KIT, 'avatar', f'avatar-{s}.png'))
    # circle-transparent variant
    s = 512
    sq = mark.resize((s, s), Image.LANCZOS).convert('RGBA')
    m = Image.new('L', (s, s), 0)
    ImageDraw.Draw(m).ellipse((0, 0, s - 1, s - 1), fill=255)
    sq.putalpha(m); sq.save(os.path.join(KIT, 'avatar', 'avatar-circle-512.png'))

    # ---- LOGO DELIVERABLES: two versions (with / without the gold ".md") ----
    # measured on the tw-9 source: the .md floats free of the trunk (trunk right edge <= x566)
    # and of the lower branches (start ~y830) -- safe box, verified by run-scan.
    no_md = no_md_img
    lg = os.path.join(KIT, 'logo')
    os.makedirs(lg, exist_ok=True)
    for name, img in [('anastomosis-md', master), ('anastomosis', no_md)]:
        img.save(os.path.join(lg, f'{name}-1024.png'))
        img.resize((2048, 2048), Image.LANCZOS).save(os.path.join(lg, f'{name}-2048.png'))
        img.resize((512, 512), Image.LANCZOS).save(os.path.join(lg, f'{name}-512.png'))
        img.resize((400, 400), Image.LANCZOS).save(os.path.join(lg, f'{name}-400.png'))
    logoA_b = b64(master.resize((480, 480), Image.LANCZOS))
    logoB_b = b64(no_md.resize((480, 480), Image.LANCZOS))
    outA, maxrA, totA = circle_metric(master)
    outB, maxrB, totB = circle_metric(no_md)
    logo_metric_a = f'{outA}/{totA} px outside the circle ({outA/totA*100:.3f}%), max radius {maxrA:.0f}/512'
    logo_metric_b = f'{outB}/{totB} px outside the circle ({outB/totB*100:.3f}%), max radius {maxrB:.0f}/512'
    report.append(f'logo: two versions built (anastomosis-md + anastomosis, .md box {MD_BOX} erased)')

    bbox = content_bbox(master)
    outside, maxr, total = circle_metric(master)
    report.append(f'source: {source} ({native}px native, background {bg_tone} -> bone {BONE})')
    report.append(f'content bbox: {bbox} | circle-crop: {outside}/{total} content px outside inscribed circle ({outside/total*100:.3f}%), max radius {maxr:.0f}/{native//2}')
    assert maxr <= native / 2, 'mark is not circle-crop safe — rescale before shipping'

    # ---- favicons: tight crop ----
    fc = square_crop(mark, bbox, 0.025).resize((512, 512), Image.LANCZOS)
    fcut = small_cut(fc)
    fv = os.path.join(KIT, 'favicon')
    fc.resize((48, 48), Image.LANCZOS).save(os.path.join(fv, 'favicon-48.png'))
    fcut.resize((32, 32), Image.LANCZOS).save(os.path.join(fv, 'favicon-32.png'))
    fcut.resize((16, 16), Image.LANCZOS).save(os.path.join(fv, 'favicon-16.png'))
    fc.save(os.path.join(fv, 'favicon-512.png'))
    fc.resize((192, 192), Image.LANCZOS).save(os.path.join(fv, 'favicon-192.png'))
    square_crop(mark, bbox, 0.08).resize((180, 180), Image.LANCZOS).save(os.path.join(fv, 'apple-touch-icon.png'))
    write_ico(os.path.join(fv, 'favicon.ico'), [fcut.resize((16, 16), Image.LANCZOS),
                                                fcut.resize((32, 32), Image.LANCZOS),
                                                fc.resize((48, 48), Image.LANCZOS)])
    shutil.copy(os.path.join(fv, 'favicon.ico'), os.path.join(HERE, 'favicon.ico'))
    manifest = {
        'name': 'Anastomosis.MD', 'short_name': 'Anastomosis',
        'icons': [
            {'src': '/favicon-192.png', 'sizes': '192x192', 'type': 'image/png'},
            {'src': '/favicon-512.png', 'sizes': '512x512', 'type': 'image/png'}],
        'theme_color': '#F7F3EB', 'background_color': '#F7F3EB', 'display': 'standalone'}
    open(os.path.join(fv, 'site.webmanifest'), 'w').write(json.dumps(manifest, indent=2))

    # ---- OG card 1200x630 ----
    serif = os.path.join(KIT, 'fonts', 'InstrumentSerif-Italic.ttf')
    mono = os.path.join(KIT, 'fonts', 'JetBrainsMono-Regular.ttf')
    W, H = 1200, 630
    card = Image.new('RGB', (W, H), BONE)
    mark_h = 348
    mk = mark.resize((mark_h, mark_h), Image.LANCZOS)
    card.paste(mk, ((W - mark_h) // 2, 30))
    stops = [(0.0, CRIMSON), (0.45, INK), (1.0, PETROL)]
    wm = gradient_wordmark('Anastomosis.MD', serif, 118, stops)
    if wm.size[0] > 1040:
        wm = wm.resize((1040, int(wm.size[1] * 1040 / wm.size[0])), Image.LANCZOS)
    card.paste(wm, ((W - wm.size[0]) // 2, 408), wm)
    dr = ImageDraw.Draw(card)
    tag = 'TWO VESSELS \u00b7 ONE MIND'
    fmono = ImageFont.truetype(mono, 27)
    track = 27 * 0.42
    total_w = sum(dr.textlength(c, font=fmono) for c in tag) + track * (len(tag) - 1)
    tracked_text(dr, ((W - total_w) / 2, 538), tag, fmono, INK3, track)
    card.save(os.path.join(KIT, 'og-1200x630.png'))

    # ---- preview page ----
    av1024 = b64(mark)
    av512 = b64(mark.resize((512, 512), Image.LANCZOS))
    av200 = b64(mark.resize((200, 200), Image.LANCZOS))
    mark.resize((240, 240), Image.LANCZOS).save(os.path.join(KIT, 'mark-240.jpg'), quality=85, optimize=True)
    fcut32 = b64(fcut.resize((32, 32), Image.LANCZOS))
    cmp16 = Image.new('RGB', (192, 80), (239, 233, 220))
    cmp16.paste(fc.resize((16, 16), Image.LANCZOS).resize((80, 80), Image.NEAREST), (4, 0))
    cmp16.paste(fcut.resize((16, 16), Image.LANCZOS).resize((80, 80), Image.NEAREST), (96, 0))
    cmp16 = b64(cmp16)
    fc32 = b64(fc.resize((32, 32), Image.LANCZOS))
    fc16 = b64(fc.resize((16, 16), Image.LANCZOS))
    fc48 = b64(fc.resize((48, 48), Image.LANCZOS))
    apple = b64(Image.open(os.path.join(fv, 'apple-touch-icon.png')))
    og = b64(card)
    snippet = (
        '<link rel="icon" type="image/png" sizes="16x16" href="data:image/png;base64,' + fc16 + '">\n'
        '<link rel="icon" type="image/png" sizes="32x32" href="data:image/png;base64,' + fc32 + '">\n'
        '<link rel="icon" type="image/png" sizes="48x48" href="data:image/png;base64,' + fc48 + '">\n'
        '<link rel="apple-touch-icon" href="data:image/png;base64,' + apple + '">')
    files = []
    for root, _, names in os.walk(KIT):
        for n in sorted(names):
            if n == 'preview.html' or n.endswith('.ttf'): continue
            p = os.path.join(root, n)
            rel = os.path.relpath(p, HERE).replace(os.sep, '/')
            files.append((rel, os.path.getsize(p)))
    rows = ''.join(
        f'<tr><td><code>{n}</code></td><td>{s:,} B</td><td><a href="{n}" download>download</a></td></tr>'
        for n, s in sorted(files))
    html = open(os.path.join(HERE, 'social_kit_preview_template.html'), errors='replace').read()
    for k, v in {
        '@@AV1024': av1024, '@@AV512': av512, '@@AV200': av200,
        '@@F16': fc16, '@@F32': fc32, '@@F48': fc48, '@@FCUT32': fcut32, '@@CMP16': cmp16, '@@APPLE': apple, '@@OG': og,
        '@@SNIPPET': snippet.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'), '@@ROWS': rows,
        '@@LOGO_A': logoA_b, '@@LOGO_B': logoB_b,
        '@@LOGO_METRIC_A': logo_metric_a, '@@LOGO_METRIC_B': logo_metric_b,
        '@@SRC': os.path.basename(source), '@@NATIVE': str(native),
        '@@BG': str(bg_tone),
        '@@METRIC': f'{outside}/{total} content pixels outside the inscribed circle ({outside/total*100:.3f}%) — max content radius {maxr:.0f} of {native//2}',
    }.items():
        html = html.replace(k, v)
    open(os.path.join(KIT, 'preview.html'), 'w').write(html)
    report.append('favicon.ico: 16+32+48 multi-size; 16/32 use the small-size cut (ink dilated for presence), 48+ native')
    report.append(f'og-1200x630.png: mark + serif gradient wordmark + tagline')
    report.append(f'active brand mark: ' + ('anastomosis (no .md)' if no_md else 'anastomosis.md') + ' -> avatars, favicons, og, mark-240.jpg')
    report.append('preview.html: self-contained preview written')
    for r in report: print('  ' + r)

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--source', default='logo-lab/tw-9.png')
    ap.add_argument('--no-md', action='store_true', help='brand mark without the gold .md')
    args = ap.parse_args()
    print(f'building social kit from {args.source}{" (no .md)" if args.no_md else ""} ...')
    build(args.source, args.no_md)
    print('done.')
