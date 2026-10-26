#!/usr/bin/env python3
"""Build logo-lab/insta.html — 'In the wild': the marks born inside Instagram profile views,
avatar-first, per the research (circle = filter; one subject; central 65%; 5-second draw test)."""
import base64, io, os
from PIL import Image

LAB = "/home/user/Medchanic.md/logo-lab"

def uri(name, maxw=980):
    im = Image.open(os.path.join(LAB, name)).convert("RGB")
    if im.size[0] > maxw:
        im = im.resize((maxw, int(im.size[1] * maxw / im.size[0])), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=90, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()

VIEWS = [
    ("ig-1.png", "The emblem, in the wild", "IG-1",
     "The vessel-join emblem as the avatar: artery loop, vein loop, gold crossing — centered, breathing room, one subject.",
     "Principle: the avatar is a symbol, not a lockup — detail dies at 110 px."),
    ("ig-2.png", "The A, in the wild", "IG-2",
     "The living A with the golden infinity crossbar, simplified to avatar scale — the letter still reads, the vessels still whisper.",
     "Principle: build a distinct icon version of the mark for exactly this use."),
    ("ig-3.png", "The circle-born loop", "IG-3",
     "NEW — the infinity scaled so its outer curves follow the circle's edge: the loop born for the crop. Crimson half, petrol half, gold at the heart.",
     "Principle: the circle is not a container, it is the frame — design inside it."),
    ("ig-4.png", "The seal", "IG-4",
     "NEW — the monogram A in a bold graphite ring: crimson and petrol diagonals, the gold infinity bar. A coin, a stamp, a guild badge.",
     "Principle: monograms make the strongest avatars — letters survive shrinking."),
    ("ig-5.png", "The negative-space disc", "IG-5",
     "NEW — one crimson disc with the infinity carved out of it, the vein flowing through the artery's field, one gold dot at the crossing. The five-second draw test, passed by construction.",
     "Principle: one shape + negative space = memorable; a stranger can draw it from memory."),
]

sections = []
for img, title, chip, note, principle in VIEWS:
    sections.append(f'''  <section class="view">
    <div class="viewhead"><span class="chip">{chip}</span><h2>{title}</h2></div>
    <div class="frame"><img src="{uri(img)}" alt="{title} — Instagram profile view"></div>
    <p class="note">{note}</p>
    <p class="principle">{principle}</p>
  </section>''')

html = f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>In the wild — Anastomosis.MD</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Instrument+Serif:ital@0;1&family=JetBrains+Mono:wght@400;600;700&display=swap" rel="stylesheet">
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
:root{{--bone:#F7F3EB;--card:#FFFDF8;--ink:#101418;--ink2:#4A4741;--ink3:#8A857A;--rule:#E2DCD0;
--crimson:#B5342A;--petrol:#1B4E5F;--gold:#C9973C;
--sans:'Inter',system-ui,sans-serif;--serif:'Instrument Serif',Georgia,serif;--mono:'JetBrains Mono',monospace}}
body{{background:var(--bone);color:var(--ink);font-family:var(--sans);padding:48px 22px 90px}}
.wrap{{max-width:920px;margin:0 auto}}
.eyebrow{{font-family:var(--mono);font-size:10px;letter-spacing:.22em;color:var(--petrol);font-weight:700;text-transform:uppercase}}
h1{{font-family:var(--serif);font-style:italic;font-weight:400;font-size:clamp(36px,5vw,56px);margin:10px 0 10px}}
.sub{{color:var(--ink3);font-size:14.5px;line-height:1.65;max-width:740px;margin-bottom:34px}}
.research{{background:var(--card);border:1px solid var(--rule);border-radius:14px;padding:22px 26px;margin-bottom:44px}}
.research h2{{font-family:var(--serif);font-style:italic;font-weight:400;font-size:26px;margin-bottom:12px}}
.research li{{font-size:13.5px;color:var(--ink2);line-height:1.7;margin-left:18px;margin-bottom:6px}}
.view{{margin-bottom:52px}}
.viewhead{{display:flex;align-items:baseline;gap:14px;margin-bottom:14px}}
.viewhead h2{{font-family:var(--serif);font-style:italic;font-weight:400;font-size:32px}}
.chip{{font-family:var(--mono);font-size:10px;letter-spacing:.14em;background:#DCE8EC;color:var(--petrol);padding:5px 10px;border-radius:4px;font-weight:700}}
.frame{{border:1px solid var(--rule);border-radius:16px;overflow:hidden;background:var(--card)}}
.frame img{{width:100%;height:auto;display:block}}
.note{{font-size:14.5px;color:var(--ink2);line-height:1.65;margin-top:14px;max-width:740px}}
.principle{{font-family:var(--mono);font-size:10.5px;letter-spacing:.08em;color:var(--gold);margin-top:8px;text-transform:uppercase;font-weight:700}}
.foot{{margin-top:48px;font-family:var(--mono);font-size:10px;letter-spacing:.16em;color:var(--ink3);text-align:center;line-height:2}}
</style></head><body>
<div class="wrap">
  <div class="eyebrow">ANASTOMOSIS.MD &middot; IN THE WILD &middot; AVATAR-FIRST &middot; 23 OCT 2026</div>
  <h1>Born in the profile view.</h1>
  <p class="sub">Per the new rule: every mark is now created inside the Instagram profile view — because that is where it will live or die. The rendered 3D style is dropped. What remains: flat marks, one subject, centered, built for the circle.</p>
  <div class="research">
    <h2>The research, applied.</h2>
    <ul>
      <li><b>The circle crop is a filter, not a container</b> — the mark lives in the central ~65% with breathing room; corners are dead territory.</li>
      <li><b>At 110 px, detail dies</b> — one subject, strong shapes, high contrast; the avatar is the symbol, never the full lockup.</li>
      <li><b>The 5-second test</b> — a stranger should be able to draw the mark from memory after seeing it once.</li>
      <li><b>One square icon everywhere</b> — the same 800&times;800 asset serves every platform.</li>
      <li><b>2&ndash;3 colours, negative space, symbol built into the form</b> — the freshest medical marks integrate, never decorate.</li>
    </ul>
  </div>
{chr(10).join(sections)}
  <div class="foot">ANASTOMOSIS.MD &middot; TWO VESSELS &middot; ONE MIND &middot; ONE ICON<br>FLAT ONLY FROM HERE &middot; THE CIRCLE IS THE FRAME</div>
</div>
</body></html>'''

out = os.path.join(LAB, "insta.html")
open(out, "w").write(html)
print("written:", out, os.path.getsize(out) // 1024, "KB")
