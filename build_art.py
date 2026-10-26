#!/usr/bin/env python3
"""Build logo-lab/art.html — 'When you say anastomosis…' — the gallery of the six
monumental pieces: the name said out loud, at full scale."""
import base64, io, os
from PIL import Image

LAB = "/home/user/Medchanic.md/logo-lab"

def uri(name, maxw=1100):
    im = Image.open(os.path.join(LAB, name)).convert("RGB")
    if im.size[0] > maxw:
        im = im.resize((maxw, int(im.size[1] * maxw / im.size[0])), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=88, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()

PIECES = [
    ("art-1.png", "The Confluence", "ART-1",
     "Two rivers that remember being two, become one — the anastomosing delta seen from above, a single ring of gold where the waters first touch."),
    ("art-2.png", "The Trees That Became One", "ART-2",
     "Inosculation — the botanical anastomosis: two vascular trees grafting branch to branch until one circulation flows through both crowns."),
    ("art-3.png", "The Rose Window", "ART-3",
     "The Circle of Willis as sacred geometry — the brain's quiet covenant of backup paths, drawn as a wheel of hope."),
    ("art-4.png", "The Map of Joins", "ART-4",
     "The circulation charted as a country — every anastomosis a golden city of light on the vascular geography of a human being."),
    ("art-5.png", "Two Vessels, One Mind", "ART-5",
     "The oldest gesture in nature: two vascular beings reaching toward each other — and sharing one flow."),
    ("art-6.png", "Collateral", "ART-6",
     "There is always another way — the braided web of joins that no single blockage can stop. Redundancy as grace."),
]

sections = []
for img, title, chip, caption in PIECES:
    sections.append(f'''  <section class="piece">
    <div class="piecehead"><span class="chip">{chip}</span><h2>{title}</h2></div>
    <div class="frame"><img src="{uri(img)}" alt="{title} — Anastomosis.MD gallery piece"></div>
    <p class="caption">{caption}</p>
  </section>''')

html = f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>When you say anastomosis — the gallery</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Instrument+Serif:ital@0;1&family=JetBrains+Mono:wght@400;600;700&display=swap" rel="stylesheet">
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
:root{{--bone:#F7F3EB;--card:#FFFDF8;--ink:#101418;--ink2:#4A4741;--ink3:#8A857A;--rule:#E2DCD0;
--crimson:#B5342A;--petrol:#1B4E5F;--gold:#C9973C;
--sans:'Inter',system-ui,sans-serif;--serif:'Instrument Serif',Georgia,serif;--mono:'JetBrains Mono',monospace}}
body{{background:var(--bone);color:var(--ink);font-family:var(--sans);padding:56px 22px 100px}}
.wrap{{max-width:980px;margin:0 auto}}
.eyebrow{{font-family:var(--mono);font-size:10px;letter-spacing:.24em;color:var(--petrol);font-weight:700;text-transform:uppercase}}
h1{{font-family:var(--serif);font-style:italic;font-weight:400;font-size:clamp(38px,6vw,64px);margin:12px 0 14px}}
.poem{{font-family:var(--serif);font-style:italic;font-size:21px;line-height:1.75;color:var(--ink2);max-width:760px;margin-bottom:10px}}
.poem b{{color:var(--ink)}}
.sub{{color:var(--ink3);font-size:14px;line-height:1.65;max-width:720px;margin:18px 0 54px}}
.piece{{margin-bottom:72px}}
.piecehead{{display:flex;align-items:baseline;gap:14px;margin-bottom:14px}}
.piecehead h2{{font-family:var(--serif);font-style:italic;font-weight:400;font-size:34px}}
.chip{{font-family:var(--mono);font-size:10px;letter-spacing:.14em;background:#F3E4C7;color:#8A6116;padding:5px 10px;border-radius:4px;font-weight:700}}
.frame{{border:1px solid var(--rule);border-radius:16px;overflow:hidden;background:var(--card);box-shadow:0 18px 50px rgba(16,20,24,.08)}}
.frame img{{width:100%;height:auto;display:block}}
.caption{{font-size:14.5px;color:var(--ink2);line-height:1.7;margin-top:16px;max-width:760px}}
.foot{{margin-top:56px;font-family:var(--mono);font-size:10px;letter-spacing:.18em;color:var(--ink3);text-align:center;line-height:2.1}}
</style></head><body>
<div class="wrap">
  <div class="eyebrow">ANASTOMOSIS.MD &middot; THE GALLERY &middot; THE NAME, SAID OUT LOUD &middot; 23 OCT 2026</div>
  <h1>When you say anastomosis&hellip;</h1>
  <p class="poem">I think of <b>rivers</b> — two rivers that ran their whole lives toward the same valley. When they meet, neither loses itself at first: they <b>braid</b>, crimson beside blue, channels splitting and rejoining — and then, deeper in the valley, they become <b>one water that remembers being two</b>. I think of trees that grew into a single organism. Of the quiet circle of joins at the base of the brain — the body's promise that <b>there is always another way</b>.</p>
  <p class="sub">This is not a logo hunt anymore. This is what the name looks like at full scale — six monumental pieces, one for each meaning the word carries. The palette is the brand; the scale is the ambition; the subject is always the same: two flows, becoming one.</p>
{chr(10).join(sections)}
  <div class="foot">ANASTOMOSIS.MD &middot; TWO VESSELS &middot; ONE MIND &middot; ONE WATER THAT REMEMBERS BEING TWO<br>THE GALLERY &middot; SIX PIECES &middot; THE BIGGEST ART YET</div>
</div>
</body></html>'''

out = os.path.join(LAB, "art.html")
open(out, "w").write(html)
print("written:", out, os.path.getsize(out) // 1024, "KB")
