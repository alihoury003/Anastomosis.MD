#!/usr/bin/env python3
"""Build logo-lab/names.html — the renaming: top 10 candidate names, 3 icons each.
Composes per-name trio images (3-up on cream) with PIL and embeds them.
Handles 1/2/3 icons per name gracefully; names without icons yet get a 'next batch' note.
"""
import base64, io, os
from PIL import Image, ImageDraw

LAB = "/home/user/Medchanic.md/logo-lab"

NAMES = [
    dict(slug="myelin", name="Myelin", domain="myelin.md",
         why="Practice myelinates. The sheath that makes nerve signals faster \u2014 the neuroscience of learning itself, and the most honest metaphor for spaced repetition in the whole body.",
         note=None),
    dict(slug="reflex", name="Reflex", domain="reflex.md",
         why="Train until it\u2019s a reflex. Pattern recognition is the exam skill \u2014 this name IS the promise.",
         note=None),
    dict(slug="dose", name="Dose", domain="dose.md",
         why="Your daily dose of questions. One syllable, everyone\u2019s word, the daily habit baked into the name.",
         note=None),
    dict(slug="stat", name="Stat", domain="stat.md",
         why="The word every hospital shouts when it means NOW. Speed as a brand.",
         note="2 of 3 icons in the next batch"),
    dict(slug="atlas", name="Atlas", domain="atlas.md",
         why="The map of everything. Every med student already lives inside an atlas \u2014 Netter made the word theirs.",
         note="icons in the next batch"),
    dict(slug="vitals", name="Vitals", domain="vitals.md",
         why="The essentials, checked daily. The dashboard IS vitals \u2014 the name says what the product does.",
         note="icons in the next batch"),
    dict(slug="triage", name="Triage", domain="triage.md",
         why="Decide what matters first. The study skill and the clinical skill, one word.",
         note="icons in the next batch"),
    dict(slug="aorta", name="Aorta", domain="aorta.md",
         why="The main line. The biggest vessel carries everything \u2014 so should your qbank.",
         note="icons in the next batch"),
    dict(slug="differential", name="Differential", domain="differential.md",
         why="Think in differentials. The core clinical skill \u2014 and the name of the game concept from the old chat. The DNA survives.",
         note="icons in the next batch"),
    dict(slug="dopamine", name="Dopamine", domain="dopamine.md",
         why="The reward. The joke every med student makes about studying \u2014 and the loop our streaks run on.",
         note="icons in the next batch"),
]

CREAM = (243, 239, 230)
RULE = (221, 214, 198)

def compose_trio(slug):
    """Compose the name's icons side by side on one cream canvas. Returns path or None."""
    paths = [os.path.join(LAB, f"{slug}-{i}.png") for i in (1, 2, 3)]
    paths = [p for p in paths if os.path.exists(p)]
    if not paths:
        return None
    if len(paths) == 1:
        im = Image.open(paths[0]).convert("RGB").resize((520, 520), Image.LANCZOS)
        out = os.path.join(LAB, f"trio-{slug}.png")
        im.save(out, "PNG", optimize=True)
        return out
    size, gut = 380, 70
    w = len(paths) * size + (len(paths) + 1) * gut
    h = size + 2 * gut
    canvas = Image.new("RGB", (w, h), CREAM)
    d = ImageDraw.Draw(canvas)
    x = gut
    for i, p in enumerate(paths):
        im = Image.open(p).convert("RGB").resize((size, size), Image.LANCZOS)
        canvas.paste(im, (x, gut))
        x += size
        if i < len(paths) - 1:
            lx = x + gut // 2
            d.line([(lx, gut + 40), (lx, h - gut - 40)], fill=RULE, width=2)
            x += gut
    out = os.path.join(LAB, f"trio-{slug}.png")
    canvas.save(out, "PNG", optimize=True)
    return out

