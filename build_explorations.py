#!/usr/bin/env python3
"""Build logo-lab/explorations.html — five new challenger marks in the old pal's roster design.
cad-1/2: caduceus with stethoscope + wrench (reference: current site mark)
evo-1/2: current site mark made premium/modern/abstract
evo-3:   V4B elevated (reference: original v4b)
"""
import base64, io, os, re
from PIL import Image

LAB = "/home/user/Medchanic.md/logo-lab"
STYLE_SRC = os.path.join(LAB, "picks.html")  # persisted clone of his roster CSS

MARKS = [
    ("cad-1", "Caduceus — one ink", "CAD-1", "The staff is the wrench; the serpents are the tubes — one ends in the bell, the other in the earpieces. The caduceus, told with our two tools."),
    ("cad-2", "Caduceus — two inks", "CAD-2", "Same myth, looser hand: the tubes cross twice in a calligraphic double-S. Teal for the tool, coral for the tubes."),
    ("cad-3", "Caduceus — eartip heads, two inks", "CAD-3", "The ask, delivered: eartips as the serpent heads facing each other, tubes as the bodies coiling the staff, Y-junction and bell as the merged tail. One honest stethoscope, one true caduceus."),
    ("cad-4", "Caduceus — eartip heads, one ink", "CAD-4", "The same mark in a single teal — one ink for the whole myth."),
    ("cad-5", "Single serpent — with wings, two inks", "CAD-5", "One stethoscope alone coils the staff: Y-junction and eartips as the forked head, bell as the tail. No creature anatomy — hardware only. Caduceus wings kept."),
    ("cad-6", "Single serpent — Asclepius, two inks", "CAD-6", "The wings removed. The rod of Asclepius, told with a wrench and one honest stethoscope."),
    ("cad-7", "Single serpent — Asclepius, one ink", "CAD-7", "The same pure rod in a single teal — the premium one-ink move."),
    ("evo-1", "Abstract — one ink", "EVO-1", "The current mark, reduced to its gesture. What survives at 16 px is what mattered all along."),
    ("evo-2", "Abstract — two inks", "EVO-2", "The same reduction in two inks — teal structure, coral coils."),
    ("evo-3", "Abstract — the heartbeat, elevated", "EVO-3", "V4B at its most sculptural: twin machined drums, one confident line, spike compressed for favicon size."),
]

src = open(STYLE_SRC).read()
style = re.search(r"<style>(.*?)</style>", src, re.S).group(1)
# strip ALL image vars + their classes (keep the base .mk/.lg/.ti rules)
style = re.sub(r'\s*--[a-z0-9_]+:url\("data:image/[a-z]+;base64,[A-Za-z0-9+/=]+"\);?', "", style)
style = re.sub(r"\n\.[a-z0-9_]+\{background-image:var\(--[a-z0-9_]+\)\}", "", style)

