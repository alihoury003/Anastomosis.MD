#!/usr/bin/env python3
"""Rebuild logo-lab/finalists.html in the OLD PAL's exact roster.html design.
- CSS cloned verbatim from his /tmp/arena-coding-uploads/roster.html
- Card anatomy identical (Instagram mock / product bar / size ladder / browser tab / note)
- v4a + v4b: the original uploaded files, re-encoded as JPEG data URIs (his technique)
- v2a/v2d/v2e: regenerated marks (no originals exist in this session)
- v5: generated from the original v4a (edit)
- Reference strip: the 7 original shortlist marks, byte-exact from his roster
"""
import base64, io, os, re
from PIL import Image

LAB = "/home/user/Medchanic.md/logo-lab"
SRC = "/tmp/arena-coding-uploads/roster.html"

src = open(SRC).read()
style = re.search(r"<style>(.*?)</style>", src, re.S).group(1)
# drop his old image vars + classes; we regenerate them
style = re.sub(r"(\s*--mk_[a-z0-9]+:url\(\"data:image/[a-z]+;base64,)[A-Za-z0-9+/=]+(\"\);?)+", "", style)
style = re.sub(r"\n\.mk_[a-z0-9]+\{background-image:var\(--mk_[a-z0-9]+\)\}", "", style)

def jpeg_uri(path, size=420, q=90):
    im = Image.open(path).convert("RGB").resize((size, size), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=q, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()

FIN = [
    ("v2a", "The wave — flat bell", "V2A", "The original: one calm line, two turns, flat ring bell. The one you called \u2018absolutely crushed it\u2019."),
    ("v2d", "The heartbeat — two colours", "V2D", "Coral rises into the spike, teal falls away. The only two-colour mark left in the running."),
    ("v2e", "The heartbeat — one ink", "V2E", "Same geometry, single teal. One ink, one favicon, one embroidery, one print."),
    ("v4a", "The heartbeat — drum bell", "V4A", "Candidate 3\u2019s drum bell on the heartbeat \u2014 the bell, exactly, from the original file."),
    ("v4b", "The heartbeat — twin drums", "V4B", "Bell and socket as a matched pair of machined parts, in the same perspective."),
    ("v5",  "The wave — drum bell", "V5", "The owed one: the wave you loved, carrying the drum bell. Calm body, sculpted head."),
]

vars_css, classes_css = [], []
for key, *_ in FIN:
    vars_css.append(f'  --mk_{key}:url("{jpeg_uri(os.path.join(LAB, key + ".png"))}");')
    classes_css.append(f".mk_{key}{{background-image:var(--mk_{key})}}")

# original shortlist marks, byte-exact from his roster
ORIG = [("mk_1","1"),("mk_2c","2C"),("mk_3","3"),("mk_3e","3E"),("mk_4m","4M"),("mk_4bm","4B-M"),("mk_4cm","4C-M")]
for var, _ in ORIG:
    m = re.search(r'--' + var + r':url\("(data:image/jpeg;base64,[A-Za-z0-9+/=]+)"\)', src)
    vars_css.append(f'  --{var}:url("{m.group(1)}");')
    classes_css.append(f".{var}{{background-image:var(--{var})}}")

cards = []
for key, title, num, note in FIN:
    cards.append(f'''  <article class="card">
    <div class="chead"><h2>{title}</h2><span class="num">{num}</span></div>
    <div class="two">
      <div class="cell">
        <div class="lbl">Instagram</div>
        <div class="ig">
          <div class="igh">&larr; <b>medchanic.md</b></div>
          <div class="igb"><div class="av mk_{key}"></div>
            <div class="igm"><b>Medchanic.MD</b><span><b>2</b> posts &nbsp; <b>1,204</b> followers</span></div></div>
          <div class="igbio"><b>Medchanic.MD</b><br>Mechanism-first exam prep</div>
          <div class="igp mk_{key}"></div>
        </div>
      </div>
      <div class="cell">
        <div class="lbl">Product bar</div>
        <div class="nav"><i class="mk mk_{key}"></i><b>Medchanic</b><em>MD</em><span class="st">11-day streak</span></div>
        <div class="lbl">Size ladder</div>
        <div class="ladder"><i class="lg mk_{key}" style="width:54px;height:54px"></i><i class="lg mk_{key}" style="width:40px;height:40px"></i><i class="lg mk_{key}" style="width:30px;height:30px"></i><i class="lg mk_{key}" style="width:21px;height:21px"></i><i class="lg mk_{key}" style="width:15px;height:15px"></i></div>
        <div class="lbl">Browser tab</div>
        <div class="tabs">
          <div class="tab on"><i class="ti mk_{key}"></i><span>Medchanic &mdash; ev&hellip;</span></div>
          <div class="tab"><i class="ti mk_{key}"></i><span>Dashboard</span></div>
        </div>
        <div class="tabbar"><div class="addr">medchanic-md.appwrite.network</div></div>
      </div>
    </div>
    <div class="note">{note}</div>
  </article>''')

orig_strip = "".join(
    f'<div class="refitem"><i class="lg {var}" style="width:54px;height:54px"></i><span>{label}</span></div>'
    for var, label in ORIG)

html = f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Finalists — Medchanic mark</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Instrument+Serif:ital@0;1&family=JetBrains+Mono:wght@400;600;700&display=swap" rel="stylesheet">
<style>{style}
{chr(10).join(classes_css)}
.refwrap{{margin-top:26px;max-width:1240px}}
.refgrid{{display:flex;flex-wrap:wrap;gap:16px;align-items:flex-start;background:var(--card);border:1px solid var(--rule);border-radius:14px;padding:16px 18px}}
.refitem{{display:flex;flex-direction:column;align-items:center;gap:7px}}
.refitem span{{font-family:var(--mono);font-size:8px;letter-spacing:.12em;color:var(--ink3);font-weight:700}}
</style></head><body>
<h1>Finalists</h1>
<p class="sub">6 marks &middot; instagram &middot; product bar &middot; size ladder &middot; browser tab</p>
<div class="grid">
{chr(10).join(cards)}
</div>
<div class="refwrap">
  <p class="sub" style="margin-bottom:10px">The shortlist they came from &middot; original files, byte-exact</p>
  <div class="refgrid">{orig_strip}</div>
</div>
<p class="sub" style="margin-top:22px">v4a &middot; v4b &mdash; the original files &nbsp;/&nbsp; v2a &middot; v2d &middot; v2e &mdash; regenerated from the original specs &nbsp;/&nbsp; v5 &mdash; born from v4a</p>
<p class="sub" style="margin-top:8px">say the name &mdash; v2a &middot; v2d &middot; v2e &middot; v4a &middot; v4b &middot; v5 &mdash; and it&rsquo;s decided</p>
</body></html>'''

# splice in the image vars right after :root{ opening
html = html.replace(":root{\n", ":root{\n" + "\n".join(vars_css) + "\n", 1)

out = os.path.join(LAB, "finalists.html")
open(out, "w").write(html)
print("written:", out, os.path.getsize(out) // 1024, "KB")