def uri(path, maxw=1180):
    im = Image.open(path).convert("RGB")
    if im.size[0] > maxw:
        im = im.resize((maxw, int(im.size[1] * maxw / im.size[0])), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=90, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()

sections = []
for i, n in enumerate(NAMES, 1):
    trio = compose_trio(n["slug"])
    img_html = f'<div class="trio"><img src="{uri(trio)}" alt="{n["name"]} — three icon directions"></div>' if trio else ""
    note_html = f'<div class="pending">{n["note"]}</div>' if n.get("note") else ""
    sections.append(f'''  <section class="namecard">
    <div class="eyebrow">CANDIDATE {i:02d} &middot; {n["domain"]}</div>
    <h2>{n["name"]}</h2>
    <p class="why">{n["why"]}</p>
    {img_html}{note_html}
  </section>''')

html = f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>The renaming — 10 candidates</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Instrument+Serif:ital@0;1&family=JetBrains+Mono:wght@400;600;700&display=swap" rel="stylesheet">
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
:root{{--paper:#F3EFE6;--card:#FFFDF8;--ink:#141311;--ink2:#4A4741;--ink3:#8A857A;--rule:#DDD6C6;--teal:#0E7C78;--teal2:#0A5F5C;--coral:#E4572E;
--sans:'Inter',system-ui,sans-serif;--serif:'Instrument Serif',Georgia,serif;--mono:'JetBrains Mono',monospace}}
body{{background:var(--paper);color:var(--ink);font-family:var(--sans);padding:48px 22px 90px}}
.wrap{{max-width:1100px;margin:0 auto}}
.eyebrow{{font-family:var(--mono);font-size:10px;letter-spacing:.2em;color:var(--teal);font-weight:700;text-transform:uppercase}}
h1{{font-family:var(--serif);font-style:italic;font-weight:400;font-size:clamp(36px,5vw,58px);margin:10px 0 8px}}
.sub{{color:var(--ink3);font-size:14.5px;line-height:1.6;max-width:720px;margin-bottom:44px}}
.namecard{{background:var(--card);border:1px solid var(--rule);border-radius:16px;padding:34px 38px 30px;margin-bottom:26px}}
.namecard h2{{font-family:var(--serif);font-style:italic;font-weight:400;font-size:46px;margin:8px 0 10px}}
.why{{font-size:14.5px;color:var(--ink2);line-height:1.65;max-width:760px;margin-bottom:20px}}
.trio{{border:1px solid var(--rule);border-radius:12px;overflow:hidden;background:var(--paper)}}
.trio img{{width:100%;height:auto;display:block}}
.pending{{margin-top:16px;font-family:var(--mono);font-size:10px;letter-spacing:.16em;text-transform:uppercase;color:var(--coral);font-weight:700}}
.foot{{margin-top:40px;font-family:var(--mono);font-size:10px;letter-spacing:.16em;color:var(--ink3);text-align:center;line-height:2}}
</style></head><body>
<div class="wrap">
  <div class="eyebrow">MEDCHANIC.MD &middot; THE RENAMING &middot; 23 OCT 2026</div>
  <h1>Ten new names.</h1>
  <p class="sub">Short, medical, meaningful — the school of \u201cSynapse\u201d, not the school of portmanteaus. Each name is something a med student already owns a feeling for, each works as a <b>name.md</b> domain, and each gets three icon directions. Verify domain and trademark availability before falling in love \u2014 the ones with known big-name neighbours are flagged below.</p>
{chr(10).join(sections)}
  <div class="foot">BATCH 1 OF 3 &middot; MYELIN &middot; REFLEX &middot; DOSE COMPLETE &middot; STAT 1/3 &middot; THE REST NEXT<br>SAY \u201cCONTINUE\u201d FOR THE NEXT TEN ICONS</div>
</div>
</body></html>'''

out = os.path.join(LAB, "names.html")
open(out, "w").write(html)
print("written:", out, os.path.getsize(out) // 1024, "KB")
for n in NAMES:
    icons = [i for i in (1, 2, 3) if os.path.exists(os.path.join(LAB, f"{n['slug']}-{i}.png"))]
    print(f"{n['slug']}: {len(icons)}/3 icons")