def jpeg_uri(path, size=440, q=90):
    im = Image.open(path).convert("RGB").resize((size, size), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=q, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()

vars_css = [f'  --{k}:url("{jpeg_uri(os.path.join(LAB, k + ".png"))}");' for k, *_ in MARKS]
classes_css = [f".{k}{{background-image:var(--{k})}}" for k, *_ in MARKS]

def card(var, title, num, note):
    return f'''  <article class="card">
    <div class="chead"><h2>{title}</h2><span class="num">{num}</span></div>
    <div class="two">
      <div class="cell">
        <div class="lbl">Instagram</div>
        <div class="ig">
          <div class="igh">&larr; <b>medchanic.md</b></div>
          <div class="igb"><div class="av {var}"></div>
            <div class="igm"><b>Medchanic.MD</b><span><b>2</b> posts &nbsp; <b>1,204</b> followers</span></div></div>
          <div class="igbio"><b>Medchanic.MD</b><br>Mechanism-first exam prep</div>
          <div class="igp {var}"></div>
        </div>
      </div>
      <div class="cell">
        <div class="lbl">Product bar</div>
        <div class="nav"><i class="mk {var}"></i><b>Medchanic</b><em>MD</em><span class="st">11-day streak</span></div>
        <div class="lbl">Size ladder</div>
        <div class="ladder"><i class="lg {var}" style="width:54px;height:54px"></i><i class="lg {var}" style="width:40px;height:40px"></i><i class="lg {var}" style="width:30px;height:30px"></i><i class="lg {var}" style="width:21px;height:21px"></i><i class="lg {var}" style="width:15px;height:15px"></i></div>
        <div class="lbl">Browser tab</div>
        <div class="tabs">
          <div class="tab on"><i class="ti {var}"></i><span>Medchanic &mdash; ev&hellip;</span></div>
          <div class="tab"><i class="ti {var}"></i><span>Dashboard</span></div>
        </div>
        <div class="tabbar"><div class="addr">medchanic-md.appwrite.network</div></div>
      </div>
    </div>
    <div class="note">{note}</div>
  </article>'''

cards = [card(k, t, n, note) for k, t, n, note in MARKS]

html = f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>New blood — Medchanic mark</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Instrument+Serif:ital@0;1&family=JetBrains+Mono:wght@400;600;700&display=swap" rel="stylesheet">
<style>{style}
{chr(10).join(classes_css)}
</style></head><body>
<h1>New blood</h1>
<p class="sub">5 marks &middot; instagram &middot; product bar &middot; size ladder &middot; browser tab</p>
<div class="grid">
{chr(10).join(cards)}
</div>
<p class="sub" style="margin-top:22px">cad-1 &middot; cad-2 &middot; evo-1 &middot; evo-2 &mdash; born from the current site mark &nbsp;/&nbsp; evo-3 &mdash; born from v4b &nbsp;/&nbsp; cad-3 cad-3 &middot; cad-4 &mdash; cad-2 refined: eartips as headsmiddot; cad-4 cad-3 &middot; cad-4 &mdash; cad-2 refined: eartips as headsmdash; cad-2 refined cad-3 &middot; cad-4 &mdash; cad-2 refined: eartips as headsnbsp;/cad-3 &middot; cad-4 &mdash; cad-2 refined: eartips as headsnbsp; cad-5 cad-3 &middot; cad-4 &mdash; cad-2 refined: eartips as headsmiddot; cad-6 cad-3 &middot; cad-4 &mdash; cad-2 refined: eartips as headsmiddot; cad-7 cad-3 &middot; cad-4 &mdash; cad-2 refined: eartips as headsmdash; single serpent, hardware only</p>
<p class="sub" style="margin-top:8px">challengers to the five picks &mdash; say any name and it enters the race</p>
</body></html>'''

html = html.replace(":root{\n", ":root{\n" + "\n".join(vars_css) + "\n", 1)
out = os.path.join(LAB, "explorations.html")
open(out, "w").write(html)
print("written:", out, os.path.getsize(out) // 1024, "KB")

# ---- technical verification ----
TEAL, CREAM, CORAL = (14, 124, 120), (243, 239, 230), (228, 87, 46)
def close(a, b, tol=40): return all(abs(x - y) <= tol for x, y in zip(a, b))
for k, *_ in MARKS:
    p = os.path.join(LAB, k + ".png")
    im = Image.open(p).convert("RGB")
    w, h = im.size
    px = im.load()
    corners = [px[3, 3], px[w - 4, 3], px[3, h - 4], px[w - 4, h - 4]]
    small = im.resize((96, 96))
    data = list(small.getdata())
    teal = sum(1 for c in data if close(c, TEAL))
    coral = sum(1 for c in data if close(c, CORAL))
    tot = len(data)
    print(f"{k}.png  {w}x{h}  bg_cream={all(close(c, CREAM, 30) for c in corners)}  teal={100*teal//tot}%  coral={100*coral//tot}%  {os.path.getsize(p)//1024}KB")
