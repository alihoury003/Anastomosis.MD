#!/usr/bin/env python3
"""Build logo-lab/names.html — the renaming: wave 1 (10 candidates, dopamine front-runner
with 10 icons) + wave 2 (8 fresh names before we lock it in)."""
import base64, io, os
from PIL import Image, ImageDraw

LAB = "/home/user/Medchanic.md/logo-lab"

NAMES = [
    # ---- wave 1 ----
    dict(slug="dopamine", name="Dopamine", domain="dopamine.md",
         why="The reward. The joke every med student makes about studying \u2014 and the exact loop our streaks run on. The front-runner: D1 and D5 are already set aside in the picks.",
         note=None),
    dict(slug="myelin", name="Myelin", domain="myelin.md",
         why="Practice myelinates. The sheath that makes nerve signals faster \u2014 the neuroscience of learning itself.",
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
         note="icons on request"),
    dict(slug="vitals", name="Vitals", domain="vitals.md",
         why="The essentials, checked daily. The dashboard IS vitals \u2014 the name says what the product does.",
         note="icons on request"),
    dict(slug="triage", name="Triage", domain="triage.md",
         why="Decide what matters first. The study skill and the clinical skill, one word.",
         note="icons on request"),
    dict(slug="aorta", name="Aorta", domain="aorta.md",
         why="The main line. The biggest vessel carries everything \u2014 so should your qbank.",
         note="icons on request"),
    dict(slug="differential", name="Differential", domain="differential.md",
         why="Think in differentials. The core clinical skill \u2014 and the name of the game concept from the old chat.",
         note="icons on request"),
    # ---- wave 2: before we lock it in ----
    dict(slug="potential", name="Potential", domain="potential.md",
         why="The action potential \u2014 and yours. A neuron fires when it crosses the line; so will you. The best double meaning in medicine.",
         note="icons if this one survives", wave2=True),
    dict(slug="threshold", name="Threshold", domain="threshold.md",
         why="Every neuron has one. Cross it, and everything fires.",
         note="icons if this one survives", wave2=True),
    dict(slug="adrenaline", name="Adrenaline", domain="adrenaline.md",
         why="The other catecholamine. For when the exam is tomorrow.",
         note="icons if this one survives", wave2=True),
    dict(slug="endorphin", name="Endorphin", domain="endorphin.md",
         why="The high that carries you through the block.",
         note="icons if this one survives", wave2=True),
    dict(slug="serotonin", name="Serotonin", domain="serotonin.md",
         why="The mood molecule \u2014 studying that doesn\u2019t feel like suffering.",
         note="icons if this one survives", wave2=True),
    dict(slug="caffeine", name="Caffeine", domain="caffeine.md",
         why="Med school\u2019s fourth vital sign.",
         note="icons if this one survives", wave2=True),
    dict(slug="ion", name="Ion", domain="ion.md",
         why="Three letters, all charge. Every thought you\u2019ll ever have is one.",
         note="icons if this one survives", wave2=True),
    dict(slug="vesicle", name="Vesicle", domain="vesicle.md",
         why="Where dopamine waits before the release \u2014 the moment before the reward.",
         note="icons if this one survives", wave2=True),
]

CREAM = (243, 239, 230)
RULE = (221, 214, 198)

def compose_trio(slug):
    """Compose the name's icons on one cream canvas (grid if many). Returns path or None."""
    paths = [os.path.join(LAB, f"{slug}-{i}.png") for i in range(1, 11)]
    paths = [p for p in paths if os.path.exists(p)]
    if not paths:
        return None
    if len(paths) == 1:
        im = Image.open(paths[0]).convert("RGB").resize((520, 520), Image.LANCZOS)
        out = os.path.join(LAB, f"trio-{slug}.png")
        im.save(out, "PNG", optimize=True)
        return out
    if len(paths) > 5:
        size, gut = 280, 45
        rows = [paths[i:i + 5] for i in range(0, len(paths), 5)]
        w = 5 * size + 6 * gut
        h = len(rows) * size + (len(rows) + 1) * gut
        canvas = Image.new("RGB", (w, h), CREAM)
        d = ImageDraw.Draw(canvas)
        for r, row in enumerate(rows):
            y = gut + r * (size + gut)
            x = gut
            for i, p in enumerate(row):
                im = Image.open(p).convert("RGB").resize((size, size), Image.LANCZOS)
                canvas.paste(im, (x, y))
                x += size
                if i < len(row) - 1:
                    lx = x + gut // 2
                    d.line([(lx, y + 40), (lx, y + size - 40)], fill=RULE, width=2)
                    x += gut
        if len(rows) > 1:
            ly = gut + size + gut // 2
            d.line([(gut + 60, ly), (w - gut - 60, ly)], fill=RULE, width=2)
        out = os.path.join(LAB, f"trio-{slug}.png")
        canvas.save(out, "PNG", optimize=True)
        return out
    size, gut = (300, 50) if len(paths) > 3 else (380, 70)
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
    if n.get("wave2") and not any(s.get("wave2") for s in NAMES[:i - 1]):
        sections.append('''  <div class="wavehead">
    <div class="eyebrow">THE SECOND WAVE &middot; BEFORE WE LOCK IT IN</div>
    <h1 class="wavetitle">Eight more names.</h1>
    <p class="sub">The dopamine direction, challenged. Same rule: real words students say, catchy enough for a handle.</p>
  </div>''')
    trio = compose_trio(n["slug"])
    img_html = f'<div class="trio"><img src="{uri(trio)}" alt="{n["name"]} — icon directions"></div>' if trio else ""
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
<title>The renaming — waves one and two</title>
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
.wavehead{{margin:64px 0 34px;padding-top:44px;border-top:2px solid var(--rule)}}
.wavetitle{{margin:10px 0 8px}}
.wavehead .sub{{margin-bottom:0}}
.foot{{margin-top:40px;font-family:var(--mono);font-size:10px;letter-spacing:.16em;color:var(--ink3);text-align:center;line-height:2}}
</style></head><body>
<div class="wrap">
  <div class="eyebrow">MEDCHANIC.MD &middot; THE RENAMING &middot; 23 OCT 2026</div>
  <h1>Ten names, then eight more.</h1>
  <p class="sub">The Synapse formula, honoured properly: <b>real medical words students say every single day</b> \u2014 not anatomy-index curiosities. Dopamine leads \u2014 ten icon directions below \u2014 with D1 and D5 already set aside in the picks. Each works as a <b>name.md</b> domain. Verify availability before falling in love.</p>
{chr(10).join(sections)}
  <div class="foot">DOPAMINE &middot; TEN ICONS &middot; D1 + D5 IN THE PICKS &middot; EIGHT CHALLENGER NAMES ABOVE<br>SAY THE WORD FOR MORE OF ANY DIRECTION</div>
</div>
</body></html>'''

out = os.path.join(LAB, "names.html")
open(out, "w").write(html)
print("written:", out, os.path.getsize(out) // 1024, "KB")
for n in NAMES:
    icons = sum(1 for i in range(1, 11) if os.path.exists(os.path.join(LAB, f"{n['slug']}-{i}.png")))
    print(f"{n['slug']}: {icons} icons")
